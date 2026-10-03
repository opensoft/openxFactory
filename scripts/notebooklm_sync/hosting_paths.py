from __future__ import annotations

import os
from pathlib import Path

HOSTING_ENV = "XFACTORY_NOTEBOOK_HOSTING_DECLARATION"
HOSTING_CONFIG_REL = ".xfactory/notebook-hosting.yaml"


def _resolve_against(root: Path, named: str) -> Path:
    candidate = Path(named).expanduser()
    return candidate if candidate.is_absolute() else root / candidate


def hosting_declaration_path(root: Path) -> Path | None:
    named = os.environ.get(HOSTING_ENV, "").strip()
    if named:
        return _resolve_against(root, named)
    config = root / HOSTING_CONFIG_REL
    try:
        text = config.read_text(encoding="utf-8")
    except OSError:
        return None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if len(line) - len(line.lstrip()) != 0:
            continue
        key, sep, value = line.strip().partition(":")
        if sep and key == "declaration_path":
            value = value.strip().strip('"').strip("'")
            if value:
                return _resolve_against(root, value)
            return None
    return None
