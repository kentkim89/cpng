import pandas as pd
from price_monitor.storage import CSV_FILE

def detect_changes():
    df = pd.read_csv(CSV_FILE, names=['timestamp','url','price'])
    # TODO: 직전 값 대비 변동 여부 계산 로직 추가
    return df
