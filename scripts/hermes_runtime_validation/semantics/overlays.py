"""Exact Git-object semantics for single-file pins and directory overlays."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import Any

import yaml

from scripts.hermes_runtime_validation.content import (
    ContentResolutionError,
    ResolvedGitContent,
    normalize_repository_path,
    resolve_git_object,
)
from scripts.hermes_runtime_validation.loader import _StrictJsonLoader, _check_json_value


Resolver = Callable[[str | os.PathLike[str], str, str], ResolvedGitContent]
Finding = dict[str, str]

OVERLAY_SCHEMA_ID = (
    "https://xforge.us/schemas/openxfactory/hermes-runtime/v2/"
    "overlay-manifest.schema.yaml"
)
OVERLAY_SCHEMA_VERSION = 1

_COMMIT = re.compile(r"[0-9a-f]{40}")
_OBJECT_ID = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
_DIGEST = re.compile(r"sha256:[0-9a-f]{64}")
_REPOSITORY = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?/"
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?"
)
_CLOSED_PATH = re.compile(r"[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*")
_SCHEMA_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9+._:/-]{0,511}")

_SINGLE_PIN_FIELDS = frozenset(
    {"repository", "commit", "path", "digest", "schema_id", "schema_version"}
)
_OVERLAY_PIN_FIELDS = frozenset(
    {
        "repository",
        "commit",
        "overlay_root",
        "manifest_path",
        "manifest_digest",
        "schema_id",
        "schema_version",
    }
)
_MANIFEST_FIELDS = frozenset(
    {"schema_version", "kind", "overlay_root", "files", "exclusions"}
)


@dataclass(frozen=True)
class _TreeEntry:
    mode: str
    object_type: str
    object_id: str
    path: str

    @property
    def is_regular(self) -> bool:
        return self.object_type == "blob" and self.mode in {"100644", "100755"}


class _GitTreeError(RuntimeError):
    pass


def _finding(code: str, path: str, message: str) -> Finding:
    return {
        "code": code,
        "severity": "error",
        "case_id": "",
        "path": path,
        "message": message,
    }


def _sorted(findings: list[Finding]) -> list[Finding]:
    return sorted(findings, key=lambda finding: (finding["path"], finding["code"]))


def _exact_commit(value: object) -> str | None:
    return value if isinstance(value, str) and _COMMIT.fullmatch(value) else None


def _canonical_path(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    try:
        normalized = normalize_repository_path(value)
    except ContentResolutionError:
        return None
    return normalized if _CLOSED_PATH.fullmatch(normalized) else None


def _canonical_repository(value: object) -> str | None:
    return value if isinstance(value, str) and _REPOSITORY.fullmatch(value) else None


def _git(checkout: Path, *arguments: str) -> bytes:
    environment = os.environ.copy()
    for name in (
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_REPLACE_REF_BASE",
    ):
        environment.pop(name, None)
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    try:
        result = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(checkout), *arguments],
            capture_output=True,
            check=False,
            timeout=30,
            env=environment,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise _GitTreeError("Git is unavailable") from exc
    if result.returncode != 0:
        raise _GitTreeError("exact Git object is unavailable")
    return result.stdout


def _exact_commit_tree(checkout: Path, commit: str) -> str:
    try:
        resolved_commit = _git(
            checkout, "rev-parse", "--verify", f"{commit}^{{commit}}"
        ).decode("ascii").strip()
        tree_oid = _git(
            checkout, "rev-parse", "--verify", f"{commit}^{{tree}}"
        ).decode("ascii").strip()
    except UnicodeDecodeError as exc:
        raise _GitTreeError("Git returned a malformed object identifier") from exc
    if resolved_commit != commit or _OBJECT_ID.fullmatch(tree_oid) is None:
        raise _GitTreeError("the supplied object is not the exact commit")
    return tree_oid


def _parse_tree_record(record: bytes) -> _TreeEntry:
    try:
        metadata, encoded_path = record.split(b"\t", 1)
        mode, object_type, object_id = metadata.decode("ascii").split(" ", 2)
        path = encoded_path.decode("utf-8")
    except (UnicodeDecodeError, ValueError) as exc:
        raise _GitTreeError("Git returned a malformed tree entry") from exc
    if _OBJECT_ID.fullmatch(object_id) is None:
        raise _GitTreeError("Git returned a malformed object identifier")
    return _TreeEntry(mode, object_type, object_id, path)


def _tree_entry(checkout: Path, commit: str, path: str) -> tuple[str, _TreeEntry]:
    tree_oid = _exact_commit_tree(checkout, commit)
    listing = _git(
        checkout,
        "ls-tree",
        "-z",
        "--full-tree",
        commit,
        "--",
        f":(literal){path}",
    )
    records = [record for record in listing.split(b"\0") if record]
    if len(records) != 1:
        raise _GitTreeError("exact Git path is unavailable")
    entry = _parse_tree_record(records[0])
    if entry.path != path:
        raise _GitTreeError("Git path resolution was not exact")
    return tree_oid, entry


def _tree_entries(
    checkout: Path, commit: str, overlay_root: str
) -> tuple[str, list[_TreeEntry]]:
    tree_oid = _exact_commit_tree(checkout, commit)
    root_record = _git(
        checkout,
        "ls-tree",
        "-z",
        "--full-tree",
        commit,
        "--",
        f":(literal){overlay_root}",
    )
    roots = [record for record in root_record.split(b"\0") if record]
    if len(roots) != 1:
        raise _GitTreeError("overlay_root is not an exact Git tree")
    root_entry = _parse_tree_record(roots[0])
    if (
        root_entry.path != overlay_root
        or root_entry.mode != "040000"
        or root_entry.object_type != "tree"
    ):
        raise _GitTreeError("overlay_root is not an exact Git tree")

    listing = _git(
        checkout,
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        commit,
        "--",
        f":(literal){overlay_root}",
    )
    entries = [
        _parse_tree_record(record)
        for record in listing.split(b"\0")
        if record
    ]
    if any(
        entry.path != overlay_root
        and not entry.path.startswith(f"{overlay_root}/")
        for entry in entries
    ):
        raise _GitTreeError("Git path resolution escaped the overlay root")
    return tree_oid, entries


def _repository_finding(value: object, expected_repository: str | None) -> Finding | None:
    repository = _canonical_repository(value)
    expected = _canonical_repository(expected_repository)
    if repository is None or expected is None or repository != expected:
        return _finding(
            "HCS-PIN-REPOSITORY",
            "repository",
            "pin repository must equal the canonical repository selected by the caller",
        )
    return None


def _schema_findings(
    pin: Mapping[str, Any],
    *,
    expected_schema_id: str | None,
    expected_schema_version: int | None,
) -> list[Finding]:
    schema_id = pin.get("schema_id")
    schema_version = pin.get("schema_version")
    has_id = schema_id is not None
    has_version = schema_version is not None
    if has_id != has_version:
        return [
            _finding(
                "HCS-PIN-SCHEMA",
                "schema_id",
                "schema_id and schema_version must be supplied together",
            )
        ]
    if has_id and (
        not isinstance(schema_id, str)
        or _SCHEMA_ID.fullmatch(schema_id) is None
        or type(schema_version) is not int
        or schema_version < 1
    ):
        return [
            _finding(
                "HCS-PIN-SCHEMA",
                "schema_id",
                "pin schema identity and version are not canonical",
            )
        ]
    if expected_schema_id is not None and schema_id != expected_schema_id:
        return [
            _finding(
                "HCS-PIN-SCHEMA",
                "schema_id",
                "pin schema identity does not match the required contract",
            )
        ]
    if expected_schema_version is not None and schema_version != expected_schema_version:
        return [
            _finding(
                "HCS-PIN-SCHEMA",
                "schema_version",
                "pin schema version does not match the required contract",
            )
        ]
    return []


def _verified_resolution_finding(
    resolver: Resolver,
    *,
    checkout: str | os.PathLike[str],
    commit: str,
    path: str,
    digest: str,
    tree_oid: str,
    tree_entry: _TreeEntry,
    digest_code: str,
) -> tuple[ResolvedGitContent | None, Finding | None]:
    try:
        resolved = resolver(checkout, commit, path)
    except Exception as exc:  # resolver is an injected dependency boundary
        return None, _finding(
            "HCS-PIN-CONTENT", path,
            f"content resolver failed closed: {type(exc).__name__}: {exc}",
        )
    if not isinstance(resolved, ResolvedGitContent):
        return None, _finding(
            "HCS-PIN-CONTENT", path, "resolver returned an invalid result"
        )
    if (
        resolved.path != path
        or resolved.commit_oid != commit
        or resolved.tree_oid != tree_oid
        or resolved.git_mode != tree_entry.mode
        or resolved.blob_oid != tree_entry.object_id
        or not tree_entry.is_regular
    ):
        return None, _finding(
            "HCS-PIN-CONTENT",
            path,
            "resolver metadata does not match the exact commit tree entry",
        )
    if not isinstance(resolved.data, bytes):
        return None, _finding(
            "HCS-PIN-CONTENT", path, "resolver bytes are unavailable"
        )
    actual_digest = f"sha256:{hashlib.sha256(resolved.data).hexdigest()}"
    if resolved.digest != actual_digest or actual_digest != digest:
        return None, _finding(
            digest_code,
            path,
            "resolved raw Git blob bytes do not match the pinned SHA-256 digest",
        )
    return resolved, None


def validate_single_file_pin(
    pin: Mapping[str, Any],
    *,
    checkout: str | os.PathLike[str],
    expected_repository: str | None = None,
    resolver: Resolver = resolve_git_object,
    expected_schema_id: str | None = None,
    expected_schema_version: int | None = None,
) -> list[Finding]:
    """Validate one regular-file pin against one exact commit and raw digest."""

    unknown = set(pin) - _SINGLE_PIN_FIELDS
    if unknown:
        return [
            _finding(
                "HCS-PIN-SCHEMA",
                "pin",
                f"single-file pin contains unknown fields {sorted(unknown)}",
            )
        ]
    repository_finding = _repository_finding(pin.get("repository"), expected_repository)
    if repository_finding:
        return [repository_finding]
    commit = _exact_commit(pin.get("commit"))
    if commit is None:
        return [
            _finding(
                "HCS-PIN-EXACT-COMMIT",
                "commit",
                "assembly pins require one exact lowercase 40-hex commit",
            )
        ]
    path = _canonical_path(pin.get("path"))
    if path is None:
        return [_finding("HCS-PIN-PATH", "path", "pin path is not canonical")]
    digest = pin.get("digest")
    if not isinstance(digest, str) or _DIGEST.fullmatch(digest) is None:
        return [_finding("HCS-PIN-DIGEST", "digest", "pin digest is not canonical")]
    schema_findings = _schema_findings(
        pin,
        expected_schema_id=expected_schema_id,
        expected_schema_version=expected_schema_version,
    )
    if schema_findings:
        return schema_findings
    try:
        tree_oid, tree_entry = _tree_entry(Path(checkout), commit, path)
    except _GitTreeError as exc:
        return [_finding("HCS-PIN-CONTENT", path, str(exc))]
    _, finding = _verified_resolution_finding(
        resolver,
        checkout=checkout,
        commit=commit,
        path=path,
        digest=digest,
        tree_oid=tree_oid,
        tree_entry=tree_entry,
        digest_code="HCS-PIN-DIGEST",
    )
    return [finding] if finding else []


def validate_overlay_manifest(
    manifest: Mapping[str, Any],
    *,
    checkout: str | os.PathLike[str],
    commit: str,
    expected_repository: str | None = None,
    resolver: Resolver = resolve_git_object,
) -> list[Finding]:
    """Validate content-only manifest membership at an external exact pin."""

    if _canonical_repository(expected_repository) is None:
        return [
            _finding(
                "HCS-PIN-REPOSITORY",
                "repository",
                "a canonical repository binding is required",
            )
        ]
    exact_commit = _exact_commit(commit)
    if exact_commit is None:
        return [
            _finding(
                "HCS-PIN-EXACT-COMMIT",
                "commit",
                "overlay validation requires one external exact commit",
            )
        ]
    missing = _MANIFEST_FIELDS - set(manifest)
    unknown = set(manifest) - _MANIFEST_FIELDS
    if missing or unknown:
        return [
            _finding(
                "HCS-OVERLAY-SCHEMA",
                "manifest",
                f"manifest fields are not closed; missing={sorted(missing)} unknown={sorted(unknown)}",
            )
        ]
    if manifest.get("schema_version") != 1 or manifest.get("kind") != "HermesRuntimeOverlayManifest":
        return [
            _finding(
                "HCS-OVERLAY-SCHEMA",
                "manifest",
                "manifest schema_version or kind is invalid",
            )
        ]
    overlay_root = _canonical_path(manifest.get("overlay_root"))
    if overlay_root is None:
        return [
            _finding(
                "HCS-OVERLAY-PATH",
                "overlay_root",
                "overlay root is not a canonical repository-relative path",
            )
        ]

    raw_files = manifest.get("files")
    raw_exclusions = manifest.get("exclusions")
    if not isinstance(raw_files, list) or not raw_files or not isinstance(raw_exclusions, list):
        return [
            _finding(
                "HCS-OVERLAY-MEMBERSHIP",
                "files",
                "files must be a non-empty array and exclusions must be an array",
            )
        ]

    findings: list[Finding] = []
    declared: list[tuple[str, str]] = []
    for index, entry in enumerate(raw_files):
        if not isinstance(entry, Mapping) or set(entry) != {"path", "digest"}:
            findings.append(
                _finding("HCS-OVERLAY-MEMBERSHIP", f"files/{index}", "invalid file entry")
            )
            continue
        path = _canonical_path(entry.get("path"))
        digest = entry.get("digest")
        if path is None or not path.startswith(f"{overlay_root}/"):
            findings.append(
                _finding(
                    "HCS-OVERLAY-PATH",
                    f"files/{index}/path",
                    "inventoried path must be canonical and below overlay_root",
                )
            )
            continue
        if not isinstance(digest, str) or _DIGEST.fullmatch(digest) is None:
            findings.append(
                _finding("HCS-OVERLAY-DIGEST", path, "inventoried digest is not canonical")
            )
            continue
        declared.append((path, digest))
    if findings:
        return _sorted(findings)

    declared_paths = [path for path, _ in declared]
    if declared_paths != sorted(declared_paths, key=lambda path: path.encode("utf-8")):
        findings.append(
            _finding(
                "HCS-OVERLAY-BYTE-ORDER",
                "files",
                "overlay inventory must be bytewise sorted by UTF-8 path bytes",
            )
        )
    if len(declared_paths) != len(set(declared_paths)):
        findings.append(
            _finding(
                "HCS-OVERLAY-EXTRA-MEMBER",
                "files",
                "overlay inventory contains a duplicate path",
            )
        )

    exclusion_paths: list[str] = []
    generated_count = 0
    for index, exclusion in enumerate(raw_exclusions):
        if not isinstance(exclusion, Mapping) or set(exclusion) != {"kind", "path"}:
            findings.append(
                _finding(
                    "HCS-OVERLAY-EXCLUSION",
                    f"exclusions/{index}",
                    "invalid exclusion entry",
                )
            )
            continue
        kind = exclusion.get("kind")
        path = _canonical_path(exclusion.get("path"))
        if path is None or not path.startswith(f"{overlay_root}/"):
            findings.append(
                _finding(
                    "HCS-OVERLAY-EXCLUSION",
                    f"exclusions/{index}/path",
                    "excluded path must be canonical and below overlay_root",
                )
            )
            continue
        allowed = kind == "gitkeep" and PurePosixPath(path).name == ".gitkeep"
        if kind == "generated_digest_inventory":
            generated_count += 1
            allowed = PurePosixPath(path).parent.as_posix() == overlay_root
        if not allowed:
            findings.append(
                _finding(
                    "HCS-OVERLAY-EXCLUSION",
                    path,
                    "only .gitkeep and one colocated generated digest inventory may be excluded",
                )
            )
            continue
        exclusion_paths.append(path)
    if generated_count > 1 or len(exclusion_paths) != len(set(exclusion_paths)):
        findings.append(
            _finding(
                "HCS-OVERLAY-EXCLUSION",
                "exclusions",
                "overlay exclusions must be unique with at most one generated inventory",
            )
        )

    try:
        tree_oid, entries = _tree_entries(Path(checkout), exact_commit, overlay_root)
    except _GitTreeError as exc:
        findings.append(_finding("HCS-PIN-CONTENT", overlay_root, str(exc)))
        return _sorted(findings)

    nonregular = sorted(entry.path for entry in entries if not entry.is_regular)
    for path in nonregular:
        findings.append(
            _finding(
                "HCS-OVERLAY-NONREGULAR",
                path,
                "overlay trees cannot contain symlinks, gitlinks, or other non-regular entries",
            )
        )
    entry_by_path = {entry.path: entry for entry in entries}
    actual_regular = {entry.path for entry in entries if entry.is_regular}
    excluded = set(exclusion_paths)
    for path in sorted(excluded - actual_regular, key=lambda item: item.encode("utf-8")):
        findings.append(
            _finding(
                "HCS-OVERLAY-EXCLUSION",
                path,
                "excluded path is not a regular file in the exact Git tree",
            )
        )

    expected = actual_regular - excluded
    declared_set = set(declared_paths)
    for path in sorted(expected - declared_set, key=lambda item: item.encode("utf-8")):
        findings.append(
            _finding(
                "HCS-OVERLAY-MISSING-MEMBER",
                path,
                "regular Git-tree member is missing from the overlay inventory",
            )
        )
    for path in sorted(declared_set - expected, key=lambda item: item.encode("utf-8")):
        findings.append(
            _finding(
                "HCS-OVERLAY-EXTRA-MEMBER",
                path,
                "inventoried member is absent from the exact regular-file tree",
            )
        )

    for path, digest in declared:
        entry = entry_by_path.get(path)
        if entry is None or not entry.is_regular:
            continue
        _, finding = _verified_resolution_finding(
            resolver,
            checkout=checkout,
            commit=exact_commit,
            path=path,
            digest=digest,
            tree_oid=tree_oid,
            tree_entry=entry,
            digest_code="HCS-OVERLAY-DIGEST",
        )
        if finding:
            findings.append(finding)
    return _sorted(findings)


def _strict_manifest_from_bytes(data: bytes) -> Mapping[str, Any] | None:
    try:
        document = yaml.load(data.decode("utf-8"), Loader=_StrictJsonLoader)
        _check_json_value(document)
    except (UnicodeError, yaml.YAMLError, ValueError):
        return None
    return document if isinstance(document, Mapping) else None


def validate_pinned_overlay(
    pin: Mapping[str, Any],
    *,
    checkout: str | os.PathLike[str],
    expected_repository: str | None = None,
    resolver: Resolver = resolve_git_object,
) -> list[Finding]:
    """Resolve, strict-load, and validate one externally pinned overlay manifest."""

    missing = _OVERLAY_PIN_FIELDS - set(pin)
    unknown = set(pin) - _OVERLAY_PIN_FIELDS
    if missing or unknown:
        return [
            _finding(
                "HCS-PIN-SCHEMA",
                "overlay_manifest_pin",
                f"overlay pin fields are not closed; missing={sorted(missing)} unknown={sorted(unknown)}",
            )
        ]
    repository_finding = _repository_finding(pin.get("repository"), expected_repository)
    if repository_finding:
        return [repository_finding]
    commit = _exact_commit(pin.get("commit"))
    if commit is None:
        return [
            _finding(
                "HCS-PIN-EXACT-COMMIT",
                "commit",
                "overlay pin requires one exact lowercase 40-hex commit",
            )
        ]
    overlay_root = _canonical_path(pin.get("overlay_root"))
    manifest_path = _canonical_path(pin.get("manifest_path"))
    if overlay_root is None or manifest_path is None:
        return [
            _finding(
                "HCS-PIN-PATH",
                "overlay_manifest_pin",
                "overlay root and manifest path must be canonical",
            )
        ]
    if manifest_path == overlay_root or manifest_path.startswith(f"{overlay_root}/"):
        return [
            _finding(
                "HCS-OVERLAY-PIN-CIRCULAR",
                "manifest_path",
                "manifest path must be outside overlay_root to prevent self-inventory",
            )
        ]
    manifest_digest = pin.get("manifest_digest")
    if not isinstance(manifest_digest, str) or _DIGEST.fullmatch(manifest_digest) is None:
        return [
            _finding(
                "HCS-PIN-DIGEST",
                "manifest_digest",
                "manifest digest is not canonical",
            )
        ]
    schema_findings = _schema_findings(
        pin,
        expected_schema_id=OVERLAY_SCHEMA_ID,
        expected_schema_version=OVERLAY_SCHEMA_VERSION,
    )
    if schema_findings:
        return schema_findings
    try:
        tree_oid, manifest_entry = _tree_entry(Path(checkout), commit, manifest_path)
    except _GitTreeError as exc:
        return [_finding("HCS-PIN-CONTENT", manifest_path, str(exc))]
    resolved_manifest, resolution_finding = _verified_resolution_finding(
        resolver,
        checkout=checkout,
        commit=commit,
        path=manifest_path,
        digest=manifest_digest,
        tree_oid=tree_oid,
        tree_entry=manifest_entry,
        digest_code="HCS-PIN-DIGEST",
    )
    if resolution_finding:
        return [resolution_finding]
    assert resolved_manifest is not None
    manifest = _strict_manifest_from_bytes(resolved_manifest.data)
    if manifest is None:
        return [
            _finding(
                "HCS-OVERLAY-SCHEMA",
                manifest_path,
                "exact manifest blob is not strict JSON-compatible YAML",
            )
        ]
    if manifest.get("overlay_root") != overlay_root:
        return [
            _finding(
                "HCS-OVERLAY-PIN-MISMATCH",
                "overlay_root",
                "external overlay pin root does not match the exact manifest blob",
            )
        ]
    return validate_overlay_manifest(
        manifest,
        checkout=checkout,
        commit=commit,
        expected_repository=expected_repository,
        resolver=resolver,
    )
