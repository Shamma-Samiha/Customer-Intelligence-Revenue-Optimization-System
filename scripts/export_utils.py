from __future__ import annotations

from pathlib import Path

import pandas as pd


def build_executive_kpis(df: pd.DataFrame) -> pd.DataFrame:
    total_sales = df["sales"].sum()
    total_profit = df["profit"].sum()
    total_orders = df["order_id"].nunique()
    total_customers = df["customer_id"].nunique()
    avg_order_value = total_sales / total_orders
    avg_sales_per_customer = total_sales / total_customers
    return pd.DataFrame(
        [
            {
                "total_sales": total_sales,
                "total_profit": total_profit,
                "total_orders": total_orders,
                "total_customers": total_customers,
                "avg_order_value": avg_order_value,
                "avg_sales_per_customer": avg_sales_per_customer,
            }
        ]
    )


def export_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
