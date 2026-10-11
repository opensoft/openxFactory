"""Frozen assignments and retry identity (data-model E4, E5 and E2 step A3).

T039, feature 035 Phase 3. Written from the family's own specification
(`specs/035-renew-resolved-council-protocol/data-model.md` E2, E4 and E5) and
from nothing else: no producer or consumer code is copied here (research R4).

THREE THINGS LIVE HERE.

* `snapshot_outcome` is the snapshot half of `admission`, the whole E4 order
  from classification on, answered as a `records.Outcome`. `check_snapshot` is
  the same order after classification, steps 2 to 7, raising `Refused`. Step 2
  judges the embedded record by its E2 schema and by the E2 rules that need no
  oracle and judge the record alone: step 2's structural rules and the offline
  roster rules of steps 11 and 12 (pre-review M3; data-model E4, dated note).
* `check_assignment` judges one assignment against E5 alone, including the
  ruled lifetime ceiling. `check_lone_assignment` adds the canonicalizability
  pre-check, for `check` on an assignment outside its snapshot.
* `retry_identity` is E2 step A3: retry identity, then once-per-pin, over the
  consumer's live snapshots. The Phase 2 admission order calls it right after E2
  step 2 (T040).

BRETT HEAP'S RULINGS OF 2026-10-08 ENCODED HERE.

* OPEN-1, "600 s challenge, 6 h assignment (Recommended)": an assignment lives
  more than 0 and at most 21600 seconds. That is the CONTRACT ceiling, which
  `seat-assignment.schema.yaml` declares as `$defs/lifetime_ceiling_seconds`
  and this module reads from there. A consumer's tighter value applies when it
  ISSUES an assignment; verification and the corpus use the ceiling (R12).
* Retry identity runs after classification, shape and binding, and before every
  check that reads something that can drift; an identical retry returns the
  same snapshot (US1 scenario 4; 025 FR-006; R21).
* Once-per-pin is `convening_conflict`, keyed on `(protocol, council_id,
  subject_pin)`, 025's once-per-pin key with the protocol added.
* "Byte-identical" means equal `xfc-jcs-sha256-1` canonical bytes.

BRETT HEAP'S RULING OF 2026-10-11T00:19:34Z, "Refuse at freeze (Recommended)":
E4 step 7 refuses a `holder.binding_ref` repeated across seats as
`assignment_shared_holder`, after every repeated `principal_ref`, so each seat
holder has its own E10 binding.

ONE ORDER POSITION THE DATA MODEL LEAVES IMPLICIT. E4 names no step for
`value_not_canonicalizable`, and § Shared definitions says such a value "is
refused ... before any digest is taken". This module runs that pre-check after
every shape check (E4 steps 2 and 3) and before the digest (step 4), the
position E2 step 2 gives it ("Shape ... Then `value_not_canonicalizable`").

Refusal messages name members and never echo a value.
"""

from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
from typing import Any, Iterable, Mapping

from ..signed_execution_chain import canonical
from . import classification, records
from .records import Outcome, Refused

SNAPSHOT_KIND = "xfactory_council_convening_snapshot"
ASSIGNMENT_KIND = "xfactory_council_seat_assignment"
SNAPSHOT_SCHEMA = "convening-snapshot.schema.yaml"
ASSIGNMENT_SCHEMA = "seat-assignment.schema.yaml"
SNAPSHOT_SCHEMA_ID = records.ID_BASE + SNAPSHOT_SCHEMA
ASSIGNMENT_SCHEMA_ID = records.ID_BASE + ASSIGNMENT_SCHEMA

#: Brett Heap's OPEN-1 ruling, the contract ceiling in seconds. The check reads
#: the value the landed schema declares; this name exists so that a test can pin
#: the two together.
ASSIGNMENT_LIFETIME_CEILING_SECONDS = 21600

#: The two operations an assignment may permit, in their one legal order.
PERMITTED_OPERATIONS = ("seat_key_registration", "seat_return")

#: The members every assignment binds to its snapshot (E4 step 5).
CONVENING_MEMBERS = ("protocol", "convening_id", "convening_digest",
                     "council_id", "candidate")

DIGEST_SUBJECT = "council_convening"
_INSTANT = "%Y-%m-%dT%H:%M:%SZ"


@lru_cache(maxsize=1)
def _default_schemas() -> records.SchemaSet:
    return records.load_schemas()


@lru_cache(maxsize=1)
def _default_registry() -> classification.Registry:
    return classification.load_registry()


def contract_lifetime_ceiling(schemas: records.SchemaSet | None = None) -> int:
    """The assignment lifetime ceiling the landed contract declares."""
    schemas = schemas if schemas is not None else _default_schemas()
    return int(schemas.family[ASSIGNMENT_SCHEMA]["$defs"]["lifetime_ceiling_seconds"]["const"])


def convening_digest(record: Any) -> dict:
    """`convening_digest`: `xfc-jcs-sha256-1`, subject `council_convening`, over
    the whole commission record (data-model E2, Derived value)."""
    return {
        "construction": canonical.CONSTRUCTION,
        "subject": DIGEST_SUBJECT,
        "value": canonical.digest(record),
    }


def convening_key(record: Mapping[str, Any]) -> tuple[Any, Any, Any]:
    """The convening key of E2 step A3: 025's once-per-pin key, the council and
    the pin, with the protocol added. A consumer may scope it further by its own
    tenancy layer, which is not a record member."""
    return (record.get("protocol"), record.get("council_id"), record.get("subject_pin"))


def _canonical(value: Any) -> str:
    return canonical.serialize(value)


def _instant(value: str) -> datetime:
    return datetime.strptime(value, _INSTANT).replace(tzinfo=timezone.utc)


def _shape(schemas: records.SchemaSet, ref: str, value: Any, code: str, member: str) -> None:
    if schemas.errors(ref, value):
        raise Refused(code, member=member)


def check_assignment(value: Any, schemas: records.SchemaSet | None = None, *,
                     member: str = "assignment") -> None:
    """One assignment against E5: its schema, then the ruled lifetime ceiling.

    Every failure is `assignment_malformed`. Validity at use (not yet valid,
    expired, operation not permitted) is Phase 4's, at registration and return.
    """
    schemas = schemas if schemas is not None else _default_schemas()
    _shape(schemas, ASSIGNMENT_SCHEMA_ID, value, "assignment_malformed", member)
    lifetime = (_instant(value["expires_at"]) - _instant(value["not_before"])).total_seconds()
    if not 0 < lifetime <= contract_lifetime_ceiling(schemas):
        raise Refused("assignment_malformed", member=member)


def check_lone_assignment(value: Any, schemas: records.SchemaSet | None = None) -> None:
    """A lone assignment, as `check` reads one: E5, then `value_not_canonicalizable`.

    Inside a snapshot the canonicalizability pre-check runs after E4 step 3, so
    alone it runs after the assignment's own E5 shape, and before any digest is
    taken (Phase 3 pre-review L3, 2026-10-09).
    """
    check_assignment(value, schemas)
    records.check_canonicalizable(value, member="assignment")


def _embedded_record(convening: Mapping[str, Any]) -> None:
    """E4 step 2 over the record a snapshot embeds, once it has passed the E2
    schema: E2 step 2's structural rules, then the offline roster rules of E2
    steps 11 and 12. A record they refuse is never admitted, so the snapshot
    embedding it is `snapshot_malformed` (Phase 3 pre-review M3; data-model E4,
    dated note of 2026-10-09). No oracle is read.
    """
    from . import resolution  # resolution imports this module, so not at the top

    try:
        resolution.structural_rules(convening)
        resolution.roster_rules(convening)
    except Refused as refused:
        raise Refused("snapshot_malformed", member=f"convening.{refused.member}") from None


def check_snapshot(snapshot: Any, schemas: records.SchemaSet | None = None) -> dict:
    """E4 steps 2 to 7, over a snapshot that has classified as a replacement
    record under its side's selection.

    Returns the derived known answers, `required_seats` and `convening_digest`,
    or raises `Refused` with the first failing check's code.
    """
    schemas = schemas if schemas is not None else _default_schemas()

    # 2. The snapshot's own shape, the embedded commission record included: its
    #    E2 schema, which the snapshot schema takes by `$ref`, then the E2 rules
    #    that need no oracle and judge the record alone.
    _shape(schemas, SNAPSHOT_SCHEMA_ID, snapshot, "snapshot_malformed", "snapshot")
    _embedded_record(snapshot["convening"])

    # 3. Every assignment against E5, in array order.
    items = snapshot["assignments"]
    for index, item in enumerate(items):
        check_assignment(item, schemas, member=f"assignments[{index}]")

    # Before any digest is taken (data-model § Shared definitions).
    records.check_canonicalizable(snapshot, member="snapshot")

    # 4. The digest recomputes over the admitted record.
    convening = snapshot["convening"]
    expected_digest = convening_digest(convening)
    if _canonical(snapshot["convening_digest"]) != _canonical(expected_digest):
        raise Refused("digest_construction_mismatch", member="convening_digest")

    # 5. Exactly one assignment per required seat, in roster order, and each
    #    bound to this convening.
    if [item["seat_id"] for item in items] != list(convening["required_seats"]):
        raise Refused("assignment_set_mismatch", member="assignments")
    expected = {
        "protocol": snapshot["protocol"],
        "convening_id": snapshot["convening_id"],
        "convening_digest": snapshot["convening_digest"],
        "council_id": convening["council_id"],
        "candidate": convening["required_seats_provenance"]["candidate"],
    }
    for index, item in enumerate(items):
        for name in CONVENING_MEMBERS:
            if _canonical(item[name]) != _canonical(expected[name]):
                raise Refused("assignment_set_mismatch",
                              member=f"assignments[{index}].{name}")

    # 6. Assignment identifiers are unique.
    seen: set[str] = set()
    for index, item in enumerate(items):
        if item["assignment_id"] in seen:
            raise Refused("assignment_duplicate",
                          member=f"assignments[{index}].assignment_id")
        seen.add(item["assignment_id"])

    # 7. No principal holds two seats, and then no binding serves two (Brett
    #    Heap, 2026-10-11T00:19:34Z, "Refuse at freeze (Recommended)"): every
    #    repeated `principal_ref` is named before any repeated `binding_ref`.
    for ref in ("principal_ref", "binding_ref"):
        held: set[str] = set()
        for index, item in enumerate(items):
            value = item["holder"][ref]
            if value in held:
                raise Refused("assignment_shared_holder",
                              member=f"assignments[{index}].holder.{ref}")
            held.add(value)

    return {"required_seats": list(convening["required_seats"]),
            "convening_digest": expected_digest}


def snapshot_outcome(snapshot: Any, *, selected_protocol: str | None,
                     schemas: records.SchemaSet | None = None,
                     registry: classification.Registry | None = None,
                     statuses: Mapping[str, str] | None = None) -> Outcome:
    """The snapshot half of `admission`, in the E4 order.

    1. Classification and selection (data-model E1): a legacy snapshot is
       refused or routed before any replacement check runs, so it is never
       called malformed.
    2 to 7. `check_snapshot`.
    """
    registry = registry if registry is not None else _default_registry()
    selected = classification.classify_and_select(snapshot, selected_protocol, registry,
                                                  statuses)
    if selected.outcome != "accept":
        return selected
    try:
        derived = check_snapshot(snapshot, schemas)
    except Refused as refused:
        return Outcome("refuse", refused.code, status_read=selected.status_read)
    return Outcome("accept", derived=derived, status_read=selected.status_read)


def retry_identity(record: Mapping[str, Any],
                   live_snapshots: Iterable[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    """E2 step A3: retry identity, then once-per-pin.

    `record` has classified as a replacement record and passed its shape check
    (E2 steps 1 and 2), so it is canonicalizable. `live_snapshots` are the
    consumer's snapshots that have not failed, as of `evaluation_time`.

    * A live snapshot whose `convening` has the record's canonical bytes is
      returned unchanged, the same `convening_id` and the same assignments, and
      the caller runs no later step.
    * Otherwise a live snapshot with the record's convening key refuses
      `convening_conflict`, and nothing is replaced.
    * Otherwise `None`: the admission order continues.

    The identical test runs over EVERY live snapshot before the once-per-pin test
    runs over any, so once-per-pin never pre-empts an identical retry.
    """
    snapshots = list(live_snapshots)
    incoming = _canonical(record)
    for snapshot in snapshots:
        if _canonical(snapshot["convening"]) == incoming:
            return snapshot
    key = convening_key(record)
    for snapshot in snapshots:
        if convening_key(snapshot["convening"]) == key:
            raise Refused("convening_conflict", member="record")
    return None
