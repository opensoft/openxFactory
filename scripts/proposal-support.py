#!/usr/bin/env python3
"""Move staged proposal support and preserve it through OpenSpec archive."""

from __future__ import annotations

import argparse
import difflib
import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

# THE DECLARED SENTINEL VOCABULARY, CONSULTED RATHER THAN RESPELLED
# (`declare-sentinel-pin-vocabulary` § 2.7). The three revision guards below
# compared against the literal `"uncommitted"` and therefore recognized ONE
# spelling of ONE condition; every other declared member reached them as though
# it were a commit name, and `git_blob_sha256` raised `SupportError` on four of
# the five. That is a real crash on a real archived manifest, not a
# hypothetical.
#
# IMPORTED RATHER THAN COPIED, unlike `manifest_rel` further down. That
# duplication is deliberate and stated — the shared rule lives in a package this
# script cannot assume — but `doc_health.pin_sentinels` is a sibling of this
# file under `scripts/` and depends on nothing outside the standard library. The
# path insertion covers the case this script is loaded by
# `spec_from_file_location` (which the tests do) rather than invoked, where
# Python inserts nothing. `scripts/bootstrap-ideation-cross-reference.py`
# already converts on the same reasoning.
_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
from doc_health.pin_sentinels import is_declared_sentinel  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None
import tarfile
from datetime import datetime, timezone


LINK_RE = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")


def utc_today() -> str:
    """TODAY IN UTC — the ONE clock every date this script stamps reads.

    `date.today()` reads the MACHINE'S LOCAL clock, and this script's dates end
    up in two places that are then compared to each other: the support bundle's
    `packaged_at`, and — through the pinned OpenSpec CLI, which reads its own
    local clock and has no date option — the name of
    `openspec/changes/archive/<YYYY-MM-DD>-<change>/`. Archiving
    `publish-openspec-cli-pin-as-contract-member` at 23:35 local / 03:35 UTC
    produced a `2026-09-07-` directory for a UTC 2026-09-08 archive (issue
    #790, PR #780's packet). Every other date in this estate — the lane rows,
    the records, the ratification lines — is UTC, so this is the clock that
    makes the archive agree with them rather than with whoever ran it.

    `datetime.now(timezone.utc).date()` rather than the deprecated
    `datetime.utcnow()`: the latter returns a NAIVE datetime that reads as
    local time to anything that later attaches a timezone.
    """
    return datetime.now(timezone.utc).date().isoformat()


class SupportError(ValueError):
    pass


# --------------------------------------------------------------------------
# LINE + FENCE PRIMITIVES — the corpus's one agreed pair, spelled here too
#
# `ideation_dashboard.round_trip`, `doc_health.families` and
# `web/views/outline-model.js` already carry the same naive ``` toggle over the
# same documents, and a companion test pins all three against a shared fixture
# set. This mover is the FOURTH, and it is added to that test rather than left
# to drift: sharing the code is not available (one of them is browser
# JavaScript, and this file is a standalone script a human runs against a
# checkout that may not have the dashboard package importable).
#
# Do not "improve" this predicate without the other three. `~~~` is a real
# CommonMark fence and NONE of the four treats it as one — deliberately.
# --------------------------------------------------------------------------

_EOL_RE = re.compile(r"\r\n|\r|\n")


def _split_keepends(text: str) -> list[tuple[str, str]]:
    """`text` as [(body, ending)] pairs, where ''.join(b + e) IS `text`.

    NOT `str.splitlines()`, which also breaks on \\x0b, \\x0c, \\x1c-\\x1e,
    \\x85, U+2028 and U+2029 — a governance document containing one of those
    would be silently re-split and rejoined into different bytes. Only the three
    real line endings separate lines here.
    """
    rows: list[tuple[str, str]] = []
    at, size = 0, len(text)
    while at < size:
        match = _EOL_RE.search(text, at)
        if match is None:
            rows.append((text[at:], ""))
            break
        rows.append((text[at:match.start()], match.group(0)))
        at = match.end()
    return rows


def _join_rows(rows: list[tuple[str, str]]) -> str:
    return "".join(body + ending for body, ending in rows)


def _document_eol(rows: list[tuple[str, str]]) -> str:
    """The flavor a NEW line takes: the document's FIRST real ending."""
    for _body, ending in rows:
        if ending:
            return ending
    return "\n"


def _is_fence(line: str) -> bool:
    return line.lstrip().startswith("```")


def _fenced_flags(rows: list[tuple[str, str]]) -> list[bool]:
    """Per-row "is inside a fence", with the fence lines themselves marked True —
    a fence delimiter is never content to be rewritten."""
    flags: list[bool] = []
    fenced = False
    for body, _ending in rows:
        if _is_fence(body):
            fenced = not fenced
            flags.append(True)
            continue
        flags.append(fenced)
    return flags


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def manifest_text(data: dict) -> str:
    # JSON is valid YAML 1.2 and keeps the command dependency-free.
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def load_manifest(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SupportError(f"invalid manifest {path}: {exc}") from exc
    if not isinstance(data, dict) or data.get("format_version") != 1:
        raise SupportError(f"invalid manifest format: {path}")
    return data


def manifest_rel(value: object) -> object:
    """A recorded manifest path, in the spelling this module's readers resolve.

    Every path field in a support manifest — `files[].path`,
    `files[].source_path`, `files[].source_snapshot_path`, `remaining_paths[]`
    — is a KEY, not prose. Two of them are joined to the support folder to
    find a file whose sha256 was recorded beside them, and `source_path` is
    handed to `git show` as `<revision>:<path>`. `transition` now records all
    of them in POSIX form (see the derivation there), but fixing a writer
    cannot reach records already on disk, and a manifest written by
    `str(PurePath)` on a Windows checkout spells every one of them with
    backslashes. On that machine they resolve; verified anywhere else they
    resolve to NOTHING — each becomes a single filename that happens to
    contain backslashes, `git show <rev>:ideation\\staging\\t\\one.md` finds no
    blob, and the recorded hashes could never be reconciled against the files
    they describe. So the reader normalizes rather than assuming its own
    spelling, exactly as `origin_errors` and
    `generator._declared_origin_staging` already do for the origin path
    (PR #221).

    THE TRADEOFF, and it is WIDER here than it was for the origin path: a
    POSIX filename may legally contain a backslash, and the staged-origin id
    grammar that ruled the case out there governs an ID, not the names of the
    files inside a topic — `select_files` takes whatever is in the folder. A
    file so named would have its entry read as a nested lookup that misses, so
    the trade is paid in a LOUD failure (`missing support file` / `missing
    source snapshot`) rather than a silent pass, and an absurd case is traded
    for a real one. Non-strings pass through untouched so a malformed manifest
    still fails exactly the way it did before.
    """
    return value.replace("\\", "/") if isinstance(value, str) else value


def ensure_inside(path: Path, parent: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(parent.resolve())
    except ValueError as exc:
        raise SupportError(f"{label} escapes {parent}") from exc
    return resolved


def reject_symlinks(path: Path) -> None:
    current = path
    while True:
        if current.is_symlink():
            raise SupportError(f"symlink not allowed: {current}")
        if current == current.parent:
            break
        current = current.parent


def repo_revision(root: Path) -> str:
    """The commit this transition is recorded at, or the declared sentinel for
    an unreadable repository.

    UNCHANGED BY `declare-sentinel-pin-vocabulary`, deliberately. `"uncommitted"`
    is returned on a NON-ZERO EXIT from `rev-parse HEAD` and on nothing else, so
    the value this writes means exactly the condition Q1 ruled it names: the
    repository's revision could not be read at all. It is NOT a dirty-tree
    stamp, and the dirty-tree branch is not added here, because this mover does
    not have the defect that branch repairs — it never records a pin that does
    not describe the content. `move()` compares every source file's sha256
    against the committed blob at this revision and RAISES rather than writing a
    manifest whose pin the content contradicts. Converting that refusal into a
    sentinel would loosen a guard nobody asked to loosen; the honest note is
    that this generator already satisfies the obligation by refusing."""
    result = subprocess.run(  # NOSONAR: argv is allowlisted; shell is disabled
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else "uncommitted"


def git_blob_sha256(root: Path, revision: str, source_path: str) -> str | None:
    # ANY DECLARED SENTINEL, not the one spelling this lane happens to write.
    # A sentinel names a condition under which no commit describes the content,
    # so there is no blob to resolve and None is the answer for every member of
    # the vocabulary. Before this consulted the declaration it compared against
    # the literal `"uncommitted"` and raised `SupportError: invalid repository
    # revision` on the other four — including `uncommitted-worktree`, which six
    # archived manifests carry, so `verify` on any of them crashed.
    if is_declared_sentinel(revision):
        return None
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", revision):
        raise SupportError(f"invalid repository revision: {revision}")
    # NORMALIZED BEFORE ANYTHING LOOKS AT IT, because both things that follow
    # read the separators: `git show` resolves `<revision>:<path>` against a
    # tree whose entries are POSIX, and the traversal guard below counts parts.
    # A backslash-spelled `source_path` from a manifest written on Windows is
    # ONE part here, so it resolves to no blob at all (the failure PR #221
    # named and deferred) and `a\..\b` would slip past a check looking for a
    # `..` component. Normalizing first fixes both.
    source = PurePosixPath(manifest_rel(source_path))
    if (source.is_absolute() or not source.parts
            or ".." in source.parts or "" in source.parts):
        raise SupportError(f"invalid repository source path: {source_path}")
    object_name = f"{revision}:{source.as_posix()}"
    result = subprocess.run(
        ["git", "-C", str(root.resolve()), "show", "--end-of-options",
         object_name],
        capture_output=True, check=False,
    )
    return sha256_bytes(result.stdout) if result.returncode == 0 else None


# THE CHANGE-ID GRAMMAR, SPELLED ONCE. Both the path-traversal guard below and
# `ratifying_commit`'s own argument check carried this pattern inline, and
# `former_id_problems` needed a third copy to say what a declared former
# identity may name. Three copies of the rule that decides how this estate
# ADDRESSES a packet is the defect `add-declared-former-id` is about, in
# miniature, so the pattern is named here and the copies are gone.
CHANGE_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")

# THE ONE SEGMENT UNDER `openspec/changes/` THAT IS NOT A PACKET. It matches
# `CHANGE_ID_RE` like any other slug, so the grammar alone never rules it out
# and every reader that resolves an id has to rule it out by name. Hoisted
# here beside the pattern for the reason the pattern itself was hoisted: the
# declaration and the walk that consumes it cannot be allowed to disagree
# about what a change id is.
RESERVED_CHANGE_ID = "archive"


def contained_dir(root: Path, path: Path) -> bool:
    """Is `path` a DIRECTORY THIS REPOSITORY ACTUALLY CONTAINS?

    THE OTHER HALF OF `active_change_dir`'S OWN GUARD. That function refuses a
    change NAME with path syntax in it, "anything with path syntax would let a
    caller-supplied name traverse outside openspec/changes/" — and a SYMLINK
    is the same traversal reached from the tree instead of from the caller.
    `is_dir()` and `iterdir()` both follow one silently, and git tracks a
    symlink as an ordinary object (mode `120000`), so it arrives through a
    pull request like any other file.

    MEASURED on this corpus's own shape: with `openspec/changes/archive`
    committed as a symlink to a directory outside the checkout,
    `former_identity_claimants` imported `stolen-identity` from an
    `.openspec.yaml` nobody in this repository wrote, and
    `declared_former_ids_in_tree` returned that outside packet's `former_ids:`
    as this corpus's lineage — a forged declaration reaching the archive gate
    through the reader. (Copilot, PR #1037 `PRRT_kwDOTAvnrs6iGr_N`.) The live
    corpus tracks ZERO symlinks anywhere, so this refuses nothing that stands
    today; it is the surface being closed, not a finding being repaired.

    RESOLVED BEFORE IT IS COMPARED, so a link CHAIN cannot walk out in more
    than one hop, and `root` is resolved too so that a checkout reached
    through a symlinked parent is not refused as foreign. A BOOLEAN rather
    than the resolved path, deliberately: callers read a packet's identity off
    the path they WALKED (`change_id_of` asks whether the parent is
    `archive/`), and handing them a resolved spelling would rename a packet
    reached through an in-repository link.
    """
    return _contained(root, path, want_dir=True)


def contained_file(root: Path, path: Path) -> bool:
    """`contained_dir` for a FILE — the same guard one level down.

    A DIRECTORY GUARD ALONE IS NOT THE SURFACE. `load_packet` opens
    `<directory>/.openspec.yaml` through `is_file()`, which follows a symlink
    exactly as `is_dir()` does, so a packet directory that IS contained can
    still carry a HEADER that is not. MEASURED at head `cce09fdd`, with a
    packet's `.openspec.yaml` committed as a symlink to a file outside the
    checkout (`git ls-files -s` → mode `120000`): the sweep claimed
    `'stolen-by-header'` and `declared_former_ids_in_tree` returned
    `['stolen-by-header']` — a lineage imported from outside the repository
    through the one file the directory guard does not cover. (Copilot, PR
    #1038 `PRRT_kwDOTAvnrs6iHNFa`.)
    """
    return _contained(root, path, want_dir=False)


def _contained(root: Path, path: Path, *, want_dir: bool) -> bool:
    try:
        resolved = path.resolve(strict=True)
        if resolved.is_dir() != want_dir:
            return False
        resolved.relative_to(root.resolve(strict=True))
    except (OSError, ValueError):
        return False
    return True


def active_change_dir(root: Path, change: str) -> Path:
    # Change ids are plain slugs; anything with path syntax would let a
    # caller-supplied name traverse outside openspec/changes/.
    if not CHANGE_ID_RE.fullmatch(change):
        raise SupportError(f"invalid change name: {change}")
    path = root / "openspec" / "changes" / change
    if not path.is_dir() or change == RESERVED_CHANGE_ID:
        raise SupportError(f"active OpenSpec change not found: {change}")
    return path


def archived_change_dir(root: Path, change: str) -> Path:
    matches = sorted((root / "openspec" / "changes" / "archive").glob(
        f"????-??-??-{change}"
    ))
    if len(matches) != 1:
        raise SupportError(
            f"expected one archived OpenSpec change for {change}, found {len(matches)}"
        )
    return matches[0]


def change_dir(root: Path, change: str, archived: bool) -> Path:
    return (archived_change_dir if archived else active_change_dir)(root, change)


STAGED_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+:staging:[a-z0-9][a-z0-9-]*$")
ADHOC_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+:adhoc:[A-Za-z0-9][A-Za-z0-9-]*$")

# The two provenance pairs an `ad_hoc` origin can carry
# (`add-drafted-proposal-origin`, issue #318). COPIED, not imported, on the
# same reasoning this file already states for `manifest_rel` and for the two
# id grammars above: `doc_health.proposal_origin` is a sibling under
# `scripts/` but it depends on PyYAML and on two further package modules,
# so it fails the "nothing outside the standard library" test that earned
# `doc_health.pin_sentinels` its import. The duplication is therefore held by
# an explicit agreement test rather than by convention —
# `test_the_gate_and_the_family_name_the_same_provenance_fields` in
# `tests/doc-health/test_proposal_origin.py`, the suite that already loads
# both sides.
APPROVAL_FIELDS = ("approved_by", "approved_on")
DRAFTING_FIELDS = ("proposed_by", "proposed_on")
STAGING_HEADER_RE = re.compile(r"^Staging ID:\s*`?([^`\s]+)`?\s*$", re.M)


def load_packet(directory: Path) -> dict | None:
    """The change's `.openspec.yaml`, or None when absent/unparseable."""
    packet = directory / ".openspec.yaml"
    if not packet.is_file():
        return None
    try:
        data = yaml.safe_load(packet.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def staging_header_id(folder: Path) -> str | None:
    """The durable `Staging ID:` a staging topic's documents declare."""
    if not folder.is_dir():
        return None
    for doc in sorted(folder.glob("*.md")):
        try:
            match = STAGING_HEADER_RE.search(doc.read_text(encoding="utf-8"))
        except OSError:
            continue
        if match:
            return match.group(1)
    return None


def origin_errors(root: Path, directory: Path, *, strict: bool,
                  manifest: dict | None = None) -> list[str]:
    """The origin-contract gate checks (add-proposal-origin-contract tasks
    2.2/2.3). `strict` is the per-change GATE posture: a missing origin is
    rejected outright. In sweep mode (strict=False) only declared origins
    are checked for coherence — pre-contract legacy visibility belongs to
    the nightly `proposal-origin` family, not to a sweeping gate."""
    name = directory.name
    packet_file = directory / ".openspec.yaml"
    if packet_file.is_file():
        packet = load_packet(directory)
        if packet is None:
            return [f"{name}: .openspec.yaml does not parse — the origin "
                    "declaration is unreadable"]
    else:
        packet = None
    origin = (packet or {}).get("origin")
    errors: list[str] = []
    if not isinstance(origin, dict):
        if strict:
            errors.append(
                f"{name}: no origin declaration — declare `origin:` "
                "(staged or ad_hoc) in .openspec.yaml")
        return errors
    kind, oid = origin.get("kind"), origin.get("id")
    if kind not in ("staged", "ad_hoc"):
        errors.append(f"{name}: unknown origin kind {kind!r}")
        return errors
    grammar = STAGED_ID_RE if kind == "staged" else ADHOC_ID_RE
    if not isinstance(oid, str) or not grammar.match(oid):
        errors.append(f"{name}: malformed durable origin id {oid!r} "
                      f"for kind {kind}")
    if (kind == "staged" and isinstance(oid, str) and ":adhoc:" in oid) or             (kind == "ad_hoc" and isinstance(oid, str) and ":staging:" in oid):
        errors.append(f"{name}: origin id and kind disagree — exactly one "
                      "origin kind per proposal")
    if kind == "staged":
        opath = origin.get("path")
        if not opath:
            errors.append(f"{name}: staged origin lacks `path`")
        elif strict:
            # Same normalization as `generator._declared_origin_staging`, and for
            # the same reason: a backslash-spelled path recorded on a Windows
            # checkout joins to one nonexistent component here, so `is_dir()`
            # fails and this coherence check SKIPS instead of running. A check
            # that silently does not run is worse than one that fails. Through
            # `manifest_rel` rather than an inline replace so this module states
            # the rule ONCE — the origin path and the file paths beside it in the
            # same record cannot be normalized two different ways.
            header = staging_header_id(root / manifest_rel(str(opath)))
            if header is not None and header != oid:
                errors.append(
                    f"{name}: staging folder {opath!r} exists but its "
                    f"`Staging ID:` ({header}) does not equal the declared "
                    f"origin id ({oid})")
    else:
        if not str(origin.get("reason") or "").strip():
            errors.append(f"{name}: ad-hoc origin lacks required `reason`")
        # THE GATE ACCEPTS THE UNAPPROVED STATE TOO, and it has to: a state
        # the nightly family calls lawful while `verify` rejects it is not a
        # lawful state, it is a state with two answers. Same three arms as
        # `doc_health.proposal_origin.check_change`, same field pairs, in the
        # same order. What the gate does NOT carry is the family's
        # ratified-status rule (class 7): this function is called at creation
        # and at transition, when the packet's status claim is `draft` by
        # construction, and the violation it names can only arise later —
        # which is when the nightly measures.
        claims_approval = any(str(origin.get(f) or "").strip()
                              for f in APPROVAL_FIELDS)
        claims_drafting = any(str(origin.get(f) or "").strip()
                              for f in DRAFTING_FIELDS)
        if claims_approval:
            for field in APPROVAL_FIELDS:
                if not str(origin.get(field) or "").strip():
                    errors.append(f"{name}: ad-hoc origin lacks required "
                                  f"`{field}`")
        elif not claims_drafting:
            errors.append(
                f"{name}: ad-hoc origin declares no provenance state — "
                "neither approval (`approved_by` + `approved_on`) nor "
                "drafting (`proposed_by` + `proposed_on`)")
        if claims_drafting:
            for field in DRAFTING_FIELDS:
                if not str(origin.get(field) or "").strip():
                    errors.append(f"{name}: drafting origin lacks required "
                                  f"`{field}`")
    if isinstance(manifest, dict) and isinstance(manifest.get("origin"), dict):
        m_origin = manifest["origin"]
        fields = ["kind", "id"] + (["path"] if kind == "staged" else [])
        for field in fields:
            if m_origin.get(field) != origin.get(field):
                errors.append(
                    f"{name}: support manifest origin `{field}` "
                    f"({m_origin.get(field)!r}) disagrees with the packet "
                    f"declaration ({origin.get(field)!r}) — the origin is "
                    "immutable after ratification")
    return errors


# --------------------------------------------------------------------------
# THE DECLARED FORMER IDENTITY
# (`release-realization` § "A moved packet declares the identity it was
#  ratified under"; add-declared-former-id, issues #1003 and #833)
#
# WHAT THIS SECTION IS. A packet whose directory MOVES to a new change id
# declares the id it moved from, in its own `.openspec.yaml`, as a member of a
# TOP-LEVEL `former_ids:` list. The declaration is the author's statement THIS
# DIRECTORY IS THAT PACKET, MOVED, and it is the only thing in the corpus that
# carries that statement: history records that two paths are similar and cannot
# record what the author MEANT by the similarity, and the two meanings need
# opposite answers — a rename of a ratified packet keeps its ratification, a
# fork authored as a copy of one gets its own.
#
# A SIBLING OF `origin:`, NEVER A MEMBER OF IT, and that is a requirement
# rather than a preference. The origin declaration is frozen at ratification
# and any post-ratification edit to it is a mutation needing an explicit
# disposition; a former-id entry is written by the very act that MOVES the
# packet, which happens after ratification BY CONSTRUCTION — a draft that
# moves owes no declaration. A member of `origin:` would therefore make every
# lawful move a mutation of a frozen declaration, a mechanism whose ordinary
# use requires an exception. `origin_block_lines` below is what makes the
# sibling position TRUE rather than conventional: it starts collecting at the
# `origin:` line and stops at the first line that is neither blank nor
# indented, so a top-level key is outside the block the archive gate freezes.
# `test_the_declaration_is_outside_the_frozen_origin_block` pins it.
#
# AN ENTRY NAMES AN ID AND NEVER A PATH, on the grammar `ratifying_commit`
# already enforces — this estate addresses a packet by its change id and
# DERIVES the path, at a ref as well as in the working tree, so an id is
# declared ONCE per identity change and both of the paths it can occupy follow
# from it. A declared path would have to restate the archive-directory
# convention in every packet that ever moved, and would have to be re-declared
# at the archive, which is not an identity change at all.
#
# THE ARCHIVE RELOCATION IS NOT A MOVE UNDER THIS REQUIREMENT and is never
# declared: it relocates `openspec/changes/<id>/` to
# `openspec/changes/archive/<YYYY-MM-DD>-<id>/` and PRESERVES the id, so a
# packet declaring it would be declaring that it used to be itself. That is
# why an entry equal to the packet's own id refuses below.
#
# WHAT THIS SECTION DOES NOT DO. It does not decide whether a COMMIT was
# entitled to add the entry it added — binding a newly added entry to the move
# that commit performs, and refusing an undeclared arrival, are the landing
# validator's, which reads a commit range this module never sees. What lives
# here is the DECLARATION and its reader: the grammar, the shape refusals, the
# append-only comparison, and the corpus ownership sweep — everything that can
# be answered from a packet and from the corpus around it.
# --------------------------------------------------------------------------

# A former-id entry is a CHANGE ID by the grammar this module already
# enforces on one — `CHANGE_ID_RE`, defined above beside `active_change_dir`,
# which was the third copy of that pattern until this section hoisted it. One
# spelling, because the declaration and the walk that consumes it cannot be
# allowed to disagree about what a change id is.
FORMER_IDS_KEY = "former_ids"

_ARCHIVE_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")


class FormerIdError(SupportError):
    """A `former_ids:` declaration that cannot be read as one.

    A subclass rather than a message so a caller can branch on "the
    declaration is malformed" without parsing prose, and so the landing
    validator can answer it with its own exit status. Every arm names the
    packet and the entry, because an operator repairs a declaration by
    editing one line of one file.

    NOT RAISED FOR AN ABSENT DECLARATION. A packet that declares no former
    identity is the ordinary case — the corpus is almost entirely such
    packets — and it reads as an empty list.
    """


def load_packet_at(root: Path, revision: str, rel_path: str, *,
                   identity: str | None = None) -> dict | None:
    """A `.openspec.yaml` AT A REVISION, parsed — None when absent or
    unparseable.

    The tree-side sibling of `load_packet`. The append-only comparison needs
    the list a packet carried at a commit's PARENT, which is not on disk
    anywhere, and reading it through `_text_at` keeps one spelling of "the
    packet at a ref" in this module.

    AND IT FAILS CLOSED, because the comparison it feeds is a read behind a
    gate like any other. Through a bare `git_show_text` an UNREADABLE parent
    answered None exactly as an ABSENT one does, `declared_former_ids` turned
    that into `[]`, and `append_only_problems` compares against `[]` without
    complaint: MEASURED, `append_only_problems("change-t", [], ["a"])` is `[]`
    while `append_only_problems("change-t", ["a", "b"], ["a"])` refuses the
    removal — so a declaration DELETED or REORDERED is accepted whenever the
    established list could not be read. That is the shed-lineage failure with
    the checkout, rather than the author, doing the shedding. Presence now
    comes off the TREE first: a genuinely absent packet is still None, and one
    the checkout cannot produce refuses `origin-retention-read-unavailable`.
    (Copilot, PR #1038 `PRRT_kwDOTAvnrs6iHw_y`.)

    `identity` names whose read this is in that refusal, and defaults to the
    id `rel_path` addresses.
    """
    identity = identity or _first_change_id_of_proposal_path(rel_path) or rel_path
    text = _text_at(root, revision, rel_path, identity=identity)
    if text is None or yaml is None:
        return None
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def change_id_of(directory: Path) -> str:
    """The change id a packet directory carries — the ARCHIVE's date prefix
    stripped, and nothing else.

    `openspec/changes/add-x` and `openspec/changes/archive/2026-09-09-add-x`
    are the same IDENTITY at two moments of its life, which is the whole
    reason the archive relocation is never a declared move.

    THE PREFIX IS THE ARCHIVE'S, AND ONLY THE ARCHIVE'S. An ACTIVE
    directory's NAME IS ITS ID, whatever that name begins with: `CHANGE_ID_RE`
    admits a leading date, `active_change_dir` resolves such an id verbatim,
    and this corpus's own test fixture carries `2026-08-04-add-dated`. Read
    unconditionally, the strip RENAMED every such live packet — and
    `former_identity_claimants`, which passes live directories through here,
    then validated and attributed `2026-08-04-add-dated`'s `former_ids:`
    declaration as `add-dated`'s, so the "an entry may not name the packet's
    OWN id" refusal was asked about the wrong packet in both directions.
    (Copilot, PR #1038 `PRRT_kwDOTAvnrs6iEmbV` and PR #1037
    `PRRT_kwDOTAvnrs6iEemp`.)

    AND THE ARCHIVED HALF IS GENUINELY AMBIGUOUS, which this function does
    NOT pretend to settle. `archive_directory_name` states the pinned CLI's
    own rule — a change whose id already carries a `YYYY-MM-DD-` prefix is
    archived under that id UNCHANGED — so `archive/2026-08-04-foo` is the
    archive of `foo` AND the archive of a change whose id IS
    `2026-08-04-foo`, and `names_this_change` says in as many words that "the
    two readings are indistinguishable from the name". This returns the
    commoner reading for the callers that want one string; a caller ASKING
    WHETHER A DIRECTORY IS A GIVEN CHANGE'S asks `names_this_change`, and a
    caller resolving an identity to a PATH asks `identity_paths_at`, which
    admits both readings and refuses where one identity matches two
    directories.
    """
    if directory.parent.name != RESERVED_CHANGE_ID:
        return directory.name
    return _ARCHIVE_DATE_RE.sub("", directory.name, count=1)


def packet_identities_of(directory: Path) -> list[str]:
    """EVERY id a packet directory can carry, the directory's own name first.

    `change_id_of`'s plural sibling, for the callers that must not silently
    choose the shorter reading. An ACTIVE directory carries exactly one id —
    its name. An ARCHIVED one carries two whenever its name is dated, because
    `archive_directory_name` preserves an already-dated id unchanged, and
    `names_this_change` says the readings "are indistinguishable from the
    name": `archive/2026-09-09-foo` is the archived `foo` AND the archived
    `2026-09-09-foo`.

    MEASURED at head `cce09fdd`, which is why this exists rather than the
    residue note it replaces: an archived packet declaring `former_ids:
    [2026-09-09-foo]` from the directory `archive/2026-09-09-foo` — a claim
    to be the move of ITSELF — was validated as `foo`, passed every arm, and
    the corpus sweep indexed the self-claim as a legitimate lineage. (Copilot
    `PRRT_kwDOTAvnrs6iG9vt`, Codex P2 `PRRT_kwDOTAvnrs6iHS5I`.)
    """
    found = [directory.name]
    stripped = change_id_of(directory)
    if stripped != directory.name:
        found.append(stripped)
    return found


def former_id_problems(change: str, packet: dict | None) -> list[str]:
    """The shape refusals over a packet's `former_ids:` — empty when the
    declaration is well formed, and empty when there is none.

    Seven refusals, each named in `release-realization` § "A moved packet
    declares the identity it was ratified under" or in this packet's own
    tasks:

    * the key declared INSIDE `origin:` rather than beside it — the position
      is normative, for the freeze reason the section header states;
    * a scalar (or a mapping) where a SEQUENCE is required;
    * an entry that is not a change id by the grammar `ratifying_commit`
      enforces;
    * an entry naming `RESERVED_CHANGE_ID` — the `archive` segment is not a
      packet, and the grammar cannot refuse it because it is a lawful slug;
    * an entry equal to the packet's OWN id — a packet cannot be the move of
      itself, and the archive relocation, which preserves the id, is the one
      move that is never declared;
    * a duplicate entry — an identity is declared once;
    * (reported by `append_only_problems`, not here) a list that rewrites what
      an earlier commit established.

    WHAT IS DELIBERATELY NOT REFUSED HERE. An entry naming an id that does not
    resolve anywhere in this corpus is NOT a shape defect: the whole point of
    a former identity is that the id it names no longer stands as a directory.
    Whether the commit that ADDED the entry was entitled to add it is the
    landing validator's question and needs a commit range, which this reader
    does not have.
    """
    problems: list[str] = []
    if not isinstance(packet, dict):
        return problems
    origin = packet.get("origin")
    if isinstance(origin, dict) and FORMER_IDS_KEY in origin:
        problems.append(
            f"{change}: `{FORMER_IDS_KEY}:` is declared INSIDE `origin:`. It "
            f"is a TOP-LEVEL SIBLING of `origin:` and never a member of it — "
            f"the origin declaration is frozen at ratification, so a member "
            f"would make every lawful move a mutation of a frozen "
            f"declaration and would need a disposition for each one")
    if FORMER_IDS_KEY not in packet:
        return problems
    declared = packet[FORMER_IDS_KEY]
    if not isinstance(declared, list):
        problems.append(
            f"{change}: `{FORMER_IDS_KEY}:` is {type(declared).__name__} "
            f"({declared!r}), and a SEQUENCE of change ids is required — a "
            f"packet may move more than once, so the declaration is a list "
            f"ordered oldest first even when it carries one entry")
        return problems
    seen: dict[str, str] = {}
    for index, entry in enumerate(declared):
        where = f"`{FORMER_IDS_KEY}[{index}]`"
        if not isinstance(entry, str) or not entry.strip():
            problems.append(
                f"{change}: {where} is {entry!r}, and an entry names a "
                f"CHANGE ID — a non-empty string matching "
                f"`{CHANGE_ID_RE.pattern}`")
            continue
        if not CHANGE_ID_RE.fullmatch(entry):
            problems.append(
                f"{change}: {where} names {entry!r}, which is not a change "
                f"id by the grammar this estate resolves a packet with "
                f"(`{CHANGE_ID_RE.pattern}`). An entry names an ID and never "
                f"a PATH: the path is derived from the id, at a ref as well "
                f"as in the working tree")
            continue
        if entry == RESERVED_CHANGE_ID:
            problems.append(
                f"{change}: {where} names {entry!r}, which is the RESERVED "
                f"segment `openspec/changes/{RESERVED_CHANGE_ID}/` and never "
                f"a packet. It matches the id grammar like any other slug, so "
                f"the pattern above cannot refuse it and this arm must — "
                f"`active_change_dir` already reserves it by name, and no "
                f"resolution of an identity to a path can return anything "
                f"for it, so the entry would stand as a declared lineage "
                f"that every reader answers with silence")
            continue
        if entry == change:
            problems.append(
                f"{change}: {where} names the packet's OWN id, which is a "
                f"claim to have been moved from itself. The archive "
                f"relocation to "
                f"`openspec/changes/archive/<YYYY-MM-DD>-{change}/` PRESERVES "
                f"the id and is never a declared move")
            continue
        if entry in seen:
            problems.append(
                f"{change}: {where} repeats {entry!r}, already declared at "
                f"{seen[entry]} — an identity is declared ONCE, and a list "
                f"that names one twice cannot say how many times the packet "
                f"moved")
            continue
        seen[entry] = where
    return problems


def declared_former_ids(change: str, packet: dict | None) -> list[str]:
    """The packet's declared former identities, OLDEST FIRST — `[]` when it
    declares none.

    Raises `FormerIdError` naming every problem when the declaration is
    malformed, rather than returning the entries it could read: a reader that
    silently drops a bad entry would hand the archive gate a SHORTER lineage
    than the author wrote, which is the shed-lineage defect arriving through
    the reader instead of through a move.
    """
    problems = former_id_problems(change, packet)
    if problems:
        raise FormerIdError("; ".join(problems))
    declared = (packet or {}).get(FORMER_IDS_KEY)
    return list(declared) if isinstance(declared, list) else []


def declared_former_ids_of(directory: Path, change: str | None = None
                           ) -> list[str]:
    """`declared_former_ids` for a packet directory on disk, active or
    archived — the shape every caller in this module wants."""
    change = change or change_id_of(directory)
    return declared_former_ids(change, load_packet(directory))


def append_only_problems(change: str, established: list[str],
                         current: list[str]) -> list[str]:
    """The append-only comparison: `current` must be `established` PLUS zero
    or more new entries at the END.

    APPEND-ONLY ACROSS COMMITS AND NOT ONLY WITHIN ONE, which is the whole
    reason this is a separate function from `former_id_problems`. The arrival
    check only ever runs at a MOVE, so without this a lawful move could be
    declared at its landing and the declaration deleted the day after, in a
    commit no arrival check ever looks at — handing the archive gate the later
    ratification under the current id, the very baseline this mechanism exists
    to keep it away from.

    `established` is the list the packet carried at the commit's PARENT and
    `current` the list it carries at the commit. A removal, a reorder and a
    respelling are all the same defect to the comparison (the established
    prefix is no longer a prefix) and each is named separately in the finding,
    because they are three different author mistakes.
    """
    if list(current[:len(established)]) == list(established):
        return []
    missing = [entry for entry in established if entry not in current]
    kept = [entry for entry in established if entry in current]
    reordered = [entry for entry in kept
                 if current.index(entry) != established.index(entry)]
    detail: list[str] = []
    if missing:
        detail.append("REMOVED " + ", ".join(repr(e) for e in missing))
    if reordered:
        detail.append("REORDERED " + ", ".join(repr(e) for e in reordered))
    if not detail:
        detail.append("REWRITTEN")
    return [f"{change}: `{FORMER_IDS_KEY}:` is APPEND-ONLY ACROSS COMMITS and "
            f"this commit rewrites it — {'; '.join(detail)}. Established "
            f"{established!r}, now {current!r}. An entry an earlier commit "
            f"established may never be removed, reordered or respelled, "
            f"whether or not this commit moves anything: a declaration "
            f"deleted after a lawful move hands the archive gate the later "
            f"ratification under the current id"]


def former_identity_claimants(root: Path) -> dict[str, list[str]]:
    """Every identity this corpus claims -> the packets claiming it.

    Two kinds of claim, and the requirement names both: a LIVE packet
    directory claims its own id, and any packet — active or archived —
    claims every id it declares in `former_ids:`. The ARCHIVED directories
    are read for their DECLARATIONS and not for their own ids: a declaration
    travels with the packet into the archived directory the archive gate
    reads, so an archived packet's lineage is still a claim on those ids.

    A malformed declaration is skipped rather than raised over: this is the
    corpus sweep, and `former_id_problems` is the reader that reports shape.

    AND THE ARCHIVED HALF IS ASKED UNDER BOTH OF ITS READINGS. An earlier
    draft of this docstring named that as a residue and left it; two reviewers
    then measured it, so it is closed rather than noted.
    `packet_identities_of` returns every id an archive directory can carry,
    and a declaration naming ANY of them is a self-claim — the arm
    `former_id_problems` can only ask about one id at a time.

    EVERY HEADER IS CONTAINMENT-CHECKED, not only every directory:
    `load_packet` opens `.openspec.yaml` through `is_file()`, which follows a
    symlink, so a contained packet directory can still carry an uncontained
    header.
    """
    claimants: dict[str, list[str]] = {}

    def claim(identity: str, by: str) -> None:
        claimants.setdefault(identity, [])
        if by not in claimants[identity]:
            claimants[identity].append(by)

    changes = root / "openspec" / "changes"
    if not contained_dir(root, changes):
        return claimants
    live = [d for d in sorted(changes.iterdir())
            if d.name != RESERVED_CHANGE_ID and contained_dir(root, d)]
    archived_root = changes / "archive"
    archived = ([d for d in sorted(archived_root.iterdir())
                 if contained_dir(root, d)]
                if contained_dir(root, archived_root) else [])
    for directory in live:
        claim(directory.name, f"the live packet `{_corpus_rel(directory)}`")
    for directory in live + archived:
        if not contained_file(root, directory / ".openspec.yaml"):
            continue
        identities = packet_identities_of(directory)
        try:
            ids = declared_former_ids_of(directory, identities[0])
        except FormerIdError:
            continue
        # A SELF-CLAIM UNDER EITHER READING OF AN ARCHIVE NAME IS STILL A
        # SELF-CLAIM. `former_id_problems` is asked about ONE id, and for the
        # ambiguous archive shape the id it was asked about may be the other
        # one — so the arm that refuses "a packet cannot be the move of
        # itself" could be evaded by declaring the directory's OTHER
        # identity. Asked here over every identity the directory can carry.
        if any(identity in ids for identity in identities):
            continue
        for identity in ids:
            claim(identity,
                  f"`{_corpus_rel(directory)}` declares it in "
                  f"`{FORMER_IDS_KEY}:`")
    return claimants


def _corpus_rel(directory: Path) -> str:
    """A packet directory as the corpus spells it, for a finding that reads
    the same on a runner and on a developer machine."""
    parts = directory.parts
    if "changes" in parts:
        index = len(parts) - 1 - parts[::-1].index("changes")
        return "/".join(("openspec",) + parts[index:])
    return directory.name


def former_identity_ownership_problems(root: Path) -> list[str]:
    """A FORMER IDENTITY HAS EXACTLY ONE OWNER — the corpus sweep that says so.

    Where two packets declare the same former id, or where an id is at once a
    live packet id and some packet's declared former id, the declaration is
    refused NAMING EVERY CLAIMANT. An identity claimed twice resolves to a
    SET, and a baseline chosen from a set is a baseline chosen by the resolver
    rather than by an author — the same line this estate's own archived-
    directory lookup draws when it returns a LIST because "two archive dates
    for one id is an AMBIGUITY the resolver must be able to report, not a
    collision to resolve by taking the newest".
    """
    problems = []
    for identity, claimants in sorted(former_identity_claimants(root).items()):
        if len(claimants) < 2:
            continue
        problems.append(
            f"former identity {identity!r} is claimed by "
            f"{len(claimants)} packets — " + "; ".join(claimants) +
            ". A former identity has EXACTLY ONE OWNER: an identity claimed "
            "twice resolves to a set, and a baseline chosen from a set is "
            "chosen by the resolver rather than by an author")
    return problems


def standing_former_id_problems(root: Path, change: str,
                                ids: list[str]) -> list[str]:
    """A DECLARED FORMER ID SHALL RESOLVE TO A PACKET THAT ACTUALLY MOVED.

    A former id that still stands as a LIVE packet directory is a claim to be
    the move of something that did not move — that shape is a COPY, and a copy
    is a new packet with its own origin, its own first ratification and no
    inherited lineage. Refused naming BOTH ids, because the repair is a choice
    between them: either the source really moved (and its directory should be
    gone) or this packet is a fork (and owes no declaration).

    Read against the tree it is GIVEN, so the archive gate can ask it of the
    working tree and the landing validator of a commit's tree.
    """
    problems = []
    for identity in ids:
        standing = root / "openspec" / "changes" / identity
        if standing.is_dir():
            problems.append(
                f"{change}: declares former id {identity!r}, but "
                f"`{_corpus_rel(standing)}` STILL STANDS in this tree. A "
                f"packet that still stands was COPIED and not moved, and a "
                f"copy is a new packet with its own origin — declare nothing, "
                f"or complete the move")
    return problems

# --------------------------------------------------------------------------
# ORIGIN RETENTION AT THE ARCHIVE GATE
# (`release-realization` § "Origin retention at archive"; issue #690)
#
# THE REQUIREMENT HAD NO RUNNING IMPLEMENTATION. `origin_errors` above checks
# PRESENCE AND SHAPE — a declaration exists, its kind is known, its id matches
# the grammar, the support manifest repeats it — and every one of those reads
# only the packet in front of it. None of them can see the declaration the
# change was RATIFIED over, so "Mutation of an origin declaration after
# ratification SHALL be rejected at the archive gate" was enforced by nobody:
# PR #685 edited the `origin.approved_by` prose of an already-ratified packet
# (commit `ab2003aa`, after the ratifying commit `517980e1`) and the archive
# landed green. The nightly `proposal-origin` family calls its own class-3
# finding "post-ratification mutation", but that finding compares the manifest
# against the packet — two copies that a lockstep edit moves together — and
# never against history.
#
# So the baseline is read from HISTORY, which is the one copy an edit at
# archive time cannot reach: the packet's `.openspec.yaml` AT THE RATIFYING
# COMMIT, the first commit whose `proposal.md` declares `Status: ratified`.
#
# THE CURRENT SIDE IS THE WORKING TREE, NOT `HEAD`, deliberately. The bytes
# that archive are the bytes on disk; in a clean checkout they are HEAD's, and
# where they are not, reading HEAD would wave through exactly the edit that is
# about to be committed as part of the archive.
#
# NO BYPASS FLAG. The requirement's own scenario says restoring or accepting a
# mutation is a contested-class act requiring an explicit disposition, and a
# flag on this gate would be the disposition nobody records.
#
# THE ACCEPTING HALF OF THAT SCENARIO IS A RECORD, NOT A FLAG (issue #745).
# `openspec/origin-dispositions.yaml`, read from the ROOT THIS GATE WAS GIVEN,
# carries an owner-attributed entry naming the ratifying commit, the accepted
# mutating commit, the keys that moved and the verbatim word; a valid entry
# moves the comparison baseline to the ACCEPTED declaration and every arm here
# then runs against that. The full reasoning, the entry's shape and every
# condition an acceptance must satisfy are stated at
# `accepted_origin_mutation` further down. The subcommand still grows no flag.
#
# A MOVED PACKET REFUSES RATHER THAN RE-BASING (issue #833). The baseline is
# resolved by walking ONE path — `openspec/changes/<change>/proposal.md`, the
# id the tree spells TODAY — and a ratified change whose directory is renamed
# afterwards has no history under its new name before the rename. The walk's
# first ratified blob is then the RENAME COMMIT, which is later than every
# mutation made in between, and the gate printed `ORIGIN RETAINED` over it:
# measured on issue #777, where a ratified change renamed on a trial branch
# passed a gate whose baseline had moved four days forward, and named verbatim
# in `ratifying_commit`'s own docstring as the failure that matters. So the
# walk now asserts what a ratifying commit IS — a FLIP, and a flip's parent
# does not already declare `ratified` — and REFUSES, named and exit 2, when
# the candidate is instead the commit that moved an already-ratified packet.
# THE REFUSAL IS THE WHOLE OF THE FIX: nothing in this corpus declares a
# former id, so there is no earlier path this walk could lawfully re-base
# onto, and inventing one from rename detection alone would be this gate
# guessing at the identity it exists to hold fixed. Following a ratified
# change across a declared rename is a later packet.
# --------------------------------------------------------------------------


class OriginRetentionError(SupportError):
    """The archive gate's origin-retention refusal — ANY arm of it.

    Four conditions raise it, and the exception is deliberately one rather
    than four: the declaration moved after ratification, the PACKET moved OR
    WAS COPIED (a ratified change renamed after its ratification — or
    duplicated to a second id, which git pairs identically and which leaves
    the baseline just as unestablishable — issue #833), no ratifying commit
    exists to compare against, or the history that holds the baseline could
    not be read. What they share is the only thing a caller can act on — the
    packet CANNOT BE SHOWN to still carry the origin it was ratified over — and
    none of them is the "fix the tree and retry" shape that `SupportError` means
    everywhere else in this script.

    A subclass rather than a message, so the CLI can answer with its own exit
    status (2) and a script can branch on "retention could not be established"
    without parsing prose. WHICH arm it was is in the message, never in the
    number. The mutation arm alone carries the further consequence the
    requirement names — restoring or accepting it is a contested-class act
    requiring an explicit disposition — and the finding for that arm says so
    in its own text.

    THE MOVED-PACKET ARM IS RAISED BY THE WALK ITSELF (`ratifying_commit`),
    not assembled as a finding by `origin_retention_errors` like the other
    three. It is not a comparison that failed: it is the comparison being
    IMPOSSIBLE, because the commit the walk would compare against is the move
    rather than the ratification, so there is nothing to put in a findings
    list and no arithmetic left to do.
    """


# `ratified`, bare or annotated (`ratified (superseded by <change>)`) — the two
# grammars `doc_health.promotion_fidelity` already recognizes for one standing,
# spelled here over this module's own fence-aware row reader rather than as a
# second private opinion about where a lifecycle header lives.
_RATIFIED_BODY_RE = re.compile(r"Status:\s*ratified\s*(\(.*\))?\s*")


def declares_ratified(text: str) -> bool:
    """Whether this `proposal.md` text's OWN header declares `ratified`.

    Fence-aware for the reason `_declares_staged_status` states above: a
    `Status: ratified` line inside a ``` block is an EXAMPLE. A proposal
    quoting one — this repository's governance prose quotes lifecycle headers
    constantly — would otherwise resolve a ratifying commit that ratified
    nothing, and the baseline the whole gate rests on would be a fenced
    example.
    """
    rows = _split_keepends(text)
    flags = _fenced_flags(rows)
    for index, (body, _ending) in enumerate(rows):
        if flags[index]:
            continue
        if _RATIFIED_BODY_RE.fullmatch(body):
            return True
    return False


def git_show_text(root: Path, revision: str, rel_path: str) -> str | None:
    """`<revision>:<rel_path>` as text, or None when git cannot resolve it."""
    result = subprocess.run(  # NOSONAR: argv is allowlisted; shell is disabled
        ["git", "-C", str(root.resolve()), "show", "--end-of-options",
         f"{revision}:{rel_path}"],
        capture_output=True, check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8", "replace")


def _pairing_rows(root: Path, revision: str, rel: str) -> list[str] | None:
    """The `--name-status` records git pairs `rel` with AT `revision` — `[]`
    when it pairs it with NOTHING, and None when the read could not be
    performed.

    THE PROBE SEPARATES THE TWO SILENCES AND RAISES NEITHER, exactly as
    `_tree_rows` does, and for the same reason: a NON-ZERO EXIT IS RETURNED AS
    None AND NEVER AS AN EMPTY LIST, because "this commit moved nothing" and
    "I cannot tell you whether it moved anything" are different facts that
    one value used to carry. `_pairing_or_refuse` is the one door that None
    leaves by; `renamed_from` is the tolerant reading kept for readers that
    are not a gate.

    A REVISION THAT RESOLVES TO NOTHING IS `[]` AND NOT None, and the
    distinction is deliberate: a question about a commit that is not there is
    not a read that failed, and it answered "no pairing" before this split as
    the paragraph on revision spellings below says it should.

    `kinds` NARROWS WHICH PAIRING COUNTS, for the one caller that needs a
    RENAME (`R`, the former path GONE) and not a COPY (`C`, the former path
    still standing) — issue #849. Default `"RC"` is every existing behaviour
    in this docstring, unchanged. It is applied by `_former_path_in` over
    these rows rather than here, so that both doors read one set of records.

    RENAME DETECTION IS GIT'S OWN, reached through `--follow` — the one mode
    that pairs a rename for a SINGLE path — and NOT through a pathspec-limited
    diff, which cannot pair one at all: limiting the diff to the DESTINATION
    filters the source side out before detection runs, so git reports a plain
    `A`. Measured on `9ec13c1a`, where the dotless draft id first appears
    (landed by PR #777): `git show --name-status --find-renames <sha> --
    <new path>` says `A`, while `git log --follow` over the same commit says
    `C099` from the old dotted path.

    A GIT CONFIG CANNOT SWITCH THE GUARD BELOW OFF, and `--follow` is what
    makes that true rather than the flag beside it: `--follow` FORCES rename
    detection, so `diff.renames=false` — and `diff.renameLimit=1` next to it,
    the other knob that can make detection give up — still reports the
    pairing (measured on git 2.43.0, with the flag and without it).
    `--find-renames` is passed anyway as a BELT, not the mechanism: it states
    the request at the call site, and it is the flag that would matter if a
    pairing were ever read from a plain diff instead. Dropping it therefore
    breaks no test, which is stated here because the property that does
    matter is pinned by a fixture carrying the hostile config in its own
    `.git/config` (`test_a_git_config_cannot_switch_the_guard_off`) rather
    than by this note.

    COPIES COUNT, not only renames. A "rename" that leaves the old directory
    standing is a DUPLICATED packet rather than a moved one, and the question
    this answers — did this packet exist under another name before this
    commit — has the same answer either way. (`9ec13c1a` above is exactly
    that shape: the pairing git found was a copy, because the commit that
    added the new name did not remove the old one.) NO `--find-copies` IS
    NEEDED for that, which is worth stating because copy detection is
    normally opt-in: `--follow` turns it on for the followed path, and a
    copied packet reports `C100` on DEFAULT config, without
    `--find-renames`, and even under `diff.renames=false` — measured on git
    2.43.0, and standing proof in
    `test_a_ratified_packet_copied_to_a_new_id_refuses_too`, which passes on
    a default-configured runner.

    ONE COMMIT IS ASKED ABOUT, not a history: `-1 <revision>` bounds the
    walk to the candidate itself, which is the only commit whose pairing the
    guard below acts on. `--follow` without it walks the whole followed
    history of the path — 0.3s per change against this repository, 58s across
    its 189 packets — for records nothing reads. A pairing is then accepted
    ONLY when its destination is `rel` itself, so a rename hop belonging to
    some other name can never be read as the predecessor of the current one.

    ANY SPELLING OF THE REVISION IS ACCEPTED, and that is a guard property
    rather than a convenience. The pairing is recognised by comparing git's
    own `%H` against the revision asked about, so `HEAD`, `HEAD~1`, a tag or
    an abbreviated sha would every one of them compare unequal to a full
    40-hex hash and be answered None — NO PAIRING, no refusal: the #833
    defect back, reached through a caller rather than a config. So the
    revision is resolved to its commit hash first (`rev-parse --verify
    <revision>^{commit}`, which also peels an annotated tag). The only
    caller today passes a full hash straight out of `git log --format=%H`,
    so this changes no answer in this corpus; it is here so that a future
    call site cannot switch the guard off by naming its commit differently
    (raised by the review bench on PR #846, pinned by
    `test_the_guard_reads_any_spelling_of_the_candidate_commit`). A revision
    that resolves to nothing answers None, as an unreadable history already
    did.
    """
    resolved = subprocess.run(  # NOSONAR: argv is allowlisted; shell is disabled
        ["git", "-C", str(root.resolve()), "rev-parse", "--verify",
         f"{revision}^{{commit}}"],
        capture_output=True, text=True, check=False,
    )
    if resolved.returncode != 0:
        return []
    revision = resolved.stdout.strip()
    listed = subprocess.run(  # NOSONAR: argv is allowlisted; shell is disabled
        ["git", "-C", str(root.resolve()), "log", "--follow",
         "--find-renames", "--name-status", "--format=%x00%H", "-1",
         revision, "--", rel],
        capture_output=True, text=True, check=False,
    )
    if listed.returncode != 0:
        return None
    for record in listed.stdout.split("\0"):
        rows = [row for row in record.splitlines() if row.strip()]
        if rows and rows[0].strip() == revision:
            return rows[1:]
    return []


def _former_path_in(rows: list[str], rel: str, kinds: str) -> str | None:
    """The source `rel` was paired with in `rows`, for a pairing of a kind
    `kinds` admits — None where the records name no such pairing."""
    for row in rows:
        fields = row.split("\t")
        if (len(fields) == 3 and fields[0][:1] in kinds
                and fields[2] == rel):
            return fields[1]
    return None


def renamed_from(root: Path, revision: str, rel: str, *,
                 kinds: str = "RC") -> str | None:
    """`_pairing_rows` read as one answer: the path `rel` was renamed or
    copied from at `revision`, or None when it was not — AND None when the
    read could not be performed at all.

    THE TOLERANT DOOR, KEPT FOR THE READERS THAT ARE NOT A GATE. Every gate
    caller goes through `_pairing_or_refuse` instead, because for a gate the
    two silences are not the same fact; this spelling survives for the tests
    and for any reader that only ever wanted "did git pair this".
    """
    rows = _pairing_rows(root, revision, rel)
    return None if rows is None else _former_path_in(rows, rel, kinds)


def _pairing_or_refuse(root: Path, revision: str, rel: str, *, kinds: str,
                       identity: str) -> str | None:
    """`_pairing_rows`, with its None raised rather than read as "no move".

    THE ONE DOOR THAT None LEAVES BY, the way `_rows_or_refuse` is for
    `_tree_rows`. MEASURED on git 2.43.0, on the `--filter=blob:none` clone
    of the #1003 chain with its promisor cut: at the hop that renames a
    ratified packet AND edits it, `git log --follow --find-renames
    --name-status -1 <hop> -- <destination>` exits **128** (`fatal: could not
    fetch … from promisor remote`), because rename pairing below an exact
    match is computed FROM CONTENT and this checkout has none to compute it
    from. Read as None that failure was indistinguishable from "this commit
    moved nothing", so the walk accepted the RENAME COMMIT as the baseline
    and the archive gate then compared the packet against the declaration
    standing after the mutation: `origin_retention_errors` returned `[]` over
    a tree the full clone of the same history refuses. That is the #833
    failure reached through a partial clone rather than through a rename, and
    "EVERY READ BEHIND THE BASELINE SHALL FAIL CLOSED" is the clause it
    contradicted.
    """
    rows = _pairing_rows(root, revision, rel)
    if rows is None:
        raise _unreadable_read_refusal(
            identity,
            f"git log --follow --find-renames --name-status -1 "
            f"{revision[:12]} -- {rel}",
            f"whether {revision[:12]} carries `{rel}` in from another packet "
            f"— the move this walk must rule out before it may take that "
            f"commit as the baseline", at=revision)
    return _former_path_in(rows, rel, kinds)


def ratified_under_a_former_path(root: Path, revision: str, rel: str, *,
                                 kinds: str = "RC",
                                 identity: str | None = None) -> str | None:
    """The path this packet occupied BEFORE `revision` moved it, when it
    ALREADY declared `Status: ratified` there — the case in which `revision`
    cannot be the ratification. None otherwise.

    `kinds` is passed straight through to `renamed_from` (default `"RC"`,
    every existing call in this docstring); see that function and the
    "THE COMMIT EXAMINED IS EVERY COMMIT" paragraph below for the one caller
    that narrows it to `"R"`.

    WHAT A RATIFYING COMMIT IS, stated as a test the candidate must pass: a
    FLIP. The commit that ratifies a packet is the commit at which its header
    STOPPED saying something else, so the packet as its parent carried it does
    NOT declare `ratified`. A commit that merely MOVED an already-ratified
    packet passes the walk's own test (the blob it lands is ratified) and
    fails this one, which is the whole of the #833 defect.

    THE PARENT IS READ AT THE PACKET'S FORMER PATH, which is the only place it
    is: after a rename there is nothing at `rel` in the parent to read, and a
    walk that read `rel` alone would find nothing missing.

    RENAMING A DRAFT IS LAWFUL AND STAYS LAWFUL. When the packet under its
    former name was still a draft, the flip really did happen at `revision`
    and the baseline is sound — the corpus does this (`46059b77`, #834,
    renamed a DRAFT change toward the dotless grammar), so this returns None
    for it and nothing refuses.

    THE COMMIT EXAMINED IS EVERY COMMIT IN THE PATH'S HISTORY, not only the
    one that ends up declaring `ratified` (issue #849, raised as a P1 on PR
    #846; closed here for RENAMES). Asking only the CANDIDATE commit left one
    shape out: a commit that renames an already-ratified packet AND
    un-ratifies the destination in the same commit is never a candidate (its
    own blob is not ratified), and a LATER commit that re-ratifies it carries
    no pairing of its own — so a walk that asked only candidates took the
    re-ratification as its baseline, later than the real ratification, and
    waved through whatever mutated in between. `ratifying_commit` now calls
    this function for EVERY commit its walk visits, not only the one whose
    blob happens to declare `ratified`, so the rename-and-un-ratify commit is
    asked the question too and answers it before any later re-ratification is
    ever reached.

    RESTRICTED TO RENAMES (`kinds="R"`) FOR THAT BROADER CALL, deliberately,
    because a COPY answers the same question ambiguously. The wider closure —
    refuse on any hop whose source declared `ratified` at that hop's parent,
    rename OR copy — cannot separate "an already-ratified packet renamed and
    un-ratified in one commit" from "a NEW packet authored as a copy of a
    ratified one, entering as a draft and ratified later": both are, to
    history, "source ratified at the hop's parent, destination not ratified
    at the hop" (probed over this corpus: 4 of 189 packets carry such a hop
    before their baseline, all four with a draft source, 0 refusals — a
    copy-inclusive closure changes today's answer for nobody, and would still
    be a trap for the first lawful fork-by-copy). A RENAME carries no such
    ambiguity: the former path is GONE, so there is no surviving original
    this could instead be "authored from" — whatever carries the ratified
    lineage now lives only at the new path, and an un-ratifying edit along
    the way mutates THAT packet's origin rather than authoring a new one. So
    the broader call below passes `kinds="R"`; a COPY is still caught only
    where it always was — at the candidate commit itself, through the
    default `kinds="RC"` — and a copy that enters as a draft and is ratified
    later remains the fork-by-copy this gate must not trap, exactly as
    before. The former-id declaration (#833's option (b)) is what would let a
    copy-shaped mutation be told apart from authoring on its own merits;
    until it lands, this is the line.

    WHERE THIS CANNOT SEE. When rename detection finds no pairing — a move
    that also rewrote `proposal.md` past git's similarity threshold, or a
    move landed as a delete-and-add in separate commits — the predecessor is
    unnameable and this returns None, leaving the pre-#833 behaviour. Naming
    a former identity is what a FORMER-ID DECLARATION would do, and that is
    the successor packet; the guard here closes the shape that was measured,
    and does not pretend to close identity.

    AND WHERE IT IS DELIBERATELY BLUNT. A packet whose `proposal.md` was
    authored as a near-verbatim COPY of an already-ratified one, and which
    entered history ratified, pairs the same way and takes the same refusal —
    even though its own creation commit would have been a sound baseline.
    History alone cannot separate "this packet moved" from "this packet was
    copied from that one", which is the whole of what a former-id declaration
    would settle, so the ambiguous case answers CANNOT RUN rather than
    guessing. Zero of the 189 active-plus-archived packets on `main` trip it
    (measured while authoring the guard), and a proposal that similar to a
    ratified one is what `add-duplicate-packet-check` exists to notice.

    AND BOTH OF ITS READS FAIL CLOSED (`tasks.md` § 3.4, the MODIFIED
    requirement's *"EVERY READ BEHIND THE BASELINE SHALL FAIL CLOSED"*). This
    guard is TWO reads, not one — the PAIRING at `revision`, and the SOURCE
    PACKET'S HEADER at `revision^` — and a partial checkout answers each of
    them with a silence indistinguishable from the innocent answer:

    * the pairing read exits non-zero and used to return None, which reads as
      "this commit moved nothing"; it now goes through `_pairing_or_refuse`;
    * the header read returned None from `git_show_text`, which reads as "the
      source was not ratified", and `git show` answers a GENUINELY ABSENT
      path and an UNREADABLE one with the same exit 128 (`design.md` M1); it
      now goes through `_text_at`, which takes presence off the TREE first,
      so an absent predecessor is still None and an unreadable one refuses.

    Either silence, read flat, skipped the refusal and let the walk take a
    LATER baseline — the failure this whole guard exists to stop, arriving
    through the checkout instead of through the rename.

    `identity` NAMES WHOSE WALK THIS IS in that refusal, and defaults to the
    id `rel` addresses so that no caller can leave the refusal unattributed.
    """
    identity = identity or _first_change_id_of_proposal_path(rel) or rel
    former = _pairing_or_refuse(root, revision, rel, kinds=kinds,
                                identity=identity)
    if former is None:
        return None
    before = _text_at(root, f"{revision}^", former, identity=identity)
    if before is not None and declares_ratified(before):
        return former
    return None


_ARCHIVE_DIR_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<id>.+)$")
_ARCHIVE_ROOT = "openspec/changes/archive/"


def _archive_dir_carries(name: str, identity: str, *,
                         live_ids: frozenset[str] | set[str]
                         = frozenset()) -> bool:
    """Is the archive directory `name` a location `identity` can occupy?

    TWO READINGS, AND THE EXACT ONE IS ASKED FIRST. `archive_directory_name`
    states the pinned CLI's own rule: a change whose id ALREADY carries a
    `YYYY-MM-DD-` prefix is archived under that id UNCHANGED, because
    "re-prefixing would stutter the name, and when the archive runs on a
    later day the folder would sort under a day on which the change did not
    happen". So `openspec/changes/archive/2026-09-09-foo` is the archived
    `foo` AND the archived `2026-09-09-foo`, and reading the date prefix
    unconditionally lost the second: `identity_paths_at(root, revision,
    "2026-09-09-foo")` reported the packet ABSENT with its `proposal.md`
    standing in that very directory, so the walk passed its ratification by.
    (Codex P2 `PRRT_kwDOTAvnrs6iElb4` and Copilot `PRRT_kwDOTAvnrs6iEmbp` on
    PR #1038.)

    ADMITTING BOTH IS WHAT THE REQUIREMENT ASKS FOR, not a hedge. The
    identity resolution "SHALL NOT infer an identity from rename detection,
    from similarity between two packets, or from any walk over a lineage" —
    and a directory name is none of those; it is the location the id occupies,
    read the two ways the estate's own archiver can have written it. Where
    ONE identity matches two directories that way, `proposal_path_at` refuses
    CANNOT RUN naming both, which is the ratified scenario *A declared
    identity resolves to two locations at one commit* and the reason this
    answers a BOOLEAN per row rather than picking a winner.
    """
    match = _ARCHIVE_DIR_RE.match(name)
    if match is not None and match.group("id") == identity:
        return True
    if name != identity:
        return False
    # THE EXACT READING YIELDS TO A LIVE PACKET OF THAT NAME, and only the
    # exact one does. `names_this_change` settles the ambiguous shape from the
    # ACTIVE ids and the reasoning holds in a static tree too: a change that
    # is LIVE has not been archived, so an archive directory spelled exactly
    # like a live id cannot be that packet's archive — it is the dated archive
    # of the stripped id. Reusing that helper wholesale went too far, because
    # its guard sat on the STRIPPED arm and suppressed a legitimate match:
    # with archived `foo` at `archive/2026-09-09-foo` and an unrelated live
    # `2026-09-09-foo`, `declared_former_ids_in_tree(root, "foo")` returned
    # `[]` although the archived packet declares a lineage. (Codex P2, PR
    # #1038 `PRRT_kwDOTAvnrs6iHS5E`.) The guard belongs on the EXACT arm,
    # where it prevents a lawful corpus reading as one identity in two places.
    #
    # `live_ids` IS EMPTY FOR A READ AT A REF, deliberately: which ids were
    # active at some commit is another tree read per commit, and admitting
    # both readings there is what the ratified ambiguity scenario expects —
    # `proposal_path_at` refuses when one identity then resolves twice.
    return name not in live_ids


def _tree_rows(root: Path, revision: str, path: str) -> list[str] | None:
    """`git ls-tree --name-only <revision> -- <path>`, or None when the read
    could not be performed.

    THE TREE ANSWERS PRESENCE, AND IT IS THE ONLY READ THAT SEPARATES THE TWO
    SILENCES. `design.md` M1 measured it on git 2.43.0 against a
    `--filter=blob:none --no-checkout` clone whose promisor remote was
    unreachable: for a path PRESENT at a commit whose blob is not locally
    available `ls-tree` prints the row and exits 0, and for a path GENUINELY
    ABSENT it prints nothing and exits 0 — while `git cat-file -e` and
    `git show` exit 128 for BOTH. So "there is nothing there" and "I cannot
    tell you" are the same value to the probes this estate's packet-at-a-ref
    lookups are built on, and a gate that reads the second as the first
    switches itself off exactly where it can prove nothing.

    A NON-ZERO EXIT IS RETURNED AS None AND NEVER AS AN EMPTY LIST, which is
    the distinction `sequenced_after._archive_dir_names_at_ref` collapses and
    which this packet's own requirement forbids reusing. EVERY CALLER NOW
    RAISES ON THAT None (`tasks.md` § 3.4): `_rows_or_refuse` is the one door
    this value leaves by, and it leaves as `origin-retention-read-unavailable`
    — CANNOT RUN, naming the read and the identity it was for. This function
    is unchanged by that slice, which was the point of landing the probe
    first: the fail-closed slice changed callers and not probes.
    """
    listed = subprocess.run(  # NOSONAR: argv is allowlisted; shell is disabled
        ["git", "-C", str(root.resolve()), "ls-tree", "--name-only",
         "--end-of-options", revision, "--", path],
        capture_output=True, text=True, check=False,
    )
    if listed.returncode != 0:
        return None
    return [row for row in listed.stdout.splitlines() if row.strip()]


_READ_UNAVAILABLE = "origin-retention-read-unavailable"


def _unreadable_read_refusal(identity: str, read: str, question: str, *,
                             at: str | None = None) -> OriginRetentionError:
    """The refusal EVERY read behind the baseline takes when it cannot be
    performed — CANNOT RUN, naming the read that failed and the identity it
    was for.

    ONE REFUSAL FOR EVERY SUCH READ, because a caller can act on exactly one
    thing: the baseline CANNOT BE ESTABLISHED from this checkout. Which read
    it was is in the message and never in the status, the way
    `OriginRetentionError`'s own docstring already says its four arms work.

    RETURNED RATHER THAN RAISED, so the `raise` stands at the call site and a
    reader of that site sees the control flow leave there rather than
    trusting a helper's name to mean "this never returns".
    """
    where = f"At commit {at[:12]}" if at else "Behind the baseline"
    return OriginRetentionError(
        f"REFUSE {_READ_UNAVAILABLE}: {identity}: the origin-retention walk "
        f"CANNOT RUN. {where} this checkout could not perform a read the "
        f"baseline rests on — `{read}` exited non-zero — so {question} "
        f"is a question it cannot answer. ABSENT AND UNREADABLE ARE THE "
        f"SAME SILENCE TO A PROBE AND NOT THE SAME FACT: reading this one "
        f"as the other would let the walk pass the commit by and take a "
        f"LATER baseline, or report {identity} as never ratified, over a "
        f"history it never read — a gate switching itself off exactly "
        f"where it can prove nothing, which is what this refusal exists to "
        f"stop. The measured shape is a `--filter=blob:none` or "
        f"`--filter=tree:0` partial clone whose promisor remote is "
        f"unreachable (`design.md` M1, git 2.43.0). Fetch the objects this "
        f"read needs (`git fetch --refetch`, or a full clone) and run the "
        f"gate again; there is no bypass flag.")


def _rows_or_refuse(root: Path, revision: str, path: str, *, identity: str,
                    question: str) -> list[str]:
    """`_tree_rows`, with its None raised rather than read as an empty tree.

    THE ONE DOOR THE None LEAVES BY. `_tree_rows` separates the two silences
    and returns them as `[]` and `None`; this is where the second stops being
    a value and becomes a refusal, so no caller has to remember which is
    which.
    """
    rows = _tree_rows(root, revision, path)
    if rows is None:
        raise _unreadable_read_refusal(
            identity, f"git ls-tree --name-only {revision[:12]} -- {path}",
            question, at=revision)
    return rows


def _text_at_a_present_path(root: Path, revision: str, rel: str, *,
                            identity: str) -> str:
    """The blob at a path THE TREE HAS ALREADY SAID STANDS at `revision`.

    So a None from `git_show_text` here is never "there is nothing there":
    the row was read off the tree one call ago, and the only remaining
    reading of the silence is that this checkout cannot produce what stands
    there. Raised, therefore, and never returned.
    """
    text = git_show_text(root, revision, rel)
    if text is None:
        raise _unreadable_read_refusal(
            identity, f"git show {revision[:12]}:{rel}",
            f"what `{rel}` declares at {revision[:12]}, where the tree says "
            f"it stands", at=revision)
    return text


def _text_at(root: Path, revision: str, rel: str, *,
             identity: str) -> str | None:
    """The blob at `rel`, None where the TREE SAYS IT IS GENUINELY ABSENT,
    and a refusal where the tree says it stands and the checkout cannot
    produce it.

    PRESENCE FIRST AND SEPARATELY, which is the whole of `design.md` M1: a
    path that is absent and a path whose blob is unavailable answer `git
    show` with the same exit 128, and only the tree tells them apart. The
    extra `ls-tree` is one subprocess per read and buys the distinction the
    requirement is about.
    """
    if not _rows_or_refuse(
            root, revision, rel, identity=identity,
            question=f"whether `{rel}` stands at {revision[:12]}"):
        return None
    return _text_at_a_present_path(root, revision, rel, identity=identity)


def identity_paths_at(root: Path, revision: str, identity: str, *,
                      archive_rows: list[str] | None = None) -> list[str]:
    """EVERY path `identity`'s `proposal.md` occupies at `revision` — the
    two-candidate rule this estate already resolves a packet by.

    THE RULE, NOT THE FUNCTION. `sequenced_after.proposal_path_at_ref` states
    the rule — the active location first, then a dated archive directory
    carrying the same id — and this reads it the same way, but it does NOT
    reuse that function's probes: `_blob_exists_at_ref` asks `git cat-file
    -e`, which exits non-zero for a missing blob and for an unreadable one
    alike, and `_archive_dir_names_at_ref` returns an empty list on ANY read
    failure. Reusing them would make an unreadable former identity read as
    ABSENT and let the walk take a later baseline, which is exactly what the
    requirement refuses: "An EXISTING probe that collapses the two SHALL NOT
    be reused for this read merely because it already resolves a packet by
    id."

    A LIST RATHER THAN A PATH, and for the reason this estate's own
    `archived_change_dirs` returns one: two locations for one id is an
    AMBIGUITY the resolver must be able to REPORT, not a collision to settle
    by taking the first sorted one. `proposal_path_at` refuses CANNOT RUN
    over a list longer than one.

    `archive_rows` is the archive listing at this revision when the caller
    already read it — a walk asks about several identities at one commit, and
    the listing is the same for all of them. It is a LIST or absent; a caller
    that read it and could not is expected to have refused already, which is
    what `_rows_or_refuse` makes unavoidable.

    AND EVERY ONE OF THESE READS FAILS CLOSED (`tasks.md` § 3.4). Three reads
    resolve an identity here — the active probe, the archive listing, and the
    archived probe — and each of them answers "nothing is there" and "I
    cannot tell you" with the same shape unless the None is raised. An
    unreadable ARCHIVE LISTING is the quietest of the three: an identity that
    stands only in the archive then resolves to nothing at all, and the walk
    passes its ratification by without ever reporting that it could not look.
    """
    found: list[str] = []
    active = f"openspec/changes/{identity}/proposal.md"
    if _rows_or_refuse(root, revision, active, identity=identity,
                       question=f"whether {identity} stands at its active "
                                f"location at {revision[:12]}"):
        found.append(active)
    if archive_rows is None:
        archive_rows = _rows_or_refuse(
            root, revision, _ARCHIVE_ROOT, identity=identity,
            question=f"what stands in the archive at {revision[:12]}, and "
                     f"so whether {identity} stands there")
    for row in archive_rows:
        name = row.rstrip("/").rsplit("/", 1)[-1]
        if not _archive_dir_carries(name, identity):
            continue
        archived = f"{_ARCHIVE_ROOT}{name}/proposal.md"
        if _rows_or_refuse(root, revision, archived, identity=identity,
                           question=f"whether {identity} stands at "
                                    f"`{archived}` at {revision[:12]}"):
            found.append(archived)
    return found


def proposal_path_at(root: Path, revision: str, identity: str, *,
                     archive_rows: list[str] | None = None) -> str | None:
    """The ONE path `identity` occupies at `revision`, or None when it
    occupies none. Refuses CANNOT RUN where it would occupy more than one."""
    found = identity_paths_at(root, revision, identity,
                              archive_rows=archive_rows)
    if len(found) > 1:
        raise OriginRetentionError(
            f"REFUSE origin-retention-identity-ambiguous: {identity}: the "
            f"origin-retention walk CANNOT RUN. At commit {revision[:12]} "
            f"this identity resolves to MORE THAN ONE location — "
            + ", ".join(f"`{path}`" for path in found) +
            " — and a baseline chosen from a set is a baseline chosen by the "
            "resolver rather than by an author. Two locations for one id is "
            "an AMBIGUITY to report and not a collision to settle by "
            "preferring one: resolve the duplicate before archiving.")
    return found[0] if found else None


def packet_yaml_of(proposal_rel: str) -> str:
    """The `.openspec.yaml` beside a packet's `proposal.md`."""
    return proposal_rel.rsplit("/", 1)[0] + "/.openspec.yaml"


def packet_yaml_at(root: Path, revision: str,
                   identities: list[str]) -> str | None:
    """The first of `identities` standing at `revision`, as its
    `.openspec.yaml` path. Callers pass the identities in the order they want
    them preferred — the CURRENT id first for a read about the packet as it
    is now, the resolved baseline identity for a read about the ratification.
    """
    for identity in identities:
        resolved = proposal_path_at(root, revision, identity)
        if resolved is not None:
            return packet_yaml_of(resolved)
    return None


def _identity_pathspecs(identity: str) -> list[str]:
    """The pathspecs that enumerate every commit that touched `identity`'s
    proposal, at either of the two locations an id can occupy.

    `:(glob)` MAGIC IS LOAD-BEARING: without it `*` matches `/` as well, so
    the archive pattern would reach every depth below `archive/`. With it the
    wildcard is confined to ONE path component, which is what a dated archive
    directory is. The pattern is deliberately WIDER than the convention — it
    matches `<anything>-<identity>`, so a neighbour whose name merely ends
    that way is enumerated too — because this selects COMMITS TO VISIT and
    nothing else: every path is re-resolved against the convention by
    `identity_paths_at` before it is read, and over-enumeration costs a read
    while under-enumeration would cost the baseline.

    AND THE EXACT ARCHIVE PATH IS ITS OWN PATHSPEC, because the glob cannot
    reach it. `archive_directory_name` archives an id that already carries a
    `YYYY-MM-DD-` prefix UNDER THAT NAME UNCHANGED, and `*-<identity>` does
    not match `<identity>`: without this third spec `ratifying_baseline`
    enumerated NO commit for such a packet and reported it as never ratified,
    while `identity_paths_at` resolved it perfectly well — the two halves of
    one resolution disagreeing about where an id can stand. (Copilot, PR
    #1038 `PRRT_kwDOTAvnrs6iG9tt`.)
    """
    return [f"openspec/changes/{identity}/proposal.md",
            f"{_ARCHIVE_ROOT}{identity}/proposal.md",
            f":(glob){_ARCHIVE_ROOT}*-{identity}/proposal.md"]


def _change_ids_of_proposal_path(rel: str) -> list[str]:
    """EVERY change id a `openspec/changes/…/proposal.md` path can address.

    A LIST, for the archived half's genuine ambiguity that
    `_archive_dir_carries` states: `archive/2026-09-09-foo` addresses `foo`
    and addresses `2026-09-09-foo`, and a reader that returned only the first
    could not recognise a packet that DECLARES the second as a former id —
    the declared move would then take the undeclared move's refusal. The
    exact directory name comes FIRST, so `_first_change_id_of_proposal_path`
    names the packet as its directory spells it.

    An ACTIVE path addresses exactly one id: its second segment, verbatim.
    """
    parts = rel.split("/")
    if len(parts) < 4 or parts[0] != "openspec" or parts[1] != "changes":
        return []
    if parts[2] == "archive":
        if len(parts) < 5:
            return []
        found = [parts[3]]
        match = _ARCHIVE_DIR_RE.match(parts[3])
        if match and match.group("id") not in found:
            found.append(match.group("id"))
        return found
    return [parts[2]]


def _first_change_id_of_proposal_path(rel: str) -> str | None:
    """The id a proposal path addresses, for the callers that want one
    string — the directory's own name, before any date-prefix reading."""
    found = _change_ids_of_proposal_path(rel)
    return found[0] if found else None


def declared_former_ids_in_tree(root: Path, change: str) -> list[str]:
    """The lineage `change` declares in the WORKING TREE, active or archived
    — `[]` when the packet is not there to ask.

    THE ARCHIVED CANDIDATE IS CHOSEN BY `names_this_change`, the reading this
    file already settled for the archive wrapper (and the ambiguity
    `archive_directory_name` creates): the exact directory name counts, the
    dated one counts, and an active change id of that exact name takes the
    directory out of the running. Asked through `change_id_of` alone, an
    archived packet under a PRESERVED date-prefixed id — `archive/2026-09-10-
    bar/` for the change `2026-09-10-bar` — matched no candidate, so its
    declared lineage came back EMPTY and `ratifying_baseline` was handed the
    UNDECLARED answer for a packet that declares. That is the shed-lineage
    failure this mechanism exists to stop, arriving through the reader.

    AND TWO CANDIDATES HOLDING A PACKET REFUSE RATHER THAN PREFERRING ONE.
    Where the identity stands BOTH actively and in the archive, the two
    `.openspec.yaml` files may declare different lineages, and returning the
    first was the whole of the choice — a lineage chosen by this reader's
    ordering rather than by an author, which is what `proposal_path_at`
    already refuses one layer down. MEASURED before it was changed: with
    `openspec/changes/change-x/` declaring `[from-the-active-copy]` and
    `openspec/changes/archive/2026-09-09-change-x/` declaring
    `[from-the-archived-copy]`, this returned the first silently. The walk
    that consumes it happened to refuse afterwards, because both locations
    also stand at the commit it visits first — but that is the COMMITTED tree
    agreeing with the working one, which is not a thing a reader of the
    WORKING tree may assume. (Copilot, PR #1037 `PRRT_kwDOTAvnrs6iGr_s`.)

    EVERY DIRECTORY IS CONTAINMENT-CHECKED, the same surface
    `former_identity_claimants` closes: a committed
    `openspec/changes/archive` symlink made this return an outside packet's
    declaration as this corpus's lineage.
    """
    changes = root / "openspec" / "changes"
    candidates = [changes / change]
    archive = changes / "archive"
    if contained_dir(root, archive):
        live_ids = contained_change_dir_names(root)
        candidates += [d for d in sorted(archive.iterdir())
                       if contained_dir(root, d)
                       and _archive_dir_carries(d.name, change,
                                                live_ids=live_ids)]
    holding = [d for d in candidates
               if contained_dir(root, d)
               and contained_file(root, d / ".openspec.yaml")]
    if len(holding) > 1:
        raise OriginRetentionError(
            f"REFUSE origin-retention-identity-ambiguous: {change}: the "
            f"origin-retention walk CANNOT RUN. In the tree being read this "
            f"identity holds a packet at MORE THAN ONE location — "
            + ", ".join(f"`{_corpus_rel(d)}`" for d in holding) +
            " — and each of them may declare a DIFFERENT `former_ids:`, so "
            "the lineage the walk resolves would be chosen by whichever this "
            "reader looked at first. A lineage chosen by the reader is the "
            "defect this mechanism exists to stop, on the same ground "
            "`proposal_path_at` refuses two locations at a commit: two "
            "places for one id is an AMBIGUITY to report, not a collision "
            "to settle by preferring one. Resolve the duplicate — an "
            "archived packet whose active directory was left standing is "
            "the usual cause — and run the gate again.")
    return declared_former_ids_of(holding[0], change) if holding else []


def ratifying_baseline(root: Path, change: str, *,
                       former_ids: list[str] | None = None
                       ) -> tuple[str, str, str] | None:
    """The baseline the archive gate compares against, resolved ACROSS THE
    DECLARED IDENTITIES: `(commit, identity, that identity's proposal path at
    that commit)`, or None when no identity of this packet has ever declared
    `Status: ratified`.

    THE DECLARATION PRESENT AT RATIFICATION IS FOUND UNDER THE IDENTITY THE
    PACKET WAS RATIFIED UNDER, WHICH IS NOT ALWAYS THE IDENTITY IT CARRIES
    NOW. Where the packet declares a former identity, the current id and every
    declared former id are resolved TOGETHER and the EARLIEST commit at which
    any of them declares `Status: ratified` is the baseline. Earliest is the
    whole of it: the failure this exists to catch is a baseline LATER than the
    real ratification, which waves through every mutation made in between, so
    a resolution that could return a later commit than some identity of the
    same packet offers would reintroduce the defect by another route.

    ONE WALK, TOPOLOGICALLY ORDERED ACROSS EVERY IDENTITY, rather than one
    walk per identity and a comparison afterwards. Comparing two commits found
    on two separate walks needs an ordering `git log` has already computed:
    `--topo-order --reverse` over the UNION of the identities' pathspecs
    visits parents before children across all of them, so the first ratified
    blob this single walk finds IS the earliest — and no commit DATES, which
    run backwards through a rebase, are ever compared.

    THE RESOLUTION IS BY IDENTITY AND NEVER BY HISTORY. Each identity is
    resolved to the path it occupies AT THE COMMIT BEING READ, by the rule
    `identity_paths_at` states, and no rename detection, similarity score or
    lineage walk decides which identity belongs to this packet — the
    DECLARATION does. An identity the packet has not declared is not an
    identity of that packet, whatever history suggests.

    AND EVERY READ BEHIND THIS BASELINE FAILS CLOSED (`tasks.md` § 3.4).
    The commit enumeration, the archive listing at each visited commit, each
    identity's presence probe, each blob this walk reads, and BOTH READS THE
    UNDECLARED-MOVE PROBE TAKES at each visited commit — the rename pairing
    and the source packet's header at that commit's parent — are six reads
    that a partial checkout answers with a silence indistinguishable from
    "nothing is there". None of them is read that way: presence comes off the
    TREE (`_rows_or_refuse`), content is read separately and only where the
    tree already said the path stands (`_text_at_a_present_path`), and a read
    that could not be performed raises `origin-retention-read-unavailable` —
    CANNOT RUN, naming the read and the identity it was for. An unreadable
    history is never reported as an unratified one, and no baseline is ever
    established from the reads that happened to succeed.

    AND THE UNDECLARED REFUSAL STAYS EXACTLY WHERE IT WAS (issue #833, PR
    #846). A packet that declares nothing gets today's behaviour: one identity
    is walked, and a commit that carries the current path in from a path
    already declaring `Status: ratified` refuses CANNOT RUN rather than
    re-basing onto the move. What a DECLARATION changes is that the refusal no
    longer fires for the move the packet DECLARED — that move has a lawful
    answer now, and the answer is the earlier identity's own ratification.
    """
    if not CHANGE_ID_RE.fullmatch(change):
        raise SupportError(f"invalid change name: {change}")
    # None MEANS "READ THE PACKET", AND `[]` MEANS "DECLARES NOTHING", which
    # are different questions and must not answer the same way: a caller that
    # forgot to pass the lineage would otherwise get the UNDECLARED answer
    # silently, which is the defect this whole mechanism is about.
    if former_ids is None:
        former_ids = declared_former_ids_in_tree(root, change)
    declared = list(former_ids)
    identities = declared + [change]
    pathspecs: list[str] = []
    for identity in identities:
        for spec in _identity_pathspecs(identity):
            if spec not in pathspecs:
                pathspecs.append(spec)
    listed = subprocess.run(  # NOSONAR: argv is allowlisted; shell is disabled
        ["git", "-C", str(root.resolve()), "log", "--full-history",
         "--topo-order", "--reverse", "--format=%H", "--", *pathspecs],
        capture_output=True, text=True, check=False,
    )
    if listed.returncode != 0:
        # AN ENUMERATION THAT FAILED IS NOT AN EMPTY HISTORY. Returning None
        # here reported "no commit in history carries `Status: ratified`" —
        # the packet as NEVER RATIFIED — for a checkout that could not read
        # the commits at all, which is the exact sentence the requirement
        # forbids: "SHALL NOT report an unreadable history as an unratified
        # one".
        raise _unreadable_read_refusal(
            change,
            "git log --full-history --topo-order --reverse -- "
            + " ".join(pathspecs),
            f"which commits ever touched this packet, under {change} or "
            f"under any identity it declares "
            f"({', '.join(declared) or 'none'})")
    rel = f"openspec/changes/{change}/proposal.md"
    for revision in listed.stdout.split():
        archive_rows = _rows_or_refuse(
            root, revision, _ARCHIVE_ROOT, identity=change,
            question=f"what stands in the archive at {revision[:12]}, and "
                     f"so where each identity of this packet stands there")
        ratified: dict[str, str] = {}
        for identity in identities:
            resolved = proposal_path_at(root, revision, identity,
                                        archive_rows=archive_rows)
            if resolved is None:
                continue
            # THE TREE HAS ALREADY SAID THIS PATH STANDS HERE, so a silent
            # blob is UNREADABLE and not "declares no ratification". Read
            # flat, this commit is skipped and the walk takes a LATER
            # baseline — the #833 failure reached through a partial clone
            # rather than through a rename.
            if declares_ratified(_text_at_a_present_path(
                    root, revision, resolved, identity=identity)):
                ratified.setdefault(identity, resolved)
        # THE REFUSAL IS ASKED BEFORE THE ANSWER IS TAKEN, exactly as it was
        # before this slice: a commit that is a MOVE of an already-ratified
        # packet refuses rather than becoming the baseline, whatever its own
        # blob says.
        _refuse_an_undeclared_move(root, revision, rel, change, declared,
                                   change in ratified)
        for identity in identities:
            if identity in ratified:
                return revision, identity, ratified[identity]
    return None


def _refuse_an_undeclared_move(root: Path, revision: str, rel: str,
                               change: str, declared: list[str],
                               ratified_here: bool) -> None:
    """PR #846's refusal, unchanged for a packet that declares nothing, and
    silent for the move that packet DECLARED.

    The pairing is read exactly as before — `kinds="RC"` where the visited
    commit's own blob declares `ratified` (a move or copy that lands already
    ratified) and `kinds="R"` where it does not (a plain rename, the former
    path gone, that lands short of ratified; issue #849). What is new is one
    test on the answer: where the paired predecessor's change id is one this
    packet DECLARES, the move is the lawful one this mechanism exists to
    admit, and the walk goes on to find that identity's own ratification.
    Where it is not, the refusal is the one PR #846 wrote, to the sentence.

    AND A PROBE THAT CANNOT BE PERFORMED IS NOT A PACKET THAT DID NOT MOVE.
    `ratified_under_a_former_path` now refuses `origin-retention-read-
    unavailable` for either of its two reads rather than answering None, so
    this function is SILENT only where the reads succeeded and said "no
    move". That is the whole of the difference: the refusal below fires on a
    move it could see, and CANNOT RUN fires on a move it could not look for.
    """
    former = ratified_under_a_former_path(
        root, revision, rel, kinds="RC" if ratified_here else "R",
        identity=change)
    if former is None:
        return
    if any(identity in declared
           for identity in _change_ids_of_proposal_path(former)):
        return
    short = revision[:12]
    declared_note = (
        f"This packet DECLARES {declared!r} in `former_ids:` and `{former}` "
        f"is not among them"
        if declared else
        "This packet declares no FORMER ID")
    raise OriginRetentionError(
        f"REFUSE origin-retention-path-moved: {change}: the "
        f"origin-retention walk CANNOT RUN. Commit {short} carries "
        f"`{rel}` in from `{former}`, which already declared "
        f"`Status: ratified` at {short}^ — so this change was "
        f"ratified under a path that is not the one it occupies now "
        f"(`{rel}`), and {short} is a MOVE OR COPY of that ratified "
        f"packet rather than its ratification, whatever `{rel}` "
        f"itself declares as of {short} — and if `{former}` still "
        f"stands in the tree then the packet was COPIED to this id "
        f"rather than moved to it, which git pairs the same way and "
        f"which leaves the same baseline unestablishable. Taking "
        f"{short} or any later commit under `{rel}` as the baseline "
        f"would compare the packet against itself and wave through "
        f"every origin mutation made between the real ratification "
        f"and it — the `ORIGIN RETAINED` measured on issue #777, "
        f"the failure issue #833 names, and the same failure "
        f"reached through an un-ratifying rename (issue #849). "
        f"{declared_note}, so the "
        f"baseline cannot be established from history alone and "
        f"this walk refuses rather than re-basing onto that "
        f"commit: archive {change} under the id it was ratified "
        f"with, or declare the source id in this packet's "
        f"`former_ids:` in the commit that performs the move. "
        f"Renaming a DRAFT change is unaffected.")


def ratifying_commit(root: Path, change: str, *,
                     former_ids: list[str] | None = None) -> str | None:
    """The FIRST commit at which THIS PACKET — under `change` or under any
    identity it declares in `former_ids:` — declares `Status: ratified`, or
    None when no commit in history does.

    A THIN WRAPPER SINCE `add-declared-former-id`: the resolution itself is
    `ratifying_baseline`, which returns the identity and the path beside the
    commit because the declaration at that commit is read under the identity
    the packet was RATIFIED under, not under the one it carries now. This
    function keeps its name and its one return value for the callers that only
    ever wanted the commit. `former_ids` defaults to the lineage the packet
    declares IN THE WORKING TREE, so a caller that has already read the packet
    passes it and a caller that has not gets the same answer.

    A line-by-line walk over the commits that touched EVERY PATH EVERY
    DECLARED IDENTITY CAN OCCUPY — the active location, the exact archive
    directory, and a dated archive directory carrying the id, for the current
    id and for each entry of `former_ids:` — oldest first, reading each blob — not `git log -S`, which would match the string
    inside a fenced example and inside a `- Status: ratified` bullet alike, and
    not `git log -G`, which has the same problem. The walk is bounded by the
    number of commits that touched a single file (a handful, for a change
    packet), and every candidate is read through `declares_ratified` so the
    resolver and the lifecycle reader cannot disagree about what a header says.

    `--full-history --topo-order --reverse` rather than a plain `--reverse`,
    because MISSING the earliest ratified blob is the failure that matters:
    the walk would then take a LATER commit as the baseline and wave through
    every mutation made between the real ratification and it. History
    simplification can prune the commit that changed the file on a merged
    branch, and commit DATES can run backwards through a rebase, so the
    ordering is taken from topology (parents before children) rather than from
    the clock.

    THE PATH IS RE-RESOLVED AT EVERY COMMIT VISITED, by `identity_paths_at`'s
    rule, so an archived packet is read where it stood at the commit being
    read rather than where it stands now — the active location before its
    archive move, the archive directory after. An earlier draft of this
    paragraph said "the path read is the ACTIVE one even when the packet being
    gated is an archived one", which was true of the single-path walk this
    docstring described before `add-declared-former-id` and is not true of
    `ratifying_baseline`. (Copilot, PR #1038 `PRRT_kwDOTAvnrs6iG9wN`.)

    AND WHEN THE PACKET'S OWN NAME MOVED AND IT DECLARED NOTHING, THIS
    REFUSES (issue #833). Where the packet declares no former identity ONE
    identity is walked, so a ratified change whose directory was RENAMED
    afterwards has no history under its new name before the rename — and the first ratified
    blob the walk finds is then the RENAME COMMIT, which is precisely "a LATER
    commit as the baseline" named above. Measured on issue #777: a ratified
    change renamed on a trial branch reported `ORIGIN RETAINED` against a
    baseline four days later than its ratification, so every mutation in
    between was waved through, while the two sibling `--archive-gate` arms
    (`validate-sequenced-after.py`, `validate-scope-globs.py`) refused loudly
    on the same tree because they resolve BY ID at a ref and say so when the
    id has no proposal there. This walk now says so too:
    `ratified_under_a_former_path` asks whether the candidate is a FLIP or a
    MOVE, and a move raises `OriginRetentionError` — CANNOT RUN, exit 2 — with
    the change, both paths and the commit named. It never re-bases silently,
    and where the packet declares nothing there is nothing to re-base ONTO, so
    a baseline under a name the tree no longer spells cannot be established at
    all. WHAT A DECLARATION CHANGES is that the move the packet DECLARED has a
    lawful answer: the identities are resolved together, the EARLIEST
    ratification any of them offers is the baseline, and the refusal below
    fires only for a move that is not among them.

    EVERY COMMIT VISITED IS ASKED, NOT ONLY THE ONE THAT DECLARES `ratified`
    (issue #849). Asking `ratified_under_a_former_path` only where
    `declares_ratified` already held true a commit that renames an
    already-ratified packet AND un-ratifies it in the same breath: that
    commit is not itself ratified, so it was never put to the question, and a
    LATER commit re-ratifying the (unmoved, from here on) path carries no
    rename pairing of its own — the walk took THAT as the baseline instead,
    later than the real ratification, exactly the failure named above by a
    longer route. So every visited commit is asked, whether or not its own
    blob declares `ratified` — with `kinds="RC"` where it does (unchanged:
    a move or copy that lands already ratified refuses, as before) and
    `kinds="R"` where it does not (new: a plain rename — the former path
    gone — that lands short of ratified still refuses, so an un-ratifying
    rename can no longer hide behind a later, pairing-free re-ratification).
    A COPY that lands short of ratified is deliberately NOT asked this way —
    see `ratified_under_a_former_path`'s own "RESTRICTED TO RENAMES" — so a
    packet honestly authored as a draft copy of a ratified one stays
    archivable.

    AND WHEN THE UN-RATIFYING HOP AND THE HOP THAT LANDS THE CURRENT NAME ARE
    TWO DIFFERENT COMMITS, THIS DOES NOT REFUSE — A DELIBERATE, OPEN GAP
    (issue #1003). The `git log` above is bounded to the ONE path this call
    was given — the change's CURRENT id — so it visits every commit that
    ever touched that literal path, starting at the commit that renamed the
    packet INTO its present name; nothing that only ever touched an EARLIER
    name is in that list at all. Ratify r, then rename r to s and un-ratify
    in the SAME commit, then — in a SEPARATE, later commit — rename s to t
    while still a draft, then ratify t: the walk for `t` visits only the
    s-to-t rename and the ratification that follows it. At the s-to-t
    rename, `ratified_under_a_former_path` reads the parent it actually
    has — the r-to-s commit's OWN result, already a draft, because that
    commit did its own un-ratifying — and finds nothing amiss; the commit
    that carried the true ratified-to-draft flip is never visited, because
    it never touched `t`. The baseline the walk returns is the LATER
    re-ratification, and everything mutated since the real first
    ratification is waved through — the #833 failure, reached by a second
    rename hop instead of one. THAT IS STILL THIS WALK'S ANSWER FOR AN
    UNDECLARED CHAIN, pinned by
    `test_an_undeclared_rename_chain_is_the_landing_validators_to_refuse`,
    which records it as what it is: no refusal, and not this gate's to take.

    CLOSED BY A DECLARATION AND NOT BY A LONGER WALK, WHICH IS WHY THE
    PARAGRAPH ABOVE STILL DESCRIBES AN UNDECLARED CHAIN. Chasing the packet's
    full rename lineage — following former paths back across every hop rather
    than only the one hop a candidate commit itself pairs — is the shape the
    ruling on this issue declines (Brett Heap, 2026-09-13): "history-walking
    archaeology that cannot carry the intent bit distinguishing
    rename-of-ratified from lawful fork-by-copy". `add-declared-former-id`
    closes it from the other side. A packet that DECLARES the chain resolves
    its baseline across every declared identity and takes the EARLIEST
    ratification of any of them, so the chain above, declared, is baselined at
    `change-r`'s own ratification and the mutation between is caught; and a
    chain that declares NOTHING is refused at the landing of its first hop by
    the house validator this packet's § 4 builds, one commit at a time, so no
    lineage ever needs walking. What this WALK does not do — deliberately — is
    reach an UNDECLARED multi-hop chain that is already in history: nothing
    connects `change-t` to `change-r` there, which is the whole argument for a
    declaration.
    """
    baseline = ratifying_baseline(root, change, former_ids=former_ids)
    return baseline[0] if baseline is not None else None


def origin_block_lines(yaml_text: str | None) -> list[str] | None:
    """The `origin:` mapping's own lines, verbatim but for trailing whitespace.

    TEXT, not the parsed mapping, because the requirement is about the
    DECLARATION and not only about the values a parser happens to keep: the
    #685 mutation moved prose inside a folded scalar, which a key-by-key
    comparison of scalars still sees (the folded value changes) but which a
    reader deserves to see as the lines it is. Trailing whitespace is
    normalized away and nothing else is — an origin block that was reflowed,
    re-indented, or re-quoted after ratification is a changed declaration.
    """
    if yaml_text is None:
        return None
    rows = _split_keepends(yaml_text)
    collected: list[str] = []
    inside = False
    for body, _ending in rows:
        if not inside:
            if re.match(r"^origin\s*:", body):
                inside = True
                collected.append(body.rstrip())
            continue
        if not body.strip():
            collected.append("")
            continue
        if body[:1] in (" ", "\t"):
            collected.append(body.rstrip())
            continue
        break
    while collected and not collected[-1]:
        collected.pop()
    return collected or None


def _origin_mapping(yaml_text: str | None) -> dict | None:
    """The `origin:` mapping as data, or None when it is absent/unparseable."""
    if yaml_text is None:
        return None
    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    origin = data.get("origin")
    return origin if isinstance(origin, dict) else None


def _changed_keys(was: dict | None, now: dict | None) -> list[str]:
    """The origin keys a mutation touched — added, removed, or re-valued.

    Advisory, and only ever an ADDITION to the line diff below it: a block
    whose lines moved while every scalar stayed equal (a re-indent, a re-quote)
    names no keys and is still refused, which is the intended order of
    authority between the text and the parse.
    """
    if was is None or now is None:
        return []
    return sorted(key for key in set(was) | set(now)
                  if was.get(key) != now.get(key))


# --------------------------------------------------------------------------
# THE EXPLICIT DISPOSITION THE REQUIREMENT ALREADY PROMISES (issue #745)
#
# THE REQUIREMENT'S OWN SCENARIO ENDS "restoring or accepting the mutation is
# a contested-class act requiring an explicit disposition", and until this
# block existed the gate could read the RESTORING half and nothing else: an
# owner's ACCEPTED mutation and an unnoticed one produced the identical
# refusal, so an acceptance was recordable as governance and unrepresentable
# as a tree state. Measured rather than argued — codeXfactory/codexFactory
# #318 recorded Brett Heap's "accept the mutation, this lane re-runs the
# archives" over `add-floor-regeneration-automation` (ratifying commit
# ec286270b10f; mutating commit 76758a1b, `changed keys: approved_by`, the
# tense of one sentence rewritten fourteen minutes later in the SAME pull
# request) and the re-run refused byte-identically.
#
# STILL NO BYPASS FLAG, AND THAT IS WHY THE CHANNEL IS A RECORD. This module's
# own reason for refusing a flag — "a flag on this gate would be the
# disposition nobody records" — is an argument against UNRECORDED acceptance,
# not against acceptance. A record is the disposition somebody records: it is
# committed, it is in the diff a reviewer reads, it names the authority, the
# date and the verbatim word, and every fact in it is re-measurable by anyone
# against the same history this gate reads. The subcommand grows no flag and
# `test_the_archive_subcommand_offers_no_bypass_flag` stays true.
#
# AN ACCEPTANCE MOVES THE BASELINE; IT DOES NOT SKIP THE COMPARISON. That is
# the whole of the mechanism and the reason it cannot decay into a bypass. On
# a valid `accept` the declaration AT THE ACCEPTED MUTATION becomes the origin
# of record, and every arm of this gate then runs against IT: the working
# tree's block must equal it EXACTLY, and the support manifest's repeated
# origin fields are compared to it rather than to the ratification (the
# accepted declaration is the one the manifest must now agree with — comparing
# to the superseded one would refuse a manifest that is correct). A second,
# undispositioned edit on top of an accepted one therefore refuses exactly as
# the first one did, and a record that accepts a commit the tree does not
# carry accepts nothing.
#
# THE SHAPE IS THE ESTATE'S EXISTING ONE, deliberately, so the corpus has ONE
# idea of a disposition. Three records already carry it and this is the
# fourth: `tests/sequenced_after/archive-date-dispositions.yaml` (a
# `schema_version` + `kind` header over a `dispositions:` list, FULL 40-hex
# object names because "this is a citation, and an abbreviation is ambiguous
# by construction", a `fact`, a `ruled_by` and a `cited_to`);
# `contracts/openspec-cli-pin.yaml`'s own `dispositions:` list, whose rule is
# the one this gate follows most closely — "Each entry ACCEPTS exactly one
# ERROR-level finding … matched on the tuple … compared WHOLE", with
# `cited_to:` REQUIRED and non-empty and an authority named, refusing
# `pin-disposition-malformed` when either is missing or when two entries would
# cover the same finding; and `health/dispositions.yaml`, whose `cite` is what
# lets doc-health's own `contested` findings — including the nightly
# `proposal-origin` family's post-ratification-mutation class, the very same
# fact seen from the report side — be answered at all.
#
# TWO DEPARTURES, both stated rather than silent. (1) The siblings' single
# `ruled_by` / `ratified_by` string is split here into `disposed_by`,
# `disposed_on` and `word`, because this is the first of the four to CHECK
# that a disposition is dated and quoted rather than only to print it. (2)
# `cited_to` rather than `recorded_at`: every other `_at` key in an entry here
# names a COMMIT, and the estate already has one spelling for "where the
# ruling is recorded". `cited_to` takes a string or a LIST of them, as the pin
# manifest's does, and its CONTENT is not pattern-matched — the sibling
# records cite issues, pull requests, spec lines and council rulings, and a
# gate that demanded a URL would refuse three of those four.
#
# READ FROM THE ROOT THE GATE WAS GIVEN, which is what makes it work in a
# CONSUMER: `proposal-support.py <consumer-root> archive <id>` runs this
# repository's script against somebody else's tree, so the record is
# `<consumer-root>/openspec/origin-dispositions.yaml` — beside the
# `openspec/changes/` it disposes — and openxFactory's own archives read
# openxFactory's own file at that same relative path. A consumer needs no
# change beyond writing the record.
#
# NO STALENESS ARM, AND THIS IS THE ONE PLACE THE SIBLINGS ARE NOT COPIED.
# Both of them refuse a stale entry — `archive-date-dispositions.yaml` reports
# one whose directory now agrees, the pin manifest refuses
# `pin-disposition-stale` "so an exception cannot outlive its condition" — and
# both are right, because THEIR conditions are transient: a directory can be
# re-measured on every run and a pin's findings are re-derived at every bump.
# AN ORIGIN DISPOSITION IS NOT TRANSIENT. Its subject archives, and the
# archived packet then carries, permanently, an origin that differs from the
# one at its ratifying commit; the entry is the only thing in the tree that
# says WHY, on whose word. A staleness rule would demand the deletion of that
# explanation on the day it starts mattering most — the day the packet lands
# in `openspec/changes/archive/` and nobody can ask the author any more. So
# entries are kept, and the honest cost is stated: an entry whose mutation was
# afterwards RESTORED in the bytes silences nothing (the gate never reads the
# record on a tree it is about to pass) and is not reported either.
#
# THE OTHER TWO PLACES THIS DELIBERATELY DOES NOT LOOK. The file is consulted
# ONLY when a mutation has already been found, so a malformed record sits
# unread until somebody needs it — at which point the refusal names the
# malformation instead of reporting "no record". And entries naming OTHER
# change ids are never validated, so one change's bad entry cannot block
# another change's archive. Neither is a corpus-wide audit of the record;
# auditing it is a doc-health family's job and not an archive gate's.
# --------------------------------------------------------------------------

#: The disposition record, RELATIVE TO THE ROOT THE GATE WAS GIVEN.
ORIGIN_DISPOSITIONS_REL = "openspec/origin-dispositions.yaml"
ORIGIN_DISPOSITIONS_SCHEMA_VERSION = 1
ORIGIN_DISPOSITIONS_KIND = "origin_dispositions"

#: Every key an entry MUST carry. An entry missing the commit it accepts, the
#: keys that moved, the authority, the date, the word or the citation is a
#: change id on a list: it would silence a finding and record nothing.
ORIGIN_DISPOSITION_KEYS = (
    "change_id", "ratified_at", "mutation_at", "changed_keys", "disposition",
    "disposed_by", "disposed_on", "word", "cited_to")

#: `fact` is the free-prose judgement the measurement could not make — the same
#: key and the same purpose as in `archive-date-dispositions.yaml`. OPTIONAL,
#: and never read by this gate; it is listed so that writing it is not an
#: unknown-key refusal.
ORIGIN_DISPOSITION_OPTIONAL_KEYS = ("fact",)

#: THE ONLY DISPOSITION THAT NEEDS A RECORD. A RESTORATION is the bytes: put
#: the ratified declaration back and this gate passes with nothing to read.
ORIGIN_DISPOSITION_ACCEPT = "accept"

#: A FULL object name, never an abbreviation — the rule
#: `archive-date-dispositions.yaml` states and for the same reason.
_FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def origin_dispositions_path(root: Path) -> Path:
    """`<root>/openspec/origin-dispositions.yaml` — the consumer's record."""
    return root.resolve().joinpath(*ORIGIN_DISPOSITIONS_REL.split("/"))


class AcceptedOriginMutation:
    """A VALIDATED `accept` entry: the declaration this gate now compares
    against, and the record that authorized the move."""

    def __init__(self, entry: dict) -> None:
        self.change_id = entry["change_id"]
        self.ratified_at = entry["ratified_at"]
        self.mutation_at = entry["mutation_at"]
        self.changed_keys = list(entry["changed_keys"])
        self.disposed_by = entry["disposed_by"]
        self.disposed_on = entry["disposed_on"]
        self.word = entry["word"]
        self.cited_to = entry["cited_to"]

    def citation(self) -> str:
        """`cited_to` as ONE readable string.

        It may be a LIST — the shape `contracts/openspec-cli-pin.yaml`'s own
        `cited_to:` takes, and the shape an entry citing an issue, a pull
        request and a ruling naturally wants. Interpolating a list into
        operator output prints a Python repr, brackets and quotes and all
        (Copilot, round 1 on PR #891), so it is joined here rather than at
        four call sites.
        """
        if isinstance(self.cited_to, list):
            return "; ".join(self.cited_to)
        return self.cited_to

    def note(self) -> str:
        """The acceptance, ANNOUNCED. An accepted mutation is never silent:
        the run says which declaration became the origin of record, on whose
        word, and where that word is written down."""
        keys = (", ".join(f"`{key}`" for key in self.changed_keys)
                or "no scalar key at all — the block's LINES alone")
        return (
            f"ORIGIN DISPOSITION ACCEPTED {self.change_id}: the declaration "
            f"at {self.mutation_at[:12]} is the ORIGIN OF RECORD — a "
            f"post-ratification mutation of {keys}, accepted by "
            f"{self.disposed_by} on {self.disposed_on} "
            f"(\"{self.word}\"), recorded at {self.citation()}. The comparison "
            f"baseline moves from the ratifying commit "
            f"{self.ratified_at[:12]} to {self.mutation_at[:12]}; every arm "
            f"of this gate still runs, now against that declaration.")


def _commit_exists(root: Path, revision: str) -> bool:
    # argv is allowlisted and `shell` is disabled; the bare marker below is
    # the syntax the analyser actually reads (Sonar S7632, PR #891).
    result = subprocess.run(  # NOSONAR
        ["git", "-C", str(root.resolve()), "rev-parse", "--verify",
         "--end-of-options", f"{revision}^{{commit}}"],
        capture_output=True, check=False)
    return result.returncode == 0


def _is_ancestor(root: Path, older: str, newer: str) -> bool:
    # argv is allowlisted and `shell` is disabled; bare marker, as above.
    result = subprocess.run(  # NOSONAR
        ["git", "-C", str(root.resolve()), "merge-base", "--is-ancestor",
         "--end-of-options", older, newer],
        capture_output=True, check=False)
    return result.returncode == 0


def load_origin_dispositions(path: Path) -> list[object]:
    """The record's `dispositions:` list, header checked, ENTRIES UNCHECKED.

    `list[object]` and not `list[dict]`, because that is what this returns:
    the header is verified here and the entries are not, so a hand-written
    record can put a string or a list where a mapping belongs. The caller
    selects with `isinstance(entry, dict)` before it reads a key, and the
    annotation says so rather than promising a shape this function never
    established (Copilot, round 1 on PR #891). Entry SHAPE is checked by
    `_entry_shape_problems`, and only for the entry that names the change
    being archived — one change's malformed entry must not block another's.

    Raises `SupportError` naming the file when the header is not this record's
    — a file at this path that is not this record cannot be read as an empty
    one, because "no dispositions" and "the wrong file" are different answers
    and only one of them is the operator's to fix.
    """
    if yaml is None:  # pragma: no cover - PyYAML is a hard dependency here
        raise SupportError(
            f"{ORIGIN_DISPOSITIONS_REL}: PyYAML is not installed, so the "
            "disposition record cannot be read")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise SupportError(
            f"{ORIGIN_DISPOSITIONS_REL}: cannot be read ({exc})") from exc
    if not isinstance(data, dict):
        raise SupportError(
            f"{ORIGIN_DISPOSITIONS_REL}: the record must be a mapping "
            f"carrying `schema_version`, `kind` and `dispositions`")
    if data.get("schema_version") != ORIGIN_DISPOSITIONS_SCHEMA_VERSION:
        raise SupportError(
            f"{ORIGIN_DISPOSITIONS_REL}: `schema_version` is "
            f"{data.get('schema_version')!r}, not the integer "
            f"{ORIGIN_DISPOSITIONS_SCHEMA_VERSION} this gate reads")
    if data.get("kind") != ORIGIN_DISPOSITIONS_KIND:
        raise SupportError(
            f"{ORIGIN_DISPOSITIONS_REL}: `kind` is {data.get('kind')!r}, not "
            f"`{ORIGIN_DISPOSITIONS_KIND}`")
    entries = data.get("dispositions")
    if entries is None:
        entries = []
    if not isinstance(entries, list):
        raise SupportError(
            f"{ORIGIN_DISPOSITIONS_REL}: `dispositions` must be a list")
    return entries


def _unknown_key_problems(entry: dict, where: str) -> list[str]:
    """Keys this gate does not read. A key it does not read cannot narrow
    what the entry accepts, so a typo is refused rather than ignored."""
    unknown = sorted(set(entry)
                     - set(ORIGIN_DISPOSITION_KEYS)
                     - set(ORIGIN_DISPOSITION_OPTIONAL_KEYS))
    if not unknown:
        return []
    # THE TWO NEAR-MISSES, NAMED. Both are real spellings ELSEWHERE in this
    # estate, so an author reaching for one has picked a sibling record's word
    # rather than mistyped.
    hints = []
    if "recorded_at" in unknown:
        hints.append("this record spells the citation `cited_to`, and `_at` "
                     "keys in an entry here name COMMITS")
    if "why" in unknown:
        hints.append("this record spells the narrative `fact`, as "
                     "`archive-date-dispositions.yaml` does "
                     "(`openspec-cli-pin.yaml` spells it `why`)")
    hint = (" — " + "; ".join(hints)) if hints else ""
    return [f"{where} carries unknown key(s) {', '.join(unknown)}{hint}. A "
            f"key this gate does not read cannot narrow what the entry "
            f"accepts, so a typo is refused rather than ignored"]


def _string_field_problems(entry: dict, where: str) -> list[str]:
    """The fields that must be non-empty strings, and the date's own shape.

    THE UNQUOTED-SCALAR TRAP IS NAMED rather than left to be guessed: YAML
    reads a bare `2026-09-10` as a DATE and a bare all-digit object name as an
    INT, which is why the sibling record's header says every scalar in an
    entry is quoted.
    """
    problems: list[str] = []
    for key in ("disposition", "disposed_by", "disposed_on", "word",
                "ratified_at", "mutation_at"):
        if key not in entry:
            continue
        value = entry[key]
        if isinstance(value, str) and value.strip():
            continue
        hint = ("" if isinstance(value, str) else
                " — quote it: YAML reads a bare date as a date and a bare "
                "all-digit object name as an integer")
        problems.append(f"{where}: `{key}` must be a non-empty string, not "
                        f"{value!r}{hint}")
    stamp = entry.get("disposed_on")
    if isinstance(stamp, str) and not _ISO_DATE_RE.fullmatch(stamp):
        problems.append(
            f"{where}: `disposed_on` is {stamp!r}, not a YYYY-MM-DD date")
    return problems


def _citation_problems(entry: dict, where: str) -> list[str]:
    """A DISPOSITION WITHOUT A CITATION IS REFUSED, NOT IGNORED — the rule
    `openspec-cli-pin.yaml` states in those words, and doc-health's
    uncited-resolution rule states in its own.

    WHAT the citation points at is not pattern-matched: the sibling records
    cite issues, pull requests, spec lines and council rulings, and a gate
    demanding a URL would refuse three of those four. A STRING OR A LIST OF
    THEM, as the pin manifest's `cited_to:` takes.
    """
    if "cited_to" not in entry:
        return []
    cited = entry["cited_to"]
    rows = cited if isinstance(cited, list) else [cited]
    if rows and all(isinstance(row, str) and row.strip() for row in rows):
        return []
    return [f"{where}: `cited_to` must be a non-empty string, or a non-empty "
            f"list of them, naming where the ruling and this measurement are "
            f"recorded — not {cited!r}"]


def _object_name_problems(entry: dict, where: str) -> list[str]:
    """FULL object names only: an abbreviation is ambiguous by construction
    and this record is a citation."""
    return [f"{where}: `{key}` is {entry[key]!r} — a FULL 40-hex object name "
            f"is required, an abbreviation being ambiguous by construction"
            for key in ("ratified_at", "mutation_at")
            if isinstance(entry.get(key), str)
            and not _FULL_SHA_RE.fullmatch(entry[key])]


def _accept_value_problems(entry: dict, where: str) -> list[str]:
    """`changed_keys`'s own shape, and the one disposition this gate reads."""
    problems: list[str] = []
    keys = entry.get("changed_keys")
    if "changed_keys" in entry and (
            not isinstance(keys, list)
            or not all(isinstance(key, str) for key in keys)):
        problems.append(
            f"{where}: `changed_keys` must be a list of strings (write `[]` "
            f"for a mutation that moved no scalar), not {keys!r}")
    disposition = entry.get("disposition")
    if (isinstance(disposition, str)
            and disposition != ORIGIN_DISPOSITION_ACCEPT):
        problems.append(
            f"{where}: `disposition` is {disposition!r}; the only disposition "
            f"this gate reads is `{ORIGIN_DISPOSITION_ACCEPT}`. RESTORING the "
            f"ratified declaration needs no record — it is the bytes")
    return problems


def _entry_shape_problems(entry: dict, change: str) -> list[str]:
    """Everything wrong with ONE entry's SHAPE, before history is consulted.

    ONE CHECK PER HELPER, and every helper reports EVERY problem it finds
    rather than the first: an operator repairing a hand-written entry should
    see the whole list once, not discover it a line at a time across five
    refusals. (Split out of one function on Sonar's cognitive-complexity
    finding for PR #891; the assertions did not move.)
    """
    where = f"{ORIGIN_DISPOSITIONS_REL}: the entry for {change}"
    missing = [key for key in ORIGIN_DISPOSITION_KEYS if key not in entry]
    return ([*_unknown_key_problems(entry, where)]
            + ([f"{where} is missing {', '.join(missing)}"] if missing else [])
            + _string_field_problems(entry, where)
            + _citation_problems(entry, where)
            + _object_name_problems(entry, where)
            + _accept_value_problems(entry, where))


def _selected_disposition_entry(
        root: Path, change: str) -> tuple[dict | None, list[str]]:
    """THE ONE entry that names `change`, or the reason there is not one.

    `(None, [])` means no entry names this change at all — the ordinary case,
    and not a defect of the record. Entries naming OTHER change ids are never
    even looked at, so one change's malformed entry cannot block another
    change's archive.
    """
    path = origin_dispositions_path(root)
    if not path.is_file():
        return None, []
    try:
        entries = load_origin_dispositions(path)
    except SupportError as exc:
        return None, [str(exc)]
    mine = [entry for entry in entries
            if isinstance(entry, dict) and entry.get("change_id") == change]
    if not mine:
        return None, []
    if len(mine) > 1:
        named = ", ".join(str(entry.get("mutation_at")) for entry in mine)
        return None, [
            f"{ORIGIN_DISPOSITIONS_REL}: {len(mine)} entries name {change} "
            f"(mutation_at: {named}). ONE entry names the accepted "
            f"declaration; a later accepted mutation REPLACES it, moving "
            f"`mutation_at` forward and widening `changed_keys` to the whole "
            f"diff from the ratifying commit"]
    return mine[0], []


def _accept_commit_problems(root: Path, entry: dict, ratifying: str,
                            where: str) -> list[str]:
    """THE COMMITS THE ENTRY NAMES, put to history rather than believed.

    Five questions, and the first NO answers: is this the baseline the gate
    itself resolved; is the named mutation a commit at all; is it a DIFFERENT
    commit; does it DESCEND from the ratification (a post-ratification
    mutation is one that comes after it); and is it in the history being
    archived.
    """
    ratified_at, mutation_at = entry["ratified_at"], entry["mutation_at"]
    if ratified_at != ratifying:
        return [f"{where} names `ratified_at` {ratified_at[:12]}, but this "
                f"change's ratifying commit is {ratifying[:12]} — the entry "
                f"disposes a mutation of some other baseline"]
    if not _commit_exists(root, mutation_at):
        return [f"{where} names `mutation_at` {mutation_at[:12]}, which is "
                f"not a commit in this repository"]
    if mutation_at == ratified_at:
        return [f"{where} names the ratifying commit as its own "
                f"`mutation_at`; there is no mutation there to accept"]
    if not _is_ancestor(root, ratified_at, mutation_at):
        return [f"{where} names a `mutation_at` ({mutation_at[:12]}) that "
                f"does not DESCEND from the ratifying commit "
                f"({ratified_at[:12]}) — a post-ratification mutation is one "
                f"that comes after it"]
    if not _is_ancestor(root, mutation_at, "HEAD"):
        return [f"{where} names a `mutation_at` ({mutation_at[:12]}) that "
                f"this checkout's HEAD does not reach; the accepted "
                f"declaration must be in the history being archived"]
    return []


def _accept_declaration_problems(root: Path, change: str, entry: dict,
                                 now_lines: list[str], now_text: str | None,
                                 where: str) -> list[str]:
    """THE DECLARATIONS THEMSELVES: does the named mutation carry one, does it
    DIFFER from the ratified one (an entry that disposes nothing refuses),
    does it move exactly the keys the entry names, and does the packet being
    archived carry it."""
    ratified_at, mutation_at = entry["ratified_at"], entry["mutation_at"]
    # RESOLVED BY IDENTITY AT EACH REF, not derived once from the id the tree
    # spells now: a packet that moved lawfully carries its ratification under
    # a former id, so the two refs this compares can name two DIFFERENT paths
    # for the same packet (`add-declared-former-id`). The lineage is read from
    # the packet, current identity preferred, and the pre-declaration answer
    # is unchanged for every packet that declares nothing.
    lineage = declared_former_ids_in_tree(root, change)
    identities = [change] + list(reversed(lineage))
    fallback = f"openspec/changes/{change}/.openspec.yaml"
    rel = packet_yaml_at(root, mutation_at, identities) or fallback
    # BOTH READS GO THROUGH `_text_at` (`tasks.md` § 3.4): presence off the
    # TREE first, so a genuinely absent declaration still reaches the findings
    # below and one the checkout cannot produce refuses CANNOT RUN.
    #
    # THE RATIFICATION READ IS THE ONE THAT WAVED SOMETHING THROUGH, and the
    # slice that landed these doors said only that its wording mis-described
    # the cause. It does more than that: `_origin_mapping(None)` is None and
    # `_changed_keys(None, …)` is `[]` by its own advisory contract, so an
    # `accept` entry declaring `changed_keys: []` compared EQUAL to a
    # measurement taken over a declaration that was never read — the
    # acceptance authorised, and the baseline moved to the accepted mutation,
    # on a checkout that could not read the ratification at all. (Copilot, PR
    # #1038 `PRRT_kwDOTAvnrs6iG9vA`.)
    at_mutation_text = _text_at(root, mutation_at, rel, identity=change)
    at_mutation = origin_block_lines(at_mutation_text)
    if at_mutation is None:
        return [f"{where} names a `mutation_at` ({mutation_at[:12]}) at "
                f"which {rel} declares no origin, so there is no declaration "
                f"to accept"]
    ratified_rel = packet_yaml_at(root, ratified_at, identities) or fallback
    at_ratification_text = _text_at(root, ratified_at, ratified_rel,
                                    identity=change)
    if origin_block_lines(at_ratification_text) == at_mutation:
        return [f"{where} accepts {mutation_at[:12]}, whose origin "
                f"declaration is IDENTICAL to the ratified one; the entry "
                f"disposes nothing"]
    measured = _changed_keys(_origin_mapping(at_ratification_text),
                             _origin_mapping(at_mutation_text))
    declared = sorted(entry["changed_keys"])
    if declared != measured:
        return [f"{where} declares `changed_keys` {declared or '[]'}, but "
                f"the diff from {ratified_at[:12]} to {mutation_at[:12]} "
                f"touches {measured or '[]'} — an acceptance covers exactly "
                f"the keys it names"]
    if now_lines != at_mutation:
        # THE KEYS BEYOND THE ACCEPTED DECLARATION, NAMED HERE AND NOT ONLY
        # DIFFED (Copilot, round 2 on PR #891). The headline finding above
        # this one compares the tree to the RATIFICATION and so names the
        # union — the accepted keys AND the new ones — because the baseline
        # does NOT move on a record whose predicate failed. This line is the
        # subtraction the operator actually needs: what this packet moves
        # that no disposition covers.
        beyond = _changed_keys(_origin_mapping(at_mutation_text),
                               _origin_mapping(now_text))
        detail = "\n".join(difflib.unified_diff(
            at_mutation, now_lines,
            fromfile=f"{mutation_at[:12]}:{rel}",
            tofile="the packet being archived", lineterm="", n=1))
        return [f"{where} accepts the declaration at {mutation_at[:12]}, and "
                f"the packet being archived does not carry it — a SECOND, "
                f"undispositioned mutation sits on top of the accepted one"
                + (f"\n  keys moved BEYOND the accepted declaration: "
                   f"{', '.join(beyond)}" if beyond else "")
                + f"\n{detail}"]
    return []


def accepted_origin_mutation(
        root: Path, change: str, ratifying: str, now_lines: list[str],
        now_text: str | None) -> tuple["AcceptedOriginMutation | None",
                                       list[str]]:
    """The record's answer for ONE change: `(accepted, problems)`.

    `accepted` is set when a SINGLE well-formed entry accepts EXACTLY the
    mutation the working tree carries. `problems` are the named reasons a
    record that exists does not apply. Both empty means no entry names this
    change at all — the ordinary case, answered by the caller's channel
    guidance rather than as a defect of the record.

    EVERY CONDITION IS MEASURED AGAINST HISTORY, not taken from the entry: the
    entry says which commits it is about, and this function reads those
    commits. An entry can therefore be wrong, and being wrong refuses while
    NAMING WHAT DID NOT MATCH — which is the difference between a disposition
    and an allow-list.

    THREE STAGES, IN THIS ORDER, and each one is what the next presumes:
    SELECT the entry, check its SHAPE (so the commit names below are strings
    and `changed_keys` is a list), then put its claims to HISTORY.

    ACCEPTANCE IS ALL OR NOTHING, and the baseline does NOT move on a record
    whose predicate failed — including the near miss where every condition
    holds but the tree has moved on again (Copilot, round 2 on PR #891,
    which proposed moving it anyway so the headline diff would be smaller).
    It is refused instead, for two reasons. A record that accepts a
    declaration THE TREE DOES NOT CARRY has accepted nothing, so treating its
    commit as the origin of record would name a declaration nobody is
    archiving; and the headline finding would then have to say the packet
    differs from "the ratifying commit <a commit that is not the
    ratification>", which is false. The actionability the proposal is after
    is delivered where it belongs — inside the record's own finding, which
    names the keys the packet moves BEYOND the accepted declaration and
    diffs against it. When a second mutation is itself accepted, the entry is
    REPLACED rather than joined by another, which the ambiguity refusal in
    `_selected_disposition_entry` says in terms.
    """
    entry, problems = _selected_disposition_entry(root, change)
    if entry is None:
        return None, problems
    problems = _entry_shape_problems(entry, change)
    if problems:
        return None, problems
    where = f"{ORIGIN_DISPOSITIONS_REL}: the entry for {change}"
    problems = (_accept_commit_problems(root, entry, ratifying, where)
                or _accept_declaration_problems(root, change, entry,
                                                now_lines, now_text, where))
    if problems:
        return None, problems
    return AcceptedOriginMutation(entry), []


def origin_disposition_channel(root: Path, change: str,
                               ratifying: str) -> str:
    """HOW to disposition, named at the point of refusal.

    The gate used to end at "this gate has no bypass flag", which is true and
    which told an operator holding a RECORDED acceptance nothing they could
    act on (codeXfactory/codexFactory #318). It still has no flag; what it
    reads instead is spelled out here, with this change's own ratifying commit
    in it so the entry can be written from the refusal.
    """
    return (
        "restoring or accepting a post-ratification origin mutation is a "
        "contested-class act requiring an explicit disposition "
        "(`release-realization` § \"Origin retention at archive\"); this "
        "gate has no bypass flag — what it reads instead is a RECORD.\n"
        f"  RESTORE: put the declaration at {ratifying[:12]} back in the "
        "packet and this gate passes with nothing to read.\n"
        f"  ACCEPT: write {origin_dispositions_path(root)} with "
        f"`schema_version: {ORIGIN_DISPOSITIONS_SCHEMA_VERSION}`, "
        f"`kind: {ORIGIN_DISPOSITIONS_KIND}` and ONE entry under "
        "`dispositions:` carrying "
        f"change_id: {change}; "
        f"ratified_at: {ratifying} (the FULL 40-hex ratifying commit); "
        "mutation_at: the FULL 40-hex commit whose declaration is accepted; "
        "changed_keys: exactly the origin keys the diff between those two "
        "commits touches; "
        f"disposition: {ORIGIN_DISPOSITION_ACCEPT}; "
        "disposed_by; disposed_on (YYYY-MM-DD); word (the verbatim ruling); "
        "cited_to (where that ruling and this measurement are recorded).\n"
        "  The accepted declaration then becomes the ORIGIN OF RECORD and "
        "this gate compares the packet against IT — a later mutation, a "
        "different key set, a missing field or another change id still "
        "refuses.")


def support_manifest(directory: Path) -> Path | None:
    """The packet's readable support manifest, active or archived shape.

    The same two paths and the same order as
    `doc_health.proposal_origin._manifest_origin`: the gate and the family
    cannot look for the manifest in two different places.
    """
    active = directory / "supporting-docs" / "manifest.yaml"
    if active.is_file():
        return active
    archived = directory / "supporting-docs.manifest.yaml"
    return archived if archived.is_file() else None


def _relative(path: Path, root: Path) -> str:
    """`path` as the repository spells it, so a finding reads the same on a
    runner and on a developer machine."""
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return str(path)


def origin_retention_errors(root: Path, directory: Path,
                            change: str | None = None) -> list[str]:
    """The archive gate's origin-retention findings — empty when retained.

    `directory` may be the active packet or an archived one (the replay of a
    landed archive reads the archived path); `change` defaults to the packet's
    own id with any archive date prefix stripped.

    RAISES rather than returns for the fourth arm: when the walk finds that
    its baseline would be the commit that MOVED an already-ratified packet
    rather than the one that ratified it, `ratifying_commit` refuses with
    `OriginRetentionError` (issue #833) and that refusal is deliberately NOT
    caught here. There is no comparison left to report — the baseline itself
    could not be established — so turning it into one more line in a findings
    list would file "cannot run" under "ran and found something", which is the
    conflation the sibling gates' CANNOT RUN status exists to avoid.

    AND THE REFUSAL FOR AN UNREADABLE READ IS NOT CAUGHT HERE EITHER
    (`tasks.md` § 3.4). `ratifying_baseline` fails closed on every read behind
    the baseline, and the `.openspec.yaml` this function then reads AT that
    baseline is one more such read: it is taken through `_text_at`, which
    establishes presence from the TREE first, so a genuinely absent
    declaration still reaches the NOT COMPARABLE arm below and an UNREADABLE
    one refuses. Before that split, a partial checkout that could not read
    the ratifying commit's `.openspec.yaml` reported `ORIGIN RETENTION NOT
    COMPARABLE` and returned `[]` — an ARCHIVE GREEN over a mutated origin,
    the defect this whole gate exists to catch, wearing the pre-contract
    packet's clothes.

    AND THE BASELINE MOVES ON A RECORDED ACCEPTANCE (issue #745). Where the
    declaration HAS moved since ratification, `<root>/openspec/origin-
    dispositions.yaml` is consulted for the explicit disposition the
    requirement's own scenario names; a valid `accept` makes the accepted
    declaration the origin of record and EVERY arm below then compares against
    it. Nothing is skipped: the tree must equal the accepted declaration
    exactly, and a record that does not apply is reported as its own finding
    naming what did not match.
    """
    root = root.resolve()
    # `change_id_of` AND NOT A FOURTH COPY OF THE STRIP: an ACTIVE directory
    # whose id begins with a date was renamed by the spelling that stood here.
    change = change or change_id_of(directory)
    if is_declared_sentinel(repo_revision(root)):
        return [f"origin retention: {change}: this repository's history is "
                "unreadable, so the declaration present at ratification "
                "cannot be resolved — the archive gate cannot verify origin "
                "retention"]
    # THROUGH THE TREE-LEVEL RESOLVER, so the two-candidate rule is not
    # bypassed by the caller handing in a directory. Read straight off
    # `directory` this took ONE packet's declaration and passed it on as
    # `former_ids=`, which skips `declared_former_ids_in_tree`'s ambiguity
    # refusal — and a lineage read from whichever of two locations the caller
    # happened to name is the resolver choosing, which is what this mechanism
    # refuses everywhere else. (Copilot, PR #1038 `PRRT_kwDOTAvnrs6iHNGM`.)
    lineage = declared_former_ids_in_tree(root, change)
    identities = [change] + list(reversed(lineage))
    baseline = ratifying_baseline(root, change, former_ids=lineage)
    if baseline is None:
        under = (f"openspec/changes/{change}/proposal.md"
                 if not lineage else
                 f"openspec/changes/{change}/proposal.md, nor under any "
                 f"identity this packet declares ({', '.join(lineage)})")
        return [f"origin retention: {change}: not ratified — no commit in "
                f"history carries `Status: ratified` in "
                f"{under}, so there is no "
                "declaration to retain. Commit the ratification before "
                "archiving."]
    revision, baseline_identity, baseline_proposal = baseline
    short = revision[:12]
    under = ("" if baseline_identity == change
             else f", under the declared former identity {baseline_identity}")
    # THE BASELINE DECLARATION IS READ UNDER THE IDENTITY THE PACKET WAS
    # RATIFIED UNDER, at the path that identity occupied AT THAT COMMIT. The
    # current id is not always that identity, and deriving the path from it
    # would read nothing at all after a lawful move — which is `git_show_text`
    # answering None, which this function reads as "declares no origin" and
    # prints as NOT COMPARABLE. A gate that goes quiet on exactly the packets
    # this mechanism exists for is the defect wearing the fix's clothes.
    was_text = _text_at(root, revision, packet_yaml_of(baseline_proposal),
                        identity=baseline_identity)
    was = origin_block_lines(was_text)
    packet_file = directory / ".openspec.yaml"
    now_text = (packet_file.read_text(encoding="utf-8")
                if packet_file.is_file() else None)
    now = origin_block_lines(now_text)
    if was is None:
        # NO BASELINE IS NOT A MUTATION, and this arm is measured rather than
        # assumed. Four of the thirty-five active changes on `main` at the time
        # of writing — add-composed-view-authoring, add-doxchat-model-intake,
        # add-lens-document-selection, add-worker-enrollment-broker — carry an
        # origin their ratifying commit does not, because their `Status:`
        # headers were written by the lifecycle-header backfill (`da1b0e90`,
        # `02009d02`) and their origins by the recorded origin sweeps
        # (`b7513733`, `f9bb1a88`) AFTERWARDS. Refusing them would block four
        # lawful archives on a defect none of them has: there is no original
        # declaration for the current one to differ from. The missing-origin
        # case belongs to `origin_errors` (strict) and to the nightly family's
        # class 1, both of which still run.
        print(f"ORIGIN RETENTION NOT COMPARABLE {change}: the packet at the "
              f"ratifying commit {short}{under} declares no origin "
              "(pre-contract packet); presence and shape are still gated")
        return []
    ratifying = revision
    errors: list[str] = []
    channel: list[str] = []
    accepted: AcceptedOriginMutation | None = None
    if now is not None and now != was:
        # THE RECORD IS CONSULTED ONLY WHERE THERE IS A MUTATION TO DISPOSE,
        # and an acceptance MOVES THE BASELINE rather than switching the
        # comparison off: `was` becomes the ACCEPTED declaration and every arm
        # below — the packet's own block, and the support manifest's repeated
        # origin fields — runs against that instead. `accepted_origin_mutation`
        # has already established that the accepted commit carries an origin
        # block and that the tree equals it, so the re-read below cannot come
        # back None.
        accepted, channel = accepted_origin_mutation(
            root, change, ratifying, now, now_text)
        if accepted is not None:
            print(accepted.note())
            revision = accepted.mutation_at
            short = revision[:12]
            # CURRENT IDENTITY FIRST, then the declared lineage newest-first:
            # an accepted mutation is by construction LATER than the
            # ratification, so the packet most likely stood under the id it
            # carries now — but a move that also edits the origin is exactly
            # the laundering case, and there the mutation commit is the one
            # under the FORMER id.
            was_text = _text_at(
                root, revision, packet_yaml_at(root, revision, identities)
                or f"openspec/changes/{change}/.openspec.yaml",
                identity=change)
            was = origin_block_lines(was_text)
    if now is None:
        errors.append(
            f"origin retention: {change}: the origin declaration present at "
            f"the ratifying commit {short}{under} is GONE from the packet "
            "being archived")
    elif now != was:
        keys = _changed_keys(_origin_mapping(was_text),
                             _origin_mapping(now_text))
        detail = "\n".join(difflib.unified_diff(
            was, now,
            fromfile=f"{short}:{packet_yaml_of(baseline_proposal)}",
            tofile=_relative(packet_file, root), lineterm="", n=1))
        errors.append(
            f"origin retention: {change}: the origin declaration differs "
            f"from the one this change was ratified over (ratifying commit "
            f"{short}{under})"
            + (f"\n  changed keys: {', '.join(keys)}" if keys else "")
            + f"\n{detail}")
    # THE MANIFEST IS THE SECOND COPY THE REQUIREMENT NAMES — "the compressed
    # supporting-document manifest SHALL retain the same origin id and path".
    # `origin_errors` already compares it to the PACKET; comparing it to the
    # DECLARATION OF RECORD is what catches the lockstep edit that moves both
    # copies together and leaves them agreeing with each other about the wrong
    # thing. The declaration of record is the RATIFYING one, or — where a
    # disposition accepted a mutation above — the ACCEPTED one, because that
    # is the declaration the manifest must now agree with; measuring against
    # the superseded ratified declaration would refuse a manifest that is
    # correct, and not measuring at all would drop an arm the requirement
    # names.
    was_map = _origin_mapping(was_text) or {}
    manifest_path = support_manifest(directory)
    if manifest_path is not None:
        try:
            m_origin = load_manifest(manifest_path).get("origin")
        except SupportError:
            m_origin = None
        if isinstance(m_origin, dict):
            fields = ["kind", "id"]
            if was_map.get("kind") == "staged":
                fields.append("path")
            baseline = ("the ACCEPTED declaration at " + short
                        if accepted is not None else "ratification")
            for field in fields:
                if field in was_map and m_origin.get(field) != was_map[field]:
                    errors.append(
                        f"origin retention: {change}: support manifest origin "
                        f"`{field}` ({m_origin.get(field)!r}) is not the one "
                        f"declared at {baseline} ({was_map[field]!r}) — "
                        f"{manifest_path.name}")
    if errors:
        # A RECORD THAT EXISTS AND DOES NOT APPLY IS ITS OWN FINDING, named
        # before the channel text: an operator who wrote an entry needs to be
        # told WHAT DID NOT MATCH, not re-told how to write one.
        errors.extend(f"origin disposition: {problem}" for problem in channel)
        errors.append(origin_disposition_channel(root, change, ratifying))
    elif accepted is not None:
        print(f"ORIGIN RETAINED {change} (declaration unchanged since the "
              f"ACCEPTED mutation {short}, dispositioned `accept` by "
              f"{accepted.disposed_by} on {accepted.disposed_on}; ratifying "
              f"commit {ratifying[:12]})")
    else:
        print(f"ORIGIN RETAINED {change} (declaration unchanged since the "
              f"ratifying commit {short}{under})")
    return errors


def write_origin_block(directory: Path, origin: dict,
                       created: str) -> None:
    """Append (never rewrite) the origin block to `.openspec.yaml`,
    creating a minimal packet when none exists. Refuses to overwrite an
    existing declaration — origins are fixed at creation."""
    packet_file = directory / ".openspec.yaml"
    existing = load_packet(directory)
    if isinstance(existing, dict) and isinstance(existing.get("origin"),
                                                 dict):
        raise SupportError(
            f"{directory.name}: origin already declared; origins are "
            "immutable — refusing to overwrite")
    lines = []
    if not packet_file.is_file():
        lines.append(f"schema: spec-driven\ncreated: {created}")
    body = [f"origin:", f"  kind: {origin['kind']}", f"  id: {origin['id']}"]
    if origin["kind"] == "staged":
        body.append(f"  path: {origin['path']}")
    else:
        body.append("  reason: >-")
        for chunk in origin["reason"].splitlines() or [origin["reason"]]:
            body.append(f"    {chunk}")
        # EVERY LAWFUL AD-HOC SHAPE IS WRITABLE BY THE SANCTIONED WRITER
        # (`add-drafted-proposal-origin`), or the unapproved state the gate
        # now accepts has no producer and is hand-authorable only. Both pairs
        # are written where both are given: who drafted a proposal is not
        # erased by who later approved it, and the drafting record is the only
        # trace of the interval.
        wrote = False
        for pair in (APPROVAL_FIELDS, DRAFTING_FIELDS):
            given = [f for f in pair if str(origin.get(f) or "").strip()]
            if given and len(given) != len(pair):
                # A HALF-GIVEN PAIR IS REFUSED, NEVER DROPPED. Writing the
                # block without it would discard the caller's intent in
                # silence and leave a record that looks complete — while the
                # gate and the nightly family both report a half-declared pair
                # as a defect, so the writer would be producing a shape its
                # own checkers reject. Caught by Copilot on PR #619.
                missing = [f for f in pair if f not in given]
                raise SupportError(
                    f"{directory.name}: ad-hoc origin gives "
                    f"{', '.join('`' + f + '`' for f in given)} without "
                    f"{', '.join('`' + f + '`' for f in missing)} — a "
                    "provenance pair is declared in full or not at all")
            if given:
                for field in pair:
                    body.append(f"  {field}: {origin[field]}")
                wrote = True
        if not wrote:
            raise SupportError(
                f"{directory.name}: an ad-hoc origin needs either "
                "`approved_by` + `approved_on` (an approved exception) or "
                "`proposed_by` + `proposed_on` (an unapproved draft); "
                "neither pair is complete")
    prefix = packet_file.read_text(encoding="utf-8").rstrip("\n") + "\n" \
        if packet_file.is_file() else "\n".join(lines) + "\n"
    packet_file.write_text(prefix + "\n".join(body) + "\n",
                           encoding="utf-8")


def markdown_target(raw: str) -> tuple[str, str] | None:
    value = raw.strip()
    if value.startswith("<") and value.endswith(">"):
        value = value[1:-1]
    if not value or value.startswith(("#", "http://", "https://", "mailto:")):
        return None
    path, marker, anchor = value.partition("#")
    return path, marker + anchor if marker else ""


def rewrite_links(text: str, old_file: Path, new_file: Path,
                  mapping: dict[Path, Path], root: Path) -> str:
    def replace(match: re.Match) -> str:
        parsed = markdown_target(match.group(2))
        if parsed is None:
            return match.group(0)
        raw_path, anchor = parsed
        old_target = ensure_inside(old_file.parent / raw_path, root,
                                   "Markdown link")
        target = mapping.get(old_target, old_target)
        if not target.exists() and target not in mapping.values():
            raise SupportError(
                f"broken relative link in {old_file}: {match.group(2)}"
            )
        relative = os.path.relpath(target, new_file.parent).replace(os.sep, "/")
        return f"{match.group(1)}({relative}{anchor})"

    return LINK_RE.sub(replace, text)


_STATUS_BODY_RE = re.compile(r"Status:\s*(\S+)\s*")
AUTHORSHIP_PREFIX = "Proposed by:"


def _status_row(rows: list[tuple[str, str]],
                flags: list[bool]) -> tuple[int, str] | None:
    """(row index, value) of the document's OWN `Status:` header, or None.

    FENCE-AWARE, and that is not fastidiousness: the first fragment this mover
    ever moved carried a copy-pasteable skeleton whose fenced example header read
    `Status: staged`, and `_declares_staged_status` already had to learn to skip
    it. Reading the example as the document's status here would flip the wrong
    line and leave the real header untouched.
    """
    for index, (body, _ending) in enumerate(rows):
        if flags[index]:
            continue
        match = _STATUS_BODY_RE.fullmatch(body)
        if match:
            return index, match.group(1)
    return None


def _header_block(rows: list[tuple[str, str]], flags: list[bool],
                  status_index: int) -> tuple[int, int]:
    """The `[start, end)` row range of the contiguous non-blank run carrying the
    document's `Status:` header — the block the authorship record belongs to.

    The record is ANCHORED to that block rather than found by "first match
    anywhere". A `Proposed by:` line sitting far below the header is not this
    document's authorship record: rewriting it there would leave the header block
    with no record at all and quietly relocate a governance line into somebody's
    prose.
    """
    start = status_index
    while start > 0 and rows[start - 1][0].strip() and not flags[start - 1]:
        start -= 1
    end = status_index + 1
    while end < len(rows) and rows[end][0].strip() and not flags[end]:
        end += 1
    return start, end


def _authorship_rows(rows: list[tuple[str, str]], flags: list[bool]) -> list[int]:
    """Row indices of the REAL authorship lines — outside every code fence.

    A `Proposed by:` line inside a fence is an EXAMPLE. Treating it as the record
    both suppressed adding the real one (a document whose only occurrence was
    fenced silently got no record at all, against the ratified "the record MUST be
    added") and rewrote the example to name the current change.
    """
    return [index for index, (body, _ending) in enumerate(rows)
            if not flags[index] and body.startswith(AUTHORSHIP_PREFIX)]


def record_authorship(text: str, change: str) -> str:
    """The staged->draft flip PLUS the document's single authorship record.

    ONE RECORD PER DOCUMENT, NOT ONE PER ATTEMPT. A document may legitimately
    reach proposal, be demoted, be worked, and reach proposal again — the
    round-trip guarantee exists so that lap is normal — and appending a fresh
    `Proposed by:` line each time turned a normal lap into an ambiguous record:
    several lines each claiming to name the proposing change say nothing about
    which one is current. So pre-existing duplicates are COLLAPSED here too; the
    ratified requirement is unconditional ("the document MUST carry exactly one
    such record"), and refreshing one of three while leaving two stale satisfies
    the letter of an update and none of the point.

    THE COLLAPSE REACHES THE WHOLE DOCUMENT, not just the header block. Only the
    KEPT record is anchored to that block; every other unfenced `Proposed by:`
    line goes, wherever it sits, because a stale record left standing in the body
    says the same ambiguous thing as one left standing in the header. A line
    inside a code fence is an example and is never touched. Measured rather than
    estimated: 0 of the corpus's 1133 markdown documents carry a second such
    record or one outside their header block today, so this governs the shape
    rather than clearing a backlog.

    THE OBLIGATION SITS HERE, on the gate that WRITES the line, and deliberately
    not on the reverse transition's refresh. That refresh is ratified as bounded
    to the round-trip provenance slots and the marked proposal-element sections,
    "leaving every other byte of that file unchanged"; deduping a header there
    would trade a data-loss guarantee for tidiness.

    ROW-BASED, NOT `re.sub` OVER THE RAW TEXT, for two demonstrated reasons.
    `^Status:\\s*staged\\s*$` consumes the newline after the header — `\\s*` is
    greedy and `$` is satisfied one line later — so a human's blank line between
    the header block and the body was deleted on every lap (7 lines in, 6 out).
    And `\\s*`/`.*$` both swallow a `\\r`, so the one rewritten line came out LF
    in a CRLF document. Rewriting a row in place keeps the ending it HAD.
    """
    rows = _split_keepends(text)
    flags = _fenced_flags(rows)
    found = _status_row(rows, flags)
    if found is None:
        return text
    status_index, _value = found
    start, end = _header_block(rows, flags, status_index)
    authorship = _authorship_rows(rows, flags)
    in_block = [index for index in authorship if start <= index < end]
    keep = in_block[0] if in_block else None
    drop = {index for index in authorship if index != keep}

    out: list[tuple[str, str]] = []
    for index, (body, ending) in enumerate(rows):
        if index == status_index:
            if keep is None:
                # A new record joins the header block directly under the status
                # it belongs to. The status row borrows the document's ending
                # flavor when it had none (a file with no trailing newline), so
                # the two lines never fuse into one.
                out.append(("Status: draft", ending or _document_eol(rows)))
                out.append((f"{AUTHORSHIP_PREFIX} {change}", ending))
            else:
                out.append(("Status: draft", ending))
            continue
        if index in drop:
            continue
        if index == keep:
            out.append((f"{AUTHORSHIP_PREFIX} {change}", ending))
            continue
        out.append((body, ending))
    return _join_rows(out)


def proposed_content(path: Path, target: Path, mapping: dict[Path, Path],
                     root: Path, change: str, historical: bool = False) -> bytes:
    data = path.read_bytes()
    if path.suffix.lower() != ".md":
        return data
    text = data.decode("utf-8")
    rows = _split_keepends(text)
    found = _status_row(rows, _fenced_flags(rows))
    if found is None:
        raise SupportError(f"governed Markdown lacks Status header: {path}")
    _index, value = found
    if value == "staged":
        text = record_authorship(text, change)
    elif value not in (
            {"draft", "record", "superseded", "retired"}
            if historical else {"draft", "record"}):
        raise SupportError(
            f"supporting Markdown status must be staged, draft, or record: {path}"
        )
    return rewrite_links(text, path, target, mapping, root).encode("utf-8")


def source_files(source: Path) -> list[Path]:
    files = []
    for path in sorted(source.rglob("*")):
        reject_symlinks(path)
        if path.is_file():
            files.append(path.resolve())
    return files


def select_files(source: Path, requested: list[str]) -> tuple[list[Path], list[Path]]:
    all_files = source_files(source)
    if not requested:
        return all_files, []
    selected = []
    for raw in requested:
        candidate = ensure_inside(source / raw, source, "selected file")
        reject_symlinks(candidate)
        if not candidate.is_file():
            raise SupportError(f"selected file not found: {raw}")
        selected.append(candidate)
    selected = sorted(set(selected))
    return selected, [path for path in all_files if path not in selected]


def move_file(source: Path, target: Path) -> None:
    # Git stores snapshots, not rename operations; review/commit still detects
    # the move without mutating the caller's index as an implementation side effect.
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))


def transition(root: Path, change: str, source_arg: str, requested: list[str],
               workspace: str | None, transition_date: str, archived: bool,
               apply: bool) -> dict:
    root = root.resolve()
    source = ensure_inside(root / source_arg, root, "staging source")
    expected = root / "ideation" / "staging"
    ensure_inside(source, expected, "staging source")
    if source == expected or not source.is_dir():
        raise SupportError("source must be a topic below ideation/staging")
    destination = change_dir(root, change, archived) / "supporting-docs"
    if (destination / "manifest.yaml").exists():
        raise SupportError(f"support manifest already exists: {destination}")

    selected, remaining = select_files(source, requested)
    if not selected:
        raise SupportError("no supporting files selected")
    mapping = {
        path: destination / path.relative_to(source) for path in selected
    }
    snapshots = {
        path: destination / "source-snapshots" / path.relative_to(source)
        for path in selected
    }
    for target in [*mapping.values(), *snapshots.values()]:
        ensure_inside(target, destination, "support destination")
        if target.exists():
            raise SupportError(f"support destination exists: {target}")

    rendered = {
        path: proposed_content(path, mapping[path], mapping, root, change,
                               historical=archived)
        for path in selected
    }
    revision = repo_revision(root)
    # POSIX SPELLING FOR EVERY RECORDED PATH, the same rule and the same reason
    # as `origin_rel` below (PR #221, whose fix named these fields as the next
    # lap). Each of the three is a machine-readable KEY: `verify_active_support`
    # joins `path` and `source_snapshot_path` to the support folder and
    # doc-health's location-conformance family joins `path` to the same folder,
    # while `source_path` becomes `<revision>:<path>` for `git show`.
    # `str(PurePath)` spells all three with backslashes on a Windows checkout,
    # so the manifest's KEYS would depend on the operating system of whoever ran
    # the gate while the sha256s beside them — content hashes — stayed correct
    # and unreconcilable. ONE DERIVATION PER PATH, so an entry cannot contradict
    # itself: each field is the single `as_posix()` value of its own path, and
    # the committed-blob check below reads `entry["source_path"]` back rather
    # than deriving that path a second time.
    entries = [
        {
            "path": mapping[path].relative_to(destination).as_posix(),
            "sha256": sha256_bytes(rendered[path]),
            "source_path": path.relative_to(root).as_posix(),
            "source_sha256": sha256_file(path),
            "source_snapshot_path":
                snapshots[path].relative_to(destination).as_posix(),
        }
        for path in selected
    ]
    # The committed-blob comparison is only askable where the revision names a
    # commit. Under ANY declared sentinel there is no tree to resolve against,
    # which is the same reasoning that returned None above and is now spelled
    # against the declaration rather than against one literal.
    if not is_declared_sentinel(revision):
        for entry in entries:
            committed = git_blob_sha256(
                root, revision, entry["source_path"])
            if committed != entry["source_sha256"]:
                raise SupportError(
                    "staging source is not committed at source revision: "
                    f"{entry['source_path']}")
    # Origin contract (add-proposal-origin-contract task 4.3): the proposal
    # gate writes the staged origin automatically. The durable id authority
    # is the staging documents' own `Staging ID:` header; the folder name is
    # the fallback for topics that predate the header convention.
    header_id = staging_header_id(source)
    origin_id = header_id or f"{root.name}:staging:{source.name}"
    # POSIX SPELLING, not `str(PurePath)`. The origin path is a MACHINE-READABLE
    # RECORD other tools split on `/` — `generator._declared_origin_staging`
    # resolves the demote's destination topic from it, and doc-health's
    # `proposal-origin` family joins it to a repo root. `str()` on a Windows
    # checkout yields `ideation\staging\<topic>`, so the record's spelling would
    # depend on the operating system of whoever ran the gate, and every reader of
    # it would silently stop resolving. The record format does not get to depend
    # on the writer's OS.
    origin_rel = source.relative_to(root).as_posix()
    origin = {"kind": "staged", "id": origin_id, "path": origin_rel}
    existing_packet = load_packet(change_dir(root, change, archived))
    declared = (existing_packet or {}).get("origin")
    if isinstance(declared, dict):
        for field in ("kind", "id", "path"):
            if declared.get(field) not in (None, origin[field]):
                raise SupportError(
                    f"declared origin `{field}` ({declared.get(field)!r}) "
                    f"disagrees with the transition source "
                    f"({origin[field]!r}) — origins are immutable")
    manifest = {
        "change_id": change,
        "files": entries,
        "format_version": 1,
        "notebook_workspace": workspace,
        "origin": origin,
        # The SAME value as `origin["path"]`, recorded a second time and read by
        # doc-health's `proposal-origin` family. One spelling, from one source, so
        # a manifest cannot contradict itself about the path it came from.
        "origin_path": origin_rel,
        # POSIX for the same reason as the entries above: this names material
        # that stayed staged, and a reader that joins it to a repo root cannot
        # be told which operating system wrote it.
        "remaining_paths": [path.relative_to(root).as_posix()
                            for path in remaining],
        "source_revision": revision,
        "transitioned_at": transition_date,
    }

    action = "MOVE" if apply else "WOULD MOVE"
    for path in selected:
        print(f"{action} {path.relative_to(root)} -> {mapping[path].relative_to(root)}")
    if not apply:
        return manifest

    for path in selected:
        snapshots[path].parent.mkdir(parents=True, exist_ok=True)
        snapshots[path].write_bytes(path.read_bytes())
        move_file(path, mapping[path])
        mapping[path].write_bytes(rendered[path])
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "manifest.yaml").write_text(
        manifest_text(manifest), encoding="utf-8"
    )
    if not isinstance(declared, dict):
        write_origin_block(change_dir(root, change, archived), origin,
                           transition_date)
    for directory in sorted(source.rglob("*"), reverse=True):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
    if source.exists() and not any(source.iterdir()):
        source.rmdir()
    return manifest


def verify_active_support(directory: Path) -> list[str]:
    support = directory / "supporting-docs"
    manifest = load_manifest(support / "manifest.yaml")
    errors = []
    root = directory.parents[2]
    revision = manifest.get("source_revision")
    for entry in manifest.get("files", []):
        path = ensure_inside(support / manifest_rel(entry["path"]), support,
                             "manifest path")
        if not path.is_file():
            errors.append(f"missing support file: {path}")
        elif sha256_file(path) != entry.get("sha256"):
            errors.append(f"support checksum mismatch: {path}")
        source_sha256 = entry.get("source_sha256")
        snapshot_valid = False
        snapshot_path = manifest_rel(entry.get("source_snapshot_path"))
        if source_sha256 and snapshot_path:
            snapshot = ensure_inside(
                support / snapshot_path, support, "source snapshot path"
            )
            reject_symlinks(snapshot)
            if not snapshot.is_file():
                errors.append(f"missing source snapshot: {snapshot}")
            elif sha256_file(snapshot) != source_sha256:
                errors.append(f"source snapshot checksum mismatch: {snapshot}")
            else:
                snapshot_valid = True
        # THE GUARD THE MEASURED CRASH REACHED THROUGH. Verifying any of the six
        # archived `uncommitted-worktree` manifests fell into this branch,
        # called `git_blob_sha256` with a value no commit shape matches, and
        # raised out of a function whose contract is to append findings.
        if source_sha256 and not is_declared_sentinel(revision):
            committed = git_blob_sha256(
                root, revision, entry.get("source_path", ""))
            if committed is None and not snapshot_valid:
                errors.append(
                    "staging source revision unavailable without valid snapshot: "
                    f"{entry.get('source_path', '')}"
                )
            elif committed is not None and committed != source_sha256:
                errors.append(
                    "staging source checksum mismatch: "
                    f"{entry.get('source_path', '')}")
        if path.suffix.lower() == ".md":
            text = path.read_text(encoding="utf-8")
            if _declares_staged_status(text):
                errors.append(f"staged status under active proposal: {path}")
    return errors


def _declares_staged_status(text: str) -> bool:
    """Whether the document's OWN header still says `staged`.

    Fence-aware, because a `Status: staged` line inside a ``` block is an
    EXAMPLE, not this document's status — the first fragment moved by this
    mover carried a copy-pasteable template skeleton whose example header said
    exactly that, and a naive multiline regex read the example as the real
    thing and failed a bundle whose real header the mover had already
    transitioned to `draft`. What is mirrored from
    `doc_health.families._scan_lines` is the FENCE-TRACKING convention alone — a
    ``` line toggling whether the rows after it count as content — rather than
    inventing a second convention for that. The line split underneath it is a
    separate rule, and a shared one: both count the three real endings below.
    Keeping a local copy of that split is a DELIBERATE CHOICE here, not an
    impossibility — importing `doc_health.lines` would work, as the sibling
    standalone `bootstrap-ideation-cross-reference.py` does from any cwd on
    Python's own `sys.path[0]` insertion, both files living directly under
    `scripts/` beside the package. This mover keeps its own copy because
    converting it was RULED out of scope (finding F7,
    `align-status-reader-to-real-lines` tasks.md 7.5): the promoted requirement
    governs how the DETERMINISTIC PASS reads a lifecycle header, and this is a
    standalone mover that reports nothing to that pass. What makes the choice
    safe is the agreement tests rather than this sentence —
    `test_the_mover_agrees_with_the_other_fence_implementations` and
    `test_the_movers_line_split_is_the_three_real_endings_and_nothing_else` pin
    the local copy to the shared rule.

    Split by this module's three-real-endings rule rather than
    `str.splitlines()`, which also breaks on \\x0b, \\x0c, \\x1c-\\x1e, \\x85,
    U+2028 and U+2029 — so this READER and the writer beside it agree about where
    the lines are, rather than each having its own opinion about the same bytes.
    """
    rows = _split_keepends(text)
    flags = _fenced_flags(rows)
    for index, (body, _ending) in enumerate(rows):
        if flags[index]:
            continue
        if re.fullmatch(r"Status:\s*staged\s*", body):
            return True
    return False


def deterministic_bundle(support: Path) -> tuple[bytes, list[dict]]:
    entries = []
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.GNU_FORMAT) as tar:
            for path in source_files(support):
                rel = path.relative_to(support).as_posix()
                data = path.read_bytes()
                info = tarfile.TarInfo(rel)
                info.size = len(data)
                info.mtime = 0
                info.mode = 0o644
                info.uid = info.gid = 0
                info.uname = info.gname = ""
                tar.addfile(info, io.BytesIO(data))
                entries.append({"path": rel, "sha256": sha256_bytes(data)})
    return buffer.getvalue(), entries


def package(root: Path, change: str, packaged_at: str, archived: bool,
            final_import_complete: bool, apply: bool) -> dict:
    root = root.resolve()
    directory = change_dir(root, change, archived)
    support = directory / "supporting-docs"
    if not support.is_dir():
        raise SupportError(f"supporting-docs folder not found: {support}")
    active_manifest = load_manifest(support / "manifest.yaml")
    if active_manifest.get("notebook_workspace") and not final_import_complete:
        raise SupportError("final NotebookLM source import is not recorded")
    errors = verify_active_support(directory)
    errors.extend(origin_errors(root, directory, strict=False,
                                manifest=active_manifest))
    if errors:
        raise SupportError("; ".join(errors))

    bundle, files = deterministic_bundle(support)
    archive_manifest = {
        "bundle": {
            "path": "supporting-docs.tar.gz",
            "sha256": sha256_bytes(bundle),
        },
        "change_id": change,
        "files": files,
        "final_notebook_import_complete": final_import_complete,
        "format_version": 1,
        "notebook_workspace": active_manifest.get("notebook_workspace"),
        "origin": active_manifest.get("origin"),
        "origin_path": active_manifest.get("origin_path"),
        "packaged_at": packaged_at,
        "source_revision": active_manifest.get("source_revision"),
        "transitioned_at": active_manifest.get("transitioned_at"),
    }
    action = "PACKAGE" if apply else "WOULD PACKAGE"
    print(f"{action} {support} ({len(files)} files)")
    if apply:
        (directory / "supporting-docs.tar.gz").write_bytes(bundle)
        (directory / "supporting-docs.manifest.yaml").write_text(
            manifest_text(archive_manifest), encoding="utf-8"
        )
        shutil.rmtree(support)
    return archive_manifest


def safe_tar_members(bundle: Path) -> dict[str, bytes]:
    members = {}
    with tarfile.open(bundle, "r:gz") as archive:
        for member in archive.getmembers():
            pure = PurePosixPath(member.name)
            if member.issym() or member.islnk() or pure.is_absolute() or ".." in pure.parts:
                raise SupportError(f"unsafe archive member: {member.name}")
            if not member.isfile():
                continue
            stream = archive.extractfile(member)
            if stream is None:
                raise SupportError(f"unreadable archive member: {member.name}")
            members[member.name] = stream.read()
    return members


def verify_archive(directory: Path) -> list[str]:
    manifest_path = directory / "supporting-docs.manifest.yaml"
    bundle = directory / "supporting-docs.tar.gz"
    manifest = load_manifest(manifest_path)
    errors = []
    if not bundle.is_file():
        return [f"missing support bundle: {bundle}"]
    if sha256_file(bundle) != manifest.get("bundle", {}).get("sha256"):
        errors.append(f"bundle checksum mismatch: {bundle}")
    try:
        members = safe_tar_members(bundle)
    except (SupportError, tarfile.TarError, OSError) as exc:
        return errors + [str(exc)]
    # The bundle's member names are POSIX by construction (`deterministic_bundle`
    # writes `as_posix()`, on every platform), so the manifest side is the only
    # half of this comparison that a Windows writer could have spelled the other
    # way. Normalize it and the two halves are the same alphabet again; without
    # it the inventory sets differ and a sound bundle reads as corrupt.
    expected = {manifest_rel(entry["path"]): entry["sha256"]
                for entry in manifest.get("files", [])}
    if set(members) != set(expected):
        errors.append(f"bundle member inventory mismatch: {bundle}")
    for path, data in members.items():
        if path in expected and sha256_bytes(data) != expected[path]:
            errors.append(f"bundled file checksum mismatch: {path}")
    return errors


def verify(root: Path, change: str | None) -> list[str]:
    root = root.resolve()
    errors = []
    active_root = root / "openspec" / "changes"
    for directory in sorted(active_root.iterdir()):
        if not directory.is_dir() or directory.name == "archive":
            continue
        if change and directory.name != change:
            continue
        support_manifest = None
        if (directory / "supporting-docs").exists():
            try:
                errors.extend(verify_active_support(directory))
                support_manifest = load_manifest(
                    directory / "supporting-docs" / "manifest.yaml")
            except SupportError as exc:
                errors.append(str(exc))
        errors.extend(origin_errors(root, directory,
                                    strict=bool(change),
                                    manifest=support_manifest))
    for directory in sorted((active_root / "archive").iterdir()):
        if not directory.is_dir():
            continue
        change_id = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", directory.name)
        if change and change_id != change:
            continue
        has_manifest = (directory / "supporting-docs.manifest.yaml").exists()
        has_bundle = (directory / "supporting-docs.tar.gz").exists()
        if has_manifest or has_bundle:
            if not (has_manifest and has_bundle):
                errors.append(f"incomplete archived support: {directory}")
            else:
                try:
                    errors.extend(verify_archive(directory))
                    errors.extend(origin_errors(
                        root, directory, strict=bool(change),
                        manifest=load_manifest(
                            directory / "supporting-docs.manifest.yaml")))
                except SupportError as exc:
                    errors.append(str(exc))
        elif change:
            errors.extend(origin_errors(root, directory, strict=True))
    misplaced = list((root / "openspec" / "specs").rglob("supporting-docs.tar.gz"))
    errors.extend(f"support bundle under canonical specs: {path}" for path in misplaced)
    return errors


# --------------------------------------------------------------------------
# THE OpenSpec CLI THIS SCRIPT DRIVES — RESOLVED THROUGH THE PIN, NEVER FROM
# PATH (issue #691)
#
# WHAT WAS WRONG. This wrapper is the SANCTIONED archive path: it runs the
# origin gate, refuses a change with open task boxes, packages supporting
# documents into a deterministic bundle, and only then archives. Every one of
# those checks was performed against a corpus adjudicated by
# `["openspec", …]` — the name, resolved by the shell out of whatever happened
# to be on PATH. `contracts/openspec-cli-pin.yaml` had meanwhile made
# `@fission-ai/openspec` a CONTENT-ADDRESSED consumption and named
# `scripts/validate-openspec-cli-pin.py` as the one entrypoint through which
# the estate obtains and runs it — and this file, the tool that performs the
# irreversible half of the act the pin exists to govern, read none of it. On
# the workstation this was found on, PATH answered `1.2.0` while the pin
# recorded `1.12.0`: the archive ran a version the repository does not pin, and
# nothing said so.
#
# WHAT RUNS NOW, AND IN WHICH ROLE.
#
#   * STRICT VALIDATION runs through the CONSUMER ENTRYPOINT itself
#     (`validate_through_the_pin` below), not through a `validate` argv this
#     file assembles. The pin's `consumer_entrypoint:` says every strict
#     validation in the estate goes through that file "and through nothing
#     else", and the reason is not ceremony: the entrypoint is where the pin's
#     `dispositions:` are applied. A finding this repository has ACCEPTED in
#     writing, with a citation and a named authority, must not block an archive
#     merely because the wrapper re-asked the question with a rawer tool.
#   * THE ARCHIVE ITSELF runs the PINNED EXECUTABLE, resolved by the
#     entrypoint's own `resolve_pinned` — fetched, hashed against the recorded
#     SHA-512 and SHA-1, installed, and asserted to report the pinned version
#     before it is invoked. The entrypoint has no archive mode and deliberately
#     never grows one (`neutral-product-pin` forbids a target-less run there),
#     so what is reused here is its RESOLVER, never a second implementation of
#     it. Nothing about which bytes the pin names is written in this file.
#
# NEVER A SILENT FALLBACK. If the pinned artifact cannot be obtained, or the
# resolved binary reports a different version, this refuses with the verifier's
# own named code and its remediation trailer, printed verbatim, and exits 2 —
# the exit `scripts/validate-openspec-cli-pin.py` and
# `scripts/install-pinned-openspec-cli.py` already use for a refusal, kept
# distinct from the exit 1 this script has always used for "your change is not
# archivable". An unanswerable question about which tool would run is never an
# implicit permission to run whichever one is nearest.
#
# THE ONE ESCAPE IS THE ENTRYPOINT'S OWN. `--path-mode` is not invented here:
# it is the verifier's flag, with the verifier's semantics and the verifier's
# limits — it uses the `openspec` on PATH and REFUSES unless that binary reports
# the pinned version, which checks the LABEL and not the referent. It exists for
# a developer who is offline with the pinned version already installed, it is
# passed straight through to the entrypoint for the validation half so the two
# halves can never run different binaries, and it is never a governed check.
# --------------------------------------------------------------------------

PIN_VERIFIER = Path(__file__).resolve().parent / "validate-openspec-cli-pin.py"

_PIN_VERIFIER_MODULE = None
_RESOLVED_OPENSPEC: dict[tuple, Path] = {}


# THE TWO CODES THIS FILE ORIGINATES, and the reason there are two rather than
# one. The refusal VOCABULARY belongs to the pin verifier: where this wrapper
# catches a `PinRefusal` it carries that code and that message through unchanged
# (`pin-tag-only`, `pin-integrity-mismatch`, `pin-unresolvable`,
# `pin-version-mismatch`, …). These two are the conditions the verifier cannot
# report about itself:
#
#   pin-entrypoint-unavailable  the entrypoint could not be LOADED, so no
#                               refusal of its own could be raised at all
#   pin-refused                 the entrypoint was called as a whole
#                               (`validate_through_the_pin`) and returned its
#                               exit 2 rather than an exception. The named code
#                               and the remediation are already on stderr,
#                               printed by the verifier; re-deriving them here
#                               would be a second copy of a vocabulary this file
#                               does not own, so what this code says is only
#                               "the entrypoint refused, and this archive stops"
#
# `tests/proposal-support/test_pinned_openspec_cli.py::
# test_the_wrapper_originated_refusal_codes_are_exactly_what_it_raises` asserts
# this tuple against the codes actually raised in this file, so a third one
# cannot be added without adding it here — which is the drift Copilot caught on
# PR #694, when this list said "exactly one" and the code raised two.
WRAPPER_REFUSAL_CODES: tuple[str, ...] = (
    "pin-entrypoint-unavailable", "pin-refused")


class PinnedCliRefusal(RuntimeError):
    """A refusal to invoke OpenSpec because the PINNED CLI is not what would run.

    Deliberately NOT a `SupportError`. That class means "this change cannot be
    archived", which `main` reports as exit 1; this one means "which tool would
    adjudicate the change is unsettled", which exits 2. A caller that branched
    on the first and got the second would read an unresolved pin as a defect in
    somebody's proposal.

    `code` is the verifier's own refusal code wherever this wrapper caught a
    `PinRefusal` — carried unchanged so a caller may branch on it — and
    otherwise one of the two in `WRAPPER_REFUSAL_CODES` above. `str()` is the
    verifier's whole message where there was one, code, detail and the fixed
    remediation trailer reproduced verbatim rather than reworded here.
    """

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


def pin_verifier():
    """The pin verifier module, LOADED rather than re-implemented.

    The same `spec_from_file_location` route `scripts/install-pinned-openspec-
    cli.py` and `tests/openspec_cli_pin/` already take to reach a hyphenated
    file. Loading it — rather than copying its parser, its hashing, its install
    or its refusal vocabulary — is the whole point: a second implementation of
    "which bytes does the pin name" would be the second copy of the pin that
    `contracts/openspec-cli-pin.yaml`'s own header describes moving apart.

    Loaded LAZILY, on first use, so that importing this script — which
    `tests/doc-health/test_proposal_origin.py` and `tests/proposal-support/` both
    do, and which every non-archive subcommand does — costs nothing and reads no
    contract it will not use.
    """
    global _PIN_VERIFIER_MODULE
    if _PIN_VERIFIER_MODULE is not None:
        return _PIN_VERIFIER_MODULE
    if not PIN_VERIFIER.is_file():
        raise PinnedCliRefusal(
            "pin-entrypoint-unavailable",
            f"REFUSE pin-entrypoint-unavailable: {PIN_VERIFIER} is missing, so "
            "the pinned OpenSpec CLI cannot be resolved and this archive would "
            "run whatever binary a shell found first. Restore the entrypoint "
            "named by `consumer_entrypoint:` in "
            "contracts/openspec-cli-pin.yaml; it is not optional tooling.")
    spec = importlib.util.spec_from_file_location(
        "openspec_cli_pin_verifier", PIN_VERIFIER)
    if spec is None or spec.loader is None:  # pragma: no cover - unreachable
        raise PinnedCliRefusal(
            "pin-entrypoint-unavailable",
            f"REFUSE pin-entrypoint-unavailable: {PIN_VERIFIER} could not be "
            "loaded as a module; the pinned CLI cannot be resolved without it.")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # pragma: no cover - a broken entrypoint
        raise PinnedCliRefusal(
            "pin-entrypoint-unavailable",
            f"REFUSE pin-entrypoint-unavailable: {PIN_VERIFIER} raised "
            f"{exc!r} while loading; the pinned CLI cannot be resolved through "
            "an entrypoint that does not import.") from exc
    _PIN_VERIFIER_MODULE = module
    return module


def pinned_openspec(path_mode: bool = False, npm: str = "npm") -> Path:
    """The pinned `openspec` EXECUTABLE, as a path, or a named refusal.

    MEMOIZED PER PROCESS, keyed by the pin file and the mode. One archive run
    resolves once, and a test session that archives several fixtures pays for
    one `npm pack` rather than one per fixture. The memo is a cache of the
    RESOLUTION, never of the verdict about the bytes: `resolve_pinned`
    re-verifies the artifact's content address on every call it is actually
    given, and the install it reuses is one named and stamped with that address.

    THE FETCH IS THROWAWAY AND THE INSTALL IS NOT, which is the split
    `resolve_pinned` is built around. The tarball lands in a
    `TemporaryDirectory` this call owns — never in a directory another tool
    also empties, because `fetch_artifact` refuses an ambiguous fetch and two
    processes sweeping one fetch directory would turn a normal run into
    `pin-unresolvable` — while the INSTALL goes to the verifier's own cache
    root, shared with `scripts/install-pinned-openspec-cli.py` rather than
    duplicated beside it, and named and stamped with the address that was
    verified.

    AND SINCE 2026-09-08 THE INSTALL IS THE PINNED DEPENDENCY CLOSURE, not a
    fresh resolution of nine caret ranges: `pinned_lockfile` and
    `verify_lockfile` are called here — the verifier's own functions, as every
    other pin question in this file is — and the bytes they return are handed to
    `resolve_pinned`, which installs them with `npm ci --ignore-scripts`. THE
    ARCHIVE ACT IS THE REASON THIS MATTERS MOST. `openspec archive` writes a
    ratified delta into canon, and until now the tree that adjudicated an
    archive could differ from the tree that adjudicated the validation that
    cleared it, on the same day, on the same machine. They are one tree now,
    because both resolve through one lockfile. No version, integrity or lockfile
    digest is written in this file; the pin is read, as always, by the
    verifier's parser.
    """
    verifier = pin_verifier()
    key = (bool(path_mode), npm, str(verifier.PIN_PATH))
    cached = _RESOLVED_OPENSPEC.get(key)
    if cached is not None:
        return cached
    try:
        pin = verifier.read_pin(verifier.PIN_PATH)
        version = verifier.pinned_version(pin)
        integrity, shasum = verifier.pinned_integrity(pin)
        package = verifier.pinned_package(pin)
        binary = verifier.pinned_binary(pin)
        lockfile, lockfile_integrity, lockfile_packages = (
            verifier.pinned_lockfile(pin, verifier.PIN_PATH))
        if path_mode:
            # The closure is still VERIFIED — that is a statement about this
            # repository's committed files — but nothing is installed through
            # it, and the message below already says `--path-mode` checks the
            # label and not the referent. The same caveat covers the tree.
            verifier.verify_lockfile(lockfile, lockfile_integrity,
                                     lockfile_packages, package, integrity)
            executable = verifier.path_executable(binary)
        else:
            lockfile_bytes = verifier.verify_lockfile(
                lockfile, lockfile_integrity, lockfile_packages, package,
                integrity)
            with tempfile.TemporaryDirectory(prefix="proposal-support-cli-") \
                    as scratch:
                executable = verifier.resolve_pinned(
                    package, version, integrity, shasum, binary, Path(scratch),
                    verifier.default_cache_root(), lockfile_bytes,
                    lockfile_integrity, npm=npm)
        reported = verifier.assert_reported_version(executable, version)
    except verifier.PinRefusal as exc:
        # Re-typed, NEVER reworded: `str(exc)` is the verifier's whole message
        # and `exc.code` its own vocabulary. This file owns the exit code it
        # maps to and nothing else about the refusal.
        raise PinnedCliRefusal(exc.code, str(exc)) from exc
    if path_mode:
        print(f"proposal-support: {package}@{reported} from PATH "
              f"({executable}). --path-mode checks the LABEL and not the "
              f"referent: these bytes were NOT hashed against the pin.",
              flush=True)
    else:
        print(f"proposal-support: {package}@{reported} from the pinned "
              f"artifact ({executable}); integrity {integrity[:23]}… verified, "
              f"over the pinned dependency closure {lockfile.name} "
              f"({lockfile_packages} packages, lockfile_integrity "
              f"{lockfile_integrity[:23]}…, installed with `npm ci "
              f"--ignore-scripts`)", flush=True)
    _RESOLVED_OPENSPEC[key] = executable
    return executable


def validate_through_the_pin(root: Path, change: str,
                             path_mode: bool = False) -> None:
    """`openspec validate <change> --strict`, run BY THE CONSUMER ENTRYPOINT.

    Called rather than re-assembled, so this archive is adjudicated by exactly
    the run the pin governs — dispositions included. `--change` narrows the scan
    to the change being archived, which is a target the entrypoint provides for
    and which decides no staleness (only an `--all` run may, and this is not
    one).

    The entrypoint's exit codes are its own and are mapped, not collapsed:
    2 is a refusal about WHICH TOOL would run and re-raises as one here; 1 is a
    finding about THIS CHANGE and becomes the `SupportError` every other gate in
    this wrapper raises.
    """
    verifier = pin_verifier()
    argv = ["--change", change, "--repo", str(root)]
    if path_mode:
        argv.append("--path-mode")
    verdict = verifier.main(argv)
    if verdict == 2:
        raise PinnedCliRefusal(
            "pin-refused",
            f"REFUSE pin-refused: the pinned OpenSpec CLI refused strict "
            f"validation of {change}; the named refusal and its remediation are "
            f"printed above. This archive is REFUSED rather than retried "
            f"against whatever `openspec` a shell would find on PATH.")
    if verdict != 0:
        raise SupportError(
            f"openspec validate {change} --strict failed through the pinned "
            f"CLI (exit {verdict}); the findings are printed above. An archive "
            f"is the act that moves a delta into canon, so it does not proceed "
            f"over a strict failure")


class ArchiveRefusal(RuntimeError):
    """The base of the exit-2 refusals THE ARCHIVE HALF ITSELF originates.

    A THIRD exit-2 family beside `OriginRetentionError` and `PinnedCliRefusal`,
    and deliberately not either of them. None of these is "this change cannot
    be archived" (exit 1, fix the packet and retry) and none is "which tool
    would archive it is unsettled": they are all "the act ran under a clock, or
    left a tree, this wrapper does not control". Which one it was is in the
    message, never in the number; all of them share exit 2 because none is the
    fix-and-retry shape.

    A BASE RATHER THAN ONE CLASS, because the post-run inspection settles two
    genuinely different questions and a caller branching on the type deserves
    to be told which. `main` catches THIS, so a subclass added later cannot
    escape the handler by being forgotten there.
    """


class ArchiveDateRefusal(ArchiveRefusal):
    """The archive date and the directory the pinned CLI named DO NOT AGREE.

    Raised for BOTH halves of the same fact: a `--date` that cannot be honoured
    (refused BEFORE the CLI runs, so nothing moves) and a directory the CLI
    named on a different day (refused AFTER it returns, with the move reverted
    when the tree allows it).
    """


class ArchiveTreeRefusal(ArchiveRefusal):
    """The CLI left a tree this wrapper will not commit and will not guess at.

    NOT A DATE FINDING, which is why it is not `ArchiveDateRefusal`: the name on
    disk may be exactly right. What is wrong is the SHAPE of the tree the child
    returned — the change standing in two places at once (a move interrupted
    part-way), or a correctly-named archive beside a non-zero exit the CLI
    itself documents as "the change remains archived".

    NEITHER ARM REVERTS. Pinned `@fission-ai/openspec@1.12.0` has three failure
    paths that end with the archive STANDING — `MoveDestinationRetainedError`
    (`dist/core/archive.js:449`, raised when the staged source could not be
    removed, "The complete destination was retained for recovery"),
    `RetirementBackupsRetainedError` (`:852`, "The change remains archived and
    each listed backup was retained for recovery") and the rollback-failure
    rethrow (`:1605-1617`, which reports that the rollback ITSELF failed) — so a
    wrapper that answered a non-zero exit by moving the destination back would
    destroy the only complete copy in exactly the cases the CLI was most careful
    to preserve it.
    """


def archive_environment() -> dict:
    """The entrypoint's environment PLUS `TZ=UTC`, for the CLI child.

    MERGED INTO `validation_environment()`, never substituted for it: that
    function settles `OPENSPEC_TELEMETRY=0` for both halves of an archive, and
    an environment assembled here from scratch would be the second answer to a
    question the entrypoint already owns.

    `TZ` is SET, not `setdefault`-ed. An operator's ambient `TZ` is precisely
    the input this refuses to trust — the archive that produced a `2026-09-07-`
    directory on a UTC 2026-09-08 (issue #790) inherited exactly such a value —
    so the one variable this wrapper does add, it decides.

    The pinned CLI has NO date option (`archive` takes `--yes --skip-specs
    --no-validate --json --store` and nothing else), so its clock is the only
    surface through which the directory name can be steered at all. That the
    steering WORKED is not assumed: `archive_change` asserts the name the CLI
    actually produced, below.
    """
    environment = dict(pin_verifier().validation_environment())
    environment["TZ"] = "UTC"
    return environment


def archive_root(root: Path) -> Path:
    return root / "openspec" / "changes" / "archive"


def archive_dir_names(root: Path) -> set[str]:
    """The names directly under `openspec/changes/archive/`, or an empty set."""
    directory = archive_root(root)
    if not directory.is_dir():
        return set()
    return {child.name for child in directory.iterdir() if child.is_dir()}


# THE PINNED CLI'S OWN PATTERN, COPIED RATHER THAN APPROXIMATED.
# `@fission-ai/openspec@1.12.0` declares it at `dist/core/archive.js:27` as
# `/^\d{4}-\d{2}-\d{2}-/` and tests the change name against it at `:1124`.
ARCHIVE_DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def archive_directory_name(change: str, archive_date: str) -> str:
    """The name the PINNED CLI will give this change's archive directory.

    COMPUTED THE WAY THE CLI COMPUTES IT, not the way this wrapper would
    prefer. A change whose id ALREADY carries a `YYYY-MM-DD-` prefix is archived
    under that id UNCHANGED — the CLI says why in its own comment
    (`archive.js:1119-1124`): "re-prefixing would stutter the name, and when the
    archive runs on a later day the folder would sort under a day on which the
    change did not happen (#1309)". It is deliberate upstream behaviour, not
    drift.

    A wrapper that always prepended today would therefore refuse a CORRECT
    archive of such a change AND revert it — a worse failure than the one this
    file exists to prevent, because the reverted archive was right. So the
    expectation is computed from the same rule the child applies, and the
    assertion below stays a claim about the CLI's CLOCK rather than about its
    naming convention.

    The consequence is stated rather than hidden: for a date-prefixed id the
    directory carries the date IN THE ID and the bundle beside it carries
    today, and those two can differ. That is the id's own doing — the estate
    has no such change today (`ls openspec/changes/archive/` is all
    `<date>-<undated-id>`) — and re-dating somebody's id is not a repair this
    wrapper is entitled to make.
    """
    if ARCHIVE_DATE_PREFIX.match(change):
        return change
    return f"{archive_date}-{change}"


def change_dir_names(root: Path) -> set[str]:
    """The ACTIVE change ids under `openspec/changes/`, `archive/` excluded."""
    directory = root / "openspec" / "changes"
    if not directory.is_dir():
        return set()
    return {child.name for child in directory.iterdir()
            if child.is_dir() and child.name != RESERVED_CHANGE_ID}


def contained_change_dir_names(root: Path) -> set[str]:
    """`change_dir_names` over the directories this repository CONTAINS.

    THE WRAPPER'S SET AND THE RESOLVER'S SET ARE NOT THE SAME QUESTION.
    `change_dir_names` answers "what did the operator's tree look like before
    the child ran", and follows a symlink as `is_dir()` does. A RESOLVER
    cannot use that set, because an uncontained entry there does not merely
    add a name — it SUPPRESSES one: `_archive_dir_carries` yields its exact
    reading to a live id of the same name, so a symlink named like a
    preserved dated identity hides that identity's real archived directory.
    MEASURED at head `018a65d3`, with `openspec/changes/2026-09-09-foo` an
    out-of-tree symlink and the packet standing at
    `archive/2026-09-09-foo`: `declared_former_ids_in_tree(root,
    "2026-09-09-foo")` returned `[]` where it returns `['old-foo']` without
    the link — an empty lineage sending the archive gate through the
    undeclared baseline. (Copilot, PR #1038 `PRRT_kwDOTAvnrs6iHxAo`.)

    `change_dir_names` itself is left alone: it is the archive wrapper's
    reading of the operator's tree, its answer is compared against directory
    names the CLI wrote, and narrowing it would change what that wrapper
    refuses on a question this one is not asking.
    """
    directory = root / "openspec" / "changes"
    if not contained_dir(root, directory):
        return set()
    return {child.name for child in directory.iterdir()
            if child.name != RESERVED_CHANGE_ID and contained_dir(root, child)}


def names_this_change(directory_name: str, change: str,
                      other_change_ids: frozenset[str] | set[str] = frozenset()
                      ) -> bool:
    """Is `directory_name` under `archive/` a directory FOR `change`?

    The question the refusal below has to answer before it moves anything: a
    directory that appeared during this run may be a WRONG-DAY copy of the
    change being archived (revert it) or a sibling lane's archive landing in a
    shared checkout (never touch it, and never tell the operator to move it
    back — it is not theirs to undo).

    ONE SHAPE IS GENUINELY AMBIGUOUS, and `other_change_ids` is what settles it.
    A directory called `2026-08-04-foo` is a wrong-day archive of `foo` AND the
    archive of a change whose id IS `2026-08-04-foo` — which
    `archive_directory_name` above exists to support, because the pinned CLI
    archives such an id under its own name unchanged. The two readings are
    indistinguishable from the name, so the name is not what decides: the ACTIVE
    change ids READ BEFORE THE CHILD RAN are. If `2026-08-04-foo` was a change
    in this repository when the run started, a new archive directory of that
    name is THAT change's archive and not a mis-dated copy of `foo`'s, and this
    run has no standing over it. (Codex round 2, P2.)

    The reading has to be taken BEFORE the child, because a sibling lane
    archiving concurrently removes its own active directory as it goes; asked
    afterwards the question would answer "no such change" for exactly the
    directory it was asked about.
    """
    if directory_name == change:
        return True
    if not ARCHIVE_DATE_PREFIX.match(directory_name):
        return False
    if directory_name in other_change_ids:
        return False
    return ARCHIVE_DATE_PREFIX.sub("", directory_name, count=1) == change


def specs_are_clean(root: Path) -> bool | None:
    """Is `openspec/specs/` free of uncommitted TRACKED changes RIGHT NOW?

    `True`/`False`, or `None` when the question cannot be asked — `root` is not
    inside a git work tree, or git could not be run. Read BEFORE the CLI is
    invoked, because it is the only moment at which the answer is about the
    operator's tree rather than about the CLI's own edits; a revert that ran
    `git checkout -- openspec/specs` over a dirty tree would discard work this
    wrapper never made.

    `--untracked-files=no`, AND THAT IS THE WHOLE POINT OF THE FLAG. The revert
    this answer gates is `git checkout -- openspec/specs`, which by definition
    cannot touch an untracked file: it restores tracked paths from the index and
    leaves everything else exactly where it is. Counting untracked files as
    "dirty" therefore disabled the revert of the CLI's TRACKED spec edits
    because of a file the revert could not have harmed — a stray scratch note
    under `openspec/specs/` was enough — and the refusal then blamed the
    operator for uncommitted work they had not done to the files in question.
    """
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain",
             "--untracked-files=no", "--", "openspec/specs"],
            check=False, capture_output=True, text=True)
    except OSError:  # pragma: no cover - git absent
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip() == ""


def specs_are_tracked(root: Path) -> bool | None:
    """Does git TRACK any file under `openspec/specs/`?

    `git checkout -- openspec/specs` exits non-zero with "pathspec ... did not
    match any file(s) known to git" when the answer is no, and a refusal that
    reported that as a FAILED revert would tell the operator their tree still
    carries edits it does not carry: everything the CLI wrote under a specs
    directory git has never seen is an untracked ADDITION, which the revert was
    never going to remove anyway and which the message already says is left in
    place. Asked before the checkout so the two readings cannot disagree.
    """
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--", "openspec/specs"],
            check=False, capture_output=True, text=True)
    except OSError:  # pragma: no cover - git absent
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip() != ""


def assert_archived_directory_date(root: Path, change: str, archive_date: str,
                                   before: set[str], archive_existed: bool,
                                   specs_clean: bool | None,
                                   returncode: int = 0,
                                   command: list[str] | None = None,
                                   other_change_ids: frozenset[str] | set[str]
                                   = frozenset()) -> None:
    """INSPECT THE TREE THE CHILD LEFT, whatever status the child returned.

    THE INSPECTION IS THE POINT, not the `TZ=UTC` above it. `TZ` is an ask of a
    child process this repository does not own; whether the child honoured it is
    a fact, and the fact is checked here rather than assumed.

    AND IT RUNS ON EVERY EXIT, which is the correction this round makes. The
    child used to be run with `check=True`, so a non-zero status raised
    `CalledProcessError` BEFORE this function was ever called — and pinned
    `@fission-ai/openspec@1.12.0` has three documented failure paths that occur
    AFTER the move, each of which ends with the archive standing
    (`MoveDestinationRetainedError` `dist/core/archive.js:449`,
    `RetirementBackupsRetainedError` `:852`, the rollback-failure rethrow
    `:1605-1617`), plus the SIGINT that leaves a half-copied split. Any of them
    left a directory on disk that nothing named and nothing date-checked, and
    the operator was told only that a subprocess had failed. The status is now
    an INPUT to the inspection rather than a reason to skip it.

    The outcomes, all of them, and each named on its own terms:

    | child | tree | outcome |
    |---|---|---|
    | 0 | `<date>-<change>/`, active path gone | ok, silently |
    | any | a directory naming `change` AND the active path still there | `archive-split`, exit 2, NOTHING touched |
    | non-zero | nothing new, active path still there | the child's own `CalledProcessError`, exit 1, tree untouched |
    | non-zero | `<date>-<change>/`, active path gone | `archive-cli-failed`, exit 2, NOTHING reverted |
    | any | a directory naming `change` on ANOTHER day | `archive-date-mismatch`, exit 2, REVERTED |
    | any | no directory naming `change` | `archive-date-mismatch`, exit 2 |

    On a date mismatch the CLI's move is REVERTED (the change directory goes
    back to its active path, and the spec edits are undone when — and only when
    — `openspec/specs/` was clean before the run) and the refusal names both
    dates. `packaged_at` is deliberately NOT unpacked: `package()` ran before
    the CLI and its bundle stays, which the refusal says out loud rather than
    leaving for the operator to discover.

    A directory that appeared during the run but names ANOTHER change is never
    reverted and never named as something to undo — in a shared checkout it is a
    sibling lane's archive landing between the two readings, and telling this
    operator to move it back would corrupt work that is not theirs.

    WHAT IS NOW TRUE, STATED EXACTLY, because the claim it replaces was not:
    every path out of `archive_change` either RETURNS having seen
    `<archive_date>-<change>/` on disk under a child that exited 0, or raises.
    Nothing else returns; there is no exit on which a directory goes unnamed.
    That is a claim about this wrapper, not about the tree afterwards — the
    split and the retained-archive arms deliberately leave a directory standing,
    and say so — and it is emphatically not "a wrong-day directory can never
    reach a commit": an operator who runs a bare `openspec archive` never came
    through here at all, and nothing in this file can reach that.
    """
    want = archive_directory_name(change, archive_date)
    created = sorted(archive_dir_names(root) - before)
    mine = [name for name in created
            if names_this_change(name, change, other_change_ids)]
    others = [name for name in created if name not in mine]
    active = root / "openspec" / "changes" / change

    # (1) THE SPLIT, FIRST AND WITHOUT A REVERT. `moveDirectory` copies and then
    # removes the staged source, so an interruption between the two — a SIGINT,
    # a full disk, the `MoveDestinationRetainedError` path itself — leaves the
    # change in TWO places. Which copy is complete is not readable off the tree,
    # and the CLI's own comment says why guessing is the wrong answer: "The
    # destination is now the only complete copy, so never erase it while trying
    # to make this failed move look atomic."
    if mine and active.exists():
        raise ArchiveTreeRefusal(
            f"REFUSE archive-split: the pinned CLI left '{change}' in TWO "
            f"places, so the archive is neither done nor undone"
            + (f" (the child exited {returncode})" if returncode else "")
            + ".\n"
            f"  active:   {active}\n"
            + "".join(f"  archived: {archive_root(root) / name}\n"
                      for name in mine)
            + "  NOTHING was moved and NOTHING was reverted: which of the two "
            "copies is complete cannot be read off the tree, and the pinned "
            "CLI's own move says why guessing is wrong — 'the destination is "
            "now the only complete copy, so never erase it while trying to "
            "make this failed move look atomic'. Compare the two by hand, keep "
            "exactly one, and re-run.")

    if want in created:
        # (2) THE NAME IS RIGHT. The date is not in question on either arm below.
        if others:
            # NAMED, NOT REFUSED. This archive is correct; a directory that
            # appeared beside it belongs to another change and this run has no
            # standing to judge it. Refusing here — which `created == [want]`
            # did — turned a correct archive into an exit 2 whose remedy told
            # the operator to move BOTH directories back.
            print(f"NOTE: {', '.join(others)} also appeared under "
                  f"openspec/changes/archive/ while this archive ran; they "
                  f"name other changes (a concurrent archive in a shared "
                  f"checkout) and are left exactly as found.", file=sys.stderr)
        if returncode == 0:
            return
        # (3) THE CLI FAILED AFTER ARCHIVING. Reverting would destroy the only
        # complete copy in precisely the three cases the CLI itself was most
        # careful to preserve it. See `ArchiveTreeRefusal`.
        raise ArchiveTreeRefusal(
            f"REFUSE archive-cli-failed: the pinned CLI exited {returncode} "
            f"AFTER archiving '{change}' — "
            f"{archive_root(root) / want} is on disk under the name this "
            f"archive date asks for and the active path is gone. THE DATE IS "
            f"NOT IN QUESTION.\n"
            "  NOT reverted, deliberately: every post-move failure this CLI "
            "documents ends with the change still archived — a staged source "
            "it could not remove, a retirement backup it could not delete, a "
            "rollback that itself failed — so this directory is the complete "
            "copy and moving it back would destroy it.\n"
            "  Read the child's own output above: it names the paths it "
            "retained. Finish what it could not, then commit the archive; "
            "nothing about the naming needs re-running.")

    # (4) THE CHILD FAILED AND MOVED NOTHING — the ordinary refusal (incomplete
    # tasks, a destination that already exists, a validation it ran itself).
    # The tree is exactly as the operator handed it over, which is the
    # fix-and-retry shape exit 1 has always meant here, so this stays the
    # child's own `CalledProcessError` rather than becoming a date finding
    # about a date nothing wrote.
    #
    # `not mine`, NOT `not created`, and the difference is a shared checkout.
    # Read globally, a sibling lane's directory landing between the two
    # readings made this condition false for a child that had moved NOTHING —
    # so the run fell through to the mismatch path, reported a date finding
    # about a directory that is not its own, and ran `git checkout --
    # openspec/specs` over a cleanliness reading taken before EITHER child ran,
    # erasing the concurrent archive's canonical spec edits. (Codex round 2,
    # P1.) The question is about THIS change, so it is asked about this
    # change's directories.
    if returncode != 0 and not mine and active.exists():
        raise subprocess.CalledProcessError(returncode, command or "openspec")

    # NAMED FROM `mine`, for the same reason: the refusal is about the
    # directory this archive did or did not produce, and quoting a sibling's
    # name as the one "the pinned CLI named" for this change is a false
    # statement about another lane's work.
    if not mine:
        got = "<no new directory>"
    elif len(mine) == 1:
        got = mine[0]
    else:
        got = ", ".join(mine)

    # RE-READ AFTER THE CHILD, and compared rather than assumed: a run that
    # began at 23:59:59 UTC took `archive_date` on one day and the child named
    # the directory on the next, and the old wording called that "the CLI's
    # clock is not UTC" — an accusation this wrapper cannot support.
    now = utc_today()
    if len(mine) > 1:
        diagnosis = ("more than one directory naming this change appeared "
                     "during this run, so which one this archive produced "
                     "cannot be read off the tree")
    elif not mine:
        diagnosis = ("the CLI created no archive directory for this change"
                     + (f" and exited {returncode}" if returncode
                        else ", and exited 0"))
    elif now != archive_date and mine[0] == f"{now}-{change}":
        diagnosis = (f"THIS RUN CROSSED MIDNIGHT UTC — the archive date was "
                     f"taken as '{archive_date}' before the CLI ran and it is "
                     f"now '{now}', which is the day the directory carries. "
                     f"The CLI's clock is not in question; the bundle's "
                     f"`packaged_at` would simply state the earlier day. "
                     f"Re-run and the two will agree")
    else:
        diagnosis = ("the CLI's clock is not UTC, or a future CLI ignored the "
                     "TZ this wrapper hands it, or the change was archived by "
                     "something other than this wrapper — this run cannot tell "
                     "which, and does not guess")
    lines = [
        f"REFUSE archive-date-mismatch: the pinned CLI named the archive "
        f"directory '{got}' but the archive date is '{archive_date}' — "
        f"{diagnosis}; nothing committed."]
    if returncode and mine:
        lines.append(
            f"  The child also exited {returncode}; its own output is above.")

    if len(mine) == 1 and (archive_root(root) / mine[0]).is_dir() \
            and not active.exists():
        shutil.move(str(archive_root(root) / mine[0]), str(active))
        lines.append(
            f"  reverted: the change directory was moved back to "
            f"openspec/changes/{change}/.")
        if not archive_existed and not archive_dir_names(root):
            try:
                archive_root(root).rmdir()
            except OSError:  # pragma: no cover - a non-empty archive root
                pass
    elif mine:
        lines.append(
            f"  NOT reverted: {len(mine)} directories naming '{change}' "
            f"appeared under openspec/changes/archive/ "
            f"({', '.join(mine)}); move them back by hand.")
    if others:
        lines.append(
            f"  LEFT ALONE: {', '.join(others)} appeared under "
            f"openspec/changes/archive/ during this run but name OTHER "
            f"changes — a concurrent archive in a shared checkout — and this "
            f"refusal does not touch them or ask you to.")

    if not mine:
        # NOTHING OF OURS MOVED, SO NOTHING OF OURS IS REVERTED. `specs_clean`
        # was read before the child; in a shared checkout it is also before a
        # SIBLING's child, and `git checkout -- openspec/specs` cannot tell the
        # two apart. A run that produced no directory of its own has no spec
        # edit of its own to undo, and reverting on its behalf would discard
        # another lane's. (Codex round 2, P1.)
        lines.append(
            "  NOT reverted: this run produced no archive directory of its "
            "own, so it has no spec edits of its own to undo — and in a shared "
            "checkout `git checkout -- openspec/specs` would discard another "
            "lane's. Read the child's output above for what it did do.")
    elif specs_clean is True and specs_are_tracked(root) is False:
        # NOT A FAILED REVERT, AND NOT REPORTED AS ONE. `git checkout --
        # openspec/specs` exits 1 with "pathspec ... did not match" where git
        # tracks nothing under that path, and printing that as "STILL IN THE
        # TREE ... undo them by hand" sent an operator hunting for tracked
        # edits that cannot exist.
        lines.append(
            "  nothing to revert under openspec/specs/: git tracks no file "
            "there, so anything the CLI wrote is an untracked addition, left "
            "in place rather than deleted.")
    elif specs_clean is True:
        # THE RETURN CODE IS READ. `check=False` keeps a failed revert from
        # replacing the refusal being raised with a `CalledProcessError` about
        # the revert — but a discarded status would let this message claim a
        # revert that did not happen (an index lock taken by another git
        # process between the cleanliness read and here is enough), and the
        # operator would then leave the CLI's spec edits in a tree they were
        # told was clean.
        completed = subprocess.run(
            ["git", "-C", str(root), "checkout", "--", "openspec/specs"],
            check=False, capture_output=True, text=True)
        if completed.returncode == 0:
            lines.append(
                "  reverted: the CLI's edits under openspec/specs/ "
                "(`git checkout -- openspec/specs`). Files it ADDED there are "
                "untracked and are left in place rather than deleted.")
        else:
            detail = " ".join(
                (completed.stderr or completed.stdout or "").split())[:200]
            lines.append(
                f"  NOT reverted: `git checkout -- openspec/specs` FAILED "
                f"(exit {completed.returncode}: {detail or 'no output'}), so "
                f"the CLI's edits under openspec/specs/ are STILL IN THE TREE. "
                f"Undo them by hand before re-running.")
    elif specs_clean is False:
        lines.append(
            "  NOT reverted: openspec/specs/ carried uncommitted changes to "
            "TRACKED files BEFORE this archive, so the CLI's spec edits were "
            "left alone — reverting them would have discarded work this "
            "wrapper did not make. Undo them by hand.")
    else:
        lines.append(
            "  NOT reverted: openspec/specs/ could not be read through git "
            "(no work tree), so the CLI's spec edits, if any, were left "
            "alone.")

    if (active / "supporting-docs.tar.gz").is_file():
        lines.append(
            "  NOT reverted: the supporting-docs bundle was written before the "
            "CLI ran and is still there; the support folder was not restored.")
    lines.append(
        f"  The archive is REFUSED rather than committed under a name that "
        f"states a day it did not happen on. Re-run once the CLI names "
        f"'{want}'; this wrapper already hands it TZ=UTC.")
    raise ArchiveDateRefusal("\n".join(lines))


def archive_change(root: Path, change: str, packaged_at: str,
                   final_import_complete: bool, yes: bool,
                   path_mode: bool = False) -> None:
    directory = active_change_dir(root, change)
    gate = origin_errors(root, directory, strict=True)
    if gate:
        raise SupportError("origin gate: " + "; ".join(gate))
    # SHAPE FIRST, THEN RETENTION, and in that order on purpose: the retention
    # comparison reads the declaration as a block of lines and as a mapping,
    # and both of those presume the packet parses and declares an origin at
    # all — which is exactly what the call above has just established.
    retention = origin_retention_errors(root, directory, change=change)
    if retention:
        raise OriginRetentionError("\n".join(retention))
    tasks = directory / "tasks.md"
    if tasks.is_file() and re.search(r"^- \[ \]", tasks.read_text(), re.M):
        raise SupportError("change has incomplete tasks")
    # RESOLVED BEFORE ANYTHING IS VALIDATED, so that a pin that cannot be
    # satisfied is reported as the named refusal it is — `pin-integrity-
    # mismatch`, `pin-unresolvable`, `pin-version-mismatch` — rather than as the
    # entrypoint's undifferentiated exit 2 further down. It is also the honest
    # order: the first question an archive asks is which tool will perform it.
    #
    # THE ENTRYPOINT RESOLVES AGAIN FOR ITS OWN HALF, and that is not waste to
    # be optimised away: it is a separate tool with its own contract, and one
    # that trusted a caller's handed-in executable would be a pinned validator
    # running a binary it did not verify. The two share the verifier's cache
    # root, so the second resolution reuses the first install and costs one
    # `npm pack` — and the artifact is re-hashed both times, which is
    # `resolve_pinned`'s property and the reason the reuse is not a shortcut.
    executable = pinned_openspec(path_mode=path_mode)
    validate_through_the_pin(root, change, path_mode=path_mode)
    # PACKAGING IS FOR A CHANGE THAT HAS SUPPORTING DOCUMENTS, and only for one.
    # The promoted rule says so in its first clause — "An OpenSpec change WITH
    # proposal supporting documents SHALL NOT archive until ... the supporting
    # folder has been converted into a deterministic bundle" — and `verify`
    # already reads it that way on both sides: it checks an active change's
    # support only `if (directory / "supporting-docs").exists()`, and an
    # archived one's bundle only when a manifest or bundle is present, falling
    # through to the origin check alone otherwise.
    #
    # This wrapper did not, and called `package()` unconditionally, so a
    # staged-origin change that legitimately never took its topic with it could
    # not be archived through the sanctioned path at all — it died on
    # "supporting-docs folder not found". SIXTEEN archived staged-origin changes
    # already had exactly that shape before this one — `add-ideation-dashboard`,
    # `add-workbench-branch-sessions`, `add-openxwallet` (whose promoted
    # capabilities relocated to `opensoft/openXwallet` at `contract-v2.0`;
    # the archived PACKET stays here and is what this count is about),
    # `add-repository-lens`,
    # `add-session-notebook-reconciliation`, … — against fifteen WITH a bundle,
    # so the bundle-less shape is the MAJORITY of staged origins, not an edge.
    # (An earlier draft of this comment said "fifteen": that is the count of the
    # COMPLEMENT, the with-bundle set. Recount by listing archived changes whose
    # `.openspec.yaml` says `kind: staged` and partitioning on the presence of
    # `supporting-docs.tar.gz`.) What was missing was the wrapper's ability to
    # produce the shape, which pushed the operator toward a bare
    # `openspec archive` and around this gate entirely.
    #
    # Found while archiving `add-doxbench-editing-phase-a`, whose task 9.2
    # deliberately KEPT the topic staged for Phase B.
    # `.exists()`, not `.is_dir()`, so this predicate is the SAME one `verify`
    # applies (F3). A `supporting-docs` that exists but is not a directory is a
    # broken change either way; what matters is that the two readers of "does
    # this change have supporting documents" cannot disagree.
    if (directory / "supporting-docs").exists():
        package(root, change, packaged_at, archived=False,
                final_import_complete=final_import_complete, apply=True)
    elif final_import_complete:
        raise SupportError(
            "--final-import-complete records a NotebookLM source import for a "
            "support bundle, and this change has no supporting-docs folder")
    else:
        print(f"NO SUPPORTING DOCS {directory} (origin retained, nothing to "
              "package)")
    command = [str(executable), "archive", change]
    if yes:
        command.append("--yes")
    # READ BEFORE THE CLI RUNS, both of them, because both questions are about
    # the tree the operator handed over rather than about what the CLI did to
    # it: which archive directories already existed (so the one the CLI creates
    # can be named exactly), and whether `openspec/specs/` was clean (so a
    # revert can only ever undo the CLI's own edits).
    existing = archive_dir_names(root)
    existed = archive_root(root).is_dir()
    clean = specs_are_clean(root)
    # AND THE ACTIVE CHANGE IDS, for the same reason and at the same moment: a
    # concurrent lane archiving `2026-08-04-foo` removes that active directory
    # as it goes, and the question "is this new archive directory a wrong-day
    # copy of MY change, or that change's own archive?" can only be answered
    # from the corpus as it stood BEFORE either child ran.
    other_ids = change_dir_names(root) - {change}
    # The entrypoint's own environment MERGED WITH `TZ=UTC`, so the two halves
    # of an archive share whatever `validation_environment()` settles
    # (`OPENSPEC_TELEMETRY=0` is currently the whole of it) rather than one of
    # them assembling an answer of its own — plus the timezone, because the
    # directory name this call produces comes from the child's clock and from
    # nothing else (issue #790). An earlier draft of this comment said the
    # merge exists "so this process does not archive under one environment
    # having validated under another", which stopped being true the moment
    # `TZ` was added: the archive child now runs under an environment the
    # validation child did not.
    #
    # `check=False`, AND DELIBERATELY. `check=True` raised before the
    # inspection below could run, so every one of the pinned CLI's documented
    # after-the-move failures — and a SIGINT part-way through the copy — left a
    # directory nothing named and nothing date-checked. The status is handed to
    # the inspection as an input instead; `assert_archived_directory_date`
    # re-raises the child's own `CalledProcessError` for the ordinary case
    # where it failed having moved nothing, so exit 1 still means what it
    # always meant.
    completed = subprocess.run(command, cwd=root, check=False,
                               env=archive_environment())
    assert_archived_directory_date(root, change, packaged_at, existing,
                                   existed, clean,
                                   returncode=completed.returncode,
                                   command=command,
                                   other_change_ids=other_ids)


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path, help="OpenSpec repository root")
    sub = ap.add_subparsers(dest="command", required=True)

    move = sub.add_parser("transition")
    move.add_argument("change")
    move.add_argument("source", help="path below ideation/staging")
    move.add_argument("--file", action="append", default=[])
    move.add_argument("--workspace")
    move.add_argument(
        "--date", default=utc_today(),
        help="the transition date recorded in the support manifest "
             "(default: TODAY IN UTC, not the machine's local date)")
    move.add_argument("--archived", action="store_true")
    move.add_argument("--apply", action="store_true")

    pack = sub.add_parser("package")
    pack.add_argument("change")
    pack.add_argument(
        "--date", default=utc_today(),
        help="the bundle's `packaged_at` (default: TODAY IN UTC, not the "
             "machine's local date)")
    pack.add_argument("--archived", action="store_true")
    pack.add_argument("--final-import-complete", action="store_true")
    pack.add_argument("--apply", action="store_true")

    check = sub.add_parser("verify")
    check.add_argument("change", nargs="?")

    adhoc = sub.add_parser("declare-adhoc")
    adhoc.add_argument("change")
    adhoc.add_argument("--reason", required=True)
    # NEITHER PAIR IS ARGPARSE-REQUIRED, because exactly one of them is
    # (`add-drafted-proposal-origin`): an approved exception passes
    # --approved-by/--approved-on, an unapproved draft passes
    # --proposed-by/--proposed-on, and `write_origin_block` refuses a call
    # that completes neither pair with a message naming both shapes.
    adhoc.add_argument("--approved-by")
    adhoc.add_argument("--approved-on")
    adhoc.add_argument("--proposed-by")
    adhoc.add_argument("--proposed-on")
    adhoc.add_argument("--slug")

    # THE ORIGIN-RETENTION REFUSAL, ON THE HELP SURFACE. An operator holding
    # an owner's acceptance found nothing here and nothing in the refusal but
    # "no bypass flag" (codeXfactory/codexFactory #318). Deliberately NAMES NO
    # FLAG, because there is none to name and
    # `test_the_archive_subcommand_offers_no_bypass_flag` reads this text.
    archive = sub.add_parser(
        "archive",
        epilog=(
            "ORIGIN RETENTION: a packet whose `origin:` block moved after its "
            "ratifying commit is REFUSED (exit 2), and the requirement makes "
            "restoring or accepting that mutation a contested-class act "
            "requiring an explicit disposition. There is no flag for it. The "
            "two repairs are (1) RESTORE the ratified declaration in the "
            "packet, which needs no record, and (2) ACCEPT it with an "
            f"owner-attributed entry in {ORIGIN_DISPOSITIONS_REL} "
            f"(schema_version: {ORIGIN_DISPOSITIONS_SCHEMA_VERSION}, "
            f"kind: {ORIGIN_DISPOSITIONS_KIND}) naming the ratifying commit, "
            "the accepted mutating commit, the keys that moved, the "
            "authority, the date, the verbatim word and the citation — after "
            "which the accepted declaration is the one this gate compares "
            "against. The refusal itself prints the record's path and every "
            "field an entry needs."))
    archive.add_argument("change")
    # DEFAULT `None`, resolved in `main` — not `utc_today()` here — so that
    # "the operator named a date" and "the operator named nothing" are
    # distinguishable. They are treated differently: a date that is not today
    # in UTC is REFUSED rather than stamped, because the pinned CLI has no date
    # option and would name the directory from its own clock regardless, and a
    # `packaged_at` that disagreed with the directory beside it is exactly the
    # split issue #790 is about.
    archive.add_argument(
        "--date", default=None,
        help="the archive date: the bundle's `packaged_at` AND the date the "
             "archive directory must carry (default: TODAY IN UTC). The "
             "pinned OpenSpec CLI has no date option — it names "
             "openspec/changes/archive/<date>-<change> from its own clock, "
             "which this wrapper fixes to UTC — so a --date that is not "
             "today in UTC cannot be honoured and is REFUSED (exit 2) before "
             "the CLI runs, rather than stamped onto a bundle beside a "
             "directory naming a different day")
    archive.add_argument("--final-import-complete", action="store_true")
    archive.add_argument("--yes", action="store_true")
    # THE ENTRYPOINT'S OWN ESCAPE, PASSED THROUGH — not a bypass invented here.
    # It uses the `openspec` on PATH and refuses unless that binary reports the
    # pinned version, so it checks the label rather than the referent; there is
    # deliberately no flag that skips the pin altogether.
    archive.add_argument(
        "--path-mode", action="store_true",
        help=("resolve the CLI from PATH, refusing unless it reports the "
              "pinned version; for an offline developer, never for a "
              "governed archive"))
    return ap


def main() -> None:
    args = parser().parse_args()
    try:
        if args.command == "transition":
            transition(args.root, args.change, args.source, args.file,
                       args.workspace, args.date, args.archived, args.apply)
        elif args.command == "package":
            package(args.root, args.change, args.date, args.archived,
                    args.final_import_complete, args.apply)
        elif args.command == "declare-adhoc":
            directory = active_change_dir(args.root.resolve(), args.change)
            slug = args.slug or args.change.removeprefix("add-")
            # THE ID DATE IS THE DECLARATION DATE AND IT NEVER MOVES AGAIN.
            # An origin declared unapproved keeps the date it was drafted on
            # when its approval later lands: the durable id is part of the
            # identity the support manifest repeats, and rewriting it at
            # approval is exactly the mutation the origin-mismatch check
            # reports. Approval is an ADDITION to this block, never a
            # re-minting of it.
            stamp = args.approved_on or args.proposed_on
            if not stamp:
                raise SupportError(
                    "declare-adhoc needs --approved-on (an approved "
                    "exception) or --proposed-on (an unapproved draft)")
            origin = {
                "kind": "ad_hoc",
                "id": f"{args.root.resolve().name}:adhoc:{stamp}-{slug}",
                "reason": args.reason,
            }
            for field in APPROVAL_FIELDS + DRAFTING_FIELDS:
                value = getattr(args, field, None)
                if value:
                    origin[field] = value
            write_origin_block(directory, origin, stamp)
            print(f"ad-hoc origin declared for {args.change}")
        elif args.command == "verify":
            errors = verify(args.root, args.change)
            if errors:
                raise SupportError("\n".join(errors))
            print("proposal support verification ok")
        else:
            # DERIVED ONCE, and compared against itself rather than recomputed:
            # two `utc_today()` calls straddling midnight would refuse a run
            # whose own default was correct when it was taken.
            today = utc_today()
            # `is None`, NOT `or`. `--date ''` is a value the operator
            # TYPED, and `args.date or today` silently replaced it with today —
            # a flag reported as honoured when nothing read it. An empty string
            # is not today in UTC, so it now takes the refusal every other
            # unhonourable date takes.
            stamp = today if args.date is None else args.date
            if stamp != today:
                raise ArchiveDateRefusal(
                    f"REFUSE archive-date-not-utc-today: --date '{stamp}' is "
                    f"not today in UTC ('{today}'). The pinned OpenSpec CLI "
                    f"has no date option — it names "
                    f"openspec/changes/archive/<date>-<change> from its own "
                    f"clock, which this wrapper fixes to UTC — so an archive "
                    f"cannot be stamped with any other day: the bundle's "
                    f"`packaged_at` would state one date and the directory "
                    f"beside it another. Re-run without --date, or pass "
                    f"'{today}'.")
            archive_change(args.root.resolve(), args.change, stamp,
                           args.final_import_complete, args.yes,
                           args.path_mode)
    except OriginRetentionError as exc:
        # EXIT 2, NOT 1: THE ORIGIN-RETENTION GATE REFUSED. Every arm of it
        # lands here — a declaration that moved after ratification, no
        # ratifying commit to compare against, an unreadable history — and
        # none of them is the "fix the tree and retry" shape exit 1 has always
        # meant for this script. So the status says "retention could not be
        # established" and no more; a caller reads WHICH arm from the message,
        # and only the mutation arm is the contested-class refusal that goes
        # to a disposition. Printed here rather than carried in `SystemExit`
        # because that argument doubles as the exit status, and an int is the
        # whole point. (argparse spends 2 on its own usage errors, which this
        # shares rather than fights: a usage error never reaches this
        # handler.) `archive_change` raises this BEFORE the pin is ever
        # resolved — retention is checked first, so this arm is reached
        # first when both could apply.
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
    except ArchiveRefusal as exc:
        # EXIT 2, THE THIRD FAMILY OF THREE. See `ArchiveRefusal`: the archive
        # happened (or would happen) under a clock — or left a tree — this
        # wrapper does not control, which is neither "fix the packet" (1) nor a
        # pin question. The BASE is caught, so `ArchiveDateRefusal` and
        # `ArchiveTreeRefusal` cannot diverge in status by one of them being
        # forgotten here.
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
    except PinnedCliRefusal as exc:
        # EXIT 2, AND ALSO NOT 1, BUT A DIFFERENT REFUSAL FROM THE ONE ABOVE.
        # Exit 1 here has always meant "this change is not archivable"; this is
        # "which tool would archive it is unsettled", which is the exit the pin
        # verifier and the pinned installer both already use. The message is
        # the verifier's own, printed verbatim. This and `OriginRetentionError`
        # share the number because neither is the "fix the packet and retry"
        # shape exit 1 means — one says the origin comparison could not be
        # trusted, the other says the tool that would adjudicate the change
        # could not be resolved — and which one it was is in the message,
        # never in the number.
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
    except (SupportError, subprocess.CalledProcessError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
