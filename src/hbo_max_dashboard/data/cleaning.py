"""Limpieza y normalización de los datos crudos."""

import ast

import pandas as pd

from ..config import GENRE_LABELS, TYPE_LABELS


def _to_list(text: object) -> list[str]:
    """Convierte "['drama', 'crime']" en ['drama', 'crime']."""
    try:
        return ast.literal_eval(text) if isinstance(text, str) else []
    except (ValueError, SyntaxError):
        return []


def clean_titles(raw: pd.DataFrame) -> pd.DataFrame:
    titles = raw.drop_duplicates("id").copy()
    titles["genres"] = titles["genres"].apply(lambda text: [GENRE_LABELS.get(g, g) for g in _to_list(text)])
    titles["production_countries"] = titles["production_countries"].apply(_to_list)
    titles["tipo"] = titles["type"].map(TYPE_LABELS)
    titles["decada"] = titles["release_year"] // 10 * 10
    titles["age_certification"] = titles["age_certification"].fillna("Sin dato")
    return titles.reset_index(drop=True)


def clean_credits(raw: pd.DataFrame) -> pd.DataFrame:
    return raw.drop_duplicates(["person_id", "id", "role"]).reset_index(drop=True)


def missing_report(raw: pd.DataFrame) -> pd.DataFrame:
    """Valores faltantes por columna, para documentar el procesamiento."""
    missing = raw.isna().sum()
    report = pd.DataFrame({"faltantes": missing, "porcentaje": (missing / len(raw) * 100).round(1)})
    return report[report["faltantes"] > 0].sort_values("faltantes", ascending=False)
