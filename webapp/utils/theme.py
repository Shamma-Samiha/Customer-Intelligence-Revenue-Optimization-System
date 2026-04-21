from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


THEME_OPTIONS = ("Light", "Dark")
THEME_KEY = "app_theme"
THEME_TOGGLE_KEY = "app_theme_is_dark"

THEMES: dict[str, dict[str, str | list[str]]] = {
    "Light": {
        "mode": "light",
        "font_family": "Source Sans 3, Segoe UI, sans-serif",
        "heading_family": "Manrope, Segoe UI, sans-serif",
        "background": "#f6f9fc",
        "background_alt": "#edf4f2",
        "sidebar_background": "#0f172a",
        "sidebar_secondary": "#11364a",
        "surface": "rgba(255,255,255,0.82)",
        "surface_alt": "rgba(248,251,253,0.9)",
        "surface_hover": "rgba(255,255,255,0.95)",
        "card_background": "rgba(255,255,255,0.88)",
        "card_gradient": "linear-gradient(180deg, rgba(255,255,255,0.94), rgba(245,249,252,0.88))",
        "text_primary": "#102033",
        "text_secondary": "#526173",
        "text_muted": "#718194",
        "sidebar_text": "#e2e8f0",
        "sidebar_text_muted": "rgba(226,232,240,0.72)",
        "accent": "#0f766e",
        "accent_secondary": "#0a8fb2",
        "accent_tertiary": "#2958d8",
        "accent_rose": "#e11d48",
        "accent_amber": "#f59e0b",
        "border": "rgba(141,156,175,0.26)",
        "border_strong": "rgba(118,138,163,0.38)",
        "shadow": "0 18px 46px rgba(15, 23, 42, 0.08)",
        "hero_start": "#102033",
        "hero_mid": "#0f5c60",
        "hero_end": "#248fcb",
        "hero_badge_bg": "rgba(255,255,255,0.12)",
        "hero_badge_border": "rgba(255,255,255,0.16)",
        "hero_glow": "rgba(255,255,255,0.22)",
        "chart_background": "rgba(255,255,255,0)",
        "chart_grid": "rgba(133,151,174,0.18)",
        "chart_legend_bg": "rgba(255,255,255,0.65)",
        "hover_background": "#ffffff",
        "colorway": ["#0f766e", "#1d4ed8", "#14b8a6", "#f59e0b", "#e11d48", "#0ea5e9", "#7c3aed"],
    },
    "Dark": {
        "mode": "dark",
        "font_family": "Source Sans 3, Segoe UI, sans-serif",
        "heading_family": "Manrope, Segoe UI, sans-serif",
        "background": "#0b1520",
        "background_alt": "#102030",
        "sidebar_background": "#0d1824",
        "sidebar_secondary": "#123044",
        "surface": "rgba(16,30,45,0.78)",
        "surface_alt": "rgba(18,34,51,0.86)",
        "surface_hover": "rgba(22,39,58,0.94)",
        "card_background": "rgba(15,29,43,0.84)",
        "card_gradient": "linear-gradient(180deg, rgba(19,35,52,0.9), rgba(12,25,38,0.84))",
        "text_primary": "#ebf3fb",
        "text_secondary": "#c2d1df",
        "text_muted": "#8ea3b7",
        "sidebar_text": "#eef5fb",
        "sidebar_text_muted": "rgba(238,245,251,0.7)",
        "accent": "#29c7b3",
        "accent_secondary": "#34b6e5",
        "accent_tertiary": "#71a8ff",
        "accent_rose": "#fb7185",
        "accent_amber": "#fbbf24",
        "border": "rgba(128,149,171,0.2)",
        "border_strong": "rgba(147,170,194,0.34)",
        "shadow": "0 24px 60px rgba(3, 8, 18, 0.34)",
        "hero_start": "#101a2a",
        "hero_mid": "#0e4e54",
        "hero_end": "#17688f",
        "hero_badge_bg": "rgba(235,243,251,0.06)",
        "hero_badge_border": "rgba(193,210,226,0.14)",
        "hero_glow": "rgba(52,182,229,0.16)",
        "chart_background": "rgba(0,0,0,0)",
        "chart_grid": "rgba(142,163,186,0.14)",
        "chart_legend_bg": "rgba(11,24,37,0.66)",
        "hover_background": "#14283b",
        "colorway": ["#2dd4bf", "#60a5fa", "#38bdf8", "#fbbf24", "#fb7185", "#a78bfa", "#22d3ee"],
    },
}


def initialize_theme() -> str:
    if THEME_KEY not in st.session_state:
        st.session_state[THEME_KEY] = THEME_OPTIONS[0]
    if THEME_TOGGLE_KEY not in st.session_state:
        st.session_state[THEME_TOGGLE_KEY] = st.session_state[THEME_KEY] == "Dark"
    else:
        st.session_state[THEME_KEY] = "Dark" if st.session_state[THEME_TOGGLE_KEY] else "Light"
    return st.session_state[THEME_KEY]


def get_active_theme_name() -> str:
    return initialize_theme()


def get_theme_tokens() -> dict[str, str | list[str]]:
    return THEMES[get_active_theme_name()]


def get_theme_mode() -> str:
    return str(get_theme_tokens()["mode"])


def _theme_css_vars(theme_name: str) -> str:
    tokens = THEMES[theme_name]
    css_lines: list[str] = []
    for key, value in tokens.items():
        if key in {"mode", "font_family", "heading_family", "colorway"}:
            continue
        css_lines.append(f"--{key.replace('_', '-')}: {value};")
    css_lines.append(f"--font-family: {tokens['font_family']};")
    css_lines.append(f"--heading-family: {tokens['heading_family']};")
    return "\n".join(css_lines)


def inject_active_theme() -> None:
    theme_name = get_active_theme_name()
    theme_slug = theme_name.lower()
    components.html(
        f"""
        <script>
        const root = window.parent.document.documentElement;
        const body = window.parent.document.body;
        root.setAttribute("data-theme", "{theme_slug}");
        body.setAttribute("data-theme", "{theme_slug}");
        const app = window.parent.document.querySelector(".stApp");
        if (app) {{
            app.setAttribute("data-theme", "{theme_slug}");
        }}
        </script>
        <style>
        html[data-theme="{theme_slug}"] {{
            {_theme_css_vars(theme_name)}
        }}
        </style>
        """,
        height=0,
    )


def render_theme_toggle() -> str:
    current_theme = initialize_theme()

    st.sidebar.markdown("## Appearance")
    st.sidebar.markdown(
        f"""
        <div class="theme-toggle-shell">
            <div class="theme-toggle-label-group">
                <div class="theme-toggle-title">Interface Theme</div>
                <div class="theme-toggle-subtitle">Soft light for daytime, refined dark for focus.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    is_dark_mode = st.sidebar.toggle(
        "Dark mode",
        value=st.session_state[THEME_TOGGLE_KEY],
        key=THEME_TOGGLE_KEY,
        help="Switch the full dashboard between Light and Dark mode.",
    )
    st.session_state[THEME_KEY] = "Dark" if is_dark_mode else "Light"
    inject_active_theme()
    return get_active_theme_name()


def load_theme_assets() -> None:
    css_path = Path(__file__).resolve().parents[1] / "assets" / "styles.css"
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def apply_theme() -> dict[str, str | list[str]]:
    initialize_theme()
    load_theme_assets()
    render_theme_toggle()
    return get_theme_tokens()
