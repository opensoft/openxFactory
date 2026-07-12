"""Grant retry cache, credential-free terminal replay, cache destruction (ARR-004-S04, SC-009)."""

from __future__ import annotations

from xfactory.avatar_runtime.values import OutcomeCode, PreflightKind

from _support import authorize, make_request


def test_exact_retry_returns_same_grant(runtime):
    a = runtime.preflight(make_request("r1"))
    b = runtime.preflight(make_request("r1"))
    assert a.grant.answer == b.grant.answer


def test_secret_cache_destroyed_on_connect(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    assert runtime.grants.has_secret("r1")
    authorize(runtime, "s")
    runtime.mark_connected("s")
    # Secret material gone; a credential-free terminal remains for replay.
    assert not runtime.grants.has_secret("r1")
    replay = runtime.terminal_replay("r1")
    assert replay.kind is PreflightKind.TERMINAL
    assert replay.outcome is OutcomeCode.CONNECTED
    assert not replay.carries_credential()


def test_terminal_replay_survives_grant_expiry(runtime, clock):
    runtime.preflight(make_request("r1"))
    clock.advance(runtime.GRANT_TTL + 1)
    b = runtime.preflight(make_request("r1"))
    assert b.kind is PreflightKind.TERMINAL
    assert b.outcome is OutcomeCode.EXPIRED
    assert not b.carries_credential()


def test_terminal_replay_needs_no_secret_material(runtime, clock):
    runtime.preflight(make_request("r1", session_id="s"))
    authorize(runtime, "s")
    runtime.mark_connected("s")
    assert not runtime.grants.has_secret("r1")
    # Replaying only reads the credential-free terminal record.
    assert runtime.terminal_replay("r1").outcome is OutcomeCode.CONNECTED
