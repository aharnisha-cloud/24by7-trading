# Watchlist

## Approach: scan wide, trade narrow

The **universe** is the NIFTY 100 (large-caps, listed in `scripts/nifty100.py`).
That's the pool Stage ① scans. It is **not** 100 things to trade — a
paper workflow with human approval on every setup only works on a handful of
names at a time.

- **Stage ① Scanner** runs across all ~100 → produces a **shortlist** of names
  showing something worth watching (trend + notable volume).
- **Stage ② Signals** looks only at the shortlist for possible setups.
- **Stages ③–⑥** (plan → risk → decide) run only on setups you choose to pursue.
- **Cap: max 3 open paper positions at once** (see risk rules below).

## Timeframe

- **1-hour chart** (1H candles), NSE cash session 09:15–15:30 IST.
- Note: the 09:15 candle often shows 0 volume (opening auction) and Yahoo adds
  a single-tick 15:30 row at the close — ignore both as signal.

## Universe

- NIFTY 100 = NIFTY 50 + NIFTY Next 50 → `scripts/nifty100.py`
- Data files: `data/<SYMBOL>_1H.csv`, refresh via
  `python scripts/fetch_nse_data.py --list nifty100 --days 60`
- Market context: `data/NSEI_1H.csv` (NIFTY 50 index)

### Known data notes (verify — your "verified data only" rule)
- **Tata Motors** demerged (2025): old `TATAMOTORS` retired → tracked as
  `TMPV` (passenger vehicles) and `TMCV` (commercial vehicles).
- **LTIM** (LTIMindtree): no data on Yahoo currently → excluded until a
  working source is found.

## Criteria (what counts as a setup)

Define your rules here so the AI scans consistently. Starting defaults:

- **Trend:** price vs the 50-period (1H) moving average; direction of last ~20 candles.
- **Trigger:** breakout of the last 20 candles' high/low, or pullback to a
  clear support/resistance level.
- **Volume:** current candle volume notably above the recent average.
- **Risk:** stop-loss defined **before** entry; minimum **2:1** reward:risk.

## Risk rules (used by Stage ④) — EDIT THESE

> These are placeholders. Confirm your real numbers.

- **Paper account size:** ₹10,00,000 (10 lakh)
- **Risk per trade:** 1% of account = ₹10,000
- **Max open paper positions:** 3
- **Max portfolio drawdown limit:** −5% (₹50,000) → stop opening new positions
  until reset
- **Currency:** INR
