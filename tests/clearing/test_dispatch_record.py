"""The ledger: one shape for admissions and refusals, and the distinctions in it.

Four properties the ratified text spends most of its words on, checked here
rather than left to the schema:

  * the refusal-ground enumeration is CLOSED and holds exactly the grounds the
    current realization can emit;
  * a bundle-less dispatch is recorded FROM DECLARATIONS, and no member of the
    shape can present a declared lane as an observed one;
  * the three verification classes stay apart;
  * disposal evidence is a FIELD, and an empty one is refused rather than read as
    a clean host.
"""

from __future__ import annotations

import copy

import yaml

from conftest import EXAMPLES, FAMILY_DIR, adjudicate

SCHEMA = yaml.safe_load(
    (FAMILY_DIR / "dispatch-record.schema.yaml").read_text(encoding="utf-8"))
CLEARED = yaml.safe_load(
    (EXAMPLES / "dispatch-record-cleared.example.yaml").read_text(encoding="utf-8"))
REFUSED = yaml.safe_load(
    (EXAMPLES / "dispatch-record-refused.example.yaml").read_text(encoding="utf-8"))


def test_the_refusal_grounds_are_exactly_the_five_a_landed_entry_can_emit() -> None:
    """SEEDED, then GROWN BY GOVERNED CHANGE — never populated.

    The requirement text names eleven refusal grounds. Two were seeded, because
    `opensoft/xFactory`'s clearing lane emits `unregistered_operation` and
    `unknown_lane_selector` and nothing else. Each of the rest becomes a member
    AS THE OPERATION THAT CAN PRODUCE IT LANDS, because an enumeration seeded
    with grounds no implementation can produce is closed in name only, and a
    ledger column with unreachable values cannot be audited against what actually
    happened.

    THREE JOINED ON 2026-09-04 and the reason is the rule, not an exception:
    `admit-deliberation-clearing-operation` (ratified by Brett Heap, PR #645,
    merged `3cf917b7`) admits register entry number two, which is the FIRST entry
    that permits one lane and refuses the other (`lane_not_permitted`), the FIRST
    to declare a return shape a host actually produces
    (`output_schema_failure`), and the FIRST whose job carries a token at all
    (`origin_scoped_credential`). SIX REMAIN ABSENT, and a fourth added here
    without a ratifier is the defect that packet exists to refuse.
    """
    assert set(SCHEMA["$defs"]["refusal_ground"]["enum"]) == {
        "unregistered_operation",
        "unknown_lane_selector",
        "lane_not_permitted",
        "output_schema_failure",
        "origin_scoped_credential",
    }


def test_each_admitted_ground_records_the_change_that_admitted_it() -> None:
    """A member nobody can trace to a ratifier is a member somebody typed."""
    described = SCHEMA["$defs"]["refusal_ground"]["description"]
    for ground in ("lane_not_permitted", "output_schema_failure",
                   "origin_scoped_credential"):
        assert ground in described
    assert "admit-deliberation-clearing-operation" in described
    assert "add-clearing-dispatch-boundary" in described


def test_the_rendering_rule_is_written_down_and_not_left_to_an_ear() -> None:
    """The awaited grounds are named in PROSE, so an identifier must be RENDERED.

    Without the rule written here, whoever admits one of the remaining six
    re-derives it from three examples — which is how `output_schema_failure` and
    `output-schema-failure` end up in one enumeration.
    """
    described = SCHEMA["$defs"]["refusal_ground"]["description"]
    assert "RENDERING RULE" in described
    for clause in ("lower-casing", "underscores", "`clearing-` prefix", "hyphen"):
        assert clause in described, clause


def test_a_record_naming_each_new_ground_validates_clean(
        reader, registry_and_docs, entries) -> None:
    """THE PROOF THESE MEMBERS ARE ADMITTED, and the only proof owed.

    `output_schema_failure` and `origin_scoped_credential` are written by the
    clearing workflow's HOSTED FINALIZER at dispatch, not by the canonical
    validator — the latter never writes a dispatch record at all — so no negative
    fixture can make either fire and none is owed. The family's "every closed
    refusal code is red-proven" rule binds the validator's finding CODES, not
    this enumeration's MEMBERS, whose proof is that a packaged record naming them
    validates CLEAN.
    """
    for ground in ("lane_not_permitted", "output_schema_failure",
                   "origin_scoped_credential"):
        doc = copy.deepcopy(REFUSED)
        doc["refusal"] = {"ground": ground, "detail": f"refused: {ground}"}
        findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
        assert findings.errors == [], (ground, findings.errors)


def test_the_validator_reads_the_enumeration_out_of_the_schema(reader) -> None:
    """No validator edit was needed to admit three members, and that is the
    design: `clearing-record-refusal-ground-unknown` calls `_refusal_grounds`,
    which reads this list at RUN TIME rather than carrying a second copy."""
    assert reader._refusal_grounds(SCHEMA) == set(
        SCHEMA["$defs"]["refusal_ground"]["enum"])


def test_a_new_ground_is_refused_until_the_schema_admits_it(
        reader, registry_and_docs, entries) -> None:
    doc = copy.deepcopy(REFUSED)
    doc["refusal"] = {"ground": "expired_handle", "detail": "the handle expired"}
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-record-refusal-ground-unknown" in \
        reader.codes_of(findings.errors), findings.errors


def test_a_bundle_less_dispatch_is_recorded_from_declarations() -> None:
    """The ratified case the first read-only operation actually is.

    "Where a registered operation is dispatched WITHOUT a sealed bundle ... the
    record carries the REGISTER ENTRY'S DECLARED data-handling classification,
    and, for each selected lane, that lane's DECLARED runner group and DECLARED
    dispatch label."
    """
    assert CLEARED["bundle_present"] is False
    assert CLEARED["declared_data_handling"] == "public_log_only"
    for lane in CLEARED["lane_declarations"]:
        assert "declared_runner_group" in lane
        assert "declared_dispatch_label" in lane
    claims = {row["field"]: row["claimed"]
              for row in CLEARED["verification"]["policy_checked"]}
    assert claims["worker_profile"] is None, (
        "there was no bundle, so there was no claim; a value here would be the "
        "record inventing one"
    )


def test_the_shape_offers_no_observed_lane_member() -> None:
    """A record that CANNOT express a claim cannot make it.

    "OBSERVED group membership is established by the periodic single-door
    attestation reading the provider's API, and SHALL NOT be taken from the
    runner's own report of itself."
    """
    lane_shape = SCHEMA["properties"]["lane_declarations"]["items"]
    assert lane_shape["additionalProperties"] is False
    assert set(lane_shape["properties"]) == {
        "lane", "declared_runner_group", "declared_dispatch_label"}
    assert not any("observed" in name for name in lane_shape["properties"])


def test_the_three_verification_classes_are_separate_members() -> None:
    verification = SCHEMA["properties"]["verification"]
    assert set(verification["required"]) == {
        "provider_verified", "policy_checked", "origin_signature"}
    provider_fields = set(
        SCHEMA["$defs"]["provider_verified_field"]["properties"]["field"]["enum"])
    policy_fields = set(
        SCHEMA["$defs"]["policy_checked_field"]["properties"]["field"]["enum"])
    assert not provider_fields & policy_fields, (
        "a field that could be reported in either set would let a record choose "
        "which assurance to claim for it"
    )


def test_a_policy_field_cannot_be_reported_as_provider_verified(
        reader, registry_and_docs, entries) -> None:
    doc = copy.deepcopy(CLEARED)
    doc["verification"]["provider_verified"].append(
        {"field": "data_handling", "claimed": "public_log_only",
         "resolved": "public_log_only", "agrees": True})
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-record-policy-field-reported-verified" in \
        reader.codes_of(findings.errors), findings.errors


def test_the_origin_signature_outcome_is_its_own_member() -> None:
    """add-cpc-clearing-boundary: "The signature outcome SHALL be recorded as its
    OWN outcome in the dispatch record and SHALL NOT be folded into the
    provider-verified set."
    """
    outcome = SCHEMA["properties"]["verification"]["properties"]["origin_signature"]
    assert set(outcome["required"]) == {"performed", "outcome"}
    assert set(outcome["properties"]["outcome"]["enum"]) == {
        "verified", "failed", "missing", "not_required"}
    assert CLEARED["verification"]["origin_signature"]["outcome"] == "not_required"


def test_a_refusal_records_what_was_asked_for() -> None:
    """`operation.claimed` survives the refusal; `operation.resolved` is null.

    A record that dropped the claim would leave the ledger unable to answer the
    question an auditor actually has after a refusal.
    """
    assert REFUSED["cleared"] is False
    assert REFUSED["operation"]["claimed"] == "coding"
    assert REFUSED["operation"]["resolved"] is None
    assert REFUSED["refusal"]["ground"] == "unregistered_operation"
    assert REFUSED["outcome"] == "refused"


def test_cleared_and_refused_cannot_both_be_asserted(
        reader, registry_and_docs, entries) -> None:
    doc = copy.deepcopy(CLEARED)
    doc["refusal"] = {"ground": "unknown_lane_selector", "detail": "stale copy"}
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-record-cleared-with-refusal" in \
        reader.codes_of(findings.errors), findings.errors

    doc = copy.deepcopy(REFUSED)
    doc["refusal"] = None
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-record-cleared-with-refusal" in \
        reader.codes_of(findings.errors), findings.errors


def test_disposal_is_required_on_every_record_including_a_refusal() -> None:
    """"the workspace itself SHALL be disposed of when the dispatch reaches a
    terminal state, INCLUDING on failure, refusal, and timeout"."""
    assert "workspace_disposal" in SCHEMA["required"]
    assert REFUSED["workspace_disposal"]["disposed"] is True
    assert REFUSED["workspace_disposal"]["method"], (
        "the refusal's disposal method says there was nothing to dispose of — in "
        "those words, rather than by leaving the field empty and letting a reader "
        "assume it"
    )


def test_an_empty_disposal_field_is_refused_but_a_false_one_is_not(
        reader, registry_and_docs, entries) -> None:
    """THE DIRECTION OF THE RULE MATTERS.

    `disposed: false` is LAWFUL — it records that the host was NOT left clean,
    which is a fact somebody can act on. What is refused is the EMPTY field,
    because an empty field and a clean host are indistinguishable to a reader and
    the attestation would count the dispatch as clean on the strength of nothing.
    """
    doc = copy.deepcopy(CLEARED)
    doc["workspace_disposal"] = {"disposed": None, "method": ""}
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-record-disposal-unattested" in \
        reader.codes_of(findings.errors), findings.errors

    doc = copy.deepcopy(CLEARED)
    doc["workspace_disposal"] = {
        "disposed": False, "disposed_at": "2026-09-03T11:09:02Z",
        "method": "teardown did not complete; the runner temp accumulator remains"}
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-record-disposal-unattested" not in \
        reader.codes_of(findings.errors), findings.errors


def test_the_chain_is_referenced_and_not_restated() -> None:
    """OQ2, settled to REFERENCE: "the ledger is its own record kind with a
    REFERENCE to the chain where one governs the work, not a second log format
    and not a chain link"."""
    chain_ref = SCHEMA["properties"]["chain_ref"]
    patterns = [option.get("pattern") for option in chain_ref["oneOf"]]
    assert r"^sha256:[0-9a-f]{64}$" in patterns
    assert {"type": "null"} in chain_ref["oneOf"]
    assert CLEARED["chain_ref"] is None


def test_this_shape_is_not_the_capability_steward_record() -> None:
    """The name collision is real; the shapes are not the same record.

    `contracts/schemas/dispatch-record.schema.yaml` answers which execution path
    served a capability request. This one answers what was cleared to a governed
    host. Different `$id`, different `kind`, disjoint required members.
    """
    other = yaml.safe_load(
        (FAMILY_DIR.parent / "schemas" / "dispatch-record.schema.yaml")
        .read_text(encoding="utf-8"))
    assert other["$id"] != SCHEMA["$id"]
    assert other["properties"]["kind"]["const"] == "dispatch_record"
    assert SCHEMA["properties"]["kind"]["const"] == "xfactory_clearing_dispatch_record"
    shared = set(other["required"]) & set(SCHEMA["required"])
    assert shared == {"schema_version", "kind", "dispatch_id"}, (
        f"the two records share more than their envelope and their identifier "
        f"name: {shared}"
    )
    # `dispatch_id` IS shared, and its shape is not: the other record's ids are
    # `disp:`-prefixed junction ids, and this one's are clearing-run ids. That a
    # name can be shared while the values behind it are unrelated is precisely
    # why the two records must not be merged into one shape — a single field
    # would have to accept both vocabularies and could distinguish neither.
    assert other["properties"]["dispatch_id"]["pattern"] == "^disp:"
    assert "pattern" not in SCHEMA["properties"]["dispatch_id"]
    assert set(other["required"]) - shared, "the other record has members of its own"
    assert set(SCHEMA["required"]) - shared, "this record has members of its own"

    ours = SCHEMA["description"]
    theirs = other["description"]
    assert "contracts/schemas/dispatch-record.schema.yaml" in ours, (
        "this schema must name the junction record it is not"
    )
    assert "contracts/clearing/dispatch-record.schema.yaml" in theirs, (
        "the junction schema must name THIS record it is not — a cross-reference "
        "asserted in one file and absent from the other is not a cross-reference, "
        "and a reader who greps the shared filename lands on a coincidence"
    )
    assert "xfactory_clearing_dispatch_record" in theirs
