#!/usr/bin/env python3
"""Stage 1 Market Scanner — computes trend/volume/level metrics for every
data/<SYMBOL>_1H.csv using ONLY the candles in those files. Invents nothing.

Outputs a ranked table and a flagged shortlist of names worth watching.
Metrics (all on the 1H series):
  close      last close
  vsMA50     % of last close above/below the 50-period close MA (trend)
  MA20>50    'up' if MA20 above MA50 (aligned trend), else 'dn'
  chg20      % change over the last 20 candles (momentum)
  volx       last completed candle volume / 20-candle average volume
  posn       where close sits in the last 20-candle high-low range (0=low,100=high)
  d20hi/lo   % distance from the 20-candle high / low (breakout proximity)

A name is FLAGGED for the shortlist if any of:
  - volx >= 1.5           (notable volume)
  - d20hi <= 0.5%         (pressing 20-bar high — possible breakout up)
  - d20lo <= 0.5%         (pressing 20-bar low — possible breakdown)
  - |vsMA50| >= 4% with aligned MA20>50 direction (strong trend)

Usage: python scripts/scan.py [--top N]
"""

import argparse
import csv
import glob
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            try:
                o, h, l, c = (float(r["open"]), float(r["high"]),
                              float(r["low"]), float(r["close"]))
                v = int(float(r["volume"]))
            except (ValueError, KeyError):
                continue
            rows.append({"dt": r["datetime"], "o": o, "h": h, "l": l, "c": c, "v": v})
    # drop the Yahoo EOD single-tick marker (o==h==l==c and 0 volume)
    cleaned = [r for r in rows if not (r["v"] == 0 and r["o"] == r["h"] == r["l"] == r["c"])]
    return cleaned


def ma(vals, n):
    if len(vals) < n:
        return None
    return sum(vals[-n:]) / n


def analyse(rows):
    if len(rows) < 51:
        return None
    closes = [r["c"] for r in rows]
    vols = [r["v"] for r in rows]
    last = closes[-1]
    ma50 = ma(closes, 50)
    ma20 = ma(closes, 20)
    vs_ma50 = (last - ma50) / ma50 * 100 if ma50 else None
    ma_dir = "up" if (ma20 and ma50 and ma20 > ma50) else "dn"
    chg20 = (last - closes[-21]) / closes[-21] * 100 if len(closes) >= 21 else None

    nonzero_v = [v for v in vols[:-1] if v > 0]  # exclude last (in-progress) candle
    avg_v = sum(nonzero_v[-20:]) / min(len(nonzero_v), 20) if nonzero_v else 0
    last_full_v = vols[-1] if vols[-1] > 0 else (nonzero_v[-1] if nonzero_v else 0)
    volx = (last_full_v / avg_v) if avg_v else 0

    hi20 = max(r["h"] for r in rows[-20:])
    lo20 = min(r["l"] for r in rows[-20:])
    rng = hi20 - lo20
    posn = (last - lo20) / rng * 100 if rng else 50
    d20hi = (hi20 - last) / last * 100
    d20lo = (last - lo20) / last * 100

    return {
        "close": last, "vsMA50": vs_ma50, "madir": ma_dir, "chg20": chg20,
        "volx": volx, "posn": posn, "d20hi": d20hi, "d20lo": d20lo,
    }


def flags(m):
    """Flags require confirmation, not a single noisy condition. A breakout
    counts only when price presses the 20-bar edge AND momentum or volume
    backs it; a trend counts only when it's stretched and aligned."""
    f = []
    if m["volx"] >= 1.5:
        f.append("VOL")
    backed = m["volx"] >= 1.2 or abs(m["chg20"]) >= 1.5
    if m["d20hi"] <= 0.3 and backed and m["chg20"] > 0:
        f.append("↑brk")
    if m["d20lo"] <= 0.3 and backed and m["chg20"] < 0:
        f.append("↓brk")
    if m["vsMA50"] is not None and abs(m["vsMA50"]) >= 4 and \
       ((m["vsMA50"] > 0) == (m["madir"] == "up")):
        f.append("TREND" + ("+" if m["vsMA50"] > 0 else "-"))
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=0, help="print only top N by volx")
    args = ap.parse_args()

    results = []
    for path in sorted(glob.glob(str(DATA_DIR / "*_1H.csv"))):
        sym = os.path.basename(path).replace("_1H.csv", "")
        if sym in ("TEMPLATE",):
            continue
        rows = load(path)
        m = analyse(rows)
        if not m:
            continue
        m["sym"] = sym
        m["flags"] = flags(m)
        results.append(m)

    results.sort(key=lambda x: x["volx"], reverse=True)
    view = results[:args.top] if args.top else results

    hdr = f"{'SYM':<12}{'close':>10}{'vsMA50':>8}{'md':>4}{'chg20':>8}{'volx':>7}{'posn':>6}{'d20hi':>7}{'d20lo':>7}  flags"
    print(hdr)
    print("-" * len(hdr))
    for m in view:
        print(f"{m['sym']:<12}{m['close']:>10.2f}{m['vsMA50']:>7.1f}%{m['madir']:>4}"
              f"{m['chg20']:>7.1f}%{m['volx']:>7.2f}{m['posn']:>6.0f}"
              f"{m['d20hi']:>6.1f}%{m['d20lo']:>6.1f}%  {' '.join(m['flags'])}")

    shortlist = [m for m in results if m["flags"]]
    print(f"\nSHORTLIST ({len(shortlist)} of {len(results)} flagged):")
    for m in sorted(shortlist, key=lambda x: (-len(x["flags"]), -x["volx"])):
        print(f"  {m['sym']:<12} {' '.join(m['flags'])}")


if __name__ == "__main__":
    main()
