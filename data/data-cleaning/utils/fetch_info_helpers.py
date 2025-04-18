import requests
from typing import List
from utils.enums import ProblemPlatform
import aiohttp
import re
import json
from bs4 import BeautifulSoup


async def get_lint_id_title_from_slug_async(session: aiohttp.ClientSession, id: str) -> List[str]:
    url = f"https://apiv1.lintcode.com/v2/api/problems/{id}/?lang=2"
    async with session.get(url) as response:
        text = await response.text()
        if response.status != 200 or not text.strip():
            raise Exception(f"LintCode: Request failed ({response.status}) or empty for id: {id}. Response: {text}")
        data = await response.json()
        return [
            str(data["data"]["id"]).strip() + ProblemPlatform.LINTCODE,
            data["data"]["title"].strip()
        ]


async def get_he_id_title_from_url_async(session: aiohttp.ClientSession, url: str) -> List[str]:
    async with session.get(url) as response:
        text = await response.text()
        if response.status != 200 or not text.strip():
            raise Exception(f"HackerEarth: Request failed ({response.status}) or empty for url: {url}. Response: {text}")
        soup = BeautifulSoup(text, 'html.parser')
        for script in soup.find_all('script'):
            if script.string and 'var initial_state =' in script.string:
                match = re.search(r'var initial_state\s*=\s*({.*?})\s*[\n;]', script.string, re.DOTALL)
                if not match:
                    raise Exception(f"HackerEarth: initial_state not found in JS for url: {url}")
                js_object = match.group(1)
                json_like = re.sub(r'(?<=\{|,)\s*(\w+)\s*:', r'"\1":', js_object)
                raw = json.loads(json_like)
                return [
                    str(raw['problemData']['id']) + ProblemPlatform.HACKEREARTH,
                    raw['problemData']['title']
                ]
        raise Exception(f"HackerEarth: Could not find script tag for url: {url}")
    

async def get_hr_id_title_from_url_async(session: aiohttp.ClientSession, url: str) -> List[str]:
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'text/html',
    }
    async with session.get(url, headers=headers) as response:
        text = await response.text()
        if response.status != 200 or not text.strip():
            raise Exception(f"HackerRank: Request failed ({response.status}) or empty for url: {url}. Response: {text}")
        soup = BeautifulSoup(text, 'html.parser')
        title = soup.title.string.split('|')[0].strip() if soup.title else None
        match = re.search(r"https://www\.hackerrank\.com/challenges/([a-z0-9-]+)", url)
        if not match:
            raise Exception(f"HackerRank: Invalid slug in url: {url}")
        return [match.group(1) + ProblemPlatform.HACKERRANK, title]
    

async def get_lc_id_title_from_slug_async(session: aiohttp.ClientSession, slug: str) -> List[str]:
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

    async with session.post(url, json={"query": query, "variables": variables}, headers=headers) as response:
        text = await response.text()
        if response.status != 200 or not text.strip():
            raise Exception(f"LeetCode: Request failed ({response.status}) or empty for slug: {slug}. Response: {text}")
        data = await response.json()
        return [
            data['data']['question']['questionFrontendId'].strip() + ProblemPlatform.LEETCODE,
            data['data']['question']['title'].strip()
        ]
    

async def get_gfg_id_title_from_slug_async(session: aiohttp.ClientSession, slug: str) -> List[str]:
    url = f"https://practiceapi.geeksforgeeks.org/api/latest/problems/{slug}"
    async with session.get(url) as response:
        text = await response.text()
        if response.status != 200 or not text.strip():
            raise Exception(f"GFG: Request failed ({response.status}) or empty for slug: {slug}. Response: {text}")
        data = await response.json()
        return [
            str(data['results']['id']).strip() + ProblemPlatform.GFG,
            data['results']['problem_name'].strip()
        ]
    

async def get_c360_id_title_from_slug_async(session: aiohttp.ClientSession, slug: str) -> List[str]:
    url = f"https://www.naukri.com/code360/api/v3/public_section/problem_detail?slug={slug}"
    headers = {
        'User-Agent': 'python-requests/2.32.3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }
    async with session.get(url, allow_redirects=True, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
        text = await response.text()
        if response.status != 200 or not text.strip():
            raise Exception(f"Code360: Request failed ({response.status}) or empty for slug: {slug}. Response: {text}")
        data = await response.json()
        return [
            str(data["data"]["offerable"]["problem"]["id"]).strip() + ProblemPlatform.CODE360,
            data["data"]["offerable"]["problem"]["name"].strip()
        ]


async def get_ib_id_title_from_slug_async(session: aiohttp.ClientSession, slug: str) -> List[str]:
    url = f"https://www.interviewbit.com/v2/problems/{slug}"
    async with session.get(url) as response:
        text = await response.text()
        if response.status != 200 or not text.strip():
            raise Exception(f"InterviewBit: Request failed ({response.status}) or empty for slug: {slug}. Response: {text}")
        data = await response.json()
        return [
            str(data["id"]).strip() + ProblemPlatform.INTERVIEWBIT,
            data["meta"]["statement"].strip()
        ]
    

async def get_spoj_id_title_from_slug_async(session: aiohttp.ClientSession, slug: str) -> List[str]:
    url = f"https://www.spoj.com/problems/{slug}/"
    async with session.get(url) as response:
        text = await response.text()
        if response.status != 200 or not text.strip():
            raise Exception(f"SPOJ: Request failed ({response.status}) or empty for slug: {slug}. Response: {text}")
        match = re.search(r'<h2 id="problem-name"[^>]*>(.*?)</h2>', text)
        if match:
            id, title = match.group(1).split("-", 1)
            return [id.strip() + ProblemPlatform.SPOJ, title.strip()]
        raise Exception(f"SPOJ: Problem name not found for slug: {slug}. HTML: {text[:300]}...")
    
    