"""RED subprocess contracts for the Hermes runtime validator entrypoint."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from types import ModuleType

import pytest
import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = REPOSITORY_ROOT / "scripts/validate-hermes-runtime-contracts.py"
CHANGE_ID = "add-hermes-customer-subject-runtime-contract"


def _git(repo: Path, *args: str) -> None:
    result = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr


@pytest.fixture
def empty_git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "alternate-repo"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    _git(repo, "config", "user.name", "Hermes Contract Tests")
    _git(repo, "config", "user.email", "hermes-contracts@example.invalid")
    (repo / "README.md").write_text("temporary validator root\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "--quiet", "-m", "initial")
    return repo


@pytest.fixture
def repository_snapshot(tmp_path: Path) -> Path:
    """Copy only the canonical validator inputs into an isolated Git root."""

    snapshot = tmp_path / "repository-snapshot"
    snapshot.mkdir()
    ignored = shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc")
    for relative in (
        Path("contracts/hermes-runtime"),
        Path("openspec/changes") / CHANGE_ID / "specs",
        Path("scripts/hermes_runtime_validation"),
        Path("tests/hermes_runtime_contracts"),
    ):
        source = REPOSITORY_ROOT / relative
        destination = snapshot / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination, ignore=ignored)
    validator = snapshot / "scripts/validate-hermes-runtime-contracts.py"
    validator.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ENTRYPOINT, validator)
    shutil.copy2(
        REPOSITORY_ROOT / "scripts/run-hermes-runtime-postgres-tests.sh",
        snapshot / "scripts/run-hermes-runtime-postgres-tests.sh",
    )
    _git(snapshot, "init", "--quiet")
    _git(snapshot, "config", "user.name", "Hermes Contract Tests")
    _git(snapshot, "config", "user.email", "hermes-contracts@example.invalid")
    _git(snapshot, "add", ".")
    _git(snapshot, "commit", "--quiet", "-m", "validator snapshot")
    return snapshot


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    assert ENTRYPOINT.is_file(), f"planned validator CLI is missing: {ENTRYPOINT}"
    return subprocess.run(
        [sys.executable, ENTRYPOINT, *args],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def _json_result(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    assert result.stderr == "", result.stderr
    payload = json.loads(result.stdout)
    assert isinstance(payload, dict)
    assert isinstance(payload.get("findings"), list)
    return payload


def _load_entrypoint() -> ModuleType:
    assert ENTRYPOINT.is_file(), f"planned validator CLI is missing: {ENTRYPOINT}"
    spec = importlib.util.spec_from_file_location(
        "hermes_runtime_validator_cli", ENTRYPOINT
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read_yaml(path: Path) -> dict:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(document, dict)
    return document


def _write_yaml(path: Path, document: dict) -> None:
    path.write_text(
        yaml.safe_dump(document, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )


def test_help_lists_the_complete_selection_and_resolver_surface() -> None:
    result = _run_cli("--help")
    assert result.returncode == 0
    for option in (
        "--strict",
        "--case",
        "--phase",
        "--json",
        "--require-candidate",
        "--require-realization",
        "--repo",
        "--domain-repo",
        "--domain-repo-root",
        "--handoff-receipt",
        "--consumer-repo",
        "--consumer-repo-root",
    ):
        assert option in result.stdout


def test_case_selection_has_deterministic_machine_output(empty_git_repo: Path) -> None:
    args = (
        "--repo",
        str(empty_git_repo),
        "--case",
        "not-an-indexed-case",
        "--json",
    )
    first = _run_cli(*args)
    second = _run_cli(*args)
    assert first.returncode == second.returncode == 2
    assert first.stdout == second.stdout
    payload = _json_result(first)
    finding = payload["findings"][0]  # type: ignore[index]
    assert {"code", "severity", "case_id", "path", "message"} <= set(finding)
    assert finding["case_id"] == "not-an-indexed-case"


def test_human_output_is_deterministic_and_contains_a_stable_code(
    empty_git_repo: Path,
) -> None:
    args = ("--repo", str(empty_git_repo), "--case", "not-an-indexed-case")
    first = _run_cli(*args)
    second = _run_cli(*args)
    assert first.returncode == second.returncode == 2
    assert (first.stdout, first.stderr) == (second.stdout, second.stderr)
    assert re.search(r"\b[A-Z][A-Z0-9]+(?:-[A-Z0-9]+){2,}\b", first.stdout)
    assert "Traceback" not in first.stdout + first.stderr


@pytest.mark.parametrize(
    ("mode_option", "expected_mode"),
    [("--require-candidate", "candidate"), ("--require-realization", "realization")],
)
def test_candidate_and_realization_modes_are_explicit_in_json_results(
    empty_git_repo: Path, mode_option: str, expected_mode: str
) -> None:
    result = _run_cli(mode_option, "--repo", str(empty_git_repo), "--json")
    assert result.returncode == 2
    assert _json_result(result)["mode"] == expected_mode


def test_candidate_and_realization_modes_are_mutually_exclusive(
    empty_git_repo: Path,
) -> None:
    result = _run_cli(
        "--require-candidate",
        "--require-realization",
        "--repo",
        str(empty_git_repo),
        "--json",
    )
    assert result.returncode == 2
    payload = _json_result(result)
    assert "mutually exclusive" in payload["findings"][0]["message"].lower()  # type: ignore[index]


@pytest.mark.parametrize(
    "mode_option", ["--require-candidate", "--require-realization"]
)
def test_future_release_modes_fail_closed_until_t077(mode_option: str) -> None:
    result = _run_cli(mode_option, "--strict", "--json")

    assert result.returncode == 2
    payload = _json_result(result)
    assert payload["status"] == "error"
    assert any(
        finding["code"] == "HRC-MODE-NOT-REALIZED" and "T077" in finding["message"]
        for finding in payload["findings"]
    )


def test_repeatable_resolver_options_reach_validation_not_argparse(
    empty_git_repo: Path, tmp_path: Path
) -> None:
    mirror_root = tmp_path / "mirrors"
    mirror_root.mkdir()
    result = _run_cli(
        "--repo",
        str(empty_git_repo),
        "--case",
        "not-an-indexed-case",
        "--domain-repo",
        f"example/domain={empty_git_repo}",
        "--domain-repo-root",
        str(mirror_root),
        "--consumer-repo",
        f"opensoft/xFactory-Hermes-Install={empty_git_repo}",
        "--consumer-repo-root",
        str(mirror_root),
        "--json",
    )
    assert result.returncode == 2
    assert "unrecognized arguments" not in result.stderr
    assert _json_result(result)["findings"][0]["case_id"] == "not-an-indexed-case"  # type: ignore[index]


def test_warning_escalation_and_exit_code_precedence_are_stable() -> None:
    cli = _load_entrypoint()
    warning = [{"severity": "warning"}]
    error = [{"severity": "error"}]
    assert cli.classify_exit_code(warning, strict=False) == 0
    assert cli.classify_exit_code(warning, strict=True) == 1
    assert cli.classify_exit_code(error, strict=False) == 1
    assert cli.classify_exit_code([], strict=False, dependency_error=True) == 2


def test_invalid_phase_is_a_harness_error_without_a_traceback() -> None:
    result = _run_cli("--phase", "database")
    assert result.returncode == 2
    assert "Traceback" not in result.stdout + result.stderr


def test_current_repository_strict_mode_executes_every_integration_gate() -> None:
    result = _run_cli("--strict", "--json")

    assert result.returncode == 0, result.stdout + result.stderr
    payload = _json_result(result)
    assert payload["status"] == "pass"
    assert payload["findings"] == []
    summary = payload["summary"]
    assert summary["catalog_members"] >= 31
    assert summary["schema_members"] >= 25
    assert summary["fixture_cases"] >= 74
    assert summary["openspec_requirements"] == 17
    assert summary["openspec_scenarios"] == 85
    assert summary["collected_test_nodes"] > 300


def test_valid_case_and_phase_selection_are_reported_deterministically() -> None:
    args = (
        "--strict",
        "--case",
        "topology-operational-two-customers",
        "--phase",
        "semantic",
        "--json",
    )
    first = _run_cli(*args)
    second = _run_cli(*args)

    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    selection = _json_result(first)["selection"]
    assert selection["case_id"] == "topology-operational-two-customers"
    assert selection["phase"] == "semantic"
    assert selection["case_ids"] == ["topology-operational-two-customers"]


def test_malformed_canonical_catalog_fails_closed(
    repository_snapshot: Path,
) -> None:
    path = repository_snapshot / "contracts/hermes-runtime/contract-index.yaml"
    document = _read_yaml(path)
    document["contracts"][1]["contract_id"] = document["contracts"][0]["contract_id"]
    _write_yaml(path, document)

    result = _run_cli("--repo", str(repository_snapshot), "--strict", "--json")

    assert result.returncode == 1
    codes = {finding["code"] for finding in _json_result(result)["findings"]}
    assert codes == {"HRC-CATALOG-INVALID"}


def test_malformed_fixture_index_fails_for_index_reason(
    repository_snapshot: Path,
) -> None:
    path = repository_snapshot / "contracts/hermes-runtime/fixtures/index.yaml"
    document = _read_yaml(path)
    document["cases"][1]["inputs"] = list(document["cases"][0]["inputs"])
    _write_yaml(path, document)

    result = _run_cli("--repo", str(repository_snapshot), "--strict", "--json")

    assert result.returncode == 1
    codes = {finding["code"] for finding in _json_result(result)["findings"]}
    assert "HGR-FIXTURE-PATH-DUPLICATE" in codes
    assert "HRC-CATALOG-INVALID" not in codes


def test_dangling_evidence_test_node_fails_exact_parity(
    repository_snapshot: Path,
) -> None:
    path = repository_snapshot / "contracts/hermes-runtime/evidence-register.yaml"
    document = _read_yaml(path)
    entry = next(item for item in document["entries"] if item["test_node_ids"])
    entry["test_node_ids"] = [
        "tests/hermes_runtime_contracts/test_missing.py::test_absent"
    ]
    _write_yaml(path, document)

    result = _run_cli("--repo", str(repository_snapshot), "--strict", "--json")

    assert result.returncode == 1
    findings = _json_result(result)["findings"]
    assert any(
        finding["code"] == "HRC-PARITY-DANGLING"
        and "test_missing.py::test_absent" in finding["message"]
        for finding in findings
    )


def test_pytest_node_collection_never_runs_test_bodies(
    repository_snapshot: Path,
) -> None:
    sentinel = repository_snapshot / (
        "tests/hermes_runtime_contracts/test_collection_only_sentinel.py"
    )
    sentinel.write_text(
        "def test_collection_only_sentinel():\n"
        "    raise AssertionError('validator executed a test body')\n",
        encoding="utf-8",
    )
    evidence_path = (
        repository_snapshot / "contracts/hermes-runtime/evidence-register.yaml"
    )
    evidence = _read_yaml(evidence_path)
    entry = next(item for item in evidence["entries"] if item["test_node_ids"])
    entry["test_node_ids"] = [
        "tests/hermes_runtime_contracts/"
        "test_collection_only_sentinel.py::test_collection_only_sentinel"
    ]
    _write_yaml(evidence_path, evidence)

    result = _run_cli("--repo", str(repository_snapshot), "--strict", "--json")

    assert result.returncode == 0, result.stdout + result.stderr
    assert _json_result(result)["status"] == "pass"
