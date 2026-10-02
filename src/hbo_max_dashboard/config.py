"""Constantes de dominio compartidas por todas las capas."""

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "archive"

MOVIE, SHOW = "Película", "Serie"
TYPE_LABELS = {"MOVIE": MOVIE, "SHOW": SHOW}

GENRE_LABELS = {
    "action": "acción",
    "animation": "animación",
    "comedy": "comedia",
    "crime": "crimen",
    "documentation": "documental",
    "drama": "drama",
    "european": "europeo",
    "family": "familiar",
    "fantasy": "fantasía",
    "history": "historia",
    "horror": "terror",
    "music": "música",
    "reality": "reality",
    "romance": "romance",
    "scifi": "ciencia ficción",
    "sport": "deporte",
    "thriller": "suspenso",
    "war": "bélico",
    "western": "western",
}

ALL_GENRES = "__all__"
TOP_N = 10
MIN_GROUP_SIZE = 10  # tamaño mínimo de un grupo para que su promedio sea confiable
MIN_DECADE_SIZE = 20  # décadas con menos títulos se omiten en las series temporales
MIN_VOTES = 1_000  # votos mínimos para usar la puntuación IMDb de un título
TOP_RATED_MIN_VOTES = 10_000
