"""Controlador: conecta los filtros con métricas y figuras."""
import pandas as pd
from dash import Dash, Input, Output

from ..logic import filters, metrics
from . import figures
from .layout import CHARTS

FILTERS = [Input("f-type", "value"), Input("f-genre", "value"), Input("f-years", "value")]
KPI_IDS = ["k-total", "k-movies", "k-shows", "k-imdb"]


def register_callbacks(app: Dash, titles: pd.DataFrame, credits: pd.DataFrame) -> None:
    @app.callback([Output(k, "children") for k in KPI_IDS] + [Output(cid, "figure") for cid, _ in CHARTS], FILTERS)
    def update(types, genre, years):
        df = filters.filter_titles(titles, types or [], genre, tuple(years))
        k = metrics.kpis(df)
        imdb = "–" if pd.isna(k["imdb_mean"]) else f"{k['imdb_mean']:.2f}"
        return (
            f"{k['total']:,}", f"{k['movies']:,}", f"{k['shows']:,}", imdb,
            figures.year_histogram(df),
            figures.genres_bar(df),
            figures.runtime_scatter(df),
            figures.countries_bar(df),
            figures.people_bar(df, credits, "ACTOR", "Actores con más títulos"),
            figures.people_bar(df, credits, "DIRECTOR", "Directores con más títulos"),
            figures.certification_donut(df),
            figures.imdb_genre_bar(df),
        )
