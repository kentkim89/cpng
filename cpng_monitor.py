import streamlit as st
import pandas as pd
from price_monitor.crawler import fetch_page
from price_monitor.parser import parse_price
from price_monitor.storage import save_price_log

st.set_page_config(page_title="Coupang 가격 모니터링", layout="wide")

# 사이드바 설정
st.sidebar.header("설정")
urls = st.sidebar.text_area(
    "모니터링할 상품 URL (줄바꿈으로 구분)",
    value="https://www.coupang.com/vp/products/1234567890"
).splitlines()

# 즉시 수집 버튼
if st.sidebar.button("가격 즉시 수집"):
    results = []
    for url in urls:
        html = fetch_page(url)
        price = parse_price(html)
        save_price_log(url, price)
        results.append((url, price))
    st.success("수집 완료!")
    for u, p in results:
        st.write(f"{u} → {p}원")

# 로그 로드 및 시각화
try:
    df = pd.read_csv("price_log.csv", names=["timestamp","url","price"])
    st.header("가격 히스토리")
    st.dataframe(df)
    st.header("가격 추이")
    for url in set(df.url):
        sub = df[df.url == url]
        st.line_chart(sub.set_index("timestamp")["price"])
except FileNotFoundError:
    st.warning("price_log.csv 파일을 찾을 수 없습니다. 먼저 '가격 즉시 수집'을 실행하세요.")
