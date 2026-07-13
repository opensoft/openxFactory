"""RED contract tests for the self-describing fixture index (T007)."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess

import pytest

from scripts.hermes_runtime_validation.fixtures import (
    collect_database_test_count,
    database_matrix_identity,
    dependency_order,
    evaluate_expected_findings,
    repository_source_identity,
    validate_index,
)
from scripts.hermes_runtime_validation.loader import load_yaml_document
from tests.hermes_runtime_contracts.support import finding_codes

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


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


def test_duplicate_fixture_paths_fail_even_across_different_cases(
    tmp_path: Path,
) -> None:
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


def _git(repository: Path, *arguments: str) -> None:
    result = subprocess.run(
        ["git", *arguments],
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def _database_index_fixture(tmp_path: Path) -> tuple[dict, Path, Path, dict]:
    fixture_root = tmp_path / "contracts/hermes-runtime/fixtures"
    fixture_root.mkdir(parents=True)
    postgres_root = tmp_path / "tests/hermes_runtime_contracts/postgres"
    test_module = postgres_root / "test_matrix.py"
    seed = postgres_root / "fixtures/seed.sql"
    assertion = postgres_root / "assertions/check.sql"
    result_path = postgres_root / "evidence/postgres-15.json"
    for path in (test_module, seed, assertion):
        path.parent.mkdir(parents=True, exist_ok=True)
    test_module.write_text(
        "import pytest\n"
        "pytestmark = pytest.mark.postgres\n"
        "def test_matrix():\n"
        "    assert True\n",
        encoding="utf-8",
    )
    seed.write_text("select 1;\n", encoding="utf-8")
    assertion.write_text("select 1;\n", encoding="utf-8")
    (tmp_path / "pytest.ini").write_text(
        "[pytest]\nmarkers =\n    postgres: synthetic database matrix\n",
        encoding="utf-8",
    )
    image = "postgres@sha256:" + "a" * 64
    image_lock = postgres_root / "images.lock.yaml"
    image_lock.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "kind": "HermesRuntimePostgresImageLock",
                "images": {
                    "15": {
                        "source_tag": "postgres:15",
                        "resolved_image": image,
                        "platform": "linux/amd64",
                        "update_evidence": {},
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    case = _case("postgres-matrix", "unused.yaml", phase="database")
    case["inputs"] = []
    case["database"] = {
        "engine": "postgresql",
        "supported_majors": [15],
        "source_paths": ["pytest.ini"],
        "test_modules": ["tests/hermes_runtime_contracts/postgres/test_matrix.py"],
        "seed_scripts": ["tests/hermes_runtime_contracts/postgres/fixtures/seed.sql"],
        "assertion_scripts": [
            "tests/hermes_runtime_contracts/postgres/assertions/check.sql"
        ],
        "row_expectations": {"customer_layers": 2},
        "digest_expectations": {"artifact_body_reverified": True},
        "authoritative_deltas": ["rejected operations write no governed rows"],
        "result_refs": [
            {
                "major": 15,
                "path": "tests/hermes_runtime_contracts/postgres/evidence/postgres-15.json",
                "expected_outcome": "pass",
            }
        ],
    }
    index = _index(case)
    _git(tmp_path, "init", "--quiet")
    _git(tmp_path, "config", "user.name", "Fixture Tests")
    _git(tmp_path, "config", "user.email", "fixtures@example.invalid")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "--quiet", "-m", "database fixture")
    result = {
        "schema_version": 1,
        "kind": "HermesRuntimePostgresEvidence",
        "major": 15,
        "outcome": "pass",
        "image": image,
        "source_identity": repository_source_identity(tmp_path, case),
        "suite": {
            "id": "hermes-runtime-postgres",
            "test_count": collect_database_test_count(tmp_path, case["database"], 15),
        },
        "matrix": database_matrix_identity(case),
    }
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(
        json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    return index, fixture_root, result_path, result


def test_database_case_requires_exact_bound_result_evidence(tmp_path: Path) -> None:
    index, fixture_root, _, _ = _database_index_fixture(tmp_path)

    assert (
        validate_index(
            index,
            fixture_root=fixture_root,
            repository_root=tmp_path,
        )
        == []
    )

    index["cases"][0]["database"]["supported_majors"] = [17]
    assert "HGR-FIXTURE-DATABASE-MAJORS" in finding_codes(
        validate_index(
            index,
            fixture_root=fixture_root,
            repository_root=tmp_path,
        )
    )


def test_database_source_inventory_rejects_cross_category_duplicates(
    tmp_path: Path,
) -> None:
    index, fixture_root, _, _ = _database_index_fixture(tmp_path)
    duplicate = index["cases"][0]["database"]["test_modules"][0]
    index["cases"][0]["database"]["source_paths"].append(duplicate)

    assert "HGR-FIXTURE-DATABASE-PATH-DUPLICATE" in finding_codes(
        validate_index(index, fixture_root=fixture_root, repository_root=tmp_path)
    )


@pytest.mark.parametrize(
    ("field", "replacement", "expected_code"),
    [
        ("schema_version", 2, "HGR-FIXTURE-DATABASE-RESULT-IDENTITY"),
        ("kind", "WrongEvidence", "HGR-FIXTURE-DATABASE-RESULT-IDENTITY"),
        ("major", 16, "HGR-FIXTURE-DATABASE-RESULT-MAJOR"),
        ("outcome", "fail", "HGR-FIXTURE-DATABASE-RESULT-OUTCOME"),
        ("image", "postgres@sha256:" + "b" * 64, "HGR-FIXTURE-DATABASE-RESULT-IMAGE"),
        (
            "source_identity",
            {
                "identity_kind": "canonical_content",
                "profile": "xfactory-postgres-source-inputs-v1",
                "member_count": 4,
                "digest": "sha256:" + "b" * 64,
            },
            "HGR-FIXTURE-DATABASE-RESULT-SOURCE",
        ),
        (
            "suite",
            {"id": "hermes-runtime-postgres", "test_count": 999},
            "HGR-FIXTURE-DATABASE-RESULT-SUITE",
        ),
        (
            "matrix",
            {
                "profile": "xfactory-postgres-matrix-v1",
                "case_id": "postgres-matrix",
                "digest": "sha256:" + "b" * 64,
            },
            "HGR-FIXTURE-DATABASE-RESULT-MATRIX",
        ),
    ],
)
def test_database_result_mismatch_fails_for_exact_reason(
    tmp_path: Path, field: str, replacement: object, expected_code: str
) -> None:
    index, fixture_root, result_path, result = _database_index_fixture(tmp_path)
    result[field] = replacement
    result_path.write_text(json.dumps(result), encoding="utf-8")

    assert expected_code in finding_codes(
        validate_index(index, fixture_root=fixture_root, repository_root=tmp_path)
    )


def test_database_result_rejects_malformed_or_stale_source_evidence(
    tmp_path: Path,
) -> None:
    index, fixture_root, result_path, result = _database_index_fixture(tmp_path)
    result_path.write_text('{"major":15,"major":16}\n', encoding="utf-8")
    assert "HGR-FIXTURE-DATABASE-RESULT-DOCUMENT" in finding_codes(
        validate_index(index, fixture_root=fixture_root, repository_root=tmp_path)
    )

    result_path.write_text(json.dumps(result), encoding="utf-8")
    tracked = tmp_path / "tests/hermes_runtime_contracts/postgres/test_matrix.py"
    tracked.write_text(
        tracked.read_text(encoding="utf-8") + "# changed\n", encoding="utf-8"
    )
    assert "HGR-FIXTURE-DATABASE-RESULT-SOURCE" in finding_codes(
        validate_index(index, fixture_root=fixture_root, repository_root=tmp_path)
    )


def test_database_result_rejects_changed_explicit_source_path(tmp_path: Path) -> None:
    index, fixture_root, _, _ = _database_index_fixture(tmp_path)
    source = tmp_path / "pytest.ini"
    source.write_text(
        source.read_text(encoding="utf-8") + "# changed\n", encoding="utf-8"
    )

    assert "HGR-FIXTURE-DATABASE-RESULT-SOURCE" in finding_codes(
        validate_index(index, fixture_root=fixture_root, repository_root=tmp_path)
    )


def test_database_source_identity_survives_result_commit_and_clean_clone(
    tmp_path: Path,
) -> None:
    index, fixture_root, _, result = _database_index_fixture(tmp_path)
    assert result["source_identity"] == {
        "identity_kind": "canonical_content",
        "profile": "xfactory-postgres-source-inputs-v1",
        "member_count": 4,
        "digest": result["source_identity"]["digest"],
    }

    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "--quiet", "-m", "commit database evidence")
    assert (
        validate_index(index, fixture_root=fixture_root, repository_root=tmp_path) == []
    )

    clone = tmp_path.parent / f"{tmp_path.name}-clone"
    _git(tmp_path.parent, "clone", "--quiet", str(tmp_path), str(clone))
    assert (
        validate_index(
            index,
            fixture_root=clone / "contracts/hermes-runtime/fixtures",
            repository_root=clone,
        )
        == []
    )


def test_database_source_identity_ignores_unindexed_repository_changes(
    tmp_path: Path,
) -> None:
    index, fixture_root, _, _ = _database_index_fixture(tmp_path)
    (tmp_path / "unrelated.txt").write_text("not a matrix input\n", encoding="utf-8")

    assert (
        validate_index(index, fixture_root=fixture_root, repository_root=tmp_path) == []
    )


def test_current_fixture_index_preserves_110_cases() -> None:
    # 79 US1/US2/US3 cases plus the 31 appended US4 jobs/release/regression/handoff
    # semantic and structural cases registered at the T077 provider gate.
    index = load_yaml_document(
        REPOSITORY_ROOT / "contracts/hermes-runtime/fixtures/index.yaml"
    )
    assert len(index["cases"]) == 110


def test_fixture_self_description_must_match_index_metadata(tmp_path: Path) -> None:
    fixture_root = tmp_path / "fixtures"
    fixture_root.mkdir()
    (fixture_root / "authority.yaml").write_text(
        "case_id: authority-case\n"
        "phase: semantic\n"
        "class: invalid\n"
        "requirement_ids: [HGR-003]\n"
        "scenario_ids: [HGR-003-S04]\n"
        'evaluation_time: "2026-07-12T12:00:00Z"\n'
        "expected:\n"
        "  outcome: fail\n"
        "  primary_finding_code: HGR-GRANT-CYCLE\n",
        encoding="utf-8",
    )
    case = _case(
        "authority-case",
        "authority.yaml",
        phase="semantic",
        evaluation_time="2026-07-12T12:00:00Z",
        outcome="fail",
        primary="HGR-GRANT-SELF-ISSUED",
    )
    case["requirement_ids"] = ["HGR-003"]
    case["scenario_ids"] = ["HGR-003-S03"]

    assert "HGR-FIXTURE-SELF-DESCRIPTION-MISMATCH" in finding_codes(
        validate_index(_index(case), fixture_root=fixture_root)
    )
