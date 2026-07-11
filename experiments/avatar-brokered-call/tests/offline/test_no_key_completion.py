"""SC-013 / Q1: no-key run completes as a valid INCONCLUSIVE record; completion != qualification."""
from avatar_f0 import INCONCLUSIVE
from avatar_f0.evidence import build_interface_impact, finalize_record, validate_results
from avatar_f0.run import build_inconclusive_record, inconclusive_report_md


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


def test_report_states_completion_is_not_qualification():
    md = inconclusive_report_md("no_lab_credential", "note")
    assert "does NOT qualify" in md
    assert "does NOT open the kernel publication gate" in md
