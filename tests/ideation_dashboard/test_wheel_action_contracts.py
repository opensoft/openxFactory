"""Contract tests for the add-wheel-action-verbs additive schema growth."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate-ideation-dashboard-contracts.py"
SCHEMAS = ROOT / "contracts" / "schemas"
EXAMPLES = ROOT / "examples" / "ideation-dashboard"
NEGATIVE = EXAMPLES / "negative"

INTENT_SCHEMA = SCHEMAS / "gate-intent.schema.yaml"
ACTION_SCHEMA = SCHEMAS / "gate-action-record.schema.yaml"

WHEEL_VERBS = {
    "promote-to-staging": "possible_id",
    "derive-possibles": "cluster_id",
    "research-brief": "possible_id",
}

POSITIVE_INTENTS = {
    "promote-to-staging": "gate-intent-promote-to-staging.example.yaml",
    "derive-possibles": "gate-intent-derive-possibles.example.yaml",
    "research-brief": "gate-intent-research-brief.example.yaml",
}

POSITIVE_RECORDS = {
    "promote-to-staging": "gate-action-record-promote-to-staging.example.yaml",
    "derive-possibles": "gate-action-record-derive-possibles.example.yaml",
    "research-brief": "gate-action-record-research-brief.example.yaml",
}


def _load_module():
    spec = importlib.util.spec_from_file_location("vidc_wheel", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def vidc():
    return _load_module()


@pytest.fixture(scope="module")
def registry_docs(vidc):
    return vidc.build_registry()


def _yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _example(name: str) -> dict[str, Any]:
    return _yaml(EXAMPLES / name)


def _schema_errors(vidc, registry_docs, doc: dict[str, Any]):
    registry, docs = registry_docs
    schema_name = vidc.KIND_TO_SCHEMA[doc["kind"]]
    validator = vidc.doc_validator(schema_name, registry, docs)
    return list(vidc.iter_errors(validator, doc))


def _validate(vidc, registry_docs, name: str, doc: dict[str, Any]):
    registry, docs = registry_docs
    findings = vidc.Findings()
    vidc.validate_instance(findings, name, doc, registry, docs, set())
    return findings


def _closed_object_paths(node: Any, path: tuple[str, ...] = ()) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        if node.get("additionalProperties") is False:
            found.append("/".join(path) or "<root>")
        for key, value in node.items():
            found.extend(_closed_object_paths(value, (*path, str(key))))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(_closed_object_paths(value, (*path, str(index))))
    return found


def test_wheel_verbs_extend_both_v1_schemas_additively():
    intent = _yaml(INTENT_SCHEMA)
    action = _yaml(ACTION_SCHEMA)

    assert intent["contract_schema_version"] == 1
    assert action["contract_schema_version"] == 1
    assert not _closed_object_paths(intent)
    assert not _closed_object_paths(action)

    assert WHEEL_VERBS.keys() <= set(intent["properties"]["verb"]["enum"])
    assert WHEEL_VERBS.keys() <= set(action["properties"]["action"]["enum"])
    assert "cluster_id" in intent["properties"]["target"]["properties"]
    assert "cluster_id" in action["$defs"]["target"]["properties"]


@pytest.mark.parametrize("verb", sorted(WHEEL_VERBS))
def test_each_wheel_intent_example_validates(vidc, registry_docs, verb):
    findings = _validate(vidc, registry_docs, POSITIVE_INTENTS[verb],
                         _example(POSITIVE_INTENTS[verb]))
    assert not findings.errors, findings.errors


@pytest.mark.parametrize("action", sorted(WHEEL_VERBS))
def test_each_wheel_action_record_example_validates(vidc, registry_docs, action):
    findings = _validate(vidc, registry_docs, POSITIVE_RECORDS[action],
                         _example(POSITIVE_RECORDS[action]))
    assert not findings.errors, findings.errors


@pytest.mark.parametrize("verb,target_field", sorted(WHEEL_VERBS.items()))
def test_each_wheel_intent_requires_its_exact_target(
    vidc, registry_docs, verb, target_field,
):
    doc = copy.deepcopy(_example(POSITIVE_INTENTS[verb]))
    del doc["target"][target_field]
    errors = _schema_errors(vidc, registry_docs, doc)
    assert any(error.validator == "required" and
               tuple(error.absolute_path) == ("target",) for error in errors), errors


@pytest.mark.parametrize("action,target_field", sorted(WHEEL_VERBS.items()))
def test_each_wheel_action_record_requires_its_exact_target(
    vidc, registry_docs, action, target_field,
):
    doc = copy.deepcopy(_example(POSITIVE_RECORDS[action]))
    del doc["target"][target_field]
    errors = _schema_errors(vidc, registry_docs, doc)
    assert any(error.validator == "required" and
               tuple(error.absolute_path) == ("target",) for error in errors), errors


@pytest.mark.parametrize("action", sorted(WHEEL_VERBS))
def test_each_wheel_action_record_requires_a_workflow_job(
    vidc, registry_docs, action,
):
    doc = copy.deepcopy(_example(POSITIVE_RECORDS[action]))
    doc["artifacts"] = [{"kind": "other", "reference": "notes/not-a-job.txt"}]
    errors = _schema_errors(vidc, registry_docs, doc)
    assert any(error.validator == "contains" and
               tuple(error.absolute_path) == ("artifacts",) for error in errors), errors


def test_packaged_wheel_negatives_fail_for_the_declared_schema_rule(
    vidc, registry_docs,
):
    expected = {
        "intent-promote-to-staging-without-possible-id.yaml":
            ("required", "target", "possible_id"),
        "intent-derive-possibles-without-cluster-id.yaml":
            ("required", "target", "cluster_id"),
        "intent-research-brief-without-possible-id.yaml":
            ("required", "target", "possible_id"),
        "gate-action-promote-to-staging-without-workflow-job.yaml":
            ("contains", "artifacts", None),
        "gate-action-derive-possibles-without-workflow-job.yaml":
            ("contains", "artifacts", None),
        "gate-action-derive-possibles-without-cluster-id.yaml":
            ("required", "target", "cluster_id"),
        "gate-action-research-brief-without-workflow-job.yaml":
            ("contains", "artifacts", None),
    }
    # required_property is matched against error.validator_value (the schema's
    # own required list) rather than the human-readable message, which is not
    # a stable jsonschema API.
    for name, (validator_name, path_head, required_property) in expected.items():
        errors = _schema_errors(vidc, registry_docs, _yaml(NEGATIVE / name))
        assert any(error.validator == validator_name and
                   tuple(error.absolute_path)[:1] == (path_head,) and
                   (required_property is None or
                    required_property in error.validator_value)
                   for error in errors), (name, errors)


def test_every_packaged_example_keeps_its_declared_result(vidc, registry_docs):
    registry, docs = registry_docs
    findings = vidc.Findings()
    vidc.check_examples(findings, registry, docs)
    assert not findings.errors, findings.errors
