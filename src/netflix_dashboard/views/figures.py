"""Construcción de figuras Plotly (vista). Cada función recibe datos ya agregados."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ..logic import metrics
from .theme import BG, CARD, MUTED, PALETTE, RED, TEXT


def _style(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=TEXT), x=0.02),
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=TEXT),
        margin=dict(l=10, r=10, t=45, b=10),
        legend=dict(title=None, orientation="h", y=1.02, yanchor="bottom", x=1, xanchor="right"),
        height=340,
    )
    fig.update_xaxes(gridcolor="#333", zeroline=False)
    fig.update_yaxes(gridcolor="#333", zeroline=False)
    return fig


def empty_figure(title: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text="Sin datos para esta selección", showarrow=False, font=dict(color=MUTED, size=14))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return _style(fig, title)


def _bar_h(data: pd.DataFrame, y: str, x: str, title: str, xlabel: str) -> go.Figure:
    if data.empty:
        return empty_figure(title)
    fig = px.bar(data.iloc[::-1], x=x, y=y, orientation="h", color_discrete_sequence=[RED])
    fig.update_layout(xaxis_title=xlabel, yaxis_title=None)
    return _style(fig, title)


def year_histogram(df: pd.DataFrame) -> go.Figure:
    title = "Títulos por año de estreno"
    data = metrics.titles_per_year(df)
    if data.empty:
        return empty_figure(title)
    fig = px.bar(data, x="release_year", y="titulos", color="tipo", color_discrete_map=PALETTE)
    fig.update_layout(barmode="stack", xaxis_title="Año", yaxis_title="Títulos")
    return _style(fig, title)


def genres_bar(df: pd.DataFrame) -> go.Figure:
    return _bar_h(metrics.top_genres(df), "genero", "titulos", "Géneros más frecuentes", "Títulos")


def runtime_scatter(df: pd.DataFrame) -> go.Figure:
    title = "Duración vs. puntuación IMDb"
    data = df.dropna(subset=["imdb_score", "runtime"])
    if data.empty:
        return empty_figure(title)
    fig = px.scatter(
        data, x="runtime", y="imdb_score", color="tipo", color_discrete_map=PALETTE,
        hover_name="title", hover_data={"release_year": True, "tipo": False}, opacity=0.6,
    )
    fig.update_layout(xaxis_title="Duración (min)", yaxis_title="IMDb")
    return _style(fig, title)


def countries_bar(df: pd.DataFrame) -> go.Figure:
    data = metrics.top_countries(df)
    title = "Top 10 países productores"
    if data.empty:
        return empty_figure(title)
    fig = px.bar(data, x="pais", y="titulos", color_discrete_sequence=[RED])
    fig.update_layout(xaxis_title="País", yaxis_title="Títulos")
    return _style(fig, title)


def people_bar(df: pd.DataFrame, credits: pd.DataFrame, role: str, title: str) -> go.Figure:
    return _bar_h(metrics.top_people(df, credits, role), "name", "titulos", title, "Títulos")


def certification_donut(df: pd.DataFrame) -> go.Figure:
    title = "Clasificación por edades"
    data = metrics.certification_counts(df)
    if data.empty:
        return empty_figure(title)
    fig = px.pie(data, names="clasificacion", values="titulos", hole=0.5,
                 color_discrete_sequence=px.colors.sequential.Reds_r)
    fig.update_traces(textinfo="percent", marker=dict(line=dict(color=BG, width=1)))
    return _style(fig, title)


def imdb_genre_bar(df: pd.DataFrame) -> go.Figure:
    data = metrics.imdb_by_genre(df)
    fig = _bar_h(data, "genero", "imdb", "IMDb promedio por género (≥1000 votos)", "IMDb promedio")
    if not data.empty:
        fig.update_xaxes(range=[max(0, data["imdb"].min() - 0.5), data["imdb"].max() + 0.2])
    return fig
