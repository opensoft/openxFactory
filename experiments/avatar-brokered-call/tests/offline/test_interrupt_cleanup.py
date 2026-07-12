"""US1-S6 / FR-005: interrupted run terminates every known call ID and records outcome."""
from avatar_f0.cleanup import CallRegistry, run_cleanup


def test_cleanup_terminates_every_known_call():
    reg = CallRegistry()
    for h in ("a" * 64, "b" * 64, "c" * 64):
        reg.register(h)
    outcomes = run_cleanup(reg, terminate=lambda cid: True)
    assert len(outcomes) == 3
    assert all(o.terminated for o in outcomes)
    assert reg.open_calls() == []


def test_cleanup_records_unconfirmed_when_no_terminator():
    reg = CallRegistry()
    reg.register("d" * 64)
    outcomes = run_cleanup(reg, terminate=None)
    assert len(outcomes) == 1
    assert outcomes[0].terminated is False
    assert outcomes[0].reason == "no_terminator"
    # unconfirmed is never treated as success
    assert reg.open_calls() == ["d" * 64]


def test_cleanup_never_raises_out_on_terminator_error():
    reg = CallRegistry()
    reg.register("e" * 64)

    def boom(cid):
        raise RuntimeError("provider gone")

    outcomes = run_cleanup(reg, terminate=boom)
    assert outcomes[0].terminated is False
    assert outcomes[0].reason == "termination_unconfirmed"
