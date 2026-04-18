import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.charts import horizontal_bar_chart, histogram_chart
from webapp.components.kpi_cards import render_insight, render_kpi_row, render_page_intro
from webapp.components.tables import show_table
from webapp.utils.loaders import load_all_data


ensure_project_on_path()

data = load_all_data()
churn = data["churn"]
render_page_intro(
    "Retention Risk Monitoring",
    "Churn Risk",
    "A proxy churn view built from inactivity and behavioral signals to help prioritize which customers deserve immediate retention attention.",
)

render_kpi_row(
    [
        ("Predicted At-Risk Customers", f"{int((churn['predicted_churn_risk'] == 1).sum()):,}"),
        ("Average Churn Probability", f"{churn['churn_probability'].mean():.1%}"),
        ("Highest Risk Probability", f"{churn['churn_probability'].max():.1%}"),
        ("Average Recency", f"{churn['recency'].mean():.0f} days"),
    ]
)

render_insight(
    "Interpretation",
    "This is a proxy churn model rather than a contractual churn label. That makes it best suited for early-warning monitoring: who to review first, which accounts deserve outreach, and how broad the retention risk pool has become.",
    tone="rose",
)

high_risk = churn.sort_values("churn_probability", ascending=False).head(25)

col1, col2 = st.columns([1.15, 0.85])
with col1:
    st.plotly_chart(histogram_chart(churn, "churn_probability", title="Churn Probability Distribution", nbins=24), use_container_width=True)
with col2:
    risk_bands = (
        churn.assign(
            risk_band=pd.cut(
                churn["churn_probability"],
                bins=[0, 0.3, 0.6, 0.8, 1.0],
                labels=["Low", "Moderate", "High", "Critical"],
                include_lowest=True,
            )
        )
        .groupby("risk_band", as_index=False)["customer_id"]
        .count()
        .rename(columns={"customer_id": "customers"})
    )
    st.plotly_chart(horizontal_bar_chart(risk_bands, "customers", "risk_band", "risk_band", "Customers by Risk Band"), use_container_width=True)

show_table(high_risk, "Highest-Risk Customers")

render_insight(
    "What Stands Out",
    f"The model currently flags {int((churn['predicted_churn_risk'] == 1).sum()):,} customers as at risk, with an average predicted churn probability of {churn['churn_probability'].mean():.1%}. This gives retention conversations a concrete starting point.",
    tone="blue",
)
