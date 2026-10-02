"""Capa de datos: lectura y limpieza. No conoce la lógica de negocio ni la UI."""

from .catalog import Catalog
from .repository import load_catalog

__all__ = ["Catalog", "load_catalog"]
