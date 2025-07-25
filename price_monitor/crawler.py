import requests
from requests.exceptions import HTTPError
from playwright.sync_api import sync_playwright, Error as PWError


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
            except PWError as pw_err:
                # Playwright 브라우저가 설치되지 않은 경우 가이드 메시지 출력
                msg = str(pw_err)
                if "Executable doesn't exist" in msg:
                    raise RuntimeError(
                        "Playwright 브라우저 실행 파일을 찾을 수 없습니다.\n"
                        "환경에서 'playwright install' 명령을 실행해 브라우저를 설치해 주세요."
                    )
                raise RuntimeError(f"Playwright error: {pw_err}")
        raise RuntimeError(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise RuntimeError(f"Other error occurred: {err}")
