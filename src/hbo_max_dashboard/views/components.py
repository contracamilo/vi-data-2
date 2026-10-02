"""Componentes HTML reutilizables del dashboard. Los colores salen de las variables CSS del tema."""

from dash import dcc, html

from .charts import ChartSpec
from .kpis import KpiSpec

CARD_STYLE = {
    "background": "var(--card)",
    "border": "1px solid var(--border)",
    "borderRadius": "10px",
    "padding": "12px 16px",
}
MUTED_TEXT = {"color": "var(--muted)", "fontSize": "13px"}


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
            html.Div(spec.label, style=MUTED_TEXT),
            html.Div(id=spec.id, style={"color": "var(--primary)", "fontSize": "28px", "fontWeight": 700}),
        ],
        style={**CARD_STYLE, "textAlign": "center"},
    )


def chart_card(spec: ChartSpec) -> html.Div:
    return html.Div(
        [
            dcc.Graph(id=spec.id, config={"displaylogo": False}),
            html.Div(spec.question, style={**MUTED_TEXT, "fontStyle": "italic", "marginTop": "6px"}),
        ],
        style=CARD_STYLE,
    )


def theme_toggle(button_id: str) -> html.Button:
    return html.Button(
        id=button_id,
        n_clicks=0,
        style={
            "background": "var(--card)",
            "color": "var(--text)",
            "border": "1px solid var(--border)",
            "borderRadius": "999px",
            "padding": "8px 16px",
            "cursor": "pointer",
            "fontSize": "14px",
            "whiteSpace": "nowrap",
        },
    )
