"""Chart creation utilities (Plotly)."""
from typing import List, Tuple
import numpy as np
import plotly.graph_objects as go


def create_investment_chart(principal: float, years: int, rates_used: List[float], expense: float, lifespan: int) -> Tuple[go.Figure, int]:
    """Create investment chart with Plotly and return (fig, retirement_year)."""
    # Build pre-retirement balances
    pre_balances = [principal]
    bal = float(principal)
    for r in rates_used:
        bal = bal * (1 + r)
        pre_balances.append(round(bal, 2))

    # Post-retirement balances
    post_balances = [pre_balances[-1]]
    bal = pre_balances[-1]
    effective_rate = float(np.mean(rates_used)) if rates_used else 0.0
    for _ in range(lifespan):
        bal = bal * (1 + effective_rate) - expense
        post_balances.append(max(round(bal, 2), 0.0))

    # Full timeline
    full_balances = pre_balances[:-1] + post_balances
    retirement_year = len(pre_balances) - 1
    years_list = list(range(len(full_balances)))
    
    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years_list,
        y=full_balances,
        mode='lines+markers',
        name='Balance',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=4)
    ))
    fig.add_vline(
        x=retirement_year,
        line_dash="dash",
        line_color="red",
        annotation_text="Retirement Start",
        annotation_position="top"
    )
    fig.update_layout(
        title="Investment Growth & Retirement Withdrawals",
        xaxis_title="Years (0 = Start)",
        yaxis_title="Balance ($)",
        hovermode='x unified',
        height=500,
        showlegend=True
    )
    return fig, retirement_year
