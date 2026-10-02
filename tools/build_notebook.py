"""Genera el entregable `dashboard_hbo_max.ipynb` a partir del paquete en `src/`.

El notebook es autocontenido (funciona en Colab sin clonar el repo): cada módulo se escribe
con `%%writefile`, y la sección de análisis sale del catálogo `views.charts.CHARTS`.

Uso: python tools/build_notebook.py           regenera el notebook (sin salidas)
     python tools/build_notebook.py --check   verifica que el código coincida con src/ (CI)
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
PKG = SRC / "hbo_max_dashboard"
OUT = ROOT / "dashboard_hbo_max.ipynb"
NB_PKG_ROOT = "_notebook_pkg"  # donde el notebook escribe el paquete (ignorado por git)

sys.path.insert(0, str(SRC))
from hbo_max_dashboard.views.charts import CHARTS  # noqa: E402


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip().splitlines(keepends=True)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": text.strip("\n").splitlines(keepends=True),
    }


def package_modules() -> list[Path]:
    """Módulos del paquete, con cada `__init__.py` antes que sus hermanos."""
    files = [p for p in PKG.rglob("*.py") if p.name != "__main__.py"]
    return sorted(files, key=lambda p: (p.parent.relative_to(PKG).parts, p.name != "__init__.py", p.name))


def header_cells() -> list[dict]:
    questions = "\n".join(f"{i}. {c.question}" for i, c in enumerate(CHARTS, 1))
    return [
        md(f"""
# HBO Max · Películas y Series
**Actividad 4 · prototipo de dashboard**

**Dataset:** [HBO Max TV Shows and Movies](https://www.kaggle.com/datasets/victorsoeiro/hbo-max-tv-shows-and-movies)
(Victor Soeiro, Kaggle), con datos de [JustWatch](https://www.justwatch.com/) del catálogo de EE. UU. en mayo de 2022:
`titles.csv` con más de 3.000 títulos y `credits.csv` con más de 66.000 créditos de actores y directores.
Las puntuaciones provienen de IMDb y TMDB.

**Preguntas que responde este análisis:**

{questions}

**Arquitectura.** El código es un paquete de Python separado en tres capas:
- `data`: lectura y limpieza de los CSV (único punto que toca el disco).
- `logic`: filtros y métricas como funciones puras sobre DataFrames (sin Dash ni Plotly).
- `views`: catálogo de gráficas, componentes, layout y callbacks de Dash.

El mismo catálogo de gráficas alimenta el análisis estático de este notebook y el dashboard interactivo.
"""),
        md("## 1. Dependencias"),
        code("%pip install -q dash plotly pandas"),
        md("## 2. Datos\nSi no están en `archive/` ni en `/content`, se piden con el diálogo de carga de Colab."),
        code("""
from pathlib import Path

DATA_DIR = next((p for p in (Path("archive"), Path("/content")) if (p / "titles.csv").exists()), None)
if DATA_DIR is None:
    from google.colab import files  # solo disponible en Colab

    files.upload()  # seleccionar titles.csv y credits.csv
    DATA_DIR = Path(".")
print("Datos en:", DATA_DIR.resolve())
"""),
    ]


def module_cells() -> list[dict]:
    dirs = sorted({p.parent.relative_to(PKG).as_posix() for p in package_modules()})
    subdirs = ", ".join(f'"{d}"' for d in dirs if d != ".")
    setup = f"""
import sys
from pathlib import Path

# Carpeta aparte: si el notebook se ejecuta dentro del repo, no tapa al paquete de src/.
PKG_ROOT = Path("{NB_PKG_ROOT}")
for sub in ("", {subdirs}):
    (PKG_ROOT / "hbo_max_dashboard" / sub).mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(PKG_ROOT))
"""
    cells = [
        md("## 3. Código del proyecto\nCada celda escribe un módulo del paquete `hbo_max_dashboard`."),
        code(setup),
    ]
    for module in package_modules():
        rel = module.relative_to(PKG).as_posix()
        cells.append(code(f"%%writefile {NB_PKG_ROOT}/hbo_max_dashboard/{rel}\n{module.read_text()}"))
    return cells


def processing_cells() -> list[dict]:
    return [
        md("## 4. Procesamiento de los datos\n### Datos crudos"),
        code("""
from hbo_max_dashboard.data.cleaning import missing_report
from hbo_max_dashboard.data.repository import read_csv

raw_titles = read_csv("titles", DATA_DIR)
raw_credits = read_csv("credits", DATA_DIR)
print(f"titles: {raw_titles.shape}   credits: {raw_credits.shape}")
raw_titles.head(3)
"""),
        md("### Valores faltantes"),
        code("missing_report(raw_titles)"),
        md("""
### Limpieza aplicada (`data/cleaning.py`)
- `genres` y `production_countries` vienen como texto (`"['drama', 'crime']"`): se convierten en listas y los géneros se traducen al español.
- `type` (MOVIE/SHOW) se traduce a `tipo` (Película/Serie) y se deriva la `decada` de estreno.
- `age_certification` faltante se marca como `Sin dato`.
- Se eliminan títulos y créditos duplicados.
- Las puntuaciones IMDb solo se promedian para títulos con al menos 1.000 votos, y los grupos con menos de 10 títulos (o décadas con menos de 20) se omiten para evitar promedios poco confiables.
"""),
        code("""
from hbo_max_dashboard.data import load_catalog

catalog = load_catalog(DATA_DIR)
print(f"Títulos: {len(catalog.titles)} (duplicados eliminados: {len(raw_titles) - len(catalog.titles)})")
print(f"Créditos: {len(catalog.credits)} (duplicados eliminados: {len(raw_credits) - len(catalog.credits)})")
catalog.titles[["title", "tipo", "release_year", "decada", "genres", "imdb_score"]].head()
"""),
    ]


def analysis_cells() -> list[dict]:
    cells = [
        md("## 5. Análisis: preguntas y hallazgos\nCada gráfica responde una pregunta sobre el catálogo completo."),
        code("""
from hbo_max_dashboard.views.charts import CHARTS
from hbo_max_dashboard.views.theme import LIGHT  # tema claro para las figuras estáticas del informe


def show(chart_id: str) -> None:
    spec = next(c for c in CHARTS if c.id == chart_id)
    spec.render(catalog.titles, catalog.credits, LIGHT).show()
"""),
    ]
    for i, spec in enumerate(CHARTS, 1):
        cells += [
            md(f"### 5.{i} {spec.title}\n**Pregunta:** {spec.question}"),
            code(f'show("{spec.id}")'),
            md(f"**Hallazgo:** {spec.insight}"),
        ]
    return cells


def closing_cells() -> list[dict]:
    return [
        md("""
## 6. Conclusiones
- HBO Max combina dos catálogos: una biblioteca de clásicos (30 % anterior al año 2000) y una oferta reciente cada vez más centrada en series y documentales.
- La calidad percibida depende más del nicho que del volumen: historia, documental y bélico superan a comedia, acción y terror.
- Las producciones antiguas puntúan más alto por sesgo de supervivencia, no porque el cine antiguo sea mejor en sí mismo.
- La popularidad no predice la calidad, y lo mejor valorado de la plataforma son sus series originales de HBO.
- Por número de apariciones, el catálogo lo definen los autores clásicos y los actores de doblaje de animación, no las estrellas de Hollywood.
"""),
        md(
            "## 7. Dashboard interactivo\nLos filtros de tipo, género y año recalculan los KPIs y las 10 gráficas. El botón de la esquina cambia entre modo día y noche."
        ),
        code("""
from hbo_max_dashboard.app import create_app

app = create_app(DATA_DIR)
app.run(jupyter_mode="inline", height=2600, debug=False)
"""),
    ]


def build() -> dict:
    cells = header_cells() + module_cells() + processing_cells() + analysis_cells() + closing_cells()
    for i, cell in enumerate(cells):
        cell["id"] = f"cell-{i:03d}"  # ids estables: regenerar no produce diffs innecesarios
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def _sources(notebook: dict) -> list[tuple[str, str]]:
    """Tipo y contenido de cada celda; ignora salidas y metadatos que agrega Colab al ejecutar."""
    return [(c["cell_type"], "".join(c["source"])) for c in notebook["cells"]]


def check() -> int:
    """Verifica que el notebook versionado tenga el mismo código que `src/` (puede incluir salidas)."""
    committed = json.loads(OUT.read_text())
    expected, actual = _sources(build()), _sources(committed)
    if expected == actual:
        print(f"{OUT.name} está al día con src/")
        return 0
    stale = next(
        (i for i, (e, a) in enumerate(zip(expected, actual, strict=False)) if e != a), min(len(expected), len(actual))
    )
    print(f"{OUT.name} está desactualizado (primera diferencia en la celda {stale}).")
    print("Ejecuta: python tools/build_notebook.py")
    return 1


def main() -> None:
    if "--check" in sys.argv:
        sys.exit(check())
    notebook = build()
    OUT.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
    print(f"Escrito {OUT.relative_to(ROOT)} ({len(notebook['cells'])} celdas)")


if __name__ == "__main__":
    main()
