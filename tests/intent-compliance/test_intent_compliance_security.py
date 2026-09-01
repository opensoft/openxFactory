from __future__ import annotations

import copy
from pathlib import Path

import pytest

from scripts.intent_compliance.discovery import (
    bounded_record_paths,
    discover_record_documents,
)
from scripts.intent_compliance.model import (
    InputLimitError,
    load_record_documents,
)
from scripts.intent_compliance.state_validation import (
    CanonicalizationError,
    canonical_digest,
)
from scripts.intent_compliance.validator import (
    RecordDocument,
    validate_documents,
)

ROOT = Path(__file__).resolve().parents[2]
POSITIVE = ROOT / "contracts" / "intent-compliance" / "examples" / "positive"


def _positive() -> list[RecordDocument]:
    return load_record_documents(sorted(POSITIVE.glob("*.yaml")))


def _codes(records: list[RecordDocument]) -> set[str]:
    return {finding.code for finding in validate_documents(records)}


def _decision(records: list[RecordDocument], gate: str) -> RecordDocument:
    return next(
        record
        for record in records
        if record.data.get("kind") == "compliance_decision"
        and record.data.get("enforcement_point") == gate
    )


def test_yaml_when_key_is_duplicated_then_input_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.yaml"
    path.write_text(
        "schema_version: 1\nkind: compliance_decision\nkind: policy_allowance\n"
    )

    with pytest.raises(InputLimitError, match="duplicate YAML key"):
        load_record_documents([path])


def test_yaml_when_alias_is_used_then_input_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "alias.yaml"
    path.write_text("schema_version: 1\nkind: policy_allowance\nx: &x [1]\ny: *x\n")

    with pytest.raises(InputLimitError, match="aliases are forbidden"):
        load_record_documents([path])


def test_yaml_when_document_exceeds_size_cap_then_input_is_rejected(
    tmp_path: Path,
) -> None:
    path = tmp_path / "large.yaml"
    path.write_text(
        "schema_version: 1\nkind: policy_allowance\npadding: " + "x" * 1_048_577
    )

    with pytest.raises(InputLimitError, match="byte limit"):
        load_record_documents([path])


def test_canonical_json_when_float_is_present_then_input_is_rejected() -> None:
    with pytest.raises(CanonicalizationError, match="integers only"):
        canonical_digest({"value": 0.5}, "digest")


def test_registry_when_applicable_history_forks_then_unique_head_is_rejected() -> None:
    records = _positive()
    registry = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
    )
    child = copy.deepcopy(registry.data)
    child["revision_id"] = "neutral.revision.fork"
    child["predecessor_revision_digest"] = registry.data["revision_digest"]
    child["published_at"] = "2026-01-15T00:00:00Z"
    child["revision_digest"] = canonical_digest(child, "revision_digest")
    sibling = copy.deepcopy(child)
    sibling["revision_id"] = "neutral.revision.sibling"
    sibling["revision_digest"] = canonical_digest(sibling, "revision_digest")

    findings = _codes(
        [
            *records,
            RecordDocument(registry.path, child),
            RecordDocument(registry.path, sibling),
        ]
    )

    assert "registry-chain-fork" in findings


def test_allowance_identity_when_registry_differs_then_id_is_not_globally_reused() -> (
    None
):
    records = _positive()
    registry = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
    )
    other = copy.deepcopy(registry.data)
    other["registry_id"] = "neutral.other-registry"
    other["revision_id"] = "neutral.other-revision.1"
    other["predecessor_revision_digest"] = None
    other["allowances"][0]["approval_digest"] = "sha256:" + "f" * 64
    other["revision_digest"] = canonical_digest(other, "revision_digest")

    findings = _codes([*records, RecordDocument(registry.path, other)])

    assert "allowance-id-reused" not in findings


def test_registry_when_newer_revision_exists_then_historical_selection_is_rejected() -> (
    None
):
    records = _positive()
    registry = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
    )
    future = copy.deepcopy(registry.data)
    future["revision_id"] = "neutral.revision.future"
    future["predecessor_revision_digest"] = registry.data["revision_digest"]
    future["published_at"] = "2028-01-01T00:00:00Z"
    future["revision_digest"] = canonical_digest(future, "revision_digest")

    findings = _codes([*records, RecordDocument(registry.path, future)])

    assert "current-registry" in findings


def test_terminal_decision_when_linear_head_revokes_then_history_is_rejected() -> None:
    records = _positive()
    admission = _decision(records, "admission")
    historical = next(
        record.data
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
        and record.data.get("revision_id") == "neutral.revision.1"
    )
    changed = copy.deepcopy(admission.data)
    changed["registry"] = {
        "status": "resolved",
        "registry_id": historical["registry_id"],
        "revision_id": historical["revision_id"],
        "revision_digest": historical["revision_digest"],
    }
    changed["resolutions"][0]["revocation_digests"] = []
    changed["deterministic_evidence"]["registry"] = copy.deepcopy(changed["registry"])
    changed["deterministic_evidence"]["evidence_digest"] = canonical_digest(
        changed["deterministic_evidence"], "evidence_digest"
    )
    changed_records = [
        RecordDocument(record.path, changed) if record is admission else record
        for record in records
    ]

    assert "current-registry" in _codes(changed_records)


def test_decision_when_credential_shaped_value_is_in_evidence_then_rejected() -> None:
    records = _positive()
    approval = _decision(records, "approval")
    changed = copy.deepcopy(approval.data)
    changed["correlation_refs"] = ["sk_live_abcdefghijklmnopqrstuvwxyz123456"]
    changed_records = [
        RecordDocument(record.path, changed) if record is approval else record
        for record in records
    ]

    assert "raw-evidence" in _codes(changed_records)


def test_registry_when_child_publication_is_not_monotonic_then_chain_is_rejected() -> (
    None
):
    records = _positive()
    child = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
        and record.data.get("revision_id") == "neutral.revision.2"
    )
    changed = copy.deepcopy(child.data)
    changed["published_at"] = "2026-01-01T00:00:00Z"
    changed["revision_digest"] = canonical_digest(changed, "revision_digest")
    changed_records = [
        RecordDocument(record.path, changed) if record is child else record
        for record in records
    ]

    assert "registry-chain-time" in _codes(changed_records)


def test_revocation_when_predecessor_is_not_effective_head_then_rejected() -> None:
    records = _positive()
    root = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
        and record.data.get("revision_id") == "neutral.revision.1"
    )
    intermediate = copy.deepcopy(root.data)
    intermediate["revision_id"] = "neutral.revision.intermediate"
    intermediate["predecessor_revision_digest"] = root.data["revision_digest"]
    intermediate["published_at"] = "2026-05-01T00:00:00Z"
    intermediate["revision_digest"] = canonical_digest(intermediate, "revision_digest")

    findings = _codes([*records, RecordDocument(root.path, intermediate)])

    assert "registry-chain" in findings


def test_revocation_when_approval_is_absent_from_predecessor_then_rejected() -> None:
    records = _positive()
    allowance = next(
        record for record in records if record.data.get("kind") == "policy_allowance"
    )
    revocation = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_revocation"
    )
    changed_allowance = copy.deepcopy(allowance.data)
    changed_allowance["allowance_id"] = "neutral.allowance.orphan"
    changed_allowance["approval_digest"] = canonical_digest(
        changed_allowance, "approval_digest"
    )
    changed_revocation = copy.deepcopy(revocation.data)
    changed_revocation["revocation_id"] = "neutral.revocation.orphan"
    changed_revocation["allowance_id"] = changed_allowance["allowance_id"]
    changed_revocation["approval_digest"] = changed_allowance["approval_digest"]
    changed_revocation["revocation_digest"] = canonical_digest(
        changed_revocation, "revocation_digest"
    )

    findings = _codes(
        [
            *records,
            RecordDocument(allowance.path, changed_allowance),
            RecordDocument(revocation.path, changed_revocation),
        ]
    )

    assert "registry-chain" in findings


def test_discovery_when_repository_has_too_many_eligible_files_then_scan_is_rejected(
    tmp_path: Path,
) -> None:
    for index in range(257):
        (tmp_path / f"record-{index}.yaml").write_text("kind: compliance_decision\n")

    with pytest.raises(InputLimitError, match="eligible input count exceeds"):
        bounded_record_paths(tmp_path)


@pytest.mark.parametrize(
    "content",
    [
        "{schema_version: 1, kind: compliance_decision}\n",
        "schema_version: 1\n? kind\n: compliance_decision\n",
    ],
)
def test_discovery_when_kind_uses_valid_yaml_syntax_then_record_is_discovered(
    tmp_path: Path, content: str
) -> None:
    path = tmp_path / "record.yaml"
    path.write_text(content, encoding="utf-8")

    documents = discover_record_documents([path])

    assert [document.data["kind"] for document in documents] == ["compliance_decision"]
