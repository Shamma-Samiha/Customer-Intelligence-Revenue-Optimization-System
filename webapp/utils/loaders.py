from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _candidate_files(root: Path) -> dict[str, list[Path]]:
    return {
        "orders": [
            root / "outputs" / "csv" / "cleaned_orders.csv",
            root / "data" / "processed" / "cleaned_orders.csv",
        ],
        "kpis": [
            root / "outputs" / "csv" / "executive_summary.csv",
            root / "data" / "processed" / "executive_kpis.csv",
        ],
        "rfm": [root / "outputs" / "csv" / "rfm_table.csv"],
        "churn": [root / "outputs" / "csv" / "churn_predictions.csv"],
        "forecast": [root / "outputs" / "csv" / "revenue_forecast.csv"],
    }


def resolve_data_path(name: str) -> Path:
    root = get_project_root()
    for path in _candidate_files(root)[name]:
        if path.exists():
            return path
    searched = "\n".join(str(path) for path in _candidate_files(root)[name])
    raise FileNotFoundError(f"Missing required dataset '{name}'. Searched:\n{searched}")


@st.cache_data(show_spinner=False)
def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    for column in ["order_date", "ship_date", "year_month", "ds", "last_order_date"]:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")
    return df


@st.cache_data(show_spinner=False)
def load_all_data() -> dict[str, pd.DataFrame]:
    files = {name: resolve_data_path(name) for name in _candidate_files(get_project_root())}
    return {name: load_csv(path) for name, path in files.items()}


def validate_app_data() -> list[str]:
    missing = []
    for name in _candidate_files(get_project_root()):
        try:
            resolve_data_path(name)
        except FileNotFoundError:
            missing.append(name)
    return missing
