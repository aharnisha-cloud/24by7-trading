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
PROMPTS.md     The six stage prompts, run in order each session
```

## Workflow (each session)

The six stage prompts live in `PROMPTS.md`. Run them in order:

1. **Update data** — paste fresh, verified candles for each watchlist symbol into `data/`.
2. **① Market Scanner** — the AI reviews the data, summarizes trend/volume per asset, flags anything missing.
3. **② Signal Detection** — possible setups only, each with confirming and invalidating evidence.
4. **③ Trade Plan** — per asset: direction, entry, target, stop, invalidation, R:R → written to `setups/`.
5. **④ Risk Manager** — position size and dollar risk checked against your rules; rule-breaking plans get BLOCKED.
6. **⑤ Monitoring** — on later check-ins with updated data: what changed, what triggered or invalidated.
7. **⑥ Final Decision** — AI recommends APPROVED / WATCHLIST / REJECTED; **you** make the actual call and log it in `logs/decisions.md`.

## Getting started

1. Edit `watchlist.md` — pick 3–5 markets and one timeframe.
2. Paste data for each symbol into `data/` using the format in `data/README.md`.
3. Run the stage prompts in order.
