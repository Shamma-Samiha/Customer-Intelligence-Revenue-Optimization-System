from __future__ import annotations

import pandas as pd
import streamlit as st


def sidebar_filters(orders: pd.DataFrame) -> pd.DataFrame:
    filtered = orders.copy()

    st.sidebar.markdown("## Filters")
    st.sidebar.caption("Refine the current view without leaving the page.")
    years = sorted(filtered["order_year"].dropna().unique().tolist()) if "order_year" in filtered.columns else []
    markets = sorted(filtered["market"].dropna().unique().tolist()) if "market" in filtered.columns else []
    regions = sorted(filtered["region"].dropna().unique().tolist()) if "region" in filtered.columns else []

    if st.sidebar.button("Reset filters", use_container_width=True):
        if years:
            st.session_state["filter_order_year"] = years
        if markets:
            st.session_state["filter_market"] = markets
        if regions:
            st.session_state["filter_region"] = regions

    if "order_year" in filtered.columns:
        selected_years = st.sidebar.multiselect("Order Year", years, default=years, key="filter_order_year")
        filtered = filtered[filtered["order_year"].isin(selected_years)]

    if "market" in filtered.columns:
        selected_markets = st.sidebar.multiselect("Market", markets, default=markets, key="filter_market")
        filtered = filtered[filtered["market"].isin(selected_markets)]

    if "region" in filtered.columns:
        selected_regions = st.sidebar.multiselect("Region", regions, default=regions, key="filter_region")
        filtered = filtered[filtered["region"].isin(selected_regions)]

    st.sidebar.metric("Orders in View", f"{filtered['order_id'].nunique():,}" if "order_id" in filtered.columns else f"{len(filtered):,}")

    return filtered
