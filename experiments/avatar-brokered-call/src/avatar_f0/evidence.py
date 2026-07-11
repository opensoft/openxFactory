"""Evidence writer: schema-valid, redacted, sole-path (FR-015/FR-016/FR-017/FR-018/SC-011).

Writes the three artifacts directly and atomically under the change's ``evidence/`` dir —
the only committed evidence location, with no second copy. A write-path allowlist ensures
a run mutates nothing outside its two owned locations.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from jsonschema.validators import Draft202012Validator

from . import CHANGE_ID, FAIL, INTERFACE_BASELINE, PROTOCOL_VERSION
from .redaction import scan, scan_prose

_PKG_ROOT = Path(__file__).resolve().parent.parent.parent  # experiments/avatar-brokered-call
SCHEMAS_DIR = _PKG_ROOT / "schemas"
EVIDENCE_RELPATH = f"openspec/changes/{CHANGE_ID}/evidence"
OWNED_CODE_RELPATH = "experiments/avatar-brokered-call"


class RedactionFailure(Exception):
    pass


class WritePathError(Exception):
    pass


def _load_schema(name: str) -> dict:
    return yaml.safe_load((SCHEMAS_DIR / name).read_text())


def validate_results(record: dict) -> None:
    Draft202012Validator(_load_schema("f0-results.schema.yaml")).validate(record)


def validate_interface_impact(doc: dict) -> None:
    Draft202012Validator(_load_schema("f0-interface-impact.schema.yaml")).validate(doc)


def assert_write_allowed(target: Path, repo_root: Path) -> None:
    target = target.resolve()
    allowed = [
        (repo_root / OWNED_CODE_RELPATH).resolve(),
        (repo_root / EVIDENCE_RELPATH).resolve(),
    ]
    if not any(str(target).startswith(str(a) + os.sep) or target == a for a in allowed):
        raise WritePathError(f"refusing to write outside owned surface: {target}")


def build_interface_impact(
    acr_source_path: str,
    acr_source_commit: str,
    acr_content_sha256: str,
    variances: Optional[List[dict]] = None,
) -> dict:
    return {
        "schema_version": 1,
        "kind": "avatar-f0-interface-impact",
        "change_id": CHANGE_ID,
        "interface_baseline": INTERFACE_BASELINE,
        "acceptance_map": {
            "source_path": acr_source_path,
            "source_commit": acr_source_commit,
            "content_sha256": acr_content_sha256,
        },
        "variances": variances or [],
    }


def finalize_record(record_body: dict, report_md: str, interface_impact: dict) -> dict:
    """Attach redaction_scan + report_sha256, then validate. Fail-closed on redaction."""
    # Scan structured evidence (field-level rules) + the prose report (prohibited classes).
    findings = scan({"record": record_body, "interface_impact": interface_impact})
    findings = findings + scan_prose(report_md)
    record = dict(record_body)
    record["redaction_scan"] = {
        "status": FAIL if findings else "PASS",
        "prohibited_findings": len(findings),
    }
    record["report_sha256"] = hashlib.sha256(report_md.encode("utf-8")).hexdigest()
    if findings:
        # Fail-closed: mark FAIL, do not permit commit (caller checks status before writing).
        record["overall"] = FAIL
    validate_results(record)
    return record


def _atomic_write(path: Path, data: str, repo_root: Path) -> None:
    assert_write_allowed(path, repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(data)
    os.replace(tmp, path)


def write_evidence(
    record: dict,
    report_md: str,
    interface_impact: dict,
    repo_root: Path,
) -> Dict[str, str]:
    """Write the three artifacts under the change evidence dir; return their paths.

    Refuses to write when a redaction finding is present (FR-017).
    """
    if record.get("redaction_scan", {}).get("status") == FAIL:
        raise RedactionFailure("redaction findings present; refusing to commit evidence")
    validate_results(record)
    validate_interface_impact(interface_impact)
    edir = (repo_root / EVIDENCE_RELPATH)
    results_path = edir / "f0-results.json"
    report_path = edir / "f0-results.md"
    impact_path = edir / "f0-interface-impact.yaml"
    _atomic_write(results_path, json.dumps(record, indent=2, sort_keys=True) + "\n", repo_root)
    _atomic_write(report_path, report_md, repo_root)
    _atomic_write(impact_path, yaml.safe_dump(interface_impact, sort_keys=True), repo_root)
    return {
        "results": str(results_path),
        "report": str(report_path),
        "interface_impact": str(impact_path),
    }
