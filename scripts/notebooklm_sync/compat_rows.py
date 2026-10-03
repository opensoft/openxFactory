from __future__ import annotations

from collections.abc import Mapping

from .nlm_client import JsonValue


def notebook_title(notebook: Mapping[str, JsonValue]) -> str | None:
    for key in ("title", "name", "emoji_title"):
        value = notebook.get(key)
        if isinstance(value, str) and value:
            return value
    return None
