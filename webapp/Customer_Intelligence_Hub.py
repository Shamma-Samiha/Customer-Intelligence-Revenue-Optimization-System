import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.kpi_cards import (
    render_action_grid,
    render_dashboard_hero,
    render_info_card,
    render_insight,
    render_page_spacer,
    render_section_header,
)
from webapp.utils.loaders import validate_app_data
from webapp.utils.theme import apply_theme


project_root = ensure_project_on_path()

st.set_page_config(
    page_title="Customer Intelligence & Revenue Forecasting System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

render_dashboard_hero(
    "Analytics Portfolio Project",
    "Customer Intelligence & Revenue Forecasting System",
    "A retail analytics dashboard for sales performance, customer segments, churn risk, and revenue forecasting.",
    badges=[
        "Executive KPI Storytelling",
        "Customer Segmentation + Churn",
        "Forecasting + Dashboard Delivery",
    ],
)

st.sidebar.markdown("## Data")
st.sidebar.caption(f"Project root: `{project_root.name}`")
if st.sidebar.button("Refresh data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

missing = validate_app_data()
if missing:
    st.error(
        "The app is missing required data files: "
        + ", ".join(missing)
        + ". Run `python scripts/run_pipeline.py` before launching or deploying the app."
    )

render_section_header(
    "Platform Overview",
    "Start here, then open a page for the part of the business you want to review.",
)

overview_col1, overview_col2 = st.columns([1.15, 1])
with overview_col1:
    render_insight(
        "What This App Covers",
        "Review sales performance, customer value, churn risk, forecast trends, and the project workflow.",
        tone="blue",
    )
with overview_col2:
    render_insight(
        "Why It Feels Different",
        "The pages are built for quick review: filters on the side, charts in the center, and short notes beside the numbers.",
        tone="teal",
    )

render_page_spacer(0.5)

feature_col1, feature_col2, feature_col3 = st.columns(3)
with feature_col1:
    render_insight(
        "Executive Summary",
        "Track scale, profitability, regional strength, and forecast direction at a glance.",
        tone="teal",
    )
with feature_col2:
    render_insight(
        "Customer Intelligence",
        "See who creates value, which segments deserve protection, and where reactivation is needed.",
        tone="blue",
    )
with feature_col3:
    render_insight(
        "Decision Support",
        "Use past orders to guide targeting, retention, and planning.",
        tone="rose",
    )

render_page_spacer(0.55)

render_section_header(
    "Explore The Workspace",
    "Open a page, adjust the filters, hover through the charts, and export the tables you need.",
)
render_action_grid(
    [
        (
            "Executive Overview",
            "Revenue, profit, region, and segment performance.",
            "pages/01_executive_overview.py",
        ),
        (
            "Customer Intelligence",
            "RFM segments, value concentration, and account priority.",
            "pages/02_customer_intelligence.py",
        ),
        (
            "Churn Risk",
            "Retention severity, churn drivers, and risk tables.",
            "pages/03_churn_risk.py",
        ),
    ]
)
render_page_spacer(0.35)
render_action_grid(
    [
        (
            "Revenue Forecast",
            "Historical momentum, future outlook, and forecast export.",
            "pages/04_revenue_forecast.py",
        ),
        (
            "Methodology",
            "Project architecture, modeling flow, and delivery notes.",
            "pages/05_project_methodology.py",
        ),
    ]
)

render_page_spacer(0.55)

detail_col1, detail_col2 = st.columns(2)
with detail_col1:
    render_info_card(
        "How To Navigate",
        "Start with Executive Overview, then move into customers, churn, and forecasting depending on the question you are answering.",
    )
with detail_col2:
    render_info_card(
        "Portfolio Signal",
        "This project shows the full flow: cleaned data, reusable scripts, models, charts, and a working dashboard.",
    )
