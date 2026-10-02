"""Controlador: traduce los filtros de la UI en KPIs y figuras."""

from dash import Dash, Input, Output

from ..data import Catalog
from ..logic import metrics
from ..logic.filters import Filters
from .charts import CHARTS
from .kpis import KPIS
from .layout import FILTER_GENRE, FILTER_TYPE, FILTER_YEARS


def register_callbacks(app: Dash, catalog: Catalog) -> None:
    @app.callback(
        [Output(spec.id, "children") for spec in KPIS] + [Output(spec.id, "figure") for spec in CHARTS],
        Input(FILTER_TYPE, "value"),
        Input(FILTER_GENRE, "value"),
        Input(FILTER_YEARS, "value"),
    )
    def update(types, genre, years):
        selection = Filters.from_inputs(types, genre, years).apply(catalog.titles)
        values = metrics.kpis(selection)
        return [spec.format(values) for spec in KPIS] + [spec.render(selection, catalog.credits) for spec in CHARTS]
