"""Fail-closed repository-relative and exact Git-object content resolution."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import subprocess


_OBJECT_ID = re.compile(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}")
_CLOSED_REPOSITORY_PATH = re.compile(r"[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*")
_INDEXED_GIT_CONFIG_ENVIRONMENT = re.compile(r"GIT_CONFIG_(?:KEY|VALUE)_[0-9]+")
_SCRUBBED_GIT_ENVIRONMENT = (
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
    "GIT_CONFIG_COUNT",
    "GIT_CONFIG_PARAMETERS",
    "GIT_DIR",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_REPLACE_REF_BASE",
    "GIT_WORK_TREE",
)


# The resolver's DECLARED condition vocabulary.
#
# `CONTENT_DEPENDENCY` is the default and stays the code every existing raise
# site takes: the repository will not open, git will not run, the read timed
# out, the argument was malformed, or an unsafe or inexact object was refused.
# None of those establishes anything about the tree that was being read.
#
# `CONTENT_PATH_ABSENT` is declared for the ONE refusal that is a fact about
# that tree: `ls-tree` resolved the commit AND its tree, and the path was not
# in it.  A caller that reduces a resolution to a presence answer or to a blob
# identity may act on that condition and must refuse every other one.
#
# The distinction is carried HERE, by a value the resolver declares, and never
# by matching the message: a message is prose, prose is edited for clarity, and
# a near-miss match would then silently reclassify a safety refusal as data —
# the same hazard the sentinel vocabulary refuses near-miss spellings for.
CONTENT_DEPENDENCY = "HRC-CONTENT-DEPENDENCY"
CONTENT_PATH_ABSENT = "HRC-CONTENT-PATH-ABSENT"


class ContentResolutionError(RuntimeError):
    """An unavailable or unsafe content dependency (CLI exit code 2)."""

    exit_code = 2

    def __init__(self, message: str, *, code: str = CONTENT_DEPENDENCY) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class ResolvedGitContent:
    path: str
    data: bytes
    git_mode: str
    commit_oid: str
    tree_oid: str
    blob_oid: str
    digest: str


def normalize_repository_path(path: str | os.PathLike[str]) -> str:
    """Return an already-canonical POSIX repository path or fail closed."""

    raw = os.fspath(path)
    if not isinstance(raw, str):
        raise ContentResolutionError("repository path must be text")
    if not raw or raw.startswith("/") or raw.startswith(":") or "\\" in raw:
        raise ContentResolutionError("repository path is not canonical")
    if any(ord(character) < 32 or ord(character) == 127 for character in raw):
        raise ContentResolutionError("repository path contains a control character")
    parts = raw.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ContentResolutionError("repository path contains a forbidden segment")
    normalized = PurePosixPath(*parts).as_posix()
    if normalized != raw or _CLOSED_REPOSITORY_PATH.fullmatch(normalized) is None:
        raise ContentResolutionError("repository path is not canonical")
    return normalized


def _sanitized_git_environment() -> dict[str, str]:
    environment = {
        name: value
        for name, value in os.environ.items()
        if name not in _SCRUBBED_GIT_ENVIRONMENT
        and _INDEXED_GIT_CONFIG_ENVIRONMENT.fullmatch(name) is None
    }
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    return environment


def _git(repo: Path, *arguments: str, binary: bool = False) -> str | bytes:
    try:
        result = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(repo), *arguments],
            capture_output=True,
            text=not binary,
            check=False,
            timeout=30,
            env=_sanitized_git_environment(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ContentResolutionError("Git content dependency is unavailable") from exc
    if result.returncode != 0:
        raise ContentResolutionError("exact Git object is unavailable")
    return result.stdout


def _repository(path: str | os.PathLike[str]) -> Path:
    repo = Path(path)
    if not repo.exists():
        raise ContentResolutionError("Git repository is unavailable")
    _git(repo, "rev-parse", "--git-dir")
    return repo


def resolve_git_object(
    repository: str | os.PathLike[str], revision: str, path: str | os.PathLike[str]
) -> ResolvedGitContent:
    """Resolve one regular file from one exact commit without reading worktree bytes."""

    repo = _repository(repository)
    normalized_path = normalize_repository_path(path)
    if not isinstance(revision, str) or _OBJECT_ID.fullmatch(revision) is None:
        raise ContentResolutionError("revision must be a full Git object ID")

    commit_oid = str(
        _git(repo, "rev-parse", "--verify", f"{revision}^{{commit}}")
    ).strip()
    if _OBJECT_ID.fullmatch(commit_oid) is None:
        raise ContentResolutionError("Git returned an invalid commit object ID")
    tree_oid = str(
        _git(repo, "rev-parse", "--verify", f"{commit_oid}^{{tree}}")
    ).strip()

    listing = bytes(
        _git(
            repo,
            "ls-tree",
            "-z",
            "--full-tree",
            commit_oid,
            "--",
            f":(literal){normalized_path}",
            binary=True,
        )
    )
    records = [record for record in listing.split(b"\0") if record]
    if len(records) != 1 or b"\t" not in records[0]:
        # The tree was read and the path was not in it.  This is the only
        # refusal in this module that is a fact about the commit rather than
        # about the environment or an unsafe object, so it is the only one that
        # declares a code of its own.
        raise ContentResolutionError(
            "exact Git path is unavailable", code=CONTENT_PATH_ABSENT
        )
    metadata, encoded_path = records[0].split(b"\t", 1)
    try:
        git_mode, object_type, blob_oid = metadata.decode("ascii").split(" ", 2)
        listed_path = encoded_path.decode("utf-8")
    except (UnicodeDecodeError, ValueError) as exc:
        raise ContentResolutionError("Git tree entry is malformed") from exc
    if listed_path != normalized_path:
        raise ContentResolutionError("Git path resolution was not exact")
    if object_type != "blob" or git_mode not in {"100644", "100755"}:
        raise ContentResolutionError("Git path is not a supported regular file")
    if _OBJECT_ID.fullmatch(blob_oid) is None:
        raise ContentResolutionError("Git returned an invalid blob object ID")

    data = bytes(_git(repo, "cat-file", "blob", blob_oid, binary=True))
    return ResolvedGitContent(
        path=normalized_path,
        data=data,
        git_mode=git_mode,
        commit_oid=commit_oid,
        tree_oid=tree_oid,
        blob_oid=blob_oid,
        digest=f"sha256:{hashlib.sha256(data).hexdigest()}",
    )
