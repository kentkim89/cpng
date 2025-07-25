import requests
from requests.exceptions import HTTPError
from playwright.sync_api import sync_playwright


def fetch_page(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    # 먼저 requests 시도
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.text
    except HTTPError as http_err:
        # 403 Forbidden 시 Playwright로 재시도
        if http_err.response.status_code == 403:
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=True,
                        args=["--no-sandbox", "--disable-gpu"]
                    )
                    page = browser.new_page(extra_http_headers=headers)
                    page.goto(url, timeout=15000)
                    content = page.content()
                    browser.close()
                    return content
            except Exception as pw_err:
                raise RuntimeError(f"Playwright error: {pw_err}")
        raise RuntimeError(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise RuntimeError(f"Other error occurred: {err}")
