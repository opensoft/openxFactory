"""Thirteenth deterministic family (US3): catalog coverage, structural
integrity, and classification-facet shape, over the per-defect fixture
matrix from quickstart section 4, a clean fixture (zero findings), the
baseline-progress mode, and a runner ``--family document-catalog``
integration test.

All tests are hermetic: the fixture workspace (shared with test_catalog
and test_catalog_baseline) is read-only, git facts come from
conftest.FakeGit, and every write lands under a tmp catalog root."""

from __future__ import annotations

import hashlib
import json
import shutil

from conftest import AS_OF, FIXTURES, FakeGit  # noqa: F401 (sys.path side effect)

from doc_health import DEFAULT_THRESHOLDS, ERROR, INFO, WARNING, Skip
from doc_health import catalog, catalog_baseline, corpus, inventory, runner
from doc_health.families import FAMILIES
from doc_health.runner import Context

fam_document_catalog = FAMILIES["document-catalog"]

WORKSPACE = FIXTURES / "catalog" / "workspace"
HEADS = {"alpha": "a" * 40, "openxFactory": "b" * 40}
DAY = AS_OF  # date(2026, 7, 9) — dates are parameters, never wall clock
DAY_STR = AS_OF.isoformat()
REPOS = ("alpha", "openxFactory")

REGISTRY_PATHS = {
    "alpha": "catalog/document-tag-registry.yaml",
    "openxFactory": "contracts/document-tag-registry.yaml",
}
REGISTRY_REVISIONS = {"alpha": "1" * 40, "openxFactory": "2" * 40}


# --- fixture construction helpers (test_catalog.py / test_catalog_baseline.py
# precedent, redefined locally per this suite's convention) ------------------

def repo_paths_for(base):
    return {p.name: p for p in sorted(base.iterdir()) if p.is_dir()}


def docs_for(repo_paths):
    docs = []
    for name in sorted(repo_paths):
        docs.extend(corpus.load_docs(name, repo_paths[name]))
    return docs


def extended_inventory(base=WORKSPACE, heads=HEADS):
    repo_paths = repo_paths_for(base)
    return inventory.build_inventory(
        docs_for(repo_paths), repo_paths, git=FakeGit(heads=heads))


def entries_for(repo, base=WORKSPACE, heads=HEADS):
    return [e for e in catalog.mechanical_entries(extended_inventory(
        base, heads)) if e["repo"] == repo]


def registry_inputs(base=WORKSPACE, heads=HEADS):
    return [
        catalog.registry_input(
            repo, REGISTRY_PATHS[repo], base / repo / REGISTRY_PATHS[repo],
            repository_revision=heads[repo],
            registry_revision=REGISTRY_REVISIONS[repo])
        for repo in sorted(REGISTRY_PATHS)]


TAXONOMY = catalog.effective_taxonomy(registry_inputs())


def ctx_for(base=WORKSPACE, heads=HEADS, catalog_root=None, thresholds=None):
    repo_paths = repo_paths_for(base)
    return Context(
        repo_paths=repo_paths, docs=docs_for(repo_paths),
        capabilities={n: corpus.spec_capabilities(p)
                     for n, p in repo_paths.items()},
        change_ids={n: corpus.change_ids(p) for n, p in repo_paths.items()},
        git=FakeGit(heads=heads), thresholds=thresholds or dict(DEFAULT_THRESHOLDS),
        as_of=AS_OF, agg_root=None, catalog_root=catalog_root)


def build_complete_baseline(root, base=WORKSPACE, heads=HEADS, repos=REPOS):
    """A completed baseline covering the full, unmodified fixture
    workspace — the zero-drift substrate every isolated-defect test
    below builds on, so the ONLY finding it sees is the one seeded
    defect (US2's own shard/resume/merge behavior is exhaustively
    covered by test_catalog_baseline.py; here it is just fixture setup)."""
    for repo in repos:
        catalog_baseline.run_shard(root, repo, 1000, DAY,
                                   entries_for(repo, base, heads))
    marker = catalog_baseline.merge_baseline(root, DAY, repos)
    assert marker is not None
    return marker


def write_incremental_snapshot(root, repo, entries, run_id, taxonomy=None):
    """One extra ordinary run (module-interfaces.md write_snapshot),
    layered on top of a baseline — the mechanism this family's checks
    use to inspect facet data no module in this feature slice writes
    yet, per document_catalog.py's own docstring."""
    return catalog.write_snapshot(
        root, DAY, run_id, repo, entries, TAXONOMY if taxonomy is None
        else taxonomy)


def valid_provenance(**overrides):
    """Per-facet provenance per the promoted
    document-catalog.template.yaml field names — `confidence` nests
    inside provenance; `evidence_refs: []` is a valid recorded value."""
    base = {
        "taxonomy_sha256": TAXONOMY["digest"],
        "method": "classifier",
        "classifier_version": "document-cataloger/1",
        "model": "claude-sonnet-5",
        "prompt_contract_version": 1,
        "confidence": 0.9,
        "section": "## Overview",
        "passage_sha256": "f" * 64,
        "evidence_refs": [],
    }
    base.update(overrides)
    return base


def valid_review(repo, decision, **overrides):
    base = {"authority": f"{repo} authority (Domain Hermes)",
            "decision": decision, "date": DAY_STR}
    base.update(overrides)
    return base


NO_CLASSIFIER_OUTPUT_STATES = ("pending", "unclassified", "policy_blocked")


def assignment(facet, state, values=(), since=DAY_STR, provenance=None,
               review=None, repo="alpha", **extra):
    """A structurally complete facet-assignment item for the given state
    — the contract entry shape ({facet, values, state, state_since,
    provenance, transitions, review} per
    document-catalog.template.yaml). Tests override exactly the one
    field under test so only the intended check fires (data-model.md
    facet state machine)."""
    data = {"facet": facet, "values": list(values), "state": state,
            "state_since": since, "transitions": [], "review": review}
    if state not in NO_CLASSIFIER_OUTPUT_STATES:
        data["provenance"] = (valid_provenance() if provenance is None
                              else provenance)
        if state in ("reviewed", "overridden") and review is None:
            data["review"] = valid_review(repo, state)
    data.update(extra)
    return data


def by_class(findings, cls):
    return [f for f in findings if f.rule.startswith(f"[{cls}] ")]


def rules(findings):
    return sorted(f.rule for f in findings)


# --- clean fixture / baseline-progress mode -----------------------------------

def test_clean_fixture_yields_zero_findings(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)
    ctx = ctx_for(catalog_root=root)
    assert fam_document_catalog(ctx) == []


def test_baseline_progress_mode_reports_info_without_per_document_findings(
        tmp_path):
    root = tmp_path / "agg"
    # "alpha" partially sharded (bounded, not complete); "openxFactory"
    # never started — a legitimate "still running" baseline state.
    catalog_baseline.run_shard(root, "alpha", 1, DAY, entries_for("alpha"))
    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    # US2 acceptance 2 / US3 acceptance 4: progress stated, never one
    # missing-entry finding per legacy document.
    assert len(got) == 1
    assert got[0].severity == INFO
    assert got[0].rule.startswith("[coverage] baseline coverage 1/5 entries")
    assert not catalog_baseline.is_baseline_complete(root)


def test_document_catalog_skips_without_catalog_root():
    ctx = ctx_for(catalog_root=None)
    got = fam_document_catalog(ctx)
    assert isinstance(got, Skip) and got.family == "document-catalog"


# --- coverage (US3 acceptance 1) -----------------------------------------------

def test_coverage_gap_after_baseline_is_flagged(tmp_path):
    root = tmp_path / "agg"
    # Baseline the corpus MINUS one document; the live corpus (ctx.docs)
    # still carries it — a document added after the baseline completed.
    missing_path = "docs/widget-overview.md"
    for repo in REPOS:
        entries = entries_for(repo)
        if repo == "alpha":
            entries = [e for e in entries if e["path"] != missing_path]
        catalog_baseline.run_shard(root, repo, 1000, DAY, entries)
    assert catalog_baseline.merge_baseline(root, DAY, REPOS) is not None

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", missing_path)]
    assert got[0].rule == "[coverage] document has no catalog entry"


# --- stale-entry (US3 acceptance 2) --------------------------------------------

def test_stale_entry_after_content_change_is_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    ws = tmp_path / "workspace"
    shutil.copytree(WORKSPACE, ws)
    edited = ws / "alpha" / "docs" / "widget-overview.md"
    edited.write_text(edited.read_text(encoding="utf-8") + "\nedited\n",
                      encoding="utf-8")

    ctx = ctx_for(base=ws, catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", "docs/widget-overview.md")]
    assert "content hash no longer matches" in got[0].rule


def test_stale_entry_after_revision_only_change_is_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    # An unrelated commit moved alpha's HEAD: every alpha document's
    # content (and hash) is byte-identical, but the recorded revision
    # no longer matches the inventory — stale per US3 acceptance 2
    # ("hash OR revision") and the contract scenario "Catalog entry is
    # stale". openxFactory's HEAD is unchanged and stays clean.
    moved = dict(HEADS, alpha="c" * 40)
    ctx = ctx_for(heads=moved, catalog_root=root)
    got = fam_document_catalog(ctx)
    assert sorted((f.severity, f.repo, f.path) for f in got) == sorted(
        (ERROR, "alpha", e["path"]) for e in entries_for("alpha"))
    assert all(f.rule.startswith("[stale-entry] ") for f in got)
    assert all("repository revision no longer matches" in f.rule
              for f in got)


def test_stale_entry_when_document_is_deleted(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    ws = tmp_path / "workspace"
    shutil.copytree(WORKSPACE, ws)
    (ws / "alpha" / "docs" / "widget-overview.md").unlink()

    ctx = ctx_for(base=ws, catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", "docs/widget-overview.md")]
    assert "no longer exists in the governed corpus" in got[0].rule


# --- duplicate-key --------------------------------------------------------------

def test_duplicate_key_in_recorded_run_is_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted_run = (root / "health" / "document-catalog" / "runs" /
                     DAY_STR / "defect-duplicate-key")
    corrupted_run.mkdir(parents=True)
    document = {
        "schema_version": 1,
        "kind": "xfactory_document_catalog",
        "status": "record",
        "run": {"run_id": "defect-duplicate-key", "repository": "alpha",
                "repository_revision": HEADS["alpha"],
                "inventory_snapshot_id": entries[0]["snapshot_id"]},
        "taxonomy": TAXONOMY,
        "entries": [entries[0], dict(entries[0])],  # duplicate key
    }
    (corrupted_run / "alpha.yaml").write_text(
        catalog.render(document), encoding="utf-8")
    (corrupted_run / "run.yaml").write_text(catalog.render({
        "schema_version": 1, "kind": "xfactory_document_catalog_run",
        "status": "record", "run_id": "defect-duplicate-key",
        "as_of": DAY_STR, "sequence": 1}), encoding="utf-8")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", entries[0]["path"])]
    assert "duplicate catalog key" in got[0].rule


def test_ambiguous_locator_row_is_flagged_not_silently_dropped(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    # Hand-corrupt the recorded baseline (same on-disk tampering
    # convention as test_duplicate_key_in_recorded_run_is_flagged): one
    # row carries BOTH a persisted path and the opaque locator fields
    # (contract scenario "Locator is ambiguous"), and its document is
    # also deleted from the live corpus. An unkeyable row never enters
    # any keyed map — without its own finding it would be invisible to
    # every check, including the stale-entry orphan scan.
    baseline_dir = root / "health" / "document-catalog" / "baseline"
    merged_path = baseline_dir / catalog_baseline.MERGED_NAME
    marker_path = baseline_dir / catalog_baseline.MARKER_NAME
    doc = json.loads(merged_path.read_text(encoding="utf-8"))
    victim = next(e for e in doc["entries"] if e["repo"] == "alpha"
                  and e["path"] == "docs/widget-overview.md")
    victim.update(catalog.opaque_locator("alpha", victim["path"]))
    rendered = catalog.render(doc)
    old_sha = hashlib.sha256(merged_path.read_bytes()).hexdigest()
    new_sha = hashlib.sha256(rendered.encode()).hexdigest()
    merged_path.write_text(rendered, encoding="utf-8")
    marker_path.write_text(
        marker_path.read_text(encoding="utf-8").replace(old_sha, new_sha),
        encoding="utf-8")

    ws = tmp_path / "workspace"
    shutil.copytree(WORKSPACE, ws)
    (ws / "alpha" / "docs" / "widget-overview.md").unlink()

    ctx = ctx_for(base=ws, catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", "docs/widget-overview.md")]
    assert got[0].rule.startswith("[duplicate-key] ")
    assert "ambiguous document locator" in got[0].rule
    assert "merged baseline" in got[0].rule


# --- artifact-type --------------------------------------------------------------

def test_invalid_artifact_type_is_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["artifact_type"] = "widget_yaml"
    write_incremental_snapshot(root, "alpha", corrupted, "defect-artifact-type")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", entries[0]["path"])]
    assert "outside the contract vocabulary" in got[0].rule


# --- taxonomy / controlled-value -----------------------------------------------

def test_unregistered_topic_tag_is_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["facet_assignments"] = [assignment(
        "topic_tags", "suggested", values=["alpha.nonexistent-tag"],
        proposed_values=[])]
    write_incremental_snapshot(root, "alpha", corrupted, "defect-taxonomy")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", entries[0]["path"])]
    assert "is not a controlled tag registry value" in got[0].rule
    assert "'alpha.nonexistent-tag'" in got[0].rule


def test_out_of_vocabulary_closed_facet_values_are_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    # One out-of-vocabulary value per closed contract vocabulary
    # (factory_scope / document_role / sensitivity_signal) — including a
    # classifier trying to LOWER caution with a value like "public",
    # which the contract's sensitivity vocabulary makes unrepresentable.
    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["facet_assignments"] = [
        assignment("factory_scope", "suggested", values=["galactic"]),
        assignment("document_role", "suggested", values=["novel"]),
        assignment("sensitivity_signal", "suggested", values=["public"]),
    ]
    write_incremental_snapshot(root, "alpha", corrupted, "defect-vocab")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert len(got) == 3
    assert all(f.severity == ERROR and f.repo == "alpha"
              and f.path == entries[0]["path"]
              and "outside the contract vocabulary" in f.rule for f in got)
    got_rules = "\n".join(rules(got))
    assert "'galactic'" in got_rules
    assert "'novel'" in got_rules
    assert "'public'" in got_rules


def test_single_valued_facet_cardinality_is_enforced(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    # Contract: factory_scope/document_role/sensitivity_signal SHALL be
    # ONE of their closed vocabulary — never a list of more than one
    # value, and (once classified) never zero. Each in-vocabulary value
    # individually passes the vocabulary check, so a dedicated
    # cardinality check is the only thing that can catch this.
    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["facet_assignments"] = [
        assignment("factory_scope", "suggested",
                   values=["domain", "neutral"]),
        assignment("document_role", "suggested", values=[]),
        assignment("sensitivity_signal", "suggested",
                   values=["unspecified"]),  # exactly one: not flagged
    ]
    write_incremental_snapshot(root, "alpha", corrupted, "defect-cardinality")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert len(got) == 2
    assert all(f.severity == ERROR and f.repo == "alpha"
              and f.path == entries[0]["path"] for f in got)
    got_rules = "\n".join(rules(got))
    assert "factory_scope carries 2 values" in got_rules
    assert "document_role carries 0 values" in got_rules
    assert "requires exactly one single value" in got_rules


def test_single_valued_facet_cardinality_skips_no_output_states(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    # `values: []` is the documented shape for a facet with no
    # classifier output yet (pending/unclassified/policy_blocked) —
    # contract scenario "Pending input changes again" — so the
    # cardinality check must not fire there.
    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["facet_assignments"] = [
        assignment("factory_scope", "pending", values=[]),
        assignment("document_role", "unclassified", values=[]),
        assignment("sensitivity_signal", "policy_blocked", values=[]),
    ]
    write_incremental_snapshot(root, "alpha", corrupted,
                               "defect-cardinality-no-output")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert got == []


def test_invented_facet_name_and_state_are_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    # `domain` was never a contract facet (the six controlled facets are
    # factory_scope/domain_contexts/capability_refs/topic_tags/
    # document_role/sensitivity_signal), and `approved` is outside the
    # six-state vocabulary — model output only ever *suggests*.
    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["facet_assignments"] = [
        assignment("domain", "suggested", values=["alpha.widgets"]),
        assignment("factory_scope", "approved", values=["domain"]),
    ]
    write_incremental_snapshot(root, "alpha", corrupted, "defect-facet-name")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert len(got) == 2
    assert all(f.severity == ERROR and f.repo == "alpha"
              and f.path == entries[0]["path"]
              and f.rule.startswith("[taxonomy] ") for f in got)
    got_rules = "\n".join(rules(got))
    assert "'domain' is not one of the contract's six controlled facets" \
        in got_rules
    assert "state 'approved' is outside the contract's six-state " \
        "vocabulary" in got_rules


def test_dict_keyed_facets_shape_is_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    # Regression guard for the contract realignment: the entry shape is
    # a facet_assignments LIST, never a dict keyed by facet name.
    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["facet_assignments"] = {
        "factory_scope": {"state": "suggested", "values": ["domain"]}}
    write_incremental_snapshot(root, "alpha", corrupted, "defect-dict-shape")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", entries[0]["path"])]
    assert "facet_assignments is not a list" in got[0].rule


def test_duplicate_facet_assignment_is_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["facet_assignments"] = [
        assignment("document_role", "suggested", values=["architecture"]),
        assignment("document_role", "suggested", values=["process"]),
    ]
    write_incremental_snapshot(root, "alpha", corrupted, "defect-dup-facet")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", entries[0]["path"])]
    assert "'document_role' is assigned more than once" in got[0].rule


def test_taxonomy_digest_mismatch_in_recorded_snapshot_is_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    tampered_taxonomy = dict(TAXONOMY, digest="0" * 64)
    run_dir = (root / "health" / "document-catalog" / "runs" / DAY_STR /
              "defect-taxonomy-digest")
    run_dir.mkdir(parents=True)
    document = {
        "schema_version": 1, "kind": "xfactory_document_catalog",
        "status": "record",
        "run": {"run_id": "defect-taxonomy-digest", "repository": "alpha",
                "repository_revision": HEADS["alpha"],
                "inventory_snapshot_id": entries[0]["snapshot_id"]},
        "taxonomy": tampered_taxonomy,
        "entries": entries,
    }
    (run_dir / "alpha.yaml").write_text(catalog.render(document),
                                        encoding="utf-8")
    (run_dir / "run.yaml").write_text(catalog.render({
        "schema_version": 1, "kind": "xfactory_document_catalog_run",
        "status": "record", "run_id": "defect-taxonomy-digest",
        "as_of": DAY_STR, "sequence": 1}), encoding="utf-8")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", "(taxonomy)")]
    assert "recorded taxonomy block is invalid" in got[0].rule


# --- resolution (capability_refs) -----------------------------------------------

def test_unresolved_capability_references_are_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    # Two defective capability references: a bare string that does not
    # name a canonical repository at all (the contract value shape is a
    # {repository, capability} pair), and a well-shaped pair whose
    # capability exists in no promoted or active OpenSpec capability set
    # for its named repository.
    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["facet_assignments"] = [assignment(
        "capability_refs", "suggested",
        values=["ghost-capability",
                {"repository": "alpha", "capability": "ghost-capability"}])]
    write_incremental_snapshot(root, "alpha", corrupted, "defect-resolution")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert len(got) == 2
    assert all(f.severity == WARNING and f.repo == "alpha"
              and f.path == entries[0]["path"]
              and f.rule.startswith("[resolution] ") for f in got)
    got_rules = "\n".join(rules(got))
    assert "does not name a canonical repository and capability" in got_rules
    assert "does not resolve to a promoted or active OpenSpec capability " \
        "in repository 'alpha'" in got_rules


def test_contract_shaped_facets_resolve_cleanly(tmp_path):
    # A complete entry across all six controlled facets, shaped exactly
    # per document-catalog.template.yaml: "widget" is a real alpha
    # capability and "document-lifecycle" a real openxFactory capability
    # (openspec/specs/*/spec.md); alpha.widgets / neutral.governance are
    # registered tags; an UNREGISTERED tag rides in proposed_values,
    # which is legal (contract "Topic tag is unknown": it stays proposed
    # rather than entering the effective values).
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["facet_assignments"] = [
        assignment("factory_scope", "suggested", values=["domain"]),
        assignment("domain_contexts", "suggested", values=["alpha"]),
        assignment("capability_refs", "suggested",
                   values=[{"repository": "alpha",
                            "capability": "widget"},
                           {"repository": "openxFactory",
                            "capability": "document-lifecycle"}]),
        assignment("topic_tags", "suggested",
                   values=["alpha.widgets", "neutral.governance"],
                   proposed_values=["alpha.brand-new-tag"]),
        assignment("document_role", "suggested", values=["architecture"]),
        assignment("sensitivity_signal", "suggested",
                   values=["unspecified"]),
    ]
    write_incremental_snapshot(root, "alpha", corrupted, "facets-ok")

    ctx = ctx_for(catalog_root=root)
    assert fam_document_catalog(ctx) == []


# --- confidence / provenance shape ---------------------------------------------

def test_confidence_and_provenance_shape_defects_are_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    # Provenance per the template field names: nested confidence out of
    # [0, 1], an empty classifier_version, and a missing evidence_refs
    # list (an EMPTY list would be valid; absence is the defect).
    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    bad_provenance = dict(valid_provenance(), confidence=1.5,
                          classifier_version="")
    del bad_provenance["evidence_refs"]
    corrupted[0]["facet_assignments"] = [assignment(
        "factory_scope", "suggested", values=["domain"],
        provenance=bad_provenance)]
    write_incremental_snapshot(root, "alpha", corrupted, "defect-confidence")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert len(got) == 2
    assert {f.rule.split("]")[0] for f in got} == {"[confidence", "[provenance"}
    assert all(f.severity == ERROR and f.repo == "alpha"
              and f.path == entries[0]["path"] for f in got)
    conf = by_class(got, "confidence")[0]
    assert "provenance confidence 1.5" in conf.rule
    prov = by_class(got, "provenance")[0]
    assert "missing classifier_version, evidence_refs" in prov.rule


def test_prompt_contract_version_must_be_an_int(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    # Contract snapshot schema fixes prompt_contract_version as
    # `{type: integer, minimum: 1}` (cataloger.py's
    # `_prompt_contract_version` enforces the same at write time); a
    # hand-authored STRING value is truthy, so a presence-only check
    # would wrongly let it pass this family's provenance shape check.
    entries = entries_for("alpha")
    string_pcv = [dict(e) for e in entries]
    string_pcv[0]["facet_assignments"] = [assignment(
        "factory_scope", "suggested", values=["domain"],
        provenance=dict(valid_provenance(), prompt_contract_version="2"))]
    write_incremental_snapshot(root, "alpha", string_pcv, "defect-pcv-string")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", entries[0]["path"])]
    assert got[0].rule.startswith("[provenance] ")
    assert "prompt_contract_version" in got[0].rule

    # The same facet, corrected to the contract's int shape, is clean.
    int_pcv = [dict(e) for e in entries]
    int_pcv[0]["facet_assignments"] = [assignment(
        "factory_scope", "suggested", values=["domain"],
        provenance=dict(valid_provenance(), prompt_contract_version=2))]
    write_incremental_snapshot(root, "alpha", int_pcv, "defect-pcv-int")

    ctx = ctx_for(catalog_root=root)
    assert fam_document_catalog(ctx) == []


def test_policy_blocked_and_unclassified_facets_are_not_shape_defects(
        tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    # Contract six-state facet vocabulary: a `policy_blocked` facet was
    # never dispatched to the classifier (orchestration records only an
    # opaque blocker reference) and `unclassified` records that no
    # controlled value could resolve — neither carries confidence or
    # provenance, and neither is a shape defect the family may flag
    # (US3 acceptance 3: structurally valid states are never judged).
    entries = entries_for("alpha")
    blocked = [dict(e) for e in entries]
    blocked[0]["facet_assignments"] = [
        assignment("factory_scope", "policy_blocked",
                   blocker_ref="BLOCK-0001"),
        assignment("capability_refs", "unclassified"),
    ]
    write_incremental_snapshot(root, "alpha", blocked, "facet-no-classifier")

    ctx = ctx_for(catalog_root=root)
    assert fam_document_catalog(ctx) == []


# --- override-standing ----------------------------------------------------------

def test_unauthorized_override_standing_is_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["facet_assignments"] = [assignment(
        "factory_scope", "overridden", values=["domain"],
        review={"authority": "beta authority (Domain Hermes)",
                "decision": "overridden", "date": DAY_STR})]
    write_incremental_snapshot(root, "alpha", corrupted, "defect-override")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", entries[0]["path"])]
    assert "does not hold ownership standing" in got[0].rule
    assert "beta authority (Domain Hermes)" in got[0].rule


def test_authorized_override_standing_is_clean(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["facet_assignments"] = [
        assignment("factory_scope", "overridden",
                   values=["domain"])]  # valid_review("alpha", ...)
    write_incremental_snapshot(root, "alpha", corrupted, "defect-override-ok")

    ctx = ctx_for(catalog_root=root)
    assert fam_document_catalog(ctx) == []


def test_neutral_repo_override_standing_uses_the_ratify_gate(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("openxFactory")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["facet_assignments"] = [assignment(
        "factory_scope", "reviewed", values=["neutral"],
        review={"authority": "openxFactory ratify gate",
                "decision": "reviewed", "date": DAY_STR})]
    write_incremental_snapshot(
        root, "openxFactory", corrupted, "defect-neutral-override")

    ctx = ctx_for(catalog_root=root)
    assert fam_document_catalog(ctx) == []


# --- immutable-path (misplaced run artifact) -----------------------------------

def test_misplaced_run_artifact_is_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    # A file sitting directly under the date directory rather than
    # inside a proper run-id subdirectory.
    stray = (root / "health" / "document-catalog" / "runs" / DAY_STR /
            "loose.yaml")
    stray.parent.mkdir(parents=True)
    stray.write_text("bogus\n", encoding="utf-8")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.path) for f in got] == [
        (ERROR, f"runs/{DAY_STR}/loose.yaml")]
    assert "does not conform to the recognized catalog" in got[0].rule


# --- recursion -------------------------------------------------------------------

def test_recursion_of_generated_records_is_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0]["path"] = (
        "health/document-catalog/runs/2026-01-01/x/widget-overview.md")
    write_incremental_snapshot(root, "alpha", corrupted, "defect-recursion")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (ERROR, "alpha", corrupted[0]["path"])]
    assert "generated catalog record entered the catalog itself" in got[0].rule


# --- pending-aging (30-warning / 90-error) -------------------------------------

def test_aged_pending_facet_warning_and_error_are_flagged(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    # 38 days before AS_OF (2026-07-09): warning (>= 30, < 90).
    corrupted[0] = dict(corrupted[0], facet_assignments=[
        assignment("factory_scope", "pending", since="2026-06-01")])
    # 189 days before AS_OF: error (>= 90).
    corrupted[1] = dict(corrupted[1], facet_assignments=[
        assignment("factory_scope", "pending", since="2026-01-01")])
    write_incremental_snapshot(root, "alpha", corrupted, "defect-pending-aging")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert sorted((f.severity, f.path) for f in got) == sorted([
        (WARNING, corrupted[0]["path"]),
        (ERROR, corrupted[1]["path"]),
    ])
    assert "factory_scope facet pending 38 days (warning at 30)" in \
        [f.rule for f in got if f.severity == WARNING][0]
    assert "factory_scope facet pending 189 days (error at 90)" in \
        [f.rule for f in got if f.severity == ERROR][0]


def test_pending_aging_respects_non_default_thresholds(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0] = dict(corrupted[0], facet_assignments=[
        assignment("factory_scope", "pending",
                   since="2026-07-01")])  # 8 days
    write_incremental_snapshot(root, "alpha", corrupted, "defect-pending-custom")

    thresholds = dict(DEFAULT_THRESHOLDS, document_catalog_pending_warning_days=5)
    ctx = ctx_for(catalog_root=root, thresholds=thresholds)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.path) for f in got] == [
        (WARNING, corrupted[0]["path"])]
    assert "warning at 5" in got[0].rule


def test_fresh_pending_facet_does_not_age(tmp_path):
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0] = dict(corrupted[0], facet_assignments=[
        assignment("factory_scope", "pending", since=DAY_STR)])
    write_incremental_snapshot(root, "alpha", corrupted, "defect-pending-fresh")

    ctx = ctx_for(catalog_root=root)
    assert fam_document_catalog(ctx) == []


def test_aged_policy_blocked_facet_never_fires_pending_aging(tmp_path):
    # Adversarial-recheck regression (contract "Host is not authorized
    # for protected content"): a policy_blocked facet must NEVER enter
    # the 30/90-day pending clocks, however old its state_since — only
    # a MISLABELED `pending` record would age, and
    # cataloger.pending_records now forbids exactly that mislabeling. A
    # genuinely pending facet of the same age on a sibling document
    # proves the aging machinery itself is live in this snapshot.
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    # 189 days before AS_OF — deep in error territory were it pending.
    # The blocker rides on the entry-level dispatch_policy (review
    # finding 1), never on a facet_assignment, so these policy_blocked
    # facets carry no blocker field of their own.
    corrupted[0] = dict(corrupted[0], facet_assignments=[
        assignment("factory_scope", "policy_blocked", since="2026-01-01"),
        assignment("topic_tags", "policy_blocked", since="2026-01-01")])
    corrupted[1] = dict(corrupted[1], facet_assignments=[
        assignment("factory_scope", "pending", since="2026-01-01")])
    write_incremental_snapshot(root, "alpha", corrupted, "blocked-no-aging")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)
    assert [(f.severity, f.path) for f in got] == [
        (ERROR, corrupted[1]["path"])]
    assert "factory_scope facet pending 189 days (error at 90)" in \
        got[0].rule


def test_malformed_pending_state_since_is_reported_not_crashed(tmp_path):
    # Review finding 3 (Copilot #2): a persisted pending facet whose
    # state_since is malformed must NOT crash the family (and every
    # family after it) out of date.fromisoformat — "2026-13-99" even
    # passes the _DATE_RE digit-shape check yet is not a real date, and a
    # non-date string fails the shape check; both are reported as shape
    # findings, and the aging clock is simply not computed.
    root = tmp_path / "agg"
    build_complete_baseline(root)

    entries = entries_for("alpha")
    corrupted = [dict(e) for e in entries]
    corrupted[0] = dict(corrupted[0], facet_assignments=[
        assignment("factory_scope", "pending", since="2026-13-99")])
    corrupted[1] = dict(corrupted[1], facet_assignments=[
        assignment("factory_scope", "pending", since="not-a-date")])
    write_incremental_snapshot(root, "alpha", corrupted, "defect-bad-since")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)  # must not raise ValueError
    assert sorted((f.severity, f.path) for f in got) == sorted([
        (ERROR, corrupted[0]["path"]),
        (ERROR, corrupted[1]["path"]),
    ])
    assert all(f.rule.startswith("[taxonomy] ") and "state_since" in f.rule
               and "not a valid" in f.rule for f in got)
    assert any("'2026-13-99'" in f.rule for f in got)


# --- catalog-integrity (corrupt / torn / foreign persisted artifacts) ----------

def test_corrupt_baseline_merged_is_reported_not_crashed(tmp_path):
    # Review findings 5/6: a corrupt/torn/foreign PERSISTED catalog
    # artifact must surface as a finding, never crash the whole
    # doc-health run. Here the merged baseline fold is truncated to
    # unparseable JSON (load_baseline read path).
    root = tmp_path / "agg"
    build_complete_baseline(root)
    merged = (root / "health" / "document-catalog" / "baseline" /
              catalog_baseline.MERGED_NAME)
    merged.write_text("{ this is not json", encoding="utf-8")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)  # must not raise
    integrity = [f for f in got if f.rule.startswith("[catalog-integrity] ")]
    assert len(integrity) == 1
    assert integrity[0].severity == ERROR


def test_corrupt_run_snapshot_is_reported_not_crashed(tmp_path):
    # A torn per-repo snapshot in the latest run (load_snapshot ->
    # _load_run read path; JSONDecodeError vector).
    root = tmp_path / "agg"
    build_complete_baseline(root)
    write_incremental_snapshot(root, "alpha", entries_for("alpha"),
                               "run-to-corrupt")
    snap = (root / "health" / "document-catalog" / "runs" / DAY_STR /
            "run-to-corrupt" / "alpha.yaml")
    snap.write_text("<<not json>>", encoding="utf-8")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)  # must not raise
    integrity = [f for f in got if f.rule.startswith("[catalog-integrity] ")]
    assert len(integrity) == 1


def test_wrong_shape_run_meta_is_reported_not_crashed(tmp_path):
    # A run.yaml that is a JSON LIST, not an object (the
    # `_load_yaml_json(meta).get('sequence')` AttributeError vector in
    # _iter_runs).
    root = tmp_path / "agg"
    build_complete_baseline(root)
    write_incremental_snapshot(root, "alpha", entries_for("alpha"),
                               "run-list-meta")
    meta = (root / "health" / "document-catalog" / "runs" / DAY_STR /
            "run-list-meta" / "run.yaml")
    meta.write_text("[1, 2, 3]\n", encoding="utf-8")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)  # must not raise
    integrity = [f for f in got if f.rule.startswith("[catalog-integrity] ")]
    assert len(integrity) == 1


def test_corrupt_baseline_shard_is_reported_not_crashed(tmp_path):
    # A foreign/torn shard artifact under shards/ (the _chain/progress
    # index vector). Progress mode reads every shard each run.
    root = tmp_path / "agg"
    catalog_baseline.run_shard(root, "alpha", 1000, DAY, entries_for("alpha"))
    shard = next((root / "health" / "document-catalog" / "baseline" /
                  "shards" / "alpha").glob("*.yaml"))
    shard.write_text("{ broken", encoding="utf-8")

    ctx = ctx_for(catalog_root=root)
    got = fam_document_catalog(ctx)  # must not raise
    integrity = [f for f in got if f.rule.startswith("[catalog-integrity] ")]
    assert len(integrity) == 1


def test_run_suite_does_not_crash_on_corrupt_catalog_artifact(tmp_path):
    # Review finding 6: run_suite's per-family dispatch (`out = fn(ctx)`)
    # has no guard, so a family that RAISED on corrupt persisted data
    # would abort the whole run. Driven through run_suite to prove the
    # family now returns a catalog-integrity finding instead.
    root = tmp_path / "agg"
    build_complete_baseline(root)
    merged = (root / "health" / "document-catalog" / "baseline" /
              catalog_baseline.MERGED_NAME)
    merged.write_text("{ truncated", encoding="utf-8")

    ctx = ctx_for(catalog_root=root)
    result = runner.run_suite(ctx, "document-catalog", set())  # must not raise
    integrity = [f for f in result.findings
                 if f.rule.startswith("[catalog-integrity] ")]
    assert len(integrity) == 1
    assert not result.skips  # surfaced as a finding, never skipped away


# --- runner integration (quickstart section 4) ---------------------------------

def test_runner_family_document_catalog_integration(tmp_path):
    repo = tmp_path / "alpha"
    shutil.copytree(WORKSPACE / "alpha", repo)
    # This fixture directory is not a real git checkout, so live-corpus
    # comparisons (coverage/stale-entry) degrade to silence per
    # document_catalog._live_mechanical_entries — the misplaced-artifact
    # defect below still surfaces through the real CLI wiring.
    stray = (repo / "health" / "document-catalog" / "runs" / DAY_STR /
            "loose.yaml")
    stray.parent.mkdir(parents=True)
    stray.write_text("bogus\n", encoding="utf-8")

    report_out = tmp_path / "report.md"
    rc = runner.main([
        "--single-repo", str(repo), "--family", "document-catalog",
        "--as-of", DAY_STR, "--report-out", str(report_out)])
    assert rc == 0
    text = report_out.read_text(encoding="utf-8")
    assert "### document-catalog" in text
    assert "misplaced catalog artifact" in text
    assert f"loose.yaml" in text


def test_runner_family_document_catalog_clean_single_repo(tmp_path):
    # No health/document-catalog/ tree at all: nothing to flag, and the
    # family still appears (with "No findings.") per FR-006.
    repo = tmp_path / "alpha"
    shutil.copytree(WORKSPACE / "alpha", repo)

    report_out = tmp_path / "report.md"
    rc = runner.main([
        "--single-repo", str(repo), "--family", "document-catalog",
        "--as-of", DAY_STR, "--report-out", str(report_out)])
    assert rc == 0
    text = report_out.read_text(encoding="utf-8")
    assert "### document-catalog" in text
    assert "No findings." in text
