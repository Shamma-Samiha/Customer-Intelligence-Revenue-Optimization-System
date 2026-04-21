import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.kpi_cards import (
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
    "A recruiter-ready retail analytics product that turns transaction history into executive performance reporting, customer intelligence, churn-risk monitoring, and forward-looking revenue planning.",
    badges=[
        "Executive KPI Storytelling",
        "Customer Segmentation + Churn",
        "Forecasting + Dashboard Delivery",
    ],
)

st.sidebar.markdown("## Navigation")
st.sidebar.caption("Use the pages below to move through the analytics story.")
st.sidebar.success(f"Deployment root: `{project_root.name}`")

missing = validate_app_data()
if missing:
    st.error(
        "The app is missing required data files: "
        + ", ".join(missing)
        + ". Run `python scripts/run_pipeline.py` before launching or deploying the app."
    )

render_section_header(
    "Platform Overview",
    "The app is structured like a modern analytics workspace: clean hierarchy, focused KPI summaries, business-facing charts, and short narrative blocks that help the viewer move from metrics to decisions.",
)

overview_col1, overview_col2 = st.columns([1.15, 1])
with overview_col1:
    render_insight(
        "What This App Covers",
        "Move from an executive performance snapshot into customer segmentation, retention risk, forward-looking forecasting, and the methodology that ties the whole product together.",
        tone="blue",
    )
with overview_col2:
    render_insight(
        "Why It Feels Different",
        "The experience is built to read like a business product rather than a notebook export: cleaner hierarchy, curated metrics, clearer charts, and insights written for decision-makers.",
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
        "Translate historical transactions into targeting, retention, and planning conversations.",
        tone="rose",
    )

render_page_spacer(0.55)

detail_col1, detail_col2 = st.columns(2)
with detail_col1:
    render_info_card(
        "How To Navigate",
        "Start with Executive Overview for the operating snapshot, then move into Customer Intelligence, Churn Risk, and Revenue Forecast to understand where commercial action should go next.",
    )
with detail_col2:
    render_info_card(
        "Portfolio Signal",
        "This project is intentionally presented as a polished analytics product, showing not just modeling capability but also structured decision support and frontend dashboard design.",
    )
