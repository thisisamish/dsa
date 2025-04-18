import os
import uuid
import json
import asyncio
import aiohttp
from tqdm.asyncio import tqdm_asyncio
import time
import pandas as pd


from utils.fetch_info_helpers import *
from utils.url2platform import *
from utils.url2slug import *




SEM: asyncio.Semaphore




async def fetch_item_data(session: aiohttp.ClientSession, url: str, item_type: str) -> dict[str, str]:
    """
    Fetch the metadata for either a problem or a tutorial URL.
    For tutorials, we only fetch id & platform; title fetching functionality is yet to be written.
    """
    if item_type == "problem":
        return await fetch_problem_data(session, url)
    elif item_type == "tutorial":
        return await fetch_tutorial_data(session, url)
    else:
        raise ValueError(f"Unknown item type: {item_type}")
    

async def fetch_tutorial_data(session: aiohttp.ClientSession, url: str) -> dict[str, str]:
    # derive platform & slug
    platform = tutorial_url2platform(url).value
    slug = tutorial_url2slug(url)

    # generate a reproducible UUID-based id
    tutorial_id = f"{uuid.uuid5(uuid.NAMESPACE_DNS, slug)}{platform}"
    title = ""

    try:
        headers = {
            'User-Agent': 'python-requests/2.32.3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Connection': 'keep-alive',
        }
        async with session.get(url, 
                            allow_redirects=True, 
                            headers=headers, 
                            timeout=aiohttp.ClientTimeout(total=10)) as response:
            html = await response.text()
            match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
            if match:
                title = match.group(1).strip()
    except Exception as e:
            print(f"Error fetching {url}: {e}")

    return {
        "id_base": slug,
        "id": tutorial_id,
        "title": title,
        "platform": platform,
    }
        

async def fetch_problem_data(session: aiohttp.ClientSession, url: str) -> dict[str, str] | None:
    async with SEM:
        try:
            platform = problem_url2platform(url)
            slug = problem_url2slug(url, platform)

            platform_function_map = {
                ProblemPlatform.LEETCODE: get_lc_id_title_from_slug_async,
                ProblemPlatform.GFG: get_gfg_id_title_from_slug_async,
                ProblemPlatform.CODE360: get_c360_id_title_from_slug_async,
                ProblemPlatform.INTERVIEWBIT: get_ib_id_title_from_slug_async,
                ProblemPlatform.SPOJ: get_spoj_id_title_from_slug_async,
                ProblemPlatform.HACKEREARTH: get_he_id_title_from_url_async,
                ProblemPlatform.HACKERRANK: get_hr_id_title_from_url_async,
                ProblemPlatform.LINTCODE: get_lint_id_title_from_slug_async,
            }

            fetch_fn = platform_function_map.get(platform)
            if not fetch_fn:
                raise ValueError(f"Unsupported platform: {platform}")

            # Some platforms expect a slug, others a URL
            param = slug if "slug" in fetch_fn.__name__ else url
            id, title = await fetch_fn(session, param)

            return {
                "id_base": slug,
                "id": id,
                "title": title,
                "platform": platform,
            }

        except Exception as e:
            print(f"❌ Failed for URL: {url}\nError: {e}")
            return None


def _load_checkpoint(checkpoint_file: str) -> dict[str, dict[str, str]]:
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
    return {}


def _save_checkpoint(checkpoint_file: str, results: dict[str, dict[str, str]]) -> None:
    with open(checkpoint_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved progress ({len(results)} items) to {checkpoint_file}")
    print("-"*30)


async def _process_batch(
        batch_data: list[tuple[int, str, str]], 
        max_concurrent: int, 
        checkpoint_file: str
) -> dict[str, dict[str, str]]:
    # Reset the global SEM so fetch_problem_data uses this limit
    global SEM
    SEM = asyncio.Semaphore(max_concurrent)

    # Load existing
    existing = _load_checkpoint(checkpoint_file)
    print(f"Loaded {len(existing)} from checkpoint")

    # Filter out already‑done
    pending = [(i, url, item_type) for i, url, item_type in batch_data if str(i) not in existing]
    if not pending:
        print("Nothing new in this batch")
        return existing

    print(f"Processing {len(pending)} URLs...")

    connector = aiohttp.TCPConnector(limit=max_concurrent)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Wrap fetch to return (idx, result_dict)
        async def _wrap(idx_url_type):
            idx, url, item_type = idx_url_type
            result = await fetch_item_data(session, url, item_type)
            return idx, result

        tasks: list[asyncio.Task] = [_wrap(item) for item in pending]
        done: list[tuple[int, dict[str, str] | None]] = await tqdm_asyncio.gather(*tasks, desc="Fetching items")

    # Merge results (skip failures where result is None)
    batch_results: dict[str, dict[str, str]] = {
        str(idx): res for idx, res in done if res is not None
    }
    combined = {**existing, **batch_results}
    _save_checkpoint(checkpoint_file, combined)
    return combined


async def _process_all(
        indices_urls_types: list[tuple[int, str, str]],
        batch_size: int,
        max_concurrent: int,
        checkpoint_file: str
) -> dict[str, dict[str, str]]:
    all_results = _load_checkpoint(checkpoint_file)

    total_batches = (len(indices_urls_types) + batch_size - 1) // batch_size
    for b in range(total_batches):
        start = b * batch_size
        batch = indices_urls_types[start:start + batch_size]
        print(f"\nBatch {b+1}/{total_batches}: items {start}-{start+len(batch)-1}")
        batch_results = await _process_batch(batch, max_concurrent, checkpoint_file)
        all_results.update(batch_results)
        _save_checkpoint(checkpoint_file, all_results)

    return all_results


async def fetch_info(
    df: pd.DataFrame,
    progress_file: str,
    url_column: str = 'expanded_stripped_url',
    type_column: str = 'type',
    batch_size: int = 200,
    max_concurrent: int = 100,
    resume: bool = False
) -> pd.DataFrame:
    """
    Asynchronously fetch problem ID, title, and platform for each URL in a DataFrame.

    This function processes problem URLs from a specified DataFrame column in batches,
    concurrently fetching details for each problem, with JSON checkpointing support to
    resume interrupted runs.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing problem URLs.
    progress_file : str
        Path to the JSON file used for saving and loading progress checkpoints.
    url_column : str, optional
        Name of the DataFrame column containing problem URLs
        (default is 'expanded_stripped_url').
    batch_size : int, optional
        Number of URLs to process in each batch
        (default is 200).
    max_concurrent : int, optional
        Maximum number of concurrent fetch operations
        (default is 100).
    resume : bool, optional
        Whether to resume from an existing checkpoint file if found.
        If False and the file exists, it will be deleted.
        (default is False).

    Returns
    -------
    pandas.DataFrame
        A copy of the input DataFrame with three new columns added:
        - **id** : str or None
            Fetched problem ID (or None if fetch failed).
        - **title** : str or None
            Fetched problem title (or None if fetch failed).
        - **platform** : str or None
            Problem platform identifier (or None if fetch failed).
    """
    urls: list[str] = df[url_column].tolist()
    types: list[str] = df[type_column].tolist()
    pairs: list[tuple[int, str, str]] = list(zip(range(len(urls)), urls, types))
    print(f"Found {len(urls)} URLs.")

    # Handle resume
    if not resume and os.path.exists(progress_file):
        print("Resume is disabled. Deleting old checkpoint...")
        os.remove(progress_file)

    start = time.time()
    results: dict[str, dict[str, str]] = await _process_all(pairs, batch_size, max_concurrent, progress_file)
    duration = time.time() - start
    print(f"\nFetched {len(results)}/{len(urls)} items in {duration:.1f}s.")

    id_bases: list[str | None] = []
    ids: list[str | None] = []
    titles: list[str | None] = []
    platforms: list[str | None] = []

    for i in range(len(urls)):
        entry = results.get(str(i))
        if entry:
            id_bases.append(entry['id_base'])
            ids.append(entry['id'])
            titles.append(entry['title'])
            platforms.append(entry['platform'])
        else:
            id_bases.append(None)
            ids.append(None)
            titles.append(None)
            platforms.append(None)

    df = df.copy()
    df['id_base'] = id_bases
    df['id'] = ids
    df['title'] = titles
    df['platform'] = platforms

    return df