"""Composición: carga los datos, arma el layout y registra los callbacks."""

from pathlib import Path

from dash import Dash

from .config import DATA_DIR
from .data import load_catalog
from .logic.filters import genre_options, year_bounds
from .views.callbacks import register_callbacks
from .views.layout import build_layout
from .views.theme import DEFAULT_THEME, css_variables


def create_app(data_dir: Path = DATA_DIR) -> Dash:
    catalog = load_catalog(data_dir)
    app = Dash(__name__, title="HBO Max · Películas y Series")
    app.index_string = _index_html()
    app.layout = build_layout(genre_options(catalog.titles), year_bounds(catalog.titles))
    register_callbacks(app, catalog)
    return app


def _index_html() -> str:
    """Plantilla HTML de Dash con las variables CSS de los temas embebidas (sin archivos de assets)."""
    return f"""<!DOCTYPE html>
<html data-theme="{DEFAULT_THEME}">
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>{css_variables()}</style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>{{%config%}}{{%scripts%}}{{%renderer%}}</footer>
    </body>
</html>"""
