from __future__ import annotations

import json
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol, TypeAlias, overload

from .models import NlmCommandError

JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
ProviderResult: TypeAlias = JsonValue | str

NLM_CONFIG = Path.home() / ".notebooklm-mcp-cli" / "config.toml"
_config_path = NLM_CONFIG
_bound_profile: str | None = None
_config_cache: tuple[tuple[int, int], str | None] | None = None


def reset_profile_state(config_path: Path | None = None) -> None:
    global _bound_profile, _config_cache, _config_path
    _bound_profile = None
    _config_cache = None
    _config_path = config_path or NLM_CONFIG


def bound_profile() -> str | None:
    return _bound_profile


def clear_profile_cache() -> None:
    global _config_cache
    _config_cache = None


def configured_nlm_profile(path: Path | None = None) -> str | None:
    global _config_cache
    target = path or _config_path
    try:
        stat = target.stat()
    except OSError:
        return None
    stamp = (stat.st_mtime_ns, stat.st_size)
    if _config_cache is not None and _config_cache[0] == stamp:
        return _config_cache[1]
    try:
        text = target.read_text(encoding="utf-8")
    except OSError:
        return None
    profile: str | None = None
    section: str | None = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            continue
        if section == "auth":
            key, separator, value = line.partition("=")
            if separator and key.strip() == "default_profile":
                profile = value.strip().strip('"').strip("'") or None
                break
    _config_cache = (stamp, profile)
    return profile


def bind_profile(profile: str | None) -> None:
    global _bound_profile
    _bound_profile = profile


def assert_still_bound() -> None:
    if _bound_profile is None:
        return
    active = configured_nlm_profile()
    if active == _bound_profile:
        return
    raise SystemExit(
        "hosting: the CLI's active profile changed mid-run — bound to "
        f"{_bound_profile!r}, now {active!r}. Refusing every further invocation: "
        "the remaining work would land in an account this install has not "
        "declared. Re-bind with "
        f"`nlm login switch {_bound_profile}` and re-run; the sync is idempotent, "
        "so a resumed run is a no-op over what finished."
    )


class NotebookProvider(Protocol):
    @overload
    def invoke(self, *args: str, parse: Literal[False]) -> str: ...

    @overload
    def invoke(self, *args: str, parse: Literal[True] = True) -> ProviderResult: ...

    def invoke(self, *args: str, parse: bool = True) -> ProviderResult: ...


class ProviderPayloadError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class NotebookRow:
    notebook_id: str
    title: str


@dataclass(frozen=True, slots=True)
class SourceRow:
    source_id: str
    title: str


def _provider_rows(payload: ProviderResult, collection: str) -> list[dict[str, JsonValue]]:
    value: JsonValue | str = payload
    if isinstance(value, dict):
        value = value.get(collection, [])
    if isinstance(value, str):
        return []
    if not isinstance(value, list):
        raise ProviderPayloadError(f"NotebookLM {collection} payload must be a list")
    rows: list[dict[str, JsonValue]] = []
    for item in value:
        if not isinstance(item, dict):
            raise ProviderPayloadError(
                f"NotebookLM {collection} entries must be JSON objects"
            )
        rows.append(item)
    return rows


def _required_text(
    row: dict[str, JsonValue], keys: tuple[str, ...], *, collection: str
) -> str:
    for key in keys:
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    joined = " or ".join(keys)
    raise ProviderPayloadError(
        f"NotebookLM {collection} entry requires non-empty {joined}"
    )


def parse_notebook_rows(payload: ProviderResult) -> list[NotebookRow]:
    return [
        NotebookRow(
            notebook_id=_required_text(row, ("id",), collection="notebooks"),
            title=_required_text(row, ("title",), collection="notebooks"),
        )
        for row in _provider_rows(payload, "notebooks")
    ]


def parse_source_rows(payload: ProviderResult) -> list[SourceRow]:
    return [
        SourceRow(
            source_id=_required_text(
                row, ("id", "source_id"), collection="sources"
            ),
            title=_required_text(row, ("title",), collection="sources"),
        )
        for row in _provider_rows(payload, "sources")
    ]


@dataclass(frozen=True, slots=True)
class NlmCliProvider:
    assert_bound: Callable[[], None] = assert_still_bound
    executable: str = "nlm"

    @overload
    def invoke(self, *args: str, parse: Literal[False]) -> str: ...

    @overload
    def invoke(self, *args: str, parse: Literal[True] = True) -> ProviderResult: ...

    def invoke(self, *args: str, parse: bool = True) -> ProviderResult:
        self.assert_bound()
        command = [self.executable, *args]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            preview = result.stderr.strip()[:300]
            raise NlmCommandError(f"nlm {' '.join(args[:3])}...: {preview}")
        if not parse:
            return result.stdout
        try:
            parsed: JsonValue = json.loads(result.stdout)
        except json.JSONDecodeError:
            return result.stdout
        return parsed
