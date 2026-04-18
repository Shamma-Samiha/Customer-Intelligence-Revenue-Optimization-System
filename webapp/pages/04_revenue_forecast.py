import streamlit as st

from webapp.bootstrap import ensure_project_on_path
from webapp.components.charts import forecast_chart
from webapp.components.kpi_cards import render_insight, render_kpi_row
from webapp.components.tables import show_table
from webapp.utils.formatters import money
from webapp.utils.loaders import load_all_data


ensure_project_on_path()

st.title("Revenue Forecast")
st.caption("Forward-looking revenue planning view based on the daily sales time series and 90-day forecast output.")

data = load_all_data()
forecast = data["forecast"]
future_only = forecast[forecast["yhat_lower"] != forecast["yhat"]].copy() if "yhat_lower" in forecast.columns else forecast.tail(90).copy()

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
    "Forecasting strengthens the project by adding a forward-looking layer. It shifts the conversation from what happened to what the business should prepare for next.",
)

st.plotly_chart(forecast_chart(forecast, "Revenue Forecast"), use_container_width=True)
show_table(forecast.tail(30), "Forecast Horizon Preview")
