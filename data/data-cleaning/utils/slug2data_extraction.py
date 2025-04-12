import requests
import re
from typing import List
from utils.enums import ProblemPlatform


def get_lc_id_title_from_slug(slug: str) -> List[str]:
    url = "https://leetcode.com/graphql"
    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionFrontendId
        title
      }
    }
    """
    variables = {"titleSlug": slug}
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}: {response.text}")
    if not response.text.strip():
        raise Exception(f"Empty response from LeetCode for slug: {slug}")

    try:
        data = response.json()
    except Exception as e:
        raise Exception(f"Error parsing JSON for slug: {slug}. Raw response: {response.text}") from e

    return [
        data['data']['question']['questionFrontendId'].strip() + ProblemPlatform.LEETCODE,
        data['data']['question']['title'].strip()
    ]


def get_gfg_id_title_from_slug(slug: str) -> List[str]:
    url = f"https://practiceapi.geeksforgeeks.org/api/latest/problems/{slug}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"GFG: Request failed with status {response.status_code} for slug: {slug}. Response: {response.text}")
    if not response.text.strip():
        raise Exception(f"GFG: Empty response for slug: {slug}")

    try:
        data = response.json()
    except Exception as e:
        raise Exception(f"GFG: JSON decode error for slug: {slug}. Raw response: {response.text}") from e

    return [
        str(data['results']['id']).strip() + ProblemPlatform.GFG,
        data['results']['problem_name'].strip()
    ]


def get_c360_id_title_from_slug(slug: str) -> List[str]:
    url = f"https://www.naukri.com/code360/api/v3/public_section/problem_detail?slug={slug}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Code360: Request failed with status {response.status_code} for slug: {slug}. Response: {response.text}")
    if not response.text.strip():
        raise Exception(f"Code360: Empty response for slug: {slug}")

    try:
        data = response.json()
    except Exception as e:
        raise Exception(f"Code360: JSON decode error for slug: {slug}. Raw response: {response.text}") from e

    return [
        str(data["data"]["offerable"]["problem"]["id"]).strip() + ProblemPlatform.CODE360,
        data["data"]["offerable"]["problem"]["name"].strip()
    ]


def get_ib_id_title_from_slug(slug: str) -> List[str]:
    url = f"https://www.interviewbit.com/v2/problems/{slug}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"InterviewBit: Request failed with status {response.status_code} for slug: {slug}. Response: {response.text}")
    if not response.text.strip():
        raise Exception(f"InterviewBit: Empty response for slug: {slug}")

    try:
        data = response.json()
    except Exception as e:
        raise Exception(f"InterviewBit: JSON decode error for slug: {slug}. Raw response: {response.text}") from e

    return [
        str(data["id"]).strip() + ProblemPlatform.INTERVIEWBIT,
        data["meta"]["statement"].strip()
    ]


def get_spoj_id_title_from_slug(slug: str) -> List[str]:
    url = f"https://www.spoj.com/problems/{slug}/"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"SPOJ: Request failed with status {response.status_code} for slug: {slug}. Response: {response.text}")
    if not response.text.strip():
        raise Exception(f"SPOJ: Empty response for slug: {slug}")

    try:
        match = re.search(r'<h2 id="problem-name"[^>]*>(.*?)</h2>', response.text)
        if match:
            id, title = match.group(1).split("-", 1)
            return [id.strip() + ProblemPlatform.SPOJ, title.strip()]
        else:
            raise Exception(f"SPOJ: Could not find problem name in the response HTML for slug: {slug}")
    except Exception as e:
        raise Exception(f"SPOJ: Error while parsing response for slug: {slug}. Raw response: {response.text[:300]}...") from e
    