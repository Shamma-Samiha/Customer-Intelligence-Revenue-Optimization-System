import streamlit as st

from webapp.bootstrap import ensure_project_on_path
from webapp.components.charts import bar_chart, scatter_chart
from webapp.components.kpi_cards import render_insight, render_kpi_row
from webapp.components.tables import show_table
from webapp.utils.formatters import money
from webapp.utils.loaders import load_all_data


ensure_project_on_path()

st.title("Customer Intelligence")
st.caption("Customer value segmentation through RFM logic, commercial concentration, and behavioral performance signals.")

data = load_all_data()
rfm = data["rfm"]

segment_summary = rfm.groupby("rfm_segment", as_index=False).agg(
    customers=("customer_id", "nunique"),
    revenue=("monetary", "sum"),
    avg_recency=("recency", "mean"),
).sort_values("revenue", ascending=False)

render_kpi_row(
    [
        ("Customers Segmented", f"{rfm['customer_id'].nunique():,}"),
        ("VIP Revenue", money(rfm.loc[rfm["rfm_segment"] == "VIP Customers", "monetary"].sum())),
        ("At-Risk Customers", f"{(rfm['rfm_segment'] == 'At Risk Customers').sum():,}"),
        ("Average Customer Value", money(rfm["monetary"].mean())),
    ]
)

render_insight(
    "Why This Matters",
    "RFM segmentation converts purchase history into an actionable customer strategy. It helps distinguish premium accounts worth defending from lower-engagement customers who need reactivation attention.",
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

render_insight(
    "Recruiter Angle",
    "This page shows more than charts. It demonstrates the ability to connect customer-level behavior to targeting, retention, and commercial prioritization.",
    tone="blue",
)
