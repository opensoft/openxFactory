"""FR-017 / SC-007: redaction allowlist + prohibited-content scan fail closed."""
from pathlib import Path

import pytest

from avatar_f0.evidence import RedactionFailure, build_interface_impact, finalize_record, write_evidence
from avatar_f0.redaction import redaction_scan, scan, scan_prose
from avatar_f0.run import build_inconclusive_record, inconclusive_report_md


def test_clean_evidence_scans_pass():
    assert redaction_scan({"trial_id": "F0-A-01", "hash": "a" * 64, "ms": 12.5})["status"] == "PASS"


@pytest.mark.parametrize("payload", [
    {"leak": "sk-ABCDEF0123456789abcdef0123456789ABCD"},
    {"sdp": "v=0\r\no=- 1 1 IN IP4 0.0.0.0\r\nm=audio 9 UDP/TLS/RTP/SAVPF 111"},
    {"ice": "candidate:842163049 1 udp 1677729535 1.2.3.4 51413 typ srflx"},
    {"auth": "Bearer abc.def.ghi"},
    {"audio": "data:audio/wav;base64,UklGR... "},
    {"blob": "X" * 2000},                    # unbounded string
    {"raw": b"\x00\x01rawbytes"},            # raw bytes
    {"token": "Ab3" + "xYz9" * 12},          # high-entropy mixed-case token
])
def test_prohibited_classes_fail_closed(payload):
    res = redaction_scan(payload)
    assert res["status"] == "FAIL"
    assert res["prohibited_findings"] >= 1


def test_prose_report_allows_length_but_rejects_secrets():
    assert scan_prose("A long narrative. " * 200) == []          # long prose is fine
    assert len(scan_prose("...contains sk-ABCDEF0123456789abcdef0123...")) == 1


def test_write_evidence_refuses_on_redaction_finding(tmp_path):
    # Build a repo_root with the allowed evidence dir, then inject a prohibited note.
    root = tmp_path
    (root / "openspec/changes/qualify-avatar-brokered-call-feasibility/evidence").mkdir(parents=True)
    body = build_inconclusive_record(started_at="2026-07-11T00:00:00Z", completed_at="2026-07-11T00:00:00Z",
                                     lab_project_ref="lab:f0", dependency_versions={})
    body["trials"][0]["note"] = "leak sk-ABCDEF0123456789abcdef0123456789ABCD"
    ii = build_interface_impact("p.yaml", "commit", "a" * 64, [])
    rec = finalize_record(body, inconclusive_report_md("no_lab_credential", "note"), ii)
    assert rec["redaction_scan"]["status"] == "FAIL"
    assert rec["overall"] == "FAIL"
    with pytest.raises(RedactionFailure):
        write_evidence(rec, "report", ii, root)
    # nothing was written
    assert not (root / "openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/f0-results.json").exists()
