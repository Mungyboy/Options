import json, os
from datetime import datetime
import yfinance as yf

os.makedirs('data', exist_ok=True)

TICKERS = ['SPY', 'QQQ', 'MSFT']

for ticker in TICKERS:
    try:
        raw = yf.download(ticker, period='2y', progress=False,
                          auto_adjust=True, multi_level_index=False)
        if raw.empty:
            raise ValueError('no data')
        bars = []
        for date, row in raw.iterrows():
            bars.append({
                'date':  str(date.date()),
                'open':  round(float(row['Open']),  4),
                'high':  round(float(row['High']),  4),
                'low':   round(float(row['Low']),   4),
                'close': round(float(row['Close']), 4),
            })
        with open(f'data/{ticker.lower()}.json', 'w') as f:
            json.dump({'bars': bars,
                       'ticker': ticker,
                       'updated': datetime.utcnow().isoformat() + 'Z',
                       'count': len(bars)}, f)
        print(f'✓ {ticker}: {len(bars)} bars saved')
    except Exception as e:
        print(f'✗ {ticker}: {e}')
