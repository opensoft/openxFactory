"""Local-backend "Open in NotebookLM" tile action (v2 brainstorm section
"Tile → NotebookLM"; the first dashboard ACTION and the local/served seam's
debut).

A tile (cluster / staged topic / active proposal) resolves to a document set
from the CURRENT snapshot + checkout, which is projected into an `xf-wb-<slug>`
scratch notebook through the existing `workbench.NotebookAdapter` (create-or-
rebind, sources synced by title + content hash). The bound alias is recorded in
a gitignored `ideation-workbench` manifest so the notebook survives the
orphan-sweep discipline (a notebook lives while a live manifest binds it).

Containment, by construction:
  * `tile_kind` is one of a fixed set; `tile_id` must match a conservative slug
    shape before it is used to look anything up;
  * a tile that does not resolve against the snapshot is rejected (never a
    fabricated set);
  * every resolved document is re-checked through `serve.resolve_source_path`
    (the same read-side path guard the `/source` viewer uses) before it is read,
    so an untrusted snapshot path can never escape the checkout root.

Every failure is a structured `NotebookActionError` identified by a stable code
from `ERROR_CATALOG` — the HTTP status and the caller-safe message are the
catalog's FIXED values, so request-derived data (tile ids, nlm stderr) never
enters a response; the optional `log_detail` is server-side-only diagnostics.
Never a traceback, never a hang (the adapter carries a subprocess timeout and
degrades gracefully when `nlm` is absent).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Sequence

from .action_errors import (
    ERROR_CATALOG,
    ERR_ACTION_FAILED,
    ERR_ACTION_UNAVAILABLE,
    ERR_INVALID_BODY,
    ERR_INVALID_TILE_ID,
    ERR_LOOPBACK_ONLY,
    ERR_NLM_FAILED,
    ERR_NLM_UNAVAILABLE,
    ERR_NO_READABLE_DOCUMENTS,
    ERR_SNAPSHOT_UNAVAILABLE,
    ERR_UNKNOWN_ACTION,
    ERR_UNKNOWN_TILE,
    ERR_UNKNOWN_TILE_KIND,
    error_body,
)
from .boundary import WORKBENCH_DIR, OutputBoundary
from .serve import resolve_source_path
from . import workbench as wb

# The three tile kinds that carry a doc set (mirrors the funnel/board/canvas
# cards the affordance mounts on). "realized" (archived) tiles are deliberately
# excluded — the action is for live governance material.
TILE_KINDS = ("cluster", "staged", "proposal")

# A tile id is a snapshot key (cluster id / staging id / change id): a slug of
# letters, digits, dot, dash, underscore. Validated before use as defence in
# depth even though it is only ever a dict lookup, never a raw path segment.
_TILE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,200}$")

# Skip an implausibly large file rather than shipping it as a notebook source.
_MAX_SOURCE_BYTES = 400_000

class NotebookActionError(Exception):
    """A refused/failed notebook action, identified by a stable `code` from
    `ERROR_CATALOG`. `status` and `message` are the catalog's fixed values —
    request-derived data never enters them. `log_detail` carries the
    server-side-only diagnostic (logged by the serve handler, never sent)."""

    def __init__(self, code: str, *, log_detail: str | None = None) -> None:
        self.code = code
        self.status, self.message = ERROR_CATALOG[code]
        self.log_detail = log_detail
        super().__init__(f"{code}: {self.message}")

    def body(self) -> dict:
        return error_body(self.code)


# --------------------------- pure doc-set resolution ---------------------------

def _find(rows: Any, key: str, value: str) -> dict | None:
    for row in rows or []:
        if isinstance(row, dict) and row.get(key) == value:
            return row
    return None


def _is_review_record(path: str) -> bool:
    """A proposal's review records live under a `review/` subfolder of the
    change dir; a tile projection deliberately drops them (OQ default: the whole
    change dir MINUS review records)."""
    return "review" in Path(path).parts


def resolve_tile_documents(tile_kind: str, tile_id: str, snapshot: dict) -> list[str] | None:
    """The pure snapshot -> repo-relative doc-set derivation for one tile.
    Returns the ordered doc list, or None when the tile does not resolve
    (unknown id / unrecognized kind):

      cluster  -> the cluster's Topics-derived member docs (document_edges)
      staged   -> the staging topic's files
      proposal -> the change folder's files MINUS review/ records
    """
    snap = snapshot or {}
    if tile_kind == "cluster":
        cluster = _find(snap.get("clusters"), "id", tile_id)
        if cluster is None:
            return None
        return [e["document"] for e in cluster.get("document_edges", []) if e.get("document")]
    if tile_kind == "staged":
        topic = _find(snap.get("staged_topics"), "staging_id", tile_id)
        return None if topic is None else list(topic.get("files") or [])
    if tile_kind == "proposal":
        change = _find(snap.get("changes"), "id", tile_id)
        if change is None:
            return None
        return [f for f in (change.get("files") or []) if not _is_review_record(f)]
    return None


# --------------------------- confinement + read ---------------------------

def _read_confined(checkout_root: Path, documents: Sequence[str]) -> list[tuple[str, str]]:
    """Read each repo-relative doc through the read-side path guard, dropping
    anything that escapes the checkout, is missing, oversized, or non-text.
    De-duplicates while preserving order. Returns [(path, text)]."""
    root = Path(checkout_root)
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for rel in documents:
        if not isinstance(rel, str) or rel in seen:
            continue
        seen.add(rel)
        target = resolve_source_path(root, rel)
        if target is None:
            continue
        try:
            if target.stat().st_size > _MAX_SOURCE_BYTES:
                continue
            text = target.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        out.append((rel, text))
    return out


# --------------------------- manifest binding ---------------------------

def _seed_for(tile_kind: str, tile_id: str) -> tuple[str, str | None, str]:
    """(seed kind, cluster_id, member via) for a tile kind. A cluster tile is a
    cluster-seeded set (via cluster-seed, no reason); staged/proposal tiles are
    ad-hoc sets whose members carry a recorded reason (manual-include)."""
    if tile_kind == "cluster":
        return wb.SEED_CLUSTER, tile_id, wb.VIA_CLUSTER_SEED
    return wb.SEED_ADHOC, None, wb.VIA_MANUAL_INCLUDE


def _load_or_create_workbench(checkout_root: Path, repository: str, name: str,
                              tile_kind: str, tile_id: str) -> wb.Workbench:
    path = Path(checkout_root) / wb.manifest_relpath(name)
    if path.is_file():
        try:
            return wb.Workbench.load(path)
        except (wb.WorkbenchError, OSError):
            pass  # unreadable/legacy manifest — recreate it fresh
    seed, cluster_id, _via = _seed_for(tile_kind, tile_id)
    return wb.Workbench.create(repository, name, seed=seed, cluster_id=cluster_id)


def _reconcile_members(workbench: wb.Workbench, tile_kind: str, tile_id: str,
                       documents: Sequence[tuple[str, str]], *, now: str) -> None:
    """Rebuild the manifest's members to EXACTLY the resolved set. A cluster
    tile's members enter via cluster-seed; staged/proposal via manual-include
    with a recorded reason (the tile that assembled them)."""
    _seed, _cluster, via = _seed_for(tile_kind, tile_id)
    reason = None if via == wb.VIA_CLUSTER_SEED else \
        f"{tile_kind} tile {tile_id!r} doc set (NotebookLM projection)"
    workbench.data["members"] = []
    for path, _text in documents:
        workbench.add_member(path, via, reason=reason, now=now)


def _persist_manifest(checkout_root: Path, workbench: wb.Workbench, alias: str, *, now: str) -> Path:
    """Bind the notebook alias, record the notebook action, and save the
    manifest through the interactivity boundary (allowlisted to the gitignored
    workbench prefix). Construction enforces the schema rules; a separate
    conformance test validates a produced manifest against the pinned schema."""
    workbench.bind_notebook(alias, now=now)
    workbench.record_action(wb.ACTION_NOTEBOOK, reference=alias, now=now)
    boundary = OutputBoundary(Path(checkout_root), [WORKBENCH_DIR])
    return wb.save(workbench, boundary, validate=False)


# --------------------------- orchestration ---------------------------

def run_notebook_action(*, tile_kind: str, tile_id: Any, snapshot: dict,
                        checkout_root: Path | str, adapter: wb.NotebookAdapter,
                        now: str | None = None) -> dict:
    """Resolve a tile's doc set, project it into its `xf-wb-<slug>` notebook, and
    record the binding manifest. Returns the UI contract
    `{url, notebook_alias, sources, created}`. Raises `NotebookActionError`
    (a fixed catalog code + status) on any refusal or degradation — never a
    traceback, and never a request-derived value in the error."""
    if tile_kind not in TILE_KINDS:
        raise NotebookActionError(ERR_UNKNOWN_TILE_KIND)
    if not isinstance(tile_id, str) or not _TILE_ID_RE.match(tile_id):
        raise NotebookActionError(ERR_INVALID_TILE_ID)

    documents = resolve_tile_documents(tile_kind, tile_id, snapshot)
    if documents is None:
        raise NotebookActionError(ERR_UNKNOWN_TILE)

    sources = _read_confined(Path(checkout_root), documents)
    if not sources:
        raise NotebookActionError(ERR_NO_READABLE_DOCUMENTS)

    if not adapter.available():
        raise NotebookActionError(ERR_NLM_UNAVAILABLE)

    name = f"{tile_kind}-{tile_id}"
    alias = wb.notebook_alias(name)
    result = wb.project_documents(adapter, alias, sources)
    if result.skipped or not result.ok:
        # the nlm-level detail is diagnostics for the operator, not the wire
        raise NotebookActionError(ERR_NLM_FAILED, log_detail=result.detail)

    now = now or wb._utcnow()
    repository = (snapshot or {}).get("repository") or Path(checkout_root).name
    workbench = _load_or_create_workbench(checkout_root, repository, name, tile_kind, tile_id)
    _reconcile_members(workbench, tile_kind, tile_id, sources, now=now)
    _persist_manifest(checkout_root, workbench, result.alias, now=now)

    return {"url": result.url, "notebook_alias": result.alias,
            "sources": result.sources_total, "created": result.created}
