"""The staging workbench's PURE scope derivation (staging-workbench-model.js;
openxFactory `add-staging-workbench` design D3/D4/D5/D7, change task 4.1).

Python-side only — no browser automation: the ACTUAL staging-workbench-model.js
runs in node (skipped when node is absent), against hand snapshots carrying the
exact `completeness` shape the generator emits and against the real fixture
snapshot. The module is copied ALONE into the harness, exactly like
lens-model.js / explorer.js, so it must stay import-free.

What is pinned here:

  workbenchScope        the per-kind document-set derivation — a cluster's
                        document edges; a possible's CITED supporting-evidence
                        documents plus a separately-labelled INHERITED section
                        of claiming-cluster members (never conflated: cited
                        evidence is a recorded pin, inherited membership is an
                        inference); a staged topic's folder corpus documents
                        plus every document whose destinations name the topic.
                        Stable (snapshot) ordering; completeness rides along
                        VERBATIM (absent means absent — design D7's no-zero-bar
                        rule starts here); an unresolvable tile is null.
  lensScopeSnapshot     the scoped projection the `lens` panel feeds the
                        EXISTING buildLensModel — the scope's own documents plus
                        the snapshot's OWN keyword_index seed filtered to the
                        scope (counts verbatim, no re-analysis).
  lensSeedKeywords      the panel's default check set — the scope's declared
                        keywords, narrowed to the scoped rail.

NAMING NOTE (design D5): this is the STAGING workbench, a read-only scoped
view. The `ideation-workbench` reference-set family (workbench.py, tested in
test_workbench.py) is a different thing and is untouched by this change.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit  # noqa: F401

from ideation_dashboard import gate_routes as gate_routes_mod
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
MODEL_JS = WEB / "views" / "staging-workbench-model.js"
NODE = shutil.which("node")

_NODE_HARNESS = """
import { workbenchScope, lensScopeSnapshot, lensSeedKeywords,
  WORKBENCH_KINDS, SIGNAL_KEYS, SECTION_KEYS } from './staging-workbench-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const scopes = cases.scopes.map(([, snapshot, kind, id]) => {
  const scope = workbenchScope(snapshot, kind, id);
  if (!scope) return null;
  // a JSON-safe projection of the scope, plus the lens re-scope built FROM it
  const scoped = lensScopeSnapshot(snapshot, scope);
  return {
    kind: scope.kind, id: scope.id, title: scope.title,
    keywords: scope.keywords,
    counts: scope.counts,
    sections: scope.sections.map((s) => ({
      key: s.key, label: s.label, inherited: s.inherited,
      documents: s.documents.map((row) => ({
        id: row.id, path: row.path, resolved: row.resolved,
        completeness: row.completeness,
      })),
    })),
    flatIds: scope.documents.map((row) => row.id),
    outline: scope.outline,
    lens: {
      docIds: scoped.documents.map((d) => d.id),
      keywordIndex: scoped.keyword_index,
      seed: lensSeedKeywords(scoped, scope),
    },
  };
});
console.log(JSON.stringify({
  kinds: WORKBENCH_KINDS, signals: SIGNAL_KEYS, sectionKeys: SECTION_KEYS,
  scopes,
}));
"""


def _run_scopes(cases, tmp_path):
    """Run every (id, snapshot, kind, tileId) case through the ACTUAL
    workbenchScope/lensScopeSnapshot/lensSeedKeywords, returning
    {"kinds": ..., "signals": ..., "scopes": {case id: scope | None}}."""
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(MODEL_JS, tmp_path / "staging-workbench-model.mjs")
    (tmp_path / "harness.mjs").write_text(_NODE_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "scope-cases.json"
    cases_path.write_text(json.dumps({"scopes": cases}), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "harness.mjs"), str(cases_path)],
        capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    out = json.loads(proc.stdout)
    return {"kinds": out["kinds"], "signals": out["signals"],
            "sectionKeys": out["sectionKeys"],
            "scopes": dict(zip([c[0] for c in cases], out["scopes"]))}


# ---- the hand snapshot: every edge family the scopes read ----------------------
#
# Completeness objects carry the EXACT generator shape (score + the five named
# signals, each {value, count}) so "verbatim" is asserted against the real
# contract, and one document (c.md) deliberately carries NONE — the excluded /
# pre-growth case whose row must surface no bar.

def _comp(score):
    return {
        "score": score,
        "structure": {"value": 1.0, "count": 3},
        "length": {"value": 0.5, "count": 210},
        "open_markers": {"value": 0.8, "count": 1},
        "keyword_coverage": {"value": 1.0, "count": 2},
        "link_degree": {"value": 0.3333, "count": 1},
    }


def _hand_snapshot():
    return {
        # `repository` is what a create's `Repository context:` header defaults
        # from (add-workbench-bullseye-and-create) — the same field every other
        # snapshot consumer reads, never a new one.
        "repository": "fixture-repo",
        "documents": [
            {"id": "ideation/brainstorm/a.md", "path": "ideation/brainstorm/a.md",
             "topics": ["alpha", "shared"], "completeness": _comp(0.72)},
            {"id": "ideation/brainstorm/b.md", "path": "ideation/brainstorm/b.md",
             "topics": ["alpha"], "completeness": _comp(0.4111),
             "destinations": {"staged_topics": ["topic-x"]}},
            # NO completeness: the pre-growth / excluded shape (design D7)
            {"id": "ideation/brainstorm/c.md", "path": "ideation/brainstorm/c.md",
             "topics": ["beta"]},
            {"id": "ideation/staging/topic-x/topic-x.md",
             "path": "ideation/staging/topic-x/topic-x.md",
             "topics": ["alpha", "gamma"], "completeness": _comp(0.9),
             "destinations": {"staged_topics": ["topic-x"]}},
        ],
        "clusters": [
            {"id": "cl-alpha", "name": "Alpha", "topics": ["alpha", "shared"],
             "document_edges": [
                 {"document": "ideation/brainstorm/a.md"},
                 {"document": "ideation/brainstorm/b.md"},
                 {"document": "ideation/staging/topic-x/topic-x.md"},
             ]},
            {"id": "cl-beta", "name": "Beta", "topics": ["beta"],
             "document_edges": [{"document": "ideation/brainstorm/c.md"}]},
        ],
        "possibles": [
            {"id": "pos-1", "title": "Possible one", "state": "latent",
             "claiming_clusters": ["cl-alpha", "cl-missing"],
             "supporting_evidence": [
                 # cited evidence OVERLAPS cluster membership (a.md) — the
                 # inherited section must not repeat it
                 {"document": "ideation/brainstorm/a.md", "section": "s",
                  "passage_sha256": "0" * 64},
                 {"document": "ideation/brainstorm/gone.md", "section": "s",
                  "passage_sha256": "1" * 64},
             ]},
            {"id": "pos-picked", "title": "Picked possible", "state": "picked",
             "claiming_clusters": ["cl-beta"],
             "pick": {"staging_id": "topic-x", "change_id": "add-x"},
             "supporting_evidence": []},
        ],
        "staged_topics": [
            {"staging_id": "topic-x",
             "files": ["ideation/staging/topic-x/manifest.yaml",
                       "ideation/staging/topic-x/topic-x.md"]},
            {"staging_id": "topic-empty", "files": []},
        ],
        "changes": [],
        "keyword_index": [
            {"keyword": "alpha", "declared_doc_count": 3},
            {"keyword": "beta", "declared_doc_count": 1},
            {"keyword": "gamma", "declared_doc_count": 1},
            {"keyword": "unrelated", "declared_doc_count": 9},
        ],
    }


SNAP = _hand_snapshot()

SCOPE_CASES = [
    ("cluster", SNAP, "cluster", "cl-alpha"),
    ("cluster-beta", SNAP, "cluster", "cl-beta"),
    ("possible", SNAP, "possible", "pos-1"),
    ("possible-picked", SNAP, "possible", "pos-picked"),
    ("staged", SNAP, "staged", "topic-x"),
    ("staged-empty", SNAP, "staged", "topic-empty"),
    # unresolvable tiles and unknown kinds are null, never an empty scope
    ("cluster-missing", SNAP, "cluster", "cl-nope"),
    ("possible-missing", SNAP, "possible", "pos-nope"),
    ("staged-missing", SNAP, "staged", "topic-nope"),
    ("unknown-kind", SNAP, "documents", "ideation/brainstorm/a.md"),
    ("no-id", SNAP, "cluster", None),
    ("empty-snapshot", {}, "cluster", "cl-alpha"),
]


def test_workbench_kind_and_signal_vocabularies(tmp_path):
    out = _run_scopes(SCOPE_CASES, tmp_path)
    assert out["kinds"] == ["cluster", "possible", "staged"]
    # the five signals in the contract's emission order — what the docs panel walks
    assert out["signals"] == ["structure", "length", "open_markers",
                              "keyword_coverage", "link_degree"]


def test_cluster_scope_is_its_document_edges(tmp_path):
    r = _run_scopes(SCOPE_CASES, tmp_path)["scopes"]["cluster"]
    assert r["kind"] == "cluster" and r["title"] == "Alpha"
    assert [s["key"] for s in r["sections"]] == ["members"]
    # the edge documents, in the snapshot's own (stable) order
    assert r["flatIds"] == ["ideation/brainstorm/a.md", "ideation/brainstorm/b.md",
                            "ideation/staging/topic-x/topic-x.md"]
    assert r["keywords"] == ["alpha", "shared"]
    assert r["counts"] == {"documents": 3, "scored": 3, "unresolved": 0,
                           "inherited": 0}
    # completeness rides along VERBATIM — score and each signal's value+count
    row = r["sections"][0]["documents"][0]
    assert row["completeness"]["score"] == 0.72
    assert row["completeness"]["length"] == {"value": 0.5, "count": 210}


def test_cluster_scope_missing_completeness_stays_missing(tmp_path):
    """The no-zero-bar rule (design D7) starts in the model: a document the
    snapshot does not score carries completeness: null, never a zeroed one."""
    r = _run_scopes(SCOPE_CASES, tmp_path)["scopes"]["cluster-beta"]
    row = r["sections"][0]["documents"][0]
    assert row["id"] == "ideation/brainstorm/c.md"
    assert row["resolved"] is True
    assert row["completeness"] is None
    assert r["counts"] == {"documents": 1, "scored": 0, "unresolved": 0,
                           "inherited": 0}


def test_possible_scope_separates_cited_from_inherited(tmp_path):
    """Cited evidence is a recorded pin; claiming-cluster membership is an
    inference — two sections, disjoint, the inherited one flagged, never
    conflated (design D4)."""
    r = _run_scopes(SCOPE_CASES, tmp_path)["scopes"]["possible"]
    assert [s["key"] for s in r["sections"]] == ["cited", "inherited"]
    cited, inherited = r["sections"]
    assert cited["inherited"] is False
    assert inherited["inherited"] is True
    # cited: the evidence pins in recorded order — including the reference the
    # snapshot cannot resolve, SHOWN as unresolved rather than silently dropped
    assert [d["id"] for d in cited["documents"]] == \
        ["ideation/brainstorm/a.md", "ideation/brainstorm/gone.md"]
    assert cited["documents"][0]["resolved"] is True
    assert cited["documents"][1]["resolved"] is False
    assert cited["documents"][1]["completeness"] is None
    # inherited: the claiming cluster's members MINUS what is already cited
    # (a.md never reappears), the unknown claiming cluster contributing nothing
    assert [d["id"] for d in inherited["documents"]] == \
        ["ideation/brainstorm/b.md", "ideation/staging/topic-x/topic-x.md"]
    # the two sections stay disjoint
    assert len(set(r["flatIds"])) == len(r["flatIds"])
    assert r["counts"] == {"documents": 4, "scored": 3, "unresolved": 1,
                           "inherited": 2}
    # keywords inherit from the claiming clusters' declared topics
    assert r["keywords"] == ["alpha", "shared"]
    # an unpicked possible has no outline material
    assert r["outline"] is None


def test_staged_scope_is_folder_docs_plus_declaring_documents(tmp_path):
    r = _run_scopes(SCOPE_CASES, tmp_path)["scopes"]["staged"]
    assert [s["key"] for s in r["sections"]] == ["folder", "declaring"]
    folder, declaring = r["sections"]
    # the folder section keeps only files that ARE catalogued corpus documents
    # (the manifest is a file, not a document)
    assert [d["id"] for d in folder["documents"]] == \
        ["ideation/staging/topic-x/topic-x.md"]
    # every document whose destinations name the topic — minus the folder's own
    # (the generator stamps in-folder docs with the destination too)
    assert [d["id"] for d in declaring["documents"]] == ["ideation/brainstorm/b.md"]
    assert r["counts"] == {"documents": 2, "scored": 2, "unresolved": 0,
                           "inherited": 0}
    # keywords come from the folder documents' declared topics
    assert r["keywords"] == ["alpha", "gamma"]
    # the outline is the topic's own file list (primaryFragmentPath resolves it)
    assert r["outline"] == {"from": "staged-topic", "stagingId": "topic-x",
                            "files": ["ideation/staging/topic-x/manifest.yaml",
                                      "ideation/staging/topic-x/topic-x.md"]}


def test_picked_possible_outline_is_the_picked_topic(tmp_path):
    """A possible PICKED into a staging topic carries that topic's outline —
    the pick is recorded register data, not an inference."""
    r = _run_scopes(SCOPE_CASES, tmp_path)["scopes"]["possible-picked"]
    assert r["outline"]["from"] == "picked-topic"
    assert r["outline"]["stagingId"] == "topic-x"
    # and a stub topic scope still answers, with an outline over no files
    empty = _run_scopes(SCOPE_CASES, tmp_path)["scopes"]["staged-empty"]
    assert empty["counts"]["documents"] == 0
    assert empty["outline"] == {"from": "staged-topic", "stagingId": "topic-empty",
                                "files": []}


def test_unresolvable_scopes_are_null(tmp_path):
    r = _run_scopes(SCOPE_CASES, tmp_path)["scopes"]
    for cid in ("cluster-missing", "possible-missing", "staged-missing",
                "unknown-kind", "no-id", "empty-snapshot"):
        assert r[cid] is None, cid


def test_lens_rescope_filters_the_existing_seed_verbatim(tmp_path):
    """The lens panel's projection RE-SCOPES the existing derivation (design
    D4): the scope's own resolved documents, and the snapshot's OWN
    keyword_index rows for the touched keywords with their corpus-wide declared
    counts VERBATIM — no recount, no new analysis, no new snapshot field."""
    scopes = _run_scopes(SCOPE_CASES, tmp_path)["scopes"]
    lens = scopes["cluster"]["lens"]
    assert lens["docIds"] == ["ideation/brainstorm/a.md", "ideation/brainstorm/b.md",
                              "ideation/staging/topic-x/topic-x.md"]
    # touched keywords: the cluster's declared topics + its documents' topics;
    # `unrelated` (untouched) is filtered out; counts are the seed's, verbatim
    assert lens["keywordIndex"] == [
        {"keyword": "alpha", "declared_doc_count": 3},
        {"keyword": "gamma", "declared_doc_count": 1},
    ]
    # the seed check set is the scope's keywords narrowed to the scoped rail
    # ("shared" is declared on a doc but absent from keyword_index -> dropped)
    assert lens["seed"] == ["alpha"]
    # the possible's lens scope spans cited + inherited documents
    pos = scopes["possible"]["lens"]
    assert pos["docIds"] == ["ideation/brainstorm/a.md", "ideation/brainstorm/b.md",
                             "ideation/staging/topic-x/topic-x.md"]


def test_scope_derivation_is_deterministic(tmp_path):
    """Same snapshot, same tile -> byte-identical scope (stable ordering)."""
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    first = _run_scopes(SCOPE_CASES, tmp_path / "a")
    second = _run_scopes(SCOPE_CASES, tmp_path / "b")
    assert first == second


# ---- the staged cluster-neighbourhood section (Brett 2026-07-25 dogfood ruling) --
#
# A staged topic's docs panel gains a THIRD section: the member documents of the
# topic's LINKED clusters (the same clusters->staged adjacency the wheel draws —
# a cluster whose `lineage.staged_picks` names the topic), separately labelled,
# styled like the possible's `inherited` section, deduped against the folder +
# declaring sections, never conflated with the topic's own material. Absent when
# the topic has no linked clusters. Health and the readiness gate are untouched
# (Python-side, folder-scoped) — nothing here feeds them.
#
# This fixture mirrors the LIVE snapshot shape Brett dogfooded: the staged topic
# has ONE own folder document and FIVE linked clusters whose member documents add
# THREE more (one own-doc overlap deduped against the folder, one overlap deduped
# against declaring, and cross-cluster repeats deduped to one entry each).

def _neighbourhood_snapshot():
    own = "ideation/staging/github-administration-plane/github-administration-plane.md"
    declaring = "ideation/brainstorm/github-plane-notes.md"
    keycloak = "openxFactory/docs/keycloak-identity-brokering.md"
    dashboard = "installs/dashboard-action-center.md"
    promotion = "openxFactory/docs/domain-to-neutral-promotion.md"
    other = "ideation/brainstorm/unrelated.md"

    def _lineage(c):
        c["lineage"] = {"staged_picks": ["github-administration-plane"]}
        return c

    return {
        "documents": [
            {"id": own, "path": own, "topics": ["github", "identity"],
             "completeness": _comp(0.9),
             "destinations": {"staged_topics": ["github-administration-plane"]}},
            {"id": declaring, "path": declaring, "topics": ["github"],
             "completeness": _comp(0.5),
             "destinations": {"staged_topics": ["github-administration-plane"]}},
            {"id": keycloak, "path": keycloak, "topics": ["identity"],
             "completeness": _comp(0.7)},
            {"id": dashboard, "path": dashboard, "topics": ["ops"],
             "completeness": _comp(0.6)},
            # NO completeness: the neighbourhood section honours the no-bar rule too
            {"id": promotion, "path": promotion, "topics": ["neutral"]},
            {"id": other, "path": other, "topics": ["misc"]},
        ],
        "clusters": [
            _lineage({"id": "cl-app-identity-tiers", "name": "App identity tiers",
                      "topics": ["identity"],
                      "document_edges": [{"document": own}, {"document": keycloak}]}),
            # a linked cluster whose only NEW member is the declaring doc -> deduped
            _lineage({"id": "cl-branch-protection", "name": "Branch protection",
                      "topics": ["github"],
                      "document_edges": [{"document": own}, {"document": declaring}]}),
            _lineage({"id": "cl-github-administration", "name": "GitHub administration",
                      "topics": ["github"],
                      "document_edges": [{"document": own}, {"document": dashboard}]}),
            _lineage({"id": "cl-opsxfactory", "name": "OpsxFactory",
                      "topics": ["ops"],
                      "document_edges": [{"document": own}, {"document": promotion}]}),
            # cross-cluster repeats of keycloak + promotion -> each deduped to one
            _lineage({"id": "cl-roles-authority-model", "name": "Roles authority model",
                      "topics": ["identity"],
                      "document_edges": [{"document": keycloak}, {"document": promotion}]}),
            # NOT linked to the topic (no lineage staged_picks) -> must never leak
            {"id": "cl-unrelated", "name": "Unrelated", "topics": ["misc"],
             "document_edges": [{"document": other}]},
        ],
        "possibles": [],
        "staged_topics": [
            {"staging_id": "github-administration-plane",
             "files": ["ideation/staging/github-administration-plane/manifest.yaml", own]},
        ],
        "changes": [],
        "keyword_index": [
            {"keyword": "github", "declared_doc_count": 2},
            {"keyword": "identity", "declared_doc_count": 2},
        ],
    }


NB_SNAP = _neighbourhood_snapshot()
NB_CASES = [
    ("hub", NB_SNAP, "staged", "github-administration-plane"),
    # the plain SNAP topic-x has NO linked clusters -> no neighbourhood section
    ("no-clusters", SNAP, "staged", "topic-x"),
]


def test_staged_scope_adds_cluster_neighbourhood_section(tmp_path):
    r = _run_scopes(NB_CASES, tmp_path)["scopes"]["hub"]
    # three sections now, the neighbourhood one LAST and flagged inherited so the
    # renderer gives it the separated (possible-inherited) treatment
    assert [s["key"] for s in r["sections"]] == ["folder", "declaring", "neighbourhood"]
    folder, declaring, neighbourhood = r["sections"]
    assert neighbourhood["inherited"] is True
    assert neighbourhood["label"] == "cluster neighbourhood"
    # folder = the one own doc; declaring = the one inbound doc (own deduped out)
    assert [d["id"] for d in folder["documents"]] == \
        ["ideation/staging/github-administration-plane/github-administration-plane.md"]
    assert [d["id"] for d in declaring["documents"]] == \
        ["ideation/brainstorm/github-plane-notes.md"]
    # neighbourhood = the 3 NEW member docs of the 5 linked clusters, in
    # cluster-then-edge order, every duplicate (own, declaring, cross-cluster
    # repeats) deduped away
    assert [d["id"] for d in neighbourhood["documents"]] == [
        "openxFactory/docs/keycloak-identity-brokering.md",
        "installs/dashboard-action-center.md",
        "openxFactory/docs/domain-to-neutral-promotion.md",
    ]


def test_cluster_neighbourhood_is_deduped_and_honours_no_bar(tmp_path):
    r = _run_scopes(NB_CASES, tmp_path)["scopes"]["hub"]
    # the three sections stay disjoint (own + declaring never reappear below)
    assert len(set(r["flatIds"])) == len(r["flatIds"])
    assert r["counts"]["documents"] == 5   # 1 folder + 1 declaring + 3 neighbourhood
    assert r["counts"]["inherited"] == 3   # the neighbourhood section is inherited
    # the unrelated cluster's document never leaked in
    assert "ideation/brainstorm/unrelated.md" not in r["flatIds"]
    # a neighbourhood doc the snapshot does not score surfaces NO bar (design D7)
    neighbourhood = r["sections"][2]
    by_id = {d["id"]: d for d in neighbourhood["documents"]}
    assert by_id["openxFactory/docs/domain-to-neutral-promotion.md"]["completeness"] is None
    assert by_id["openxFactory/docs/keycloak-identity-brokering.md"]["completeness"] is not None


def test_staged_scope_has_no_neighbourhood_when_no_linked_clusters(tmp_path):
    """A staged topic with no clusters linking to it keeps just the folder +
    declaring sections — the neighbourhood section is absent, not an empty one."""
    r = _run_scopes(NB_CASES, tmp_path)["scopes"]["no-clusters"]
    assert [s["key"] for s in r["sections"]] == ["folder", "declaring"]
    assert all(s["key"] != "neighbourhood" for s in r["sections"])


# ---- the lens SESSION + the create SEEDING (add-workbench-bullseye-and-create) ----
#
# Both rules live in the PURE model module so they are pinned here rather than in
# a browser: the checked-keyword selection is workbench-SESSION state (design D4
# — a tab switch must not destroy it, a new scope must reseed it), and each tab
# seeds the create dialog from the material that tab is showing (design D7). The
# gate-off CLI descriptor is asserted by PARSING it with the real CLI parser, so
# the browser's fallback and the terminal surface cannot drift.

_CREATE_HARNESS = """
import {
  workbenchScope, lensScopeSnapshot, lensSessionSeed, scopeKey, toggleKeyword,
  createArea, createSeed, createOffered, createRequest,
  createSource, createDocumentCommand, CREATE_ROUTE, CREATE_TABS,
  BRAINSTORM_AREA, STAGING_AREA,
} from './staging-workbench-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));

const scopes = {};
for (const [id, snapshot, kind, tileId] of cases.scopes) {
  const scope = workbenchScope(snapshot, kind, tileId);
  const scoped = lensScopeSnapshot(snapshot, scope);
  // a fresh mount seeds from the scope; a tab switch hands the SAME session back
  const first = lensSessionSeed(null, scoped, scope);
  const edited = { key: first.key, checked: toggleKeyword(first.checked, 'gamma') };
  const afterTabSwitch = lensSessionSeed(edited, scoped, scope);
  // a DIFFERENT scope reseeds rather than carrying the previous keywords forward
  const otherScope = workbenchScope(snapshot, 'cluster', 'cl-beta');
  const otherScoped = otherScope ? lensScopeSnapshot(snapshot, otherScope) : null;
  const afterScopeChange = otherScope
    ? lensSessionSeed(edited, otherScoped, otherScope) : null;
  const seeds = {};
  for (const tab of CREATE_TABS) {
    seeds[tab] = {
      offered: createOffered(scope, tab),
      seed: createSeed(snapshot, scope, tab, { checked: edited.checked }),
    };
  }
  // an activated bullseye SECTOR narrows the lens topics seed to that sector's
  // own matched combination (open question 2's ruling) and leaves the recipe
  // citation naming the full checked set
  const sector = createSeed(snapshot, scope, 'lens',
    { checked: ['alpha', 'beta', 'gamma'], pinned: ['alpha'], subset: ['alpha', 'gamma'] });
  scopes[id] = {
    key: scopeKey(scope),
    area: createArea(scope),
    session: {
      first, edited, afterTabSwitch,
      switchKeptIt: afterTabSwitch === edited,
      afterScopeChange,
    },
    seeds,
    sector,
    request: createRequest(seeds.docs.seed, { title: 'T', summary: 'S' }),
    command: createDocumentCommand(seeds.lens.seed, { actor: 'brett' }),
  };
}
console.log(JSON.stringify({
  scopes, route: CREATE_ROUTE, tabs: CREATE_TABS,
  areas: { brainstorm: BRAINSTORM_AREA, staging: STAGING_AREA },
  // the `Status:` a create into each of these areas seeds — `brainstorm`
  // everywhere, per the ruling; the area is never consulted
  statuses: cases.areas.map((a) => [a,
    createSeed({repository: 'r'}, {kind: 'cluster', id: 'c'}, 'docs', {area: a}).status]),
  toggles: cases.toggles.map(([list, kw]) => toggleKeyword(list, kw)),
  sources: cases.sources.map(([kind, tab]) => createSource(
    {generation: {source_revision: 'f'.repeat(40)}},
    {kind, id: 'the-id'}, tab, {checked: ['alpha', 'beta'], pinned: ['alpha']})),
}));
"""

_STATUS_AREAS = ["ideation/brainstorm/", "ideation/staging/topic-x/",
                 "ideation/staging/", "ideation/drafts/", "docs/"]
_TOGGLES = [[["alpha"], "beta"], [["alpha", "beta"], "alpha"], [[], "alpha"],
            [["alpha", "beta"], "beta"]]
_SOURCES = [["cluster", "docs"], ["staged", "lens"], ["possible", "outline"]]


def _run_create(cases, tmp_path):
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(MODEL_JS, tmp_path / "staging-workbench-model.mjs")
    (tmp_path / "harness.mjs").write_text(_CREATE_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "create-cases.json"
    cases_path.write_text(json.dumps({"scopes": cases, "areas": _STATUS_AREAS,
                                      "toggles": _TOGGLES, "sources": _SOURCES}),
                          encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "harness.mjs"), str(cases_path)],
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


CREATE_CASES = [
    ("cluster", SNAP, "cluster", "cl-alpha"),
    ("possible", SNAP, "possible", "pos-1"),
    ("staged", SNAP, "staged", "topic-x"),
]


def test_lens_selection_survives_a_tab_switch_and_reseeds_on_a_new_scope(tmp_path):
    out = _run_create(CREATE_CASES, tmp_path)["scopes"]
    staged = out["staged"]
    # the fresh seed is the scope's declared keywords narrowed to the scoped rail
    assert staged["session"]["first"]["checked"] == ["alpha", "gamma"]
    assert staged["session"]["first"]["key"] == "staged|topic-x"
    # the human unchecks `gamma`, visits docs/outline, and returns: the session
    # comes back UNCHANGED (the panel never rebuilds it)
    assert staged["session"]["edited"]["checked"] == ["alpha"]
    assert staged["session"]["afterTabSwitch"]["checked"] == ["alpha"]
    assert staged["session"]["switchKeptIt"] is True
    # opening a DIFFERENT tile reseeds from THAT scope rather than carrying the
    # previous selection forward
    reseeded = staged["session"]["afterScopeChange"]
    assert reseeded["key"] == "cluster|cl-beta"
    assert reseeded["checked"] == ["beta"]


def test_toggle_keyword_is_order_preserving_and_idempotent(tmp_path):
    out = _run_create(CREATE_CASES, tmp_path)
    assert out["toggles"] == [["alpha", "beta"], ["beta"], ["alpha"], ["alpha"]]


def test_create_seed_is_per_tab_and_per_scope_kind(tmp_path):
    out = _run_create(CREATE_CASES, tmp_path)["scopes"]
    # a STAGED scope writes into its own topic folder, on every tab
    staged = out["staged"]["seeds"]
    assert staged["docs"]["seed"]["area"] == "ideation/staging/topic-x/"
    assert staged["outline"]["seed"]["area"] == "ideation/staging/topic-x/"
    # topics: the tile's keywords on docs/outline, the LIVE checked set on lens
    assert staged["docs"]["seed"]["topics"] == ["alpha", "gamma"]
    assert staged["outline"]["seed"]["topics"] == ["alpha", "gamma"]
    assert staged["lens"]["seed"]["topics"] == ["alpha"]
    # a cluster / possible scope has no topic folder -> the brainstorm area
    assert out["cluster"]["seeds"]["docs"]["seed"]["area"] == "ideation/brainstorm/"
    assert out["possible"]["seeds"]["docs"]["seed"]["area"] == "ideation/brainstorm/"
    # repository context comes from the snapshot; title/summary are NEVER seeded
    for scope in out.values():
        for entry in scope["seeds"].values():
            assert entry["seed"]["repositoryContext"] == "fixture-repo"
            assert entry["seed"]["title"] == "" and entry["seed"]["summary"] == ""


def test_create_seed_status_is_always_brainstorm(tmp_path):
    """Brett's 2026-07-25 ruling on open question 1: `brainstorm` in EVERY area,
    including a staging topic folder — "these are brainstorm docs". The area is
    never consulted (an earlier pass derived `staged` and the ruling REVERSED
    it), and the JS agrees with the Python default, so the browser affordance and
    a hand-rolled request land the same header."""
    from ideation_dashboard import authoring

    out = _run_create(CREATE_CASES, tmp_path)
    assert dict(out["statuses"]) == {area: "brainstorm" for area in _STATUS_AREAS}
    assert authoring.DEFAULT_STATUS == "brainstorm"
    # the reversed helper is gone on BOTH sides
    assert not hasattr(authoring, "status_for_area")
    assert "statusForArea" not in MODEL_JS.read_text(encoding="utf-8")
    scopes = out["scopes"]
    # a staged scope's PLACEMENT is what ties the document to the packet, and it
    # is unchanged — only the status default moved
    assert scopes["staged"]["seeds"]["docs"]["seed"]["area"] == "ideation/staging/topic-x/"
    for scope in scopes.values():
        for entry in scope["seeds"].values():
            assert entry["seed"]["status"] == "brainstorm"


def test_sector_activation_seeds_only_that_sectors_keywords(tmp_path):
    """Brett's 2026-07-25 ruling on open question 2: activating a ring SECTOR
    seeds `Topics:` from that sector's own matched combination, not from the whole
    checked set — while the `Source:` recipe still names the FULL checked and
    pinned sets at the source revision (that is what makes the membership
    re-derivable) plus the sector actually acted on."""
    out = _run_create(CREATE_CASES, tmp_path)["scopes"]
    for name, scope in out.items():
        sector = scope["sector"]
        # exactly the sector's subset, in the sector's own order
        assert sector["topics"] == ["alpha", "gamma"], name
        # the recipe still records everything that was checked
        assert "checked alpha, beta, gamma" in sector["source"], name
        assert "pinned alpha" in sector["source"], name
        assert sector["source"].endswith("· bullseye sector alpha ∧ gamma"), name
        assert sector["status"] == "brainstorm", name
    # with NO subset (the centre region and the labelled button) the whole
    # checked set is the seed — one dialog, one rule, two seeds
    assert out["staged"]["seeds"]["lens"]["seed"]["topics"] == ["alpha"]
    assert "bullseye sector" not in out["staged"]["seeds"]["lens"]["seed"]["source"]


def test_create_source_cites_the_scope_and_the_recipe(tmp_path):
    docs_src, lens_src, outline_src = _run_create(CREATE_CASES, tmp_path)["sources"]
    # docs / outline: the workbench scope, by kind and id
    assert docs_src == "staging workbench scope: cluster the-id"
    assert outline_src == "staging workbench scope: possible the-id"
    # lens: the RECIPE (checked + pinned) at the snapshot's source_revision, so
    # the membership that motivated the document re-derives from the record
    assert lens_src.startswith("staging workbench scope: staged the-id · "
                               "keyword-lens recipe: checked alpha, beta · "
                               "pinned alpha · at source_revision ")
    assert lens_src.endswith("f" * 40)


def test_outline_create_is_hidden_for_cluster_and_possible_scopes(tmp_path):
    """Hidden, not disabled: a cluster or a possible has no staging topic folder
    to write a fragment into, and a disabled control would imply a precondition
    the human could satisfy from here (design D7 consequence)."""
    out = _run_create(CREATE_CASES, tmp_path)["scopes"]
    assert out["staged"]["seeds"]["outline"]["offered"] is True
    assert out["cluster"]["seeds"]["outline"]["offered"] is False
    assert out["possible"]["seeds"]["outline"]["offered"] is False
    # docs + lens are offered on every scope kind
    for scope in out.values():
        assert scope["seeds"]["docs"]["offered"] is True
        assert scope["seeds"]["lens"]["offered"] is True


def test_create_request_matches_the_route_contract(tmp_path):
    """The request body the browser sends is exactly the body the route
    validates — one payload definition, pinned from both sides.

    The set GREW by exactly two fields on 2026-07-26 (007-workbench-branch-sessions
    T023a): `scope_kind` + `scope_id`, the tile identity the route resolves the
    BRANCH SESSION from. It grew by exactly ONE more on the same day (T082):
    `continuation`, the human's answer to the FR-025 resume-or-new report, which
    the route already accepted and only the workbench transport was not sending.
    It grew by exactly ONE more on 2026-07-27 (PR #49 review finding 8, leg a):
    `repository`, the identity of the repository THIS PAGE IS READING. The route
    used to have no repository input at all and keyed the session off whichever
    registry entry was ACTIVE — which the client-side selector does not move — so
    a create issued from a repoB page opened a session in repoA. It is distinct
    from `repository_context`, which is a DOCUMENT HEADER value the human can
    edit; the two are both present here deliberately.

    This is payload arithmetic, not a relaxed pin — the assertion is still an
    exact set, and the transport pins below
    (`test_staging_workbench_view_has_no_write_path`,
    `test_create_transport_uses_the_injected_fetcher_spelling`) are untouched: no
    new request site, no second body definition."""
    out = _run_create(CREATE_CASES, tmp_path)
    assert out["route"] == "/actions/gate/create-document"
    assert "create-document" in gate_routes_mod.EXECUTING_VERBS
    body = out["scopes"]["staged"]["request"]
    assert set(body) == {"area", "title", "summary", "topics",
                         "repository_context", "repository", "kind", "status",
                         "source", "scope_kind", "scope_id", "continuation"}
    # the registry key the route confines the write to, and the header field —
    # seeded from the same selected snapshot, carried as two separate values
    assert body["repository"] == body["repository_context"]
    assert body["title"] == "T" and body["summary"] == "S"
    assert body["area"] == "ideation/staging/topic-x/"
    assert body["status"] == "brainstorm"   # every area (open question 1's ruling)
    # the workbench spells a staged tile `staged`; the session's scope vocabulary
    # spells it `staged-topic`, and the MODEL owns the mapping (T023a)
    assert body["scope_kind"] == "staged-topic"
    assert body["scope_id"] == "topic-x"
    assert body["scope_kind"] in gate_routes_mod.branch_session.SCOPE_KINDS
    # a cluster and a possible carry their own kind verbatim
    assert out["scopes"]["cluster"]["request"]["scope_kind"] == "cluster"
    assert out["scopes"]["possible"]["request"]["scope_kind"] == "possible"
    # and the route accepts it (hermetic: a tmp checkout, no server needed).
    # No session registry is declared here, so there is nowhere liveness could
    # live and the route takes its PRE-SESSION path — byte-identical, which is
    # what keeps `create-document` outside a session unchanged (FR-018).
    root = tmp_path / "checkout"
    root.mkdir()
    status, payload = gate_routes_mod.run_gate_action(
        "create-document", body, checkout_root=root, actor="brett",
        snapshot_path=None,
        # the repository half the SERVE supplies on every call (finding 8): the
        # body names the repository the page is reading, and the route confines
        # the write to the repository it is served from. Naming one the server
        # cannot honour — or cannot check — refuses; that arm has its own test in
        # test_session_confinement.py.
        repository=body["repository"])
    assert status == 200 and payload["ok"] is True
    assert payload["path"] == "ideation/staging/topic-x/t.md"
    assert "ref" not in payload and "commit" not in payload


def test_gate_off_descriptor_is_the_real_cli_invocation(tmp_path):
    """Design D8: with the gate capability absent the affordance renders the
    exact `cli.py gate create-document ...` command. Pinned by PARSING it with
    the real CLI parser — a descriptor the CLI would reject is a broken promise."""
    import shlex

    from ideation_dashboard import cli

    command = _run_create(CREATE_CASES, tmp_path)["scopes"]["staged"]["command"]
    assert command.startswith("python3 scripts/ideation_dashboard/cli.py "
                              "gate create-document ")
    argv = shlex.split(command)[2:]          # drop `python3 <script>`
    args = cli.build_parser().parse_args(argv)
    assert args.func is cli.cmd_gate_create_document
    assert args.actor == "brett"
    assert args.area == "ideation/staging/topic-x/"
    assert args.status == "brainstorm"
    assert args.topics == "alpha"            # the LIVE checked set, on the lens tab
    assert args.repository_context == "fixture-repo"
    assert "keyword-lens recipe" in args.source
    # the human values are placeholders until typed, never invented
    assert args.title == "<title>"
    assert args.summary == "<one-sentence summary>"


# ---- write-path enforcement (task 4.6 + add-workbench-bullseye-and-create) --------

def test_staging_workbench_view_has_no_write_path():
    """The staging workbench VIEW carries no transport: it issues no fetch of its
    own (the outline reads /source ONLY through viewer.js's renderViewer, so the
    bundle keeps its fixed fetch call sites), no POST, and no XHR — the ONE write
    the surface performs (the `create-document` gate verb) lives in the sibling
    swb-create.js, which takes an injected fetcher. The pure model module still
    imports nothing at all (the node-harness standalone rule)."""
    view = (WEB / "views" / "staging-workbench.js").read_text(encoding="utf-8")
    assert "fetch(" not in view
    assert "POST" not in view.replace("no POST", "")  # prose states the rule; code has none
    assert "XMLHttpRequest" not in view
    model = MODEL_JS.read_text(encoding="utf-8")
    assert "fetch(" not in model
    assert not re.findall(r"^\s*import\s", model, re.MULTILINE), \
        "the pure model module must stay import-free (node-harness standalone)"


CREATE_JS = WEB / "views" / "swb-create.js"


def test_create_transport_uses_the_injected_fetcher_spelling():
    """Design D5: the create request lives in the sibling module and uses the
    `doFetch` spelling dispose.js / gate.js / lens.js established — which is what
    keeps it out of test_renderer.py's pinned set of `fetch(`-bearing bundle
    files, and what makes the transport injectable for tests."""
    body = CREATE_JS.read_text(encoding="utf-8")
    assert "const doFetch = fetcher || fetch;" in body
    assert "doFetch(" in body
    assert "fetch(" not in body          # the case-sensitive bundle pin
    assert "XMLHttpRequest" not in body
    assert body.count("method: \"POST\"") == 1   # exactly ONE write, not a family
    # the route the browser calls is the model's single constant, not a literal
    assert 'from "./staging-workbench-model.js"' in body
    assert "CREATE_ROUTE" in body
    # every dynamic value binds through helpers.el's textContent; innerHTML is
    # only ever cleared
    for m in re.finditer(r"\.innerHTML\s*=\s*([^;]+);", body):
        assert m.group(1).strip() == '""', \
            f"non-clearing innerHTML assignment: {m.group(0)!r}"


def test_a_running_write_says_so_on_its_own_button():
    """Brett, 2026-08-10: "i pressed create twice", and the log says what that
    cost. Press one opened the session, committed the document and regenerated
    the session snapshot, then answered `200` — 90 seconds later, contending
    with press two. Press two JOINED that session, found the document already
    there, and answered `409 corpus documents are create-only` in 15 seconds.
    So the FIRST answer the human read was the refusal of their own duplicate,
    for work that had in fact landed.

    `disabled` alone caused it: it says "not now" and nothing about "working".
    Both write buttons now carry a RUNNING LABEL for as long as the request is
    in flight, restored in `finally` so a refusal is retriable in place with
    its own words back on the button — the same shape notebook.js's action
    already used ("opening NotebookLM…")."""
    create = CREATE_JS.read_text(encoding="utf-8")
    session = (WEB / "views" / "swb-session.js").read_text(encoding="utf-8")
    for name, body in (("swb-create.js", create), ("swb-session.js", session)):
        assert "const label = submit.textContent;" in body, name
        assert "submit.disabled = true;" in body, name
        assert "} finally {\n      submit.textContent = label;\n    }" in body, name
        # the running label must be SET before the await and never left behind
        assert body.index("submit.textContent = ") < body.index("} finally {"), name
    # the create names what the wait is FOR — a create is not a file write, it
    # opens a branch session, which is why it takes as long as it does. The
    # DEFAULT is stated here and a host may name its own (the draft view says
    # "saving…", because from there the human is saving a document they can
    # already see — Brett, 2026-08-10).
    assert ('submit.textContent = o.runningLabel '
            '|| "creating… (opening the branch session)";') in create
    assert '"saving… (opening the branch session)"' in (
        WEB / "views" / "staging-workbench.js").read_text(encoding="utf-8")
    assert 'submit.textContent = label + "…";' in session


def test_workbench_posture_and_affordances_are_capability_derived():
    """Tasks 5.1/5.7/5.9: `caps` is threaded in from app.js's ONE probe, the
    posture pill is derived from it (the hosted image keeps the exact `read-only`
    string it shows today), and no create control is rendered without it.

    The mount's seam list GREW on 2026-07-26 (007-workbench-branch-sessions T082)
    by `active` + `index` — the ACTIVE (repository, ref) key and the serving
    index's roster, which are what make the SESSION posture honest (FR-045). Both
    are read-only inputs app.js already holds; neither is a transport.

    It grew by ONE more on 2026-07-27 (PR #49 review finding 16): `sourceBase`,
    the ACTIVE key's own keyed `/source/` base, which app.js already computes at
    the same place for the explorer/viewer. Without it the OUTLINE pane's viewer
    fell back to the unkeyed `/source/` and the server resolved that to the
    active (main) entry, so a DRAFT view's outline rendered `main`'s bytes or
    404'd. Also a read-only input app.js already holds, and still not a
    transport — the viewer owns the fetch, exactly as it did before."""
    view = (WEB / "views" / "staging-workbench.js").read_text(encoding="utf-8")
    create = CREATE_JS.read_text(encoding="utf-8")
    app = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "app.js").read_text(
        encoding="utf-8")
    # the mount takes caps + fetcher, and app.js hands the probe's verdict over
    assert "{ onOpenDoc, caps, fetcher, active, index," in view
    # …and by ONE more on 2026-07-28 (T092 acceptance sweep, defect 5):
    # `onSessionRekey`, the shell's answer to "the create just opened a branch
    # session". The overlay carries no transport, so app.js owns the fetch and
    # the overlay adopts what it returns — the same division as every other seam
    # on this list.
    assert "sourceBase, edit, onSessionRekey," in view
    assert "onSessionEnded, onScopeOpened } = {})" in view
    assert "mountStagingWorkbench(" in app and "caps, active, index," in app
    assert "sourceBase: workbenchSourceBase, edit: workbenchEdit," in app
    assert "onScopeOpened: routeWorkbenchScope, onSessionRekey: rekeyToSession," in app
    assert "onSessionEnded: resetEndedSession });" in app
    assert "let shellSnapshot = snapshot;" in view
    assert "let shellActive = active;" in view
    opened = view.split("function open(kind, id) {", 1)[1].split(
        "\n  }\n\n  return { open, close };", 1)[0]
    assert opened.index("snapshot = shellSnapshot;") \
        < opened.index("index = shellIndex;") \
        < opened.index("scope = workbenchScope(snapshot, kind, id);") \
        < opened.index("const routed = onScopeOpened(scope.ref);") \
        < opened.index("sourceBase = routed.sourceBase;") \
        < opened.index("drawTab();"), opened
    ending = view.split("onSessionEnded: async () => {", 1)[1].split(
        "\n      },", 1)[0]
    assert ending.index("const next = await onSessionEnded();") \
        < ending.index("const shellWasCurrent =") \
        < ending.index("snapshot = next.snapshot;") \
        < ending.index("index = next.index;") \
        < ending.index("if (shellWasCurrent) {") \
        < ending.index("shellSnapshot = snapshot;") \
        < ending.index("scope = workbenchScope(snapshot, scope.kind, scope.id);") \
        < ending.index("drawTab();"), ending
    session = SESSION_JS.read_text(encoding="utf-8")
    assert "await o.onSessionEnded(result, ending);" in session
    assert "const ending = await renderOutcome(" in session
    # PIN EVOLUTION (T104 F1): `rekeyToSession` now delegates to
    # `adoptSessionRef`, the ONE adoption path a session key change takes --
    # the create's re-key and the governed Save's hand-off both arrive there,
    # so the shell can no longer follow a session on one route and not the
    # other. The re-scope assertion moves to that function; the pin itself
    # (re-derive the scope from the adopted snapshot, never a `rescoped`
    # fallback) is unchanged.
    assert "return adoptSessionRef(ref);" in view
    rekey = view.split("function adoptSessionRef(ref, {", 1)[1].split(
        "\n  }\n", 1)[0]
    assert "scope = workbenchScope(snapshot, scope.kind, scope.id);" in rekey
    assert "if (rescoped) scope = rescoped;" not in rekey
    # the pill is a branch on the capability, never a constant
    assert 'gateOn ? "gate: create-document" : "read-only"' in view
    assert "createGateLive(caps)" in view
    # gate-off renders the descriptor and returns BEFORE any live control exists
    assert "if (!createGateLive(o.caps)) return renderDescriptor(host, seed, o);" in create
    assert "createDocumentCommand(" in create


def test_lens_tab_seeds_its_create_from_the_live_checked_session():
    """Regression pin (caught by the Playwright pass, not by the pure tests): the
    lens tab's affordance and its bullseye gesture must both be handed the LIVE
    checked set, or the dialog opens with an empty `Topics:` and a "checked none"
    recipe citation while the rail plainly shows a selection. A SECTOR narrows
    only the topics seed (`subset`) and still rides on the same live object, so
    the recipe citation cannot lose the real selection either."""
    view = (WEB / "views" / "staging-workbench.js").read_text(encoding="utf-8")
    assert "const live = { slot: dialog, checked: [...session.checked] };" in view
    assert 'create.mount(forming, "lens", live)' in view
    assert 'create.open(dialog, "lens",' in view
    assert "{ ...live, subset: [...region.keywords] }" in view
    # the non-sector path (centre region) passes `live` untouched
    assert ": live)" in view


# ---- against the real fixture snapshot ------------------------------------------

def test_scopes_derive_from_the_real_fixture_snapshot(tmp_path):
    snap = generate_snapshot(BASE_REPO, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit())
    cluster_id = snap["clusters"][0]["id"]
    staging_id = snap["staged_topics"][0]["staging_id"]
    cases = [
        ("real-cluster", snap, "cluster", cluster_id),
        ("real-staged", snap, "staged", staging_id),
    ]
    r = _run_scopes(cases, tmp_path)["scopes"]
    cluster = r["real-cluster"]
    assert cluster is not None
    assert cluster["counts"]["documents"] == \
        len(snap["clusters"][0]["document_edges"])
    # every resolved row carries the generator's completeness object verbatim
    for section in cluster["sections"]:
        for row in section["documents"]:
            if row["resolved"]:
                assert row["completeness"] is not None
                assert set(row["completeness"]) == \
                    {"score", "structure", "length", "open_markers",
                     "keyword_coverage", "link_degree"}
    staged = r["real-staged"]
    assert staged is not None
    assert staged["outline"]["stagingId"] == staging_id


# ==========================================================================
# THE SESSION SURFACE (007-workbench-branch-sessions Phase 9, T076-T079)
#
# The workbench grew THREE live session affordances (edit, save, abandon) plus a
# DESCRIPTOR-ONLY notebook re-sync (spec C10), an honest session posture
# indicator (FR-045), and a gate-off posture in which every one of them is a
# copyable CLI descriptor and no session write is reachable from the page
# (FR-046). The renderer boundary is the delicate part, so it is pinned three
# ways:
#
#   * the VIEW and the pure MODEL stay transport-free — no `fetch(`, no `POST`,
#     no `XMLHttpRequest`, and the model still imports nothing (T076);
#   * the NEW sibling `swb-session.js` matches the transport spelling literally,
#     with exactly ONE `method: "POST"` even though it addresses THREE routes —
#     one shared request helper, route constants in the pure model (T077);
#   * every descriptor is asserted by PARSING it with the REAL CLI parser, so a
#     gate-off page cannot promise a command the terminal would reject (T079).
# ==========================================================================

SESSION_JS = WEB / "views" / "swb-session.js"
APP_JS = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "app.js"

_SESSION_HARNESS = """
import {
  workbenchScope, lensScopeSnapshot, lensSessionSeed,
  sessionPosture, sessionRequest, sessionCommand, notebookRefreshCommand,
  sessionBranchBase, sessionOrdinal, sessionRefs, tileSessionRefs,
  sessionActionsLive, sessionSurfaceHidden, sessionRoute, createSeed, createRequest,
  createDocumentCommand, normalizeContinuation,
  advertisedTiles, otherTileBranches,
  SESSION_AFFORDANCES, LIVE_SESSION_AFFORDANCES, DESCRIPTOR_ONLY_AFFORDANCES,
  SESSION_VERBS, SESSION_LABELS, CONTINUATIONS, MAIN_REF,
} from './staging-workbench-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const snapshot = cases.snapshot;
// one snapshot per posture case, so a case can grow the TILE INVENTORY the G12
// question is asked against (finding 18) without changing every other case
const snapshots = { main: snapshot, sibling: cases.siblingSnapshot };

function scopeOf(kind, id, snap) {
  return workbenchScope(snap || snapshot, kind, id) || { kind, id };
}

const postures = {};
for (const [id, kind, tileId, rawOpts] of cases.postures) {
  const { snapshotKey, ...opts } = rawOpts;
  const snap = snapshots[snapshotKey || 'main'];
  postures[id] = sessionPosture(scopeOf(kind, tileId, snap),
                                { snapshot: snap, ...opts });
}

const branches = cases.branches.map(([kind, id]) => sessionBranchBase({ kind, id }));
const ordinals = cases.ordinals.map(([ref, base]) => sessionOrdinal(ref, base));

const scope = scopeOf('staged', 'topic-x');
const requests = {};
const commands = {};
for (const affordance of SESSION_AFFORDANCES) {
  requests[affordance] = sessionRequest(affordance, scope, cases.values);
  commands[affordance] = sessionCommand(affordance,
    { ...cases.values, scope, actor: 'brett', branch: 'draft/topic-x' });
}

// The UI-lifetime WORKBENCH session (design D14) is a different object entirely
// from the BRANCH session posture: neither carries the other's keys, which is
// what makes the two impossible to confuse in a view.
const lensSession = lensSessionSeed(null, lensScopeSnapshot(snapshot, scope), scope);

// The create body's `continuation` field (FR-025's answer token), which the
// workbench transport now carries (T082) — the ONE payload definition.
const createSeeded = createSeed(snapshot, scope, 'docs', {});
console.log(JSON.stringify({
  postures, branches, ordinals, requests, commands,
  affordances: SESSION_AFFORDANCES,
  live: LIVE_SESSION_AFFORDANCES,
  descriptorOnly: DESCRIPTOR_ONLY_AFFORDANCES,
  verbs: SESSION_VERBS,
  labels: SESSION_LABELS,
  mainRef: MAIN_REF,
  routes: SESSION_AFFORDANCES.map((a) => [a, sessionRoute(a)]),
  capabilityVerdicts: cases.caps.map((c) => sessionActionsLive(c)),
  surfaceHidden: cases.caps.map((c) => sessionSurfaceHidden(c)),
  refs: cases.refs.map(([index, repository]) => sessionRefs(index, repository)),
  family: cases.family.map(([refs, kind, id]) => tileSessionRefs(refs, { kind, id })),
  lensSessionKeys: Object.keys(lensSession).sort(),
  postureKeys: Object.keys(postures.draft_own).sort(),
  continuations: CONTINUATIONS,
  normalizedContinuations: cases.continuations.map((c) => normalizeContinuation(c)),
  createBody: createRequest(createSeeded, { title: 'T', summary: 'S' }),
  createResumeBody: createRequest(createSeeded,
    { title: 'T', summary: 'S', continuation: 'resume' }),
  createResumeCommand: createDocumentCommand(
    { ...createSeeded, title: 'T', summary: 'S', continuation: 'new' },
    { actor: 'brett' }),
  notebookDryRun: notebookRefreshCommand({ branch: 'draft/topic-x' }),
  notebookApply: notebookRefreshCommand({ branch: 'draft/topic-x', apply: true }),
  // the page's own tile inventory (finding 18), and the G12 map derived from it
  advertised: cases.inventories.map((key) =>
    advertisedTiles(snapshots[key]).map((t) => [t.kind, t.id])),
  otherBranches: cases.others.map(([key, kind, id]) =>
    [...otherTileBranches(snapshots[key], { kind, id }).entries()]
      .map(([branch, tile]) => [branch, tile.kind, tile.id])),
  // the command the card would hand the human for each posture case — the
  // artifact finding 18 is actually about
  notebookForPosture: Object.fromEntries(Object.entries(postures).map(
    ([id, posture]) => [id, notebookRefreshCommand({ posture, apply: true })])),
}));
"""

# One index shape per posture case. The serving index advertises a LIVE session
# as an ordinary (repository, ref) row — that is the roster FR-014 validates a
# session key against — so the posture reads the roster rather than inventing a
# second liveness signal.
_MAIN_ONLY_INDEX = {"entries": [{"repository": "fixture-repo", "ref": "main"}]}
_SESSION_INDEX = {"entries": [
    {"repository": "fixture-repo", "ref": "main"},
    {"repository": "fixture-repo", "ref": "draft/topic-x"},
]}
_ORDINAL_INDEX = {"entries": [
    {"repository": "fixture-repo", "ref": "main"},
    {"repository": "fixture-repo", "ref": "draft/topic-x"},
    {"repository": "fixture-repo", "ref": "draft/topic-x-2"},
]}
# THE FINDING-18 WORLD: the inventory grows a SIBLING tile whose own
# deterministic branch is `draft/topic-x-2` — a staging folder is just a folder
# name, so this needs no collision machinery at all. It is also exactly the state
# the mandatory T049(c) engine test builds.
SIBLING_SNAP = {
    **_hand_snapshot(),
    "staged_topics": [*_hand_snapshot()["staged_topics"],
                      {"staging_id": "topic-x-2", "files": []}],
}

_OTHER_TILE_CASES = [
    ["main", "staged", "topic-x"],        # no sibling: nothing is another tile's
    ["sibling", "staged", "topic-x"],     # the sibling owns draft/topic-x-2
    ["sibling", "staged", "topic-x-2"],   # …and from ITS side, topic-x owns the base
]

# the roster in T049(c)'s state: ONLY the sibling tile's session is live
_SIBLING_ONLY_INDEX = {"entries": [
    {"repository": "fixture-repo", "ref": "main"},
    {"repository": "fixture-repo", "ref": "draft/topic-x-2"},
]}
_MAIN = {"repository": "fixture-repo", "ref": "main"}
_ON_DRAFT = {"repository": "fixture-repo", "ref": "draft/topic-x"}
_ON_DRAFT_2 = {"repository": "fixture-repo", "ref": "draft/topic-x-2"}
_ON_OTHER = {"repository": "fixture-repo", "ref": "draft/other-topic"}

_POSTURE_CASES = [
    # no index at all (a static image, an older server): nothing claims a session
    ("no_index", "staged", "topic-x", {"active": None, "index": None,
                                      "repository": "fixture-repo"}),
    ("main_only", "staged", "topic-x", {"active": _MAIN, "index": _MAIN_ONLY_INDEX}),
    # a session is live on the tile, but THIS view is main
    ("live_elsewhere", "staged", "topic-x", {"active": _MAIN, "index": _SESSION_INDEX}),
    # the view IS the session — the draft view
    ("draft_own", "staged", "topic-x", {"active": _ON_DRAFT, "index": _SESSION_INDEX}),
    # an ordinal family: the tile's ONE session is the HIGHEST ordinal
    ("draft_ordinal", "staged", "topic-x", {"active": _ON_DRAFT_2, "index": _ORDINAL_INDEX}),
    ("ordinal_from_main", "staged", "topic-x", {"active": _MAIN, "index": _ORDINAL_INDEX}),
    # a draft view that is ANOTHER tile's session
    ("draft_foreign", "staged", "topic-x", {"active": _ON_OTHER, "index": _SESSION_INDEX}),
    # this page-lifetime ENDED the session (a merged save / an abandon): the
    # affordances re-derive from the same derivation, and the ref is still NAMED
    ("ended", "staged", "topic-x", {"active": _MAIN, "index": _SESSION_INDEX,
                                   "ended": ["draft/topic-x"]}),
    # ...including when the page is sitting ON the ref that just ended, which must
    # NOT read as a stranger's session
    ("ended_on_ref", "staged", "topic-x", {"active": _ON_DRAFT,
                                           "index": _SESSION_INDEX,
                                           "ended": ["draft/topic-x"]}),
    ("cluster", "cluster", "cl-alpha", {"active": _MAIN, "index": _MAIN_ONLY_INDEX}),
    # a create OPENED the session one click ago: the boot-time roster cannot know
    # it, so the page-lifetime overlay is what keeps the indicator honest
    ("just_opened", "staged", "topic-x", {"active": _MAIN,
                                          "index": _MAIN_ONLY_INDEX,
                                          "repository": "fixture-repo",
                                          "opened": ["draft/topic-x"]}),
    # opened AND then ended in the same page life
    ("opened_then_ended", "staged", "topic-x", {"active": _MAIN,
                                                "index": _MAIN_ONLY_INDEX,
                                                "repository": "fixture-repo",
                                                "opened": ["draft/topic-x"],
                                                "ended": ["draft/topic-x"]}),
    # FINDING 18: the roster's ONLY family ref is the SIBLING tile's own branch.
    # This is T049(c)'s state, from the tile that does NOT own the session.
    ("sibling_owns_the_ordinal", "staged", "topic-x",
     {"active": _MAIN, "index": _SIBLING_ONLY_INDEX, "snapshotKey": "sibling"}),
    # …and from the tile that DOES own it: its own base name is now another tile's
    # nothing, so the session is plainly its own
    ("sibling_is_its_own_session", "staged", "topic-x-2",
     {"active": _MAIN, "index": _SIBLING_ONLY_INDEX, "snapshotKey": "sibling"}),
    # the page sitting ON the ambiguous ref: still unmerged work, still not a
    # claim about whose session it is
    ("on_the_ambiguous_ref", "staged", "topic-x",
     {"active": _ON_DRAFT_2, "index": _SIBLING_ONLY_INDEX,
      "snapshotKey": "sibling"}),
    # this tile's OWN session at the base name, with the sibling's ordinal ALSO on
    # the roster: the own session is reported and never hidden by the sibling
    ("own_session_beside_a_sibling_ordinal", "staged", "topic-x",
     {"active": _MAIN, "index": _ORDINAL_INDEX, "snapshotKey": "sibling"}),
]

_BRANCH_CASES = [["staged", "topic-x"], ["cluster", "cl-alpha"],
                 ["possible", "pos-1"],
                 # a colon-qualified corpus staging id reduces to its final
                 # segment (research R2) — `:` is not a legal ref character
                 ["staged", "openxFactory:staging:demo-topic"],
                 # a path-shaped id opens no branch in another namespace
                 ["staged", "evil/../main"], ["nope", "topic-x"], ["staged", ""]]

_ORDINAL_CASES = [["draft/topic-x", "draft/topic-x"],
                  ["draft/topic-x-2", "draft/topic-x"],
                  ["draft/topic-x-11", "draft/topic-x"],
                  # NOT family members (branch_session.ordinal_of's strictness)
                  ["draft/topic-x-02", "draft/topic-x"],
                  ["draft/topic-x-and-more", "draft/topic-x"],
                  ["draft/topic-xical", "draft/topic-x"],
                  ["draft/other", "draft/topic-x"]]

_CAP_CASES = [
    {"actions": {"gate": True, "session": True}},
    {"actions": {"gate": True}},              # an older server: gate implies session
    {"actions": {"gate": True, "session": False}},   # the HOSTED plane (FR-048)
    {"actions": {"gate": False, "session": True}},
    {"actions": {}},
    None,
]

_REF_CASES = [
    [_ORDINAL_INDEX, "fixture-repo"],
    [_ORDINAL_INDEX, "other-repo"],
    [None, "fixture-repo"],
]

_FAMILY_CASES = [
    [["draft/topic-x-2", "draft/topic-x"], "staged", "topic-x"],
    [["draft/topic-x", "draft/other"], "staged", "topic-x"],
    [["cluster/cl-alpha"], "cluster", "cl-alpha"],
]

_SESSION_VALUES = {
    "document": "ideation/staging/topic-x/topic-x.md",
    "content": "# Replacement\n",
    "reason": "the exploration stopped",
    "contentFile": "/tmp/replacement.md",
}

_CONTINUATION_CASES = [None, "", "resume", "NEW", " new ", "restart"]


def _run_session(tmp_path):
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(MODEL_JS, tmp_path / "staging-workbench-model.mjs")
    (tmp_path / "harness.mjs").write_text(_SESSION_HARNESS, encoding="utf-8")
    cases_path = tmp_path / "session-cases.json"
    cases_path.write_text(json.dumps({
        "snapshot": SNAP, "siblingSnapshot": SIBLING_SNAP,
        "postures": _POSTURE_CASES, "branches": _BRANCH_CASES,
        "ordinals": _ORDINAL_CASES, "caps": _CAP_CASES, "refs": _REF_CASES,
        "family": _FAMILY_CASES, "values": _SESSION_VALUES,
        "continuations": _CONTINUATION_CASES,
        "inventories": ["main", "sibling"],
        "others": _OTHER_TILE_CASES,
    }), encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "harness.mjs"), str(cases_path)],
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


# ---- T076: the view and the model stay transport-free -------------------------

def test_the_session_surface_added_no_transport_to_the_view_or_the_model():
    """T076 / FR-044: the workbench gained three LIVE session affordances, and
    neither the view nor its pure model gained a transport for any of them.

    Deliberately STRICTER than the pre-existing pin above
    (`test_staging_workbench_view_has_no_write_path`, which must still pass
    UNMODIFIED): the write method is banned from the MODEL too, and `import(`
    from both. The session ROUTES live in the pure model as constants — one
    definition the node harness and the Python route tests both read — while the
    only module that calls one is the sibling transport.

    The method ban is a WORD-boundary match here rather than the substring the
    older pin uses, because the model legitimately contains the word POSTURE (the
    FR-045 derivation). A word-boundary match is the stricter reading of the same
    rule — the substring form would have to be weakened to a `.replace()` to cope,
    which is exactly the direction a pin must never move."""
    view = (WEB / "views" / "staging-workbench.js").read_text(encoding="utf-8")
    model = MODEL_JS.read_text(encoding="utf-8")
    for name, body in (("staging-workbench.js", view),
                       ("staging-workbench-model.js", model)):
        assert "fetch(" not in body, f"{name} carries a transport"
        assert not re.search(r"\bPOST\b", body), f"{name} names a write method"
        assert "XMLHttpRequest" not in body, f"{name} carries an XHR"
        assert "import(" not in body, f"{name} carries a dynamic import"
    assert not re.findall(r"^\s*import\s", model, re.MULTILINE), \
        "the pure model module must stay import-free (node-harness standalone)"
    # the three session routes are MODEL constants; the view names none of them
    for route in ("/actions/gate/edit-document", "/actions/gate/open-pr",
                  "/actions/gate/abandon-session"):
        assert route in model, f"{route} is not a model constant"
        assert route not in view, f"the view names the route {route}"
    assert "/actions/" not in view
    # the view reaches the transport ONLY through the sibling module
    assert 'from "./swb-session.js"' in view
    # and the pre-existing pin is still THE pin: a clobber cannot pass by
    # deleting the assertion it was supposed to satisfy
    own = Path(__file__).read_text(encoding="utf-8")
    assert "def test_staging_workbench_view_has_no_write_path" in own
    assert 'assert "POST" not in view.replace("no POST", "")' in own


# ---- T077: the transport spelling, literally ---------------------------------

def test_session_transport_uses_the_injected_fetcher_spelling():
    """T077 / FR-044, plan Constraint 11: the NEW session transport matches the
    pinned spelling `swb-create.js` established, character for character — which
    is what keeps it OUT of test_renderer.py's `fetch(`-bearing file set and what
    makes the transport injectable for tests.

    THREE routes, ONE `method: "POST"`: the pin allows exactly one write literal
    per transport file, so the three session verbs share ONE request helper and
    select their route from the pure model's constants. That is the pin's design,
    not a way around it — a second POST literal here would mean a second,
    unreviewed write site."""
    body = SESSION_JS.read_text(encoding="utf-8")
    assert "const doFetch = fetcher || fetch;" in body
    assert "doFetch(" in body
    assert "fetch(" not in body          # the case-sensitive bundle pin
    assert "XMLHttpRequest" not in body
    assert "import(" not in body
    assert body.count("method: \"POST\"") == 1, \
        "three session routes share ONE request helper (plan Constraint 11)"
    # the ONE request helper: its definition plus its TWO call sites -- the
    # session-bar affordances and the doxBench Save transport (T080, 2026-07-30);
    # both ride the same single write-method literal above
    assert body.count("submitSession(") == 3
    # routes and payloads come from the pure model, never from a literal here
    assert 'from "./staging-workbench-model.js"' in body
    for symbol in ("sessionRoute", "sessionRequest", "sessionCommand",
                   "sessionActionsLive"):
        assert symbol in body, f"{symbol} is not consulted by the transport"
    assert "/actions/gate/" not in body, \
        "a route literal in the transport would be a second definition"
    # session refusals render in dispose.js's panel, identically to every other
    # refusal on the page (research R6)
    assert 'from "./dispose.js"' in body
    assert "panelEntry(" in body
    # every dynamic value binds through helpers.el's textContent; innerHTML is
    # only ever cleared
    for m in re.finditer(r"\.innerHTML\s*=\s*([^;]+);", body):
        assert m.group(1).strip() == '""', \
            f"non-clearing innerHTML assignment: {m.group(0)!r}"


def test_the_session_transport_addresses_exactly_the_three_live_routes(tmp_path):
    """T077: four affordances, THREE routes. `refresh-notebook` resolves to NO
    route at all (spec C10) — it is not a gate verb, so a route for it would be
    an artifact no contract declares."""
    out = _run_session(tmp_path)
    assert out["affordances"] == ["edit", "save", "abandon", "refresh-notebook"]
    assert out["live"] == ["edit", "save", "abandon"]
    assert out["descriptorOnly"] == ["refresh-notebook"]
    assert dict(out["routes"]) == {
        "edit": "/actions/gate/edit-document",
        "save": "/actions/gate/open-pr",
        "abandon": "/actions/gate/abandon-session",
        "refresh-notebook": None,
    }
    # every live route is a verb the engine actually executes
    for affordance, verb in out["verbs"].items():
        assert verb in gate_routes_mod.EXECUTING_VERBS, verb
        assert dict(out["routes"])[affordance].endswith(verb)
    assert "refresh-notebook" not in out["verbs"]
    assert "refresh-notebook" not in gate_routes_mod.EXECUTING_VERBS


def test_the_session_request_bodies_match_the_route_contracts(tmp_path):
    """T077: the three request bodies are exactly the bodies the routes validate
    — pinned from BOTH sides, by handing each one to the real body parser."""
    out = _run_session(tmp_path)
    edit = out["requests"]["edit"]
    assert set(edit) == {"scope_kind", "scope_id", "document", "content"}
    assert edit["scope_kind"] == "staged-topic" and edit["scope_id"] == "topic-x"
    parsed, err = gate_routes_mod._edit_body(edit)
    assert err is None and parsed["document"] == edit["document"]
    save = out["requests"]["save"]
    assert set(save) == {"scope_kind", "scope_id"}      # title/body both optional
    parsed, err = gate_routes_mod._open_pr_body(save)
    assert err is None and parsed["_scope"] == ("staged-topic", "topic-x")
    abandon = out["requests"]["abandon"]
    assert set(abandon) == {"scope_kind", "scope_id", "reason"}
    parsed, err = gate_routes_mod._abandon_body(abandon)
    assert err is None and parsed["reason"] == "the exploration stopped"
    # the descriptor-only affordance has NO body at all
    assert out["requests"]["refresh-notebook"] is None


# ---- T078: the session posture indicator -------------------------------------

def test_the_session_posture_names_the_branch_and_marks_the_draft_view(tmp_path):
    """T078 / FR-045: the indicator is honest about three separate things — that
    a branch session is ACTIVE, WHICH branch it is on, and whether THIS view is a
    draft view. It reads the serving index's roster (where a live session is an
    ordinary (repository, ref) row) plus the ACTIVE key, so it invents no second
    liveness signal."""
    p = _run_session(tmp_path)["postures"]
    # the draft view: the workbench is reading unmerged work, and says so
    own = p["draft_own"]
    assert own["draft"] is True and own["ownTile"] is True and own["live"] is True
    assert own["branch"] == "draft/topic-x"
    assert "DRAFT VIEW" in own["label"] and "draft/topic-x" in own["label"]
    # a live session the human is NOT currently viewing: named, not hidden
    elsewhere = p["live_elsewhere"]
    assert elsewhere["live"] is True and elsewhere["draft"] is False
    assert elsewhere["branch"] == "draft/topic-x"
    assert "DRAFT VIEW" not in elsewhere["label"]
    assert "main" in elsewhere["label"]
    # no session at all
    assert p["main_only"]["live"] is False and p["main_only"]["branch"] is None
    assert "no branch session" in p["main_only"]["label"]
    assert p["no_index"]["live"] is False and p["no_index"]["draft"] is False
    # the ordinal family: the tile's ONE session is the HIGHEST ordinal
    # (branch_session.live_session_branches joins live[-1])
    assert p["draft_ordinal"]["branch"] == "draft/topic-x-2"
    assert p["draft_ordinal"]["family"] == ["draft/topic-x", "draft/topic-x-2"]
    assert p["ordinal_from_main"]["branch"] == "draft/topic-x-2"
    # a draft view that belongs to ANOTHER tile is not claimed as this tile's
    foreign = p["draft_foreign"]
    assert foreign["draft"] is True and foreign["ownTile"] is False
    assert foreign["activeRef"] == "draft/other-topic"
    assert "another tile" in foreign["label"]
    # an ENDED session (a merged save, an abandon) stops being claimed as LIVE,
    # and is still NAMED — the affordance row keys its disabled state on
    # `posture.branch`, so a null here would silently re-offer a dead session
    assert p["ended"]["live"] is False
    assert p["ended"]["branch"] == "draft/topic-x"
    assert p["ended"]["endedBranch"] == "draft/topic-x"
    assert "ended" in p["ended"]["label"] and "draft/topic-x" in p["ended"]["label"]
    # and a page sitting ON the ref that just ended is told exactly that, never
    # that it is looking at another tile's session
    on_ref = p["ended_on_ref"]
    assert on_ref["live"] is False and on_ref["ownTile"] is False
    assert on_ref["branch"] == "draft/topic-x"
    assert "ENDED" in on_ref["label"]
    assert "another tile" not in on_ref["label"]
    # the base name is derived for every tile kind, session or not
    assert p["cluster"]["base"] == "cluster/cl-alpha"
    # a session OPENED one click ago is live even though the boot-time roster
    # advertises only `main` — otherwise the bar would read "no branch session"
    # immediately after opening one
    opened = p["just_opened"]
    assert opened["live"] is True and opened["branch"] == "draft/topic-x"
    assert "session live" in opened["label"]
    # ...and the two overlays compose: opened, then ended, in one page life
    both = p["opened_then_ended"]
    assert both["live"] is False and both["branch"] == "draft/topic-x"
    assert "ended" in both["label"]


def test_the_posture_never_claims_another_tiles_session_as_this_tiles(tmp_path):
    """PR #49 second-review finding 18. In exactly the state the mandatory T049(c)
    engine test builds — tile `topic-x-2` live at `draft/topic-x-2`, tile `topic-x`
    with no session — the card for `topic-x` announced "session live ·
    draft/topic-x-2" and built a copyable
    `sync-notebooklm-books.py … --session-ref draft/topic-x-2 --apply`, which
    re-syncs the OTHER tile's session notebook from the OTHER tile's worktree. The
    engine meanwhile refused every session verb on that tile.

    The page cannot know WHOSE session a ref is (the owner the OPEN recorded is not
    projected), so the honest answer is AMBIGUOUS — never this tile's, and never a
    command built against it."""
    out = _run_session(tmp_path)
    p = out["postures"]
    card = p["sibling_owns_the_ordinal"]

    assert card["live"] is False, "another tile's session is not this tile's"
    assert card["branch"] is None
    assert card["ambiguousRef"] == "draft/topic-x-2"
    assert card["ambiguousOwner"] == "topic-x-2"
    assert "AMBIGUOUS" in card["label"]
    assert "topic-x-2" in card["label"]
    assert "session live ·" not in card["label"]
    # the artifact the finding is about: no command is filled in with that ref
    command = out["notebookForPosture"]["sibling_owns_the_ordinal"]
    assert "draft/topic-x-2" not in command
    assert "--session-ref '<branch>'" in command

    # the OWNING tile is unaffected: its session is plainly its own
    owner = p["sibling_is_its_own_session"]
    assert owner["live"] is True and owner["branch"] == "draft/topic-x-2"
    assert owner["ambiguousRef"] is None
    assert "session live" in owner["label"]
    assert ("draft/topic-x-2"
            in out["notebookForPosture"]["sibling_is_its_own_session"])

    # a tile's OWN live session is never hidden by a sibling's ordinal being on
    # the roster too — that is the mirror-image defect (engine finding 6)
    both = p["own_session_beside_a_sibling_ordinal"]
    assert both["live"] is True and both["branch"] == "draft/topic-x"
    assert both["ambiguousRef"] == "draft/topic-x-2"
    assert "session live" in both["label"]
    assert "draft/topic-x-2" in both["detail"], "the ambiguity is still REPORTED"

    # and a page sitting ON the ambiguous ref is told what it is reading without
    # being told whose it is
    on_ref = p["on_the_ambiguous_ref"]
    assert on_ref["draft"] is True and on_ref["ownTile"] is False
    assert on_ref["live"] is False
    assert "AMBIGUOUS" in on_ref["label"]
    assert "another tile's session" not in on_ref["label"], \
        "'another tile's' is a claim this page cannot make either"


def test_the_pages_tile_inventory_is_the_engines_tile_inventory(tmp_path):
    """Finding 18's mechanism, pinned against the Python it mirrors:
    `advertisedTiles` reads the same three registers `discover_tile_inventory`
    unions, and `otherTileBranches` is `TileInventory.other_branches`."""
    from ideation_dashboard import branch_session as bs

    out = _run_session(tmp_path)
    inventories = {"main": SNAP, "sibling": SIBLING_SNAP}
    for key, tiles in zip(["main", "sibling"], out["advertised"]):
        snapshot = inventories[key]
        expected = ([["staged", t["staging_id"]] for t in snapshot["staged_topics"]]
                    + [["cluster", c["id"]] for c in snapshot["clusters"]]
                    + [["possible", p["id"]] for p in snapshot["possibles"]])
        assert tiles == expected, key

    kinds = {"staged": bs.STAGED_TOPIC, "cluster": bs.CLUSTER,
             "possible": bs.POSSIBLE}
    for (key, kind, tile_id), got in zip(_OTHER_TILE_CASES, out["otherBranches"]):
        snapshot = inventories[key]
        inventory = bs.TileInventory.from_scopes(
            staged_topics=[t["staging_id"] for t in snapshot["staged_topics"]],
            clusters=[c["id"] for c in snapshot["clusters"]],
            possibles=[p["id"] for p in snapshot["possibles"]])
        python_side = {
            branch: (tile.scope_kind, tile.scope_id) for branch, tile
            in inventory.other_branches(bs.Tile(kinds[kind], tile_id)).items()}
        js_side = {branch: (kinds[k], i) for branch, k, i in got}
        assert js_side == python_side, (key, kind, tile_id)


def test_the_posture_agrees_with_live_session_branches_on_ownership(tmp_path):
    """Finding 18's parity leg, which the suite did not have: the JS posture was
    only ever compared against `bs.ordinal_of`, so the two surfaces could disagree
    about WHOSE session a ref is and nothing noticed.

    The engine's answer for the T049(c) state is asserted here from the REAL
    `live_session_branches` over a two-tile inventory, in the three shapes the
    registry can be in — the owner recorded as the sibling, the owner recorded as
    this tile, and no owner at all. In NO shape is `draft/topic-x-2` tile
    `topic-x`'s live session, which is exactly what the page must not claim."""
    from ideation_dashboard import branch_session as bs
    from ideation_dashboard import snapshot_registry as reg

    inventory = bs.TileInventory.from_scopes(
        staged_topics=["topic-x", "topic-x-2"])
    mine = bs.Tile(bs.STAGED_TOPIC, "topic-x")
    sibling = bs.Tile(bs.STAGED_TOPIC, "topic-x-2")

    def registry_with(owner):
        registry = reg.SnapshotRegistry()
        entry = reg.SnapshotEntry(repository="fixture-repo", ref="draft/topic-x-2")
        entry.session_tile = bs.tile_key(owner)
        registry.register(entry)
        return registry

    # (a) the sibling owns it: the engine EXCLUDES it from this tile (T049(c))
    assert bs.live_session_branches(registry_with(sibling), "fixture-repo", mine,
                                    inventory=inventory) == ()
    assert bs.live_session_branches(registry_with(sibling), "fixture-repo", sibling,
                                    inventory=inventory) == ("draft/topic-x-2",)
    # (b) this tile owns it (its own second session): the engine reports it, and
    #     the page's ambiguity is the honest conservative answer for the same state
    assert bs.live_session_branches(registry_with(mine), "fixture-repo", mine,
                                    inventory=inventory) == ("draft/topic-x-2",)
    # (c) no owner recorded: the engine REFUSES rather than answering "no session"
    with pytest.raises(bs.CrossTileCollision):
        bs.live_session_branches(registry_with(None), "fixture-repo", mine,
                                 inventory=inventory)

    # the page's claim, against all three: it never says "this tile's live session"
    card = _run_session(tmp_path)["postures"]["sibling_owns_the_ordinal"]
    assert card["live"] is False and card["branch"] is None
    assert card["ambiguousRef"] == "draft/topic-x-2"


def test_the_session_branch_derivation_agrees_with_the_python_side(tmp_path):
    """T078: the browser derives a session branch name for the posture and for
    every descriptor, so a DRIFT from `branch_session.session_branch` would name
    a branch nobody is on. Pinned against the real Python derivation."""
    from ideation_dashboard import branch_session as bs

    out = _run_session(tmp_path)
    js = out["branches"]
    assert js[0] == bs.session_branch(bs.STAGED_TOPIC, "topic-x") == "draft/topic-x"
    assert js[1] == bs.session_branch(bs.CLUSTER, "cl-alpha") == "cluster/cl-alpha"
    assert js[2] == bs.session_branch(bs.POSSIBLE, "pos-1") == "possible/pos-1"
    # the colon-qualified corpus staging id reduces the same way (research R2)
    assert js[3] == bs.session_branch(bs.STAGED_TOPIC,
                                      "openxFactory:staging:demo-topic")
    # and every refused shape derives NOTHING rather than a wrong branch
    for name, scope_id in ((js[4], "evil/../main"), (js[6], "")):
        assert name is None
        with pytest.raises(bs.SessionRefused):
            bs.session_branch(bs.STAGED_TOPIC, scope_id)
    assert js[5] is None            # an unknown scope kind
    # the ordinal reader is exactly `branch_session.ordinal_of`'s strictness
    base = "draft/topic-x"
    for (ref, _b), got in zip(_ORDINAL_CASES, out["ordinals"]):
        assert got == bs.ordinal_of(ref, base), ref


def test_the_branch_session_posture_is_not_the_ui_workbench_session(tmp_path):
    """T078 / design D14: two different things are called a "session" here, and
    the view must never confuse them. The BRANCH session is derived state on a
    git branch; the WORKBENCH session is the UI-lifetime checked-keyword
    selection. Neither derivation carries the other's keys, and the posture is
    also distinct from the gate-capability pill: a plane can advertise the gate
    and still refuse sessions (the hosted plane, FR-048)."""
    out = _run_session(tmp_path)
    assert out["lensSessionKeys"] == ["checked", "key"]
    posture_keys = set(out["postureKeys"])
    assert {"branch", "draft", "live", "ownTile", "activeRef"} <= posture_keys
    assert not posture_keys & {"checked", "key"}
    # the capability question is its own derivation, and `session: false` wins
    # over an advertised gate (the hosted plane never gets a live session)
    assert out["capabilityVerdicts"] == [True, True, False, False, False, False]
    # …and "no live control" is NOT the same answer as "no session surface at
    # all" (PR #49 review finding 14): only the plane that explicitly declares
    # `session: false` — the HOSTED probe's own statement — hides the surface.
    # The gate-off local/static planes keep FR-046's descriptors.
    assert out["surfaceHidden"] == [False, False, True, False, False, False]
    # and the view renders them as SEPARATE elements: the gate pill keeps its
    # exact existing spelling, the posture chip is its own class
    view = (WEB / "views" / "staging-workbench.js").read_text(encoding="utf-8")
    assert 'gateOn ? "gate: create-document" : "read-only"' in view
    assert "swb-posture" in view
    assert "sessionPosture(" in view


def test_the_session_roster_reading_is_the_index_the_selector_already_reads(tmp_path):
    """T078: session liveness on the page comes from the SERVING index — the
    same roster the repository selector validates a key against — filtered to the
    active repository, because two repositories can carry the same tile id."""
    out = _run_session(tmp_path)
    assert out["refs"] == [["draft/topic-x", "draft/topic-x-2"], [], []]
    assert out["family"] == [["draft/topic-x", "draft/topic-x-2"],
                             ["draft/topic-x"], ["cluster/cl-alpha"]]
    assert out["mainRef"] == "main"


# ---- T079: gate-off, every affordance is a copyable CLI descriptor -----------

def test_gate_off_session_affordances_are_the_real_cli_invocations(tmp_path):
    """T079 / FR-046: with the gate capability absent every session affordance
    renders as a COPYABLE CLI DESCRIPTOR — asserted by PARSING each one with the
    REAL CLI parser, so a descriptor the terminal would reject is caught here."""
    import shlex

    from ideation_dashboard import cli

    out = _run_session(tmp_path)
    parser = cli.build_parser()
    expected = {"edit": cli.cmd_gate_edit_document,
                "save": cli.cmd_gate_open_pr,
                "abandon": cli.cmd_gate_abandon_session}
    for affordance, func in expected.items():
        command = out["commands"][affordance]
        assert command.startswith("python3 scripts/ideation_dashboard/cli.py gate "
                                  + out["verbs"][affordance] + " "), command
        args = parser.parse_args(shlex.split(command)[2:])
        assert args.func is func
        assert args.actor == "brett"
        assert args.scope_kind == "staged-topic"
        assert args.scope_id == "topic-x"
    # the edit descriptor carries the document and a --content-file (never
    # inline text, so a shell cannot mangle a document)
    edit = parser.parse_args(shlex.split(out["commands"]["edit"])[2:])
    assert edit.document == _SESSION_VALUES["document"]
    assert edit.content_file == _SESSION_VALUES["contentFile"]
    # the abandon descriptor carries the REQUIRED reason
    end = parser.parse_args(shlex.split(out["commands"]["abandon"])[2:])
    assert end.reason == _SESSION_VALUES["reason"]
    # save's title/body are OPTIONAL and are not invented when unfilled
    save = parser.parse_args(shlex.split(out["commands"]["save"])[2:])
    assert save.title is None and save.body_file is None


def test_the_notebook_refresh_is_a_descriptor_in_BOTH_gate_postures(tmp_path):
    """T079 / spec C10: `refresh-notebook` is the ONE affordance that renders as
    a descriptor with the gate capability PRESENT as well as absent — it is not a
    gate route and not a `gate` subcommand, so no transport, no route, and no
    `fetch` arithmetic belong to it. The line is FR-040's real invocation."""
    out = _run_session(tmp_path)
    dry = out["notebookDryRun"]
    # every interpolated value is SINGLE-quoted (PR #49 review finding 15): the
    # workspace-root placeholder carries `<`/`>` and the branch is derived from a
    # tile id the page did not author
    assert dry == ("python3 scripts/sync-notebooklm-books.py '<workspace root>' "
                   "--session-ref 'draft/topic-x'")
    assert out["notebookApply"] == dry + " --apply"
    # the flags are the sync script's real ones, and there is no route or verb
    sync = (REPO_ROOT / "scripts" / "sync-notebooklm-books.py").read_text(encoding="utf-8")
    assert '"--session-ref"' in sync and '"--apply"' in sync
    assert "refresh-notebook" not in gate_routes_mod.EXECUTING_VERBS
    for path in sorted(WEB.rglob("*.js")):
        body = path.read_text(encoding="utf-8")
        assert "refresh-notebook" not in body or path.name in {
            "staging-workbench-model.js", "swb-session.js"}
        assert "/actions/gate/refresh" not in body
    # the affordance is in the offered set and NOT in the live set
    assert "refresh-notebook" in out["affordances"]
    assert "refresh-notebook" not in out["live"]


def test_no_session_write_is_reachable_from_a_gate_off_page():
    """T079 / FR-046: gate-off, the mount returns the descriptors BEFORE any live
    control exists — the same early-return shape `swb-create.js` is pinned on —
    and the capability is asked exactly once, through the pure model's one
    derivation, so no branch of this file can reach a different verdict."""
    body = SESSION_JS.read_text(encoding="utf-8")
    assert ("if (!sessionActionsLive(o.caps)) "
            "return renderSessionDescriptors(host, ctx, o);") in body
    # ONE capability question, asked through the model — never re-derived here
    assert body.count("sessionActionsLive(") == 1
    assert "caps.actions" not in body
    # the descriptor renderer cannot reach the transport
    descriptors = body.split("function renderSessionDescriptors", 1)[1]
    descriptors = descriptors.split("\nfunction ", 1)[0]
    assert "submitSession" not in descriptors
    assert "sessionCommand(" in descriptors


def test_the_create_outcome_tells_the_shell_a_session_opened():
    """T082 / FR-045: the posture is derived from a roster fetched at BOOT, so a
    create that OPENS a session must tell the shell — otherwise the indicator reads
    "no branch session" one click after opening one, which is the exact dishonesty
    FR-045 exists to prevent.

    The wiring is the VIEW's, not a sibling-to-sibling import: `swb-create.js`
    raises the event and `staging-workbench.js` hands it to `swb-session.js`'s
    overlay, so the two transport modules stay independent of each other (the same
    reason app.js owns every cross-view jump)."""
    create = CREATE_JS.read_text(encoding="utf-8")
    view = (WEB / "views" / "staging-workbench.js").read_text(encoding="utf-8")
    session = SESSION_JS.read_text(encoding="utf-8")
    # the create reports the branch to the human AND to the shell
    assert 'box.appendChild(el("div", "swb-cline", "session branch: " + result.ref' in create
    assert "await onSessionOpened(result);" in create
    assert "await renderOutcome(result, payload" in create
    assert 'from "./swb-session.js"' not in create, \
        "the two transport modules must not depend on each other"
    # the view is the wiring, and it re-derives the bar — AND re-keys, since the
    # T092 acceptance sweep (defect 5). Redrawing the bar was ALL this used to do,
    # and this assertion pinned that: the page stayed keyed to `main`, where
    # FR-014a guarantees the created document is NOT, so the human read
    # `created ✓` beside `could not load … (HTTP 404)` and the rewrite picker
    # offered only the documents that predated their create. All three calls are
    # pinned in ORDER, because the order is the fix: the created path joins the
    # picker's overlay, the bar re-derives, and the shell re-keys to the session
    # ref. swb-create awaits that hand-off before its `onOpenDoc` jump, so the
    # source read and edit action change keys together only after the session
    # snapshot is ready.
    wiring = view.split("onSessionOpened: (result) => {", 1)[1].split("},", 1)[0]
    assert wiring.index("sessionOpened(result.ref);") \
        < wiring.index("documentCreated(result.ref, result.path);") \
        < wiring.index("drawSession();") \
        < wiring.index("return rekeyToSession(result.ref);"), wiring
    # the jump is keyed to the SESSION ref and `main` is never widened — the
    # main-keyed 404 on a draft document is correct session isolation
    assert "onSessionRekey" in view
    assert "opened: openedSessions(), ended: endedSessions()" in view
    # both overlays live in the session module, beside the one that consumes them
    assert "export function sessionOpened(" in session
    assert "export function openedSessions(" in session
    assert "export function endedSessions(" in session
    assert "export function documentCreated(" in session
    assert "export function createdDocuments(" in session
    # a create's notebook notice is a NOTICE on both surfaces, never an error
    assert "notebook_notice" in create and "notebook_notice" in session
    assert 'el("div", "swb-cnote swb-notice"' in create


def test_the_save_form_says_what_a_blank_title_and_body_actually_do():
    """PR #49 second-review finding R2-13: the form's copy told the human that
    blank meant "the engine's default", full stop — while a blank SECOND save
    silently replaced the pull request's human-authored title and body with that
    default. The engine now preserves what a human wrote (see
    `test_a_blank_second_save_leaves_the_human_authored_title_and_body_intact`), and
    the copy has to say the same thing, because the copy is what the human decides
    from.

    Pinned on the SOURCE text: this is prose, and prose is the defect here."""
    body = SESSION_JS.read_text(encoding="utf-8")
    save_form = body.split("affordance === SESSION_SAVE", 1)[1].split("} else {", 1)[0]
    # the note names BOTH paths and the guarantee
    assert "FIRST save" in save_form and "LATER save" in save_form
    assert "left exactly as they are" in save_form
    assert "never overwrites reviewer-facing text you wrote" in save_form
    # and neither placeholder promises the default on a later save any more
    assert "blank keeps the existing title" in save_form
    assert "blank keeps the existing body" in save_form
    assert "optional — the engine names the branch and its tile" not in body
    assert "optional — the default body carries D18's notice" not in body
    # the response note the engine now returns is RENDERED (the row walks `notes`)
    assert "for (const note of result.notes || [])" in body


# ---- T082's payload arithmetic: the create body's `continuation` -------------

def test_the_create_body_carries_the_continuation_answer(tmp_path):
    """T082 / FR-025: the workbench transport now carries the resume-or-new
    ANSWER. The field is ALWAYS present and `null` until the human answers, so
    the payload has one shape rather than two — and `null` is exactly what the
    route's `normalize_continuation` already reads as "no answer, show me the
    choice"."""
    out = _run_session(tmp_path)
    assert out["continuations"] == ["resume", "new"]
    assert out["normalizedContinuations"] == [None, None, "resume", "new", "new",
                                              None]
    from ideation_dashboard import branch_session as bs
    assert list(bs.CONTINUATIONS) == out["continuations"]
    body = out["createBody"]
    assert body["continuation"] is None
    assert out["createResumeBody"]["continuation"] == "resume"
    # the route accepts both shapes (a null answer is not a shaping error)
    for candidate in (body, out["createResumeBody"]):
        parsed, err = gate_routes_mod._create_body(candidate, {"repository": "r"})
        assert err is None, err
    assert gate_routes_mod._create_body(body, {"repository": "r"})[0]["_continuation"] is None
    assert gate_routes_mod._create_body(
        out["createResumeBody"], {"repository": "r"})[0]["_continuation"] == "resume"
    # the DESCRIPTOR carries it too, or the copyable command would be a
    # different action from the button
    assert "--continuation 'new'" in out["createResumeCommand"]


# ---- T088's finding: the ENDING's report must survive its own re-render -------

# The DOM the mount actually needs, and nothing else: `helpers.el` (createElement
# + className + textContent), `append`/`appendChild`/`insertBefore`, `setAttribute`,
# the literal `innerHTML = ""` clears, `addEventListener`, and dispose.js's
# `querySelector(".refusalpanel-list")` on the panel it builds in `document.body`.
# Modelled after `test_bullseye_widget.py`'s SVG-only DOM — the same instrument,
# widened to the HTML surface this module touches.
_DOM_SHIM = r"""
class Node {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.children = []; this.attributes = {}; this.listeners = {};
    this.className = ''; this._text = '';
  }
  get textContent() {
    return this._text + this.children.map((c) => c.textContent).join('');
  }
  set textContent(value) { this.children = []; this._text = String(value); }
  set innerHTML(value) {
    if (String(value) !== '') throw new Error('only literal "" clears are allowed');
    this.children = []; this._text = '';
  }
  appendChild(child) { this.children.push(child); return child; }
  append(...kids) { for (const k of kids) this.appendChild(k); }
  insertBefore(child, ref) {
    const at = this.children.indexOf(ref);
    this.children.splice(at < 0 ? 0 : at, 0, child);
    return child;
  }
  contains(node) {
    return this === node || this.children.some((c) => c.contains(node));
  }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  querySelector(selector) {
    const cls = selector.replace(/^\./, '');
    return this.walk().find((n) => String(n.className).split(' ').includes(cls))
      || null;
  }
  walk() {
    return this.children.reduce((all, c) => all.concat(c.walk()), [this]);
  }
}
globalThis.document = {
  createElement: (tag) => new Node(tag),
  createTextNode: (text) => { const n = new Node('#text'); n._text = String(text);
    return n; },
  body: new Node('body'),
};
function byClass(root, cls) {
  return root.walk().filter((n) => String(n.className).split(' ').includes(cls));
}
function byText(root, text) {
  return root.walk().filter((n) => n.textContent.includes(text));
}
async function click(node) {
  for (const fn of node.listeners.click || []) await fn({});
}
"""

# The BEHAVIOURAL harness for T088's replay: mount, act, let the ending re-render,
# and look for the engine's report in the freshly built slot. Nothing here reads
# the module's SOURCE — that is the entire point (finding B13).
_ENDING_REPLAY_HARNESS = _DOM_SHIM + """
import { mountSessionAffordances, sessionEndingReport } from './swb-session.js';

const BRANCH = 'draft/demo-topic';
const ctx = {
  scope: { kind: 'staged', id: 'demo-topic' },
  posture: { live: true, branch: BRANCH, ownTile: true, draft: true,
             repository: 'openxFactory', activeRef: BRANCH },
  documents: ['ideation/staging/demo-topic/note.md'],
};
const caps = { actions: { gate: true, session: true } };
const RESULT = {
  ok: true, ref: BRANCH, reason: 'the spike answered its question',
  torn_down: ['worktree', 'registry-entry', 'notebook'], branch_retained: true,
  record: 'ideation/dashboard/gate-records/draft-demo-topic/abandon.yaml',
};
const fetcher = async () => ({ status: 200, json: async () => RESULT });

let host = new Node('div');
let rerenders = 0;
let resetFinished = false;
let rerenderSawReset = false;
const opts = {
  caps, actor: 'brett', fetcher,
  onSessionEnded: async () => {
    await Promise.resolve();
    resetFinished = true;
  },
  onRerender: () => { rerenders += 1; host = new Node('div');
                      rerenderSawReset = resetFinished;
                      mountSessionAffordances(host, ctx, opts); },
};
mountSessionAffordances(host, ctx, opts);

// the human ends the session: open the abandon form, fill the reason, submit
const abandon = byClass(host, 'swb-sessionbtn')
  .find((b) => b.textContent.toLowerCase().includes('abandon'));
await click(abandon);
const reason = host.walk().find((n) => n.attributes['aria-label'] === 'Reason');
reason.value = RESULT.reason;
const submit = byClass(host, 'cbtn').find((b) => b.textContent === 'abandon-session');
await click(submit);

// `host` is now the object the ending's own re-render built
const landed = byClass(host, 'swb-clanded');
console.log(JSON.stringify({
  rerenders,
  rerenderSawReset,
  replayedBoxes: landed.length,
  replayText: landed.map((b) => b.textContent).join(' | '),
  namesTheRecord: byText(host, RESULT.record).length > 0,
  namesTheTeardown: byText(host, 'worktree, registry-entry, notebook').length > 0,
  reportForTheBranch: !!sessionEndingReport(BRANCH),
  buttonsDisabled: byClass(host, 'swb-sessionbtn').every((b) => b.disabled === true),
}));
"""


def _run_ending_replay(tmp_path):
    """Drive the REAL `swb-session.js` (and its real imports) under node against a
    minimal DOM. Views are copied as-is with a `type: module` package.json, so no
    import specifier is rewritten and the module graph under test is production's."""
    if NODE is None:
        pytest.skip("node not available for the DOM-driven session probe")
    views = tmp_path / "views"
    views.mkdir()
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    for name in ("swb-session.js", "helpers.js", "dispose.js",
                 "staging-workbench-model.js"):
        shutil.copy(WEB / "views" / name, views / name)
    harness = views / "ending-replay.js"
    harness.write_text(_ENDING_REPLAY_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def test_the_ending_report_really_reaches_the_slot_the_re_render_rebuilt(tmp_path):
    """PR #49 second-review tail B13: the BEHAVIOUR T088 is named for, asserted.

    The pin below is shape-only — it requires the module's source to contain
    `endedReports.get(`, which is satisfied by ANY key. Mutation-proven: replacing
    the lookup with `endedReports.get("a key nothing ever sets")` left that pin and
    all 103 tests of this module plus `test_session_confinement.py` PASSING, so the
    most consequential moment of a session's life could silently stop reporting
    with a green suite. The invariant is an AGREEMENT between two keys — the one
    `renderOutcome` writes (`String(result.ref)`) and the one the mount reads
    (`String(ctx.posture.branch)`) — and an agreement cannot be pinned by quoting
    one side.

    So this drives the real module: mount, abandon, let the ENDING's own
    `onRerender` rebuild the row, and require the engine's report to be present in
    the rebuilt slot, naming the teardown and the record verbatim (FR-044)."""
    out = _run_ending_replay(tmp_path)

    assert out["rerenders"] == 1, "the ending must re-render the affordance row"
    assert out["rerenderSawReset"] is True, (
        "the main-view handoff must finish before the ending re-renders")
    assert out["replayedBoxes"] == 1, out
    assert out["reportForTheBranch"] is True
    assert out["namesTheRecord"] is True, out["replayText"]
    assert out["namesTheTeardown"] is True, out["replayText"]
    assert "the session ENDED (abandoned)" in out["replayText"]
    # and the row that came back offers no verb a session that is over could take
    assert out["buttonsDisabled"] is True


def test_the_ending_report_survives_the_re_render_the_ending_triggers():
    """T088 (found by the Playwright smoke, not by any pure test): an ENDING
    re-renders the affordance row (Phase 9 note 6 — a session that is over must
    stop offering itself), and `drawSession` rebuilds the session host from
    scratch, which DESTROYS the `.swb-cslot` the outcome was just written into.

    The engine's answer for the most consequential moment of a session's life —
    what was torn down, whether the branch was deleted — therefore appeared and
    vanished within one tick, leaving only tooltips and the posture chip. FR-044
    requires the engine's answer to reach the human VERBATIM; an answer erased by
    the same event that produced it is not reported.

    The fix keeps ONE renderer for the landed box and REPLAYS the remembered
    report into the freshly built slot, so the live outcome and the replay can
    never diverge — the same reason the `ended` overlay itself exists.

    SHAPE ONLY, AND SAID SO (PR #49 second-review tail B13). What this test can
    see is source structure: one `landedBox` definition, the write literal, the
    T077 write-site arithmetic. It CANNOT see whether the two keys agree — the
    review replaced the lookup key with a string nothing ever sets and every
    assertion here still passed. The behaviour is owned by
    `test_the_ending_report_really_reaches_the_slot_the_re_render_rebuilt`, which
    drives the real module under node."""
    body = SESSION_JS.read_text(encoding="utf-8")
    # the report is remembered per branch, beside the ending it belongs to
    assert "const endedReports = new Map();" in body
    assert ("endedReports.set(String(result.ref), { affordance, result, ending });"
            in body)
    # ONE renderer for the landed box: the live outcome and the replay both use it
    assert body.count("function landedBox(") == 1
    assert "const box = landedBox(affordance, result, ending);" in body
    mount = body.split("export function mountSessionAffordances", 1)[1]
    assert "endedReports.get(" in mount, \
        "the mount must replay the remembered ending report into the new slot"
    assert "slot.appendChild(landedBox(" in mount
    # and it is still ONE request helper and one write literal (the T077 pins
    # hold; T080 added a second CALLER of the same helper, never a second site)
    assert body.count("submitSession(") == 3
    assert body.count('method: "POST"') == 1


# ==========================================================================
# PR #49 review finding 15 — a copyable descriptor is SAFE to paste
#
# The descriptors promise to be "copy-pasteable verbatim". `q()` wrapped values
# in DOUBLE quotes (which preserve `$` and backtick expansion) and roughly half
# the slots were interpolated with no quoting at all, so a backtick in ordinary
# engineering prose SILENTLY MUTATED the pasted command and `$(…)`, backticks and
# bare metacharacters arriving from snapshot- and corpus-derived slots reached the
# pasting human's shell in the served checkout.
#
# The oracle is the SHELL, not `shlex`. `shlex.split` tokenizes without expanding,
# so every hostile descriptor below parsed green under the pre-existing
# descriptor-parity tests — which is exactly why those tests did not catch this.
# Here each descriptor is pasted into a real `/bin/sh` whose `python3` is a shim
# that records its argv, and the assertion is that the argv holds the intended
# values BYTE-FOR-BYTE. Payloads use shell BUILTINS only (`printf`), so a hostile
# descriptor needs no external binary to prove expansion and leaves nothing behind
# on the filesystem; `PATH` is the shim directory alone.
# ==========================================================================

# The payloads. `PWNED` is ASSEMBLED by the shell (`printf 'PWN%sD' E`) and
# therefore appears NOWHERE in the literal text — so finding it in the recorded
# argv or in the shell's output is proof the shell evaluated something, and the
# assertion cannot be satisfied by the payload simply travelling through intact.
# Shell BUILTINS only: no external program can run, and nothing is written.
_SUBST = "$(printf 'PWN%sD' E)"
_BACKTICK = "`printf 'PWN%sD' E`"
_SEPARATOR = "; printf 'PWN%sD' E"

# Each value carries an expansion or a command separator, and several carry a
# single quote — the one character single-quoting itself has to escape.
_HOSTILE_VALUES = {
    "actor": f"Brett O'Hara {_BACKTICK}",
    "title": f"Draft {_SUBST} it",
    "summary": f"why it's {_BACKTICK} needed",
    "keyword": f"alpha{_SUBST}",
    "repositoryContext": f"repo{_SEPARATOR}",
    "document": "ideation/staging/topic-x/a b's.md",
    "contentFile": f"/tmp/x{_SEPARATOR}",
    "notes": f"note with 'quotes', $HOME and {_BACKTICK}",
    "bodyFile": f"/tmp/body {_SUBST}",
    "reason": f"stopped — see `git log`{_SEPARATOR}",
    "scopeId": f"topic-x{_SEPARATOR}",
    "branch": f"draft/{_SUBST}",
    "workspaceRoot": f"/tmp/ws {_SUBST}",
}

_HOSTILE_HARNESS = """
import {
  workbenchScope, createSeed, createDocumentCommand, sessionCommand,
  notebookRefreshCommand,
} from './staging-workbench-model.mjs';
import { readFileSync } from 'node:fs';
const cases = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const v = cases.values;
const snapshot = cases.snapshot;
const scope = workbenchScope(snapshot, 'staged', 'topic-x') || {
  kind: 'staged', id: 'topic-x' };
// The create descriptor is built through the REAL seeding path, with the hostile
// value arriving as a CHECKED KEYWORD — i.e. snapshot/corpus-derived material,
// not something the human typed (the reachability the review asserts).
const seeded = createSeed(snapshot, scope, 'lens', { checked: [v.keyword] });
const hostileScope = { kind: 'staged', id: v.scopeId };
console.log(JSON.stringify({
  create: createDocumentCommand(
    { ...seeded, title: v.title, summary: v.summary,
      repositoryContext: v.repositoryContext },
    { actor: v.actor }),
  edit: sessionCommand('edit', {
    scope: hostileScope, actor: v.actor, document: v.document,
    contentFile: v.contentFile, notes: v.notes }),
  save: sessionCommand('save', {
    scope: hostileScope, actor: v.actor, title: v.title, bodyFile: v.bodyFile }),
  abandon: sessionCommand('abandon', {
    scope: hostileScope, actor: v.actor, reason: v.reason }),
  notebook: notebookRefreshCommand({
    branch: v.branch, workspaceRoot: v.workspaceRoot, apply: true }),
}));
"""

# Which hostile values each descriptor must carry through untouched.
_HOSTILE_EXPECTED = {
    "create": ("actor", "title", "summary", "repositoryContext"),
    "edit": ("actor", "scopeId", "document", "contentFile", "notes"),
    "save": ("actor", "scopeId", "title", "bodyFile"),
    "abandon": ("actor", "scopeId", "reason"),
    "notebook": ("branch", "workspaceRoot"),
}

_PYTHON3_SHIM = """#!/bin/sh
for arg in "$@"; do printf '%s\\0' "$arg" >> "$XF_ARGV_LOG"; done
"""


def _hostile_descriptors(tmp_path):
    if NODE is None:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(MODEL_JS, tmp_path / "staging-workbench-model.mjs")
    (tmp_path / "hostile.mjs").write_text(_HOSTILE_HARNESS, encoding="utf-8")
    cases = tmp_path / "hostile-cases.json"
    cases.write_text(json.dumps({"snapshot": SNAP, "values": _HOSTILE_VALUES}),
                     encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "hostile.mjs"), str(cases)],
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def _paste_into_a_shell(tmp_path, command):
    """Run `command` the way a human pastes it, and return (argv, stdout).

    `python3` is a shim that records its argv; `PATH` holds nothing else, so the
    payloads deliberately use shell BUILTINS and no external program can run."""
    shim_dir = tmp_path / "shim"
    shim_dir.mkdir(exist_ok=True)
    shim = shim_dir / "python3"
    shim.write_text(_PYTHON3_SHIM, encoding="utf-8")
    shim.chmod(0o755)
    log = tmp_path / "argv.log"
    log.write_bytes(b"")
    done = subprocess.run(["/bin/sh", "-c", command], cwd=str(tmp_path),
                          capture_output=True, text=True, timeout=60,
                          env={"PATH": str(shim_dir), "XF_ARGV_LOG": str(log)})
    raw = log.read_bytes().decode("utf-8")
    argv = [part for part in raw.split("\0") if part != ""]
    return argv, done.stdout + done.stderr


def _unquoted_characters(command):
    """The characters of `command` that a POSIX shell would read as SYNTAX —
    everything outside single quotes, with `\\x` counted as the literal `x`.

    Written as a small lexer rather than a quote-parity toggle because the
    escape spelling for an inner `'` is `'\\''` (close, escaped literal quote,
    reopen), and a toggle mis-reads that as re-entering quoted text — it would
    call a genuinely unquoted `$` safe."""
    out = []
    index, inside = 0, False
    while index < len(command):
        char = command[index]
        if inside:
            inside = char != "'"
            index += 1
            continue
        if char == "'":
            inside = True
        elif char == "\\":
            index += 1              # the escaped character is a literal
        else:
            out.append(char)
        index += 1
    return out

@pytest.mark.parametrize("name", sorted(_HOSTILE_EXPECTED))
def test_a_pasted_descriptor_carries_hostile_values_through_verbatim(tmp_path, name):
    """Finding 15(a), the CORRECTNESS half: the descriptor claims to be copyable
    verbatim, and a backtick or `$` in a human-typed reason/notes/title used to
    change what the command said. Pasted into a real shell, every value must
    arrive as ONE argument, byte-identical."""
    command = _hostile_descriptors(tmp_path)[name]
    argv, output = _paste_into_a_shell(tmp_path, command)

    for key in _HOSTILE_EXPECTED[name]:
        assert _HOSTILE_VALUES[key] in argv, (key, argv)
    # finding 15(b), the EXECUTION half: nothing expanded, nothing ran
    assert "PWNED" not in "".join(argv), argv
    assert "PWNED" not in output, output


@pytest.mark.parametrize("name", sorted(_HOSTILE_EXPECTED))
def test_a_hostile_descriptor_stays_one_command(tmp_path, name):
    """A `;` in a snapshot-derived scope id used to SPLIT the pasted line, so the
    shell ran a second command the descriptor never showed. One paste, one
    invocation of the tool the descriptor names."""
    command = _hostile_descriptors(tmp_path)[name]
    argv, _output = _paste_into_a_shell(tmp_path, command)

    tool = ("scripts/sync-notebooklm-books.py" if name == "notebook"
            else "scripts/ideation_dashboard/cli.py")
    assert argv[:1] == [tool], argv


@pytest.mark.parametrize("name", sorted(_HOSTILE_EXPECTED))
def test_no_descriptor_leaves_a_shell_metacharacter_unquoted(tmp_path, name):
    """The structural reading of the same rule, so a NEW slot added without
    quoting fails here even if no test case happens to send it a payload: outside
    the single quotes a descriptor contains flag names and literal paths only."""
    command = _hostile_descriptors(tmp_path)[name]
    remainder = "".join(_unquoted_characters(command))
    for char in "$`;&|<>()\n\"":
        assert char not in remainder, (char, remainder)


def test_the_hostile_descriptors_still_parse_into_the_real_cli(tmp_path):
    """Quoting is not validation, and it does not pretend to be: the descriptor
    hands the hostile value to the CLI as one argument, and the CLI's OWN
    allowlist (`looks_ref_legal` and the body validator) is what refuses it —
    inside the process, which is the layer that can refuse."""
    import shlex

    from ideation_dashboard import cli

    out = _hostile_descriptors(tmp_path)
    parser = cli.build_parser()
    for name in ("create", "edit", "save", "abandon"):
        args = parser.parse_args(shlex.split(out[name])[2:])
        assert args.actor == _HOSTILE_VALUES["actor"]
    abandon = parser.parse_args(shlex.split(out["abandon"])[2:])
    assert abandon.scope_id == _HOSTILE_VALUES["scopeId"]
    assert abandon.reason == _HOSTILE_VALUES["reason"]
    # and the id the shell handed over intact is refused by the derivation
    from ideation_dashboard import branch_session as bs
    with pytest.raises(bs.SessionRefused):
        bs.session_branch(bs.STAGED_TOPIC, abandon.scope_id)


# ==========================================================================
# T083 (010-doxbench-editor-chat, US5): the VISIBLE name is exactly `doxBench`
# and every STABLE TECHNICAL IDENTIFIER survives unrenamed.
#
# This suite is the predecessor authority for `staging-workbench.js` /
# `staging-workbench-model.js`, so the naming rule is pinned HERE rather than in
# the feature's own files — a later pass that "tidies" the presentation name back
# to the predecessor spelling, or that renames a protocol identifier while
# chasing FR-001, fails in the suite that owns the module.
#
# BOTH DIRECTIONS, deliberately (FR-001 + FR-002 are one rule with two halves):
#
#   FR-001  every HUMAN-VISIBLE string in the view — headings, fallback titles,
#           tooltips, accessible names — reads exactly `doxBench`.
#   FR-002  the rename creates no second capability and migrates nothing:
#           `staging-workbench*.js` filenames, `mountStagingWorkbench`,
#           `nav.openWorkbench`, `WORKBENCH_KINDS`, the `swb-` class/id prefix
#           and the gitignored `ideation/workbench/` tree stay exactly as they
#           are. These are the exceptions the compatibility-migration checklist
#           NOTES record as "not presentation-name exceptions and must not be
#           migrated".
#
# `/workbench/*` ROUTES are a third checklist exception and are NOT pinned here:
# they are T050/T051 and do not exist yet, so an assertion about them would be a
# claim about unbuilt code.
# ==========================================================================

VIEW_JS = WEB / "views" / "staging-workbench.js"
DOXBENCH_NAME = "doxBench"


def _string_literals(source: str) -> list[str]:
    """Every DOUBLE-quoted literal in `source`, with `//` line comments and
    `/* */` blocks removed and module specifiers (`./…`) dropped.

    A hand scanner rather than a regex: a regex cannot tell a `//` inside a
    string from a comment, and this view's tooltips contain both slashes and
    apostrophes. Single-quoted and template literals are skipped over (never
    collected) so their contents cannot be mistaken for code."""
    out: list[str] = []
    i, n = 0, len(source)
    while i < n:
        char = source[i]
        if char == "/" and source[i + 1:i + 2] == "/":
            while i < n and source[i] != "\n":
                i += 1
        elif char == "/" and source[i + 1:i + 2] == "*":
            end = source.find("*/", i + 2)
            i = n if end < 0 else end + 2
        elif char == '"':
            j, buf = i + 1, []
            while j < n and source[j] != '"':
                if source[j] == "\\":
                    j += 1
                buf.append(source[j])
                j += 1
            out.append("".join(buf))
            i = j + 1
        elif char in "'`":
            quote, j = char, i + 1
            while j < n and source[j] != quote:
                if source[j] == "\\":
                    j += 1
                j += 1
            i = j + 1
        else:
            i += 1
    return [s for s in out if not s.startswith("./") and not s.startswith("../")]


def test_no_visible_string_in_the_view_carries_the_predecessor_name():
    """FR-001 / SC-009: the human-visible surface names the product, and the
    product is `doxBench`. Every visible literal is scanned rather than a
    hand-listed few, so a NEW sentence that says `workbench` at a human fails
    here without anybody remembering to add an assertion for it."""
    literals = _string_literals(VIEW_JS.read_text(encoding="utf-8"))
    assert literals, "the literal scanner found nothing — it is broken, not the view"
    offenders = [s for s in literals if "workbench" in s.lower()]
    assert offenders == [], (
        "visible string(s) still carry the predecessor presentation name; "
        f"technical identifiers are exempt but these are prose: {offenders}")


def test_the_visible_name_is_spelled_with_the_exact_doxbench_casing():
    """FR-001 is a CASING requirement, not just a word requirement: `Doxbench`,
    `DoxBench` and `doxbench` in a visible sentence all fail SC-009."""
    literals = _string_literals(VIEW_JS.read_text(encoding="utf-8"))
    # the class/attribute vocabulary is a technical identifier, and CSS class
    # names are lower-case by construction (`doxbench-canvas`) — those are
    # exempt, and excluding them FIRST is what stops this test from being
    # satisfied by a class name while no human-readable name exists at all
    prose = [s for s in literals if not s.startswith("doxbench-")]
    named = [s for s in prose if "doxbench" in s.lower()]
    assert named, "the view names the product nowhere a human can read it"
    wrong = [s for s in named if DOXBENCH_NAME not in s]
    assert wrong == [], f"visible name(s) with the wrong casing: {wrong}"


def test_the_fallback_titles_name_the_product_rather_than_the_predecessor():
    """The two degraded headings — an ended session's tile that is gone from
    main, and a tile that does not resolve in the snapshot — are the ONLY places
    the shell writes a product name instead of a scope title, so they are where
    the predecessor spelling survived longest."""
    view = VIEW_JS.read_text(encoding="utf-8")
    assert f'title.textContent = "{DOXBENCH_NAME}";' in view
    assert view.count(f'title.textContent = "{DOXBENCH_NAME}";') == 2
    assert 'title.textContent = "staging workbench";' not in view


def test_the_posture_pill_tooltips_name_the_product():
    """The pill's `title` is the sentence that states what authority the plane
    has (design D9). It is human-visible text and it named the predecessor."""
    view = VIEW_JS.read_text(encoding="utf-8")
    pill = view.split("const gateOn = createGateLive(caps);", 1)[1].split(
        "const closeBtn", 1)[0]
    assert DOXBENCH_NAME in pill
    assert "workbench" not in pill.replace("createGateLive", "")


def test_the_stable_technical_identifiers_are_not_renamed():
    """FR-002 / SC-009's second half: `all existing technical artifacts continue
    to load without migration`. The rename is PRESENTATION only, and every
    identifier below is load-bearing for something outside this feature."""
    view = VIEW_JS.read_text(encoding="utf-8")
    model = MODEL_JS.read_text(encoding="utf-8")
    app = (WEB / "app.js").read_text(encoding="utf-8")
    wheel = (WEB / "views" / "wheel.js").read_text(encoding="utf-8")

    # the FILENAMES the checklist names (a rename here would break every
    # importer and every predecessor test that reads them by path)
    assert VIEW_JS.is_file() and MODEL_JS.is_file()
    assert 'from "./staging-workbench-model.js"' in view

    # the MOUNT and the NAV verb app.js/wheel.js already speak
    assert "export function mountStagingWorkbench(" in view
    assert 'import { mountStagingWorkbench } from "./views/staging-workbench.js";' in app
    assert "openWorkbench:" in app
    assert "opts.nav?.openWorkbench" in wheel

    # the MODEL's exported vocabulary (imported by swb-create/swb-session and
    # unit-tested by this file's own harness)
    assert "export const WORKBENCH_KINDS" in model
    assert "export function workbenchScope(" in model
    assert "workbenchScope," in view

    # the `swb-` class/id prefix — every rule in styles.css and every selector
    # in every predecessor harness reads it
    assert view.count('"swb-') >= 20
    assert 'title.id = "swb-title";' in view


def test_the_gitignored_workbench_tree_is_not_migrated():
    """The other `workbench` sense (design D5: the `ideation-workbench`
    reference-set family) shares the word and is a DIFFERENT capability. FR-002
    forbids migrating it, and conflating the two is the mistake the naming note
    at the top of this file exists to prevent."""
    lens_model = (WEB / "views" / "lens-model.js").read_text(encoding="utf-8")
    canvas_model = (WEB / "views" / "canvas-model.js").read_text(encoding="utf-8")
    assert 'export const WORKBENCH_DIR = "ideation/workbench/";' in lens_model
    assert 'export const DRAFTS_DIR = "ideation/workbench/drafts/";' in canvas_model


# ---------------------------------------------------------------------------
# T055: the chat rail joins the shell as the THIRD region behind `.has-rail`.
# Source-level doctrine pins (the shell stays transport-free and forwards the
# two chat transports to the rail mount verbatim); the rail's own behavior is
# pinned DOM-free in test_doxbench_chat_view.py.
# ---------------------------------------------------------------------------

SWB_JS = WEB / "views" / "staging-workbench.js"


def test_the_shell_imports_and_mounts_the_chat_rail_behind_has_rail():
    source = SWB_JS.read_text(encoding="utf-8")
    assert 'from "./doxbench-chat.js"' in source
    assert "mountDoxBenchChatRail(" in source
    assert 'classList.toggle("has-rail"' in source


def test_the_shell_forwards_the_two_chat_transports_and_opens_no_route():
    source = SWB_JS.read_text(encoding="utf-8")
    assert "doxbench.catalog" in source or "doxbench?.catalog" in source
    assert "doxbench.chatTurn" in source or "doxbench?.chatTurn" in source
    assert "fetch(" not in source, "the shell must stay transport-free"


def test_the_rail_region_is_a_named_landmark_like_its_two_siblings():
    source = SWB_JS.read_text(encoding="utf-8")
    assert 'aria-label", "doxBench chat rail"' in source


# ---------------------------------------------------------------------------
# T104 F10-1, the POSTURE LADDER's missing rung. Every model-catalog failure
# used to fall through to `approvedModelCount === 0`'s editor-only sentence,
# "no approved model is configured" — a misdiagnosis for a 403 stale console
# token (recoverable by reload) and for a 500 broken catalog (the answer
# could not be read at all). The pure ladder now carries a `catalogFailure`
# fact between source-unavailable and editor-only; the rail's own rendering
# of the same postures is pinned in test_doxbench_chat_view.py.
# ---------------------------------------------------------------------------

_POSTURE_LADDER_HARNESS = """
import { presentationPosture } from './staging-workbench-model.mjs';

const CAPABLE = {
  gateLive: true, surfaceHidden: false,
  repository: 'fixture-repo', ref: 'main',
  sourceAvailable: true, approvedModelCount: 0,
};
const out = {};
out.staleToken = presentationPosture({
  ...CAPABLE, catalogFailure: 'console_required' });
out.unreadable = presentationPosture({
  ...CAPABLE, catalogFailure: 'unreadable' });
out.editorOnly = presentationPosture({ ...CAPABLE, catalogFailure: null });
out.capable = presentationPosture({
  ...CAPABLE, approvedModelCount: 1, catalogFailure: null });
// AUTHORITY ORDER: the ladder is most-restrictive first, so a hidden or
// gate-off surface is never described by the lesser catalog condition
out.hiddenWins = presentationPosture({
  ...CAPABLE, surfaceHidden: true, catalogFailure: 'unreadable' }).kind;
out.gateOffWins = presentationPosture({
  ...CAPABLE, gateLive: false, catalogFailure: 'unreadable' }).kind;
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def posture_ladder_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the posture-ladder probe")
    tmp_path = tmp_path_factory.mktemp("swb-posture-ladder")
    shutil.copy(MODEL_JS, tmp_path / "staging-workbench-model.mjs")
    harness = tmp_path / "posture-ladder-harness.mjs"
    harness.write_text(_POSTURE_LADDER_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_a_stale_token_catalog_failure_gets_its_own_recoverable_rung(
        posture_ladder_results):
    p = posture_ladder_results["staleToken"]
    assert p["kind"] == "console-token-stale"
    assert p["canvas"] is True, "both editors stay usable (FR-025)"
    assert "stale" in p["note"] and "reload" in p["note"]
    assert "no approved model" not in p["note"]


def test_an_unreadable_catalog_gets_its_own_rung_distinct_from_configured_none(
        posture_ladder_results):
    p = posture_ladder_results["unreadable"]
    assert p["kind"] == "catalog-unreadable"
    assert p["canvas"] is True
    assert "could not be read" in p["note"]
    assert "no approved model" not in p["note"]


def test_the_editor_only_and_capable_rungs_are_unchanged(posture_ladder_results):
    e = posture_ladder_results["editorOnly"]
    assert e["kind"] == "editor-only"
    assert "no approved model is configured" in e["note"]
    c = posture_ladder_results["capable"]
    assert c["kind"] == "capable-local" and c["note"] is None


def test_the_catalog_rungs_never_outrank_hidden_or_gate_off(
        posture_ladder_results):
    assert posture_ladder_results["hiddenWins"] == "hosted-hidden"
    assert posture_ladder_results["gateOffWins"] == "gate-off"


def test_the_shell_threads_the_rails_catalog_failure_into_the_posture_note():
    """The wiring half: the shell's two presentationPosture call sites (the
    canvas draw and the onState refresh) both carry the rail-reported
    catalog failure, the onState comparison re-renders when the FAILURE
    changes (not only the count), and a rail teardown resets it exactly like
    approvedModelCount."""
    source = SWB_JS.read_text(encoding="utf-8")
    assert source.count("catalogFailure: railCatalogFailure") == 2
    assert "chatState.catalogFailure" in source
    teardown = source.split("function teardownRail()", 1)[1].split(
        "\n  }", 1)[0]
    assert "railCatalogFailure = null;" in teardown
