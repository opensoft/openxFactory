"""T035 — frozen assignments and retry identity (feature 035, Phase 3, PR-3).

Data-model E4 (the convening snapshot), E5 (the seat assignment) and E2 step A3
(retry identity and once-per-pin), under Brett Heap's rulings of 2026-10-08:

* OPEN-1, "600 s challenge, 6 h assignment (Recommended)": an assignment's
  lifetime is greater than 0 and at most 21600 seconds. That is the CONTRACT
  ceiling; a consumer's tighter value applies at issuance only, so verification
  and these tests use the ceiling (research R12).
* Retry identity runs after classification, shape and binding, and BEFORE every
  drift check, so an identical retry returns the same snapshot even after the
  governed tip or the live head moved (US1 scenario 4; 025 FR-006; R21).
* Once-per-pin is `convening_conflict`, keyed on `(protocol, council_id,
  subject_pin)`, 025's once-per-pin key with the protocol added.
* "Byte-identical" means equal `xfc-jcs-sha256-1` canonical bytes.

The module under test is imported as `scripts.council_convening.assignments`,
never under a bare name (see this package's `__init__.py`).
"""

from __future__ import annotations

import copy
import json

import pytest

from scripts.council_convening import assignments
from scripts.council_convening.records import Refused
from scripts.signed_execution_chain import canonical

from .conftest import VECTORS as VECTORS_DIR
from .assignment_fixtures import (
    CEILING,
    LEGACY,
    REPLACEMENT,
    SHA_HEAD,
    assignment,
    convening_record,
    digest_of,
    snapshot,
)


def refusal(callable_, *args, **kwargs) -> str:
    with pytest.raises(Refused) as caught:
        callable_(*args, **kwargs)
    return caught.value.code


def check(value: dict, selected: str | None = REPLACEMENT) -> dict:
    """The snapshot half of `admission`, the whole E4 order from classification:
    the derived values on an accept, `Refused` with the outcome's code on a
    refusal."""
    outcome = assignments.snapshot_outcome(value, selected_protocol=selected)
    if outcome.outcome == "refuse":
        raise Refused(outcome.refusal)
    assert outcome.outcome == "accept", outcome
    assert outcome.findings == ()
    return dict(outcome.derived)


# --- the ceiling and the closed operation set ------------------------------------


def test_the_ruled_assignment_ceiling_is_21600_seconds_and_is_read_from_the_contract():
    # OPEN-1. The module checks against the ceiling the landed schema declares,
    # and its named constant must agree with it, so the contract and the
    # reference implementation cannot hold two values.
    assert assignments.ASSIGNMENT_LIFETIME_CEILING_SECONDS == CEILING
    assert assignments.contract_lifetime_ceiling() == CEILING


def test_the_permitted_operations_are_the_two_operations_in_order():
    assert assignments.PERMITTED_OPERATIONS == ("seat_key_registration", "seat_return")


# --- E4 and E5 shapes ---------------------------------------------------------------


def test_a_well_formed_snapshot_is_accepted_with_its_derived_values():
    value = snapshot()
    derived = check(value)
    assert derived == {
        "required_seats": ["seat-a", "seat-b"],
        "convening_digest": digest_of(value["convening"]),
    }


@pytest.mark.parametrize("mutate", [
    pytest.param(lambda s: s.pop("admitted_at"), id="admitted_at-missing"),
    pytest.param(lambda s: s.update(extra=True), id="unknown-member"),
    pytest.param(lambda s: s.update(kind="xfactory_council_seat_assignment"),
                 id="wrong-kind"),
    pytest.param(lambda s: s.update(convening_id="bad id with spaces"),
                 id="convening_id-grammar"),
    pytest.param(lambda s: s.update(convening_id="convening-0001\n"),
                 id="convening_id-trailing-newline"),
    pytest.param(lambda s: s.update(admitted_at="2026-02-30T00:00:00Z"),
                 id="admitted_at-not-a-calendar-date"),
    pytest.param(lambda s: s["convening_digest"].update(subject="council_seat_return_payload"),
                 id="digest-subject-not-council_convening"),
    pytest.param(lambda s: s["convening"].update(unexpected="x"),
                 id="convening-fails-the-E2-schema"),
    pytest.param(lambda s: s.update(assignments={}), id="assignments-not-an-array"),
])
def test_a_snapshot_that_fails_its_schema_is_snapshot_malformed(mutate):
    value = snapshot()
    mutate(value)
    assert refusal(check, value) == "snapshot_malformed"


@pytest.mark.parametrize("mutate", [
    pytest.param(lambda a: a.pop("holder"), id="holder-missing"),
    pytest.param(lambda a: a.update(extra=1), id="unknown-member"),
    pytest.param(lambda a: a.update(kind="xfactory_council_convening_snapshot"),
                 id="wrong-kind"),
    pytest.param(lambda a: a.update(assignment_id="assignment-seat-a\n"),
                 id="assignment_id-trailing-newline"),
    pytest.param(lambda a: a["holder"].update(principal_kind="shared_token"),
                 id="principal_kind-not-in-the-closed-set"),
    pytest.param(lambda a: a["holder"].update(secret="x"), id="holder-unknown-member"),
    pytest.param(lambda a: a.update(not_before="2026-10-09T00:00:00+00:00"),
                 id="not_before-not-a-utc_instant"),
    pytest.param(lambda a: a["convening_digest"].update(subject="gate_verdict"),
                 id="digest-subject-not-council_convening"),
])
def test_an_assignment_that_fails_E5_is_assignment_malformed(mutate):
    value = snapshot()
    mutate(value["assignments"][1])
    assert refusal(check, value) == "assignment_malformed"


# --- the embedded record's offline rules (pre-review M3) -----------------------------
#
# E4 step 2, `snapshot_malformed`, judges the embedded `convening` by the E2 rules
# that need no oracle and judge the record alone: its schema, E2 step 2's
# structural rules, and the offline roster rules of steps 11 and 12. A record
# those rules refuse is never admitted, so a snapshot embedding it is malformed
# (data-model E4, dated note of 2026-10-09). Each case below is otherwise sound:
# `rebuilt` recomputes the digest and issues one assignment per required seat.


def rebuilt(convening: dict) -> dict:
    value = snapshot(convening)
    for index, item in enumerate(value["assignments"]):
        item["assignment_id"] = f"assignment-{index}"
        item["holder"]["principal_ref"] = f"principal-{index}"
    return value


def conditional(*, held=True, seat="seat-c") -> dict:
    """Two standing seats and one held `pr_facts` condition adding `seat`."""
    roster = ["seat-a", "seat-b"] + ([seat] if held and seat is not None else [])
    record = convening_record(required_seats=roster)
    prov = record["required_seats_provenance"]
    prov["conditions"] = [{
        "seat": seat, "predicate": "changed_paths_intersect", "input_contract": "pr_facts",
        "parameters": {"protected_paths": ["src/**"]}, "held": held}]
    prov["fact_sources"] = [{"input_contract": "pr_facts", "source": "candidate_pull"}]
    prov["consumed_facts"] = {"pr_facts": {
        "changed_paths": ["README.md", "src/app/main.py"],
        "changed_files_total": 2, "changed_paths_entry_count": 2}}
    return record


def rule_conditional(touched=("policy/authority/approvers.yaml", "policy/readme.md")) -> dict:
    """Two standing seats and one held `rule_facts` condition adding seat-c, read
    from the candidate's subject, the gate-rules shape."""
    record = convening_record(required_seats=["seat-a", "seat-b", "seat-c"])
    prov = record["required_seats_provenance"]
    prov["candidate"]["subject_path"] = "policy/packets/change-17.yaml"
    prov["conditions"] = [{
        "seat": "seat-c", "predicate": "rule_touches_security_posture",
        "input_contract": "rule_facts",
        "parameters": {"security_surfaces": ["policy/authority/**"]}, "held": True}]
    prov["fact_sources"] = [{"input_contract": "rule_facts", "source": "candidate_subject"}]
    prov["consumed_facts"] = {"rule_facts": {"rule_touched_paths": list(touched)}}
    return record


def _sources(*paths):
    return [{"kind": "file", "path": p, "sha256": "sha256:" + "3" * 64} for p in paths]


def _set(record, member, value):
    record["required_seats_provenance"][member] = value
    return record


INADMISSIBLE = [
    # E2 step 2's structural rules.
    pytest.param(lambda: _set(convening_record(), "governed", {
        "repository": "example-owner/example-rules", "revision": "2" * 40,
        "sources": _sources("rules/zeta.yaml", "rules/alpha.yaml")}),
        "sources", id="sources-out-of-bytewise-order"),
    pytest.param(lambda: _set(convening_record(), "governed", {
        "repository": "example-owner/example-rules", "revision": "2" * 40,
        "sources": _sources("rules/alpha.yaml", "rules/alpha.yaml")}),
        "sources", id="sources-repeated"),
    pytest.param(lambda: _set(convening_record(), "class_inputs", {
        "repository": "example-owner/example-candidate", "head_ref": "feature/alpha"}),
        "class_inputs", id="class_inputs-without-matched_class"),
    pytest.param(lambda: _set(convening_record(), "matched_class", "standard"),
                 "class_inputs", id="matched_class-without-class_inputs"),
    pytest.param(lambda: _set(convening_record(), "governed", {
        "repository": "example-owner/example-rules", "revision": "2" * 40,
        "sources": [{"kind": "listing", "path": "rules", "suffixes": [".yaml"],
                     "entries": ["rules/alpha.yaml"]}]}),
        "entries", id="listing-entry-not-a-file-source"),
    pytest.param(lambda: _set(conditional(), "fact_sources", [
        {"input_contract": "pr_facts", "source": "candidate_pull"},
        {"input_contract": "pr_facts", "source": "candidate_pull"}]),
        "fact_sources", id="fact_sources-contract-repeated"),
    pytest.param(lambda: _set(conditional(), "consumed_facts", {"pr_facts": {
        "changed_paths": ["src/app/main.py", "README.md"],
        "changed_files_total": 2, "changed_paths_entry_count": 2}}),
        "changed_paths", id="changed_paths-unsorted"),
    pytest.param(lambda: _set(conditional(), "consumed_facts", {"pr_facts": {
        "changed_paths": ["README.md", "README.md"],
        "changed_files_total": 2, "changed_paths_entry_count": 2}}),
        "changed_paths", id="changed_paths-repeated"),
    # Brett Heap, 2026-10-11T00:19:34Z, "Same rule, in PR-3 (Recommended)".
    pytest.param(lambda: rule_conditional(("policy/readme.md",
                                           "policy/authority/approvers.yaml")),
                 "rule_touched_paths", id="rule_touched_paths-unsorted"),
    pytest.param(lambda: rule_conditional(("policy/authority/approvers.yaml",
                                           "policy/authority/approvers.yaml")),
                 "rule_touched_paths", id="rule_touched_paths-repeated"),
    # E2 step 11's offline half and step 12.
    pytest.param(lambda: conditional(seat=None), "seat", id="held-condition-seat-unbound"),
    pytest.param(lambda: _set(convening_record(required_seats=[]), "standing_seats", []),
                 "required_seats", id="zero-seats"),
    pytest.param(lambda: _set(convening_record(required_seats=["seat-a", "seat-a"]),
                              "standing_seats", ["seat-a"]),
                 "required_seats", id="roster-repeated-seat"),
    pytest.param(lambda: _set(convening_record(required_seats=["seat-a", "seat-b"]),
                              "standing_seats", ["seat-a"]),
                 "required_seats", id="roster-not-the-standing-and-held-seats"),
    pytest.param(lambda: _set(convening_record(required_seats=["seat-b", "seat-a"]),
                              "standing_seats", ["seat-a", "seat-b"]),
                 "required_seats", id="roster-reordered"),
    pytest.param(lambda: conditional(held=False) | {"required_seats": ["seat-a", "seat-b",
                                                                      "seat-c"]},
                 "required_seats", id="roster-carries-an-unheld-condition-seat"),
]


@pytest.mark.parametrize("build, member", INADMISSIBLE)
def test_a_snapshot_embedding_a_record_an_offline_E2_rule_refuses_is_snapshot_malformed(
        build, member):
    value = rebuilt(build())
    with pytest.raises(Refused) as caught:
        assignments.check_snapshot(value)
    assert caught.value.code == "snapshot_malformed"
    assert caught.value.member == f"convening.{member}"


def test_a_snapshot_embedding_a_held_conditional_seat_is_accepted():
    value = rebuilt(conditional())
    assert check(value)["required_seats"] == ["seat-a", "seat-b", "seat-c"]
    value = rebuilt(rule_conditional())
    assert check(value)["required_seats"] == ["seat-a", "seat-b", "seat-c"]


def test_the_embedded_record_s_rules_are_step_2_so_they_precede_assignment_malformed():
    value = rebuilt(_set(convening_record(required_seats=["seat-a", "seat-b"]),
                         "standing_seats", ["seat-a"]))
    value["assignments"][0]["expires_at"] = "2026-10-09T06:00:01Z"
    assert refusal(check, value) == "snapshot_malformed"


def test_a_zero_seat_snapshot_never_passes():
    # A snapshot with no required seat and no assignment matches "one assignment
    # per required seat" vacuously; Phase 4 completion over it would pass too.
    value = rebuilt(_set(convening_record(required_seats=[]), "standing_seats", []))
    assert value["assignments"] == []
    assert refusal(check, value) == "snapshot_malformed"


def test_a_lone_assignment_is_checked_against_E5_alone():
    convening = convening_record()
    assignments.check_assignment(assignment(convening, "convening-0001", "seat-a"))
    broken = assignment(convening, "convening-0001", "seat-a")
    broken.pop("seat_id")
    assert refusal(assignments.check_assignment, broken) == "assignment_malformed"


def test_a_lone_assignment_that_is_not_canonicalizable_is_refused_after_its_shape():
    # Pre-review L3. Inside a snapshot the same bytes are refused
    # `value_not_canonicalizable` after E4 step 3, so a lone assignment takes the
    # pre-check after its own E5 shape, never before it.
    convening = convening_record()
    value = assignment(convening, "convening-0001", "seat-a")
    value["candidate"]["subject_path"] = "rules/\ud800.yaml"
    assignments.check_assignment(value)       # E5's grammars admit it
    assert refusal(assignments.check_lone_assignment, value) == "value_not_canonicalizable"
    value["expires_at"] = "2026-10-09T06:00:01Z"
    assert refusal(assignments.check_lone_assignment, value) == "assignment_malformed"
    assignments.check_lone_assignment(assignment(convening, "convening-0001", "seat-a"))


# --- the ruled ceiling (OPEN-1) ---------------------------------------------------------


@pytest.mark.parametrize("expires_at, outcome", [
    pytest.param("2026-10-09T06:00:00Z", None, id="exactly-21600-seconds-accepted"),
    # Pre-review L1: lifetimes below the ceiling are accepted too, so a check of
    # `lifetime == 21600` is wrong.
    pytest.param("2026-10-09T00:00:01Z", None, id="one-second-accepted"),
    pytest.param("2026-10-09T01:00:00Z", None, id="one-hour-accepted"),
    pytest.param("2026-10-09T06:00:01Z", "assignment_malformed", id="21601-seconds"),
    pytest.param("2026-10-09T00:00:00Z", "assignment_malformed", id="zero"),
    pytest.param("2026-10-08T23:59:59Z", "assignment_malformed", id="negative"),
])
def test_the_assignment_lifetime_is_bounded_by_the_contract_ceiling(expires_at, outcome):
    value = snapshot()
    value["assignments"][0]["expires_at"] = expires_at
    if outcome is None:
        check(value)
    else:
        assert refusal(check, value) == outcome


def test_the_ceiling_does_not_depend_on_the_date_the_lifetime_crosses():
    # A lifetime is a duration between two instants, never a wall-clock reading:
    # one crossing a month end and a leap day measures the same.
    value = snapshot()
    value["assignments"][0]["not_before"] = "2028-02-29T21:00:00Z"
    value["assignments"][0]["expires_at"] = "2028-03-01T03:00:00Z"
    check(value)
    value["assignments"][0]["expires_at"] = "2028-03-01T03:00:01Z"
    assert refusal(check, value) == "assignment_malformed"


# --- permitted_operations ------------------------------------------------------------


@pytest.mark.parametrize("operations", [
    pytest.param(["seat_key_registration", "seat_return"], id="both"),
    pytest.param(["seat_key_registration"], id="registration-only"),
    pytest.param(["seat_return"], id="return-only"),
])
def test_a_non_empty_ordered_duplicate_free_subset_is_accepted(operations):
    value = snapshot()
    value["assignments"][0]["permitted_operations"] = operations
    check(value)


@pytest.mark.parametrize("operations", [
    pytest.param([], id="empty"),
    pytest.param(["seat_return", "seat_return"], id="repeated"),
    pytest.param(["seat_return", "seat_key_registration"], id="reordered"),
    pytest.param(["seat_key_registration", "seat_return", "seat_return"], id="three"),
    pytest.param(["seat_execution"], id="unknown"),
    pytest.param("seat_return", id="not-a-list"),
])
def test_any_other_operation_list_is_assignment_malformed(operations):
    value = snapshot()
    value["assignments"][0]["permitted_operations"] = operations
    assert refusal(check, value) == "assignment_malformed"


# --- convening_digest recomputation -----------------------------------------------------


def test_a_digest_that_does_not_recompute_over_convening_is_digest_construction_mismatch():
    value = snapshot()
    value["convening_digest"]["value"] = "sha256:" + "0" * 64
    for item in value["assignments"]:
        item["convening_digest"] = copy.deepcopy(value["convening_digest"])
    assert refusal(check, value) == "digest_construction_mismatch"


def test_a_convening_edited_after_freezing_no_longer_recomputes():
    value = snapshot()
    value["convening"]["packet_refs"] = ["packet/alpha-2"]
    assert refusal(check, value) == "digest_construction_mismatch"


def test_the_digest_is_taken_over_canonical_bytes_not_transport_order():
    # Member order in transport is not part of the record: the digest is over
    # the `xfc-jcs-sha256-1` serialization.
    value = snapshot()
    convening = value["convening"]
    value["convening"] = dict(reversed(list(convening.items())))
    check(value)


# --- one assignment per seat, in roster order -------------------------------------------


@pytest.mark.parametrize("seats", [
    pytest.param(["seat-a", "seat-b", "seat-c"], id="extra"),
    pytest.param(["seat-a"], id="missing"),
    pytest.param([], id="none"),
    pytest.param(["seat-b", "seat-a"], id="reordered"),
    pytest.param(["seat-a", "seat-c"], id="same-count-wrong-seat"),
    pytest.param(["seat-a", "seat-a"], id="same-seat-twice"),
])
def test_anything_but_one_assignment_per_required_seat_in_order_is_a_set_mismatch(seats):
    value = snapshot(seats=seats)
    for index, item in enumerate(value["assignments"]):
        item["assignment_id"] = f"assignment-{index}"
        item["holder"]["principal_ref"] = f"principal-{index}"
    assert refusal(check, value) == "assignment_set_mismatch"


@pytest.mark.parametrize("member, replacement", [
    pytest.param("protocol", LEGACY, id="protocol"),
    pytest.param("convening_id", "convening-0002", id="convening_id"),
    pytest.param("convening_digest",
                 {"construction": "xfc-jcs-sha256-1", "subject": "council_convening",
                  "value": "sha256:" + "4" * 64}, id="convening_digest"),
    pytest.param("council_id", "council-beta", id="council_id"),
    pytest.param("candidate",
                 {"repository": "example-owner/example-candidate", "pull_number": 8,
                  "head_sha": SHA_HEAD}, id="candidate-pull_number"),
    pytest.param("candidate",
                 {"repository": "example-owner/example-candidate", "pull_number": 7,
                  "head_sha": SHA_HEAD, "subject_path": "rules/packet.yaml"},
                 id="candidate-subject_path-added"),
])
def test_an_assignment_whose_convening_members_differ_is_a_set_mismatch(member, replacement):
    # I11: an assignment bound to another convening is a Phase 3 set mismatch,
    # never the Phase 4 `cross_convening_context`.
    value = snapshot()
    value["assignments"][1][member] = replacement
    assert refusal(check, value) == "assignment_set_mismatch"


def test_a_repeated_assignment_id_is_assignment_duplicate():
    value = snapshot()
    value["assignments"][1]["assignment_id"] = value["assignments"][0]["assignment_id"]
    assert refusal(check, value) == "assignment_duplicate"


def test_one_principal_on_two_seats_is_assignment_shared_holder():
    value = snapshot()
    value["assignments"][1]["holder"]["principal_ref"] = (
        value["assignments"][0]["holder"]["principal_ref"])
    assert refusal(check, value) == "assignment_shared_holder"


def test_a_binding_shared_across_seats_is_assignment_shared_holder():
    # Brett Heap, 2026-10-11T00:19:34Z, "Refuse at freeze (Recommended)". A shared
    # binding let seat A's claims pass seat B's binding at registration (E7 step
    # 5), so each seat holder has its own E10 binding. The code is reused, so the
    # refusal vocabulary is unchanged.
    value = snapshot()
    assert value["assignments"][0]["holder"]["binding_ref"] != (
        value["assignments"][1]["holder"]["binding_ref"])
    check(value)
    value["assignments"][1]["holder"]["binding_ref"] = (
        value["assignments"][0]["holder"]["binding_ref"])
    with pytest.raises(Refused) as caught:
        assignments.check_snapshot(value)
    assert caught.value.code == "assignment_shared_holder"
    assert caught.value.member == "assignments[1].holder.binding_ref"


def test_every_repeated_principal_is_named_before_any_repeated_binding():
    # Step 7 checks every repeated `principal_ref` first, then every repeated
    # `binding_ref`. Both are `assignment_shared_holder`, so only the member tells
    # the order; the corpus vector for this pair pins the code alone.
    seats = ["seat-a", "seat-b", "seat-c"]
    record = convening_record(required_seats=seats)
    record["required_seats_provenance"]["standing_seats"] = list(seats)
    value = snapshot(record)
    items = value["assignments"]
    items[1]["holder"]["binding_ref"] = items[0]["holder"]["binding_ref"]
    items[2]["holder"]["principal_ref"] = items[0]["holder"]["principal_ref"]
    with pytest.raises(Refused) as caught:
        assignments.check_snapshot(value)
    assert caught.value.code == "assignment_shared_holder"
    assert caught.value.member == "assignments[2].holder.principal_ref"


def test_the_duplicate_check_precedes_the_shared_binding_check():
    value = snapshot()
    value["assignments"][1]["assignment_id"] = value["assignments"][0]["assignment_id"]
    value["assignments"][1]["holder"]["binding_ref"] = (
        value["assignments"][0]["holder"]["binding_ref"])
    assert refusal(check, value) == "assignment_duplicate"


# --- the E4 order --------------------------------------------------------------------


def test_classification_runs_first_so_a_legacy_snapshot_is_never_called_malformed():
    value = snapshot()
    value["protocol"] = LEGACY
    value["unexpected"] = True
    assert refusal(check, value) == "legacy_protocol_refused"


def test_a_replacement_snapshot_under_a_legacy_selection_is_not_selected():
    outcome = assignments.snapshot_outcome(snapshot(), selected_protocol=LEGACY,
                                           statuses={LEGACY: "in_use"})
    assert (outcome.outcome, outcome.refusal) == ("refuse", "protocol_not_selected")
    assert outcome.status_read


def test_offline_a_replacement_snapshot_is_judged_under_the_replacement_rules():
    assert check(snapshot(), selected=None)["required_seats"] == ["seat-a", "seat-b"]
    broken = snapshot()
    broken["assignments"].reverse()
    assert refusal(check, broken, None) == "assignment_set_mismatch"


def test_offline_a_legacy_snapshot_is_routed_never_passed():
    value = snapshot()
    value["protocol"] = LEGACY
    outcome = assignments.snapshot_outcome(value, selected_protocol=None)
    assert (outcome.outcome, outcome.findings) == ("route", ("legacy_protocol_routed",))


def test_an_unknown_protocol_is_protocol_unknown_before_shape():
    value = snapshot()
    value["protocol"] = "xfc-resolved-council-9"
    value.pop("admitted_at")
    assert refusal(check, value) == "protocol_unknown"


def test_snapshot_malformed_precedes_assignment_malformed():
    value = snapshot()
    value.pop("admitted_at")
    value["assignments"][0]["expires_at"] = "2026-10-09T06:00:01Z"
    assert refusal(check, value) == "snapshot_malformed"


def test_assignment_malformed_is_at_its_E4_position_before_the_digest_and_set_checks():
    value = snapshot(seats=["seat-b", "seat-a"])
    value["convening_digest"]["value"] = "sha256:" + "0" * 64
    value["assignments"][1]["expires_at"] = "2026-10-09T06:00:01Z"
    assert refusal(check, value) == "assignment_malformed"


def test_the_first_malformed_assignment_in_array_order_is_the_one_named():
    value = snapshot()
    value["assignments"][0]["permitted_operations"] = []
    value["assignments"][1].pop("holder")
    with pytest.raises(Refused) as caught:
        assignments.check_snapshot(value)
    assert caught.value.code == "assignment_malformed"
    assert caught.value.member == "assignments[0]"


def test_a_value_that_is_not_canonicalizable_is_refused_before_the_digest():
    # A lone surrogate passes every grammar the schemas declare (a packet
    # reference forbids only control characters), so it reaches the digest step
    # unless the canonicalizability pre-check runs first.
    value = snapshot()
    value["convening"]["packet_refs"] = ["packet/\ud800"]
    assert refusal(check, value) == "value_not_canonicalizable"


def test_the_digest_check_precedes_the_set_check():
    value = snapshot(seats=["seat-b", "seat-a"])
    value["convening_digest"]["value"] = "sha256:" + "0" * 64
    assert refusal(check, value) == "digest_construction_mismatch"


def test_the_set_check_precedes_the_duplicate_check():
    value = snapshot(seats=["seat-a", "seat-b", "seat-c"])
    value["assignments"][2]["assignment_id"] = value["assignments"][0]["assignment_id"]
    assert refusal(check, value) == "assignment_set_mismatch"


def test_the_duplicate_check_precedes_the_shared_holder_check():
    value = snapshot()
    value["assignments"][1]["assignment_id"] = value["assignments"][0]["assignment_id"]
    value["assignments"][1]["holder"]["principal_ref"] = (
        value["assignments"][0]["holder"]["principal_ref"])
    assert refusal(check, value) == "assignment_duplicate"


def test_a_refusal_message_never_echoes_a_value():
    value = snapshot()
    value["assignments"][0]["holder"]["principal_ref"] = "principal-visible-marker"
    value["assignments"][1]["holder"]["principal_ref"] = "principal-visible-marker"
    with pytest.raises(Refused) as caught:
        assignments.check_snapshot(value)
    assert caught.value.code == "assignment_shared_holder"
    assert "principal-visible-marker" not in str(caught.value)


# --- retry identity and once-per-pin (E2 step A3) ---------------------------------------


def live(record: dict, convening_id: str = "convening-0001") -> dict:
    return snapshot(record, convening_id=convening_id)


def test_the_convening_key_is_protocol_council_and_subject_pin():
    record = convening_record()
    assert assignments.convening_key(record) == (
        REPLACEMENT, "council-alpha", SHA_HEAD)


def test_an_identical_record_returns_the_live_snapshot_unchanged():
    record = convening_record()
    existing = live(record)
    returned = assignments.retry_identity(copy.deepcopy(record), [existing])
    assert returned == existing
    assert returned["convening_id"] == "convening-0001"
    assert returned["assignments"] == existing["assignments"]


def test_byte_identical_means_equal_canonical_bytes_not_equal_transport():
    record = convening_record()
    existing = live(record)
    resent = dict(reversed(list(copy.deepcopy(record).items())))
    resent["required_seats_provenance"] = dict(
        reversed(list(resent["required_seats_provenance"].items())))
    assert list(resent) != list(record)
    assert assignments.retry_identity(resent, [existing]) == existing


def test_no_live_snapshot_means_no_retry_and_no_conflict():
    assert assignments.retry_identity(convening_record(), []) is None


@pytest.mark.parametrize("mutate", [
    pytest.param(lambda r: r.update(packet_refs=["packet/alpha-2"]), id="packet_refs"),
    pytest.param(lambda r: r.update(mix_id="mix-1"), id="mix_id-added"),
    pytest.param(lambda r: r["required_seats_provenance"]["candidate"].update(pull_number=8),
                 id="only-candidate-pull_number"),
    pytest.param(lambda r: r["required_seats_provenance"]["candidate"].update(
        subject_path="rules/packet.yaml"), id="only-candidate-subject_path"),
    pytest.param(lambda r: r["required_seats_provenance"]["governed"].update(
        revision="5" * 40), id="governed-revision"),
])
def test_a_different_record_for_the_same_key_is_convening_conflict(mutate):
    record = convening_record()
    existing = live(record)
    resent = copy.deepcopy(record)
    mutate(resent)
    assert assignments.convening_key(resent) == assignments.convening_key(record)
    assert refusal(assignments.retry_identity, resent, [existing]) == "convening_conflict"


def test_a_record_for_the_same_council_at_another_pin_is_not_a_conflict():
    record = convening_record()
    existing = live(record)
    other = convening_record(subject_pin="6" * 40)
    other["required_seats_provenance"]["candidate"]["head_sha"] = "6" * 40
    assert assignments.retry_identity(other, [existing]) is None


def test_a_record_for_another_council_at_the_same_pin_is_not_a_conflict():
    existing = live(convening_record())
    other = convening_record(council_id="council-beta")
    assert assignments.retry_identity(other, [existing]) is None


def test_once_per_pin_never_pre_empts_an_identical_retry():
    # The identical snapshot has the record's own key, so a once-per-pin test run
    # first would refuse an identical retry as a conflict. The identical test runs
    # over every live snapshot before the once-per-pin test runs over any. The
    # snapshots for other keys are listed first. No two live snapshots share a
    # key, because once-per-pin allows one (pre-review M2), so a conflicting
    # snapshot beside the identical one is a state no consumer can hold.
    record = convening_record()
    identical = live(record, convening_id="convening-0001")
    other_pin = convening_record(subject_pin="6" * 40)
    other_pin["required_seats_provenance"]["candidate"]["head_sha"] = "6" * 40
    other_council = convening_record(council_id="council-beta")
    returned = assignments.retry_identity(
        copy.deepcopy(record),
        [live(other_pin, "convening-0009"), live(other_council, "convening-0008"), identical])
    assert returned["convening_id"] == "convening-0001"


def test_a_conflict_replaces_nothing():
    record = convening_record()
    existing = live(record)
    frozen = copy.deepcopy(existing)
    resent = copy.deepcopy(record)
    resent["packet_refs"] = ["packet/alpha-2"]
    with pytest.raises(Refused):
        assignments.retry_identity(resent, [existing])
    assert existing == frozen


def test_a_conflict_message_never_echoes_a_value():
    record = convening_record()
    resent = copy.deepcopy(record)
    resent["packet_refs"] = ["packet/visible-marker"]
    with pytest.raises(Refused) as caught:
        assignments.retry_identity(resent, [live(record)])
    assert "visible-marker" not in str(caught.value)


# --- retry identity inside the admission order (E2 step A3; T040) ------------------
#
# Each drift vector is adjudicated twice through the corpus. Without its live
# snapshot the same record and environment must REFUSE with the drift code, which
# shows the drift is real; with it, the identical retry must return the live
# snapshot, which shows retry identity runs before every drift check.

DRIFT = [
    pytest.param("asg-retry-identical-after-tip-moved-accept", "rule_superseded",
                 id="governed-source-changed-at-the-tip"),
    pytest.param("asg-retry-identical-after-head-moved-accept", "candidate_head_moved",
                 id="live-head-moved"),
]


def _context():
    from scripts.council_convening import classification, corpus, records

    return corpus.Context(records.load_schemas(), classification.load_registry())


def _vector(case_id: str) -> dict:
    import json

    from .conftest import VECTORS

    return json.loads((VECTORS / "assignment" / f"{case_id}.json").read_text(encoding="utf-8"))


def _without_live_snapshots(vector: dict) -> dict:
    stripped = copy.deepcopy(vector)
    del stripped["environment"]["issued"]
    return stripped


@pytest.mark.parametrize("case_id, drift_code", DRIFT)
def test_an_identical_retry_returns_the_same_snapshot_even_after_drift(case_id, drift_code):
    from scripts.council_convening import corpus

    context = _context()
    vector = _vector(case_id)
    fresh = corpus.adjudicate(_without_live_snapshots(vector), context)
    assert (fresh.outcome, fresh.refusal) == ("refuse", drift_code)
    retried = corpus.adjudicate(vector, context)
    assert retried.outcome == "accept"
    assert retried.derived["convening_id"] == "convening-0001"
    assert retried.derived["convening_digest"] == digest_of(vector["inputs"]["record"])
    returned, = vector["environment"]["issued"]["live_snapshots"]
    assert retried.derived["snapshot_digest"] == canonical.digest(returned)


def test_a_returned_snapshot_derives_the_digest_of_the_whole_snapshot():
    # Pre-review M1. E4: an identical retry returns "the same `convening_id` and
    # the same assignments". The id alone would let a consumer that re-issues
    # assignments on retry agree with the corpus; the digest of the snapshot it
    # returns does not.
    from scripts.council_convening import corpus

    vector = _vector("asg-retry-identical-returns-snapshot-accept")
    returned, = vector["environment"]["issued"]["live_snapshots"]
    derived = corpus.adjudicate(vector, _context()).derived
    assert derived == vector["expected"]["derived"]
    assert derived["snapshot_digest"] == canonical.digest(returned)
    reissued = copy.deepcopy(returned)
    reissued["assignments"][0]["assignment_id"] = "assignment-reissued"
    assert canonical.digest(reissued) != derived["snapshot_digest"]


def test_a_conflict_is_refused_before_the_head_is_read():
    from scripts.council_convening import corpus

    context = _context()
    vector = _vector("asg-retry-order-conflict-before-head-moved-refuse")
    fresh = corpus.adjudicate(_without_live_snapshots(vector), context)
    assert (fresh.outcome, fresh.refusal) == ("refuse", "candidate_head_moved")
    conflict = corpus.adjudicate(vector, context)
    assert (conflict.outcome, conflict.refusal) == ("refuse", "convening_conflict")


def test_a_fresh_admission_derives_no_convening_id():
    # `convening_id` is the consumer's, issued when it writes the snapshot, so a
    # record that admits fresh has none; only a returned snapshot names one.
    from scripts.council_convening import corpus

    outcome = corpus.adjudicate(
        _vector("asg-retry-same-council-other-pin-not-conflict-accept"), _context())
    assert outcome.outcome == "accept"
    assert "convening_id" not in outcome.derived
    assert "snapshot_digest" not in outcome.derived


@pytest.mark.parametrize("strip", [
    pytest.param(lambda env: env.pop("issued"), id="no-issued"),
    pytest.param(lambda env: env["issued"].pop("live_snapshots"), id="issued-without-live"),
])
def test_an_admission_vector_without_live_snapshots_has_no_live_snapshot(strip):
    # Reading 3, now in conformance-corpus.md beside "absent, not empty": an
    # absent `environment.issued.live_snapshots` reads as "the consumer holds no
    # live snapshot". The consumer's run of the shared commission vectors and
    # every Phase 2 admission vector rely on it.
    from scripts.council_convening import corpus

    vector = copy.deepcopy(_vector("asg-retry-identical-returns-snapshot-accept"))
    strip(vector["environment"])
    outcome = corpus.adjudicate(vector, _context())
    assert outcome.outcome == "accept"
    assert "convening_id" not in outcome.derived
    assert "snapshot_digest" not in outcome.derived


# --- the live snapshots are oracle data, and must be sound (pre-review M2, L2) -------
#
# A vector whose live snapshots are no consumer's state cannot be adjudicated. It
# is a harness error, which the corpus reports as a vector input error, exactly
# as it reports every other oracle datum a vector cannot supply (Phase 2's
# reading 8). It is never a refusal and never a traceback.


def _live_snapshots_error(mutate) -> str:
    from scripts.council_convening import resolution

    vector = copy.deepcopy(_vector("asg-retry-identical-returns-snapshot-accept"))
    mutate(vector["environment"]["issued"]["live_snapshots"])
    oracles = resolution.VectorOracles(vector["environment"])
    with pytest.raises(resolution.HarnessError) as caught:
        oracles.live_snapshots()
    return str(caught.value)


def _second_with_the_same_key(live_list):
    conflicting = copy.deepcopy(live_list[0])
    conflicting["convening"]["packet_refs"] = ["example-org/example-app#41"]
    conflicting["convening_id"] = "convening-0000"
    conflicting["convening_digest"] = digest_of(conflicting["convening"])
    for item in conflicting["assignments"]:
        item["convening_id"] = "convening-0000"
        item["convening_digest"] = digest_of(conflicting["convening"])
    live_list.insert(0, conflicting)


def test_two_live_snapshots_with_one_convening_key_are_a_harness_error():
    message = _live_snapshots_error(_second_with_the_same_key)
    assert "convening key" in message


def _surrogate(live_list):
    live_list[0]["convening"]["packet_refs"] = ["packet/\ud800"]


@pytest.mark.parametrize("mutate", [
    pytest.param(lambda live: live[0].update(convening_id="bad id\n"),
                 id="convening_id-grammar"),
    pytest.param(lambda live: live[0].pop("assignments"), id="assignments-missing"),
    pytest.param(lambda live: live[0]["assignments"].pop(), id="assignment-set-short"),
    pytest.param(lambda live: live[0]["convening_digest"].update(
        value="sha256:" + "0" * 64), id="digest-does-not-recompute"),
    pytest.param(_surrogate, id="not-canonicalizable"),
    pytest.param(lambda live: live.append("not a snapshot"), id="not-an-object"),
])
def test_a_live_snapshot_that_is_not_a_sound_snapshot_is_a_harness_error(mutate):
    message = _live_snapshots_error(mutate)
    assert "live snapshot" in message
    assert "bad id" not in message and "\ud800" not in message


def test_the_corpus_reports_an_unsound_live_snapshot_as_a_vector_input_error():
    from scripts.council_convening import corpus

    vector = copy.deepcopy(_vector("asg-retry-identical-returns-snapshot-accept"))
    _surrogate(vector["environment"]["issued"]["live_snapshots"])
    with pytest.raises(corpus.VectorInputError):
        corpus.adjudicate(vector, _context())


# --- the area is its builder's output (pre-review L6) ---------------------------------


def test_the_assignment_area_is_exactly_what_its_builder_writes():
    # Rebuild with `python3 -m tests.council_convening.assignment_vectors`, then
    # regenerate the index. This fails when Phase 2 edits the base vector the
    # retry vectors copy, or when a fixture moves, until the area is rebuilt.
    from . import assignment_vectors

    assert assignment_vectors.drift() == []


def _base():
    from . import assignment_vectors

    return assignment_vectors.base_vector()


def test_every_retry_vector_copies_phase_2s_base_vector():
    from . import assignment_vectors

    base = _base()
    record, environment = base["inputs"]["record"], base["environment"]
    allowed = [environment, assignment_vectors.tip_moved(environment),
               assignment_vectors.head_moved(environment)]
    retry = sorted((VECTORS_DIR / "assignment").glob("asg-retry-*.json"))
    assert len(retry) == 12
    for path in retry:
        vector = json.loads(path.read_text(encoding="utf-8"))
        env = copy.deepcopy(vector["environment"])
        live_list = env.pop("issued")["live_snapshots"]
        assert env in allowed, path.name
        for live_snapshot in live_list:
            convening = live_snapshot["convening"]
            same_key = (convening["council_id"], convening["subject_pin"]) == (
                record["council_id"], record["subject_pin"])
            if same_key:
                # A live snapshot with the record's key embeds the base record.
                assert convening == record, path.name
            else:
                # One for another key differs from it in the key alone.
                other = copy.deepcopy(convening)
                other["council_id"] = record["council_id"]
                other["subject_pin"] = record["subject_pin"]
                other["required_seats_provenance"]["candidate"]["head_sha"] = (
                    record["required_seats_provenance"]["candidate"]["head_sha"])
                assert other == record, path.name


def test_the_snapshot_half_is_shared_and_the_retry_vectors_are_consumer_only():
    # Reading 4, a reading the owner can overrule at PR review. The snapshot half
    # reads no oracle, and 049 T015b implements the provider half of these
    # encodings, so the producer runs it too. Only the consumer holds live
    # snapshots.
    for path in sorted((VECTORS_DIR / "assignment").glob("*.json")):
        vector = json.loads(path.read_text(encoding="utf-8"))
        if "snapshot" in vector["inputs"]:
            assert vector["applies_to"] == ["producer", "consumer"], path.name
            assert "environment" not in vector, path.name
        else:
            assert path.name.startswith("asg-retry-"), path.name
            assert vector["applies_to"] == ["consumer"], path.name
