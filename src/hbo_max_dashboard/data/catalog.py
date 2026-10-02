"""Modelo de datos del catálogo."""

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class Catalog:
    """Títulos y créditos ya limpios. Se carga una vez y no se modifica."""

    titles: pd.DataFrame
    credits: pd.DataFrame
