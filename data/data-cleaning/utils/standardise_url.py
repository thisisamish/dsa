from urllib.parse import urlparse, urlunparse
import aiohttp
import asyncio
import json
import os
from functools import partial
from tqdm.asyncio import tqdm_asyncio
import time
import pandas as pd


from utils.enums import ProblemPlatform
from utils.url2platform import *




def strip_query_params(url: str) -> str:
    parsed = urlparse(url)
    clean_url = urlunparse(parsed._replace(query="", fragment=""))
    return clean_url


def _load_checkpoint(checkpoint_file):
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
    return {}


def _save_checkpoint(checkpoint_file, results):
    with open(checkpoint_file, 'w') as f:
        json.dump(results, f)
    print(f"Progress saved to {checkpoint_file}")
    print("-"*70)


async def _identity_pair(idx, url):
    return idx, url


async def _process_batch(batch_data, max_concurrent, checkpoint_file, filter_list: list[str]):
    # Create a semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(max_concurrent)
    
    # Load any existing checkpoint data
    existing_results = _load_checkpoint(checkpoint_file)
    print(f"Loaded {len(existing_results)} results from checkpoint")
    
    # Filter batch to exclude already processed URLs
    pending_batch = [(idx, url) for idx, url in batch_data if str(idx) not in existing_results]
    
    if not pending_batch:
        print("All URLs in this batch have already been processed")
        return existing_results
    
    print(f"Processing {len(pending_batch)} pending URLs in this batch")
    
    # Process the pending URLs
    conn = aiohttp.TCPConnector(limit=max_concurrent)
    async with aiohttp.ClientSession(connector=conn) as session:
        # Create a partial function with the session and semaphore
        expand_func = partial(expand_url, session, semaphore=semaphore, max_retries=3, filter_list=filter_list)
        
        # Use tqdm to show progress
        tasks = []
        for url_data in pending_batch:
            idx, url = url_data
            if should_be_expanded(url, filter_list):
                # Add a small delay between creating tasks to avoid hammering the server
                await asyncio.sleep(0.01)
                tasks.append(expand_func(url_data))
            else:
                tasks.append(asyncio.create_task(_identity_pair(idx, url)))
        
        # Execute all tasks with progress bar
        results = await tqdm_asyncio.gather(*tasks, desc="Expanding URLs")
        
        # Convert results to dictionary and merge with existing results
        batch_results = {str(idx): url for idx, url in results}
        combined_results = {**existing_results, **batch_results}
        
        # Save checkpoint
        _save_checkpoint(checkpoint_file, combined_results)
        
        return combined_results


async def _expand_urls(
        urls: list[str],
        batch_size: int,
        max_concurrent: int, 
        checkpoint_file: str,
        filter_list: list[str]
):
    # Create index-URL pairs
    url_data = list(enumerate(urls))
    total_urls = len(url_data)
    
    # Process in batches
    all_results = _load_checkpoint(checkpoint_file)
    
    for i in range(0, total_urls, batch_size):
        batch = url_data[i:i+batch_size]
        print(f"\nProcessing batch {i//batch_size + 1}/{(total_urls + batch_size - 1)//batch_size}")
        
        # Process this batch
        batch_results = await _process_batch(batch, max_concurrent, checkpoint_file, filter_list)
        all_results.update(batch_results)
        
        # Save overall progress after each batch
        _save_checkpoint(checkpoint_file, all_results)
    
    # Convert results back to a list in original order
    expanded_urls = [all_results.get(str(i), url) for i, url in enumerate(urls)]
    return expanded_urls


def should_be_expanded(url, filter_list: list[str]) -> bool:
    if len(filter_list) == 0:
        return True
    for item in filter_list:
        if url in item:
            return True
    return False


async def expand_url(session, url_data: tuple[int, str], semaphore, max_retries: int, filter_list: list[str]) -> tuple[int, str]:
    index, short_url = url_data
    
    if not should_be_expanded(short_url, filter_list):
        return index, short_url

    for attempt in range(max_retries):
        try:
            # Use semaphore to limit concurrent requests
            async with semaphore:
                # Set headers and timeout for the request
                headers = {
                    'User-Agent': 'python-requests/2.32.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept': '*/*',
                    'Connection': 'keep-alive',
                }
                # Use a context manager for the request
                async with session.head(short_url, 
                                    allow_redirects=True, 
                                    headers=headers, 
                                    timeout=aiohttp.ClientTimeout(total=10)) as response:
                    # Return the final URL after redirects
                    return index, str(response.url)
        except Exception as e:
            print(f"Attempt {attempt+1} (HEAD) failed for {short_url}: {e}")
            await asyncio.sleep(1)  # brief pause before retrying
    
    print(f"Failed to expand {short_url} after {max_retries} attempts for HEAD.")
    return index, short_url


async def standardise_urls_async(
        df: pd.DataFrame,
        checkpoint_file: str,
        url_column: str = 'url',
        batch_size: int = 200,
        max_concurrent: int = 100,
        resume: bool = False,
        filter_list: list[str] = [],
    ) -> pd.DataFrame:
    """
    Expands shortened URLs and then strips query params from them in a pandas DataFrame using concurrent
    HTTP requests with checkpointing and batching support.

    This function processes the column containing URLs of the input DataFrame, expands each URL to its final 
    destination, and adds a new column 'expanded_url'. It supports batching and concurrency to 
    improve performance, and checkpointing to allow resuming from the last saved state in case 
    of interruption.

    Parameters
    ----------
    df : pd.DataFrame
        A pandas DataFrame containing a 'url' column with shortened or redirecting URLs.
    checkpoint_file : str
        Path to a checkpoint file used for saving intermediate results and resuming progress.
    batch_size : int, optional
        Number of URLs to process in each batch (default is 200).
    url_column : str, optional
        The column name which contains the URLs (default is 'url').
    max_concurrent : int, optional
        Maximum number of concurrent URL expansion operations (default is 100).
    resume : bool, optional
        Whether to resume processing from the checkpoint file if it exists (default is False).

    Returns
    -------
    pd.DataFrame
        The input DataFrame with an additional column 'expanded_url' containing the final resolved URLs.
    """
    urls = df[url_column].tolist()
    
    to_be_expanded_count = 0
    if len(filter_list) == 0:
        to_be_expanded_count = len(urls)
        print(f"Filter list is empty. Trying to expand all {to_be_expanded_count} URLs.")
    else:
        to_be_expanded_count = sum(should_be_expanded(url, filter_list) for url in urls)
        print(f"Found {to_be_expanded_count} shortened URLs out of {len(urls)} total URLs.")
    
    # Delete checkpoint file if not resuming
    if not resume and os.path.exists(checkpoint_file):
        print(f"Resume option is set to false. Deleted previous checkpoint file: {checkpoint_file}")
        os.remove(checkpoint_file)
    
    # Process the URLs asynchronously with batching and checkpointing
    start_time = time.time()
    expanded_urls = await _expand_urls(urls, batch_size, max_concurrent, checkpoint_file, filter_list)
    end_time = time.time()
    
    print(f"\n{to_be_expanded_count}/{len(urls)} URLs expanded in {end_time - start_time:.2f} seconds.")
    
    df = df.copy()
    df['expanded_url'] = expanded_urls
    df['expanded_stripped_url'] = df['expanded_url'].apply(
        lambda url: strip_query_params(url) if is_problem_url(url) else url
    )
    return df