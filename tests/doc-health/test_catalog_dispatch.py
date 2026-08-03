"""Document-cataloger dispatch orchestration (`catalog_dispatch.py`):
prepare-phase shard-bundle build and merge-phase recommendation fold.

A fake worker -- the fixture shell scripts under fixtures/ (T001), run via
subprocess and captured to a findings file -- stands in for the model
invocation everywhere; plain `--catalog-unavailable-reason` strings stand
in for the workflow watchdog's own reasons. No live model calls in tests,
following test_semantic.py/test_cataloger.py conventions. All tests are
hermetic: the fixture workspace (shared with test_catalog.py/
test_cataloger.py) is read-only, git facts come from conftest.FakeGit, and
every write lands under a tmp catalog root."""

from __future__ import annotations

import json
import os
import subprocess
from datetime import date
from pathlib import Path

import pytest

from conftest import FIXTURES, FakeGit  # noqa: F401 (sys.path side effect)

from doc_health import catalog, catalog_baseline, cataloger, inventory
from doc_health import catalog_dispatch
from doc_health.corpus import load_docs

WORKSPACE = FIXTURES / "catalog" / "workspace"
HEADS = {"alpha": "a" * 40, "openxFactory": "b" * 40}
LATER_HEADS = {"alpha": "c" * 40, "openxFactory": "d" * 40}
DAY = date(2026, 7, 9)  # AS_OF is a parameter, never wall clock
LATER_DAY = date(2026, 7, 10)

FAKE_WORKER = FIXTURES / "fake-claude-cataloger.sh"
FAKE_WORKER_INVALID = FIXTURES / "fake-claude-cataloger-invalid.sh"

MODEL = catalog_dispatch.DEFAULT_MODEL


def two_repo_setup():
    """Both fixture repositories (alpha: 5 entries, openxFactory: 10
    entries; shared with test_catalog_baseline.py) -- unlike alpha_setup(),
    used specifically to prove baseline scope narrows to ONE repository
    among several governed ones."""
    repo_paths = {p.name: p for p in sorted(WORKSPACE.iterdir())
                 if p.is_dir()}
    docs = []
    for name in sorted(repo_paths):
        docs.extend(load_docs(name, repo_paths[name]))
    inv = inventory.build_inventory(docs, repo_paths, git=FakeGit(heads=HEADS))
    return repo_paths, docs, inv


def alpha_setup():
    """One real, small fixture repo (shared with test_cataloger.py):
    docs/protected-roster.md (handling: protected, never dispatched),
    docs/widget-overview.md, docs/widget-register.md,
    examples/widget-walkthrough.md, plus the promoted
    openspec/specs/widget/spec.md -- 5 entries, 4 eligible for dispatch."""
    repo_paths = {"alpha": WORKSPACE / "alpha"}
    docs = load_docs("alpha", repo_paths["alpha"])
    inv = inventory.build_inventory(docs, repo_paths, git=FakeGit(heads=HEADS))
    return repo_paths, docs, inv


def run_fake_worker(script, **env_overrides) -> str:
    env = dict(os.environ)
    env.update({k: str(v) for k, v in env_overrides.items()})
    result = subprocess.run(["sh", str(script)], capture_output=True,
                            text=True, env=env, check=True)
    return result.stdout


def first_shard_and_job(repo_paths, inv):
    """Reconstruct the same (single, first-run) shard/job
    `prepare_catalog_bundle`/`merge_catalog_findings` would compute
    internally, using only the public `catalog.py`/`cataloger.py`
    functions -- the same convention test_cataloger.py's own
    `shard_and_job` helper uses."""
    prompt_version, _ = cataloger.load_prompt_contract()
    taxonomy = catalog_dispatch._effective_taxonomy(repo_paths, inv)
    selections = cataloger.select(
        inv, None, [], current_taxonomy_sha256=taxonomy["digest"],
        current_prompt_version=prompt_version)
    shards = cataloger.build_shards(
        selections, budget=catalog_dispatch.DEFAULT_SHARD_BUDGET)
    assert len(shards) == 1  # small fixture corpus: exactly one shard
    shard = shards[0]
    job = cataloger.envelope(DAY, MODEL, prompt_version, shard,
                             taxonomy["digest"])
    return shard, job


# --- smoke test (T005) -------------------------------------------------------

def test_module_imports_and_catalogmeta_constructs_with_all_fields():
    meta = catalog_dispatch.CatalogMeta(
        snapshot_refs=["a/b.yaml"], total_docs=5, cataloged=2,
        state_counts={"pending": 1, "suggested": 1, "reviewed": 0,
                     "overridden": 0, "unclassified": 0,
                     "policy_blocked": 0},
        new_count=1, changed_count=0, deleted_count=0, stale_count=0,
        rejected_count=0, inventory_version="abc123", taxonomy_digest="d" * 4,
        classifier_version=cataloger.CLASSIFIER_VERSION, prompt_version=1,
        model=MODEL, recommendation_refs=["r.yaml"], skipped_reason=None,
        baseline_progress=None, pending_aging={}, deviations=[])
    assert meta.total_docs == 5 and meta.model == MODEL
    assert meta.state_counts["pending"] == 1
    assert catalog_dispatch.WORKER_UNAVAILABLE == "worker_unavailable"
    assert catalog_dispatch.CHILD_QUEUE_TIMEOUT == "child_queue_timeout"
    assert catalog_dispatch.CHILD_TIMEOUT == "child_timeout"
    # Defaults are permissive (mirrors SweepMeta's trailing-defaults style).
    assert catalog_dispatch.CatalogMeta().snapshot_refs == []
    assert catalog_dispatch.CatalogMeta().deviations == []


# --- prepare_catalog_bundle (T006 / US1 acceptance) --------------------------

def test_prepare_catalog_bundle_first_run_writes_bundle_not_snapshot(
        tmp_path):
    repo_paths, docs, inv = alpha_setup()
    out_dir = tmp_path / "bundle"
    meta = catalog_dispatch.prepare_catalog_bundle(
        repo_paths, docs, DAY, tmp_path, out_dir, MODEL, inv,
        allowed_output_root=tmp_path)
    # select() sees all 5 entries (protected filtering happens in
    # build_shards, not select()); the shard itself excludes the protected
    # one, so exactly 4 documents are actually dispatched.
    assert meta["selection_count"] == 5
    assert meta["shard_count"] == 1
    assert meta["new_count"] == 5  # catalog.diff: first run, nothing prior
    assert meta["model"] == MODEL

    shard_files = sorted((out_dir / "shards").glob("*.json"))
    assert len(shard_files) == 1
    dispatched_paths = {d["path"] for f in shard_files
                        for d in json.loads(f.read_text())["documents"]}
    assert "docs/protected-roster.md" not in dispatched_paths
    assert "docs/widget-overview.md" in dispatched_paths
    assert (out_dir / "prompt.md").is_file()
    assert (out_dir / "output.schema.json").is_file()

    # Deliberately does NOT durably write the snapshot itself (module
    # docstring): a caller running prepare then merge against the SAME
    # checkout (e.g. --single-repo local/PR-gate use) would otherwise hit
    # catalog.write_snapshot's immutability guard, since run_id depends only
    # on (inventory, taxonomy) -- identical between the two phases in one
    # cycle. merge_catalog_findings is the one call that commits.
    assert catalog.load_snapshot(tmp_path) is None


def test_prepare_catalog_bundle_is_deterministic_on_a_clean_rerun(tmp_path):
    repo_paths, docs, inv = alpha_setup()
    first = catalog_dispatch.prepare_catalog_bundle(
        repo_paths, docs, DAY, tmp_path, tmp_path / "bundle-1", MODEL, inv,
        allowed_output_root=tmp_path)
    again = catalog_dispatch.prepare_catalog_bundle(
        repo_paths, docs, DAY, tmp_path, tmp_path / "bundle-2", MODEL, inv,
        allowed_output_root=tmp_path)
    assert first["run_id"] == again["run_id"]
    assert first == again


def test_prepare_then_merge_in_the_same_checkout_never_conflicts(tmp_path):
    # Regression: a caller invoking prepare then merge against the SAME
    # catalog_root (a real scenario -- e.g. --single-repo local/PR-gate use,
    # not only the two-job nightly workflow's separate ephemeral runners)
    # must never hit catalog.write_snapshot's immutability guard, since
    # run_id depends only on (inventory, taxonomy) and is therefore
    # identical between the two calls in one cycle.
    repo_paths, docs, inv = alpha_setup()
    catalog_dispatch.prepare_catalog_bundle(
        repo_paths, docs, DAY, tmp_path, tmp_path / "bundle", MODEL, inv,
        allowed_output_root=tmp_path)
    meta = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        findings_path=None, unavailable_reason=None)
    assert meta.snapshot_refs
    assert catalog.load_snapshot(tmp_path) is not None


def test_prepare_catalog_bundle_rejects_mismatched_inventory(tmp_path):
    repo_paths, docs, inv = alpha_setup()
    bad_inv = [dict(e) for e in inv]
    bad_inv[0] = dict(bad_inv[0], content_hash="0" * 64)
    with pytest.raises(ValueError, match="differs from the deterministic"):
        catalog_dispatch.prepare_catalog_bundle(
            repo_paths, docs, DAY, tmp_path, tmp_path / "bundle", MODEL,
            bad_inv, allowed_output_root=tmp_path)


def test_prepare_catalog_bundle_rejects_output_outside_boundary(tmp_path):
    repo_paths, docs, inv = alpha_setup()
    with pytest.raises(ValueError, match="escapes"):
        catalog_dispatch.prepare_catalog_bundle(
            repo_paths, docs, DAY, tmp_path, tmp_path.parent / "outside",
            MODEL, inv, allowed_output_root=tmp_path)


def test_prepare_catalog_bundle_baseline_mode_advances_one_shard(tmp_path):
    # US2 acceptance 1 / task T014: no complete baseline exists yet -- this
    # invocation runs exactly one bounded, resumable baseline shard (never
    # a full-corpus write) and dispatches zero classification shards.
    repo_paths, docs, inv = alpha_setup()
    out_dir = tmp_path / "bundle"
    meta = catalog_dispatch.prepare_catalog_bundle(
        repo_paths, docs, DAY, tmp_path, out_dir, MODEL, inv,
        allowed_output_root=tmp_path, baseline_mode=True)
    assert meta["shard_count"] == 0
    assert meta["selection_count"] == 0
    assert meta["model"] is None  # never dispatched this invocation
    bp = meta["baseline_progress"]
    assert bp["repos_total"] == 1 and bp["cataloged"] > 0
    assert not bp["complete"]  # one bounded shard, not the whole repo
    # Structurally consistent (empty) bundle: still self-contained.
    assert (out_dir / "prompt.md").is_file()
    assert (out_dir / "output.schema.json").is_file()
    assert json.loads((out_dir / "shards.json").read_text()) == []
    # This call is a preview (module docstring): nothing is committed to
    # the real mechanical snapshot from a baseline-mode prepare call.
    assert catalog.load_snapshot(tmp_path) is None
    shard_path = (tmp_path / "health" / "document-catalog" / "baseline"
                 / "shards" / "alpha" / "0001.yaml")
    assert shard_path.is_file()


def test_prepare_catalog_bundle_baseline_mode_scope_narrows_to_one_repo(
        tmp_path):
    repo_paths, docs, inv = alpha_setup()
    with pytest.raises(ValueError, match="unknown baseline scope"):
        catalog_dispatch.prepare_catalog_bundle(
            repo_paths, docs, DAY, tmp_path, tmp_path / "bundle", MODEL, inv,
            allowed_output_root=tmp_path, baseline_mode=True,
            scope="not-a-real-repo")


def test_baseline_mode_scope_advances_only_the_named_repository(tmp_path):
    # Manual scope override (data-model.md "catalog-scope"): among several
    # governed repositories, only the named one advances this invocation
    # -- the default (unscoped) order would otherwise pick "alpha" first.
    repo_paths, docs, inv = two_repo_setup()
    meta = catalog_dispatch.prepare_catalog_bundle(
        repo_paths, docs, DAY, tmp_path, tmp_path / "bundle", MODEL, inv,
        allowed_output_root=tmp_path, baseline_mode=True,
        scope="openxFactory", shard_budget=3)
    bp = meta["baseline_progress"]
    assert bp["repos_total"] == 1  # only openxFactory has any shard state
    assert bp["cataloged"] == 3 and not bp["complete"]
    shard_path = (tmp_path / "health" / "document-catalog" / "baseline"
                 / "shards" / "openxFactory" / "0001.yaml")
    assert shard_path.is_file()
    alpha_shards = (tmp_path / "health" / "document-catalog" / "baseline"
                   / "shards" / "alpha")
    assert not alpha_shards.exists()  # scope narrowed away from alpha


def test_baseline_mode_completes_and_merges_across_repeated_calls(tmp_path):
    # Driving the (single-repo) fixture baseline to completion: repeated
    # bounded prepare-phase invocations eventually cover the whole repo and
    # the deterministic merge lands, all from THIS module's own orchestration
    # entry point (not catalog_baseline.py directly).
    repo_paths, docs, inv = alpha_setup()
    for _ in range(10):  # more than enough bounded calls for 5 entries
        meta = catalog_dispatch.prepare_catalog_bundle(
            repo_paths, docs, DAY, tmp_path, tmp_path / "bundle", MODEL, inv,
            allowed_output_root=tmp_path, baseline_mode=True,
            shard_budget=2)
        if meta["baseline_progress"]["complete"]:
            break
    assert meta["baseline_progress"]["complete"]
    assert catalog_baseline.is_baseline_complete(tmp_path)


def test_merge_catalog_findings_baseline_mode_durably_advances_and_reports(
        tmp_path):
    # merge_catalog_findings's own parallel call is what durably persists
    # baseline advancement (module docstring: it runs in the job that
    # commits health/); the always-unconditional snapshot write (US1) is
    # untouched by baseline_mode.
    repo_paths, _, inv = alpha_setup()
    meta = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        findings_path=None, unavailable_reason=None, baseline_mode=True)
    assert meta.baseline_progress is not None
    assert meta.baseline_progress["repos_total"] == 1
    assert meta.model is None  # never dispatched in baseline mode
    assert meta.snapshot_refs  # the unconditional snapshot write still lands
    assert catalog.load_snapshot(tmp_path) is not None
    shard_path = (tmp_path / "health" / "document-catalog" / "baseline"
                 / "shards" / "alpha" / "0001.yaml")
    assert shard_path.is_file()  # durably recorded, unlike prepare's preview


def test_merge_catalog_findings_non_baseline_reports_no_baseline_progress(
        tmp_path):
    repo_paths, _, inv = alpha_setup()
    meta = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        findings_path=None, unavailable_reason=None)
    assert meta.baseline_progress is None


# --- merge_catalog_findings: US1 acceptance scenarios (T011) -----------------

def test_merge_no_worker_registered_records_skip_and_still_writes_snapshot(
        tmp_path):
    # Acceptance 1: no cataloger worker registered -- the deterministic
    # snapshot still lands, recording the cataloger as skipped, and the run
    # never waited on a child that was never dispatched.
    repo_paths, _, inv = alpha_setup()
    meta = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        findings_path=None, unavailable_reason=None)
    assert meta.skipped_reason == catalog_dispatch.WORKER_UNAVAILABLE
    assert meta.model is None  # never dispatched
    assert meta.rejected_count == 0
    assert meta.snapshot_refs
    assert catalog.load_snapshot(tmp_path) is not None


def test_merge_queue_timeout_reason_still_writes_snapshot(tmp_path):
    # Acceptance 2: a dispatched child that never leaves the queue records
    # child_queue_timeout, and the snapshot/report still land.
    repo_paths, _, inv = alpha_setup()
    meta = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv, findings_path=None,
        unavailable_reason=catalog_dispatch.CHILD_QUEUE_TIMEOUT)
    assert meta.skipped_reason == catalog_dispatch.CHILD_QUEUE_TIMEOUT
    assert meta.model == MODEL  # dispatch DID happen, just never finished
    assert meta.snapshot_refs


def test_merge_run_timeout_reason_still_writes_snapshot(tmp_path):
    # Acceptance 3: a dispatched child that starts running but never
    # completes records child_timeout, and finalize proceeds unaffected.
    repo_paths, _, inv = alpha_setup()
    meta = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv, findings_path=None,
        unavailable_reason=catalog_dispatch.CHILD_TIMEOUT)
    assert meta.skipped_reason == catalog_dispatch.CHILD_TIMEOUT
    assert meta.snapshot_refs


def test_merge_non_success_conclusion_reason_still_writes_snapshot(tmp_path):
    # Acceptance 4: a child returning a non-success conclusion (failed,
    # cancelled, unauthorized) records the specific reason; snapshot lands.
    repo_paths, _, inv = alpha_setup()
    for reason in ("child_failure", "child_cancelled"):
        meta = catalog_dispatch.merge_catalog_findings(
            repo_paths, DAY, tmp_path, MODEL, inv, findings_path=None,
            unavailable_reason=reason)
        assert meta.skipped_reason == reason
        assert meta.snapshot_refs


def test_merge_missing_findings_file_is_skipped_not_crashed(tmp_path):
    # PR #6 review: a missing/unreadable artifact is an availability
    # problem, not a cataloger.enforce_contract validation failure, so it
    # must not inflate rejected_count (data-model.md: rejected_count is
    # for whole-artifact contract rejections only).
    repo_paths, _, inv = alpha_setup()
    meta = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        findings_path=tmp_path / "absent.json")
    assert meta.rejected_count == 0
    assert "missing" in meta.skipped_reason
    assert meta.snapshot_refs  # still lands: unavailability never crashes


def test_merge_successful_merge_from_fake_worker_artifact(tmp_path):
    # Acceptance 5: a child that returns validated output before either
    # deadline gets its recommendation evidence merged into the snapshot.
    repo_paths, _, inv = alpha_setup()
    shard, job = first_shard_and_job(repo_paths, inv)
    job_id = job["job"]["id"]
    target = next(s for s in shard.selections
                 if s.path == "docs/widget-overview.md")

    findings_text = run_fake_worker(
        FAKE_WORKER, REPO=target.repo, DOC_PATH=target.path)
    findings_path = tmp_path / f"{job_id}.json"
    findings_path.write_text(findings_text, encoding="utf-8")

    meta = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        job_id=job_id, findings_path=findings_path)

    assert meta.rejected_count == 0
    assert meta.skipped_reason is None
    assert meta.model == MODEL
    assert meta.state_counts["suggested"] == 1
    assert meta.recommendation_refs  # persisted as immutable evidence
    snap = catalog.load_snapshot(tmp_path)
    entry = next(e for e in snap["repos"]["alpha"]["entries"]
                if e["path"] == "docs/widget-overview.md")
    fs = next(a for a in entry["facet_assignments"]
             if a["facet"] == "factory_scope")
    assert fs["values"] == ["domain"] and fs["state"] == "suggested"


def test_merge_persists_evidence_when_job_id_is_omitted(tmp_path):
    # PR #6 review: a caller relying on the single-shard job_id
    # auto-inference (_match_shard's job_id=None path) must still get its
    # recommendation evidence durably persisted -- previously this was
    # silently dropped because the persistence guard checked the
    # caller-supplied job_id directly rather than the resolved one.
    repo_paths, _, inv = alpha_setup()
    shard, job = first_shard_and_job(repo_paths, inv)
    job_id = job["job"]["id"]
    target = next(s for s in shard.selections
                 if s.path == "docs/widget-overview.md")

    findings_text = run_fake_worker(
        FAKE_WORKER, REPO=target.repo, DOC_PATH=target.path)
    findings_path = tmp_path / f"{job_id}.json"
    findings_path.write_text(findings_text, encoding="utf-8")

    meta = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        findings_path=findings_path)  # job_id deliberately omitted

    assert meta.rejected_count == 0
    assert meta.recommendation_refs  # persisted despite the omitted job_id
    assert Path(meta.recommendation_refs[0]).name == f"{job_id}.yaml"


def test_merge_rejects_a_contract_violating_fake_worker_artifact(tmp_path):
    # Spec edge case "Classifier emits partially valid output": whole-
    # artifact rejection, counted as rejected_count, entries stay pending.
    repo_paths, _, inv = alpha_setup()
    shard, job = first_shard_and_job(repo_paths, inv)
    job_id = job["job"]["id"]
    target = next(s for s in shard.selections
                 if s.path == "docs/widget-overview.md")

    findings_text = run_fake_worker(
        FAKE_WORKER_INVALID, REPO=target.repo, DOC_PATH=target.path)
    findings_path = tmp_path / f"{job_id}.json"
    findings_path.write_text(findings_text, encoding="utf-8")

    meta = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        job_id=job_id, findings_path=findings_path)

    assert meta.rejected_count == 1
    assert "rejected" in meta.skipped_reason
    assert not meta.recommendation_refs
    snap = catalog.load_snapshot(tmp_path)
    entry = next(e for e in snap["repos"]["alpha"]["entries"]
                if e["path"] == "docs/widget-overview.md")
    # No suggested facet landed; the selected-but-uncovered facets are
    # recorded explicitly pending instead (never silently dropped).
    assert all(a["state"] != "suggested" for a in entry["facet_assignments"])
    assert any(a["state"] == "pending" for a in entry["facet_assignments"])


def test_merge_job_id_mismatch_is_skipped_not_crashed(tmp_path):
    # PR #6 review: a mismatched job id is an availability/mismatch
    # problem, not a cataloger.enforce_contract validation failure, so it
    # must not inflate rejected_count either.
    repo_paths, _, inv = alpha_setup()
    findings_path = tmp_path / "recommendation.json"
    findings_path.write_text(
        json.dumps({"entries": []}), encoding="utf-8")
    meta = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        job_id="CATJOB-does-not-exist", findings_path=findings_path)
    assert meta.rejected_count == 0
    assert "does not match any shard" in meta.skipped_reason
    assert meta.snapshot_refs


# --- US2 orchestration-level acceptance (T018) --------------------------------

def test_merge_unrelated_commit_selects_nothing_for_reclassification(
        tmp_path):
    # US2 acceptance 2: an inventory change limited to an unrelated
    # repository commit (revision moves, no governed content changes)
    # selects zero entries for semantic reclassification, and the run
    # still produces a full mechanical snapshot.
    repo_paths, docs, inv = alpha_setup()
    first = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        findings_path=None, unavailable_reason=None)
    assert first.snapshot_refs

    later_inv = inventory.build_inventory(
        docs, repo_paths, git=FakeGit(heads=LATER_HEADS))
    # Sanity: revision moved, governed content did not.
    assert later_inv != inv
    assert {(e["repo"], e["path"], e["content_hash"]) for e in later_inv} \
        == {(e["repo"], e["path"], e["content_hash"]) for e in inv}

    second = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, later_inv,
        findings_path=None, unavailable_reason=None)
    assert (second.new_count, second.changed_count, second.deleted_count) \
        == (0, 0, 0)
    assert second.snapshot_refs


def test_merge_same_run_identity_is_immutable_refused_or_noop(
        tmp_path):
    # US2 acceptance 3: a second run attempting to write the same run
    # identity's snapshot is a safe no-op on identical content, and a
    # DIFFERING write under that identical identity is refused outright
    # -- the recorded artifact is never mutated either way.
    repo_paths, _, inv = alpha_setup()
    first = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        findings_path=None, unavailable_reason=None)
    recorded = Path(first.snapshot_refs[0]).read_bytes()

    # Identical replay (same as_of, inventory, catalog state): safe no-op.
    second = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        findings_path=None, unavailable_reason=None)
    assert second.snapshot_refs == first.snapshot_refs
    assert Path(second.snapshot_refs[0]).read_bytes() == recorded

    # A differing write under the SAME (as_of, inventory) run identity --
    # a real recommendation arriving for the shard this run would have
    # dispatched -- is refused, never silently overwriting the recorded
    # snapshot (catalog.py's absolute immutability guard; module
    # docstring).
    shard, job = first_shard_and_job(repo_paths, inv)
    job_id = job["job"]["id"]
    target = next(s for s in shard.selections
                 if s.path == "docs/widget-overview.md")
    findings_text = run_fake_worker(
        FAKE_WORKER, REPO=target.repo, DOC_PATH=target.path)
    findings_path = tmp_path / f"{job_id}.json"
    findings_path.write_text(findings_text, encoding="utf-8")
    with pytest.raises(catalog.CatalogError, match="immutable"):
        catalog_dispatch.merge_catalog_findings(
            repo_paths, DAY, tmp_path, MODEL, inv,
            job_id=job_id, findings_path=findings_path)
    assert Path(first.snapshot_refs[0]).read_bytes() == recorded


def test_undelivered_recommendation_is_merged_only_by_a_later_run(tmp_path):
    # Spec edge case / US2 acceptance 3: a recommendation that never made
    # it into today's snapshot (child cancelled/late) can never rewrite
    # today's already-recorded snapshot (refused outright -- previous
    # test); the still-pending document is instead reselected fresh by a
    # LATER run (a distinct run identity) and merged there, leaving the
    # earlier snapshot untouched.
    repo_paths, _, inv = alpha_setup()
    first = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, inv,
        findings_path=None,
        unavailable_reason=catalog_dispatch.CHILD_QUEUE_TIMEOUT)
    prior_bytes = Path(first.snapshot_refs[0]).read_bytes()
    assert first.state_counts["suggested"] == 0

    # The later run reconstructs the shard/job it would independently
    # dispatch today, exactly as merge_catalog_findings does internally
    # (test_cataloger.py/this file's own first_shard_and_job convention).
    prompt_version, _ = cataloger.load_prompt_contract()
    taxonomy = catalog_dispatch._effective_taxonomy(repo_paths, inv)
    prev_run = catalog.load_snapshot(tmp_path)
    prev_entries = [e for doc in prev_run["repos"].values()
                   for e in doc.get("entries") or []]
    selections = cataloger.select(
        inv, prev_entries, prev_entries,
        current_taxonomy_sha256=taxonomy["digest"],
        current_prompt_version=prompt_version)
    shards = cataloger.build_shards(
        selections, budget=catalog_dispatch.DEFAULT_SHARD_BUDGET)
    assert len(shards) == 1  # the still-pending small fixture corpus
    job = cataloger.envelope(LATER_DAY, MODEL, prompt_version, shards[0],
                            taxonomy["digest"])
    job_id = job["job"]["id"]
    target = next(s for s in shards[0].selections
                 if s.path == "docs/widget-overview.md")
    findings_text = run_fake_worker(
        FAKE_WORKER, REPO=target.repo, DOC_PATH=target.path)
    findings_path = tmp_path / f"{job_id}.json"
    findings_path.write_text(findings_text, encoding="utf-8")

    second = catalog_dispatch.merge_catalog_findings(
        repo_paths, LATER_DAY, tmp_path, MODEL, inv,
        job_id=job_id, findings_path=findings_path)
    assert second.state_counts["suggested"] == 1
    assert second.snapshot_refs != first.snapshot_refs
    assert Path(first.snapshot_refs[0]).read_bytes() == prior_bytes


def test_forced_baseline_mode_after_completion_never_blocks_the_snapshot(
        tmp_path):
    # A forced --catalog-baseline invocation (data-model.md's operator
    # escape hatch) against an ALREADY-complete baseline whose corpus has
    # since drifted would otherwise hit catalog_baseline.run_shard's own
    # "baseline is already complete" refusal -- this feature's single most
    # important invariant (deterministic reporting never depends on the
    # cataloger/baseline machinery) must hold even for this narrow,
    # deliberately-forced edge case: the unconditional snapshot write
    # still lands and no CatalogError ever escapes merge_catalog_findings.
    repo_paths, docs, inv = alpha_setup()
    for _ in range(10):
        meta = catalog_dispatch.prepare_catalog_bundle(
            repo_paths, docs, DAY, tmp_path, tmp_path / "bundle", MODEL, inv,
            allowed_output_root=tmp_path, baseline_mode=True, shard_budget=2)
        if meta["baseline_progress"]["complete"]:
            break
    assert catalog_baseline.is_baseline_complete(tmp_path)

    # Simulate corpus drift since the baseline completed: a differing
    # content_hash means _advance_baseline's run_shard recomputes a
    # DIFFERENT corpus_hash for "alpha," which catalog_baseline.run_shard
    # refuses outright once the baseline marker exists ("post-baseline
    # corpus changes flow through the mechanical catalog pass").
    drifted_inv = [dict(e) for e in inv]
    drifted_inv[0] = dict(drifted_inv[0], content_hash="f" * 64)

    result = catalog_dispatch.merge_catalog_findings(
        repo_paths, DAY, tmp_path, MODEL, drifted_inv,
        findings_path=None, unavailable_reason=None, baseline_mode=True)
    assert result.snapshot_refs  # never blocked despite the forced,
    assert catalog.load_snapshot(tmp_path) is not None  # already-complete,
    assert result.baseline_progress is not None  # drifted-corpus collision
