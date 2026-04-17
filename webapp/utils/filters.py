from __future__ import annotations

import pandas as pd
import streamlit as st


def sidebar_filters(orders: pd.DataFrame) -> pd.DataFrame:
    filtered = orders.copy()

    if "order_year" in filtered.columns:
        years = sorted(filtered["order_year"].dropna().unique().tolist())
        selected_years = st.sidebar.multiselect("Order Year", years, default=years)
        filtered = filtered[filtered["order_year"].isin(selected_years)]

    if "market" in filtered.columns:
        markets = sorted(filtered["market"].dropna().unique().tolist())
        selected_markets = st.sidebar.multiselect("Market", markets, default=markets)
        filtered = filtered[filtered["market"].isin(selected_markets)]

    if "region" in filtered.columns:
        regions = sorted(filtered["region"].dropna().unique().tolist())
        selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
        filtered = filtered[filtered["region"].isin(selected_regions)]

    return filtered
