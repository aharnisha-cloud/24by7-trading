#!/usr/bin/env python3
"""Print precise trade-planning levels for given symbols, computed only from
data/<SYMBOL>_1H.csv: last close, 20-bar high/low, MA20, MA50, and ATR(14)
for stop sizing. Usage: python scripts/levels.py PNB APOLLOHOSP"""
import csv
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def load(sym):
    rows = []
    with open(DATA / f"{sym}_1H.csv") as f:
        for r in csv.DictReader(f):
            o, h, l, c, v = (float(r["open"]), float(r["high"]), float(r["low"]),
                             float(r["close"]), int(float(r["volume"])))
            rows.append((r["datetime"], o, h, l, c, v))
    return [r for r in rows if not (r[5] == 0 and r[1] == r[2] == r[3] == r[4])]


def atr(rows, n=14):
    trs = []
    for i in range(1, len(rows)):
        h, l, pc = rows[i][2], rows[i][3], rows[i-1][4]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    return sum(trs[-n:]) / n


for sym in sys.argv[1:]:
    rows = load(sym)
    closes = [r[4] for r in rows]
    last = closes[-1]
    hi20 = max(r[2] for r in rows[-20:])
    lo20 = min(r[3] for r in rows[-20:])
    ma20 = sum(closes[-20:]) / 20
    ma50 = sum(closes[-50:]) / 50
    a = atr(rows)
    print(f"\n{sym}  (last {rows[-1][0]} IST)")
    print(f"  last close : {last:.2f}")
    print(f"  20-bar high: {hi20:.2f}   20-bar low: {lo20:.2f}")
    print(f"  MA20       : {ma20:.2f}   MA50      : {ma50:.2f}")
    print(f"  ATR(14)    : {a:.2f}  ({a/last*100:.2f}% of price)")
    print(f"  last 6 closes: {[round(c,2) for c in closes[-6:]]}")
