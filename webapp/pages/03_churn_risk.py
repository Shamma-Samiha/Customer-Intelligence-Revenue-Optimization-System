import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.charts import bar_chart, horizontal_bar_chart, histogram_chart, render_chart
from webapp.components.kpi_cards import (
    render_dashboard_hero,
    render_info_card,
    render_insight,
    render_kpi_row,
    render_page_spacer,
    render_section_header,
)
from webapp.components.tables import show_table
from webapp.utils.formatters import compact_number, days, pct
from webapp.utils.loaders import load_all_data
from webapp.utils.theme import apply_theme


ensure_project_on_path()
apply_theme()

data = load_all_data()
churn = data["churn"].copy()

st.sidebar.markdown("## Risk Controls")
if st.sidebar.button("Reset risk view", use_container_width=True):
    st.session_state["risk_threshold"] = 0.60
    st.session_state["risk_min_value"] = 0
    st.session_state["risk_top_n"] = 15
risk_threshold = st.sidebar.slider("High-risk threshold", 0.10, 0.95, 0.60, 0.05, key="risk_threshold")
min_customer_value = st.sidebar.slider(
    "Minimum revenue at risk",
    0,
    int(churn["monetary"].max()),
    0,
    step=max(1, int(churn["monetary"].max() / 100)),
    key="risk_min_value",
)
top_n = st.sidebar.slider("Customers to review", 5, 40, 15, key="risk_top_n")

churn = churn[churn["monetary"] >= min_customer_value].copy()
high_risk_mask = churn["churn_probability"] >= risk_threshold
high_risk_count = int(high_risk_mask.sum())
churn_rate = high_risk_count / len(churn) if len(churn) else 0

risk_bands = (
    churn.assign(
        risk_band=pd.cut(
            churn["churn_probability"],
            bins=[0, 0.3, 0.6, 0.8, 1.0],
            labels=["Low", "Moderate", "High", "Critical"],
            include_lowest=True,
        )
    )
    .groupby("risk_band", observed=False, as_index=False)["customer_id"]
    .count()
    .rename(columns={"customer_id": "customers"})
)

numeric_candidates = [
    column
    for column in [
        "recency",
        "frequency",
        "monetary",
        "avg_discount",
        "avg_profit",
        "total_quantity",
        "total_profit",
        "avg_order_value",
        "profit_margin",
    ]
    if column in churn.columns
]
driver_strength = (
    pd.DataFrame(
        {
            "feature": numeric_candidates,
            "strength": [
                abs(churn[column].corr(churn["churn_probability"]))
                if churn[column].nunique() > 1
                else 0
                for column in numeric_candidates
            ],
        }
    )
    .fillna(0)
    .sort_values("strength", ascending=False)
    .head(6)
)
driver_strength["feature"] = driver_strength["feature"].str.replace("_", " ").str.title()

high_risk = (
    churn.sort_values("churn_probability", ascending=False)
    .head(top_n)[["customer_name", "recency", "frequency", "monetary", "churn_probability"]]
    .rename(
        columns={
            "customer_name": "Customer",
            "recency": "Recency",
            "frequency": "Frequency",
            "monetary": "Revenue",
            "churn_probability": "Churn Probability",
        }
    )
)

render_dashboard_hero(
    "Retention Risk Monitoring",
    "Churn Risk",
    "Find customers with higher churn risk and decide who needs attention first.",
    badges=[
        f"High-Risk Base: {high_risk_count:,}",
        f"Average Risk: {pct(churn['churn_probability'].mean())}",
        f"Avg Recency: {int(churn['recency'].mean()):,} days",
    ],
)

render_kpi_row(
    [
        ("Churn Rate", pct(churn_rate)),
        ("High-Risk Customers", compact_number(high_risk_count)),
        ("Average Risk", pct(churn["churn_probability"].mean())),
        ("Avg Recency", days(churn["recency"].mean())),
    ]
)

render_page_spacer(0.9)

render_section_header(
    "Risk Distribution",
    "Review how risk is spread across the customer base and which behavior signals move with churn probability.",
)

col1, col2 = st.columns(2)
with col1:
    render_chart(
        histogram_chart(churn, "churn_probability", title="Churn Probability Distribution", nbins=24),
        "Churn Probability",
        "Customers",
    )
with col2:
    render_chart(
        horizontal_bar_chart(
            risk_bands.sort_values("customers", ascending=True),
            "customers",
            "risk_band",
            "risk_band",
            "Customers by Risk Band",
        ),
        "Customers",
        "Risk Band",
    )

col3, col4 = st.columns(2)
with col3:
    render_chart(
        bar_chart(driver_strength, "feature", "strength", title="Feature Importance Signals"),
        "Feature",
        "Correlation Strength",
    )
with col4:
    render_info_card(
        "Business Recommendation",
        "Start with critical-risk customers, use lighter recovery campaigns for moderate risk, and keep low-risk customers in regular lifecycle programs.",
    )
    render_info_card(
        "Operational Focus",
        "Spend retention time where risk and customer value overlap, instead of reviewing the whole base the same way.",
    )

render_page_spacer(0.55)

render_section_header(
    "Decision Support",
    "Pair the risk score with revenue and behavior so the next action is obvious.",
)

insight_col1, insight_col2, insight_col3 = st.columns(3)
with insight_col1:
    render_insight(
        "What To Notice",
        f"{compact_number(high_risk_count)} customers are above the selected risk threshold in this view.",
        tone="rose",
    )
with insight_col2:
    render_insight(
        "Business Insight",
        "The driver chart helps separate inactivity, lower value, and margin issues instead of treating every risk score as the same problem.",
        tone="blue",
    )
with insight_col3:
    render_insight(
        "Decision Angle",
        "Review high-risk, high-revenue customers first. That is where a save attempt can protect the most future revenue.",
        tone="teal",
    )

render_page_spacer(0.45)

show_table(high_risk, "Highest-Risk Customers")
