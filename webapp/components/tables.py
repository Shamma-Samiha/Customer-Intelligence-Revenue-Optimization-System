import streamlit as st


def show_table(df, title: str):
    st.markdown(f'<div class="section-header" style="font-size:1.15rem; margin-top:0.25rem;">{title}</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True, height=380)
