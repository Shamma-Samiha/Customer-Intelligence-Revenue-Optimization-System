import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.charts import horizontal_bar_chart, line_chart, render_chart
from webapp.components.kpi_cards import (
    render_dashboard_hero,
    render_insight,
    render_kpi_row,
    render_page_spacer,
    render_section_header,
)
from webapp.utils.filters import sidebar_filters
from webapp.utils.formatters import money
from webapp.utils.loaders import load_all_data
from webapp.utils.theme import apply_theme

ensure_project_on_path()
apply_theme()

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

render_dashboard_hero(
    "Leadership Dashboard",
    "Executive Overview",
    "A premium operating snapshot of revenue scale, profitability, regional concentration, and segment performance designed for fast business review and recruiter-ready storytelling.",
    badges=[
        f"Leading Region: {top_region}",
        f"Top Segment: {top_segment}",
        f"Orders in View: {total_orders:,}",
    ],
)

with st.container():
    render_kpi_row(
        [
            ("Total Sales", money(total_sales)),
            ("Total Profit", money(total_profit)),
            ("Avg Order Value", money(avg_order_value)),
            ("Profit Margin", f"{profit_margin:.1%}"),
        ]
    )

render_page_spacer(1.05)

with st.container():
    render_section_header(
        "Performance Momentum",
        "Track how revenue and profit evolve over time to understand whether scale is translating into healthier business performance.",
    )
    col1, col2 = st.columns(2)
    with col1:
        render_chart(
            line_chart(monthly, "year_month", "sales", "Monthly Sales Trend"),
            "Month",
            "Sales",
        )
    with col2:
        render_chart(
            line_chart(monthly, "year_month", "profit", "Monthly Profit Trend"),
            "Month",
            "Profit",
        )

render_page_spacer(0.9)

with st.container():
    render_section_header(
        "Commercial Mix",
        "Compare where sales are concentrated geographically and which customer segments are driving the strongest share of revenue.",
    )
    col3, col4 = st.columns(2)
    with col3:
        render_chart(
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
        render_chart(
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

render_page_spacer(0.9)

with st.container():
    render_section_header(
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
