"""Determinism: clock-driven transitions, order-independence (ARR-003-S01/S02, ARR-008-S02, SC-003/004)."""

from __future__ import annotations

from xfactory.avatar_runtime.values import PreflightKind

from _support import ack_for, build_fresh_runtime, make_request


def _authorize_scenario():
    """A full grant -> authorize flow; returns observable authoritative outputs."""
    rt = build_fresh_runtime()
    res = rt.preflight(make_request("r1", session_id="s"))
    rt.open_sideband("s")
    rt.verify_sideband("s")
    ev = rt.submit_lease_ack("s", ack_for(rt, "s"))
    log = rt.event_log("s").records()
    return (
        res.kind,
        res.grant.answer,
        ev.payload,
        tuple((e.sequence, e.payload) for e in log),
    )


def test_repeated_runs_produce_identical_results():
    assert _authorize_scenario() == _authorize_scenario()


def test_time_dependent_transition_is_deterministic():
    def readiness_outcome():
        rt = build_fresh_runtime()
        rt.preflight(make_request("r1", session_id="s"))
        rt.open_sideband("s")
        rt.clock.advance(rt.READINESS_TTL + 1)
        return rt.check_readiness("s").outcome

    assert readiness_outcome() == readiness_outcome()


def test_reordered_provider_and_sideband_follow_declared_transitions():
    # lease_ack submitted before sideband verification is withheld; the declared
    # transition order (verify -> authorize) governs, not call order.
    rt = build_fresh_runtime()
    rt.preflight(make_request("r1", session_id="s"))
    assert rt.submit_lease_ack("s", ack_for(rt, "s")) is None  # withheld
    rt.open_sideband("s")
    rt.verify_sideband("s")
    assert rt.submit_lease_ack("s", ack_for(rt, "s")) is not None


def test_grant_is_deterministic_across_instances():
    a = build_fresh_runtime().preflight(make_request("r1"))
    b = build_fresh_runtime().preflight(make_request("r1"))
    assert a.kind is b.kind is PreflightKind.GRANT
    assert a.grant.answer == b.grant.answer
    assert a.grant.offer_fingerprint == b.grant.offer_fingerprint
