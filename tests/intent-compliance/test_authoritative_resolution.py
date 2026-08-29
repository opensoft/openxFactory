from __future__ import annotations

import copy
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from scripts.intent_compliance import authority_validation
from scripts.intent_compliance.model import RecordDocument, load_record_documents
from scripts.intent_compliance.schema_validation import (
    schema_findings,
    schema_validators,
)
from scripts.intent_compliance.state_validation import canonical_digest
from scripts.intent_compliance.validator import validate_documents

ROOT = Path(__file__).resolve().parents[2]
FAMILY = ROOT / "contracts" / "intent-compliance"
POSITIVE = FAMILY / "examples" / "positive"
VALIDATOR = ROOT / "scripts" / "validate-intent-compliance.py"
SCHEMA_VALIDATORS = schema_validators(FAMILY)

INVALID_REPOSITORY_PATHS = (
    pytest.param("", id="empty"),
    pytest.param(".", id="dot-segment"),
    pytest.param("..", id="dot-dot-segment"),
    pytest.param("policies/", id="trailing-empty-segment"),
    pytest.param("policies/./standing-policy.md", id="nested-dot-segment"),
    pytest.param("policies/../standing-policy.md", id="nested-dot-dot-segment"),
    pytest.param("/policies/standing-policy.md", id="absolute"),
    pytest.param("policies//standing-policy.md", id="duplicate-separator"),
    pytest.param("policies:standing-policy.md", id="colon"),
    pytest.param(r"policies\standing-policy.md", id="backslash"),
    pytest.param("policies/standing\npolicy.md", id="line-feed-control"),
    pytest.param("policies/standing\x7fpolicy.md", id="delete-control"),
    pytest.param("policies/standing-policy\u00ff.md", id="unicode"),
)


def _positive() -> list[RecordDocument]:
    return load_record_documents(sorted(POSITIVE.glob("*.yaml")))


def _codes(records: list[RecordDocument]) -> set[str]:
    return {finding.code for finding in validate_documents(records)}


def _record_with_source_path(
    kind: str, path: str, *, ratification: bool
) -> RecordDocument:
    record = next(item for item in _positive() if item.data.get("kind") == kind)
    changed = copy.deepcopy(record.data)
    policy_source = changed["policy_source"]
    assert isinstance(policy_source, dict)
    source = policy_source["ratification_record"] if ratification else policy_source
    assert isinstance(source, dict)
    source["path"] = path
    return RecordDocument(record.path, changed)


def _git(repository: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


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
        RecordDocument(allowance.path, changed), SCHEMA_VALIDATORS
    )

    # Then
    assert "schema" in {finding.code for finding in findings}


@pytest.mark.parametrize("kind", ["veto_class_vocabulary", "compliance_decision"])
@pytest.mark.parametrize("ratification", [False, True], ids=["policy", "ratification"])
@pytest.mark.parametrize("path", INVALID_REPOSITORY_PATHS)
def test_policy_source_when_path_is_resolver_invalid_then_schema_rejects(
    kind: str, ratification: bool, path: str
) -> None:
    # Given
    document = _record_with_source_path(kind, path, ratification=ratification)

    # When
    findings = schema_findings(document, SCHEMA_VALIDATORS)

    # Then
    assert {finding.code for finding in findings} == {"schema"}


@pytest.mark.parametrize("kind", ["veto_class_vocabulary", "compliance_decision"])
@pytest.mark.parametrize("ratification", [False, True], ids=["policy", "ratification"])
@pytest.mark.parametrize(
    "path", ["standing-policy.md", "POLICIES/.standing/.../policy-2"]
)
def test_policy_source_when_path_is_resolver_valid_then_schema_accepts(
    kind: str, ratification: bool, path: str
) -> None:
    # Given
    document = _record_with_source_path(kind, path, ratification=ratification)

    # When
    findings = schema_findings(document, SCHEMA_VALIDATORS)

    # Then
    assert findings == []


@pytest.mark.parametrize("ratification", [False, True], ids=["policy", "ratification"])
def test_public_cli_when_source_path_is_schema_invalid_then_exits_one(
    tmp_path: Path, ratification: bool
) -> None:
    # Given
    repository = tmp_path / "trusted"
    repository.mkdir()
    _git(repository, "init", "-q")
    _git(repository, "config", "user.email", "intent@example.invalid")
    _git(repository, "config", "user.name", "Intent Test")
    policy = repository / "policies" / "standing-policy.md"
    policy.parent.mkdir()
    policy.write_text("standing policy\n")
    ratification_record = repository / "governance" / "ratification.md"
    ratification_record.parent.mkdir()
    ratification_record.write_text("ratified\n")
    _git(repository, "add", "policies", "governance")
    _git(repository, "commit", "-qm", "authority sources")
    source_commit = _git(repository, "rev-parse", "HEAD")
    family = repository / "contracts" / "intent-compliance" / "records"
    family.mkdir(parents=True)
    for source in sorted(POSITIVE.glob("*.yaml")):
        (family / source.name).write_bytes(source.read_bytes())
    vocabulary = _record_with_source_path(
        "veto_class_vocabulary",
        "policies:standing-policy.md",
        ratification=ratification,
    )
    policy_source = vocabulary.data["policy_source"]
    assert isinstance(policy_source, dict)
    policy_source["revision"] = source_commit
    policy_source["content_digest"] = _sha256(policy)
    ratification_source = policy_source["ratification_record"]
    assert isinstance(ratification_source, dict)
    ratification_source["content_digest"] = _sha256(ratification_record)
    (family / "vocabulary.example.yaml").write_text(
        yaml.safe_dump(vocabulary.data, sort_keys=False)
    )
    _git(repository, "add", "contracts/intent-compliance/records")
    _git(repository, "commit", "-qm", "trusted authority family")
    trusted_commit = _git(repository, "rev-parse", "HEAD")
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "decision.example.yaml").write_bytes(
        (POSITIVE / "decision.example.yaml").read_bytes()
    )

    # When
    command = [
        sys.executable,
        str(VALIDATOR),
        "--strict",
        "--trusted-repository",
        str(repository),
        "--trusted-repository-id",
        "example/domain-factory",
        "--trusted-commit",
        trusted_commit,
        str(candidate),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    # Then
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert (
        ": schema:" in completed.stderr
        and "validator harness error" not in completed.stderr
    )


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
