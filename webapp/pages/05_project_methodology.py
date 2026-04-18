import streamlit as st

from webapp.bootstrap import ensure_project_on_path
from webapp.components.kpi_cards import render_insight


ensure_project_on_path()

st.title("Project Methodology")
st.caption("How the end-to-end analytics workflow was structured from raw retail data to deployable decision support.")

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
