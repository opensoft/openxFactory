"""Command validation, dedupe, revision guard (ARR-006-S01/S02, FR-024/025)."""

from __future__ import annotations

from xfactory.avatar_runtime.values import Command

from _support import make_request


def test_duplicate_command_returns_first_result_no_repeat(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    first = runtime.submit_command(Command("c1", "s", 0, "speak"))
    assert first.accepted
    rev = first.revision
    again = runtime.submit_command(Command("c1", "s", 0, "speak"))
    assert again.revision == rev and again.accepted == first.accepted
    # Effect applied once — revision advanced only once.
    assert runtime.registry.get("s").state_revision == rev


def test_stale_revision_guard_rejected_without_transition(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    runtime.submit_command(Command("c1", "s", 0, "speak"))  # revision -> 1
    res = runtime.submit_command(Command("c2", "s", 0, "speak", expected_revision=0))
    assert not res.accepted
    assert runtime.registry.get("s").state_revision == 1


def test_disallowed_verb_rejected(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    res = runtime.submit_command(Command("c1", "s", 0, "exfiltrate"))
    assert not res.accepted


def test_wrong_epoch_rejected(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    res = runtime.submit_command(Command("c1", "s", 7, "speak"))
    assert not res.accepted
