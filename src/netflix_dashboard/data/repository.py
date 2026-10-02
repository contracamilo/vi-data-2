"""Acceso a las fuentes de datos (CSV). Único módulo que toca el disco."""
from pathlib import Path

import pandas as pd

from ..config import DATA_DIR
from .cleaning import clean_titles


def read_csv(name: str, data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Lee `name.csv` o `name_csv.zip`, lo que exista."""
    for candidate in (f"{name}.csv", f"{name}_csv.zip"):
        path = Path(data_dir) / candidate
        if path.exists():
            return pd.read_csv(path)
    raise FileNotFoundError(f"No se encontró {name}.csv ni {name}_csv.zip en {data_dir}")


def load_titles(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    return clean_titles(read_csv("titles", data_dir))


def load_credits(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    return read_csv("credits", data_dir)
