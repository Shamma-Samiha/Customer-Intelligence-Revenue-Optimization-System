import streamlit as st


st.title("Project Methodology")
st.caption("How the end-to-end analytics workflow was designed and delivered.")

st.markdown(
    '''
    1. Raw retail transaction data was loaded and validated.
    2. The dataset was standardized, cleaned, and enriched with time and margin features.
    3. Exploratory analysis identified revenue, profit, customer, geographic, and product patterns.
    4. RFM segmentation translated transaction history into actionable customer groups.
    5. A proxy churn-risk model scored customers using recency and behavioral features.
    6. A 90-day forecast created a forward-looking planning layer for decision-makers.
    7. Outputs were structured to support both Power BI and this Streamlit application.
    '''
)
