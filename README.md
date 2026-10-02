# HBO Max · Películas y Series (Dash)

Dashboard interactivo con Python, Dash y Plotly sobre el
catálogo de HBO Max en EE. UU. (JustWatch, mayo de 2022)

## Datos y créditos

Dataset [HBO Max TV Shows and Movies](https://www.kaggle.com/datasets/victorsoeiro/hbo-max-tv-shows-and-movies),
publicado en Kaggle por Victor Soeiro. Los datos fueron obtenidos de [JustWatch](https://www.justwatch.com/) en mayo de
2022 y corresponden al catálogo disponible en Estados Unidos. Las puntuaciones provienen de IMDb y TMDB.

## Qué responde

Diez visualizaciones, cada una ligada a una pregunta de análisis: composición del catálogo por década, evolución de los
géneros, cantidad vs. calidad por género, IMDb por década (sesgo de supervivencia), duración de las películas,
popularidad vs. calidad, títulos mejor valorados, temporadas vs. calidad, directores y actores más presentes. Filtros por
tipo, género y año recalculan cinco KPIs y todas las gráficas.

## Arquitectura

```
src/hbo_max_dashboard/
├── config.py          constantes de dominio (etiquetas, umbrales)
├── data/              CAPA DE DATOS: repository (lee CSV) · cleaning (limpia) · catalog (modelo Catalog)
├── logic/             LÓGICA: filters (Filters) · metrics (KPIs y agregaciones), funciones puras sin Dash/Plotly
├── views/             VISTAS
│   ├── charts.py      catálogo de gráficas: pregunta + métrica + figura (fuente única de verdad)
│   ├── kpis.py        KPIs de cabecera y formato en español
│   ├── figures.py     primitivas Plotly con el tema
│   ├── components.py  tarjetas y grillas
│   ├── layout.py      estructura de la página
│   └── callbacks.py   filtros -> KPIs + figuras
└── app.py             composición
```

- La dependencia apunta en un solo sentido: `views -> logic -> (DataFrames)`, y `app` conecta `data` con `views`.
  Un test verifica que `data` y `logic` no importan Dash ni Plotly.
- `views/charts.py` alimenta el layout, el callback y el notebook: agregar una gráfica es agregar un `ChartSpec`.
- El notebook entregable se **genera** desde `src/` con `tools/build_notebook.py` (no se edita a mano). La CI falla si
  quedó desactualizado.

## Configuración

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python -m hbo_max_dashboard        # servidor en http://127.0.0.1:8050 (DASH_DEBUG=0 para desactivar debug)
pytest                             # tests
ruff check . && ruff format .      # lint y formato
python tools/build_notebook.py     # regenera dashboard_hbo_max.ipynb
```

En Colab: subir `dashboard_hbo_max.ipynb`, ejecutar todo y subir los dos CSV cuando se pidan.
