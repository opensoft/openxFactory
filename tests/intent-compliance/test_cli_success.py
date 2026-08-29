from __future__ import annotations

import copy
import hashlib
import subprocess
import sys
from pathlib import Path

import yaml

from scripts.intent_compliance.evidence_validation import decision_digest
from scripts.intent_compliance.model import Record
from scripts.intent_compliance.state_validation import canonical_digest

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate-intent-compliance.py"


def _git(repository: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _decision(base: Record, gate: str) -> Record:
    decision = copy.deepcopy(base)
    decision["decision_id"] = f"neutral.decision.{gate}"
    decision["enforcement_point"] = gate
    decision["evaluated_at"] = {
        "approval": "2026-02-01T00:00:00Z",
        "dispatch": "2026-02-01T00:00:01Z",
        "admission": "2026-02-01T00:00:02Z",
    }[gate]
    if gate == "dispatch":
        evidence: Record = {
            "decision_id": decision["decision_id"],
            "decision_digest": decision_digest(decision),
            "evaluated_content_digest": decision["evaluated_content_digest"],
            "registry_id": decision["registry"]["registry_id"],
            "conditioned_revision_digest": decision["registry"]["revision_digest"],
            "evaluator_id": decision["evaluator"]["evaluator_id"],
            "evaluator_version": decision["evaluator"]["version"],
            "expires_at": "2026-02-01T00:01:00Z",
            "evidence_digest": "sha256:" + "0" * 64,
        }
        evidence["evidence_digest"] = canonical_digest(evidence, "evidence_digest")
        decision["dispatch_authorization_evidence"] = evidence
    return decision


def test_public_cli_when_target_and_snapshot_are_valid_then_exits_zero(
    tmp_path: Path,
) -> None:
    # Given
    repository = tmp_path / "trusted"
    repository.mkdir()
    _git(repository, "init", "-q")
    _git(repository, "config", "user.email", "intent@example.invalid")
    _git(repository, "config", "user.name", "Intent Test")
    policy = repository / "policies" / "standing-policy.md"
    ratification = repository / "governance" / "ratification.md"
    policy.parent.mkdir()
    ratification.parent.mkdir()
    policy.write_text("standing policy\n")
    ratification.write_text("ratified\n")
    _git(repository, "add", "policies", "governance")
    _git(repository, "commit", "-qm", "authority sources")
    source_commit = _git(repository, "rev-parse", "HEAD")
    policy_source: Record = {
        "repository": "example/domain-factory",
        "path": "policies/standing-policy.md",
        "revision": source_commit,
        "content_digest": "sha256:" + hashlib.sha256(policy.read_bytes()).hexdigest(),
        "ratification_record": {
            "path": "governance/ratification.md",
            "content_digest": "sha256:"
            + hashlib.sha256(ratification.read_bytes()).hexdigest(),
        },
    }
    vocabulary: Record = {
        "schema_version": 1,
        "kind": "veto_class_vocabulary",
        "vocabulary_id": "neutral.policy.v1",
        "vocabulary_digest": "sha256:" + "0" * 64,
        "policy_source": policy_source,
        "classes": [
            {
                "class_id": "neutral.restricted_action",
                "owner_role": "neutral.policy_owner",
                "allowance_issuer_roles": ["neutral.allowance_issuer"],
                "allowance_revoker_roles": ["neutral.allowance_revoker"],
            }
        ],
    }
    vocabulary["vocabulary_digest"] = canonical_digest(
        vocabulary, "vocabulary_digest"
    )
    registry: Record = {
        "schema_version": 1,
        "kind": "policy_allowance_registry",
        "registry_id": "neutral.registry",
        "revision_id": "neutral.revision.1",
        "revision_digest": "sha256:" + "0" * 64,
        "predecessor_revision_digest": None,
        "published_at": "2026-01-01T00:00:00Z",
        "allowances": [],
    }
    registry["revision_digest"] = canonical_digest(registry, "revision_digest")
    family = repository / "contracts" / "intent-compliance"
    family.mkdir(parents=True)
    (family / "authority.yaml").write_text(
        yaml.safe_dump_all([vocabulary, registry], sort_keys=False)
    )
    _git(repository, "add", "contracts/intent-compliance")
    _git(repository, "commit", "-qm", "authority family")
    trusted_commit = _git(repository, "rev-parse", "HEAD")
    deterministic: Record = {
        "evaluated_content_digest": "sha256:" + "b" * 64,
        "vocabulary_id": vocabulary["vocabulary_id"],
        "vocabulary_digest": vocabulary["vocabulary_digest"],
        "registry_id": registry["registry_id"],
        "revision_digest": registry["revision_digest"],
        "evaluator_id": "neutral.evaluator",
        "evaluator_version": "1.0.0",
        "finding_digests": [],
        "evidence_codes": ["neutral.deterministic_scan_complete"],
        "ambiguity_refs": [],
        "evidence_digest": "sha256:" + "0" * 64,
    }
    deterministic["evidence_digest"] = canonical_digest(
        deterministic, "evidence_digest"
    )
    base: Record = {
        "schema_version": 1,
        "kind": "compliance_decision",
        "decision_id": "neutral.decision.placeholder",
        "governed_binding_id": "neutral.binding.1",
        "enforcement_point": "approval",
        "outcome": "allow",
        "evaluated_content_digest": "sha256:" + "b" * 64,
        "policy_source": policy_source,
        "vocabulary": {
            "vocabulary_id": vocabulary["vocabulary_id"],
            "vocabulary_digest": vocabulary["vocabulary_digest"],
        },
        "registry": {
            "registry_id": registry["registry_id"],
            "revision_id": registry["revision_id"],
            "revision_digest": registry["revision_digest"],
        },
        "allowance_references": [],
        "resolutions": [],
        "findings": [],
        "rationale_codes": ["neutral.no_restricted_action"],
        "redacted_detail_codes": [],
        "correlation_refs": [],
        "evaluator": {"evaluator_id": "neutral.evaluator", "version": "1.0.0"},
        "deterministic_evidence": deterministic,
        "evaluated_at": "2026-02-01T00:00:00Z",
    }
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "decisions.yaml").write_text(
        yaml.safe_dump_all(
            [_decision(base, gate) for gate in ("approval", "dispatch", "admission")],
            sort_keys=False,
        )
    )

    # When
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
            trusted_commit,
            str(candidate),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    # Then
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "intent-compliance validation ok" in completed.stdout
