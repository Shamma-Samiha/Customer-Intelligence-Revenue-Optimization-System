import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.charts import donut_chart, horizontal_bar_chart, scatter_chart
from webapp.components.kpi_cards import render_insight, render_kpi_row, render_page_intro
from webapp.components.tables import show_table
from webapp.utils.formatters import money
from webapp.utils.loaders import load_all_data


ensure_project_on_path()

data = load_all_data()
rfm = data["rfm"]
render_page_intro(
    "Customer Value Lens",
    "Customer Intelligence",
    "RFM segmentation reframes transaction history into a customer strategy: who creates outsized value, who is drifting, and where retention effort should be focused.",
)

segment_summary = rfm.groupby("rfm_segment", as_index=False).agg(
    customers=("customer_id", "nunique"),
    revenue=("monetary", "sum"),
    avg_recency=("recency", "mean"),
).sort_values("revenue", ascending=False)
top_customers = rfm.nlargest(15, "monetary")[["customer_name", "rfm_segment", "recency", "frequency", "monetary"]]

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
    "RFM is useful because it turns raw purchasing behavior into something operational. It separates high-value relationships worth protecting from customers whose inactivity or lower engagement suggests a very different strategy.",
)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(horizontal_bar_chart(segment_summary, "customers", "rfm_segment", "rfm_segment", "Customer Count by RFM Segment"), use_container_width=True)
with col2:
    st.plotly_chart(donut_chart(segment_summary, "rfm_segment", "revenue", "Revenue Mix by Segment"), use_container_width=True)

col3, col4 = st.columns([1.25, 0.75])
with col3:
    st.plotly_chart(
        scatter_chart(rfm, "recency", "monetary", "rfm_segment", "Recency vs Monetary by Segment"),
        use_container_width=True,
    )
with col4:
    render_insight(
        "How To Read This",
        "Customers toward the upper-left are especially valuable because they combine recent engagement with strong monetary contribution. Lower-right clusters are the ones to monitor more carefully.",
        tone="blue",
    )
    render_insight(
        "Business Use",
        "This view supports loyalty planning, premium account reviews, and reactivation targeting. It helps explain not only who is valuable, but how current that value really is.",
        tone="teal",
    )

show_table(top_customers, "Top Customers by Monetary Value")

render_insight(
    "Recruiter Angle",
    "This page works because it connects analysis to action. Instead of just showing a segmentation chart, it makes it easy to discuss targeting, retention, and commercial prioritization in business language.",
    tone="blue",
)
