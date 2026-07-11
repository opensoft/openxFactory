"""SC-002/SC-003/SC-005: metric summary math."""
from avatar_f0.metrics import build_metrics, duration_summary, percentile
from avatar_f0.trials import f0a_baseline, f0d_revocation


def test_percentile_and_summary():
    vals = [10.0, 20.0, 30.0, 40.0, 50.0]
    assert percentile(vals, 50) == 30.0
    assert percentile(vals, 100) == 50.0
    s = duration_summary(vals)
    assert s == {"count": 5, "p50": 30.0, "p95": 48.0, "max": 50.0}


def test_empty_summary_is_zeroed():
    assert duration_summary([]) == {"count": 0, "p50": 0.0, "p95": 0.0, "max": 0.0}


def test_build_metrics_from_real_trials():
    trials = [f0a_baseline.run(f"F0-A-{i:02d}") for i in range(1, 6)]
    trials.append(f0d_revocation.run("F0-D-01"))
    m = build_metrics(trials)
    assert m["sideband_ready_ms"]["count"] == 5
    assert m["first_playable_after_authorized_ms"]["count"] >= 5
    assert m["hangup_to_terminal_ms"]["count"] == 1
    # bounds are comfortably met by the simulated timeline
    assert m["sideband_ready_ms"]["p95"] <= 3000
    assert m["first_playable_after_authorized_ms"]["p95"] <= 2000
    assert m["hangup_to_terminal_ms"]["max"] <= 5000
