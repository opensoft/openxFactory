from __future__ import annotations

import copy
import subprocess
from pathlib import Path

from scripts.intent_compliance import authority_validation
from scripts.intent_compliance.model import RecordDocument, load_record_documents
from scripts.intent_compliance.schema_validation import (
    schema_findings,
    schema_validators,
)
from scripts.intent_compliance.state_validation import canonical_digest
from scripts.intent_compliance.validator import validate_documents

ROOT = Path(__file__).resolve().parents[2]
POSITIVE = ROOT / "contracts" / "intent-compliance" / "examples" / "positive"


def _positive() -> list[RecordDocument]:
    return load_record_documents(sorted(POSITIVE.glob("*.yaml")))


def _codes(records: list[RecordDocument]) -> set[str]:
    return {finding.code for finding in validate_documents(records)}


def _git(repository: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def test_registry_when_listed_revocation_record_is_missing_then_rejected() -> None:
    # Given
    records = _positive()
    latest = next(
        record
        for record in records
        if record.data.get("kind") == "policy_allowance_registry"
        and record.data.get("revision_id") == "neutral.revision.2"
    )
    changed = copy.deepcopy(latest.data)
    entry = changed["allowances"][0]
    assert isinstance(entry, dict)
    entry["revocation_digests"] = ["sha256:" + "f" * 64]
    changed["revision_digest"] = canonical_digest(changed, "revision_digest")
    changed_records = [
        RecordDocument(record.path, changed) if record is latest else record
        for record in records
    ]

    # When
    codes = _codes(changed_records)

    # Then
    assert "registry-revocation" in codes


def test_allowance_when_role_exists_only_in_other_vocabulary_digest_then_rejected() -> (
    None
):
    # Given
    records = _positive()
    vocabulary = next(
        record
        for record in records
        if record.data.get("kind") == "veto_class_vocabulary"
    )
    allowance = next(
        record for record in records if record.data.get("kind") == "policy_allowance"
    )
    substituted_vocabulary = copy.deepcopy(vocabulary.data)
    substituted_vocabulary["classes"][0]["allowance_issuer_roles"] = [
        "neutral.substituted_issuer"
    ]
    substituted_vocabulary["vocabulary_digest"] = canonical_digest(
        substituted_vocabulary, "vocabulary_digest"
    )
    changed_allowance = copy.deepcopy(allowance.data)
    issuer = changed_allowance["issuer"]
    assert isinstance(issuer, dict)
    issuer["authority_role"] = "neutral.substituted_issuer"
    changed_allowance["approval_digest"] = canonical_digest(
        changed_allowance, "approval_digest"
    )
    changed_records = [
        RecordDocument(record.path, changed_allowance)
        if record is allowance
        else record
        for record in records
    ]
    changed_records.append(RecordDocument(vocabulary.path, substituted_vocabulary))

    # When
    codes = _codes(changed_records)

    # Then
    assert "authority-attribution" in codes


def test_policy_approval_when_principal_and_role_are_missing_then_schema_rejects() -> (
    None
):
    # Given
    records = _positive()
    allowance = next(
        record for record in records if record.data.get("kind") == "policy_allowance"
    )
    changed = copy.deepcopy(allowance.data)
    approval = changed["policy_approval"]
    assert isinstance(approval, dict)
    approval.pop("principal_id", None)
    approval.pop("authority_role", None)

    # When
    findings = schema_findings(
        RecordDocument(allowance.path, changed),
        schema_validators(ROOT / "contracts" / "intent-compliance"),
    )

    # Then
    assert "schema" in {finding.code for finding in findings}


def test_submission_when_candidate_omits_newer_trusted_registry_then_rejected(
    tmp_path: Path,
) -> None:
    # Given
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "intent@example.invalid")
    _git(tmp_path, "config", "user.name", "Intent Test")
    family = tmp_path / "contracts" / "intent-compliance" / "records"
    family.mkdir(parents=True)
    for source in sorted(POSITIVE.glob("*.yaml")):
        (family / source.name).write_bytes(source.read_bytes())
    _git(tmp_path, "add", "contracts/intent-compliance/records")
    _git(tmp_path, "commit", "-qm", "trusted authority family")
    snapshot = authority_validation.TrustedSnapshot(
        tmp_path,
        "example/domain-factory",
        _git(tmp_path, "rev-parse", "HEAD"),
    )
    submitted: list[RecordDocument] = []
    for record in _positive():
        if record.data.get("kind") != "compliance_decision":
            continue
        changed = copy.deepcopy(record.data)
        changed["evaluated_at"] = "2026-07-01T00:00:00Z"
        submitted.append(RecordDocument(record.path, changed))

    # When
    findings = authority_validation.validate_authoritative_submission(
        submitted, snapshot
    )

    # Then
    assert "current-registry" in {finding.code for finding in findings}
