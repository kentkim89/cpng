from price_monitor.config import PRODUCT_URLS
from price_monitor.crawler import fetch_page
from price_monitor.parser import parse_price
from price_monitor.storage import save_price_log


def run_once():
    for url in PRODUCT_URLS:
        html = fetch_page(url)
        price = parse_price(html)
        print(f"[{url}] 현재 가격: {price}원")
        save_price_log(url, price)

if __name__ == '__main__':
    run_once()
