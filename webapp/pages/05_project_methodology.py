import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.kpi_cards import (
    render_dashboard_hero,
    render_info_card,
    render_insight,
    render_kpi_row,
    render_page_spacer,
    render_section_header,
)
from webapp.utils.theme import apply_theme


ensure_project_on_path()
apply_theme()

render_dashboard_hero(
    "Project Architecture",
    "Project Methodology",
    "How the project moves from raw retail data to dashboard pages, customer scoring, churn risk, and forecasting.",
    badges=[
        "Data Pipeline to Dashboard",
        "Reusable Analytics Workflow",
        "Recruiter-Ready Delivery",
    ],
)

render_kpi_row(
    [
        ("Pipeline Stages", "7"),
        ("Core Models", "3"),
        ("Delivery Modes", "2"),
        ("Project Scope", "End-to-End"),
    ]
)

render_page_spacer(0.9)

render_section_header(
    "Methodology Overview",
    "A plain-English look at the pipeline, modeling choices, and app structure behind the dashboard.",
)

col1, col2 = st.columns(2)
with col1:
    render_info_card(
        "Data Pipeline",
        "The workflow starts with retail transactions, cleans and validates them, then exports datasets used by both notebooks and the Streamlit app.",
    )
with col2:
    render_info_card(
        "Modeling",
        "The project uses exploratory analysis, RFM segmentation, churn-risk scoring, and revenue forecasting. Each piece answers a different business question.",
    )

col3, col4 = st.columns(2)
with col3:
    render_info_card(
        "Tools Used",
        "The app is built with Python, pandas, Plotly, Streamlit, and notebooks for the analysis workflow.",
    )
with col4:
    render_info_card(
        "Delivery Output",
        "The repo keeps scripts, processed outputs, dashboard pages, and documentation in separate places so the work is easier to review and rerun.",
    )

render_page_spacer(0.55)

render_section_header(
    "Why The Workflow Matters",
    "The structure matters because it shows how the analysis can be rerun, explained, and used in a dashboard.",
)

insight_col1, insight_col2, insight_col3 = st.columns(3)
with insight_col1:
    render_insight(
        "What To Notice",
        "Data loading, transformation, modeling, and presentation are kept separate. That makes the project easier to maintain and explain.",
        tone="blue",
    )
with insight_col2:
    render_insight(
        "Business Insight",
        "Each analytic step maps to a business use case: customer priority, churn prevention, performance tracking, or revenue planning.",
        tone="teal",
    )
with insight_col3:
    render_insight(
        "Decision Angle",
        "The page shows both technical workflow and business delivery, which makes the project easier to discuss in a review.",
        tone="blue",
    )
