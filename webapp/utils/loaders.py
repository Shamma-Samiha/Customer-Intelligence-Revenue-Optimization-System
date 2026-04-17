from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


def get_project_root() -> Path:
    current = Path(__file__).resolve().parents[2]
    return current


@st.cache_data(show_spinner=False)
def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_all_data() -> dict[str, pd.DataFrame]:
    root = get_project_root()
    files = {
        "orders": root / "data" / "processed" / "cleaned_orders.csv",
        "kpis": root / "data" / "processed" / "executive_kpis.csv",
        "rfm": root / "outputs" / "csv" / "rfm_table.csv",
        "churn": root / "outputs" / "csv" / "churn_predictions.csv",
        "forecast": root / "outputs" / "csv" / "revenue_forecast.csv",
    }
    return {name: load_csv(path) for name, path in files.items() if path.exists()}
