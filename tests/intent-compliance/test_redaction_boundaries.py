from __future__ import annotations

import copy
from pathlib import Path

import pytest

from scripts.intent_compliance.model import RecordDocument, load_record_documents
from scripts.intent_compliance.validator import validate_documents

ROOT = Path(__file__).resolve().parents[2]
POSITIVE = ROOT / "contracts" / "intent-compliance" / "examples" / "positive"


def _positive() -> list[RecordDocument]:
    return load_record_documents(sorted(POSITIVE.glob("*.yaml")))


def _codes(records: list[RecordDocument]) -> set[str]:
    return {finding.code for finding in validate_documents(records)}


@pytest.mark.parametrize(
    "credential",
    [
        "sk_live_abcdefghijklmnopqrstuvwxyz123456",
        "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij123456",
        "github_pat_11ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz123456",
        "glpat-ABCDEFGHIJKLMNOPQRSTUVWXYZ1234",
        "AKIAABCDEFGHIJKLMNOP",
        "xoxb-1234567890-abcdefghijklmnop",
    ],
)
def test_decision_when_credential_shaped_value_is_in_evidence_then_rejected(
    credential: str,
) -> None:
    records = _positive()
    decision = next(
        record
        for record in records
        if record.data.get("kind") == "compliance_decision"
        and record.data.get("enforcement_point") == "approval"
    )
    changed = copy.deepcopy(decision.data)
    changed["correlation_refs"] = [credential]
    changed_records = [
        RecordDocument(record.path, changed) if record is decision else record
        for record in records
    ]

    assert "raw-evidence" in _codes(changed_records)


def test_decision_when_credential_is_mapping_key_then_diagnostic_redacts_it() -> None:
    credential = "sk_live_abcdefghijklmnopqrstuvwxyz123456"
    document = RecordDocument(
        Path("candidate.yaml"),
        {
            "schema_version": 1,
            "kind": "compliance_decision",
            credential: credential,
        },
    )

    findings = validate_documents([document])

    assert any(finding.code == "raw-evidence" for finding in findings)
    assert all(credential not in finding.message for finding in findings)
    assert sum(finding.code == "raw-evidence" for finding in findings) == 1
