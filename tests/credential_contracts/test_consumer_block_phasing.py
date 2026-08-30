"""THE BUILT-AND-DRIVEN FIXTURE (add-binding-consumer-identity §1.1b).

The packet's decisive repair was found by four council seats independently, and
every one of them found it the same way: by building the prescribed schema and
DRIVING a record through it. Two Copilot reviews, three author self-catches and
a Codex P1 round had read the same prescription and missed it. So the six shapes
a domain could ALREADY hold are driven here against both releases — the minor
from the shipped bytes, the major from `major_projection.py` — and the ratified
scenario "it stays VALID at the introducing minor and is warned rather than
refused, in EVERY one of those shapes" is a test rather than a promise.

NOTHING NARROWS AT THIS CUT. That is what the first half of this file measures,
and it is a measurement rather than a claim.
"""
from __future__ import annotations

import copy
import importlib.util
import re
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

from major_projection import (ACCESS_MODES, DOCUMENT_REF_PATTERN, IDENTIFIER_PATTERN,
                              branch_for_kind, load_minor_schema, project_major_schema)

BINDING_KIND = "xfactory_credential_binding_template"
REQUIREMENTS_KIND = "xfactory_credential_requirements"

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples" / "credential-contracts"


def _validator_module():
    spec = importlib.util.spec_from_file_location(
        "credential_contracts_validator", ROOT / "scripts" / "validate-credential-contracts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = _validator_module()
MINOR = Draft202012Validator(load_minor_schema())
MAJOR = Draft202012Validator(project_major_schema())


def _binding_doc(consumer=..., key="example_system_read"):
    binding = {
        "provider": "azure_key_vault",
        "vault": "kv-example",
        "secret_ref": "example-secret-reference",
        "owner": "example-platform",
        "rotation_policy": "operator_managed",
    }
    if consumer is not ...:
        binding["consumer"] = consumer
    return {
        "schema_version": 1,
        "kind": "xfactory_credential_binding_template",
        "client": {"id": "example-client"},
        "credential_bindings": {key: binding},
    }


def _errors(validator, doc):
    return [e.message for e in validator.iter_errors(doc)]


# THE SIX SHAPES. Each is a value a domain could hold TODAY, because the binding
# object carries no `additionalProperties: false` and never has.
SHAPES = {
    "object with neither declared member": {"totally": "unchecked"},
    "a scalar consumer value": "locally-shaped-string",
    "a list consumer value": ["locally-shaped"],
    "declared members, placeholder values": {"holder_ref": "<holder>",
                                             "fetch_identity": "<identity>"},
    "declared members plus an undeclared extra": {"holder_ref": "example:holder",
                                                  "fetch_identity": "example-identity",
                                                  "totally": "unchecked"},
    "no block at all": ...,
}


@pytest.mark.parametrize("name", list(SHAPES))
def test_all_six_shapes_validate_at_the_introducing_minor(name):
    """The claim the first prescription falsified: at the minor the schema
    constrains NOTHING about the block, so every shape a domain could already
    hold stays valid."""
    assert _errors(MINOR, _binding_doc(SHAPES[name])) == [], name


@pytest.mark.parametrize("name", list(SHAPES))
def test_every_shape_that_stays_valid_is_WARNED_rather_than_silently_accepted(name):
    """Staying valid is only half the scenario. A shape the major refuses and no
    code names is a shape the deprecation does not serve, so each of the five
    non-conforming shapes must raise a `consumer-*` warning at the minor."""
    doc = _binding_doc(SHAPES[name])
    codes = [code for code, _ in VALIDATOR._deprecation_warnings(doc)]
    assert codes, f"{name} validates at the minor and warns nothing"
    assert all(c in VALIDATOR.DEPRECATION_CODES for c in codes)


@pytest.mark.parametrize("name", [n for n in SHAPES if n != "no block at all"])
def test_five_of_the_six_are_REFUSED_at_the_major(name):
    """Every constraining act lands together at the major — requiredness within
    the block, the closure, and the member grammar."""
    assert _errors(MAJOR, _binding_doc(SHAPES[name])) != [], name


def test_a_blockless_binding_passes_the_majors_SCHEMA_and_is_refused_by_its_VALIDATOR():
    """The sixth shape is the one the two layers split, and the split is a
    ruling: a missing block is a VALIDATOR error at the major, never a schema
    error, because keeping it in the validator is what lets the declared stub
    token exempt a scaffolded repository."""
    doc = _binding_doc()
    assert _errors(MAJOR, doc) == []
    codes = [code for code, _ in VALIDATOR._deprecation_warnings(doc)]
    assert codes == ["consumer-identity-undeclared"]


# --------------------------- the stub exemption (§1.6) ---------------------------

def test_the_stub_token_alone_validates_at_BOTH_releases():
    """`consumer: {instantiation_stub: true}` — the exact bytes the domain-starter
    generator emits. Clean at the introducing minor AND at the major, which is
    the property the two rejected drafts each failed at one end."""
    doc = _binding_doc({"instantiation_stub": True})
    assert _errors(MINOR, doc) == []
    assert _errors(MAJOR, doc) == []
    assert VALIDATOR._deprecation_warnings(doc) == []


def test_the_major_refuses_an_incomplete_NON_stub_and_accepts_a_stub():
    """`if not required(instantiation_stub) then required(holder_ref,
    fetch_identity)` — verified by construction rather than by reading it."""
    assert _errors(MAJOR, _binding_doc({"holder_ref": "example:holder"})) != []
    assert _errors(MAJOR, _binding_doc({"instantiation_stub": True})) == []


def test_a_stub_named_FILE_exempts_nothing():
    """The exemption is the TOKEN. A record carrying live values in a file called
    `*.template.yaml` is a record: it warns now and is refused at the major,
    exactly as if it were named anything else. The packaged probe is
    `warning/live-values-in-stub-named-file.template.yaml`, and this is the
    assertion that its NAME buys it nothing."""
    stub_named = EXAMPLES / "warning" / "live-values-in-stub-named-file.template.yaml"
    doc = yaml.safe_load(stub_named.read_text())
    codes = [code for code, _ in VALIDATOR._deprecation_warnings(doc)]
    assert "consumer-identity-undeclared" in codes


def test_a_false_valued_token_is_a_warning_now_and_an_error_at_the_major():
    """A const-true token declared false validates on the current major —
    verified — so refusing it in a minor would be a new refusal like any other."""
    doc = _binding_doc({"holder_ref": "example:holder",
                        "fetch_identity": "example-identity",
                        "instantiation_stub": False})
    assert _errors(MINOR, doc) == []
    assert [c for c, _ in VALIDATOR._deprecation_warnings(doc)] == ["consumer-token-not-true"]
    assert _errors(MAJOR, doc) != []


# --------------------------- the map key (§1.3) ---------------------------

PLAUSIBLE_EXISTING_KEYS = ["corpus content write", "m365-admin (legacy)",
                           "_leading_underscore", "sync.lane#1"]


@pytest.mark.parametrize("key", PLAUSIBLE_EXISTING_KEYS)
def test_a_key_the_grammar_refuses_is_VALID_today_and_warned(key):
    """Four of five plausible existing keys are valid today and refused by the
    grammar, so imposing it at the minor would refuse four shapes the current
    major accepts — the fourth instance of the defect the council convened over,
    arriving inside the fix round for it."""
    doc = _binding_doc({"instantiation_stub": True}, key=key)
    assert _errors(MINOR, doc) == []
    assert "consumer-binding-key-grammar" in [c for c, _ in VALIDATOR._deprecation_warnings(doc)]


@pytest.mark.parametrize("key", PLAUSIBLE_EXISTING_KEYS)
def test_the_same_keys_are_REFUSED_at_the_major(key):
    assert _errors(MAJOR, _binding_doc({"instantiation_stub": True}, key=key)) != []


def test_a_conforming_key_is_valid_at_both_releases():
    doc = _binding_doc({"instantiation_stub": True}, key="projection_sync_lane")
    assert _errors(MINOR, doc) == []
    assert _errors(MAJOR, doc) == []


def test_the_binding_link_condition_needs_no_grammar_at_the_minor():
    """The sixth lift condition compares the reference's id to the key as a
    STRING. The grammar's job is to stop a key being a shape the comparison
    cannot express — a major-release job — so an ungrammatical key still links."""
    index = {"r.yaml": [{"id": "corpus content write", "access_mode": "workload_identity"}]}
    ref = {"requirement_id": "corpus content write", "requirements_document_ref": "r.yaml"}
    status, record = VALIDATOR.resolve_requirement(ref, index)
    assert status == "ok" and record["access_mode"] == "workload_identity"


# --------------------------- access_mode (§1.4) ---------------------------

def test_an_out_of_vocabulary_access_mode_is_valid_now_and_refused_at_the_major():
    doc = {"schema_version": 1, "kind": "xfactory_credential_requirements",
           "domain": {"id": "example"},
           "requirements": [{"id": "r", "purpose": "p", "access_mode": "Workload_Identity",
                             "requires_domain_approval": True, "requires_human_approval": False,
                             "max_grant_minutes": 60, "audit_required": True}]}
    assert _errors(MINOR, doc) == []
    assert [c for c, _ in VALIDATOR._deprecation_warnings(doc)] == [
        "consumer-access-mode-vocabulary"]
    assert _errors(MAJOR, doc) != []


def test_the_vocabularys_initial_members_are_the_values_already_in_the_wild():
    assert list(VALIDATOR.ACCESS_MODES) == sorted(ACCESS_MODES)


# --------------------------- the document reference (§1.5) ---------------------------

@pytest.mark.parametrize("bad", ["../x.yaml", "/etc/x.yaml", "OpsxFactory:credentials/r.yaml",
                                 "credentials/../../x.yaml", "credentials/r.json", "r"])
def test_the_document_grammar_refuses_escaping_absolute_and_foreign_references(bad):
    assert not VALIDATOR.DOCUMENT_REF.fullmatch(bad), bad
    assert not re.compile(DOCUMENT_REF_PATTERN).fullmatch(bad), bad


@pytest.mark.parametrize("good", ["r.yaml", "credentials/r.yaml", "credentials/sub/r.yml",
                                  "two-consumer-operated-identity.requirements.example.yaml"])
def test_the_document_grammar_admits_repository_relative_yaml(good):
    assert VALIDATOR.DOCUMENT_REF.fullmatch(good), good


# --------------------------- the mirrors ---------------------------

def test_the_validators_grammars_match_the_projection_it_will_become():
    """The projection is what the major cut is checked against, so a drift
    between it and the shipped validator would make the check meaningless."""
    assert VALIDATOR.IDENTIFIER.pattern == IDENTIFIER_PATTERN
    assert VALIDATOR.DOCUMENT_REF.pattern == DOCUMENT_REF_PATTERN


def test_the_schema_describes_every_member_the_validator_enforces():
    """At this minor the schema CONSTRAINS nothing about the block, so its
    description is the only place a member set is declared to a pinned consumer.
    That makes the mirror structural rather than decorative: a member the
    validator warns about and the schema never names would be a rule with no
    published home."""
    binding = branch_for_kind(load_minor_schema(), BINDING_KIND)
    credential_bindings = binding["properties"]["credential_bindings"]
    described = credential_bindings["additionalProperties"]["properties"]["consumer"][
        "description"]
    for member in VALIDATOR.CONSUMER_MEMBERS:
        assert member in described, member
    # the map-key grammar is published on the map, which is where it applies
    assert IDENTIFIER_PATTERN in credential_bindings["description"]


def test_the_schema_declares_the_access_mode_vocabulary_it_does_not_yet_enforce():
    requirements = branch_for_kind(load_minor_schema(), REQUIREMENTS_KIND)
    described = requirements["properties"]["requirements"]["items"][
        "properties"]["access_mode"]["description"]
    for mode in VALIDATOR.ACCESS_MODES:
        assert mode in described, mode


def test_the_block_declares_no_constraint_keyword_at_this_release():
    """The one assertion that would have caught the defect four seats found: the
    shipped `consumer:` subschema carries a description and NOTHING else."""
    credential_bindings = branch_for_kind(load_minor_schema(), BINDING_KIND)[
        "properties"]["credential_bindings"]
    consumer = credential_bindings["additionalProperties"]["properties"]["consumer"]
    assert set(consumer) == {"description"}
    assert "propertyNames" not in credential_bindings


def test_the_binding_object_stays_UNCLOSED_at_both_releases():
    """Closing the binding object is a further breaking act with a much wider
    blast radius and is NOT this change — at either release."""
    for schema in (load_minor_schema(), project_major_schema()):
        binding = branch_for_kind(schema, BINDING_KIND)[
            "properties"]["credential_bindings"]["additionalProperties"]
        assert "additionalProperties" not in binding


# --------------------------- the packaged corpus at both releases ---------------------------

@pytest.mark.parametrize("path", sorted(EXAMPLES.glob("*.example.yaml")), ids=lambda p: p.name)
def test_every_packaged_POSITIVE_validates_at_the_major_too(path):
    """A corpus that models the introducing minor and not the major would leave
    the major's preconditions looking evidenced while evidencing nothing."""
    doc = yaml.safe_load(path.read_text())
    assert _errors(MAJOR, doc) == [], path.name


@pytest.mark.parametrize("path", sorted((EXAMPLES / "warning").glob("*.yaml")),
                         ids=lambda p: p.name)
def test_every_packaged_WARNING_fixture_stays_schema_valid_at_the_minor(path):
    """The whole point of the phasing: these records are warned, not refused."""
    assert _errors(MINOR, yaml.safe_load(path.read_text())) == [], path.name


def test_the_projection_changes_nothing_it_was_not_asked_to():
    """A projection that quietly moved a third thing would make every assertion
    above measure the wrong schema."""
    minor, major = load_minor_schema(), project_major_schema()
    for branch_minor, branch_major in zip(minor["oneOf"], major["oneOf"]):
        kind = branch_minor.get("properties", {}).get("kind", {}).get("const")
        if kind in ("xfactory_credential_binding_template",
                    "xfactory_credential_requirements"):
            continue
        assert branch_minor == branch_major, kind
    assert copy.deepcopy(minor) == load_minor_schema(), "the projection mutated its input"
