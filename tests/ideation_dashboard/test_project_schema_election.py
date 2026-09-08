"""The project register's SCHEMA-ELECTION fields (`add-project-repo-schema`).

Two halves, because the rules live in two places and neither half proves the
other. The SHAPE half is `contracts/schemas/project-register.schema.yaml`: the
three fields exist, are optional, and `role` is closed to the three values. The
RELATION half is `check_project_schema_election` in
`scripts/validate-ideation-dashboard-contracts.py`: four rules the shape cannot
express, each relating one field to another.

AND ONE NEGATIVE THAT IS NOT A RULE AT ALL: a register declaring none of the
three fields must stay valid and quiet. That is the ratified doctrine expressed
as a test — "a project that DECLINES it is not less governed" — and it is the
assertion that would fail first if the fields ever stopped being optional.

Follows the harness pattern of `test_validate_ideation_dashboard_contracts.py`:
importlib module-load for a hyphenated script, plus the packaged schema read
directly.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate-ideation-dashboard-contracts.py"
REGISTER_SCHEMA = ROOT / "contracts" / "schemas" / "project-register.schema.yaml"


def _load_module():
    spec = importlib.util.spec_from_file_location("vidc_election", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod():
    return _load_module()


@pytest.fixture(scope="module")
def schema():
    return yaml.safe_load(REGISTER_SCHEMA.read_text(encoding="utf-8"))


def _codes(findings) -> list[str]:
    return [line.split("[", 1)[1].split("]", 1)[0] for line in findings.errors]


def _run(mod, projects):
    findings = mod.Findings()
    mod.check_project_register_rules(
        findings, "register", {"projects": projects})
    return findings


# ---------------------------------------------------------------- the shape --

def test_the_three_fields_exist_and_are_optional(schema):
    project = schema["$defs"]["project"]
    props = project["properties"]
    assert "schema" in props and "reference" in props
    assert "repository_roles" in props
    # `id` alone is required: an electing project and a declining one are the
    # same shape, which is what "confers nothing" looks like structurally.
    assert project["required"] == ["id"]


def test_role_is_closed_to_the_three_values(schema):
    entry = schema["$defs"]["project"]["properties"]["repository_roles"]["items"]
    assert entry["required"] == ["repository", "role"]
    assert entry["properties"]["role"]["enum"] == ["spec", "code", "assembly"]


def test_repositories_items_are_still_strings(schema):
    """The one assertion that guards the live readers.

    `scripts/ideation_dashboard/register.py` reads these items as strings. If a
    later change retypes them to objects this test fails FIRST, before the
    dashboard silently stops resolving grouping.
    """
    items = schema["$defs"]["project"]["properties"]["repositories"]["items"]
    assert items["type"] == "string"


def test_the_confers_nothing_posture_is_restated_for_the_new_fields(schema):
    description = schema["description"]
    assert "DEFECTIVE" in description
    assert "clearance eligibility" in description
    assert "repository_roles" in description


# ------------------------------------------------------------ the relations --

def test_a_full_election_is_accepted(mod):
    findings = _run(mod, [{
        "id": "medxscribe",
        "schema": "project-repo-schema",
        "reference": "docs/project-repo-schema.md",
        "repositories": ["MedxScribe", "MedxScribe-spec", "MedxScribe-code"],
        "repository_roles": [
            {"repository": "MedxScribe", "role": "assembly"},
            {"repository": "MedxScribe-spec", "role": "spec"},
            {"repository": "MedxScribe-code", "role": "code"},
        ],
    }])
    assert findings.errors == []


def test_a_project_declaring_nothing_is_accepted(mod):
    """The ratified doctrine as a test: declining costs nothing and owes
    nothing."""
    findings = _run(mod, [{"id": "core", "repositories": ["openxFactory"]}])
    assert findings.errors == []


def test_a_role_naming_an_unlisted_repository_is_refused(mod):
    findings = _run(mod, [{
        "id": "atlas",
        "repositories": ["Atlas"],
        "repository_roles": [{"repository": "Atlas-spec", "role": "spec"}],
    }])
    assert "project-role-unknown-repository" in _codes(findings)


def test_a_repository_given_two_roles_is_refused(mod):
    findings = _run(mod, [{
        "id": "atlas",
        "repositories": ["Atlas"],
        "repository_roles": [
            {"repository": "Atlas", "role": "assembly"},
            {"repository": "Atlas", "role": "code"},
        ],
    }])
    assert "project-duplicate-repository-role" in _codes(findings)


def test_two_assembly_roots_are_refused(mod):
    findings = _run(mod, [{
        "id": "atlas",
        "repositories": ["Atlas", "Atlas-two"],
        "repository_roles": [
            {"repository": "Atlas", "role": "assembly"},
            {"repository": "Atlas-two", "role": "assembly"},
        ],
    }])
    assert "project-multiple-assembly-roles" in _codes(findings)


def test_a_reference_without_a_schema_is_refused(mod):
    findings = _run(mod, [{
        "id": "atlas",
        "reference": "docs/project-repo-schema.md",
        "repositories": ["Atlas"],
    }])
    assert "project-reference-without-schema" in _codes(findings)


def test_a_schema_without_a_reference_is_accepted(mod):
    """Only one direction is a defect. A project may elect and record no
    reference; a reference to an election nobody declared names nothing."""
    findings = _run(mod, [{
        "id": "atlas",
        "schema": "project-repo-schema",
        "repositories": ["Atlas"],
    }])
    assert findings.errors == []


def test_a_malformed_roles_list_is_refused_rather_than_ignored(mod):
    findings = _run(mod, [{
        "id": "atlas", "repositories": ["Atlas"], "repository_roles": "spec",
    }])
    assert "project-roles-not-a-list" in _codes(findings)


def test_the_election_rules_do_not_disturb_the_grouping_rules(mod):
    """The pre-existing D10 rules still fire beside the new ones, so the
    addition is additive in the validator as well as in the schema."""
    findings = mod.Findings()
    mod.check_project_register_rules(findings, "register", {
        "projects": [{"id": "dup"}, {"id": "dup"}],
        "project_groups": [{"id": "g", "projects": ["missing"]}],
    })
    codes = _codes(findings)
    assert "project-duplicate-id" in codes
    assert "project-dangling-group-member" in codes
