import csv
from datetime import datetime

CSV_FILE = 'price_log.csv'

def save_price_log(url: str, price: float):
    ts = datetime.now().isoformat()
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([ts, url, price])
