from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Customer Intelligence & Revenue Forecasting System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = Path(__file__).resolve().parent / "assets" / "styles.css"
st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.markdown(
    '''
    <div class="hero">
        <div style="font-size:13px; letter-spacing:0.14em; text-transform:uppercase; opacity:0.85;">Analytics Portfolio Project</div>
        <h1 style="margin:8px 0 10px;">Customer Intelligence & Revenue Forecasting System</h1>
        <p style="font-size:1.05rem; max-width:900px; line-height:1.7; margin:0;">
            A recruiter-ready retail analytics platform combining exploratory analysis, RFM segmentation,
            churn-risk modeling, and 90-day revenue forecasting in one polished business-facing application.
        </p>
    </div>
    ''',
    unsafe_allow_html=True,
)

st.markdown("### App Navigation")
st.write("Use the page menu in the sidebar to explore Executive Overview, Customer Intelligence, Churn Risk, Revenue Forecast, and Project Methodology.")
