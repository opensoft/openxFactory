"""FR-013/FR-014 / US4-S4: revocation separate offsets, terminal <= 5 s; unconfirmed not success."""
from avatar_f0.trials import f0d_revocation


def test_revocation_records_separate_offsets_and_meets_bound():
    r = f0d_revocation.run("F0-D-01")
    assert r.status == "PASS"
    d = r.durations_ms
    # revocation_request, hangup_request (t_hangup_sent) and terminal are distinct offsets
    assert d["t_revocation_request"] < d["t_hangup_sent"] < d["t_peer_terminal"]
    assert (d["t_peer_terminal"] - d["t_hangup_sent"]) <= 5000


def test_unconfirmed_terminal_is_inconclusive_never_success():
    r = f0d_revocation.run("F0-D-02", observable=False)
    assert r.status == "INCONCLUSIVE"
    assert "t_peer_terminal" not in r.durations_ms
