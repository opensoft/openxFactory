"""Record builders for the Phase 3 tests: the E2 record a snapshot binds, the
E4 snapshot and its E5 assignments (feature 035, data-model E2, E4 and E5).

Shared by `test_assignments.py` (T035) and the `check` cases in
`test_validator_cli.py` (T037), so the two describe one well-formed snapshot.
Every builder returns a fresh value; a test mutates its own copy.

It imports no implementation module, so a test module that uses it still fails
at its own import while the implementation is absent (the tests-first rule).
"""

from __future__ import annotations

import copy

from scripts.signed_execution_chain import canonical

REPLACEMENT = "xfc-resolved-council-1"
LEGACY = "xfactory-council-seat-return/v1"

SHA_HEAD = "1" * 40
SHA_REVISION = "2" * 40
SHA_FILE = "sha256:" + "3" * 64

#: Brett Heap's OPEN-1 ruling of 2026-10-08, "600 s challenge, 6 h assignment
#: (Recommended)": the contract ceiling on an assignment's lifetime.
CEILING = 21600


def convening_record(**overrides) -> dict:
    """A shape-valid E2 record of an unclassed council with two standing seats.

    The snapshot half (E4) does not re-run the E2 order: it binds this record,
    verbatim, by `convening_digest`. So the record only has to pass the E2
    schema, which `convening-snapshot.schema.yaml` takes by `$ref`.
    """
    record = {
        "schema_version": 1,
        "kind": "xfactory_council_convening",
        "protocol": REPLACEMENT,
        "council_id": "council-alpha",
        "subject_pin": SHA_HEAD,
        "packet_refs": ["packet/alpha-1"],
        "required_seats": ["seat-a", "seat-b"],
        "required_seats_provenance": {
            "candidate": {
                "repository": "example-owner/example-candidate",
                "pull_number": 7,
                "head_sha": SHA_HEAD,
            },
            "governed": {
                "repository": "example-owner/example-rules",
                "revision": SHA_REVISION,
                "sources": [
                    {"kind": "file", "path": "rules/council-alpha.yaml",
                     "sha256": SHA_FILE},
                ],
            },
            "standing_seats": ["seat-a", "seat-b"],
            "conditions": [],
            "fact_sources": [],
            "consumed_facts": {},
        },
    }
    record.update(overrides)
    return record


def digest_of(record: dict) -> dict:
    """`convening_digest`: `xfc-jcs-sha256-1`, subject `council_convening`."""
    return {
        "construction": "xfc-jcs-sha256-1",
        "subject": "council_convening",
        "value": canonical.digest(record),
    }


def assignment(convening: dict, convening_id: str, seat_id: str, **overrides) -> dict:
    """One E5 assignment for `seat_id`, bound to `convening`, living six hours."""
    value = {
        "schema_version": 1,
        "kind": "xfactory_council_seat_assignment",
        "protocol": REPLACEMENT,
        "convening_id": convening_id,
        "convening_digest": digest_of(convening),
        "council_id": convening["council_id"],
        "candidate": copy.deepcopy(
            convening["required_seats_provenance"]["candidate"]),
        "assignment_id": f"assignment-{seat_id}",
        "seat_id": seat_id,
        "holder": {
            "principal_kind": "github_oidc_job",
            "principal_ref": f"principal-{seat_id}",
            "binding_ref": "binding-seat",
        },
        "permitted_operations": ["seat_key_registration", "seat_return"],
        "not_before": "2026-10-09T00:00:00Z",
        "expires_at": "2026-10-09T06:00:00Z",
    }
    value.update(overrides)
    return value


def snapshot(convening: dict | None = None, *, convening_id: str = "convening-0001",
             seats: list[str] | None = None) -> dict:
    """An E4 snapshot of `convening` with one assignment per seat in `seats`,
    which defaults to the record's `required_seats`, in order."""
    convening = convening_record() if convening is None else copy.deepcopy(convening)
    seats = list(convening["required_seats"]) if seats is None else seats
    return {
        "schema_version": 1,
        "kind": "xfactory_council_convening_snapshot",
        "protocol": REPLACEMENT,
        "convening_id": convening_id,
        "convening_digest": digest_of(convening),
        "convening": convening,
        "assignments": [assignment(convening, convening_id, seat) for seat in seats],
        "admitted_at": "2026-10-09T00:00:00Z",
    }
