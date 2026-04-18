import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.kpi_cards import render_insight, render_page_intro


ensure_project_on_path()

render_page_intro(
    "Project Architecture",
    "Project Methodology",
    "The workflow behind the interface, from raw retail data ingestion to deployable business-facing analytics delivery.",
)

st.markdown("### Workflow")
st.markdown(
    """
    1. Raw retail transaction data was loaded and validated.
    2. The dataset was standardized, cleaned, and enriched with time and margin features.
    3. Exploratory analysis identified revenue, profit, customer, geographic, and product patterns.
    4. RFM segmentation translated transaction history into actionable customer groups.
    5. A proxy churn-risk model scored customers using recency and behavioral features.
    6. A 90-day forecast created a forward-looking planning layer for decision-makers.
    7. Dashboard-ready outputs were structured for both Power BI and Streamlit delivery.
    """
)

render_insight(
    "Portfolio Positioning",
    "This project demonstrates the full analytics lifecycle: data engineering, business analysis, customer intelligence, machine learning, forecasting, dashboard design, and deployment readiness.",
)

col1, col2 = st.columns(2)
with col1:
    render_insight(
        "Why This Structure Works",
        "The project separates raw data, cleaned data, processed outputs, modeling logic, notebooks, and dashboard code. That makes the work easier to validate, maintain, and explain professionally.",
        tone="blue",
    )
with col2:
    render_insight(
        "Recruiter Signal",
        "A strong portfolio project is not just an analysis notebook. It shows end-to-end thinking: reusable scripts, business framing, deployment readiness, and clear stakeholder communication.",
        tone="teal",
    )
