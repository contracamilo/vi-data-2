# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A university assignment (Universidad de La Salle, "Actividad 4. Mi primer prototipo de dashboard", due 2026-10-04), not a software project. The repo is `contracamilo/vi-data-2` on GitHub (private). The goal is a Python **Dash** dashboard built on a dataset from Kaggle or Datos Abiertos de Colombia.

Requirements from the assignment PDF (kept outside the repo, in `../vi-data-2-material/`):
- Minimum **6 visualizations** that are relevant, legible and coherent with the data.
- **Filters / interactive elements** (Dash callbacks).
- Basic data processing/cleaning before visualizing.
- Visualizations should answer meaningful questions about the dataset (the heaviest grading criterion, 2.5 of 5 points).
- Deliverables: a **notebook (.ipynb)** run in Google Colab, plus a video of at most 5 minutes explaining the dashboard. The notebook is self-contained and generated from `src/` (see Architecture); in Colab the user uploads the CSVs.
- `../vi-data-2-material/dashboardProfe.png` is a screenshot of the instructor's example dashboard, useful as a layout reference.

## Commands

```bash
source .venv/bin/activate && pip install -r requirements.txt   # setup (editable install)
python -m hbo_max_dashboard                                    # run the dashboard (port 8050)
pytest                                                         # all tests
pytest tests/test_logic.py::test_kpis_are_consistent           # single test
python tools/build_notebook.py                                 # regenerate dashboard_hbo_max.ipynb
```

## Architecture

Package in `src/hbo_max_dashboard/` with three layers; dependencies point only downward (enforced by a test):
- `data/`: `repository.py` reads CSVs (only module touching disk), `cleaning.py` parses list columns and normalizes. No Dash/Plotly.
- `logic/`: `filters.py` (selection rules) and `metrics.py` (KPIs and aggregations), pure functions on DataFrames. No Dash/Plotly.
- `views/`: `theme.py`, `figures.py` (one Plotly figure per function), `layout.py`, `callbacks.py` (single callback: filters -> 4 KPIs + 8 figures). `layout.CHARTS` and the callback outputs must stay in the same order.
- `app.py` composes them; `config.py` holds domain constants.

The `.ipynb` deliverable is **generated** by `tools/build_notebook.py`, which embeds every module as a `%%writefile` cell. Never edit the notebook by hand. When adding or moving a module, update `MODULES` in that script.

## Reference dashboard (instructor's example)

The example was built on this same dataset (the screenshot is branded Netflix, but the data is HBO Max). Our version uses a dark purple HBO Max theme (`views/theme.py`). The slider range comes from the data (~30% of titles predate 2000). Layout, top to bottom:
- Title and subtitle.
- Filter row: Tipo (checklist: Película/Serie), Género (dropdown, "Todos los géneros"), Año de estreno (RangeSlider, 2000-2022).
- KPI row: Títulos, Películas, Series, IMDb promedio.
- Chart grid (4 per row): titles per release year (histogram, colored by type), top genres (horizontal bar), runtime vs IMDb score (scatter), top 10 production countries (bar), top actors by number of titles (horizontal bar), age certification (donut).

The example has visible bugs to avoid: the "Títulos" KPI shows 0, and the Películas and Series KPIs show the same value (3,574). Compute each KPI from its own filtered subset.

## Data (`archive/`)

HBO Max catalog (JustWatch, US, May 2022; Kaggle) titles/credits:
- `titles.csv` (~3.3k rows): `id, title, type (MOVIE|SHOW), description, release_year, age_certification, runtime, genres, production_countries, seasons, imdb_id, imdb_score, imdb_votes, tmdb_popularity, tmdb_score`.
- `credits.csv` (~66k rows): `person_id, id, name, character, role (ACTOR|DIRECTOR)`. It joins to titles on `id`.

Gotchas for processing:
- `genres` and `production_countries` are stringified Python lists (`"['drama', 'family']"`). Parse them with `ast.literal_eval` and explode before grouping.
- `seasons` is only populated for shows, and `runtime` has a different meaning for shows (episode length).
- Scores, votes and `age_certification` have missing values.
