import streamlit as st
import plotly.express as px

from webapp.components.tables import show_table
from webapp.utils.loaders import load_all_data


st.title("Churn Risk")
st.caption("Behavior-based churn-risk scoring for retention prioritization.")

data = load_all_data()
churn = data["churn"]

col1, col2 = st.columns(2)
with col1:
    st.metric("Predicted At-Risk Customers", f"{int((churn['predicted_churn_risk'] == 1).sum()):,}")
with col2:
    st.metric("Average Churn Probability", f"{churn['churn_probability'].mean():.1%}")

fig = px.histogram(churn, x="churn_probability", nbins=30, title="Churn Probability Distribution")
st.plotly_chart(fig, use_container_width=True)

high_risk = churn.sort_values("churn_probability", ascending=False).head(25)
show_table(high_risk, "Highest-Risk Customers")
