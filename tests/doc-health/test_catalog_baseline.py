"""Baseline build (US2): bounded repository shards, interruption plus
stateless resume, deterministic merge to exactly one entry per governed
document, progress-mode coverage without per-document findings, and the
complete-coverage enforcement gate that stays off until the merge
writes the ``baseline_complete`` marker.

All tests are hermetic: the fixture workspace is read-only (mutation
scenarios copy it into pytest tmp dirs), git facts come from
conftest.FakeGit, and every write lands under a tmp baseline root."""

from __future__ import annotations

import hashlib
import json
import os
import shutil

import pytest

from conftest import AS_OF, FIXTURES, FakeGit  # noqa: F401 (sys.path side effect)

from doc_health import catalog, catalog_baseline, inventory
from doc_health.corpus import load_docs

WORKSPACE = FIXTURES / "catalog" / "workspace"
HEADS = {"alpha": "a" * 40, "openxFactory": "b" * 40}
LATER_HEADS = {"alpha": "c" * 40, "openxFactory": "d" * 40}
DAY = AS_OF  # date(2026, 7, 9) — dates are parameters, never wall clock
DAY_STR = AS_OF.isoformat()
REPOS = ("alpha", "openxFactory")  # 5 + 10 governed fixture documents


def repo_paths_for(base):
    return {p.name: p for p in sorted(base.iterdir()) if p.is_dir()}


def docs_for(repo_paths):
    docs = []
    for name in sorted(repo_paths):
        docs.extend(load_docs(name, repo_paths[name]))
    return docs


def extended_inventory(base=WORKSPACE, heads=HEADS):
    repo_paths = repo_paths_for(base)
    return inventory.build_inventory(
        docs_for(repo_paths), repo_paths, git=FakeGit(heads=heads))


def entries_for(repo, base=WORKSPACE, heads=HEADS):
    return [e for e in catalog.mechanical_entries(
        extended_inventory(base, heads)) if e["repo"] == repo]


def prohibit_protected(entry):
    """Stand-in handling-gate policy (test_catalog precedent): path
    persistence is prohibited for source-declared protected handling."""
    return entry.get("handling") == "protected"


def opaque_entries_for(repo, base=WORKSPACE, heads=HEADS):
    """Mechanical entries with the handling gate applied: protected
    documents carry the opaque locator and omit the path."""
    return [e for e in catalog.mechanical_entries(
        extended_inventory(base, heads),
        path_prohibited=prohibit_protected) if e["repo"] == repo]


def baseline_root(root):
    return root / "health" / "document-catalog" / "baseline"


def shard_files(root, repo):
    shards = baseline_root(root) / "shards" / repo
    return sorted(shards.iterdir()) if shards.is_dir() else []


def read_yaml_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def complete_repo(root, repo, budget, base=WORKSPACE, heads=HEADS):
    """Drive one repository to completion in bounded invocations. Every
    invocation rebuilds its inputs from scratch — resume state lives
    only in the persisted shard artifacts (interruption semantics)."""
    while True:
        state = catalog_baseline.run_shard(
            root, repo, budget, DAY, entries_for(repo, base, heads))
        if state.complete:
            return state


def tree_state(base):
    return {
        p.relative_to(base).as_posix():
            hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(base.rglob("*")) if p.is_file()}


# --- bounded shards (T010) ----------------------------------------------------

def test_run_shard_is_bounded_by_the_entry_budget(tmp_path):
    root = tmp_path / "agg"
    entries = entries_for("alpha")
    assert len(entries) == 5
    state = catalog_baseline.run_shard(root, "alpha", 2, DAY, entries)
    # US2 acceptance 1: each shard is bounded by the entry budget.
    assert state.processed == 2
    assert state.cataloged == 2 and state.total == 5
    assert not state.complete
    assert state.repo == "alpha" and state.sequence == 1
    assert state.start_after is None
    assert state.cursor == entries[1]["path"]
    # The shard-state artifact is on disk, immutable-shaped, and carries
    # the data-model fields: repo, budget, cursor, complete flag, shard
    # content hash.
    assert state.path == baseline_root(root) / "shards" / "alpha" / "0001.yaml"
    doc = read_yaml_json(state.path)
    assert doc["kind"] == "xfactory_document_catalog_baseline_shard"
    assert doc["status"] == "record"
    assert (doc["repo"], doc["budget"], doc["cursor"], doc["complete"]) == \
        ("alpha", 2, state.cursor, False)
    assert (doc["as_of"], doc["sequence"], doc["total"]) == (DAY_STR, 1, 5)
    assert doc["start_after"] is None
    assert doc["entries"] == entries[:2]
    assert doc["corpus_hash"] == state.corpus_hash
    assert doc["shard_content_hash"] == hashlib.sha256(json.dumps(
        entries[:2], sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    # Byte-stable rendering (research D3): sorted keys, fixed indent,
    # trailing newline.
    text = state.path.read_text(encoding="utf-8")
    assert text == json.dumps(doc, indent=2, sort_keys=True) + "\n"
    # A budget covering the whole repository completes in one shard.
    other = catalog_baseline.run_shard(
        tmp_path / "agg2", "alpha", 5, DAY, entries)
    assert other.complete and other.processed == 5


def test_shard_budget_and_entries_are_validated(tmp_path):
    root = tmp_path / "agg"
    entries = entries_for("alpha")
    for bad in (0, -1, 2.0, "2", True):
        with pytest.raises(ValueError, match="budget"):
            catalog_baseline.run_shard(root, "alpha", bad, DAY, entries)
    # Entries must belong to the shard's repository.
    with pytest.raises(ValueError, match="belong"):
        catalog_baseline.run_shard(root, "openxFactory", 2, DAY, entries)
    # Migration-loaded entries (null freshness) cannot seed the baseline.
    stale = [dict(entries[0], revision=None)]
    with pytest.raises(ValueError, match="revision"):
        catalog_baseline.run_shard(root, "alpha", 2, DAY, stale)
    with pytest.raises(ValueError):
        catalog_baseline.run_shard(root, "../alpha", 2, DAY, entries)
    assert not root.exists()  # nothing landed


def test_interrupted_baseline_resumes_from_the_persisted_cursor(tmp_path):
    # US2 acceptance 1: the build is resumable after interruption —
    # every invocation below rebuilds its inputs from scratch, so the
    # only resume state is the recorded shard artifacts.
    root = tmp_path / "agg"
    entries = entries_for("alpha")
    first = catalog_baseline.run_shard(
        root, "alpha", 2, DAY, entries_for("alpha"))
    recorded = first.path.read_bytes()
    # ... the process dies here — even mid-write: an interrupted shard
    # write leaves at worst an orphaned temp file, never a truncated
    # artifact, so it is invisible to the resuming invocation ...
    (first.path.parent / "0002.yaml.tmp").write_text("{trunc",
                                                     encoding="utf-8")
    second = catalog_baseline.run_shard(
        root, "alpha", 2, DAY, entries_for("alpha"))
    assert second.start_after == first.cursor
    assert (second.sequence, second.processed, second.cataloged) == (2, 2, 4)
    assert not second.complete
    third = catalog_baseline.run_shard(
        root, "alpha", 2, DAY, entries_for("alpha"))
    assert third.complete
    assert (third.sequence, third.processed, third.cataloged) == (3, 1, 5)
    assert third.cursor == entries[-1]["path"]
    # Immutable shard-state artifacts: earlier shards never rewritten.
    # The crashed writer's orphaned temp file persists untouched — no
    # invocation ever shares (or cleans) another writer's temp name —
    # and stays invisible to shard loading and resume.
    assert first.path.read_bytes() == recorded
    assert [p.name for p in shard_files(root, "alpha")] == \
        ["0001.yaml", "0002.yaml", "0002.yaml.tmp", "0003.yaml"]
    assert (first.path.parent / "0002.yaml.tmp").read_text(
        encoding="utf-8") == "{trunc"
    # The chain covers the repository exactly, in order, no duplicates.
    walked = [e for p in shard_files(root, "alpha") if p.suffix == ".yaml"
              for e in read_yaml_json(p)["entries"]]
    assert walked == entries
    # A racing writer that loses the exclusive link can never rewrite a
    # recorded shard artifact — it fails closed.
    with pytest.raises(catalog.CatalogError, match="already exists"):
        catalog_baseline._write_exclusive(first.path, "tampered")
    assert first.path.read_bytes() == recorded


def test_racing_same_sequence_writers_record_only_the_winners_bytes(
        tmp_path, monkeypatch):
    # Two invocations that computed the same shard sequence race. Each
    # writes its OWN unique temp file, so the loser can neither
    # truncate nor substitute the winner's bytes; the first hard-link
    # wins, the loser fails closed with CatalogError (never a stray
    # FileNotFoundError from a winner unlinking a shared temp), and the
    # recorded immutable artifact is byte-identical to an unraced run
    # of the winning invocation.
    root = tmp_path / "agg"
    entries = entries_for("alpha")
    real_link = os.link
    fired = []

    def interleaved_link(src, dst, *args, **kwargs):
        if not fired:
            fired.append(True)
            # Writer B lands BETWEEN writer A's temp write and A's
            # link: it loads the same empty chain, computes the same
            # sequence number, and publishes first.
            winner = catalog_baseline.run_shard(
                root, "alpha", 5, DAY, entries)
            assert winner.complete and winner.sequence == 1
        return real_link(src, dst, *args, **kwargs)

    monkeypatch.setattr(os, "link", interleaved_link)
    with pytest.raises(catalog.CatalogError, match="already exists"):
        catalog_baseline.run_shard(root, "alpha", 2, DAY, entries)
    monkeypatch.undo()

    # The recorded artifact holds exactly the winner's bytes — never a
    # blend, a truncation, or the loser's content under the winner's
    # claim — and parses as a valid record.
    recorded = baseline_root(root) / "shards" / "alpha" / "0001.yaml"
    reference = tmp_path / "ref"
    catalog_baseline.run_shard(reference, "alpha", 5, DAY, entries)
    assert recorded.read_bytes() == \
        (baseline_root(reference) / "shards" / "alpha" /
         "0001.yaml").read_bytes()
    doc = read_yaml_json(recorded)
    assert doc["budget"] == 5 and doc["complete"]
    assert doc["entries"] == entries
    # Neither writer leaves temp litter, and the loser's later retry is
    # a clean resume over the winner's recorded chain.
    assert [p.name for p in shard_files(root, "alpha")] == ["0001.yaml"]
    retry = catalog_baseline.run_shard(root, "alpha", 2, DAY, entries)
    assert retry.complete and retry.processed == 0


def test_completed_repository_reruns_are_noops(tmp_path):
    root = tmp_path / "agg"
    complete_repo(root, "alpha", 2)
    before = {p.name: p.read_bytes() for p in shard_files(root, "alpha")}
    again = catalog_baseline.run_shard(
        root, "alpha", 2, DAY, entries_for("alpha"))
    # Resume = re-run, skip completed shards (research D5): no new
    # artifact, nothing rewritten, coverage already total.
    assert again.complete and again.processed == 0
    assert again.cataloged == again.total == 5
    assert {p.name: p.read_bytes()
            for p in shard_files(root, "alpha")} == before


def test_corpus_change_mid_baseline_restarts_the_repository_walk(tmp_path):
    # Spec edge case: the merged baseline stays deterministic — a walk
    # over changed content restarts as a new chain instead of mixing
    # two corpus states.
    root = tmp_path / "agg"
    partial = catalog_baseline.run_shard(
        root, "openxFactory", 4, DAY, entries_for("openxFactory"))
    assert not partial.complete
    ws = tmp_path / "workspace"
    shutil.copytree(WORKSPACE, ws)
    (ws / "openxFactory" / "docs" / "arrived-mid-baseline.md").write_text(
        "Status: draft\n\nLanded while the baseline was paused.\n",
        encoding="utf-8")
    restart = catalog_baseline.run_shard(
        root, "openxFactory", 4, DAY,
        entries_for("openxFactory", ws, LATER_HEADS))
    assert restart.start_after is None  # fresh walk, not a continuation
    assert restart.sequence == 2
    assert restart.corpus_hash != partial.corpus_hash
    assert (restart.cataloged, restart.total) == (4, 11)
    final = complete_repo(root, "openxFactory", 4, ws, LATER_HEADS)
    assert final.complete and final.cataloged == final.total == 11
    # Unrelated revision churn is NOT a corpus change: the walk resumes.
    unchanged = catalog_baseline.run_shard(
        tmp_path / "agg2", "alpha", 2, DAY, entries_for("alpha"))
    resumed = catalog_baseline.run_shard(
        tmp_path / "agg2", "alpha", 2, DAY,
        entries_for("alpha", WORKSPACE, LATER_HEADS))
    assert resumed.start_after == unchanged.cursor


# --- deterministic merge (T011) -------------------------------------------------

def test_merge_waits_for_every_repository_and_writes_no_marker(tmp_path):
    root = tmp_path / "agg"
    # No shards at all: nothing to merge.
    assert catalog_baseline.merge_baseline(root, DAY, REPOS) is None
    complete_repo(root, "alpha", 2)
    # A governed repository still unavailable (never sharded, invisible
    # on disk) gates the merge: the required repos input names it.
    assert catalog_baseline.merge_baseline(root, DAY, repos=REPOS) is None
    # A partially sharded repository gates the merge even when only
    # discovered on disk (absent from the named set).
    catalog_baseline.run_shard(
        root, "openxFactory", 4, DAY, entries_for("openxFactory"))
    assert catalog_baseline.merge_baseline(root, DAY, ("alpha",)) is None
    # US2 acceptance 3 (gate): nothing landed — no marker, no merge
    # output, enforcement stays off.
    assert not (baseline_root(root) / "baseline_complete.yaml").exists()
    assert not (baseline_root(root) / "merged.yaml").exists()
    assert not catalog_baseline.is_baseline_complete(root)
    assert catalog_baseline.load_baseline(root) is None
    # Completing the outstanding repository unlocks the merge.
    complete_repo(root, "openxFactory", 4)
    marker = catalog_baseline.merge_baseline(root, DAY, repos=REPOS)
    assert marker == baseline_root(root) / "baseline_complete.yaml"
    assert catalog_baseline.is_baseline_complete(root)


def test_merge_requires_the_full_governed_repository_set(tmp_path):
    # FR-005 / SC-001: the merge cannot derive the governed corpus from
    # disk — a repository unavailable before its FIRST shard leaves no
    # trace under shards/, so an empty merge would freeze the baseline
    # over a partial corpus and permanently refuse the late
    # repository's shards. The governed set is therefore a required,
    # validated input (``repos`` has no default, so omitting it
    # entirely is a Python-level TypeError — that's calling-convention
    # enforcement, not application logic, so it isn't asserted here).
    root = tmp_path / "agg"
    complete_repo(root, "alpha", 2)
    for bad in (None, [], (), "alpha"):
        with pytest.raises(ValueError, match="governed repository set"):
            catalog_baseline.merge_baseline(root, DAY, bad)
    with pytest.raises(ValueError, match="invalid repository id"):
        catalog_baseline.merge_baseline(root, DAY, ("alpha", "../evil"))
    # Nothing landed: no marker, no merged fold, enforcement off.
    assert not (baseline_root(root) / "baseline_complete.yaml").exists()
    assert not (baseline_root(root) / "merged.yaml").exists()
    assert not catalog_baseline.is_baseline_complete(root)
    # The never-sharded governed repository gates the merge (returns
    # None) — and its shard can still arrive later (spec edge case "A
    # repository is unavailable mid-baseline: its shard resumes
    # later"), because the baseline was never prematurely frozen.
    assert catalog_baseline.merge_baseline(root, DAY, REPOS) is None
    late = catalog_baseline.run_shard(
        root, "openxFactory", 10, DAY, entries_for("openxFactory"))
    assert late.complete
    marker = catalog_baseline.merge_baseline(root, DAY, REPOS)
    assert marker == baseline_root(root) / "baseline_complete.yaml"
    assert catalog_baseline.is_baseline_complete(root)
    merged = catalog_baseline.load_baseline(root)
    assert len(merged["entries"]) == 15  # SC-001: full governed corpus


def test_merged_baseline_has_exactly_one_entry_per_governed_document(tmp_path):
    root = tmp_path / "agg"
    complete_repo(root, "alpha", 2)
    complete_repo(root, "openxFactory", 3)
    marker = catalog_baseline.merge_baseline(root, DAY, REPOS)
    merged = catalog_baseline.load_baseline(root)
    # US2 acceptance 3 / SC-001: exactly one mechanically correct entry
    # per governed document, folded in (repo, locator) order.
    expected = catalog.mechanical_entries(extended_inventory())
    assert merged["entries"] == expected
    keys = [(e["repo"], e["path"]) for e in merged["entries"]]
    assert len(keys) == len(set(keys)) == 15
    assert keys == sorted(keys)
    assert merged["kind"] == "xfactory_document_catalog_baseline"
    assert {r: c["entries"] for r, c in merged["repos"].items()} == \
        {"alpha": 5, "openxFactory": 10}
    marker_doc = read_yaml_json(marker)
    assert marker_doc["kind"] == \
        "xfactory_document_catalog_baseline_complete"
    assert marker_doc["status"] == "record"
    assert marker_doc["as_of"] == DAY_STR
    assert marker_doc["repos"] == {"alpha": 5, "openxFactory": 10}
    assert marker_doc["total_entries"] == 15
    rendered = (baseline_root(root) / "merged.yaml").read_bytes()
    assert marker_doc["merged_sha256"] == \
        hashlib.sha256(rendered).hexdigest()


def test_merge_is_deterministic_across_shard_schedules(tmp_path):
    # The fold is a pure function of the corpus, not of shard budgets,
    # invocation order, or interruptions: two independent baselines
    # built on different schedules render byte-identical output, and a
    # re-merge is an idempotent no-op.
    one, two = tmp_path / "one", tmp_path / "two"
    complete_repo(one, "alpha", 2)
    complete_repo(one, "openxFactory", 4)
    complete_repo(two, "openxFactory", 1)  # other order, other budgets
    complete_repo(two, "alpha", 5)
    assert catalog_baseline.merge_baseline(one, DAY, repos=REPOS)
    assert catalog_baseline.merge_baseline(two, DAY, repos=REPOS)
    merged = (baseline_root(one) / "merged.yaml").read_bytes()
    assert merged == (baseline_root(two) / "merged.yaml").read_bytes()
    assert merged.endswith(b"\n") and b"\r" not in merged
    assert (baseline_root(one) / "baseline_complete.yaml").read_bytes() == \
        (baseline_root(two) / "baseline_complete.yaml").read_bytes()
    # Deterministic re-merge: same marker, same bytes, no error — even
    # on a later date (the record keeps the completing merge's date).
    marker = baseline_root(one) / "baseline_complete.yaml"
    recorded = marker.read_bytes()
    assert catalog_baseline.merge_baseline(one, DAY, REPOS) == marker
    assert catalog_baseline.merge_baseline(one, "2026-07-10", REPOS) == marker
    assert marker.read_bytes() == recorded
    assert (baseline_root(one) / "merged.yaml").read_bytes() == merged


def test_recorded_baseline_is_frozen_after_the_marker(tmp_path):
    root = tmp_path / "agg"
    complete_repo(root, "alpha", 2)
    complete_repo(root, "openxFactory", 4)
    assert catalog_baseline.merge_baseline(root, DAY, repos=REPOS)
    # Post-baseline corpus changes flow through the mechanical pass:
    # new shard work is refused, and the recorded fold cannot be
    # rewritten by a differing merge.
    ws = tmp_path / "workspace"
    shutil.copytree(WORKSPACE, ws)
    (ws / "alpha" / "docs" / "post-baseline.md").write_text(
        "Status: draft\n\nArrived after the baseline completed.\n",
        encoding="utf-8")
    changed = entries_for("alpha", ws, LATER_HEADS)
    with pytest.raises(catalog.CatalogError, match="complete"):
        catalog_baseline.run_shard(root, "alpha", 2, DAY, changed)
    # Unchanged-corpus reruns stay harmless no-ops.
    noop = catalog_baseline.run_shard(
        root, "alpha", 2, DAY, entries_for("alpha"))
    assert noop.complete and noop.processed == 0


def test_crashed_merge_heals_and_marker_is_written_last(tmp_path):
    # A merged.yaml without the marker is a crashed merge, not a
    # record: it is invisible to load_baseline, leaves the gate off,
    # and heals idempotently on retry.
    root = tmp_path / "agg"
    complete_repo(root, "alpha", 2)
    complete_repo(root, "openxFactory", 4)
    merged_path = baseline_root(root) / "merged.yaml"
    merged_path.parent.mkdir(parents=True, exist_ok=True)
    merged_path.write_text("{}\n", encoding="utf-8")  # crashed remnant
    assert not catalog_baseline.is_baseline_complete(root)
    assert catalog_baseline.load_baseline(root) is None
    marker = catalog_baseline.merge_baseline(root, DAY, REPOS)
    assert marker.is_file()
    assert catalog_baseline.load_baseline(root)["entries"] == \
        catalog.mechanical_entries(extended_inventory())


def test_opaque_locator_entries_flow_through_the_baseline_without_leakage(
        tmp_path):
    # SC-007 / FR-012 over the baseline artifact class (shards, merged
    # fold, marker): a path-prohibited document is baselined under its
    # opaque locator, the resume cursor round-trips as the opaque
    # document_ref, and the protected path never appears in any
    # baseline artifact.
    root = tmp_path / "agg"
    entries = opaque_entries_for("alpha")
    opaque = [e for e in entries if "path" not in e]
    assert len(opaque) == 1
    ref = opaque[0]["document_ref"]
    assert opaque[0]["path_sha256"] == catalog.opaque_locator(
        "alpha", "docs/protected-roster.md")["path_sha256"]
    # Mixed path/opaque ordering within one repo: the opaque entry
    # sorts by document_ref among the persisted paths, and the shard
    # boundary is placed exactly ON it so the persisted cursor IS the
    # opaque reference.
    idx = entries.index(opaque[0])
    assert idx < len(entries) - 1  # a resume happens after the cursor
    first = catalog_baseline.run_shard(root, "alpha", idx + 1, DAY, entries)
    assert not first.complete
    assert first.cursor == ref
    assert read_yaml_json(first.path)["cursor"] == ref
    second = catalog_baseline.run_shard(
        root, "alpha", len(entries), DAY, entries)
    assert second.start_after == ref  # cursor round-trips opaquely
    assert second.complete and second.cataloged == len(entries)
    walked = [e for p in shard_files(root, "alpha")
              for e in read_yaml_json(p)["entries"]]
    assert walked == entries  # exact cover, mixed ordering preserved
    # The merged baseline carries the opaque entry — exactly one entry
    # per governed document, path omitted for the protected one.
    complete_repo(root, "openxFactory", 4)
    assert catalog_baseline.merge_baseline(root, DAY, REPOS)
    merged = catalog_baseline.load_baseline(root)
    assert merged["entries"] == catalog.mechanical_entries(
        extended_inventory(), path_prohibited=prohibit_protected)
    assert [e for e in merged["entries"] if "path" not in e] == [opaque[0]]
    # Leakage sweep over every baseline artifact: the protected path
    # never appears; the opaque reference does.
    artifacts = [p for p in sorted(root.rglob("*")) if p.is_file()]
    assert artifacts
    for artifact in artifacts:
        assert "protected-roster" not in \
            artifact.read_text(encoding="utf-8"), artifact
    merged_text = (baseline_root(root) / "merged.yaml").read_text(
        encoding="utf-8")
    assert ref in merged_text


# --- progress mode (T011) -------------------------------------------------------

def test_progress_reports_coverage_without_per_document_findings(tmp_path):
    root = tmp_path / "agg"
    empty = catalog_baseline.progress(root)
    assert (empty.repos, empty.cataloged, empty.total) == ((), 0, 0)
    assert (empty.repos_total, empty.complete, empty.percent) == (0, False, 0.0)
    # Partial baseline: alpha complete, openxFactory 4 of 10.
    complete_repo(root, "alpha", 2)
    catalog_baseline.run_shard(
        root, "openxFactory", 4, DAY, entries_for("openxFactory"))
    prog = catalog_baseline.progress(root)
    assert [(r.repo, r.cataloged, r.total, r.complete)
            for r in prog.repos] == \
        [("alpha", 5, 5, True), ("openxFactory", 4, 10, False)]
    assert (prog.cataloged, prog.total) == (9, 15)
    assert (prog.repos_complete, prog.repos_total) == (1, 2)
    assert prog.percent == pytest.approx(60.0)
    assert not prog.complete
    # US2 acceptance 2: progress is stated as aggregate counts only —
    # no per-document identity, so an incomplete baseline can never
    # surface one missing-entry finding per legacy document.
    surface = repr(prog)
    for entry in catalog.mechanical_entries(extended_inventory()):
        assert entry["path"] not in surface
        assert entry["content_hash"] not in surface
    assert set(vars(prog.repos[0])) == \
        {"repo", "cataloged", "total", "complete"}
    # Completion drives coverage to 100% and flips the gate.
    complete_repo(root, "openxFactory", 4)
    assert catalog_baseline.merge_baseline(root, DAY, repos=REPOS)
    done = catalog_baseline.progress(root)
    assert done.complete and done.percent == pytest.approx(100.0)
    assert (done.cataloged, done.total) == (15, 15)


def test_enforcement_gate_stays_off_until_the_merge_writes_the_marker(tmp_path):
    root = tmp_path / "agg"
    assert not catalog_baseline.is_baseline_complete(root)
    complete_repo(root, "alpha", 3)
    complete_repo(root, "openxFactory", 3)
    # Every shard chain is complete, but only the deterministic merge
    # writes the marker — enforcement stays off until then (FR-005).
    assert not catalog_baseline.is_baseline_complete(root)
    assert not catalog_baseline.progress(root).complete
    marker = catalog_baseline.merge_baseline(root, DAY, repos=REPOS)
    assert marker.name == "baseline_complete.yaml"
    assert catalog_baseline.is_baseline_complete(root)
    assert catalog_baseline.progress(root).complete


# --- non-mutation boundary (SC-003) ---------------------------------------------

def test_baseline_writes_only_under_the_baseline_paths(tmp_path):
    ws = tmp_path / "workspace"
    shutil.copytree(WORKSPACE, ws)
    root = tmp_path / "agg"
    before = tree_state(ws)
    complete_repo(root, "alpha", 2, ws, HEADS)
    complete_repo(root, "openxFactory", 4, ws, HEADS)
    catalog_baseline.merge_baseline(root, DAY, repos=REPOS)
    catalog_baseline.progress(root)
    catalog_baseline.load_baseline(root)
    assert tree_state(ws) == before  # no source document touched
    created = tree_state(root)
    assert created  # shard artifacts, merged fold, and marker landed...
    assert all(p.startswith("health/document-catalog/baseline/")
               for p in created)  # ...and only there
    # Generated baseline records are excluded from corpus discovery so
    # the catalog never catalogs itself.
    assert all(inventory.is_generated_catalog_path(p) for p in created)


# --- exclusive merge recording (recheck fix) -----------------------------------

def test_racing_differing_fold_merge_cannot_clobber_the_recorded_baseline(
        tmp_path, monkeypatch):
    """A merge that computed its fold before a racer recorded a different
    one must fail closed at the exclusive marker claim — the recorded
    baseline's bytes stay exactly the racer's (no clobber, no blend)."""
    ws = tmp_path / "ws"
    shutil.copytree(WORKSPACE, ws)
    root = tmp_path / "run"
    for repo in REPOS:
        complete_repo(root, repo, 99, base=ws)

    original = catalog_baseline._write_exclusive
    fired = {"done": False}

    def interleaved(path, text):
        if not fired["done"]:
            fired["done"] = True
            # racer B: edit an alpha doc (content change restarts the
            # chain), rebuild it, and record a differing fold + marker.
            # The path joined below is a fixed fixture constant, never
            # entry data — confirm it names a real governed alpha doc
            # before joining it.
            governed_alpha_doc = "docs/protected-roster.md"
            assert any(
                e.get("path") == governed_alpha_doc
                for e in entries_for("alpha", base=ws))
            target = ws / "alpha" / governed_alpha_doc
            target.write_text(
                target.read_text(encoding="utf-8") + "\nEdited mid-race.\n",
                encoding="utf-8")
            complete_repo(root, "alpha", 99, base=ws)
            catalog_baseline.merge_baseline(root, DAY, REPOS)
        return original(path, text)

    monkeypatch.setattr(catalog_baseline, "_write_exclusive", interleaved)
    racer_marker = baseline_root(root) / "baseline_complete.yaml"
    with pytest.raises(catalog_baseline.CatalogError,
                       match="differing fold is refused"):
        catalog_baseline.merge_baseline(root, DAY, REPOS)

    recorded = read_yaml_json(racer_marker)
    merged_bytes = (baseline_root(root) / "merged.yaml").read_bytes()
    assert hashlib.sha256(merged_bytes).hexdigest() == \
        recorded["merged_sha256"]
    assert catalog_baseline.load_baseline(root) is not None  # verifies hash


def test_crashed_publish_heals_on_identical_remerge(tmp_path):
    """The marker is recorded before merged.yaml publishes; a winner that
    crashes between the two is healed by any later merge of the identical
    fold, restoring byte-identical canonical content."""
    root = tmp_path / "run"
    for repo in REPOS:
        complete_repo(root, repo, 99)
    marker = catalog_baseline.merge_baseline(root, DAY, REPOS)
    merged_path = baseline_root(root) / "merged.yaml"
    before = merged_path.read_bytes()
    merged_path.unlink()  # simulate the crash between marker and publish
    with pytest.raises(catalog_baseline.CatalogError, match="heal"):
        catalog_baseline.load_baseline(root)  # fails closed, never raw OSError
    again = catalog_baseline.merge_baseline(root, DAY, REPOS)
    assert again == marker
    assert merged_path.read_bytes() == before
    assert catalog_baseline.load_baseline(root) is not None
