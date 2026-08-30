from __future__ import annotations

import shutil
from pathlib import Path
from typing import Final

from tests.hermes_runtime_contracts.validator_cli_support import (
    CHANGE_ID,
    governed_change_specs_path,
    json_result,
    read_yaml,
    repository_snapshot_fixture,
    run_cli,
    write_yaml,
    yaml_mapping,
)

IMPORTED_FIXTURES: Final = (repository_snapshot_fixture,)


def test_duplicate_archived_governed_change_fails_closed(
    repository_snapshot: Path,
) -> None:
    original = repository_snapshot / governed_change_specs_path(repository_snapshot)
    duplicate = (
        repository_snapshot
        / "openspec/changes/archive"
        / f"2099-01-01-{CHANGE_ID}"
        / "specs"
    )
    _ = duplicate.parent.mkdir(parents=True)
    _ = shutil.copytree(original, duplicate)

    result = run_cli("--repo", str(repository_snapshot), "--strict", "--json")

    assert result.returncode == 1
    codes = {finding["code"] for finding in json_result(result)["findings"]}
    assert codes == {"HRC-OPENSPEC-ARCHIVE-AMBIGUOUS"}


def test_incomplete_archived_governed_change_directory_is_ignored(
    repository_snapshot: Path,
) -> None:
    incomplete = (
        repository_snapshot / "openspec/changes/archive" / f"2099-01-01-{CHANGE_ID}"
    )
    _ = incomplete.mkdir(parents=True)

    result = run_cli("--repo", str(repository_snapshot), "--strict", "--json")

    assert result.returncode == 0, result.stdout + result.stderr
    assert json_result(result)["status"] == "pass"


def test_malformed_canonical_catalog_fails_closed(
    repository_snapshot: Path,
) -> None:
    path = repository_snapshot / "contracts/hermes-runtime/contract-index.yaml"
    document = read_yaml(path)
    contracts = document["contracts"]
    assert isinstance(contracts, list)
    first = yaml_mapping(contracts[0])
    second = yaml_mapping(contracts[1])
    second["contract_id"] = first["contract_id"]
    write_yaml(path, document)

    result = run_cli("--repo", str(repository_snapshot), "--strict", "--json")

    assert result.returncode == 1
    codes = {finding["code"] for finding in json_result(result)["findings"]}
    assert codes == {"HRC-CATALOG-INVALID"}


def test_malformed_fixture_index_fails_for_index_reason(
    repository_snapshot: Path,
) -> None:
    path = repository_snapshot / "contracts/hermes-runtime/fixtures/index.yaml"
    document = read_yaml(path)
    cases = document["cases"]
    assert isinstance(cases, list)
    first = yaml_mapping(cases[0])
    second = yaml_mapping(cases[1])
    inputs = first["inputs"]
    assert isinstance(inputs, list)
    second["inputs"] = list(inputs)
    write_yaml(path, document)

    result = run_cli("--repo", str(repository_snapshot), "--strict", "--json")

    assert result.returncode == 1
    codes = {finding["code"] for finding in json_result(result)["findings"]}
    assert "HGR-FIXTURE-PATH-DUPLICATE" in codes
    assert "HRC-CATALOG-INVALID" not in codes


def test_dangling_evidence_test_node_fails_exact_parity(
    repository_snapshot: Path,
) -> None:
    path = repository_snapshot / "contracts/hermes-runtime/evidence-register.yaml"
    document = read_yaml(path)
    entries = document["entries"]
    assert isinstance(entries, list)
    mapped_entries = [yaml_mapping(item) for item in entries]
    entry = next(item for item in mapped_entries if item["test_node_ids"])
    entry["test_node_ids"] = [
        "tests/hermes_runtime_contracts/test_missing.py::test_absent"
    ]
    write_yaml(path, document)

    result = run_cli("--repo", str(repository_snapshot), "--strict", "--json")

    assert result.returncode == 1
    findings = json_result(result)["findings"]
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
    _ = sentinel.write_text(
        """def test_collection_only_sentinel():
    raise AssertionError('validator executed a test body')
""",
        encoding="utf-8",
    )
    evidence_path = (
        repository_snapshot / "contracts/hermes-runtime/evidence-register.yaml"
    )
    evidence = read_yaml(evidence_path)
    entries = evidence["entries"]
    assert isinstance(entries, list)
    mapped_entries = [yaml_mapping(item) for item in entries]
    entry = next(item for item in mapped_entries if item["test_node_ids"])
    entry["test_node_ids"] = [
        "tests/hermes_runtime_contracts/test_collection_only_sentinel.py::test_collection_only_sentinel"
    ]
    write_yaml(evidence_path, evidence)

    result = run_cli("--repo", str(repository_snapshot), "--strict", "--json")

    assert result.returncode == 0, result.stdout + result.stderr
    assert json_result(result)["status"] == "pass"
