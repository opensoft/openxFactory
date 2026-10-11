"""The builder of the corpus's `assignment` area (feature 035, Phase 3, T036).

Every vector under `contracts/council-convening/conformance/vectors/assignment/`
is this module's output, byte for byte, and nothing else is there.
`test_assignments.py` holds the corpus to that (pre-review L6, 2026-10-09).
Regenerate, then regenerate the index, from the repository root:

    python3 -m tests.council_convening.assignment_vectors          # write
    python3 -m tests.council_convening.assignment_vectors --check  # compare
    python3 -m scripts.council_convening.generate

TWO HALVES, two sources.

* The SNAPSHOT HALF (boundary `admission`, `inputs.snapshot`) is built from
  `assignment_fixtures.py`, which these tests share. It reads no oracle, so it
  is shared, `applies_to: [producer, consumer]`: 049 T015b implements the
  provider half of the snapshot and assignment encodings, and runs the same E4
  order over the same bytes. That is a reading the owner can overrule at PR
  review (conformance-corpus § How each side runs a shared vector, dated note
  of 2026-10-09).
* The RETRY VECTORS (boundary `admission`, `inputs.record` with
  `environment.issued.live_snapshots`) are COPIES of Phase 2's
  `admission-accept-conditional-seat-not-held`: its record and its whole
  admission environment, with only the mutations named below, plus the live
  snapshots. They are consumer-only, because only the consumer holds live
  snapshots. When Phase 2 edits that vector, `test_assignments.py` fails until
  this builder is rerun.

INDEPENDENCE. Every expected outcome here is written by hand, as each case's
`refuse(...)` or `accept(...)`, never read back from the reference
implementation (research R4). An accept's derived values are computed from
the fixtures with `canonical.digest`, which is why they carry
`derived_origin: generated`. The one implementation function used is
`corpus.dump_json`, the corpus's byte format.

EVERY HOLDER'S `binding_ref` comes from `holder_binding_ref` in
`assignment_fixtures.py`: one binding per seat, since E4 step 7 refuses a
binding repeated across seats (Brett Heap, 2026-10-11T00:19:34Z, "Refuse at
freeze (Recommended)").
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

from .assignment_fixtures import (
    LEGACY,
    REPLACEMENT,
    convening_record,
    digest_of,
    snapshot,
)
from .conftest import REPO_ROOT, VECTORS

from scripts.signed_execution_chain import canonical  # noqa: E402  (after conftest)

AREA = VECTORS / "assignment"
EVALUATION_TIME = "2026-10-09T01:00:00Z"
BOTH_SIDES = ("producer", "consumer")
CONSUMER = ("consumer",)

#: Phase 2's admission accept vector, which every retry vector copies.
BASE_VECTOR = VECTORS / "resolution" / "admission-accept-conditional-seat-not-held.json"

#: The governed source the tip-moved retry vector changes at the tip.
TIP_MOVED_SOURCE = ":rules/councils/review-council.yaml"

WRONG_DIGEST = {"construction": "xfc-jcs-sha256-1", "subject": "council_convening",
                "value": "sha256:" + "0" * 64}


# --- the vector envelope ---------------------------------------------------------


def _vector(case_id, *, inputs, expected, requirement_ids, applies_to,
            environment=None) -> dict:
    value = {
        "schema_version": 1,
        "kind": "openxfactory-council-convening-conformance-vector",
        "case_id": case_id,
        "area": "assignment",
        "boundary": "admission",
        "applies_to": list(applies_to),
        "requirement_ids": list(requirement_ids),
        "evaluation_time": EVALUATION_TIME,
        "inputs": inputs,
        "expected": expected,
    }
    if environment is not None:
        value["environment"] = environment
    return value


def accept(derived) -> dict:
    return {"outcome": "accept", "refusal": None, "findings": [], "derived": derived,
            "derived_origin": "generated"}


def refuse(code) -> dict:
    return {"outcome": "refuse", "refusal": code, "findings": [], "derived": {},
            "derived_origin": "hand"}


def snapshot_derived(snap) -> dict:
    """An accepted snapshot's known answers: its roster and its digest."""
    return {"required_seats": list(snap["convening"]["required_seats"]),
            "convening_digest": digest_of(snap["convening"])}


# --- records the snapshot half embeds ------------------------------------------------


def three_seat_record() -> dict:
    record = convening_record(required_seats=["seat-a", "seat-b", "seat-c"])
    record["required_seats_provenance"]["standing_seats"] = ["seat-a", "seat-b", "seat-c"]
    return record


def conditional_record(*, held=True, seat="seat-c") -> dict:
    """Two standing seats and one `pr_facts` condition, held, that adds `seat`.
    It passes every offline E2 rule."""
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


def rule_conditional_record(touched=("policy/authority/approvers.yaml",
                                     "policy/readme.md")) -> dict:
    """Two standing seats and one held `rule_facts` condition, read from the
    candidate's subject, that adds seat-c: the gate-rules shape."""
    record = three_seat_record()
    prov = record["required_seats_provenance"]
    prov["standing_seats"] = ["seat-a", "seat-b"]
    prov["candidate"]["subject_path"] = "policy/packets/change-17.yaml"
    prov["conditions"] = [{
        "seat": "seat-c", "predicate": "rule_touches_security_posture",
        "input_contract": "rule_facts",
        "parameters": {"security_surfaces": ["policy/authority/**"]}, "held": True}]
    prov["fact_sources"] = [{"input_contract": "rule_facts", "source": "candidate_subject"}]
    prov["consumed_facts"] = {"rule_facts": {"rule_touched_paths": list(touched)}}
    return record


def renumber(snap) -> dict:
    """Give every assignment a distinct id and holder, so a vector whose defect is
    the seat set carries no second defect."""
    for index, item in enumerate(snap["assignments"]):
        item["assignment_id"] = f"assignment-{index}"
        item["holder"]["principal_ref"] = f"principal-{index}"
    return snap


# --- the snapshot half -------------------------------------------------------------


def snapshot_cases() -> list[dict]:
    cases = []

    def add(case_id, snap, expected, reqs=("FR-005", "SC-002")):
        cases.append(_vector(case_id, inputs={"snapshot": snap,
                                              "selected_protocol": REPLACEMENT},
                             expected=expected, requirement_ids=reqs,
                             applies_to=BOTH_SIDES))

    base = snapshot()
    add("asg-snapshot-accept", base, accept(snapshot_derived(base)),
        ("FR-004", "FR-005", "FR-006", "SC-002"))

    three = snapshot(three_seat_record())
    add("asg-snapshot-accept-three-seats", three, accept(snapshot_derived(three)))

    # A roster with a held condition's seat: the offline roster rules compute it
    # from the standing seats and the held conditions (pre-review M3).
    held = snapshot(conditional_record())
    add("asg-snapshot-accept-conditional-seat-held", held, accept(snapshot_derived(held)),
        ("FR-004", "FR-005", "SC-002"))

    # The ruled ceiling, OPEN-1: 21600 s accepted; 21601, zero, negative refused.
    for case_id, expires_at, expected in [
        ("asg-ceiling-exactly-21600-seconds-accept", "2026-10-09T06:00:00Z", None),
        ("asg-ceiling-21601-seconds-refuse", "2026-10-09T06:00:01Z", "assignment_malformed"),
        ("asg-ceiling-zero-lifetime-refuse", "2026-10-09T00:00:00Z", "assignment_malformed"),
        ("asg-ceiling-negative-lifetime-refuse", "2026-10-08T23:59:59Z", "assignment_malformed"),
    ]:
        snap = snapshot()
        snap["assignments"][1]["expires_at"] = expires_at
        add(case_id, snap,
            accept(snapshot_derived(snap)) if expected is None else refuse(expected),
            ("FR-005", "FR-007"))

    # Lifetimes below the ceiling are accepted too, so a check of
    # `lifetime == 21600` cannot pass the corpus (pre-review L1).
    for case_id, expires_at in [
        ("asg-lifetime-one-second-accept", "2026-10-09T00:00:01Z"),
        ("asg-lifetime-one-hour-accept", "2026-10-09T01:00:00Z"),
    ]:
        snap = snapshot()
        snap["assignments"][1]["expires_at"] = expires_at
        add(case_id, snap, accept(snapshot_derived(snap)), ("FR-005", "FR-007"))

    # permitted_operations: one of exactly three lists.
    for case_id, ops, expected in [
        ("asg-operations-registration-only-accept", ["seat_key_registration"], None),
        ("asg-operations-return-only-accept", ["seat_return"], None),
        ("asg-operations-empty-refuse", [], "assignment_malformed"),
        ("asg-operations-repeated-refuse", ["seat_return", "seat_return"], "assignment_malformed"),
        ("asg-operations-reordered-refuse", ["seat_return", "seat_key_registration"],
         "assignment_malformed"),
        ("asg-operations-unknown-refuse", ["seat_execution"], "assignment_malformed"),
    ]:
        snap = snapshot()
        snap["assignments"][0]["permitted_operations"] = ops
        add(case_id, snap,
            accept(snapshot_derived(snap)) if expected is None else refuse(expected),
            ("FR-005", "FR-007"))

    # Shapes.
    snap = snapshot()
    del snap["admitted_at"]
    add("asg-snapshot-malformed-missing-member-refuse", snap, refuse("snapshot_malformed"))

    snap = snapshot()
    snap["convening"]["unexpected"] = "x"
    add("asg-snapshot-malformed-convening-fails-e2-refuse", snap, refuse("snapshot_malformed"))

    snap = snapshot()
    snap["convening_id"] = "convening-0001\n"
    add("asg-snapshot-malformed-trailing-newline-refuse", snap, refuse("snapshot_malformed"))

    # The embedded record's own offline rules (pre-review M3): E2 step 2's
    # structural rules and the offline roster rules of steps 11 and 12. Each
    # snapshot is otherwise sound: its digest recomputes over the record it
    # embeds, and it carries one assignment per required seat.
    for case_id, record in _inadmissible_records():
        add(case_id, renumber(snapshot(record)), refuse("snapshot_malformed"),
            ("FR-004", "FR-005", "SC-002"))

    snap = snapshot()
    del snap["assignments"][1]["holder"]
    add("asg-assignment-malformed-missing-holder-refuse", snap, refuse("assignment_malformed"))

    snap = snapshot()
    snap["assignments"][0]["holder"]["principal_kind"] = "shared_token"
    add("asg-assignment-malformed-principal-kind-refuse", snap, refuse("assignment_malformed"),
        ("FR-005", "FR-006"))

    # The digest recomputes over the admitted record.
    snap = snapshot()
    snap["convening"]["packet_refs"] = ["packet/alpha-2"]
    add("asg-digest-convening-edited-refuse", snap, refuse("digest_construction_mismatch"))

    snap = snapshot()
    snap["convening_digest"] = copy.deepcopy(WRONG_DIGEST)
    for item in snap["assignments"]:
        item["convening_digest"] = copy.deepcopy(WRONG_DIGEST)
    add("asg-digest-value-wrong-refuse", snap, refuse("digest_construction_mismatch"))

    # One assignment per required seat, in roster order.
    for case_id, seats in [
        ("asg-set-extra-refuse", ["seat-a", "seat-b", "seat-c"]),
        ("asg-set-missing-refuse", ["seat-a"]),
        ("asg-set-reordered-refuse", ["seat-b", "seat-a"]),
        ("asg-set-same-count-wrong-seat-refuse", ["seat-a", "seat-c"]),
    ]:
        add(case_id, renumber(snapshot(seats=seats)), refuse("assignment_set_mismatch"))

    # Each of the five convening members E4 step 5 names (pre-review M4 added
    # the digest).
    for case_id, member, value in [
        ("asg-set-member-convening-id-differs-refuse", "convening_id", "convening-0002"),
        ("asg-set-member-protocol-differs-refuse", "protocol", LEGACY),
        ("asg-set-member-council-id-differs-refuse", "council_id", "council-beta"),
        ("asg-set-member-convening-digest-differs-refuse", "convening_digest",
         {"construction": "xfc-jcs-sha256-1", "subject": "council_convening",
          "value": "sha256:" + "4" * 64}),
    ]:
        snap = snapshot()
        snap["assignments"][1][member] = value
        add(case_id, snap, refuse("assignment_set_mismatch"))

    snap = snapshot()
    snap["assignments"][1]["candidate"]["pull_number"] = 8
    add("asg-set-member-candidate-differs-refuse", snap, refuse("assignment_set_mismatch"))

    snap = snapshot()
    snap["assignments"][1]["assignment_id"] = snap["assignments"][0]["assignment_id"]
    add("asg-duplicate-assignment-id-refuse", snap, refuse("assignment_duplicate"))

    snap = snapshot()
    snap["assignments"][1]["holder"]["principal_ref"] = (
        snap["assignments"][0]["holder"]["principal_ref"])
    add("asg-shared-holder-refuse", snap, refuse("assignment_shared_holder"),
        ("FR-005", "FR-006", "SC-002"))

    # One binding on two seats, with distinct principals (Brett Heap,
    # 2026-10-11T00:19:34Z, "Refuse at freeze (Recommended)"): the same code.
    snap = snapshot()
    snap["assignments"][1]["holder"]["binding_ref"] = (
        snap["assignments"][0]["holder"]["binding_ref"])
    add("asg-shared-binding-refuse", snap, refuse("assignment_shared_holder"),
        ("FR-005", "FR-006", "FR-007", "SC-002"))

    # The E4 order, each adjacent pair pinned by a two-defect record.
    snap = snapshot()
    snap["protocol"] = LEGACY
    snap["unexpected"] = True
    add("asg-order-classification-before-shape-refuse", snap, refuse("legacy_protocol_refused"),
        ("FR-005", "FR-011"))

    snap = snapshot()
    del snap["admitted_at"]
    snap["assignments"][0]["expires_at"] = "2026-10-09T06:00:01Z"
    add("asg-order-snapshot-before-assignment-malformed-refuse", snap,
        refuse("snapshot_malformed"))

    # The embedded record's roster rules are step 2's too.
    record = convening_record(required_seats=["seat-a", "seat-b"])
    record["required_seats_provenance"]["standing_seats"] = ["seat-a"]
    snap = snapshot(record)
    snap["assignments"][0]["expires_at"] = "2026-10-09T06:00:01Z"
    add("asg-order-convening-roster-before-assignment-malformed-refuse", snap,
        refuse("snapshot_malformed"), ("FR-004", "FR-005"))

    snap = snapshot(seats=["seat-b", "seat-a"])
    snap["convening_digest"]["value"] = "sha256:" + "0" * 64
    snap["assignments"][1]["expires_at"] = "2026-10-09T06:00:01Z"
    add("asg-order-assignment-malformed-before-digest-refuse", snap,
        refuse("assignment_malformed"))

    # `value_not_canonicalizable` sits after step 3 and before step 4, the place
    # E2 step 2 gives it (reading 1; data-model E4, dated note of 2026-10-09).
    # A lone surrogate passes every grammar a packet reference has, so only the
    # canonicalizability pre-check can refuse it before the digest is compared.
    snap = snapshot()
    snap["convening"]["packet_refs"] = ["packet/\ud800"]
    snap["convening_digest"] = copy.deepcopy(WRONG_DIGEST)
    for item in snap["assignments"]:
        item["convening_digest"] = copy.deepcopy(WRONG_DIGEST)
    add("asg-order-not-canonicalizable-before-digest-refuse", snap,
        refuse("value_not_canonicalizable"), ("FR-005",))

    snap = snapshot()
    snap["convening"]["packet_refs"] = ["packet/\ud800"]
    snap["convening_digest"] = copy.deepcopy(WRONG_DIGEST)
    for item in snap["assignments"]:
        item["convening_digest"] = copy.deepcopy(WRONG_DIGEST)
    snap["assignments"][1]["expires_at"] = "2026-10-09T06:00:01Z"
    add("asg-order-assignment-malformed-before-not-canonicalizable-refuse", snap,
        refuse("assignment_malformed"), ("FR-005",))

    snap = renumber(snapshot(seats=["seat-b", "seat-a"]))
    snap["convening_digest"]["value"] = "sha256:" + "0" * 64
    add("asg-order-digest-before-set-refuse", snap, refuse("digest_construction_mismatch"))

    snap = snapshot(seats=["seat-a", "seat-b", "seat-c"])
    snap["assignments"][2]["assignment_id"] = snap["assignments"][0]["assignment_id"]
    add("asg-order-set-before-duplicate-refuse", snap, refuse("assignment_set_mismatch"))

    snap = snapshot()
    snap["assignments"][1]["assignment_id"] = snap["assignments"][0]["assignment_id"]
    snap["assignments"][1]["holder"]["principal_ref"] = (
        snap["assignments"][0]["holder"]["principal_ref"])
    add("asg-order-duplicate-before-shared-holder-refuse", snap, refuse("assignment_duplicate"))

    # The shared binding is step 7's, after the duplicate check of step 6.
    snap = snapshot()
    snap["assignments"][1]["assignment_id"] = snap["assignments"][0]["assignment_id"]
    snap["assignments"][1]["holder"]["binding_ref"] = (
        snap["assignments"][0]["holder"]["binding_ref"])
    add("asg-order-duplicate-before-shared-binding-refuse", snap,
        refuse("assignment_duplicate"), ("FR-005", "FR-006"))

    # Inside step 7, every repeated principal is checked before any repeated
    # binding. Both are `assignment_shared_holder`, so this vector pins the pair's
    # code; which repeat is named first is the refusal's member, which no vector
    # compares, and `test_assignments.py` pins it.
    snap = snapshot(three_seat_record())
    items = snap["assignments"]
    items[1]["holder"]["binding_ref"] = items[0]["holder"]["binding_ref"]
    items[2]["holder"]["principal_ref"] = items[0]["holder"]["principal_ref"]
    add("asg-order-shared-principal-before-shared-binding-refuse", snap,
        refuse("assignment_shared_holder"), ("FR-005", "FR-006"))
    return cases


def _inadmissible_records():
    """(case_id, record) for each embedded record an offline E2 rule refuses."""
    # Step 2: sources out of bytewise path order.
    record = convening_record()
    record["required_seats_provenance"]["governed"]["sources"] = [
        {"kind": "file", "path": "rules/zeta.yaml", "sha256": "sha256:" + "3" * 64},
        {"kind": "file", "path": "rules/alpha.yaml", "sha256": "sha256:" + "3" * 64}]
    yield "asg-snapshot-malformed-convening-sources-unsorted-refuse", record

    # Step 2: `class_inputs` without `matched_class`.
    record = convening_record()
    record["required_seats_provenance"]["class_inputs"] = {
        "repository": "example-owner/example-candidate", "head_ref": "feature/alpha"}
    yield "asg-snapshot-malformed-convening-class-inputs-without-matched-class-refuse", record

    # Step 2: a consumed `changed_paths` not in bytewise order (Brett Heap,
    # 2026-10-09T17:35:34Z, "Sorted and unique (Recommended)").
    record = conditional_record()
    record["required_seats_provenance"]["consumed_facts"]["pr_facts"]["changed_paths"] = [
        "src/app/main.py", "README.md"]
    yield "asg-snapshot-malformed-convening-changed-paths-unsorted-refuse", record

    # Step 2: a consumed `rule_touched_paths` out of bytewise order, or repeated
    # (Brett Heap, 2026-10-11T00:19:34Z, "Same rule, in PR-3 (Recommended)").
    yield ("asg-snapshot-malformed-convening-rule-touched-paths-unsorted-refuse",
           rule_conditional_record(("policy/readme.md", "policy/authority/approvers.yaml")))
    yield ("asg-snapshot-malformed-convening-rule-touched-paths-repeated-refuse",
           rule_conditional_record(("policy/authority/approvers.yaml",
                                    "policy/authority/approvers.yaml")))

    # Step 11's offline half: a held condition with no seat.
    record = conditional_record(seat=None)
    yield "asg-snapshot-malformed-convening-held-seat-unbound-refuse", record

    # Step 12: an empty roster, so a zero-seat snapshot with no assignments.
    record = convening_record(required_seats=[])
    record["required_seats_provenance"]["standing_seats"] = []
    yield "asg-snapshot-malformed-convening-zero-seats-refuse", record

    # Step 12: a repeated seat.
    record = convening_record(required_seats=["seat-a", "seat-a"])
    record["required_seats_provenance"]["standing_seats"] = ["seat-a"]
    yield "asg-snapshot-malformed-convening-roster-duplicate-seat-refuse", record

    # Step 12: a roster that is not the standing seats and the held seats.
    record = convening_record(required_seats=["seat-a", "seat-b"])
    record["required_seats_provenance"]["standing_seats"] = ["seat-a"]
    yield "asg-snapshot-malformed-convening-roster-mismatch-refuse", record


# --- retry identity and once-per-pin (E2 step A3) -------------------------------------


def base_vector(path: Path = BASE_VECTOR) -> dict:
    """Phase 2's admission accept vector: a record that admits fresh, and the full
    admission environment it admits under."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _retry(case_id, record, environment, live, expected, reqs) -> dict:
    environment = copy.deepcopy(environment)
    environment["issued"] = {"live_snapshots": live}
    return _vector(case_id, inputs={"record": record, "selected_protocol": REPLACEMENT},
                   expected=expected, requirement_ids=reqs, applies_to=CONSUMER,
                   environment=environment)


def tip_moved(environment) -> dict:
    """The base environment with one governed source changed at the tip."""
    moved = copy.deepcopy(environment)
    for key, entry in moved["governed"].items():
        if key.endswith(TIP_MOVED_SOURCE):
            entry["tip_sha256"] = "sha256:" + "e" * 64
    return moved


def head_moved(environment) -> dict:
    """The base environment with the candidate's live head moved."""
    moved = copy.deepcopy(environment)
    for key in moved["live_heads"]:
        moved["live_heads"][key] = "f" * 40
    return moved


def retry_cases(base_path: Path = BASE_VECTOR) -> list[dict]:
    base = base_vector(base_path)
    record = base["inputs"]["record"]
    env = base["environment"]
    live_one = snapshot(record, convening_id="convening-0001")
    fresh = accept({"required_seats": list(record["required_seats"]),
                    "convening_digest": digest_of(record)})
    # A returned snapshot names its consumer-issued id and the digest of the
    # whole snapshot returned, so the same assignments are compared, not only
    # the same id (pre-review M1; conformance-corpus § derived, 2026-10-09).
    returned = accept({"required_seats": list(record["required_seats"]),
                       "convening_digest": digest_of(record),
                       "convening_id": "convening-0001",
                       "snapshot_digest": canonical.digest(live_one)})

    other_pin = copy.deepcopy(record)
    other_pin["subject_pin"] = "9" * 40
    other_pin["required_seats_provenance"]["candidate"]["head_sha"] = "9" * 40
    other_council = copy.deepcopy(record)
    other_council["council_id"] = "other-council"
    live_other_pin = snapshot(other_pin, convening_id="convening-0009")
    live_other_council = snapshot(other_council, convening_id="convening-0008")
    cases = []

    # An identical retry returns the live snapshot unchanged.
    cases.append(_retry("asg-retry-identical-returns-snapshot-accept",
                        copy.deepcopy(record), env, [live_one], returned,
                        ("FR-004", "FR-005", "SC-002")))

    # ... even after a governed source changed at the tip (without the live
    # snapshot this environment refuses rule_superseded) ...
    cases.append(_retry("asg-retry-identical-after-tip-moved-accept",
                        copy.deepcopy(record), tip_moved(env), [live_one], returned,
                        ("FR-004", "FR-005")))

    # ... and after the live head moved (without it: candidate_head_moved).
    cases.append(_retry("asg-retry-identical-after-head-moved-accept",
                        copy.deepcopy(record), head_moved(env), [live_one], returned,
                        ("FR-004", "FR-005")))

    # Once-per-pin never pre-empts an identical retry. The identical snapshot
    # shares the record's key, and the snapshots for other keys are listed
    # first. At most one live snapshot has any one key: once-per-pin allows
    # no more (pre-review M2).
    cases.append(_retry(
        "asg-retry-identical-not-pre-empted-by-once-per-pin-accept",
        copy.deepcopy(record), env, [live_other_pin, live_other_council, live_one],
        returned, ("FR-004", "SC-002")))

    # A different record for the same (protocol, council_id, subject_pin).
    for case_id, mutate in [
        ("asg-retry-conflict-packet-refs-refuse",
         lambda r: r.update(packet_refs=["example-org/example-app#41"])),
        ("asg-retry-conflict-pull-number-only-refuse",
         lambda r: r["required_seats_provenance"]["candidate"].update(pull_number=43)),
        ("asg-retry-conflict-subject-path-only-refuse",
         lambda r: r["required_seats_provenance"]["candidate"].update(
             subject_path="rules/packet.yaml")),
    ]:
        resent = copy.deepcopy(record)
        mutate(resent)
        cases.append(_retry(case_id, resent, env, [live_one],
                            refuse("convening_conflict"), ("FR-004", "SC-002")))

    # The same council at another pin, or another council at this pin, is not a
    # conflict: the record admits fresh.
    cases.append(_retry("asg-retry-same-council-other-pin-not-conflict-accept",
                        copy.deepcopy(record), env, [live_other_pin], fresh, ("FR-004",)))
    cases.append(_retry("asg-retry-other-council-same-pin-not-conflict-accept",
                        copy.deepcopy(record), env, [live_other_council], fresh,
                        ("FR-004",)))

    # The order around A3.
    malformed = copy.deepcopy(record)
    malformed["unexpected"] = True
    cases.append(_retry("asg-retry-order-shape-before-conflict-refuse", malformed,
                        env, [live_one], refuse("convening_malformed"), ("FR-004",)))

    secret = copy.deepcopy(record)
    secret["packet_refs"] = [{"$parts": ["gh", "p_" + "A" * 24]}]
    cases.append(_retry("asg-retry-order-conflict-before-secret-refuse", secret,
                        env, [live_one], refuse("convening_conflict"), ("FR-002", "FR-004")))

    conflict_and_drift = copy.deepcopy(record)
    conflict_and_drift["packet_refs"] = ["example-org/example-app#41"]
    cases.append(_retry("asg-retry-order-conflict-before-head-moved-refuse",
                        conflict_and_drift, head_moved(env), [live_one],
                        refuse("convening_conflict"), ("FR-004",)))
    return cases


# --- the area as files -----------------------------------------------------------------


def build() -> dict[str, bytes]:
    """`{file name: bytes}` for every vector of the area, in the corpus's format."""
    from scripts.council_convening import corpus

    cases = snapshot_cases() + retry_cases()
    names = [f"{case['case_id']}.json" for case in cases]
    if len(names) != len(set(names)):
        raise ValueError("two assignment vectors share a case_id")
    return {name: corpus.dump_json(case) for name, case in zip(names, cases)}


def drift(built: dict[str, bytes] | None = None, area: Path = AREA) -> list[str]:
    """The file names whose committed bytes differ from the builder's, or that
    exist on one side only, sorted."""
    built = build() if built is None else built
    committed = {path.name: path.read_bytes() for path in area.glob("*.json")}
    return sorted(name for name in set(built) | set(committed)
                  if built.get(name) != committed.get(name))


def main(argv: list[str]) -> int:
    built = build()
    if "--check" in argv:
        stale = drift(built)
        for name in stale:
            print(f"drift: vectors/assignment/{name}")
        print(f"{len(built)} vectors built, {len(stale)} differ")
        return 1 if stale else 0
    AREA.mkdir(parents=True, exist_ok=True)
    for path in AREA.glob("*.json"):
        if path.name not in built:
            path.unlink()
    for name, raw in built.items():
        (AREA / name).write_bytes(raw)
    print(f"wrote {len(built)} vectors to "
          f"{(AREA.relative_to(REPO_ROOT)).as_posix()}; now run "
          f"python3 -m scripts.council_convening.generate")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
