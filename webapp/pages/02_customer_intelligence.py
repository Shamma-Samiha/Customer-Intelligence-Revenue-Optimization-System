import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path, load_app_styles
from webapp.components.charts import donut_chart, horizontal_bar_chart, scatter_chart
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


def show_chart(fig, x_title: str, y_title: str) -> None:
    fig.update_xaxes(title=x_title)
    fig.update_yaxes(title=y_title)
    st.plotly_chart(fig, use_container_width=True)


ensure_project_on_path()
load_app_styles()

data = load_all_data()
rfm = data["rfm"].copy()

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
    rfm.nlargest(12, "monetary")[
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
    "A structured view of customer quality and value concentration, turning RFM outputs into a cleaner commercial dashboard for targeting, retention, and account prioritization.",
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
    "Use this section to understand how customer value is distributed, which segments dominate revenue, and where recent engagement is strongest.",
)

col1, col2 = st.columns(2)
with col1:
    show_chart(
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
    show_chart(
        donut_chart(segment_summary, "rfm_segment", "revenue", "Revenue Share by Segment"),
        "",
        "",
    )

col3, col4 = st.columns(2)
with col3:
    show_chart(
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
    show_chart(
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
    "The analytics are most useful when they help a stakeholder decide where to defend value, where to reactivate relationships, and where to keep premium service levels high.",
)

insight_col1, insight_col2, insight_col3 = st.columns(3)
with insight_col1:
    render_insight(
        "What To Notice",
        f"{top_segment} currently contributes the largest value pool, which means the strongest customer economics are concentrated rather than evenly spread across the portfolio.",
        tone="blue",
    )
with insight_col2:
    render_insight(
        "Business Insight",
        "High-revenue customers with low recency should move into proactive outreach or loyalty campaigns before value concentration turns into avoidable attrition.",
        tone="teal",
    )
with insight_col3:
    render_insight(
        "Decision Angle",
        "Use the RFM mix to separate premium account management from reactivation workflows instead of treating every customer with the same sales or retention motion.",
        tone="blue",
    )

render_page_spacer(0.45)

detail_col1, detail_col2 = st.columns([1.2, 0.8])
with detail_col1:
    show_table(top_customers, "Highest-Value Customers")
with detail_col2:
    render_info_card(
        "Top Segment Readout",
        f"{top_segment} leads the portfolio on aggregated revenue. That makes it the clearest segment to protect with differentiated service, upsell design, and retention monitoring.",
    )
    render_info_card(
        "Coverage Signal",
        f"The dataset currently tracks {compact_number(rfm['customer_id'].nunique())} customers, making this page a strong summary of both scale and value density in the customer base.",
    )
