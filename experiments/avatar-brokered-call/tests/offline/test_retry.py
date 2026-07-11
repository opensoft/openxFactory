"""US1-S4/S5 / FR-010 / SC-006: exact retry single-call; changed retry no disclosure."""
from avatar_f0.trials import f0e_exact_retry, f0f_changed_retry


def test_exact_retry_creates_at_most_one_provider_call():
    r = f0e_exact_retry.run("F0-E-01")
    assert r.status == "PASS"
    assert r.provider_calls_created == 1


def test_changed_retry_no_second_call_and_no_prior_answer():
    r = f0f_changed_retry.run("F0-F-01")
    assert r.status == "PASS"
    assert r.provider_calls_created == 1


def test_changed_retry_raises_idempotency_conflict_directly():
    from avatar_f0.broker import IdempotencyConflict, SimulatedBroker
    b = SimulatedBroker()
    b.create_call("req-x", "offer-A")
    try:
        b.create_call("req-x", "offer-B")
        raised = False
    except IdempotencyConflict:
        raised = True
    assert raised
    assert b.provider_calls_created == 1  # no second billable call
