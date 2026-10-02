"""Primitivas de gráficas Plotly.

Son funciones de presentación puras: reciben datos ya agregados y no conocen el dominio ni
los colores. `apply_theme` pinta la figura terminada con el tema activo.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .theme import FONT, Theme

HEIGHT = 380


def style(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        font=dict(family=FONT),
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(title=None, orientation="h", y=1.0, yanchor="bottom", x=1, xanchor="right"),
        hoverlabel=dict(font=dict(family=FONT)),
        height=HEIGHT,
    )
    fig.update_xaxes(zeroline=False)
    fig.update_yaxes(zeroline=False)
    return fig


# Trazas que pintamos con un color sólido. Plotly usa `scattergl` en lugar de `scatter` con muchos puntos.
SOLID_TRACES = ("bar", "scatter", "scattergl", "box")


def apply_theme(fig: go.Figure, theme: Theme, title: str = "") -> go.Figure:
    """Aplica colores del tema: fondo, textos, grilla, escala continua y series por nombre."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=theme.text), x=0.02, y=0.97),
        paper_bgcolor=theme.card,
        plot_bgcolor=theme.card,
        font=dict(color=theme.text),
    )
    # el heatmap usa la escala completa; en los demás el tono más bajo se confundiría con el fondo
    has_heatmap = any(trace.type == "heatmap" for trace in fig.data)
    fig.update_layout(coloraxis_colorscale=list(theme.sequential if has_heatmap else theme.sequential[1:]))
    fig.update_xaxes(gridcolor=theme.border, linecolor=theme.border)
    fig.update_yaxes(gridcolor=theme.border, linecolor=theme.border)
    fig.update_annotations(font_color=theme.muted, bgcolor=theme.card)
    for trace in fig.data:
        if trace.type not in SOLID_TRACES:
            continue
        if trace.type in ("scatter", "scattergl") and trace.text is not None:
            trace.textfont.color = theme.text
        if getattr(trace.marker, "coloraxis", None):  # color continuo: lo define la escala del tema
            continue
        color = theme.palette.get(trace.name, theme.primary)  # series por nombre (Película/Serie)
        trace.marker.color = color
        if trace.type != "bar":
            trace.line.color = color
    return fig


def empty(message: str = "Sin datos para esta selección") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, showarrow=False, font=dict(size=14))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return style(fig)


def note(fig: go.Figure, text: str) -> go.Figure:
    """Anotación pequeña en la esquina inferior derecha (p. ej. una correlación)."""
    fig.add_annotation(
        text=text,
        xref="paper",
        yref="paper",
        x=1,
        y=0,
        xanchor="right",
        yanchor="bottom",
        showarrow=False,
        font=dict(size=12),
    )
    return fig


def stacked_bar(data: pd.DataFrame, x: str, y: str, color: str, labels: dict[str, str]) -> go.Figure:
    if data.empty:
        return empty()
    fig = px.bar(data, x=x, y=y, color=color, labels=labels)
    fig.update_layout(barmode="stack")
    return style(fig)


def heatmap(pivot: pd.DataFrame, xlabel: str, value_label: str) -> go.Figure:
    if pivot.empty:
        return empty()
    fig = px.imshow(
        pivot,
        text_auto=".0f",
        aspect="auto",
        labels=dict(x=xlabel, y="", color=value_label),
    )
    fig.update_xaxes(type="category", showgrid=False)
    fig.update_yaxes(showgrid=False)
    return style(fig)


def bubble(data: pd.DataFrame, x: str, y: str, size: str, text: str, labels: dict[str, str]) -> go.Figure:
    if data.empty:
        return empty()
    fig = px.scatter(
        data,
        x=x,
        y=y,
        size=size,
        text=text,
        labels=labels,
        size_max=40,
        color=y,
        hover_name=text,
    )
    fig.update_traces(textposition="top center", textfont=dict(size=11))
    fig.update_layout(coloraxis_showscale=False)
    return style(fig)


def line(data: pd.DataFrame, x: str, y: str, labels: dict[str, str], hover: list[str] | None = None) -> go.Figure:
    if data.empty:
        return empty()
    fig = px.line(data, x=x, y=y, labels=labels, markers=True, hover_data=hover)
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    return style(fig)


def scatter(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str,
    labels: dict[str, str],
    hover_name: str,
    log_x: bool = False,
) -> go.Figure:
    if data.empty:
        return empty()
    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        labels=labels,
        hover_name=hover_name,
        log_x=log_x,
        opacity=0.55,
    )
    fig.update_traces(marker=dict(size=6))
    return style(fig)


def bar_h(
    data: pd.DataFrame,
    x: str,
    y: str,
    labels: dict[str, str],
    color: str | None = None,
    hover: list[str] | None = None,
    range_color: tuple[float, float] | None = None,
) -> go.Figure:
    """Barras horizontales con el primer elemento arriba. `color` puede ser categórico o numérico."""
    if data.empty:
        return empty()
    fig = px.bar(
        data.iloc[::-1],
        x=x,
        y=y,
        orientation="h",
        labels=labels,
        hover_data=hover,
        color=color,
        range_color=range_color,
    )
    fig.update_yaxes(title=None)
    return style(fig)


def box(data: pd.DataFrame, x: str, y: str, labels: dict[str, str], hover_name: str) -> go.Figure:
    if data.empty:
        return empty()
    fig = px.box(
        data,
        x=x,
        y=y,
        labels=labels,
        points="all",
        hover_name=hover_name,
    )
    fig.update_traces(marker=dict(size=4, opacity=0.5), jitter=0.4)
    return style(fig)
