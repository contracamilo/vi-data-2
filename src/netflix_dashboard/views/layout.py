"""Estructura HTML del dashboard (vista). No contiene lógica de datos."""
from dash import dcc, html

from ..config import ALL_GENRES, TYPE_LABELS, YEAR_MAX, YEAR_MIN
from .theme import BG, CARD, MUTED, RED, TEXT

CARD_STYLE = {"background": CARD, "borderRadius": "8px", "padding": "12px 16px"}
GRID_4 = {"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(300px, 1fr))", "gap": "12px", "marginBottom": "12px"}

CHARTS = [
    ("g-year", "Títulos por año"),
    ("g-genres", "Géneros"),
    ("g-scatter", "Duración vs IMDb"),
    ("g-countries", "Países"),
    ("g-actors", "Actores"),
    ("g-directors", "Directores"),
    ("g-cert", "Clasificación"),
    ("g-imdb-genre", "IMDb por género"),
]


def _filter(label: str, control) -> html.Div:
    return html.Div([html.Div(label, style={"marginBottom": "8px", "fontWeight": 600}), control], style=CARD_STYLE)


def _kpi(label: str, value_id: str) -> html.Div:
    return html.Div(
        [html.Div(label, style={"color": MUTED, "fontSize": "13px"}),
         html.Div(id=value_id, style={"color": RED, "fontSize": "28px", "fontWeight": 700})],
        style={**CARD_STYLE, "textAlign": "center"},
    )


def build_layout(genres: list[str]) -> html.Div:
    return html.Div(
        style={"background": BG, "color": TEXT, "minHeight": "100vh", "padding": "20px", "fontFamily": "system-ui, sans-serif"},
        children=[
            html.H1("NETFLIX · Películas y Series", style={"color": RED, "margin": 0}),
            html.P("Explora el catálogo de Netflix: géneros, años, puntuaciones de IMDb y elenco.", style={"color": MUTED}),
            html.Div(style={**GRID_4, "gridTemplateColumns": "1fr 1.5fr 2fr"}, children=[
                _filter("Tipo", dcc.Checklist(
                    id="f-type", value=list(TYPE_LABELS.values()), inline=True,
                    options=list(TYPE_LABELS.values()), inputStyle={"marginRight": "4px", "marginLeft": "12px"})),
                _filter("Género", dcc.Dropdown(
                    id="f-genre", value=ALL_GENRES, clearable=False,
                    options=[{"label": "Todos los géneros", "value": ALL_GENRES}] + [{"label": g, "value": g} for g in genres],
                    style={"color": "#000"})),
                _filter("Año de estreno", dcc.RangeSlider(
                    id="f-years", min=YEAR_MIN, max=YEAR_MAX, step=1, value=[YEAR_MIN, YEAR_MAX],
                    marks={y: str(y) for y in range(YEAR_MIN, YEAR_MAX + 1, 4)},
                    tooltip={"placement": "bottom", "always_visible": False})),
            ]),
            html.Div(style=GRID_4, children=[
                _kpi("Títulos", "k-total"), _kpi("Películas", "k-movies"),
                _kpi("Series", "k-shows"), _kpi("IMDb promedio", "k-imdb"),
            ]),
            html.Div(style=GRID_4, children=[html.Div(dcc.Graph(id=cid), style=CARD_STYLE) for cid, _ in CHARTS]),
        ],
    )
