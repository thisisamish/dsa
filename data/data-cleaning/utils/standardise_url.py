import requests
from urllib.parse import urlparse, urlunparse


def expand_url(url: str) -> str:
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url
    except requests.RequestException as e:
        print(f"Error expanding {url}: {e}")
        raise ValueError

def strip_query_params(url: str) -> str:
    parsed = urlparse(url)
    clean_url = urlunparse(parsed._replace(query="", fragment=""))
    return clean_url