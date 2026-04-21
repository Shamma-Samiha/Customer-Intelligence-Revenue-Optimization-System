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
    "A cleaner explanation of how the product moves from raw retail data to executive reporting, customer intelligence, churn scoring, and revenue forecasting.",
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
    "This page translates the build process into a recruiter-ready delivery story: data pipeline, modeling approach, and the tools that made the product deployable and business-facing.",
)

col1, col2 = st.columns(2)
with col1:
    render_info_card(
        "Data Pipeline",
        "The workflow starts with raw retail transactions, then moves through validation, cleaning, feature engineering, and export-ready structured datasets. That foundation supports both analysis notebooks and production-style app delivery.",
    )
with col2:
    render_info_card(
        "Modeling",
        "The analytics layer combines exploratory analysis, RFM segmentation, proxy churn-risk scoring, and 90-day revenue forecasting. Each model adds a distinct decision-support angle rather than repeating the same business story.",
    )

col3, col4 = st.columns(2)
with col3:
    render_info_card(
        "Tools Used",
        "Python, pandas, Plotly, Streamlit, and supporting notebook workflows were used to build a full-stack analytics artifact that can be demonstrated as both a technical and stakeholder-facing project.",
    )
with col4:
    render_info_card(
        "Delivery Output",
        "The final result is organized into reusable scripts, processed outputs, dashboard pages, and deployable app structure so the work reads like a product build instead of a one-off notebook analysis.",
    )

render_page_spacer(0.55)

render_section_header(
    "Why The Workflow Matters",
    "Strong portfolio projects show clear thinking about architecture and communication, not only charts and model output. These narrative cards make that structure visible.",
)

insight_col1, insight_col2, insight_col3 = st.columns(3)
with insight_col1:
    render_insight(
        "What To Notice",
        "The project separates ingestion, transformation, modeling, and presentation layers. That separation improves maintainability and makes the methodology easier to explain in interviews or demos.",
        tone="blue",
    )
with insight_col2:
    render_insight(
        "Business Insight",
        "Each analytic step is tied to a real business decision: customer prioritization, churn prevention, executive performance tracking, or forward planning.",
        tone="teal",
    )
with insight_col3:
    render_insight(
        "Decision Angle",
        "Recruiters and hiring managers can read this workflow as evidence of end-to-end ownership, from data engineering discipline through polished stakeholder delivery.",
        tone="blue",
    )
