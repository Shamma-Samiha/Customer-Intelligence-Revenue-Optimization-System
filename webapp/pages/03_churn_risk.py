import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path, load_app_styles
from webapp.components.charts import bar_chart, horizontal_bar_chart, histogram_chart
from webapp.components.kpi_cards import (
    render_info_card,
    render_insight,
    render_kpi_row,
    render_page_intro,
    render_section_header,
)
from webapp.components.tables import show_table
from webapp.utils.formatters import compact_number, days, pct
from webapp.utils.loaders import load_all_data


def show_chart(fig, x_title: str, y_title: str) -> None:
    fig.update_xaxes(title=x_title)
    fig.update_yaxes(title=y_title)
    st.plotly_chart(fig, use_container_width=True)


ensure_project_on_path()
load_app_styles()

data = load_all_data()
churn = data["churn"].copy()
high_risk_mask = churn["predicted_churn_risk"] == 1
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
    .head(15)[["customer_name", "recency", "frequency", "monetary", "churn_probability"]]
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

render_page_intro(
    "Retention Risk Monitoring",
    "Churn Risk",
    "A business-ready early warning dashboard that surfaces how broad the risk pool is, where risk is concentrated, and which customers deserve immediate retention attention.",
)

render_kpi_row(
    [
        ("Churn Rate", pct(churn_rate)),
        ("High-Risk Customers", compact_number(high_risk_count)),
        ("Average Risk", pct(churn["churn_probability"].mean())),
        ("Avg Recency", days(churn["recency"].mean())),
    ]
)

render_section_header(
    "Risk Distribution",
    "Read this page as a retention prioritization view: how much of the base is drifting, how severe the current risk mix is, and which signals align most strongly with churn probability.",
)

col1, col2 = st.columns(2)
with col1:
    show_chart(
        histogram_chart(churn, "churn_probability", title="Churn Probability Distribution", nbins=24),
        "Churn Probability",
        "Customers",
    )
with col2:
    show_chart(
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
    show_chart(
        bar_chart(driver_strength, "feature", "strength", title="Feature Importance Signals"),
        "Feature",
        "Correlation Strength",
    )
with col4:
    render_info_card(
        "Business Recommendation",
        "Critical-risk customers should move into immediate outreach, moderate-risk customers should be handled with automated nurture or offer-based recovery, and the low-risk base should stay in efficiency-focused lifecycle programs.",
    )
    render_info_card(
        "Operational Focus",
        "Use this dashboard to allocate retention resources toward recent deterioration patterns instead of spreading the same attention budget across the entire customer portfolio.",
    )

render_section_header(
    "Decision Support",
    "The strongest retention dashboards do more than list risky accounts. They connect severity, drivers, and action so the commercial team knows what to do next.",
)

insight_col1, insight_col2, insight_col3 = st.columns(3)
with insight_col1:
    render_insight(
        "What To Notice",
        f"{compact_number(high_risk_count)} customers are already flagged as high risk, which makes the current churn pool material enough to justify a targeted retention workflow instead of ad hoc review.",
        tone="rose",
    )
with insight_col2:
    render_insight(
        "Business Insight",
        "The driver chart shows which behavioral signals move most closely with risk probability, helping frame whether churn is mainly an inactivity issue, a value decline issue, or a margin-quality issue.",
        tone="blue",
    )
with insight_col3:
    render_insight(
        "Decision Angle",
        "Prioritize accounts with both high churn probability and meaningful revenue contribution first, because those customers represent the fastest path to protecting future revenue.",
        tone="teal",
    )

show_table(high_risk, "Highest-Risk Customers")
