from __future__ import annotations

import copy
import hashlib
import subprocess
from pathlib import Path

import pytest
import yaml

from scripts.intent_compliance import authority_validation
from scripts.intent_compliance.model import (
    Record,
    RecordDocument,
    load_record_documents,
)

ROOT = Path(__file__).resolve().parents[2]
POSITIVE = ROOT / "contracts" / "intent-compliance" / "examples" / "positive"


def _git(repository: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _initialize_repository(repository: Path) -> None:
    _git(repository, "init", "-q")
    _git(repository, "config", "user.email", "intent@example.invalid")
    _git(repository, "config", "user.name", "Intent Test")


def _positive(kind: str) -> RecordDocument:
    records = load_record_documents(sorted(POSITIVE.glob("*.yaml")))
    return next(record for record in records if record.data.get("kind") == kind)


def _commit_authority_source(repository: Path, authorizations: list[Record]) -> str:
    source = repository / "governance.yaml"
    source.write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "kind": "intent_compliance_authority",
                "authorizations": authorizations,
            },
            sort_keys=False,
        )
    )
    _git(repository, "add", "governance.yaml")
    _git(repository, "commit", "-qm", "authority source")
    return _git(repository, "rev-parse", "HEAD")


def _source_reference(repository: Path, revision: str) -> dict[str, str]:
    return {
        "repository": "example/domain-factory",
        "path": "governance.yaml",
        "revision": revision,
        "content_digest": "sha256:"
        + hashlib.sha256((repository / "governance.yaml").read_bytes()).hexdigest(),
    }


def _authority_records() -> list[Record]:
    return [
        {
            "principal_id": "neutral.issuer.1",
            "authority_role": "neutral.allowance_issuer",
            "approval_ids": [],
        },
        {
            "principal_id": "neutral.revoker.1",
            "authority_role": "neutral.allowance_revoker",
            "approval_ids": [],
        },
        {
            "principal_id": "neutral.approver.1",
            "authority_role": "neutral.policy_approver",
            "approval_ids": ["neutral.policy_approval.1"],
        },
    ]


def _allowance(repository: Path, revision: str) -> RecordDocument:
    allowance = _positive("policy_allowance")
    changed = copy.deepcopy(allowance.data)
    source = _source_reference(repository, revision)
    issuer = changed["issuer"]
    approval = changed["policy_approval"]
    assert isinstance(issuer, dict) and isinstance(approval, dict)
    issuer["authority_source"] = source
    approval["principal_id"] = "neutral.approver.1"
    approval["authority_role"] = "neutral.policy_approver"
    approval["authority_source"] = source
    return RecordDocument(allowance.path, changed)


def _revocation(repository: Path, revision: str) -> RecordDocument:
    revocation = _positive("policy_allowance_revocation")
    changed = copy.deepcopy(revocation.data)
    revoker = changed["revoker"]
    assert isinstance(revoker, dict)
    revoker["authority_source"] = _source_reference(repository, revision)
    return RecordDocument(revocation.path, changed)


@pytest.fixture
def authority_context(
    tmp_path: Path,
) -> tuple[Path, str, authority_validation.TrustedSnapshot]:
    _initialize_repository(tmp_path)
    revision = _commit_authority_source(tmp_path, _authority_records())
    snapshot = authority_validation.TrustedSnapshot(
        tmp_path, "example/domain-factory", revision
    )
    return tmp_path, revision, snapshot


def test_authority_source_when_issuer_tuple_is_not_authorized_then_rejected(
    authority_context: tuple[Path, str, authority_validation.TrustedSnapshot],
) -> None:
    # Given
    repository, revision, snapshot = authority_context
    allowance = _allowance(repository, revision)
    issuer = allowance.data["issuer"]
    assert isinstance(issuer, dict)
    issuer["principal_id"] = "neutral.unauthorized_issuer"

    # When
    findings = authority_validation.verify_authoritative_sources([allowance], snapshot)

    # Then
    assert "authority-attribution" in {finding.code for finding in findings}


def test_authority_source_when_revoker_tuple_is_not_authorized_then_rejected(
    authority_context: tuple[Path, str, authority_validation.TrustedSnapshot],
) -> None:
    # Given
    repository, revision, snapshot = authority_context
    revocation = _revocation(repository, revision)
    revoker = revocation.data["revoker"]
    assert isinstance(revoker, dict)
    revoker["principal_id"] = "neutral.unauthorized_revoker"

    # When
    findings = authority_validation.verify_authoritative_sources([revocation], snapshot)

    # Then
    assert "authority-attribution" in {finding.code for finding in findings}


def test_authority_source_when_trusted_blob_is_not_authority_document_then_rejected(
    tmp_path: Path,
) -> None:
    # Given
    _initialize_repository(tmp_path)
    (tmp_path / "governance.yaml").write_text("trusted but arbitrary\n")
    _git(tmp_path, "add", "governance.yaml")
    _git(tmp_path, "commit", "-qm", "arbitrary trusted blob")
    revision = _git(tmp_path, "rev-parse", "HEAD")
    snapshot = authority_validation.TrustedSnapshot(
        tmp_path, "example/domain-factory", revision
    )

    # When
    findings = authority_validation.verify_authoritative_sources(
        [_allowance(tmp_path, revision)], snapshot
    )

    # Then
    assert "authority-source-content" in {finding.code for finding in findings}


@pytest.mark.parametrize(
    ("field", "substitution"),
    [
        ("principal_id", "neutral.substituted_approver"),
        ("authority_role", "neutral.substituted_policy_role"),
        ("approval_id", "neutral.substituted_policy_approval"),
    ],
)
def test_authority_source_when_approval_binding_is_substituted_then_rejected(
    authority_context: tuple[Path, str, authority_validation.TrustedSnapshot],
    field: str,
    substitution: str,
) -> None:
    # Given
    repository, revision, snapshot = authority_context
    allowance = _allowance(repository, revision)
    approval = allowance.data["policy_approval"]
    assert isinstance(approval, dict)
    approval[field] = substitution

    # When
    findings = authority_validation.verify_authoritative_sources([allowance], snapshot)

    # Then
    assert "authority-attribution" in {finding.code for finding in findings}


def test_authority_source_when_authorization_count_exceeds_bound_then_rejected(
    tmp_path: Path,
) -> None:
    # Given
    _initialize_repository(tmp_path)
    authorizations: list[Record] = [
        {
            "principal_id": f"neutral.issuer.{index}",
            "authority_role": "neutral.allowance_issuer",
            "approval_ids": [],
        }
        for index in range(65)
    ]
    revision = _commit_authority_source(tmp_path, authorizations)
    snapshot = authority_validation.TrustedSnapshot(
        tmp_path, "example/domain-factory", revision
    )

    # When
    findings = authority_validation.verify_authoritative_sources(
        [_allowance(tmp_path, revision)], snapshot
    )

    # Then
    assert "authority-source-content" in {finding.code for finding in findings}
