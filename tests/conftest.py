import pytest

from hbo_max_dashboard.data import Catalog, load_catalog


@pytest.fixture(scope="session")
def catalog() -> Catalog:
    return load_catalog()


@pytest.fixture(scope="session")
def titles(catalog):
    return catalog.titles


@pytest.fixture(scope="session")
def empty_titles(titles):
    return titles.iloc[:0]
