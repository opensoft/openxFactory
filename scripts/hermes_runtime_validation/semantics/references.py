"""Pure and exact-object customer-subject reference-policy conformance rules."""

from __future__ import annotations

from collections.abc import Callable, Mapping
import os
import re
import uuid
from typing import Any

from scripts.hermes_runtime_validation.content import ResolvedGitContent, resolve_git_object


_SUBJECT_URN = re.compile(
    r"^urn:xfactory:subject:"
    r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$"
)
_NEUTRAL_TOKEN = re.compile(r"^[a-z][a-z0-9._-]{0,127}$")
_CANONICAL_REPOSITORY = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?/"
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?$"
)
_COMMIT = re.compile(r"^[0-9a-f]{40}$")
_PATH = re.compile(
    r"^(?!/)(?!.*(?:^|/)(?:\.|\.\.)(?:/|$))(?!.*//)(?!.*\\)"
    r"[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*$"
)
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")

_ALLOWED_CONSTRUCTIONS = {"uuidv4", "uuidv7", "keyed_tokenization"}
_FORBIDDEN_CONSTRUCTIONS = {
    "uuidv1",
    "uuidv3",
    "uuidv5",
    "reversible_encoding",
    "raw_hash",
    "unkeyed_hash",
    "unkeyed_derivation",
    "direct_identifier",
}
_CLAIMS = {
    "surrogate_pseudonymous",
    "no_direct_identifier",
    "no_secret",
    "no_reversible_encoding",
    "no_unkeyed_derivation",
    "construction_authorized",
}
_SENSITIVE_CLAIMS = {
    "surrogate_pseudonymous",
    "no_direct_identifier",
    "no_secret",
}
_DERIVATION_CLAIMS = {
    "no_reversible_encoding",
    "no_unkeyed_derivation",
    "construction_authorized",
}

Resolver = Callable[[str | os.PathLike[str], str, str], ResolvedGitContent]
Finding = dict[str, str]


def _finding(code: str, path: str, message: str) -> Finding:
    return {"code": code, "severity": "error", "path": path, "message": message}


def _sorted(findings: list[Finding]) -> list[Finding]:
    unique: dict[tuple[str, str], Finding] = {}
    for finding in findings:
        unique.setdefault((finding["path"], finding["code"]), finding)
    return sorted(unique.values(), key=lambda finding: (finding["path"], finding["code"]))


def _valid_policy_pin(value: object) -> bool:
    if not isinstance(value, Mapping):
        return False
    return (
        isinstance(value.get("repository"), str)
        and _CANONICAL_REPOSITORY.fullmatch(value["repository"]) is not None
        and isinstance(value.get("commit"), str)
        and _COMMIT.fullmatch(value["commit"]) is not None
        and isinstance(value.get("path"), str)
        and _PATH.fullmatch(value["path"]) is not None
        and isinstance(value.get("digest"), str)
        and _DIGEST.fullmatch(value["digest"]) is not None
    )


def _valid_key_reference(value: object) -> bool:
    if not isinstance(value, Mapping):
        return False
    return (
        isinstance(value.get("provider"), str)
        and _NEUTRAL_TOKEN.fullmatch(value["provider"]) is not None
        and isinstance(value.get("key_id"), str)
        and bool(value["key_id"])
        and value.get("algorithm") == "hmac-sha256"
    )


def validate_customer_subject(
    customer_subject: Mapping[str, Any],
    reference_profile: Mapping[str, Any],
) -> list[Finding]:
    """Purely validate one subject against a complete issuer policy profile.

    This function binds identities, policy digests, attestation claims, and the
    declared construction without performing I/O. Use
    :func:`validate_customer_subject_full` at an admission/release boundary to
    additionally prove the policy pin from exact Git-object bytes.
    """

    if not isinstance(customer_subject, Mapping):
        return [
            _finding(
                "HCS-SUBJECT-REQUIRED",
                "customer_subject",
                "Customer layers require a customer_subject mapping",
            )
        ]
    if not isinstance(reference_profile, Mapping):
        return [
            _finding(
                "HCS-SUBJECT-PROFILE-REQUIRED",
                "reference_profile",
                "a pinned issuer reference profile is required",
            )
        ]

    findings: list[Finding] = []
    for field in ("kind", "issuer", "namespace"):
        value = customer_subject.get(field)
        if not isinstance(value, str) or _NEUTRAL_TOKEN.fullmatch(value) is None:
            findings.append(
                _finding(
                    "HCS-SUBJECT-IDENTITY-SYNTAX",
                    f"customer_subject.{field}",
                    f"{field} must be a bounded neutral token",
                )
            )

    ref = customer_subject.get("ref")
    match = _SUBJECT_URN.fullmatch(ref) if isinstance(ref, str) else None
    parsed_uuid: uuid.UUID | None = None
    if match is None:
        findings.append(
            _finding(
                "HCS-SUBJECT-REF-SYNTAX",
                "customer_subject.ref",
                "ref must be a lowercase urn:xfactory:subject:<uuid> surrogate",
            )
        )
    else:
        try:
            parsed_uuid = uuid.UUID(match.group(1))
        except ValueError:
            findings.append(
                _finding(
                    "HCS-SUBJECT-REF-SYNTAX",
                    "customer_subject.ref",
                    "ref contains an invalid RFC UUID surrogate",
                )
            )

    attestation_digest = customer_subject.get("issuer_attestation_digest")
    attestation_digest_valid = (
        isinstance(attestation_digest, str)
        and _DIGEST.fullmatch(attestation_digest) is not None
    )
    if not attestation_digest_valid:
        findings.append(
            _finding(
                "HCS-SUBJECT-ATTESTATION-REQUIRED",
                "customer_subject.issuer_attestation_digest",
                "a lowercase SHA-256 issuer attestation digest is required",
            )
        )

    policy_pin = customer_subject.get("reference_policy_pin")
    pin_valid = _valid_policy_pin(policy_pin)
    if not pin_valid:
        findings.append(
            _finding(
                "HCS-SUBJECT-POLICY-PIN-REQUIRED",
                "customer_subject.reference_policy_pin",
                "an exact canonical repository/commit/path/digest policy pin is required",
            )
        )
    policy_digest = policy_pin.get("digest") if isinstance(policy_pin, Mapping) else None

    profile_issuer = reference_profile.get("issuer")
    profile_namespace = reference_profile.get("namespace")
    if (
        profile_issuer != customer_subject.get("issuer")
        or profile_namespace != customer_subject.get("namespace")
    ):
        findings.append(
            _finding(
                "HCS-SUBJECT-PROFILE-SCOPE-MISMATCH",
                "reference_profile",
                "profile issuer and namespace must exactly match the subject tuple",
            )
        )

    profile_policy_digest = reference_profile.get("policy_digest")
    profile_policy_valid = (
        isinstance(profile_policy_digest, str)
        and _DIGEST.fullmatch(profile_policy_digest) is not None
    )
    if pin_valid and (
        not profile_policy_valid or policy_digest != profile_policy_digest
    ):
        findings.append(
            _finding(
                "HCS-SUBJECT-POLICY-PIN-MISMATCH",
                "customer_subject.reference_policy_pin.digest",
                "reference policy pin must match the evaluated profile policy digest",
            )
        )

    attestation_value = reference_profile.get("attestation")
    attestation = attestation_value if isinstance(attestation_value, Mapping) else None
    claims: Mapping[str, Any] | None = None
    if attestation is None:
        findings.append(
            _finding(
                "HCS-SUBJECT-ATTESTATION-REQUIRED",
                "reference_profile.attestation",
                "a complete issuer attestation is required",
            )
        )
    else:
        recorded_digest = attestation.get("attestation_digest")
        required_attestation_fields = (
            isinstance(attestation.get("attestation_id"), str)
            and bool(attestation["attestation_id"])
            and isinstance(attestation.get("attested_at"), str)
            and isinstance(recorded_digest, str)
            and _DIGEST.fullmatch(recorded_digest) is not None
            and isinstance(attestation.get("policy_digest"), str)
            and _DIGEST.fullmatch(attestation["policy_digest"]) is not None
            and isinstance(attestation.get("issuer"), str)
        )
        if not required_attestation_fields:
            findings.append(
                _finding(
                    "HCS-SUBJECT-ATTESTATION-REQUIRED",
                    "reference_profile.attestation",
                    "issuer attestation identity, time, and digests are required",
                )
            )
        else:
            if attestation.get("issuer") != profile_issuer:
                findings.append(
                    _finding(
                        "HCS-SUBJECT-ATTESTATION-SCOPE-MISMATCH",
                        "reference_profile.attestation.issuer",
                        "attestation issuer must match the profile and subject issuer",
                    )
                )
            if (
                not profile_policy_valid
                or attestation.get("policy_digest") != profile_policy_digest
            ):
                findings.append(
                    _finding(
                        "HCS-SUBJECT-POLICY-PIN-MISMATCH",
                        "reference_profile.attestation.policy_digest",
                        "attestation must bind the exact evaluated policy digest",
                    )
                )
            if attestation_digest_valid and recorded_digest != attestation_digest:
                findings.append(
                    _finding(
                        "HCS-SUBJECT-ATTESTATION-MISMATCH",
                        "customer_subject.issuer_attestation_digest",
                        "subject attestation digest must match the pinned profile attestation",
                    )
                )

        claims_value = attestation.get("claims")
        if not isinstance(claims_value, Mapping) or not _CLAIMS <= set(claims_value):
            findings.append(
                _finding(
                    "HCS-SUBJECT-ATTESTATION-REQUIRED",
                    "reference_profile.attestation.claims",
                    "all closed issuer attestation claims are required",
                )
            )
        else:
            claims = claims_value

    sensitive = (
        reference_profile.get("contains_direct_identifier") is not False
        or reference_profile.get("contains_secret") is not False
        or not isinstance(reference_profile.get("sentinel_hits"), list)
        or bool(reference_profile.get("sentinel_hits"))
        or (
            claims is not None
            and any(claims.get(name) is not True for name in _SENSITIVE_CLAIMS)
        )
    )
    if sensitive:
        findings.append(
            _finding(
                "HCS-SUBJECT-SENSITIVE-SENTINEL",
                "reference_profile",
                "issuer claims or deterministic sentinel evidence indicate sensitive material",
            )
        )
    if claims is not None and any(
        claims.get(name) is not True for name in _DERIVATION_CLAIMS
    ):
        findings.append(
            _finding(
                "HCS-SUBJECT-DERIVATION-FORBIDDEN",
                "reference_profile.attestation.claims",
                "attestation does not prohibit reversible or unkeyed derivation",
            )
        )

    construction = reference_profile.get("construction")
    if construction in _FORBIDDEN_CONSTRUCTIONS or construction not in _ALLOWED_CONSTRUCTIONS:
        findings.append(
            _finding(
                "HCS-SUBJECT-DERIVATION-FORBIDDEN",
                "reference_profile.construction",
                "deterministic, reversible, direct, and unkeyed derivations are forbidden",
            )
        )
    elif construction == "keyed_tokenization":
        if reference_profile.get("keyed") is not True:
            findings.append(
                _finding(
                    "HCS-SUBJECT-DERIVATION-FORBIDDEN",
                    "reference_profile.keyed",
                    "keyed_tokenization requires an affirmative keyed declaration",
                )
            )
        if not _valid_key_reference(reference_profile.get("key_reference")):
            findings.append(
                _finding(
                    "HCS-SUBJECT-KEY-REFERENCE-REQUIRED",
                    "reference_profile.key_reference",
                    "approved keyed tokenization requires an opaque governed key reference",
                )
            )
        # The keyed token is carried in the constrained RFC UUID envelope. It
        # is not misrepresented as an independently random UUIDv4/UUIDv7.
    elif parsed_uuid is not None:
        expected_version = 4 if construction == "uuidv4" else 7
        if parsed_uuid.version != expected_version:
            findings.append(
                _finding(
                    "HCS-SUBJECT-UUID-VERSION",
                    "customer_subject.ref",
                    f"{construction} profile requires a UUIDv{expected_version} surrogate",
                )
            )
        if reference_profile.get("keyed") is not False or "key_reference" in reference_profile:
            findings.append(
                _finding(
                    "HCS-SUBJECT-DERIVATION-FORBIDDEN",
                    "reference_profile.keyed",
                    "independently random UUID profiles cannot claim keyed derivation",
                )
            )

    return _sorted(findings)


def validate_customer_subject_full(
    customer_subject: Mapping[str, Any],
    reference_profile: Mapping[str, Any],
    *,
    checkout: str | os.PathLike[str] | None,
    expected_repository: str | None,
    resolver: Resolver = resolve_git_object,
) -> list[Finding]:
    """Validate semantic binding plus the exact reference-policy Git object."""

    from scripts.hermes_runtime_validation.semantics.overlays import (
        validate_single_file_pin,
    )

    findings = validate_customer_subject(customer_subject, reference_profile)
    policy_pin = customer_subject.get("reference_policy_pin")
    if not _valid_policy_pin(policy_pin):
        return findings
    if checkout is None:
        findings.append(
            _finding(
                "HCS-PIN-CONTENT",
                "customer_subject.reference_policy_pin",
                "an exact policy checkout or mirror is required",
            )
        )
        return _sorted(findings)
    if not isinstance(expected_repository, str) or not expected_repository:
        findings.append(
            _finding(
                "HCS-PIN-REPOSITORY",
                "customer_subject.reference_policy_pin.repository",
                "an independently expected canonical repository is required",
            )
        )
        return _sorted(findings)

    pin_findings = validate_single_file_pin(
        policy_pin,
        checkout=checkout,
        expected_repository=expected_repository,
        resolver=resolver,
    )
    findings.extend(pin_findings)
    return _sorted(findings)
