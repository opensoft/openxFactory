"""RED contracts for repository-relative and exact Git-object resolution."""

from __future__ import annotations

import hashlib
import importlib
import os
from pathlib import Path
import subprocess
from types import ModuleType

import pytest


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repository"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    _git(repo, "config", "user.name", "Hermes Contract Tests")
    _git(repo, "config", "user.email", "hermes-contracts@example.invalid")
    return repo


@pytest.fixture
def content() -> ModuleType:
    try:
        return importlib.import_module("scripts.hermes_runtime_validation.content")
    except ModuleNotFoundError as exc:
        pytest.fail(f"planned exact-object resolver is missing: {exc}")


def _commit_file(
    repo: Path, path: str, body: bytes, *, executable: bool = False
) -> str:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(body)
    if executable:
        target.chmod(0o755)
    _git(repo, "add", "--", path)
    _git(repo, "commit", "--quiet", "-m", f"add {path}")
    return _git(repo, "rev-parse", "HEAD")


def _assert_dependency_error(content: ModuleType, operation: object) -> None:
    with pytest.raises(content.ContentResolutionError) as caught:
        operation()  # type: ignore[operator]
    assert caught.value.exit_code == 2


def test_resolves_exact_commit_tree_and_blob_not_worktree(
    content: ModuleType, git_repo: Path
) -> None:
    first = _commit_file(git_repo, "contracts/example.yaml", b"version: one\n")
    (git_repo / "contracts/example.yaml").write_bytes(b"dirty working tree\n")

    resolved = content.resolve_git_object(git_repo, first, "contracts/example.yaml")

    assert resolved.data == b"version: one\n"
    assert resolved.commit_oid == first
    assert resolved.tree_oid == _git(git_repo, "rev-parse", f"{first}^{{tree}}")
    assert resolved.blob_oid == _git(
        git_repo, "rev-parse", f"{first}:contracts/example.yaml"
    )


def test_rejects_object_available_only_through_inherited_alternate_directory(
    content: ModuleType,
    git_repo: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    alternate = tmp_path / "alternate"
    alternate.mkdir()
    _git(alternate, "init", "--quiet")
    _git(alternate, "config", "user.name", "Hermes Contract Tests")
    _git(alternate, "config", "user.email", "hermes-contracts@example.invalid")
    alternate_commit = _commit_file(
        alternate, "alternate-only.txt", b"alternate object\n"
    )
    monkeypatch.setenv(
        "GIT_ALTERNATE_OBJECT_DIRECTORIES", str(alternate / ".git" / "objects")
    )

    with pytest.raises(content.ContentResolutionError) as caught:
        content.resolve_git_object(git_repo, alternate_commit, "alternate-only.txt")

    assert caught.value.code == content.CONTENT_DEPENDENCY


def test_resolves_objects_from_a_legitimate_linked_worktree(
    content: ModuleType, git_repo: Path, tmp_path: Path
) -> None:
    commit = _commit_file(git_repo, "linked-only.txt", b"linked worktree object\n")
    linked_worktree = tmp_path / "linked-worktree"
    _git(
        git_repo,
        "worktree",
        "add",
        "--quiet",
        "--detach",
        str(linked_worktree),
        commit,
    )

    resolved = content.resolve_git_object(linked_worktree, commit, "linked-only.txt")

    assert resolved.data == b"linked worktree object\n"
    assert resolved.commit_oid == commit


def test_sanitized_git_environment_removes_redirects_and_command_scope_config(
    content: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    inherited_overrides = {
        "GIT_COMMON_DIR": "hostile-common-dir",
        "GIT_DIR": "hostile-git-dir",
        "GIT_WORK_TREE": "hostile-work-tree",
        "GIT_INDEX_FILE": "hostile-index",
        "GIT_OBJECT_DIRECTORY": "hostile-objects",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES": "hostile-alternates",
        "GIT_REPLACE_REF_BASE": "refs/hostile/replace/",
        "GIT_CONFIG_PARAMETERS": "'core.bare=true'",
        "GIT_CONFIG_COUNT": "2",
        "GIT_CONFIG_KEY_0": "core.bare",
        "GIT_CONFIG_VALUE_0": "true",
        "GIT_CONFIG_KEY_37": "core.worktree",
        "GIT_CONFIG_VALUE_37": "hostile-work-tree",
    }
    for name, value in inherited_overrides.items():
        monkeypatch.setenv(name, value)

    environment = content._sanitized_git_environment()

    assert inherited_overrides.keys().isdisjoint(environment)
    assert environment["GIT_NO_REPLACE_OBJECTS"] == "1"


@pytest.mark.parametrize(
    "path",
    ["", "/absolute", "../outside", "a/../b", "./a", "a/./b", "a//b", "a\\b"],
)
def test_rejects_noncanonical_repository_paths(content: ModuleType, path: str) -> None:
    _assert_dependency_error(content, lambda: content.normalize_repository_path(path))


@pytest.mark.parametrize(
    "executable, expected_mode", [(False, "100644"), (True, "100755")]
)
def test_preserves_supported_regular_file_modes(
    content: ModuleType, git_repo: Path, executable: bool, expected_mode: str
) -> None:
    commit = _commit_file(git_repo, "bin/check", b"#!/bin/sh\n", executable=executable)
    resolved = content.resolve_git_object(git_repo, commit, "bin/check")
    assert resolved.git_mode == expected_mode


def test_missing_commit_or_path_is_an_exit_two_dependency_error(
    content: ModuleType, git_repo: Path
) -> None:
    commit = _commit_file(git_repo, "present.txt", b"present\n")
    _assert_dependency_error(
        content, lambda: content.resolve_git_object(git_repo, "0" * 40, "present.txt")
    )
    _assert_dependency_error(
        content, lambda: content.resolve_git_object(git_repo, commit, "missing.txt")
    )


def test_rejects_tree_symlink_and_submodule_objects(
    content: ModuleType, git_repo: Path, tmp_path: Path
) -> None:
    commit = _commit_file(git_repo, "nested/file.txt", b"nested\n")
    _assert_dependency_error(
        content, lambda: content.resolve_git_object(git_repo, commit, "nested")
    )

    os.symlink("nested/file.txt", git_repo / "link.txt")
    _git(git_repo, "add", "link.txt")
    _git(git_repo, "commit", "--quiet", "-m", "add symlink")
    symlink_commit = _git(git_repo, "rev-parse", "HEAD")
    _assert_dependency_error(
        content,
        lambda: content.resolve_git_object(git_repo, symlink_commit, "link.txt"),
    )

    child = tmp_path / "child"
    child.mkdir()
    _git(child, "init", "--quiet")
    _git(child, "config", "user.name", "Hermes Contract Tests")
    _git(child, "config", "user.email", "hermes-contracts@example.invalid")
    child_commit = _commit_file(child, "README.md", b"child\n")
    _git(
        git_repo,
        "update-index",
        "--add",
        "--cacheinfo",
        f"160000,{child_commit},vendor/child",
    )
    _git(git_repo, "commit", "--quiet", "-m", "add gitlink")
    gitlink_commit = _git(git_repo, "rev-parse", "HEAD")
    _assert_dependency_error(
        content,
        lambda: content.resolve_git_object(git_repo, gitlink_commit, "vendor/child"),
    )


def test_digest_is_sha256_of_exact_raw_blob(
    content: ModuleType, git_repo: Path
) -> None:
    body = b"raw bytes: \x00\xff\r\n"
    commit = _commit_file(git_repo, "raw.bin", body)
    resolved = content.resolve_git_object(git_repo, commit, "raw.bin")
    assert resolved.digest == f"sha256:{hashlib.sha256(body).hexdigest()}"


# --- the declared condition vocabulary (fix-content-resolution-conflation) ----
#
# Fifteen refusals reach `resolve_git_object` and exactly ONE of them is a fact
# about the tree that was read: `ls-tree` resolved the commit and its tree, and
# the path was not in it.  A caller that reduces a resolution to presence or to
# a blob identity may act on that one and must refuse the other fourteen, so
# the resolver declares which it observed.
#
# The distinction is carried by the declared `code` and NEVER by the message:
# a message is prose, prose is edited for clarity, and a near-miss match would
# silently reclassify a safety refusal as release data (OD-4).


def test_the_default_code_is_unchanged_and_the_absence_code_is_distinct(
    content: ModuleType,
) -> None:
    assert content.CONTENT_DEPENDENCY == "HRC-CONTENT-DEPENDENCY"
    assert content.CONTENT_PATH_ABSENT != content.CONTENT_DEPENDENCY
    # Additive: the default every existing raise site takes is untouched, so no
    # caller that never read a code observes any change.
    assert content.ContentResolutionError("x").code == content.CONTENT_DEPENDENCY


def test_only_the_absent_path_refusal_declares_the_absence_code(
    content: ModuleType, git_repo: Path, tmp_path: Path
) -> None:
    """One data answer, fourteen non-answers, told apart by a declared code.

    Every failing condition here is driven by ARGUMENT or by committed data
    rather than by a real timeout (Q4): a genuine 30-second store timeout is
    slow and flaky, and the requirement is about the DISTINCTION rather than
    about any one way of failing.
    """

    commit = _commit_file(git_repo, "nested/file.txt", b"nested\n")
    os.symlink("nested/file.txt", git_repo / "link.txt")
    _git(git_repo, "add", "link.txt")
    _git(git_repo, "commit", "--quiet", "-m", "add symlink")
    symlink_commit = _git(git_repo, "rev-parse", "HEAD")

    with pytest.raises(content.ContentResolutionError) as absent:
        content.resolve_git_object(git_repo, commit, "missing.txt")
    assert absent.value.code == content.CONTENT_PATH_ABSENT

    others = {
        "the commit is not in the store": lambda: content.resolve_git_object(
            git_repo, "0" * 40, "nested/file.txt"
        ),
        "the repository cannot be opened": lambda: content.resolve_git_object(
            tmp_path / "not-a-repository", commit, "nested/file.txt"
        ),
        "the revision is not an object id": lambda: content.resolve_git_object(
            git_repo, "HEAD", "nested/file.txt"
        ),
        "the path is not canonical": lambda: content.resolve_git_object(
            git_repo, commit, "nested/../nested/file.txt"
        ),
        "the path is a directory": lambda: content.resolve_git_object(
            git_repo, commit, "nested"
        ),
        "the path is a symbolic link": lambda: content.resolve_git_object(
            git_repo, symlink_commit, "link.txt"
        ),
    }
    for condition, operation in others.items():
        with pytest.raises(content.ContentResolutionError) as caught:
            operation()
        assert caught.value.exit_code == 2, condition
        assert caught.value.code == content.CONTENT_DEPENDENCY, condition
        assert caught.value.code != content.CONTENT_PATH_ABSENT, condition
