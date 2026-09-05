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
from datetime import date


LINK_RE = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")


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
# --------------------------------------------------------------------------


class OriginRetentionError(SupportError):
    """The archive gate's origin-retention refusal — ANY arm of it.

    Three conditions raise it, and the exception is deliberately one rather
    than three: the declaration moved after ratification, no ratifying commit
    exists to compare against, or the history that holds the baseline could
    not be read. What they share is the only thing a caller can act on — the
    packet CANNOT BE SHOWN to still carry the origin it was ratified over —
    and none of them is the "fix the tree and retry" shape that `SupportError`
    means everywhere else in this script.

    A subclass rather than a message, so the CLI can answer with its own exit
    status (2) and a script can branch on "retention could not be established"
    without parsing prose. WHICH arm it was is in the message, never in the
    number. The mutation arm alone carries the further consequence the
    requirement names — restoring or accepting it is a contested-class act
    requiring an explicit disposition — and the finding for that arm says so
    in its own text.
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
    """
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", change):
        raise SupportError(f"invalid change name: {change}")
    rel = f"openspec/changes/{change}/proposal.md"
    listed = subprocess.run(  # NOSONAR: argv is allowlisted; shell is disabled
        ["git", "-C", str(root.resolve()), "log", "--full-history",
         "--topo-order", "--reverse", "--format=%H", "--", rel],
        capture_output=True, text=True, check=False,
    )
    if listed.returncode != 0:
        return None
    for revision in listed.stdout.split():
        blob = git_show_text(root, revision, rel)
        if blob is not None and declares_ratified(blob):
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
    errors: list[str] = []
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
    # RATIFYING DECLARATION is what catches the lockstep edit that moves both
    # copies together and leaves them agreeing with each other about the wrong
    # thing.
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
            for field in fields:
                if field in was_map and m_origin.get(field) != was_map[field]:
                    errors.append(
                        f"origin retention: {change}: support manifest origin "
                        f"`{field}` ({m_origin.get(field)!r}) is not the one "
                        f"declared at ratification ({was_map[field]!r}) — "
                        f"{manifest_path.name}")
    if errors:
        errors.append(
            "restoring or accepting a post-ratification origin mutation is a "
            "contested-class act requiring an explicit disposition "
            "(`release-realization` § \"Origin retention at archive\"); this "
            "gate has no bypass flag")
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
        if path_mode:
            executable = verifier.path_executable(binary)
        else:
            with tempfile.TemporaryDirectory(prefix="proposal-support-cli-") \
                    as scratch:
                executable = verifier.resolve_pinned(
                    package, version, integrity, shasum, binary, Path(scratch),
                    verifier.default_cache_root(), npm=npm)
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
              f"artifact ({executable}); integrity {integrity[:23]}… verified",
              flush=True)
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
    # The entrypoint's own environment, so this process does not archive under
    # one environment having validated under another; `OPENSPEC_TELEMETRY=0` is
    # the only thing it settles, and it settles it for both halves.
    subprocess.run(command, cwd=root, check=True,
                   env=pin_verifier().validation_environment())


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path, help="OpenSpec repository root")
    sub = ap.add_subparsers(dest="command", required=True)

    move = sub.add_parser("transition")
    move.add_argument("change")
    move.add_argument("source", help="path below ideation/staging")
    move.add_argument("--file", action="append", default=[])
    move.add_argument("--workspace")
    move.add_argument("--date", default=date.today().isoformat())
    move.add_argument("--archived", action="store_true")
    move.add_argument("--apply", action="store_true")

    pack = sub.add_parser("package")
    pack.add_argument("change")
    pack.add_argument("--date", default=date.today().isoformat())
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

    archive = sub.add_parser("archive")
    archive.add_argument("change")
    archive.add_argument("--date", default=date.today().isoformat())
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
            archive_change(args.root.resolve(), args.change, args.date,
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
