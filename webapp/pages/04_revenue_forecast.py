import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path, load_app_styles
from webapp.components.charts import area_line_chart, forecast_chart
from webapp.components.kpi_cards import (
    render_info_card,
    render_insight,
    render_kpi_row,
    render_page_intro,
    render_section_header,
)
from webapp.components.tables import show_table
from webapp.utils.formatters import compact_number, money, pct
from webapp.utils.loaders import load_all_data


def show_chart(fig, x_title: str, y_title: str) -> None:
    fig.update_xaxes(title=x_title)
    fig.update_yaxes(title=y_title)
    st.plotly_chart(fig, use_container_width=True)


ensure_project_on_path()
load_app_styles()

data = load_all_data()
forecast = data["forecast"].copy().sort_values("ds")
history = (
    forecast.loc[forecast["yhat"].eq(forecast["yhat_lower"]) & forecast["yhat"].eq(forecast["yhat_upper"])]
    if {"yhat_lower", "yhat_upper"}.issubset(forecast.columns)
    else forecast.iloc[:-90]
)
future = (
    forecast.loc[~forecast.index.isin(history.index)].copy()
    if not history.empty
    else forecast.tail(90).copy()
)
if future.empty:
    future = forecast.tail(90).copy()
    history = forecast.iloc[:-len(future)].copy()

last_30_actual = history.tail(30)["yhat"].sum() if not history.empty else 0
next_30_forecast = future.head(30)["yhat"].sum() if not future.empty else 0
growth_rate = (next_30_forecast - last_30_actual) / last_30_actual if last_30_actual else 0

history_vs_forecast = pd.concat(
    [
        history.assign(series="Historical")[["ds", "yhat", "series"]],
        future.assign(series="Forecast")[["ds", "yhat", "series"]],
    ],
    ignore_index=True,
)
weekly_forecast = future.copy()
weekly_forecast["week"] = weekly_forecast["ds"].dt.to_period("W").astype(str)
weekly_summary = weekly_forecast.groupby("week", as_index=False)["yhat"].sum().tail(10)
monthly_history = history.copy()
if not monthly_history.empty:
    monthly_history["month"] = monthly_history["ds"].dt.to_period("M").astype(str)
    monthly_summary = monthly_history.groupby("month", as_index=False)["yhat"].sum().tail(12)
else:
    monthly_summary = pd.DataFrame(columns=["month", "yhat"])

forecast_preview = (
    future.head(14)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    .rename(
        columns={
            "ds": "Date",
            "yhat": "Forecast",
            "yhat_lower": "Lower Bound",
            "yhat_upper": "Upper Bound",
        }
    )
)

render_page_intro(
    "Forward Planning Layer",
    "Revenue Forecast",
    "A polished planning view that connects historical sales momentum with the projected revenue path ahead, making the forecast easier to use in budgeting and growth conversations.",
)

render_kpi_row(
    [
        ("Forecasted Revenue", money(future["yhat"].sum())),
        ("Growth Rate", pct(growth_rate)),
        ("Forecast Horizon", f"{compact_number(len(future))} days"),
        ("Peak Forecast Day", money(future["yhat"].max())),
    ]
)

render_section_header(
    "Performance Outlook",
    "The goal here is to compare current momentum with the modeled path ahead, then highlight whether the next planning window points to acceleration, stabilization, or softer revenue expectations.",
)

col1, col2 = st.columns(2)
with col1:
    show_chart(forecast_chart(forecast, "Historical vs Forecast Revenue"), "Date", "Revenue")
with col2:
    forecast_mix = px.line(
        history_vs_forecast,
        x="ds",
        y="yhat",
        color="series",
        title="Historical vs Forecast Trend",
        color_discrete_map={"Historical": "#0f766e", "Forecast": "#1d4ed8"},
    )
    forecast_mix.update_layout(
        legend=dict(orientation="h", x=0, y=1.05),
        margin=dict(l=16, r=16, t=64, b=16),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="Inter, Segoe UI, sans-serif", color="#0f172a"),
        title_font=dict(size=24, color="#0f172a"),
    )
    forecast_mix.update_traces(mode="lines", line=dict(width=3))
    show_chart(forecast_mix, "Date", "Revenue")

col3, col4 = st.columns(2)
with col3:
    show_chart(
        area_line_chart(weekly_summary, "week", "yhat", "Weekly Forecasted Revenue"),
        "Week",
        "Forecast Revenue",
    )
with col4:
    if monthly_summary.empty:
        render_info_card(
            "Trend Readout",
            "Historical monthly data is not available in the current forecast extract, so the page centers on the future revenue path and planning horizon instead.",
        )
    else:
        show_chart(
            area_line_chart(monthly_summary, "month", "yhat", "Recent Historical Revenue"),
            "Month",
            "Revenue",
        )

render_section_header(
    "Future Insights",
    "A good forecast page should help a stakeholder talk about planning, not just prediction. These blocks turn the model output into practical decision signals.",
)

insight_col1, insight_col2, insight_col3 = st.columns(3)
with insight_col1:
    render_insight(
        "What To Notice",
        f"The current model projects {money(future['yhat'].sum())} across the forecast horizon, with the next 30-day window implying a {pct(growth_rate)} move versus the latest 30-day actual baseline.",
        tone="blue",
    )
with insight_col2:
    render_insight(
        "Business Insight",
        "Look for whether expected peaks cluster around a few periods or appear more evenly spread. Concentrated peaks create staffing and inventory pressure even when total revenue looks healthy.",
        tone="teal",
    )
with insight_col3:
    render_insight(
        "Decision Angle",
        "Use the forecast as a planning range for commercial targets, cash expectations, and operating readiness rather than treating it as a single guaranteed outcome.",
        tone="blue",
    )

detail_col1, detail_col2 = st.columns([1.2, 0.8])
with detail_col1:
    show_table(forecast_preview, "Forecast Horizon Preview")
with detail_col2:
    render_info_card(
        "Planning Recommendation",
        "Track actual revenue against this forecast weekly. That cadence makes it easier to catch divergence early and update operating assumptions before they become budget problems.",
    )
    render_info_card(
        "Signal Quality",
        "The confidence band gives leadership a better planning frame than a single point estimate, especially when discussing stretch targets or downside protection.",
    )
