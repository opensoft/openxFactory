from __future__ import annotations

from datetime import UTC, datetime

from .model import JsonValue


def parse_timestamp(value: JsonValue) -> datetime:
    if not isinstance(value, str):
        return datetime.min.replace(tzinfo=UTC)
    normalized = f"{value[:-1]}+00:00" if value.endswith(("Z", "z")) else value
    return datetime.fromisoformat(normalized)
