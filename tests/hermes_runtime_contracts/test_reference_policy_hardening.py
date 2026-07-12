"""Adversarial contracts for HCS-002 reference-policy binding and pin resolution."""

from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from scripts.hermes_runtime_validation.content import resolve_git_object
from scripts.hermes_runtime_validation.semantics import references
from tests.hermes_runtime_contracts.support import commit_files, finding_codes, init_git_repo


SHA_A = "sha256:" + "a" * 64
SHA_B = "sha256:" + "b" * 64
SHA_D = "sha256:" + "d" * 64
COMMIT = "c" * 40
UUID4 = "9f32f1de-82a7-4e38-a83d-9e5dd9189a11"
UUID7 = "018f47a0-7b2c-7abc-8def-0123456789ab"
UUID8 = "018f47a0-7b2c-8abc-8def-0123456789ab"
REPOSITORY = "opensoft/exampleFactory"


def _pin(*, commit: str = COMMIT, path: str = "policies/customer-subject.yaml", digest: str = SHA_B) -> dict:
    return {
        "repository": REPOSITORY,
        "commit": commit,
        "path": path,
        "digest": digest,
    }


def _subject(ref_uuid: str = UUID4, *, pin: dict | None = None) -> dict:
    return {
        "kind": "software_project",
        "issuer": "example-domain",
        "namespace": "customer-subjects",
        "ref": f"urn:xfactory:subject:{ref_uuid}",
        "reference_policy_pin": pin or _pin(),
        "issuer_attestation_digest": SHA_D,
    }


def _profile(construction: str = "uuidv4", *, policy_digest: str = SHA_B) -> dict:
    profile = {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-customer-subject-reference-profile",
        "profile_id": "example-domain-customer-subjects-v1",
        "issuer": "example-domain",
        "namespace": "customer-subjects",
        "policy_digest": policy_digest,
        "construction": construction,
        "keyed": construction == "keyed_tokenization",
        "contains_direct_identifier": False,
        "contains_secret": False,
        "sentinel_hits": [],
        "attestation": {
            "attestation_id": "attestation-customer-subjects-v1",
            "issuer": "example-domain",
            "policy_digest": policy_digest,
            "attestation_digest": SHA_D,
            "attested_at": "2026-07-12T12:00:00Z",
            "claims": {
                "surrogate_pseudonymous": True,
                "no_direct_identifier": True,
                "no_secret": True,
                "no_reversible_encoding": True,
                "no_unkeyed_derivation": True,
                "construction_authorized": True,
            },
        },
    }
    if construction == "keyed_tokenization":
        profile["key_reference"] = {
            "provider": "example-kms",
            "key_id": "customer-subject-tokenization-v1",
            "algorithm": "hmac-sha256",
        }
    return profile


def _codes(findings: list[dict[str, str]]) -> list[str]:
    return finding_codes(findings)


@pytest.mark.parametrize(
    ("ref_uuid", "construction"),
    [(UUID4, "uuidv4"), (UUID7, "uuidv7"), (UUID8, "keyed_tokenization")],
)
def test_complete_random_and_keyed_profiles_pass(
    ref_uuid: str, construction: str
) -> None:
    assert references.validate_customer_subject(
        _subject(ref_uuid), _profile(construction)
    ) == []


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("attestation_issuer", "HCS-SUBJECT-ATTESTATION-SCOPE-MISMATCH"),
        ("attestation_policy", "HCS-SUBJECT-POLICY-PIN-MISMATCH"),
        ("attestation_digest", "HCS-SUBJECT-ATTESTATION-MISMATCH"),
    ],
)
def test_subject_profile_and_attestation_are_one_bound_chain(
    mutation: str, expected_code: str
) -> None:
    subject = _subject()
    profile = _profile()
    if mutation == "attestation_issuer":
        profile["attestation"]["issuer"] = "other-issuer"
    elif mutation == "attestation_policy":
        profile["attestation"]["policy_digest"] = SHA_A
    else:
        profile["attestation"]["attestation_digest"] = SHA_A
    assert _codes(references.validate_customer_subject(subject, profile)) == [
        expected_code
    ]


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("profile_attestation", "HCS-SUBJECT-ATTESTATION-REQUIRED"),
        ("policy_pin", "HCS-SUBJECT-POLICY-PIN-REQUIRED"),
        ("key_reference", "HCS-SUBJECT-KEY-REFERENCE-REQUIRED"),
        ("claims", "HCS-SUBJECT-ATTESTATION-REQUIRED"),
        ("unkeyed_claim", "HCS-SUBJECT-DERIVATION-FORBIDDEN"),
        ("direct_identifier_claim", "HCS-SUBJECT-SENSITIVE-SENTINEL"),
    ],
)
def test_required_policy_evidence_fails_closed_for_one_exact_reason(
    mutation: str, expected_code: str
) -> None:
    construction = "keyed_tokenization" if mutation == "key_reference" else "uuidv4"
    subject = _subject(UUID8 if construction == "keyed_tokenization" else UUID4)
    profile = _profile(construction)
    if mutation == "profile_attestation":
        profile.pop("attestation")
    elif mutation == "policy_pin":
        subject.pop("reference_policy_pin")
    elif mutation == "key_reference":
        profile.pop("key_reference")
    elif mutation == "claims":
        profile["attestation"].pop("claims")
    elif mutation == "unkeyed_claim":
        profile["attestation"]["claims"]["no_unkeyed_derivation"] = False
    else:
        profile["attestation"]["claims"]["no_direct_identifier"] = False
    assert _codes(references.validate_customer_subject(subject, profile)) == [
        expected_code
    ]


@pytest.fixture
def exact_policy_repo(tmp_path: Path) -> tuple[Path, str, bytes]:
    repo = init_git_repo(tmp_path / "policy-repo")
    body = b"schema_version: 1\nkind: issuer-reference-policy\n"
    commit = commit_files(repo, {"policies/customer-subject.yaml": body})
    return repo, commit, body


def _exact_subject_profile(
    commit: str, body: bytes
) -> tuple[dict, dict]:
    digest = f"sha256:{hashlib.sha256(body).hexdigest()}"
    return (
        _subject(pin=_pin(commit=commit, digest=digest)),
        _profile(policy_digest=digest),
    )


def test_full_validation_resolves_exact_commit_bytes_not_dirty_worktree(
    exact_policy_repo: tuple[Path, str, bytes],
) -> None:
    repo, commit, body = exact_policy_repo
    subject, profile = _exact_subject_profile(commit, body)
    (repo / "policies/customer-subject.yaml").write_bytes(b"dirty spoof\n")
    assert references.validate_customer_subject_full(
        subject,
        profile,
        checkout=repo,
        expected_repository=REPOSITORY,
        resolver=resolve_git_object,
    ) == []


def test_full_validation_requires_checkout_and_expected_repository(
    exact_policy_repo: tuple[Path, str, bytes],
) -> None:
    repo, commit, body = exact_policy_repo
    subject, profile = _exact_subject_profile(commit, body)
    assert "HCS-PIN-CONTENT" in _codes(
        references.validate_customer_subject_full(
            subject,
            profile,
            checkout=None,
            expected_repository=REPOSITORY,
            resolver=resolve_git_object,
        )
    )
    assert "HCS-PIN-REPOSITORY" in _codes(
        references.validate_customer_subject_full(
            subject,
            profile,
            checkout=repo,
            expected_repository="opensoft/otherFactory",
            resolver=resolve_git_object,
        )
    )


@pytest.mark.parametrize("failure", ["commit", "path", "digest"])
def test_full_validation_rejects_missing_object_path_and_raw_digest_drift(
    exact_policy_repo: tuple[Path, str, bytes], failure: str
) -> None:
    repo, commit, body = exact_policy_repo
    subject, profile = _exact_subject_profile(commit, body)
    if failure == "commit":
        subject["reference_policy_pin"]["commit"] = "f" * 40
    elif failure == "path":
        subject["reference_policy_pin"]["path"] = "policies/missing.yaml"
    else:
        wrong = "sha256:" + "e" * 64
        subject["reference_policy_pin"]["digest"] = wrong
        profile["policy_digest"] = wrong
        profile["attestation"]["policy_digest"] = wrong

    codes = _codes(
        references.validate_customer_subject_full(
            subject,
            profile,
            checkout=repo,
            expected_repository=REPOSITORY,
            resolver=resolve_git_object,
        )
    )
    expected = "HCS-PIN-DIGEST" if failure == "digest" else "HCS-PIN-CONTENT"
    assert expected in codes


def test_negative_reference_fixtures_have_complete_unrelated_evidence() -> None:
    fixture_root = (
        Path(__file__).resolve().parents[2]
        / "contracts/hermes-runtime/fixtures/references"
    )
    from scripts.hermes_runtime_validation.loader import load_yaml_document

    for path in sorted(fixture_root.glob("*.yaml")):
        fixture = load_yaml_document(path)
        profile = fixture["reference_profile"]
        assert profile["schema_version"] == 1, path
        assert profile["kind"] == (
            "openxfactory-hermes-runtime-customer-subject-reference-profile"
        ), path
        assert profile["profile_id"], path
        assert profile["attestation"]["claims"], path
        if profile["construction"] == "keyed_tokenization":
            assert profile["key_reference"], path
        assert _codes(
            references.validate_customer_subject(
                fixture["customer_subject"], fixture["reference_profile"]
            )
        ) == ([fixture["expected"]["primary_finding_code"]] if fixture["expected"]["outcome"] == "fail" else []), path


def test_fixture_schema_errors_are_limited_to_the_intended_violation() -> None:
    from scripts.hermes_runtime_validation.loader import load_yaml_document

    contract_root = Path(__file__).resolve().parents[2] / "contracts/hermes-runtime"
    shared = load_yaml_document(contract_root / "shared-definitions.schema.yaml")
    profile_schema = load_yaml_document(
        contract_root / "customer-subject-reference-profile.schema.yaml"
    )
    registry = (
        Registry()
        .with_resource(shared["$id"], Resource.from_contents(shared))
        .with_resource(profile_schema["$id"], Resource.from_contents(profile_schema))
    )
    profile_validator = Draft202012Validator(
        profile_schema, registry=registry, format_checker=FormatChecker()
    )
    subject_validator = Draft202012Validator(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": profile_schema["$id"] + "#/$defs/customer_subject",
        },
        registry=registry,
        format_checker=FormatChecker(),
    )

    for path in sorted((contract_root / "fixtures/references").glob("*.yaml")):
        fixture = load_yaml_document(path)
        profile_paths = [
            tuple(error.absolute_path)
            for error in profile_validator.iter_errors(fixture["reference_profile"])
        ]
        subject_paths = [
            tuple(error.absolute_path)
            for error in subject_validator.iter_errors(fixture["customer_subject"])
        ]
        if path.name in {
            "unsafe-derivation.yaml",
            "uuidv1-subject.yaml",
            "uuidv3-subject.yaml",
            "uuidv5-subject.yaml",
        }:
            assert profile_paths == [("construction",)], path
            assert subject_paths == [], path
        elif path.name == "missing-attestation.yaml":
            assert profile_paths == [], path
            assert subject_paths == [()], path
        else:
            assert profile_paths == [], path
            assert subject_paths == [], path
