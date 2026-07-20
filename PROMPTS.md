# Stage Prompts

Run these in order each session. Stages 1–2 run on the whole watchlist;
Stage 3–4 run per asset; Stage 5 runs on later check-ins; Stage 6 closes the
loop. Everything is paper-only and the final decision is always human.

## ① Market Scanner

> Review the data I provide for my watchlist [paste price, volume, trend, key
> levels, and any news]. For each asset, summarize: current trend, notable
> volume, and whether anything looks worth watching. Use ONLY my data — don't
> invent prices or news. Flag anything missing.

## ② Signal Detection

> From the scanned data, identify POSSIBLE setups — breakouts, pullbacks,
> momentum, trend continuation, or reversals. For each, state the evidence and
> what would confirm or invalidate it. Be clear these are possible setups, NOT
> guaranteed trades.

## ③ Trade Plan

> For [asset], turn this setup into a clear plan: direction, entry condition,
> target, stop-loss, invalidation level, timeframe, and risk-to-reward ratio —
> plus a one-line reason for the setup. Keep it specific and testable.
> Paper-trading plan only.

Output goes to `setups/YYYY-MM-DD_SYMBOL_direction.md` using `setups/TEMPLATE.md`.

## ④ Risk Manager

> Account size [$X], max [1%] risk per trade. For entry [X] and stop [Y],
> calculate exact position size and dollar risk. Check total exposure, current
> open positions, volatility, and my max drawdown limit. Flag anything that
> breaks my rules and BLOCK the plan if it does.

Defaults (edit in `watchlist.md`): $10,000 paper account, 1% risk per trade,
max 3 open paper positions.

## ⑤ Monitoring

> Here's my current watchlist + active paper setups [paste updated data].
> Re-scan, tell me what changed, whether any setup triggered or invalidated,
> and whether risk still looks OK. Suggest watchlist updates and what alerts I
> should set. No predictions.

Updates setup statuses and `logs/decisions.md`.

## ⑥ Final Decision

> Summarize the setup, signal strength, risk level, and the trade plan. Give a
> final status: APPROVED / WATCHLIST / REJECTED — with your reasoning. State
> clearly this is paper-only and requires human review. The decision and risk
> are mine.

The AI's status is a recommendation. You record YOUR decision in the setup
file and `logs/decisions.md` — a plan is not live until you mark it APPROVED.
