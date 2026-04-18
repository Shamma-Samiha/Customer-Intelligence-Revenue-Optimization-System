import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.kpi_cards import render_insight
from webapp.utils.loaders import validate_app_data


project_root = ensure_project_on_path()

st.set_page_config(
    page_title="Customer Intelligence & Revenue Forecasting System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = Path(__file__).resolve().parent / "assets" / "styles.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero">
        <div style="font-size:13px; letter-spacing:0.14em; text-transform:uppercase; opacity:0.85;">Analytics Portfolio Project</div>
        <h1 style="margin:8px 0 10px;">Customer Intelligence & Revenue Forecasting System</h1>
        <p style="font-size:1.05rem; max-width:900px; line-height:1.7; margin:0;">
            A recruiter-ready retail analytics platform combining exploratory analysis, RFM segmentation,
            churn-risk modeling, and 90-day revenue forecasting in one polished business-facing application.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

missing = validate_app_data()
if missing:
    st.error(
        "The app is missing required data files: "
        + ", ".join(missing)
        + ". Run `python scripts/run_pipeline.py` before launching or deploying the app."
    )

st.sidebar.markdown("## Navigation")
st.sidebar.caption("Use the pages below to move through the analytics story.")
st.sidebar.success(f"Deployment root: `{project_root.name}`")

st.markdown('<div class="section-header">Platform Overview</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">A polished analytics workspace that turns a retail transaction dataset into a strategic story about growth, customer value, churn risk, and revenue planning.</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1.15, 1])
with col1:
    render_insight(
        "What This App Covers",
        "Move from an executive performance snapshot into customer segmentation, retention risk, forward-looking forecasting, and the methodology that ties the whole product together.",
        tone="blue",
    )
with col2:
    render_insight(
        "Why It Feels Different",
        "The experience is built to read like a business product rather than a notebook export: cleaner hierarchy, curated metrics, clearer charts, and insights written for decision-makers.",
        tone="teal",
    )

col3, col4, col5 = st.columns(3)
with col3:
    render_insight(
        "Executive Summary",
        "Track scale, profitability, regional strength, and forecast direction at a glance.",
        tone="teal",
    )
with col4:
    render_insight(
        "Customer Intelligence",
        "See who creates value, which segments deserve protection, and where reactivation is needed.",
        tone="blue",
    )
with col5:
    render_insight(
        "Decision Support",
        "Translate historical transactions into targeting, retention, and planning conversations.",
        tone="rose",
    )
