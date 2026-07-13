"""Portable contracts for governed artifacts, approvals, and trace evidence."""

from __future__ import annotations

import hashlib
import importlib
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from scripts.hermes_runtime_validation import migration
from scripts.hermes_runtime_validation.loader import load_yaml_document
from scripts.hermes_runtime_validation.semantics.authority import (
    canonical_record_digest,
    validate_authority_document,
)
from tests.hermes_runtime_contracts.support import finding_codes

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_ROOT = ROOT / "contracts/hermes-runtime"
FIXTURE_ROOT = CONTRACT_ROOT / "fixtures"
SCHEMA_NAMES = (
    "artifact-record.schema.yaml",
    "artifact-lifecycle-event.schema.yaml",
    "approval-decision-policy.schema.yaml",
    "approval-request.schema.yaml",
    "approval-decision.schema.yaml",
    "approval-supersession-event.schema.yaml",
    "traceability-edge.schema.yaml",
)

SHA_A = "sha256:" + "a" * 64
SHA_B = "sha256:" + "b" * 64
SHA_C = "sha256:" + "c" * 64
COMMIT = "d" * 40
NOW = "2026-07-12T12:00:00Z"
LATER = "2026-07-12T13:00:00Z"
EXPIRED = "2026-07-12T11:00:00Z"

# The US3 migration semantic family carries its own fixture kind and
# evaluation time; the Lane D registration record pins the primary
# finding code for each *-invalid case.
MIGRATION_FIXTURE_KIND = "openxfactory-hermes-runtime-migration-fixture"
MIGRATION_NOW = "2026-07-13T12:00:00Z"
MIGRATION_PRIMARY_CODES = {
    "mapping-payload-invalid": "HGR-MIGRATION-PAYLOAD-MAPPING",
    "quarantine-record-invalid": "HGR-QUARANTINE-DEPENDENCY",
}
QUARANTINE_DEPENDENCY_FIELDS = frozenset(
    {"promoted", "promoted_operation_authorization_id"}
)


def _scope(layer_id: str = "customer-a") -> dict:
    return {
        "scope_kind": "layer",
        "installation_id": "install-01",
        "stack_id": "stack-01",
        "layer_id": layer_id,
    }


def _resource(
    resource_id: str,
    *,
    layer_id: str = "customer-a",
    digest: str = SHA_A,
    resource_type: str = "artifact",
) -> dict:
    return {
        "installation_id": "install-01",
        "stack_id": "stack-01",
        "layer_id": layer_id,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "digest": digest,
    }


def _principal_ref(
    principal_id: str, *, digest: str = SHA_A, layer_id: str = "customer-a"
) -> dict:
    return {
        "scope": _scope(layer_id),
        "principal_id": principal_id,
        "record_digest": digest,
    }


def _grant_ref(grant_id: str, *, digest: str = SHA_B) -> dict:
    return {
        "installation_id": "install-01",
        "grant_id": grant_id,
        "record_digest": digest,
    }


def _binding_ref(binding_id: str, *, digest: str = SHA_B) -> dict:
    return {
        "installation_id": "install-01",
        "binding_id": binding_id,
        "record_digest": digest,
    }


def _operation_ref(operation_id: str, *, digest: str = SHA_C) -> dict:
    return {
        "installation_id": "install-01",
        "operation_id": operation_id,
        "record_digest": digest,
    }


def _principal(
    principal_id: str,
    *,
    principal_type: str = "agent",
    digest: str = SHA_A,
    layer_id: str = "customer-a",
) -> dict:
    return {
        "principal_id": principal_id,
        "record_digest": digest,
        "principal_type": principal_type,
        "scope": _scope(layer_id),
        "initial_lifecycle_state": "provisioning",
    }


def _activation_projection(principal: dict) -> dict:
    return {
        "event_id": f"activate-{principal['principal_id']}",
        "principal_ref": {
            "scope": deepcopy(principal["scope"]),
            "principal_id": principal["principal_id"],
            "record_digest": principal["record_digest"],
        },
        "from_state": "provisioning",
        "to_state": "active",
        "occurred_at": EXPIRED,
    }


def _grant(
    grant_id: str,
    principal_ref: dict,
    *,
    action: str,
    resource_constraint: dict,
    digest: str = SHA_B,
    layer_id: str = "customer-a",
) -> dict:
    return {
        "installation_id": "install-01",
        "grant_id": grant_id,
        "record_digest": digest,
        "principal_ref": deepcopy(principal_ref),
        "scope": _scope(layer_id),
        "action": action,
        "resource_constraint": deepcopy(resource_constraint),
        "starts_at": EXPIRED,
        "expires_at": LATER,
    }


def _artifact(body: bytes = b"portable artifact body\n") -> dict:
    digest = "sha256:" + hashlib.sha256(body).hexdigest()
    return {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-artifact-record",
        "installation_id": "install-01",
        "stack_id": "stack-01",
        "layer_id": "customer-a",
        "artifact_id": "artifact-01",
        "content_digest": digest,
        "byte_size": len(body),
        "media_type": "application/octet-stream",
        "producer_principal_ref": _principal_ref("worker-a"),
        "producer_grant_ref": _grant_ref("grant-produce-a"),
        "storage_key": f"install-01/customer-a/sha256/{digest.removeprefix('sha256:')}",
        "created_at": NOW,
    }


def _artifact_event(artifact: dict) -> dict:
    return {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-artifact-lifecycle-event",
        "event_id": "artifact-event-01",
        "event_digest": SHA_C,
        "installation_id": artifact["installation_id"],
        "stack_id": artifact["stack_id"],
        "layer_id": artifact["layer_id"],
        "artifact_id": artifact["artifact_id"],
        "artifact_record_digest": SHA_A,
        "predecessor_ref": {
            "kind": "artifact_record",
            "id": artifact["artifact_id"],
            "digest": SHA_A,
        },
        "event_type": "available",
        "actor_principal_ref": _principal_ref("worker-a"),
        "actor_grant_ref": _grant_ref("grant-produce-a"),
        "occurred_at": NOW,
        "reason": "content-finalized",
    }


def _policy(*, conflict_resolution: str = "contested") -> dict:
    return {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-approval-decision-policy",
        "policy_id": "policy-pr-admission",
        "policy_digest": SHA_C,
        "authority_scope": _scope(),
        "reviewer_selectors": [
            {
                "selector_id": "manager",
                "principal_ids": ["manager-a"],
                "minimum_count": 1,
                "distinct_principals": True,
            },
            {
                "selector_id": "security",
                "principal_ids": ["security-a"],
                "minimum_count": 1,
                "distinct_principals": True,
            },
        ],
        "aggregation": "all_required_selectors",
        "conflict_resolution": conflict_resolution,
        "supersession_authorities": [
            {"event_type": event_type, "principal_ids": ["manager-a"]}
            for event_type in ("expired", "cancelled", "revoked")
        ],
        "created_at": NOW,
    }


def _policy_pin(policy: dict) -> dict:
    return {
        "repository": "opensoft/exampleFactory",
        "commit": COMMIT,
        "path": "policies/pr-admission.yaml",
        "digest": policy["policy_digest"],
        "schema_id": (
            "https://xforge.us/schemas/openxfactory/hermes-runtime/v2/"
            "approval-decision-policy.schema.yaml"
        ),
        "schema_version": 1,
    }


def _request(policy: dict, artifact: dict) -> dict:
    return {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-approval-request",
        "request_id": "approval-request-01",
        "request_digest": SHA_A,
        "owning_scope": _scope(),
        "target": _resource(artifact["artifact_id"], digest=artifact["content_digest"]),
        "requested_action": "execute",
        "authority_scope": _scope(),
        "requester_principal_ref": _principal_ref("requester-a"),
        "requester_grant_ref": _grant_ref("grant-request-a"),
        "reviewer_selector_ids": ["manager", "security"],
        "decision_policy_id": policy["policy_id"],
        "decision_policy_digest": policy["policy_digest"],
        "decision_policy_pin": _policy_pin(policy),
        "created_at": NOW,
        "expires_at": LATER,
    }


def _decision(
    request: dict,
    *,
    selector_id: str,
    principal_ref: dict,
    grant_ref: dict,
    decision: str = "approve",
) -> dict:
    return {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-approval-decision",
        "decision_id": f"decision-{selector_id}-{decision}",
        "decision_digest": SHA_B if selector_id == "manager" else SHA_C,
        "request_id": request["request_id"],
        "request_digest": request["request_digest"],
        "owning_scope": deepcopy(request["owning_scope"]),
        "target": deepcopy(request["target"]),
        "requested_action": request["requested_action"],
        "authority_scope": deepcopy(request["authority_scope"]),
        "decision_policy_id": request["decision_policy_id"],
        "decision_policy_digest": request["decision_policy_digest"],
        "reviewer_selector_id": selector_id,
        "actual_reviewer_principal_ref": deepcopy(principal_ref),
        "reviewer_grant_ref": deepcopy(grant_ref),
        "decision": decision,
        "decided_at": NOW,
    }


def _supersession(request: dict, *, event_type: str = "cancelled") -> dict:
    return {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-approval-supersession-event",
        "event_id": f"supersession-{event_type}",
        "event_digest": SHA_C,
        "event_type": event_type,
        "target_kind": "request",
        "target_id": request["request_id"],
        "target_digest": request["request_digest"],
        "owning_scope": deepcopy(request["owning_scope"]),
        "authority_scope": deepcopy(request["authority_scope"]),
        "issuer_principal_ref": _principal_ref("manager-a"),
        "issuer_grant_ref": _grant_ref("grant-manager-supersede", digest=SHA_C),
        "effective_at": NOW,
        "reason": f"governed-{event_type}",
    }


def _approval_inputs(*, conflict_resolution: str = "contested") -> dict:
    artifact = _artifact()
    policy = _policy(conflict_resolution=conflict_resolution)
    request = _request(policy, artifact)
    request_resource = {
        "installation_id": request["owning_scope"]["installation_id"],
        "stack_id": request["owning_scope"]["stack_id"],
        "layer_id": request["owning_scope"]["layer_id"],
        "resource_type": "approval_request",
        "resource_id": request["request_id"],
        "digest": request["request_digest"],
    }
    principals = [
        _principal("requester-a", principal_type="human"),
        _principal("manager-a"),
        _principal("security-a"),
    ]
    grants = [
        _grant(
            "grant-request-a",
            _principal_ref("requester-a"),
            action="request_approval",
            resource_constraint=request["target"],
        ),
        _grant(
            "grant-manager-a",
            _principal_ref("manager-a"),
            action="decide_approval",
            resource_constraint=request_resource,
        ),
        _grant(
            "grant-security-a",
            _principal_ref("security-a"),
            action="decide_approval",
            resource_constraint=request_resource,
        ),
        _grant(
            "grant-manager-supersede",
            _principal_ref("manager-a"),
            action="supersede_approval",
            resource_constraint=request_resource,
            digest=SHA_C,
        ),
    ]
    grant_by_id = {item["grant_id"]: item for item in grants}
    decisions = [
        _decision(
            request,
            selector_id="manager",
            principal_ref=grant_by_id["grant-manager-a"]["principal_ref"],
            grant_ref=_grant_ref("grant-manager-a"),
        ),
        _decision(
            request,
            selector_id="security",
            principal_ref=grant_by_id["grant-security-a"]["principal_ref"],
            grant_ref=_grant_ref("grant-security-a"),
        ),
    ]
    return {
        "artifact": artifact,
        "policy": policy,
        "request": request,
        "decisions": decisions,
        "authority": {
            "evaluation_time": NOW,
            "principals": principals,
            "principal_lifecycle_events": [
                _activation_projection(principal) for principal in principals
            ],
            "authority_grants": grants,
            "grant_revocations": [],
        },
    }


def _seal(record: dict) -> dict:
    sealed = deepcopy(record)
    sealed["record_digest_profile"] = "xfactory-canonical-json-v1"
    sealed["record_digest"] = canonical_record_digest(sealed)
    return sealed


def _exact_principal_ref(principal: dict) -> dict:
    return {
        "scope": deepcopy(principal["scope"]),
        "principal_id": principal["principal_id"],
        "record_digest": principal["record_digest"],
    }


def _exact_grant_ref(grant: dict) -> dict:
    return {
        "installation_id": grant["installation_id"],
        "grant_id": grant["grant_id"],
        "record_digest": grant["record_digest"],
    }


def _sealed_principal(
    principal_id: str, scope: dict, *, principal_type: str = "agent"
) -> dict:
    return _seal(
        {
            "schema_version": 1,
            "kind": "openxfactory-principal",
            "principal_id": principal_id,
            "principal_type": principal_type,
            "scope": deepcopy(scope),
            "initial_lifecycle_state": "provisioning",
            "created_at": EXPIRED,
        }
    )


def _authority_policy_pin() -> dict:
    return {
        "repository": "opensoft/exampleFactory",
        "commit": COMMIT,
        "path": "policies/authority.yaml",
        "digest": SHA_C,
        "schema_id": (
            "https://xforge.us/schemas/openxfactory/hermes-runtime/v2/"
            "authority-grant.schema.yaml"
        ),
        "schema_version": 1,
    }


def _sealed_grant(
    grant_id: str,
    principal_ref: dict,
    scope: dict,
    action: str,
    resource_constraint: dict,
    *,
    root_anchor_ref: dict | None = None,
    issuer_grant_ref: dict | None = None,
) -> dict:
    grant = {
        "schema_version": 1,
        "kind": "openxfactory-authority-grant",
        "grant_id": grant_id,
        "installation_id": "install-01",
        "grant_kind": "root" if root_anchor_ref is not None else "delegated",
        "principal_ref": deepcopy(principal_ref),
        "scope": deepcopy(scope),
        "action": action,
        "resource_constraint": deepcopy(resource_constraint),
        "policy_pin": _authority_policy_pin(),
        "starts_at": EXPIRED,
        "expires_at": LATER,
        "issued_at": EXPIRED,
    }
    if root_anchor_ref is not None:
        grant["root_anchor_ref"] = deepcopy(root_anchor_ref)
    if issuer_grant_ref is not None:
        grant["issuer_grant_ref"] = deepcopy(issuer_grant_ref)
    return _seal(grant)


def _sealed_activation_event(principal: dict, authorizing_grant: dict) -> dict:
    return _seal(
        {
            "schema_version": 1,
            "kind": "openxfactory-principal-lifecycle-event",
            "event_id": f"activate-{principal['principal_id']}",
            "principal_ref": _exact_principal_ref(principal),
            "predecessor_ref": {
                "kind": "registration",
                "id": principal["principal_id"],
                "record_digest": principal["record_digest"],
            },
            "from_state": "provisioning",
            "to_state": "active",
            "authorizing_grant_ref": _exact_grant_ref(authorizing_grant),
            "occurred_at": EXPIRED,
            "reason": "activate governed principal",
        }
    )


def _integrated_approval_document() -> tuple[dict, dict]:
    inputs = _approval_inputs()
    installation_scope = {
        "scope_kind": "installation",
        "installation_id": "install-01",
    }
    root = _sealed_principal("root-authority", installation_scope)
    requester = _sealed_principal("requester-a", _scope(), principal_type="human")
    manager = _sealed_principal("manager-a", _scope())
    security = _sealed_principal("security-a", _scope())
    principals = [root, requester, manager, security]

    anchor = _seal(
        {
            "schema_version": 1,
            "kind": "openxfactory-installation-trust-anchor",
            "anchor_id": "anchor-genesis",
            "installation_id": "install-01",
            "anchor_kind": "genesis",
            "principal_ref": _exact_principal_ref(root),
            "key_ref": {
                "provider": "test-keyring",
                "key_id": "root-key",
                "algorithm": "ed25519",
            },
            "policy_pin": _authority_policy_pin(),
            "effective_at": EXPIRED,
            "authorized_evidence_digest": SHA_A,
            "created_at": EXPIRED,
        }
    )
    anchor_ref = {
        "installation_id": "install-01",
        "anchor_id": anchor["anchor_id"],
        "record_digest": anchor["record_digest"],
    }
    issue_grant = _sealed_grant(
        "grant-root-issue",
        _exact_principal_ref(root),
        installation_scope,
        "issue_grant",
        {
            "installation_id": "install-01",
            "resource_type": "policy_namespace",
            "resource_id": "authority-issuance",
        },
        root_anchor_ref=anchor_ref,
    )
    transition_grant = _sealed_grant(
        "grant-root-transition",
        _exact_principal_ref(root),
        installation_scope,
        "transition_lifecycle",
        {
            "installation_id": "install-01",
            "resource_type": "policy_namespace",
            "resource_id": "principal-lifecycle",
        },
        root_anchor_ref=anchor_ref,
    )
    principal_lifecycle_events = [
        _sealed_activation_event(principal, transition_grant)
        for principal in principals
    ]
    issuer_ref = _exact_grant_ref(issue_grant)
    request_resource = _approval_resource(inputs["request"], "approval_request")
    request_grant = _sealed_grant(
        "grant-request-a",
        _exact_principal_ref(requester),
        _scope(),
        "request_approval",
        inputs["request"]["target"],
        issuer_grant_ref=issuer_ref,
    )
    manager_grant = _sealed_grant(
        "grant-manager-a",
        _exact_principal_ref(manager),
        _scope(),
        "decide_approval",
        request_resource,
        issuer_grant_ref=issuer_ref,
    )
    security_grant = _sealed_grant(
        "grant-security-a",
        _exact_principal_ref(security),
        _scope(),
        "decide_approval",
        request_resource,
        issuer_grant_ref=issuer_ref,
    )

    inputs["request"]["requester_principal_ref"] = _exact_principal_ref(requester)
    inputs["request"]["requester_grant_ref"] = _exact_grant_ref(request_grant)
    for decision, principal, grant in (
        (inputs["decisions"][0], manager, manager_grant),
        (inputs["decisions"][1], security, security_grant),
    ):
        decision["actual_reviewer_principal_ref"] = _exact_principal_ref(principal)
        decision["reviewer_grant_ref"] = _exact_grant_ref(grant)

    authority_document = {
        "evaluation_time": NOW,
        "principals": principals,
        "principal_lifecycle_events": principal_lifecycle_events,
        "trust_anchors": [anchor],
        "authority_grants": [
            issue_grant,
            transition_grant,
            request_grant,
            manager_grant,
            security_grant,
        ],
    }
    document = {
        "operation": "evaluate_approval",
        "evaluation_time": NOW,
        "authority_document": authority_document,
        "input": {
            "request": inputs["request"],
            "policy": inputs["policy"],
            "decisions": inputs["decisions"],
            "supersessions": [],
            "target": inputs["request"]["target"],
        },
    }
    return document, inputs


def _trace_inputs(*, same_layer: bool = False) -> dict:
    source = _resource("artifact-source", digest=SHA_A)
    target = _resource(
        "artifact-target",
        layer_id="customer-a" if same_layer else "customer-b",
        digest=SHA_B,
    )
    source_scope = _scope("customer-a")
    target_scope = _scope("customer-a" if same_layer else "customer-b")
    creator_principal_ref = _principal_ref("trace-writer-a")
    source_grant_ref = _grant_ref("grant-trace-a", digest=SHA_A)
    target_grant_ref = _grant_ref("grant-accept-b", digest=SHA_C)
    binding_ref = _binding_ref("binding-a-b")
    authority = {
        "operation_authorization_ref": _operation_ref("operation-01"),
        "binding_ref": binding_ref,
        "grant_refs": [source_grant_ref, target_grant_ref],
    }
    edge = {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-traceability-edge",
        "edge_id": "trace-edge-01",
        "edge_digest": SHA_C,
        "owning_scope": deepcopy(target_scope),
        "relation": "project_resource",
        "source": source,
        "target": target,
        "creator_principal_ref": creator_principal_ref,
        "creator_grant_ref": source_grant_ref,
        "cross_layer_authority": authority,
        "created_at": NOW,
    }
    operation = {
        "operation_id": "operation-01",
        "record_digest": SHA_C,
        "source_scope": source_scope,
        "target_scope": target_scope,
        "source_resource": deepcopy(source),
        "target_resource": deepcopy(target),
        "action": "project_resource",
        "actor_principal_ref": creator_principal_ref,
        "source_grant_ref": source_grant_ref,
        "target_acceptance_grant_ref": target_grant_ref,
        "binding_ref": binding_ref,
        "authorized_at": NOW,
        "target_result": deepcopy(target),
    }
    binding = {
        "binding_id": "binding-a-b",
        "record_digest": SHA_B,
        "source_scope": source_scope,
        "target_scope": target_scope,
        "source_resource": deepcopy(source),
        "target_resource": deepcopy(target),
        "action": "project_resource",
    }
    resources = {
        (
            source["installation_id"],
            source["stack_id"],
            source["layer_id"],
            source["resource_type"],
            source["resource_id"],
        ): deepcopy(source),
        (
            target["installation_id"],
            target["stack_id"],
            target["layer_id"],
            target["resource_type"],
            target["resource_id"],
        ): deepcopy(target),
    }
    source_grant = _grant(
        "grant-trace-a",
        creator_principal_ref,
        action="project_resource",
        resource_constraint=source,
        digest=SHA_A,
    )
    target_grant = _grant(
        "grant-accept-b",
        _principal_ref("acceptor-b", digest=SHA_C, layer_id="customer-b"),
        action="accept_cross_layer",
        resource_constraint=target,
        digest=SHA_C,
        layer_id="customer-b",
    )
    return {
        "edge": edge,
        "resources": resources,
        "operations": {operation["operation_id"]: operation},
        "bindings": {binding["binding_id"]: binding},
        "authority": {
            "evaluation_time": NOW,
            "principals": [
                _principal("trace-writer-a"),
                _principal(
                    "acceptor-b",
                    digest=SHA_C,
                    layer_id="customer-b",
                ),
            ],
            "authority_grants": [source_grant, target_grant],
            "grant_revocations": [],
            "cross_layer_bindings": [binding],
            "operation_authorizations": [operation],
            "resources": list(resources.values()),
        },
    }


@pytest.fixture
def api():
    return importlib.import_module(
        "scripts.hermes_runtime_validation.semantics.evidence"
    )


@pytest.fixture(scope="module")
def validators() -> dict[str, Draft202012Validator]:
    names = ("shared-definitions.schema.yaml", *SCHEMA_NAMES)
    documents = {name: load_yaml_document(CONTRACT_ROOT / name) for name in names}
    resources = [
        (
            document["$id"],
            Resource.from_contents(document, default_specification=DRAFT202012),
        )
        for document in documents.values()
    ]
    registry = Registry().with_resources(resources)
    result = {}
    for name in SCHEMA_NAMES:
        document = documents[name]
        Draft202012Validator.check_schema(document)
        result[name] = Draft202012Validator(
            document,
            registry=registry,
            format_checker=FormatChecker(),
        )
    return result


def _errors(validator: Draft202012Validator, document: dict) -> list[str]:
    return sorted(error.message for error in validator.iter_errors(document))


def _codes(result: dict | list[dict]) -> list[str]:
    findings = result["findings"] if isinstance(result, dict) else result
    return finding_codes(findings)


def test_closed_schemas_validate_complete_governed_evidence(
    validators: dict[str, Draft202012Validator],
) -> None:
    artifact = _artifact()
    approval = _approval_inputs()
    trace = _trace_inputs()
    documents = {
        "artifact-record.schema.yaml": artifact,
        "artifact-lifecycle-event.schema.yaml": _artifact_event(artifact),
        "approval-decision-policy.schema.yaml": approval["policy"],
        "approval-request.schema.yaml": approval["request"],
        "approval-decision.schema.yaml": approval["decisions"][0],
        "approval-supersession-event.schema.yaml": _supersession(approval["request"]),
        "traceability-edge.schema.yaml": trace["edge"],
    }

    assert {
        name: _errors(validators[name], doc) for name, doc in documents.items()
    } == {name: [] for name in documents}
    for name, document in documents.items():
        extended = deepcopy(document)
        extended["unreviewed_authority"] = True
        assert _errors(validators[name], extended), name


def test_schemas_require_actual_reviewer_and_forbid_trace_authority_grants(
    validators: dict[str, Draft202012Validator],
) -> None:
    approval = _approval_inputs()
    decision = approval["decisions"][0]
    decision.pop("actual_reviewer_principal_ref")
    assert _errors(validators["approval-decision.schema.yaml"], decision)

    edge = _trace_inputs()["edge"]
    edge["authorizes"] = True
    assert _errors(validators["traceability-edge.schema.yaml"], edge)

    unscoped = _trace_inputs()["edge"]
    unscoped["source"].pop("layer_id")
    assert _errors(validators["traceability-edge.schema.yaml"], unscoped)

    role_policy = _approval_inputs()["policy"]
    role_policy["reviewer_selectors"][0]["reviewer_role"] = "manager"
    assert _errors(validators["approval-decision-policy.schema.yaml"], role_policy)

    role_event = _supersession(_approval_inputs()["request"])
    role_event["issuer_role"] = "manager"
    assert _errors(validators["approval-supersession-event.schema.yaml"], role_event)


@pytest.mark.parametrize("stage", ["admission", "approval", "execution"])
def test_artifact_body_digest_and_size_are_reverified_at_every_gate(
    api, stage: str
) -> None:
    body = b"portable artifact body\n"
    artifact = _artifact(body)
    assert api.validate_artifact_body(artifact, body, stage=stage) == []

    drifted = body[:-1] + b"!"
    assert _codes(api.validate_artifact_body(artifact, drifted, stage=stage)) == [
        "HGR-ARTIFACT-DIGEST-MISMATCH"
    ]


def test_artifact_size_missing_body_and_storage_key_have_stable_reasons(api) -> None:
    body = b"portable artifact body\n"
    artifact = _artifact(body)

    wrong_size = deepcopy(artifact)
    wrong_size["byte_size"] += 1
    assert _codes(api.validate_artifact_body(wrong_size, body, stage="admission")) == [
        "HGR-ARTIFACT-SIZE-MISMATCH"
    ]
    assert _codes(api.validate_artifact_body(artifact, None, stage="execution")) == [
        "HGR-ARTIFACT-BODY-MISSING"
    ]

    traversing = deepcopy(artifact)
    traversing["storage_key"] = "../customer-b/artifact"
    assert _codes(api.validate_artifact_record(traversing)) == [
        "HGR-ARTIFACT-STORAGE-KEY"
    ]


def test_artifact_record_and_lifecycle_history_are_append_only(api) -> None:
    artifact = _artifact()
    rewritten = deepcopy(artifact)
    rewritten["media_type"] = "text/plain"
    assert _codes(api.validate_artifact_immutability(artifact, rewritten)) == [
        "HGR-ARTIFACT-IMMUTABLE"
    ]

    event = _artifact_event(artifact)
    changed = deepcopy(event)
    changed["reason"] = "rewritten"
    assert _codes(api.validate_artifact_lifecycle_append_only([event], [changed])) == [
        "HGR-ARTIFACT-LIFECYCLE-IMMUTABLE"
    ]
    assert _codes(api.validate_artifact_lifecycle_append_only([event], [])) == [
        "HGR-ARTIFACT-LIFECYCLE-DELETE"
    ]


def test_artifact_anti_oracle_rejects_before_body_lookup_with_one_response(api) -> None:
    lookups: list[str] = []

    def body_lookup() -> bytes:
        lookups.append("called")
        return b"secret"

    foreign = api.admit_artifact_access(
        _scope("customer-a"), _scope("customer-b"), body_lookup
    )
    absent = api.admit_artifact_access(_scope("customer-a"), None, body_lookup)

    assert (
        foreign
        == absent
        == {
            "allowed": False,
            "status": 404,
            "code": "HGR-ARTIFACT-NOT-AVAILABLE",
            "body": None,
        }
    )
    assert lookups == []


def test_matching_requester_reviewers_policy_and_quorum_authorize(api) -> None:
    inputs = _approval_inputs()
    result = api.evaluate_approval(
        inputs["request"],
        inputs["policy"],
        inputs["decisions"],
        authority_document=inputs["authority"],
        target=inputs["request"]["target"],
        evaluation_time=NOW,
    )
    assert result == {"state": "approved", "authorizes": True, "findings": []}


def test_high_level_evidence_gate_validates_authority_once_before_approval(
    api, monkeypatch
) -> None:
    document, _ = _integrated_approval_document()
    assert (
        validate_authority_document(document["authority_document"], evaluation_time=NOW)
        == []
    )
    calls = []
    validator = api.validate_authority_document

    def counted_validator(authority_document, *, evaluation_time=None):
        calls.append(evaluation_time)
        return validator(authority_document, evaluation_time=evaluation_time)

    monkeypatch.setattr(api, "validate_authority_document", counted_validator)
    assert api.validate_evidence_document(document) == {
        "state": "approved",
        "authorizes": True,
        "findings": [],
    }
    assert calls == [NOW]


def test_unreachable_locally_matching_grant_cannot_pass_high_level_gate(api) -> None:
    document, inputs = _integrated_approval_document()
    manager_grant = next(
        item
        for item in document["authority_document"]["authority_grants"]
        if item["grant_id"] == "grant-manager-a"
    )
    manager_grant["issuer_grant_ref"] = _grant_ref("unreachable-issuer")
    manager_grant["record_digest"] = canonical_record_digest(manager_grant)
    inputs["decisions"][0]["reviewer_grant_ref"] = _exact_grant_ref(manager_grant)

    assert (
        api.evaluate_approval(
            inputs["request"],
            inputs["policy"],
            inputs["decisions"],
            authority_document=document["authority_document"],
            target=inputs["request"]["target"],
            evaluation_time=NOW,
        )["authorizes"]
        is True
    )

    result = api.validate_evidence_document(document)
    assert result["state"] == "invalid"
    assert result["authorizes"] is False
    assert "HGR-GRANT-REFERENCE" in _codes(result)


@pytest.mark.parametrize(
    "operation",
    ["validate_artifact_body", "evaluate_approval", "validate_trace_edge"],
)
def test_high_level_gate_stops_before_every_evidence_dispatch_on_bad_authority(
    api, operation: str
) -> None:
    result = api.validate_evidence_document(
        {
            "operation": operation,
            "evaluation_time": NOW,
            "authority_document": {"evaluation_time": NOW},
            "input": {},
        }
    )
    assert result["state"] == "invalid"
    assert result["authorizes"] is False
    assert _codes(result) == ["HGR-ANCHOR-GENESIS-CARDINALITY"]


def test_requester_and_actual_reviewer_authority_are_distinct_and_exact(api) -> None:
    requester = _approval_inputs()
    requester["request"]["requester_principal_ref"] = _principal_ref(
        "another-requester"
    )
    assert _codes(
        api.evaluate_approval(
            requester["request"],
            requester["policy"],
            requester["decisions"],
            authority_document=requester["authority"],
            target=requester["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-REQUESTER-AUTHORITY"]

    reviewer = _approval_inputs()
    reviewer["decisions"][0]["reviewer_grant_ref"] = _grant_ref("grant-security-a")
    assert _codes(
        api.evaluate_approval(
            reviewer["request"],
            reviewer["policy"],
            reviewer["decisions"],
            authority_document=reviewer["authority"],
            target=reviewer["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-REVIEWER-AUTHORITY"]


def test_requester_and_reviewer_grants_bind_exact_target_digests(api) -> None:
    requester = _approval_inputs()
    requester_grant = next(
        item
        for item in requester["authority"]["authority_grants"]
        if item["grant_id"] == "grant-request-a"
    )
    requester_grant["resource_constraint"]["digest"] = SHA_C
    assert _codes(
        api.evaluate_approval(
            requester["request"],
            requester["policy"],
            requester["decisions"],
            authority_document=requester["authority"],
            target=requester["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-REQUESTER-AUTHORITY"]

    reviewer = _approval_inputs()
    reviewer_grant = next(
        item
        for item in reviewer["authority"]["authority_grants"]
        if item["grant_id"] == "grant-manager-a"
    )
    reviewer_grant["resource_constraint"]["digest"] = SHA_C
    assert _codes(
        api.evaluate_approval(
            reviewer["request"],
            reviewer["policy"],
            reviewer["decisions"],
            authority_document=reviewer["authority"],
            target=reviewer["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-REVIEWER-AUTHORITY"]


def test_reviewer_selector_uses_closed_principal_identity_not_asserted_role(
    api,
) -> None:
    inputs = _approval_inputs()
    request_resource = _approval_resource(inputs["request"], "approval_request")
    unselected = _principal("unselected-reviewer")
    inputs["authority"]["principals"].append(unselected)
    inputs["authority"]["principal_lifecycle_events"].append(
        _activation_projection(unselected)
    )
    inputs["authority"]["authority_grants"].append(
        _grant(
            "grant-unselected-reviewer",
            _principal_ref("unselected-reviewer"),
            action="decide_approval",
            resource_constraint=request_resource,
            digest=SHA_A,
        )
    )
    inputs["decisions"][0]["actual_reviewer_principal_ref"] = _principal_ref(
        "unselected-reviewer"
    )
    inputs["decisions"][0]["reviewer_grant_ref"] = _grant_ref(
        "grant-unselected-reviewer", digest=SHA_A
    )
    assert _codes(
        api.evaluate_approval(
            inputs["request"],
            inputs["policy"],
            inputs["decisions"],
            authority_document=inputs["authority"],
            target=inputs["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-REVIEWER-SELECTOR"]


def test_principal_type_selector_is_neutral_and_authority_bound(api) -> None:
    inputs = _approval_inputs()
    selector = inputs["policy"]["reviewer_selectors"][0]
    selector.pop("principal_ids")
    selector["principal_types"] = ["agent"]
    assert api.evaluate_approval(
        inputs["request"],
        inputs["policy"],
        inputs["decisions"],
        authority_document=inputs["authority"],
        target=inputs["request"]["target"],
        evaluation_time=NOW,
    ) == {"state": "approved", "authorizes": True, "findings": []}


def test_group_principal_selector_is_exact_and_not_membership_inference(api) -> None:
    inputs = _approval_inputs()
    selector = inputs["policy"]["reviewer_selectors"][0]
    selector.pop("principal_ids")
    selector["group_principal_ids"] = ["manager-group"]
    group = _principal("manager-group", principal_type="group", digest=SHA_C)
    inputs["authority"]["principals"].append(group)
    inputs["authority"]["principal_lifecycle_events"].append(
        _activation_projection(group)
    )
    request_resource = _approval_resource(inputs["request"], "approval_request")
    inputs["authority"]["authority_grants"].append(
        _grant(
            "grant-manager-group",
            _principal_ref("manager-group", digest=SHA_C),
            action="decide_approval",
            resource_constraint=request_resource,
            digest=SHA_A,
        )
    )
    inputs["decisions"][0]["actual_reviewer_principal_ref"] = _principal_ref(
        "manager-group", digest=SHA_C
    )
    inputs["decisions"][0]["reviewer_grant_ref"] = _grant_ref(
        "grant-manager-group", digest=SHA_A
    )
    assert api.evaluate_approval(
        inputs["request"],
        inputs["policy"],
        inputs["decisions"],
        authority_document=inputs["authority"],
        target=inputs["request"]["target"],
        evaluation_time=NOW,
    ) == {"state": "approved", "authorizes": True, "findings": []}


@pytest.mark.parametrize(
    ("grant_id", "code"),
    [
        ("grant-request-a", "HGR-APPROVAL-REQUESTER-AUTHORITY"),
        ("grant-manager-a", "HGR-APPROVAL-REVIEWER-AUTHORITY"),
    ],
)
def test_append_only_grant_revocation_invalidates_later_approval_use(
    api, grant_id: str, code: str
) -> None:
    inputs = _approval_inputs()
    grant = next(
        item
        for item in inputs["authority"]["authority_grants"]
        if item["grant_id"] == grant_id
    )
    inputs["authority"]["grant_revocations"].append(
        {
            "grant_ref": _grant_ref(grant_id, digest=grant["record_digest"]),
            "effective_at": NOW,
        }
    )
    assert _codes(
        api.evaluate_approval(
            inputs["request"],
            inputs["policy"],
            inputs["decisions"],
            authority_document=inputs["authority"],
            target=inputs["request"]["target"],
            evaluation_time=NOW,
        )
    ) == [code]


def test_inactive_reviewer_principal_cannot_use_a_locally_matching_grant(api) -> None:
    inputs = _approval_inputs()
    inputs["authority"]["principal_lifecycle_events"] = [
        event
        for event in inputs["authority"]["principal_lifecycle_events"]
        if event["principal_ref"]["principal_id"] != "manager-a"
    ]
    assert _codes(
        api.evaluate_approval(
            inputs["request"],
            inputs["policy"],
            inputs["decisions"],
            authority_document=inputs["authority"],
            target=inputs["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-REVIEWER-AUTHORITY"]


def _approval_resource(record: dict, resource_type: str) -> dict:
    identifier = "request" if resource_type == "approval_request" else "decision"
    return {
        "installation_id": record["owning_scope"]["installation_id"],
        "stack_id": record["owning_scope"]["stack_id"],
        "layer_id": record["owning_scope"]["layer_id"],
        "resource_type": resource_type,
        "resource_id": record[f"{identifier}_id"],
        "digest": record[f"{identifier}_digest"],
    }


def test_policy_and_target_drift_fail_before_aggregation(api) -> None:
    policy_drift = _approval_inputs()
    policy_drift["request"]["decision_policy_digest"] = SHA_A
    assert _codes(
        api.evaluate_approval(
            policy_drift["request"],
            policy_drift["policy"],
            policy_drift["decisions"],
            authority_document=policy_drift["authority"],
            target=policy_drift["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-POLICY-MISMATCH"]

    target_drift = _approval_inputs()
    target = deepcopy(target_drift["request"]["target"])
    target["digest"] = SHA_C
    assert _codes(
        api.evaluate_approval(
            target_drift["request"],
            target_drift["policy"],
            target_drift["decisions"],
            authority_document=target_drift["authority"],
            target=target,
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-TARGET-DRIFT"]


def test_request_cannot_narrow_policy_selectors_and_decisions_must_be_in_window(
    api,
) -> None:
    narrowed = _approval_inputs()
    narrowed["request"]["reviewer_selector_ids"] = ["manager"]
    assert _codes(
        api.evaluate_approval(
            narrowed["request"],
            narrowed["policy"],
            narrowed["decisions"],
            authority_document=narrowed["authority"],
            target=narrowed["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-REVIEWER-SELECTOR"]

    late = _approval_inputs()
    late["decisions"][0]["decided_at"] = LATER
    assert _codes(
        api.evaluate_approval(
            late["request"],
            late["policy"],
            late["decisions"],
            authority_document=late["authority"],
            target=late["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-DECISION-TIME"]


def test_policy_cannot_duplicate_supersession_authority_for_one_event(api) -> None:
    inputs = _approval_inputs()
    inputs["policy"]["supersession_authorities"][1]["event_type"] = "expired"
    assert _codes(
        api.evaluate_approval(
            inputs["request"],
            inputs["policy"],
            inputs["decisions"],
            authority_document=inputs["authority"],
            target=inputs["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-POLICY-SUPERSESSION"]


def test_policy_aggregation_enforces_quorum_and_supports_explicit_minimum(api) -> None:
    insufficient = _approval_inputs()
    insufficient["decisions"] = insufficient["decisions"][:1]
    assert _codes(
        api.evaluate_approval(
            insufficient["request"],
            insufficient["policy"],
            insufficient["decisions"],
            authority_document=insufficient["authority"],
            target=insufficient["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-INSUFFICIENT"]

    minimum = _approval_inputs()
    minimum["policy"]["aggregation"] = "minimum_approvals"
    minimum["policy"]["minimum_approvals"] = 1
    minimum["decisions"] = minimum["decisions"][:1]
    result = api.evaluate_approval(
        minimum["request"],
        minimum["policy"],
        minimum["decisions"],
        authority_document=minimum["authority"],
        target=minimum["request"]["target"],
        evaluation_time=NOW,
    )
    assert result == {"state": "approved", "authorizes": True, "findings": []}


def test_expired_request_is_non_authorizing_without_rewriting_history(api) -> None:
    inputs = _approval_inputs()
    inputs["request"]["expires_at"] = EXPIRED
    result = api.evaluate_approval(
        inputs["request"],
        inputs["policy"],
        inputs["decisions"],
        authority_document=inputs["authority"],
        target=inputs["request"]["target"],
        evaluation_time=NOW,
    )
    assert result["state"] == "expired"
    assert result["authorizes"] is False
    assert _codes(result) == ["HGR-APPROVAL-EXPIRED"]


@pytest.mark.parametrize("event_type", ["expired", "cancelled", "revoked"])
def test_authorized_expiry_cancellation_and_revocation_are_non_authorizing(
    api, event_type: str
) -> None:
    inputs = _approval_inputs()
    result = api.evaluate_approval(
        inputs["request"],
        inputs["policy"],
        inputs["decisions"],
        supersessions=[_supersession(inputs["request"], event_type=event_type)],
        authority_document=inputs["authority"],
        target=inputs["request"]["target"],
        evaluation_time=NOW,
    )
    assert result == {"state": event_type, "authorizes": False, "findings": []}


def test_decision_supersession_removes_only_the_exact_decision(api) -> None:
    inputs = _approval_inputs()
    event = _supersession(inputs["request"], event_type="revoked")
    decision = inputs["decisions"][0]
    decision_resource = {
        "installation_id": decision["owning_scope"]["installation_id"],
        "stack_id": decision["owning_scope"]["stack_id"],
        "layer_id": decision["owning_scope"]["layer_id"],
        "resource_type": "approval_decision",
        "resource_id": decision["decision_id"],
        "digest": decision["decision_digest"],
    }
    inputs["authority"]["authority_grants"].append(
        _grant(
            "grant-manager-supersede-decision",
            _principal_ref("manager-a"),
            action="supersede_approval",
            resource_constraint=decision_resource,
            digest=SHA_A,
        )
    )
    event.update(
        {
            "target_kind": "decision",
            "target_id": decision["decision_id"],
            "target_digest": decision["decision_digest"],
            "issuer_grant_ref": _grant_ref(
                "grant-manager-supersede-decision", digest=SHA_A
            ),
        }
    )
    result = api.evaluate_approval(
        inputs["request"],
        inputs["policy"],
        inputs["decisions"],
        supersessions=[event],
        authority_document=inputs["authority"],
        target=inputs["request"]["target"],
        evaluation_time=NOW,
    )
    assert result["state"] == "pending"
    assert result["authorizes"] is False
    assert _codes(result) == ["HGR-APPROVAL-INSUFFICIENT"]


def test_valid_supersession_cannot_hide_a_later_unauthorized_event(api) -> None:
    inputs = _approval_inputs()
    valid = _supersession(inputs["request"], event_type="cancelled")
    invalid = _supersession(inputs["request"], event_type="revoked")
    invalid["issuer_principal_ref"] = _principal_ref("intruder")
    assert _codes(
        api.evaluate_approval(
            inputs["request"],
            inputs["policy"],
            inputs["decisions"],
            supersessions=[valid, invalid],
            authority_document=inputs["authority"],
            target=inputs["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-SUPERSESSION-AUTHORITY"]


def test_unauthorized_supersession_fails_closed_and_cannot_be_ignored(api) -> None:
    inputs = _approval_inputs()
    event = _supersession(inputs["request"])
    event["issuer_principal_ref"] = _principal_ref("intruder")
    assert _codes(
        api.evaluate_approval(
            inputs["request"],
            inputs["policy"],
            inputs["decisions"],
            supersessions=[event],
            authority_document=inputs["authority"],
            target=inputs["request"]["target"],
            evaluation_time=NOW,
        )
    ) == ["HGR-APPROVAL-SUPERSESSION-AUTHORITY"]


@pytest.mark.parametrize(
    ("conflict_resolution", "state", "code"),
    [
        ("contested", "contested", "HGR-APPROVAL-CONTESTED"),
        ("reject_overrides", "rejected", None),
    ],
)
def test_conflicting_terminal_decisions_follow_only_the_pinned_policy(
    api, conflict_resolution: str, state: str, code: str | None
) -> None:
    inputs = _approval_inputs(conflict_resolution=conflict_resolution)
    inputs["decisions"][1]["decision"] = "reject"
    result = api.evaluate_approval(
        inputs["request"],
        inputs["policy"],
        inputs["decisions"],
        authority_document=inputs["authority"],
        target=inputs["request"]["target"],
        evaluation_time=NOW,
    )
    assert result["state"] == state
    assert result["authorizes"] is False
    assert _codes(result) == ([] if code is None else [code])


def test_approval_records_are_wholly_immutable(api) -> None:
    inputs = _approval_inputs()
    changed = deepcopy(inputs["decisions"][0])
    changed["decision"] = "reject"
    assert _codes(
        api.validate_approval_immutability(inputs["decisions"][0], changed)
    ) == ["HGR-APPROVAL-IMMUTABLE"]


def test_cross_layer_trace_binds_endpoints_operation_binding_and_grants(api) -> None:
    inputs = _trace_inputs()
    assert (
        api.validate_trace_edge(
            inputs["edge"],
            authority_document=inputs["authority"],
            evaluation_time=NOW,
        )
        == []
    )


def test_cross_layer_trace_without_authority_fails_closed(api) -> None:
    inputs = _trace_inputs()
    inputs["edge"].pop("cross_layer_authority")
    assert _codes(
        api.validate_trace_edge(
            inputs["edge"],
            authority_document=inputs["authority"],
            evaluation_time=NOW,
        )
    ) == ["HGR-TRACE-AUTHORITY-REQUIRED"]


def test_trace_endpoint_digest_drift_is_one_primary_reason(api) -> None:
    inputs = _trace_inputs()
    inputs["edge"]["source"]["digest"] = SHA_C
    assert _codes(
        api.validate_trace_edge(
            inputs["edge"],
            authority_document=inputs["authority"],
            evaluation_time=NOW,
        )
    ) == ["HGR-TRACE-ENDPOINT-DIGEST"]


def test_trace_operation_and_binding_mismatches_have_stable_reasons(api) -> None:
    operation = _trace_inputs()
    operation["operations"]["operation-01"]["target_resource"]["digest"] = SHA_C
    assert _codes(
        api.validate_trace_edge(
            operation["edge"],
            authority_document=operation["authority"],
            evaluation_time=NOW,
        )
    ) == ["HGR-TRACE-OPERATION-AUTHORIZATION"]

    binding = _trace_inputs()
    binding["bindings"]["binding-a-b"]["action"] = "another_action"
    assert _codes(
        api.validate_trace_edge(
            binding["edge"],
            authority_document=binding["authority"],
            evaluation_time=NOW,
        )
    ) == ["HGR-TRACE-BINDING"]


def test_trace_grant_refs_require_exact_canonical_documents(api) -> None:
    inputs = _trace_inputs()
    inputs["authority"]["authority_grants"] = [
        item
        for item in inputs["authority"]["authority_grants"]
        if item["grant_id"] != "grant-accept-b"
    ]
    assert _codes(
        api.validate_trace_edge(
            inputs["edge"],
            authority_document=inputs["authority"],
            evaluation_time=NOW,
        )
    ) == ["HGR-TRACE-GRANT"]


def test_same_layer_trace_cannot_claim_unrelated_cross_layer_authority(api) -> None:
    inputs = _trace_inputs(same_layer=True)
    assert _codes(
        api.validate_trace_edge(
            inputs["edge"],
            authority_document=inputs["authority"],
            evaluation_time=NOW,
        )
    ) == ["HGR-TRACE-UNRELATED-AUTHORITY"]


def test_trace_edges_are_append_only_and_never_authority(api) -> None:
    edge = _trace_inputs()["edge"]
    changed = deepcopy(edge)
    changed["relation"] = "rewritten"
    assert _codes(api.validate_trace_immutability(edge, changed)) == [
        "HGR-TRACE-IMMUTABLE"
    ]


def _migration_validators() -> (
    tuple[Draft202012Validator, Draft202012Validator, Draft202012Validator]
):
    documents = [
        load_yaml_document(CONTRACT_ROOT / name)
        for name in (
            "migrations/v1-to-v2-mapping.schema.yaml",
            "legacy-quarantine-record.schema.yaml",
            "shared-definitions.schema.yaml",
        )
    ]
    registry = Registry().with_resources(
        (
            document["$id"],
            Resource.from_contents(document, default_specification=DRAFT202012),
        )
        for document in documents
    )
    mapping_schema, quarantine_schema, _ = documents
    for schema in (mapping_schema, quarantine_schema):
        Draft202012Validator.check_schema(schema)

    def _validator(target: dict | str) -> Draft202012Validator:
        schema = target if isinstance(target, dict) else {"$ref": target}
        return Draft202012Validator(
            schema, registry=registry, format_checker=FormatChecker()
        )

    return (
        _validator(mapping_schema),
        _validator(mapping_schema["$id"] + "#/$defs/authority_envelope"),
        _validator(quarantine_schema),
    )


def _assert_migration_mapping_case(
    fixture: dict,
    path: Path,
    mapping_validator: Draft202012Validator,
    envelope_validator: Draft202012Validator,
) -> None:
    payload = fixture["mapping_payload"]
    assert not _errors(mapping_validator, payload), path
    if fixture["expected"]["outcome"] == "pass":
        migration.validate_mapping_payload(payload)
        envelope = fixture["authority_envelope"]
        assert not _errors(envelope_validator, envelope), path
        migration.validate_authority_envelope(envelope, payload=payload)
    else:
        with pytest.raises(migration.MigrationContractError) as excinfo:
            migration.validate_mapping_payload(payload)
        assert excinfo.value.code == fixture["expected"]["primary_finding_code"], path


def _assert_migration_quarantine_case(
    fixture: dict, path: Path, quarantine_validator: Draft202012Validator
) -> None:
    record = fixture["quarantine_record"]
    if fixture["expected"]["outcome"] == "pass":
        assert not _errors(quarantine_validator, record), path
    else:
        # The closed record contract must reject the promotion /
        # authoritative-dependency fields — and only those fields.
        assert _errors(quarantine_validator, record), path
        assert QUARANTINE_DEPENDENCY_FIELDS <= set(record), path
        trimmed = {
            key: value
            for key, value in record.items()
            if key not in QUARANTINE_DEPENDENCY_FIELDS
        }
        assert not _errors(quarantine_validator, trimmed), path


def test_portable_fixture_matrix_is_self_describing_and_reason_specific() -> None:
    proven_primary_codes = {
        "HGR-ARTIFACT-IMMUTABLE",
        "HGR-ARTIFACT-DIGEST-MISMATCH",
        "HGR-ARTIFACT-SIZE-MISMATCH",
        "HGR-ARTIFACT-STORAGE-KEY",
        "HGR-ARTIFACT-NOT-AVAILABLE",
        "HGR-APPROVAL-REQUESTER-AUTHORITY",
        "HGR-APPROVAL-REVIEWER-AUTHORITY",
        "HGR-APPROVAL-REVIEWER-SELECTOR",
        "HGR-GRANT-REFERENCE",
        "HGR-APPROVAL-POLICY-MISMATCH",
        "HGR-APPROVAL-POLICY-SUPERSESSION",
        "HGR-APPROVAL-TARGET-DRIFT",
        "HGR-APPROVAL-IMMUTABLE",
        "HGR-APPROVAL-SUPERSESSION-AUTHORITY",
        "HGR-APPROVAL-CONTESTED",
        "HGR-TRACE-AUTHORITY-REQUIRED",
        "HGR-TRACE-ENDPOINT-DIGEST",
        "HGR-TRACE-UNRELATED-AUTHORITY",
    }
    counts = {}
    fixtures = []
    for group in ("artifacts", "approvals", "traceability"):
        paths = sorted((FIXTURE_ROOT / group).glob("*.yaml"))
        counts[group] = len(paths)
        for path in paths:
            fixture = load_yaml_document(path)
            fixtures.append(fixture)
            assert (
                fixture["kind"]
                == "openxfactory-hermes-runtime-portable-evidence-fixture"
            )
            assert fixture["case_id"]
            assert fixture["requirement_ids"]
            assert fixture["scenario_ids"]
            assert fixture["evaluation_time"] == NOW
            expected = fixture["expected"]
            assert expected["outcome"] in {"pass", "fail"}
            if expected["outcome"] == "fail":
                assert "mutation" in fixture or "input" in fixture
                assert expected["primary_finding_code"].startswith("HGR-")
                assert expected["primary_finding_code"] in proven_primary_codes
                assert expected.get("allowed_secondary_codes", []) == []
            if fixture["case_id"] == "approval-authority-chain-valid":
                assert (
                    validate_authority_document(
                        fixture["document"]["authority_document"],
                        evaluation_time=fixture["evaluation_time"],
                    )
                    == []
                )
    mapping_validator, envelope_validator, quarantine_validator = (
        _migration_validators()
    )
    migration_paths = sorted((FIXTURE_ROOT / "migration").glob("*.yaml"))
    counts["migration"] = len(migration_paths)
    for path in migration_paths:
        fixture = load_yaml_document(path)
        fixtures.append(fixture)
        assert fixture["kind"] == MIGRATION_FIXTURE_KIND, path
        assert fixture["case_id"], path
        assert fixture["requirement_ids"], path
        assert fixture["scenario_ids"], path
        assert fixture["evaluation_time"] == MIGRATION_NOW, path
        expected = fixture["expected"]
        assert expected["outcome"] in {"pass", "fail"}, path
        if expected["outcome"] == "fail":
            assert expected["primary_finding_code"] == (
                MIGRATION_PRIMARY_CODES[fixture["case_id"]]
            ), path
            assert expected.get("allowed_secondary_codes", []) == [], path
        if "mapping_payload" in fixture:
            _assert_migration_mapping_case(
                fixture, path, mapping_validator, envelope_validator
            )
        else:
            _assert_migration_quarantine_case(fixture, path, quarantine_validator)
    assert counts == {
        "artifacts": 6,
        "approvals": 15,
        "traceability": 4,
        "migration": 4,
    }
    case_ids = {fixture["case_id"] for fixture in fixtures}
    assert len(case_ids) == len(fixtures)
    for fixture in fixtures:
        if "base_case_id" in fixture:
            assert fixture["base_case_id"] in case_ids
