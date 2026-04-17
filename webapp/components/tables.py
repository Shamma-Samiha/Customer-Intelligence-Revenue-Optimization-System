import streamlit as st


def show_table(df, title: str):
    st.markdown(f"### {title}")
    st.dataframe(df, use_container_width=True, hide_index=True)
