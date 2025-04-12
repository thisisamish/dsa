import requests
import re
import json
from bs4 import BeautifulSoup
from utils.enums import ProblemPlatform
from typing import List

def get_he_id_title_from_url(url: str) -> List[str]:
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"HackerEarth: Request failed with status {response.status_code} for url: {url}. Response: {response.text}")
    if not response.text.strip():
        raise Exception(f"HackerEarth: Empty response for url: {url}")

    try:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup.find_all('script'):
            if script.string and 'var initial_state =' in script.string:
                script_text = script.string
                match = re.search(r'var initial_state\s*=\s*({.*?})\s*[\n;]', script_text, re.DOTALL)
                if not match:
                    raise Exception(f"HackerEarth: initial_state object not found in the script for url: {url}")
                
                js_object = match.group(1)

                def quote_keys(js):
                    # Avoid quoting already quoted keys (e.g., "key":)
                    return re.sub(r'(?<=\{|,)\s*(\w+)\s*:', r'"\1":', js)

                json_like = quote_keys(js_object)
                try:
                    raw = json.loads(json_like)
                    return [str(raw['problemData']['id']) + ProblemPlatform.HACKEREARTH, raw['problemData']['title']]
                except json.JSONDecodeError as e:
                    raise Exception(f"HackerEarth: JSON decode failed for url: {url}. Error: {e}. Extracted JSON: {json_like[:300]}...")
        
        raise Exception(f"HackerEarth: Could not find the target <script> tag in the HTML for url: {url}")
    
    except Exception as e:
        raise Exception(f"HackerEarth: Error while parsing response for url: {url}. Raw response: {response.text[:300]}...") from e


def get_hr_id_title_from_url(url: str) -> List[str]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"HackerRank: Request failed with status {response.status_code} for url: {url}. Response: {response.text}")
        
        # Check if the response body is empty
        if not response.text.strip():
            raise Exception(f"HackerRank: Empty response for url: {url}")

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Extract the title from the <title> tag
        title = soup.title.string.split('|')[0].strip() if soup.title else None
        if not title:
            raise Exception(f"HackerRank: Title not found in the <title> tag for url: {url}")

        # Extract the ID from the URL using regex
        id = ""
        pattern = r"https://www\.hackerrank\.com/challenges/([a-z0-9-]+)"
        match = re.search(pattern, url)
        if match:
            id = match.group(1) + ProblemPlatform.HACKERRANK
        else:
            raise ValueError(f"HackerRank: Invalid URL or slug format for url: {url}")

        return [id, title]
    
    except Exception as e:
        raise Exception(f"HackerRank: Error while processing url: {url}. Error: {str(e)}") from e

