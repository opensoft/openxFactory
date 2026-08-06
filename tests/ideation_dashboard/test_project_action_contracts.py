"""Contract tests for the add-project-scoped-selection additive schema growth.

Same harness as test_wheel_action_contracts.py: the packaged create-project
intent/record examples validate through the delegated validator, the per-verb
target conditional bites, and the workflow-job companion is not optional.
"""
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

INTENT_SCHEMA = SCHEMAS / "gate-intent.schema.yaml"
ACTION_SCHEMA = SCHEMAS / "gate-action-record.schema.yaml"

PROJECT_VERBS = ("create-project", "edit-project")
POSITIVE_INTENT = "gate-intent-create-project.example.yaml"
POSITIVE_RECORD = "gate-action-record-create-project.example.yaml"
POSITIVE_INTENTS = {v: f"gate-intent-{v}.example.yaml" for v in PROJECT_VERBS}
POSITIVE_RECORDS = {v: f"gate-action-record-{v}.example.yaml" for v in PROJECT_VERBS}


def _load_module():
    spec = importlib.util.spec_from_file_location("vidc_project", SCRIPT)
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


def test_project_verbs_extend_both_v1_schemas_additively():
    intent = _yaml(INTENT_SCHEMA)
    action = _yaml(ACTION_SCHEMA)
    assert intent["contract_schema_version"] == 1
    assert action["contract_schema_version"] == 1
    for verb in PROJECT_VERBS:
        assert verb in intent["properties"]["verb"]["enum"]
        assert verb in action["properties"]["action"]["enum"]
    assert "project_id" in intent["properties"]["target"]["properties"]
    assert "project_id" in action["$defs"]["target"]["properties"]


@pytest.mark.parametrize("verb", PROJECT_VERBS)
def test_each_project_intent_example_validates(vidc, registry_docs, verb):
    findings = _validate(vidc, registry_docs, POSITIVE_INTENTS[verb],
                         _example(POSITIVE_INTENTS[verb]))
    assert not findings.errors, findings.errors


@pytest.mark.parametrize("verb", PROJECT_VERBS)
def test_each_project_record_example_validates(vidc, registry_docs, verb):
    findings = _validate(vidc, registry_docs, POSITIVE_RECORDS[verb],
                         _example(POSITIVE_RECORDS[verb]))
    assert not findings.errors, findings.errors


@pytest.mark.parametrize("verb", PROJECT_VERBS)
def test_each_project_intent_requires_project_id(vidc, registry_docs, verb):
    doc = copy.deepcopy(_example(POSITIVE_INTENTS[verb]))
    del doc["target"]["project_id"]
    errors = _schema_errors(vidc, registry_docs, doc)
    assert any(error.validator == "required" and
               tuple(error.absolute_path) == ("target",) for error in errors), errors


@pytest.mark.parametrize("verb", PROJECT_VERBS)
def test_each_project_record_requires_project_id(vidc, registry_docs, verb):
    doc = copy.deepcopy(_example(POSITIVE_RECORDS[verb]))
    del doc["target"]["project_id"]
    errors = _schema_errors(vidc, registry_docs, doc)
    assert any(error.validator == "required" and
               tuple(error.absolute_path) == ("target",) for error in errors), errors


@pytest.mark.parametrize("verb", PROJECT_VERBS)
def test_each_project_record_requires_its_workflow_job(vidc, registry_docs, verb):
    """Design D2: the descriptor is not optional companionship — a commission
    record that does not carry it is not a commission."""
    doc = copy.deepcopy(_example(POSITIVE_RECORDS[verb]))
    doc["artifacts"] = [{"kind": "other", "reference": "somewhere-else"}]
    errors = _schema_errors(vidc, registry_docs, doc)
    assert any(error.validator == "contains" for error in errors), errors
