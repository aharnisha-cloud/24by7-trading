#!/usr/bin/env python3
"""Fetch hourly OHLCV candles for NSE symbols into data/ as CSV.

Uses Yahoo Finance's public chart API directly with a browser User-Agent.
(yfinance's default request path gets HTTP 429 from cloud IPs; the chart
endpoint with a browser UA does not.) No API key required.

Usage:
    python scripts/fetch_nse_data.py RELIANCE TCS HDFCBANK
    python scripts/fetch_nse_data.py --list nifty100          # all 100
    python scripts/fetch_nse_data.py --list nifty50 --days 90
    python scripts/fetch_nse_data.py ^NSEI                     # NIFTY 50 index

NSE symbols get a .NS suffix automatically (RELIANCE -> RELIANCE.NS).
Indices are passed with a leading ^ (^NSEI = NIFTY 50, ^NSEBANK = BANK NIFTY).

Output: data/<SYMBOL>_1H.csv (datetime,open,high,low,close,volume — oldest
first, IST timestamps).

Always spot-check a few candles against your broker/charting platform before
using the data — this is convenience, not a verified feed.
"""

import argparse
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nifty100 import NIFTY_50, NIFTY_100, NIFTY_NEXT_50  # noqa: E402

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0 Safari/537.36"),
    "Accept": "application/json",
}
LISTS = {"nifty50": NIFTY_50, "niftynext50": NIFTY_NEXT_50, "nifty100": NIFTY_100}

IST = "Asia/Kolkata"


def to_yahoo(symbol: str) -> str:
    if symbol.startswith("^") or symbol.endswith(".NS"):
        return symbol
    return f"{symbol}.NS"


def fetch_one(symbol: str, days: int, max_retries: int = 4):
    ticker = to_yahoo(symbol)
    params = {"interval": "1h", "range": f"{days}d"}
    for attempt in range(max_retries):
        try:
            r = requests.get(CHART_URL.format(symbol=ticker), params=params,
                             headers=HEADERS, timeout=30)
        except requests.RequestException as exc:
            wait = 2 ** attempt
            print(f"    network error ({exc.__class__.__name__}); retry in {wait}s")
            time.sleep(wait)
            continue
        if r.status_code == 429 or r.status_code >= 500:
            wait = 2 ** attempt
            print(f"    HTTP {r.status_code}; backing off {wait}s")
            time.sleep(wait)
            continue
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}"
        return r.json(), None
    return None, "gave up after retries"


def parse(payload):
    """Return list of (dt_utc_seconds, o, h, l, c, v) skipping null candles."""
    result = payload["chart"]["result"][0]
    ts = result["timestamp"]
    q = result["indicators"]["quote"][0]
    rows = []
    for i, t in enumerate(ts):
        o, h, l, c, v = (q["open"][i], q["high"][i], q["low"][i],
                         q["close"][i], q["volume"][i])
        if None in (o, h, l, c):
            continue
        rows.append((t, o, h, l, c, v or 0))
    return rows


def write_csv(symbol: str, rows) -> Path:
    from datetime import datetime, timezone, timedelta
    ist = timezone(timedelta(hours=5, minutes=30))
    safe = symbol.replace("^", "").replace(".NS", "").replace(".", "-")
    path = DATA_DIR / f"{safe}_1H.csv"
    with open(path, "w") as f:
        f.write("datetime,open,high,low,close,volume\n")
        for t, o, h, l, c, v in rows:
            dt = datetime.fromtimestamp(t, tz=timezone.utc).astimezone(ist)
            f.write(f"{dt.strftime('%Y-%m-%d %H:%M')},"
                    f"{round(o, 2)},{round(h, 2)},{round(l, 2)},"
                    f"{round(c, 2)},{int(v)}\n")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("symbols", nargs="*", help="NSE symbols, e.g. RELIANCE TCS ^NSEI")
    parser.add_argument("--list", choices=LISTS.keys(),
                        help="fetch a predefined universe instead of listing symbols")
    parser.add_argument("--days", type=int, default=60,
                        help="calendar days of history (max ~730 for 1h; default 60)")
    parser.add_argument("--pause", type=float, default=0.6,
                        help="seconds to pause between symbols (politeness)")
    args = parser.parse_args()

    symbols = list(args.symbols)
    if args.list:
        symbols = LISTS[args.list] + symbols
    if not symbols:
        parser.error("give symbols or --list")

    DATA_DIR.mkdir(exist_ok=True)
    ok, failed = [], []
    for i, symbol in enumerate(symbols, 1):
        print(f"[{i}/{len(symbols)}] {symbol}")
        payload, err = fetch_one(symbol, args.days)
        if err:
            print(f"    !! {err}")
            failed.append((symbol, err))
        else:
            try:
                rows = parse(payload)
            except (KeyError, IndexError, TypeError):
                print("    !! unexpected response shape (bad/renamed symbol?)")
                failed.append((symbol, "no data"))
                continue
            if not rows:
                print("    !! empty")
                failed.append((symbol, "empty"))
            else:
                path = write_csv(symbol, rows)
                print(f"    {len(rows)} candles -> {path.relative_to(DATA_DIR.parent)}")
                ok.append(symbol)
        if i < len(symbols):
            time.sleep(args.pause)

    print(f"\nDone. {len(ok)} ok, {len(failed)} failed.")
    if failed:
        print("Failed (check symbol names / renames):")
        for s, why in failed:
            print(f"  {s}: {why}")


if __name__ == "__main__":
    main()
