# setups/ — Trade plans

One file per proposed trade. The AI writes these; **you approve or reject them**.
A plan is never acted on (even on paper) while its status is `PROPOSED`.

## File naming

```
YYYY-MM-DD_SYMBOL_direction.md     e.g. 2026-07-20_SPY_long.md
```

## Template

Copy `TEMPLATE.md` for each new setup. Every plan must include:

- Entry price and trigger condition
- Stop-loss (defined **before** entry, always)
- Target(s) and reward:risk ratio
- Position size based on the risk rules in `watchlist.md`
- The reasoning, referencing the specific data in `data/`
- Status: `PROPOSED` → `APPROVED` / `REJECTED` → `FILLED` / `EXPIRED` → `CLOSED`
