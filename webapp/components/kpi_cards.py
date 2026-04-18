import streamlit as st


def render_kpi_row(items: list[tuple[str, str]]) -> None:
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.markdown(
            f'''
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )


def render_insight(title: str, text: str, tone: str = "teal") -> None:
    st.markdown(
        f'''
        <div class="insight-card insight-{tone}">
            <div class="insight-title">{title}</div>
            <div class="insight-text">{text}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
