"""Estructura de la página. No contiene lógica de datos."""

from dash import dcc, html

from ..config import ALL_GENRES, TYPE_LABELS
from .charts import CHARTS
from .components import chart_card, filter_card, grid, kpi_card, theme_toggle
from .kpis import KPIS
from .theme import DEFAULT_THEME, FONT

FILTER_TYPE, FILTER_GENRE, FILTER_YEARS = "f-type", "f-genre", "f-years"
THEME_STORE, THEME_TOGGLE = "theme", "theme-toggle"


def _filters(genres: list[str], year_bounds: tuple[int, int]) -> html.Div:
    year_min, year_max = year_bounds
    first_mark = year_min - year_min % 10 + 10
    return grid(
        [
            filter_card(
                "Tipo",
                dcc.Checklist(
                    id=FILTER_TYPE,
                    options=list(TYPE_LABELS.values()),
                    value=list(TYPE_LABELS.values()),
                    inline=True,
                    inputStyle={"marginRight": "4px", "marginLeft": "12px"},
                ),
            ),
            filter_card(
                "Género",
                dcc.Dropdown(
                    id=FILTER_GENRE,
                    value=ALL_GENRES,
                    clearable=False,
                    options=[{"label": "Todos los géneros", "value": ALL_GENRES}]
                    + [{"label": g.capitalize(), "value": g} for g in genres],
                ),
            ),
            filter_card(
                "Año de estreno",
                dcc.RangeSlider(
                    id=FILTER_YEARS,
                    min=year_min,
                    max=year_max,
                    step=1,
                    value=[year_min, year_max],
                    marks={y: str(y) for y in range(first_mark, year_max + 1, 20)},
                    tooltip={"placement": "bottom"},
                ),
            ),
        ],
        min_width=260,
    )


def _header() -> html.Div:
    return html.Div(
        [
            html.Div(
                [
                    html.H1("HBO MAX · Películas y Series", style={"color": "var(--primary)", "margin": 0}),
                    html.P(
                        "Catálogo de HBO Max en EE. UU. (mayo 2022): qué ofrece, de qué épocas y qué tan bien valorado está.",
                        style={"color": "var(--muted)", "margin": "6px 0 16px"},
                    ),
                ]
            ),
            theme_toggle(THEME_TOGGLE),
        ],
        style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "gap": "12px"},
    )


def build_layout(genres: list[str], year_bounds: tuple[int, int]) -> html.Div:
    return html.Div(
        style={
            "background": "var(--bg)",
            "color": "var(--text)",
            "minHeight": "100vh",
            "padding": "20px",
            "fontFamily": FONT,
        },
        children=[
            dcc.Store(id=THEME_STORE, storage_type="local", data=DEFAULT_THEME),
            _header(),
            _filters(genres, year_bounds),
            grid([kpi_card(spec) for spec in KPIS], min_width=180),
            grid([chart_card(spec) for spec in CHARTS], min_width=520),
        ],
    )
