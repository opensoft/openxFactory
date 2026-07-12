"""SC-008: results validate against the owned schema; schema drift-guard to registered copy."""
import hashlib
from pathlib import Path

from avatar_f0.evidence import (SCHEMAS_DIR, build_interface_impact, finalize_record,
                                validate_interface_impact, validate_results, write_evidence)
from avatar_f0.run import build_inconclusive_record, inconclusive_report_md

REPO_ROOT = Path(__file__).resolve().parents[4]
REGISTERED = REPO_ROOT / "openspec/changes/qualify-avatar-brokered-call-feasibility/supporting-docs/f0-results.schema.yaml"
REGISTERED_SHA = "bc81d1882f091bd7cf1b5945aad57ac518837a6024dc52c833b1d17c67ed4220"


def test_results_schema_drift_guard():
    owned = (SCHEMAS_DIR / "f0-results.schema.yaml").read_bytes()
    assert hashlib.sha256(owned).hexdigest() == REGISTERED_SHA
    # byte-identical to the registered supporting-docs copy
    assert owned == REGISTERED.read_bytes()


def test_inconclusive_record_validates_and_writes(tmp_path):
    root = tmp_path
    (root / "openspec/changes/qualify-avatar-brokered-call-feasibility/evidence").mkdir(parents=True)
    body = build_inconclusive_record(started_at="2026-07-11T00:00:00Z", completed_at="2026-07-11T00:00:00Z",
                                     lab_project_ref="lab:f0", dependency_versions={"aiortc": "1.9.0"})
    ii = build_interface_impact("map.yaml", "commit", "b" * 64, [])
    rec = finalize_record(body, inconclusive_report_md("no_lab_credential", "note"), ii)
    validate_results(rec)             # zero errors
    validate_interface_impact(ii)
    assert rec["overall"] == "INCONCLUSIVE"
    assert rec["redaction_scan"] == {"status": "PASS", "prohibited_findings": 0}
    paths = write_evidence(rec, inconclusive_report_md("no_lab_credential", "note"), ii, root)
    assert Path(paths["results"]).is_file()
    assert Path(paths["interface_impact"]).is_file()
