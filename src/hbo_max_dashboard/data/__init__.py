"""Capa de datos: lectura y limpieza. No conoce la lógica de negocio ni la UI."""
from .repository import load_credits, load_titles

__all__ = ["load_titles", "load_credits"]
