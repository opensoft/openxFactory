"""Shared document inventory: the snapshot both doc-health passes and the
document catalog report against.

Extracted from `semantic.py` (openxFactory `add-document-cataloging`
tasks 3.1/3.2; feature tasks T002/T003). Two entry shapes exist:

- legacy sweep entries (`repo`, `path`, `status`, `content_hash`) — what
  the semantic sweep has always emitted; ``build_inventory(docs)``
  preserves them byte-for-byte.
- extended catalog entries (data-model.md "Inventory entry") adding
  `kind`, `repository_context`, `handling`, `artifact_type`, `revision`,
  and `snapshot_id`; produced when `repo_paths` is supplied. Promoted
  `openspec/specs/*/spec.md` documents join the extended inventory
  without expanding the governed v1 corpus. `revision` is always the
  owning repo's HEAD — never null in a freshly built inventory.

``load_previous`` is the single migration read path: prior list-format
artifacts (sweep v1) normalize to the extended entry shape with absent
extended fields set to null.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from . import corpus
from .lines import split_keepends

# Contract vocabulary — exactly two values exist for the governed v1
# corpus (document-catalog.template.yaml / tag-application matrix).
GOVERNANCE_MARKDOWN = "governance_markdown"
PROMOTED_SPEC = "promoted_spec"

_PROMOTED_SPEC_RE = re.compile(r"openspec/specs/[^/]+/spec\.md\Z")

# Fields absent from the prior list-format artifact; load_previous fills
# them with null (data-model.md, Migration).
EXTENDED_FIELDS = (
    "kind", "repository_context", "handling", "artifact_type",
    "revision", "snapshot_id",
)
BASE_FIELDS = ("repo", "path", "status", "content_hash")

# Generated catalog records (snapshots, run metadata, recommendation
# evidence) live under this prefix and are excluded from corpus
# discovery so the catalog never catalogs itself
# (add-document-cataloging "Generated catalog is encountered";
# feature task T008).
GENERATED_CATALOG_PREFIX = "health/document-catalog/"


def is_generated_catalog_path(path: str) -> bool:
    """True when a repo-relative path is generated catalog output."""
    return path.startswith(GENERATED_CATALOG_PREFIX) or \
        path == GENERATED_CATALOG_PREFIX.rstrip("/")


def _sort_key(entry: dict) -> tuple:
    return (entry["repo"], entry["path"])


def _header_value(text: str, name: str) -> str | None:
    """Value of a `Name: value` header in the doc's header block, None if
    absent — the SAME scan window, over the same real lines, the status/kind
    parsers use (`corpus.parse_status`/`parse_kind`, both through
    `doc_health.lines.split_keepends`)."""
    prefix = f"{name}: "
    for body, _ending in split_keepends(text)[:corpus.STATUS_SCAN_LINES]:
        if body.startswith(prefix):
            return body[len(prefix):].strip() or None
    return None


def artifact_type_for(path: str) -> str:
    """Contract artifact-type derivation (research D2): promoted
    `openspec/specs/*/spec.md` files are `promoted_spec`; every other
    governed Markdown document is `governance_markdown`."""
    return PROMOTED_SPEC if _PROMOTED_SPEC_RE.fullmatch(path) \
        else GOVERNANCE_MARKDOWN


def _base_entry(doc) -> dict:
    """The legacy sweep entry — byte-for-byte what semantic.py emitted."""
    return {"repo": doc.repo, "path": doc.path,
            "status": doc.status or "(none)",
            "content_hash": hashlib.sha256(doc.text.encode()).hexdigest()}


def _extended_entry(repo: str, path: str, text: str, status: str | None,
                    kind: str | None, revision: str) -> dict:
    return {
        "repo": repo,
        "path": path,
        "status": status or "(none)",
        "kind": kind,
        "repository_context": _header_value(text, "Repository context"),
        # "Handling: <value>" is an engineering-internal convention for
        # this field, not a header the openxFactory document-lifecycle
        # contract ratifies (it publishes `declared_handling` as an
        # opaque source-declared value with no prescribed header
        # syntax). Pending the openxFactory schema lane defining a
        # canonical header, this is this codebase's own reading of
        # "source-declared handling"; a ratified convention may require
        # revisiting this line.
        "handling": _header_value(text, "Handling"),
        "artifact_type": artifact_type_for(path),
        "revision": revision,
        "content_hash": hashlib.sha256(text.encode()).hexdigest(),
    }


def snapshot_id(entries: list[dict]) -> str:
    """Run-scoped inventory id: content hash of the canonical entry
    rendering with `snapshot_id` itself excluded (research D4 — derived
    from inventory content, never wall clock)."""
    canonical = json.dumps(
        [{k: v for k, v in e.items() if k != "snapshot_id"}
         for e in entries],
        sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def build_inventory(docs, repo_paths: dict | None = None,
                    git=None) -> list[dict]:
    """Machine-readable doc inventory, sorted (repo, path) for byte-stable
    emission.

    With `docs` alone: the legacy sweep entries, unchanged from the
    pre-extraction `semantic.build_inventory`. With `repo_paths`: extended
    catalog entries per data-model.md, including each repository's
    promoted specs without expanding the governed corpus. `revision` is
    the owning repo's HEAD, resolved through `git` (an injectable object
    exposing ``head_sha(repo_path)``; defaults to ``corpus.RealGit()``,
    so the documented two-argument call yields real revisions). It is
    never null in a freshly built inventory — data-model.md types it
    `str`, and null exists only on the `load_previous` migration path —
    so a doc owned by a repo absent from `repo_paths`, or a repo whose
    HEAD cannot be resolved, raises ValueError.

    Generated catalog records (paths under
    `health/document-catalog/`) are excluded in both shapes so the
    catalog never catalogs itself (recursion exclusion, task T008).
    """
    docs = [d for d in docs if not is_generated_catalog_path(d.path)]
    if repo_paths is None:
        return sorted((_base_entry(d) for d in docs), key=_sort_key)
    missing = {d.repo for d in docs} - set(repo_paths)
    if missing:
        raise ValueError("docs reference repos absent from repo_paths: "
                         + ", ".join(sorted(missing)))
    if git is None:
        git = corpus.RealGit()
    revisions = {}
    for name in sorted(repo_paths):
        head = git.head_sha(Path(repo_paths[name]))
        if not head:
            raise ValueError(f"cannot resolve HEAD revision for repo "
                             f"{name!r} at {repo_paths[name]}")
        revisions[name] = head
    entries = [
        _extended_entry(d.repo, d.path, d.text, d.status, d.kind,
                        revisions[d.repo])
        for d in docs]
    for name in sorted(repo_paths):
        repo_path = Path(repo_paths[name])
        for spec in corpus.promoted_spec_paths(repo_path):
            # Same tolerant decoding as the governed-doc walk
            # (corpus.load_docs): a single malformed-encoding file must
            # never crash the whole inventory build.
            text = spec.read_text(encoding="utf-8", errors="replace")
            entries.append(_extended_entry(
                name, spec.relative_to(repo_path).as_posix(), text,
                corpus.parse_status(text), corpus.parse_kind(text),
                revisions[name]))
    # Duplicate-key guard: governed docs (GOVERNED_ROOTS) and promoted
    # specs (openspec/specs/*/spec.md) never overlap in a real corpus
    # walk, but this function's `docs` argument is caller-supplied — a
    # duplicate (repo, path) here would silently violate the "exactly one
    # entry per document" invariant the catalog depends on, so it is
    # rejected rather than silently kept.
    seen = set()
    for entry in entries:
        key = _sort_key(entry)
        if key in seen:
            raise ValueError(f"duplicate inventory key: {key!r}")
        seen.add(key)
    entries.sort(key=_sort_key)
    sid = snapshot_id(entries)
    for entry in entries:
        entry["snapshot_id"] = sid
    return entries


def changed_paths(current: list[dict], previous: list[dict]) -> set[tuple]:
    """(repo, path) entries new or content-changed vs the previous
    inventory (hash diff, per the contract — no second git walk)."""
    prev = {(e["repo"], e["path"]): e["content_hash"] for e in previous}
    return {(e["repo"], e["path"]) for e in current
            if prev.get((e["repo"], e["path"])) != e["content_hash"]}


def load_previous(path) -> list[dict] | None:
    """Read a previous inventory artifact; None when it does not exist.

    The single migration read path: both the extended format and the
    prior list-format artifact (sweep v1) load here, normalized to the
    extended entry shape — absent extended fields become null
    (data-model.md, Migration). Anything else is rejected.
    """
    p = Path(path)
    if not p.is_file():
        return None
    raw = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError(f"unrecognized inventory artifact shape: {p}")
    entries = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict) or any(
                key not in item for key in BASE_FIELDS):
            raise ValueError(f"inventory entry {i} is not a valid "
                             f"inventory entry: {p}")
        entry = dict(item)
        for name in EXTENDED_FIELDS:
            entry.setdefault(name, None)
        entries.append(entry)
    entries.sort(key=_sort_key)
    return entries
