"""Indicadores de la cabecera: qué se muestra y cómo se formatea."""

from collections.abc import Callable
from dataclasses import dataclass

from ..logic.metrics import Kpis

NO_DATA = "–"


def fmt_int(value: int) -> str:
    """Separador de miles en español: 3294 -> '3.294'."""
    return f"{value:,}".replace(",", ".")


def fmt_pct(value: float | None) -> str:
    return NO_DATA if value is None else f"{value * 100:.0f} %"


def fmt_score(value: float | None) -> str:
    return NO_DATA if value is None else f"{value:.2f}".replace(".", ",")


@dataclass(frozen=True)
class KpiSpec:
    id: str
    label: str
    format: Callable[[Kpis], str]


KPIS: tuple[KpiSpec, ...] = (
    KpiSpec("k-total", "Títulos", lambda k: fmt_int(k.total)),
    KpiSpec("k-movies", "Películas", lambda k: fmt_int(k.movies)),
    KpiSpec("k-shows", "Series", lambda k: fmt_int(k.shows)),
    KpiSpec("k-imdb", "IMDb promedio", lambda k: fmt_score(k.imdb_mean)),
    KpiSpec("k-classics", "Estrenados antes de 2000", lambda k: fmt_pct(k.share_before_2000)),
)
