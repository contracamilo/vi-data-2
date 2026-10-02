"""Catálogo de visualizaciones: única fuente de verdad para el dashboard y el notebook.

Cada `ChartSpec` une una pregunta de análisis con la métrica que la responde (capa de lógica)
y la primitiva que la dibuja (`figures`). El layout, los callbacks y el notebook iteran
`CHARTS`, así que agregar una gráfica es agregar una entrada aquí.
"""

from collections.abc import Callable
from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go

from ..logic import metrics
from . import figures

Builder = Callable[[pd.DataFrame, pd.DataFrame], go.Figure]


@dataclass(frozen=True)
class ChartSpec:
    id: str
    title: str
    question: str
    insight: str  # lectura sobre el catálogo completo, se usa en el notebook
    build: Builder

    def render(self, titles: pd.DataFrame, credits: pd.DataFrame) -> go.Figure:
        return self.build(titles, credits).update_layout(title_text=self.title)


def _catalog_by_decade(titles: pd.DataFrame, _: pd.DataFrame) -> go.Figure:
    return figures.stacked_bar(
        metrics.titles_by_decade(titles),
        x="decada",
        y="titulos",
        color="tipo",
        labels={"decada": "Década de estreno", "titulos": "Títulos"},
    )


def _genre_mix(titles: pd.DataFrame, _: pd.DataFrame) -> go.Figure:
    return figures.heatmap(metrics.genre_share_by_decade(titles), xlabel="Década", value_label="% títulos")


def _genre_quality(titles: pd.DataFrame, _: pd.DataFrame) -> go.Figure:
    return figures.bubble(
        metrics.genre_quality(titles),
        x="titulos",
        y="imdb",
        size="calificados",
        text="genero",
        labels={"titulos": "Títulos en el catálogo", "imdb": "IMDb promedio", "calificados": "Títulos calificados"},
    )


def _imdb_by_decade(titles: pd.DataFrame, _: pd.DataFrame) -> go.Figure:
    return figures.line(
        metrics.imdb_by_decade(titles),
        x="decada",
        y="imdb",
        hover=["titulos"],
        labels={"decada": "Década de estreno", "imdb": "IMDb promedio", "titulos": "Títulos"},
    )


def _runtime_by_decade(titles: pd.DataFrame, _: pd.DataFrame) -> go.Figure:
    return figures.line(
        metrics.movie_runtime_by_decade(titles),
        x="decada",
        y="duracion",
        hover=["titulos"],
        labels={"decada": "Década de estreno", "duracion": "Duración mediana (min)", "titulos": "Películas"},
    )


def _popularity_vs_quality(titles: pd.DataFrame, _: pd.DataFrame) -> go.Figure:
    data = metrics.popularity_vs_quality(titles)
    fig = figures.scatter(
        data,
        x="tmdb_popularity",
        y="imdb_score",
        color="tipo",
        hover_name="title",
        log_x=True,
        labels={"tmdb_popularity": "Popularidad TMDB (escala log)", "imdb_score": "IMDb"},
    )
    rho = metrics.rank_correlation(data, "tmdb_popularity", "imdb_score")
    return figures.note(fig, f"Correlación (Spearman) = {rho:.2f}") if rho is not None else fig


def _top_rated(titles: pd.DataFrame, _: pd.DataFrame) -> go.Figure:
    fig = figures.bar_h(
        metrics.top_rated(titles),
        x="imdb_score",
        y="title",
        color="tipo",
        hover=["release_year", "imdb_votes"],
        labels={"imdb_score": "IMDb", "title": "", "release_year": "Año", "imdb_votes": "Votos", "tipo": ""},
    )
    return fig.update_xaxes(range=[7, 10])


def _seasons_quality(titles: pd.DataFrame, _: pd.DataFrame) -> go.Figure:
    return figures.box(
        metrics.imdb_by_seasons(titles),
        x="temporadas",
        y="imdb_score",
        hover_name="title",
        labels={"temporadas": "Temporadas", "imdb_score": "IMDb"},
    )


def _top_directors(titles: pd.DataFrame, credits: pd.DataFrame) -> go.Figure:
    return figures.bar_h(
        metrics.top_people(titles, credits, "DIRECTOR"),
        x="titulos",
        y="name",
        color="imdb",
        range_color=(5.5, 8.5),
        labels={"titulos": "Títulos", "name": "", "imdb": "IMDb prom."},
    )


def _top_actors(titles: pd.DataFrame, credits: pd.DataFrame) -> go.Figure:
    return figures.bar_h(
        metrics.top_people(titles, credits, "ACTOR"),
        x="titulos",
        y="name",
        color="pct_animacion",
        range_color=(0, 100),
        labels={"titulos": "Títulos", "name": "", "pct_animacion": "% animación"},
    )


CHARTS: tuple[ChartSpec, ...] = (
    ChartSpec(
        "g-decades",
        "Catálogo por década de estreno",
        "¿HBO Max es un catálogo de estrenos o de clásicos?",
        "El 30 % del catálogo se estrenó antes del año 2000 y hay películas desde la década de 1910: HBO Max mantiene una biblioteca de clásicos (Warner, TCM, Criterion) muy superior a la de otras plataformas. Las series prácticamente no existen antes de 1990 y su peso crece en cada década: en los 2020 ya son el 41 % de los estrenos.",
        _catalog_by_decade,
    ),
    ChartSpec(
        "g-genre-mix",
        "Peso de cada género por década (%)",
        "¿Cómo ha cambiado la oferta de géneros con el tiempo?",
        "El drama dominaba el cine clásico (70–80 % de los títulos entre 1930 y 1959) y hoy está en torno al 35 %. El romance cae del 51 % en los años 30 al 6 % en los 2020, mientras que el documental pasa de menos del 3 % entre 1930 y 1959 a más del 30 % desde 2010: la plataforma apuesta por la no ficción en su contenido reciente.",
        _genre_mix,
    ),
    ChartSpec(
        "g-genre-quality",
        "Cantidad vs. calidad por género",
        "¿Los géneros más abundantes son también los mejor valorados?",
        "Cantidad y calidad no van de la mano. Comedia (1.120 títulos) y acción están por debajo del promedio, y terror es el peor valorado (6,5). Los mejor puntuados son géneros de nicho: historia (7,5), documental y bélico (7,3–7,4). El drama es la excepción: es el género más abundante y aun así está entre los mejor valorados (7,15).",
        _genre_quality,
    ),
    ChartSpec(
        "g-imdb-decade",
        "IMDb promedio por década de estreno",
        "¿Las producciones antiguas están mejor valoradas que las recientes?",
        "Las producciones de 1920–1960 promedian ~7,4 en IMDb y las de 1980 en adelante ~6,8. No es que el cine antiguo fuera mejor: es un sesgo de supervivencia. Del pasado solo se conservan y licencian los clásicos que resistieron el tiempo, mientras que del presente llega todo lo que se produce.",
        _imdb_by_decade,
    ),
    ChartSpec(
        "g-runtime",
        "Duración mediana de las películas",
        "¿Las películas se han vuelto más largas o más cortas?",
        "La duración mediana de las películas se estabilizó en ~100–105 minutos desde los años 40 hasta los 2000, y en las dos últimas décadas bajó a ~90 minutos. Antes de 1930 dominan los cortometrajes y largometrajes mudos más breves (Chaplin, por ejemplo).",
        _runtime_by_decade,
    ),
    ChartSpec(
        "g-popularity",
        "Popularidad vs. calidad",
        "¿Lo más popular es lo mejor valorado?",
        "La correlación de rangos entre popularidad en TMDB y puntuación IMDb es prácticamente nula (≈ 0,01). Hay títulos muy populares con notas mediocres y joyas con poca audiencia: la popularidad no es un buen indicador de calidad para recomendar contenido.",
        _popularity_vs_quality,
    ),
    ChartSpec(
        "g-top-rated",
        "Los 10 títulos mejor valorados (≥10.000 votos)",
        "¿Qué es lo mejor del catálogo y de dónde viene?",
        "7 de los 10 títulos mejor valorados son series, y cinco de ellas son producciones originales de HBO (Chernobyl, Band of Brothers, The Wire, Game of Thrones, The Sopranos). El valor diferencial de la plataforma está en su contenido propio, no solo en el licenciado.",
        _top_rated,
    ),
    ChartSpec(
        "g-seasons",
        "IMDb de las series según sus temporadas",
        "¿Las series que duran más temporadas son mejores?",
        "Las series con 3–5 temporadas tienen una mediana de IMDb ligeramente mayor (7,8–7,95) que las de una sola temporada (7,6). El efecto es pequeño y se explica por selección: solo se renuevan las series que funcionan. A partir de 6 temporadas la nota vuelve a bajar un poco.",
        _seasons_quality,
    ),
    ChartSpec(
        "g-directors",
        "Directores con más títulos",
        "¿Qué directores definen el catálogo y qué tan bien valorados están?",
        "Los directores más presentes son autores clásicos: Charlie Chaplin, Yasujirō Ozu, Satyajit Ray, Ingmar Bergman y Hayao Miyazaki, todos con IMDb promedio cercano a 8. Junto a ellos aparecen documentalistas de HBO (Jon Alpert, Alexandra Pelosi) y Sam Liu, director de las películas animadas de DC.",
        _top_directors,
    ),
    ChartSpec(
        "g-actors",
        "Actores con más títulos",
        "¿Quiénes aparecen más en el catálogo y en qué tipo de contenido?",
        "Los actores con más títulos son actores de doblaje (Grey DeLisle, Frank Welker, Tara Strong, Tom Kenny) y más de la mitad de sus títulos son animados: el catálogo de animación de Warner Bros. y Cartoon Network pesa más que cualquier estrella de cine. El único actor de imagen real en el top es Charlie Chaplin.",
        _top_actors,
    ),
)
