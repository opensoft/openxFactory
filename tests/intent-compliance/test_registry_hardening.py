from __future__ import annotations

import copy
from pathlib import Path

from scripts.intent_compliance.model import RecordDocument, load_record_documents
from scripts.intent_compliance.state_validation import canonical_digest
from scripts.intent_compliance.validator import validate_documents

ROOT = Path(__file__).resolve().parents[2]
POSITIVE = ROOT / "contracts" / "intent-compliance" / "examples" / "positive"


def _positive() -> list[RecordDocument]:
    return load_record_documents(sorted(POSITIVE.glob("*.yaml")))


def _codes(records: list[RecordDocument]) -> set[str]:
    return {finding.code for finding in validate_documents(records)}


def test_registry_when_revision_repeats_allowance_id_then_rejected() -> None:
    records = _positive()
    latest = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
        and record.data.get("revision_id") == "neutral.revision.2"
    )
    changed = copy.deepcopy(latest.data)
    changed["allowances"].append(copy.deepcopy(changed["allowances"][0]))
    changed["revision_digest"] = canonical_digest(changed, "revision_digest")
    changed_records = [
        RecordDocument(record.path, changed) if record is latest else record
        for record in records
    ]

    codes = _codes(changed_records)

    assert "registry-duplicate-allowance" in codes


def test_revocations_when_allowance_history_has_two_roots_then_rejected() -> None:
    records = _positive()
    revocation = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_revocation"
    )
    second_root = copy.deepcopy(revocation.data)
    second_root["revocation_id"] = "neutral.revocation.second-root"
    second_root["revoked_at"] = "2026-06-01T00:00:01Z"
    second_root["revocation_digest"] = canonical_digest(
        second_root, "revocation_digest"
    )
    latest = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
        and record.data.get("revision_id") == "neutral.revision.2"
    )
    changed_registry = copy.deepcopy(latest.data)
    changed_registry["allowances"][0]["revocation_digests"].append(
        second_root["revocation_digest"]
    )
    changed_registry["revision_digest"] = canonical_digest(
        changed_registry, "revision_digest"
    )
    changed_records = [
        RecordDocument(record.path, changed_registry) if record is latest else record
        for record in records
    ]
    changed_records.append(RecordDocument(revocation.path, second_root))

    codes = _codes(changed_records)

    assert "revocation-chain-root" in codes


def test_revocation_when_child_predates_predecessor_then_rejected() -> None:
    records = _positive()
    revocation = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_revocation"
    )
    child = copy.deepcopy(revocation.data)
    child["revocation_id"] = "neutral.revocation.child"
    child["predecessor_event_digest"] = revocation.data["revocation_digest"]
    child["revoked_at"] = "2026-05-31T23:59:59Z"
    child["revocation_digest"] = canonical_digest(child, "revocation_digest")
    latest = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
        and record.data.get("revision_id") == "neutral.revision.2"
    )
    changed_registry = copy.deepcopy(latest.data)
    changed_registry["allowances"][0]["revocation_digests"].append(
        child["revocation_digest"]
    )
    changed_registry["revision_digest"] = canonical_digest(
        changed_registry, "revision_digest"
    )
    changed_records = [
        RecordDocument(record.path, changed_registry) if record is latest else record
        for record in records
    ]
    changed_records.append(RecordDocument(revocation.path, child))

    codes = _codes(changed_records)

    assert "revocation-chain-time" in codes


def test_registry_when_entry_has_no_matching_approval_record_then_rejected() -> None:
    records = _positive()
    latest = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
        and record.data.get("revision_id") == "neutral.revision.2"
    )
    changed = copy.deepcopy(latest.data)
    changed["allowances"].append(
        {
            "allowance_id": "neutral.allowance.orphan",
            "approval_digest": "sha256:" + "f" * 64,
            "revocation_digests": [],
        }
    )
    changed["revision_digest"] = canonical_digest(changed, "revision_digest")
    changed_records = [
        RecordDocument(record.path, changed) if record is latest else record
        for record in records
    ]

    assert "registry-approval" in _codes(changed_records)
