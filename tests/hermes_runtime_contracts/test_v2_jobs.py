"""Scoped v2 job lifecycle contracts and v1 compatibility proof (T066/T070/T071)."""

from __future__ import annotations

import subprocess
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from scripts.hermes_runtime_validation.loader import load_yaml_document
from scripts.hermes_runtime_validation.semantics import jobs
from tests.hermes_runtime_contracts.support import finding_codes

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_ROOT = ROOT / "contracts/hermes-runtime"
FIXTURE_ROOT = CONTRACT_ROOT / "fixtures"
V2_SCHEMA_NAMES = (
    "hermes-job-envelope-v2.schema.yaml",
    "hermes-job-run-v2.schema.yaml",
    "hermes-job-event-v2.schema.yaml",
)
V2_KIND_BY_SCHEMA = {
    "hermes-job-envelope-v2.schema.yaml": jobs.ENVELOPE_KIND,
    "hermes-job-run-v2.schema.yaml": jobs.RUN_KIND,
    "hermes-job-event-v2.schema.yaml": jobs.EVENT_KIND,
}

# The v1 job surface is byte-frozen at the US3 checkpoint (NJE-004-S05 / U8).
US3_CHECKPOINT = "66b1406"
V1_SCHEMA_PATHS = (
    "contracts/schemas/hermes-job-envelope.schema.yaml",
    "contracts/schemas/hermes-job-run.schema.yaml",
    "contracts/schemas/hermes-job-event.schema.yaml",
)
V1_ENVELOPE_EXAMPLE_PATHS = (
    "examples/merge-master/merge-master-job.example.yaml",
    "examples/project-alfa/decomposition/"
    "hermes-feature-decomposition-job.example.yaml",
    "examples/project-alfa/end-to-end-reference/"
    "hermes-merge-council-job.example.yaml",
    "examples/project-alfa/end-to-end-reference/"
    "hermes-non-doc-pilot-job.example.yaml",
    "examples/project-alfa/end-to-end-reference/"
    "hermes-pr-admission-job.example.yaml",
    "examples/project-alfa/merge-council/hermes-merge-council-job.example.yaml",
    "examples/project-alfa/pr-admission/hermes-pr-admission-job.example.yaml",
)

SHA_A = "sha256:" + "a" * 64
SHA_B = "sha256:" + "b" * 64
SHA_C = "sha256:" + "c" * 64
NOW = "2026-07-13T12:00:00Z"
SUBJECT_REF = "urn:xfactory:subject:0f8f1c2d-3a4b-4c5d-8e6f-708192a3b4c5"
JOBS_FIXTURE_KIND = "openxfactory-hermes-runtime-portable-evidence-fixture"
FORBIDDEN_DOMAIN_NOUNS = ("project", "repository", "feature", "patient", "company")
JOBS_PRIMARY_CODES = {
    "jobs-envelope-missing-scope": "HGR-JOB-SCOPE-MISSING",
    "jobs-run-scope-mismatch": "HGR-JOB-SCOPE-MISMATCH",
    "jobs-event-correlation-unknown-run": "HGR-JOB-CORRELATION",
    "jobs-event-sequence-regression": "HGR-JOB-SEQUENCE",
    "jobs-cross-layer-source-foreign": "HGR-JOB-CROSS-LAYER",
    "jobs-envelope-domain-noun": "HGR-JOB-DOMAIN-NOUN",
    "jobs-retired-layer-new-job": "HGR-JOB-LAYER-TERMINAL",
}


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
    resource_type: str,
    layer_id: str = "customer-a",
    digest: str = SHA_A,
) -> dict:
    return {
        "installation_id": "install-01",
        "stack_id": "stack-01",
        "layer_id": layer_id,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "digest": digest,
    }


def _principal_ref(principal_id: str, *, layer_id: str = "customer-a") -> dict:
    return {
        "scope": _scope(layer_id),
        "principal_id": principal_id,
        "record_digest": SHA_A,
    }


def _grant_ref(grant_id: str) -> dict:
    return {
        "installation_id": "install-01",
        "grant_id": grant_id,
        "record_digest": SHA_B,
    }


def _binding_ref(binding_id: str) -> dict:
    return {
        "installation_id": "install-01",
        "binding_id": binding_id,
        "record_digest": SHA_B,
    }


def _envelope() -> dict:
    return {
        "schema_version": 1,
        "kind": jobs.ENVELOPE_KIND,
        "owning_scope": _scope(),
        "job_id": "job-01",
        "job_type": "governed-workflow-stage",
        "issuer_principal_ref": _principal_ref("hermes-issuer-a"),
        "issued_at": NOW,
        "customer_subject_ref": SUBJECT_REF,
        "workflow_refs": [
            _resource("workflow-stage-map", resource_type="contract", digest=SHA_B)
        ],
        "worker_requirements": {
            "pool_id": "worker-pool-a",
            "capability_ids": ["governed-execution"],
        },
        "routing_policy_ref": _resource(
            "routing-policy-a", resource_type="policy", digest=SHA_B
        ),
        "approval_requirements": {
            "approval_required": True,
            "decision_policy_ref": _resource(
                "decision-policy-a", resource_type="policy", digest=SHA_C
            ),
        },
        "required_output_ids": ["governed-result"],
        "trace_root_ref": _resource(
            "trace-root-01", resource_type="artifact", digest=SHA_C
        ),
        "stop_condition_ids": ["budget-exhausted", "human-halt"],
    }


def _run() -> dict:
    return {
        "schema_version": 1,
        "kind": jobs.RUN_KIND,
        "owning_scope": _scope(),
        "run_id": "run-01",
        "job_id": "job-01",
        "job_record_digest": SHA_A,
        "status": "running",
        "current_stage_id": "stage-execute",
        "worker_principal_ref": _principal_ref("worker-a"),
        "worker_grant_ref": _grant_ref("grant-execute-a"),
        "started_at": NOW,
        "event_refs": [_resource("event-01", resource_type="job_event", digest=SHA_C)],
        "artifact_refs": [
            _resource("artifact-01", resource_type="artifact", digest=SHA_A)
        ],
        "approval_refs": [
            _resource("decision-01", resource_type="approval_decision", digest=SHA_B)
        ],
        "trace_refs": [
            _resource("trace-edge-01", resource_type="trace_edge", digest=SHA_C)
        ],
    }


def _event(*, sequence: int = 0, event_id: str = "event-01") -> dict:
    return {
        "schema_version": 1,
        "kind": jobs.EVENT_KIND,
        "owning_scope": _scope(),
        "event_id": event_id,
        "job_id": "job-01",
        "run_id": "run-01",
        "sequence": sequence,
        "event_type": "run-started",
        "actor_principal_ref": _principal_ref("worker-a"),
        "occurred_at": NOW,
        "payload_ref": _resource(
            f"{event_id}-payload", resource_type="job_event", digest=SHA_B
        ),
        "payload_schema_id": (
            "https://xforge.us/schemas/openxfactory/hermes-runtime/v2/"
            "job-event-payloads/run-started.schema.yaml"
        ),
        "payload_schema_version": 1,
    }


def _cross_layer_requirement(*, target_layer: str = "customer-b") -> dict:
    return {
        "source_resource": _resource("artifact-source", resource_type="artifact"),
        "target_resource": _resource(
            "artifact-target",
            resource_type="artifact",
            layer_id=target_layer,
            digest=SHA_B,
        ),
        "binding_ref": _binding_ref("binding-a-b"),
    }


def _layer_lifecycle(state: str = "active", *, layer_id: str = "customer-a") -> list:
    return [
        {
            "installation_id": "install-01",
            "stack_id": "stack-01",
            "layer_id": layer_id,
            "state": state,
        }
    ]


def _admission_document(state: str = "active") -> dict:
    return {
        "operation": "admit_new_job",
        "evaluation_time": NOW,
        "input": {
            "job": _envelope(),
            "layer_lifecycle": _layer_lifecycle(state),
        },
    }


def _correlation_document() -> dict:
    return {
        "operation": "validate_job_correlation",
        "evaluation_time": NOW,
        "input": {
            "job": _envelope(),
            "runs": [_run()],
            "events": [
                _event(sequence=0, event_id="event-01"),
                _event(sequence=1, event_id="event-02"),
            ],
        },
    }


def _retired_evidence_document() -> dict:
    run = _run()
    run["status"] = "completed"
    run["completed_at"] = NOW
    run["summary_ref"] = _resource(
        "run-summary-01", resource_type="artifact", digest=SHA_B
    )
    available = [
        deepcopy(reference)
        for field in ("event_refs", "artifact_refs", "approval_refs", "trace_refs")
        for reference in run[field]
    ]
    available.append(deepcopy(run["summary_ref"]))
    return {
        "operation": "evaluate_retired_layer_evidence",
        "evaluation_time": NOW,
        "input": {
            "run": run,
            "layer_lifecycle": _layer_lifecycle("retired"),
            "available_evidence": available,
        },
    }


@pytest.fixture(scope="module")
def validators() -> dict[str, Draft202012Validator]:
    names = ("shared-definitions.schema.yaml", *V2_SCHEMA_NAMES)
    documents = {name: load_yaml_document(CONTRACT_ROOT / name) for name in names}
    registry = Registry().with_resources(
        (
            document["$id"],
            Resource.from_contents(document, default_specification=DRAFT202012),
        )
        for document in documents.values()
    )
    result = {}
    for name in V2_SCHEMA_NAMES:
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


def _codes(findings: list[dict]) -> list[str]:
    return finding_codes(findings)


def _validate(document: dict) -> list[dict]:
    return jobs.validate_jobs_document(document, evaluation_time=NOW)


def test_v2_schemas_validate_complete_scoped_records_and_stay_closed(
    validators: dict[str, Draft202012Validator],
) -> None:
    documents = {
        "hermes-job-envelope-v2.schema.yaml": _envelope(),
        "hermes-job-run-v2.schema.yaml": _run(),
        "hermes-job-event-v2.schema.yaml": _event(),
    }
    assert {
        name: _errors(validators[name], document)
        for name, document in documents.items()
    } == {name: [] for name in documents}
    for name, document in documents.items():
        extended = deepcopy(document)
        extended["unreviewed_authority"] = True
        assert _errors(validators[name], extended), name


def test_v2_schema_headers_carry_pinned_contract_identity() -> None:
    expected_versions = {name: 2 for name in V2_SCHEMA_NAMES}
    for name in V2_SCHEMA_NAMES:
        document = load_yaml_document(CONTRACT_ROOT / name)
        assert document["schema_version"] == 1, name
        assert document["kind"] == "openxfactory-hermes-runtime-contract-schema", name
        assert document["$id"] == (
            "https://xforge.us/schemas/openxfactory/hermes-runtime/v2/" + name
        ), name
        assert document["contract_id"] == name.removesuffix(".schema.yaml"), name
        assert document["contract_schema_version"] == expected_versions[name], name
        assert document["properties"]["kind"]["const"] == V2_KIND_BY_SCHEMA[name], name
        assert document["additionalProperties"] is False, name


def test_every_v2_record_requires_the_neutral_layer_scope_tuple(
    validators: dict[str, Draft202012Validator],
) -> None:
    documents = {
        "hermes-job-envelope-v2.schema.yaml": _envelope(),
        "hermes-job-run-v2.schema.yaml": _run(),
        "hermes-job-event-v2.schema.yaml": _event(),
    }
    for name, document in documents.items():
        unscoped = deepcopy(document)
        unscoped.pop("owning_scope")
        assert _errors(validators[name], unscoped), name
        partial = deepcopy(document)
        partial["owning_scope"].pop("layer_id")
        assert _errors(validators[name], partial), name


def test_no_required_property_or_enum_encodes_a_domain_noun() -> None:
    def _tokens(value: str) -> set[str]:
        return set(value.replace("-", "_").lower().split("_"))

    def _walk(node: object, name: str) -> None:
        if isinstance(node, dict):
            required = node.get("required")
            if isinstance(required, list):
                for property_name in required:
                    assert not (
                        _tokens(str(property_name)) & set(FORBIDDEN_DOMAIN_NOUNS)
                    ), (name, property_name)
            enum = node.get("enum")
            if isinstance(enum, list):
                for member in enum:
                    assert not (_tokens(str(member)) & set(FORBIDDEN_DOMAIN_NOUNS)), (
                        name,
                        member,
                    )
            for value in node.values():
                _walk(value, name)
        elif isinstance(node, list):
            for value in node:
                _walk(value, name)

    for name in V2_SCHEMA_NAMES:
        _walk(load_yaml_document(CONTRACT_ROOT / name), name)


def test_neutral_envelope_rejects_domain_noun_properties_structurally(
    validators: dict[str, Draft202012Validator],
) -> None:
    for noun in FORBIDDEN_DOMAIN_NOUNS:
        extended = _envelope()
        extended[noun] = "overlay-owned"
        assert _errors(validators["hermes-job-envelope-v2.schema.yaml"], extended), noun


def test_run_couples_to_its_job_and_summary_requires_completion(
    validators: dict[str, Draft202012Validator],
) -> None:
    validator = validators["hermes-job-run-v2.schema.yaml"]
    orphaned = _run()
    orphaned.pop("job_id")
    assert _errors(validator, orphaned)

    unfinished = _run()
    unfinished["summary_ref"] = _resource(
        "run-summary-01", resource_type="artifact", digest=SHA_B
    )
    assert _errors(validator, unfinished)
    unfinished["completed_at"] = NOW
    assert not _errors(validator, unfinished)


def test_event_sequence_is_a_required_non_negative_integer(
    validators: dict[str, Draft202012Validator],
) -> None:
    validator = validators["hermes-job-event-v2.schema.yaml"]
    for mutation in (
        lambda event: event.pop("sequence"),
        lambda event: event.update(sequence=-1),
        lambda event: event.update(sequence="0"),
        lambda event: event.pop("run_id"),
        lambda event: event.pop("payload_ref"),
    ):
        event = _event()
        mutation(event)
        assert _errors(validator, event)


def test_valid_admission_correlation_and_single_records_have_no_findings() -> None:
    assert _validate(_admission_document()) == []
    assert _validate(_correlation_document()) == []
    assert _validate(_envelope()) == []
    assert _validate(_run()) == []
    assert _validate(_event()) == []


def test_run_and_event_scope_drift_from_their_job_fails() -> None:
    drifted_run = _correlation_document()
    drifted_run["input"]["runs"][0]["owning_scope"]["layer_id"] = "customer-b"
    assert _codes(_validate(drifted_run)) == ["HGR-JOB-SCOPE-MISMATCH"]

    drifted_event = _correlation_document()
    drifted_event["input"]["events"][1]["owning_scope"]["layer_id"] = "customer-b"
    assert _codes(_validate(drifted_event)) == ["HGR-JOB-SCOPE-MISMATCH"]


def test_run_and_event_correlation_to_the_exact_job_is_enforced() -> None:
    foreign_run = _correlation_document()
    foreign_run["input"]["runs"][0]["job_id"] = "job-02"
    assert _codes(_validate(foreign_run)) == ["HGR-JOB-CORRELATION"]

    unknown_run = _correlation_document()
    unknown_run["input"]["events"][1]["run_id"] = "run-99"
    assert _codes(_validate(unknown_run)) == ["HGR-JOB-CORRELATION"]

    foreign_event = _correlation_document()
    foreign_event["input"]["events"][0]["job_id"] = "job-02"
    assert _codes(_validate(foreign_event)) == ["HGR-JOB-CORRELATION"]


def test_event_sequences_are_monotonic_per_run() -> None:
    regression = _correlation_document()
    regression["input"]["events"][1]["sequence"] = 0
    assert _codes(_validate(regression)) == ["HGR-JOB-SEQUENCE"]

    negative = _correlation_document()
    negative["input"]["events"][0]["sequence"] = -1
    assert "HGR-JOB-SEQUENCE" in _codes(_validate(negative))


def test_record_missing_or_malformed_scope_fails_semantically() -> None:
    unscoped = _envelope()
    unscoped.pop("owning_scope")
    assert _codes(_validate(unscoped)) == ["HGR-JOB-SCOPE-MISSING"]

    malformed = _event()
    malformed["owning_scope"] = {"scope_kind": "installation"}
    assert _codes(_validate(malformed)) == ["HGR-JOB-SCOPE-MISSING"]


def test_domain_nouns_fail_semantically_while_extensions_stay_descriptive() -> None:
    for noun in FORBIDDEN_DOMAIN_NOUNS:
        injected = _envelope()
        injected[noun] = "overlay-owned"
        assert _codes(_validate(injected)) == ["HGR-JOB-DOMAIN-NOUN"], noun

    nested = _envelope()
    nested["worker_requirements"]["repository_pool"] = "worker-pool-a"
    assert _codes(_validate(nested)) == ["HGR-JOB-DOMAIN-NOUN"]

    overlay = _envelope()
    overlay["extensions"] = {
        "codexfactory.engineering": {
            "repository": "opensoft/project-alfa",
            "feature_id": "feat-001",
        }
    }
    assert _validate(overlay) == []


def test_cross_layer_reference_binds_exact_source_target_and_binding() -> None:
    valid = _correlation_document()
    valid["input"]["job"]["cross_layer_requirements"] = [_cross_layer_requirement()]
    assert _validate(valid) == []

    foreign_source = _correlation_document()
    requirement = _cross_layer_requirement()
    requirement["source_resource"]["layer_id"] = "customer-b"
    foreign_source["input"]["job"]["cross_layer_requirements"] = [requirement]
    assert _codes(_validate(foreign_source)) == ["HGR-JOB-CROSS-LAYER"]

    # A source that reuses the job's layer_id but lives in a foreign
    # installation or stack must NOT pass as in-scope: layer_id is unique only
    # within a stack, so the check compares the full (installation, stack,
    # layer) tuple, not layer_id alone.
    foreign_installation = _correlation_document()
    requirement = _cross_layer_requirement()
    requirement["source_resource"]["installation_id"] = "install-99"
    foreign_installation["input"]["job"]["cross_layer_requirements"] = [requirement]
    assert _codes(_validate(foreign_installation)) == ["HGR-JOB-CROSS-LAYER"]

    foreign_stack = _correlation_document()
    requirement = _cross_layer_requirement()
    requirement["source_resource"]["stack_id"] = "stack-99"
    foreign_stack["input"]["job"]["cross_layer_requirements"] = [requirement]
    assert _codes(_validate(foreign_stack)) == ["HGR-JOB-CROSS-LAYER"]

    # A target in a foreign installation/stack is likewise not a same-stack
    # cross-layer edge even when its layer_id differs from the source.
    foreign_target = _correlation_document()
    requirement = _cross_layer_requirement()
    requirement["target_resource"]["installation_id"] = "install-99"
    foreign_target["input"]["job"]["cross_layer_requirements"] = [requirement]
    assert _codes(_validate(foreign_target)) == ["HGR-JOB-CROSS-LAYER"]

    unbound = _correlation_document()
    requirement = _cross_layer_requirement()
    requirement.pop("binding_ref")
    unbound["input"]["job"]["cross_layer_requirements"] = [requirement]
    assert _codes(_validate(unbound)) == ["HGR-JOB-CROSS-LAYER"]

    same_layer = _correlation_document()
    same_layer["input"]["job"]["cross_layer_requirements"] = [
        _cross_layer_requirement(target_layer="customer-a")
    ]
    assert _codes(_validate(same_layer)) == ["HGR-JOB-CROSS-LAYER"]


@pytest.mark.parametrize("state", ["retired", "suspended"])
def test_terminal_layer_lifecycle_denies_new_governed_jobs(state: str) -> None:
    assert _codes(_validate(_admission_document(state))) == ["HGR-JOB-LAYER-TERMINAL"]


def test_new_job_admission_fails_closed_without_a_registered_layer() -> None:
    unregistered = _admission_document()
    unregistered["input"]["layer_lifecycle"] = _layer_lifecycle(
        "active", layer_id="customer-b"
    )
    assert _codes(_validate(unregistered)) == ["HGR-JOB-LAYER-UNKNOWN"]

    unknown_state = _admission_document("upgraded")
    assert _codes(_validate(unknown_state)) == ["HGR-JOB-LAYER-STATE"]


def test_retired_layer_preserves_artifact_approval_trace_and_audit_access() -> None:
    assert _validate(_retired_evidence_document()) == []

    dropped = _retired_evidence_document()
    dropped["input"]["available_evidence"] = [
        reference
        for reference in dropped["input"]["available_evidence"]
        if reference["resource_type"] != "approval_decision"
    ]
    assert _codes(_validate(dropped)) == ["HGR-JOB-EVIDENCE-DROPPED"]


def test_unknown_operations_and_documents_fail_closed() -> None:
    assert _codes(_validate({"operation": "promote_job", "input": {}})) == [
        "HGR-JOB-OPERATION-UNKNOWN"
    ]
    assert _codes(_validate({"kind": "unrelated-record"})) == [
        "HGR-JOB-OPERATION-UNKNOWN"
    ]


def _embedded_v2_records(node: object) -> list[dict]:
    records: list[dict] = []
    if isinstance(node, dict):
        if node.get("kind") in V2_KIND_BY_SCHEMA.values():
            records.append(node)
        for value in node.values():
            records.extend(_embedded_v2_records(value))
    elif isinstance(node, list):
        for value in node:
            records.extend(_embedded_v2_records(value))
    return records


def test_jobs_fixture_matrix_is_self_describing_and_executable(
    validators: dict[str, Draft202012Validator],
) -> None:
    schema_by_kind = {
        kind: validators[name] for name, kind in V2_KIND_BY_SCHEMA.items()
    }
    paths = sorted((FIXTURE_ROOT / "jobs").glob("*.yaml"))
    assert [path.name for path in paths] == [
        "cross-layer-reference-valid.yaml",
        "cross-layer-source-foreign.yaml",
        "envelope-admission-valid.yaml",
        "envelope-domain-noun.yaml",
        "envelope-missing-scope.yaml",
        "event-correlation-unknown-run.yaml",
        "event-sequence-regression.yaml",
        "lifecycle-valid.yaml",
        "overlay-extension-valid.yaml",
        "retired-layer-evidence-preserved.yaml",
        "retired-layer-new-job.yaml",
        "run-scope-mismatch.yaml",
    ]
    case_ids = set()
    for path in paths:
        fixture = load_yaml_document(path)
        assert fixture["schema_version"] == 1, path
        assert fixture["kind"] == JOBS_FIXTURE_KIND, path
        assert fixture["case_id"].startswith("jobs-"), path
        case_ids.add(fixture["case_id"])
        assert fixture["phase"] == "semantic", path
        assert fixture["requirement_ids"], path
        assert fixture["scenario_ids"], path
        assert fixture["evaluation_time"] == NOW, path
        assert fixture["operation"] == "validate_jobs_document", path
        expected = fixture["expected"]
        findings = jobs.validate_jobs_document(
            fixture["document"], evaluation_time=fixture["evaluation_time"]
        )
        if expected["outcome"] == "pass":
            assert fixture["class"] == "valid", path
            assert findings == [], path
            for record in _embedded_v2_records(fixture["document"]):
                assert not _errors(schema_by_kind[record["kind"]], record), path
        else:
            assert fixture["class"] == "invalid", path
            assert expected["outcome"] == "fail", path
            assert expected["primary_finding_code"] == (
                JOBS_PRIMARY_CODES[fixture["case_id"]]
            ), path
            assert expected["allowed_secondary_codes"] == [], path
            assert findings, path
            assert {finding["code"] for finding in findings} == {
                expected["primary_finding_code"]
            }, path
    assert case_ids == set(JOBS_PRIMARY_CODES) | {
        "jobs-envelope-admission-valid",
        "jobs-lifecycle-valid",
        "jobs-cross-layer-reference-valid",
        "jobs-overlay-extension-valid",
        "jobs-retired-layer-evidence-preserved",
    }


def _checkpoint_blob(path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{US3_CHECKPOINT}:{path}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return completed.stdout


def test_v1_job_schemas_are_byte_frozen_at_the_us3_checkpoint() -> None:
    for path in V1_SCHEMA_PATHS:
        assert (ROOT / path).read_bytes() == _checkpoint_blob(path), path


def test_v1_job_schemas_still_validate_their_pinned_example_fixtures() -> None:
    validators_by_path = {}
    for path in V1_SCHEMA_PATHS:
        schema = load_yaml_document(ROOT / path)
        Draft202012Validator.check_schema(schema)
        validators_by_path[path] = Draft202012Validator(
            schema, format_checker=FormatChecker()
        )
    envelope_validator = validators_by_path[V1_SCHEMA_PATHS[0]]
    for example_path in V1_ENVELOPE_EXAMPLE_PATHS:
        document = load_yaml_document(ROOT / example_path)
        assert not _errors(envelope_validator, document), example_path
