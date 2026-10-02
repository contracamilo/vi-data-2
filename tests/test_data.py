import pandas as pd

from hbo_max_dashboard.config import MOVIE, SHOW
from hbo_max_dashboard.data.cleaning import _to_list, clean_titles, missing_report


def test_to_list_handles_bad_input():
    assert _to_list("['drama', 'crime']") == ["drama", "crime"]
    assert _to_list("not a list [") == []
    assert _to_list(None) == []


def test_clean_titles_translates_and_derives_columns():
    raw = pd.DataFrame(
        {
            "id": ["a", "a", "b"],
            "type": ["MOVIE", "MOVIE", "SHOW"],
            "release_year": [1999, 1999, 2021],
            "genres": ["['scifi', 'drama']", "['scifi']", "[]"],
            "production_countries": ["['US']", "['US']", "[]"],
            "age_certification": [None, None, "TV-MA"],
        }
    )
    titles = clean_titles(raw)
    assert len(titles) == 2  # id duplicado eliminado
    assert titles.loc[0, "genres"] == ["ciencia ficción", "drama"]
    assert list(titles["tipo"]) == [MOVIE, SHOW]
    assert list(titles["decada"]) == [1990, 2020]
    assert titles.loc[0, "age_certification"] == "Sin dato"


def test_catalog_is_clean(catalog):
    assert catalog.titles["id"].is_unique
    assert all(isinstance(g, list) for g in catalog.titles["genres"])
    assert not catalog.credits.duplicated(["person_id", "id", "role"]).any()


def test_missing_report_only_lists_columns_with_gaps():
    report = missing_report(pd.DataFrame({"a": [1, None], "b": [1, 2]}))
    assert list(report.index) == ["a"] and report.loc["a", "porcentaje"] == 50.0
