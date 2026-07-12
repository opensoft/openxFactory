"""SC-013 / Q1: no-key run completes as a valid INCONCLUSIVE record; completion != qualification."""
from avatar_f0 import INCONCLUSIVE
from avatar_f0.evidence import build_interface_impact, finalize_record, validate_results
from avatar_f0.run import (MANDATORY_ASSERTIONS, build_inconclusive_record,
                           inconclusive_report_md)


def test_no_key_completion_record_is_valid_and_inconclusive():
    body = build_inconclusive_record(
        started_at="2026-07-11T00:00:00Z", completed_at="2026-07-11T00:00:00Z",
        lab_project_ref="lab:f0", dependency_versions={"aiortc": "1.9.0"})
    ii = build_interface_impact("map.yaml", "commit", "c" * 64, [])
    rec = finalize_record(body, inconclusive_report_md("no_lab_credential", "note"), ii)
    validate_results(rec)
    assert rec["overall"] == INCONCLUSIVE
    # nothing fabricated: no measurements, all trials INCONCLUSIVE, groups not completed
    assert all(t["durations_ms"] == {} for t in rec["trials"])
    assert all(g["completed"] == 0 and g["passed"] == 0 for g in rec["trial_groups"])
    assert rec["environment"]["network_type"] == "none"


def test_mandatory_cross_cutting_assertions_are_registered():
    # FR-005/FR-006/FR-012: readiness-timeout, interrupted-run, and bounded-cleanup must be
    # registered so a future live PASS cannot silently omit them. In the no-key state they
    # are present but INCONCLUSIVE (never PASS).
    body = build_inconclusive_record(
        started_at="2026-07-11T00:00:00Z", completed_at="2026-07-11T00:00:00Z",
        lab_project_ref="lab:f0", dependency_versions={})
    ids = {a["id"] for a in body["assertions"]}
    for aid in ("F0-C-READINESS_TIMEOUT", "F0-D-INTERRUPTED", "F0-D-BOUNDED_CLEANUP"):
        assert aid in ids
    assert set(MANDATORY_ASSERTIONS).issubset(ids)
    assert all(a["status"] == INCONCLUSIVE for a in body["assertions"])


def test_report_states_completion_is_not_qualification():
    md = inconclusive_report_md("no_lab_credential", "note")
    assert "does NOT qualify" in md
    assert "does NOT open the kernel publication gate" in md
