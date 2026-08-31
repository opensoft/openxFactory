from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import TypeAlias, override

JsonValue: TypeAlias = (
    None | bool | int | str | list["JsonValue"] | dict[str, "JsonValue"]
)
YamlValue: TypeAlias = (
    JsonValue
    | float
    | bytes
    | date
    | set[str | int | bool | None]
    | tuple[JsonValue, JsonValue]
)
Record: TypeAlias = dict[str, JsonValue]


@dataclass(slots=True)
class InputLimitError(Exception):
    path: Path
    detail: str

    @override
    def __str__(self) -> str:
        return f"{self.path}: {self.detail}"


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    source: str
    message: str


@dataclass(frozen=True, slots=True)
class RecordDocument:
    path: Path
    data: Record


def as_record(value: JsonValue) -> Record | None:
    if isinstance(value, dict):
        return value
    return None


def as_records(value: JsonValue) -> list[Record]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def as_strings(value: JsonValue) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]
