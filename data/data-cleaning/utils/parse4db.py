from utils.link2data_extraction import *
from utils.id2data_extraction import *
from utils.slug2data_extraction import *
from utils.url2slug import *
from utils.url2platform import *
from tqdm import tqdm
from typing import List, Dict
import uuid


def tutorials_parse4db(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    parsed_data = []
    for index, tutorial in tqdm(enumerate(data), desc="Processing URLs", ncols=100, total=len(data)):
        platform = tutorial_url2platform(tutorial["url"]).value
        slug = tutorial_url2slug(tutorial["url"])
        id = f"{(uuid.uuid5(uuid.NAMESPACE_DNS, slug))}{platform}"

        parsed_data.append({
            "id": id,
            "type": "tutorial",
            "title": tutorial["title"],
            "platform": platform,
            "href": tutorial["url"],
        })
    return parsed_data


def problems_parse4db(data: List[str], progress_file: str = None) -> List[Dict[str, str]]:
    parsed_data = []

    try:
        with open(progress_file, 'r') as f:
            parsed_data = json.load(f)
        print(f"Loaded {len(parsed_data)} previously parsed items.")
    except FileNotFoundError:
        pass  # Start fresh if no progress file

    start_index = len(parsed_data)

    for index, url in tqdm(
        zip(range(start_index, len(data)), data[start_index:]),
        desc="Processing URLs",
        initial=start_index,
        ncols=100,
        total=len(data)
    ):
        try:
            id = ""
            title = ""
            platform = problem_url2platform(url).value
            slug = problem_url2slug(url)

            if platform == "LC":
                [id, title] = get_lc_id_title_from_slug(slug)
            elif platform == "GFG":
                [id, title] = get_gfg_id_title_from_slug(slug)
            elif platform == "C360":
                [id, title] = get_c360_id_title_from_slug(slug)
            elif platform == "IB":
                [id, title] = get_ib_id_title_from_slug(slug)
            elif platform == "SPOJ":
                [id, title] = get_spoj_id_title_from_slug(slug)
            elif platform == "HE":
                [id, title] = get_he_id_title_from_url(url)
            elif platform == "HR":
                [id, title] = get_hr_id_title_from_url(url)
            elif platform == "LINT":
                problem_id = url.strip('/').split('/')[-1]
                [id, title] = get_lint_id_title_from_id(problem_id)
            else:
                raise ValueError(f"ID and title extracting function not defined for {platform}. URL is {url}")

            parsed_data.append({
                "id": id,
                "type": "problem",
                "title": title,
                "platform": platform,
                "href": url,
            })
        except Exception as e:
            # Save progress before raising error
            with open(progress_file, 'w') as f:
                json.dump(parsed_data, f, indent=2)
            print(f"\n❌ Error at index {index}: {url}\n{e}")
            raise  # Reraise the exception after saving state
    
    # Save final progress if all goes well
    with open(progress_file, 'w') as f:
        json.dump(parsed_data, f, indent=2)

    return parsed_data