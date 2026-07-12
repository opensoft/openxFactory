"""Runtime destruction needs no migration/cleanup/secret recovery (ARR-001-S03, FR-003, SC-009)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _support import authorize, make_request  # noqa: E402


def test_destroy_discards_all_in_memory_state(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    authorize(runtime, "s")
    runtime.mark_connected("s")
    assert runtime.registry.all()  # state exists

    runtime.destroy()
    assert runtime.destroyed
    assert runtime.registry.all() == []
    assert not runtime.grants.has_secret("r1")


def test_terminal_replay_requires_no_secret_material(runtime):
    runtime.preflight(make_request("r1", session_id="s"))
    authorize(runtime, "s")
    runtime.mark_connected("s")
    # No secret grant material remains, yet a credential-free terminal replays.
    assert not runtime.grants.has_secret("r1")
    replay = runtime.terminal_replay("r1")
    assert replay is not None and not replay.carries_credential()
