import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.charts import area_line_chart, forecast_chart
from webapp.components.kpi_cards import render_insight, render_kpi_row, render_page_intro
from webapp.components.tables import show_table
from webapp.utils.formatters import money
from webapp.utils.loaders import load_all_data


ensure_project_on_path()

data = load_all_data()
forecast = data["forecast"]
future_only = forecast[forecast["yhat_lower"] != forecast["yhat"]].copy() if "yhat_lower" in forecast.columns else forecast.tail(90).copy()
render_page_intro(
    "Forward Planning Layer",
    "Revenue Forecast",
    "A forward-looking view that extends the historical sales pattern into a 90-day planning horizon for budgeting, staffing, and stakeholder communication.",
)

render_kpi_row(
    [
        ("Forecast Horizon", f"{len(future_only):,} days"),
        ("Projected Revenue", money(future_only["yhat"].sum())),
        ("Avg Daily Forecast", money(future_only["yhat"].mean())),
        ("Peak Forecast Day", money(future_only["yhat"].max())),
    ]
)

render_insight(
    "Planning Lens",
    "Forecasting makes the app more strategic. It shifts the story from reporting what happened to preparing for what is likely to happen next, which is where decision support becomes most valuable.",
)

col1, col2 = st.columns([1.15, 0.85])
with col1:
    st.plotly_chart(forecast_chart(forecast, "Revenue Forecast"), use_container_width=True)
with col2:
    weekly = future_only.copy()
    weekly["week"] = weekly["ds"].dt.to_period("W").astype(str)
    weekly_summary = weekly.groupby("week", as_index=False)["yhat"].sum().tail(10)
    st.plotly_chart(area_line_chart(weekly_summary, "week", "yhat", "Weekly Forecasted Revenue", color="#1d4ed8"), use_container_width=True)

render_insight(
    "How To Use This",
    "Use the forecast to frame commercial planning conversations: expected revenue rhythm, likely peaks, and whether current momentum supports aggressive or conservative operating assumptions.",
    tone="blue",
)

show_table(forecast.tail(30), "Forecast Horizon Preview")
