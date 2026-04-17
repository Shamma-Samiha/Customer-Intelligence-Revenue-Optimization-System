from __future__ import annotations

import pandas as pd


def score_by_quantile(series: pd.Series, labels: list[int], ascending: bool = True) -> pd.Series:
    ranked = series.rank(method="first", ascending=ascending)
    return pd.qcut(ranked, q=len(labels), labels=labels).astype(int)


def segment_customer(row: pd.Series) -> str:
    r = row["r_score"]
    f = row["f_score"]
    m = row["m_score"]
    if r >= 4 and f >= 4 and m >= 4:
        return "VIP Customers"
    if r >= 3 and f >= 3:
        return "Loyal Customers"
    if r >= 4 and f <= 2:
        return "New Customers"
    if r <= 2 and (f >= 3 or m >= 3):
        return "At Risk Customers"
    return "Regular Customers"


def build_rfm_table(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()
    working["order_date"] = pd.to_datetime(working["order_date"], errors="coerce")
    snapshot_date = working["order_date"].max() + pd.Timedelta(days=1)

    rfm = (
        working.groupby(["customer_id", "customer_name"], as_index=False)
        .agg(
            recency=("order_date", lambda x: (snapshot_date - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("sales", "sum"),
            avg_discount=("discount", "mean"),
            avg_profit=("profit", "mean"),
            total_quantity=("quantity", "sum"),
            last_order_date=("order_date", "max"),
        )
    )

    rfm["r_score"] = score_by_quantile(rfm["recency"], [4, 3, 2, 1], ascending=True)
    rfm["f_score"] = score_by_quantile(rfm["frequency"], [1, 2, 3, 4], ascending=True)
    rfm["m_score"] = score_by_quantile(rfm["monetary"], [1, 2, 3, 4], ascending=True)
    rfm["rfm_total"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]
    rfm["rfm_score"] = (
        rfm["r_score"].astype(str)
        + rfm["f_score"].astype(str)
        + rfm["m_score"].astype(str)
    )
    rfm["rfm_segment"] = rfm.apply(segment_customer, axis=1)
    return rfm.sort_values(["rfm_total", "monetary"], ascending=[False, False]).reset_index(drop=True)
