"""Ideation-organizer dispatch orchestration (`organizer_dispatch.py`):
prepare-phase bundle build, merge-phase validation/persistence, authorized
disposition append, and the report-section integration
(add-cross-factory-ideation-routing tasks 7.1-7.4).

Above all, this proves task 7.4's hard invariant: an offline, unauthorized,
stale-signal, invalid-output, or failed organizer analysis can neither delay
nor suppress deterministic reporting — every failure mode folds into an
`OrganizerRunMeta.skipped_reason`, `merge_organizer_findings` never raises on
untrusted worker input, persists nothing on failure, and the deterministic
report renders unchanged with the organizer summarized as a non-blocking skip.

All tests are hermetic (test_catalog_dispatch.py conventions): the read-only
`fixtures/ideation-routing/` corpus, git facts from `conftest.FakeGit`, a fake
worker (the fixture shell script, or an inline dict) for the model-invocation
boundary, and every write under a tmp evidence root. No live model calls; no
wall clock (`conftest.AS_OF`)."""

from __future__ import annotations

import json
import os
import subprocess
from datetime import date
from types import SimpleNamespace

import pytest

from conftest import AS_OF, FIXTURES, FakeGit  # noqa: F401 (sys.path side effect)

from doc_health import (CRITICAL, ERROR, Finding, ideation_routing,
                        organizer, report)
from doc_health import organizer_dispatch as od

WORKSPACE = FIXTURES / "ideation-routing"
HEADS = {"openxFactory": "b" * 40, "MedxFactory": "a" * 40}
MODEL = od.DEFAULT_MODEL
IDEA = "XFI-2026-014"  # the fixture's unclassified/intake inbox idea
IDEA_SRC = "ideation/brainstorm/inbox/XFI-2026-014/idea.md"

HOST = {"tenant_boundary": "opensoft", "data_boundary": "opensoft-internal",
        "handling_classes": ["internal-governance"]}

FAKE_WORKER = FIXTURES / "fake-claude-organizer.sh"
FAKE_WORKER_INVALID = FIXTURES / "fake-claude-organizer-invalid.sh"


def setup():
    """The governed routing corpus (openxFactory + MedxFactory fixture repos)
    and the FakeGit that resolves each repo's committed HEAD -- the same shape
    `ideation_routing._collect` returns and `organizer.select` consumes."""
    repo_paths = {p.name: p for p in sorted(WORKSPACE.iterdir()) if p.is_dir()}
    git = FakeGit(heads=HEADS)
    records = ideation_routing._collect(
        SimpleNamespace(repo_paths=repo_paths))[0]
    return records, repo_paths, git


def dispatched(records, as_of=AS_OF, model=MODEL, **select_kwargs):
    """The (selection, job, job_id) the prepare phase would dispatch first --
    reconstructed with the same public functions the dispatch glue uses
    internally (test_catalog_dispatch's `first_shard_and_job` convention)."""
    rid = od._run_id(records, as_of)
    prompt_version, _ = organizer.load_prompt_contract()
    sels = organizer.dispatchable(
        organizer.select(records, None, as_of=as_of, **select_kwargs))
    first = od._dispatch_order(sels)[0]
    job = organizer.envelope(as_of, first, rid, model, prompt_version)
    return first, job, job["job"]["id"]


def run_fake_worker(script, **env_overrides) -> str:
    env = dict(os.environ)
    env.update({k: str(v) for k, v in env_overrides.items()})
    return subprocess.run(["sh", str(script)], capture_output=True, text=True,
                          env=env, check=True).stdout


def recommendation(cid="candidate-01", repo="openxFactory", path=IDEA_SRC,
                   section="problem-statement",
                   passage="Could be neutral doc-health or Ops monitoring.",
                   **overrides):
    rec = {"claim_candidate_id": cid,
           "source_ref": {"repository": repo, "path": path,
                          "section": section, "passage": passage},
           "summary": "Cross-repo freshness signal",
           "recommended_scope": "unclassified", "alternatives": [],
           "domain_local_exclusions": [], "ambiguity": ["Owner unknown"],
           "rationale": "Captured before ownership is known.",
           "confidence": 0.72}
    rec.update(overrides)
    return rec


def write_artifact(tmp_path, job_id, recommendations):
    path = tmp_path / f"{job_id}.json"
    path.write_text(json.dumps({"recommendations": recommendations}),
                    encoding="utf-8")
    return path


# --- smoke -------------------------------------------------------------------

def test_module_imports_and_meta_constructs_with_all_fields():
    meta = od.OrganizerRunMeta(
        selected=2, dispatchable=1, by_reason={"changed": 1, "manual": 1},
        ready=True, readiness_reason="ready", authorized=1,
        authorization_denied=0, skipped_reason=None, queue_timeouts=0,
        run_timeouts=0, runs=1, rejected=0, recommendation_count=1,
        dispatched_idea=IDEA, evidence_refs=["e.yaml"],
        linked_evidence_refs=["e.yaml"], model=MODEL, prompt_version=1,
        run_id="abc", deviations=[])
    assert meta.selected == 2 and meta.dispatched_idea == IDEA
    assert od.WORKER_UNAVAILABLE == "worker_unavailable"
    assert od.CHILD_QUEUE_TIMEOUT == "child_queue_timeout"
    assert od.CHILD_TIMEOUT == "child_timeout"
    assert od.OrganizerRunMeta().evidence_refs == []
    assert od.OrganizerRunMeta().by_reason == {}


def test_run_id_is_deterministic_and_wall_clock_free():
    records, _, _ = setup()
    assert od._run_id(records, AS_OF) == od._run_id(records, AS_OF)
    assert od._run_id(records, AS_OF) != od._run_id(records, date(2026, 7, 10))


# --- prepare (task 7.1) ------------------------------------------------------

def test_prepare_selects_and_bundles_the_unclassified_idea(tmp_path):
    records, repo_paths, git = setup()
    out = tmp_path / "bundle"
    meta = od.prepare_organizer_bundle(
        records, repo_paths, AS_OF, out, MODEL,
        allowed_output_root=tmp_path, git=git, host=HOST)
    # XFI-2026-014 (unclassified/intake) qualifies as `changed`; XFI-2026-003
    # (routed) never ages and is not a qualifying scope, so is not selected.
    assert meta["by_reason"] == {"changed": 1}
    assert meta["dispatchable"] == 1 and meta["idea_count"] == 1
    assert meta["authorized"] == 1 and meta["authorization_denied"] == 0
    job_ids = json.loads((out / "ideas.json").read_text())
    assert len(job_ids) == 1 and job_ids[0].startswith("IDEAORG-")
    assert (out / "prompt.md").is_file()
    assert (out / "output.schema.json").is_file()
    assert (out / "ideas" / f"{job_ids[0]}.input.txt").is_file()
    # The self-contained input embeds the committed source, framed as data.
    body = (out / "ideas" / f"{job_ids[0]}.input.txt").read_text()
    assert "Untrusted idea payload" in body and IDEA_SRC in body


def test_prepare_writes_no_evidence_or_routing_state(tmp_path):
    # Prepare is bundle-only (spec "a temporary workflow artifact alone MUST
    # NOT satisfy persistence"): nothing lands under health/ideation-organizer/.
    records, repo_paths, git = setup()
    od.prepare_organizer_bundle(records, repo_paths, AS_OF, tmp_path / "b",
                                MODEL, allowed_output_root=tmp_path, git=git,
                                host=HOST)
    assert not (tmp_path / "health" / "ideation-organizer").exists()


def test_prepare_is_deterministic_on_a_clean_rerun(tmp_path):
    records, repo_paths, git = setup()
    a = od.prepare_organizer_bundle(records, repo_paths, AS_OF,
                                    tmp_path / "b1", MODEL,
                                    allowed_output_root=tmp_path, git=git,
                                    host=HOST)
    b = od.prepare_organizer_bundle(records, repo_paths, AS_OF,
                                    tmp_path / "b2", MODEL,
                                    allowed_output_root=tmp_path, git=git,
                                    host=HOST)
    assert a == b
    assert (tmp_path / "b1" / "ideas.json").read_text() == \
        (tmp_path / "b2" / "ideas.json").read_text()


def test_prepare_rejects_output_outside_boundary(tmp_path):
    records, repo_paths, git = setup()
    with pytest.raises(ValueError, match="escapes"):
        od.prepare_organizer_bundle(
            records, repo_paths, AS_OF, tmp_path.parent / "outside", MODEL,
            allowed_output_root=tmp_path, git=git, host=HOST)


def test_prepare_fails_closed_when_no_host_attestation(tmp_path):
    # spec "Missing readiness or authorization SHALL record a fail-closed skip
    # without sending source content or identifying metadata": with no host,
    # every dispatchable idea is denied and nothing is bundled.
    records, repo_paths, git = setup()
    out = tmp_path / "bundle"
    meta = od.prepare_organizer_bundle(
        records, repo_paths, AS_OF, out, MODEL,
        allowed_output_root=tmp_path, git=git, host=None)
    assert meta["dispatchable"] == 1
    assert meta["authorized"] == 0 and meta["authorization_denied"] == 1
    assert meta["idea_count"] == 0
    assert json.loads((out / "ideas.json").read_text()) == []
    assert not (out / "ideas").exists()  # no idea content bundled at all


def test_prepare_denies_source_whose_handling_is_unauthorized(tmp_path):
    # A source whose declared handling is not among the host's authorized
    # classes is denied (fail closed) and never bundled.
    records, repo_paths, git = setup()
    policy = {("openxFactory", IDEA_SRC): {
        "tenant_boundary": "opensoft", "data_boundary": "opensoft-internal",
        "handling": "protected", "redaction_permitted": False}}
    out = tmp_path / "bundle"
    meta = od.prepare_organizer_bundle(
        records, repo_paths, AS_OF, out, MODEL, allowed_output_root=tmp_path,
        git=git, host=HOST, source_handling=policy)
    assert meta["authorized"] == 0 and meta["authorization_denied"] == 1
    assert meta["idea_count"] == 0


def test_prepare_manual_request_selects_a_non_qualifying_idea(tmp_path):
    # spec trigger "Manual operator request": a named Idea ID is reviewed even
    # when its scope/status would not qualify on its own.
    records, repo_paths, git = setup()
    meta = od.prepare_organizer_bundle(
        records, repo_paths, AS_OF, tmp_path / "b", MODEL,
        allowed_output_root=tmp_path, git=git, host=HOST,
        manual_idea_ids=["XFI-2026-003"])
    assert meta["by_reason"].get("manual") == 1


# --- merge success (task 7.2) ------------------------------------------------

def test_merge_success_from_fake_worker_artifact_persists_evidence(tmp_path):
    records, repo_paths, git = setup()
    _, _, job_id = dispatched(records)
    text = run_fake_worker(FAKE_WORKER, REPO="openxFactory", DOC_PATH=IDEA_SRC)
    path = tmp_path / f"{job_id}.json"
    path.write_text(text, encoding="utf-8")

    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=path, host=HOST)

    assert meta.skipped_reason is None and meta.rejected == 0
    assert meta.recommendation_count == 1 and meta.runs == 1
    assert meta.dispatched_idea == IDEA and meta.model == MODEL
    assert meta.authorized == 1 and meta.authorization_denied == 0
    assert len(meta.evidence_refs) == 1
    ev = tmp_path / "health" / "ideation-organizer" / AS_OF.isoformat() / \
        f"{IDEA}-{meta.run_id}.yaml"
    assert ev.is_file()
    # The persisted record is immutable evidence (status: record); the raw
    # passage was reduced to a digest and dropped, never copied centrally.
    doc = json.loads(ev.read_text())
    assert doc["status"] == "record"
    assert doc["kind"] == organizer.RECOMMENDATION_KIND
    sref = doc["recommendations"][0]["source_ref"]
    assert "passage_sha256" in sref and "passage" not in sref
    assert doc["recommendations"][0]["disposition"] == "pending_review"
    assert meta.linked_evidence_refs  # linked for the report


def test_merge_persists_when_job_id_omitted_single_idea(tmp_path):
    records, repo_paths, git = setup()
    _, _, job_id = dispatched(records)
    path = write_artifact(tmp_path, job_id, [recommendation()])
    # job_id recovered from the filename stem (single-idea auto-inference).
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=path, host=HOST)
    assert meta.recommendation_count == 1 and meta.evidence_refs


def test_merge_is_idempotent_on_identical_replay(tmp_path):
    records, repo_paths, git = setup()
    _, _, job_id = dispatched(records)
    path = write_artifact(tmp_path, job_id, [recommendation()])
    first = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=path, host=HOST)
    again = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=path, host=HOST)
    assert first.evidence_refs == again.evidence_refs  # exclusive-write no-op


# --- merge failure modes (task 7.4): never delay/suppress deterministic ------

def test_merge_offline_no_findings_records_skip_and_persists_nothing(tmp_path):
    records, repo_paths, git = setup()
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=None, unavailable_reason=None, host=HOST)
    assert meta.skipped_reason == od.WORKER_UNAVAILABLE
    assert meta.recommendation_count == 0 and meta.evidence_refs == []
    assert not (tmp_path / "health" / "ideation-organizer").exists()


def test_merge_queue_timeout_records_watchdog_queue_count(tmp_path):
    records, repo_paths, git = setup()
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=None, unavailable_reason=od.CHILD_QUEUE_TIMEOUT,
        host=HOST)
    assert meta.skipped_reason == od.CHILD_QUEUE_TIMEOUT
    assert meta.queue_timeouts == 1 and meta.run_timeouts == 0
    assert meta.evidence_refs == []


def test_merge_run_timeout_records_watchdog_run_count(tmp_path):
    records, repo_paths, git = setup()
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=None, unavailable_reason=od.CHILD_TIMEOUT, host=HOST)
    assert meta.skipped_reason == od.CHILD_TIMEOUT
    assert meta.run_timeouts == 1 and meta.queue_timeouts == 0


def test_merge_child_conclusion_reasons_are_recorded(tmp_path):
    records, repo_paths, git = setup()
    for reason in ("child_failure", "child_cancelled"):
        meta = od.merge_organizer_findings(
            records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
            findings_path=None, unavailable_reason=reason, host=HOST)
        assert meta.skipped_reason == reason and meta.evidence_refs == []


def test_merge_missing_findings_file_is_skipped_not_crashed(tmp_path):
    records, repo_paths, git = setup()
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=tmp_path / "absent.json", host=HOST)
    assert meta.rejected == 0 and "missing" in meta.skipped_reason
    assert meta.evidence_refs == []


def test_merge_unreadable_findings_file_is_skipped_not_crashed(tmp_path):
    records, repo_paths, git = setup()
    _, _, job_id = dispatched(records)
    bad = tmp_path / f"{job_id}.json"
    bad.write_text("{ this is not json", encoding="utf-8")
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=bad, host=HOST)
    assert meta.rejected == 0 and "unreadable" in meta.skipped_reason


def test_merge_job_id_mismatch_is_skipped_not_crashed(tmp_path):
    records, repo_paths, git = setup()
    path = tmp_path / "IDEAORG-doesnotexist.json"
    path.write_text(json.dumps({"recommendations": [recommendation()]}),
                    encoding="utf-8")
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=path, host=HOST)
    assert meta.rejected == 0
    assert "does not match any idea" in meta.skipped_reason
    assert meta.evidence_refs == []


def test_merge_invalid_output_is_rejected_not_crashed(tmp_path):
    records, repo_paths, git = setup()
    _, _, job_id = dispatched(records)
    text = run_fake_worker(FAKE_WORKER_INVALID, REPO="openxFactory",
                           DOC_PATH=IDEA_SRC)
    path = tmp_path / f"{job_id}.json"
    path.write_text(text, encoding="utf-8")
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=path, host=HOST)
    assert meta.rejected == 1 and "rejected" in meta.skipped_reason
    assert meta.recommendation_count == 0 and meta.evidence_refs == []
    assert not (tmp_path / "health" / "ideation-organizer").exists()


def test_merge_unauthorized_host_fails_closed_and_persists_nothing(tmp_path):
    # A valid artifact for an idea whose host is not attested: fail-closed skip,
    # nothing persisted centrally (defense in depth beyond the prepare gate).
    records, repo_paths, git = setup()
    _, _, job_id = dispatched(records)
    path = write_artifact(tmp_path, job_id, [recommendation()])
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=path, host=None)
    assert meta.authorization_denied == 1 and meta.authorized == 0
    assert "fail closed" in meta.skipped_reason
    assert meta.recommendation_count == 0 and meta.evidence_refs == []
    assert not (tmp_path / "health" / "ideation-organizer").exists()


def test_merge_stale_catalog_signal_never_selects_or_persists(tmp_path):
    # spec "Catalog entry is stale": a stale signal is dropped by
    # eligible_catalog_signals, so it can neither add a selection nor cause any
    # persistence -- the deterministic run is untouched.
    records, repo_paths, git = setup()
    stale = organizer.eligible_catalog_signals(
        {"repos": {"openxFactory": {
            "run": {"inventory_snapshot_id": "OLD"},
            "taxonomy": {"digest": "OLD"},
            "entries": [{"repo": "openxFactory", "path": "docs/guide.md",
                         "content_hash": "h", "facet_assignments": []}]}}},
        [{"repo": "openxFactory", "path": "docs/guide.md",
          "content_hash": "DIFFERENT", "snapshot_id": "NEW"}], "CURRENT")
    assert stale == []  # stale, dropped
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=None, catalog_signals=stale, host=HOST)
    # Only the deterministic `changed` selection remains; no signal was added.
    assert "catalog_signal" not in meta.by_reason
    assert meta.evidence_refs == []


# --- output-policy filtering on the merge path (task 7.2 / spec 5.4) ---------

def test_merge_protected_path_drops_all_recs_records_skip(tmp_path):
    records, repo_paths, git = setup()
    _, _, job_id = dispatched(records)
    path = write_artifact(tmp_path, job_id, [recommendation()])
    policies = {("openxFactory", IDEA_SRC): {"path_protected": True}}
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=path, host=HOST, output_policies=policies)
    assert meta.recommendation_count == 0 and meta.evidence_refs == []
    assert "suppressed by source output policy" in meta.skipped_reason


def test_merge_field_suppression_persists_with_blanked_fields(tmp_path):
    records, repo_paths, git = setup()
    _, _, job_id = dispatched(records)
    path = write_artifact(tmp_path, job_id,
                          [recommendation(proposed_owner="openxFactory")])
    policies = {("openxFactory", IDEA_SRC): {"suppress": {"proposed_owner"}}}
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=path, host=HOST, output_policies=policies)
    assert meta.recommendation_count == 1 and meta.evidence_refs
    doc = json.loads((tmp_path / "health" / "ideation-organizer" /
                      AS_OF.isoformat() /
                      f"{IDEA}-{meta.run_id}.yaml").read_text())
    # The prohibited proposed_owner is blanked (null), never copied centrally.
    assert doc["recommendations"][0]["proposed_owner"] is None


# --- evidence linking for the NEXT report (task 7.2) -------------------------

def test_prior_evidence_is_linked_by_a_later_skipping_run(tmp_path):
    # spec "Organizer evidence lands after report finalization": evidence in
    # the immutable tree is summarized by the NEXT report even when the current
    # run itself dispatches nothing -- linked_evidence scans the durable tree,
    # never a single run's in-memory result, and never edits a closed report.
    records, repo_paths, git = setup()
    _, _, job_id = dispatched(records)
    path = write_artifact(tmp_path, job_id, [recommendation()])
    first = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=path, host=HOST)
    assert first.evidence_refs

    # A later run that is itself offline still links the earlier evidence.
    later = od.merge_organizer_findings(
        records, repo_paths, date(2026, 7, 10), MODEL, git=git,
        evidence_root=tmp_path, findings_path=None,
        unavailable_reason=od.WORKER_UNAVAILABLE, host=HOST)
    assert later.evidence_refs == []  # this run persisted nothing
    assert first.evidence_refs[0].endswith(later.linked_evidence_refs[0])


def test_linked_evidence_reads_only_never_writes(tmp_path):
    records, repo_paths, git = setup()
    assert od.linked_evidence(tmp_path) == []  # empty tree
    assert not (tmp_path / "health").exists()  # scanning created nothing


# --- non-default watchdog thresholds are disclosed (spec) --------------------

def test_non_default_watchdog_thresholds_reported_as_deviation(tmp_path):
    records, repo_paths, git = setup()
    meta = od.merge_organizer_findings(
        records, repo_paths, AS_OF, MODEL, git=git, evidence_root=tmp_path,
        findings_path=None, host=HOST, queue_timeout_seconds=300,
        run_timeout_seconds=900)
    assert any("queue-timeout=300s" in d for d in meta.deviations)
    assert any("run-timeout=900s" in d for d in meta.deviations)


# --- authorized disposition append onto the routing record (task 7.2) --------

def routing_014():
    records, _, _ = setup()
    return next(r for _, _, r in records if r["idea_id"] == IDEA)


def test_authorized_accept_advances_claim_and_records_evidence():
    rec = routing_014()
    ref = "health/ideation-organizer/2026-07-09/XFI-2026-014-abc.yaml"
    updated = od.append_disposition(
        rec, "XFI-2026-014-C01", "accepted",
        actor_ref="openxFactory ratify gate", evidence_ref=ref,
        occurred_at="2026-07-14T00:00:00Z", authorized=True)
    claim = updated["claims"][0]
    assert claim["disposition"] == "proposed"  # unresolved -> proposed (legal)
    last = claim["transitions"][-1]
    assert last["from"] == "unresolved" and last["to"] == "proposed"
    assert last["evidence_refs"] == [ref]
    assert last["actor_ref"] == "openxFactory ratify gate"


def test_authorized_reject_moves_claim_to_rejected():
    rec = routing_014()
    updated = od.append_disposition(
        rec, "XFI-2026-014-C01", "rejected", actor_ref="owner",
        evidence_ref="e.yaml", occurred_at="t", authorized=True)
    assert updated["claims"][0]["disposition"] == "rejected"


def test_unauthorized_disposition_fails_closed_and_changes_nothing():
    rec = routing_014()
    before = json.dumps(rec, sort_keys=True)
    with pytest.raises(PermissionError):
        od.append_disposition(rec, "XFI-2026-014-C01", "accepted",
                              actor_ref="x", evidence_ref="e",
                              occurred_at="t", authorized=False)
    assert json.dumps(rec, sort_keys=True) == before  # untouched


def test_disposition_append_is_append_only_and_never_mutates_input():
    rec = routing_014()
    before = json.dumps(rec, sort_keys=True)
    prior_len = len(rec["claims"][0]["transitions"])
    updated = od.append_disposition(
        rec, "XFI-2026-014-C01", "accepted", actor_ref="a",
        evidence_ref="e.yaml", occurred_at="t", authorized=True)
    # Input deep-copied and untouched; the update only appends one transition.
    assert json.dumps(rec, sort_keys=True) == before
    assert len(updated["claims"][0]["transitions"]) == prior_len + 1
    assert updated["claims"][0]["transitions"][:prior_len] == \
        rec["claims"][0]["transitions"]


def test_illegal_disposition_transition_is_refused():
    rec = routing_014()
    rec["claims"][0]["disposition"] = "routed"  # terminal
    with pytest.raises(ValueError, match="illegal|no legal forward"):
        od.append_disposition(rec, "XFI-2026-014-C01", "accepted",
                              actor_ref="a", evidence_ref="e",
                              occurred_at="t", authorized=True)


def test_disposition_requires_known_claim_and_evidence_ref():
    rec = routing_014()
    with pytest.raises(ValueError, match="no claim"):
        od.append_disposition(rec, "XFI-2026-999-C01", "accepted",
                              actor_ref="a", evidence_ref="e",
                              occurred_at="t", authorized=True)
    with pytest.raises(ValueError, match="evidence-record"):
        od.append_disposition(rec, "XFI-2026-014-C01", "accepted",
                              actor_ref="a", evidence_ref="",
                              occurred_at="t", authorized=True)


def test_disposition_module_has_no_report_editing_surface():
    # 7.2 "never editing closed reports": the disposition adapter touches only
    # the routing record it is handed and returns it; it has no report path,
    # no writer, and no lifecycle-mutation entry point beyond this one append.
    assert not hasattr(od, "edit_report")
    assert not hasattr(od, "write_report")


# --- report section (task 7.3): counts render, never block -------------------

def _meta(**overrides):
    fields = dict(
        selected=3, dispatchable=2, by_reason={"changed": 2, "aging": 1},
        ready=True, readiness_reason="ready", authorized=2,
        authorization_denied=1, skipped_reason="child_timeout",
        queue_timeouts=1, run_timeouts=1, runs=1, rejected=1,
        recommendation_count=2, dispatched_idea=IDEA,
        evidence_refs=["health/ideation-organizer/2026-07-09/"
                       "XFI-2026-014-abc.yaml"],
        linked_evidence_refs=["health/ideation-organizer/2026-07-09/"
                              "XFI-2026-014-abc.yaml"],
        model=MODEL, prompt_version=1, run_id="abc",
        deviations=["organizer queue-timeout=300s (default 600s)"])
    fields.update(overrides)
    return od.OrganizerRunMeta(**fields)


def test_report_section_renders_every_count():
    text = report.render(AS_OF, [], [], [], [], 0, [], [],
                         organizer_meta=_meta())
    assert "## Ideation Organizer" in text
    assert "Skipped: child_timeout" in text
    assert "selection: 3 selected, 2 dispatchable (aging=1, changed=2)" in text
    assert "readiness: ready=true (ready)" in text
    assert "authorization: 2 authorized, 1 denied" in text
    assert "watchdog: 1 queue timeout(s), 1 run timeout(s), 1 run(s)" in text
    assert ("recommendations: 2 (dispatched idea XFI-2026-014, rejected 1)"
            in text)
    assert "organizer: prompt contract v1, model claude-sonnet-5" in text
    assert "evidence (this run): health/ideation-organizer" in text
    assert "linked evidence: 1 record(s)" in text
    assert "non-default configuration: organizer queue-timeout=300s" in text
    assert text.index("## Ideation Organizer") < \
        text.index("## Findings By Family")


def test_report_section_omits_optionals_when_absent():
    text = report.render(AS_OF, [], [], [], [], 0, [], [],
                         organizer_meta=_meta(skipped_reason=None,
                                              deviations=[],
                                              evidence_refs=[],
                                              linked_evidence_refs=[]))
    assert "Skipped:" not in text
    assert "non-default configuration:" not in text
    assert "evidence (this run): (none)" in text
    assert "linked evidence: 0 record(s)" in text


def test_report_section_never_leaks_into_ranked_plan():
    # 7.3 hard invariant: organizer counts are read-only render input -- no
    # organizer content ever becomes a Ranked Plan line or a regression, even
    # beside a real finding from an unrelated family.
    meta = _meta()
    findings = [Finding(ERROR, "tag-hygiene", "alpha", "docs/x.md",
                        "missing status header", "add a Status: header")]
    text = report.render(AS_OF, findings, [], [], [], 0, [], [],
                         organizer_meta=meta)
    assert "## Ideation Organizer" in text
    plan = [l for l in text.splitlines() if l.startswith("- severity=")]
    assert len(plan) == 1
    m = report.PLAN_RE.match(plan[0])
    assert m and m.group(2) == "tag-hygiene"
    for value in (meta.dispatched_idea, meta.skipped_reason, meta.model,
                  *meta.evidence_refs):
        assert not any(value in line for line in plan)


def test_report_without_organizer_meta_has_no_section():
    text = report.render(AS_OF, [], [], [], [], 0, [], [])
    assert "## Ideation Organizer" not in text


def test_organizer_skip_never_blocks_deterministic_report():
    # The whole point of 7.4: with the organizer recorded as an offline skip
    # AND real critical/error findings present, the report still renders the
    # ranked plan and regression set exactly as it would without the organizer.
    findings = [Finding(CRITICAL, "standard-backing", "a", "p", "r", "act")]
    new = report.regressions(findings, set())  # all new vs empty previous
    meta = _meta(skipped_reason=od.WORKER_UNAVAILABLE, recommendation_count=0,
                 evidence_refs=[])
    with_org = report.render(AS_OF, findings, [], [], [], 0, [], new,
                             organizer_meta=meta)
    without = report.render(AS_OF, findings, [], [], [], 0, [], new)
    # The deterministic content (ranked plan + regression headline) is
    # byte-identical apart from the extra non-blocking organizer section.
    assert "New regressions vs previous report: 1" in with_org
    plan_with = [l for l in with_org.splitlines() if l.startswith("- severity=")]
    plan_without = [l for l in without.splitlines()
                    if l.startswith("- severity=")]
    assert plan_with == plan_without
