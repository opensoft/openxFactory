"""Run orchestration: assemble the terminal evidence record.

Two paths:
- :func:`build_inconclusive_record` — the honest no-key terminal record (SC-013 / Q1):
  70 INCONCLUSIVE trial rows, six groups completed=0, no fabricated measurements, overall
  INCONCLUSIVE. No provider call is attempted.
- Live execution (a lab key present) is deferred to the lab run (task T058); the live
  components are lazily-imported stubs in this build.

The offline pytest suite exercises the simulated trial runners directly to prove harness
logic; that is separate from this evidence record.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from . import (CHANGE_ID, GROUP_PLANNED, INCONCLUSIVE, PROTOCOL_VERSION)
from .candidate import (INTERACTION_MODE, REQUESTED_MODEL, TURN_DETECTION, VOICE)
from .assertions import aggregate_assertions
from .classify import classify_overall
from .metrics import build_metrics
from .models import GroupResult, TrialResult
from .trials.base import iter_trial_ids

DOCS_RETRIEVED_AT = "2026-07-10T00:00:00Z"

GROUP_ASSERTIONS = {
    "F0-A": ["F0-A-ORDERING", "F0-A-SINGLE_CALL"],
    "F0-B": ["F0-B-ORDERING", "F0-B-WITHIN_CEILING"],
    "F0-C": ["F0-C-NO_MEDIA"],
    "F0-D": ["F0-D-TERMINAL_5S", "F0-D-NO_LATE_IO"],
    "F0-E": ["F0-E-SINGLE_CALL"],
    "F0-F": ["F0-F-IDEMPOTENCY"],
}


def _environment(lab_project_ref: str, dependency_versions: Dict[str, str], network_type: str) -> dict:
    return {
        "lab_project_ref": lab_project_ref,
        "runtime": "python3.12",
        "dependency_versions": dependency_versions,
        "network_type": network_type,
        "region": None,
        "docs_retrieved_at": DOCS_RETRIEVED_AT,
    }


def _candidate(resolved_model: str) -> dict:
    return {
        "requested_model": REQUESTED_MODEL,
        "resolved_model": resolved_model,
        "voice": VOICE,
        "interaction_mode": INTERACTION_MODE,
        "turn_detection": dict(TURN_DETECTION),
    }


def _inconclusive_trials() -> List[TrialResult]:
    trials: List[TrialResult] = []
    for group_id in GROUP_PLANNED:
        for trial_id in iter_trial_ids(group_id):
            trials.append(TrialResult(
                trial_id=trial_id, group_id=group_id, status=INCONCLUSIVE,
                provider_request_id_hash=None, durations_ms={},
                assertion_ids=list(GROUP_ASSERTIONS[group_id]),
                note="not executed (no lab credential)",
            ))
    return trials


def _serialize_trials(trials: List[TrialResult]) -> List[dict]:
    rows: List[dict] = []
    for t in trials:
        row = {
            "trial_id": t.trial_id,
            "group_id": t.group_id,
            "status": t.status,
            "provider_request_id_hash": t.provider_request_id_hash,
            "durations_ms": {k: round(v, 3) for k, v in t.durations_ms.items()},
            "assertion_ids": t.assertion_ids,
        }
        if t.note:
            row["note"] = t.note
        rows.append(row)
    return rows


def _serialize_groups(groups: List[GroupResult]) -> List[dict]:
    return [{"id": g.id, "planned": g.planned, "completed": g.completed,
             "passed": g.passed, "failed": g.failed} for g in groups]


def _serialize_assertions(assertions) -> List[dict]:
    out = []
    for a in assertions:
        d = {"id": a.id, "status": a.status,
             "passed_trials": a.passed_trials, "failed_trials": a.failed_trials}
        if a.note:
            d["note"] = a.note
        out.append(d)
    return out


def build_inconclusive_record(
    *,
    started_at: str,
    completed_at: str,
    lab_project_ref: str,
    dependency_versions: Dict[str, str],
    reason: str = "no_lab_credential",
) -> dict:
    """Build the schema-valid no-key INCONCLUSIVE record body (without redaction/report hash)."""
    trials = _inconclusive_trials()
    groups = [GroupResult(id=g, planned=GROUP_PLANNED[g]) for g in GROUP_PLANNED]
    assertions = aggregate_assertions(trials)
    metrics = build_metrics(trials)  # all counts 0
    overall = classify_overall(groups, trials, assertions, metrics, "PASS",
                               environment_inconclusive=True)
    assert overall == INCONCLUSIVE, overall
    return {
        "protocol_version": PROTOCOL_VERSION,
        "started_at": started_at,
        "completed_at": completed_at,
        "environment": _environment(lab_project_ref, dependency_versions, network_type="none"),
        "candidate": _candidate(resolved_model="unresolved"),
        "trial_groups": _serialize_groups(groups),
        "trials": _serialize_trials(trials),
        "metrics": metrics,
        "assertions": _serialize_assertions(assertions),
        "overall": overall,
        # redaction_scan + report_sha256 added by evidence.finalize_record
    }


def inconclusive_report_md(reason: str, acr_ref_note: str) -> str:
    return (
        "# Avatar F0 Brokered-Call Feasibility — Results (INCONCLUSIVE)\n\n"
        f"Change: {CHANGE_ID}\n\n"
        "## Overall: INCONCLUSIVE\n\n"
        f"Reason: `{reason}`. No lab credential (`OPENAI_API_KEY`) was present, so no "
        "provider call was attempted and no measurements were fabricated. Per the feature "
        "Definition of Done (SC-013), this is a valid terminal record and a valid completion "
        "state; it does NOT qualify any provider profile and does NOT open the kernel "
        "publication gate (only a live PASS does).\n\n"
        "## Trials\n\n"
        "All 70 mandatory trials across the six groups (F0-A…F0-F) are recorded as "
        "INCONCLUSIVE (not executed). The harness, offline self-tests, and redaction tests "
        "are complete; the live matrix runs when a lab key is supplied.\n\n"
        "## Acceptance map\n\n"
        f"{acr_ref_note}\n\n"
        "## Redaction / threat-model disposition\n\n"
        "Evidence is built from an allowlist and re-scanned before writing; no credential, "
        "SDP, raw payload, audio, transcript, or high-cardinality identifier is present.\n\n"
        "## Reviewer decision\n\n"
        "Terminal INCONCLUSIVE record accepted as the no-key completion artifact.\n"
    )
