"""FR-017 / SC-007: redaction allowlist + prohibited-content scan fail closed."""
from pathlib import Path

import pytest

from avatar_f0.evidence import RedactionFailure, build_interface_impact, finalize_record, write_evidence
from avatar_f0.redaction import redaction_scan, scan, scan_log, scan_prose
from avatar_f0.run import build_inconclusive_record, inconclusive_report_md

TRANSCRIPT = (
    "Hello, thank you for calling the clinic today. I would like to schedule an appointment "
    "with the doctor for next Tuesday afternoon if that is at all possible. Could you please "
    "confirm whether that time slot is currently available for me?"
)


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
    {"session": "550e8400-e29b-41d4-a716-446655440000"},  # UUID-shaped high-cardinality ID
    {"utterance": TRANSCRIPT},                # plaintext transcript
])
def test_prohibited_classes_fail_closed(payload):
    res = redaction_scan(payload)
    assert res["status"] == "FAIL"
    assert res["prohibited_findings"] >= 1


def test_sha256_and_bounded_fields_not_flagged_as_uuid_or_transcript():
    # sha256 hashes (unhyphenated 64-hex) and short bounded notes must stay allowlisted.
    clean = {
        "hash": "a" * 64,
        "req_id_hash": "0b1f5742b744e686a0e3a970a5df1ddeea88a8ce0ce6fdd602f3731672f5e50e",
        "note": "not executed (no lab credential)",
        "variance": "provider released answer before sideband verified",
    }
    assert redaction_scan(clean)["status"] == "PASS"


def test_log_sink_scans_logs_and_crash_output():
    # FR-017: emitted logs/traces/crash output are redaction-scanned; clean text passes,
    # leaked secrets / UUIDs / transcripts fail closed.
    assert scan_log("") == []
    assert scan_log("INFO run started; overall=INCONCLUSIVE; groups=6") == []
    assert len(scan_log("Traceback: OPENAI_API_KEY=sk-ABCDEF0123456789abcdef0123456789ABCD")) >= 1
    assert len(scan_log("crash while handling 550e8400-e29b-41d4-a716-446655440000")) >= 1
    assert len(scan_log(TRANSCRIPT)) >= 1


def test_finalize_record_scans_emitted_logs(tmp_path):
    body = build_inconclusive_record(started_at="2026-07-11T00:00:00Z", completed_at="2026-07-11T00:00:00Z",
                                     lab_project_ref="lab:f0", dependency_versions={})
    ii = build_interface_impact("p.yaml", "commit", "a" * 64, [])
    rec = finalize_record(body, inconclusive_report_md("no_lab_credential", "note"), ii,
                          emitted_logs="fatal: leaked sk-ABCDEF0123456789abcdef0123456789ABCD")
    assert rec["redaction_scan"]["status"] == "FAIL"
    assert rec["overall"] == "FAIL"


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
