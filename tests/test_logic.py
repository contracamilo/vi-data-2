import pytest

from hbo_max_dashboard.config import ALL_GENRES, MOVIE, SHOW
from hbo_max_dashboard.logic import metrics
from hbo_max_dashboard.logic.filters import Filters


def test_filters_from_inputs_normalizes_ui_values():
    f = Filters.from_inputs(None, None, [1990.0, 2000.0])
    assert f == Filters(types=(), genre=ALL_GENRES, years=(1990, 2000))


def test_filter_by_type_years_and_genre(titles):
    df = Filters((SHOW,), "drama", (2010, 2015)).apply(titles)
    assert len(df) > 0
    assert set(df["tipo"]) == {SHOW}
    assert df["release_year"].between(2010, 2015).all()
    assert all("drama" in g for g in df["genres"])


def test_kpis_are_consistent(titles):
    k = metrics.kpis(titles)
    assert k.total == k.movies + k.shows == len(titles)
    assert 0 < k.share_before_2000 < 1


def test_kpis_on_empty_selection(empty_titles):
    k = metrics.kpis(empty_titles)
    assert (k.total, k.imdb_mean, k.share_before_2000) == (0, None, None)


def test_genre_share_is_a_percentage(titles):
    share = metrics.genre_share_by_decade(titles)
    assert ((share >= 0) & (share <= 100)).all().all()
    assert "drama" in share.index


def test_runtime_only_uses_movies(titles):
    shows_only = titles[titles["tipo"] == SHOW]
    assert metrics.movie_runtime_by_decade(shows_only).empty


def test_seasons_only_uses_shows_and_buckets(titles):
    data = metrics.imdb_by_seasons(titles)
    assert set(data["temporadas"]) <= {"1", "2", "3", "4", "5", "6+"}
    assert metrics.imdb_by_seasons(titles[titles["tipo"] == MOVIE]).empty


def test_top_rated_respects_min_votes(titles):
    top = metrics.top_rated(titles, n=5, min_votes=50_000)
    assert len(top) == 5 and (top["imdb_votes"] >= 50_000).all()
    assert top["imdb_score"].is_monotonic_decreasing


def test_top_people_respects_selection(titles, catalog):
    movies = titles[titles["tipo"] == MOVIE]
    top = metrics.top_people(movies, catalog.credits, "DIRECTOR", n=5)
    assert len(top) == 5 and top["titulos"].is_monotonic_decreasing
    assert top["pct_animacion"].between(0, 100).all()


@pytest.mark.parametrize(
    "fn",
    [
        metrics.titles_by_decade,
        metrics.genre_share_by_decade,
        metrics.genre_quality,
        metrics.imdb_by_decade,
        metrics.movie_runtime_by_decade,
        metrics.popularity_vs_quality,
        metrics.top_rated,
        metrics.imdb_by_seasons,
    ],
)
def test_metrics_handle_empty_selection(fn, empty_titles):
    assert fn(empty_titles).empty


def test_rank_correlation_needs_enough_data(empty_titles):
    assert metrics.rank_correlation(empty_titles, "imdb_score", "tmdb_score") is None
