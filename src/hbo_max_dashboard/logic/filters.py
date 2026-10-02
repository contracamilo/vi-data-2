"""Reglas de selección: qué títulos entran según los filtros del usuario."""
import pandas as pd

from ..config import ALL_GENRES


def filter_titles(titles: pd.DataFrame, types: list[str], genre: str, years: tuple[int, int]) -> pd.DataFrame:
    mask = titles["tipo"].isin(types) & titles["release_year"].between(*years)
    if genre != ALL_GENRES:
        mask &= titles["genres"].apply(lambda g: genre in g)
    return titles[mask]


def genre_options(titles: pd.DataFrame) -> list[str]:
    return sorted(titles["genres"].explode().dropna().unique())


def year_bounds(titles: pd.DataFrame) -> tuple[int, int]:
    return int(titles["release_year"].min()), int(titles["release_year"].max())
