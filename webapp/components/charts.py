from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go


def bar_chart(data, x, y, color=None, title=""):
    fig = px.bar(data, x=x, y=y, color=color or x, title=title)
    fig.update_layout(margin=dict(l=16, r=16, t=56, b=16), legend_title_text="")
    return fig


def line_chart(data, x, y, title=""):
    fig = px.line(data, x=x, y=y, title=title)
    fig.update_layout(margin=dict(l=16, r=16, t=56, b=16))
    return fig


def scatter_chart(data, x, y, color=None, title=""):
    fig = px.scatter(data, x=x, y=y, color=color, title=title)
    fig.update_layout(margin=dict(l=16, r=16, t=56, b=16), legend_title_text="")
    return fig


def forecast_chart(data, title="Forecasted Revenue"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["ds"], y=data["yhat"], mode="lines", name="Forecast"))
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
            )
        )
    fig.update_layout(title=title, margin=dict(l=16, r=16, t=56, b=16))
    return fig
