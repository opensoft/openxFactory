"""Shared deterministic pytest fixtures for Hermes runtime contracts."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.hermes_runtime_contracts.support import (
    REPO_ROOT,
    deterministic_environment,
    init_git_repo,
    run_command,
    write_yaml,
)


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def fixed_evaluation_time() -> str:
    return "2026-07-12T12:00:00Z"


@pytest.fixture
def deterministic_env() -> dict[str, str]:
    return deterministic_environment()


@pytest.fixture
def yaml_writer():
    return write_yaml


@pytest.fixture
def command_runner():
    return run_command


@pytest.fixture
def synthetic_git_repo(tmp_path: Path) -> Path:
    return init_git_repo(tmp_path / "repo")
