from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go

PRIMARY = "#0f766e"
SECONDARY = "#1d4ed8"
ACCENT = "#f59e0b"
ROSE = "#e11d48"
SLATE = "#334155"
BG = "rgba(255,255,255,0)"
COLORWAY = ["#0f766e", "#1d4ed8", "#14b8a6", "#f59e0b", "#e11d48", "#7c3aed", "#0ea5e9"]


def _apply_theme(fig, title: str):
    fig.update_layout(
        title=title,
        margin=dict(l=16, r=16, t=64, b=16),
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        colorway=COLORWAY,
        font=dict(family="Inter, Segoe UI, sans-serif", color="#0f172a"),
        title_font=dict(size=24, color="#0f172a"),
        legend_title_text="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(255,255,255,0.6)",
        ),
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Inter, Segoe UI, sans-serif"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.22)", zeroline=False)
    return fig


def bar_chart(data, x, y, color=None, title=""):
    fig = px.bar(data, x=x, y=y, color=color or x, title=title, text_auto=".2s")
    fig.update_traces(marker_line_width=0, opacity=0.94)
    return _apply_theme(fig, title)


def horizontal_bar_chart(data, x, y, color=None, title=""):
    fig = px.bar(data, x=x, y=y, color=color or y, orientation="h", title=title, text_auto=".2s")
    fig.update_traces(marker_line_width=0, opacity=0.95)
    return _apply_theme(fig, title)


def line_chart(data, x, y, title=""):
    fig = px.line(data, x=x, y=y, title=title)
    fig.update_traces(line=dict(width=3, color=SECONDARY))
    return _apply_theme(fig, title)


def area_line_chart(data, x, y, title="", color=PRIMARY):
    fig = px.area(data, x=x, y=y, title=title)
    fig.update_traces(line=dict(width=3, color=color), fillcolor="rgba(15,118,110,0.14)")
    return _apply_theme(fig, title)


def scatter_chart(data, x, y, color=None, title=""):
    fig = px.scatter(data, x=x, y=y, color=color, title=title)
    fig.update_traces(marker=dict(size=11, opacity=0.72, line=dict(width=0)))
    return _apply_theme(fig, title)


def histogram_chart(data, x, color=None, title="", nbins=30):
    fig = px.histogram(data, x=x, color=color, nbins=nbins, title=title, opacity=0.9)
    return _apply_theme(fig, title)


def donut_chart(data, names, values, title=""):
    fig = px.pie(data, names=names, values=values, hole=0.58, title=title)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return _apply_theme(fig, title)


def forecast_chart(data, title="Forecasted Revenue"):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["ds"],
            y=data["yhat"],
            mode="lines",
            name="Forecast",
            line=dict(color=SECONDARY, width=3),
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
                fillcolor="rgba(14,165,233,0.16)",
            )
        )
    return _apply_theme(fig, title)
