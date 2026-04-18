import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.charts import bar_chart, line_chart
from webapp.components.kpi_cards import render_insight, render_kpi_row
from webapp.utils.filters import sidebar_filters
from webapp.utils.formatters import money
from webapp.utils.loaders import load_all_data


ensure_project_on_path()

st.title("Executive Overview")
st.caption("A leadership-ready summary of scale, profitability, operating footprint, and forward-looking revenue momentum.")

data = load_all_data()
orders = sidebar_filters(data["orders"])
kpis = data["kpis"].iloc[0]
forecast = data["forecast"]

render_kpi_row(
    [
        ("Total Sales", money(kpis["total_sales"])),
        ("Total Profit", money(kpis["total_profit"])),
        ("Total Orders", f"{int(kpis['total_orders']):,}"),
        ("Total Customers", f"{int(kpis['total_customers']):,}"),
    ]
)

monthly = orders.groupby("year_month", as_index=False)[["sales", "profit"]].sum()
region_summary = orders.groupby("region", as_index=False)["sales"].sum().sort_values("sales", ascending=False)

st.markdown("### Performance Story")
render_insight(
    "Executive Readout",
    "Use this page to assess whether top-line growth is translating into durable business value. The focus is not only on scale, but on the quality and trajectory of performance.",
)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(line_chart(monthly, "year_month", "sales", "Monthly Sales Trend"), use_container_width=True)
with col2:
    st.plotly_chart(line_chart(monthly, "year_month", "profit", "Monthly Profit Trend"), use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(bar_chart(region_summary, "region", "sales", "region", "Sales by Region"), use_container_width=True)
with col4:
    st.plotly_chart(line_chart(forecast.tail(120), "ds", "yhat", "Revenue Forecast Outlook"), use_container_width=True)

render_insight(
    "Business Interpretation",
    "This page is meant to answer the first stakeholder question quickly: how large the business is, where revenue is concentrated, and whether the short-term trend supports confident planning.",
    tone="blue",
)
