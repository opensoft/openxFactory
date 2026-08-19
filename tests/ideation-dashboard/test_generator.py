"""The generator's derivation rules over the deterministic fixture corpus: doc
entries and stages, Topics-ONLY cluster edges, link-count tallies, one-for-one
register projection with NO fabricated history, staged topics, changes, the
declared keyword index, and project grouping (FR-003/FR-004/FR-007; spec US1)."""

from __future__ import annotations

import pytest

from conftest import (  # noqa: F401  (sys.path side effect)
    BASE_REPO, NEGATIVES, PINNED_REVISION, FakeGit, find_openxfactory_validator,
)

from ideation_dashboard import fixtures, generator, snapshot
from ideation_dashboard.boundary import OutputBoundary
from ideation_dashboard.generator import generate_snapshot
from ideation_dashboard.register import CrossReferenceIndexAdapter

WORKED_EXAMPLE_POSSIBLES = {
    "pos-avatar-inline", "pos-avatar-lab", "pos-dtn-autopromote",
    "pos-health-sweep", "pos-ideation-governance",
}
LEGACY_DOCS = {
    "ideation/brainstorm/legacy-note.md",
    "ideation/staging/keyword-lens/README.md",
}


def _snap(**over):
    kwargs = {"source_revision": PINNED_REVISION, "git": FakeGit()}
    kwargs.update(over)
    return generate_snapshot(BASE_REPO, "fixture-repo", **kwargs)


def _by_id(items):
    return {item["id"]: item for item in items}


# ---- documents ----

def test_documents_are_the_governed_ideation_corpus():
    docs = _by_id(_snap()["documents"])
    assert set(docs) == {
        "ideation/brainstorm/avatar-client-lab.md",
        "ideation/brainstorm/doc-health-checks.md",
        "ideation/brainstorm/dtn-register.md",
        "ideation/brainstorm/legacy-note.md",
        "ideation/staging/ideation-governance/README.md",
        "ideation/staging/keyword-lens/README.md",
    }


def test_document_headers_and_destinations_project():
    docs = _by_id(_snap()["documents"])
    packet = docs["ideation/staging/ideation-governance/README.md"]
    assert packet["stage"] == "staged"
    assert packet["kind"] == "staging-packet"
    assert packet["topics"] == ["ideation-governance"]
    assert packet["dates"]["captured"] == "2026-07-11"
    # a staging-packet doc heads into its topic folder
    assert packet["destinations"]["staged_topics"] == ["ideation-governance"]
    # a plain brainstorm doc has no staging destination
    assert "destinations" not in docs["ideation/brainstorm/legacy-note.md"]


# ---- Topics-only cluster edges ----

def test_cluster_edges_derive_strictly_from_topics_headers():
    clusters = _by_id(_snap()["clusters"])
    gov = clusters["cl-ideation-governance"]
    members = sorted(e["document"] for e in gov["document_edges"])
    # exactly the docs whose Topics: header names ideation-governance
    assert members == [
        "ideation/brainstorm/doc-health-checks.md",
        "ideation/brainstorm/dtn-register.md",
        "ideation/staging/ideation-governance/README.md",
    ]
    # each edge names the topic that matched — nothing beyond declared Topics:
    assert all(e["matched_topics"] == ["ideation-governance"] for e in gov["document_edges"])
    # legacy-note declares only ideation-dashboard, so it is NOT a governance member...
    assert "ideation/brainstorm/legacy-note.md" not in members
    # ...but IS an ideation-dashboard member (the multi-cluster edge lands correctly)
    dash = sorted(e["document"] for e in clusters["cl-ideation-dashboard"]["document_edges"])
    assert "ideation/brainstorm/legacy-note.md" in dash
    assert "ideation/staging/keyword-lens/README.md" in dash


# ---- tallies count LINKS, not cards ----

def test_tallies_equal_link_counts():
    snap = _snap()
    clusters = _by_id(snap["clusters"])
    for c in snap["clusters"]:
        assert c["tallies"]["document_links"] == len(c["document_edges"])
    assert clusters["cl-ideation-dashboard"]["tallies"]["document_links"] == 3
    assert clusters["cl-avatar"]["tallies"]["document_links"] == 1
    # possible_links count claiming edges (links), including the multi-cluster claim
    assert clusters["cl-ideation-governance"]["tallies"]["possible_links"] == 2
    assert clusters["cl-avatar"]["tallies"]["possible_links"] == 2
    assert clusters["cl-keyword-lens"]["tallies"]["possible_links"] == 0


def test_cluster_lineage_is_distinct_from_member_edges():
    clusters = _by_id(_snap()["clusters"])
    gov = clusters["cl-ideation-governance"]
    # downstream progression, not the member docs
    assert gov["lineage"]["staged_picks"] == ["ideation-governance"]
    assert gov["lineage"]["proposals"] == ["add-ideation-governance"]


# ---- cross-reference data spine: names, readiness heat, conflict flags ----

def test_cluster_names_flow_from_the_cross_reference_index():
    clusters = _by_id(_snap()["clusters"])
    # a name that DIFFERS from the titleized slug proves it came from the index
    assert clusters["cl-avatar"]["name"] == "Avatar Client Lab"
    assert clusters["cl-dtn"]["name"] == "DTN Candidate Register"
    # a cluster ABSENT from the index falls back to the titleized topic slug
    assert clusters["cl-keyword-lens"]["name"] == "Keyword Lens"


def test_titleize_fallback_spaces_and_title_cases_the_slug():
    assert generator._titleize("keyword-lens") == "Keyword Lens"
    assert generator._titleize("doc_health") == "Doc Health"
    assert generator._titleize("") == ""


def test_scored_readiness_attaches_as_the_flat_heat_map_funnel_renders():
    clusters = _by_id(_snap()["clusters"])
    # the SCORED cross-ref tiers project to the flat {tier: score} map (numeric
    # values only) funnel.js's readinessHeat iterates — no {tiers: [...]} nesting
    assert clusters["cl-doc-health"]["readiness"] == {"domain": 9, "company": 8, "project": 8}


def test_unscored_readiness_is_omitted_so_the_heat_stays_dormant():
    clusters = _by_id(_snap()["clusters"])
    # all-unscored panels emit NO readiness key (the binding stays dormant until
    # the scoring worker emits numbers)
    assert "readiness" not in clusters["cl-avatar"]
    assert "readiness" not in clusters["cl-ideation-governance"]
    assert "readiness" not in clusters["cl-keyword-lens"]


def test_conflict_flags_pass_through_verbatim():
    clusters = _by_id(_snap()["clusters"])
    assert clusters["cl-ideation-governance"]["conflict_flags"] == [
        {"kind": "tier-spread", "tiers": ["domain", "project"],
         "detail": "domain and project tiers diverge"}]
    # clusters without index conflict flags carry none
    assert "conflict_flags" not in clusters["cl-doc-health"]


# ---- possibles: one-for-one projection, no fabrication ----

def test_only_worked_examples_carry_possibles():
    snap = _snap()
    assert {p["id"] for p in snap["possibles"]} == WORKED_EXAMPLE_POSSIBLES
    # no possible pins evidence to a legacy doc (no invented history)
    for p in snap["possibles"]:
        for pin in p.get("supporting_evidence", []):
            assert pin["document"] not in LEGACY_DOCS


def test_snapshot_possible_equals_register_entry_field_for_field():
    snap = _snap()
    possibles = _by_id(snap["possibles"])
    entries = CrossReferenceIndexAdapter.discover(BASE_REPO).possibles_by_id()
    assert set(possibles) == set(entries)  # one-for-one
    for pid, entry in entries.items():
        # the snapshot possible carries exactly the register entry's projected
        # fields (provenance dropped; evidence document == doc id, an identity map)
        expected = {k: v for k, v in entry.items()
                    if k in fixtures.POSSIBLE_FIELDS and v is not None}
        assert possibles[pid] == expected


def test_pick_edge_cites_staging_id_and_inherited_change_id():
    possibles = _by_id(_snap()["possibles"])
    pick = possibles["pos-ideation-governance"]["pick"]
    assert pick == {"staging_id": "ideation-governance", "change_id": "add-ideation-governance"}


def test_option_set_and_cited_rejection_project():
    possibles = _by_id(_snap()["possibles"])
    assert possibles["pos-avatar-inline"]["option_set"]["id"] == "os-avatar-shape"
    rejection = possibles["pos-dtn-autopromote"]
    assert rejection["state"] == "rejected" and rejection["reason"] and rejection["citation"]


def test_uncited_rejection_is_not_papered_over_and_fails_validation(tmp_path):
    # Pointed at the negative register, the generator faithfully projects the
    # uncited rejection (it does NOT fabricate a citation)...
    snap = _snap(possibles_source=NEGATIVES / "uncited-rejection.register.yaml")
    rejection = _by_id(snap["possibles"])["pos-uncited-reject"]
    assert rejection["state"] == "rejected" and "citation" not in rejection
    # ...so the pinned validator rejects the snapshot loudly.
    validator = find_openxfactory_validator()
    if validator is None:
        pytest.skip("no reachable openxFactory checkout")
    boundary = OutputBoundary(tmp_path, ["out/"])
    path = snapshot.write_snapshot(snap, tmp_path / "out" / "neg.json", boundary)
    with pytest.raises(snapshot.SnapshotInvalid):
        snapshot.validate_or_raise(path, validator=validator)


# ---- staged topics, changes, keyword index ----

def test_staged_topics_project_with_target_change():
    staged = {s["staging_id"]: s for s in _snap()["staged_topics"]}
    assert set(staged) == {"ideation-governance", "keyword-lens"}
    assert staged["ideation-governance"]["target_change"] == "add-ideation-governance"
    assert staged["ideation-governance"]["files"] == [
        "ideation/staging/ideation-governance/README.md"]
    # keyword-lens has no picked possible, so no target change
    assert "target_change" not in staged["keyword-lens"]


def test_changes_project_status_ratification_and_task_progress():
    changes = _by_id(_snap()["changes"])
    active = changes["add-ideation-governance"]
    assert active["status"] == "active"
    assert active["task_progress"] == {"completed": 2, "total": 4}
    assert active["origin_staging_id"] == "ideation-governance"
    assert "ratification" not in active
    archived = changes["add-document-cataloging"]
    assert archived["status"] == "archived"
    # The archived fixture change records no governed ratifier (no `.openspec.yaml`
    # ratifier), so ratification stays DORMANT: a date-only object would fail the
    # pinned schema's required [ratifier, date] and skip the nightly lane. The
    # date-from-folder derivation is exercised directly below.
    assert "ratification" not in archived


def test_keyword_index_is_declared_counts_only():
    snap = _snap()
    kw = {k["keyword"]: k for k in snap["keyword_index"]}
    assert kw["ideation-dashboard"]["declared_doc_count"] == 3
    assert kw["avatar"]["declared_doc_count"] == 1
    # inferred counts are deferred until document-cataloging lands
    assert all("inferred_doc_count" not in entry for entry in snap["keyword_index"])


# ---- project grouping ----

def test_project_grouping_resolves_from_the_register():
    snap = _snap()
    assert snap["project"] == "fixture-core"
    assert snap["project_group"] == "fixture-family"


def test_unregistered_repository_renders_ungrouped():
    snap = generate_snapshot(BASE_REPO, "not-registered",
                             source_revision=PINNED_REVISION, git=FakeGit())
    assert "project" not in snap
    assert "project_group" not in snap


# ---- per-document degradation (dashboard-lane-resilience Fix 1) -------------
#
# A document whose Status: header is missing/unparseable derived `stage: null`,
# which the pinned validator rejects ("None is not of type 'string'" / "None is
# not one of [...]") — one unheadered doc failed the whole snapshot and DoSed the
# nightly lane (reproduced at openxFactory 7bb6c4e: docs/sops/README.md and
# docs/sops/openai-realtime-f0-lab-credential.md). The generator now degrades
# PER DOCUMENT: an entry it cannot make schema-valid is excluded and reported.

def _mini_corpus(root, docs):
    """A minimal governed corpus at `root`: {repo-relative path: text}."""
    for rel, text in docs.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return root


def _validate(snap, out_root):
    validator = find_openxfactory_validator()
    if validator is None:
        pytest.skip("no reachable openxFactory checkout")
    boundary = OutputBoundary(out_root, ["out/"])
    path = snapshot.write_snapshot(snap, out_root / "out" / "s.json", boundary)
    return snapshot.validate_snapshot(path, validator=validator)


def test_headerless_document_is_excluded_not_emitted_with_stage_null(tmp_path):
    corpus_root = _mini_corpus(tmp_path / "repo", {
        "ideation/brainstorm/good.md": "Status: brainstorm\nTopics: alpha\n\nbody\n",
        "ideation/brainstorm/headerless.md": "# no governance header\n\nprose\n",
    })
    excluded = []
    snap = generate_snapshot(corpus_root, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit(),
                             excluded_documents=excluded)
    # the good doc projects; the headerless one is dropped ENTIRELY — never
    # emitted with a null stage
    assert {d["id"] for d in snap["documents"]} == {"ideation/brainstorm/good.md"}
    assert all(d["stage"] is not None for d in snap["documents"])
    # its exclusion is reported with path + reason
    assert excluded == [{"path": "ideation/brainstorm/headerless.md",
                         "reason": "missing or unparseable Status: header"}]
    # the whole snapshot now VALIDATES (no dangling edge survives the drop)
    result = _validate(snap, tmp_path / "v1")
    assert result.ok, result.stdout + result.stderr


def test_unrecognized_status_value_is_also_excluded(tmp_path):
    # fixing the CLASS, not just stage:null — a present-but-invalid Status value
    # would equally poison the enum, so it is excluded too.
    corpus_root = _mini_corpus(tmp_path / "repo", {
        "ideation/brainstorm/good.md": "Status: draft\n\nbody\n",
        "ideation/brainstorm/weird.md": "Status: in-progress\n\nbody\n",
    })
    excluded = []
    snap = generate_snapshot(corpus_root, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit(),
                             excluded_documents=excluded)
    assert {d["id"] for d in snap["documents"]} == {"ideation/brainstorm/good.md"}
    assert excluded == [{"path": "ideation/brainstorm/weird.md",
                         "reason": "unrecognized lifecycle status 'in-progress'"}]
    assert _validate(snap, tmp_path / "v2").ok


def test_all_documents_headerless_yields_empty_but_valid_documents(tmp_path):
    # The edge case: EVERY doc is defective. An empty documents[] is schema-legal
    # (an array with zero items), so the snapshot still validates rather than the
    # lane skipping wholesale.
    corpus_root = _mini_corpus(tmp_path / "repo", {
        "ideation/brainstorm/a.md": "no header\n",
        "ideation/brainstorm/b.md": "also none\n",
    })
    excluded = []
    snap = generate_snapshot(corpus_root, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit(),
                             excluded_documents=excluded)
    assert snap["documents"] == []
    assert {e["path"] for e in excluded} == {
        "ideation/brainstorm/a.md", "ideation/brainstorm/b.md"}
    assert _validate(snap, tmp_path / "v3").ok


def test_exclusion_reporting_is_opt_in(tmp_path):
    # Callers that pass no list (renderers, cli) are unaffected: the defective
    # doc is still excluded from documents[], the reporting is simply out-of-band.
    corpus_root = _mini_corpus(tmp_path / "repo", {
        "ideation/brainstorm/good.md": "Status: staged\n\nbody\n",
        "ideation/brainstorm/headerless.md": "nope\n",
    })
    snap = generate_snapshot(corpus_root, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit())
    assert {d["id"] for d in snap["documents"]} == {"ideation/brainstorm/good.md"}


# ---- ratification: derived from the archive folder + governed ratifier ---------

def _archived_corpus(tmp_path, *, ratifier: str | None):
    """A minimal corpus with one archived change under a `YYYY-MM-DD-<id>`
    folder; when `ratifier` is given it is recorded in `.openspec.yaml`."""
    root = _mini_corpus(tmp_path / "repo", {
        "ideation/brainstorm/good.md": "Status: brainstorm\nTopics: alpha\n\nbody\n"})
    folder = root / "openspec" / "changes" / "archive" / "2026-07-09-add-x"
    folder.mkdir(parents=True)
    (folder / "proposal.md").write_text(
        "# Change: add-x\n\nStatus: ratified\nRatified by: add-x\n", encoding="utf-8")
    if ratifier is not None:
        (folder / ".openspec.yaml").write_text(
            f"schema: spec-driven\nratified_by: {ratifier}\n", encoding="utf-8")
    return root


def test_archived_change_date_derives_from_the_folder_prefix():
    from pathlib import Path
    cid, status, _folder, date = generator._archived_change(Path("2026-07-09-add-x"))
    assert (cid, status, date) == ("add-x", "archived", "2026-07-09")


def test_ratification_emits_folder_date_and_governed_ratifier(tmp_path):
    root = _archived_corpus(tmp_path, ratifier="openxFactory ratify authority")
    snap = generate_snapshot(root, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit())
    change = _by_id(snap["changes"])["add-x"]
    # date FROM THE FOLDER, ratifier FROM THE GOVERNED METADATA (not proposal.md)
    assert change["ratification"] == {
        "ratifier": "openxFactory ratify authority", "date": "2026-07-09"}
    # and the resulting snapshot conforms (proving {ratifier, date} is valid)
    validator = find_openxfactory_validator()
    if validator is None:
        pytest.skip("no reachable openxFactory checkout")
    boundary = OutputBoundary(tmp_path / "v", ["out/"])
    path = snapshot.write_snapshot(snap, tmp_path / "v" / "out" / "s.json", boundary)
    assert snapshot.validate_snapshot(path, validator=validator).ok


def test_ratification_dormant_without_a_governed_ratifier(tmp_path):
    root = _archived_corpus(tmp_path, ratifier=None)  # proposal.md carries the phantom header
    snap = generate_snapshot(root, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit())
    change = _by_id(snap["changes"])["add-x"]
    # the phantom `Ratified by:` proposal header is IGNORED; with no governed
    # ratifier, ratification is omitted (date-only would fail the pinned schema)
    assert "ratification" not in change


# ---- possibles: bootstrap index (no register section) yields empty ------------

def test_bootstrap_index_yields_empty_possibles_but_names_still_flow(tmp_path):
    root = _mini_corpus(tmp_path / "repo", {
        "ideation/brainstorm/good.md": "Status: brainstorm\nTopics: alpha\n\nbody\n"})
    (root / "ideation" / "cross-reference.yaml").write_text(
        "schema_version: 1\nkind: ideation-cross-reference\n"
        "generation: {source_revision: deadbeef}\n"
        "topic_entries:\n"
        "  - {id: cl-alpha, name: Alpha Cluster, topics: [alpha],\n"
        "     tag_sources: [topics-header], members: [],\n"
        "     extension_fit: {has_promoted_fit: false, statement: none}}\n",
        encoding="utf-8")
    snap = generate_snapshot(root, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit())
    assert snap["possibles"] == []                                   # bootstrap: empty
    assert _by_id(snap["clusters"])["cl-alpha"]["name"] == "Alpha Cluster"  # name flows


# ---- origin_staging_id: the declared precedence order ------------------------
#
# `refine-demote-round-trip-mechanics` part 1. The field used to come from the
# possibles-register pick edge ALONE, and the forward transition removes the
# staging folder that edge points at — so it resolved to None for exactly the
# changes that had actually reached proposal, which is the condition a demote
# exists to reverse. Measured on the real corpus at the time: 12 of 12 active
# changes reported None, against ONE pick edge in the whole register (carrying no
# `change_id` at all). The answer was already on disk and unread: the forward
# transition writes an `origin:` block into the change's own `.openspec.yaml`.

def _change_with_origin(tmp_path, block: str, *, staging_folder: bool = True):
    """A minimal corpus with one ACTIVE change declaring `block` as its origin,
    and NO pick edge anywhere — the 12-of-12 shape."""
    # `good.md` declares a `Possible feats` section so the no-fabrication guard
    # in `fixtures.project_possibles` lets a register entry cited to it through —
    # without that, a pick edge silently never reaches the projection and the
    # precedence tests below would pass for the wrong reason.
    docs = {"ideation/brainstorm/good.md":
            "Status: brainstorm\nTopics: alpha\n\n## Possible feats\n\nbody\n"}
    if staging_folder:
        docs["ideation/staging/returned-topic/README.md"] = (
            "# Returned Topic\n\nStatus: staged\nKind: staging-packet\n"
            "Topics: alpha\n\nbody\n")
    root = _mini_corpus(tmp_path / "repo", docs)
    folder = root / "openspec" / "changes" / "add-x"
    folder.mkdir(parents=True)
    (folder / "proposal.md").write_text("# Change: add-x\n\nStatus: draft\n",
                                        encoding="utf-8")
    if block:
        (folder / ".openspec.yaml").write_text(
            "schema: spec-driven\ncreated: 2026-08-19\n" + block, encoding="utf-8")
    return root


def _origin_of(root):
    snap = generate_snapshot(root, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit())
    return _by_id(snap["changes"])["add-x"]["origin_staging_id"]


def test_origin_staging_id_resolves_from_the_changes_own_recorded_origin(tmp_path):
    """The 12-of-12 shape: a staged origin declared on the change, NO pick edge
    in the register, and the field still resolves."""
    root = _change_with_origin(tmp_path, (
        "origin:\n  kind: staged\n"
        "  id: fixture-repo:staging:returned-topic\n"
        "  path: ideation/staging/returned-topic\n"))
    assert _origin_of(root) == "returned-topic"
    # and there really is no pick edge doing the work
    snap = generate_snapshot(root, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit())
    assert snap["possibles"] == []


def test_origin_staging_id_is_the_paths_basename_not_the_namespaced_id(tmp_path):
    """The declared id is namespaced and the field is compared against
    `staged_topics[].staging_id`, which is the bare topic. Deriving from the path
    keeps ONE spelling of the id's shape. Here the two disagree deliberately, so a
    reader of `origin.id` produces a value that matches no staged topic."""
    root = _change_with_origin(tmp_path, (
        "origin:\n  kind: staged\n"
        "  id: fixture-repo:staging:SOME-OTHER-SPELLING\n"
        "  path: ideation/staging/returned-topic\n"))
    assert _origin_of(root) == "returned-topic"


def test_a_trailing_slash_on_the_declared_path_does_not_become_an_empty_topic(tmp_path):
    root = _change_with_origin(tmp_path, (
        "origin:\n  kind: staged\n"
        "  id: fixture-repo:staging:returned-topic\n"
        "  path: ideation/staging/returned-topic/\n"))
    assert _origin_of(root) == "returned-topic"


def test_a_nested_staging_source_resolves_to_the_topic_not_the_subfolder(tmp_path):
    """`proposal-support.py transition` accepts ANY directory below
    `ideation/staging/` as its source, so a real declared origin can read
    `ideation/staging/<topic>/openspec`. A basename rule answers `openspec` — a
    topic nobody named, and one the demote would then silently plan every
    returning file into. The topic is the first segment after the staging root."""
    root = _change_with_origin(tmp_path, (
        "origin:\n  kind: staged\n"
        "  id: fixture-repo:staging:returned-topic\n"
        "  path: ideation/staging/returned-topic/openspec\n"))
    assert _origin_of(root) == "returned-topic"


def test_a_declared_path_outside_the_staging_root_resolves_nothing(tmp_path):
    """A malformed declaration is a refusal case, not a parsing challenge: the
    origin contract puts staged sources below `ideation/staging/`, and guessing a
    topic out of a path that is not there would target a folder nobody chose."""
    for bad in ("docs/somewhere-else", "ideation/brainstorm/a-note",
                "ideation/staging", "returned-topic"):
        root = _change_with_origin(
            tmp_path / bad.replace("/", "_"),
            f"origin:\n  kind: staged\n"
            f"  id: fixture-repo:staging:returned-topic\n  path: {bad}\n",
            staging_folder=False)
        assert _origin_of(root) is None, bad


def test_an_ad_hoc_origin_resolves_nothing(tmp_path):
    """A change that never came from staging has no topic to return to, and
    inventing one would move material somewhere nobody chose."""
    root = _change_with_origin(tmp_path, (
        "origin:\n  kind: ad_hoc\n"
        "  id: fixture-repo:adhoc:2026-08-19-add-x\n"
        "  reason: born from an annotation\n"
        "  approved_by: Brett\n  approved_on: 2026-08-19\n"), staging_folder=False)
    assert _origin_of(root) is None


def test_an_ad_hoc_origin_carrying_a_staged_looking_path_still_resolves_nothing(tmp_path):
    """The KIND gate on its own, with the path guard unable to cover for it.
    `origin_errors` does not forbid extra keys, so an ad-hoc declaration can carry
    a `path` that looks exactly like a staged one — and the answer is still
    nothing, because the kind is the statement about where the change came from.
    Found by mutation: with only `test_an_ad_hoc_origin_resolves_nothing`, deleting
    the kind check passed, since a real ad-hoc origin has no `path` to parse."""
    root = _change_with_origin(tmp_path, (
        "origin:\n  kind: ad_hoc\n"
        "  id: fixture-repo:adhoc:2026-08-19-add-x\n"
        "  path: ideation/staging/returned-topic\n"
        "  reason: born from an annotation\n"
        "  approved_by: Brett\n  approved_on: 2026-08-19\n"))
    assert _origin_of(root) is None


def test_a_change_with_no_openspec_metadata_resolves_nothing(tmp_path):
    root = _change_with_origin(tmp_path, "", staging_folder=False)
    assert _origin_of(root) is None


def test_a_staged_origin_missing_its_path_resolves_nothing(tmp_path):
    """`origin.path` is the only field this reads; a staged origin without one is
    malformed (the proposal gate's own `origin_errors` says so) and must not be
    guessed at from the namespaced id."""
    root = _change_with_origin(tmp_path, (
        "origin:\n  kind: staged\n"
        "  id: fixture-repo:staging:returned-topic\n"), staging_folder=False)
    assert _origin_of(root) is None


def test_the_recorded_origin_outranks_a_disagreeing_pick_edge(tmp_path):
    """The precedence order is an ORDER, not a replacement: the recorded origin
    leads because it is the source the forward transition writes and does not
    destroy, and the pick edge keeps working wherever one still exists (asserted
    by the base-repo fixture, which has a pick edge and no `.openspec.yaml`)."""
    root = _change_with_origin(tmp_path, (
        "origin:\n  kind: staged\n"
        "  id: fixture-repo:staging:returned-topic\n"
        "  path: ideation/staging/returned-topic\n"))
    (root / "ideation" / "cross-reference.yaml").write_text(
        "schema_version: 1\nkind: ideation-cross-reference\n"
        "generation: {source_revision: deadbeef}\n"
        "possibles_register:\n"
        "  - id: pos-other\n    title: Other\n    claim: Something else.\n"
        "    state: picked\n"
        "    provenance: {document: ideation/brainstorm/good.md, section: Possible feats}\n"
        "    pick: {staging_id: a-stale-edge, change_id: add-x}\n",
        encoding="utf-8")
    snap = generate_snapshot(root, "fixture-repo",
                             source_revision=PINNED_REVISION, git=FakeGit())
    # the edge really did reach the projection — otherwise this passes vacuously
    assert [p["pick"] for p in snap["possibles"]] == [
        {"staging_id": "a-stale-edge", "change_id": "add-x"}]
    assert _origin_of(root) == "returned-topic"


def test_the_pick_edge_still_answers_where_no_origin_is_recorded(tmp_path):
    root = _change_with_origin(tmp_path, "")
    (root / "ideation" / "cross-reference.yaml").write_text(
        "schema_version: 1\nkind: ideation-cross-reference\n"
        "generation: {source_revision: deadbeef}\n"
        "possibles_register:\n"
        "  - id: pos-other\n    title: Other\n    claim: Something else.\n"
        "    state: picked\n"
        "    provenance: {document: ideation/brainstorm/good.md, section: Possible feats}\n"
        "    pick: {staging_id: returned-topic, change_id: add-x}\n",
        encoding="utf-8")
    assert _origin_of(root) == "returned-topic"
