"""RED contracts for the Gate G0 consumer handoff receipt (T069, T075)."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from scripts.hermes_runtime_validation.consumer_handoff import (
    CONSUMER_REPOSITORY,
    ConsumerHandoffDependencyError,
    build_consumer_resolver,
    validate_handoff_receipt,
)
from scripts.hermes_runtime_validation.loader import load_yaml_document
from tests.hermes_runtime_contracts.support import commit_files, init_git_repo

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
FAMILY_ROOT = REPOSITORY_ROOT / "contracts/hermes-runtime"
FIXTURE_ROOT = FAMILY_ROOT / "fixtures"
SCHEMA_PATH = FAMILY_ROOT / "consumer-handoff-receipt.schema.yaml"
SHARED_DEFINITIONS_PATH = FAMILY_ROOT / "shared-definitions.schema.yaml"

RECEIPT_KIND = "openxfactory-hermes-runtime-consumer-handoff-receipt"
PLACEHOLDER_COMMIT = "1" * 40

FIXTURE_FILES: dict[str, str] = {
    "handoff-consumer-receipt-wrong-repository": (
        "pins/consumer-receipt-wrong-repository.yaml"
    ),
    "handoff-receipt-valid": "pins/handoff-receipt-valid.yaml",
    "handoff-receipt-older-pin": "pins/handoff-receipt-older-pin.yaml",
    "handoff-receipt-tag-drift": "pins/handoff-receipt-tag-drift.yaml",
    "handoff-receipt-commit-drift": "pins/handoff-receipt-commit-drift.yaml",
    "handoff-receipt-packet-path-drift": (
        "pins/handoff-receipt-packet-path-drift.yaml"
    ),
    "handoff-receipt-packet-digest-drift": (
        "pins/handoff-receipt-packet-digest-drift.yaml"
    ),
    "handoff-receipt-manifest-digest-drift": (
        "pins/handoff-receipt-manifest-digest-drift.yaml"
    ),
    "handoff-receipt-drift-check-passed": (
        "pins/handoff-receipt-drift-check-passed.yaml"
    ),
}

# Receipts that must satisfy the closed structural schema; the remaining
# negatives are semantic-only (field agreement and digest parity need the
# exact landed Git objects, which structure alone cannot see).
SCHEMA_VALID_CASES = frozenset(
    {
        "handoff-receipt-valid",
        "handoff-receipt-older-pin",
        "handoff-receipt-tag-drift",
        "handoff-receipt-packet-digest-drift",
        "handoff-receipt-manifest-digest-drift",
    }
)

EXPECTED_PRIMARY_CODES: dict[str, str | None] = {
    "handoff-consumer-receipt-wrong-repository": "HGR-HANDOFF-CONSUMER-REPOSITORY",
    "handoff-receipt-valid": None,
    "handoff-receipt-older-pin": None,
    "handoff-receipt-tag-drift": "HGR-HANDOFF-TAG",
    "handoff-receipt-commit-drift": "HGR-HANDOFF-COMMIT",
    "handoff-receipt-packet-path-drift": "HGR-HANDOFF-PACKET-PATH",
    "handoff-receipt-packet-digest-drift": "HGR-HANDOFF-PACKET-DIGEST",
    "handoff-receipt-manifest-digest-drift": "HGR-HANDOFF-ARTIFACT-DIGEST",
    "handoff-receipt-drift-check-passed": "HGR-HANDOFF-CHECK-RESULTS",
}


def _digest(body: bytes) -> str:
    return f"sha256:{hashlib.sha256(body).hexdigest()}"


def _codes(findings: list[dict[str, str]]) -> list[str]:
    return [finding["code"] for finding in findings]


def _fixture(case_id: str) -> dict[str, Any]:
    document = load_yaml_document(FIXTURE_ROOT / FIXTURE_FILES[case_id])
    assert isinstance(document, dict)
    return document


def _receipt(fixture: Mapping[str, Any], commit: str | None = None) -> dict[str, Any]:
    receipt = deepcopy(fixture["input"]["value"])
    if commit is not None and receipt.get("consumer_commit") == PLACEHOLDER_COMMIT:
        receipt["consumer_commit"] = commit
    return receipt


def _build_consumer_repo(
    tmp_path: Path, fixture: Mapping[str, Any]
) -> tuple[Path, str]:
    repo = init_git_repo(tmp_path / "consumer")
    files = {
        entry["path"]: entry["content_utf8"] for entry in fixture["git_tree"]["entries"]
    }
    commit = commit_files(repo, files, message="landed Gate G0 closure packet")
    return repo, commit


class _RecordingResolver:
    """Repository resolver double that records every invocation."""

    def __init__(self, target: Path | None = None) -> None:
        self.calls: list[str] = []
        self._target = target

    def __call__(self, repository: str) -> Path:
        self.calls.append(repository)
        if self._target is None:
            raise ConsumerHandoffDependencyError(
                "recording resolver has no repository to offer"
            )
        return self._target


def _receipt_validator() -> Draft202012Validator:
    schema = load_yaml_document(SCHEMA_PATH)
    shared = load_yaml_document(SHARED_DEFINITIONS_PATH)
    registry: Registry = Registry().with_resources(
        [
            (
                schema["$id"],
                Resource.from_contents(schema, default_specification=DRAFT202012),
            ),
            (
                shared["$id"],
                Resource.from_contents(shared, default_specification=DRAFT202012),
            ),
        ]
    )
    return Draft202012Validator(
        schema, registry=registry, format_checker=FormatChecker()
    )


def test_schema_annotations_are_canonical() -> None:
    schema = load_yaml_document(SCHEMA_PATH)
    assert schema["schema_version"] == 1
    assert schema["kind"] == "openxfactory-hermes-runtime-contract-schema"
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["$id"] == (
        "https://xforge.us/schemas/openxfactory/hermes-runtime/v2/"
        "consumer-handoff-receipt.schema.yaml"
    )
    assert schema["contract_id"] == "consumer-handoff-receipt"
    assert schema["contract_schema_version"] == 1
    Draft202012Validator.check_schema(schema)

    assert schema["properties"]["schema_version"] == {"const": 1}
    assert schema["properties"]["kind"] == {"const": RECEIPT_KIND}
    assert schema["properties"]["consumer_repository"] == {
        "const": "opensoft/xFactory-Hermes-Install"
    }
    assert schema["properties"]["provider"]["properties"]["repository"] == {
        "const": "opensoft/openxFactory"
    }
    packet_path = schema["properties"]["closure_packet"]["properties"]["path"]
    assert packet_path["pattern"].startswith("^evidence/gates/g0/")

    def assert_closed(node: object, location: str) -> None:
        if isinstance(node, dict):
            if node.get("type") == "object":
                assert (
                    node.get("additionalProperties") is False
                ), f"{location} is not closed"
            for key, value in node.items():
                assert_closed(value, f"{location}/{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                assert_closed(value, f"{location}/{index}")

    assert_closed(schema, "$")


@pytest.mark.parametrize("case_id", sorted(FIXTURE_FILES))
def test_schema_accepts_and_rejects_indexed_fixture_receipts(case_id: str) -> None:
    validator = _receipt_validator()
    receipt = _receipt(_fixture(case_id))

    assert validator.is_valid(receipt) is (case_id in SCHEMA_VALID_CASES)


@pytest.mark.parametrize(
    "mutation",
    ["extra_property", "missing_negative_results", "empty_positive_results"],
)
def test_schema_rejects_open_or_incomplete_check_surfaces(mutation: str) -> None:
    validator = _receipt_validator()
    receipt = _receipt(_fixture("handoff-receipt-valid"))
    if mutation == "extra_property":
        receipt["working_tree_digest"] = _digest(b"spoof\n")
    elif mutation == "missing_negative_results":
        del receipt["check_results"]["negative"]
    else:
        receipt["check_results"]["positive"] = []

    assert not validator.is_valid(receipt)


def test_wrong_product_receipt_fails_before_any_object_lookup() -> None:
    fixture = _fixture("handoff-consumer-receipt-wrong-repository")
    receipt = _receipt(fixture)
    assert receipt["consumer_repository"] == "FarHeap/Hermes-Install"
    resolver = _RecordingResolver()

    findings = validate_handoff_receipt(receipt, consumer_resolver=resolver)

    assert _codes(findings) == ["HGR-HANDOFF-CONSUMER-REPOSITORY"]
    assert resolver.calls == []


def test_wrong_product_precedes_every_other_receipt_defect() -> None:
    receipt = _receipt(_fixture("handoff-consumer-receipt-wrong-repository"))
    receipt["consumer_commit"] = "main"
    receipt["provider"]["tag"] = "contract-v9.9"
    receipt["closure_packet"]["path"] = "evidence/gates/g1/contract-v1.7.yaml"
    resolver = _RecordingResolver()

    findings = validate_handoff_receipt(receipt, consumer_resolver=resolver)

    assert _codes(findings) == ["HGR-HANDOFF-CONSUMER-REPOSITORY"]
    assert resolver.calls == []


def test_canonical_consumer_receipt_accepted_end_to_end(tmp_path: Path) -> None:
    fixture = _fixture("handoff-receipt-valid")
    repo, commit = _build_consumer_repo(tmp_path, fixture)
    receipt = _receipt(fixture, commit)
    resolver = build_consumer_resolver({CONSUMER_REPOSITORY: repo}, None)

    assert validate_handoff_receipt(receipt, consumer_resolver=resolver) == []


def test_older_bundle_pin_remains_conformant(tmp_path: Path) -> None:
    fixture = _fixture("handoff-receipt-older-pin")
    repo, commit = _build_consumer_repo(tmp_path, fixture)
    receipt = _receipt(fixture, commit)
    assert receipt["bundle_tag"] == "contract-v1.6"
    resolver = build_consumer_resolver({CONSUMER_REPOSITORY: repo}, None)

    assert validate_handoff_receipt(receipt, consumer_resolver=resolver) == []


def test_recorded_digests_match_an_independent_hashlib_oracle(
    tmp_path: Path,
) -> None:
    fixture = _fixture("handoff-receipt-valid")
    receipt = _receipt(fixture)
    bytes_by_path = {
        entry["path"]: entry["content_utf8"].encode("utf-8")
        for entry in fixture["git_tree"]["entries"]
    }

    recorded = {
        receipt["closure_packet"]["path"]: receipt["closure_packet"]["digest"],
        receipt["compatibility_manifest"]["path"]: receipt["compatibility_manifest"][
            "digest"
        ],
        receipt["checker"]["path"]: receipt["checker"]["digest"],
        receipt["runtime_binding"]["path"]: receipt["runtime_binding"]["digest"],
        receipt["evidence"]["path"]: receipt["evidence"]["digest"],
    }
    for result in (
        receipt["check_results"]["positive"] + receipt["check_results"]["negative"]
    ):
        recorded[result["evidence_path"]] = result["evidence_digest"]

    for path, recorded_digest in recorded.items():
        assert recorded_digest == _digest(bytes_by_path[path])

    repo, commit = _build_consumer_repo(tmp_path, fixture)
    resolver = build_consumer_resolver({CONSUMER_REPOSITORY: repo}, None)
    assert (
        validate_handoff_receipt(_receipt(fixture, commit), consumer_resolver=resolver)
        == []
    )


@pytest.mark.parametrize(
    ("artifact", "expected_code"),
    [
        ("closure_packet", "HGR-HANDOFF-PACKET-DIGEST"),
        ("compatibility_manifest", "HGR-HANDOFF-ARTIFACT-DIGEST"),
        ("checker", "HGR-HANDOFF-ARTIFACT-DIGEST"),
        ("runtime_binding", "HGR-HANDOFF-ARTIFACT-DIGEST"),
        ("evidence", "HGR-HANDOFF-ARTIFACT-DIGEST"),
        ("positive_check_evidence", "HGR-HANDOFF-ARTIFACT-DIGEST"),
    ],
)
def test_recorded_artifact_digest_drift_is_rejected(
    tmp_path: Path, artifact: str, expected_code: str
) -> None:
    fixture = _fixture("handoff-receipt-valid")
    repo, commit = _build_consumer_repo(tmp_path, fixture)
    receipt = _receipt(fixture, commit)
    drifted = _digest(b"deliberately drifted bytes\n")
    if artifact == "positive_check_evidence":
        receipt["check_results"]["positive"][0]["evidence_digest"] = drifted
    else:
        receipt[artifact]["digest"] = drifted
    resolver = build_consumer_resolver({CONSUMER_REPOSITORY: repo}, None)

    findings = validate_handoff_receipt(receipt, consumer_resolver=resolver)

    assert _codes(findings) == [expected_code]


@pytest.mark.parametrize("case_id", sorted(FIXTURE_FILES))
def test_semantic_matrix_over_indexed_fixtures(tmp_path: Path, case_id: str) -> None:
    fixture = _fixture(case_id)
    repo, commit = _build_consumer_repo(tmp_path, fixture)
    receipt = _receipt(fixture, commit)
    resolver = build_consumer_resolver({CONSUMER_REPOSITORY: repo}, None)

    findings = validate_handoff_receipt(receipt, consumer_resolver=resolver)

    expected_primary = EXPECTED_PRIMARY_CODES[case_id]
    if expected_primary is None:
        assert findings == []
    else:
        assert _codes(findings) == [expected_primary]


@pytest.mark.parametrize(
    ("case_id", "expected_code"),
    [
        ("handoff-receipt-tag-drift", "HGR-HANDOFF-TAG"),
        ("handoff-receipt-commit-drift", "HGR-HANDOFF-COMMIT"),
        ("handoff-receipt-packet-path-drift", "HGR-HANDOFF-PACKET-PATH"),
    ],
)
def test_internal_consistency_defects_fail_before_object_lookup(
    case_id: str, expected_code: str
) -> None:
    receipt = _receipt(_fixture(case_id))
    resolver = _RecordingResolver()

    findings = validate_handoff_receipt(receipt, consumer_resolver=resolver)

    assert _codes(findings) == [expected_code]
    assert resolver.calls == []


@pytest.mark.parametrize(
    "drop",
    [
        "closure_packet",
        "compatibility_manifest",
        "checker",
        "runtime_binding",
        "evidence",
        "check_results",
    ],
)
def test_receipt_missing_a_reproduced_block_is_a_clean_finding(drop: str) -> None:
    # A receipt that omits a block consumed during digest reproduction must be a
    # clean field-agreement finding on the runtime path, never an uncaught
    # KeyError (which would break the 0/1/2 exit-code contract). The defect is
    # reported before any object lookup, so the resolver is never called.
    receipt = _receipt(_fixture("handoff-receipt-valid"))
    del receipt[drop]
    resolver = _RecordingResolver()

    findings = validate_handoff_receipt(receipt, consumer_resolver=resolver)

    assert "HGR-HANDOFF-STRUCTURE" in _codes(findings)
    assert resolver.calls == []


def test_receipt_block_missing_digest_field_is_a_clean_finding() -> None:
    receipt = _receipt(_fixture("handoff-receipt-valid"))
    del receipt["compatibility_manifest"]["digest"]
    resolver = _RecordingResolver()

    findings = validate_handoff_receipt(receipt, consumer_resolver=resolver)

    assert _codes(findings) == ["HGR-HANDOFF-STRUCTURE"]
    assert resolver.calls == []


def test_provider_repository_must_be_openxfactory() -> None:
    receipt = _receipt(_fixture("handoff-receipt-valid"))
    receipt["provider"]["repository"] = "FarHeap/openxFactory"
    resolver = _RecordingResolver()

    findings = validate_handoff_receipt(receipt, consumer_resolver=resolver)

    assert _codes(findings) == ["HGR-HANDOFF-PROVIDER"]
    assert resolver.calls == []


def test_negative_drift_check_must_record_failure(tmp_path: Path) -> None:
    fixture = _fixture("handoff-receipt-drift-check-passed")
    negative = fixture["input"]["value"]["check_results"]["negative"]
    assert [result["outcome"] for result in negative] == ["pass"]
    resolver = _RecordingResolver()

    findings = validate_handoff_receipt(_receipt(fixture), consumer_resolver=resolver)

    assert _codes(findings) == ["HGR-HANDOFF-CHECK-RESULTS"]
    assert resolver.calls == []

    positive_drift = _receipt(_fixture("handoff-receipt-valid"))
    positive_drift["check_results"]["positive"][0]["outcome"] = "fail"
    findings = validate_handoff_receipt(
        positive_drift, consumer_resolver=_RecordingResolver()
    )
    assert _codes(findings) == ["HGR-HANDOFF-CHECK-RESULTS"]


@pytest.mark.parametrize("missing", ["path", "commit"])
def test_missing_recorded_object_is_a_dependency_error(
    tmp_path: Path, missing: str
) -> None:
    fixture = _fixture("handoff-receipt-valid")
    repo, commit = _build_consumer_repo(tmp_path, fixture)
    receipt = _receipt(fixture, commit)
    if missing == "path":
        receipt["checker"]["path"] = "config/scripts/absent-checker.py"
    else:
        receipt["consumer_commit"] = "2" * 40
    resolver = build_consumer_resolver({CONSUMER_REPOSITORY: repo}, None)

    with pytest.raises(ConsumerHandoffDependencyError) as excinfo:
        validate_handoff_receipt(receipt, consumer_resolver=resolver)

    assert excinfo.value.exit_code == 2


def test_unresolvable_consumer_repository_is_a_dependency_error(
    tmp_path: Path,
) -> None:
    fixture = _fixture("handoff-receipt-valid")
    _, commit = _build_consumer_repo(tmp_path, fixture)
    receipt = _receipt(fixture, commit)
    resolver = build_consumer_resolver(None, tmp_path / "empty-root")

    with pytest.raises(ConsumerHandoffDependencyError) as excinfo:
        validate_handoff_receipt(receipt, consumer_resolver=resolver)

    assert excinfo.value.exit_code == 2

    with pytest.raises(ConsumerHandoffDependencyError):
        validate_handoff_receipt(
            receipt, consumer_resolver=build_consumer_resolver(None, None)
        )


def test_consumer_resolver_deterministic_root_rules(tmp_path: Path) -> None:
    root = tmp_path / "mirrors"
    plain = root / "opensoft" / "xFactory-Hermes-Install"
    plain.mkdir(parents=True)

    resolver = build_consumer_resolver(None, root)
    assert resolver(CONSUMER_REPOSITORY) == plain

    bare = root / "opensoft" / "xFactory-Hermes-Install.git"
    bare.mkdir()
    with pytest.raises(ConsumerHandoffDependencyError):
        resolver(CONSUMER_REPOSITORY)

    override = tmp_path / "explicit-checkout"
    override.mkdir()
    mapped = build_consumer_resolver({CONSUMER_REPOSITORY: override}, root)
    assert mapped(CONSUMER_REPOSITORY) == override

    with pytest.raises(ConsumerHandoffDependencyError):
        resolver("opensoft/absent-repository")
    with pytest.raises(ConsumerHandoffDependencyError):
        resolver("not-a-canonical-repository")
    with pytest.raises(ConsumerHandoffDependencyError):
        build_consumer_resolver({"../escape": override}, None)


def test_working_tree_spoof_is_rejected(tmp_path: Path) -> None:
    fixture = _fixture("handoff-receipt-valid")
    repo, commit = _build_consumer_repo(tmp_path, fixture)
    receipt = _receipt(fixture, commit)
    packet_path = receipt["closure_packet"]["path"]
    spoofed = b"schema_version: 1\nkind: spoofed-working-tree-packet\n"
    (repo / packet_path).write_bytes(spoofed)
    resolver = build_consumer_resolver({CONSUMER_REPOSITORY: repo}, None)

    # The committed bytes still verify even though the working tree drifted.
    assert validate_handoff_receipt(receipt, consumer_resolver=resolver) == []

    # A receipt recording the spoofed working-tree bytes must be rejected:
    # validation reads exact commit bytes, never the mutable working tree.
    spoofed_receipt = deepcopy(receipt)
    spoofed_receipt["closure_packet"]["digest"] = _digest(spoofed)
    findings = validate_handoff_receipt(spoofed_receipt, consumer_resolver=resolver)
    assert _codes(findings) == ["HGR-HANDOFF-PACKET-DIGEST"]


@pytest.mark.parametrize("case_id", sorted(FIXTURE_FILES))
def test_fixture_self_description_is_consistent(case_id: str) -> None:
    fixture = _fixture(case_id)
    assert fixture["schema_version"] == 1
    assert fixture["kind"] == "openxfactory-hermes-runtime-portable-evidence-fixture"
    assert fixture["case_id"] == case_id
    assert case_id.startswith("handoff-")
    assert fixture["phase"] == "semantic"
    assert fixture["evaluation_time"] == "2026-07-13T12:00:00Z"
    assert fixture["requirement_ids"] == ["SCO-002"]
    assert fixture["scenario_ids"]
    assert all(scenario.startswith("SCO-002-S") for scenario in fixture["scenario_ids"])
    assert fixture["git_tree"]["repository"] == CONSUMER_REPOSITORY

    expected = fixture["expected"]
    expected_primary = EXPECTED_PRIMARY_CODES[case_id]
    if expected_primary is None:
        assert fixture["class"] == "valid"
        assert expected == {"outcome": "pass", "allowed_secondary_codes": []}
    else:
        assert fixture["class"] == "invalid"
        assert expected["outcome"] == "fail"
        assert expected["primary_finding_code"] == expected_primary
        assert expected["primary_finding_code"].startswith("HGR-HANDOFF-")
        assert expected["allowed_secondary_codes"] == []
