"""THE PRESCRIPTION FOR THE NEXT MAJOR, MADE EXECUTABLE.

add-binding-consumer-identity declares the `consumer:` block at an additive
minor and constrains it at the next major. Everything about that second half is
prescription today — no shipped bytes carry it — and the packet's own quotable
finding is what this module exists to answer:

    A prescribed fix applied without a verifier is an unverified change,
    whatever its provenance.

Four council seats found the packet's decisive defect by BUILDING the prescribed
schema and driving a record through it; two Copilot reviews, three author
self-catches and a Codex P1 round had all READ the prescription instead. So the
prescription is built here, once, and both releases are driven against the same
six shapes — the minor from the SHIPPED schema, the major from this projection.

WHAT THE PROJECTION IS AND IS NOT. It is a test fixture, not a second contract:
nothing consumes it, no digest covers it, and the day the major is cut the acts
below move into `contracts/schemas/xfactory-credential-contracts.schema.yaml`
and this module becomes the diff to check the cut against. It carries exactly
the acts the ratified packet names and no others:

  * `type: object` on the block                          (§1.1a)
  * `additionalProperties: false` on the block           (§1.1a)
  * the identifier `pattern` on `holder_ref`/`fetch_identity` and on
    `requirement_ref.requirement_id`                     (§1.1a)
  * the qualified two-member `requirement_ref` object    (§1.1)
  * the repository-relative `requirements_document_ref` grammar (§1.5)
  * `const: true` on both tokens                         (§1.1)
  * `if not required(instantiation_stub) then required(holder_ref,
    fetch_identity)`                                     (§1.6)
  * `propertyNames` on the `credential_bindings` map     (§1.3)
  * `enum` on `access_mode`                              (§1.4)

WHAT IT DELIBERATELY DOES NOT DO — and each omission is a ruling, not a gap:

  * it does NOT require `consumer:` on a binding. A blockless template validates
    at the major's SCHEMA and is refused by its VALIDATOR
    (`consumer-identity-undeclared` as an error). Keeping the refusal in the
    validator is what lets the stub exemption reach it.
  * it does NOT close the BINDING OBJECT around the block. That is a further
    breaking act with a much wider blast radius and a named successor of its
    own.
"""
from __future__ import annotations

import copy
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "contracts/schemas/xfactory-credential-contracts.schema.yaml"

# Mirrored from the shipped validator so the two cannot drift apart unnoticed;
# `test_consumer_block_phasing.py` asserts the mirror.
IDENTIFIER_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$"
DOCUMENT_REF_PATTERN = (
    r"^(?!.*(?:^|/)\.\.(?:/|$))[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*\.(?:yaml|yml)$")
ACCESS_MODES = ["contents_write", "delegated_api", "dispatch_only", "workload_identity"]

_IDENTIFIER = {"type": "string", "minLength": 1, "maxLength": 200,
               "pattern": IDENTIFIER_PATTERN}

CONSUMER_AT_THE_MAJOR = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "holder_ref": dict(_IDENTIFIER),
        "fetch_identity": dict(_IDENTIFIER),
        "requirement_ref": {
            "type": "object",
            "required": ["requirement_id", "requirements_document_ref"],
            "additionalProperties": False,
            "properties": {
                "requirement_id": dict(_IDENTIFIER),
                "requirements_document_ref": {
                    "type": "string", "minLength": 1, "maxLength": 300,
                    "pattern": DOCUMENT_REF_PATTERN,
                },
            },
        },
        "shared_credential_acknowledged": {"const": True},
        "instantiation_stub": {"const": True},
    },
    # THE STUB EXEMPTION, expressed where a filename could never reach: a schema
    # can condition on a PROPERTY. A record that declares the token owes no
    # identifiers; every other record owes both.
    "if": {"not": {"required": ["instantiation_stub"]}},
    "then": {"required": ["holder_ref", "fetch_identity"]},
}

BINDING_KEY_AT_THE_MAJOR = {
    "type": "string", "minLength": 1, "maxLength": 200,
    "pattern": IDENTIFIER_PATTERN,
}


def load_minor_schema() -> dict:
    """The schema as SHIPPED — the introducing minor."""
    return yaml.safe_load(SCHEMA_PATH.read_text())


def branch_for_kind(schema: dict, kind: str) -> dict:
    """The `oneOf` member that governs one record kind."""
    for member in schema["oneOf"]:
        if member.get("properties", {}).get("kind", {}).get("const") == kind:
            return member
    raise AssertionError(f"no oneOf branch for kind {kind!r}")


_branch = branch_for_kind


def project_major_schema(minor: dict | None = None) -> dict:
    """The shipped schema PLUS every act the ratified packet defers to the major."""
    schema = copy.deepcopy(minor if minor is not None else load_minor_schema())

    bindings = _branch(schema, "xfactory_credential_binding_template")
    credential_bindings = bindings["properties"]["credential_bindings"]
    credential_bindings["propertyNames"] = copy.deepcopy(BINDING_KEY_AT_THE_MAJOR)
    binding = credential_bindings["additionalProperties"]
    binding["properties"]["consumer"] = copy.deepcopy(CONSUMER_AT_THE_MAJOR)

    requirements = _branch(schema, "xfactory_credential_requirements")
    item = requirements["properties"]["requirements"]["items"]
    access_mode = item["properties"]["access_mode"]
    access_mode.pop("description", None)
    access_mode["enum"] = list(ACCESS_MODES)

    return schema
