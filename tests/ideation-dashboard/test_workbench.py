"""US7 workbench reference-set tests (T029).

Covers the manifest engine, the fully-mockable notebook adapter + orphan sweep,
and the bounded actions — the acceptance criteria of the spec "Workbench
reference sets" requirement and its scenarios:

  * manifest CRUD round-trips SCHEMA-VALID against the pinned openxFactory
    validator (create → save-through-boundary → validate → reload);
  * the recipe block is present exactly when `seed.kind == recipe` (the schema
    conditional), and a recipe-seeded set with no recipe is refused;
  * the override discipline: a `manual-include` member and every `excluded`
    entry without a recorded reason are REFUSED (recorded, never silent);
  * the committed-manifest guard: the pinned validator rejects a TRACKED
    manifest, our `committed_manifests()` mirrors it, and NO manifest is tracked
    in this repo (our test manifests all live under tmp_path);
  * the notebook adapter runs entirely on an injected FAKE runner (the real nlm
    is never invoked) and degrades gracefully when unavailable; the orphan sweep
    deletes unbound `xf-wb-*` notebooks and keeps bound ones;
  * draft-organize writes a header-compliant skeleton OUTSIDE `ideation/staging/`
    (and a staging path is refused by the boundary);
  * scoped doc-health invokes the real machinery in-process, scoped to the set;
  * readiness is a recorded NOT-AVAILABLE stub, never a fabricated score;
  * a source removed from the set drops only the reference — the corpus document
    is untouched;
  * out-of-allowlist writes are refused by the boundary.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from conftest import BASE_REPO, REPO_ROOT, find_openxfactory_validator

from ideation_dashboard import workbench as wb
from ideation_dashboard.boundary import BoundaryViolation, OutputBoundary, STAGING_DIR

VALIDATOR = find_openxfactory_validator()

NOW = "2026-07-14T08:00:00Z"


def _boundary(root: Path, *extra: str) -> OutputBoundary:
    return OutputBoundary(root, [wb.WORKBENCH_DIR, *extra])


# ----------------------------------------------------------------------------
# a FAKE nlm runner — tests NEVER touch the real CLI
# ----------------------------------------------------------------------------

class FakeNlm:
    """Records every call and models `notebook create|list|delete`. Injected as
    the adapter's `runner`; a test that sets `available=True` still never reaches
    the real nlm because this stands in for it."""

    def __init__(self, notebooks: list[dict] | None = None) -> None:
        self.calls: list[tuple] = []
        self.notebooks: list[dict] = list(notebooks or [])

    def __call__(self, *args: str, parse: bool = True):
        self.calls.append(args)
        if args[:2] == ("notebook", "create"):
            nb = {"id": f"nb-{len(self.notebooks) + 1}", "title": args[2]}
            self.notebooks.append(nb)
            return nb
        if args[:2] == ("notebook", "list"):
            return list(self.notebooks)
        if args[:2] == ("notebook", "delete"):
            nid = args[2]
            self.notebooks = [n for n in self.notebooks if n.get("id") != nid]
            return ""
        return {}


def _boom(*args, **kwargs):
    raise AssertionError("the real nlm runner must never be called in tests")


# ----------------------------------------------------------------------------
# manifest CRUD + schema conformance
# ----------------------------------------------------------------------------

def _seeded_set() -> wb.Workbench:
    w = wb.Workbench.create("fixture-repo", "Dashboard readiness sweep",
                            seed=wb.SEED_CLUSTER, cluster_id="cl-x", now=NOW)
    w.add_member("ideation/brainstorm/dtn-register.md", wb.VIA_CLUSTER_SEED, now=NOW)
    w.add_member("ideation/brainstorm/legacy-note.md", wb.VIA_MANUAL_INCLUDE,
                 reason="belongs in the readiness sweep even though it predates the cluster", now=NOW)
    w.exclude("ideation/brainstorm/doc-health-checks.md", "out of dashboard scope", now=NOW)
    w.set_recipe({"checked": ["ideation-dashboard", "keyword-lens"],
                  "pinned": ["ideation-dashboard"]}, now=NOW)
    w.bind_notebook(now=NOW)
    return w


def test_manifest_create_save_reload_roundtrip(tmp_path):
    w = _seeded_set()
    written = wb.save(w, _boundary(tmp_path))
    assert written == (tmp_path / wb.manifest_relpath(w.data["name"])).resolve()
    assert wb.WORKBENCH_DIR in written.as_posix()

    reloaded = wb.Workbench.load(written)
    assert reloaded.data["kind"] == "ideation-workbench"
    assert reloaded.data["schema_version"] == 1
    assert reloaded.data["seed"] == {"kind": "cluster-seeded", "cluster_id": "cl-x"}
    assert reloaded.notebook_alias() == "xf-wb-dashboard-readiness-sweep"
    assert reloaded.member_documents() == [
        "ideation/brainstorm/dtn-register.md", "ideation/brainstorm/legacy-note.md"]
    # the manual-include member carried its reason; the excluded entry carried its own
    manual = next(m for m in reloaded.data["members"] if m["via"] == "manual-include")
    assert manual["reason"]
    assert reloaded.data["excluded"][0]["reason"]


@pytest.mark.skipif(VALIDATOR is None, reason="pinned openxFactory validator not reachable")
def test_saved_manifest_validates_clean_against_the_pinned_validator(tmp_path):
    w = _seeded_set()
    # save(validate=True) re-runs the pinned validator and raises on any failure
    written = wb.save(w, _boundary(tmp_path), validate=True, validator=VALIDATOR)
    proc = subprocess.run([sys.executable, str(VALIDATOR), str(written)],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr


@pytest.mark.skipif(VALIDATOR is None, reason="pinned openxFactory validator not reachable")
def test_recipe_seeded_manifest_carries_the_recipe_block_and_validates(tmp_path):
    # seed.kind == recipe ⇒ the recipe block is REQUIRED (schema conditional)
    w = wb.Workbench.create("fixture-repo", "Lens recipe set", seed=wb.SEED_RECIPE,
                            recipe={"checked": ["ideation-dashboard", "keyword-lens"],
                                    "pinned": ["keyword-lens"],
                                    "last_run": {"source_revision": "abcd" * 10}}, now=NOW)
    w.add_member("ideation/brainstorm/dtn-register.md", wb.VIA_RECIPE_MATCH, now=NOW)
    written = wb.save(w, _boundary(tmp_path), validate=True, validator=VALIDATOR)
    reloaded = wb.Workbench.load(written)
    assert reloaded.data["seed"]["kind"] == "recipe"
    assert reloaded.data["recipe"]["checked"] == ["ideation-dashboard", "keyword-lens"]


def test_recipe_seeded_without_a_recipe_is_refused():
    with pytest.raises(wb.WorkbenchError, match="recipe"):
        wb.Workbench.create("r", "no recipe", seed=wb.SEED_RECIPE, now=NOW)


def test_recipe_pinned_must_be_a_subset_of_checked():
    w = wb.Workbench.create("r", "s", now=NOW)
    with pytest.raises(wb.WorkbenchError, match="pinned"):
        w.set_recipe({"checked": ["a"], "pinned": ["b"]}, now=NOW)


def test_cluster_seeded_without_cluster_id_is_refused():
    with pytest.raises(wb.WorkbenchError, match="cluster_id"):
        wb.Workbench.create("r", "s", seed=wb.SEED_CLUSTER, now=NOW)


# ----------------------------------------------------------------------------
# override discipline — recorded, never a silent set edit
# ----------------------------------------------------------------------------

def test_manual_include_without_reason_is_refused():
    w = wb.Workbench.create("r", "s", now=NOW)
    with pytest.raises(wb.WorkbenchError, match="reason"):
        w.add_member("doc.md", wb.VIA_MANUAL_INCLUDE, now=NOW)
    assert w.member_documents() == []  # the refused member never entered the set


def test_excluded_without_reason_is_refused():
    w = wb.Workbench.create("r", "s", now=NOW)
    with pytest.raises(wb.WorkbenchError, match="reason"):
        w.exclude("doc.md", "", now=NOW)
    assert not w.data.get("excluded")


def test_unknown_via_and_action_are_refused():
    w = wb.Workbench.create("r", "s", now=NOW)
    with pytest.raises(wb.WorkbenchError):
        w.add_member("doc.md", "telepathy", now=NOW)
    with pytest.raises(wb.WorkbenchError):
        w.record_action("mind-meld", now=NOW)


def test_excluding_a_member_drops_it_from_members():
    w = wb.Workbench.create("r", "s", now=NOW)
    w.add_member("doc.md", wb.VIA_RECIPE_MATCH, now=NOW)
    w.exclude("doc.md", "actually out of scope", now=NOW)
    assert w.member_documents() == []
    assert w.data["excluded"][0]["document"] == "doc.md"


# ----------------------------------------------------------------------------
# committed-manifest guard (validator + code-side mirror + repo-clean)
# ----------------------------------------------------------------------------

def _init_git_repo(root: Path) -> None:
    for args in (["init", "-q"], ["config", "user.email", "t@t"],
                 ["config", "user.name", "t"]):
        subprocess.run(["git", "-C", str(root), *args], check=True,
                       capture_output=True, text=True)


def _commit(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", rel], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "x"], check=True, capture_output=True)


@pytest.mark.skipif(VALIDATOR is None, reason="pinned openxFactory validator not reachable")
def test_committed_manifest_is_rejected_by_the_pinned_validator(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    _init_git_repo(root)
    manifest = wb.Workbench.create("repo", "leaked set", now=NOW)
    manifest.add_member("docs/x.md", wb.VIA_RECIPE_MATCH, now=NOW)
    _commit(root, "docs/leaked.workbench.yaml", manifest.render())
    proc = subprocess.run([sys.executable, str(VALIDATOR), "--repo", str(root)],
                          capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    assert "committed-workbench-manifest" in out, out
    assert proc.returncode != 0


def test_committed_manifests_detects_a_tracked_manifest(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    _init_git_repo(root)
    _commit(root, "docs/leaked.workbench.yaml", wb.Workbench.create("repo", "leaked", now=NOW).render())
    assert wb.committed_manifests(root) == ["docs/leaked.workbench.yaml"]
    with pytest.raises(wb.WorkbenchError, match="committed"):
        wb.assert_no_committed_manifests(root)


def test_no_workbench_manifest_is_tracked_in_this_repo():
    # the test manifests all live under tmp_path; none leaked into tracked content
    assert wb.committed_manifests(REPO_ROOT) == []


# ----------------------------------------------------------------------------
# notebook adapter (FAKE runner only) + graceful degradation
# ----------------------------------------------------------------------------

def test_notebook_create_uses_the_injected_runner():
    fake = FakeNlm()
    adapter = wb.NotebookAdapter(fake, available=True)
    r = adapter.create("xf-wb-alpha")
    assert r.ok and not r.skipped and r.notebook_id == "nb-1"
    assert ("notebook", "create", "xf-wb-alpha") in fake.calls


def test_notebook_create_speaks_the_plain_form_the_0_5_26_cli_accepts():
    """The T092 re-run drift (2026-08-04), pinned: nlm 0.5.26 REJECTS `--json`
    on `notebook create` (it still accepts it on list/get/source list), and its
    create answers PLAIN TEXT with an `ID: <uuid>` line. A create spoken with
    the flag degraded every at-open session notebook until the FR-040 sync was
    driven by hand. This fake IS that CLI: any create carrying `--json` raises
    exactly like typer does; the plain form answers the 0.5.26 text."""
    class Nlm0526:
        def __init__(self) -> None:
            self.calls: list[tuple] = []
            self.notebooks: list[dict] = []

        def __call__(self, *args: str, parse: bool = True):
            self.calls.append(args)
            if args[:2] == ("notebook", "create"):
                if "--json" in args:
                    raise RuntimeError(
                        "nlm notebook create...: No such option: --json")
                nb = {"id": f"nb-{len(self.notebooks) + 1}", "title": args[2]}
                self.notebooks.append(nb)
                return (f"✓ Created notebook: \n{args[2]}\n  ID: {nb['id']}\n")
            if args[:2] == ("notebook", "list"):
                return list(self.notebooks)
            return {}

    fake = Nlm0526()
    adapter = wb.NotebookAdapter(fake, available=True)
    r = adapter.create("xf-wb-drift")
    assert r.ok and not r.skipped, r.detail
    # the id is read off the plain-text `ID:` line — no fresh list needed here
    assert r.notebook_id == "nb-1"


def test_ensure_notebook_resolves_the_id_by_listing_when_create_echoes_none():
    """The other half of the 0.5.26 shape: a CLI whose create output carries
    no readable id is NOT a failure — `_ensure_notebook` already promises to
    resolve it from a fresh title listing, and this pins that promise against
    a create that answers bare prose."""
    class MuteCreateNlm:
        def __init__(self) -> None:
            self.notebooks: list[dict] = []

        def __call__(self, *args: str, parse: bool = True):
            if args[:2] == ("notebook", "create"):
                self.notebooks.append(
                    {"id": "nb-listed", "title": args[2]})
                return "Created."           # no ID line at all
            if args[:2] == ("notebook", "list"):
                return list(self.notebooks)
            return {}

    adapter = wb.NotebookAdapter(MuteCreateNlm(), available=True)
    notebook_id, created, failure = wb._ensure_notebook(adapter, "xf-wb-mute")
    assert failure is None and created is True
    assert notebook_id == "nb-listed"


def test_notebook_alias_must_be_scratch_prefixed():
    adapter = wb.NotebookAdapter(FakeNlm(), available=True)
    with pytest.raises(wb.WorkbenchError):
        adapter.create("not-a-scratch-alias")


def test_notebook_delete_resolves_alias_to_id_then_deletes():
    fake = FakeNlm([{"id": "nb-7", "title": "xf-wb-gone"}])
    adapter = wb.NotebookAdapter(fake, available=True)
    r = adapter.delete("xf-wb-gone")
    assert r.ok and r.notebook_id == "nb-7"
    assert ("notebook", "delete", "nb-7", "--confirm") in fake.calls
    assert fake.notebooks == []  # actually removed from the fake store


def test_notebook_adapter_degrades_when_nlm_unavailable():
    # available=False ⇒ the runner (here a landmine) is NEVER invoked
    adapter = wb.NotebookAdapter(_boom, available=False)
    r = adapter.create("xf-wb-x")
    assert r.skipped and not r.ok and "unavailable" in r.detail
    assert adapter.list_scratch() == []
    assert adapter.delete("xf-wb-x").skipped


def test_list_scratch_filters_to_the_xf_wb_prefix():
    fake = FakeNlm([{"id": "1", "title": "xf-wb-a"}, {"id": "2", "title": "xf-canon"},
                    {"id": "3", "title": "xf-wb-b"}])
    adapter = wb.NotebookAdapter(fake, available=True)
    titles = sorted(wb._notebook_title(n) for n in adapter.list_scratch())
    assert titles == ["xf-wb-a", "xf-wb-b"]


# ----------------------------------------------------------------------------
# orphan sweep
# ----------------------------------------------------------------------------

def test_orphan_sweep_deletes_unbound_and_keeps_bound(tmp_path):
    # one live manifest binds xf-wb-alpha; xf-wb-orphan has none
    boundary = _boundary(tmp_path)
    live = wb.Workbench.create("r", "Alpha", now=NOW)
    live.bind_notebook("xf-wb-alpha", now=NOW)
    wb.save(live, boundary)
    fake = FakeNlm([{"id": "1", "title": "xf-wb-alpha"},
                    {"id": "2", "title": "xf-wb-orphan"},
                    {"id": "3", "title": "xf-canon"}])
    adapter = wb.NotebookAdapter(fake, available=True)
    result = wb.orphan_sweep(tmp_path, adapter)
    assert result.deleted == ["xf-wb-orphan"]
    assert result.kept == ["xf-wb-alpha"]
    # the orphan is gone from the store; the bound one and the non-scratch remain
    assert sorted(n["title"] for n in fake.notebooks) == ["xf-canon", "xf-wb-alpha"]


def test_orphan_sweep_skipped_when_nlm_unavailable(tmp_path):
    adapter = wb.NotebookAdapter(_boom, available=False)
    result = wb.orphan_sweep(tmp_path, adapter)
    assert result.skipped and not result.deleted


def test_deleting_a_manifest_then_sweeping_removes_its_bound_notebook(tmp_path):
    # spec scenario: a saved set's manifest is removed ⇒ the next sweep deletes
    # its bound xf-wb-* notebook rather than leaving it lingering.
    boundary = _boundary(tmp_path)
    w = wb.Workbench.create("r", "Ephemeral", now=NOW)
    w.bind_notebook("xf-wb-ephemeral", now=NOW)
    manifest_path = wb.save(w, boundary)
    fake = FakeNlm([{"id": "1", "title": "xf-wb-ephemeral"}])
    adapter = wb.NotebookAdapter(fake, available=True)
    # while the manifest is live, the sweep keeps the notebook
    assert wb.orphan_sweep(tmp_path, adapter).kept == ["xf-wb-ephemeral"]
    # remove the manifest, sweep again ⇒ the notebook is deleted
    manifest_path.unlink()
    result = wb.orphan_sweep(tmp_path, adapter)
    assert result.deleted == ["xf-wb-ephemeral"]
    assert fake.notebooks == []


# ----------------------------------------------------------------------------
# draft-organize — skeleton OUTSIDE ideation/staging/, header-compliant
# ----------------------------------------------------------------------------

REQUIRED_HEADERS = ("Status:", "Kind:", "Summary:", "Topics:",
                    "Repository context:", "Captured:")


def test_draft_organize_writes_outside_staging_and_is_header_compliant(tmp_path):
    boundary = _boundary(tmp_path)
    w = wb.Workbench.create("fixture-repo", "Gate console lineage", seed=wb.SEED_ADHOC, now=NOW)
    w.add_member("ideation/brainstorm/dtn-register.md", wb.VIA_MANUAL_INCLUDE,
                 reason="noticed a shared lineage", now=NOW)
    result = wb.draft_organize(w, boundary, now=NOW)

    assert result.completed
    rel = result.reference
    # written OUTSIDE ideation/staging/ (moving into staging is a human gate action)
    assert not rel.startswith(STAGING_DIR)
    assert rel.startswith(wb.ORGANIZE_DIR)
    written = tmp_path / rel
    assert written.is_file()

    text = written.read_text(encoding="utf-8")
    assert text.startswith("# Staged (DRAFT): Gate console lineage")
    for header in REQUIRED_HEADERS:
        assert header in text, f"missing packet header {header!r}"
    # header-compliant per the packet conventions (staging-fragment fields present)
    assert "Staging ID: fixture-repo:staging:gate-console-lineage" in text
    assert "Target capabilities:" in text
    # NOT falsely marked staged (it is pre-staging material)
    assert "Status: draft" in text
    assert "Status: staged" not in text
    # the member is listed in the skeleton body
    assert "ideation/brainstorm/dtn-register.md" in text
    # the action was recorded on the manifest with the skeleton path
    assert w.data["action_history"][-1] == {
        "action": "draft-organize", "at": NOW, "reference": rel}


def test_draft_organize_refuses_a_staging_path(tmp_path):
    # if a caller allowlists ideation/staging/, the draft-skeleton guard still
    # refuses it — the skeleton must land OUTSIDE staging.
    boundary = OutputBoundary(tmp_path, [STAGING_DIR])
    with pytest.raises(BoundaryViolation) as exc:
        boundary.permit_draft_skeleton(f"{STAGING_DIR}some-topic/skeleton.md")
    assert exc.value.refusal.kind == "outside-allowlist"
    assert "outside ideation/staging/" in exc.value.refusal.reason


# ----------------------------------------------------------------------------
# readiness — recorded NOT-AVAILABLE stub, never a fabricated score
# ----------------------------------------------------------------------------

def test_readiness_is_a_recorded_not_available_stub():
    w = wb.Workbench.create("r", "s", now=NOW)
    result = wb.run_readiness(w)
    assert result.status == "not-available"
    assert result.reference == wb.READINESS_NOT_AVAILABLE_REF
    assert not getattr(result, "score", None)  # no fabricated score field
    # the attempt is recorded, not silent
    assert w.data["action_history"][-1]["action"] == "readiness"


# ----------------------------------------------------------------------------
# scoped doc-health — the REAL machinery, in-process, scoped to the set
# ----------------------------------------------------------------------------

def test_scoped_doc_health_runs_real_machinery_over_the_fixture():
    docs = ["ideation/brainstorm/dtn-register.md", "ideation/brainstorm/legacy-note.md"]
    w = wb.Workbench.create("fixture-repo", "DH scope", now=NOW)
    result = wb.run_scoped_doc_health(BASE_REPO, docs, repository="fixture-repo",
                                      as_of=date(2026, 7, 14), wb=w)
    assert result.completed
    # every finding (if any) is confined to the scoped documents
    assert all(f.path in set(docs) for f in result.findings)
    # a doc-health action was recorded with a scoped reference
    assert w.data["action_history"][-1]["action"] == "doc-health"
    assert w.data["action_history"][-1]["reference"].startswith("health/scoped/")


def test_scoped_doc_health_finds_a_real_missing_status(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "bad.md").write_text("# No status header\n\nbody\n", encoding="utf-8")
    result = wb.run_scoped_doc_health(tmp_path, ["docs/bad.md"], repository="tmp",
                                      as_of=date(2026, 7, 14))
    families = {(f.family, f.rule) for f in result.findings}
    assert ("status-validity", "missing status header") in families


def test_scoped_doc_health_ignores_out_of_scope_docs(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "bad.md").write_text("# No status\n\nbody\n", encoding="utf-8")
    (tmp_path / "docs" / "good.md").write_text(
        "# Good\n\nStatus: brainstorm\nKind: brainstorm\n", encoding="utf-8")
    # scope to good.md only ⇒ bad.md's finding is not surfaced
    result = wb.run_scoped_doc_health(tmp_path, ["docs/good.md"], repository="tmp",
                                      as_of=date(2026, 7, 14))
    assert all(f.path == "docs/good.md" for f in result.findings)


# ----------------------------------------------------------------------------
# boundary refusals + corpus safety
# ----------------------------------------------------------------------------

def test_save_outside_the_allowlist_is_refused(tmp_path):
    # a boundary allowlisting only ideation/workbench/ refuses a write elsewhere
    boundary = _boundary(tmp_path)
    w = wb.Workbench.create("r", "s", now=NOW)
    with pytest.raises(BoundaryViolation) as exc:
        wb.save(w, boundary, relpath="docs/leaked.workbench.yaml")
    assert exc.value.refusal.kind == "outside-allowlist"
    assert boundary.refusals  # recorded, not silent


def test_removing_a_member_leaves_the_corpus_document_untouched(tmp_path):
    # spec scenario: a source removed from an xf-wb-* notebook drops only the
    # reference; the corpus document is untouched.
    corpus_doc = tmp_path / "ideation" / "brainstorm" / "keep.md"
    corpus_doc.parent.mkdir(parents=True)
    corpus_doc.write_text("# Keep\n\nStatus: brainstorm\n", encoding="utf-8")
    before = corpus_doc.read_bytes()

    w = wb.Workbench.create("r", "s", now=NOW)
    w.add_member("ideation/brainstorm/keep.md", wb.VIA_RECIPE_MATCH, now=NOW)
    assert w.remove_member("ideation/brainstorm/keep.md", now=NOW) is True
    assert w.member_documents() == []
    # the corpus document on disk is byte-identical — the manifest touched nothing
    assert corpus_doc.is_file()
    assert corpus_doc.read_bytes() == before
