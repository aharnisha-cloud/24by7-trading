"""NIFTY 100 constituent list (NSE symbols, no .NS suffix).

SNAPSHOT — index membership changes at each rebalance and companies get
renamed (e.g. Zomato -> Eternal). Treat this as a starting universe and
verify against the official NSE/NiftyIndices factsheet before relying on it.
The fetch script reports any symbol that returns no data so you can prune.

NIFTY 100 = NIFTY 50 + NIFTY Next 50.
"""

NIFTY_50 = [
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "INFY", "HINDUNILVR", "ITC",
    "SBIN", "BHARTIARTL", "BAJFINANCE", "KOTAKBANK", "LT", "HCLTECH", "AXISBANK",
    "MARUTI", "SUNPHARMA", "TITAN", "ULTRACEMCO", "NESTLEIND", "WIPRO", "ONGC",
    "NTPC", "POWERGRID", "M&M", "TATAMOTORS", "TATASTEEL", "JSWSTEEL", "ADANIENT",
    "ADANIPORTS", "COALINDIA", "BAJAJFINSV", "HDFCLIFE", "SBILIFE", "GRASIM",
    "BRITANNIA", "CIPLA", "DRREDDY", "EICHERMOT", "HEROMOTOCO", "HINDALCO",
    "INDUSINDBK", "TECHM", "APOLLOHOSP", "BAJAJ-AUTO", "BPCL", "TATACONSUM",
    "SHRIRAMFIN", "TRENT", "ETERNAL",
    # Tata Motors demerged (2025) into two listed entities — old TATAMOTORS
    # ticker is retired. Both successors below:
    "TMPV.NS", "TMCV.NS",
    # NOTE: LTIM (LTIMindtree) has no data on Yahoo Finance right now —
    # excluded until a working source is found. Add back when available.
]

NIFTY_NEXT_50 = [
    "ADANIGREEN", "ADANIPOWER", "ADANIENSOL", "AMBUJACEM", "DMART",
    "BAJAJHLDNG", "BANKBARODA", "BERGEPAINT", "BEL", "BOSCHLTD", "CANBK",
    "CHOLAFIN", "COLPAL", "DABUR", "DLF", "GAIL", "GODREJCP", "HAVELLS",
    "ICICIGI", "ICICIPRULI", "IOC", "INDIGO", "NAUKRI", "JINDALSTEL", "JIOFIN",
    "LICI", "MARICO", "MOTHERSON", "MUTHOOTFIN", "PIDILITIND", "PFC", "PNB",
    "RECLTD", "SIEMENS", "SRF", "TVSMOTOR", "TATAPOWER", "TORNTPHARM", "VBL",
    "VEDL", "ZYDUSLIFE", "IRCTC", "HAL", "ABB", "UNITDSPR", "PAGEIND",
    "INDHOTEL", "GODREJPROP", "IDEA", "MAXHEALTH",
]

NIFTY_100 = NIFTY_50 + NIFTY_NEXT_50

# Index tickers on Yahoo (use with the fetch script directly)
INDICES = {
    "NIFTY50": "^NSEI",
    "NIFTYBANK": "^NSEBANK",
    "NIFTY100": "^CNX100",
}
