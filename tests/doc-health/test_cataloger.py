"""Bounded document-cataloger worker module (US4/US5): change-driven
selection, bounded/protected-filtered shard building, the neutral job
envelope, whole-artifact output validation, immutable recommendation
persistence, later-snapshot-only merge, authority-checked owner
dispositions, and content/taxonomy/prompt invalidation.

A fake worker (a plain Python callable returning a dict, or raising)
stands in for the model everywhere — no live model calls in tests
(quickstart section 5). All tests are hermetic: the fixture workspace
(shared with test_catalog.py) is read-only, git facts come from
conftest.FakeGit, and every write lands under a tmp catalog root."""

from __future__ import annotations

import hashlib
import json
from datetime import date

import pytest

from conftest import AS_OF, FIXTURES, FakeGit  # noqa: F401 (sys.path side effect)

from doc_health import DEFAULT_THRESHOLDS, WARNING
from doc_health import cataloger, catalog, catalog_baseline, corpus, inventory
from doc_health.corpus import load_docs
from doc_health.families import FAMILIES
from doc_health.runner import Context
from doc_health.semantic import NEUTRAL_DISPOSER, NEUTRAL_REPO

WORKSPACE = FIXTURES / "catalog" / "workspace"
HEADS = {"alpha": "a" * 40, "openxFactory": "b" * 40}
LATER_HEADS = {"alpha": "c" * 40, "openxFactory": "d" * 40}
DAY = AS_OF  # date(2026, 7, 9) — dates are parameters, never wall clock
DAY_STR = AS_OF.isoformat()
# Transitions record an RFC 3339 date-time (snapshot schema
# #/$defs/transition occurred_at: {format: date-time}) derived
# deterministically from the run date; state_since stays the bare date.
DAY_DT = f"{DAY_STR}T00:00:00Z"

MODEL = "claude-sonnet-5"
# The contract provenance shape fixes prompt_contract_version as an
# integer >= 1 and taxonomy_sha256 as a 64-hex effective digest
# (xfactory-document-catalog-snapshot.schema.yaml #/$defs/provenance).
PROMPT_VERSION = 1
TAXONOMY_SHA = "e" * 64

REGISTRY_PATHS = {
    "alpha": "catalog/document-tag-registry.yaml",
    "openxFactory": "contracts/document-tag-registry.yaml",
}
REGISTRY_REVISIONS = {"alpha": "1" * 40, "openxFactory": "2" * 40}


# --- fixture-workspace helpers (test_catalog.py precedent) -------------------

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


def registry_inputs(base=WORKSPACE, heads=HEADS):
    return [
        catalog.registry_input(
            repo, REGISTRY_PATHS[repo], base / repo / REGISTRY_PATHS[repo],
            repository_revision=heads[repo],
            registry_revision=REGISTRY_REVISIONS[repo])
        for repo in sorted(REGISTRY_PATHS)]


TAXONOMY = catalog.effective_taxonomy(registry_inputs())


# --- hand-built entry / facet-assignment helpers (test_document_catalog.py
# precedent: a structurally complete fixture where tests override exactly
# the one field under test) ----------------------------------------------

def make_entry(repo="alpha", path="docs/a.md", content_hash="1" * 64,
              handling=None, **extra):
    entry = {
        "repo": repo, "path": path, "status": "draft", "kind": None,
        "repository_context": None, "handling": handling,
        "artifact_type": "governance_markdown", "revision": "a" * 40,
        "content_hash": content_hash, "snapshot_id": "s" * 64,
    }
    entry.update(extra)
    return entry


def valid_provenance(**overrides):
    base = {
        "taxonomy_sha256": TAXONOMY_SHA, "method": "classifier",
        "classifier_version": cataloger.CLASSIFIER_VERSION, "model": MODEL,
        "prompt_contract_version": PROMPT_VERSION, "confidence": 0.9,
        "section": "## Overview", "passage_sha256": "f" * 64,
        "evidence_refs": [],
    }
    base.update(overrides)
    return base


def facet_assignment(facet, values, state="suggested", since=DAY_STR,
                     provenance=None, **extra):
    """A structurally complete facet-assignment item (data-model.md
    facet state machine); tests override exactly the field under test."""
    data = {"facet": facet, "values": list(values), "proposed_values": [],
            "state": state, "state_since": since, "transitions": [],
            "review": None}
    if state not in ("pending", "unclassified", "policy_blocked"):
        data["provenance"] = (valid_provenance() if provenance is None
                              else provenance)
    data.update(extra)
    return data


def catalog_entry(entry, assignments=()):
    """A catalogued entry: mechanical fields plus (optionally)
    facet_assignments — absent entirely when never classified."""
    out = dict(entry)
    if assignments:
        out["facet_assignments"] = list(assignments)
    return out


# The verbatim grounding excerpt a prompt-contract-v2 worker returns, and
# the digest orchestration computes from it — normalized EXACTLY as
# ``semantic.passage_id`` does (`" ".join(passage.split())`) so the two
# doc-health lanes agree byte-for-byte on the passage digest.
DEFAULT_PASSAGE = "The Overview section grounds this classification."


def expected_passage_sha256(passage):
    """The provenance ``passage_sha256`` ``enforce_contract`` computes for a
    given worker passage — the cross-lane-consistent normalized digest."""
    return hashlib.sha256(" ".join(passage.split()).encode()).hexdigest()


DEFAULT_PASSAGE_SHA256 = expected_passage_sha256(DEFAULT_PASSAGE)


def raw_assignment(facet, values, confidence=0.9, section="## Overview",
                   passage=DEFAULT_PASSAGE, evidence_refs=(),
                   proposed_values=()):
    """A well-formed WORKER-side facet assignment (before harness
    provenance is added by ``enforce_contract``). Prompt contract v2: the
    worker returns the grounding ``passage`` VERBATIM (a tool-less model
    cannot hash it); orchestration computes the persisted
    ``passage_sha256``."""
    return {"facet": facet, "values": list(values), "confidence": confidence,
            "section": section, "passage": passage,
            "evidence_refs": list(evidence_refs),
            "proposed_values": list(proposed_values)}


def job_for(shard, taxonomy=TAXONOMY_SHA, model=MODEL,
           prompt=PROMPT_VERSION):
    return cataloger.envelope(DAY, model, prompt, shard, taxonomy)


def shard_and_job(*selections):
    shard = cataloger.build_shards(list(selections), budget=10)[0]
    return shard, job_for(shard)


# --- select() (T017) ----------------------------------------------------------

def test_first_run_selects_the_full_corpus():
    # Acceptance 1: a first cataloger run selects everything.
    inv = [make_entry(path="docs/a.md", content_hash="1" * 64),
          make_entry(path="docs/b.md", content_hash="2" * 64)]
    selections = cataloger.select(inv, None, [])
    assert [(s.repo, s.path, s.reason) for s in selections] == \
        [("alpha", "docs/a.md", "baseline"),
         ("alpha", "docs/b.md", "baseline")]
    # Never mutates any input.
    assert inv[0]["content_hash"] == "1" * 64


def test_unchanged_corpus_selects_nothing_across_unrelated_commits():
    # Acceptance 1 continued + contract "Unchanged incremental run
    # executes": zero selection even though revision moved.
    entry = make_entry(content_hash="1" * 64, revision="a" * 40)
    cat = [catalog_entry(entry, [facet_assignment(
        "factory_scope", ["domain"])])]
    unrelated_commit = dict(entry, revision="b" * 40)
    selections = cataloger.select([unrelated_commit], [entry], cat)
    assert selections == []


def test_new_document_is_selected():
    existing = make_entry(path="docs/a.md", content_hash="1" * 64)
    cat = [catalog_entry(existing, [facet_assignment(
        "factory_scope", ["domain"])])]
    new_doc = make_entry(path="docs/b.md", content_hash="2" * 64)
    selections = cataloger.select([existing, new_doc], [existing], cat)
    assert [(s.repo, s.path, s.reason) for s in selections] == \
        [("alpha", "docs/b.md", "new")]


def test_changed_content_is_selected_and_only_that_document():
    # Acceptance for SC-004: "a single document edit selects only that
    # document."
    a = make_entry(path="docs/a.md", content_hash="1" * 64)
    b = make_entry(path="docs/b.md", content_hash="2" * 64)
    cat = [catalog_entry(a, [facet_assignment("factory_scope", ["domain"])]),
          catalog_entry(b, [facet_assignment("factory_scope", ["domain"])])]
    edited_a = dict(a, content_hash="9" * 64)
    selections = cataloger.select([edited_a, b], [a, b], cat)
    assert [(s.repo, s.path, s.reason) for s in selections] == \
        [("alpha", "docs/a.md", "changed")]


def test_missing_classification_is_selected():
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    other = make_entry(path="docs/b.md", content_hash="2" * 64)
    cat = [catalog_entry(entry),  # mechanically catalogued, never classified
          catalog_entry(other, [facet_assignment(
              "factory_scope", ["domain"])])]
    selections = cataloger.select([entry, other], [entry, other], cat)
    assert [(s.repo, s.path, s.reason) for s in selections] == \
        [("alpha", "docs/a.md", "missing")]


def test_pending_facet_is_selected():
    entry = make_entry(content_hash="1" * 64)
    cat = [catalog_entry(entry, [facet_assignment(
        "factory_scope", ["domain"], state="pending")])]
    selections = cataloger.select([entry], [entry], cat)
    assert [(s.repo, s.path, s.reason) for s in selections] == \
        [("alpha", "docs/a.md", "pending")]


def test_taxonomy_or_prompt_incompatible_facet_is_stale():
    # Contract "Taxonomy has a breaking change".
    entry = make_entry(content_hash="1" * 64)
    cat = [catalog_entry(entry, [facet_assignment(
        "factory_scope", ["domain"],
        provenance=valid_provenance(taxonomy_sha256="old" * 16))])]
    selections = cataloger.select(
        [entry], [entry], cat, current_taxonomy_sha256=TAXONOMY_SHA)
    assert [(s.repo, s.path, s.reason) for s in selections] == \
        [("alpha", "docs/a.md", "stale")]
    # Without a current taxonomy/prompt to compare against, nothing is
    # falsely flagged stale.
    assert cataloger.select([entry], [entry], cat) == []
    prompt_stale = [catalog_entry(entry, [facet_assignment(
        "factory_scope", ["domain"],
        provenance=valid_provenance(prompt_contract_version=0))])]
    selections = cataloger.select(
        [entry], [entry], prompt_stale, current_prompt_version=1)
    assert [s.reason for s in selections] == ["stale"]


def test_generated_catalog_paths_are_never_selected():
    generated = make_entry(
        path="health/document-catalog/runs/2026-07-08/x/alpha.yaml")
    assert cataloger.select([generated], None, []) == []


def test_end_to_end_first_run_over_the_fixture_workspace_selects_and_shards():
    inv = extended_inventory()
    alpha_inv = [e for e in inv if e["repo"] == "alpha"]
    selections = cataloger.select(alpha_inv, None, [])
    assert selections and all(s.reason == "baseline" for s in selections)
    shards = cataloger.build_shards(selections, budget=3)
    dispatched = {s.path for shard in shards for s in shard.selections}
    # The protected fixture document never reaches a shard.
    assert "docs/protected-roster.md" not in dispatched
    assert dispatched == {s.path for s in selections} - {
        "docs/protected-roster.md"}
    assert all(len(shard.selections) <= 3 for shard in shards)


def test_end_to_end_unchanged_corpus_selects_nothing_after_full_classification():
    # Independent Test: "a re-run over an unchanged corpus selects
    # nothing", over the real fixture corpus, including an unrelated
    # commit (later HEADs, zero content change).
    inv = extended_inventory()
    alpha_inv = [e for e in inv if e["repo"] == "alpha"]
    fully_classified = [
        catalog_entry(e, [facet_assignment("factory_scope", ["domain"])])
        for e in alpha_inv]
    assert cataloger.select(alpha_inv, alpha_inv, fully_classified) == []
    later_inv = [e for e in extended_inventory(WORKSPACE, LATER_HEADS)
                if e["repo"] == "alpha"]
    assert cataloger.select(later_inv, alpha_inv, fully_classified) == []


# --- build_shards (T017) ------------------------------------------------------

def test_build_shards_bounds_and_orders_deterministically():
    selections = [
        cataloger.Selection("alpha", "docs/c.md", "3" * 64, "new",
                           make_entry(path="docs/c.md")),
        cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                           make_entry(path="docs/a.md")),
        cataloger.Selection("alpha", "docs/b.md", "2" * 64, "new",
                           make_entry(path="docs/b.md")),
    ]
    shards = cataloger.build_shards(selections, budget=2)
    assert len(shards) == 2
    assert [s.path for s in shards[0].selections] == \
        ["docs/a.md", "docs/b.md"]
    assert [s.path for s in shards[1].selections] == ["docs/c.md"]
    # Deterministic shard ids: caller order never matters.
    again = cataloger.build_shards(list(reversed(selections)), budget=2)
    assert [s.shard_id for s in shards] == [s.shard_id for s in again]


def test_build_shards_filters_protected_before_dispatch():
    protected = cataloger.Selection(
        "alpha", "docs/protected.md", "9" * 64, "new",
        make_entry(path="docs/protected.md", handling="protected"))
    ordinary = cataloger.Selection(
        "alpha", "docs/a.md", "1" * 64, "new", make_entry())
    shards = cataloger.build_shards([protected, ordinary], budget=10)
    dispatched = [s.path for shard in shards for s in shard.selections]
    assert dispatched == ["docs/a.md"]


def test_build_shards_rejects_a_non_positive_budget():
    with pytest.raises(ValueError):
        cataloger.build_shards([], budget=0)
    with pytest.raises(ValueError):
        cataloger.build_shards([], budget=True)  # bool is not a real int here
    with pytest.raises(ValueError):
        cataloger.build_shards([], budget=-1)


# --- job envelope (T018) ------------------------------------------------------

def test_envelope_is_neutral_bounded_and_deterministic():
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard = cataloger.build_shards([sel], budget=10)[0]
    env = cataloger.envelope(DAY, MODEL, PROMPT_VERSION, shard, TAXONOMY_SHA)
    job = env["job"]
    assert job["job_type"] == "document_cataloger"
    assert job["worker_selector"] == {
        "profile": "document-cataloger", "model": MODEL,
        "prompt_contract_version": PROMPT_VERSION}
    assert job["auth_profile"] == "read_only_no_credentials"
    assert job["stop_conditions"]["max_repo_writes"] == 0
    assert job["traceability"]["shard_id"] == shard.shard_id
    assert job["traceability"]["taxonomy_sha256"] == TAXONOMY_SHA
    assert job["traceability"]["as_of"] == DAY_STR
    # Deterministic id: identical inputs -> identical job id, never wall
    # clock; a different shard -> a different id.
    again = cataloger.envelope(DAY, MODEL, PROMPT_VERSION, shard, TAXONOMY_SHA)
    assert again["job"]["id"] == job["id"]
    other_shard = cataloger.build_shards(
        [cataloger.Selection("alpha", "docs/z.md", "0" * 64, "new",
                             make_entry(path="docs/z.md"))], budget=10)[0]
    other = cataloger.envelope(DAY, MODEL, PROMPT_VERSION, other_shard,
                               TAXONOMY_SHA)
    assert other["job"]["id"] != job["id"]


def test_envelope_requires_a_valid_taxonomy_digest_and_prompt_version():
    # Reconciliation items 1 & 3: the effective taxonomy digest is a
    # REQUIRED argument, validated against the contract pattern
    # `^[0-9a-f]{64}$` (never null/malformed into provenance), and the
    # prompt version is coerced to the contract's integer form.
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard = cataloger.build_shards([sel], budget=10)[0]
    for bad_digest in (None, "", "t" * 64, "abc", "A" * 64, "e" * 63):
        with pytest.raises(ValueError):
            cataloger.envelope(DAY, MODEL, PROMPT_VERSION, shard, bad_digest)
    for bad_version in ("one", 0, -1, True, 1.5, None):
        with pytest.raises(ValueError):
            cataloger.envelope(DAY, MODEL, bad_version, shard, TAXONOMY_SHA)
    # A valid string form is coerced to the integer the provenance shape
    # requires, and the id stays stable across the string/int forms.
    string_form = cataloger.envelope(DAY, MODEL, "1", shard, TAXONOMY_SHA)
    assert string_form["job"]["worker_selector"][
        "prompt_contract_version"] == 1
    assert string_form["job"]["id"] == cataloger.envelope(
        DAY, MODEL, 1, shard, TAXONOMY_SHA)["job"]["id"]


def test_load_prompt_contract_returns_an_integer_version():
    # Reconciliation item 1: the version is coerced to the contract's
    # integer form at load time, never left as the regex string capture.
    # Prompt contract v2 moved passage evidence to a worker-returned
    # verbatim passage (digest computed orchestration-side); v3 dropped
    # the worker-echoed content_hash (sourced authoritatively from the
    # shard instead).
    version, text = cataloger.load_prompt_contract()
    assert version == 3 and isinstance(version, int)
    assert "Prompt-Contract-Version" in text


# --- whole-artifact output validation (T018) ---------------------------------

def test_enforce_contract_accepts_a_valid_artifact():
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    raw = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [
            raw_assignment("factory_scope", ["domain"]),
            raw_assignment("topic_tags", ["alpha.widgets"],
                          proposed_values=["alpha.new-topic"]),
        ],
    }]}
    records, rejects = cataloger.enforce_contract(raw, shard, job)
    assert rejects == []
    assert len(records) == 1
    record = records[0]
    assert record["repo"] == "alpha" and record["path"] == "docs/a.md"
    assert record["content_hash"] == "1" * 64
    facets = {a["facet"]: a for a in record["facet_assignments"]}
    assert set(facets) == {"factory_scope", "topic_tags"}
    fs = facets["factory_scope"]
    assert fs["values"] == ["domain"] and fs["state"] == "suggested"
    assert fs["state_since"] == DAY_STR
    assert fs["provenance"] == {
        "taxonomy_sha256": TAXONOMY_SHA, "method": "classifier",
        "classifier_version": cataloger.CLASSIFIER_VERSION, "model": MODEL,
        "prompt_contract_version": PROMPT_VERSION, "confidence": 0.9,
        "section": "## Overview",
        # Computed orchestration-side from the worker's verbatim passage
        # (prompt contract v2), never copied from worker output.
        "passage_sha256": DEFAULT_PASSAGE_SHA256,
        "evidence_refs": [],
    }
    assert fs["transitions"] == [{"from": "pending", "to": "suggested",
                                  "occurred_at": DAY_DT,
                                  "evidence_refs": []}]
    assert fs["review"] is None
    assert facets["topic_tags"]["proposed_values"] == ["alpha.new-topic"]


def test_enforce_contract_rejects_invented_effective_tags():
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    raw = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [raw_assignment("factory_scope", ["galactic"])],
    }]}
    records, rejects = cataloger.enforce_contract(raw, shard, job)
    assert records == []
    assert any("invented" in r for r in rejects)


def test_enforce_contract_rejects_sensitivity_lowering_below_declared_handling():
    # Contract scenario "Sensitivity inference lowers caution".
    entry = make_entry(path="docs/sensitive.md", content_hash="5" * 64,
                       handling="confidential")
    sel = cataloger.Selection("alpha", "docs/sensitive.md", "5" * 64, "new",
                              entry)
    shard, job = shard_and_job(sel)
    raw = {"entries": [{
        "repo": "alpha", "path": "docs/sensitive.md",
        "content_hash": "5" * 64,
        "facet_assignments": [
            raw_assignment("sensitivity_signal", ["unspecified"])],
    }]}
    records, rejects = cataloger.enforce_contract(raw, shard, job)
    assert records == []
    assert any("lower" in r for r in rejects)
    # Raising caution (never lowering) is always accepted.
    raised = {"entries": [{
        "repo": "alpha", "path": "docs/sensitive.md",
        "content_hash": "5" * 64,
        "facet_assignments": [
            raw_assignment("sensitivity_signal", ["potentially_sensitive"])],
    }]}
    records, rejects = cataloger.enforce_contract(raised, shard, job)
    assert rejects == [] and len(records) == 1


def test_enforce_contract_rejects_missing_provenance():
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    # The two worker-supplied evidence fields (prompt contract v2): a
    # `section` reference and the verbatim grounding `passage`.
    for missing_field in ("section", "passage"):
        bad = raw_assignment("factory_scope", ["domain"])
        del bad[missing_field]
        raw = {"entries": [{
            "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
            "facet_assignments": [bad],
        }]}
        records, rejects = cataloger.enforce_contract(raw, shard, job)
        assert records == []
        assert any(missing_field.split("_")[0] in r for r in rejects)


def test_enforce_contract_computes_passage_digest_when_worker_cannot_hash():
    # Live-run regression (runs 29344503264 / 29344452894): the cataloger
    # child runs tool-less and single-turn (`claude -p --tools ""
    # --max-turns 1`) and CANNOT compute SHA-256 — on the first real run
    # it rationally returned empty entries rather than fabricate a hash.
    # Prompt contract v2 therefore has the worker return the grounding
    # PASSAGE verbatim and orchestration computes the digest (mirroring
    # `semantic.passage_id`). A facet assignment carrying `passage` but NO
    # `passage_sha256` is accepted, and the persisted provenance digest is
    # the computed normalized-passage hash — never a worker-copied one.
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    passage = "Workers  must\nalways ground\ttheir suggestions."
    item = raw_assignment("factory_scope", ["domain"], passage=passage)
    assert "passage_sha256" not in item  # a tool-less model never sends one
    raw = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [item],
    }]}
    records, rejects = cataloger.enforce_contract(raw, shard, job)
    assert rejects == [] and len(records) == 1
    prov = records[0]["facet_assignments"][0]["provenance"]
    assert prov["passage_sha256"] == expected_passage_sha256(passage)
    # A 64-char lowercase hex digest by construction (schema
    # #/$defs/provenance `passage_sha256: {pattern: "^[0-9a-f]{64}$"}`).
    assert len(prov["passage_sha256"]) == 64
    assert all(c in "0123456789abcdef" for c in prov["passage_sha256"])
    # A worker-supplied `passage_sha256` is an unread key under v2 (the
    # validator has never rejected unexpected per-assignment keys): the
    # COMPUTED digest wins and the worker's fabricated copy never persists.
    spoofed = raw_assignment("document_role", ["process"], passage=passage)
    spoofed["passage_sha256"] = "b" * 64  # meaningless / fabricated
    raw2 = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [spoofed],
    }]}
    records2, rejects2 = cataloger.enforce_contract(raw2, shard, job)
    assert rejects2 == []
    assert records2[0]["facet_assignments"][0]["provenance"][
        "passage_sha256"] == expected_passage_sha256(passage)


def test_enforce_contract_rejects_missing_or_empty_passage():
    # Prompt contract v2: the verbatim grounding passage is required worker
    # evidence — orchestration cannot derive a digest without it. A
    # missing, empty, whitespace-only, or non-string passage voids the
    # whole artifact, the same whole-artifact semantics as the neighboring
    # section check.
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    missing = raw_assignment("factory_scope", ["domain"])
    del missing["passage"]
    for bad_item in (
            missing,
            raw_assignment("factory_scope", ["domain"], passage=""),
            raw_assignment("factory_scope", ["domain"], passage="   "),
            raw_assignment("factory_scope", ["domain"], passage=123),
            raw_assignment("factory_scope", ["domain"], passage=None)):
        raw = {"entries": [{
            "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
            "facet_assignments": [bad_item],
        }]}
        records, rejects = cataloger.enforce_contract(raw, shard, job)
        assert records == []
        assert any("passage" in r for r in rejects)


def test_enforce_contract_rejects_malformed_evidence_refs_elements():
    # Review finding 2: each evidence_refs element must satisfy the
    # contract evidence_ref shape (snapshot schema #/$defs/evidence_ref
    # oneOf: a non-empty string, OR a {repo, path} mapping of non-empty
    # strings and no other keys). Validating only "is a list" let an
    # empty string, a partial/over-populated mapping, and non-string/
    # non-object elements through into a schema-invalid record.
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    for bad in ([""], [{"repo": "x"}], [{"path": "y"}], [123], [None],
                [True], [{"repo": "x", "path": "y", "extra": 1}],
                [{"repo": "", "path": "y"}], [{"repo": "x", "path": ""}],
                ["ok", ""]):
        raw = {"entries": [{
            "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
            "facet_assignments": [raw_assignment(
                "factory_scope", ["domain"], evidence_refs=bad)],
        }]}
        records, rejects = cataloger.enforce_contract(raw, shard, job)
        assert records == [], bad
        assert any("evidence_refs" in r for r in rejects), bad
    # Both accepted evidence_ref shapes (a non-empty string and a
    # {repo, path} mapping) pass and are copied verbatim into provenance.
    good = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [raw_assignment(
            "factory_scope", ["domain"],
            evidence_refs=["a passage citation",
                           {"repo": "alpha", "path": "docs/b.md"}])],
    }]}
    records, rejects = cataloger.enforce_contract(good, shard, job)
    assert rejects == [] and len(records) == 1
    assert records[0]["facet_assignments"][0]["provenance"][
        "evidence_refs"] == ["a passage citation",
                             {"repo": "alpha", "path": "docs/b.md"}]


def test_enforce_contract_rejects_non_numeric_confidence():
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    for bad_confidence in ("high", None, True, 1.5, -0.1):
        raw = {"entries": [{
            "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
            "facet_assignments": [raw_assignment(
                "factory_scope", ["domain"], confidence=bad_confidence)],
        }]}
        records, rejects = cataloger.enforce_contract(raw, shard, job)
        assert records == []
        assert any("confidence" in r for r in rejects)


def test_enforce_contract_rejects_the_whole_artifact_not_just_the_bad_entry():
    # Spec edge case "Classifier emits partially valid output": the
    # valid docs/a.md entry is never rescued from the invalid artifact.
    good = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                               make_entry(path="docs/a.md"))
    bad_sel = cataloger.Selection(
        "alpha", "docs/b.md", "2" * 64, "new",
        make_entry(path="docs/b.md", content_hash="2" * 64))
    shard, job = shard_and_job(good, bad_sel)
    raw = {"entries": [
        {"repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
         "facet_assignments": [raw_assignment("factory_scope", ["domain"])]},
        {"repo": "alpha", "path": "docs/b.md", "content_hash": "2" * 64,
         "facet_assignments": [raw_assignment(
             "factory_scope", ["not-a-scope"])]},
    ]}
    records, rejects = cataloger.enforce_contract(raw, shard, job)
    assert records == []
    assert rejects


def test_enforce_contract_accepts_entries_without_content_hash():
    # Prompt contract v3 regression (live run 29349336374 / child
    # 29349393119): under v2 the worker echoed the 64-char content_hash and
    # a single dropped hex character in ONE of 25 otherwise-correct entries
    # (...184c45095009cb1a vs ...184c95009cb1a, 63 chars) voided the whole
    # artifact. v3 drops the echo entirely -- an artifact whose entries
    # carry NO content_hash is accepted, and every persisted record's
    # content_hash is the AUTHORITATIVE shard-selection value.
    sel_a = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                                make_entry(path="docs/a.md"))
    sel_b = cataloger.Selection("alpha", "docs/b.md", "2" * 64, "new",
                                make_entry(path="docs/b.md",
                                           content_hash="2" * 64))
    shard, job = shard_and_job(sel_a, sel_b)
    raw = {"entries": [
        {"repo": "alpha", "path": "docs/a.md",  # no content_hash echoed
         "facet_assignments": [raw_assignment("factory_scope", ["domain"])]},
        {"repo": "alpha", "path": "docs/b.md",  # no content_hash echoed
         "facet_assignments": [raw_assignment("document_role", ["process"])]},
    ]}
    records, rejects = cataloger.enforce_contract(raw, shard, job)
    assert rejects == [] and len(records) == 2
    by_path = {r["path"]: r for r in records}
    assert by_path["docs/a.md"]["content_hash"] == "1" * 64
    assert by_path["docs/b.md"]["content_hash"] == "2" * 64


def test_enforce_contract_ignores_a_wrong_echoed_content_hash():
    # Prompt contract v3 regression (live run 29349336374 / child
    # 29349393119): a worker-echoed content_hash carries no integrity and is
    # now an unread key. Even a WRONG echo (the v2 one-dropped-hex-char
    # failure mode, here exaggerated to a fully different value) is accepted,
    # and the persisted record carries the authoritative shard hash, never
    # the echo -- exactly as a fabricated passage_sha256 is ignored.
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    raw = {"entries": [
        {"repo": "alpha", "path": "docs/a.md", "content_hash": "9" * 64,
         "facet_assignments": [raw_assignment("factory_scope", ["domain"])]},
    ]}
    records, rejects = cataloger.enforce_contract(raw, shard, job)
    assert rejects == [] and len(records) == 1
    # The authoritative shard-selection hash, never the "9"*64 echo.
    assert records[0]["content_hash"] == "1" * 64


def test_enforce_contract_rejects_an_out_of_shard_entry():
    # A (repo, path) not in the dispatched shard is still a whole-artifact
    # rejection (unchanged by v3: identity is still matched by (repo, path);
    # only the content_hash echo and its stale-re-read check were removed).
    # The worker no longer echoes content_hash at all.
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    not_dispatched = {"entries": [
        {"repo": "alpha", "path": "docs/not-dispatched.md",
         "facet_assignments": [raw_assignment("factory_scope", ["domain"])]},
    ]}
    records, rejects = cataloger.enforce_contract(not_dispatched, shard, job)
    assert records == [] and any("dispatched shard" in r for r in rejects)


def test_enforce_contract_rejects_malformed_output_shapes():
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    for bad_output in (None, [], "oops", {"entries": "nope"}, {},
                      {"entries": [None]}, {"entries": [{"repo": "alpha"}]}):
        records, rejects = cataloger.enforce_contract(bad_output, shard, job)
        assert records == [] and rejects


def test_enforce_contract_rejects_non_string_repo_and_path_without_raising():
    # Module invariant (cataloger.py docstring): enforce_contract never
    # raises on untrusted worker output. A malformed worker may return
    # structurally wrong — even NON-HASHABLE — repo/path values (a
    # plausible LLM output malformation); each must reject the
    # artifact, never TypeError out of the shard-key/duplicate lookups.
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    for bad in (["alpha"], {"name": "alpha"}, 7, None, "", True):
        for field in ("repo", "path"):
            entry = {"repo": "alpha", "path": "docs/a.md",
                     "content_hash": "1" * 64,
                     "facet_assignments": [
                         raw_assignment("factory_scope", ["domain"])]}
            entry[field] = bad
            records, rejects = cataloger.enforce_contract(
                {"entries": [entry]}, shard, job)
            assert records == []
            assert any("non-empty strings" in r for r in rejects)
    # Repeating the same malformed key exercises the duplicate-entry
    # path too: both entries reject individually, never raise.
    entry = {"repo": ["alpha"], "path": "docs/a.md",
             "content_hash": "1" * 64,
             "facet_assignments": [
                 raw_assignment("factory_scope", ["domain"])]}
    records, rejects = cataloger.enforce_contract(
        {"entries": [entry, dict(entry)]}, shard, job)
    assert records == [] and len(rejects) == 2


def test_enforce_contract_rejects_malformed_capability_refs():
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    raw = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [
            raw_assignment("capability_refs", ["not-a-pair"])],
    }]}
    records, rejects = cataloger.enforce_contract(raw, shard, job)
    assert records == []
    assert any("repository, capability" in r for r in rejects)
    valid = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [raw_assignment(
            "capability_refs",
            [{"repository": "openxFactory",
              "capability": "document-lifecycle"}])],
    }]}
    records, rejects = cataloger.enforce_contract(valid, shard, job)
    assert rejects == [] and len(records) == 1


def test_enforce_contract_rejects_unknown_facet_and_duplicate_assignment():
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    unknown = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [raw_assignment("made_up_facet", ["x"])],
    }]}
    records, rejects = cataloger.enforce_contract(unknown, shard, job)
    assert records == []
    assert any("made_up_facet" in r for r in rejects)

    dup = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [
            raw_assignment("factory_scope", ["domain"]),
            raw_assignment("factory_scope", ["neutral"]),
        ],
    }]}
    records, rejects = cataloger.enforce_contract(dup, shard, job)
    assert records == [] and any("more than once" in r for r in rejects)


def test_enforce_contract_rejects_non_string_topic_and_domain_values():
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    raw = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [raw_assignment("domain_contexts", [123])],
    }]}
    records, rejects = cataloger.enforce_contract(raw, shard, job)
    assert records == [] and any("non-empty" in r for r in rejects)


def test_enforce_contract_requires_a_complete_job_envelope():
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    broken = {"job": {k: v for k, v in job["job"].items()
                      if k != "traceability"}}
    with pytest.raises(ValueError):
        cataloger.enforce_contract({"entries": []}, shard, broken)


def test_registered_tag_ids_merges_every_registry_in_scope():
    # The merged controlled topic-tag vocabulary: every `- id:` declared
    # by any document-tag-registry.yaml under any repository in scope —
    # the same registry files the taxonomy digest pins, parse-identical
    # to the deterministic family's registry read
    # (document_catalog._controlled_tag_ids, namespace registrations
    # included), so the dispatch validator and the family can never
    # disagree about what resolves.
    tags = cataloger.registered_tag_ids(repo_paths_for(WORKSPACE))
    assert tags == frozenset({"alpha", "alpha.widgets", "neutral",
                              "neutral.governance", "neutral.lifecycle"})


def test_enforce_contract_rejects_topic_tags_missing_from_the_registries():
    # Contract scenario "Topic tag is unknown": an unregistered tag may
    # travel only as a PROPOSED tag, never as an effective suggestion.
    registered = cataloger.registered_tag_ids(repo_paths_for(WORKSPACE))
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    invented = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [
            raw_assignment("factory_scope", ["domain"]),
            raw_assignment("topic_tags",
                          ["alpha.widgets", "alpha.invented"]),
        ],
    }]}
    records, rejects = cataloger.enforce_contract(
        invented, shard, job, registered_tags=registered)
    assert records == []  # whole-artifact: the valid facet is not rescued
    assert any("alpha.invented" in r and "resolve" in r for r in rejects)
    # Registered effective values, with the unregistered tag only ever
    # PROPOSED, are accepted.
    proposed = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [raw_assignment(
            "topic_tags", ["alpha.widgets", "neutral.governance"],
            proposed_values=["alpha.brand-new"])],
    }]}
    records, rejects = cataloger.enforce_contract(
        proposed, shard, job, registered_tags=registered)
    assert rejects == [] and len(records) == 1


def test_enforce_contract_rejects_duplicate_entries_for_one_document():
    # Reject-whole contract: two entries for the same (repo, path) in
    # one artifact are conflicting records — they must never survive
    # validation to silently last-write-win at a downstream merge.
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "new",
                              make_entry())
    shard, job = shard_and_job(sel)
    raw = {"entries": [
        {"repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
         "facet_assignments": [raw_assignment("factory_scope", ["domain"])]},
        {"repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
         "facet_assignments": [raw_assignment("factory_scope", ["neutral"])]},
    ]}
    records, rejects = cataloger.enforce_contract(raw, shard, job)
    assert records == []
    assert any("duplicate" in r for r in rejects)


# --- immutable recommendation persistence (T019) -----------------------------

def test_persist_recommendations_writes_an_immutable_record(tmp_path):
    records = [{"repo": "alpha", "path": "docs/a.md",
                "content_hash": "1" * 64,
                "facet_assignments": [
                    facet_assignment("factory_scope", ["domain"])]}]
    path = cataloger.persist_recommendations(
        tmp_path, DAY, "CATJOB-abc123", records)
    assert path == (tmp_path / "health" / "document-catalog"
                    / "recommendations" / DAY_STR / "CATJOB-abc123.yaml")
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["status"] == "record"
    assert doc["kind"] == "xfactory_document_catalog_recommendation"
    assert doc["job_id"] == "CATJOB-abc123"
    assert doc["as_of"] == DAY_STR
    assert doc["entries"] == records
    text = path.read_text(encoding="utf-8")
    assert text == json.dumps(json.loads(text), indent=2,
                              sort_keys=True) + "\n"


def test_persist_recommendations_is_idempotent_and_immutable(tmp_path):
    records = [{"repo": "alpha", "path": "docs/a.md",
                "content_hash": "1" * 64, "facet_assignments": []}]
    path = cataloger.persist_recommendations(tmp_path, DAY, "job-1", records)
    before = path.read_bytes()
    again = cataloger.persist_recommendations(tmp_path, DAY, "job-1", records)
    assert again == path
    assert path.read_bytes() == before
    with pytest.raises(catalog.CatalogError, match="immutable"):
        cataloger.persist_recommendations(
            tmp_path, DAY, "job-1",
            [{"repo": "alpha", "path": "docs/other.md",
              "content_hash": "2" * 64, "facet_assignments": []}])
    assert path.read_bytes() == before  # never rewritten


def test_persist_recommendations_rejects_unsafe_job_ids(tmp_path):
    for bad in ("", "../escape", ".", "..", "a/b", ".hidden"):
        with pytest.raises(ValueError):
            cataloger.persist_recommendations(tmp_path, DAY, bad, [])
    assert not (tmp_path / "health").exists()


def test_persist_recommendations_is_byte_identical_across_worker_order(
        tmp_path):
    # The idempotent-no-op retry guarantee must hold for LOGICALLY
    # identical retries: a worker returning the same records in a
    # different JSON entry (or facet-assignment) order renders the same
    # bytes, never a phantom immutability conflict.
    fs = facet_assignment("factory_scope", ["domain"])
    tt = facet_assignment("topic_tags", ["alpha.widgets"])
    rec_a = {"repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
             "facet_assignments": [fs, tt]}
    rec_a_reordered = dict(rec_a, facet_assignments=[tt, fs])
    rec_b = {"repo": "alpha", "path": "docs/b.md", "content_hash": "2" * 64,
             "facet_assignments": [
                 facet_assignment("document_role", ["process"])]}
    path = cataloger.persist_recommendations(
        tmp_path, DAY, "job-1", [rec_b, rec_a])
    before = path.read_bytes()
    again = cataloger.persist_recommendations(
        tmp_path, DAY, "job-1", [rec_a_reordered, rec_b])
    assert again == path
    assert path.read_bytes() == before
    # Canonical persisted order: entries by (repo, path), assignments by
    # facet — and the caller's records are never mutated to get there.
    doc = json.loads(before.decode("utf-8"))
    assert [e["path"] for e in doc["entries"]] == ["docs/a.md", "docs/b.md"]
    assert [a["facet"] for a in doc["entries"][0]["facet_assignments"]] == \
        ["factory_scope", "topic_tags"]
    assert rec_a_reordered["facet_assignments"][0] is tt


# --- later-snapshot-only merge (T019, catalog.merge_recommendations) --------

def test_merge_recommendations_discards_stale_by_content_hash():
    base = [make_entry(path="docs/a.md", content_hash="1" * 64),
           make_entry(path="docs/b.md", content_hash="2" * 64)]
    stale_record = {
        "repo": "alpha", "path": "docs/a.md",
        "content_hash": "0" * 64,  # does not match the live entry
        "facet_assignments": [facet_assignment("factory_scope", ["domain"])],
    }
    fresh_record = {
        "repo": "alpha", "path": "docs/b.md", "content_hash": "2" * 64,
        "facet_assignments": [facet_assignment("factory_scope", ["neutral"])],
    }
    merged = catalog.merge_recommendations(base, [stale_record, fresh_record])
    by_path = {e["path"]: e for e in merged}
    assert "facet_assignments" not in by_path["docs/a.md"]  # discarded stale
    assert by_path["docs/b.md"]["facet_assignments"][0]["values"] == \
        ["neutral"]
    # Never mutates the base entries passed in.
    assert "facet_assignments" not in base[1]


def test_merge_recommendations_ignores_records_with_no_matching_entry():
    base = [make_entry(path="docs/a.md", content_hash="1" * 64)]
    orphan = {"repo": "alpha", "path": "docs/nonexistent.md",
             "content_hash": "9" * 64,
             "facet_assignments": [facet_assignment(
                 "factory_scope", ["domain"])]}
    merged = catalog.merge_recommendations(base, [orphan])
    assert merged == base  # never invents an entry


def test_merge_recommendations_never_clobbers_an_owner_disposed_facet():
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    reviewed = facet_assignment("factory_scope", ["domain"], state="reviewed")
    reviewed["review"] = {"authority": "alpha authority (Domain Hermes)",
                          "decision": "reviewed", "date": DAY_STR}
    base = [catalog_entry(entry, [reviewed])]
    record = {"repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
             "facet_assignments": [
                 facet_assignment("factory_scope", ["neutral"])]}
    merged = catalog.merge_recommendations(base, [record])
    fs = next(a for a in merged[0]["facet_assignments"]
             if a["facet"] == "factory_scope")
    assert fs["state"] == "reviewed" and fs["values"] == ["domain"]


def test_merge_recommendations_resolves_racing_records_deterministically():
    # Racing recommendation records for the same (entry, facet) resolve
    # by the deterministic precedence rule — newest state_since, then
    # highest confidence, then the canonical rendered assignment — never
    # by caller-supplied list order.
    base = [make_entry(path="docs/a.md", content_hash="1" * 64)]
    older = {"repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
             "facet_assignments": [facet_assignment(
                 "factory_scope", ["domain"], since="2026-07-08",
                 provenance=valid_provenance(confidence=0.95))]}
    newer = {"repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
             "facet_assignments": [facet_assignment(
                 "factory_scope", ["neutral"], since="2026-07-09",
                 provenance=valid_provenance(confidence=0.5))]}
    one = catalog.merge_recommendations(base, [older, newer])
    other = catalog.merge_recommendations(base, [newer, older])
    assert one == other  # caller order never decides the winner
    fs = next(a for a in one[0]["facet_assignments"]
             if a["facet"] == "factory_scope")
    assert fs["values"] == ["neutral"]  # newest state_since wins outright

    # Same day: the higher-confidence suggestion wins, in either order.
    confident = {"repo": "alpha", "path": "docs/a.md",
                 "content_hash": "1" * 64,
                 "facet_assignments": [facet_assignment(
                     "factory_scope", ["cross_domain"], since="2026-07-09",
                     provenance=valid_provenance(confidence=0.9))]}
    one = catalog.merge_recommendations(base, [newer, confident])
    other = catalog.merge_recommendations(base, [confident, newer])
    assert one == other
    fs = next(a for a in one[0]["facet_assignments"]
             if a["facet"] == "factory_scope")
    assert fs["values"] == ["cross_domain"]

    # Full tie on date and confidence: the canonical rendered form is
    # the final, total tie-break — still order-independent.
    tied_a = {"repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
              "facet_assignments": [facet_assignment(
                  "factory_scope", ["domain"], since="2026-07-09",
                  provenance=valid_provenance(confidence=0.9))]}
    tied_b = {"repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
              "facet_assignments": [facet_assignment(
                  "factory_scope", ["neutral"], since="2026-07-09",
                  provenance=valid_provenance(confidence=0.9))]}
    one = catalog.merge_recommendations(base, [tied_a, tied_b])
    other = catalog.merge_recommendations(base, [tied_b, tied_a])
    assert one == other


def test_merge_recommendations_overrides_are_not_yet_implemented():
    base = [make_entry()]
    with pytest.raises(NotImplementedError):
        catalog.merge_recommendations(base, [], overrides=[{"anything": True}])
    assert catalog.merge_recommendations(base, [], overrides=None) == base
    assert catalog.merge_recommendations(base, [], overrides=[]) == base


def test_merge_recommendations_rejects_duplicate_base_entries():
    dup = [make_entry(), make_entry()]
    with pytest.raises(ValueError, match="duplicate"):
        catalog.merge_recommendations(dup, [])


def test_merge_recommendations_lands_only_in_a_later_immutable_snapshot(
        tmp_path):
    # Data-model.md "Catalog snapshot": "merge writes a NEW snapshot,
    # never edits one." Uses the real fixture workspace + real
    # write_snapshot/run_id machinery, exactly as a later nightly run
    # merging an asynchronously-arrived recommendation would.
    root = tmp_path / "agg"
    inv_one = extended_inventory()
    alpha_one = [e for e in catalog.mechanical_entries(inv_one)
                if e["repo"] == "alpha"]
    rid_one = catalog.run_id(inv_one, TAXONOMY)
    path_one = catalog.write_snapshot(
        root, DAY, rid_one, "alpha", alpha_one, TAXONOMY)
    before = path_one.read_bytes()

    target = next(e for e in alpha_one if e["path"] == "docs/widget-overview.md")
    record = {"repo": "alpha", "path": target["path"],
             "content_hash": target["content_hash"],
             "facet_assignments": [
                 facet_assignment("factory_scope", ["domain"])]}

    # A later nightly run: fresh pinned revisions, zero content change.
    inv_two = extended_inventory(WORKSPACE, LATER_HEADS)
    alpha_two = [e for e in catalog.mechanical_entries(inv_two)
                if e["repo"] == "alpha"]
    merged = catalog.merge_recommendations(alpha_two, [record])
    rid_two = catalog.run_id(inv_two, TAXONOMY)
    assert rid_two != rid_one
    path_two = catalog.write_snapshot(
        root, DAY, rid_two, "alpha", merged, TAXONOMY)

    # The prior immutable snapshot is byte-for-byte untouched...
    assert path_one.read_bytes() == before
    old_doc = json.loads(path_one.read_text(encoding="utf-8"))
    assert all("facet_assignments" not in e for e in old_doc["entries"])
    # ...and the classification appears only in the new one.
    new_doc = json.loads(path_two.read_text(encoding="utf-8"))
    new_target = next(e for e in new_doc["entries"]
                      if e["path"] == target["path"])
    assert new_target["facet_assignments"][0]["values"] == ["domain"]

    # Forcing the merged content under the OLD run id is refused — a
    # merge never rewrites an existing snapshot.
    with pytest.raises(catalog.CatalogError, match="immutable"):
        catalog.write_snapshot(root, DAY, rid_one, "alpha", merged, TAXONOMY)
    assert path_one.read_bytes() == before


# --- explicit pending marking for never-assigned facets ----------------------

def test_pending_records_mark_only_never_assigned_facets():
    entry = make_entry(content_hash="1" * 64)
    cat = [catalog_entry(entry, [
        facet_assignment("factory_scope", ["domain"]),
        facet_assignment("document_role", [], state="pending",
                         since="2026-07-01")])]
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "pending",
                              dict(entry))
    records = cataloger.pending_records([sel], cat, DAY)
    assert len(records) == 1
    record = records[0]
    assert (record["repo"], record["path"], record["content_hash"]) == \
        ("alpha", "docs/a.md", "1" * 64)
    # The suggested facet is untouched (only invalidate — feature task
    # T022 — may return it to pending) and the already-pending facet
    # keeps its original aging clock (never re-marked, or every run
    # would reset it); only the four never-assigned facets gain
    # explicit pending state, its clock starting at the dispatch date.
    assert [(a["facet"], a["state"], a["state_since"], a["values"])
            for a in record["facet_assignments"]] == [
        ("capability_refs", "pending", DAY_STR, []),
        ("domain_contexts", "pending", DAY_STR, []),
        ("sensitivity_signal", "pending", DAY_STR, []),
        ("topic_tags", "pending", DAY_STR, []),
    ]


def test_pending_records_are_empty_for_fully_assigned_documents():
    entry = make_entry(content_hash="1" * 64)
    cat = [catalog_entry(entry, [
        facet_assignment(f, ["x"]) for f in cataloger.FACET_NAMES])]
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "changed",
                              dict(entry))
    assert cataloger.pending_records([sel], cat, DAY) == []


def test_pending_records_order_is_deterministic():
    a = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "baseline",
                            make_entry(path="docs/a.md"))
    b = cataloger.Selection("alpha", "docs/b.md", "2" * 64, "baseline",
                            make_entry(path="docs/b.md",
                                       content_hash="2" * 64))
    one = cataloger.pending_records([a, b], [], DAY)
    other = cataloger.pending_records([b, a], [], DAY)
    assert one == other  # caller order never matters
    assert [r["path"] for r in one] == ["docs/a.md", "docs/b.md"]


def test_pending_records_never_mislabel_a_protected_selection_pending():
    # Adversarial-recheck regression (contract "Host is not authorized
    # for protected content"): pending_records used to trust its caller
    # to pre-filter protected selections and emitted a plain `pending`
    # record carrying the real path — exactly what
    # persist_recommendations would write into an immutable artifact.
    # Defense in depth: the function applies the handling policy itself.
    sel = cataloger.Selection(
        "alpha", "docs/protected-roster.md", "9" * 64, "baseline",
        make_entry(path="docs/protected-roster.md", content_hash="9" * 64,
                   handling="protected"))
    records = cataloger.pending_records([sel], [], DAY)
    assert len(records) == 1
    record = records[0]
    locator = catalog.opaque_locator("alpha", "docs/protected-roster.md")
    # The US1 opaque locator replaces the path — no identifying
    # metadata is carried at all.
    assert "path" not in record
    assert record["document_ref"] == locator["document_ref"]
    assert record["path_sha256"] == locator["path_sha256"]
    assert record["content_hash"] == "9" * 64
    # Every facet is policy_blocked — never ordinary pending — and the
    # deterministic opaque blocker reference lives on the entry-level
    # dispatch_policy (handling-gate decision), NEVER on a facet_assignment
    # (the snapshot facet_assignment shape forbids a blocker field).
    assert [a["facet"] for a in record["facet_assignments"]] == \
        sorted(cataloger.FACET_NAMES)
    assert all("blocker_ref" not in a for a in record["facet_assignments"])
    assert all(a["state"] == "policy_blocked" and a["values"] == []
               and a["state_since"] == DAY_STR
               for a in record["facet_assignments"])
    policy = record["dispatch_policy"]
    assert policy["state"] == "blocked"
    assert policy["blocked_reference"]["blocker_ref"] == \
        cataloger.blocker_reference(locator["document_ref"],
                                    cataloger.PROTECTED_HANDLING_BLOCKER)
    assert policy["blocked_reference"]["reason_code"] == \
        cataloger.PROTECTED_HANDLING_REASON_CODE
    # The blocker reference is the 64-char lowercase hex the contract
    # fixes (blocker_reference.blocker_ref pattern ^[0-9a-f]{64}$).
    blk = policy["blocked_reference"]["blocker_ref"]
    assert len(blk) == 64 and all(c in "0123456789abcdef" for c in blk)
    # SC-007 leakage sweep over the exact bytes this record would
    # persist: no real path, and no `pending` state anywhere.
    rendered = catalog.render(records)
    assert "protected-roster" not in rendered
    assert "pending" not in rendered
    # Deterministic: a rerun produces the identical record.
    assert cataloger.pending_records([sel], [], DAY) == records


def test_pending_records_never_remark_an_already_blocked_facet():
    # Carry-forward parity with pending: a facet already recorded
    # policy_blocked under the opaque locator keeps its original
    # state_since — re-marking would churn the record every run.
    sel = cataloger.Selection(
        "alpha", "docs/protected-roster.md", "9" * 64, "new",
        make_entry(path="docs/protected-roster.md", content_hash="9" * 64,
                   handling="protected"))
    locator = catalog.opaque_locator("alpha", "docs/protected-roster.md")
    blocked_entry = {
        "repo": "alpha", "document_ref": locator["document_ref"],
        "path_sha256": locator["path_sha256"], "content_hash": "9" * 64,
        "dispatch_policy": cataloger.blocked_dispatch_policy(
            locator["document_ref"]),
        "facet_assignments": [
            {"facet": facet, "values": [], "proposed_values": [],
             "state": "policy_blocked", "state_since": "2026-07-01",
             "transitions": [], "review": None}
            for facet in cataloger.FACET_NAMES]}
    assert cataloger.pending_records([sel], [blocked_entry], DAY) == []


def test_offline_skip_path_records_protected_selection_policy_blocked(
        tmp_path):
    # SC-007 end to end over the offline/skip path (contract "Cataloger
    # is offline" x "Host is not authorized for protected content"):
    # the skip path operates on raw select() output — no shard is ever
    # built, so build_shards' protected filter never runs — and
    # pending_records is the last line of defense before persistence.
    root = tmp_path / "agg"
    inv = extended_inventory()
    # The policy-aware mechanical catalog (US1): the same handling-gate
    # policy that bars dispatch prohibits path persistence.
    entries = catalog.mechanical_entries(
        inv, path_prohibited=cataloger.is_protected)
    for repo in ("alpha", "openxFactory"):
        catalog_baseline.run_shard(
            root, repo, 1000, DAY,
            [e for e in entries if e["repo"] == repo])
    assert catalog_baseline.merge_baseline(
        root, DAY, ("alpha", "openxFactory")) is not None

    alpha_inv = [e for e in inv if e["repo"] == "alpha"]
    selections = cataloger.select(alpha_inv, None, [])
    protected = [s for s in selections if cataloger.is_protected(s.entry)]
    assert [s.path for s in protected] == ["docs/protected-roster.md"]
    # Worker offline: the caller records a skip and merges
    # pending_records alone — no shard, no dispatch, no shard filter.
    records = cataloger.pending_records(selections, [], DAY)
    artifact = cataloger.persist_recommendations(
        root, DAY, "CATJOB-offline-skip", records)

    ref = catalog.opaque_locator(
        "alpha", "docs/protected-roster.md")["document_ref"]
    alpha_entries = [e for e in entries if e["repo"] == "alpha"]
    merged = catalog.merge_recommendations(alpha_entries, records)
    catalog.write_snapshot(root, DAY, "offline-skip-flow", "alpha",
                           merged, TAXONOMY)

    # The protected document's facets land policy_blocked under the
    # opaque locator (never silently classified, never pending)...
    blocked = next(e for e in merged if e.get("document_ref") == ref)
    assert "path" not in blocked
    assert {(a["facet"], a["state"]) for a in blocked["facet_assignments"]} \
        == {(f, "policy_blocked") for f in cataloger.FACET_NAMES}
    # The blocker rides on the entry-level dispatch_policy (handling-gate
    # decision), never on a facet_assignment (schema-forbidden there):
    # the merge carried the decision from the pending_records marker.
    assert all("blocker_ref" not in a for a in blocked["facet_assignments"])
    assert blocked["dispatch_policy"]["state"] == "blocked"
    assert blocked["dispatch_policy"]["blocked_reference"]["blocker_ref"] == \
        cataloger.blocker_reference(ref, cataloger.PROTECTED_HANDLING_BLOCKER)
    # ...while every unprotected selection keeps the ordinary explicit
    # pending marking.
    plain = [e for e in merged if "path" in e]
    assert plain
    for entry in plain:
        assert all(a["state"] == "pending"
                   for a in entry.get("facet_assignments", []))

    # SC-007 leakage sweep over EVERY persisted catalog artifact
    # (baseline shards, merged baseline, recommendation record,
    # snapshot): the protected path and content never appear; the
    # opaque reference does.
    artifacts = [p for p in sorted(root.rglob("*")) if p.is_file()]
    assert artifact in artifacts
    for path in artifacts:
        text = path.read_text(encoding="utf-8")
        assert "protected-roster" not in text, path
        assert "PROTECTED-ROSTER-ALPHA" not in text, path
    assert ref in artifact.read_text(encoding="utf-8")

    # Downstream aging (the recheck's mislabeling consequence): 37 days
    # on, every unprotected pending facet warns; the policy_blocked
    # document never enters the 30/90-day clocks at all.
    repo_paths = repo_paths_for(WORKSPACE)
    ctx = Context(
        repo_paths=repo_paths, docs=docs_for(repo_paths),
        capabilities={n: corpus.spec_capabilities(p)
                     for n, p in repo_paths.items()},
        change_ids={n: corpus.change_ids(p)
                   for n, p in repo_paths.items()},
        git=FakeGit(heads=HEADS), thresholds=dict(DEFAULT_THRESHOLDS),
        as_of=date(2026, 8, 15), agg_root=None, catalog_root=root)
    findings = FAMILIES["document-catalog"](ctx)
    aging = [f for f in findings if f.rule.startswith("[pending-aging]")]
    expected = sorted(
        (sel.path,
         f"[pending-aging] {facet} facet pending 37 days (warning at 30)")
        for sel in selections if not cataloger.is_protected(sel.entry)
        for facet in cataloger.FACET_NAMES)
    assert sorted((f.path, f.rule) for f in aging) == expected
    assert not any(f.path == ref for f in aging)


# The snapshot schema's #/$defs/facet_assignment is
# `additionalProperties: false` with exactly these keys — a `blocker_ref`
# here is schema-invalid (review finding 1).
_FACET_ASSIGNMENT_KEYS = {
    "facet", "values", "proposed_values", "state", "state_since",
    "provenance", "transitions", "review"}


def test_protected_document_snapshot_conforms_to_facet_assignment_shape(
        tmp_path):
    # Review finding 1: a never-dispatched protected document's blocker
    # must live on the entry-level dispatch_policy (handling-gate
    # decision), NEVER on a facet_assignment — the merged snapshot's
    # facet_assignment shape is additionalProperties:false and lists no
    # blocker field, so a `blocker_ref` there yields a schema-invalid
    # snapshot. This drives the full pending_records ->
    # merge_recommendations -> write_snapshot -> load_snapshot path and
    # structurally validates the persisted entry.
    root = tmp_path / "agg"
    inv = extended_inventory()
    entries = catalog.mechanical_entries(
        inv, path_prohibited=cataloger.is_protected)
    alpha_inv = [e for e in inv if e["repo"] == "alpha"]
    selections = cataloger.select(alpha_inv, None, [])
    records = cataloger.pending_records(selections, [], DAY)
    alpha_entries = [e for e in entries if e["repo"] == "alpha"]
    merged = catalog.merge_recommendations(alpha_entries, records)
    catalog.write_snapshot(root, DAY, "conformance-run", "alpha", merged,
                           TAXONOMY)

    doc = catalog.load_snapshot(root, run_id="conformance-run")["repos"]["alpha"]
    ref = catalog.opaque_locator(
        "alpha", "docs/protected-roster.md")["document_ref"]
    blocked = next(e for e in doc["entries"] if e.get("document_ref") == ref)
    # Every facet_assignment carries ONLY schema-recognized keys — no
    # blocker_ref anywhere — and stays policy_blocked.
    for a in blocked["facet_assignments"]:
        unexpected = set(a) - _FACET_ASSIGNMENT_KEYS
        assert not unexpected, unexpected
        assert a["state"] == "policy_blocked"
    # The blocker lives on the entry-level dispatch_policy: state blocked,
    # a source_policy_ref, a 64-hex blocker_ref, and (blocked => forbidden)
    # no host_attestation_ref.
    policy = blocked["dispatch_policy"]
    assert policy["state"] == "blocked"
    assert isinstance(policy["source_policy_ref"], str) \
        and policy["source_policy_ref"]
    assert "host_attestation_ref" not in policy
    br = policy["blocked_reference"]["blocker_ref"]
    assert len(br) == 64 and all(c in "0123456789abcdef" for c in br)
    assert policy["blocked_reference"]["reason_code"] == \
        cataloger.PROTECTED_HANDLING_REASON_CODE
    # No identifying metadata leaks into the persisted snapshot bytes.
    rendered = catalog.render(doc)
    assert "protected-roster" not in rendered
    assert "PROTECTED-ROSTER-ALPHA" not in rendered


def test_partial_classification_reaches_explicit_pending_and_stays_selectable():
    # Review finding: cataloger-prompt.md sanctions partial coverage
    # ("as many of the six controlled facets as the content supports"),
    # so a validated artifact may resolve only SOME facets — the
    # uncovered ones must not silently vanish from reselection. The
    # dispatch flow merges pending_records alongside the validated
    # records, landing every uncovered facet in an explicit pending
    # state that select() keeps re-selecting.
    entry = make_entry(content_hash="1" * 64)
    sel = cataloger.Selection("alpha", "docs/a.md", "1" * 64, "baseline",
                              dict(entry))
    shard, job = shard_and_job(sel)
    raw = {"entries": [{
        "repo": "alpha", "path": "docs/a.md", "content_hash": "1" * 64,
        "facet_assignments": [raw_assignment("factory_scope", ["domain"])],
    }]}
    validated, rejects = cataloger.enforce_contract(raw, shard, job)
    assert rejects == []
    pending = cataloger.pending_records([sel], [], DAY)
    merged = catalog.merge_recommendations([entry], validated + pending)
    facets = {a["facet"]: a for a in merged[0]["facet_assignments"]}
    assert set(facets) == set(cataloger.FACET_NAMES)
    # The covered facet is suggested — a same-dispatch validated
    # suggestion always beats the pending marker (equal state_since,
    # higher precedence by provenance confidence)...
    assert facets["factory_scope"]["state"] == "suggested"
    assert facets["factory_scope"]["values"] == ["domain"]
    # ...and every uncovered facet is explicitly pending with the
    # dispatch date starting its aging clock.
    for facet in set(cataloger.FACET_NAMES) - {"factory_scope"}:
        assert facets[facet]["state"] == "pending"
        assert facets[facet]["state_since"] == DAY_STR
        assert facets[facet]["values"] == []
    # Reselection: the same unchanged corpus now re-selects the
    # document as pending instead of treating it as fully classified.
    selections = cataloger.select([entry], [entry], merged)
    assert [(s.repo, s.path, s.reason) for s in selections] == \
        [("alpha", "docs/a.md", "pending")]


def test_pending_marked_facets_age_into_the_family_pending_aging_findings(
        tmp_path):
    # Contract scenario "Pending state crosses an aging boundary" now
    # reaches facets a worker legitimately left unassigned: once the
    # dispatch flow marks them pending, the deterministic family's
    # 30/90-day thresholds fire from the recorded state_since
    # (research D8) — over the real baseline/snapshot/family machinery.
    root = tmp_path / "agg"
    inv = extended_inventory()
    for repo in ("alpha", "openxFactory"):
        catalog_baseline.run_shard(
            root, repo, 1000, DAY,
            [e for e in catalog.mechanical_entries(inv)
             if e["repo"] == repo])
    assert catalog_baseline.merge_baseline(
        root, DAY, ("alpha", "openxFactory")) is not None

    alpha_inv = [e for e in inv if e["repo"] == "alpha"]
    selections = cataloger.select(alpha_inv, None, [])
    shard = cataloger.build_shards(selections, budget=1000)[0]
    dispatched = list(shard.selections)
    job = job_for(shard, taxonomy=TAXONOMY["digest"])
    target = dispatched[0]
    raw = {"entries": [{
        "repo": target.repo, "path": target.path,
        "content_hash": target.content_hash,
        "facet_assignments": [raw_assignment("factory_scope", ["domain"])],
    }]}
    validated, rejects = cataloger.enforce_contract(raw, shard, job)
    assert rejects == []
    pending = cataloger.pending_records(dispatched, [], DAY)
    alpha_entries = [e for e in catalog.mechanical_entries(inv)
                     if e["repo"] == "alpha"]
    merged = catalog.merge_recommendations(alpha_entries,
                                           validated + pending)
    catalog.write_snapshot(root, DAY, "pending-marking-flow", "alpha",
                           merged, TAXONOMY)

    # 37 days after the dispatch date every still-pending facet warns
    # (>= 30, < 90); the facet the worker resolved never ages; the
    # protected roster was never dispatched, so it is policy territory,
    # not pending. The clean fixture is otherwise finding-free.
    repo_paths = repo_paths_for(WORKSPACE)
    ctx = Context(
        repo_paths=repo_paths, docs=docs_for(repo_paths),
        capabilities={n: corpus.spec_capabilities(p)
                     for n, p in repo_paths.items()},
        change_ids={n: corpus.change_ids(p)
                   for n, p in repo_paths.items()},
        git=FakeGit(heads=HEADS), thresholds=dict(DEFAULT_THRESHOLDS),
        as_of=date(2026, 8, 15), agg_root=None, catalog_root=root)
    findings = FAMILIES["document-catalog"](ctx)
    assert findings and all(f.severity == WARNING for f in findings)
    expected = sorted(
        (sel.path,
         f"[pending-aging] {facet} facet pending 37 days (warning at 30)")
        for sel in dispatched for facet in cataloger.FACET_NAMES
        if not (sel.path == target.path and facet == "factory_scope"))
    assert sorted((f.path, f.rule) for f in findings) == expected


# --- offline / partial / invalid worker isolation (T020) --------------------

def _dispatch_and_isolate(invoke, shard, job):
    """Test-local emulation of the orchestration isolation contract
    (``semantic.run_sweep`` precedent): a worker failure of any kind —
    offline, partial, or invalid output — never raises past this
    boundary; it degrades to an empty result with a recorded reason,
    and nothing downstream (persistence, mechanical snapshots) is ever
    reached."""
    try:
        raw = invoke()
    except Exception as exc:  # worker offline or crashed
        return [], f"worker unavailable: {exc}"
    records, rejects = cataloger.enforce_contract(raw, shard, job)
    if rejects:
        return [], f"worker output rejected: {rejects}"
    return records, None


def test_worker_offline_partial_or_invalid_output_never_disturbs_mechanical_results(
        tmp_path):
    root = tmp_path / "agg"
    inv = extended_inventory()
    alpha = [e for e in catalog.mechanical_entries(inv) if e["repo"] == "alpha"]
    rid = catalog.run_id(inv, TAXONOMY)
    snapshot_path = catalog.write_snapshot(
        root, DAY, rid, "alpha", alpha, TAXONOMY)
    before = snapshot_path.read_bytes()

    target = next(e for e in alpha if e["path"] == "docs/widget-overview.md")
    sel = cataloger.Selection(
        "alpha", target["path"], target["content_hash"], "new", target)
    shard = cataloger.build_shards([sel], budget=10)[0]
    job = job_for(shard, taxonomy=TAXONOMY["digest"])

    def offline():
        raise RuntimeError("Cloud PC host unreachable")

    def invalid():
        return {"entries": "not-a-list"}

    good_entry = {"repo": "alpha", "path": target["path"],
                 "content_hash": target["content_hash"],
                 "facet_assignments": [
                     raw_assignment("factory_scope", ["domain"])]}
    bad_entry = {"repo": "alpha", "path": target["path"],
                "content_hash": target["content_hash"],
                "facet_assignments": [
                    raw_assignment("factory_scope", ["not-a-scope"])]}

    def partial():
        # Whole-artifact rejection: one invalid entry voids the whole
        # dispatch even though a valid entry was also present.
        return {"entries": [good_entry, bad_entry]}

    for invoke in (offline, invalid, partial):
        records, skip_reason = _dispatch_and_isolate(invoke, shard, job)
        assert records == []
        assert skip_reason is not None
        # The mechanical snapshot is untouched no matter what...
        assert snapshot_path.read_bytes() == before
        # ...and nothing was ever persisted from the failed dispatch.
        recs_dir = root / "health" / "document-catalog" / "recommendations"
        assert not recs_dir.exists()


# --- owner dispositions (T021) ------------------------------------------------

# The owner-override artifact's required fields, mirrored from the merged
# openxFactory arbiter schema xfactory-document-tag-overrides.schema.yaml
# (#/$defs/override.required, change task 2.2). apply_dispositions reads
# these exact names; the structural test below pins the alignment so a
# future rename on either side fails loudly (reconciliation item 6).
OVERRIDE_SCHEMA_REQUIRED = frozenset({
    "repo", "source_content_hash", "facet", "decision", "actor",
    "occurred_at", "rationale", "evidence_refs"})


def override_artifact(repo, path=None, document_ref=None, path_sha256=None,
                      source_content_hash="1" * 64, facet="factory_scope",
                      decision="reviewed", values=None, actor=None,
                      occurred_at=DAY_DT, rationale="owner disposition",
                      evidence_refs=None, **extra):
    """A raw owner-override artifact matching the arbiter schema
    ``xfactory-document-tag-overrides.schema.yaml`` (#/$defs/override): the
    exact shape ``apply_dispositions`` reads from
    ``catalog/document-tag-overrides.yaml``. ``actor`` defaults to the
    OWNING authority for ``repo`` (the same convention
    ``cataloger._disposition_authority`` computes) so tests only override it
    to exercise the invalid-standing path. ``occurred_at`` is a full RFC
    3339 date-time (schema ``occurred_at: {format: date-time}``); the merged
    facet's ``state_since`` derives its bare-date portion."""
    artifact = {
        "repo": repo, "source_content_hash": source_content_hash,
        "facet": facet, "decision": decision,
        "actor": actor if actor is not None
        else (NEUTRAL_DISPOSER if repo == NEUTRAL_REPO
              else f"{repo} authority (Domain Hermes)"),
        "occurred_at": occurred_at,
        "rationale": rationale,
        "evidence_refs": list(evidence_refs) if evidence_refs is not None
        else [],
    }
    if path is not None:
        artifact["path"] = path
    if document_ref is not None:
        artifact["document_ref"] = document_ref
        artifact["path_sha256"] = path_sha256
    if values is not None:
        artifact["values"] = values
    artifact.update(extra)
    return artifact


def test_override_artifact_field_names_match_the_arbiter_schema():
    # Reconciliation item 6: apply_dispositions' override-artifact field
    # names had no arbiter until the merged
    # xfactory-document-tag-overrides.schema.yaml became one. The fixture
    # the disposition tests feed apply_dispositions must carry EXACTLY the
    # schema's required field names (no legacy authority/date/content_hash
    # aliases), and apply_dispositions must accept it end to end under
    # those names — producing a review block in the snapshot schema's
    # #/$defs/review shape.
    artifact = override_artifact(
        "alpha", path="docs/a.md", decision="overridden", values=["neutral"])
    assert OVERRIDE_SCHEMA_REQUIRED <= set(artifact)
    assert not ({"authority", "date", "content_hash"} & set(artifact))

    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    base = [catalog_entry(entry, [facet_assignment(
        "factory_scope", ["domain"])])]
    result = cataloger.apply_dispositions(base, [artifact])
    fs = result[0]["facet_assignments"][0]
    assert fs["state"] == "overridden" and fs["values"] == ["neutral"]
    # The merged review block carries exactly the snapshot schema's
    # #/$defs/review required fields (the override's `actor` -> `authority`).
    assert set(fs["review"]) == {
        "decision", "authority", "occurred_at", "rationale", "evidence_refs"}
    assert fs["review"]["authority"] == "alpha authority (Domain Hermes)"

    # A schema-invalid override (missing the required rationale) is
    # discarded, prior state retained — the same silent-discard contract
    # as every other failed gate.
    no_rationale = override_artifact(
        "alpha", path="docs/a.md", decision="reviewed")
    del no_rationale["rationale"]
    assert cataloger.apply_dispositions(base, [no_rationale]) == base


def test_apply_dispositions_accepts_a_valid_reviewed_decision():
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    suggested = facet_assignment("factory_scope", ["domain"])
    base = [catalog_entry(entry, [suggested])]
    artifact = override_artifact("alpha", path="docs/a.md", decision="reviewed")

    result = cataloger.apply_dispositions(base, [artifact])

    fs = result[0]["facet_assignments"][0]
    assert fs["state"] == "reviewed"
    assert fs["values"] == ["domain"]  # reviewed affirms the existing value
    assert fs["state_since"] == DAY_STR  # bare-date portion of occurred_at
    assert fs["review"] == {"decision": "reviewed",
                            "authority": "alpha authority (Domain Hermes)",
                            "occurred_at": DAY_DT,
                            "rationale": "owner disposition",
                            "evidence_refs": []}
    assert fs["provenance"] == suggested["provenance"]  # evidence unchanged
    assert fs["transitions"] == [{"from": "suggested", "to": "reviewed",
                                  "occurred_at": DAY_DT,
                                  "evidence_refs": []}]
    # Never mutates the caller's inputs.
    assert base[0]["facet_assignments"][0]["state"] == "suggested"


def test_apply_dispositions_accepts_overridden_with_replacement_values():
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    suggested = facet_assignment("factory_scope", ["domain"])
    base = [catalog_entry(entry, [suggested])]
    artifact = override_artifact("alpha", path="docs/a.md",
                                 decision="overridden", values=["neutral"])

    result = cataloger.apply_dispositions(base, [artifact])

    fs = result[0]["facet_assignments"][0]
    assert fs["state"] == "overridden" and fs["values"] == ["neutral"]
    assert fs["review"]["decision"] == "overridden"
    assert fs["provenance"] == suggested["provenance"]


def test_apply_dispositions_rejects_overridden_without_replacement_values():
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    base = [catalog_entry(entry, [facet_assignment(
        "factory_scope", ["domain"])])]
    # No `values` supplied: overridden MUST name replacement values.
    artifact = override_artifact("alpha", path="docs/a.md",
                                 decision="overridden")
    assert cataloger.apply_dispositions(base, [artifact]) == base


def test_apply_dispositions_rejects_unauthorized_authority():
    # Contract scenario "Unauthorized override is supplied": ignored,
    # prior state retained.
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    base = [catalog_entry(entry, [facet_assignment(
        "factory_scope", ["domain"])])]
    artifact = override_artifact(
        "alpha", path="docs/a.md", decision="overridden", values=["neutral"],
        actor="beta authority (Domain Hermes)")
    assert cataloger.apply_dispositions(base, [artifact]) == base


def test_apply_dispositions_neutral_repo_uses_the_ratify_gate():
    entry = make_entry(repo="openxFactory", path="docs/a.md",
                       content_hash="1" * 64)
    base = [catalog_entry(entry, [facet_assignment(
        "factory_scope", ["neutral"])])]
    wrong = override_artifact(
        "openxFactory", path="docs/a.md", decision="reviewed",
        actor="alpha authority (Domain Hermes)")
    assert cataloger.apply_dispositions(base, [wrong]) == base

    right = override_artifact("openxFactory", path="docs/a.md",
                              decision="reviewed")
    result = cataloger.apply_dispositions(base, [right])
    fs = result[0]["facet_assignments"][0]
    assert fs["state"] == "reviewed"
    assert fs["review"]["authority"] == "openxFactory ratify gate"


def test_apply_dispositions_discards_a_stale_content_hash():
    # Contract scenario "Source content changes after review": an
    # override recorded against superseded content must never apply.
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    base = [catalog_entry(entry, [facet_assignment(
        "factory_scope", ["domain"])])]
    artifact = override_artifact("alpha", path="docs/a.md",
                                 source_content_hash="9" * 64,
                                 decision="reviewed")
    assert cataloger.apply_dispositions(base, [artifact]) == base


def test_apply_dispositions_discards_when_facet_was_never_assigned():
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    base = [catalog_entry(entry)]  # never classified at all
    artifact = override_artifact("alpha", path="docs/a.md", decision="reviewed")
    assert cataloger.apply_dispositions(base, [artifact]) == base
    # A record that never resolves to an unambiguous locator is
    # likewise discarded, never guessed at.
    ambiguous = override_artifact("alpha", path="docs/a.md", decision="reviewed")
    ambiguous["document_ref"] = "x" * 64
    ambiguous["path_sha256"] = "y" * 64
    assert cataloger.apply_dispositions(base, [ambiguous]) == base


def test_apply_dispositions_never_mutates_inputs_and_rejects_duplicate_base_keys():
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    suggested = facet_assignment("factory_scope", ["domain"])
    base = [catalog_entry(entry, [suggested])]
    artifact = override_artifact("alpha", path="docs/a.md", decision="reviewed")
    before_base = json.loads(json.dumps(base))
    before_artifact = json.loads(json.dumps(artifact))

    result = cataloger.apply_dispositions(base, [artifact])

    assert base == before_base  # snapshot input untouched
    assert artifact == before_artifact  # override input untouched
    assert result is not base
    assert result[0] is not base[0]

    dup = [make_entry(), make_entry()]
    with pytest.raises(ValueError, match="duplicate"):
        cataloger.apply_dispositions(dup, [])


def test_apply_dispositions_protected_entry_never_leaks():
    # SC-007: applying an (authorized) disposition to a protected,
    # opaque-locatored entry must never introduce the real path or
    # content into the result, alongside an ordinary disposition
    # applying normally in the same call.
    locator = catalog.opaque_locator("alpha", "docs/protected-roster.md")
    blocked_entry = {
        "repo": "alpha", "document_ref": locator["document_ref"],
        "path_sha256": locator["path_sha256"], "content_hash": "9" * 64,
        "dispatch_policy": cataloger.blocked_dispatch_policy(
            locator["document_ref"]),
        "facet_assignments": [{
            "facet": "factory_scope", "values": [], "proposed_values": [],
            "state": "policy_blocked", "state_since": "2026-07-01",
            "transitions": [], "review": None,
        }],
    }
    ordinary = catalog_entry(make_entry(path="docs/a.md", content_hash="1" * 64),
                             [facet_assignment("factory_scope", ["domain"])])
    base = [blocked_entry, ordinary]

    ordinary_override = override_artifact("alpha", path="docs/a.md",
                                          decision="reviewed")
    protected_override = override_artifact(
        "alpha", document_ref=locator["document_ref"],
        path_sha256=locator["path_sha256"], source_content_hash="9" * 64,
        decision="overridden", values=["domain"])

    result = cataloger.apply_dispositions(
        base, [ordinary_override, protected_override])

    rendered = catalog.render(result)
    assert "protected-roster" not in rendered
    assert "PROTECTED-ROSTER-ALPHA" not in rendered
    blocked_result = next(
        e for e in result if e.get("document_ref") == locator["document_ref"])
    assert "path" not in blocked_result
    assert blocked_result["path_sha256"] == locator["path_sha256"]
    # The ordinary disposition applied normally in the same call.
    ordinary_result = next(e for e in result if e.get("path") == "docs/a.md")
    assert ordinary_result["facet_assignments"][0]["state"] == "reviewed"


# --- content/taxonomy/prompt invalidation (T022) ------------------------------

def test_invalidate_content_change_returns_suggested_facet_to_pending():
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    suggested = facet_assignment("factory_scope", ["domain"])
    cat_entries = [catalog_entry(entry, [suggested])]
    changed_inv = [make_entry(path="docs/a.md", content_hash="9" * 64)]

    result = cataloger.invalidate(cat_entries, changed_inv, DAY)

    fs = result[0]["facet_assignments"][0]
    assert fs["state"] == "pending"
    assert fs["values"] == []
    assert "provenance" not in fs  # pending carries no classifier output
    assert fs["review"] is None
    assert fs["state_since"] == DAY_STR  # reset for the new semantic input
    assert fs["transitions"] == [{"from": "suggested", "to": "pending",
                                  "occurred_at": DAY_DT,
                                  "evidence_refs": []}]
    # Never mutates the caller's inputs.
    assert cat_entries[0]["facet_assignments"][0]["state"] == "suggested"
    assert changed_inv[0]["content_hash"] == "9" * 64


def test_invalidate_records_pending_to_pending_event_when_already_pending():
    # Contract scenario "Pending input changes again".
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    pending = facet_assignment("document_role", [], state="pending",
                               since="2026-07-01")
    cat_entries = [catalog_entry(entry, [pending])]
    changed_inv = [make_entry(path="docs/a.md", content_hash="9" * 64)]

    result = cataloger.invalidate(cat_entries, changed_inv, DAY)

    fs = result[0]["facet_assignments"][0]
    assert fs["state"] == "pending"
    assert fs["state_since"] == DAY_STR  # reset, never carried forward here
    assert fs["transitions"] == [{"from": "pending", "to": "pending",
                                  "occurred_at": DAY_DT,
                                  "evidence_refs": []}]


def test_invalidate_is_a_noop_when_nothing_changed():
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    suggested = facet_assignment("factory_scope", ["domain"], since="2026-07-01")
    cat_entries = [catalog_entry(entry, [suggested])]
    unchanged_inv = [make_entry(path="docs/a.md", content_hash="1" * 64)]

    result = cataloger.invalidate(cat_entries, unchanged_inv, DAY)

    assert result == cat_entries
    # state_since carries forward: it is never touched on a no-op.
    assert result[0]["facet_assignments"][0]["state_since"] == "2026-07-01"


def test_invalidate_taxonomy_version_change_invalidates_only_that_facet():
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    stale = facet_assignment(
        "factory_scope", ["domain"],
        provenance=valid_provenance(taxonomy_sha256="old" * 16))
    fresh = facet_assignment("document_role", ["process"])
    cat_entries = [catalog_entry(entry, [stale, fresh])]
    unchanged_inv = [make_entry(path="docs/a.md", content_hash="1" * 64)]

    result = cataloger.invalidate(
        cat_entries, unchanged_inv, DAY, current_taxonomy_sha256=TAXONOMY_SHA)

    facets = {a["facet"]: a for a in result[0]["facet_assignments"]}
    assert facets["factory_scope"]["state"] == "pending"
    assert facets["document_role"] == fresh  # untouched, byte-identical
    # Without a current taxonomy to compare against, nothing invalidates.
    assert cataloger.invalidate(cat_entries, unchanged_inv, DAY) == cat_entries


def test_invalidate_prompt_version_change_invalidates_the_affected_facet():
    # Version-change invalidation (contract "Taxonomy has a breaking
    # change"): a prompt-contract version mismatch invalidates the
    # affected facet the same way a taxonomy mismatch does.
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    stale = facet_assignment(
        "factory_scope", ["domain"],
        provenance=valid_provenance(prompt_contract_version=0))
    cat_entries = [catalog_entry(entry, [stale])]
    unchanged_inv = [make_entry(path="docs/a.md", content_hash="1" * 64)]

    result = cataloger.invalidate(
        cat_entries, unchanged_inv, DAY, current_prompt_version=1)
    assert result[0]["facet_assignments"][0]["state"] == "pending"

    # A matching prompt version invalidates nothing.
    matching = [catalog_entry(entry, [facet_assignment(
        "factory_scope", ["domain"],
        provenance=valid_provenance(prompt_contract_version=1))])]
    result = cataloger.invalidate(
        matching, unchanged_inv, DAY, current_prompt_version=1)
    assert result[0]["facet_assignments"][0]["state"] == "suggested"


def test_invalidate_leaves_owner_disposed_facets_reachable_too():
    # data-model.md: "any -> pending: only by content/taxonomy/prompt
    # invalidation" — a reviewed/overridden facet is not exempt from a
    # genuine content change; only `merge_recommendations` (a stale or
    # racing RECOMMENDATION) is barred from touching it.
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    reviewed = facet_assignment("factory_scope", ["domain"], state="reviewed")
    reviewed["review"] = {"authority": "alpha authority (Domain Hermes)",
                          "decision": "reviewed", "date": "2026-07-01"}
    cat_entries = [catalog_entry(entry, [reviewed])]
    changed_inv = [make_entry(path="docs/a.md", content_hash="9" * 64)]

    result = cataloger.invalidate(cat_entries, changed_inv, DAY)
    fs = result[0]["facet_assignments"][0]
    assert fs["state"] == "pending"
    assert fs["review"] is None


def test_invalidate_content_change_returns_unclassified_facet_to_pending():
    # Reconciliation item 7 (contract "Full baseline and incremental
    # refresh": classification carries forward only "when ... content hash
    # ... remain[s] unchanged"; scenario "Capability cannot resolve" ->
    # `unclassified`). An `unclassified` facet is a content/taxonomy-grounded
    # classification RESULT, so a content change makes it stale and it
    # re-enters `pending` for reclassification, exactly like a `suggested`
    # facet. It carries no provenance, so ONLY its own document's content
    # change triggers it.
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    unclassified = facet_assignment("capability_refs", [],
                                    state="unclassified", since="2026-07-01")
    assert "provenance" not in unclassified  # unclassified carries none
    cat_entries = [catalog_entry(entry, [unclassified])]
    changed_inv = [make_entry(path="docs/a.md", content_hash="9" * 64)]

    result = cataloger.invalidate(cat_entries, changed_inv, DAY)

    fs = result[0]["facet_assignments"][0]
    assert fs["state"] == "pending"
    assert fs["values"] == []
    assert fs["state_since"] == DAY_STR  # reset for the new semantic input
    assert fs["transitions"] == [{"from": "unclassified", "to": "pending",
                                  "occurred_at": DAY_DT, "evidence_refs": []}]
    # An unchanged document leaves the unclassified facet byte-identical.
    unchanged_inv = [make_entry(path="docs/a.md", content_hash="1" * 64)]
    assert cataloger.invalidate(cat_entries, unchanged_inv, DAY) == cat_entries

    # `policy_blocked` is the one state deliberately EXCLUDED: a
    # never-dispatched, opaque protected facet is never returned to
    # pending even when content changes (defense in depth, never a
    # classification result).
    locator = catalog.opaque_locator("alpha", "docs/protected-roster.md")
    blocked = {
        "repo": "alpha", "document_ref": locator["document_ref"],
        "path_sha256": locator["path_sha256"], "content_hash": "9" * 64,
        "dispatch_policy": cataloger.blocked_dispatch_policy(
            locator["document_ref"]),
        "facet_assignments": [{
            "facet": "factory_scope", "values": [], "proposed_values": [],
            "state": "policy_blocked", "state_since": "2026-07-01",
            "transitions": [], "review": None}]}
    assert cataloger.invalidate([blocked], changed_inv, DAY) == [blocked]


def test_invalidate_leaves_a_deleted_document_untouched():
    entry = make_entry(path="docs/a.md", content_hash="1" * 64)
    cat_entries = [catalog_entry(entry, [facet_assignment(
        "factory_scope", ["domain"])])]
    # The document is absent from the current inventory entirely —
    # deletion is catalog.diff's concern, not this function's.
    result = cataloger.invalidate(cat_entries, [], DAY)
    assert result == cat_entries


def test_invalidate_never_resolves_or_touches_a_protected_opaque_entry():
    # SC-007: an opaque (protected) entry has no path to resolve
    # against the inventory and must never be touched — even
    # adversarially, when the real underlying document IS present in
    # the inventory with different content.
    locator = catalog.opaque_locator("alpha", "docs/protected-roster.md")
    blocked_entry = {
        "repo": "alpha", "document_ref": locator["document_ref"],
        "path_sha256": locator["path_sha256"], "content_hash": "9" * 64,
        "dispatch_policy": cataloger.blocked_dispatch_policy(
            locator["document_ref"]),
        "facet_assignments": [{
            "facet": "factory_scope", "values": [], "proposed_values": [],
            "state": "policy_blocked", "state_since": "2026-07-01",
            "transitions": [], "review": None,
        }],
    }
    adversarial_inv = [make_entry(path="docs/protected-roster.md",
                                  content_hash="0" * 64)]

    result = cataloger.invalidate([blocked_entry], adversarial_inv, DAY)

    assert result == [blocked_entry]
    rendered = catalog.render(result)
    assert "protected-roster" not in rendered
    assert "PROTECTED-ROSTER-ALPHA" not in rendered


# --- reference propagation (contract "One document changes": "only that
# entry and any entries invalidated by its references MUST become
# pending classification") ----------------------------------------------------

def referencing_entry(path, refs, facet="factory_scope", state="suggested",
                      since="2026-07-01"):
    """An UNCHANGED-content entry whose one classified facet cites
    other documents through provenance evidence_refs."""
    entry = make_entry(path=path, content_hash="1" * 64)
    assignment = facet_assignment(
        facet, ["domain"], state=state, since=since,
        provenance=valid_provenance(evidence_refs=list(refs)))
    return catalog_entry(entry, [assignment])


def test_invalidate_propagates_to_entries_citing_the_changed_document():
    # docs/a.md changes; docs/b.md is UNCHANGED but its factory_scope
    # classification cited docs/a.md as evidence — that facet (and only
    # that facet) must also become pending.
    changed = catalog_entry(
        make_entry(path="docs/a.md", content_hash="1" * 64),
        [facet_assignment("factory_scope", ["domain"])])
    citing = referencing_entry(
        "docs/b.md", [{"repo": "alpha", "path": "docs/a.md"}])
    uncited = facet_assignment("document_role", ["process"],
                               since="2026-07-01")
    citing["facet_assignments"].append(uncited)
    inv = [make_entry(path="docs/a.md", content_hash="9" * 64),
           make_entry(path="docs/b.md", content_hash="1" * 64)]

    result = cataloger.invalidate([changed, citing], inv, DAY)

    facets = {a["facet"]: a for a in result[1]["facet_assignments"]}
    cited_facet = facets["factory_scope"]
    assert cited_facet["state"] == "pending"
    assert cited_facet["values"] == []
    assert "provenance" not in cited_facet
    assert cited_facet["state_since"] == DAY_STR  # reset, not carried
    # The trigger survives the provenance drop: the transition event
    # records WHICH cited document invalidated the facet.
    assert cited_facet["transitions"] == [
        {"from": "suggested", "to": "pending", "occurred_at": DAY_DT,
         "evidence_refs": [{"repo": "alpha", "path": "docs/a.md"}]}]
    # The facet that cited nothing is untouched, byte-identical.
    assert facets["document_role"] == uncited
    # The changed document's own facet still invalidates as before.
    assert result[0]["facet_assignments"][0]["state"] == "pending"
    # Inputs are never mutated.
    assert citing["facet_assignments"][0]["state"] == "suggested"


def test_invalidate_reference_propagation_is_single_hop():
    # a.md changed; b.md cites a.md; c.md cites b.md. Only b.md's citing
    # facet becomes pending — c.md's evidence about b.md's UNCHANGED
    # content still holds ("only that entry and any entries invalidated
    # by its references": the changed document's blast radius, not a
    # transitive closure).
    changed = catalog_entry(
        make_entry(path="docs/a.md", content_hash="1" * 64),
        [facet_assignment("factory_scope", ["domain"])])
    cites_a = referencing_entry(
        "docs/b.md", [{"repo": "alpha", "path": "docs/a.md"}])
    cites_b = referencing_entry(
        "docs/c.md", [{"repo": "alpha", "path": "docs/b.md"}])
    inv = [make_entry(path="docs/a.md", content_hash="9" * 64),
           make_entry(path="docs/b.md", content_hash="1" * 64),
           make_entry(path="docs/c.md", content_hash="1" * 64)]

    result = cataloger.invalidate([changed, cites_a, cites_b], inv, DAY)

    assert result[1]["facet_assignments"][0]["state"] == "pending"
    assert result[2] == cites_b  # untouched, byte-identical


def test_invalidate_reference_propagation_and_the_pending_boundary():
    # A pending facet carries no provenance (the pending_records shape),
    # so it has NO recorded citations to invalidate: it carries forward
    # untouched — it is already a live classification question, and the
    # classifier will read the cited document's NEW content when it
    # finally runs. A facet that (defensively) DOES retain citation
    # provenance while pending records the contract's pending-to-pending
    # invalidation event and resets state_since, exactly like a content
    # change on its own document ("Pending input changes again").
    changed = catalog_entry(
        make_entry(path="docs/a.md", content_hash="1" * 64),
        [facet_assignment("factory_scope", ["domain"])])
    bare_pending = facet_assignment("factory_scope", [], state="pending",
                                    since="2026-07-01")
    with_provenance = facet_assignment("document_role", [], state="pending",
                                       since="2026-07-01")
    with_provenance["provenance"] = valid_provenance(
        evidence_refs=[{"repo": "alpha", "path": "docs/a.md"}])
    citing = catalog_entry(
        make_entry(path="docs/b.md", content_hash="1" * 64),
        [bare_pending, with_provenance])
    inv = [make_entry(path="docs/a.md", content_hash="9" * 64),
           make_entry(path="docs/b.md", content_hash="1" * 64)]

    result = cataloger.invalidate([changed, citing], inv, DAY)

    facets = {a["facet"]: a for a in result[1]["facet_assignments"]}
    assert facets["factory_scope"] == bare_pending  # carried forward
    fs = facets["document_role"]
    assert fs["state"] == "pending"
    assert "provenance" not in fs
    assert fs["state_since"] == DAY_STR  # reset for the new semantic input
    assert fs["transitions"] == [
        {"from": "pending", "to": "pending", "occurred_at": DAY_DT,
         "evidence_refs": [{"repo": "alpha", "path": "docs/a.md"}]}]


def test_invalidate_unresolvable_or_unchanged_references_never_propagate():
    # Only a {repo, path} mapping citing a CHANGED document propagates.
    # Strings, partial mappings, opaque document_ref locators, and
    # references to unchanged or uncataloged documents are all inert.
    changed = catalog_entry(
        make_entry(path="docs/a.md", content_hash="1" * 64),
        [facet_assignment("factory_scope", ["domain"])])
    locator = catalog.opaque_locator("alpha", "docs/a.md")
    inert = referencing_entry("docs/b.md", [
        "docs/a.md",                                   # bare string
        {"path": "docs/a.md"},                         # no repo
        {"repo": "alpha"},                             # no path
        {"repo": "alpha", "path": "docs/other.md"},    # unchanged doc
        {"repo": "beta", "path": "docs/a.md"},         # unknown repo
        {"document_ref": locator["document_ref"],      # opaque locator:
         "path_sha256": locator["path_sha256"]},       # never resolved
    ])
    inv = [make_entry(path="docs/a.md", content_hash="9" * 64),
           make_entry(path="docs/b.md", content_hash="1" * 64),
           make_entry(path="docs/other.md", content_hash="2" * 64)]

    result = cataloger.invalidate([changed, inert], inv, DAY)

    assert result[1] == inert  # untouched, byte-identical
    # The changed document itself still invalidated normally.
    assert result[0]["facet_assignments"][0]["state"] == "pending"


def test_invalidate_reference_propagation_is_deterministic_and_deduplicated():
    # Two changed cited documents, listed twice each in evidence_refs
    # and in reverse order: the recorded transition evidence is sorted
    # and de-duplicated regardless of input order, and repeated calls
    # are byte-identical (catalog.render precedent).
    changed_a = catalog_entry(
        make_entry(path="docs/a.md", content_hash="1" * 64),
        [facet_assignment("factory_scope", ["domain"])])
    changed_b = catalog_entry(
        make_entry(path="docs/b.md", content_hash="2" * 64),
        [facet_assignment("factory_scope", ["domain"])])
    citing = referencing_entry("docs/c.md", [
        {"repo": "alpha", "path": "docs/b.md"},
        {"repo": "alpha", "path": "docs/a.md"},
        {"repo": "alpha", "path": "docs/b.md"},
    ])
    inv = [make_entry(path="docs/a.md", content_hash="9" * 64),
           make_entry(path="docs/b.md", content_hash="8" * 64),
           make_entry(path="docs/c.md", content_hash="1" * 64)]

    first = cataloger.invalidate([changed_a, changed_b, citing], inv, DAY)
    second = cataloger.invalidate([changed_a, changed_b, citing], inv, DAY)

    assert catalog.render(first) == catalog.render(second)
    event = first[2]["facet_assignments"][0]["transitions"][0]
    assert event["evidence_refs"] == [
        {"repo": "alpha", "path": "docs/a.md"},
        {"repo": "alpha", "path": "docs/b.md"}]
