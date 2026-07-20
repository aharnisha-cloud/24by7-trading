# 24by7 Trading — Paper Trading Assistant

An AI-assisted **paper trading** workflow. The AI analyzes data and proposes
trade plans; **you approve every decision**. No real money, no broker
connection, no automated order execution — ever.

## Ground rules

1. **Paper only.** All trades are simulated. This repo never connects to a broker.
2. **Human approval.** The AI proposes; you decide. Nothing is "executed" (even on paper) without your explicit OK.
3. **Log everything.** Every proposal, approval, rejection, and outcome goes in `logs/`.
4. **Verified data only.** You paste market data you've checked yourself into `data/`. The AI does not fetch live prices.

## Folder structure

```
data/     Market data you paste in (OHLC candles, one file per symbol)
setups/   Trade plans the AI proposes (entry, stop, target, reasoning)
logs/     Decision log + results of every paper trade
watchlist.md   Your markets and timeframe
```

## Workflow (each session)

1. **Update data** — paste fresh, verified candles for each watchlist symbol into `data/`.
2. **Stage 1 – Scan:** ask the AI to review the data and flag anything matching your criteria.
3. **Stage 2 – Plan:** for flagged symbols, the AI writes a trade plan in `setups/` (entry, stop-loss, target, position size, risk:reward, reasoning).
4. **Stage 3 – Approve:** you review each plan and mark it `APPROVED` or `REJECTED` (with a reason).
5. **Stage 4 – Log:** approved plans get a row in `logs/decisions.md`. When the trade resolves (paper), record the outcome.
6. **Stage 5 – Review:** periodically ask the AI to analyze `logs/` for what's working and what isn't.

## Getting started

1. Edit `watchlist.md` — pick 3–5 markets and one timeframe.
2. Paste data for each symbol into `data/` using the format in `data/README.md`.
3. Run the stage prompts in order.
