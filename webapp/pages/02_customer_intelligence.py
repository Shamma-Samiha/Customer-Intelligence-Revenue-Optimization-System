import streamlit as st

from webapp.components.charts import bar_chart, scatter_chart
from webapp.components.tables import show_table
from webapp.utils.loaders import load_all_data


st.title("Customer Intelligence")
st.caption("RFM segmentation, customer value concentration, and customer-level behavior analysis.")

data = load_all_data()
rfm = data["rfm"]

segment_summary = rfm.groupby("rfm_segment", as_index=False).agg(
    customers=("customer_id", "nunique"),
    revenue=("monetary", "sum"),
    avg_recency=("recency", "mean"),
)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(segment_summary, "rfm_segment", "customers", "rfm_segment", "Customers by RFM Segment"), use_container_width=True)
with col2:
    st.plotly_chart(bar_chart(segment_summary, "rfm_segment", "revenue", "rfm_segment", "Revenue by RFM Segment"), use_container_width=True)

st.plotly_chart(
    scatter_chart(rfm, "recency", "monetary", "rfm_segment", "Recency vs Monetary by Customer Segment"),
    use_container_width=True,
)

show_table(rfm.head(25), "Top Customers by RFM Score")
