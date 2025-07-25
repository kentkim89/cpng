from bs4 import BeautifulSoup

def parse_price(html: str) -> float:
    soup = BeautifulSoup(html, 'html.parser')
    price_tag = soup.select_one('.total-price .price-value')
    if not price_tag:
        raise ValueError('가격 정보를 찾을 수 없습니다.')
    text = price_tag.get_text().replace(',', '').strip()
    return float(text)
