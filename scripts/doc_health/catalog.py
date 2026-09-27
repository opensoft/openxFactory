"""Mechanical document catalog: deterministic entries, diffs, and
immutable per-repository run snapshots.

Realizes the US1 slice of the openxFactory `add-document-cataloging`
change (feature tasks T005-T009). Everything here is a pure function of
its inputs plus explicit filesystem state under the catalog root — no
wall-clock reads, no randomness, stable locator-keyed ordering, and
byte-identical rendering for identical inputs (research D3: JSON
documents written into ``.yaml`` files with sorted keys, fixed indent,
``\\n`` line endings, and a trailing newline).

Run layout (research D4; contract "Governed document catalog coverage"):

    health/document-catalog/runs/YYYY-MM-DD/<run-id>/
        run.yaml            run metadata (run_id, as_of, sequence)
        <repo...>.yaml      one immutable snapshot per repository;
                            slash-separated repo IDs become subdirs
    health/document-catalog/runs/.sequence/
        <NNNNNN>.yaml       atomically claimed run-sequence records

``<run-id>`` is a content address (``run_id``): a SHA-256 over every
per-repository snapshot document the run records, so one id names
exactly one content. An existing run directory for the same id is a
completed no-op, and any difference in recorded content — inventory,
taxonomy, a carried-forward or freshly merged classification, the date
stamped on a pending marker — is a new run, never a conflicting rewrite
of an immutable one. Runs recorded before opensoft/xFactory#519 used
the inventory-plus-taxonomy key (``legacy_run_id``) instead, which did
not cover classification: two producers of the same corpus state
recorded different snapshots under one id (``87544bd5…`` on 2026-09-24,
written by the nightly and again by a manual run; ``5ac351da…`` on
2026-08-16 and again, with pending markers added, on 2026-08-17).
``run_id_scheme`` tells the two schemes apart when a recorded run is
verified.

Concurrent-run protection (spec US1 acceptance 5): every recorded run
first claims a sequence number by creating a claim file with
``O_CREAT | O_EXCL`` — the kernel admits exactly one winner per number,
so recorded ``(as_of, sequence)`` pairs are unique and totally ordered
and "latest" is never a tie-break. A run dated earlier than any claimed
or recorded run is refused as stale before it creates anything, and a
run directory without ``run.yaml`` (crashed or in-flight) is not a
recorded run: it is invisible to ``load_snapshot`` and heals
idempotently on retry.

Every snapshot records its effective-taxonomy provenance (contract
"Controlled classification facets and provenance"): the SHA-256 digest
computed from the ordered canonical repository, path, registry content
hash, and registry-version inputs, each input also carrying the pinned
repository revision and the registry file's last-modifying revision —
provenance that never alters the digest.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from . import inventory

# All catalog output lands under this root-relative prefix — the same
# prefix `inventory.is_generated_catalog_path` excludes from corpus
# discovery so the catalog never catalogs itself.
CATALOG_DIR = Path("health") / "document-catalog"
RUNS_DIR = CATALOG_DIR / "runs"
SEQUENCE_DIR = RUNS_DIR / ".sequence"

# Run-metadata file name inside each run directory; reserved (a repo
# named "run" would collide with it and is refused).
RUN_META_NAME = "run.yaml"

SNAPSHOT_KIND = "xfactory_document_catalog"
RUN_META_KIND = "xfactory_document_catalog_run"
SEQUENCE_CLAIM_KIND = "xfactory_document_catalog_sequence_claim"
SCHEMA_VERSION = 1

# The mechanical catalog-entry fields (data-model.md "Inventory entry" /
# "Catalog entry" identity + freshness; classification facets join only
# through a later snapshot merge, never here). When handling policy
# prohibits persisting the path, `path` is replaced by the opaque
# locator fields (contract scenario "Path persistence is prohibited").
ENTRY_FIELDS = inventory.BASE_FIELDS + inventory.EXTENDED_FIELDS
OPAQUE_LOCATOR_FIELDS = ("document_ref", "path_sha256")

# Effective-taxonomy input shape (contract "Controlled classification
# facets and provenance"): the first four fields are the ordered digest
# inputs; the two revisions are provenance only and never alter the
# digest.
TAXONOMY_DIGEST_FIELDS = (
    "repository", "path", "content_sha256", "registry_version")
TAXONOMY_PROVENANCE_FIELDS = ("repository_revision", "registry_revision")
TAXONOMY_INPUT_FIELDS = TAXONOMY_DIGEST_FIELDS + TAXONOMY_PROVENANCE_FIELDS

_REGISTRY_VERSION_RE = re.compile(r"^registry_version:\s*(\S+)\s*$",
                                  re.MULTILINE)

# Domain separator for deterministic opaque document references; the
# authorized reference-resolution scheme is owned by the openxFactory
# opaque-locator contract (change tasks 2.x).
_DOCUMENT_REF_DOMAIN = "xfactory-document-ref"


class CatalogError(RuntimeError):
    """Immutability or run-ordering violation (stale overwrite,
    conflicting rewrite of an existing snapshot)."""


def render(document: dict) -> str:
    """Byte-stable rendering (research D3): JSON — a YAML subset — with
    sorted keys, fixed indent, and a trailing newline; the exact
    precedent proposal-support.py and the sync manifest use."""
    return json.dumps(document, indent=2, sort_keys=True) + "\n"


# --- document locators --------------------------------------------------------

def opaque_locator(repo: str, path: str) -> dict:
    """Policy-opaque locator for a document whose path must not be
    persisted (contract scenario "Path persistence is prohibited"):
    a deterministic opaque document reference — stable across runs so
    diffs and carry-forward key correctly — plus the path SHA-256 the
    contract requires. Neither field reveals the path."""
    return {
        "document_ref": hashlib.sha256(
            f"{_DOCUMENT_REF_DOMAIN}\n{repo}\n{path}\n".encode()).hexdigest(),
        "path_sha256": hashlib.sha256(str(path).encode()).hexdigest(),
    }


def _locator(entry: dict) -> tuple:
    """The entry's canonical document locator: ``("path", <path>)`` when
    the path is persisted, ``("opaque", <document_ref>)`` when policy
    prohibits persistence. An entry supplying both a persisted path and
    an opaque reference, or neither, is rejected (contract scenario
    "Locator is ambiguous")."""
    path = entry.get("path")
    ref = entry.get("document_ref")
    path_sha = entry.get("path_sha256")
    if path is not None:
        if ref is not None or path_sha is not None:
            raise ValueError(
                "ambiguous document locator (persisted path plus opaque "
                f"reference): {entry.get('repo')}:{path}")
        return ("path", path)
    if ref is None or path_sha is None:
        raise ValueError(
            "ambiguous document locator (neither persisted path nor "
            f"complete opaque reference) in repo {entry.get('repo')!r}")
    return ("opaque", ref)


def _entry_key(entry: dict) -> tuple:
    return (entry["repo"], _locator(entry)[1])


# --- mechanical entries -------------------------------------------------------

def mechanical_entries(inv: list[dict], path_prohibited=None) -> list[dict]:
    """Catalog entries — mechanical fields only — from a freshly built
    extended inventory (contracts/module-interfaces.md).

    Returns new dicts carrying exactly the mechanical identity and
    freshness fields, sorted by ``(repo, locator)``. Requires the
    extended inventory shape with resolved ``revision``/``snapshot_id``
    — a legacy or migration-loaded inventory (null extended fields)
    cannot seed the catalog and raises ValueError. Generated catalog
    records are excluded defensively (recursion exclusion), matching
    the corpus-discovery filter in ``inventory.build_inventory``.

    ``path_prohibited`` is the handling-gate policy hook (contract
    scenario "Path persistence is prohibited"): a callable over the
    inventory entry returning True when source policy forbids storing
    the repository-relative path. Those entries carry the opaque
    locator (``document_ref`` + ``path_sha256``) and omit ``path``.
    The default (None) persists every path; the runner supplies the
    promoted handling-gate policy once the openxFactory contract
    artifacts (change tasks 2.x) land.
    """
    entries = []
    for item in inv:
        if inventory.is_generated_catalog_path(item.get("path", "")):
            continue
        missing = [f for f in ENTRY_FIELDS if f not in item]
        if missing:
            raise ValueError(
                "inventory entry is not an extended catalog entry "
                f"(missing {', '.join(missing)}): "
                f"{item.get('repo')}:{item.get('path')}")
        for field in ("revision", "content_hash", "snapshot_id",
                      "artifact_type"):
            if item[field] is None:
                raise ValueError(
                    f"inventory entry has null {field} — the catalog "
                    "requires a freshly built extended inventory: "
                    f"{item['repo']}:{item['path']}")
        entry = {f: item[f] for f in ENTRY_FIELDS}
        if path_prohibited is not None and path_prohibited(item):
            del entry["path"]
            entry.update(opaque_locator(item["repo"], item["path"]))
        entries.append(entry)
    entries.sort(key=_entry_key)
    return entries


@dataclass(frozen=True)
class CatalogDiff:
    """Deterministic snapshot diff: entry sets keyed ``(repo, locator)``
    — the persisted path, or the opaque document reference when policy
    prohibits path persistence.

    A rename is a deletion plus an addition — no fabricated continuity
    (contract "Document is deleted or renamed"). ``modified`` is decided
    by ``content_hash`` alone: an unrelated repository commit (revision
    or snapshot-id change with identical content) is not a modification
    (design decision 8).
    """
    added: tuple
    modified: tuple
    deleted: tuple

    @property
    def empty(self) -> bool:
        return not (self.added or self.modified or self.deleted)

    @property
    def added_keys(self) -> tuple:
        return tuple(_entry_key(e) for e in self.added)

    @property
    def modified_keys(self) -> tuple:
        return tuple(_entry_key(e) for e in self.modified)

    @property
    def deleted_keys(self) -> tuple:
        return tuple(_entry_key(e) for e in self.deleted)


def _keyed(entries: list[dict], label: str) -> dict:
    keyed = {}
    for entry in entries:
        key = _entry_key(entry)
        if key in keyed:
            raise ValueError(
                f"duplicate catalog key in {label} entries: {key}")
        keyed[key] = entry
    return keyed


def diff(prev_entries: list[dict], curr_entries: list[dict]) -> CatalogDiff:
    """Added / modified / deleted between two catalog entry sets."""
    prev = _keyed(prev_entries, "previous")
    curr = _keyed(curr_entries, "current")
    added = [curr[k] for k in sorted(set(curr) - set(prev))]
    deleted = [prev[k] for k in sorted(set(prev) - set(curr))]
    modified = [curr[k] for k in sorted(set(curr) & set(prev))
                if curr[k]["content_hash"] != prev[k]["content_hash"]]
    return CatalogDiff(added=tuple(added), modified=tuple(modified),
                       deleted=tuple(deleted))


# --- effective taxonomy -------------------------------------------------------

def registry_input(repository, path, registry_file, repository_revision,
                   registry_revision) -> dict:
    """One pinned-registry taxonomy input (contract "Controlled
    classification facets and provenance").

    The canonical ``repository`` and repo-relative POSIX ``path`` plus
    the registry file's content SHA-256 and declared
    ``registry_version`` enter the digest; ``repository_revision`` (the
    current pinned repository revision) and ``registry_revision`` (the
    registry file's last-modifying revision) are recorded as provenance
    only and never alter the digest. A registry file that declares no
    ``registry_version`` is an incomplete taxonomy input and rejected.
    """
    data = Path(registry_file).read_bytes()
    match = _REGISTRY_VERSION_RE.search(data.decode("utf-8"))
    if not match:
        raise ValueError(
            f"taxonomy input is incomplete: registry file declares no "
            f"registry_version: {registry_file}")
    return {
        "repository": str(repository),
        "path": str(path),
        "content_sha256": hashlib.sha256(data).hexdigest(),
        "registry_version": match.group(1),
        "repository_revision": str(repository_revision),
        "registry_revision": str(registry_revision),
    }


def _canonical_taxonomy_inputs(inputs, provenance_required: bool) -> list[dict]:
    """Validate and canonically order taxonomy registry inputs by
    ``(repository, path)``; incomplete or duplicate inputs are rejected
    (contract scenario "Taxonomy inputs are incomplete")."""
    fields = TAXONOMY_INPUT_FIELDS if provenance_required \
        else TAXONOMY_DIGEST_FIELDS
    canonical = []
    for i, item in enumerate(inputs or []):
        if not isinstance(item, dict):
            raise ValueError(f"taxonomy input {i} is not a mapping")
        missing = [f for f in fields if not item.get(f)]
        if missing:
            raise ValueError(
                "taxonomy input is incomplete (missing "
                f"{', '.join(missing)}): input {i}")
        canonical.append({f: str(item[f]) for f in fields})
    if not canonical:
        raise ValueError(
            "taxonomy inputs are incomplete: at least one ordered "
            "pinned-registry input is required")
    canonical.sort(key=lambda c: (c["repository"], c["path"]))
    keys = [(c["repository"], c["path"]) for c in canonical]
    for a, b in zip(keys, keys[1:]):
        if a == b:
            raise ValueError(f"duplicate taxonomy registry input: {a}")
    return canonical


def taxonomy_digest(inputs) -> str:
    """Effective-taxonomy digest per the contract formula: SHA-256 over
    the ordered canonical repository, path, registry content hash, and
    registry-version inputs (design decision 5).

    Inputs are dicts carrying at least ``TAXONOMY_DIGEST_FIELDS`` (see
    ``registry_input``), ordered canonically by ``(repository, path)``
    so the digest is independent of caller order and of machine-local
    file locations. Repository revisions are provenance only — they
    never enter the digest, so an unrelated commit cannot invalidate
    classifications keyed to it, while moving registry content between
    repositories or paths, or bumping a registry version, always
    changes it.
    """
    digest = hashlib.sha256()
    for item in _canonical_taxonomy_inputs(inputs, provenance_required=False):
        for field in TAXONOMY_DIGEST_FIELDS:
            digest.update(item[field].encode())
            digest.update(b"\n")
        digest.update(b"\x00\n")
    return digest.hexdigest()


def effective_taxonomy(inputs) -> dict:
    """The effective-taxonomy block every snapshot records (contract
    "Controlled classification facets and provenance"): the digest plus
    the ordered pinned-registry inputs, each carrying the pinned
    repository revision and registry-file revision as provenance.
    Incomplete inputs — including missing provenance — are rejected."""
    canonical = _canonical_taxonomy_inputs(inputs, provenance_required=True)
    return {"digest": taxonomy_digest(canonical), "inputs": canonical}


def _validate_taxonomy(taxonomy) -> dict:
    """Normalize/validate the taxonomy block for snapshot embedding: a
    snapshot lacking the digest or an ordered pinned-registry input is
    rejected, as is a digest that does not match its inputs."""
    if not isinstance(taxonomy, dict):
        raise ValueError(
            "taxonomy inputs are incomplete: a snapshot requires the "
            "effective-taxonomy block (digest + ordered registry inputs)")
    declared = taxonomy.get("digest")
    if not declared:
        raise ValueError(
            "taxonomy inputs are incomplete: snapshot taxonomy carries "
            "no effective digest")
    block = effective_taxonomy(taxonomy.get("inputs"))
    if block["digest"] != declared:
        raise ValueError(
            "taxonomy digest does not match its ordered registry inputs")
    return block


# --- run identity -------------------------------------------------------------

# Domain separator, and the version of the content-address scheme: no other
# digest in the catalog hashes this prefix, so a run id can never equal an
# inventory snapshot id, a taxonomy digest, or a legacy key by construction.
_RUN_ID_DOMAIN = "xfactory-document-catalog-run/content-v1"

# The two run-id schemes a recorded run can satisfy (``run_id_scheme``).
CONTENT_ADDRESSED = "content-addressed"
LEGACY_INPUT_KEY = "legacy-input-key"


def _blank_run_id(document: dict) -> dict:
    """A shallow copy of one snapshot document with ``run.run_id`` emptied:
    the id is an address of the content, so it cannot be an input to
    itself. Nothing else is touched."""
    blanked = dict(document)
    run = document.get("run")
    blanked["run"] = dict(run, run_id="") if isinstance(run, dict) else run
    return blanked


def _address(bodies: dict) -> str:
    """SHA-256 over the scheme's domain separator and, per repository in
    sorted order, a framed ``[repository, byte length]`` header followed by
    that repository's blanked snapshot bytes. Framing keeps the
    concatenation unambiguous, so two different body sets can never hash
    alike short of a SHA-256 collision."""
    digest = hashlib.sha256(f"{_RUN_ID_DOMAIN}\n".encode("utf-8"))
    for repo in sorted(bodies):
        body = bodies[repo]
        digest.update(json.dumps([repo, len(body)]).encode("utf-8") + b"\n")
        digest.update(body)
    return digest.hexdigest()


def content_digest(documents: dict) -> str:
    """The content address of a run's snapshot documents (``{repository:
    snapshot document}``): ``_address`` over each document's byte-stable
    rendering (``render``) with its own ``run.run_id`` blanked — exactly
    the bytes ``write_snapshot`` persists, less the id. Pure: reads nothing
    but its argument."""
    return _address({
        repo: render(_blank_run_id(document)).encode("utf-8")
        for repo, document in documents.items()})


def _persisted_digest(name: str, texts: dict) -> str | None:
    """``content_digest`` recomputed from PERSISTED snapshot texts
    (``{repository: file text}``), byte for byte: nothing is parsed or
    re-rendered, only the one ``"run_id": "<name>"`` pair the canonical
    rendering carries (inside ``run``) is blanked in place. For a file the
    writer produced, the result equals ``content_digest`` of its parsed
    document; a serialization-only edit — indentation, key order, trailing
    whitespace — changes it just as a content edit does, where a parsed
    comparison would render the original bytes back. None when a text does
    not carry that pair exactly once (not the writer's rendering)."""
    pair = f'"run_id": {json.dumps(name)}'
    bodies = {}
    for repo, text in texts.items():
        if text.count(pair) != 1:
            return None
        bodies[repo] = text.replace(pair, '"run_id": ""', 1).encode("utf-8")
    return _address(bodies)


def run_id(entries_by_repo: dict, taxonomy) -> str:
    """The run id a run recording ``entries_by_repo`` (``{repository: that
    repository's catalog entries}``) under the effective ``taxonomy`` block
    writes: the content address (``content_digest``) of exactly the
    per-repository snapshot documents ``write_snapshot`` renders for them.

    Deterministic (research D4 — never wall clock) AND content-addressed
    (opensoft/xFactory#519): identical recorded content => identical id =>
    the same immutable run directory, and different recorded content =>
    a different id, whatever made it differ. That second half is what the
    inventory-plus-taxonomy key (``legacy_run_id``) lacked: a snapshot's
    content is shaped by more than the inventory and the taxonomy — by the
    classification carried forward from whichever run the writing tree
    last recorded, by the validated recommendations a cataloger child
    returned or did not return, and by the ``state_since`` date every new
    pending marker is stamped with — so one key could name two contents.
    Every input still participates because every input shows in the
    content: each entry's ``revision`` and ``snapshot_id`` (so an unrelated
    commit that moves a repository's HEAD is still a new run, as a
    snapshot's provenance must reflect the revision it was taken at —
    data-model.md, Catalog entry freshness) and the effective taxonomy
    block. ``diff()``'s per-document ``modified`` classification stays
    content-hash-only (design decision 8).

    Raises ValueError, before anything could land, for an empty run, an
    incomplete taxonomy, or anything ``write_snapshot`` would itself refuse
    for ANY repository of the run (a repository id that is not a safe path
    segment, a foreign entry, an ambiguous or duplicate locator, mixed
    revisions) — so ``write_run`` can never record some repositories of a
    run and then fail on a later one, leaving a partial run behind."""
    if not entries_by_repo:
        raise ValueError("a run records at least one repository snapshot")
    for repo in entries_by_repo:
        _repo_segments(repo)
    taxonomy_block = _validate_taxonomy(taxonomy)
    return content_digest({
        repo: _snapshot_document("", repo, list(entries), taxonomy_block)
        for repo, entries in entries_by_repo.items()})


def _legacy_key(inventory_snapshot_id: str, taxonomy_digest) -> str:
    if taxonomy_digest is None:
        return inventory_snapshot_id
    return hashlib.sha256(
        f"{inventory_snapshot_id}\n{taxonomy_digest}\n".encode()).hexdigest()


def legacy_run_id(inv: list[dict], taxonomy=None) -> str:
    """The id every run recorded before opensoft/xFactory#519 used: the
    inventory content hash, folded with the effective taxonomy digest when
    one is supplied. It is NOT a content address — it never covered the
    classification a run records — so it must never be used to mint the id
    of a new run (``run_id`` does that). It survives so a recorded run
    written under it can still be recognized as honestly derived
    (``run_id_scheme``), and because the recorded history keeps those
    names forever."""
    base = inventory.snapshot_id(inv)
    if taxonomy is None:
        return base
    digest = taxonomy.get("digest") if isinstance(taxonomy, dict) \
        else str(taxonomy)
    if not digest:
        raise ValueError("taxonomy carries no effective digest")
    return _legacy_key(base, digest)


def _is_legacy_named(name: str, documents: dict) -> bool:
    """Every document derives ``name`` as its legacy key from its own
    recorded ``run.inventory_snapshot_id`` and ``taxonomy.digest``."""
    for document in documents.values():
        inventory_id = document["run"].get("inventory_snapshot_id")
        taxonomy = document.get("taxonomy")
        digest = taxonomy.get("digest") if isinstance(taxonomy, dict) \
            else None
        if not isinstance(inventory_id, str) or not inventory_id:
            return False
        if name not in {_legacy_key(inventory_id, None),
                        _legacy_key(inventory_id, digest)}:
            return False
    return True


def run_id_scheme(name: str, documents: dict,
                  texts: dict | None = None) -> str | None:
    """The run-id scheme a RECORDED run satisfies, or None.

    ``documents`` maps each repository to the snapshot document the run
    holds for it (``load_snapshot(...)["repos"]``) and ``name`` is the run
    directory's name. Every document must record ``name`` as its own
    ``run.run_id``; then the run is ``CONTENT_ADDRESSED`` when ``name`` is
    the content address of exactly this run, or ``LEGACY_INPUT_KEY`` when
    ``name`` is the pre-#519 key each document's own recorded inventory
    snapshot id and taxonomy digest derive. A legacy run's content cannot
    be verified — that key never covered classification, which is the
    defect #519 records — so the legacy answer says only that the name is
    honestly derived. None means the directory holds content its name does
    not address: a snapshot edited after it was recorded, a repository
    snapshot lost, or files mixed from different runs.

    ``texts`` (``{repository: persisted file text}``, the same repositories
    as ``documents``) makes the content test byte-exact
    (``_persisted_digest``): a recorded run is verified against the bytes on
    disk, so even a serialization-only edit breaks its identity. Without
    ``texts`` the test runs over ``content_digest`` of the parsed documents,
    for callers holding a run in memory. The cheap legacy test runs first,
    so the recorded legacy history is never re-hashed."""
    if not documents:
        return None
    if texts is not None and set(texts) != set(documents):
        return None
    for document in documents.values():
        if not isinstance(document, dict) \
                or not isinstance(document.get("run"), dict) \
                or document["run"].get("run_id") != name:
            return None
    if _is_legacy_named(name, documents):
        return LEGACY_INPUT_KEY
    address = content_digest(documents) if texts is None \
        else _persisted_digest(name, texts)
    if address == name:
        return CONTENT_ADDRESSED
    return None


def _as_of_str(as_of) -> str:
    """Normalize as_of to a bare YYYY-MM-DD string, validating it parses.

    ``datetime`` is a subclass of ``date`` — a naive ``isinstance(as_of,
    date)`` check would accept a ``datetime`` and call its
    ``isoformat()``, which includes a time component (and a ``:`` that
    is not a safe path segment on every filesystem), producing a run
    directory name outside the documented ``YYYY-MM-DD`` contract. A
    ``datetime`` is rejected explicitly and must be narrowed to a
    ``date`` by the caller.
    """
    if isinstance(as_of, datetime):
        raise ValueError(
            f"as_of must be a date, not a datetime: {as_of!r}")
    if isinstance(as_of, date):
        return as_of.isoformat()
    return date.fromisoformat(str(as_of)).isoformat()


def _repo_segments(repo: str) -> list[str]:
    """Path segments for a repository ID (slash-separated repo IDs
    become subdirectories per the contract); refuses anything that
    could escape the run directory or collide with run metadata."""
    segments = str(repo).split("/")
    if repo in ("", "run") or any(
            not seg or seg in (".", "..") or "\\" in seg or seg.startswith(".")
            for seg in segments):
        raise ValueError(f"invalid repository id for snapshot path: {repo!r}")
    return segments


def _repo_file(run_dir: Path, repo: str) -> Path:
    segments = _repo_segments(repo)
    return run_dir.joinpath(*segments[:-1]) / (segments[-1] + ".yaml")


def _write_rendered(path: Path, text: str) -> None:
    """Crash-safe AND concurrency-safe write: the content lands complete
    in a UNIQUE per-invocation temp file (``mkstemp``, never a shared
    fixed ``.tmp`` name in the destination dir), then an atomic
    ``os.replace`` publishes it.

    Because every writer owns its own temp, two racing writers of the
    same target — even with DIFFERENT bytes, as when two runs of one
    ``run_id`` each claim a distinct sequence and write ``run.yaml`` —
    can never share, truncate, or unlink each other's temp: neither a
    torn/corrupt destination file nor a stray ``FileNotFoundError`` from
    a winner consuming a shared temp is possible (both of which the fixed
    ``.tmp`` predecessor admitted — the same hazard
    ``catalog_baseline._write_exclusive`` already guards against with a
    per-invocation temp). The last ``os.replace`` wins atomically;
    identical-content racers converge on identical bytes. Perms are
    ``mkstemp``'s default 0600 — git normalizes modes on commit, so
    there is no need to widen them here."""
    fd, tmp_name = tempfile.mkstemp(
        dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(tmp, path)  # atomic publish; consumes this temp only
    except BaseException:
        tmp.unlink(missing_ok=True)  # own temp, if os.replace never ran
        raise


def _load_yaml_json(path: Path) -> dict:
    """Parse one persisted catalog JSON artifact into its mapping.

    Persisted catalog artifacts are immutable machine-written records, but
    a bad merge, truncated/torn write, hand-edit, or foreign file can
    leave unparseable or wrong-shape bytes on disk. The deterministic
    family that reads these every run must REPORT that as a finding and
    never crash the whole doc-health run (the contract rule every checker
    relies on: malformed data is reported, never fatal), so a malformed or
    non-object artifact raises the controlled ``CatalogError`` its callers
    already handle — rather than a raw ``JSONDecodeError``/``AttributeError``
    surfacing deep inside a generator or index expression."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CatalogError(f"corrupt catalog artifact {path}: {exc}")
    if not isinstance(data, dict):
        raise CatalogError(
            f"corrupt catalog artifact {path}: expected a JSON object, got "
            f"{type(data).__name__}")
    return data


def _iter_runs(root: Path):
    """Yield (as_of, sequence, run_id, run_dir) for every RECORDED run
    under the catalog root, in deterministic order. A run directory
    without ``run.yaml`` is a crashed or in-flight run, not a record —
    it is skipped so it can never be selected as "latest" or block
    newer work; a retry of the same content heals it."""
    runs_root = Path(root) / RUNS_DIR
    if not runs_root.is_dir():
        return
    for date_dir in sorted(runs_root.iterdir()):
        if not date_dir.is_dir() or date_dir.name.startswith("."):
            continue
        for run_dir in sorted(date_dir.iterdir()):
            if not run_dir.is_dir() or run_dir.name.startswith("."):
                continue
            meta_path = run_dir / RUN_META_NAME
            if not meta_path.is_file():
                continue  # unrecorded: crashed or still in flight
            sequence = _load_yaml_json(meta_path).get("sequence", 0)
            yield date_dir.name, sequence, run_dir.name, run_dir


# --- sequence claims (concurrent-run protection) ------------------------------

def _read_claims(claims_dir: Path) -> list[tuple]:
    """(sequence, as_of) for every claimed sequence number. A claim
    whose content has not landed yet still occupies its number (the
    filename is the claim); its date is simply unknown."""
    claims = []
    if not claims_dir.is_dir():
        return claims
    for path in sorted(claims_dir.iterdir()):
        stem, _, suffix = path.name.partition(".")
        if not path.is_file() or suffix != "yaml" or not stem.isdigit():
            continue
        as_of = None
        try:
            as_of = _load_yaml_json(path).get("as_of")
        except (OSError, ValueError, CatalogError):
            pass  # claim created, content not yet flushed (or unreadable)
        claims.append((int(stem), as_of))
    return claims


def _claim_sequence(root: Path, day: str, rid: str) -> int:
    """Atomically claim the next run sequence number.

    Claim records under ``runs/.sequence/`` are created with
    ``O_CREAT | O_EXCL``: exactly one run can ever own a number, so two
    racing runs can never record the same sequence and run recency —
    the ``(as_of, sequence)`` pair — is total over recorded runs. The
    stale refusal lives inside the claim loop: a run dated earlier than
    any claimed or recorded run is refused, and losing a claim race
    forces a re-scan, so a newer-dated run that claims first is always
    visible before an older-dated run can claim (spec US1
    acceptance 5).
    """
    claims_dir = Path(root) / SEQUENCE_DIR
    claims_dir.mkdir(parents=True, exist_ok=True)
    while True:
        highest, newest = 0, None
        for seq, as_of in _read_claims(claims_dir):
            highest = max(highest, seq)
            if as_of is not None and (newest is None or as_of > newest):
                newest = as_of
        for as_of, seq, _rid, _dir in _iter_runs(root):
            highest = max(highest, seq)
            if newest is None or as_of > newest:
                newest = as_of
        if newest is not None and day < newest:
            raise CatalogError(
                f"stale snapshot refused: run dated {day} is older than "
                f"the latest recorded run ({newest})")
        sequence = highest + 1
        claim_path = claims_dir / f"{sequence:06d}.yaml"
        try:
            fd = os.open(claim_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            continue  # lost the race — re-scan and retry
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(render({
                "schema_version": SCHEMA_VERSION,
                "kind": SEQUENCE_CLAIM_KIND,
                "status": "record",
                "sequence": sequence,
                "as_of": day,
                "run_id": rid,
            }))
        return sequence


# --- snapshots ----------------------------------------------------------------

def _snapshot_document(rid: str, repo: str, entries: list[dict],
                       taxonomy: dict) -> dict:
    """The per-repository snapshot document. Deliberately excludes the
    run date so identical corpus state renders byte-identically across
    runs (spec US1 acceptance 2); the date lives in the run path and
    run metadata. Records the effective-taxonomy digest and its ordered
    pinned-registry provenance inputs (contract "Controlled
    classification facets and provenance")."""
    entries = sorted(entries, key=_entry_key)
    for entry in entries:
        if entry["repo"] != repo:
            raise ValueError(
                f"entry {_entry_key(entry)} does not belong to "
                f"repository {repo!r}")
    _keyed(entries, repo)  # unique locator keys, unambiguous locators
    revisions = sorted({e["revision"] for e in entries})
    snapshot_ids = sorted({e["snapshot_id"] for e in entries})
    if len(revisions) > 1 or len(snapshot_ids) > 1:
        raise ValueError(
            f"mixed revisions or snapshot ids in one repository "
            f"snapshot for {repo!r}")
    return {
        "schema_version": SCHEMA_VERSION,
        "kind": SNAPSHOT_KIND,
        "status": "record",
        "run": {
            "run_id": rid,
            "repository": repo,
            "repository_revision": revisions[0] if revisions else None,
            "inventory_snapshot_id":
                snapshot_ids[0] if snapshot_ids else None,
        },
        "taxonomy": taxonomy,
        "entries": entries,
    }


def write_snapshot(root, as_of, run_id, repo, entries, taxonomy) -> Path:
    """Write one repository's immutable snapshot into the dated,
    run-scoped catalog path; returns the snapshot file path.

    - Taxonomy provenance: every snapshot records the effective
      taxonomy digest plus its ordered pinned-registry inputs;
      ``taxonomy`` is the ``effective_taxonomy`` block and a snapshot
      lacking the digest or an ordered input is refused.
    - Sequence claim: a run without recorded metadata first claims a
      unique sequence number atomically (``_claim_sequence``); recorded
      ``(as_of, sequence)`` recency is therefore total and never
      tie-broken.
    - Stale refusal: a run dated earlier than any claimed or recorded
      run is refused inside the claim step, before anything lands
      (spec US1 acceptance 5). Completing the remaining repository
      files of an already-recorded run is never stale — its recency was
      fixed when its sequence was claimed.
    - Identical-content no-op: an existing snapshot file with the same
      rendered bytes returns its path unchanged (completed run).
    - Immutability: an existing snapshot file with different bytes is
      never rewritten — CatalogError. Run ids are content addresses
      (``run_id``; ``write_run`` mints them), so different content is
      always a different run and this refusal is reached only through a
      directory that was edited by hand, mixed from two runs, or named by
      a caller that did not mint its id from the content it writes.
    - Crash safety: ``run.yaml`` is written after the snapshot file, so
      a recorded run always holds at least one repository snapshot;
      directories without ``run.yaml`` are invisible to
      ``load_snapshot`` and heal idempotently on retry.
    """
    root = Path(root)
    day = _as_of_str(as_of)
    rid = str(run_id)
    if not rid or "/" in rid or rid in (".", "..") or rid.startswith("."):
        raise ValueError(f"invalid run id: {run_id!r}")
    taxonomy_block = _validate_taxonomy(taxonomy)
    document = _snapshot_document(rid, repo, list(entries), taxonomy_block)
    rendered = render(document)

    run_dir = root / RUNS_DIR / day / rid
    target = _repo_file(run_dir, repo)
    meta_path = run_dir / RUN_META_NAME

    if target.is_file():
        if target.read_text(encoding="utf-8") != rendered:
            raise CatalogError(
                f"immutable snapshot already exists with different "
                f"content: {target}")
        if meta_path.is_file():
            return target  # completed no-op: already recorded
        # fall through: heal a crash between snapshot and run.yaml

    sequence = None
    if not meta_path.is_file():
        # Includes the stale refusal; raises before anything is created.
        sequence = _claim_sequence(root, day, rid)
        run_dir.parent.mkdir(parents=True, exist_ok=True)
        try:
            run_dir.mkdir()
        except FileExistsError:
            pass  # raced an identical-content run — same rid, same bytes

    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_file():  # re-check: race lost mid-write
        if target.read_text(encoding="utf-8") != rendered:
            raise CatalogError(
                f"immutable snapshot already exists with different "
                f"content: {target}")
    else:
        _write_rendered(target, rendered)

    if sequence is not None and not meta_path.is_file():
        _write_rendered(meta_path, render({
            "schema_version": SCHEMA_VERSION,
            "kind": RUN_META_KIND,
            "status": "record",
            "run_id": rid,
            "as_of": day,
            "sequence": sequence,
        }))
    return target


def write_run(root, as_of, entries_by_repo: dict, taxonomy
              ) -> tuple[str, dict]:
    """Record one run: mint its content-addressed id from exactly the
    content being recorded (``run_id``) and write every repository's
    snapshot under it (``write_snapshot``, in sorted repository order, with
    all of its sequence-claim, stale-refusal, immutability, and crash-heal
    guarantees). Returns ``(run_id, {repository: snapshot path})``.

    This is the one call the dispatch layer records a run through, so no
    caller can pair a content with an id that does not address it — the
    pairing opensoft/xFactory#519 found two producers disagreeing over.
    Two independent trees recording the same content converge on the same
    id and byte-identical files; recording different content can never
    reuse an id, whichever tree or date it lands on."""
    rid = run_id(entries_by_repo, taxonomy)
    paths = {}
    for repo in sorted(entries_by_repo):
        paths[repo] = write_snapshot(root, as_of, rid, repo,
                                     entries_by_repo[repo], taxonomy)
    return rid, paths


def _snapshot_files(run_dir: Path):
    """(repository, path) for every per-repository snapshot file of one run
    directory, in sorted path order; slash-separated repository ids come
    back from their subdirectories."""
    for path in sorted(run_dir.rglob("*.yaml")):
        if path == run_dir / RUN_META_NAME:
            continue
        rel = path.relative_to(run_dir)
        yield "/".join(rel.parts)[:-len(".yaml")], path


def _load_run(run_dir: Path, day: str, sequence: int, rid: str) -> dict:
    repos = {repo: _load_yaml_json(path)
             for repo, path in _snapshot_files(run_dir)}
    return {"as_of": day, "run_id": rid, "sequence": sequence,
            "repos": repos}


def _load_run_texts(run_dir: Path) -> dict:
    """{repository: persisted snapshot text} for one run directory — the
    bytes ``run_id_scheme`` verifies a recorded run against. An unreadable
    file raises the same controlled ``CatalogError`` ``_load_yaml_json``
    does."""
    texts = {}
    for repo, path in _snapshot_files(run_dir):
        try:
            texts[repo] = path.read_text(encoding="utf-8")
        except (OSError, ValueError) as exc:
            raise CatalogError(f"corrupt catalog artifact {path}: {exc}")
    return texts


def load_snapshot(root, as_of=None, run_id=None) -> dict | None:
    """Load the latest — or a specific — recorded run.

    Returns ``{"as_of", "run_id", "sequence", "repos": {repo: doc}}``
    or None when nothing matches. ``as_of`` narrows to a date (latest
    run on that date by recorded sequence); ``run_id`` narrows to a
    specific run (latest date when the same content recurred — for a
    content-addressed id, byte-identical content; a pre-#519 legacy id
    promises only the same inventory and taxonomy). Only
    recorded runs (with ``run.yaml``) participate: sequence numbers are
    claimed atomically and unique, so "latest" is a total order, never
    a tie-break, and a crashed run directory is never returned.
    """
    day = _as_of_str(as_of) if as_of is not None else None
    rid = str(run_id) if run_id is not None else None
    candidates = [
        (d, seq, r, run_dir) for d, seq, r, run_dir in _iter_runs(root)
        if (day is None or d == day) and (rid is None or r == rid)]
    if not candidates:
        return None
    d, seq, r, run_dir = max(candidates, key=lambda c: (c[0], c[1]))
    return _load_run(run_dir, d, seq, r)


# --- recommendation merge (US4 task T019) -------------------------------------

# Facet states a recommendation merge must never clobber: they were
# reached only through owner disposition authority
# (``cataloger.apply_dispositions``, feature task T021 — not yet
# realized), and a stale or racing recommendation record folding in
# after the fact must not silently overwrite an owner's decision.
_OWNER_DISPOSED_STATES = ("reviewed", "overridden")


def _assignment_precedence(assignment: dict) -> tuple:
    """Total, deterministic precedence between RACING recommendation
    assignments competing for the same (entry, facet) within one merge:
    the newer ``state_since`` wins (a later dispatch saw the same
    content later); ties fall to the higher provenance ``confidence``;
    any remaining tie is broken by the canonical rendered form of the
    assignment itself. The order is total over distinct assignments —
    two candidates that compare fully equal are byte-identical, i.e.
    not in conflict at all — so the merge winner never depends on the
    order a caller supplies the records in."""
    provenance = assignment.get("provenance")
    if not isinstance(provenance, dict):
        provenance = {}
    confidence = provenance.get("confidence")
    if isinstance(confidence, bool) or not isinstance(confidence,
                                                      (int, float)):
        confidence = float("-inf")
    return (str(assignment.get("state_since") or ""), float(confidence),
            render(assignment))


def _apply_assignment(entry: dict, facet: str, assignment: dict) -> None:
    """Fold one winning facet assignment into `entry` in place; a facet
    currently in an owner-disposed state is left untouched (protected
    from a stale or racing merge — the invalidation that would
    legitimately return it to `pending` is ``cataloger.invalidate``,
    feature task T022, not this function)."""
    existing = {a["facet"]: a for a in entry.get("facet_assignments", [])
               if isinstance(a, dict) and a.get("facet")}
    current = existing.get(facet)
    if current is not None and \
            current.get("state") in _OWNER_DISPOSED_STATES:
        return  # owner-approved state is protected from this merge
    existing[facet] = copy.deepcopy(assignment)
    entry["facet_assignments"] = [existing[f] for f in sorted(existing)]


def merge_recommendations(snapshot, records, overrides=None) -> list[dict]:
    """Fold validated recommendation records into a NEW catalog entry
    set (data-model.md "Recommendation record"; contract "External
    catalog application and disposition authority").

    ``snapshot`` is one repository's CURRENT catalog entries (mechanical
    only, or already carrying ``facet_assignments`` from an earlier
    merge) — the base state this merge folds onto; it is never mutated.
    ``records`` are validated recommendation records
    (``cataloger.enforce_contract`` output, or the pending /
    policy-blocked markers from ``cataloger.pending_records``): each
    targets one document by ``repo`` plus its canonical locator — the
    persisted ``path``, or the opaque ``document_ref``/``path_sha256``
    pair when handling policy prohibits path persistence — and
    ``content_hash``. A record whose target has
    no matching entry, or whose ``content_hash`` no longer matches the
    live entry's, is discarded as STALE — data-model.md: "mismatch at
    merge = discard as stale" — never applied, never raised; a record
    with no unambiguous locator is likewise discarded, never guessed
    at. A facet
    the record would touch is skipped instead of overwritten when that
    facet is already in an owner-disposed state (``reviewed`` /
    ``overridden``), so a stale or racing recommendation can never
    clobber a human decision. A record that also carries an entry-level
    ``dispatch_policy`` (the handling-gate decision a protected
    document's ``pending_records`` marker records — the blocker lives
    there, never on a facet_assignment) has that decision copied onto its
    matched entry, so a blocked document's snapshot entry records why
    dispatch was refused.

    Racing records: when two or more supplied records target the same
    entry AND facet, the winner is resolved by the deterministic
    precedence rule (``_assignment_precedence``: newest ``state_since``,
    then highest provenance ``confidence``, then the canonical rendered
    assignment as the total tie-break) — never by the caller-supplied
    list order, so logically identical merges produce byte-identical
    snapshots regardless of arrival order.

    Returns a brand-new list of entries (deep-copied; neither
    ``snapshot`` nor ``records`` is mutated) sorted by
    ``(repo, locator)`` — the caller writes it into a NEW immutable
    snapshot via ``write_snapshot``; this function never touches disk
    and never rewrites an existing snapshot (data-model.md "Catalog
    snapshot": "merge writes a NEW snapshot, never edits one").

    ``overrides`` (owner reviewed/overridden dispositions) is accepted
    for interface stability (module-interfaces.md), but authority-
    checked disposition application is a later phase
    (``cataloger.apply_dispositions``, feature task T021); a non-empty
    ``overrides`` therefore raises ``NotImplementedError`` rather than
    silently dropping or misapplying a disposition.
    """
    if overrides:
        raise NotImplementedError(
            "owner disposition application is realized by "
            "cataloger.apply_dispositions (feature task T021); "
            "merge_recommendations does not yet apply overrides")
    _keyed(snapshot, "merge base")  # unique, unambiguous locator keys
    base = {_entry_key(e): copy.deepcopy(e) for e in snapshot}
    winners = {}  # (entry key, facet) -> winning assignment across records
    for record in records or []:
        try:
            key = _entry_key(record)
        except (KeyError, ValueError):
            continue  # no unambiguous locator — never guesses a target
        target = base.get(key)
        if target is None:
            continue  # no matching catalog entry — never invents one
        if target.get("content_hash") != record.get("content_hash"):
            continue  # stale by content_hash: discard, never raise
        dispatch_policy = record.get("dispatch_policy")
        if isinstance(dispatch_policy, dict):
            # A never-dispatched protected document's blocker lives on the
            # entry's dispatch_policy handling-gate decision (per-document
            # gate), never on a facet_assignment (schema-forbidden there);
            # carry it onto the merged entry so the snapshot records why
            # dispatch was blocked (cataloger.blocked_dispatch_policy).
            target["dispatch_policy"] = copy.deepcopy(dispatch_policy)
        for assignment in record.get("facet_assignments", []):
            facet = assignment.get("facet") if isinstance(assignment, dict) \
                else None
            if facet is None:
                continue
            slot = (key, facet)
            current = winners.get(slot)
            if current is None or _assignment_precedence(assignment) \
                    > _assignment_precedence(current):
                winners[slot] = assignment
    for (key, facet), assignment in winners.items():
        _apply_assignment(base[key], facet, assignment)
    return [base[k] for k in sorted(base)]
