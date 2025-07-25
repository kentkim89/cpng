import requests
from requests.exceptions import HTTPError

def fetch_page(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.text
    except HTTPError as http_err:
        # 재시도 로직 또는 None 반환으로 에러 처리
        raise RuntimeError(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise RuntimeError(f"Other error occurred: {err}")
