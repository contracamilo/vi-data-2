"""Indicadores y agregaciones sobre una selección de títulos."""
import pandas as pd

from ..config import MIN_VOTES, TOP_N


def kpis(df: pd.DataFrame) -> dict:
    return {
        "total": len(df),
        "movies": int((df["tipo"] == "Película").sum()),
        "shows": int((df["tipo"] == "Serie").sum()),
        "imdb_mean": df["imdb_score"].mean(),
    }


def titles_per_year(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["release_year", "tipo"]).size().reset_index(name="titulos")


def top_genres(df: pd.DataFrame, n: int = TOP_N) -> pd.DataFrame:
    counts = df["genres"].explode().dropna().value_counts().head(n)
    return counts.rename_axis("genero").reset_index(name="titulos")


def top_countries(df: pd.DataFrame, n: int = TOP_N) -> pd.DataFrame:
    counts = df["production_countries"].explode().dropna().value_counts().head(n)
    return counts.rename_axis("pais").reset_index(name="titulos")


def top_people(df: pd.DataFrame, credits: pd.DataFrame, role: str, n: int = TOP_N) -> pd.DataFrame:
    """Personas con más títulos dentro de la selección actual."""
    sel = credits[(credits["role"] == role) & credits["id"].isin(df["id"])]
    counts = sel.groupby("name")["id"].nunique().nlargest(n)
    return counts.rename("titulos").reset_index()


def certification_counts(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["age_certification"].value_counts()
    return counts.rename_axis("clasificacion").reset_index(name="titulos")


def imdb_by_genre(df: pd.DataFrame, n: int = TOP_N, min_votes: int = MIN_VOTES) -> pd.DataFrame:
    """IMDb promedio por género, ignorando títulos con pocos votos."""
    rated = df[df["imdb_votes"] >= min_votes].explode("genres").dropna(subset=["genres", "imdb_score"])
    stats = rated.groupby("genres")["imdb_score"].agg(["mean", "size"])
    stats = stats[stats["size"] >= 10].nlargest(n, "mean")
    return stats["mean"].rename("imdb").rename_axis("genero").reset_index()
