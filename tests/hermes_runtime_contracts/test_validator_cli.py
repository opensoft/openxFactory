"""RED subprocess contracts for the Hermes runtime validator entrypoint."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Final

import pytest

from tests.hermes_runtime_contracts.validator_cli_support import (
    empty_git_repo_fixture,
    json_result,
    load_entrypoint,
    run_cli,
)

IMPORTED_FIXTURES: Final = (empty_git_repo_fixture,)


def test_help_lists_the_complete_selection_and_resolver_surface() -> None:
    result = run_cli("--help")
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
    first = run_cli(*args)
    second = run_cli(*args)
    assert first.returncode == second.returncode == 2
    assert first.stdout == second.stdout
    payload = json_result(first)
    finding = payload["findings"][0]
    assert {"code", "severity", "case_id", "path", "message"} <= set(finding)
    assert finding["case_id"] == "not-an-indexed-case"


def test_human_output_is_deterministic_and_contains_a_stable_code(
    empty_git_repo: Path,
) -> None:
    args = ("--repo", str(empty_git_repo), "--case", "not-an-indexed-case")
    first = run_cli(*args)
    second = run_cli(*args)
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
    result = run_cli(mode_option, "--repo", str(empty_git_repo), "--json")
    assert result.returncode == 2
    assert json_result(result)["mode"] == expected_mode


def test_candidate_and_realization_modes_are_mutually_exclusive(
    empty_git_repo: Path,
) -> None:
    result = run_cli(
        "--require-candidate",
        "--require-realization",
        "--repo",
        str(empty_git_repo),
        "--json",
    )
    assert result.returncode == 2
    payload = json_result(result)
    assert "mutually exclusive" in payload["findings"][0]["message"].lower()


@pytest.mark.parametrize(
    "mode_option", ["--require-candidate", "--require-realization"]
)
def test_release_modes_require_a_domain_resolver_input(mode_option: str) -> None:
    # U7: candidate/realization require a domain resolver; its absence is a
    # dependency error (exit 2), never a silent pass.
    result = run_cli(mode_option, "--strict", "--json")

    assert result.returncode == 2
    payload = json_result(result)
    assert payload["status"] == "error"
    assert any(
        finding["code"] == "HRC-DOMAIN-RESOLVER-REQUIRED"
        for finding in payload["findings"]
    )


def test_candidate_mode_on_the_real_repository_requires_domain_mirrors(
    tmp_path: Path,
) -> None:
    # Post-realization (T079 cut contract-v1.9), the realized release digest
    # inventory is present, so --require-candidate no longer short-circuits at
    # HGR-RELEASE-INVENTORY-MISSING. It proceeds to live domain-regression
    # resolution, which fails closed as a dependency error (exit 2) when the
    # mirror root holds none of the supported repositories.
    result = run_cli(
        "--require-candidate",
        "--strict",
        "--domain-repo-root",
        str(tmp_path),
        "--json",
    )

    assert result.returncode == 2, result.stdout + result.stderr
    payload = json_result(result)
    assert payload["mode"] == "candidate"
    assert payload["status"] == "error"
    codes = {finding["code"] for finding in payload["findings"]}
    assert "HGR-REGRESSION-DEPENDENCY" in codes
    # The realized inventory exists now; the missing-inventory state is gone.
    assert "HGR-RELEASE-INVENTORY-MISSING" not in codes


@pytest.mark.parametrize(
    ("mode_option", "expected_mode"),
    [("--require-candidate", "candidate"), ("--require-realization", "realization")],
)
def test_release_mode_field_is_preserved_on_the_real_repository(
    tmp_path: Path, mode_option: str, expected_mode: str
) -> None:
    # An empty mirror root makes domain-regression resolution a dependency
    # error (exit 2); the mode field is still reported.
    result = run_cli(
        mode_option,
        "--domain-repo-root",
        str(tmp_path),
        "--json",
        timeout=60,
    )

    assert result.returncode == 2
    assert json_result(result)["mode"] == expected_mode


def test_handoff_receipt_without_a_consumer_repository_is_a_dependency_error(
    tmp_path: Path,
) -> None:
    # U7: --handoff-receipt implies consumer resolution; without a resolvable
    # consumer repository it is a dependency error (exit 2).
    receipt = tmp_path / "receipt.yaml"
    _ = receipt.write_text(
        "consumer_repository: opensoft/xFactory-Hermes-Install\n", encoding="utf-8"
    )
    result = run_cli("--handoff-receipt", str(receipt), "--json")

    assert result.returncode == 2
    payload = json_result(result)
    assert any(
        finding["code"] == "HRC-CONSUMER-RESOLVER-REQUIRED"
        for finding in payload["findings"]
    )


def test_repeatable_resolver_options_reach_validation_not_argparse(
    empty_git_repo: Path, tmp_path: Path
) -> None:
    mirror_root = tmp_path / "mirrors"
    mirror_root.mkdir()
    result = run_cli(
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
    assert json_result(result)["findings"][0]["case_id"] == "not-an-indexed-case"


def test_warning_escalation_and_exit_code_precedence_are_stable() -> None:
    cli = load_entrypoint()
    warning = [{"severity": "warning"}]
    error = [{"severity": "error"}]
    assert cli.classify_exit_code(warning, strict=False) == 0
    assert cli.classify_exit_code(warning, strict=True) == 1
    assert cli.classify_exit_code(error, strict=False) == 1
    assert cli.classify_exit_code([], strict=False, dependency_error=True) == 2


def test_invalid_phase_is_a_harness_error_without_a_traceback() -> None:
    result = run_cli("--phase", "database")
    assert result.returncode == 2
    assert "Traceback" not in result.stdout + result.stderr


def test_current_repository_strict_mode_executes_every_integration_gate() -> None:
    result = run_cli("--strict", "--json")

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json_result(result)
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
    first = run_cli(*args)
    second = run_cli(*args)

    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    selection = json_result(first)["selection"]
    assert selection["case_id"] == "topology-operational-two-customers"
    assert selection["phase"] == "semantic"
    assert selection["case_ids"] == ["topology-operational-two-customers"]
