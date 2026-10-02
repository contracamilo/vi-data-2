"""Reglas de selección: qué títulos entran según los filtros del usuario."""

from collections.abc import Sequence
from dataclasses import dataclass

import pandas as pd

from ..config import ALL_GENRES


@dataclass(frozen=True)
class Filters:
    types: tuple[str, ...]
    genre: str = ALL_GENRES
    years: tuple[int, int] | None = None

    @classmethod
    def from_inputs(cls, types: Sequence[str] | None, genre: str | None, years: Sequence[int] | None) -> "Filters":
        """Normaliza los valores crudos que llegan de los controles de la UI."""
        return cls(
            types=tuple(types or ()),
            genre=genre or ALL_GENRES,
            years=(int(years[0]), int(years[1])) if years else None,
        )

    def apply(self, titles: pd.DataFrame) -> pd.DataFrame:
        mask = titles["tipo"].isin(self.types)
        if self.years:
            mask &= titles["release_year"].between(*self.years)
        if self.genre != ALL_GENRES:
            mask &= titles["genres"].apply(lambda genres: self.genre in genres)
        return titles[mask]


def genre_options(titles: pd.DataFrame) -> list[str]:
    return sorted(titles["genres"].explode().dropna().unique())


def year_bounds(titles: pd.DataFrame) -> tuple[int, int]:
    return int(titles["release_year"].min()), int(titles["release_year"].max())
