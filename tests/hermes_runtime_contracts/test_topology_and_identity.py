"""RED contract for US1 topology, subject identity, and provisioning semantics."""

from __future__ import annotations

import importlib
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from scripts.hermes_runtime_validation.fixtures import evaluate_expected_findings
from scripts.hermes_runtime_validation.loader import load_yaml_document
from tests.hermes_runtime_contracts.support import finding_codes


SHA_A = "sha256:" + "a" * 64
SHA_B = "sha256:" + "b" * 64
COMMIT = "c" * 40
UUID4 = "9f32f1de-82a7-4e38-a83d-9e5dd9189a11"
UUID7 = "018f47a0-7b2c-7abc-8def-0123456789ab"
UUID8 = "018f47a0-7b2c-8abc-8def-0123456789ab"

FIXTURE_ROOT = (
    Path(__file__).resolve().parents[2] / "contracts/hermes-runtime/fixtures"
)
FIXTURE_INDEX = load_yaml_document(FIXTURE_ROOT / "index.yaml")
TOPOLOGY_CASES = tuple(
    case
    for case in FIXTURE_INDEX["cases"]
    if any(str(path).startswith("topology/") for path in case.get("inputs", []))
)


@pytest.fixture
def api():
    return (
        importlib.import_module("scripts.hermes_runtime_validation.semantics.topology"),
        importlib.import_module("scripts.hermes_runtime_validation.semantics.references"),
    )


def _pin(path: str) -> dict:
    return {
        "repository": "opensoft/exampleFactory",
        "commit": COMMIT,
        "path": path,
        "digest": SHA_A,
    }


def _overlay_pin(role: str, suffix: str) -> dict:
    root = f"overlays/{role}-{suffix}"
    return {
        "repository": "opensoft/exampleFactory",
        "commit": COMMIT,
        "overlay_root": root,
        "manifest_path": f"manifests/{role}-{suffix}.overlay.yaml",
        "manifest_digest": SHA_A,
        "schema_id": "https://xforge.us/schemas/openxfactory/hermes-runtime/v2/overlay-manifest.schema.yaml",
        "schema_version": 1,
    }


def _subject(
    ref_uuid: str = UUID4,
    *,
    kind: str = "software_project",
    attested: bool = True,
) -> dict:
    policy_pin = _pin("policies/customer-subject.yaml")
    policy_pin["digest"] = SHA_B
    subject = {
        "kind": kind,
        "issuer": "example-domain",
        "namespace": "customer-subjects",
        "ref": f"urn:xfactory:subject:{ref_uuid}",
        "reference_policy_pin": policy_pin,
    }
    if attested:
        subject["issuer_attestation_digest"] = SHA_B
    return subject


def _profile(
    construction: str = "uuidv4",
    *,
    sentinel_hits: list[str] | None = None,
) -> dict:
    profile = {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-customer-subject-reference-profile",
        "profile_id": "example-domain-customer-subjects-v1",
        "issuer": "example-domain",
        "namespace": "customer-subjects",
        "policy_digest": SHA_B,
        "construction": construction,
        "keyed": construction == "keyed_tokenization",
        "contains_direct_identifier": False,
        "contains_secret": False,
        "sentinel_hits": sentinel_hits or [],
        "attestation": {
            "attestation_id": "attestation-customer-subjects-v1",
            "issuer": "example-domain",
            "policy_digest": SHA_B,
            "attestation_digest": SHA_B,
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


def _template(role: str) -> dict:
    return {
        "role": role,
        "display_name": f"{role.title()} Hermes",
        "overlay": f"hermes/{role}",
    }


def _layer(
    role: str,
    suffix: str,
    *,
    subject: dict | None = None,
) -> dict:
    layer = {
        "installation_id": "install-01",
        "stack_id": "stack-01",
        "layer_id": f"{role}-{suffix}",
        "role": role,
        "template_role": role,
        "display_name": f"{role.title()} {suffix}",
        "policy_namespace": f"stack-01.{role}.{suffix}",
        "overlay_manifest_pin": _overlay_pin(role, suffix),
        "initial_lifecycle_state": "provisioning",
        "created_at": "2026-07-12T12:00:00Z",
    }
    if subject is not None:
        layer["customer_subject"] = subject
    return layer


def _topology(*, state: str = "operational", customers: int = 2) -> dict:
    layers = [_layer("client", "singleton"), _layer("domain", "singleton")]
    for index in range(customers):
        ref = UUID4 if index == 0 else UUID7
        layers.append(_layer("customer", chr(ord("a") + index), subject=_subject(ref)))
    document = {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-topology",
        "installation_id": "install-01",
        "stack_id": "stack-01",
        "derived_topology_state": state,
        "role_templates": [_template("customer"), _template("client"), _template("domain")],
        "layer_registrations": layers,
        "lifecycle_projections": [
            {
                "entity_kind": "installation",
                "installation_id": "install-01",
                "latest_event_id": None,
                "latest_event_digest": None,
                "state": state,
                "terminal_time": None,
            },
            {
                "entity_kind": "stack",
                "installation_id": "install-01",
                "stack_id": "stack-01",
                "latest_event_id": None,
                "latest_event_digest": None,
                "state": state,
                "terminal_time": None,
            },
        ],
    }
    _sync_layer_projections(document)
    return document


def _sync_layer_projections(document: dict) -> None:
    topology_projections = [
        projection
        for projection in document.get("lifecycle_projections", [])
        if projection.get("entity_kind") != "layer"
    ]
    topology_projections.extend(
        {
            "entity_kind": "layer",
            "installation_id": layer["installation_id"],
            "stack_id": layer["stack_id"],
            "layer_id": layer["layer_id"],
            "latest_event_id": None,
            "latest_event_digest": None,
            "state": "active",
            "terminal_time": None,
        }
        for layer in document["layer_registrations"]
    )
    document["lifecycle_projections"] = topology_projections


def _codes(findings: list[dict]) -> list[str]:
    return finding_codes(findings)


def test_one_customer_template_supports_two_runtime_instances(api) -> None:
    topology, _ = api
    document = _topology(customers=2)

    assert topology.validate_topology(document) == []
    assert [item["role"] for item in document["role_templates"]].count("customer") == 1
    assert [item["role"] for item in document["layer_registrations"]].count("customer") == 2


def test_configured_topology_allows_subject_onboarding_later(api) -> None:
    topology, _ = api
    assert topology.validate_topology(_topology(state="configured", customers=0)) == []


def test_operational_topology_requires_an_active_customer(api) -> None:
    topology, _ = api
    assert _codes(topology.validate_topology(_topology(customers=0))) == [
        "HCS-TOPOLOGY-CUSTOMER-MIN"
    ]


@pytest.mark.parametrize(
    ("role", "count", "code"),
    [
        ("client", 0, "HCS-TOPOLOGY-CLIENT-CARDINALITY"),
        ("client", 2, "HCS-TOPOLOGY-CLIENT-CARDINALITY"),
        ("domain", 0, "HCS-TOPOLOGY-DOMAIN-CARDINALITY"),
        ("domain", 2, "HCS-TOPOLOGY-DOMAIN-CARDINALITY"),
    ],
)
def test_singleton_runtime_role_cardinality_is_exact(api, role: str, count: int, code: str) -> None:
    topology, _ = api
    document = _topology()
    document["layer_registrations"] = [
        layer for layer in document["layer_registrations"] if layer["role"] != role
    ]
    document["layer_registrations"].extend(
        _layer(role, f"extra-{index}") for index in range(count)
    )
    _sync_layer_projections(document)

    assert _codes(topology.validate_topology(document)) == [code]


@pytest.mark.parametrize(
    ("role", "code"),
    [
        ("client", "HCS-TOPOLOGY-CLIENT-CARDINALITY"),
        ("domain", "HCS-TOPOLOGY-DOMAIN-CARDINALITY"),
    ],
)
def test_singleton_role_rejects_active_plus_failed_lifetime_registration(
    api, role: str, code: str
) -> None:
    topology, _ = api
    document = _topology(customers=1)
    extra = _layer(role, "failed-replacement")
    document["layer_registrations"].append(extra)
    _sync_layer_projections(document)
    extra_projection = next(
        projection
        for projection in document["lifecycle_projections"]
        if projection.get("layer_id") == extra["layer_id"]
    )
    extra_projection["state"] = "failed"

    assert _codes(topology.validate_topology(document)) == [code]


@pytest.mark.parametrize("kind", ["software_project", "patient", "client_company"])
def test_domain_aliases_use_the_same_neutral_subject_shape(api, kind: str) -> None:
    topology, references = api
    document = _topology(customers=1)
    customer = next(
        layer for layer in document["layer_registrations"] if layer["role"] == "customer"
    )
    customer["customer_subject"] = _subject(kind=kind)

    assert references.validate_customer_subject(customer["customer_subject"], _profile()) == []
    assert topology.validate_topology(document) == []
    assert not ({"project", "patient", "client_company", "ledger"} & document.keys())


def test_customer_subject_is_required_only_on_customer_layers(api) -> None:
    topology, _ = api
    customer_missing = _topology(customers=1)
    customer_missing["layer_registrations"][-1].pop("customer_subject")
    assert _codes(topology.validate_topology(customer_missing)) == ["HCS-SUBJECT-REQUIRED"]

    client_subject = _topology(customers=1)
    client_subject["layer_registrations"][0]["customer_subject"] = _subject(UUID7)
    assert _codes(topology.validate_topology(client_subject)) == ["HCS-SUBJECT-FORBIDDEN"]


@pytest.mark.parametrize(
    ("ref_uuid", "construction"),
    [(UUID4, "uuidv4"), (UUID7, "uuidv7"), (UUID8, "keyed_tokenization")],
)
def test_approved_reference_profiles_validate(api, ref_uuid: str, construction: str) -> None:
    _, references = api
    assert references.validate_customer_subject(
        _subject(ref_uuid), _profile(construction)
    ) == []


def test_reference_syntax_attestation_and_sentinel_fail_for_exact_reasons(api) -> None:
    _, references = api
    malformed = _subject()
    malformed["ref"] = "patient-12345"
    assert _codes(references.validate_customer_subject(malformed, _profile())) == [
        "HCS-SUBJECT-REF-SYNTAX"
    ]

    assert _codes(
        references.validate_customer_subject(_subject(attested=False), _profile())
    ) == ["HCS-SUBJECT-ATTESTATION-REQUIRED"]

    assert _codes(
        references.validate_customer_subject(
            _subject(), _profile(sentinel_hits=["fixture-direct-identifier"])
        )
    ) == ["HCS-SUBJECT-SENSITIVE-SENTINEL"]


@pytest.mark.parametrize("version", ["uuidv1", "uuidv3", "uuidv5"])
def test_unsafe_uuid_derivations_fail_closed(api, version: str) -> None:
    _, references = api
    version_digit = {"uuidv1": "1", "uuidv3": "3", "uuidv5": "5"}[version]
    ref_uuid = f"9f32f1de-82a7-{version_digit}e38-a83d-9e5dd9189a11"

    assert _codes(
        references.validate_customer_subject(_subject(ref_uuid), _profile(version))
    ) == ["HCS-SUBJECT-DERIVATION-FORBIDDEN"]


def test_duplicate_static_role_and_unknown_alias_have_stable_reasons(api) -> None:
    topology, _ = api
    templates = [_template("customer"), _template("client"), _template("domain")]
    aliases = [
        "per_customer_subject",
        "per_project",
        "per_patient",
        "per_ledger",
        "per_campaign",
    ]
    assert topology.validate_static_templates(templates, isolation_scopes=aliases) == []

    assert _codes(
        topology.validate_static_templates(
            templates + [_template("customer")], isolation_scopes=aliases
        )
    ) == ["HCS-STATIC-ROLE-DUPLICATE"]
    assert _codes(
        topology.validate_static_templates(templates, isolation_scopes=["per_repository_owner"])
    ) == ["HCS-STATIC-ISOLATION-UNKNOWN"]


def test_canonical_domain_validator_rejects_duplicate_customer_template(
    tmp_path: Path,
    repo_root: Path,
    yaml_writer,
    command_runner,
) -> None:
    domain_repo = tmp_path / "duplicate-customer-stack"
    stack = {
        "schema_version": 1,
        "kind": "xfactory_domain_stack",
        "domain": {"id": "fixture_domain"},
        "xfactory": {
            "contract_repo": "opensoft/openxFactory",
            "contract_name": "xfactory-domain-stack",
            "contract_ref_type": "commit",
            "contract_ref": COMMIT,
            "contract_schema_version": 1,
            "contract_declared_at": "contracts/manifest.yaml",
            "contract_source": "git",
        },
        "hermes": {
            "layers": [
                {
                    "role": "customer",
                    "display_name": "Customer Hermes",
                    "overlay": "overlays/customer",
                },
                {
                    "role": "customer",
                    "display_name": "Second Customer Template",
                    "overlay": "overlays/customer-two",
                },
                {
                    "role": "client",
                    "display_name": "Client Hermes",
                    "overlay": "overlays/client",
                },
                {
                    "role": "domain",
                    "display_name": "Domain Hermes",
                    "overlay": "overlays/domain",
                },
            ]
        },
        "tenancy": {
            "tenant_kinds": ["pilot"],
            "isolation": {"pilot": "per_customer_subject"},
        },
        "omnigent": {"domain_overlay": "omnigent"},
    }
    yaml_writer(domain_repo / "stack.yaml", stack)
    for relative in (
        "overlays/customer/agent.yaml",
        "overlays/customer-two/agent.yaml",
        "overlays/client/agent.yaml",
        "overlays/domain/agent.yaml",
    ):
        yaml_writer(domain_repo / relative, {"schema_version": 1})
    (domain_repo / "omnigent").mkdir(parents=True)

    result = command_runner(
        [
            sys.executable,
            repo_root / "scripts/validate-domain-factory.py",
            domain_repo,
            "--no-secret-scan",
        ],
        cwd=repo_root,
    )

    assert result.returncode == 1
    assert result.stdout.count(
        "ERROR: stack.yaml: duplicate hermes layer role 'customer'"
    ) == 1
    assert "1 error(s)" in result.stdout


def test_extension_layer_cannot_evasively_represent_customer_subject(api) -> None:
    topology, _ = api
    document = _topology(customers=1)
    extension = _layer("extension", "shadow", subject=_subject(UUID7))
    extension["template_role"] = "extension"
    document["role_templates"].append(_template("extension"))
    document["layer_registrations"].append(extension)
    _sync_layer_projections(document)

    assert _codes(topology.validate_topology(document)) == [
        "HCS-TOPOLOGY-EXTENSION-CUSTOMER-EVASION"
    ]


def test_runtime_layer_must_bind_the_declared_template_role(api) -> None:
    topology, _ = api
    document = _topology(customers=1)
    document["layer_registrations"][-1]["template_role"] = "client"

    assert _codes(topology.validate_topology(document)) == [
        "HCS-TOPOLOGY-TEMPLATE-ROLE-MISMATCH"
    ]


def test_every_registration_is_bound_to_the_one_stack(api) -> None:
    topology, _ = api
    document = _topology(customers=1)
    document["layer_registrations"][-1]["stack_id"] = "foreign-stack"
    _sync_layer_projections(document)

    assert "HCS-TOPOLOGY-STACK-SCOPE-MISMATCH" in _codes(
        topology.validate_topology(document)
    )


def test_projection_state_vocabulary_is_entity_specific(api) -> None:
    topology, _ = api
    document = _topology(customers=1)
    customer_projection = next(
        projection
        for projection in document["lifecycle_projections"]
        if projection.get("layer_id") == "customer-a"
    )
    customer_projection["state"] = "operational"

    assert "HCS-LIFECYCLE-PROJECTION-STATE" in _codes(
        topology.validate_topology(document)
    )


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("layer_id", "HCS-TOPOLOGY-LAYER-ID-REUSE"),
        ("policy_namespace", "HCS-TOPOLOGY-POLICY-NAMESPACE-REUSE"),
        ("customer_subject", "HCS-TOPOLOGY-SUBJECT-REUSE"),
    ],
)
def test_retired_tombstones_forbid_identity_reuse(api, field: str, code: str) -> None:
    topology, _ = api
    document = _topology(customers=1)
    customer = document["layer_registrations"][-1]
    tombstone = {
        "layer_id": "retired-other",
        "policy_namespace": "stack-01.customer.retired-other",
        "customer_subject": _subject(UUID7),
    }
    tombstone[field] = deepcopy(customer[field])

    document["retired_layer_tombstones"] = [tombstone]
    assert _codes(topology.validate_topology(document)) == [code]


def _retired_topology_with_tombstones() -> dict:
    document = _topology(state="retired", customers=1)
    layer_projections = {
        projection["layer_id"]: projection
        for projection in document["lifecycle_projections"]
        if projection["entity_kind"] == "layer"
    }
    tombstones = []
    for layer in document["layer_registrations"]:
        projection = layer_projections[layer["layer_id"]]
        projection.update(
            state="retired",
            latest_event_id=f"retire-{layer['layer_id']}",
            latest_event_digest=SHA_A,
            terminal_time="2026-07-12T12:30:00Z",
        )
        tombstone = {
            "layer_id": layer["layer_id"],
            "policy_namespace": layer["policy_namespace"],
            "retired_event_id": projection["latest_event_id"],
            "retired_event_digest": projection["latest_event_digest"],
        }
        if layer["role"] == "customer":
            tombstone["customer_subject"] = deepcopy(layer["customer_subject"])
        tombstones.append(tombstone)
    document["retired_layer_tombstones"] = tombstones
    return document


def test_retired_layers_require_exact_unique_terminal_tombstones(api) -> None:
    topology, _ = api
    valid = _retired_topology_with_tombstones()
    assert topology.validate_topology(valid) == []

    missing = deepcopy(valid)
    missing["retired_layer_tombstones"].pop()
    assert "HCS-TOPOLOGY-TOMBSTONE-MISSING" in _codes(
        topology.validate_topology(missing)
    )

    mismatched = deepcopy(valid)
    mismatched["retired_layer_tombstones"][0]["policy_namespace"] = "wrong.namespace"
    assert "HCS-TOPOLOGY-TOMBSTONE-MISMATCH" in _codes(
        topology.validate_topology(mismatched)
    )

    duplicate = deepcopy(valid)
    duplicate["retired_layer_tombstones"].append(
        deepcopy(duplicate["retired_layer_tombstones"][0])
    )
    assert "HCS-TOPOLOGY-TOMBSTONE-DUPLICATE" in _codes(
        topology.validate_topology(duplicate)
    )


def _provision_request(key: str, subject: dict, layer_id: str = "customer-a") -> dict:
    return {
        "idempotency_key": key,
        "customer_subject": subject,
        "layer_id": layer_id,
        "lifecycle_record_id": "lifecycle-customer-a",
    }


def test_provisioning_retries_converge_and_conflicting_key_reuse_fails(api) -> None:
    topology, _ = api
    original = _provision_request("provision-001", _subject())
    assert topology.validate_provisioning_requests([original, deepcopy(original)]) == []

    conflicting = _provision_request("provision-001", _subject(UUID7), "customer-b")
    assert _codes(
        topology.validate_provisioning_requests([original, conflicting])
    ) == ["HCS-PROVISION-IDEMPOTENCY-CONFLICT"]


def _topology_fixture(name: str) -> dict:
    return load_yaml_document(FIXTURE_ROOT / "topology" / name)


def test_closed_topology_graph_rejects_installing_direct_retirement(api) -> None:
    topology, _ = api

    assert _codes(
        topology.validate_lifecycle_transition(
            "installation", "installing", "retired"
        )
    ) == ["HCS-LIFECYCLE-TRANSITION"]
    assert _codes(
        topology.validate_lifecycle_transition("stack", "installing", "retired")
    ) == ["HCS-LIFECYCLE-TRANSITION"]


def test_suspended_snapshot_requires_preserved_customer_registration(api) -> None:
    topology, _ = api
    document = _topology_fixture("suspended-preserves-registrations.yaml")
    customer_ids = {
        layer["layer_id"]
        for layer in document["layer_registrations"]
        if layer["role"] == "customer"
    }
    document["layer_registrations"] = [
        layer
        for layer in document["layer_registrations"]
        if layer["layer_id"] not in customer_ids
    ]
    document["layer_lifecycle_events"] = [
        event
        for event in document["layer_lifecycle_events"]
        if event["layer_id"] not in customer_ids
    ]
    document["lifecycle_projections"] = [
        projection
        for projection in document["lifecycle_projections"]
        if projection.get("layer_id") not in customer_ids
    ]

    assert "HCS-TOPOLOGY-SUSPENDED-CUSTOMER-PRESERVATION" in _codes(
        topology.validate_topology_document(document)
    )


def test_retired_snapshot_requires_preserved_singleton_registrations(api) -> None:
    topology, _ = api
    document = _topology_fixture("retired-all-layers.yaml")
    document["layer_registrations"] = []
    document["layer_lifecycle_events"] = []
    document["lifecycle_projections"] = [
        projection
        for projection in document["lifecycle_projections"]
        if projection["entity_kind"] != "layer"
    ]
    document["retired_layer_tombstones"] = []

    assert "HCS-TOPOLOGY-RETIREMENT-PRESERVATION" in _codes(
        topology.validate_topology_document(document)
    )


def test_topology_append_only_rejects_suspended_customer_deletion(api) -> None:
    topology, _ = api
    original = _topology_fixture("suspended-preserves-registrations.yaml")
    candidate = deepcopy(original)
    customer_ids = {
        layer["layer_id"]
        for layer in candidate["layer_registrations"]
        if layer["role"] == "customer"
    }
    candidate["layer_registrations"] = [
        layer
        for layer in candidate["layer_registrations"]
        if layer["layer_id"] not in customer_ids
    ]
    candidate["layer_lifecycle_events"] = [
        event
        for event in candidate["layer_lifecycle_events"]
        if event["layer_id"] not in customer_ids
    ]
    candidate["lifecycle_projections"] = [
        projection
        for projection in candidate["lifecycle_projections"]
        if projection.get("layer_id") not in customer_ids
    ]

    assert "HCS-LIFECYCLE-REGISTRATION-DELETE" in _codes(
        topology.validate_append_only_topology(original, candidate)
    )


def test_topology_append_only_rejects_retired_evidence_erasure(api) -> None:
    topology, _ = api
    original = _topology_fixture("retired-all-layers.yaml")
    candidate = deepcopy(original)
    candidate["layer_registrations"] = []
    candidate["layer_lifecycle_events"] = []
    candidate["lifecycle_projections"] = [
        projection
        for projection in candidate["lifecycle_projections"]
        if projection["entity_kind"] != "layer"
    ]
    candidate["retired_layer_tombstones"] = []

    codes = _codes(topology.validate_append_only_topology(original, candidate))
    assert "HCS-LIFECYCLE-REGISTRATION-DELETE" in codes
    assert "HCS-TOPOLOGY-TOMBSTONE-DELETE" in codes


def test_topology_append_only_rejects_registration_and_event_rewrites(api) -> None:
    topology, _ = api
    original = _topology_fixture("operational-two-customers.yaml")
    candidate = deepcopy(original)
    candidate["layer_registrations"][-1]["display_name"] = "Rewritten Customer"
    customer_id = candidate["layer_registrations"][-1]["layer_id"]
    customer_event = next(
        event
        for event in candidate["layer_lifecycle_events"]
        if event["layer_id"] == customer_id
    )
    customer_event["reason"] = "rewritten-history"

    codes = _codes(topology.validate_append_only_topology(original, candidate))
    assert "HCS-LIFECYCLE-REGISTRATION-IMMUTABLE" in codes
    assert "HCS-LIFECYCLE-EVENT-UPDATE" in codes


def test_orphan_layer_projection_is_rejected(api) -> None:
    topology, _ = api
    document = _topology_fixture("configured-no-customers.yaml")
    document["lifecycle_projections"].append(
        {
            "entity_kind": "layer",
            "installation_id": document["installation_id"],
            "stack_id": document["stack_id"],
            "layer_id": "ghost-customer",
            "latest_event_id": None,
            "latest_event_digest": None,
            "state": "active",
            "terminal_time": None,
        }
    )

    assert "HCS-LIFECYCLE-PROJECTION-ORPHAN" in _codes(
        topology.validate_topology_document(document)
    )


def test_orphan_retirement_tombstone_is_rejected(api) -> None:
    topology, _ = api
    document = _topology_fixture("configured-no-customers.yaml")
    document["retired_layer_tombstones"] = [
        {
            "layer_id": "never-registered",
            "policy_namespace": "stack-01.customer.never-registered",
            "retired_event_id": "fabricated-retirement",
            "retired_event_digest": SHA_A,
        }
    ]

    assert "HCS-TOPOLOGY-TOMBSTONE-ORPHAN" in _codes(
        topology.validate_topology_document(document)
    )


@pytest.mark.parametrize(
    "mutation",
    ["layer_id", "lifecycle_record_id", "customer_subject"],
)
def test_provision_result_binds_exact_customer_registration(
    api, mutation: str
) -> None:
    topology, _ = api
    document = _topology_fixture("provision-retry-same-key.yaml")
    for request in document["provisioning_requests"]:
        if mutation == "layer_id":
            request["layer_id"] = "missing-layer"
        elif mutation == "lifecycle_record_id":
            request["lifecycle_record_id"] = "missing-registration"
        else:
            request["customer_subject"]["ref"] = (
                "urn:xfactory:subject:aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
            )

    assert _codes(topology.validate_topology_document(document)) == [
        "HCS-PROVISION-RESULT-UNBOUND"
    ]


def test_conflicted_provision_key_retains_one_primary_reason(api) -> None:
    topology, _ = api
    document = _topology_fixture("provision-key-subject-conflict.yaml")

    assert _codes(topology.validate_topology_document(document)) == [
        "HCS-PROVISION-IDEMPOTENCY-CONFLICT"
    ]


@pytest.mark.parametrize("state", ["suspended", "retired"])
def test_new_job_admission_rejects_nonworking_topology_states(
    api, state: str
) -> None:
    topology, _ = api

    assert _codes(
        topology.validate_new_job_admission({"derived_topology_state": state})
    ) == ["HCS-TOPOLOGY-NEW-JOB-FORBIDDEN"]


def test_new_job_admission_allows_operational_topology(api) -> None:
    topology, _ = api

    assert topology.validate_new_job_admission(
        {"derived_topology_state": "operational"}
    ) == []


@pytest.mark.parametrize(
    "case",
    TOPOLOGY_CASES,
    ids=[str(case["case_id"]) for case in TOPOLOGY_CASES],
)
def test_indexed_topology_fixture_matches_exact_expected_reason(api, case: dict) -> None:
    topology, _ = api
    assert len(case["inputs"]) == 1
    document = load_yaml_document(FIXTURE_ROOT / case["inputs"][0])

    result = evaluate_expected_findings(
        case,
        topology.validate_topology_document(document),
    )

    assert result["passed"] is True, result


def test_all_indexed_topology_fixtures_close_against_offline_schema_family() -> None:
    contract_root = FIXTURE_ROOT.parent
    schema_names = (
        "shared-definitions.schema.yaml",
        "customer-subject-reference-profile.schema.yaml",
        "installation-lifecycle-event.schema.yaml",
        "stack-lifecycle-event.schema.yaml",
        "layer-lifecycle-event.schema.yaml",
        "overlay-manifest.schema.yaml",
        "runtime-topology.schema.yaml",
    )
    schemas = [load_yaml_document(contract_root / name) for name in schema_names]
    for schema in schemas:
        Draft202012Validator.check_schema(schema)
    registry = Registry().with_resources(
        (
            schema["$id"],
            Resource.from_contents(schema, default_specification=DRAFT202012),
        )
        for schema in schemas
    )
    topology_schema = next(
        schema for schema in schemas if schema["contract_id"] == "runtime-topology"
    )
    validator = Draft202012Validator(
        topology_schema,
        registry=registry,
        format_checker=FormatChecker(),
    )

    for case in TOPOLOGY_CASES:
        document = load_yaml_document(FIXTURE_ROOT / case["inputs"][0])
        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
        assert errors == [], (
            case["case_id"],
            [(list(error.path), error.message) for error in errors],
        )
