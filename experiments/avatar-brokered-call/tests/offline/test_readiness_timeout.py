"""FR-012 / US4-S2: readiness-timeout (F0-C path) withholds media, terminates, fails if leaked."""
from avatar_f0.cleanup import CallRegistry
from avatar_f0.trials import f0c_sideband_failure


def test_readiness_timeout_withholds_and_terminates():
    reg = CallRegistry()
    r = f0c_sideband_failure.run("F0-C-05", variant="readiness_timeout", registry=reg)
    assert r.status == "PASS"
    assert not r.media_authorized
    assert not r.answer_applied
    assert reg.open_calls() == []               # terminated
    assert "t_media_authorized" not in r.durations_ms


def test_readiness_within_deadline_still_authorizes_baseline():
    from avatar_f0.trials import f0b_delayed
    r = f0b_delayed.run("F0-B-03")              # delay 1500-2500 < 3000 default
    assert r.status == "PASS"
    assert r.durations_ms["t_sideband_verified"] <= 3000
