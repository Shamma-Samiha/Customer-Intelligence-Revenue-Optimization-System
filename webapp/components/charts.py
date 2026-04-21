from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from webapp.utils.theme import get_theme_tokens


def _visible_legend_items(fig) -> int:
    return sum(1 for trace in fig.data if getattr(trace, "showlegend", True) is not False)


def style_figure(fig, title: str):
    theme = get_theme_tokens()
    colorway = list(theme["colorway"])
    title_text = title or fig.layout.title.text or ""
    legend_items = _visible_legend_items(fig)
    show_legend = legend_items > 1

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.01,
            xanchor="left",
            y=0.98,
            yanchor="top",
            pad=dict(b=20),
        ),
        margin=dict(l=16, r=16, t=126 if show_legend else 84, b=24),
        paper_bgcolor=str(theme["chart_background"]),
        plot_bgcolor=str(theme["chart_background"]),
        colorway=colorway,
        font=dict(family=str(theme["font_family"]), color=str(theme["text_primary"])),
        title_font=dict(size=20, color=str(theme["text_primary"]), family=str(theme["heading_family"])),
        legend_title_text="",
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.0,
            xanchor="left",
            x=0,
            entrywidthmode="pixels",
            entrywidth=120,
            tracegroupgap=8,
            bgcolor=str(theme["chart_legend_bg"]),
            bordercolor=str(theme["border"]),
            borderwidth=1,
            itemclick="toggleothers",
            font=dict(color=str(theme["text_secondary"])),
        ),
        hoverlabel=dict(
            bgcolor=str(theme["hover_background"]),
            font_size=13,
            font_family=str(theme["font_family"]),
            font_color=str(theme["text_primary"]),
            bordercolor=str(theme["border"]),
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor=str(theme["border"]),
        automargin=True,
        tickfont=dict(color=str(theme["text_secondary"])),
        title_font=dict(color=str(theme["text_secondary"])),
    )
    fig.update_yaxes(
        gridcolor=str(theme["chart_grid"]),
        zeroline=False,
        linecolor=str(theme["border"]),
        automargin=True,
        tickfont=dict(color=str(theme["text_secondary"])),
        title_font=dict(color=str(theme["text_secondary"])),
    )
    return fig


def bar_chart(data, x, y, color=None, title=""):
    fig = px.bar(data, x=x, y=y, color=color or x, title=title, text_auto=".2s")
    fig.update_traces(marker_line_width=0, opacity=0.94)
    fig.update_layout(showlegend=False)
    return style_figure(fig, title)


def horizontal_bar_chart(data, x, y, color=None, title=""):
    fig = px.bar(data, x=x, y=y, color=color or y, orientation="h", title=title, text_auto=".2s")
    fig.update_traces(marker_line_width=0, opacity=0.95)
    fig.update_layout(showlegend=False)
    return style_figure(fig, title)


def line_chart(data, x, y, title=""):
    theme = get_theme_tokens()
    fig = px.line(data, x=x, y=y, title=title)
    fig.update_traces(line=dict(width=3, color=str(theme["accent_tertiary"])))
    return style_figure(fig, title)


def area_line_chart(data, x, y, title="", color=None):
    theme = get_theme_tokens()
    area_color = color or str(theme["accent"])
    fig = px.area(data, x=x, y=y, title=title)
    fill_color = "rgba(15,118,110,0.14)" if get_theme_tokens()["mode"] == "light" else "rgba(45,212,191,0.18)"
    fig.update_traces(line=dict(width=3, color=area_color), fillcolor=fill_color)
    return style_figure(fig, title)


def scatter_chart(data, x, y, color=None, title=""):
    fig = px.scatter(data, x=x, y=y, color=color, title=title)
    fig.update_traces(marker=dict(size=10, opacity=0.66, line=dict(width=0)))
    return style_figure(fig, title)


def histogram_chart(data, x, color=None, title="", nbins=30):
    fig = px.histogram(data, x=x, color=color, nbins=nbins, title=title, opacity=0.9)
    return style_figure(fig, title)


def donut_chart(data, names, values, title=""):
    fig = px.pie(data, names=names, values=values, hole=0.58, title=title)
    fig.update_traces(textposition="inside", textinfo="percent+label", insidetextorientation="radial")
    fig.update_layout(showlegend=False, margin=dict(l=16, r=16, t=84, b=16))
    return style_figure(fig, title)


def forecast_chart(data, title="Forecasted Revenue"):
    theme = get_theme_tokens()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["ds"],
            y=data["yhat"],
            mode="lines",
            name="Forecast",
            line=dict(color=str(theme["accent_tertiary"]), width=3),
        )
    )
    if {"yhat_lower", "yhat_upper"}.issubset(data.columns):
        fig.add_trace(
            go.Scatter(
                x=data["ds"],
                y=data["yhat_upper"],
                mode="lines",
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=data["ds"],
                y=data["yhat_lower"],
                mode="lines",
                fill="tonexty",
                line=dict(width=0),
                name="Confidence Band",
                hoverinfo="skip",
                fillcolor="rgba(14,165,233,0.16)" if theme["mode"] == "light" else "rgba(56,189,248,0.18)",
            )
        )
    return style_figure(fig, title)


def render_chart(fig, x_title: str = "", y_title: str = "") -> None:
    if x_title:
        fig.update_xaxes(title=x_title)
    if y_title:
        fig.update_yaxes(title=y_title)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
