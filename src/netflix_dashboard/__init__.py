"""Dashboard interactivo del catálogo de Netflix.

Capas (la dependencia solo apunta hacia abajo):
    views  ->  logic      (Dash/Plotly; filtros y métricas)
    app    ->  data       (composición; lectura y limpieza de CSV)
"""
