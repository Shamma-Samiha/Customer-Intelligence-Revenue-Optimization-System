import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path, load_app_styles
from webapp.components.charts import horizontal_bar_chart, line_chart
from webapp.components.kpi_cards import render_insight, render_kpi_row
from webapp.utils.filters import sidebar_filters
from webapp.utils.formatters import money
from webapp.utils.loaders import load_all_data


def show_chart(fig, x_title: str, y_title: str) -> None:
    fig.update_xaxes(title=x_title)
    fig.update_yaxes(title=y_title)
    st.plotly_chart(fig, use_container_width=True)


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero" style="margin-bottom:1.4rem;">
            <div style="font-size:0.78rem; letter-spacing:0.16em; text-transform:uppercase; opacity:0.88; font-weight:700;">
                Leadership Dashboard
            </div>
            <div style="font-family:'Manrope','Segoe UI',sans-serif; font-size:3rem; line-height:1.02; font-weight:800; margin:0.45rem 0 0.85rem;">
                Executive Overview
            </div>
            <div style="max-width:820px; font-size:1.08rem; line-height:1.75; opacity:0.96;">
                A premium operating snapshot of revenue scale, profitability, regional concentration, and segment performance
                designed for fast business review and recruiter-ready storytelling.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_card(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-header">{title}</div>
            <div class="section-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


ensure_project_on_path()
load_app_styles()

data = load_all_data()
orders = sidebar_filters(data["orders"]).copy()

total_sales = orders["sales"].sum()
total_profit = orders["profit"].sum()
total_orders = orders["order_id"].nunique()
avg_order_value = total_sales / total_orders if total_orders else 0
profit_margin = total_profit / total_sales if total_sales else 0

monthly = (
    orders.groupby("year_month", as_index=False)[["sales", "profit"]]
    .sum()
    .sort_values("year_month")
)
region_summary = (
    orders.groupby("region", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
)
segment_summary = (
    orders.groupby("segment", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
)

top_region = region_summary.iloc[0]["region"] if not region_summary.empty else "N/A"
top_segment = segment_summary.iloc[0]["segment"] if not segment_summary.empty else "N/A"

render_hero()

with st.container():
    render_kpi_row(
        [
            ("Total Sales", money(total_sales)),
            ("Total Profit", money(total_profit)),
            ("Avg Order Value", money(avg_order_value)),
            ("Profit Margin", f"{profit_margin:.1%}"),
        ]
    )

st.markdown("<div style='height:1.05rem;'></div>", unsafe_allow_html=True)

with st.container():
    render_section_card(
        "Performance Momentum",
        "Track how revenue and profit evolve over time to understand whether scale is translating into healthier business performance.",
    )
    col1, col2 = st.columns(2)
    with col1:
        show_chart(
            line_chart(monthly, "year_month", "sales", "Monthly Sales Trend"),
            "Month",
            "Sales",
        )
    with col2:
        show_chart(
            line_chart(monthly, "year_month", "profit", "Monthly Profit Trend"),
            "Month",
            "Profit",
        )

st.markdown("<div style='height:0.9rem;'></div>", unsafe_allow_html=True)

with st.container():
    render_section_card(
        "Commercial Mix",
        "Compare where sales are concentrated geographically and which customer segments are driving the strongest share of revenue.",
    )
    col3, col4 = st.columns(2)
    with col3:
        show_chart(
            horizontal_bar_chart(
                region_summary.sort_values("sales", ascending=True),
                "sales",
                "region",
                "region",
                "Top Regions by Sales",
            ),
            "Sales",
            "Region",
        )
    with col4:
        show_chart(
            horizontal_bar_chart(
                segment_summary.sort_values("sales", ascending=True),
                "sales",
                "segment",
                "segment",
                "Sales by Segment",
            ),
            "Sales",
            "Segment",
        )

st.markdown("<div style='height:0.9rem;'></div>", unsafe_allow_html=True)

with st.container():
    render_section_card(
        "Executive Insight Panel",
        "Use these short reads to connect the dashboard signals with commercial interpretation and decision-making.",
    )
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    with insight_col1:
        render_insight(
            "What To Notice",
            f"Revenue is led by {top_region}, while {top_segment} is the strongest segment in the current filtered view.",
            tone="blue",
        )
    with insight_col2:
        render_insight(
            "Business Insight",
            "The strongest executive read comes from comparing growth with profitability instead of treating top-line expansion as success on its own.",
            tone="teal",
        )
    with insight_col3:
        render_insight(
            "Decision Angle",
            "Use this page to decide where leadership attention should go next: scaling strong segments, fixing margin pressure, or rebalancing regional concentration.",
            tone="blue",
        )
