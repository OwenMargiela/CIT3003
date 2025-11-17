"""Investment calculation functions.

This module depends on NumPy. If NumPy is not installed the import will raise
an informative error telling the user how to install it.
"""
try:
    import numpy as np
except ImportError as e:
    raise ImportError(
        "`numpy` is required by retirement_investment_app.core.calculations. "
        "Install it with `pip install numpy` or `pip install -r Documentation/requirements.txt`."
    ) from e


def fixedInvestor(principal, rate, years):
    """Simulate compound growth at a fixed annual rate (vectorized)."""
    if years <= 0:
        return round(principal, 2)
    return round(float(principal) * float((1 + rate) ** years), 2)


def variableInvestor(principal, rateList):
    """Simulate compound growth with different yearly rates (vectorized)."""
    if not rateList:
        return round(principal, 2)
    rates = np.array(rateList, dtype=float)
    growth = np.prod(1.0 + rates)
    return round(float(principal) * float(growth), 2)


def finallyRetired(balance, expense, rate, target_years=None):
    """
    Simulate yearly withdrawals after retirement.
    Returns (years_elapsed, breakdown_list).
    If target_years is provided, simulation stops after target_years even if still positive.
    """
    years = 0
    breakdown = []
    bal = float(balance)
    max_years_cap = 120
    while bal > 0 and (target_years is None or years < target_years) and years < max_years_cap:
        bal = bal * (1 + rate) - expense
        years += 1
        breakdown.append(round(bal, 2))
    return years, breakdown


def maximumExpensed(balance, rate, target_years=30, tolerance=0.01):
    """
    Binary search (successive approximation) to find the maximum sustainable annual withdrawal
    such that the balance is approximately zero after target_years.
    Returns the withdrawal rounded to 2 decimals.
    """
    low, high = 0.0, float(balance)
    while (high - low) > tolerance:
        mid = (low + high) / 2.0
        years, breakdown = finallyRetired(balance, mid, rate, target_years)
        final_balance = breakdown[-1] if breakdown else balance
        if final_balance > 0:
            low = mid
        else:
            high = mid
    return round(low, 2)
