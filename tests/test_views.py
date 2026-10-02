import pathlib

import pytest

from hbo_max_dashboard.app import create_app
from hbo_max_dashboard.views.charts import CHARTS
from hbo_max_dashboard.views.kpis import KPIS, fmt_int, fmt_pct, fmt_score

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
    assert spec.render(titles, catalog.credits).layout.title.text == spec.title
    assert spec.render(empty_titles, catalog.credits).layout.title.text == spec.title


def test_formatting_uses_spanish_conventions():
    assert fmt_int(3294) == "3.294"
    assert fmt_score(6.884) == "6,88"
    assert fmt_pct(0.3) == "30 %"
    assert fmt_pct(None) == fmt_score(None) == "–"


def test_callback_wires_filters_to_all_outputs():
    app = create_app()
    callback = next(iter(app.callback_map.values()))["callback"].__wrapped__
    out = callback(["Película", "Serie"], "__all__", [1900, 2022])
    assert len(out) == len(KPIS) + len(CHARTS)
    assert out[0] == "3.294"
    assert callback([], "__all__", [1900, 2022])[0] == "0"
