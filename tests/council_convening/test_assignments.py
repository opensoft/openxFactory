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

import pytest

from scripts.council_convening import assignments
from scripts.council_convening.records import Refused

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


def test_a_lone_assignment_is_checked_against_E5_alone():
    convening = convening_record()
    assignments.check_assignment(assignment(convening, "convening-0001", "seat-a"))
    broken = assignment(convening, "convening-0001", "seat-a")
    broken.pop("seat_id")
    assert refusal(assignments.check_assignment, broken) == "assignment_malformed"


# --- the ruled ceiling (OPEN-1) ---------------------------------------------------------


@pytest.mark.parametrize("expires_at, outcome", [
    pytest.param("2026-10-09T06:00:00Z", None, id="exactly-21600-seconds-accepted"),
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


def test_a_shared_binding_is_not_a_shared_holder():
    # The binding names the workflow configuration both seat jobs run under; the
    # holder is the principal. Two seats may share the first, never the second.
    value = snapshot()
    assert value["assignments"][0]["holder"]["binding_ref"] == (
        value["assignments"][1]["holder"]["binding_ref"])
    check(value)


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
    # The identical-retry test runs over every live snapshot before the
    # once-per-pin test runs over any, so a conflicting live snapshot listed
    # first cannot turn an identical retry into a conflict.
    record = convening_record()
    conflicting = copy.deepcopy(record)
    conflicting["packet_refs"] = ["packet/alpha-0"]
    first = live(conflicting, convening_id="convening-0000")
    identical = live(record, convening_id="convening-0001")
    other_pin = live(convening_record(subject_pin="6" * 40), convening_id="convening-0009")
    returned = assignments.retry_identity(copy.deepcopy(record), [other_pin, first, identical])
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
