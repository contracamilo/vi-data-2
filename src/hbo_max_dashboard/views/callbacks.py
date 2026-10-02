"""Controlador: traduce los filtros y el tema de la UI en KPIs y figuras."""

from dash import Dash, Input, Output, State

from ..data import Catalog
from ..logic import metrics
from ..logic.filters import Filters
from .charts import CHARTS
from .kpis import KPIS
from .layout import FILTER_GENRE, FILTER_TYPE, FILTER_YEARS, THEME_STORE, THEME_TOGGLE
from .theme import DARK, LIGHT, get_theme

# El cambio de tema ocurre en el navegador (sin ida y vuelta al servidor) para que sea instantáneo.
_TOGGLE_THEME_JS = f"""
function(nClicks, current) {{
    return current === "{LIGHT.name}" ? "{DARK.name}" : "{LIGHT.name}";
}}
"""

_APPLY_THEME_JS = f"""
function(theme) {{
    document.documentElement.dataset.theme = theme || "{DARK.name}";
    return theme === "{LIGHT.name}" ? "🌙 Modo noche" : "☀️ Modo día";
}}
"""


def register_callbacks(app: Dash, catalog: Catalog) -> None:
    app.clientside_callback(
        _TOGGLE_THEME_JS,
        Output(THEME_STORE, "data"),
        Input(THEME_TOGGLE, "n_clicks"),
        State(THEME_STORE, "data"),
        prevent_initial_call=True,  # si no, su no-op inicial bloquea el callback que aplica el tema
    )
    app.clientside_callback(_APPLY_THEME_JS, Output(THEME_TOGGLE, "children"), Input(THEME_STORE, "data"))

    @app.callback(
        [Output(spec.id, "children") for spec in KPIS] + [Output(spec.id, "figure") for spec in CHARTS],
        Input(FILTER_TYPE, "value"),
        Input(FILTER_GENRE, "value"),
        Input(FILTER_YEARS, "value"),
        Input(THEME_STORE, "data"),
    )
    def update(types, genre, years, theme_name):
        selection = Filters.from_inputs(types, genre, years).apply(catalog.titles)
        theme = get_theme(theme_name)
        values = metrics.kpis(selection)
        return [spec.format(values) for spec in KPIS] + [
            spec.render(selection, catalog.credits, theme) for spec in CHARTS
        ]
