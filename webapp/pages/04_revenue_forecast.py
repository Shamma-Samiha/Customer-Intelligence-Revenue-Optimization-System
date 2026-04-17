import streamlit as st

from webapp.components.charts import line_chart
from webapp.components.tables import show_table
from webapp.utils.loaders import load_all_data


st.title("Revenue Forecast")
st.caption("Forward-looking revenue view for planning, target setting, and business communication.")

data = load_all_data()
forecast = data["forecast"]

st.plotly_chart(line_chart(forecast, "ds", "yhat", "Revenue Forecast"), use_container_width=True)
show_table(forecast.tail(30), "Forecast Horizon Preview")
