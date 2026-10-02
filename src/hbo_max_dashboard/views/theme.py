"""Temas visuales (noche y día): única fuente de los colores de la página y de las gráficas.

La página usa variables CSS generadas desde estos objetos (`css_variables`), incluidas las
`--Dash-*` con las que Dash 4 pinta sus controles. Las figuras de Plotly no leen CSS, así que
reciben el `Theme` directamente (`figures.apply_theme`).
"""

from dataclasses import dataclass, field

from ..config import MOVIE, SHOW

FONT = "system-ui, -apple-system, Segoe UI, sans-serif"


@dataclass(frozen=True)
class Theme:
    name: str
    bg: str
    card: str
    border: str
    text: str
    muted: str
    primary: str
    secondary: str
    sequential: tuple[str, ...]  # escala continua, de poco a mucho
    hover: str  # fondo de hover/selección en controles
    palette: dict[str, str] = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "palette", {MOVIE: self.primary, SHOW: self.secondary})


DARK = Theme(
    name="dark",
    bg="#10091c",
    card="#1b1230",
    border="#342a52",
    text="#f2f0f7",
    muted="#b3a9cc",
    primary="#a274f7",
    secondary="#2dd4bf",
    sequential=("#2a1d4a", "#4c2a85", "#7c4ddb", "#b794f6", "#ede4ff"),
    hover="rgba(162, 116, 247, 0.18)",
)

LIGHT = Theme(
    name="light",
    bg="#f5f2fa",
    card="#ffffff",
    border="#e2daf0",
    text="#1d1530",
    muted="#5b5272",
    primary="#6d28d9",
    secondary="#0f766e",
    sequential=("#f1ebff", "#d4c2fb", "#a47cef", "#6d28d9", "#3b1580"),
    hover="rgba(109, 40, 217, 0.10)",
)

THEMES = {t.name: t for t in (DARK, LIGHT)}
DEFAULT_THEME = DARK.name


def get_theme(name: str | None) -> Theme:
    return THEMES.get(name or DEFAULT_THEME, DARK)


def _variables(t: Theme) -> dict[str, str]:
    return {
        # variables propias del dashboard
        "--bg": t.bg,
        "--card": t.card,
        "--border": t.border,
        "--text": t.text,
        "--muted": t.muted,
        "--primary": t.primary,
        # variables de los controles de Dash 4 (por defecto pensadas para fondo claro)
        "--Dash-Text-Primary": t.text,
        "--Dash-Text-Strong": t.text,
        "--Dash-Text-Weak": t.muted,
        "--Dash-Text-Disabled": t.muted,
        "--Dash-Fill-Inverse-Strong": t.card,
        "--Dash-Fill-Interactive-Strong": t.primary,
        "--Dash-Fill-Interactive-Weak": t.hover,
        "--Dash-Fill-Primary-Hover": t.hover,
        "--Dash-Fill-Primary-Active": t.hover,
        "--Dash-Fill-Disabled": t.border,
        "--Dash-Stroke-Strong": t.muted,
        "--Dash-Stroke-Weak": t.border,
    }


def css_variables() -> str:
    """Hoja de estilos con un bloque de variables por tema, activado por `<html data-theme=...>`."""
    blocks = []
    for theme in THEMES.values():
        body = "\n".join(f"  {k}: {v};" for k, v in _variables(theme).items())
        blocks.append(f':root[data-theme="{theme.name}"] {{\n{body}\n  color-scheme: {theme.name};\n}}')
    return "\n".join(blocks) + "\nbody { margin: 0; background: var(--bg); }\n"
