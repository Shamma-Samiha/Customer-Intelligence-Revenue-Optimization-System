from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd


ENCODINGS = ("utf-8", "latin1", "cp1252")


def get_project_root(current: Path | None = None) -> Path:
    current = current or Path.cwd()
    if (current / "data").exists():
        return current
    if (current.parent / "data").exists():
        return current.parent
    return current


def read_csv_with_fallback(path: Path) -> Tuple[pd.DataFrame, str]:
    for encoding in ENCODINGS:
        try:
            return pd.read_csv(path, encoding=encoding), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unable to read {path} using supported encodings.")


def standardize_columns(columns: pd.Index) -> list[str]:
    cleaned = (
        columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(".", "_", regex=False)
        .str.replace(" ", "_", regex=False)
        .str.replace("/", "_", regex=False)
    )
    return cleaned.tolist()


def clean_superstore_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = standardize_columns(cleaned.columns)

    rename_map = {
        "customer_id": "customer_id",
        "customer_name": "customer_name",
        "order_date": "order_date",
        "order_id": "order_id",
        "order_priority": "order_priority",
        "product_id": "product_id",
        "product_name": "product_name",
        "ship_date": "ship_date",
        "ship_mode": "ship_mode",
        "shipping_cost": "shipping_cost",
        "sub_category": "sub_category",
    }
    cleaned = cleaned.rename(columns=rename_map)

    drop_candidates = [
        "记录数",
        "è®°å½æ°",
        "row_id",
        "year",
        "market2",
        "weeknum",
    ]
    drop_columns = [col for col in drop_candidates if col in cleaned.columns]
    cleaned = cleaned.drop(columns=drop_columns)

    date_columns = [col for col in ["order_date", "ship_date"] if col in cleaned.columns]
    for column in date_columns:
        cleaned[column] = pd.to_datetime(cleaned[column], errors="coerce")

    numeric_columns = ["sales", "profit", "discount", "quantity", "shipping_cost"]
    for column in numeric_columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    cleaned["order_year"] = cleaned["order_date"].dt.year
    cleaned["order_month"] = cleaned["order_date"].dt.month
    cleaned["order_day"] = cleaned["order_date"].dt.day
    cleaned["month_name"] = cleaned["order_date"].dt.month_name()
    cleaned["year_month"] = cleaned["order_date"].dt.to_period("M").dt.to_timestamp()
    cleaned["profit_margin"] = np.where(cleaned["sales"] != 0, cleaned["profit"] / cleaned["sales"], 0.0)

    return cleaned


def load_raw_data(project_root: Path | None = None) -> pd.DataFrame:
    project_root = get_project_root(project_root)
    path = project_root / "data" / "raw" / "superstore_raw.csv"
    df, _ = read_csv_with_fallback(path)
    return df


def load_cleaned_data(project_root: Path | None = None) -> pd.DataFrame:
    project_root = get_project_root(project_root)
    path = project_root / "data" / "cleaned" / "superstore_cleaned.csv"
    df = pd.read_csv(path)
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    if "ship_date" in df.columns:
        df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")
    if "year_month" in df.columns:
        df["year_month"] = pd.to_datetime(df["year_month"], errors="coerce")
    return df
