"""UI components to render results and market preview."""
from typing import Any
import streamlit as st
import pandas as pd
import numpy as np
from .charts import create_investment_chart


def display_market_preview(market_years: int, fetch_func):
    """Fetch and display market returns preview using provided fetch function."""
    st.subheader("📊 Preview Market Data")
    col1, col2 = st.columns([1, 4])
    with col1:
        preview_btn = st.button("Preview S&P 500 Returns", use_container_width=True)

    if preview_btn:
        with st.spinner("Fetching market data..."):
            rates = fetch_func(market_years)
            if rates:
                st.success(f"✅ Fetched {len(rates)} years of S&P 500 data")
                preview_df = pd.DataFrame({
                    'Year': range(1, len(rates) + 1),
                    'Annual Return': [f"{r:.2%}" for r in rates],
                    'Return (Decimal)': [f"{r:.4f}" for r in rates]
                })
                st.dataframe(preview_df, use_container_width=True, height=400)


def display_results(results: Any):
    """Render the calculation results dict into Streamlit UI."""
    st.markdown("---")
    st.header("📊 Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Balance at Retirement", f"${results['balance']:,.2f}")
    with col2:
        st.metric("Maximum Annual Expense", f"${results['max_expense']:,.2f}")
    with col3:
        st.metric("Funds Last", f"{results['duration']} years")

    st.markdown("---")
    st.subheader("📈 Investment Trajectory")
    fig, retirement_year = create_investment_chart(
        results['principal'], 
        results['years'], 
        results['rates_used'], 
        results['max_expense'], 
        results['lifespan']
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Rate Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Rate Mode:**")
        st.info(results['mode'])
    with col2:
        st.markdown("**Average Annual Return:**")
        avg_return = float(np.mean(results['rates_used'])) if results['rates_used'] else 0.0
        st.info(f"{avg_return:.2%}")
    with col3:
        st.markdown("**Final Balance After Withdrawals:**")
        final_bal = results['breakdown'][-1] if results['breakdown'] else results['balance']
        st.info(f"${final_bal:,.2f}")

    with st.expander("📋 Year-by-Year Breakdown (Post-Retirement)"):
        breakdown_df = pd.DataFrame({
            'Year': range(1, len(results['breakdown']) + 1),
            'Balance': [f"${bal:,.2f}" for bal in results['breakdown']]
        })
        st.dataframe(breakdown_df, use_container_width=True, height=400)

    with st.expander("📊 Rates Used (Pre-Retirement)"):
        rates_df = pd.DataFrame({
            'Year': range(1, len(results['rates_used']) + 1),
            'Rate': [f"{r:.2%}" for r in results['rates_used']]
        })
        st.dataframe(rates_df, use_container_width=True, height=400)
