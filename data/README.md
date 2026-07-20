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
