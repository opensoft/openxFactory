from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Final, override

from scripts.hermes_runtime_validation.content import (
    ContentResolutionError,
    ResolvedGitContent,
    resolve_git_object,
)

from .model import MAX_DISCOVERY_FILES, MAX_INPUT_BYTES, Finding

UNTRUSTED_GIT_ENVIRONMENT: Final = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
    "GIT_REPLACE_REF_BASE",
)


@dataclass(frozen=True, slots=True)
class SourceCoordinates:
    revision: str
    path: str
    expected_digest: str


@dataclass(slots=True)  # noqa: MUTABLE_OK
class TrustedSnapshotError(Exception):
    """Trusted-snapshot failure with mutable exception traceback state."""

    repository: Path
    detail: str

    @override
    def __str__(self) -> str:
        return f"{self.repository}: {self.detail}"


@dataclass(frozen=True, slots=True)
class TrustedSnapshot:
    repository: Path
    repository_id: str
    commit: str

    def __post_init__(self) -> None:
        if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", self.repository_id) is None:
            raise TrustedSnapshotError(
                self.repository, "trusted repository ID must be an owner/name pair"
            )
        if re.fullmatch(r"[0-9a-f]{40}", self.commit) is None:
            raise TrustedSnapshotError(
                self.repository, "trusted commit must be a full lowercase SHA-1"
            )
        if (
            _git(
                self.repository, "cat-file", "-e", f"{self.commit}^{{commit}}"
            ).returncode
            != 0
        ):
            raise TrustedSnapshotError(
                self.repository, "trusted commit is unavailable in repository"
            )


def read_git_blob(
    repository_root: Path, source: SourceCoordinates, label: str
) -> tuple[bytes | None, list[Finding]]:
    spec = f"{source.revision}:{source.path}"
    try:
        resolved = _resolve_bounded_git_object(
            repository_root,
            source.revision,
            source.path,
        )
    except ContentResolutionError as error:
        raise TrustedSnapshotError(repository_root, f"cannot resolve {spec}") from error
    if resolved.digest != source.expected_digest:
        return None, [Finding("authority-source", label, f"digest mismatch for {spec}")]
    return resolved.data, []


def source_ancestry_findings(
    snapshot: TrustedSnapshot, revision: str, label: str
) -> list[Finding]:
    if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
        return [
            Finding(
                "authority-source-ancestry",
                label,
                "source revision must be a full lowercase SHA-1",
            )
        ]
    available = _git(
        snapshot.repository,
        "cat-file",
        "-e",
        f"{revision}^{{commit}}",
    )
    if available.returncode != 0:
        return [
            Finding(
                "authority-source-ancestry",
                label,
                "source revision is unavailable in the trusted repository",
            )
        ]
    completed = _git(
        snapshot.repository,
        "merge-base",
        "--is-ancestor",
        revision,
        snapshot.commit,
    )
    if completed.returncode == 1:
        return [
            Finding(
                "authority-source-ancestry",
                label,
                "source revision is not an ancestor of the trusted commit",
            )
        ]
    if completed.returncode != 0:
        raise TrustedSnapshotError(
            snapshot.repository, "cannot verify trusted source ancestry"
        )
    return []


def trusted_family_paths(snapshot: TrustedSnapshot) -> list[str]:
    completed = _git(
        snapshot.repository,
        "ls-tree",
        "-r",
        "--name-only",
        "-z",
        snapshot.commit,
        "--",
        "contracts/intent-compliance",
        binary=True,
    )
    if completed.returncode != 0:
        raise TrustedSnapshotError(
            snapshot.repository, "cannot enumerate the authoritative family"
        )
    raw_output = completed.stdout
    if not isinstance(raw_output, bytes):
        raise TrustedSnapshotError(
            snapshot.repository, "authoritative family listing was not binary"
        )
    paths = [item.decode("utf-8") for item in raw_output.split(b"\0") if item]
    if len(paths) > MAX_DISCOVERY_FILES:
        raise TrustedSnapshotError(
            snapshot.repository,
            f"authoritative family exceeds {MAX_DISCOVERY_FILES} files",
        )
    eligible = [
        path
        for path in paths
        if Path(path).suffix in {".yaml", ".yml"}
        and "examples" not in Path(path).parts
        and not Path(path).name.endswith((".schema.yaml", ".template.yaml"))
    ]
    return eligible


def read_trusted_family_blob(snapshot: TrustedSnapshot, path: str) -> bytes:
    try:
        resolved = _resolve_bounded_git_object(
            snapshot.repository,
            snapshot.commit,
            path,
        )
    except ContentResolutionError as error:
        raise TrustedSnapshotError(
            snapshot.repository, f"cannot resolve family blob: {path}"
        ) from error
    return resolved.data


def _resolve_bounded_git_object(
    repository: Path, revision: str, path: str
) -> ResolvedGitContent:
    resolved = resolve_git_object(repository, revision, path)
    if len(resolved.data) > MAX_INPUT_BYTES:
        raise ContentResolutionError(f"Git blob exceeds {MAX_INPUT_BYTES} bytes")
    return resolved


def _git(
    repository_root: Path, *arguments: str, binary: bool = False
) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    environment = os.environ.copy()
    for name in UNTRUSTED_GIT_ENVIRONMENT:
        environment.pop(name, None)
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    try:
        completed = subprocess.run(
            ["git", "--no-replace-objects", *arguments],
            cwd=repository_root,
            check=False,
            capture_output=True,
            text=not binary,
            timeout=5,
            env=environment,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise TrustedSnapshotError(
            repository_root, "trusted Git dependency is unavailable"
        ) from error
    return completed
