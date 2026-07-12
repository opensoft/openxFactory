"""Deterministic helpers shared by Hermes runtime contract tests."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXED_GIT_DATE = "2026-01-01T00:00:00+00:00"


@dataclass(frozen=True)
class CommandResult:
    """Stable subprocess result with an assertion-friendly failure message."""

    argv: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    def assert_success(self) -> "CommandResult":
        if self.returncode != 0:
            command = " ".join(self.argv)
            raise AssertionError(
                f"command failed ({self.returncode}): {command}\n"
                f"stdout:\n{self.stdout}\nstderr:\n{self.stderr}"
            )
        return self


def deterministic_environment(overrides: Mapping[str, str] | None = None) -> dict[str, str]:
    """Return a locale/time/hash-stable environment for subprocess tests."""

    environment = os.environ.copy()
    environment.update(
        {
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PYTHONHASHSEED": "0",
            "TZ": "UTC",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_AUTHOR_DATE": FIXED_GIT_DATE,
            "GIT_COMMITTER_DATE": FIXED_GIT_DATE,
        }
    )
    if overrides:
        environment.update(overrides)
    return environment


def run_command(
    argv: Sequence[str | os.PathLike[str]],
    *,
    cwd: Path,
    env: Mapping[str, str] | None = None,
    input_text: str | None = None,
    check: bool = False,
) -> CommandResult:
    """Run a command without a shell and capture normalized text output."""

    command = tuple(os.fspath(item) for item in argv)
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=deterministic_environment(env),
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    result = CommandResult(
        argv=command,
        returncode=completed.returncode,
        stdout=completed.stdout.replace("\r\n", "\n"),
        stderr=completed.stderr.replace("\r\n", "\n"),
    )
    return result.assert_success() if check else result


def write_yaml(path: Path, document: object) -> Path:
    """Write deterministic YAML for temporary synthetic contract inputs."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(document, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )
    return path


def init_git_repo(path: Path) -> Path:
    """Initialize a deterministic local Git repository with a test identity."""

    path.mkdir(parents=True, exist_ok=True)
    run_command(["git", "init", "--quiet"], cwd=path, check=True)
    run_command(["git", "config", "user.name", "Hermes Contract Tests"], cwd=path, check=True)
    run_command(["git", "config", "user.email", "hermes-tests@example.invalid"], cwd=path, check=True)
    run_command(["git", "config", "commit.gpgsign", "false"], cwd=path, check=True)
    return path


def commit_files(
    repo: Path,
    files: Mapping[str, str | bytes],
    *,
    message: str = "synthetic fixture",
) -> str:
    """Commit files and return the exact commit object ID."""

    for relative_path, content in files.items():
        target = repo / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            target.write_bytes(content)
        else:
            target.write_text(content, encoding="utf-8")
    run_command(["git", "add", "--", *sorted(files)], cwd=repo, check=True)
    run_command(["git", "commit", "--quiet", "-m", message], cwd=repo, check=True)
    return run_command(["git", "rev-parse", "HEAD"], cwd=repo, check=True).stdout.strip()


def finding_codes(findings: Sequence[Mapping[str, object]]) -> list[str]:
    """Extract finding codes without weakening their deterministic order."""

    return [str(finding["code"]) for finding in findings]
