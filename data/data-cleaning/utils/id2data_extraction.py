import requests
from typing import List
from utils.enums import ProblemPlatform


def get_lint_id_title_from_id(id: str) -> List[str]:
    url = f"https://apiv1.lintcode.com/v2/api/problems/{id}/?lang=2"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"LintCode: Request failed with status {response.status_code} for id: {id}. Response: {response.text}")
    if not response.text.strip():
        raise Exception(f"LintCode: Empty response for id: {id}")

    try:
        data = response.json()
    except Exception as e:
        raise Exception(f"LintCode: JSON decode error for id: {id}. Raw response: {response.text}") from e

    return [
        str(data["data"]["id"]).strip() + ProblemPlatform.LINTCODE,
        data["data"]["title"].strip()
    ]
