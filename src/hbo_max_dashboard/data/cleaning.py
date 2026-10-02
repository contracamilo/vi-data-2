"""Limpieza y normalización de los datos crudos."""
import ast

import pandas as pd

from ..config import TYPE_LABELS


def _to_list(text) -> list:
    """Convierte "['drama', 'crime']" en ['drama', 'crime']."""
    try:
        return ast.literal_eval(text) if isinstance(text, str) else []
    except (ValueError, SyntaxError):
        return []


def clean_titles(raw: pd.DataFrame) -> pd.DataFrame:
    titles = raw.copy()
    titles["genres"] = titles["genres"].apply(_to_list)
    titles["production_countries"] = titles["production_countries"].apply(_to_list)
    titles["tipo"] = titles["type"].map(TYPE_LABELS)
    titles["age_certification"] = titles["age_certification"].fillna("Sin dato")
    return titles
