from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from scripts.intent_compliance.schema_validation import (
    schema_findings,
    schema_validators,
)
from scripts.intent_compliance.validator import (
    RecordDocument,
    load_record_documents,
    validate_documents,
)

ROOT = Path(__file__).resolve().parents[2]
FAMILY = ROOT / "contracts" / "intent-compliance"
POSITIVE = FAMILY / "examples" / "positive"
VALIDATOR = ROOT / "scripts" / "validate-intent-compliance.py"


def _trusted_snapshot(repository: Path) -> tuple[Path, str]:
    subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
    subprocess.run(
        ["git", "config", "user.email", "intent@example.invalid"],
        cwd=repository,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Intent Test"],
        cwd=repository,
        check=True,
    )
    (repository / "snapshot.txt").write_text("trusted\n", encoding="utf-8")
    subprocess.run(["git", "add", "snapshot.txt"], cwd=repository, check=True)
    subprocess.run(
        ["git", "commit", "-qm", "trusted snapshot"], cwd=repository, check=True
    )
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return repository, completed.stdout.strip()


def test_positive_corpus_when_valid_then_has_no_findings() -> None:
    records = load_record_documents(sorted(POSITIVE.glob("*.yaml")))

    findings = validate_documents(records)

    assert findings == []


def test_templates_when_loaded_then_each_satisfies_its_schema() -> None:
    validators = schema_validators(FAMILY)
    templates = load_record_documents(sorted(FAMILY.glob("*.template.yaml")))

    findings = [
        finding
        for template in templates
        for finding in schema_findings(template, validators)
    ]

    assert findings == []


def test_allowance_id_when_repointed_in_later_revision_then_fails() -> None:
    records = load_record_documents(sorted(POSITIVE.glob("*.yaml")))
    registry = next(record for record in records if record.data.get("kind") == "policy_allowance_registry")
    later = RecordDocument(
        path=registry.path,
        data={
            **registry.data,
            "revision_id": "neutral.revision.2",
            "revision_digest": "sha256:" + "f" * 64,
            "predecessor_revision_digest": registry.data["revision_digest"],
            "allowances": [{
            "allowance_id": "neutral.allowance.1",
            "approval_digest": "sha256:" + "0" * 64,
            "revocation_digests": [],
            }],
        },
    )

    findings = validate_documents([*records, later])

    assert "allowance-id-reused" in {finding.code for finding in findings}


def test_public_cli_when_self_test_runs_then_exits_zero() -> None:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "intent-compliance validation ok" in completed.stdout


def test_public_cli_when_strict_consumer_has_no_records_then_exits_one(tmp_path: Path) -> None:
    trusted_repository = tmp_path / "trusted"
    trusted_repository.mkdir()
    repository, commit = _trusted_snapshot(trusted_repository)
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    completed = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--strict",
            "--trusted-repository",
            str(repository),
            "--trusted-repository-id",
            "example/domain-factory",
            "--trusted-commit",
            commit,
            str(candidate),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 1
    assert "no governed intent-compliance records found" in completed.stderr


def test_public_cli_when_kind_is_quoted_then_record_is_not_silently_skipped(
    tmp_path: Path,
) -> None:
    trusted_repository = tmp_path / "trusted"
    trusted_repository.mkdir()
    repository, commit = _trusted_snapshot(trusted_repository)
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "record.yaml").write_text(
        'schema_version: 1\nkind: "compliance_decision"\n', encoding="utf-8"
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--strict",
            "--trusted-repository",
            str(repository),
            "--trusted-repository-id",
            "example/domain-factory",
            "--trusted-commit",
            commit,
            str(candidate),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 1
    assert "no governed intent-compliance records found" not in completed.stderr
    assert "schema" in completed.stderr


@pytest.mark.parametrize(
    "content",
    ["kind: compliance_decision\nbad: [", "{kind: compliance_decision, bad: [}"],
)
def test_public_cli_when_consumer_yaml_is_invalid_then_exits_two(
    tmp_path: Path, content: str
) -> None:
    trusted_repository = tmp_path / "trusted"
    trusted_repository.mkdir()
    repository, commit = _trusted_snapshot(trusted_repository)
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    _ = (candidate / "broken.yaml").write_text(content, encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--trusted-repository",
            str(repository),
            "--trusted-repository-id",
            "example/domain-factory",
            "--trusted-commit",
            commit,
            str(candidate),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 2
    assert "validator harness error" in completed.stderr


@pytest.mark.parametrize(
    "content",
    [
        "kind_value: &kind_value compliance_decision\nkind: *kind_value\n",
        "base: &base\n  kind: compliance_decision\n<<: *base\n",
    ],
)
def test_public_cli_when_governed_kind_uses_alias_then_exits_two(
    tmp_path: Path, content: str
) -> None:
    trusted_repository = tmp_path / "trusted"
    trusted_repository.mkdir()
    repository, commit = _trusted_snapshot(trusted_repository)
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "valid.yaml").write_text(
        "kind: compliance_decision\n", encoding="utf-8"
    )
    (candidate / "aliased.yaml").write_text(content, encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--strict",
            "--trusted-repository",
            str(repository),
            "--trusted-repository-id",
            "example/domain-factory",
            "--trusted-commit",
            commit,
            str(candidate),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 2
    assert "YAML aliases are forbidden" in completed.stderr


@pytest.mark.parametrize("target_kind", ["file", "directory", "parent"])
def test_public_cli_when_target_path_contains_symlink_then_exits_two(
    tmp_path: Path, target_kind: str
) -> None:
    trusted_repository = tmp_path / "trusted"
    trusted_repository.mkdir()
    repository, commit = _trusted_snapshot(trusted_repository)
    real_parent = tmp_path / "real-parent"
    real_parent.mkdir()
    candidate = real_parent / "candidate"
    candidate.mkdir()
    record = candidate / "record.yaml"
    record.write_text("kind: compliance_decision\n", encoding="utf-8")
    if target_kind == "file":
        target = tmp_path / "target.yaml"
        target.symlink_to(record)
    elif target_kind == "directory":
        target = tmp_path / "target"
        target.symlink_to(candidate, target_is_directory=True)
    else:
        linked_parent = tmp_path / "linked-parent"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        target = linked_parent / "candidate"

    completed = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--strict",
            "--trusted-repository",
            str(repository),
            "--trusted-repository-id",
            "example/domain-factory",
            "--trusted-commit",
            commit,
            str(target),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 2
    assert "validator harness error" in completed.stderr


def test_public_cli_when_target_has_no_trusted_snapshot_then_exits_two(
    tmp_path: Path,
) -> None:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 2
    assert "trusted repository, repository ID, and commit" in completed.stderr


def test_public_cli_when_target_does_not_exist_then_exits_two(tmp_path: Path) -> None:
    # Given
    missing = tmp_path / "missing"

    # When
    completed = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--trusted-repository",
            str(tmp_path),
            "--trusted-repository-id",
            "example/domain-factory",
            "--trusted-commit",
            "0" * 40,
            str(missing),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    # Then
    assert completed.returncode == 2
    assert "target does not exist" in completed.stderr
