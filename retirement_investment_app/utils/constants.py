"""Configuration constants for the Retirement Investment Optimization app."""

# Default values
DEFAULT_PRINCIPAL = 10000.0
DEFAULT_YEARS = 20
DEFAULT_LIFESPAN = 30
DEFAULT_FIXED_RATE = 0.07
DEFAULT_VARIABLE_RATES = "0.05, 0.06, 0.07, 0.08"
DEFAULT_MARKET_YEARS = 20

# Limits
MIN_PRINCIPAL = 0.0
MIN_YEARS = 1
MIN_RATE = 0.0
MAX_RATE = 1.0
MAX_YEARS_CAP = 120

# Binary search parameters
TOLERANCE = 0.01

# UI Configuration
PAGE_TITLE = "Retirement Investment Optimization"
PAGE_ICON = "🏦"

# Rate modes
RATE_MODE_FIXED = "Fixed Rate"
RATE_MODE_VARIABLE = "Variable Rate"
RATE_MODE_MARKET = "Real S&P 500 Market Data"
UPLOADED_RATES = "Upload CSV Data"
