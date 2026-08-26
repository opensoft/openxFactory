"""SC-008: results validate against the owned schema; schema drift-guard to registered copy."""
import hashlib
from pathlib import Path

from avatar_f0.evidence import (SCHEMAS_DIR, build_interface_impact, finalize_record,
                                validate_interface_impact, validate_results, write_evidence)
from avatar_f0.run import build_inconclusive_record, inconclusive_report_md

REPO_ROOT = Path(__file__).resolve().parents[4]
_CHANGE = "qualify-avatar-brokered-call-feasibility"
_SCHEMA_NAME = "f0-results.schema.yaml"
REGISTERED_SHA = "6a94e4a38e08ba5f1eb32dfa3956cec15d9393a4f63019757a270ecb8ee3dc6f"


def _registered_schema_bytes() -> bytes:
    """The registered copy in the owning change — live, or in the packaged
    archive bundle once the change archives (issue #30 option C: the change
    moves and its supporting-docs tarball, but the drift guard keeps
    guarding the same bytes)."""
    live = REPO_ROOT / "openspec/changes" / _CHANGE / "supporting-docs" / _SCHEMA_NAME
    if live.is_file():
        return live.read_bytes()
    (archived,) = REPO_ROOT.glob(f"openspec/changes/archive/*-{_CHANGE}")
    loose = archived / "supporting-docs" / _SCHEMA_NAME
    if loose.is_file():
        return loose.read_bytes()
    import tarfile
    with tarfile.open(archived / "supporting-docs.tar.gz", "r:gz") as bundle:
        stream = bundle.extractfile(_SCHEMA_NAME)
        assert stream is not None, f"{_SCHEMA_NAME} missing from packaged archive"
        return stream.read()


def test_results_schema_drift_guard():
    owned = (SCHEMAS_DIR / "f0-results.schema.yaml").read_bytes()
    assert hashlib.sha256(owned).hexdigest() == REGISTERED_SHA
    # byte-identical to the registered supporting-docs copy
    assert owned == _registered_schema_bytes()


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
