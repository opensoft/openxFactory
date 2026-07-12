"""US1-S3 / FR-009 / SC-004: sideband failure authorizes no media, no answer, terminates."""
from avatar_f0.trials import f0c_sideband_failure
from avatar_f0.cleanup import CallRegistry


def test_sideband_failure_authorizes_no_media_and_terminates():
    reg = CallRegistry()
    r = f0c_sideband_failure.run("F0-C-01", registry=reg)
    assert r.status == "PASS"
    assert not r.media_authorized
    assert not r.answer_applied
    # every known call was terminated (fail-closed)
    assert reg.open_calls() == []


def test_sideband_failure_never_reaches_first_media():
    r = f0c_sideband_failure.run("F0-C-02")
    assert "t_first_output_playable" not in r.durations_ms
    assert "t_media_authorized" not in r.durations_ms
