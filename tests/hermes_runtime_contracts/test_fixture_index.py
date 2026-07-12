"""RED contract tests for the self-describing fixture index (T007)."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from scripts.hermes_runtime_validation.fixtures import (
    dependency_order,
    evaluate_expected_findings,
    validate_index,
)
from tests.hermes_runtime_contracts.support import finding_codes


def _case(
    case_id: str,
    path: str,
    *,
    phase: str = "structural",
    depends_on: list[str] | None = None,
    evaluation_time: str | None = None,
    outcome: str = "pass",
    primary: str | None = None,
    secondary: list[str] | None = None,
) -> dict:
    case = {
        "case_id": case_id,
        "phase": phase,
        "class": "valid" if outcome == "pass" else "invalid",
        "requirement_ids": ["HCS-001"],
        "scenario_ids": ["HCS-001-S01"],
        "inputs": [path],
        "depends_on": depends_on or [],
        "expected": {
            "outcome": outcome,
            "allowed_secondary_codes": secondary or [],
        },
        "evidence_id": f"EVIDENCE-{case_id.upper()}",
    }
    if evaluation_time is not None:
        case["evaluation_time"] = evaluation_time
    if primary is not None:
        case["expected"]["primary_finding_code"] = primary
    return case


def _index(*cases: dict) -> dict:
    return {
        "schema_version": 1,
        "kind": "hermes-runtime-fixture-index",
        "cases": list(cases),
    }


def _codes(index: dict, fixture_root: Path) -> list[str]:
    return finding_codes(validate_index(index, fixture_root=fixture_root))


def test_valid_index_has_no_findings(tmp_path: Path) -> None:
    fixture_root = tmp_path / "fixtures"
    (fixture_root / "topology").mkdir(parents=True)
    (fixture_root / "topology" / "valid.yaml").write_text("{}\n", encoding="utf-8")
    index = _index(_case("topology-valid", "topology/valid.yaml"))

    assert validate_index(index, fixture_root=fixture_root) == []


def test_duplicate_fixture_paths_fail_even_across_different_cases(tmp_path: Path) -> None:
    fixture_root = tmp_path / "fixtures"
    (fixture_root / "shared.yaml").parent.mkdir(parents=True)
    (fixture_root / "shared.yaml").write_text("{}\n", encoding="utf-8")
    index = _index(
        _case("first", "shared.yaml"),
        _case("second", "shared.yaml"),
    )

    assert "HGR-FIXTURE-PATH-DUPLICATE" in _codes(index, fixture_root)


def test_selected_case_includes_transitive_dependencies_in_stable_order() -> None:
    index = _index(
        _case("base", "base.yaml"),
        _case("middle", "middle.yaml", depends_on=["base"]),
        _case("leaf", "leaf.yaml", depends_on=["middle"]),
    )

    assert dependency_order(index, selected_case_ids=["leaf"]) == (
        "base",
        "middle",
        "leaf",
    )


def test_missing_dependency_fails_closed(tmp_path: Path) -> None:
    index = _index(_case("leaf", "leaf.yaml", depends_on=["absent"]))

    codes = _codes(index, tmp_path)
    assert "HGR-FIXTURE-DEPENDENCY-MISSING" in codes
    assert "HGR-FIXTURE-DEPENDENCY-CYCLE" not in codes


def test_dependency_cycle_fails_closed(tmp_path: Path) -> None:
    index = _index(
        _case("alpha", "alpha.yaml", depends_on=["beta"]),
        _case("beta", "beta.yaml", depends_on=["alpha"]),
    )

    assert "HGR-FIXTURE-DEPENDENCY-CYCLE" in _codes(index, tmp_path)


def test_semantic_case_requires_fixed_evaluation_time(tmp_path: Path) -> None:
    index = _index(_case("semantic", "semantic.yaml", phase="semantic"))

    assert "HGR-FIXTURE-EVALUATION-TIME-REQUIRED" in _codes(index, tmp_path)


def test_semantic_case_accepts_canonical_utc_evaluation_time(tmp_path: Path) -> None:
    case = _case(
        "semantic",
        "semantic.yaml",
        phase="semantic",
        evaluation_time="2026-07-12T12:00:00Z",
    )
    fixture_root = tmp_path / "fixtures"
    fixture_root.mkdir()
    (fixture_root / "semantic.yaml").write_text("{}\n", encoding="utf-8")

    assert validate_index(_index(case), fixture_root=fixture_root) == []


def test_negative_case_requires_stable_primary_finding_code(tmp_path: Path) -> None:
    index = _index(_case("invalid", "invalid.yaml", outcome="fail"))

    assert "HGR-FIXTURE-PRIMARY-CODE-REQUIRED" in _codes(index, tmp_path)


def test_wrong_reason_does_not_satisfy_negative_fixture() -> None:
    case = _case(
        "invalid",
        "invalid.yaml",
        outcome="fail",
        primary="HCS-TOPOLOGY-CUSTOMER-MIN",
    )

    result = evaluate_expected_findings(
        case,
        [{"code": "HCS-SCHEMA-REQUIRED", "path": "layers"}],
    )

    assert result["passed"] is False
    assert result["missing_primary"] is True


def test_primary_and_declared_secondary_findings_satisfy_fixture() -> None:
    case = _case(
        "invalid",
        "invalid.yaml",
        outcome="fail",
        primary="HCS-TOPOLOGY-CUSTOMER-MIN",
        secondary=["HCS-TOPOLOGY-READINESS"],
    )
    findings = [
        {"code": "HCS-TOPOLOGY-READINESS", "path": "state"},
        {"code": "HCS-TOPOLOGY-CUSTOMER-MIN", "path": "layers"},
    ]

    result = evaluate_expected_findings(case, findings)

    assert result["passed"] is True
    assert result["actual_codes"] == (
        "HCS-TOPOLOGY-CUSTOMER-MIN",
        "HCS-TOPOLOGY-READINESS",
    )


def test_unapproved_secondary_finding_rejects_fixture() -> None:
    case = deepcopy(
        _case(
            "invalid",
            "invalid.yaml",
            outcome="fail",
            primary="HCS-TOPOLOGY-CUSTOMER-MIN",
        )
    )
    result = evaluate_expected_findings(
        case,
        [
            {"code": "HCS-TOPOLOGY-CUSTOMER-MIN", "path": "layers"},
            {"code": "HCS-UNRELATED", "path": "other"},
        ],
    )

    assert result["passed"] is False
    assert result["unexpected_codes"] == ("HCS-UNRELATED",)
