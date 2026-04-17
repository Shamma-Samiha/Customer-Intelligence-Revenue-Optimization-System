from __future__ import annotations

import plotly.express as px


def bar_chart(data, x, y, color=None, title=""):
    return px.bar(data, x=x, y=y, color=color or x, title=title)


def line_chart(data, x, y, title=""):
    return px.line(data, x=x, y=y, title=title)


def scatter_chart(data, x, y, color=None, title=""):
    return px.scatter(data, x=x, y=y, color=color, title=title)
