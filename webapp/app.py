from pathlib import Path

import streamlit as st

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
    '<div class="section-subtitle">This Streamlit experience packages the full analytics workflow into a presentation-ready application for recruiters, hiring managers, and stakeholders.</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1.2, 1])
with col1:
    render_insight(
        "What This App Covers",
        "Executive KPIs, customer intelligence, churn-risk prioritization, revenue forecasting, and project methodology are all available through the sidebar page flow.",
        tone="blue",
    )
with col2:
    render_insight(
        "Deployment Notes",
        "The app uses repository-relative paths, cached CSV loading, and package-safe imports so it can deploy cleanly on Streamlit Community Cloud.",
        tone="teal",
    )

st.markdown("### App Navigation")
st.write("Open the sidebar pages to walk from business summary to customer strategy, retention risk, forecasting, and methodology.")
