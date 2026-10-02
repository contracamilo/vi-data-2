# Dashboard Netflix (Dash)

Actividad 4 - Visualización de datos, Universidad de La Salle. Dashboard interactivo con Python, Dash y Plotly sobre el catálogo de Netflix (`archive/titles.csv`, `archive/credits.csv`).

## Arquitectura

```
src/netflix_dashboard/
├── config.py          constantes de dominio (rutas, etiquetas, límites)
├── data/              CAPA DE DATOS: leer CSV y limpiarlos (repository, cleaning)
├── logic/             LÓGICA: filtros y métricas puras sobre DataFrames (sin Dash/Plotly)
├── views/             VISTAS: tema, figuras Plotly, layout y callbacks de Dash
└── app.py             composición: carga datos -> arma layout -> registra callbacks
```

La dependencia solo apunta hacia abajo: `views -> logic`, y `app` une `data` con `views`.
`data` y `logic` no importan Dash ni Plotly (lo verifica `tests/test_logic.py`), así que se prueban sin interfaz.

## Configuración

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python -m netflix_dashboard   # servidor en http://127.0.0.1:8050
pytest                        # tests
python tools/build_notebook.py   # regenera dashboard_netflix.ipynb (entregable para Colab)
```

El notebook `dashboard_netflix.ipynb` se genera a partir de `src/`; no se edita a mano.
