import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webapp.bootstrap import ensure_project_on_path
from webapp.components.kpi_cards import render_insight, render_kpi_row
from webapp.components.tables import show_table
from webapp.utils.loaders import load_all_data


ensure_project_on_path()

st.title("Churn Risk")
st.caption("Proxy churn-risk monitoring based on inactivity and customer transaction behavior.")

data = load_all_data()
churn = data["churn"]

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
    "This is a proxy churn model rather than a contractual churn label. It is most useful as an early-warning layer for review, campaign prioritization, and retention triage.",
    tone="rose",
)

fig = px.histogram(churn, x="churn_probability", nbins=30, title="Churn Probability Distribution")
st.plotly_chart(fig, use_container_width=True)

high_risk = churn.sort_values("churn_probability", ascending=False).head(25)
show_table(high_risk, "Highest-Risk Customers")
