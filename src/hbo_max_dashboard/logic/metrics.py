"""Indicadores y agregaciones sobre una selección de títulos.

Funciones puras: reciben DataFrames y devuelven DataFrames o valores, sin efectos.
"""

from dataclasses import dataclass

import pandas as pd

from ..config import MIN_DECADE_SIZE, MIN_GROUP_SIZE, MIN_VOTES, MOVIE, SHOW, TOP_N, TOP_RATED_MIN_VOTES


@dataclass(frozen=True)
class Kpis:
    total: int
    movies: int
    shows: int
    imdb_mean: float | None
    share_before_2000: float | None


def kpis(df: pd.DataFrame) -> Kpis:
    total = len(df)
    imdb = df["imdb_score"].mean()
    return Kpis(
        total=total,
        movies=int((df["tipo"] == MOVIE).sum()),
        shows=int((df["tipo"] == SHOW).sum()),
        imdb_mean=None if pd.isna(imdb) else float(imdb),
        share_before_2000=float((df["release_year"] < 2000).mean()) if total else None,
    )


def _rated(df: pd.DataFrame, min_votes: int = MIN_VOTES) -> pd.DataFrame:
    """Títulos con suficientes votos para que su puntuación IMDb sea representativa."""
    return df[df["imdb_votes"] >= min_votes].dropna(subset=["imdb_score"])


def titles_by_decade(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["decada", "tipo"]).size().reset_index(name="titulos")


def genre_share_by_decade(df: pd.DataFrame, n: int = TOP_N) -> pd.DataFrame:
    """% de títulos de cada década que pertenecen a cada uno de los `n` géneros principales."""
    per_decade = df.groupby("decada").size()
    decades = per_decade[per_decade >= MIN_DECADE_SIZE].index
    exploded = df[df["decada"].isin(decades)].explode("genres").dropna(subset=["genres"])
    top = exploded["genres"].value_counts().head(n).index
    counts = exploded[exploded["genres"].isin(top)].groupby(["genres", "decada"]).size().unstack(fill_value=0)
    return (counts.div(per_decade[decades], axis=1) * 100).round(1).reindex(top)


def genre_quality(df: pd.DataFrame, min_votes: int = MIN_VOTES) -> pd.DataFrame:
    """Por género: cuántos títulos hay y qué tan bien valorados están."""
    exploded = df.explode("genres").dropna(subset=["genres"])
    size = exploded.groupby("genres").size().rename("titulos")
    rated = _rated(exploded, min_votes).groupby("genres")["imdb_score"].agg(imdb="mean", calificados="size")
    stats = rated.join(size)
    stats = stats[stats["calificados"] >= MIN_GROUP_SIZE]
    return stats.round({"imdb": 2}).rename_axis("genero").reset_index()


def imdb_by_decade(df: pd.DataFrame, min_votes: int = MIN_VOTES) -> pd.DataFrame:
    stats = _rated(df, min_votes).groupby("decada")["imdb_score"].agg(imdb="mean", titulos="size")
    return stats[stats["titulos"] >= MIN_DECADE_SIZE].round({"imdb": 2}).reset_index()


def movie_runtime_by_decade(df: pd.DataFrame) -> pd.DataFrame:
    movies = df[(df["tipo"] == MOVIE) & (df["runtime"] > 0)]
    stats = movies.groupby("decada")["runtime"].agg(duracion="median", titulos="size")
    return stats[stats["titulos"] >= MIN_DECADE_SIZE].reset_index()


def popularity_vs_quality(df: pd.DataFrame, min_votes: int = MIN_VOTES) -> pd.DataFrame:
    rated = _rated(df, min_votes)
    return rated[rated["tmdb_popularity"] > 0]


def rank_correlation(df: pd.DataFrame, x: str, y: str) -> float | None:
    """Correlación de Spearman: robusta a valores extremos como la popularidad."""
    if len(df) < MIN_GROUP_SIZE:
        return None
    return float(df[x].rank().corr(df[y].rank()))


def top_rated(df: pd.DataFrame, n: int = TOP_N, min_votes: int = TOP_RATED_MIN_VOTES) -> pd.DataFrame:
    cols = ["title", "release_year", "tipo", "imdb_score", "imdb_votes"]
    return _rated(df, min_votes).nlargest(n, ["imdb_score", "imdb_votes"])[cols]


def imdb_by_seasons(df: pd.DataFrame, max_bucket: int = 6, min_votes: int = MIN_VOTES) -> pd.DataFrame:
    """Puntuación de cada serie agrupada por número de temporadas (el último grupo es `max_bucket`+)."""
    shows = _rated(df[df["tipo"] == SHOW], min_votes).dropna(subset=["seasons"])
    seasons = shows["seasons"].astype(int).clip(upper=max_bucket)
    labels = seasons.astype(str).where(seasons < max_bucket, f"{max_bucket}+")
    return shows.assign(temporadas=labels)[["title", "temporadas", "imdb_score"]].sort_values(
        "temporadas", key=lambda s: s.str.rstrip("+").astype(int)
    )


def top_people(df: pd.DataFrame, credits: pd.DataFrame, role: str, n: int = TOP_N) -> pd.DataFrame:
    """Personas con más títulos en la selección, con su IMDb promedio y % de títulos animados."""
    sel = credits[(credits["role"] == role) & credits["id"].isin(df["id"])]
    if sel.empty:
        return pd.DataFrame(columns=["name", "titulos", "imdb", "pct_animacion"])
    info = df.set_index("id")
    sel = sel.assign(
        imdb=sel["id"].map(info["imdb_score"]),
        animada=sel["id"].map(info["genres"].apply(lambda g: "animación" in g)),
    )
    stats = sel.groupby("name").agg(titulos=("id", "nunique"), imdb=("imdb", "mean"), pct_animacion=("animada", "mean"))
    stats["pct_animacion"] *= 100
    return stats.nlargest(n, "titulos").round({"imdb": 2, "pct_animacion": 0}).reset_index()
