#!/usr/bin/env python3
"""Verify `docs/opendox-carve-manifest.yaml` — FLOOR PART 1 of the RULED
four-part floor for the openDox/openXdox carve.

WHAT THIS FILE IS. `split-opendox-two-layer-product` § D6 (RULING OQ-1, `#656`
comment `5547060378`) replaced the openXwallet extraction's byte-identity floor,
which is unavailable here, with a four-part floor whose FIRST part is a mapping
manifest: one row per file under the moved paths, carrying its `openxFactory`
path, its `sha256` at the NAMED CARVE COMMIT, its destination repository and
path, and one of exactly three dispositions. The ruling's own sentence is the
whole requirement this file enforces — **"a file in no row, or an edit in no
class, is an UNDECLARED MOVEMENT and the carve REFUSES"** — and a manifest that
nothing checks is a claim, not a floor.

THE MANIFEST DOES NOT EXIST YET, AND THAT IS NOT A FAILURE. It is authored at
the carve commit as the LAST thing on that tree (the § 6 ceremony), so this
validator is landed BEFORE its subject. Given no manifest it prints
`NO MANIFEST <path> (nothing to validate)` and exits 0. That is a deliberate
seat-holding pass and the one place here that is not fail-closed: the alternative
is a red suite for every pull request between this file and the carve, which
would train the lane to ignore it. Everything after the manifest appears is
fail-closed.

SIX ORDERED CHECKS, FIRST FAILURE WINS (the scout memo § 1.3, 2026-09-08).

  1. SHAPE — `schema_version`/`kind`, the three consts, a 40-lowercase-hex
     `carve_commit`, a label `carve_tag`, the closed maps and lists, and the
     per-disposition required keys (`carve-shape-invalid`).
  2. REVISION — refuse unless the repository's `HEAD`, or `--at <sha>`, resolves
     to `carve_commit` (`carve-revision-mismatch`). This is what makes "a file
     changed on main between the manifest and the move" a REFUSAL on the next
     pull request rather than a surprise at the destination.
  3. DIGEST — recompute the sha256 of the RAW GIT BLOB at `carve_commit` for
     every moved row and compare the recorded `git_mode` from the tree
     (`carve-digest-mismatch`); a row for a path the commit does not carry is
     `carve-path-absent`.
  4. SURFACE COMPLETENESS — walk `git ls-tree -r <carve_commit>` under every
     `moved_paths:` prefix; every file there must appear in EXACTLY one row
     (`carve-file-undeclared` / `carve-file-duplicated`). This is
     `validate-openreposhape-pin.py`'s check 5 re-aimed, and it is the ruling's
     "a file in no row" sentence as running code — the one failure mode per-file
     digests cannot see, because they say nothing about a file nobody listed.
  5. CLOSED VOCABULARIES — `disposition`, `edits[].class`, `destination` and
     `reason` are each membership-tested against a closed list
     (`carve-vocabulary-unknown`).
  6. DISPOSITION CONSISTENCY — `moved_with_declared_edit` with no `edits:` is
     `moved_verbatim` mislabelled; `moved_verbatim` or `not_moved` with `edits:`
     is a contradiction (`carve-disposition-inconsistent`). Then the rows'
     file order must equal their bytewise-UTF-8 sort, which is what the const
     `path_order: bytewise_utf8` claims (`carve-path-order-violation`).

WHY THE VOCABULARIES ARE CLOSED IN CODE AND NOT IN A SCHEMA UNDER `contracts/`.
The three dispositions and the three edit classes are Brett Heap's ruling,
verbatim, and `edit_classes:` is asserted EQUAL to `EDIT_CLASSES` below rather
than merely read from the file — a manifest that declares its own fourth class
would otherwise validate against itself. The packet had proposed a fourth class
("vocabulary parameterization"); the ruling does not carry it, so it is not here.
`not_moved_reasons:` is the one vocabulary the ruling did NOT author (RULED OQ-C,
2026-09-09: the disposition list stays three and the REASON carries the nuance),
so the file declares its own list and this validator requires it to be a SUBSET
of `KNOWN_NOT_MOVED_REASONS` — declared-and-known, so neither a typo nor a
silently widened vocabulary passes.

WHY NO SCHEMA FILE SHIPS WITH THIS. A new artifact under `contracts/` fires
`release-tag-gate` and the digest inventory; this validator is one file with its
shape checks in code, which is also the precedent
`validate-openreposhape-pin.py` sets for a pin-like claim with exactly one
instance.

WHERE THE MANIFEST LIVES. `docs/opendox-carve-manifest.yaml`, the path § 3.1 and
§ D6 name verbatim, RULED OQ-E (2026-09-09) after the scout measured that `docs/`
holds no other machine-validated YAML in this repository. The break with the
convention is honoured, not corrected, and the manifest's own `header:` records
it.

Exit codes:
  0  the manifest verifies, or there is no manifest yet
  2  ANY refusal, and any environment failure

  There is deliberately NO exit 1, on `validate-openreposhape-pin.py`'s
  reasoning: the gate's only question is "may this carve proceed", and the answer
  is the same for "a digest drifted" and "the bytes could not be read". A
  two-valued failure invites a caller that treats one of them as a warning.

Run: `python3 scripts/validate-carve-manifest.py`; driven on every required-suite
pass by `tests/carve_manifest/test_carve_manifest.py`, which is the § 8.2 seat.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - the repository ships PyYAML
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]

# The ruled path, § 3.1 and design.md § D6 verbatim (RULED OQ-E). Relative, so
# `--repo` moves the whole question to another tree without moving the path.
MANIFEST_RELPATH = "docs/opendox-carve-manifest.yaml"

SCHEMA_VERSION = 1
KIND = "opendox-carve-manifest"

# The three consts of the row grammar, borrowed from the release-digest
# inventory (`contracts/releases/release-digest-inventory.schema.yaml:19-42`) so
# a reader of one document already knows how to read the other.
CONSTS: dict[str, str] = {
    "digest_algorithm": "sha256",
    "digest_source": "raw_git_blob",
    "path_order": "bytewise_utf8",
}

# RULED, three and not four. Order included: "the ruling's own, VERBATIM".
EDIT_CLASSES: tuple[str, ...] = ("import rewrites", "path constants",
                                 "adapter calls")

DISPOSITIONS: tuple[str, ...] = ("moved_verbatim", "moved_with_declared_edit",
                                 "not_moved")
MOVED_DISPOSITIONS: tuple[str, ...] = ("moved_verbatim",
                                       "moved_with_declared_edit")

# RULED OQ-C. The manifest declares its own subset of these; it may not declare
# a reason that is not here.
KNOWN_NOT_MOVED_REASONS: tuple[str, ...] = (
    "stays_openxfactory_adapter",
    "stays_openxfactory_governance",
    "deleted_at_carve",
    "superseded_by_split",
    "replicated_at_destination",
)

# The refusal vocabulary, FIXED and ordered by the check that raises it. Other
# code may branch on the CODE, so no failure path here may invent one.
#
# `carve-unreadable` is NOT in the vocabulary and its absence is the point, on
# `validate-openreposhape-pin.py`'s reasoning: the nine below each describe a
# MANIFEST that disagrees with the tree it claims, every one of them a finding a
# reviewer can act on. `carve-unreadable` describes an environment in which no
# finding can be reached at all. It still exits 2 — excluded from the
# vocabulary, not from fail-closure.
REFUSAL_CODES: tuple[str, ...] = (
    "carve-shape-invalid",
    "carve-revision-mismatch",
    "carve-digest-mismatch",
    "carve-path-absent",
    "carve-file-undeclared",
    "carve-file-duplicated",
    "carve-vocabulary-unknown",
    "carve-disposition-inconsistent",
    "carve-path-order-violation",
)

REMEDIATION = (
    "Remediation: re-cut the manifest AT the carve commit — recompute every "
    "sha256 from the real bytes (`git cat-file blob <carve_commit>:<path> | "
    "sha256sum`), never edit a digest to make this pass — or, where the tree "
    "has moved since, name a NEW carve_commit and recompute the whole file: "
    "the § 6 ceremony re-cuts, it never carries digests forward. Verify at a "
    "specific revision with `--at <sha>`."
)

COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
TAG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
REPO_RE = re.compile(r"^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")
MODE_RE = re.compile(r"^(100644|100755|120000)$")
EDIT_KEYS = {"class", "lines", "note"}
ROW_KEYS = {"source_path", "git_mode", "sha256", "disposition", "destination",
            "destination_path", "edits", "reason", "evidence"}


class CarveRefusal(Exception):
    """A named, remediable refusal.

    Carries the machine-readable `code` separately from the human `detail`, so a
    caller can branch on the code without parsing prose.

    `render(manifest)` is the ONE place the human message is assembled — code,
    detail and the fixed remediation trailer — and `main()` prints exactly that
    and nothing else, so the trailer cannot be dropped by a caller that forgot
    it exists. It is a method rather than `__str__` because the message names
    the manifest that failed, which the exception does not carry: every check
    below can be raised from a nested helper that has no idea which file it is
    reading, and threading the path through all of them to satisfy `__str__`
    would put the same string in several hands.
    """

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(code, detail)

    def render(self, manifest: Path) -> str:
        return f"FAIL {manifest}: {self.code} — {self.detail}\n{REMEDIATION}"


# --------------------------------------------------------------------------
# git
# --------------------------------------------------------------------------

def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    """git, capturing BYTES — blob contents must not go through a decoder."""
    try:
        return subprocess.run(["git", "-C", str(repo), *args],
                              capture_output=True, check=False)
    except OSError as exc:  # pragma: no cover - no git on the host
        raise CarveRefusal("carve-unreadable",
                           f"git could not be run in {repo}: {exc}") from exc


def resolve_revision(repo: Path, at: str | None) -> str:
    """The revision this run is asking about: `--at <sha>` or `HEAD`."""
    ref = at if at is not None else "HEAD"
    done = _git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    if done.returncode != 0 or not done.stdout.strip():
        if at is not None:
            raise CarveRefusal(
                "carve-revision-mismatch",
                f"--at {at!r} does not resolve to a commit in {repo}; the "
                "manifest's digests are taken at exactly one revision and an "
                "unresolvable one is not that revision")
        raise CarveRefusal(
            "carve-unreadable",
            f"{repo} has no resolvable HEAD; this validator reads the carve "
            "commit's tree out of a real git repository")
    return done.stdout.decode("utf-8", "replace").strip()


def tree_at(repo: Path, commit: str) -> dict[str, str]:
    """`{path: git_mode}` for every BLOB at `commit`.

    One `ls-tree` for the whole tree rather than a call per row: the modes are
    needed for check 3 and the path set for check 4, and both come out of the
    same listing. `-z` because a path is bytes and git quotes unusual ones
    otherwise; `--full-tree` because the answer must not depend on where this
    process was started.
    """
    done = _git(repo, "ls-tree", "-r", "-z", "--full-tree", commit)
    if done.returncode != 0:
        raise CarveRefusal(
            "carve-unreadable",
            f"`git ls-tree -r {commit[:12]}` failed in {repo}: "
            + done.stderr.decode("utf-8", "replace").strip())
    tree: dict[str, str] = {}
    for record in done.stdout.decode("utf-8", "surrogateescape").split("\0"):
        if not record:
            continue
        meta, _, path = record.partition("\t")
        fields = meta.split(" ")
        if len(fields) != 3:  # pragma: no cover - git's format is stable
            raise CarveRefusal("carve-unreadable",
                               f"unparseable ls-tree record {record!r}")
        mode, kind, _oid = fields
        if kind == "blob":
            tree[path] = mode
    return tree


def blob_at(repo: Path, commit: str, path: str) -> bytes | None:
    """The RAW bytes of `path` at `commit`, or None where it is not a blob."""
    done = _git(repo, "cat-file", "blob", f"{commit}:{path}")
    if done.returncode != 0:
        return None
    return done.stdout


# --------------------------------------------------------------------------
# reading
# --------------------------------------------------------------------------

def read_manifest(path: Path) -> dict[str, Any]:
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    # `ValueError` covers `UnicodeDecodeError`: a manifest that is not valid
    # UTF-8 is unreadable, and it must reach the reader as this named exit-2
    # refusal rather than as a traceback and exit 1.
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise CarveRefusal("carve-unreadable",
                           f"the manifest could not be parsed: {exc}") from exc
    if not isinstance(doc, dict):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"the manifest is not a mapping (parsed as {type(doc).__name__})")
    return doc


def _require_str(doc: dict, key: str, where: str) -> str:
    value = doc.get(key)
    if not isinstance(value, str) or not value.strip():
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} declares `{key}: {value!r}`; a non-empty string is "
            "required")
    return value


# --------------------------------------------------------------------------
# check 1 — shape
# --------------------------------------------------------------------------

def check_shape(doc: dict[str, Any]) -> None:
    """Everything answerable from the document alone, before any git call.

    THE `edits[]` ENTRY GRAMMAR IS ENFORCED HERE and the memo lists it under
    check 6. It is moved forward deliberately: it is a property of the document
    and of nothing else, and check 5 must read `edits[].class` before check 6
    runs — a vocabulary check that first had to defend itself against a
    malformed entry would be two checks wearing one name. Check 6 keeps what is
    actually its own: whether the entries AGREE with the disposition.
    """
    if doc.get("schema_version") != SCHEMA_VERSION:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`schema_version: {doc.get('schema_version')!r}`; this validator "
            f"reads version {SCHEMA_VERSION} only")
    if doc.get("kind") != KIND:
        raise CarveRefusal("carve-shape-invalid",
                           f"`kind: {doc.get('kind')!r}`, not {KIND!r}")
    for key, expected in CONSTS.items():
        if doc.get(key) != expected:
            raise CarveRefusal(
                "carve-shape-invalid",
                f"`{key}: {doc.get(key)!r}` is not the const {expected!r}; "
                "the row grammar is the release-digest inventory's and its "
                "consts are not a per-manifest choice")

    commit = doc.get("carve_commit")
    if not isinstance(commit, str) or not COMMIT_RE.match(commit):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`carve_commit: {commit!r}` is not 40 lowercase hex characters; "
            "the carve's referent is a commit, and an abbreviation, a branch "
            "name or a tag is a movable name rather than a referent")
    tag = _require_str(doc, "carve_tag", "the manifest")
    if not TAG_RE.match(tag):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`carve_tag: {tag!r}` is not a label; the tag is a HUMAN LABEL "
            "beside the commit and never the referent")
    source = _require_str(doc, "source_repository", "the manifest")
    if not REPO_RE.match(source):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`source_repository: {source!r}` is not `owner/name`")

    destinations = doc.get("destinations")
    if not isinstance(destinations, dict) or not destinations:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`destinations:` is not a non-empty mapping ({destinations!r}); "
            "a row's `destination` is a KEY here, because one typo otherwise "
            "ships a file to a repository nobody declared")
    for key, entry in destinations.items():
        if not isinstance(entry, dict):
            raise CarveRefusal(
                "carve-shape-invalid",
                f"`destinations.{key}` is not a mapping ({entry!r})")
        _require_str(entry, "repository", f"`destinations.{key}`")
        _require_str(entry, "leg", f"`destinations.{key}`")

    classes = doc.get("edit_classes")
    if not isinstance(classes, list) or tuple(classes) != EDIT_CLASSES:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`edit_classes: {classes!r}` is not the RULED list "
            f"{list(EDIT_CLASSES)!r}, verbatim and in order. The list is "
            "closed: an edit is expressible as one of these three or it is not "
            "a carve edit at all")

    reasons = doc.get("not_moved_reasons")
    if not isinstance(reasons, list) or not reasons:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`not_moved_reasons:` is not a non-empty list ({reasons!r})")
    unknown = [r for r in reasons if r not in KNOWN_NOT_MOVED_REASONS]
    if unknown:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`not_moved_reasons:` declares {unknown!r}, which this validator "
            f"does not know; the known set is {list(KNOWN_NOT_MOVED_REASONS)!r} "
            "(RULED OQ-C). The reason vocabulary carries the nuance the three "
            "dispositions cannot, so it is declared AND known — a file may not "
            "widen it by declaring it")

    moved_paths = doc.get("moved_paths")
    if not isinstance(moved_paths, list) or not moved_paths:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`moved_paths:` is not a non-empty list ({moved_paths!r}); it is "
            "the SURFACE the completeness check walks, and an empty surface "
            "declares nothing")
    for entry in moved_paths:
        if not isinstance(entry, str) or not entry.strip():
            raise CarveRefusal(
                "carve-shape-invalid",
                f"`moved_paths:` holds a non-path entry ({entry!r})")

    rows = doc.get("rows")
    if not isinstance(rows, list) or not rows:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`rows:` is not a non-empty list ({rows!r})")
    for index, row in enumerate(rows):
        _check_row_shape(index, row, moved_paths)


def _check_row_shape(index: int, row: Any, moved_paths: list[str]) -> None:
    where = f"rows[{index}]"
    if not isinstance(row, dict):
        raise CarveRefusal("carve-shape-invalid",
                           f"{where} is not a mapping ({row!r})")
    stray = sorted(set(row) - ROW_KEYS)
    if stray:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} carries the unknown key(s) {stray!r}; the row grammar is "
            "closed, so a field nobody validates is a field nobody reads")
    source_path = _require_str(row, "source_path", where)
    if not in_surface(source_path, moved_paths):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} declares `source_path: {source_path!r}`, which lies "
            "under no `moved_paths:` prefix; the manifest declares what LEAVES "
            "the surface, and a row outside it makes the completeness check "
            "answer a different question from the one it asks")

    disposition = row.get("disposition")
    if not isinstance(disposition, str) or not disposition:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} ({source_path}) declares `disposition: {disposition!r}`; "
            "a string is required")
    # A disposition OUTSIDE the three is left to check 5, which owns the closed
    # vocabularies: refusing it here would report a vocabulary miss under a
    # shape code and hide which check is doing the work.
    if disposition in MOVED_DISPOSITIONS:
        mode = row.get("git_mode")
        if not isinstance(mode, str) or not MODE_RE.match(mode):
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{where} ({source_path}) declares `git_mode: {mode!r}`; a "
                "quoted git file mode is required (a mode flip is what a blob "
                "digest does not see, and an unquoted 100644 parses as an int)")
        digest = row.get("sha256")
        if not isinstance(digest, str) or not SHA256_RE.match(digest):
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{where} ({source_path}) declares `sha256: {digest!r}`, which "
                "is not 64 lowercase hex characters")
        _require_str(row, "destination", f"{where} ({source_path})")
        _require_str(row, "destination_path", f"{where} ({source_path})")
        for key in ("reason", "evidence"):
            if key in row:
                raise CarveRefusal(
                    "carve-shape-invalid",
                    f"{where} ({source_path}) is `{disposition}` and carries "
                    f"`{key}:`; a reason answers why a file did NOT move")
    elif disposition == "not_moved":
        _require_str(row, "reason", f"{where} ({source_path})")
        _require_str(row, "evidence", f"{where} ({source_path})")
        for key in ("sha256", "git_mode"):
            if key in row:
                raise CarveRefusal(
                    "carve-shape-invalid",
                    f"{where} ({source_path}) is `not_moved` and carries "
                    f"`{key}:`; a digest at the carve commit is the claim that "
                    "these bytes arrive somewhere, and nothing arrives")

    edits = row.get("edits")
    if edits is not None:
        _check_edits_shape(where, source_path, edits)


def _check_edits_shape(where: str, source_path: str, edits: Any) -> None:
    if not isinstance(edits, list):
        raise CarveRefusal("carve-shape-invalid",
                           f"{where} ({source_path}) declares `edits:` as "
                           f"{edits!r}; a list is required")
    for position, edit in enumerate(edits):
        at = f"{where}.edits[{position}] ({source_path})"
        if not isinstance(edit, dict):
            raise CarveRefusal("carve-shape-invalid",
                               f"{at} is not a mapping ({edit!r})")
        stray = sorted(set(edit) - EDIT_KEYS)
        if stray:
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{at} carries the unknown key(s) {stray!r}; an edit is "
                "`{class, lines, note?}` and nothing else")
        if not isinstance(edit.get("class"), str) or not edit["class"]:
            raise CarveRefusal("carve-shape-invalid",
                               f"{at} declares `class: {edit.get('class')!r}`")
        lines = edit.get("lines")
        if not isinstance(lines, list) or not lines:
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{at} declares `lines: {lines!r}`; at least one line number "
                "at the carve commit is required. Without them "
                "`moved_with_declared_edit` is only a label — the line numbers "
                "are what make the claim falsifiable at the destination")
        for line in lines:
            if not isinstance(line, int) or isinstance(line, bool) or line < 1:
                raise CarveRefusal(
                    "carve-shape-invalid",
                    f"{at} declares the line {line!r}; line numbers are "
                    "positive integers")
        if "note" in edit and (not isinstance(edit["note"], str)
                               or not edit["note"].strip()):
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{at} declares `note: {edit['note']!r}`; a note is prose or "
                "it is absent")


def in_surface(path: str, moved_paths: list[str]) -> bool:
    """Is `path` under one of the declared prefixes (or named exactly)?

    Segment-aware: `scripts/ideation_dashboard` does not swallow
    `scripts/ideation_dashboard_old/x.py`, which a bare `startswith` would.
    """
    for entry in moved_paths:
        prefix = entry.rstrip("/")
        if path == prefix or path.startswith(prefix + "/"):
            return True
    return False


# --------------------------------------------------------------------------
# checks 2-6
# --------------------------------------------------------------------------

def check_revision(repo: Path, doc: dict, at: str | None) -> str:
    resolved = resolve_revision(repo, at)
    carve_commit = doc["carve_commit"]
    if resolved != carve_commit:
        asked = f"--at {at}" if at is not None else "HEAD"
        raise CarveRefusal(
            "carve-revision-mismatch",
            f"{asked} in {repo} is {resolved}, but the manifest's digests are "
            f"taken at carve_commit {carve_commit}. The manifest is authored "
            "as the LAST thing on the carve tree, so a tree that has moved "
            "since is exactly the condition this refuses: re-cut at a new "
            "carve commit, or verify the old one with "
            f"`--at {carve_commit[:12]}`")
    return carve_commit


def check_digests(repo: Path, doc: dict, tree: dict[str, str]) -> int:
    commit = doc["carve_commit"]
    recomputed = 0
    for index, row in enumerate(doc["rows"]):
        if row.get("disposition") not in MOVED_DISPOSITIONS:
            continue
        path = row["source_path"]
        if path not in tree:
            raise CarveRefusal(
                "carve-path-absent",
                f"rows[{index}] records a sha256 for {path}, which "
                f"{doc['source_repository']}@{commit[:12]} does not carry as a "
                "file; a digest of nothing is not a digest")
        if tree[path] != row["git_mode"]:
            raise CarveRefusal(
                "carve-digest-mismatch",
                f"{path}: MODE DRIFT — the manifest records git_mode "
                f"{row['git_mode']} and the tree at {commit[:12]} carries "
                f"{tree[path]}. A mode flip is the one change a blob digest "
                "cannot see, which is why the mode is carried")
        content = blob_at(repo, commit, path)
        if content is None:  # pragma: no cover - ls-tree already said blob
            raise CarveRefusal(
                "carve-path-absent",
                f"{path} could not be read as a blob at {commit[:12]}")
        actual = hashlib.sha256(content).hexdigest()
        recomputed += 1
        if actual != row["sha256"]:
            raise CarveRefusal(
                "carve-digest-mismatch",
                f"{path}: DIGEST DRIFT\n"
                f"  recorded   {row['sha256']}\n"
                f"  recomputed {actual}\n"
                f"the bytes at {commit[:12]} are not the bytes this row "
                "promises the destination")
    return recomputed


def check_surface(doc: dict, tree: dict[str, str]) -> int:
    """Every file under the declared prefixes appears in EXACTLY one row."""
    commit = doc["carve_commit"]
    surface = {p for p in tree if in_surface(p, doc["moved_paths"])}

    seen: dict[str, int] = {}
    for index, row in enumerate(doc["rows"]):
        path = row["source_path"]
        if path in seen:
            raise CarveRefusal(
                "carve-file-duplicated",
                f"{path} appears in rows[{seen[path]}] AND rows[{index}]; a "
                "file has exactly one disposition and exactly one destination, "
                "and a file with two rows has neither")
        seen[path] = index

    undeclared = sorted(surface - set(seen))
    if undeclared:
        raise CarveRefusal(
            "carve-file-undeclared",
            f"the carve surface at {commit[:12]} carries {len(undeclared)} "
            "file(s) that NO row declares: "
            + ", ".join(undeclared[:10])
            + (" …" if len(undeclared) > 10 else "")
            + " — a file in no row is an UNDECLARED MOVEMENT and the carve "
              "refuses (RULING OQ-1)")
    absent = sorted(set(seen) - surface)
    if absent:
        raise CarveRefusal(
            "carve-path-absent",
            f"the manifest declares {len(absent)} row(s) for path(s) the "
            f"carve surface at {commit[:12]} does not carry: "
            + ", ".join(absent[:10]) + (" …" if len(absent) > 10 else ""))
    return len(surface)


def check_vocabularies(doc: dict) -> None:
    destinations = doc["destinations"]
    declared_classes = doc["edit_classes"]
    declared_reasons = doc["not_moved_reasons"]
    for index, row in enumerate(doc["rows"]):
        where = f"rows[{index}] ({row['source_path']})"
        disposition = row["disposition"]
        if disposition not in DISPOSITIONS:
            raise CarveRefusal(
                "carve-vocabulary-unknown",
                f"{where} declares `disposition: {disposition!r}`; the list is "
                f"CLOSED at {list(DISPOSITIONS)!r} (RULED OQ-C — three, and "
                "the `not_moved` reason carries any nuance the three cannot)")
        destination = row.get("destination")
        if destination is not None and destination not in destinations:
            raise CarveRefusal(
                "carve-vocabulary-unknown",
                f"{where} declares `destination: {destination!r}`, which is "
                f"not a key of `destinations:` ({sorted(destinations)!r})")
        for position, edit in enumerate(row.get("edits") or []):
            if edit["class"] not in declared_classes:
                raise CarveRefusal(
                    "carve-vocabulary-unknown",
                    f"{where}.edits[{position}] declares "
                    f"`class: {edit['class']!r}`, which is not one of "
                    f"{list(EDIT_CLASSES)!r}. An edit in no class is an "
                    "UNDECLARED MOVEMENT and the carve refuses (RULING OQ-1)")
        reason = row.get("reason")
        if reason is not None and reason not in declared_reasons:
            raise CarveRefusal(
                "carve-vocabulary-unknown",
                f"{where} declares `reason: {reason!r}`, which the manifest's "
                f"own `not_moved_reasons:` ({list(declared_reasons)!r}) does "
                "not carry")


def check_disposition_consistency(doc: dict) -> None:
    for index, row in enumerate(doc["rows"]):
        where = f"rows[{index}] ({row['source_path']})"
        disposition = row["disposition"]
        edits = row.get("edits") or []
        if disposition == "moved_with_declared_edit" and not edits:
            raise CarveRefusal(
                "carve-disposition-inconsistent",
                f"{where} is `moved_with_declared_edit` with no `edits:`; that "
                "is `moved_verbatim` mislabelled, and a manifest whose "
                "dispositions do not distinguish is the label without the "
                "floor")
        if disposition == "moved_verbatim" and edits:
            raise CarveRefusal(
                "carve-disposition-inconsistent",
                f"{where} is `moved_verbatim` and declares {len(edits)} "
                "edit(s); verbatim means the destination's bytes equal this "
                "digest, which a declared edit contradicts")
        if disposition == "not_moved" and edits:
            raise CarveRefusal(
                "carve-disposition-inconsistent",
                f"{where} is `not_moved` and declares {len(edits)} edit(s); a "
                "file that does not move takes no carve edit")

    # `path_order: bytewise_utf8` is a claim about THIS document, and a const
    # nothing enforces is a comment. Bytewise on the UTF-8 encoding, not on
    # Python's code points, because that is what the const names and what git
    # and `sort` agree on.
    paths = [row["source_path"] for row in doc["rows"]]
    # `surrogateescape` on the ENCODE, not only on the decode that produced
    # these strings: a path is bytes, and a repository carrying a non-UTF-8 one
    # would otherwise raise `UnicodeEncodeError` out of this comparison and end
    # the process with a traceback and exit 1 — the exit code this file's
    # docstring says does not exist. The refusal must stay a refusal even for
    # the paths git can name and Unicode cannot.
    ordered = sorted(paths, key=lambda p: p.encode("utf-8", "surrogateescape"))
    if paths != ordered:
        first = next(i for i, (a, b) in enumerate(zip(paths, ordered)) if a != b)
        raise CarveRefusal(
            "carve-path-order-violation",
            f"the rows are not in `path_order: bytewise_utf8`; rows[{first}] "
            f"is {paths[first]!r} where the bytewise order puts "
            f"{ordered[first]!r}. A ~430-row manifest is reviewed by diff, and "
            "a diff of an unsorted file hides a moved row inside a reordering")


# --------------------------------------------------------------------------
# the run
# --------------------------------------------------------------------------

def validate(manifest_path: Path, repo: Path,
             at: str | None) -> dict[str, Any]:
    """The six checks in order, first failure wins."""
    doc = read_manifest(manifest_path)
    check_shape(doc)
    commit = check_revision(repo, doc, at)
    tree = tree_at(repo, commit)
    recomputed = check_digests(repo, doc, tree)
    surface = check_surface(doc, tree)
    check_vocabularies(doc)
    check_disposition_consistency(doc)

    counts = {d: 0 for d in DISPOSITIONS}
    for row in doc["rows"]:
        counts[row["disposition"]] += 1
    return {
        "result": "ok",
        "manifest": str(manifest_path),
        "carve_commit": commit,
        "carve_tag": doc["carve_tag"],
        "source_repository": doc["source_repository"],
        "rows": len(doc["rows"]),
        "dispositions": counts,
        "digests_recomputed": recomputed,
        "surface": surface,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate-carve-manifest.py",
        description=("Verify docs/opendox-carve-manifest.yaml — FLOOR PART 1 "
                     "of the RULED four-part floor (split-opendox § D6)."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--manifest", metavar="PATH", default=None,
        help=f"the manifest to verify (default: <repo>/{MANIFEST_RELPATH})")
    parser.add_argument(
        "--repo", metavar="DIR", default=None,
        help="the git repository the digests are taken in (default: this one)")
    parser.add_argument(
        "--at", metavar="SHA", default=None,
        help=("verify against this revision instead of HEAD; it must still "
              "resolve to the manifest's carve_commit"))
    parser.add_argument(
        "--json", action="store_true",
        help="print one JSON object on stdout instead of the human line")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve() if args.repo else ROOT
    manifest_path = (Path(args.manifest).resolve() if args.manifest
                     else repo / MANIFEST_RELPATH)

    # THE SEAT-HOLDING PASS, and the one place here that is not fail-closed.
    # See the module docstring: this validator lands BEFORE its subject.
    if not manifest_path.is_file():
        if args.json:
            print(json.dumps({"result": "no-manifest",
                              "manifest": str(manifest_path)}))
        else:
            print(f"NO MANIFEST {manifest_path} (nothing to validate)")
        return 0

    try:
        summary = validate(manifest_path, repo, args.at)
    except CarveRefusal as exc:
        if args.json:
            print(json.dumps({"result": "refused", "code": exc.code,
                              "detail": exc.detail,
                              "manifest": str(manifest_path)}))
        else:
            print(exc.render(manifest_path), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(summary))
    else:
        counts = summary["dispositions"]
        print(f"OK {manifest_path}: {summary['rows']} row(s) at "
              f"{summary['source_repository']}@{summary['carve_commit'][:12]} "
              f"({summary['carve_tag']}) — "
              f"{counts['moved_verbatim']} moved_verbatim, "
              f"{counts['moved_with_declared_edit']} moved_with_declared_edit, "
              f"{counts['not_moved']} not_moved; "
              f"{summary['digests_recomputed']} digest(s) recomputed; "
              f"{summary['surface']} file(s) in the declared surface with none "
              "undeclared")
    return 0


if __name__ == "__main__":
    sys.exit(main())
