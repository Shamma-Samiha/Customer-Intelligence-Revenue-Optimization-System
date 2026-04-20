from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ensure_project_on_path() -> Path:
    root = get_project_root()
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return root


def load_app_styles() -> None:
    css_path = Path(__file__).resolve().parent / "assets" / "styles.css"
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
