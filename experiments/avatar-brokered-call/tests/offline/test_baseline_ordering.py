"""US1-S1 / FR-008 / SC-001: baseline ordering invariant + single provider call."""
from avatar_f0.trials import f0a_baseline
from avatar_f0.trials.base import ORDER


def test_baseline_passes_with_ordered_authorization_and_single_call():
    r = f0a_baseline.run("F0-A-01")
    assert r.status == "PASS"
    assert r.provider_calls_created == 1
    assert r.media_authorized and r.answer_applied


def test_media_authorized_after_both_channels_and_before_answer_and_first_media():
    r = f0a_baseline.run("F0-A-02")
    d = r.durations_ms
    # sideband_verified <= answer_released <= lease_ack <= media_authorized <= answer_applied <= first_input_sent
    seq = [d[m] for m in ORDER]
    assert seq == sorted(seq)
    assert d["t_media_authorized"] <= d["t_answer_applied"]
    assert d["t_media_authorized"] <= d.get("t_first_output_playable", float("inf"))


def test_all_baseline_trial_ids_pass():
    from avatar_f0.trials.base import iter_trial_ids
    statuses = [f0a_baseline.run(tid).status for tid in iter_trial_ids("F0-A")]
    assert len(statuses) == 20
    assert set(statuses) == {"PASS"}
