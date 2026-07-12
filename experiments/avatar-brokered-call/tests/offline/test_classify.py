"""FR-016 / SC-002/SC-003: PASS/FAIL/INCONCLUSIVE derivation; p95 miss is not averaged away."""
from avatar_f0 import FAIL, INCONCLUSIVE, PASS
from avatar_f0.classify import classify_overall, metric_bound_failures
from avatar_f0.models import AssertionResult, GroupResult, TrialResult


def _full_groups():
    return [GroupResult(id=g, planned=p, completed=p, passed=p, failed=0)
            for g, p in (("F0-A", 20), ("F0-B", 10), ("F0-C", 10),
                         ("F0-D", 10), ("F0-E", 10), ("F0-F", 10))]


def _good_metrics():
    return {
        "sideband_ready_ms": {"count": 30, "p50": 900, "p95": 2800, "max": 4800},
        "first_playable_after_authorized_ms": {"count": 30, "p50": 400, "p95": 1800, "max": 1900},
        "hangup_to_terminal_ms": {"count": 10, "p50": 800, "p95": 900, "max": 1000},
    }


def test_pass_when_everything_passes():
    groups = _full_groups()
    trials = [TrialResult("F0-A-01", "F0-A", PASS, None, {}, ["F0-A-ORDERING"])]
    asserts = [AssertionResult("F0-A-ORDERING", PASS, 20, 0)]
    assert classify_overall(groups, trials, asserts, _good_metrics(), PASS) == PASS


def test_fail_on_any_contrary_trial():
    groups = _full_groups()
    trials = [TrialResult("F0-A-01", "F0-A", FAIL, None, {}, ["F0-A-ORDERING"])]
    assert classify_overall(groups, trials, [], _good_metrics(), PASS) == FAIL


def test_inconclusive_when_group_incomplete():
    groups = _full_groups()
    groups[0].completed = 0
    groups[0].passed = 0
    assert classify_overall(groups, [], [], _good_metrics(), PASS) == INCONCLUSIVE


def test_p95_miss_is_a_fail_not_averaged_away():
    m = _good_metrics()
    m["sideband_ready_ms"]["p50"] = 100  # great average
    m["sideband_ready_ms"]["p95"] = 3200  # but p95 over the 3000 bound
    assert "sideband_ready_ms.p95>3000.0" in metric_bound_failures(m)
    assert classify_overall(_full_groups(), [], [], m, PASS) == FAIL


def test_hard_ceiling_max_miss_is_a_fail():
    m = _good_metrics()
    m["sideband_ready_ms"]["max"] = 5200  # over the 5000 hard ceiling
    assert classify_overall(_full_groups(), [], [], m, PASS) == FAIL


def test_redaction_fail_forces_overall_fail():
    assert classify_overall(_full_groups(), [], [], _good_metrics(), FAIL) == FAIL
