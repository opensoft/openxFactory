"""Portable contracts for immutable authority, isolation bindings, and G0 work."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from scripts.hermes_runtime_validation.loader import load_yaml_document
from scripts.hermes_runtime_validation.semantics import authority
from tests.hermes_runtime_contracts.support import finding_codes

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_ROOT = REPO_ROOT / "contracts/hermes-runtime"
FIXTURE_ROOT = CONTRACT_ROOT / "fixtures"

SHA_A = "sha256:" + "a" * 64
SHA_B = "sha256:" + "b" * 64
SHA_C = "sha256:" + "c" * 64
COMMIT = "d" * 40
EVALUATION_TIME = "2026-07-12T12:30:00Z"

AUTHORITY_SCHEMAS = (
    "principal.schema.yaml",
    "principal-lifecycle-event.schema.yaml",
    "database-principal-binding.schema.yaml",
    "database-principal-binding-revocation.schema.yaml",
    "installation-trust-anchor.schema.yaml",
    "installation-trust-anchor-event.schema.yaml",
    "authority-grant.schema.yaml",
    "authority-grant-revocation.schema.yaml",
    "cross-layer-binding.schema.yaml",
    "cross-layer-binding-revocation.schema.yaml",
    "operation-authorization.schema.yaml",
)

AUTHORITY_FIXTURES = (
    "authority/active-authority.yaml",
    "authority/grant-self-issued.yaml",
    "authority/grant-cycle.yaml",
    "authority/grant-scope-widening.yaml",
    "authority/grant-revoked.yaml",
    "authority/anchor-rotation-as-of.yaml",
    "authority/anchor-rotation-unauthorized.yaml",
    "authority/binding-reversed.yaml",
    "authority/binding-transitive.yaml",
    "authority/binding-source-swapped.yaml",
    "authority/binding-revoked.yaml",
    "authority/operation-evidence-drift.yaml",
    "isolation/database-session-user-conflict.yaml",
    "isolation/database-binding-revoked.yaml",
    "isolation/assume-scope-grant-revoked.yaml",
)

EXACT_AUTHORITY_ACTIONS = {
    "assume_scope",
    "issue_grant",
    "revoke_grant",
    "rotate_trust_anchor",
    "revoke_trust_anchor",
    "create_binding",
    "revoke_binding",
    "accept_cross_layer",
    "project_resource",
    "create_artifact",
    "request_approval",
    "decide_approval",
    "supersede_approval",
    "transition_lifecycle",
    "run_migration",
    "publish_contract",
}


def _pin(path: str) -> dict:
    return {
        "repository": "opensoft/exampleFactory",
        "commit": COMMIT,
        "path": path,
        "digest": SHA_A,
    }


def _scope(layer_id: str | None = None) -> dict:
    if layer_id is None:
        return {"scope_kind": "installation", "installation_id": "install-01"}
    return {
        "scope_kind": "layer",
        "installation_id": "install-01",
        "stack_id": "stack-01",
        "layer_id": layer_id,
    }


def _resource(
    resource_id: str,
    *,
    layer_id: str | None = None,
    digest: str | None = SHA_A,
    resource_type: str = "artifact",
) -> dict:
    result = {"installation_id": "install-01"}
    if layer_id is not None:
        result.update({"stack_id": "stack-01", "layer_id": layer_id})
    result.update({"resource_type": resource_type, "resource_id": resource_id})
    if digest is not None:
        result["digest"] = digest
    return result


def _finalize(record: dict) -> dict:
    record["record_digest_profile"] = authority.RECORD_DIGEST_PROFILE
    record["record_digest"] = authority.canonical_record_digest(record)
    return record


def _principal(principal_id: str, principal_type: str, scope: dict) -> dict:
    return _finalize(
        {
            "schema_version": 1,
            "kind": "openxfactory-principal",
            "principal_id": principal_id,
            "principal_type": principal_type,
            "scope": deepcopy(scope),
            "initial_lifecycle_state": "provisioning",
            "created_at": "2026-07-12T11:45:00Z",
        }
    )


def _principal_ref(principal: dict) -> dict:
    return {
        "scope": deepcopy(principal["scope"]),
        "principal_id": principal["principal_id"],
        "record_digest": principal["record_digest"],
    }


def _anchor_ref(anchor: dict) -> dict:
    return {
        "installation_id": anchor["installation_id"],
        "anchor_id": anchor["anchor_id"],
        "record_digest": anchor["record_digest"],
    }


def _grant_ref(grant: dict) -> dict:
    return {
        "installation_id": grant["installation_id"],
        "grant_id": grant["grant_id"],
        "record_digest": grant["record_digest"],
    }


def _binding_ref(binding: dict) -> dict:
    return {
        "installation_id": binding["source_scope"]["installation_id"],
        "binding_id": binding["binding_id"],
        "record_digest": binding["record_digest"],
    }


def _database_binding_ref(binding: dict) -> dict:
    return {
        "installation_id": binding["scope"]["installation_id"],
        "binding_id": binding["binding_id"],
        "record_digest": binding["record_digest"],
    }


def _root_grant(grant_id: str, action: str, principal: dict, anchor: dict) -> dict:
    return _finalize(
        {
            "schema_version": 1,
            "kind": "openxfactory-authority-grant",
            "grant_id": grant_id,
            "installation_id": "install-01",
            "grant_kind": "root",
            "principal_ref": _principal_ref(principal),
            "scope": _scope(),
            "action": action,
            "resource_constraint": _resource(
                "installation-authority-policy",
                digest=SHA_A,
                resource_type="policy",
            ),
            "policy_pin": _pin("policies/installation-authority.yaml"),
            "root_anchor_ref": _anchor_ref(anchor),
            "starts_at": "2026-07-12T11:50:00Z",
            "issued_at": "2026-07-12T11:55:00Z",
        }
    )


def _delegated_grant(
    grant_id: str,
    action: str,
    principal: dict,
    scope: dict,
    resource_constraint: dict,
    issuer: dict,
    *,
    issued_at: str = "2026-07-12T12:01:00Z",
) -> dict:
    return _finalize(
        {
            "schema_version": 1,
            "kind": "openxfactory-authority-grant",
            "grant_id": grant_id,
            "installation_id": "install-01",
            "grant_kind": "delegated",
            "principal_ref": _principal_ref(principal),
            "scope": deepcopy(scope),
            "action": action,
            "resource_constraint": deepcopy(resource_constraint),
            "policy_pin": _pin("policies/delegated-authority.yaml"),
            "issuer_grant_ref": _grant_ref(issuer),
            "starts_at": "2026-07-12T12:00:00Z",
            "expires_at": "2026-07-13T00:00:00Z",
            "issued_at": issued_at,
        }
    )


def _activation_event(principal: dict, grant: dict, suffix: str) -> dict:
    return _finalize(
        {
            "schema_version": 1,
            "kind": "openxfactory-principal-lifecycle-event",
            "event_id": f"principal-{suffix}-active",
            "principal_ref": _principal_ref(principal),
            "predecessor_ref": {
                "kind": "registration",
                "id": principal["principal_id"],
                "record_digest": principal["record_digest"],
            },
            "from_state": "provisioning",
            "to_state": "active",
            "authorizing_grant_ref": _grant_ref(grant),
            "occurred_at": "2026-07-12T12:02:00Z",
            "reason": "activate governed pilot principal",
        }
    )


def _base_document() -> dict:
    installation_scope = _scope()
    source_scope = _scope("customer-a")
    target_scope = _scope("domain-01")
    root = _principal("root-authority", "group", installation_scope)
    source = _principal("customer-a-worker", "service", source_scope)
    target = _principal("domain-reviewer", "agent", target_scope)
    principals = [root, source, target]

    anchor = _finalize(
        {
            "schema_version": 1,
            "kind": "openxfactory-installation-trust-anchor",
            "anchor_id": "anchor-genesis",
            "installation_id": "install-01",
            "anchor_kind": "genesis",
            "principal_ref": _principal_ref(root),
            "key_ref": {
                "provider": "installation-kms",
                "key_id": "anchor-genesis-key",
                "algorithm": "ed25519",
            },
            "policy_pin": _pin("policies/trust-anchor.yaml"),
            "effective_at": "2026-07-12T11:50:00Z",
            "authorized_evidence_digest": SHA_A,
            "created_at": "2026-07-12T11:50:00Z",
        }
    )

    root_issue = _root_grant("root-issue-grant", "issue_grant", root, anchor)
    root_rotate = _root_grant("root-rotate-anchor", "rotate_trust_anchor", root, anchor)
    root_revoke_anchor = _root_grant(
        "root-revoke-anchor", "revoke_trust_anchor", root, anchor
    )
    root_revoke_grant = _root_grant("root-revoke-grant", "revoke_grant", root, anchor)
    root_transition = _root_grant(
        "root-transition-lifecycle", "transition_lifecycle", root, anchor
    )

    source_identity = _resource(
        "customer-a-policy",
        layer_id="customer-a",
        digest=None,
        resource_type="policy_namespace",
    )
    target_identity = _resource(
        "domain-policy",
        layer_id="domain-01",
        digest=None,
        resource_type="policy_namespace",
    )
    source_resource = _resource(
        "artifact-source-v1", layer_id="customer-a", digest=SHA_A
    )
    target_resource = _resource(
        "artifact-target-draft-v1", layer_id="domain-01", digest=SHA_B
    )

    source_issuer = _delegated_grant(
        "source-issue-grant",
        "issue_grant",
        source,
        source_scope,
        source_identity,
        root_issue,
    )
    target_issuer = _delegated_grant(
        "target-issue-grant",
        "issue_grant",
        target,
        target_scope,
        target_identity,
        root_issue,
    )
    source_project = _delegated_grant(
        "source-project-resource",
        "project_resource",
        source,
        source_scope,
        source_resource,
        source_issuer,
    )
    source_binding = _delegated_grant(
        "source-create-binding",
        "create_binding",
        source,
        source_scope,
        source_resource,
        source_issuer,
    )
    source_revoke_binding = _delegated_grant(
        "source-revoke-binding",
        "revoke_binding",
        source,
        source_scope,
        source_resource,
        source_issuer,
    )
    source_assume = _delegated_grant(
        "source-assume-scope",
        "assume_scope",
        source,
        source_scope,
        source_identity,
        source_issuer,
    )
    target_accept = _delegated_grant(
        "target-accept-cross-layer",
        "accept_cross_layer",
        target,
        target_scope,
        target_resource,
        target_issuer,
    )

    grants = [
        root_issue,
        root_rotate,
        root_revoke_anchor,
        root_revoke_grant,
        root_transition,
        source_issuer,
        target_issuer,
        source_project,
        source_binding,
        source_revoke_binding,
        source_assume,
        target_accept,
    ]

    lifecycle_events = [
        _activation_event(root, root_transition, "root"),
        _activation_event(source, root_transition, "source"),
        _activation_event(target, root_transition, "target"),
    ]
    database_binding = _finalize(
        {
            "schema_version": 1,
            "kind": "openxfactory-database-principal-binding",
            "binding_id": "db-bind-customer-a",
            "scope": deepcopy(source_scope),
            "session_user": "hgr_customer_a_runtime",
            "role_class": "runtime",
            "principal_ref": _principal_ref(source),
            "creator_grant_ref": _grant_ref(source_assume),
            "bound_at": "2026-07-12T12:03:00Z",
        }
    )
    binding = _finalize(
        {
            "schema_version": 1,
            "kind": "openxfactory-cross-layer-binding",
            "binding_id": "binding-customer-a-to-domain",
            "source_scope": deepcopy(source_scope),
            "target_scope": deepcopy(target_scope),
            "source_resource": deepcopy(source_resource),
            "target_resource": deepcopy(target_resource),
            "action": "project_resource",
            "purpose": "diagnostic-projection",
            "creator_principal_ref": _principal_ref(source),
            "creator_grant_ref": _grant_ref(source_binding),
            "target_acceptance_principal_ref": _principal_ref(target),
            "target_acceptance_grant_ref": _grant_ref(target_accept),
            "starts_at": "2026-07-12T12:05:00Z",
            "expires_at": "2026-07-13T00:00:00Z",
            "created_at": "2026-07-12T12:05:00Z",
        }
    )
    operation = _finalize(
        {
            "schema_version": 1,
            "kind": "openxfactory-operation-authorization",
            "operation_id": "operation-diagnostic-projection",
            "source_scope": deepcopy(source_scope),
            "target_scope": deepcopy(target_scope),
            "source_resource": deepcopy(source_resource),
            "target_resource": deepcopy(target_resource),
            "action": "project_resource",
            "purpose": "diagnostic-projection",
            "actor_principal_ref": _principal_ref(source),
            "source_grant_ref": _grant_ref(source_project),
            "target_acceptance_grant_ref": _grant_ref(target_accept),
            "binding_ref": _binding_ref(binding),
            "anchor_ref": _anchor_ref(anchor),
            "authorized_at": "2026-07-12T12:10:00Z",
            "target_result": deepcopy(target_resource),
            "transaction_id": "tx-diagnostic-projection",
        }
    )
    return {
        "evaluation_time": EVALUATION_TIME,
        "principals": principals,
        "principal_lifecycle_events": lifecycle_events,
        "database_principal_bindings": [database_binding],
        "database_principal_binding_revocations": [],
        "trust_anchors": [anchor],
        "trust_anchor_events": [],
        "authority_grants": grants,
        "grant_revocations": [],
        "cross_layer_bindings": [binding],
        "binding_revocations": [],
        "operation_authorizations": [operation],
        "resources": [
            {
                "resource_ref": deepcopy(target_resource),
                "immutable": True,
                "lifecycle_state": "draft",
            }
        ],
    }


def _by_id(document: dict, collection: str, field: str, identifier: str) -> dict:
    return next(item for item in document[collection] if item[field] == identifier)


def _add_rotation(document: dict, *, authorized: bool) -> None:
    root = _by_id(document, "principals", "principal_id", "root-authority")
    genesis = document["trust_anchors"][0]
    rotated = _finalize(
        {
            "schema_version": 1,
            "kind": "openxfactory-installation-trust-anchor",
            "anchor_id": "anchor-rotated-01",
            "installation_id": "install-01",
            "anchor_kind": "rotated",
            "principal_ref": _principal_ref(root),
            "key_ref": {
                "provider": "installation-kms",
                "key_id": "anchor-rotated-key",
                "algorithm": "ed25519",
            },
            "policy_pin": _pin("policies/trust-anchor.yaml"),
            "effective_at": "2026-07-12T12:20:00Z",
            "authorized_evidence_digest": SHA_B,
            "created_at": "2026-07-12T12:19:00Z",
        }
    )
    grant_id = "root-rotate-anchor" if authorized else "root-issue-grant"
    grant = _by_id(document, "authority_grants", "grant_id", grant_id)
    event = _finalize(
        {
            "schema_version": 1,
            "kind": "openxfactory-installation-trust-anchor-event",
            "event_id": "anchor-rotation-01",
            "installation_id": "install-01",
            "predecessor_ref": {
                "kind": "registration",
                "id": genesis["anchor_id"],
                "record_digest": genesis["record_digest"],
            },
            "event_type": "rotate",
            "predecessor_anchor_ref": _anchor_ref(genesis),
            "successor_anchor_ref": _anchor_ref(rotated),
            "authorizing_principal_ref": _principal_ref(root),
            "authorizing_grant_ref": _grant_ref(grant),
            "effective_at": "2026-07-12T12:20:00Z",
            "occurred_at": "2026-07-12T12:20:00Z",
            "reason": "rotate installation trust root",
        }
    )
    document["trust_anchors"].append(rotated)
    document["trust_anchor_events"].append(event)


def _add_grant_revocation(
    document: dict, target_grant_id: str = "source-project-resource"
) -> None:
    root = _by_id(document, "principals", "principal_id", "root-authority")
    issuer = _by_id(document, "authority_grants", "grant_id", "root-revoke-grant")
    target = _by_id(document, "authority_grants", "grant_id", target_grant_id)
    document["grant_revocations"].append(
        _finalize(
            {
                "schema_version": 1,
                "kind": "openxfactory-authority-grant-revocation",
                "revocation_id": f"revoke-{target_grant_id}",
                "installation_id": "install-01",
                "grant_ref": _grant_ref(target),
                "issuer_principal_ref": _principal_ref(root),
                "issuer_grant_ref": _grant_ref(issuer),
                "effective_at": "2026-07-12T12:15:00Z",
                "reason": "end exact projection authority",
            }
        )
    )


def _add_binding_revocation(document: dict) -> None:
    binding = document["cross_layer_bindings"][0]
    source = _by_id(document, "principals", "principal_id", "customer-a-worker")
    target = _by_id(document, "principals", "principal_id", "domain-reviewer")
    source_grant = _by_id(
        document, "authority_grants", "grant_id", "source-revoke-binding"
    )
    target_grant = _by_id(
        document, "authority_grants", "grant_id", "target-accept-cross-layer"
    )
    document["binding_revocations"].append(
        _finalize(
            {
                "schema_version": 1,
                "kind": "openxfactory-cross-layer-binding-revocation",
                "revocation_id": "revoke-customer-a-to-domain",
                "binding_ref": _binding_ref(binding),
                "source_principal_ref": _principal_ref(source),
                "source_grant_ref": _grant_ref(source_grant),
                "target_acceptance_principal_ref": _principal_ref(target),
                "target_acceptance_grant_ref": _grant_ref(target_grant),
                "effective_at": "2026-07-12T12:15:00Z",
                "reason": "target withdraws exact projection acceptance",
            }
        )
    )


def _add_database_revocation(document: dict) -> None:
    binding = document["database_principal_bindings"][0]
    root = _by_id(document, "principals", "principal_id", "root-authority")
    grant = _by_id(document, "authority_grants", "grant_id", "root-revoke-grant")
    document["database_principal_binding_revocations"].append(
        _finalize(
            {
                "schema_version": 1,
                "kind": "openxfactory-database-principal-binding-revocation",
                "revocation_id": "revoke-db-customer-a",
                "scope": deepcopy(binding["scope"]),
                "binding_ref": _database_binding_ref(binding),
                "issuer_principal_ref": _principal_ref(root),
                "issuer_grant_ref": _grant_ref(grant),
                "effective_at": "2026-07-12T12:15:00Z",
                "reason": "retire authenticated database binding",
            }
        )
    )


def _set_principal_state_as_of(
    document: dict,
    principal_id: str,
    state: str,
    *,
    occurred_at: str = "2026-07-12T12:08:00Z",
) -> None:
    activation = next(
        event
        for event in document["principal_lifecycle_events"]
        if event["principal_ref"]["principal_id"] == principal_id
    )
    if state == "provisioning":
        document["principal_lifecycle_events"].remove(activation)
        return
    principal = _by_id(document, "principals", "principal_id", principal_id)
    grant = _by_id(
        document,
        "authority_grants",
        "grant_id",
        "root-transition-lifecycle",
    )
    document["principal_lifecycle_events"].append(
        _finalize(
            {
                "schema_version": 1,
                "kind": "openxfactory-principal-lifecycle-event",
                "event_id": f"principal-{principal_id}-{state}",
                "principal_ref": _principal_ref(principal),
                "predecessor_ref": {
                    "kind": "event",
                    "id": activation["event_id"],
                    "record_digest": activation["record_digest"],
                },
                "from_state": "active",
                "to_state": state,
                "authorizing_grant_ref": _grant_ref(grant),
                "occurred_at": occurred_at,
                "reason": f"move governed principal to {state}",
            }
        )
    )


def _fixture_findings(fixture: dict) -> list[dict]:
    document = _base_document()
    scenario = fixture["scenario"]
    evaluation_time = fixture["evaluation_time"]
    operation = document["operation_authorizations"][0]
    if scenario == "active_authority":
        return authority.validate_authority_document(document)
    if scenario == "grant_self_issued":
        grant = _by_id(
            document, "authority_grants", "grant_id", "source-project-resource"
        )
        grant["issuer_grant_ref"] = _grant_ref(grant)
        return authority.validate_grant_authority(
            grant["grant_id"], document, evaluation_time=evaluation_time
        )
    if scenario == "grant_cycle":
        source = _by_id(document, "authority_grants", "grant_id", "source-issue-grant")
        target = _by_id(document, "authority_grants", "grant_id", "target-issue-grant")
        source["issuer_grant_ref"] = _grant_ref(target)
        target["issuer_grant_ref"] = _grant_ref(source)
        return authority.validate_grant_authority(
            source["grant_id"], document, evaluation_time=evaluation_time
        )
    if scenario == "grant_scope_widening":
        grant = _by_id(
            document, "authority_grants", "grant_id", "source-project-resource"
        )
        grant["scope"] = _scope()
        return authority.validate_grant_authority(
            grant["grant_id"], document, evaluation_time=evaluation_time
        )
    if scenario == "grant_revoked":
        _add_grant_revocation(document)
        return authority.validate_grant_authority(
            "source-project-resource", document, evaluation_time=evaluation_time
        )
    if scenario == "anchor_rotation_as_of":
        _add_rotation(document, authorized=True)
        root = _by_id(document, "principals", "principal_id", "root-authority")
        rotated = _by_id(document, "trust_anchors", "anchor_id", "anchor-rotated-01")
        new_root = _root_grant(
            "rotated-root-publish", "publish_contract", root, rotated
        )
        new_root["starts_at"] = "2026-07-12T12:20:00Z"
        new_root["issued_at"] = "2026-07-12T12:21:00Z"
        _finalize(new_root)
        document["authority_grants"].append(new_root)
        historical = authority.validate_operation_authorization(operation, document)
        current = authority.validate_grant_authority(
            "source-project-resource", document, evaluation_time=evaluation_time
        )
        new_current = authority.validate_grant_authority(
            "rotated-root-publish", document, evaluation_time=evaluation_time
        )
        if (
            historical == []
            and finding_codes(current) == ["HGR-GRANT-ANCHOR"]
            and new_current == []
        ):
            return []
        return historical + current + new_current
    if scenario == "anchor_rotation_unauthorized":
        _add_rotation(document, authorized=False)
        return authority.validate_authority_document(document)
    if scenario == "binding_reversed":
        operation["source_scope"], operation["target_scope"] = (
            operation["target_scope"],
            operation["source_scope"],
        )
        operation["source_resource"], operation["target_resource"] = (
            operation["target_resource"],
            operation["source_resource"],
        )
        return authority.validate_operation_authorization(operation, document)
    if scenario == "binding_transitive":
        operation["binding_ref"] = {
            "installation_id": "install-01",
            "binding_id": "binding-customer-a-to-client-via-domain",
            "record_digest": SHA_C,
        }
        return authority.validate_operation_authorization(operation, document)
    if scenario == "binding_source_swapped":
        operation["source_resource"] = _resource(
            "artifact-source-v2", layer_id="customer-a", digest=SHA_C
        )
        return authority.validate_operation_authorization(operation, document)
    if scenario == "binding_revoked":
        _add_binding_revocation(document)
        operation["authorized_at"] = evaluation_time
        return authority.validate_operation_authorization(operation, document)
    if scenario == "operation_evidence_drift":
        operation["target_result"] = _resource(
            "artifact-target-draft-v1", layer_id="domain-01", digest=SHA_C
        )
        return authority.validate_operation_authorization(operation, document)
    if scenario == "database_session_user_conflict":
        duplicate = deepcopy(document["database_principal_bindings"][0])
        duplicate["binding_id"] = "db-bind-customer-a-duplicate"
        _finalize(duplicate)
        document["database_principal_bindings"].append(duplicate)
        return authority.validate_authority_document(document)
    if scenario == "database_binding_revoked":
        _add_database_revocation(document)
        return authority.validate_database_principal_binding(
            "hgr_customer_a_runtime",
            _scope("customer-a"),
            document,
            evaluation_time=evaluation_time,
        )
    if scenario == "assume_scope_grant_revoked":
        _add_grant_revocation(document, "source-assume-scope")
        return authority.validate_database_principal_binding(
            "hgr_customer_a_runtime",
            _scope("customer-a"),
            document,
            evaluation_time=evaluation_time,
        )
    raise AssertionError(f"unknown authority fixture scenario {scenario!r}")


def _offline_registry() -> tuple[Registry, dict[str, dict]]:
    paths = ("shared-definitions.schema.yaml", *AUTHORITY_SCHEMAS)
    documents = {name: load_yaml_document(CONTRACT_ROOT / name) for name in paths}
    resources = [
        (
            document["$id"],
            Resource.from_contents(document, default_specification=DRAFT202012),
        )
        for document in documents.values()
    ]
    return Registry().with_resources(resources), documents


def test_authority_schema_family_compiles_in_closed_offline_registry() -> None:
    assert len(AUTHORITY_SCHEMAS) == 11
    registry, documents = _offline_registry()
    for name in AUTHORITY_SCHEMAS:
        Draft202012Validator.check_schema(documents[name])
        Draft202012Validator(
            documents[name], registry=registry, format_checker=FormatChecker()
        )


def test_active_authority_records_validate_against_all_eleven_schemas() -> None:
    registry, documents = _offline_registry()
    document = _base_document()
    schema_by_kind = {
        documents[name]["properties"]["kind"]["const"]: documents[name]
        for name in AUTHORITY_SCHEMAS
    }
    records = [
        record
        for collection in authority._COLLECTION_IDS
        for record in document[collection]
    ]
    kinds_seen = {record["kind"] for record in records}
    # Add one structurally valid instance for schema kinds not needed by the
    # active path through the reason-specific helpers.
    _add_database_revocation(document)
    _add_grant_revocation(document)
    _add_binding_revocation(document)
    _add_rotation(document, authorized=True)
    records = [
        record
        for collection in authority._COLLECTION_IDS
        for record in document[collection]
    ]
    kinds_seen = {record["kind"] for record in records}
    assert kinds_seen == set(schema_by_kind)
    for record in records:
        errors = list(
            Draft202012Validator(
                schema_by_kind[record["kind"]],
                registry=registry,
                format_checker=FormatChecker(),
            ).iter_errors(record)
        )
        assert errors == [], f"{record['kind']}: {[error.message for error in errors]}"


def test_exact_action_vocabulary_has_no_wildcard_or_domain_escape() -> None:
    shared = load_yaml_document(CONTRACT_ROOT / "shared-definitions.schema.yaml")
    assert set(shared["$defs"]["authority_action"]["enum"]) == EXACT_AUTHORITY_ACTIONS
    assert "*" not in EXACT_AUTHORITY_ACTIONS
    assert all(
        "project_alfa" not in action and "patient" not in action
        for action in EXACT_AUTHORITY_ACTIONS
    )


def test_canonical_digest_profile_is_semantic_and_rejects_floats() -> None:
    record = {"z": [True, None, {"nested": "value"}], "a": 1, "record_digest": SHA_A}
    expected_bytes = json.dumps(
        {"a": 1, "z": [True, None, {"nested": "value"}]},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    assert (
        authority.canonical_record_digest(record)
        == "sha256:" + hashlib.sha256(expected_bytes).hexdigest()
    )
    reordered = {"record_digest": SHA_B, "a": 1, "z": [True, None, {"nested": "value"}]}
    assert authority.canonical_record_digest(
        reordered
    ) == authority.canonical_record_digest(record)
    nested_changed = deepcopy(record)
    nested_changed["z"][2]["record_digest"] = SHA_B
    assert authority.canonical_record_digest(
        nested_changed
    ) != authority.canonical_record_digest(record)
    with pytest.raises(ValueError, match="floating-point"):
        authority.canonical_record_digest({"value": 1.0})
    with pytest.raises(ValueError, match="not a JSON value"):
        authority.canonical_record_digest({"value": {"not-json"}})


def test_self_describing_authority_fixture_matrix_has_exact_counts_and_reasons() -> (
    None
):
    assert len(AUTHORITY_FIXTURES) == 15
    missing = [
        path for path in AUTHORITY_FIXTURES if not (FIXTURE_ROOT / path).is_file()
    ]
    assert missing == []
    case_ids: set[str] = set()
    for relative in AUTHORITY_FIXTURES:
        fixture = load_yaml_document(FIXTURE_ROOT / relative)
        assert fixture["kind"] == "openxfactory-authority-fixture"
        assert fixture["case_id"] not in case_ids
        case_ids.add(fixture["case_id"])
        assert fixture["phase"] == "semantic"
        assert fixture["class"] in {"valid", "invalid"}
        assert fixture["requirement_ids"]
        assert fixture["scenario_ids"]
        assert fixture["scenario"]
        assert fixture["operation"]
        assert fixture["evaluation_time"].endswith("Z")
        expected = fixture["expected"]
        findings = _fixture_findings(fixture)
        codes = finding_codes(findings)
        if expected["outcome"] == "pass":
            assert findings == [], fixture["case_id"]
        else:
            assert fixture["mutation"]
            assert expected["primary_finding_code"] in codes, (
                fixture["case_id"],
                findings,
            )


def test_principal_lifecycle_is_predecessor_linked_and_closed() -> None:
    document = _base_document()
    event = document["principal_lifecycle_events"][1]
    event["to_state"] = "suspended"
    _finalize(event)
    assert "HGR-PRINCIPAL-LIFECYCLE-TRANSITION" in finding_codes(
        authority.validate_authority_document(document)
    )


@pytest.mark.parametrize("principal_id", ["customer-a-worker", "domain-reviewer"])
@pytest.mark.parametrize("state", ["provisioning", "suspended", "retired"])
def test_full_validation_rejects_every_non_active_required_operation_principal(
    principal_id: str, state: str
) -> None:
    document = _base_document()
    _set_principal_state_as_of(document, principal_id, state)

    findings = authority.validate_authority_document(document)

    assert "HGR-PRINCIPAL-INACTIVE" in finding_codes(findings), findings


def test_operation_principal_lifecycle_is_evaluated_at_authorization_time() -> None:
    document = _base_document()
    _set_principal_state_as_of(
        document,
        "domain-reviewer",
        "retired",
        occurred_at="2026-07-12T12:20:00Z",
    )

    assert (
        authority.validate_operation_authorization(
            document["operation_authorizations"][0], document
        )
        == []
    )

    assert finding_codes(
        authority.validate_active_principal(
            _principal_ref(
                _by_id(document, "principals", "principal_id", "domain-reviewer")
            ),
            document,
            evaluation_time=EVALUATION_TIME,
            path="reviewer_principal_ref",
        )
    ) == ["HGR-PRINCIPAL-INACTIVE"]


def test_authority_records_are_append_only_and_semantically_recomputed() -> None:
    previous = _base_document()
    current = deepcopy(previous)
    assert authority.validate_append_only_authority(previous, current) == []

    mutated = deepcopy(previous)
    mutated["principals"][0]["principal_type"] = "human"
    _finalize(mutated["principals"][0])
    assert "HGR-AUTHORITY-RECORD-UPDATE" in finding_codes(
        authority.validate_append_only_authority(previous, mutated)
    )

    deleted = deepcopy(previous)
    deleted["authority_grants"].pop()
    codes = finding_codes(authority.validate_append_only_authority(previous, deleted))
    assert "HGR-AUTHORITY-RECORD-DELETE" in codes
    assert "HGR-AUTHORITY-RECORD-REORDER" in codes
