"""Constantes compartidas: rutas, etiquetas y paleta."""
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "archive"

TYPE_LABELS = {"MOVIE": "Película", "SHOW": "Serie"}
ALL_GENRES = "__all__"

YEAR_MIN, YEAR_MAX = 2000, 2022
TOP_N = 10
MIN_VOTES = 1000  # votos mínimos para promediar IMDb por género
