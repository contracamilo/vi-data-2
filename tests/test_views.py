import pathlib

import pytest

from hbo_max_dashboard.app import create_app
from hbo_max_dashboard.views.charts import CHARTS
from hbo_max_dashboard.views.kpis import KPIS, fmt_int, fmt_pct, fmt_score
from hbo_max_dashboard.views.theme import DARK, LIGHT, THEMES, css_variables

SRC = pathlib.Path(__file__).resolve().parents[1] / "src" / "hbo_max_dashboard"


def test_layers_do_not_import_ui():
    for layer in ("data", "logic"):
        for module in (SRC / layer).glob("*.py"):
            source = module.read_text()
            assert "import dash" not in source and "from dash" not in source, module
            assert "plotly" not in source, module


def test_chart_ids_are_unique_and_at_least_six():
    ids = [c.id for c in CHARTS] + [k.id for k in KPIS]
    assert len(ids) == len(set(ids))
    assert len(CHARTS) >= 6


@pytest.mark.parametrize("spec", CHARTS, ids=lambda s: s.id)
def test_every_chart_renders_full_and_empty(spec, titles, empty_titles, catalog):
    assert spec.render(titles, catalog.credits, DARK).layout.title.text == spec.title
    assert spec.render(empty_titles, catalog.credits, LIGHT).layout.title.text == spec.title


def test_formatting_uses_spanish_conventions():
    assert fmt_int(3294) == "3.294"
    assert fmt_score(6.884) == "6,88"
    assert fmt_pct(0.3) == "30 %"
    assert fmt_pct(None) == fmt_score(None) == "–"


def test_callback_wires_filters_to_all_outputs():
    app = create_app()
    server_callbacks = [cb["callback"] for cb in app.callback_map.values() if "callback" in cb]
    assert len(server_callbacks) == 1  # el tema se cambia en el navegador (clientside)
    callback = server_callbacks[0].__wrapped__
    out = callback(["Película", "Serie"], "__all__", [1900, 2022], "dark")
    assert len(out) == len(KPIS) + len(CHARTS)
    assert out[0] == "3.294"
    assert callback([], "__all__", [1900, 2022], "light")[0] == "0"


@pytest.mark.parametrize("theme", [DARK, LIGHT], ids=lambda t: t.name)
@pytest.mark.parametrize("chart_id", ["g-decades", "g-popularity", "g-top-rated"])  # bar, scattergl, bar_h
def test_theme_colors_reach_figures(theme, chart_id, titles, catalog):
    spec = next(c for c in CHARTS if c.id == chart_id)
    fig = spec.render(titles, catalog.credits, theme)
    assert fig.layout.paper_bgcolor == theme.card
    assert {t.name: t.marker.color for t in fig.data} == theme.palette


def test_css_defines_every_theme_and_dash_controls():
    css = css_variables()
    for name in THEMES:
        assert f':root[data-theme="{name}"]' in css
    assert "--Dash-Text-Primary" in css
