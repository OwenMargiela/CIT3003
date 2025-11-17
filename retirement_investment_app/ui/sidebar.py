"""
Sidebar UI components for user input parameters for the retirement app.
Handles fixed, variable, market, and CSV-uploaded rates.
"""

import streamlit as st
from utils.constants import (
    DEFAULT_PRINCIPAL, DEFAULT_YEARS, DEFAULT_LIFESPAN,
    DEFAULT_FIXED_RATE, DEFAULT_VARIABLE_RATES, DEFAULT_MARKET_YEARS,
    MIN_PRINCIPAL, MIN_YEARS, MIN_RATE, MAX_RATE,
    RATE_MODE_FIXED, RATE_MODE_VARIABLE, RATE_MODE_MARKET
)


def parse_csv(uploaded_file):
    """
    Parse CSV file to extract a 'rate' column (case-insensitive).
    
    Returns:
        list[float] | None: list of rates or None if parsing fails
    """
    try:
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        cols = [c.lower() for c in df.columns]
        if 'rate' in cols:
            rate_col = df.columns[cols.index('rate')]
            return [float(x) for x in df[rate_col].tolist() if x == x]
        return None
    except Exception:
        # fallback to csv module
        import io, csv
        uploaded_file.seek(0)
        reader = csv.DictReader(io.StringIO(uploaded_file.read().decode('utf-8')))
        rates = []
        for row in reader:
            for k, v in row.items():
                if k.lower() == 'rate':
                    try:
                        rates.append(float(v))
                    except Exception:
                        pass
        return rates if rates else None


def render_sidebar():
    """
    Render sidebar with all input parameters.
    
    Returns:
        dict: Dictionary containing all user inputs
    """
    st.sidebar.header("📊 Input Parameters")

    # ------------------ Basic inputs ------------------
    principal = st.sidebar.number_input(
        "Principal ($)",
        min_value=MIN_PRINCIPAL,
        value=DEFAULT_PRINCIPAL,
        step=1000.0
    )

    years = st.sidebar.number_input(
        "Years until retirement",
        min_value=MIN_YEARS,
        value=DEFAULT_YEARS,
        step=1
    )

    lifespan = st.sidebar.number_input(
        "Expected lifespan after retirement (years)",
        min_value=MIN_YEARS,
        value=DEFAULT_LIFESPAN,
        step=1
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Rate Configuration")

    # ------------------ Rate mode selection ------------------
    rate_mode = st.sidebar.radio(
        "Select Rate Type",
        [RATE_MODE_FIXED, RATE_MODE_VARIABLE, RATE_MODE_MARKET]
    )

    # Initialize variables
    fixed_rate = None
    variable_rates_input = None
    market_years = None
    uploaded_rates = None
    
    
    # Optional CSV Upload

    # ------------------ CSV upload ------------------
    # uploaded_file = st.sidebar.file_uploader(
    #     "Upload CSV of rates (columns: year, rate)",
    #     type=["csv"],
    #     help="Optional: CSV must include a 'rate' column (year column optional)."
    # )
    # if uploaded_file is not None:
    #     uploaded_rates = parse_csv(uploaded_file)
    #     if uploaded_rates:
    #         st.sidebar.success(f"Uploaded {len(uploaded_rates)} rates from CSV")
    #     else:
    #         st.sidebar.error("CSV must include a 'rate' column with numeric values")
    #         uploaded_rates = None

    # ------------------ Rate-specific inputs ------------------
    if rate_mode == RATE_MODE_FIXED:
        fixed_rate = st.sidebar.number_input(
            "Annual interest rate",
            min_value=MIN_RATE,
            max_value=MAX_RATE,
            value=DEFAULT_FIXED_RATE,
            step=0.01,
            format="%.4f"
        )

    elif rate_mode == RATE_MODE_VARIABLE:
        variable_rates_input = st.sidebar.text_area(
            "Rates per year (comma-separated)",
            value=DEFAULT_VARIABLE_RATES,
            help="Enter comma-separated decimal values (e.g., 0.05, 0.06, 0.07)"
        )

    else:  # RATE_MODE_MARKET
        market_years = st.sidebar.number_input(
            "Years of market history to fetch",
            min_value=MIN_YEARS,
            value=DEFAULT_MARKET_YEARS,
            step=1
        )

    st.sidebar.markdown("---")
    calculate_btn = st.sidebar.button(
        "🚀 Calculate",
        type="primary",
        use_container_width=True
    )

    # ------------------ Return dictionary ------------------
    return {
        'principal': principal,
        'years': years,
        'lifespan': lifespan,
        'rate_mode': rate_mode,
        'fixed_rate': fixed_rate,
        'variable_rates_input': variable_rates_input,
        'market_years': market_years,
        'uploaded_rates': uploaded_rates,  # ✅ included
        'calculate_btn': calculate_btn
    }


# """Sidebar UI components for user input parameters."""

# import streamlit as st
# from utils.constants import (
#     DEFAULT_PRINCIPAL, DEFAULT_YEARS, DEFAULT_LIFESPAN,
#     DEFAULT_FIXED_RATE, DEFAULT_VARIABLE_RATES, DEFAULT_MARKET_YEARS,
#     MIN_PRINCIPAL, MIN_YEARS, MIN_RATE, MAX_RATE,
#     RATE_MODE_FIXED, RATE_MODE_VARIABLE, RATE_MODE_MARKET, UPLOADED_RATES
# )


# def render_sidebar():
#     """
#     Render sidebar with all input parameters.
    
#     Returns:
#         dict: Dictionary containing all user inputs
#     """
#     st.sidebar.header("📊 Input Parameters")

#     principal = st.sidebar.number_input(
#         "Principal ($)", 
#         min_value=MIN_PRINCIPAL, 
#         value=DEFAULT_PRINCIPAL, 
#         step=1000.0
#     )

#     years = st.sidebar.number_input(
#         "Years until retirement", 
#         min_value=MIN_YEARS, 
#         value=DEFAULT_YEARS, 
#         step=1
#     )

#     lifespan = st.sidebar.number_input(
#         "Expected lifespan after retirement (years)", 
#         min_value=MIN_YEARS, 
#         value=DEFAULT_LIFESPAN, 
#         step=1
#     )

#     st.sidebar.markdown("---")
#     st.sidebar.subheader("Rate Configuration")

#     rate_mode = st.sidebar.radio(
#         "Select Rate Type",
#         [RATE_MODE_FIXED, RATE_MODE_VARIABLE, RATE_MODE_MARKET, UPLOADED_RATES ]
#     )

#     fixed_rate = None
#     variable_rates_input = None
#     market_years = None
#     uploaded_rates = None

#     # CSV uploader (optional) - accepts CSV with at least a 'rate' column (case-insensitive)
#     uploaded_file = st.sidebar.file_uploader(
#         "Upload CSV of rates (columns: year, rate)", type=["csv"], help="CSV must include a 'rate' column. Year column is optional."
#     )
#     if rate_mode == UPLOADED_RATES:
#         try:
#             # Prefer pandas if available for convenience
#             try:
#                 import pandas as _pd
#                 df = _pd.read_csv(uploaded_file)
#                 cols = [c.lower() for c in df.columns]
#                 if 'rate' in cols:
#                     rate_col = df.columns[cols.index('rate')]
#                     uploaded_rates = [float(x) for x in df[rate_col].tolist() if x == x]
#                     st.sidebar.success(f"Uploaded {len(uploaded_rates)} rates from CSV")
#                 else:
#                     st.sidebar.error("CSV must include a 'rate' column (case-insensitive).")
#                     uploaded_rates = None
#             except Exception:
#                 # Fallback to csv module
#                 import io, csv as _csv
#                 uploaded_file.seek(0)
#                 text = uploaded_file.read().decode('utf-8')
#                 reader = _csv.DictReader(io.StringIO(text))
#                 rates = []
#                 for row in reader:
#                     # find 'rate' key case-insensitive
#                     for k, v in row.items():
#                         if k.lower() == 'rate':
#                             try:
#                                 rates.append(float(v))
#                             except Exception:
#                                 pass
#                 if rates:
#                     uploaded_rates = rates
#                     st.sidebar.success(f"Uploaded {len(uploaded_rates)} rates from CSV")
#                 else:
#                     st.sidebar.error("CSV must include a 'rate' column (case-insensitive).")
#                     uploaded_rates = None
#         except Exception as e:
#             st.sidebar.error(f"Failed to parse CSV: {e}")
#             uploaded_rates = None

#     if rate_mode == RATE_MODE_FIXED:
#         fixed_rate = st.sidebar.number_input(
#             "Annual interest rate", 
#             min_value=MIN_RATE, 
#             max_value=MAX_RATE, 
#             value=DEFAULT_FIXED_RATE, 
#             step=0.01, 
#             format="%.4f"
#         )

#     elif rate_mode == RATE_MODE_VARIABLE:
#         variable_rates_input = st.sidebar.text_area(
#             "Rates per year (comma-separated)", 
#             value=DEFAULT_VARIABLE_RATES,
#             help="Enter comma-separated decimal values (e.g., 0.05, 0.06, 0.07)"
#         )

#     else:  # RATE_MODE_MARKET
#         market_years = st.sidebar.number_input(
#             "Years of market history to fetch", 
#             min_value=MIN_YEARS, 
#             value=DEFAULT_MARKET_YEARS, 
#             step=1
#         )

#     st.sidebar.markdown("---")
#     calculate_btn = st.sidebar.button(
#         "🚀 Calculate", 
#         type="primary", 
#         use_container_width=True
#     )

#     return {
#         'principal': principal,
#         'years': years,
#         'lifespan': lifespan,
#         'rate_mode': rate_mode,
#         'fixed_rate': fixed_rate,
#         'variable_rates_input': variable_rates_input,
#         'market_years': market_years,
#         'calculate_btn': calculate_btn
#     }
# """
# Sidebar UI components for user input parameters.
# """

# import streamlit as st
# from utils.constants import (
#     DEFAULT_PRINCIPAL, DEFAULT_YEARS, DEFAULT_LIFESPAN,
#     DEFAULT_FIXED_RATE, DEFAULT_VARIABLE_RATES, DEFAULT_MARKET_YEARS,
#     MIN_PRINCIPAL, MIN_YEARS, MIN_RATE, MAX_RATE,
#     RATE_MODE_FIXED, RATE_MODE_VARIABLE, RATE_MODE_MARKET
# )


# def render_sidebar():
#     """
#     Render sidebar with all input parameters.
    
#     Returns:
#         dict: Dictionary containing all user inputs
#     """
#     st.sidebar.header("📊 Input Parameters")
    
#     # Basic parameters
#     principal = st.sidebar.number_input(
#         "Principal ($)", 
#         min_value=MIN_PRINCIPAL, 
#         value=DEFAULT_PRINCIPAL, 
#         step=1000.0
#     )
    
#     years = st.sidebar.number_input(
#         "Years until retirement", 
#         min_value=MIN_YEARS, 
#         value=DEFAULT_YEARS, 
#         step=1
#     )
    
#     lifespan = st.sidebar.number_input(
#         "Expected lifespan after retirement (years)", 
#         min_value=MIN_YEARS, 
#         value=DEFAULT_LIFESPAN, 
#         step=1
#     )
    
#     st.sidebar.markdown("---")
#     st.sidebar.subheader("Rate Configuration")
    
#     # Rate mode selection
#     rate_mode = st.sidebar.radio(
#         "Select Rate Type",
#         [RATE_MODE_FIXED, RATE_MODE_VARIABLE, RATE_MODE_MARKET]
#     )
    
#     # Rate-specific inputs
#     fixed_rate = None
#     variable_rates_input = None
#     market_years = None
    
#     if rate_mode == RATE_MODE_FIXED:
#         fixed_rate = st.sidebar.number_input(
#             "Annual interest rate", 
#             min_value=MIN_RATE, 
#             max_value=MAX_RATE, 
#             value=DEFAULT_FIXED_RATE, 
#             step=0.01, 
#             format="%.4f"
#         )
    
#     elif rate_mode == RATE_MODE_VARIABLE:
#         variable_rates_input = st.sidebar.text_area(
#             "Rates per year (comma-separated)", 
#             value=DEFAULT_VARIABLE_RATES,
#             help="Enter comma-separated decimal values (e.g., 0.05, 0.06, 0.07)"
#         )
    
#     else:  # RATE_MODE_MARKET
#         market_years = st.sidebar.number_input(
#             "Years of market history to fetch", 
#             min_value=MIN_YEARS, 
#             value=DEFAULT_MARKET_YEARS, 
#             step=1
#         )
    
#     # Calculate button
#     st.sidebar.markdown("---")
#     calculate_btn = st.sidebar.button(
#         "🚀 Calculate", 
#         type="primary", 
#         use_container_width=True
#     )
    
#     return {
#         'principal': principal,
#         'years': years,
#         'lifespan': lifespan,
#         'rate_mode': rate_mode,
#         'fixed_rate': fixed_rate,
#         'variable_rates_input': variable_rates_input,
#         'market_years': market_years,
#         'uploaded_rates': uploaded_rates,
#         'calculate_btn': calculate_btn
#     }
