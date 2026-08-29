from __future__ import annotations

import copy
import hashlib
import subprocess
from pathlib import Path

import pytest

from scripts.intent_compliance import authority_validation
from scripts.intent_compliance.authority_repository import TrustedSnapshotError
from scripts.intent_compliance.model import (
    InputLimitError,
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


def _positive_allowance() -> RecordDocument:
    records = load_record_documents(sorted(POSITIVE.glob("*.yaml")))
    return next(record for record in records if record.data.get("kind") == "policy_allowance")


def _allowance_with_source(repository: Path, revision: str) -> RecordDocument:
    allowance = _positive_allowance()
    changed = copy.deepcopy(allowance.data)
    source_path = repository / "governance.yaml"
    source = {
        "repository": "example/domain-factory",
        "path": "governance.yaml",
        "revision": revision,
        "content_digest": "sha256:" + hashlib.sha256(source_path.read_bytes()).hexdigest(),
    }
    issuer = changed["issuer"]
    approval = changed["policy_approval"]
    assert isinstance(issuer, dict) and isinstance(approval, dict)
    issuer["authority_source"] = source
    approval["authority_source"] = source
    return RecordDocument(allowance.path, changed)


def test_authority_source_when_revision_and_repository_match_snapshot_then_it_is_trusted(
    tmp_path: Path,
) -> None:
    # Given
    _initialize_repository(tmp_path)
    (tmp_path / "governance.yaml").write_text("trusted source\n")
    _git(tmp_path, "add", "governance.yaml")
    _git(tmp_path, "commit", "-qm", "trusted source")
    source_revision = _git(tmp_path, "rev-parse", "HEAD")
    (tmp_path / "snapshot.txt").write_text("trusted snapshot\n")
    _git(tmp_path, "add", "snapshot.txt")
    _git(tmp_path, "commit", "-qm", "trusted snapshot")
    trusted_commit = _git(tmp_path, "rev-parse", "HEAD")
    snapshot = authority_validation.TrustedSnapshot(
        tmp_path, "example/domain-factory", trusted_commit
    )

    # When
    findings = authority_validation.verify_authoritative_sources(
        [_allowance_with_source(tmp_path, source_revision)], snapshot
    )

    # Then
    assert findings == []


def test_authority_source_when_revision_is_not_snapshot_ancestor_then_it_is_rejected(
    tmp_path: Path,
) -> None:
    # Given
    _initialize_repository(tmp_path)
    (tmp_path / "snapshot.txt").write_text("trusted snapshot\n")
    _git(tmp_path, "add", "snapshot.txt")
    _git(tmp_path, "commit", "-qm", "trusted snapshot")
    trusted_commit = _git(tmp_path, "rev-parse", "HEAD")
    (tmp_path / "governance.yaml").write_text("local-only source\n")
    _git(tmp_path, "add", "governance.yaml")
    _git(tmp_path, "commit", "-qm", "local-only source")
    local_only_revision = _git(tmp_path, "rev-parse", "HEAD")
    snapshot = authority_validation.TrustedSnapshot(
        tmp_path, "example/domain-factory", trusted_commit
    )

    # When
    findings = authority_validation.verify_authoritative_sources(
        [_allowance_with_source(tmp_path, local_only_revision)], snapshot
    )

    # Then
    assert "authority-source-ancestry" in {finding.code for finding in findings}


def test_authority_source_when_repository_id_differs_then_it_is_rejected(
    tmp_path: Path,
) -> None:
    _initialize_repository(tmp_path)
    (tmp_path / "governance.yaml").write_text("trusted source\n")
    _git(tmp_path, "add", "governance.yaml")
    _git(tmp_path, "commit", "-qm", "trusted source")
    trusted_commit = _git(tmp_path, "rev-parse", "HEAD")
    snapshot = authority_validation.TrustedSnapshot(
        tmp_path, "trusted/domain-factory", trusted_commit
    )

    findings = authority_validation.verify_authoritative_sources(
        [_allowance_with_source(tmp_path, trusted_commit)], snapshot
    )

    assert "authority-repository" in {finding.code for finding in findings}


def test_authority_source_when_git_entry_is_symlink_then_it_is_rejected(
    tmp_path: Path,
) -> None:
    _initialize_repository(tmp_path)
    (tmp_path / "target.txt").write_text("trusted source\n")
    (tmp_path / "governance.yaml").symlink_to("target.txt")
    _git(tmp_path, "add", "target.txt", "governance.yaml")
    _git(tmp_path, "commit", "-qm", "symlink source")
    trusted_commit = _git(tmp_path, "rev-parse", "HEAD")
    snapshot = authority_validation.TrustedSnapshot(
        tmp_path, "example/domain-factory", trusted_commit
    )

    with pytest.raises(TrustedSnapshotError, match="cannot resolve"):
        authority_validation.verify_authoritative_sources(
            [_allowance_with_source(tmp_path, trusted_commit)], snapshot
        )


def test_trusted_snapshot_when_git_environment_redirects_repository_then_ignores_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Given
    trusted = tmp_path / "trusted"
    trusted.mkdir()
    _initialize_repository(trusted)
    (trusted / "snapshot.txt").write_text("trusted snapshot\n")
    _git(trusted, "add", "snapshot.txt")
    _git(trusted, "commit", "-qm", "trusted snapshot")
    trusted_commit = _git(trusted, "rev-parse", "HEAD")
    redirected = tmp_path / "redirected"
    redirected.mkdir()
    _initialize_repository(redirected)
    monkeypatch.setenv("GIT_DIR", str(redirected / ".git"))

    # When
    snapshot = authority_validation.TrustedSnapshot(
        trusted, "example/domain-factory", trusted_commit
    )

    # Then
    assert snapshot.commit == trusted_commit


def test_trusted_snapshot_when_family_exceeds_aggregate_budget_then_rejected(
    tmp_path: Path,
) -> None:
    # Given
    _initialize_repository(tmp_path)
    family = tmp_path / "contracts" / "intent-compliance"
    family.mkdir(parents=True)
    for index in range(5):
        (family / f"authority-{index}.yaml").write_text(
            "kind: policy_allowance_registry\npadding: " + "x" * 900_000
        )
    _git(tmp_path, "add", "contracts/intent-compliance")
    _git(tmp_path, "commit", "-qm", "oversized family")
    trusted_commit = _git(tmp_path, "rev-parse", "HEAD")
    snapshot = authority_validation.TrustedSnapshot(
        tmp_path, "example/domain-factory", trusted_commit
    )

    # When
    with pytest.raises(InputLimitError, match="aggregate input exceeds"):
        authority_validation.load_authoritative_documents(snapshot)


def test_trusted_snapshot_when_family_entry_is_symlink_then_rejected(
    tmp_path: Path,
) -> None:
    _initialize_repository(tmp_path)
    family = tmp_path / "contracts" / "intent-compliance"
    family.mkdir(parents=True)
    (family / "target.txt").write_text("kind: policy_allowance_registry\n")
    (family / "authority.yaml").symlink_to("target.txt")
    _git(tmp_path, "add", "contracts/intent-compliance")
    _git(tmp_path, "commit", "-qm", "symlink family")
    trusted_commit = _git(tmp_path, "rev-parse", "HEAD")
    snapshot = authority_validation.TrustedSnapshot(
        tmp_path, "example/domain-factory", trusted_commit
    )

    with pytest.raises(TrustedSnapshotError, match="cannot resolve family blob"):
        authority_validation.load_authoritative_documents(snapshot)
