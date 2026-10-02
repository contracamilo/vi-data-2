# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A university assignment (Universidad de La Salle, "Actividad 4. Mi primer prototipo de dashboard", due 2026-10-04), not a software project. There is no code, build system, tests or git repo yet. The goal is a Python **Dash** dashboard built on a dataset from Kaggle or Datos Abiertos de Colombia.

Requirements from the assignment PDF (kept outside the repo, in `../vi-data-2-material/`):
- Minimum **6 visualizations** that are relevant, legible and coherent with the data.
- **Filters / interactive elements** (Dash callbacks).
- Basic data processing/cleaning before visualizing.
- Visualizations should answer meaningful questions about the dataset (the heaviest grading criterion, 2.5 of 5 points).
- Deliverables: a **notebook (.ipynb)** run in Google Colab, plus a video of at most 5 minutes explaining the dashboard. The notebook is the deliverable, so keep the dashboard self-contained in it (including how it loads the CSVs).
- `../vi-data-2-material/dashboardProfe.png` is a screenshot of the instructor's example dashboard, useful as a layout reference.

## Reference dashboard (instructor's example)

Same Netflix dataset, dark theme with red accents (Plotly dark template, `#E50914`-style red). Layout, top to bottom:
- Title and subtitle.
- Filter row: Tipo (checklist: Película/Serie), Género (dropdown, "Todos los géneros"), Año de estreno (RangeSlider, 2000-2022).
- KPI row: Títulos, Películas, Series, IMDb promedio.
- Chart grid (4 per row): titles per release year (histogram, colored by type), top genres (horizontal bar), runtime vs IMDb score (scatter), top 10 production countries (bar), top actors by number of titles (horizontal bar), age certification (donut).

The example has visible bugs to avoid: the "Títulos" KPI shows 0, and the Películas and Series KPIs show the same value (3,574). Compute each KPI from its own filtered subset.

## Data (`archive/`)

A Netflix-style titles/credits dataset (Kaggle):
- `titles.csv` (~3.4k rows): `id, title, type (MOVIE|SHOW), description, release_year, age_certification, runtime, genres, production_countries, seasons, imdb_id, imdb_score, imdb_votes, tmdb_popularity, tmdb_score`.
- `credits.csv` (~66k rows): `person_id, id, name, character, role (ACTOR|DIRECTOR)`. It joins to titles on `id`.

Gotchas for processing:
- `genres` and `production_countries` are stringified Python lists (`"['drama', 'family']"`). Parse them with `ast.literal_eval` and explode before grouping.
- `seasons` is only populated for shows, and `runtime` has a different meaning for shows (episode length).
- Scores, votes and `age_certification` have missing values.
