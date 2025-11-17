"""Market data fetching helpers.

This module avoids importing Streamlit so it can be imported in non-UI
environments (tests, linters). If `yfinance`/`pandas` are not present the
fetch function returns `None` and emits a warning.
"""
from typing import List, Optional
import warnings

try:
    import yfinance as yf
    import pandas as pd
except Exception:
    yf = None
    pd = None


def fetch_market_returns(years: int = 20) -> Optional[List[float]]:
    """Fetch last `years` of S&P 500 annual returns using Yahoo Finance.

    Returns a list of annual returns as decimals (e.g., 0.08 for 8%), or None on failure.
    """
    if yf is None or pd is None:
        warnings.warn("yfinance or pandas not installed; cannot fetch market returns.")
        return None

    try:
        df = yf.download("^GSPC", period=f"{years}y", interval="1mo", progress=False)["Close"]
        
        if df is None or df.empty:
            raise RuntimeError("No data returned from Yahoo Finance.")
        yearly = df.resample("Y").last().pct_change().dropna()
        returns = yearly.values.flatten().tolist()
        return [float(r) for r in returns]
    except Exception as e:
        warnings.warn(f"Failed to fetch S&P 500 data: {e}")
        return None
