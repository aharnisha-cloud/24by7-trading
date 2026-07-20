# data/ — Market data

Paste **verified** market data here, one CSV file per symbol per timeframe.

## File naming

```
SYMBOL_TIMEFRAME.csv     e.g. SPY_1H.csv, BTC-USD_1H.csv
```

## Format (CSV, newest rows at the bottom)

```csv
datetime,open,high,low,close,volume
2026-07-17 14:00,562.10,563.45,561.80,563.20,1250000
2026-07-17 15:00,563.20,564.00,562.50,563.75,980000
```

- `datetime` in your local exchange time or UTC — pick one and stay consistent.
- Include enough history for the indicators you use (e.g. 100+ candles for a 50-period MA).
- Source the data from your own charting platform or data provider and eyeball
  it before pasting — the AI trusts what's in this folder.

See `TEMPLATE.csv` for a starting file.

## Getting NSE (India) data

Easiest free option — Yahoo Finance via the helper script (run on your own
machine; NSE symbols use a `.NS` suffix there):

```bash
pip install yfinance
python scripts/fetch_nse_data.py RELIANCE TCS HDFCBANK INFY
python scripts/fetch_nse_data.py ^NSEI          # NIFTY 50 index
python scripts/fetch_nse_data.py --days 90 TATAMOTORS
```

This writes `data/RELIANCE_1H.csv` etc. in the right format, timestamps in
IST. Yahoo serves hourly candles up to ~730 days back.

Alternatives:
- **TradingView** — chart `NSE:RELIANCE` on 1H, export chart data (paid plans).
- **Your broker** — Zerodha Kite Connect, Upstox, or Angel One SmartAPI all
  serve historical intraday candles via API.
- **NSE website** — bhavcopy downloads are daily-only, not hourly.

NSE notes:
- Market hours are 09:15–15:30 IST, so "hourly" candles start at 09:15,
  10:15, ... and the last candle of the day is short (15:15–15:30).
- Whatever the source, spot-check a few candles against your broker's chart
  before using the file — Yahoo data occasionally has gaps or bad ticks.
