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


def _commit_file(repo: Path, path: str, body: bytes, *, executable: bool = False) -> str:
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


@pytest.mark.parametrize(
    "path",
    ["", "/absolute", "../outside", "a/../b", "./a", "a/./b", "a//b", "a\\b"],
)
def test_rejects_noncanonical_repository_paths(content: ModuleType, path: str) -> None:
    _assert_dependency_error(content, lambda: content.normalize_repository_path(path))


@pytest.mark.parametrize("executable, expected_mode", [(False, "100644"), (True, "100755")])
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
        content, lambda: content.resolve_git_object(git_repo, symlink_commit, "link.txt")
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


def test_digest_is_sha256_of_exact_raw_blob(content: ModuleType, git_repo: Path) -> None:
    body = b"raw bytes: \x00\xff\r\n"
    commit = _commit_file(git_repo, "raw.bin", body)
    resolved = content.resolve_git_object(git_repo, commit, "raw.bin")
    assert resolved.digest == f"sha256:{hashlib.sha256(body).hexdigest()}"
