"""Fábrica de la aplicación Dash."""
from pathlib import Path

from dash import Dash

from .config import DATA_DIR
from .data import load_credits, load_titles
from .logic.filters import genre_options, year_bounds
from .views.callbacks import register_callbacks
from .views.layout import build_layout


def create_app(data_dir: Path = DATA_DIR) -> Dash:
    titles = load_titles(data_dir)
    credits = load_credits(data_dir)
    app = Dash(__name__, title="HBO Max · Películas y Series")
    app.layout = build_layout(genre_options(titles), year_bounds(titles))
    register_callbacks(app, titles, credits)
    return app
