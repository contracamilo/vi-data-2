"""Genera `dashboard_netflix.ipynb` a partir del paquete en src/, para entregarlo
como notebook autocontenido (Colab). Ejecutar: python tools/build_notebook.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "src" / "netflix_dashboard"
MODULES = [
    "__init__", "config",
    "data/__init__", "data/cleaning", "data/repository",
    "logic/__init__", "logic/filters", "logic/metrics",
    "views/__init__", "views/theme", "views/figures", "views/layout", "views/callbacks",
    "app",
]


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip().splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": text.strip("\n").splitlines(keepends=True)}


cells = [
    md("""
# Dashboard Netflix · Películas y Series
Dashboard interactivo (Dash + Plotly) sobre el catálogo de Netflix.
El código está separado en tres capas: **datos** (`data`: lectura y limpieza), **lógica** (`logic`: filtros y métricas) y **vistas** (`views`: layout, figuras y callbacks).
"""),
    md("## 1. Dependencias"),
    code("!pip install -q dash plotly pandas"),
    md("## 2. Datos\nSube `titles.csv` y `credits.csv` (Archivos de Colab) o colócalos en la carpeta `archive/`."),
    code("""
from pathlib import Path

DATA_DIR = next((p for p in (Path("archive"), Path("/content")) if (p / "titles.csv").exists()), None)
if DATA_DIR is None:
    from google.colab import files
    files.upload()
    DATA_DIR = Path(".")
print("Datos en:", DATA_DIR.resolve())
"""),
    md("## 3. Módulos\nCada celda escribe un módulo del paquete `netflix_dashboard` (capas `data`, `logic` y `views`)."),
]
cells.append(code("from pathlib import Path\n\nfor sub in ('', 'data', 'logic', 'views'):\n    Path('netflix_dashboard', sub).mkdir(parents=True, exist_ok=True)"))
for name in MODULES:
    body = (PKG / f"{name}.py").read_text()
    cells.append(code(f"%%writefile netflix_dashboard/{name}.py\n{body}"))
cells += [
    md("## 4. Ejecutar el dashboard"),
    code("""
from netflix_dashboard.app import create_app

app = create_app(DATA_DIR)
app.run(jupyter_mode="inline", height=1400, debug=False)
"""),
]

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
      "nbformat": 4, "nbformat_minor": 5}
out = ROOT / "dashboard_netflix.ipynb"
out.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
print("Escrito", out)
