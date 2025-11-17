"""Main Streamlit application entrypoint for the refactored retirement app."""
import streamlit as st
import numpy as np
from utils.constants import (
    PAGE_TITLE, PAGE_ICON,
    RATE_MODE_FIXED, RATE_MODE_VARIABLE, RATE_MODE_MARKET
)
from core.calculations import (
    fixedInvestor, variableInvestor, finallyRetired, maximumExpensed
)
from core.data_fetch import fetch_market_returns
from ui.sidebar import render_sidebar
from ui.results import display_results, display_market_preview


def main():
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
    st.title(f"{PAGE_ICON} {PAGE_TITLE}")
    st.markdown("*Powered by NumPy & Yahoo Finance*")

    inputs = render_sidebar()

    if inputs['rate_mode'] == RATE_MODE_MARKET:
        display_market_preview(inputs['market_years'], fetch_market_returns)

    if inputs['calculate_btn']:
        process_calculation(inputs)

    if 'results' in st.session_state:
        display_results(st.session_state.results)
    else:
        st.info("👈 Enter your parameters in the sidebar and click **Calculate** to see results.")

    st.markdown("---")
    st.markdown("*CIT3003 Group Project - Developed by Jayda Miller, Andre, Joshua*")


def process_calculation(inputs):
    try:
        if inputs['principal'] <= 0 or inputs['years'] <= 0 or inputs['lifespan'] <= 0:
            st.error("❌ Principal, years until retirement, and lifespan must be > 0.")
            return

        with st.spinner("Calculating..."):
            # If the user uploaded a CSV of rates, use it (overrides other rate inputs)
            uploaded = inputs.get('uploaded_rates')
            if uploaded:
                # pad or truncate to requested years
                rate_list = list(uploaded)
                if len(rate_list) < inputs['years']:
                    rate_list = rate_list + [rate_list[-1]] * (inputs['years'] - len(rate_list))
                else:
                    rate_list = rate_list[: inputs['years']]

                balance = variableInvestor(inputs['principal'], rate_list)
                effective_rate = float(np.mean(rate_list)) if rate_list else 0.0
                rates_used = rate_list

            else:
                if inputs['rate_mode'] == RATE_MODE_MARKET:
                    balance, rates_used, effective_rate = calculate_market_mode(
                        inputs['principal'], inputs['years'], inputs['market_years']
                    )
                    if balance is None:
                        return

                elif inputs['rate_mode'] == RATE_MODE_FIXED:
                    balance, rates_used, effective_rate = calculate_fixed_mode(
                        inputs['principal'], inputs['years'], inputs['fixed_rate']
                    )

                else:
                    balance, rates_used, effective_rate = calculate_variable_mode(
                        inputs['principal'], inputs['years'], inputs['variable_rates_input']
                    )
                    if balance is None:
                        return

            max_expense = maximumExpensed(balance, effective_rate, inputs['lifespan'])
            duration, breakdown = finallyRetired(balance, max_expense, effective_rate, inputs['lifespan'])

            st.session_state.results = {
                'balance': balance,
                'max_expense': max_expense,
                'duration': duration,
                'breakdown': breakdown,
                'rates_used': rates_used,
                'principal': inputs['principal'],
                'years': inputs['years'],
                'lifespan': inputs['lifespan'],
                'mode': inputs['rate_mode']
            }

            st.success("✅ Calculation complete!")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")


def calculate_market_mode(principal, years, market_years):
    rate_list = fetch_market_returns(market_years)
    if not rate_list:
        return None, None, None

    if len(rate_list) < years:
        pad = [rate_list[-1]] * (years - len(rate_list))
        pre_rates = (rate_list + pad)[:years]
    else:
        pre_rates = rate_list[-years:]

    balance = variableInvestor(principal, pre_rates)
    effective_rate = float(np.mean(pre_rates)) if pre_rates else 0.0
    return balance, pre_rates, effective_rate


def calculate_fixed_mode(principal, years, fixed_rate):
    balance = fixedInvestor(principal, fixed_rate, years)
    rates_used = [fixed_rate] * years
    effective_rate = fixed_rate
    return balance, rates_used, effective_rate


def calculate_variable_mode(principal, years, variable_rates_input):
    try:
        rate_list = [float(x.strip()) for x in variable_rates_input.split(',') if x.strip()]
    except Exception:
        st.error("❌ Variable rates must be comma-separated decimal numbers (e.g., 0.05, 0.06)")
        return None, None, None

    if not rate_list:
        st.error("❌ Please enter at least one rate value.")
        return None, None, None

    if len(rate_list) < years:
        rate_list = rate_list + [rate_list[-1]] * (years - len(rate_list))
    else:
        rate_list = rate_list[:years]

    balance = variableInvestor(principal, rate_list)
    effective_rate = float(np.mean(rate_list)) if rate_list else 0.0
    return balance, rate_list, effective_rate


if __name__ == "__main__":
    main()
