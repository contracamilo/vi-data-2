"""Componentes HTML reutilizables del dashboard."""

from dash import dcc, html

from .charts import ChartSpec
from .kpis import KpiSpec
from .theme import CARD, MUTED, PRIMARY

CARD_STYLE = {"background": CARD, "borderRadius": "10px", "padding": "12px 16px"}


def grid(children: list, min_width: int, **style) -> html.Div:
    return html.Div(
        children,
        style={
            "display": "grid",
            "gridTemplateColumns": f"repeat(auto-fit, minmax(min({min_width}px, 100%), 1fr))",
            "gap": "12px",
            "marginBottom": "12px",
            **style,
        },
    )


def filter_card(label: str, control) -> html.Div:
    return html.Div([html.Div(label, style={"marginBottom": "8px", "fontWeight": 600}), control], style=CARD_STYLE)


def kpi_card(spec: KpiSpec) -> html.Div:
    return html.Div(
        [
            html.Div(spec.label, style={"color": MUTED, "fontSize": "13px"}),
            html.Div(id=spec.id, style={"color": PRIMARY, "fontSize": "28px", "fontWeight": 700}),
        ],
        style={**CARD_STYLE, "textAlign": "center"},
    )


def chart_card(spec: ChartSpec) -> html.Div:
    return html.Div(
        [
            dcc.Graph(id=spec.id, config={"displaylogo": False}),
            html.Div(
                spec.question, style={"color": MUTED, "fontSize": "13px", "fontStyle": "italic", "marginTop": "6px"}
            ),
        ],
        style=CARD_STYLE,
    )
