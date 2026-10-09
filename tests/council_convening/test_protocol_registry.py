"""T006: the closed protocol registry and classification (data-model E1, R10).

THIS FILE HOLDS AN INDEPENDENT FROZEN COPY of the registry as landed at Phase 1,
on the clearing family's pattern (`tests/clearing/test_register_closure.py`). The
instance, the validator's own landed constant and this copy must agree. Moving
any one of them alone turns this file red, and moving all three is a governed
contract change, not an edit.

Classification is probed in its written order:

1. a record whose `protocol` is the replacement is a replacement record, whatever
   else it carries (I3);
2. a record whose `protocol` is the legacy `protocol_id` is legacy, and any other
   `protocol` value is `protocol_unknown`;
3. a record with no `protocol` is legacy when a recognition rule matches, and
   `protocol_unknown` otherwise.

The effects are the Phase 1 rows of the E1 effects table. The rows for the legacy
statuses `deprecated` and `historical_only` land in Phase 6, so at this commit
the reference implementation refuses to guess them.
"""

from __future__ import annotations

import copy

import pytest
import yaml

from scripts.council_convening import classification, records

from .conftest import LEGACY, PROTOCOL_REGISTRY, PROTOCOL_REGISTRY_SCHEMA, REPLACEMENT

LANDED_AT_PHASE_1 = [
    {
        "protocol_id": "xfc-resolved-council-1",
        "role": "replacement",
        "status": "available",
        "signing_contexts": [
            "xfc-resolved-council-1/seat-key-registration",
            "xfc-resolved-council-1/seat-return",
        ],
        "introduced_in": None,
        "deprecated_in": None,
        "removed_in": None,
    },
    {
        "protocol_id": "xfactory-council-seat-return/v1",
        "role": "legacy",
        "status": "in_use",
        "signing_contexts": [
            "xfactory-council-seat-return/v1",
            "xfactory-council-seat-key-authorization/v1",
        ],
        "recognition": [
            {"rule": "convening_block_without_roster",
             "block_member": "council_convening",
             "roster_member": "required_seats"},
            {"rule": "legacy_signing_context",
             "member_paths": [["signature", "protocol"]]},
            {"rule": "root_authorization_member",
             "members": ["root_key_fingerprint", "root_signature", "authorization"]},
        ],
        "introduced_in": None,
        "deprecated_in": None,
        "removed_in": None,
    },
]

SHA = "0123456789abcdef0123456789abcdef01234567"
FPR = "sha256:" + "ab" * 32


@pytest.fixture(scope="module")
def instance() -> dict:
    return yaml.safe_load(PROTOCOL_REGISTRY.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def schema_doc() -> dict:
    return yaml.safe_load(PROTOCOL_REGISTRY_SCHEMA.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def schemas():
    return records.load_schemas()


@pytest.fixture(scope="module")
def registry():
    return classification.load_registry()


# --------------------------------------------------------------------------
# The instance, entry by entry.
# --------------------------------------------------------------------------

def test_the_instance_header(instance):
    assert instance["schema_version"] == 1
    assert instance["kind"] == "xfactory_council_protocol_registry"
    assert instance["registry_id"] == "council-convening-protocols"
    assert instance["registry_version"] == 1


def test_exactly_two_entries_as_landed(instance):
    assert instance["protocols"] == LANDED_AT_PHASE_1


def test_every_tag_field_is_null_until_a_cut(instance):
    for entry in instance["protocols"]:
        for member in ("introduced_in", "deprecated_in", "removed_in"):
            assert entry[member] is None, (entry["protocol_id"], member)


def test_the_status_enumeration_already_holds_all_five_statuses(schema_doc):
    statuses = schema_doc["$defs"]["status"]["enum"]
    assert statuses == ["available", "admission_eligible", "in_use",
                        "deprecated", "historical_only"]


def test_the_schema_carries_the_house_header(schema_doc):
    assert schema_doc["schema_version"] == 1
    assert schema_doc["kind"] == "openxfactory-council-convening-contract-schema"
    assert schema_doc["name"] == "xfactory_council_protocol_registry"
    assert schema_doc["$id"] == (
        "https://xforge.us/schemas/openxfactory/council-convening/v1/"
        "protocol-registry.schema.yaml")
    assert schema_doc["contract_schema_version"] == 1


def test_the_landed_instance_has_no_findings(schemas, instance):
    assert classification.registry_findings(schemas, instance) == []


def test_the_validator_constant_agrees_with_this_frozen_copy():
    landed = classification.LANDED_PROTOCOLS
    assert list(landed) == [entry["protocol_id"] for entry in LANDED_AT_PHASE_1]
    for entry in LANDED_AT_PHASE_1:
        assert landed[entry["protocol_id"]]["role"] == entry["role"]
        assert landed[entry["protocol_id"]]["signing_contexts"] == entry["signing_contexts"]
        assert landed[entry["protocol_id"]].get("recognition") == entry.get("recognition")


# --------------------------------------------------------------------------
# Closure: an added, removed or renamed entry is refused by name.
# --------------------------------------------------------------------------

def _codes(findings):
    return [code for code, _message in findings]


def test_an_added_entry_is_refused(schemas, instance):
    mutated = copy.deepcopy(instance)
    extra = copy.deepcopy(mutated["protocols"][0])
    extra["protocol_id"] = "xfc-resolved-council-2"
    mutated["protocols"].append(extra)
    assert "council-convening-registry-closure" in _codes(
        classification.registry_findings(schemas, mutated))


def test_a_removed_entry_is_refused(schemas, instance):
    mutated = copy.deepcopy(instance)
    mutated["protocols"].pop()
    assert "council-convening-registry-closure" in _codes(
        classification.registry_findings(schemas, mutated))


def test_a_renamed_entry_is_refused(schemas, instance):
    mutated = copy.deepcopy(instance)
    mutated["protocols"][1]["protocol_id"] = "xfactory-council-seat-return/v2"
    assert "council-convening-registry-closure" in _codes(
        classification.registry_findings(schemas, mutated))


def test_a_rewritten_signing_context_is_refused(schemas, instance):
    mutated = copy.deepcopy(instance)
    mutated["protocols"][0]["signing_contexts"][1] = "xfc-resolved-council-1/return"
    assert "council-convening-registry-closure" in _codes(
        classification.registry_findings(schemas, mutated))


def test_a_status_outside_the_entrys_role_is_a_schema_finding(schemas, instance):
    mutated = copy.deepcopy(instance)
    mutated["protocols"][0]["status"] = "in_use"
    assert "council-convening-schema" in _codes(
        classification.registry_findings(schemas, mutated))


def test_a_malformed_tag_is_a_schema_finding(schemas, instance):
    mutated = copy.deepcopy(instance)
    mutated["protocols"][0]["introduced_in"] = "v5"
    assert "council-convening-schema" in _codes(
        classification.registry_findings(schemas, mutated))


def test_a_tag_with_a_trailing_newline_is_a_schema_finding(schemas, instance):
    """The registry schema is a whole document with the house `$schema` header,
    so this holds only if the family's whole-string `pattern` survives the
    descent into it (it once did not, and this tag passed)."""
    accepted = copy.deepcopy(instance)
    accepted["protocols"][1]["introduced_in"] = "contract-v4.0"
    assert classification.registry_findings(schemas, accepted) == []
    mutated = copy.deepcopy(instance)
    mutated["protocols"][1]["introduced_in"] = "contract-v4.0\n"
    assert classification.registry_findings(schemas, mutated) == [
        ("council-convening-schema",
         "protocol registry: fails `pattern` at protocols/1/introduced_in")]


def test_a_status_move_is_not_a_closure_finding(schemas, instance):
    """Statuses and tags are instance data the cuts move (R19); closure pins the
    identity of each entry, not its lifecycle position."""
    mutated = copy.deepcopy(instance)
    mutated["protocols"][1]["status"] = "deprecated"
    mutated["protocols"][1]["deprecated_in"] = "contract-v4.1"
    assert classification.registry_findings(schemas, mutated) == []


# --------------------------------------------------------------------------
# Classification, in its written order.
# --------------------------------------------------------------------------

def _classify(registry, record):
    try:
        return classification.classify(record, registry)
    except records.Refused as refused:
        return refused.code


def test_rule_1_a_replacement_record_is_replacement(registry):
    assert _classify(registry, {"kind": "xfactory_council_convening",
                                "protocol": REPLACEMENT}) == "replacement"


def test_rule_1_root_authorization_members_never_make_it_legacy(registry):
    """I3: a replacement record carrying root-authorization members classifies as
    replacement, and is refused later as `root_authorization_refused` (Phase 4)."""
    record = {"protocol": REPLACEMENT, "root_key_fingerprint": FPR,
              "root_signature": "sig", "authorization": {"by": "root"},
              "council_convening": {"council_id": "c"},
              "signing_context": "xfactory-council-seat-key-authorization/v1"}
    assert _classify(registry, record) == "replacement"


def test_rule_2_the_legacy_protocol_id_is_legacy(registry):
    # The legacy wire's seat-return block.
    record = {"protocol": LEGACY, "key_fingerprint": FPR, "signature": "sig"}
    assert _classify(registry, record) == "legacy"


@pytest.mark.parametrize("protocol", [
    "xfc-resolved-council-2",
    "xfactory-council-seat-key-authorization/v1",   # a legacy CONTEXT, not the protocol_id
    "xfc-resolved-council-1/seat-return",
    "",
    None,
    1,
])
def test_rule_2_any_other_protocol_value_is_unknown(registry, protocol):
    assert _classify(registry, {"protocol": protocol}) == "protocol_unknown"


def test_rule_3a_a_roster_less_convening_block_is_legacy(registry):
    envelope = {"council_convening": {"council_id": "merge-readiness",
                                      "subject_pin": SHA,
                                      "packet_refs": ["opensoft/openxFactory#1268"]}}
    assert _classify(registry, envelope) == "legacy"


def test_rule_3a_a_convening_block_with_a_roster_is_not_recognized(registry):
    envelope = {"council_convening": {"council_id": "merge-readiness",
                                      "required_seats": ["security"]}}
    assert _classify(registry, envelope) == "protocol_unknown"


def test_rule_3a_a_convening_member_that_is_not_an_object_is_not_recognized(registry):
    assert _classify(registry, {"council_convening": "merge-readiness"}) == "protocol_unknown"


# The legacy seat result as it is really produced and read: codexFactory
# `council_seat_signing.py` returns the three-key block, and Hermes
# `review_authority.py` reads it under the seat result's `signature` member
# (SIGNATURE_BLOCK_KEY, SIGNATURE_BLOCK_KEYS). The context string sits at
# `signature.protocol`, and the seat result itself carries no `protocol`.
SIG64 = "A" * 85 + "Q"
HERMES_SEAT_RESULT = {
    "seat": "security",
    "result": "approve",
    "rationale": "no finding",
    "undispositioned_conditions": 0,
    "signature": {"protocol": LEGACY, "key_fingerprint": FPR, "signature": SIG64},
}


@pytest.mark.parametrize("record", [
    HERMES_SEAT_RESULT,
    {"signature": {"protocol": "xfactory-council-seat-key-authorization/v1",
                   "key_fingerprint": FPR, "signature": SIG64}},
])
def test_rule_3b_a_legacy_context_at_signature_protocol_is_legacy(registry, record):
    assert _classify(registry, record) == "legacy"


@pytest.mark.parametrize("record", [
    # No legacy artifact carries a `signing_context` member at either path the
    # first reading guessed; neither is a recognition path.
    {"signing_context": "xfactory-council-seat-return/v1"},
    {"context": {"signing_context": "xfactory-council-seat-key-authorization/v1"}},
    # A replacement context string is not in the legacy set.
    {"signature": {"protocol": "xfc-resolved-council-1/seat-return",
                   "key_fingerprint": FPR, "signature": SIG64}},
    # A string-valued `signature`, as a replacement return carries, has no path.
    {"seat": "security", "signature": SIG64},
    {"signature": {"protocol": ["xfactory-council-seat-return/v1"]}},
])
def test_rule_3b_anything_else_is_unknown(registry, record):
    assert _classify(registry, record) == "protocol_unknown"


def test_a_replacement_return_with_a_string_signature_is_replacement(registry):
    record = {"protocol": REPLACEMENT, "kind": "xfactory_council_seat_return",
              "signature": SIG64}
    assert _classify(registry, record) == "replacement"


def test_the_hermes_seat_result_routes_offline_and_under_a_legacy_selection(registry):
    offline = classification.classify_and_select(HERMES_SEAT_RESULT, None, registry)
    assert offline.as_expected()["outcome"] == "route"
    assert offline.as_expected()["findings"] == ["legacy_protocol_routed"]
    selected = classification.classify_and_select(
        HERMES_SEAT_RESULT, LEGACY, registry, statuses={LEGACY: "in_use"})
    assert selected.as_expected()["outcome"] == "route"


def test_the_hermes_seat_result_is_refused_under_the_replacement_selection(registry):
    outcome = classification.classify_and_select(HERMES_SEAT_RESULT, REPLACEMENT, registry)
    assert (outcome.outcome, outcome.refusal) == ("refuse", "legacy_protocol_refused")


@pytest.mark.parametrize("member", ["root_key_fingerprint", "root_signature",
                                    "authorization"])
def test_rule_3c_a_root_authorized_registration_is_legacy(registry, member):
    record = {"seat_id": "security", "public_key": "A" * 42 + "E", member: "x"}
    assert _classify(registry, record) == "legacy"


def test_rule_3_no_protocol_and_no_recognition_is_unknown(registry):
    assert _classify(registry, {"kind": "xfactory_council_convening",
                                "council_id": "c"}) == "protocol_unknown"
    assert _classify(registry, {}) == "protocol_unknown"


def test_a_non_object_record_is_unknown(registry):
    assert _classify(registry, ["protocol", REPLACEMENT]) == "protocol_unknown"


# --------------------------------------------------------------------------
# The selection-dependent effects: the Phase 1 rows.
# --------------------------------------------------------------------------

LEGACY_RECORD = {"protocol": LEGACY, "key_fingerprint": FPR, "signature": "sig"}
REPLACEMENT_RECORD = {"kind": "xfactory_council_convening", "protocol": REPLACEMENT}
IN_USE = {LEGACY: "in_use"}


def _outcome(registry, record, selected, statuses=None):
    return classification.classify_and_select(record, selected, registry, statuses)


def test_a_legacy_record_under_a_replacement_selection_is_refused(registry):
    outcome = _outcome(registry, LEGACY_RECORD, REPLACEMENT)
    assert (outcome.outcome, outcome.refusal, outcome.findings) == (
        "refuse", "legacy_protocol_refused", ())
    assert outcome.status_read is False


def test_a_replacement_record_under_a_legacy_selection_is_not_selected(registry):
    outcome = _outcome(registry, REPLACEMENT_RECORD, LEGACY, IN_USE)
    assert (outcome.outcome, outcome.refusal) == ("refuse", "protocol_not_selected")
    assert outcome.status_read is True


@pytest.mark.parametrize("selected, statuses", [(LEGACY, IN_USE), (None, None)])
def test_a_legacy_record_under_a_legacy_selection_or_offline_is_routed(
        registry, selected, statuses):
    outcome = _outcome(registry, LEGACY_RECORD, selected, statuses)
    assert outcome.outcome == "route"
    assert outcome.refusal is None
    assert outcome.findings == ("legacy_protocol_routed",)
    assert outcome.derived == {"classification": "legacy"}
    assert outcome.status_read is (selected == LEGACY)


@pytest.mark.parametrize("selected", [REPLACEMENT, None])
def test_a_replacement_record_proceeds_under_a_replacement_selection_or_offline(
        registry, selected):
    outcome = _outcome(registry, REPLACEMENT_RECORD, selected)
    assert (outcome.outcome, outcome.refusal, outcome.findings) == ("accept", None, ())
    assert outcome.derived == {"classification": "replacement"}


def test_classification_runs_before_the_selection_is_read(registry):
    outcome = _outcome(registry, {"protocol": "xfc-resolved-council-2"}, LEGACY, IN_USE)
    assert (outcome.outcome, outcome.refusal) == ("refuse", "protocol_unknown")
    assert outcome.status_read is False


def test_the_registry_instance_status_is_used_when_there_is_no_override(registry):
    outcome = _outcome(registry, LEGACY_RECORD, LEGACY)
    assert outcome.outcome == "route" and outcome.status_read is True


@pytest.mark.parametrize("status", ["deprecated", "historical_only"])
def test_the_phase_6_rows_are_not_guessed_at_this_commit(registry, status):
    with pytest.raises(classification.EffectNotLanded):
        _outcome(registry, LEGACY_RECORD, LEGACY, {LEGACY: status})


def test_a_selection_that_names_no_registry_entry_is_a_harness_error(registry):
    with pytest.raises(KeyError):
        _outcome(registry, LEGACY_RECORD, "xfc-resolved-council-2")
