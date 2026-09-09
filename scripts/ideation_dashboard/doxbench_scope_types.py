"""The five FROZEN doxBench scope types
(`split-opendox-two-layer-product` § 3.1, pre-carve split S-1).

COLUMN: **openDox**. Lifted OUT of `doxbench_scope.py` UNCHANGED, byte for
byte, because that file's two halves belong to two different columns and
§ 3.1's carve manifest files every path with exactly ONE disposition — a file
whose halves go to two repositories cannot be filed at all. `ScopeConfinementError`,
`ScopeKey`, `ScopeDocument`, `ScopeSection` and `ScopeProjection` are frozen
value types over `(repository, ref, tile_kind, tile_id)` and a projected
document set; they carry no staging vocabulary and a reader with no notion of
factories, gates or tenants uses them exactly as this repository does. The
OWNERSHIP AUTHORITY that produces them — `resolve_scope`, path confinement
against the selected registry root, the editable classification and the
section vocabulary — stays in `doxbench_scope.py`, which is openXdox's column.

WHAT THE MOVE REMOVES. `doxbench_packet`, `doxbench_telemetry` and
`doxbench_turns` are openDox modules that imported the types ALONE out of the
openXdox module; they now import them from here and three cross-column edges
are gone. `serve_workbench.py` keeps its four lazy `doxbench_scope` imports,
because it reaches the AUTHORITY as well as the types (`resolve_scope`,
`session_created_paths_for_scope`, `is_live_session_ref`) — splitting an
import that genuinely spans both halves would trade a real edge for a
pretended one, so the manifest records it as a residual edge instead.

WHY `SCOPE_KINDS` TRAVELLED WITH THE TYPES rather than staying with the
authority. `ScopeKey.__post_init__` validates `tile_kind` against it, so the
tuple is the frozen type's own value domain: leaving it behind would need
either a circular import back into `doxbench_scope` or a second copy of the
same three strings, and a co-authoritative constant is the pattern this
repository repairs everywhere else. It has NO other reader in the tree —
every other `SCOPE_KINDS` in this package is `branch_session.SCOPE_KINDS`, a
DIFFERENT tuple with different spellings — so the move costs no caller
anything, and `doxbench_scope` re-exports it beside the five types so
`doxbench_scope.SCOPE_KINDS` and every landed import path still resolve.

NOTHING HERE REACHES a filesystem, a socket or a provider: it is five frozen
dataclasses, their `as_dict` projections and one validation tuple.

INVOCATION (design D12): `serve.py` runs BOTH as a script and as a module, so
this module uses ABSOLUTE `ideation_dashboard.*` imports, never `from . import`.
This one imports nothing from the package at all, and must not start: it is
the bottom of the scope graph.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

SCOPE_KINDS = ("cluster", "possible", "staged")


class ScopeConfinementError(ValueError):
    """Raised when snapshot or session state names an unsafe source path."""


@dataclass(frozen=True, slots=True)
class ScopeKey:
    repository: str
    ref: str
    tile_kind: str
    tile_id: str

    def __post_init__(self) -> None:
        for field_name in ("repository", "ref", "tile_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.tile_kind not in SCOPE_KINDS:
            raise ValueError(
                f"tile_kind must be one of {', '.join(SCOPE_KINDS)}"
            )

    def as_dict(self) -> dict[str, str]:
        return {
            "repository": self.repository,
            "ref": self.ref,
            "tile_kind": self.tile_kind,
            "tile_id": self.tile_id,
        }


@dataclass(frozen=True, slots=True)
class ScopeDocument:
    id: str
    path: str
    resolved: bool

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "path": self.path, "resolved": self.resolved}


@dataclass(frozen=True, slots=True)
class ScopeSection:
    key: str
    label: str
    note: str
    inherited: bool
    owned: bool
    documents: tuple[ScopeDocument, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "label": self.label,
            "note": self.note,
            "inherited": self.inherited,
            "owned": self.owned,
            "documents": [row.as_dict() for row in self.documents],
        }


@dataclass(frozen=True, slots=True)
class ScopeProjection:
    key: ScopeKey
    title: str
    keywords: tuple[str, ...]
    source_revision: str
    sections: tuple[ScopeSection, ...]
    context_paths: tuple[str, ...]
    editable_paths: tuple[str, ...]
    outline_path: str | None
    active_document_candidates: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "key": self.key.as_dict(),
            "title": self.title,
            "keywords": list(self.keywords),
            "source_revision": self.source_revision,
            "sections": [section.as_dict() for section in self.sections],
            "context_paths": list(self.context_paths),
            "editable_paths": list(self.editable_paths),
            "outline_path": self.outline_path,
            "active_document_candidates": list(
                self.active_document_candidates
            ),
        }
