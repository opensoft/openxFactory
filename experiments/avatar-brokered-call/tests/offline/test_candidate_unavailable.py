"""US2-S3 / FR-004: candidate unavailable / no key → INCONCLUSIVE, never inferred."""
from avatar_f0 import INCONCLUSIVE, PASS
from avatar_f0.broker import BrokerCreateFailed, SimulatedBroker
from avatar_f0.classify import classify_overall
from avatar_f0.models import GroupResult
from avatar_f0.run import build_inconclusive_record


def test_no_key_record_is_inconclusive_with_no_fabrication():
    rec = build_inconclusive_record(
        started_at="2026-07-11T00:00:00Z", completed_at="2026-07-11T00:00:00Z",
        lab_project_ref="lab:f0", dependency_versions={})
    assert rec["overall"] == INCONCLUSIVE
    assert len(rec["trials"]) == 70
    assert all(t["status"] == INCONCLUSIVE for t in rec["trials"])
    assert all(t["provider_request_id_hash"] is None for t in rec["trials"])
    assert all(g["completed"] == 0 for g in rec["trial_groups"])


def test_environment_inconclusive_never_pass():
    groups = [GroupResult(id="F0-A", planned=20, completed=0)]
    out = classify_overall(groups, [], [], {}, "PASS", environment_inconclusive=True)
    assert out == INCONCLUSIVE


def test_provider_create_failure_is_not_inferred_as_pass_or_fail():
    b = SimulatedBroker(fail_create=True)
    try:
        b.create_call("req", "offer")
        failed = False
    except BrokerCreateFailed:
        failed = True
    assert failed
    assert b.provider_calls_created == 0  # nothing inferred / created
