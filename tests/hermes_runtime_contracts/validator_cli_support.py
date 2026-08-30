from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import (
    Final,
    Protocol,
    TypeAlias,
    TypedDict,
    runtime_checkable,
)

import pytest
import yaml

REPOSITORY_ROOT: Final = Path(__file__).resolve().parents[2]
ENTRYPOINT: Final = REPOSITORY_ROOT / "scripts/validate-hermes-runtime-contracts.py"
CHANGE_ID: Final = "add-hermes-customer-subject-runtime-contract"

YamlScalar: TypeAlias = str | int | float | bool | None
YamlValue: TypeAlias = YamlScalar | list["YamlValue"] | dict[str, "YamlValue"]
YamlObject: TypeAlias = dict[str, YamlValue]


class FindingJson(TypedDict):
    code: str
    severity: str
    case_id: str | None
    path: str | None
    message: str


class SelectionJson(TypedDict):
    case_id: str | None
    case_ids: list[str]
    phase: str | None


class SummaryJson(TypedDict):
    catalog_members: int
    schema_members: int
    fixture_cases: int
    openspec_requirements: int
    openspec_scenarios: int
    collected_test_nodes: int


class ReportJson(TypedDict):
    mode: str
    status: str
    findings: list[FindingJson]
    summary: SummaryJson
    selection: SelectionJson


class ReportDecoder(Protocol):
    def __call__(self, s: str) -> ReportJson: ...


class YamlLoader(Protocol):
    def __call__(self, stream: str) -> YamlValue: ...


@runtime_checkable
class ValidatorModule(Protocol):
    def classify_exit_code(
        self,
        findings: Sequence[Mapping[str, str]],
        *,
        strict: bool,
        dependency_error: bool = False,
    ) -> int: ...


decode_report: ReportDecoder = json.loads
safe_yaml_load: YamlLoader = yaml.safe_load


def governed_change_specs_path(repo_root: Path) -> Path:
    active = Path("openspec/changes") / CHANGE_ID / "specs"
    if (repo_root / active).is_dir():
        return active
    archived = sorted(
        path.relative_to(repo_root)
        for path in (repo_root / "openspec/changes/archive").glob(
            f"????-??-??-{CHANGE_ID}/specs"
        )
        if path.is_dir()
    )
    assert len(archived) == 1, f"expected one archived packet for {CHANGE_ID}"
    return archived[0]


def run_git(repo: Path, *args: str) -> None:
    result = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr


@pytest.fixture(name="empty_git_repo")
def empty_git_repo_fixture(tmp_path: Path) -> Path:
    repo = tmp_path / "alternate-repo"
    _ = repo.mkdir()
    run_git(repo, "init", "--quiet")
    run_git(repo, "config", "user.name", "Hermes Contract Tests")
    run_git(repo, "config", "user.email", "hermes-contracts@example.invalid")
    _ = (repo / "README.md").write_text("temporary validator root\n", encoding="utf-8")
    run_git(repo, "add", "README.md")
    run_git(repo, "commit", "--quiet", "-m", "initial")
    return repo


@pytest.fixture(name="repository_snapshot")
def repository_snapshot_fixture(tmp_path: Path) -> Path:
    snapshot = tmp_path / "repository-snapshot"
    _ = snapshot.mkdir()
    ignored = shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc")
    for relative in (
        Path("contracts/hermes-runtime"),
        governed_change_specs_path(REPOSITORY_ROOT),
        Path("scripts/hermes_runtime_validation"),
        Path("tests/hermes_runtime_contracts"),
    ):
        source = REPOSITORY_ROOT / relative
        destination = snapshot / relative
        _ = destination.parent.mkdir(parents=True, exist_ok=True)
        _ = shutil.copytree(source, destination, ignore=ignored)

    family_root = REPOSITORY_ROOT / "contracts/hermes-runtime"
    catalog = read_yaml(family_root / "contract-index.yaml")
    contracts = catalog["contracts"]
    assert isinstance(contracts, list)
    for value in contracts:
        entry = yaml_mapping(value)
        path = entry["path"]
        assert isinstance(path, str)
        member = (family_root / path).resolve(strict=True)
        relative = member.relative_to(REPOSITORY_ROOT)
        destination = snapshot / relative
        if destination.exists():
            continue
        _ = destination.parent.mkdir(parents=True, exist_ok=True)
        _ = shutil.copy2(member, destination)

    validator = snapshot / "scripts/validate-hermes-runtime-contracts.py"
    _ = validator.parent.mkdir(parents=True, exist_ok=True)
    _ = shutil.copy2(ENTRYPOINT, validator)
    _ = shutil.copy2(
        REPOSITORY_ROOT / "scripts/run-hermes-runtime-postgres-tests.sh",
        snapshot / "scripts/run-hermes-runtime-postgres-tests.sh",
    )
    for pinned in (
        Path("contracts/schemas/hermes-operational-postgres.sql"),
        Path("scripts/apply-hermes-runtime-postgres-v2.py"),
        Path("scripts/hermes-runtime-dataset-digest.py"),
        Path("scripts/run-hermes-v1-to-v2-migration.sh"),
        Path("scripts/validate-hermes-runtime-postgres.py"),
    ):
        pinned_destination = snapshot / pinned
        _ = pinned_destination.parent.mkdir(parents=True, exist_ok=True)
        _ = shutil.copy2(REPOSITORY_ROOT / pinned, pinned_destination)
    run_git(snapshot, "init", "--quiet")
    run_git(snapshot, "config", "user.name", "Hermes Contract Tests")
    run_git(snapshot, "config", "user.email", "hermes-contracts@example.invalid")
    run_git(snapshot, "add", ".")
    run_git(snapshot, "commit", "--quiet", "-m", "validator snapshot")
    return snapshot


def run_cli(*args: str, timeout: float = 30) -> subprocess.CompletedProcess[str]:
    assert ENTRYPOINT.is_file(), f"planned validator CLI is missing: {ENTRYPOINT}"
    return subprocess.run(
        [sys.executable, ENTRYPOINT, *args],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )


def json_result(result: subprocess.CompletedProcess[str]) -> ReportJson:
    assert result.stderr == "", result.stderr
    payload = decode_report(result.stdout)
    assert isinstance(payload.get("findings"), list)
    return payload


def load_entrypoint() -> ValidatorModule:
    assert ENTRYPOINT.is_file(), f"planned validator CLI is missing: {ENTRYPOINT}"
    spec = importlib.util.spec_from_file_location(
        "hermes_runtime_validator_cli", ENTRYPOINT
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert isinstance(module, ValidatorModule)
    return module


def read_yaml(path: Path) -> YamlObject:
    document = safe_yaml_load(path.read_text(encoding="utf-8"))
    assert isinstance(document, dict)
    return document


def write_yaml(path: Path, document: YamlObject) -> None:
    _ = path.write_text(
        yaml.safe_dump(document, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def yaml_mapping(value: YamlValue) -> YamlObject:
    assert isinstance(value, dict)
    return value
