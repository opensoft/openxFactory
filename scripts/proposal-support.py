#!/usr/bin/env python3
"""Move staged proposal support and preserve it through OpenSpec archive."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess

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
    result = subprocess.run(  # NOSONAR: argv is allowlisted; shell is disabled
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else "uncommitted"


def git_blob_sha256(root: Path, revision: str, source_path: str) -> str | None:
    if revision == "uncommitted":
        return None
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", revision):
        raise SupportError(f"invalid repository revision: {revision}")
    source = PurePosixPath(source_path)
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
            # that silently does not run is worse than one that fails.
            header = staging_header_id(root / str(opath).replace("\\", "/"))
            if header is not None and header != oid:
                errors.append(
                    f"{name}: staging folder {opath!r} exists but its "
                    f"`Staging ID:` ({header}) does not equal the declared "
                    f"origin id ({oid})")
    else:
        for field in ("reason", "approved_by", "approved_on"):
            if not str(origin.get(field) or "").strip():
                errors.append(f"{name}: ad-hoc origin lacks required "
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
        body.append(f"  approved_by: {origin['approved_by']}")
        body.append(f"  approved_on: {origin['approved_on']}")
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
    entries = [
        {
            "path": str(mapping[path].relative_to(destination)),
            "sha256": sha256_bytes(rendered[path]),
            "source_path": str(path.relative_to(root)),
            "source_sha256": sha256_file(path),
            "source_snapshot_path": str(
                snapshots[path].relative_to(destination)
            ),
        }
        for path in selected
    ]
    if revision != "uncommitted":
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
        "remaining_paths": [str(path.relative_to(root)) for path in remaining],
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
        path = ensure_inside(support / entry["path"], support, "manifest path")
        if not path.is_file():
            errors.append(f"missing support file: {path}")
        elif sha256_file(path) != entry.get("sha256"):
            errors.append(f"support checksum mismatch: {path}")
        source_sha256 = entry.get("source_sha256")
        snapshot_valid = False
        snapshot_path = entry.get("source_snapshot_path")
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
        if source_sha256 and revision != "uncommitted":
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
    separate rule, and a shared one: both count the three real endings below, but
    this module cannot import the primitive, so the agreement is held by
    `test_the_mover_agrees_with_the_other_fence_implementations` and
    `test_the_movers_line_split_is_the_three_real_endings_and_nothing_else`
    rather than by this sentence.

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
    expected = {entry["path"]: entry["sha256"] for entry in manifest.get("files", [])}
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


def archive_change(root: Path, change: str, packaged_at: str,
                   final_import_complete: bool, yes: bool) -> None:
    directory = active_change_dir(root, change)
    gate = origin_errors(root, directory, strict=True)
    if gate:
        raise SupportError("origin gate: " + "; ".join(gate))
    tasks = directory / "tasks.md"
    if tasks.is_file() and re.search(r"^- \[ \]", tasks.read_text(), re.M):
        raise SupportError("change has incomplete tasks")
    subprocess.run(
        ["openspec", "validate", change, "--strict"], cwd=root, check=True
    )
    package(root, change, packaged_at, archived=False,
            final_import_complete=final_import_complete, apply=True)
    command = ["openspec", "archive", change]
    if yes:
        command.append("--yes")
    subprocess.run(command, cwd=root, check=True)


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
    adhoc.add_argument("--approved-by", required=True)
    adhoc.add_argument("--approved-on", required=True)
    adhoc.add_argument("--slug")

    archive = sub.add_parser("archive")
    archive.add_argument("change")
    archive.add_argument("--date", default=date.today().isoformat())
    archive.add_argument("--final-import-complete", action="store_true")
    archive.add_argument("--yes", action="store_true")
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
            write_origin_block(directory, {
                "kind": "ad_hoc",
                "id": f"{args.root.resolve().name}:adhoc:"
                      f"{args.approved_on}-{slug}",
                "reason": args.reason,
                "approved_by": args.approved_by,
                "approved_on": args.approved_on,
            }, args.approved_on)
            print(f"ad-hoc origin declared for {args.change}")
        elif args.command == "verify":
            errors = verify(args.root, args.change)
            if errors:
                raise SupportError("\n".join(errors))
            print("proposal support verification ok")
        else:
            archive_change(args.root.resolve(), args.change, args.date,
                           args.final_import_complete, args.yes)
    except (SupportError, subprocess.CalledProcessError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
