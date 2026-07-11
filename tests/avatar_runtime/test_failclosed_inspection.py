"""Reviewer-facing fail-closed inspection: purpose mapping + kill switch
(ARR-007-S01, ARR-007-S03, FR-028/031).

NOTE (F1): ARR-007-S01/S03 are also covered by US1 tests (test_authority_ports,
test_kill_switches); scenario-test-map.yaml records each as a SINGLE entry
listing both the US1 and US3 test nodes.
"""

from __future__ import annotations

from xfactory.avatar_runtime.values import KillSwitchState, OutcomeCode, PreflightKind

from _support import PROFILE, make_request


def test_purpose_mapping_absent_denies(runtime, provider):
    res = runtime.preflight(make_request("r1", purposes=frozenset({"avatar.unmapped"})))
    assert res.kind is PreflightKind.DENIAL
    assert res.outcome is OutcomeCode.PURPOSE_UNMAPPED
    assert provider.create_count == 0  # denied before provider creation


def test_kill_switch_denies_new_matching_requests(runtime):
    runtime.kill_switch = KillSwitchState(disabled_profiles=frozenset({PROFILE}))
    res = runtime.preflight(make_request("r1", profile=PROFILE))
    assert res.outcome is OutcomeCode.KILLED
