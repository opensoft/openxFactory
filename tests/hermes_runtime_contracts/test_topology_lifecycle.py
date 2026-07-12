"""RED tests for immutable, event-derived topology lifecycle state (T022)."""

from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.hermes_runtime_validation.semantics.topology import (
    derive_lifecycle_projection,
    validate_append_only_history,
    validate_lifecycle_history,
    validate_lifecycle_transition,
)
from tests.hermes_runtime_contracts.support import finding_codes

REGISTRATION_DIGEST = "sha256:" + "a" * 64
EVENT_1_DIGEST = "sha256:" + "b" * 64
EVENT_2_DIGEST = "sha256:" + "c" * 64
EVENT_3_DIGEST = "sha256:" + "d" * 64
GRANT_DIGEST = "sha256:" + "e" * 64


def _registration(*, initial_state: str = "provisioning") -> dict:
    return {
        "entity_kind": "layer",
        "registration_id": "layer-customer-a",
        "registration_digest": REGISTRATION_DIGEST,
        "installation_id": "installation-1",
        "stack_id": "stack-1",
        "layer_id": "customer-a",
        "role": "customer",
        "initial_lifecycle_state": initial_state,
    }


def _event(
    event_id: str,
    event_digest: str,
    predecessor_id: str,
    predecessor_digest: str,
    from_state: str,
    to_state: str,
    occurred_at: str,
) -> dict:
    return {
        "event_id": event_id,
        "event_digest": event_digest,
        "installation_id": "installation-1",
        "stack_id": "stack-1",
        "layer_id": "customer-a",
        "predecessor_ref": {
            "kind": "registration" if predecessor_id == "layer-customer-a" else "event",
            "id": predecessor_id,
            "digest": predecessor_digest,
        },
        "from_state": from_state,
        "to_state": to_state,
        "authority_grant_id": "grant-lifecycle",
        "authority_grant_digest": GRANT_DIGEST,
        "occurred_at": occurred_at,
        "reason": "governed-lifecycle-transition",
    }


def _active_history() -> list[dict]:
    return [
        _event(
            "event-1",
            EVENT_1_DIGEST,
            "layer-customer-a",
            REGISTRATION_DIGEST,
            "provisioning",
            "active",
            "2026-07-12T12:00:00Z",
        )
    ]


def _suspended_history() -> list[dict]:
    return _active_history() + [
        _event(
            "event-2",
            EVENT_2_DIGEST,
            "event-1",
            EVENT_1_DIGEST,
            "active",
            "suspended",
            "2026-07-12T12:01:00Z",
        )
    ]


def _projection(state: str, event_id: str, digest: str, *, terminal_time=None) -> dict:
    return {
        "entity_kind": "layer",
        "installation_id": "installation-1",
        "stack_id": "stack-1",
        "layer_id": "customer-a",
        "latest_event_id": event_id,
        "latest_event_digest": digest,
        "state": state,
        "terminal_time": terminal_time,
    }


def _codes(findings: list[dict]) -> list[str]:
    return finding_codes(findings)


def test_linear_history_derives_current_projection() -> None:
    registration = _registration()
    history = _suspended_history()

    projection = derive_lifecycle_projection("layer", registration, history)

    assert projection == _projection("suspended", "event-2", EVENT_2_DIGEST)
    assert validate_lifecycle_history("layer", registration, history, projection) == []


def test_first_event_must_reference_exact_registration_id_and_digest() -> None:
    history = _active_history()
    history[0]["predecessor_ref"]["digest"] = EVENT_1_DIGEST

    findings = validate_lifecycle_history("layer", _registration(), history, None)

    assert "HCS-LIFECYCLE-PREDECESSOR-MISMATCH" in _codes(findings)


def test_event_chain_requires_exact_predecessor_id_and_digest() -> None:
    history = _suspended_history()
    history[1]["predecessor_ref"]["id"] = "event-other"

    findings = validate_lifecycle_history("layer", _registration(), history, None)

    assert "HCS-LIFECYCLE-PREDECESSOR-MISMATCH" in _codes(findings)


def test_predecessor_kind_is_registration_first_and_event_afterward() -> None:
    first_wrong = _active_history()
    first_wrong[0]["predecessor_ref"]["kind"] = "event"
    assert "HCS-LIFECYCLE-PREDECESSOR-KIND" in _codes(
        validate_lifecycle_history("layer", _registration(), first_wrong, None)
    )

    later_wrong = _suspended_history()
    later_wrong[1]["predecessor_ref"]["kind"] = "registration"
    assert "HCS-LIFECYCLE-PREDECESSOR-KIND" in _codes(
        validate_lifecycle_history("layer", _registration(), later_wrong, None)
    )


@pytest.mark.parametrize("field", ["installation_id", "stack_id", "layer_id"])
def test_event_scope_must_match_immutable_registration(field: str) -> None:
    history = _active_history()
    history[0][field] = "foreign-scope"

    assert "HCS-LIFECYCLE-SCOPE-MISMATCH" in _codes(
        validate_lifecycle_history("layer", _registration(), history, None)
    )


def test_predecessor_fork_is_rejected() -> None:
    history = _active_history()
    history.extend(
        [
            _event(
                "event-2",
                EVENT_2_DIGEST,
                "event-1",
                EVENT_1_DIGEST,
                "active",
                "suspended",
                "2026-07-12T12:01:00Z",
            ),
            _event(
                "event-3",
                EVENT_3_DIGEST,
                "event-1",
                EVENT_1_DIGEST,
                "active",
                "failed",
                "2026-07-12T12:02:00Z",
            ),
        ]
    )

    findings = validate_lifecycle_history("layer", _registration(), history, None)

    assert "HCS-LIFECYCLE-PREDECESSOR-FORK" in _codes(findings)


def test_projection_must_reconcile_to_event_chain() -> None:
    findings = validate_lifecycle_history(
        "layer",
        _registration(),
        _suspended_history(),
        _projection("active", "event-1", EVENT_1_DIGEST),
    )

    assert "HCS-LIFECYCLE-PROJECTION-DRIFT" in _codes(findings)


def test_direct_registration_mutation_is_rejected() -> None:
    original = _registration()
    candidate = deepcopy(original)
    candidate["initial_lifecycle_state"] = "active"

    findings = validate_append_only_history(original, [], candidate, [])

    assert "HCS-LIFECYCLE-REGISTRATION-IMMUTABLE" in _codes(findings)


def test_existing_event_update_is_rejected() -> None:
    original = _active_history()
    candidate = deepcopy(original)
    candidate[0]["reason"] = "rewritten-reason"

    findings = validate_append_only_history(
        _registration(), original, _registration(), candidate
    )

    assert "HCS-LIFECYCLE-EVENT-UPDATE" in _codes(findings)


def test_existing_event_delete_is_rejected() -> None:
    original = _suspended_history()

    findings = validate_append_only_history(
        _registration(), original, _registration(), original[:1]
    )

    assert "HCS-LIFECYCLE-EVENT-DELETE" in _codes(findings)


def test_valid_successor_append_preserves_history() -> None:
    original = _suspended_history()
    candidate = original + [
        _event(
            "event-3",
            EVENT_3_DIGEST,
            "event-2",
            EVENT_2_DIGEST,
            "suspended",
            "active",
            "2026-07-12T12:02:00Z",
        )
    ]

    assert validate_append_only_history(
        _registration(), original, _registration(), candidate
    ) == []


def test_suspended_layer_can_recover_only_through_governed_successor() -> None:
    assert validate_lifecycle_transition("layer", "suspended", "active") == []

    history = _suspended_history() + [
        _event(
            "event-3",
            EVENT_3_DIGEST,
            "event-2",
            EVENT_2_DIGEST,
            "suspended",
            "active",
            "2026-07-12T12:02:00Z",
        )
    ]
    projection = derive_lifecycle_projection("layer", _registration(), history)
    assert projection["state"] == "active"


def test_retired_is_terminal_for_topology_and_layer_lifecycles() -> None:
    for entity_kind, attempted_state in (
        ("installation", "operational"),
        ("stack", "operational"),
        ("layer", "active"),
    ):
        findings = validate_lifecycle_transition(entity_kind, "retired", attempted_state)
        assert "HCS-LIFECYCLE-RETIRED-TERMINAL" in _codes(findings)


def test_retirement_projection_preserves_terminal_event_time() -> None:
    history = _active_history() + [
        _event(
            "event-2",
            EVENT_2_DIGEST,
            "event-1",
            EVENT_1_DIGEST,
            "active",
            "retired",
            "2026-07-12T12:03:00Z",
        )
    ]

    projection = derive_lifecycle_projection("layer", _registration(), history)

    assert projection == _projection(
        "retired",
        "event-2",
        EVENT_2_DIGEST,
        terminal_time="2026-07-12T12:03:00Z",
    )
