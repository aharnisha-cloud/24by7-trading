#!/usr/bin/env python3
"""Fetch hourly OHLCV candles for NSE symbols into data/ as CSV.

Usage:
    pip install yfinance
    python scripts/fetch_nse_data.py RELIANCE TCS HDFCBANK
    python scripts/fetch_nse_data.py --days 60 INFY

NSE symbols get a .NS suffix automatically (RELIANCE -> RELIANCE.NS).
Indices can be passed as-is with a leading ^ (e.g. ^NSEI for NIFTY 50).

Output: data/<SYMBOL>_1H.csv in the repo's standard format
(datetime,open,high,low,close,volume — oldest first, IST timestamps).

Always eyeball the output against your broker/charting platform before
using it for analysis — this is convenience, not a verified feed.
"""

import argparse
import sys
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    sys.exit("yfinance not installed. Run: pip install yfinance")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def to_yahoo(symbol: str) -> str:
    if symbol.startswith("^") or "." in symbol:
        return symbol
    return f"{symbol}.NS"


def fetch(symbol: str, days: int) -> None:
    ticker = to_yahoo(symbol)
    df = yf.Ticker(ticker).history(period=f"{days}d", interval="1h")
    if df.empty:
        print(f"  !! no data returned for {ticker} — check the symbol")
        return

    df = df.tz_convert("Asia/Kolkata")
    out = df.reset_index()[["Datetime", "Open", "High", "Low", "Close", "Volume"]]
    out.columns = ["datetime", "open", "high", "low", "close", "volume"]
    out["datetime"] = out["datetime"].dt.strftime("%Y-%m-%d %H:%M")
    for col in ("open", "high", "low", "close"):
        out[col] = out[col].round(2)
    out["volume"] = out["volume"].astype(int)

    safe_name = symbol.replace("^", "").replace(".", "-")
    path = DATA_DIR / f"{safe_name}_1H.csv"
    out.to_csv(path, index=False)
    print(f"  {ticker}: {len(out)} candles, {out['datetime'].iloc[0]} -> "
          f"{out['datetime'].iloc[-1]} -> {path.relative_to(DATA_DIR.parent)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbols", nargs="+", help="NSE symbols, e.g. RELIANCE TCS ^NSEI")
    parser.add_argument("--days", type=int, default=60,
                        help="How many calendar days of history (max ~730 for 1h)")
    args = parser.parse_args()

    DATA_DIR.mkdir(exist_ok=True)
    for symbol in args.symbols:
        print(f"Fetching {symbol} ...")
        fetch(symbol, args.days)


if __name__ == "__main__":
    main()
