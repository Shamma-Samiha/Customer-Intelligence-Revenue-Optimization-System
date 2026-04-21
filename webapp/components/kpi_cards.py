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


def render_dashboard_hero(eyebrow: str, title: str, subtitle: str, badges: list[str] | None = None) -> None:
    badge_html = ""
    if badges:
        badge_html = '<div class="hero-badges">' + "".join(
            f'<span class="hero-badge">{badge}</span>' for badge in badges
        ) + "</div>"
    st.markdown(
        f'''
        <div class="hero hero-premium">
            <div class="hero-kicker">{eyebrow}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
            {badge_html}
        </div>
        ''',
        unsafe_allow_html=True,
    )


def render_page_intro(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f'''
        <div class="page-hero">
            <div class="page-eyebrow">{eyebrow}</div>
            <div class="page-title">{title}</div>
            <div class="page-subtitle">{subtitle}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def render_page_spacer(height: float = 1.0) -> None:
    st.markdown(f"<div style='height:{height:.2f}rem;'></div>", unsafe_allow_html=True)


def render_section_header(title: str, subtitle: str) -> None:
    st.markdown(
        f'''
        <div class="section-card">
            <div class="section-header">{title}</div>
            <div class="section-subtitle">{subtitle}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def render_info_card(title: str, text: str) -> None:
    st.markdown(
        f'''
        <div class="section-card info-card">
            <div class="section-header info-card-title">{title}</div>
            <div class="section-subtitle info-card-text">{text}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
