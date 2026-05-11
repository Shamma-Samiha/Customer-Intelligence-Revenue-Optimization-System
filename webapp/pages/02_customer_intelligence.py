import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.charts import donut_chart, horizontal_bar_chart, render_chart, scatter_chart
from webapp.components.kpi_cards import (
    render_dashboard_hero,
    render_info_card,
    render_insight,
    render_kpi_row,
    render_page_spacer,
    render_section_header,
)
from webapp.components.tables import show_table
from webapp.utils.formatters import compact_number, days, money
from webapp.utils.loaders import load_all_data
from webapp.utils.theme import apply_theme


ensure_project_on_path()
apply_theme()

data = load_all_data()
rfm = data["rfm"].copy()

st.sidebar.markdown("## Customer Controls")
segments = sorted(rfm["rfm_segment"].dropna().unique().tolist())
if st.sidebar.button("Reset customer view", use_container_width=True):
    st.session_state["customer_segments"] = segments
    st.session_state["customer_min_revenue"] = 0
    st.session_state["customer_top_n"] = 12
selected_segments = st.sidebar.multiselect("RFM Segment", segments, default=segments, key="customer_segments")
min_revenue = st.sidebar.slider(
    "Minimum customer revenue",
    0,
    int(rfm["monetary"].max()),
    0,
    step=max(1, int(rfm["monetary"].max() / 100)),
    key="customer_min_revenue",
)
top_n = st.sidebar.slider("Customers to show", 5, 30, 12, key="customer_top_n")
rfm = rfm[rfm["rfm_segment"].isin(selected_segments) & (rfm["monetary"] >= min_revenue)].copy()

segment_summary = (
    rfm.groupby("rfm_segment", as_index=False)
    .agg(
        customers=("customer_id", "nunique"),
        revenue=("monetary", "sum"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
    )
    .sort_values("revenue", ascending=False)
)
top_segment = segment_summary.iloc[0]["rfm_segment"] if not segment_summary.empty else "N/A"
top_customers = (
    rfm.nlargest(top_n, "monetary")[
        ["customer_name", "rfm_segment", "recency", "frequency", "monetary"]
    ]
    .rename(
        columns={
            "customer_name": "Customer",
            "rfm_segment": "Segment",
            "recency": "Recency",
            "frequency": "Frequency",
            "monetary": "Revenue",
        }
    )
)

render_dashboard_hero(
    "Customer Value Lens",
    "Customer Intelligence",
    "See which customers buy often, spend the most, and may need a different follow-up plan.",
    badges=[
        f"Top Segment: {top_segment}",
        f"Customer Base: {rfm['customer_id'].nunique():,}",
        f"Avg Recency: {int(rfm['recency'].mean()):,} days",
    ],
)

render_kpi_row(
    [
        ("Total Customers", compact_number(rfm["customer_id"].nunique())),
        ("Average Revenue", money(rfm["monetary"].mean())),
        ("Top Segment", top_segment),
        ("Avg Recency", days(rfm["recency"].mean())),
    ]
)

render_page_spacer(0.9)

render_section_header(
    "Customer Portfolio Snapshot",
    "A quick look at customer value: who makes up the base, who brings in revenue, and who has been active recently.",
)

col1, col2 = st.columns(2)
with col1:
    render_chart(
        horizontal_bar_chart(
            segment_summary.sort_values("customers", ascending=True),
            "customers",
            "rfm_segment",
            "rfm_segment",
            "RFM Segment Distribution",
        ),
        "Customers",
        "Segment",
    )
with col2:
    render_chart(
        donut_chart(segment_summary, "rfm_segment", "revenue", "Revenue Share by Segment"),
        "",
        "",
    )

col3, col4 = st.columns(2)
with col3:
    render_chart(
        scatter_chart(
            rfm,
            "recency",
            "monetary",
            "rfm_segment",
            "Customer Distribution: Recency vs Revenue",
        ),
        "Recency (days)",
        "Revenue",
    )
with col4:
    render_chart(
        scatter_chart(
            rfm,
            "frequency",
            "monetary",
            "rfm_segment",
            "Customer Distribution: Frequency vs Revenue",
        ),
        "Order Frequency",
        "Revenue",
    )

render_page_spacer(0.6)

render_section_header(
    "Interpretation Layer",
    "Use these notes to turn the segment mix into outreach, retention, and account priority decisions.",
)

insight_col1, insight_col2, insight_col3 = st.columns(3)
with insight_col1:
    render_insight(
        "What To Notice",
        f"{top_segment} brings in the most revenue in this view, so a small group of customers is carrying a large share of value.",
        tone="blue",
    )
with insight_col2:
    render_insight(
        "Business Insight",
        "High-spend customers who have not ordered recently are worth a direct check-in before they drift further away.",
        tone="teal",
    )
with insight_col3:
    render_insight(
        "Decision Angle",
        "Treat loyal buyers, at-risk customers, and occasional shoppers differently instead of sending the same campaign to everyone.",
        tone="blue",
    )

render_page_spacer(0.45)

detail_col1, detail_col2 = st.columns([1.2, 0.8])
with detail_col1:
    show_table(top_customers, "Highest-Value Customers")
with detail_col2:
    render_info_card(
        "Top Segment Readout",
        f"{top_segment} is the biggest revenue segment after filtering. Keep this group visible when planning service, offers, and retention work.",
    )
    render_info_card(
        "Coverage Signal",
        f"This view includes {compact_number(rfm['customer_id'].nunique())} customers after filtering.",
    )
