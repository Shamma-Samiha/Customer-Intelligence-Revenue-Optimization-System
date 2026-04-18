import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.charts import area_line_chart, horizontal_bar_chart, line_chart
from webapp.components.kpi_cards import render_insight, render_kpi_row, render_page_intro
from webapp.utils.filters import sidebar_filters
from webapp.utils.formatters import money
from webapp.utils.loaders import load_all_data


ensure_project_on_path()

data = load_all_data()
orders = sidebar_filters(data["orders"])
forecast = data["forecast"]
profit_margin = orders["profit"].sum() / orders["sales"].sum() if orders["sales"].sum() else 0
avg_order_value = orders["sales"].sum() / orders["order_id"].nunique() if orders["order_id"].nunique() else 0

render_page_intro(
    "Leadership Dashboard",
    "Executive Overview",
    "A leadership-ready summary of scale, profitability, operating footprint, and forward-looking revenue momentum.",
)

render_kpi_row(
    [
        ("Total Sales", money(orders["sales"].sum())),
        ("Total Profit", money(orders["profit"].sum())),
        ("Avg Order Value", money(avg_order_value)),
        ("Profit Margin", f"{profit_margin:.1%}"),
    ]
)

monthly = orders.groupby("year_month", as_index=False)[["sales", "profit"]].sum()
region_summary = (
    orders.groupby("region", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
    .head(10)
)
segment_summary = (
    orders.groupby("segment", as_index=False)[["sales", "profit"]]
    .sum()
    .assign(profit_margin=lambda x: x["profit"] / x["sales"])
    .sort_values("sales", ascending=False)
)

render_insight(
    "Executive Readout",
    f"Revenue currently stands at {money(orders['sales'].sum())} with a profit pool of {money(orders['profit'].sum())}. The strongest leadership view comes from pairing that scale with margin quality and regional concentration rather than treating growth alone as success.",
)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(area_line_chart(monthly, "year_month", "sales", "Monthly Sales Momentum"), use_container_width=True)
with col2:
    st.plotly_chart(line_chart(monthly, "year_month", "profit", "Monthly Profit Trend"), use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(horizontal_bar_chart(region_summary, "sales", "region", "region", "Top Regions by Sales"), use_container_width=True)
with col4:
    st.plotly_chart(line_chart(forecast.tail(120), "ds", "yhat", "Revenue Forecast Outlook"), use_container_width=True)

col5, col6 = st.columns([1.1, 0.9])
with col5:
    st.plotly_chart(horizontal_bar_chart(segment_summary, "sales", "segment", "segment", "Sales by Customer Segment"), use_container_width=True)
with col6:
    top_segment = segment_summary.iloc[0]["segment"] if not segment_summary.empty else "N/A"
    render_insight(
        "What To Notice",
        f"The filtered view highlights how performance is distributed across segments and regions. Right now, the leading segment is {top_segment}, which helps explain where current commercial strength is concentrated.",
        tone="blue",
    )
    render_insight(
        "Decision Angle",
        "Executives should use this page to ask whether the strongest revenue pools are also the most profitable and whether recent momentum supports confident planning assumptions.",
        tone="teal",
    )
