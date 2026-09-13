#!/usr/bin/env python3
"""Move staged proposal support and preserve it through OpenSpec archive."""

from __future__ import annotations

import argparse
from collections.abc import Iterator
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


def active_change_dir(root: Path, change: str) -> Path:
    # Change ids are plain slugs; anything with path syntax would let a
    # caller-supplied name traverse outside openspec/changes/.
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", change):
        raise SupportError(f"invalid change name: {change}")
    path = root / "openspec" / "changes" / change
    if not path.is_dir() or change == "archive":
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
#
# AND THE WHOLE LINEAGE IS ASKED, NOT ONE PATH (issue #1003). That refusal
# can only be raised for commits the walk ENUMERATES, and the enumeration is
# path-limited to the name the tree spells today — so a ratified packet
# renamed and un-ratified in one commit, renamed AGAIN while draft, and
# re-ratified under its third name put the guilty hop outside the
# enumeration entirely, and the walk accepted the re-ratification exactly as
# it did before #833 (measured on the reproduction in #1003, routed there
# from PR #999's review bench). The hops are now followed backwards through
# `renamed_from` — renames only, never copies, so a lawful fork-by-copy
# stays archivable — and every commit of every earlier name is asked the
# same question with the name it had then. The baseline is still resolved
# under the current name alone, because there is still nothing to re-base
# onto.
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

    THE UNREADABLE-HISTORY ARM IS RAISED THERE TOO where the walk is what
    could not read it (issue #1003): resolving a packet's rename lineage asks
    git for an earlier name's history, and a git that declines to answer
    leaves the same impossible comparison rather than a finding to collect.
    The same arm reached through `origin_retention_errors` — no repository,
    no readable blob at the baseline — is still assembled there, unchanged.
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


def renamed_from(root: Path, revision: str, rel: str, *,
                 kinds: str = "RC") -> str | None:
    """The path `rel` was RENAMED OR COPIED FROM at `revision`, or None when it
    came into being there outright (or was merely modified there).

    `kinds` NARROWS WHICH PAIRING COUNTS, for the one caller that needs a
    RENAME (`R`, the former path GONE) and not a COPY (`C`, the former path
    still standing) — issue #849. Default `"RC"` is every existing behaviour
    in this docstring, unchanged.

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
    <revision>^{commit}`, which also peels an annotated tag). Both callers
    today pass a full hash straight out of `git log --format=%H`,
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
        return None
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
        if not rows or rows[0].strip() != revision:
            continue
        for row in rows[1:]:
            fields = row.split("\t")
            if (len(fields) == 3 and fields[0][:1] in kinds
                    and fields[2] == rel):
                return fields[1]
    return None


def ratified_under_a_former_path(root: Path, revision: str, rel: str, *,
                                 kinds: str = "RC") -> str | None:
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
    ever reached. Since issue #1003 the commits it asks are the packet's
    WHOLE RENAME LINEAGE's — every name it has had, each asked with the name
    it had then — but the question asked at each of them is the one stated
    here, unwidened: `_lineage_commits` changes which commits reach this
    function, never what it answers.

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
    """
    former = renamed_from(root, revision, rel, kinds=kinds)
    if former is None:
        return None
    before = git_show_text(root, f"{revision}^", former)
    if before is not None and declares_ratified(before):
        return former
    return None


def _commits_touching(root: Path, rel: str,
                      bounds: list[str] | None = None) -> list[str] | None:
    """The commits that touched `rel`, OLDEST FIRST, read from `bounds` when
    given (the revisions the history is walked back from, so a predecessor's
    commits can be asked for as they stood BEFORE the hop that renamed it).

    `--full-history --topo-order --reverse` for the reason `ratifying_commit`
    states and re-states: MISSING the earliest ratified blob is the failure
    that matters, so history simplification must not prune a commit that
    changed the file on a merged branch and a rebased clock must not reorder
    anything. NOT `--follow`, which is the other way this could have been
    written and the reason it is not: `--follow` walks the SIMPLIFIED history
    of one path, so making it the enumeration would trade that property away
    to buy the rename hops — and the hops are bought instead, without the
    trade, by `_incarnation` asking `renamed_from` one commit at a time.

    NONE IS NOT AN EMPTY HISTORY, and keeping them apart is the guard's
    business (raised by the review bench on PR #1024). An empty list is git's
    ANSWER — nothing earlier touched this name. None is git DECLINING TO
    ANSWER: an unreadable object, a revision that does not resolve, a
    checkout carrying only part of the history. The caller that resolves the
    baseline treats None as it always treated a failed `git log` (no
    ratifying commit, so the gate's own `not ratified` refusal, never a
    pass), and the lineage walk treats it as CANNOT RUN rather than as "there
    is nothing earlier here" — which would switch the guard off exactly where
    it is meant to bite.
    """
    arguments = ["--full-history", "--topo-order", "--reverse", "--format=%H"]
    arguments.extend(bounds or [])
    listed = subprocess.run(  # NOSONAR: argv is allowlisted; shell is disabled
        ["git", "-C", str(root.resolve()), "log", *arguments, "--", rel],
        capture_output=True, text=True, check=False,
    )
    if listed.returncode != 0:
        return None
    return listed.stdout.split()


def _parents(root: Path, revision: str) -> list[str] | None:
    """`revision`'s parents — ALL of them — or None when git could not answer.

    ALL of them, rather than the `<revision>^` that names the first parent
    only: a predecessor's history has to be read from every side a merge
    brought together, or a rename whose source was ratified on the second
    parent would be read as a draft (raised by the review bench on PR #1024).
    MEASURED, because the shape matters more than the fear: the pairing this
    walk follows is never reported AT a merge commit — `git log --follow -1
    <merge> -- <path>` answers with the BRANCH's own rename commit rather
    than the merge, and `renamed_from` accepts a pairing only where git's
    `%H` is the revision asked about — so the merged rename is asked about at
    the branch commit that made it, where the parent read is exact, and every
    hop bounded here has one parent in practice. The list is used because it
    is the honest shape of the question, not because a merge hop has been
    seen.
    """
    listed = subprocess.run(  # NOSONAR: argv is allowlisted; shell is disabled
        ["git", "-C", str(root.resolve()), "rev-list", "--parents", "-n", "1",
         "--end-of-options", revision],
        capture_output=True, text=True, check=False,
    )
    if listed.returncode != 0:
        return None
    fields = listed.stdout.split()
    return fields[1:]


def _unreadable_lineage(change: str, rel: str,
                        revision: str) -> OriginRetentionError:
    """The refusal for a lineage git would not read — the same CANNOT RUN
    shape as every other arm of this gate, raised for the same reason.

    The walk was asking whether an EARLIER name of this packet already
    declared `Status: ratified` when it was renamed, and git declined to
    answer. An unanswered question is not a clean answer: reading the silence
    as "there is nothing earlier" would switch the guard off precisely where
    it is meant to bite — in a checkout whose history is not all there
    (raised by the review bench on PR #1024).
    """
    short = revision[:12]
    return OriginRetentionError(
        f"REFUSE origin-retention-history-unreadable: {change}: the "
        f"origin-retention walk CANNOT RUN. Resolving this packet's rename "
        f"lineage needed the history of `{rel}` as it stood before {short}, "
        f"and git would not read it — an unreadable object, or a checkout "
        f"carrying only part of the history. The walk therefore cannot tell "
        f"an earlier name that was ALREADY RATIFIED when it was renamed from "
        f"one that was still a draft, so the baseline was never established "
        f"and this refuses rather than passing on a silence (issues #833, "
        f"#1003). Re-run the archive in a checkout carrying the packet's "
        f"whole history.")


def _moved_packet_refusal(change: str, rel: str, path: str, former: str,
                          revision: str) -> OriginRetentionError:
    """The `origin-retention-path-moved` refusal, in ONE place for the two
    callers that raise it.

    `path` is the name the packet occupied AT `revision`; `rel` is the one it
    occupies now. They are the same string for every hop that touched the
    name the tree spells today — which was every hop this refusal could reach
    before issue #1003 — so that wording is unchanged to the byte, and the
    lineage case ADDS a sentence rather than rewording the rest: an operator
    who has read this refusal before should not have to re-read it to find
    what is different, and what is different is only that the hop sits
    earlier in the packet's rename lineage than the commits that touched its
    current name.
    """
    short = revision[:12]
    message = (
        f"REFUSE origin-retention-path-moved: {change}: the "
        f"origin-retention walk CANNOT RUN. Commit {short} carries "
        f"`{path}` in from `{former}`, which already declared "
        f"`Status: ratified` at {short}^ — so this change was "
        f"ratified under a path that is not the one it occupies now "
        f"(`{rel}`), and {short} is a MOVE OR COPY of that ratified "
        f"packet rather than its ratification, whatever `{path}` "
        f"itself declares as of {short} — and if `{former}` still "
        f"stands in the tree then the packet was COPIED to this id "
        f"rather than moved to it, which git pairs the same way and "
        f"which leaves the same baseline unestablishable. Taking "
        f"{short} or any later commit under `{path}` as the baseline "
        f"would compare the packet against itself and wave through "
        f"every origin mutation made between the real ratification "
        f"and it — the `ORIGIN RETAINED` measured on issue #777, "
        f"the failure issue #833 names, and the same failure "
        f"reached through an un-ratifying rename (issue #849). "
        f"Nothing in this corpus declares a FORMER ID, so the "
        f"baseline cannot be established from history alone and "
        f"this walk refuses rather than re-basing onto that "
        f"commit: archive {change} under the id it was ratified "
        f"with, or land the former-id declaration (a later packet) "
        f"before renaming a ratified change. Renaming a DRAFT "
        f"change is unaffected.")
    if path != rel:
        message += (
            f" AND THE HOP IS NOT AT THIS PACKET'S CURRENT NAME: `{path}` "
            f"was itself renamed onward to `{rel}` later, so the move above "
            f"sits EARLIER IN THE RENAME LINEAGE than any commit that "
            f"touched the name the tree spells today — the chain shape issue "
            f"#1003 names, which a walk enumerating only `{rel}`'s own "
            f"history never reaches.")
    return OriginRetentionError(message)


def _refuse_if_moved(root: Path, change: str, rel: str, path: str,
                     revision: str) -> bool:
    """Put ONE commit to the walk's question, and answer whether the packet's
    own blob declares `ratified` there.

    RAISES when `revision` brought the packet into `path` from a name that
    already declared `Status: ratified` at `revision^` — with `kinds="RC"`
    where the blob at `path` is itself ratified (a MOVE OR COPY landing
    already-ratified, issue #833) and `kinds="R"` where it is not (a true
    rename, the former path gone, issue #849; a COPY there is the lawful
    fork-by-copy `ratified_under_a_former_path` protects). Both readings are
    that function's — this is the pair of them asked at one commit, WITH THE
    PATH THAT COMMIT SPELLED, so that the current name's loop in
    `ratifying_commit` and the lineage beside it cannot drift apart about
    what the question is.
    """
    blob = git_show_text(root, revision, path)
    ratified_here = blob is not None and declares_ratified(blob)
    former = ratified_under_a_former_path(
        root, revision, path, kinds="RC" if ratified_here else "R")
    if former is not None:
        raise _moved_packet_refusal(change, rel, path, former, revision)
    return ratified_here


def _incarnation(root: Path, change: str, rel: str,
                 hop: str) -> list[str]:
    """The commits of the INCARNATION of `rel` that `hop` renamed away, oldest
    first — not every commit that ever spelled that name.

    A PATH IS NOT AN IDENTITY, and a reused one must not contaminate the
    packet holding it now (raised by the review bench on PR #1024). Where an
    intermediate name was occupied by a DIFFERENT packet before — moved away
    or deleted, the name later taken by a new draft — the whole history of
    that name carries the old occupant's hops, and a lineage that read them
    would refuse this packet for somebody else's move, permanently, on a gate
    with no bypass flag (#690). So the history is trimmed at the commit that
    brought THIS incarnation into being: reading newest first, commits are
    kept until one is reached where the name stood in no parent, and that one
    is the last kept.

    TRIMMING LOSES NO HOP, which is why it is safe as well as necessary: git
    pairs a rename when the destination is ADDED, so only the commit that
    brought the name into being can carry a predecessor at all — a commit
    that found the name already standing in its parent is a modification and
    reports none. The question is still asked at every commit kept, and a
    pairing found at any of them still refuses.

    A BOUND GIT WILL NOT READ IS CANNOT RUN rather than an empty history, for
    the reason `_commits_touching` states.
    """
    parents = _parents(root, hop)
    if parents is None:
        raise _unreadable_lineage(change, rel, hop)
    if not parents:
        # A pairing cannot be found at a parentless commit — git detects a
        # rename against a parent's tree — so this is the belt rather than
        # the mechanism: a hop reached here always has one.
        return []
    revisions = _commits_touching(root, rel, parents)
    if revisions is None:
        raise _unreadable_lineage(change, rel, hop)
    kept: list[str] = []
    for revision in reversed(revisions):
        kept.append(revision)
        ancestors = _parents(root, revision)
        if ancestors is None:
            raise _unreadable_lineage(change, rel, revision)
        if not any(git_show_text(root, ancestor, rel) is not None
                   for ancestor in ancestors):
            break
    kept.reverse()
    return kept


def _lineage_commits(root: Path, change: str,
                     rel: str) -> Iterator[tuple[str, str]]:
    """Every commit the walk must ask, as `(path, revision)` pairs, OLDEST
    FIRST across the packet's whole rename lineage (issue #1003).

    THE OUTER WALK FOLLOWS NO RENAME, and that is the gap this closes. The
    enumeration is `git log -- <one path>`, which lists the commits that
    touched THE NAME THE TREE SPELLS TODAY and nothing else, so #849's
    closure — asking every commit the walk visits, not only the ones whose
    blob declares `ratified` — reached exactly ONE hop. Measured on the shape
    routed from PR #999's review bench: after `ratify r → rename+un-ratify
    r→s → rename s→t while draft → ratify t`, the commits under `t` BEGIN at
    the `s→t` hop, whose former blob (`s`) is a draft and refuses nothing,
    and the re-ratification under `t` carries no pairing of its own — so the
    walk took that as its baseline, later than the real ratification, waving
    through every mutation in between. The `r→s` hop, where the ratified
    packet actually moved, was never enumerated at all.

    SO THE LINEAGE IS ASSEMBLED HOP BY HOP, out of `renamed_from` rather than
    out of a `--follow` enumeration, which would have traded away the
    `--full-history` property the walk depends on. The hops themselves are
    therefore still git's own detection through `--follow` — the mode NO GIT
    CONFIG CAN SWITCH OFF (see `renamed_from`, and the fixture carrying the
    hostile config) — while each name in the lineage is enumerated exactly as
    the current one always was.

    PREDECESSORS COME FIRST in the order returned, so a refusal names the
    EARLIEST hop that moved an already-ratified packet rather than whichever
    hop the enumeration happened to reach first. That is the commit an
    operator can act on: it is where the packet left the name it was ratified
    under.

    RENAMES ONLY (`kinds="R"`), never copies, which is the line #999 drew for
    the same reason. A COPY leaves the source standing, so following one
    backwards would walk into the SOURCE packet's history and take its
    ratification as this packet's problem — refusing a packet honestly
    authored as a draft copy of a ratified one, the fork-by-copy this gate
    must not trap.

    ITERATIVE, WITH A `seen` MEMO, rather than recursive: the lineage is
    finite (every hop is bounded by a strictly earlier commit, and no commit
    is its own ancestor), so no cap on its depth is needed and none is
    imposed — a cap would be a refusal for a packet renamed often but
    lawfully, and "renaming a DRAFT change is unaffected" has no number in it
    (raised by the review bench on PR #1024).

    LAZY, so that the caller's early return still costs what it used to. The
    walk stops at the first commit that declares `ratified` under the current
    name, and the ordinary packet — never renamed, ratified early, with
    commits after — must not pay for enumerating a lineage nobody reads.
    Measured: yielding as they are found rather than returning a finished
    list took `tests/proposal-support` from 98s back to the 40s it ran in
    before the lineage existed.

    THE CURRENT NAME'S OWN SEGMENT IS NOT TRIMMED, unlike the predecessors':
    the walk has always asked every commit that touched the name the tree
    spells today, whatever occupied it before, and narrowing that here would
    be a behaviour change this issue did not ask for.

    WHAT THIS DOES NOT REACH, stated rather than implied: an un-ratification
    landing in its OWN commit BEFORE the rename leaves every hop moving a
    DRAFT, so no hop answers the question and the later re-ratification is
    still the baseline. Whether a re-ratification after a return to draft is
    lawfully a NEW baseline is a governance question rather than this
    function's; #1003 names the shape whose un-ratification rides IN the
    rename commit; and today's answer for the other shape is pinned by
    `test_an_un_ratification_before_the_rename_is_a_stated_gap` rather than
    changed here.
    """
    seen: set[tuple[str, str]] = set()
    # each frame is [path, commits oldest-first, index, descended already?]
    frames: list[list] = [[rel, _commits_touching(root, rel) or [], 0, False]]
    while frames:
        path, revisions, index, descended = frames[-1]
        if index >= len(revisions):
            frames.pop()
            continue
        revision = revisions[index]
        if not descended:
            frames[-1][3] = True
            former = renamed_from(root, revision, path, kinds="R")
            if former is not None and (former, revision) not in seen:
                seen.add((former, revision))
                frames.append([former,
                               _incarnation(root, change, former, revision),
                               0, False])
                continue
        frames[-1][2] = index + 1
        frames[-1][3] = False
        yield path, revision


def ratifying_commit(root: Path, change: str) -> str | None:
    """The FIRST commit whose `openspec/changes/<change>/proposal.md` declares
    `Status: ratified`, or None when no commit in history does.

    A line-by-line walk over the commits that touched that ONE path, oldest
    first, reading each blob — not `git log -S`, which would match the string
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

    The path read is the ACTIVE one even when the packet being gated is an
    archived one: the archive move renames it, and the history before that
    rename is where the ratification lives.

    AND WHEN THE PACKET'S OWN NAME MOVED, THIS REFUSES (issue #833). One path
    is walked, so a ratified change whose directory was RENAMED afterwards has
    no history under its new name before the rename — and the first ratified
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
    and there is nothing to re-base ONTO: no former-id declaration exists in
    this corpus (that is the successor packet), so a baseline under a name the
    tree no longer spells cannot be established at all.

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

    AND THE COMMITS VISITED ARE THE WHOLE LINEAGE'S, NOT ONLY THOSE THAT
    TOUCHED THE NAME THE TREE SPELLS TODAY (issue #1003). Asking every
    visited commit left the ENUMERATION path-limited, and a path-limited
    `git log` follows no rename, so the closure above reached exactly ONE
    hop: put a lawful draft rename between the move and the current name —
    `ratify r → rename+un-ratify r→s → rename s→t while draft → ratify t` —
    and the walk for `t` begins at the `s→t` hop, whose former blob is a
    draft, while the `r→s` hop that moved the ratified packet is never
    enumerated. So the commits put to the question are now assembled by
    `_lineage_commits` — the current name's own, and behind each hop the
    commits of the incarnation that hop renamed away, oldest first, renames
    only — and the question asked at each of them is the one this docstring
    already states.

    THE BASELINE STILL COMES FROM THE CURRENT NAME ALONE. A ratification
    found under a former name is a refusal and never a commit to re-base
    onto, for the reason this docstring already gives: nothing here declares
    a former id, so a baseline under a name the tree no longer spells cannot
    be established at all.
    """
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", change):
        raise SupportError(f"invalid change name: {change}")
    rel = f"openspec/changes/{change}/proposal.md"
    for path, revision in _lineage_commits(root, change, rel):
        ratified_here = _refuse_if_moved(root, change, rel, path, revision)
        if ratified_here and path == rel:
            return revision
    return None


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
    rel = f"openspec/changes/{change}/.openspec.yaml"
    at_mutation_text = git_show_text(root, mutation_at, rel)
    at_mutation = origin_block_lines(at_mutation_text)
    if at_mutation is None:
        return [f"{where} names a `mutation_at` ({mutation_at[:12]}) at "
                f"which {rel} declares no origin, so there is no declaration "
                f"to accept"]
    at_ratification_text = git_show_text(root, ratified_at, rel)
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
    change = change or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", directory.name)
    if is_declared_sentinel(repo_revision(root)):
        return [f"origin retention: {change}: this repository's history is "
                "unreadable, so the declaration present at ratification "
                "cannot be resolved — the archive gate cannot verify origin "
                "retention"]
    revision = ratifying_commit(root, change)
    if revision is None:
        return [f"origin retention: {change}: not ratified — no commit in "
                f"history carries `Status: ratified` in "
                f"openspec/changes/{change}/proposal.md, so there is no "
                "declaration to retain. Commit the ratification before "
                "archiving."]
    short = revision[:12]
    was_text = git_show_text(
        root, revision, f"openspec/changes/{change}/.openspec.yaml")
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
              f"ratifying commit {short} declares no origin (pre-contract "
              "packet); presence and shape are still gated")
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
            was_text = git_show_text(
                root, revision, f"openspec/changes/{change}/.openspec.yaml")
            was = origin_block_lines(was_text)
    if now is None:
        errors.append(
            f"origin retention: {change}: the origin declaration present at "
            f"the ratifying commit {short} is GONE from the packet being "
            "archived")
    elif now != was:
        keys = _changed_keys(_origin_mapping(was_text),
                             _origin_mapping(now_text))
        detail = "\n".join(difflib.unified_diff(
            was, now,
            fromfile=f"{short}:openspec/changes/{change}/.openspec.yaml",
            tofile=_relative(packet_file, root), lineterm="", n=1))
        errors.append(
            f"origin retention: {change}: the origin declaration differs "
            f"from the one this change was ratified over (ratifying commit "
            f"{short})"
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
              f"ratifying commit {short})")
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
            if child.is_dir() and child.name != "archive"}


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
