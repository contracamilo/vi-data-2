import pytest

from netflix_dashboard.data import load_credits, load_titles
from netflix_dashboard.logic import filters, metrics
from netflix_dashboard.config import ALL_GENRES


@pytest.fixture(scope="module")
def titles():
    return load_titles()


@pytest.fixture(scope="module")
def credits():
    return load_credits()


def test_cleaning_parses_lists(titles):
    assert all(isinstance(g, list) for g in titles["genres"])
    assert set(titles["tipo"].unique()) == {"Película", "Serie"}
    assert titles["age_certification"].notna().all()


def test_filter_by_type_and_years(titles):
    df = filters.filter_titles(titles, ["Serie"], ALL_GENRES, (2010, 2015))
    assert set(df["tipo"]) == {"Serie"}
    assert df["release_year"].between(2010, 2015).all()


def test_filter_by_genre(titles):
    df = filters.filter_titles(titles, ["Película", "Serie"], "drama", (1900, 2022))
    assert len(df) > 0 and all("drama" in g for g in df["genres"])


def test_kpis_are_consistent(titles):
    k = metrics.kpis(titles)
    assert k["total"] == k["movies"] + k["shows"]


def test_empty_selection_does_not_break(titles, credits):
    df = filters.filter_titles(titles, [], ALL_GENRES, (2000, 2022))
    assert metrics.kpis(df)["total"] == 0
    assert metrics.top_genres(df).empty
    assert metrics.top_people(df, credits, "ACTOR").empty
    assert metrics.imdb_by_genre(df).empty


def test_top_people_respects_filter(titles, credits):
    df = filters.filter_titles(titles, ["Película"], ALL_GENRES, (2000, 2022))
    top = metrics.top_people(df, credits, "ACTOR", n=5)
    assert len(top) == 5 and top["titulos"].is_monotonic_decreasing


def test_logic_and_data_layers_do_not_import_ui():
    import pathlib

    root = pathlib.Path(__file__).resolve().parents[1] / "src" / "netflix_dashboard"
    for layer in ("logic", "data"):
        for f in (root / layer).glob("*.py"):
            src = f.read_text()
            assert "dash" not in src.replace("netflix_dashboard", "") and "plotly" not in src, f
