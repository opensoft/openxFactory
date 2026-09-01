from __future__ import annotations

import os
from pathlib import Path

import pytest

from scripts.intent_compliance.model import InputLimitError, load_single_mapping_text
from scripts.intent_compliance.negative_corpus import negative_case_documents
from scripts.intent_compliance.validator import (
    expected_failure_code,
    load_record_documents,
    validate_documents,
)

ROOT = Path(__file__).resolve().parents[2]
NEGATIVE = ROOT / "contracts" / "intent-compliance" / "examples" / "negative"
POSITIVE = ROOT / "contracts" / "intent-compliance" / "examples" / "positive"
EXPECTED_CODES = {
    "allowance-reference-substitution.yaml": {"allowance-reference-substitution"},
    "approval-content-changed.yaml": {"enforcement-binding"},
    "classifier-error-as-allow.yaml": {
        "classifier-outcome",
        "composition-outcome",
    },
    "duplicate-class-id.yaml": {"duplicate-class-id"},
    "hermes-review-as-allow.yaml": {"composition-outcome"},
    "indeterminate-scope-as-allow.yaml": {"composition-outcome", "scope-outcome"},
    "missing-classifier-limits.yaml": {"schema"},
    "raw-intent-evidence.yaml": {"raw-evidence", "schema"},
    "reused-allowance-id.yaml": {"allowance-id-reused", "registry-append-only"},
    "unauthorized-issuer.yaml": {"authority-attribution"},
    "unauthorized-revoker.yaml": {"authority-attribution"},
    "unclaimed-veto-as-allow.yaml": {
        "allowance-claim-closure",
        "composition-outcome",
    },
}


@pytest.mark.parametrize("path", sorted(NEGATIVE.glob("*.yaml")), ids=lambda path: path.name)
def test_negative_fixture_when_validated_then_fails_for_declared_reason(path: Path) -> None:
    expected = expected_failure_code(path)
    baseline = load_record_documents(sorted(POSITIVE.glob("*.yaml")))
    records = negative_case_documents(path, baseline)

    findings = validate_documents(records)

    codes = {finding.code for finding in findings}
    assert expected in codes
    assert codes == EXPECTED_CODES[path.name]


def test_negative_corpus_when_loaded_then_covers_required_failure_paths() -> None:
    codes = {expected_failure_code(path) for path in NEGATIVE.glob("*.yaml")}

    assert {
        "duplicate-class-id",
        "authority-attribution",
        "schema",
        "classifier-outcome",
        "composition-outcome",
        "allowance-reference-substitution",
    } <= codes


def test_negative_fixture_when_oversized_then_rejected_before_loading(
    tmp_path: Path,
) -> None:
    path = tmp_path / "oversized.yaml"
    path.write_text(
        "schema_version: 1\nkind: intent_compliance_negative_fixture\npadding: "
        + "x" * 1_048_576,
        encoding="utf-8",
    )

    with pytest.raises(InputLimitError, match="input exceeds"):
        negative_case_documents(path, [])


def test_negative_fixture_when_symlinked_then_rejected_before_loading(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.yaml"
    target.write_text(
        "schema_version: 1\nkind: intent_compliance_negative_fixture\n"
        "mutation: duplicate_class_id\n",
        encoding="utf-8",
    )
    path = tmp_path / "fixture.yaml"
    path.symlink_to(target)

    with pytest.raises(InputLimitError, match="regular file"):
        negative_case_documents(path, [])


@pytest.mark.parametrize("fixture_kind", ["oversized", "symlink", "fifo"])
def test_negative_fixture_metadata_when_input_is_hostile_then_rejected_before_reading(
    tmp_path: Path, fixture_kind: str
) -> None:
    path = tmp_path / "fixture.yaml"
    if fixture_kind == "oversized":
        path.write_text("x" * 1_048_577, encoding="utf-8")
    elif fixture_kind == "symlink":
        target = tmp_path / "target.yaml"
        target.write_text(
            "# expected-failure: schema\n# requirement: closed-bounded-redacted-decisions\n",
            encoding="utf-8",
        )
        path.symlink_to(target)
    else:
        os.mkfifo(path)

    with pytest.raises(InputLimitError):
        expected_failure_code(path)


@pytest.mark.parametrize("path", sorted(NEGATIVE.glob("*.yaml")), ids=lambda path: path.name)
def test_negative_fixture_when_published_then_has_versioned_envelope(path: Path) -> None:
    descriptor = load_single_mapping_text(path.read_text(encoding="utf-8"), path)

    assert descriptor["schema_version"] == 1
    assert descriptor["kind"] == "intent_compliance_negative_fixture"
