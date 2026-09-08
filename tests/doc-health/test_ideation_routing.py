"""Fourteenth deterministic family (add-cross-factory-ideation-routing):
routing schema/vocabulary conformance, central Idea-ID allocation, unique
Idea/Claim definitions, paired-document identity, legal transitions, blocker
and destination-acceptance checks, structured-reference resolution, aggregation
backlog boundary, nightly-skip / strict-materialization external-path
resolution, lightweight Markdown provenance, proposal provenance, routing
aging, and organizer-evidence shape.

All tests are hermetic: the clean base fixture under
``fixtures/ideation-routing/`` is read-only, per-defect corpora are built under
``tmp_path``, and no test reads wall-clock time (``conftest.AS_OF`` is the
aging reference)."""

from __future__ import annotations

import shutil
from types import SimpleNamespace

import yaml

from conftest import AS_OF, FIXTURES

from doc_health import (AUTO_FIXABLE, CONTESTED, DEFAULT_THRESHOLDS, ERROR,
                        INFO, WARNING, Skip)
from doc_health import corpus, ideation_routing, runner
from doc_health.families import FAMILIES
from doc_health.runner import Context

from action_pins import assert_actions_pinned, harvest_static

fam = FAMILIES["ideation-routing"]
BASE = FIXTURES / "ideation-routing"
DAY_STR = AS_OF.isoformat()


# --- corpus/context helpers ---------------------------------------------------

def ctx_over(root, agg_root=None, thresholds=None, strict=False):
    """Build a Context over a corpus root. With no aggregation checkout the
    fixture layout (`conftest.make_ctx`) is used — every direct-child directory
    is a governed repo. With an aggregation checkout the aggregation layout is
    used — openxFactory plus xFactories/* only (installs/, ideation/, and other
    top-level dirs are the aggregation root, never governed corpora)."""
    if agg_root is not None:
        repo_paths = {}
        if (root / "openxFactory").is_dir():
            repo_paths["openxFactory"] = root / "openxFactory"
        factories = root / "xFactories"
        if factories.is_dir():
            for child in sorted(factories.iterdir()):
                if child.is_dir():
                    repo_paths[child.name] = child
    else:
        repo_paths = {p.name: p for p in sorted(root.iterdir()) if p.is_dir()}
    docs = []
    for name, path in repo_paths.items():
        docs.extend(corpus.load_docs(name, path))
    ctx = Context(
        repo_paths=repo_paths, docs=docs,
        capabilities={n: corpus.spec_capabilities(p)
                      for n, p in repo_paths.items()},
        change_ids={n: corpus.change_ids(p) for n, p in repo_paths.items()},
        git=None, thresholds=thresholds or dict(DEFAULT_THRESHOLDS),
        as_of=AS_OF, agg_root=agg_root)
    ctx.routing_strict = strict
    return ctx


def classes(findings):
    """The `[class]` tag on each finding's rule."""
    return [f.rule.split("]", 1)[0][1:] for f in findings]


def has_class(findings, cls):
    return cls in classes(findings)


def only_classes(findings):
    return sorted(set(classes(findings)))


# --- valid artifact builders (mutated per defect) -----------------------------

CLAIM_TRAILS = {
    "unresolved": ["unresolved"],
    "proposed": ["unresolved", "proposed"],
    "routed": ["unresolved", "proposed", "routed"],
    "deferred": ["unresolved", "deferred"],
    "rejected": ["unresolved", "rejected"],
}
RECORD_TRAILS = {
    "intake": ["intake"],
    "triaging": ["intake", "triaging"],
    "split": ["intake", "triaging", "split"],
    "routed": ["intake", "triaging", "routed"],
    "deferred": ["intake", "deferred"],
    "rejected": ["intake", "rejected"],
}
EARLY = "2026-01-01T00:00:00Z"


def _transitions(trail, last_occurred):
    """A contiguous null->...->trail[-1] history; only the final edge carries
    `last_occurred` so a record's latest-transition age is deterministic."""
    states = [None] + list(trail)
    out = []
    for i in range(len(states) - 1):
        out.append({"from": states[i], "to": states[i + 1], "actor_ref": "x",
                    "occurred_at": last_occurred if i == len(states) - 2
                    else EARLY, "evidence_refs": []})
    return out


def valid_claim(cid, disposition="proposed"):
    claim = {
        "claim_id": cid, "summary": "s",
        "source_ref": {"source_index": 0, "section": "sec",
                       "passage_sha256": "c" * 64},
        "proposed_owner": "openxFactory", "accepted_owner": None,
        "target_capability": None, "destination": None, "blocker": None,
        "dependencies": [], "domain_local_exclusions": [],
        "disposition": disposition, "rationale": "r", "acceptance": None,
        "transitions": _transitions(CLAIM_TRAILS[disposition], EARLY),
    }
    if disposition == "unresolved":
        claim["blocker"] = "owner unknown"
    if disposition == "routed":
        claim.update(
            accepted_owner="openxFactory", target_capability="cap",
            destination={"repository": "openxFactory", "path": "a/b.md",
                         "revision": "e" * 40},
            acceptance={"actor_ref": "o", "accepted_at": "2026-01-02T00:00:00Z",
                        "evidence_refs": ["acceptance note"]})
    return claim


def valid_record(idea="XFI-2026-050", status="triaging", claims=None,
                 last_transition="2026-07-01T00:00:00Z"):
    default_disposition = "routed" if status == "routed" else "proposed"
    return {
        "schema_version": 1,
        "kind": "xfactory_idea_routing_record",
        "idea_id": idea,
        "title": "Test idea",
        "scope": "cross_domain",
        "routing_status": status,
        "sources": [{"repository": "openxFactory",
                     "path": "ideation/brainstorm/cross-domain/x/idea.md",
                     "revision": "a" * 40, "context": "document",
                     "passage_sha256": "b" * 64}],
        "deduplication_rationale": None,
        "domains_touched": [], "candidate_owners": [],
        "claims": claims if claims is not None else [
            valid_claim(f"{idea}-C01", disposition=default_disposition)],
        "transitions": _transitions(RECORD_TRAILS[status], last_transition),
        "successors": [], "notes": None,
    }


def write_record(root, dirname, record, paired=True):
    d = root / "openxFactory" / "ideation" / "brainstorm" / "cross-domain" / \
        dirname
    d.mkdir(parents=True, exist_ok=True)
    (d / "routing.yaml").write_text(yaml.safe_dump(record, sort_keys=False),
                                    encoding="utf-8")
    if paired:
        (d / "routing-summary.md").write_text(
            f"Status: record\nIdea ID: {record['idea_id']}\n", encoding="utf-8")
    return d


def write_doc(root, relpath, text, repo="openxFactory"):
    p = root / repo / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def empty_root(tmp_path):
    root = tmp_path / "corpus"
    (root / "openxFactory" / "ideation").mkdir(parents=True)
    return root


# --- clean base + prospective compatibility -----------------------------------

def test_clean_base_fixture_yields_zero_findings():
    assert fam(ctx_over(BASE)) == []


def test_ordinary_documents_without_routing_sidecars_are_untouched(tmp_path):
    # A repo with brainstorm/docs prose but no routing artifact at all: the
    # family must be silent (spec "Prospective compatibility and migration";
    # delta scenario "Ordinary document lacks routing metadata").
    root = empty_root(tmp_path)
    write_doc(root, "ideation/brainstorm/idea.md",
              "# Idea\n\nStatus: brainstorm\n\nNo routing metadata here.\n")
    write_doc(root, "docs/policy.md", "# Policy\n\nStatus: standard\n")
    assert fam(ctx_over(root)) == []


def test_pyyaml_unavailable_skips(monkeypatch):
    monkeypatch.setattr(ideation_routing, "yaml", None)
    got = fam(ctx_over(BASE))
    assert isinstance(got, Skip) and got.family == "ideation-routing"


def test_unparseable_record_is_reported_not_crashed(tmp_path):
    root = empty_root(tmp_path)
    d = root / "openxFactory" / "ideation" / "brainstorm" / "inbox" / "x"
    d.mkdir(parents=True)
    (d / "routing.yaml").write_text("kind: xfactory_idea_routing_record\n"
                                    ": : not valid yaml : :\n", encoding="utf-8")
    got = fam(ctx_over(root))
    assert any("unparseable" in f.rule for f in got)


# --- schema / vocabulary ------------------------------------------------------

def test_invalid_scope_and_status_flagged(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record()
    rec["scope"] = "totally-made-up"
    rec["routing_status"] = "archived"
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    rules = "\n".join(f.rule for f in got)
    assert "scope 'totally-made-up' is outside" in rules
    assert "routing_status 'archived' is outside" in rules
    assert all(f.resolution == CONTESTED for f in got if "[schema]" in f.rule)
    # PIN (commissioned 2026-08-27, after `promotion_fidelity._ACTION` was
    # mutated and 85 tests stayed green — no doc-health family's action line
    # was pinned anywhere). An action line is operator guidance rendered in
    # every ranked-plan row; nothing else in this repository notices it
    # changing, so each family gets one verbatim pin in its own suite. This
    # family passes literals at many construction sites; the two this fixture
    # already produces are pinned here rather than duplicated.
    scope_action = next(f.action for f in got if "scope 'totally-made-up'" in f.rule)
    status_action = next(f.action for f in got if "routing_status 'archived'" in f.rule)
    assert scope_action == "record a controlled routing scope"
    assert status_action == "record a controlled routing status"


def test_multi_source_without_dedup_flagged(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record()
    rec["sources"].append({"repository": "xFactories/MedxFactory",
                           "path": "ideation/brainstorm/o.md",
                           "revision": "d" * 40})
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    assert has_class(got, "schema")
    assert any("deduplication_rationale" in f.rule for f in got)


def test_intake_pending_capture_misuse_flagged(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record(status="triaging")
    rec["sources"][0]["revision"] = "pending_capture"
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    assert any("pending_capture at routing_status" in f.rule for f in got)


def test_pending_capture_valid_during_intake(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record(status="intake",
                       claims=[valid_claim("XFI-2026-050-C01",
                                           disposition="unresolved")])
    rec["claims"][0]["blocker"] = "owner unknown"
    rec["sources"][0]["revision"] = "pending_capture"
    rec["transitions"] = [
        {"from": None, "to": "intake", "actor_ref": "x",
         "occurred_at": "2026-07-08T00:00:00Z", "evidence_refs": []}]
    write_record(root, "XFI-2026-050", rec)
    assert fam(ctx_over(root)) == []


# --- transitions --------------------------------------------------------------

def test_illegal_routing_transition_flagged(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record(status="routed")
    # intake -> routed is not a legal edge (must pass through triaging).
    rec["transitions"] = [
        {"from": None, "to": "intake", "actor_ref": "x",
         "occurred_at": "2026-07-01T00:00:00Z", "evidence_refs": []},
        {"from": "intake", "to": "routed", "actor_ref": "x",
         "occurred_at": "2026-07-02T00:00:00Z", "evidence_refs": []}]
    rec["claims"] = [valid_claim("XFI-2026-050-C01", disposition="routed")]
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    assert any("illegal transition 'intake' -> 'routed'" in f.rule for f in got)
    assert has_class(got, "transition")


def test_noncontiguous_transition_history_flagged(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record(status="triaging")
    rec["transitions"] = [
        {"from": None, "to": "intake", "actor_ref": "x",
         "occurred_at": "2026-07-01T00:00:00Z", "evidence_refs": []},
        {"from": "split", "to": "triaging", "actor_ref": "x",
         "occurred_at": "2026-07-02T00:00:00Z", "evidence_refs": []}]
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    assert has_class(got, "transition-chain")


def test_illegal_claim_transition_flagged(tmp_path):
    root = empty_root(tmp_path)
    claim = valid_claim("XFI-2026-050-C01", disposition="routed")
    # unresolved -> routed skips the mandatory proposed step.
    claim["transitions"] = [
        {"from": None, "to": "unresolved", "actor_ref": "x",
         "occurred_at": "2026-07-01T00:00:00Z", "evidence_refs": []},
        {"from": "unresolved", "to": "routed", "actor_ref": "x",
         "occurred_at": "2026-07-02T00:00:00Z", "evidence_refs": []}]
    claim.update(accepted_owner="openxFactory", target_capability="cap",
                 destination={"repository": "openxFactory", "path": "a/b.md",
                              "revision": "e" * 40},
                 acceptance={"actor_ref": "o", "accepted_at": "2026-07-02T0:0:0Z",
                             "evidence_refs": ["note"]})
    rec = valid_record(status="split", claims=[claim])
    rec["transitions"].append(
        {"from": "triaging", "to": "split", "actor_ref": "x",
         "occurred_at": "2026-07-03T00:00:00Z", "evidence_refs": []})
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    assert any("illegal transition 'unresolved' -> 'routed'" in f.rule
               for f in got)


# --- claim identity -----------------------------------------------------------

def test_claim_id_prefix_mismatch_flagged(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record(idea="XFI-2026-050",
                       claims=[valid_claim("XFI-2026-999-C01")])
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    assert has_class(got, "claim-id")
    assert any("does not derive from record idea_id" in f.rule for f in got)


def test_duplicate_claim_id_within_record_flagged_once(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record(claims=[valid_claim("XFI-2026-050-C01"),
                               valid_claim("XFI-2026-050-C01")])
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    dup = [f for f in got if "[duplicate-claim]" in f.rule]
    # Intra-record duplicate is reported exactly once (not also by the
    # cross-record corpus check).
    assert len(dup) == 1 and "defined 2 times in one record" in dup[0].rule


def test_duplicate_claim_id_across_records_flagged(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "slot-a",
                 valid_record(idea="XFI-2026-050",
                              claims=[valid_claim("XFI-2026-050-C01")]))
    write_record(root, "slot-b",
                 valid_record(idea="XFI-2026-051",
                              claims=[valid_claim("XFI-2026-050-C01")]))
    got = fam(ctx_over(root))
    dup = [f for f in got if "[duplicate-claim]" in f.rule
           and "in 2 records" in f.rule]
    assert len(dup) == 2  # one finding per offending record


def test_duplicate_canonical_record_for_one_idea_flagged(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "slot-a", valid_record(idea="XFI-2026-050"))
    write_record(root, "slot-b", valid_record(idea="XFI-2026-050",
                                               claims=[valid_claim(
                                                   "XFI-2026-050-C01")]))
    got = fam(ctx_over(root))
    dup = [f for f in got if "[duplicate-idea]" in f.rule]
    assert len(dup) == 2
    # cross-record duplicate claim id is ALSO expected here (same claim in two
    # records) — the duplicate-idea class is what this test asserts on.
    assert all("2 canonical routing records" in f.rule for f in dup)


# --- blocker / destination acceptance -----------------------------------------

def test_unresolved_claim_without_blocker_flagged(tmp_path):
    root = empty_root(tmp_path)
    claim = valid_claim("XFI-2026-050-C01", disposition="unresolved")
    claim["blocker"] = None
    write_record(root, "XFI-2026-050", valid_record(claims=[claim]))
    got = fam(ctx_over(root))
    assert has_class(got, "blocker")
    assert any("names no blocker" in f.rule for f in got)


def test_unresolved_claim_with_blocker_is_accepted(tmp_path):
    root = empty_root(tmp_path)
    claim = valid_claim("XFI-2026-050-C01", disposition="unresolved")
    claim["blocker"] = "Owner unknown; needs triage."
    write_record(root, "XFI-2026-050", valid_record(claims=[claim]))
    assert fam(ctx_over(root)) == []


def test_routed_claim_without_acceptance_flagged(tmp_path):
    root = empty_root(tmp_path)
    claim = valid_claim("XFI-2026-050-C01", disposition="routed")
    claim["acceptance"] = None  # routed but no destination-owner acceptance
    rec = valid_record(status="split", claims=[claim])
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    assert has_class(got, "routed-acceptance")


def test_routed_record_with_active_claim_flagged(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record(status="routed",
                       claims=[valid_claim("XFI-2026-050-C01",
                                           disposition="proposed")])
    rec["transitions"] = [
        {"from": None, "to": "intake", "actor_ref": "x",
         "occurred_at": "2026-07-01T00:00:00Z", "evidence_refs": []},
        {"from": "intake", "to": "triaging", "actor_ref": "x",
         "occurred_at": "2026-07-02T00:00:00Z", "evidence_refs": []},
        {"from": "triaging", "to": "routed", "actor_ref": "x",
         "occurred_at": "2026-07-03T00:00:00Z", "evidence_refs": []}]
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    assert any("routed while claim" in f.rule for f in got)


# --- references (stale / traversal / normalization) ---------------------------

def test_unknown_repository_reference_flagged(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record()
    rec["sources"][0]["repository"] = "NotARepo"
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root, agg_root=root))
    assert has_class(got, "reference")
    assert any("NotARepo" in f.rule for f in got)


def test_path_traversal_reference_flagged(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record()
    rec["sources"][0]["path"] = "../MedxFactory/ideation/x.md"
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    ref = [f for f in got if "[reference]" in f.rule]
    assert ref and any("path traversal" in f.rule for f in ref)
    assert all(f.resolution == CONTESTED for f in ref)


def test_backslash_path_is_auto_fixable_normalization(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record()
    rec["sources"][0]["path"] = "ideation\\brainstorm\\idea.md"
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    norm = [f for f in got if "[path-normalization]" in f.rule]
    assert len(norm) == 1
    assert norm[0].severity == WARNING and norm[0].resolution == AUTO_FIXABLE
    # It must NOT also be reported as a contested reference defect.
    assert not any("[reference]" in f.rule and "backslash" not in f.rule
                   for f in got)


# --- paired documents ---------------------------------------------------------

def test_missing_paired_document_flagged(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"),
                 paired=False)
    got = fam(ctx_over(root))
    assert any("[paired-document]" in f.rule and "no paired" in f.rule
               for f in got)


def test_paired_document_idea_id_mismatch_flagged(tmp_path):
    root = empty_root(tmp_path)
    d = write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"),
                     paired=False)
    (d / "routing-summary.md").write_text(
        "Status: record\nIdea ID: XFI-2026-999\n", encoding="utf-8")
    got = fam(ctx_over(root))
    assert any("[paired-document]" in f.rule and "does not match" not in f.rule
               and "XFI-2026-999" in f.rule for f in got)


def test_paired_directory_idea_id_mismatch_flagged(tmp_path):
    root = empty_root(tmp_path)
    # Idea-ID-named directory that disagrees with the record's idea_id.
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"))
    # rename by re-writing under an idea-id dir that mismatches
    d = root / "openxFactory/ideation/brainstorm/inbox/XFI-2026-777"
    d.mkdir(parents=True)
    (d / "routing.yaml").write_text(
        yaml.safe_dump(valid_record(idea="XFI-2026-050",
                                    claims=[valid_claim("XFI-2026-050-C02")]),
                       sort_keys=False), encoding="utf-8")
    (d / "idea.md").write_text("Status: record\nIdea ID: XFI-2026-050\n",
                               encoding="utf-8")
    got = fam(ctx_over(root))
    assert any("does not match its directory 'XFI-2026-777'" in f.rule
               for f in got)


# --- central allocation -------------------------------------------------------

def test_unallocated_idea_flagged_when_index_present(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"))
    write_doc(root, "ideation/routing-index.yaml", yaml.safe_dump({
        "schema_version": 1, "kind": "xfactory_ideation_routing_index",
        "allocations": [], "notes": None}, sort_keys=False))
    got = fam(ctx_over(root))
    assert any("[central-allocation]" in f.rule
               and "not allocated" in f.rule for f in got)


def test_duplicate_allocation_flagged(tmp_path):
    root = empty_root(tmp_path)
    write_doc(root, "ideation/routing-index.yaml", yaml.safe_dump({
        "schema_version": 1, "kind": "xfactory_ideation_routing_index",
        "allocations": [
            {"idea_id": "XFI-2026-050",
             "routing_record": {"repository": "openxFactory", "path": "x"}},
            {"idea_id": "XFI-2026-050",
             "routing_record": {"repository": "openxFactory", "path": "x"}}],
        "notes": None}, sort_keys=False))
    got = fam(ctx_over(root))
    assert any("allocated 2 times" in f.rule for f in got)


def test_dangling_allocation_pointer_flagged(tmp_path):
    root = empty_root(tmp_path)
    write_doc(root, "ideation/routing-index.yaml", yaml.safe_dump({
        "schema_version": 1, "kind": "xfactory_ideation_routing_index",
        "allocations": [
            {"idea_id": "XFI-2026-050",
             "routing_record": {"repository": "openxFactory",
                                "path": "ideation/nowhere/routing.yaml"}}],
        "notes": None}, sort_keys=False))
    got = fam(ctx_over(root))
    assert any("does not exist" in f.rule for f in got)


# --- aging --------------------------------------------------------------------

def test_routing_record_aging_warning_and_error(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "warn", valid_record(idea="XFI-2026-060",
                 status="triaging", last_transition="2026-06-01T00:00:00Z"))
    write_record(root, "err", valid_record(
        idea="XFI-2026-061", status="intake",
        claims=[valid_claim("XFI-2026-061-C01", disposition="unresolved")],
        last_transition="2026-03-01T00:00:00Z"))
    got = [f for f in fam(ctx_over(root)) if "[aging]" in f.rule]
    sev = sorted((f.severity, f.repo) for f in got)
    assert (WARNING, "openxFactory") in sev  # 38 days
    assert (ERROR, "openxFactory") in sev    # 130 days
    assert all(f.resolution == CONTESTED for f in got)


def test_routed_and_deferred_records_do_not_age(tmp_path):
    root = empty_root(tmp_path)
    # Very old latest transition — a deferred and a routed record must NOT age.
    write_record(root, "def", valid_record(
        idea="XFI-2026-070", status="deferred",
        claims=[valid_claim("XFI-2026-070-C01", disposition="deferred")],
        last_transition="2026-01-01T00:00:00Z"))
    write_record(root, "rtd", valid_record(
        idea="XFI-2026-071", status="routed",
        last_transition="2026-01-01T00:00:00Z"))
    assert not any("[aging]" in f.rule for f in fam(ctx_over(root)))


def test_non_default_aging_thresholds_change_severity(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "warn", valid_record(idea="XFI-2026-060",
                 status="triaging", last_transition="2026-06-01T00:00:00Z"))
    # 38 days: default => warning; with error threshold lowered to 30 => error.
    thresholds = dict(DEFAULT_THRESHOLDS,
                      routing_warning_days=10, routing_error_days=30)
    got = [f for f in fam(ctx_over(root, thresholds=thresholds))
           if "[aging]" in f.rule]
    assert got and got[0].severity == ERROR


# --- aggregation backlog boundary ---------------------------------------------

def test_aggregation_root_ideation_placement_flagged(tmp_path):
    root = empty_root(tmp_path)
    (root / "ideation" / "brainstorm").mkdir(parents=True)
    (root / "ideation" / "brainstorm" / "backlog.md").write_text(
        "# Backlog\n\nStatus: brainstorm\n", encoding="utf-8")
    got = fam(ctx_over(root, agg_root=root))
    backlog = [f for f in got if "[aggregation-backlog]" in f.rule]
    assert len(backlog) == 1
    assert backlog[0].repo == "xFactory" and backlog[0].severity == ERROR


def test_no_aggregation_backlog_without_agg_root(tmp_path):
    root = empty_root(tmp_path)
    assert not any("[aggregation-backlog]" in f.rule for f in fam(ctx_over(root)))


# --- external-path resolution (nightly skip vs strict materialization) --------

def _record_referencing_install(root, dirname="ext"):
    rec = valid_record(idea="XFI-2026-080")
    rec["sources"].append({"repository": "installs/cloudpc-install",
                           "path": "planning/host.md", "revision": "f" * 40})
    write_record(root, dirname, rec)


def test_external_path_skipped_in_nightly_reported_not_passed(tmp_path):
    root = empty_root(tmp_path)
    _record_referencing_install(root)
    got = fam(ctx_over(root, agg_root=root))
    ext = [f for f in got if "[external-path]" in f.rule]
    assert len(ext) == 1
    assert ext[0].severity == INFO and "skipped" in ext[0].rule
    assert "installs/cloudpc-install" in ext[0].path


def test_external_path_error_in_strict_mode(tmp_path):
    root = empty_root(tmp_path)
    _record_referencing_install(root)
    got = fam(ctx_over(root, agg_root=root, strict=True))
    ext = [f for f in got if "[external-path]" in f.rule]
    assert len(ext) == 1 and ext[0].severity == ERROR
    assert "materializing" in ext[0].rule


def test_materialized_external_path_not_flagged(tmp_path):
    root = empty_root(tmp_path)
    _record_referencing_install(root)
    (root / "installs" / "cloudpc-install").mkdir(parents=True)
    got = fam(ctx_over(root, agg_root=root, strict=True))
    assert not any("[external-path]" in f.rule for f in got)


# --- Markdown provenance (copied record / destination / staged pointers) ------

def test_copied_full_routing_record_in_destination_flagged(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"))
    write_doc(root, "ideation/staging/topic/liaison.md",
              "# Liaison skeleton\n\nStatus: draft\n\n"
              "```yaml\nkind: xfactory_idea_routing_record\n"
              "idea_id: XFI-2026-050\n```\n")
    got = fam(ctx_over(root))
    assert any("[copied-record]" in f.rule for f in got)


def test_fenced_example_in_brainstorm_is_not_flagged(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"))
    # A source brainstorm that merely illustrates the schema in a fence and a
    # fenced Claim ID reference — neither is a real definition/copy.
    write_doc(root, "ideation/brainstorm/notes.md",
              "# Notes\n\nStatus: brainstorm\n\n"
              "```yaml\nkind: xfactory_idea_routing_record\n"
              "idea_id: XFI-2026-999\n```\n\n"
              "Inline `Claim IDs: XFI-2026-999-C09` in prose too.\n")
    got = fam(ctx_over(root))
    assert not any("[copied-record]" in f.rule for f in got)
    assert not any("[staged-pointer]" in f.rule for f in got)


def test_destination_misleading_singular_idea_id_flagged(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"))
    write_doc(root, "ideation/staging/topic/dest.md",
              "# Destination\n\nStatus: draft\n"
              "Idea ID: XFI-2026-050\n"
              "Source Idea IDs: XFI-2026-050\n"
              "Claim IDs: XFI-2026-050-C01\n")
    got = fam(ctx_over(root))
    assert any("[destination-provenance]" in f.rule
               and "misleading singular Idea ID" in f.rule for f in got)


def test_routing_records_header_must_be_json_array(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"))
    write_doc(root, "ideation/staging/topic/dest.md",
              "# Destination\n\nStatus: draft\n"
              "Source Idea IDs: XFI-2026-050\n"
              "Claim IDs: XFI-2026-050-C01\n"
              "Routing records: not-a-json-array\n")
    got = fam(ctx_over(root))
    assert any("Routing records header does not parse" in f.rule for f in got)


def test_routing_records_header_valid_json_array_ok(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"))
    ref = ('[{"repository": "openxFactory", "path": '
           '"ideation/brainstorm/cross-domain/XFI-2026-050/routing.yaml", '
           '"revision": "%s"}]' % ("a" * 40))
    write_doc(root, "ideation/staging/topic/dest.md",
              "# Destination\n\nStatus: draft\n"
              "Source Idea IDs: XFI-2026-050\n"
              "Claim IDs: XFI-2026-050-C01\n"
              f"Routing records: {ref}\n")
    assert not any("[destination-provenance]" in f.rule for f in fam(ctx_over(root)))


def test_unresolved_staged_claim_pointer_flagged(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"))
    write_doc(root, "ideation/staging/topic/dest.md",
              "# Destination\n\nStatus: draft\n"
              "Source Idea IDs: XFI-2026-050\n"
              "Claim IDs: XFI-2026-050-C99\n")  # C99 does not exist
    got = fam(ctx_over(root))
    assert any("[staged-pointer]" in f.rule and "XFI-2026-050-C99" in f.rule
               for f in got)


def test_source_idea_id_header_without_record_flagged(tmp_path):
    root = empty_root(tmp_path)
    write_doc(root, "ideation/brainstorm/orphan.md",
              "# Orphan\n\nStatus: brainstorm\nIdea ID: XFI-2026-050\n")
    got = fam(ctx_over(root))
    assert any("[staged-pointer]" in f.rule
               and "no canonical routing record" in f.rule for f in got)


# --- proposal provenance ------------------------------------------------------

def _write_manifest(root, provenance):
    write_doc(root,
              "openspec/changes/add-liaison/supporting-docs/manifest.yaml",
              yaml.safe_dump({"format_version": 1, "files": [],
                              "ideation_provenance": provenance},
                             sort_keys=False))


def test_proposal_provenance_pending_capture_flagged(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"))
    _write_manifest(root, [{
        "idea_id": "XFI-2026-050", "claim_ids": ["XFI-2026-050-C01"],
        "routing_record": {"repository": "openxFactory", "path": "r.yaml",
                           "revision": "pending_capture"}}])
    got = fam(ctx_over(root))
    assert any("[proposal-provenance]" in f.rule and "pending_capture" in f.rule
               for f in got)


def test_proposal_provenance_missing_claim_flagged(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"))
    _write_manifest(root, [{
        "idea_id": "XFI-2026-050", "claim_ids": ["XFI-2026-050-C09"],
        "routing_record": {"repository": "openxFactory", "path": "r.yaml",
                           "revision": "a" * 40}}])
    got = fam(ctx_over(root))
    assert any("absent from the pinned routing record" in f.rule for f in got)


def test_proposal_without_ideation_provenance_is_valid(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"))
    write_doc(root,
              "openspec/changes/add-x/supporting-docs/manifest.yaml",
              yaml.safe_dump({"format_version": 1, "files": []},
                             sort_keys=False))
    assert not any("[proposal-provenance]" in f.rule for f in fam(ctx_over(root)))


def test_valid_proposal_provenance_ok(tmp_path):
    root = empty_root(tmp_path)
    write_record(root, "XFI-2026-050", valid_record(idea="XFI-2026-050"))
    _write_manifest(root, [{
        "idea_id": "XFI-2026-050", "claim_ids": ["XFI-2026-050-C01"],
        "routing_record": {"repository": "openxFactory",
                           "path": "ideation/x/routing.yaml",
                           "revision": "a" * 40}}])
    assert not any("[proposal-provenance]" in f.rule for f in fam(ctx_over(root)))


# --- resolution classes -------------------------------------------------------

def test_resolution_classes_are_contested_except_normalization(tmp_path):
    root = empty_root(tmp_path)
    rec = valid_record()
    rec["scope"] = "bad"                                  # contested schema
    rec["sources"][0]["path"] = "ideation\\a\\b.md"        # auto-fixable
    write_record(root, "XFI-2026-050", rec)
    got = fam(ctx_over(root))
    for f in got:
        if "[path-normalization]" in f.rule:
            assert f.resolution == AUTO_FIXABLE
        elif "[external-path]" in f.rule:
            assert f.resolution == AUTO_FIXABLE
        else:
            assert f.resolution == CONTESTED, f.rule


# --- runner integration -------------------------------------------------------

def test_runner_family_ideation_routing_integration(tmp_path):
    repo = tmp_path / "openxFactory"
    shutil.copytree(BASE / "openxFactory", repo)
    report_out = tmp_path / "report.md"
    rc = runner.main([
        "--single-repo", str(repo), "--family", "ideation-routing",
        "--as-of", DAY_STR, "--report-out", str(report_out)])
    assert rc == 0
    text = report_out.read_text(encoding="utf-8")
    assert "### ideation-routing" in text


def test_runner_family_ideation_routing_reports_defect(tmp_path):
    root = tmp_path / "corpus"
    (root / "openxFactory" / "ideation").mkdir(parents=True)
    rec = valid_record(idea="XFI-2026-050")
    rec["scope"] = "not-a-scope"
    d = root / "openxFactory/ideation/brainstorm/cross-domain/XFI-2026-050"
    d.mkdir(parents=True)
    (d / "routing.yaml").write_text(yaml.safe_dump(rec, sort_keys=False),
                                    encoding="utf-8")
    (d / "routing-summary.md").write_text(
        "Status: record\nIdea ID: XFI-2026-050\n", encoding="utf-8")
    report_out = tmp_path / "report.md"
    rc = runner.main([
        "--single-repo", str(root / "openxFactory"),
        "--family", "ideation-routing", "--as-of", DAY_STR,
        "--fail-on", "error", "--report-out", str(report_out)])
    assert rc == 1  # error-severity finding trips the gate
    text = report_out.read_text(encoding="utf-8")
    assert "### ideation-routing" in text
    assert "not-a-scope" in text


def test_runner_config_discloses_non_default_routing_thresholds(tmp_path):
    root = tmp_path / "corpus"
    (root / "openxFactory" / "ideation").mkdir(parents=True)
    cfg = tmp_path / "cfg.yaml"
    cfg.write_text("thresholds:\n  routing_warning_days: 7\n", encoding="utf-8")
    report_out = tmp_path / "report.md"
    rc = runner.main([
        "--single-repo", str(root / "openxFactory"),
        "--family", "ideation-routing", "--as-of", DAY_STR,
        "--config", str(cfg), "--report-out", str(report_out)])
    assert rc == 0
    text = report_out.read_text(encoding="utf-8")
    assert "routing_warning_days=7" in text


# --- P4b: root-level governed-repo recognition (split-openxwallet-repo 11.2) --
#
# `_governed_repo_ids` decides which repository ids are resolvable WITHOUT
# materialization. Before P4b it derived the whole set from `ctx.repo_paths`,
# which `corpus.discover_repos` fills with `openxFactory` plus `xFactories/*` and
# nothing else — so `openXwallet`, pinned at the aggregation ROOT, was classed
# `external` and fell under the nightly-skip / strict-materialization path. The
# openAvatar precedent is the empirical proof (council concern 4): a root-level
# repository derives nothing automatically.

def test_governed_repo_ids_admit_the_root_level_product_allowlist():
    ids = ideation_routing._governed_repo_ids(
        SimpleNamespace(repo_paths={"openxFactory": None,
                                    "LedgerxFactory": None}))
    assert ids == {"openxFactory", "xFactories/LedgerxFactory",
                   "openAvatar", "openXwallet"}


def test_governed_repo_ids_admit_root_products_with_no_checkout_in_scope():
    """The allowlist is a claim about TOPOLOGY, not about this run's checkout.

    `discover_repos` can never place a root-level product in `repo_paths`, so a
    set derived from it alone would stay permanently narrow — which is the whole
    defect. A single-repo self-gate has one entry and must still resolve a
    reference into `openXwallet`."""
    ids = ideation_routing._governed_repo_ids(
        SimpleNamespace(repo_paths={"openxFactory": None}))
    assert {"openAvatar", "openXwallet"} <= ids


def test_governed_repo_ids_never_prefix_a_root_product_with_xfactories():
    """Defensive: if `discover_repos` is ever widened to sweep a root product's
    own documents, the two sites must not disagree about that product's id —
    `xFactories/openXwallet` is a repository that exists nowhere."""
    ids = ideation_routing._governed_repo_ids(
        SimpleNamespace(repo_paths={"openxFactory": None, "openXwallet": None}))
    assert "openXwallet" in ids
    assert "xFactories/openXwallet" not in ids


def test_governed_repo_ids_do_not_admit_installs():
    """The allowlist, not the rule. Admitting every root-level `.gitmodules` pin
    would enrol the nine `installs/*` runtime repositories as governed."""
    ids = ideation_routing._governed_repo_ids(
        SimpleNamespace(repo_paths={"openxFactory": None}))
    assert not any(i.startswith("installs/") for i in ids)


def test_convention_mode_recognizes_a_root_product_id(tmp_path):
    """A bare-name repository id has no PATTERN to be accepted by — it is
    shape-indistinguishable from a typo — so the convention fallback needs the
    allowlist too, or openxFactory's own `--single-repo` self-gate reports a
    sound reference into `openXwallet` as an unknown repository."""
    known, mode, _agg = ideation_routing._known_repositories(
        SimpleNamespace(repo_paths={"openxFactory": None}, agg_root=None))
    assert mode == "convention"
    assert ideation_routing._repository_unknown_reason(
        "openXwallet", known, mode) is None
    assert ideation_routing._repository_unknown_reason(
        "openAvatar", known, mode) is None
    reason = ideation_routing._repository_unknown_reason(
        "openNotAProduct", known, mode)
    assert reason is not None and "root-level neutral product" in reason


def test_allowlist_lives_in_corpus_as_the_single_authority():
    assert corpus.ROOT_LEVEL_GOVERNED_PRODUCTS == ("openAvatar", "openXwallet")
    assert (ideation_routing.ROOT_LEVEL_GOVERNED_PRODUCTS
            is corpus.ROOT_LEVEL_GOVERNED_PRODUCTS)


def test_every_action_string_the_ideation_routing_family_can_emit_is_pinned_verbatim(
        tmp_path):
    """`fam_ideation_routing` raises SIXTY-THREE distinct action strings
    across its nineteen finding classes. `#448` (`cadc05ec`) pinned two of
    them (`test_invalid_scope_and_status_flagged`, above — the family's
    thinnest coverage of the twenty pinned in that change, 2 of 42 measured
    at the time). Steward follow-up (Brett, 2026-08-28) widens that to the
    whole set, table-driven.

    SIXTY-ONE are pinned BEHAVIOURALLY: one consolidated `tmp_path` corpus
    below packs a central routing-index (duplicate allocation, an
    unallocated record, a broken allocation pointer, a bad structured
    reference), a maximally-malformed routing record (bad idea_id/scope/
    status/schema_version, three defective sources, a broken transition
    chain, six defective claims covering every claim-shape/claim-id/
    blocker/routed-acceptance branch, and five defective structured
    references covering unknown-repository/missing-path/backslash-
    normalization/traversal/external-path), two records sharing one Idea ID
    (duplicate-idea, corpus claim uniqueness), a routed record whose active
    claim trips the routed-record gate, two records isolating the
    missing-sources and non-list-claims shapes, two paired-document defects
    (missing pairing, mismatched Idea ID), a consolidated Markdown
    destination (copied-record, multiple/misleading Idea ID headers,
    unresolved staged-pointers, both `Routing records:` header defects), an
    aggregation-root ideation backlog, an external (unmaterialized) pinned
    repository read in both nightly and strict mode, two active-proposal
    manifests covering every `ideation_provenance` shape defect, and two
    unparseable YAML files (index and record) in a second repo — into one
    run of the family (plus a second run with `ctx.routing_strict = True`
    for the strict-mode external-path action).

    The remaining TWO are pinned STATICALLY because they are structurally
    UNREACHABLE through `fam_ideation_routing`'s own collection path, not
    merely uncovered by this fixture: `_collect` only appends a parsed
    YAML document to `records` when it is a `dict` AND
    `dict.get("kind") == RECORD_KIND` — so a record whose top-level YAML is
    not a mapping, or whose `kind` is wrong, is silently skipped by
    `_collect` itself and never reaches `_shape_findings`, where the
    "restore the routing-record shape or remove the file" and "declare the
    canonical routing-record kind" literals live. Read via `ast` (scoped to
    the whole module — `ideation_routing.py` is a single-family module) as
    the honest fallback the module docstring describes for exactly this
    case.
    """
    root = tmp_path
    openx = root / "openxFactory"
    for d in ("ideation/inbox/XFI-2026-001", "ideation/inbox/XFI-2026-002",
              "ideation/inbox/XFI-2026-003", "ideation/inbox/XFI-2026-005",
              "ideation/inbox/XFI-2026-006", "ideation/cross-domain/XFI-2026-004",
              "ideation/cross-domain/consolidated"):
        (openx / d).mkdir(parents=True)

    (openx / "ideation/routing-index.yaml").write_text("""\
kind: xfactory_ideation_routing_index
schema_version: 1
allocations:
  - idea_id: XFI-2026-001
    routing_record:
      repository: openxFactory
      path: ideation/inbox/XFI-2026-001/routing.yaml
  - idea_id: XFI-2026-001
    routing_record:
      repository: openxFactory
      path: ideation/inbox/XFI-2026-001/routing.yaml
  - idea_id: XFI-2026-099
    routing_record:
      repository: openxFactory
      path: ideation/inbox/XFI-2026-099/routing.yaml
stray_reference:
  repository: bad
  path: ../escape.md
""")

    # RECORD A: the shape/claim/transition/reference showcase. idea_id is
    # deliberately malformed ("BAD-ID") sitting in a directory literally
    # named "XFI-2026-001", which doubles as the paired-document mismatch
    # scenario (directory name vs. the record's own idea_id).
    (openx / "ideation/inbox/XFI-2026-001/routing.yaml").write_text("""\
kind: xfactory_idea_routing_record
schema_version: 2
idea_id: "BAD-ID"
scope: not-a-scope
routing_status: not-a-status
sources:
  - repository: openxFactory
    path: ideation/inbox/XFI-2026-001/idea.md
    revision: short
  - repository: openxFactory
    path: ideation/inbox/XFI-2026-001/idea.md
    revision: pending_capture
  - not-a-mapping-source
transitions:
  - from: "not-null"
    to: intake
    occurred_at: "2026-01-01T00:00:00Z"
  - from: bogus_from
    to: intake
    occurred_at: "2026-01-02T00:00:00Z"
  - from: intake
    to: not_a_real_state
    occurred_at: "2026-01-03T00:00:00Z"
  - not-a-mapping-transition
claims:
  - claim_id: "wrong-format"
  - claim_id: "dup-claim"
    disposition: unresolved
  - claim_id: "dup-claim"
    disposition: unresolved
    blocker: "same blocker"
  - claim_id: "wrong-format2"
    disposition: proposed
  - claim_id: "wrong-format3"
    disposition: routed
  - not-a-mapping-claim
bad_ref_unknown_repo:
  repository: "totally-unknown-repo-xyz"
  path: "some/path"
bad_ref_no_path:
  repository: openxFactory
bad_ref_backslash_ok:
  repository: openxFactory
  path: "docs\\\\legacy.md"
bad_ref_traversal:
  repository: openxFactory
  path: "../outside.md"
bad_ref_external:
  repository: "installs/agenttower"
  path: "some/file"
  revision: "0123456789012345678901234567890123456789"
""")
    (openx / "ideation/inbox/XFI-2026-001/idea.md").write_text(
        "Idea ID: XFI-2026-001\n")

    # RECORD B1/B2: the SAME idea (and the SAME claim) canonically defined
    # twice — duplicate-idea and corpus-claim-uniqueness.
    record_b = """\
kind: xfactory_idea_routing_record
schema_version: 1
idea_id: XFI-2026-002
scope: unclassified
routing_status: intake
sources:
  - repository: openxFactory
    path: ideation/inbox/XFI-2026-002/idea.md
    revision: pending_capture
transitions:
  - from: null
    to: intake
    occurred_at: "2020-01-01T00:00:00Z"
claims:
  - claim_id: XFI-2026-002-C01
    disposition: unresolved
    blocker: capacity
"""
    (openx / "ideation/inbox/XFI-2026-002/routing.yaml").write_text(record_b)
    (openx / "ideation/inbox/XFI-2026-002/idea.md").write_text(
        "Idea ID: XFI-2026-002\n")
    (openx / "ideation/cross-domain/XFI-2026-004/routing.yaml").write_text(record_b)
    (openx / "ideation/cross-domain/XFI-2026-004/idea.md").write_text(
        "Idea ID: XFI-2026-002\n")

    # RECORD C: routed while an active claim remains unresolved (the
    # routed-record gate), on an otherwise-clean transition chain.
    (openx / "ideation/inbox/XFI-2026-003/routing.yaml").write_text("""\
kind: xfactory_idea_routing_record
schema_version: 1
idea_id: XFI-2026-003
scope: unclassified
routing_status: routed
sources:
  - repository: openxFactory
    path: ideation/inbox/XFI-2026-003/idea.md
    revision: pending_capture
transitions:
  - from: null
    to: intake
    occurred_at: "2026-01-01T00:00:00Z"
  - from: intake
    to: triaging
    occurred_at: "2026-01-02T00:00:00Z"
  - from: triaging
    to: routed
    occurred_at: "2026-01-03T00:00:00Z"
claims:
  - claim_id: XFI-2026-003-C01
    disposition: unresolved
    blocker: still deciding
""")
    (openx / "ideation/inbox/XFI-2026-003/idea.md").write_text(
        "Idea ID: XFI-2026-003\n")

    # RECORD F: no `sources` key at all, and no paired document.
    (openx / "ideation/inbox/XFI-2026-005/routing.yaml").write_text("""\
kind: xfactory_idea_routing_record
schema_version: 1
idea_id: XFI-2026-005
scope: unclassified
routing_status: intake
transitions:
  - from: null
    to: intake
    occurred_at: "2026-01-01T00:00:00Z"
claims: []
""")

    # RECORD G: `claims` is a scalar, not a list; its paired document
    # declares the WRONG Idea ID.
    (openx / "ideation/inbox/XFI-2026-006/routing.yaml").write_text("""\
kind: xfactory_idea_routing_record
schema_version: 1
idea_id: XFI-2026-006
scope: unclassified
routing_status: intake
sources:
  - repository: openxFactory
    path: ideation/inbox/XFI-2026-006/idea.md
    revision: pending_capture
transitions:
  - from: null
    to: intake
    occurred_at: "2026-01-01T00:00:00Z"
claims: oops-not-a-list
""")
    (openx / "ideation/inbox/XFI-2026-006/idea.md").write_text(
        "Idea ID: XFI-2026-999\n")

    # A consolidated Markdown destination: copied-record, two Idea ID
    # headers (both the "too many" and "misleading singular on a
    # destination" findings), unresolved Source Idea IDs / Claim IDs, and
    # both `Routing records:` header defects.
    (openx / "ideation/cross-domain/consolidated/note.md").write_text("""\
# Consolidated

Idea ID: XFI-2026-001
Idea ID: XFI-2026-777
Source Idea IDs: XFI-2026-001, XFI-2026-888
Claim IDs: XFI-2026-001-C01, XFI-2026-777-C99
Routing records: not-valid-json
Routing records: [{"repository": "openxFactory", "path": "x"}]

This consolidated destination also embeds xfactory_idea_routing_record as
prose, which the family reads as a copied record.
""")

    # Aggregation-root ideation backlog.
    (root / "ideation").mkdir(parents=True, exist_ok=True)

    # Proposal provenance: every `ideation_provenance` shape defect.
    (openx / "openspec/changes/change-x/supporting-docs").mkdir(parents=True)
    (openx / "openspec/changes/change-x/supporting-docs/manifest.yaml"
     ).write_text("format_version: 1\nideation_provenance: not-a-list\n")
    (openx / "openspec/changes/change-y/supporting-docs").mkdir(parents=True)
    (openx / "openspec/changes/change-y/supporting-docs/manifest.yaml"
     ).write_text("""\
format_version: 1
ideation_provenance:
  - "not-a-mapping"
  - idea_id: "BAD"
    claim_ids: []
    routing_record:
      revision: pending_capture
  - idea_id: XFI-2026-002
    claim_ids: ["XFF-BOGUS"]
  - idea_id: XFI-2026-999
    claim_ids: ["whatever"]
    routing_record:
      revision: "0123456789012345678901234567890123456789"
""")

    # A second repo with two unparseable routing YAML files.
    gamma = root / "gamma"
    (gamma / "ideation").mkdir(parents=True)
    (gamma / "ideation/routing-index.yaml").write_text("key: [1, 2\n")
    (gamma / "ideation/inbox/broken").mkdir(parents=True)
    (gamma / "ideation/inbox/broken/routing.yaml").write_text("key: [1, 2\n")

    repo_paths = {"openxFactory": openx, "gamma": gamma}
    docs = []
    for name, path in repo_paths.items():
        docs.extend(corpus.load_docs(name, path))
    ctx = Context(
        repo_paths=repo_paths, docs=docs,
        capabilities={n: corpus.spec_capabilities(p)
                      for n, p in repo_paths.items()},
        change_ids={n: corpus.change_ids(p) for n, p in repo_paths.items()},
        git=None, thresholds=dict(DEFAULT_THRESHOLDS), as_of=AS_OF,
        agg_root=root)

    behavioral = set(f.action for f in fam(ctx))
    ctx.routing_strict = True
    behavioral |= set(f.action for f in fam(ctx))
    behavioral = frozenset(behavioral)

    static = harvest_static(ideation_routing)

    EXPECTED_ACTIONS = {
        "restore the routing-record shape or remove the file",
        "declare the canonical routing-record kind",
        "pin schema_version: 1 per the promoted routing-record schema",
        "allocate a central Idea ID matching the promoted grammar",
        "record a controlled routing scope",
        "record a controlled routing status",
        "list every source the routing record derives from",
        "record repository/path/revision for every source",
        "commit the source revision before leaving intake",
        "pin a full committed revision (or pending_capture in intake)",
        "record why the sources are one canonical idea",
        "record claims as a list",
        "resolve or defer every active claim before routing the record",
        "record each transition as a mapping",
        "begin the append-only history at null",
        "keep the transition history contiguous and append-only",
        "use a controlled transition edge",
        "follow the promoted transition graph",
        "end the transition history at the current state",
        "record each claim as a mapping",
        "assign a Claim ID derived from the record's Idea ID",
        "record a controlled claim disposition",
        "name the blocker keeping the claim unresolved, or dispose it",
        "name the proposed owner or return the claim to unresolved",
        "record destination-owner acceptance before routing a claim",
        "record the committed destination reference for the routed claim",
        "record the acceptance actor, time, and evidence",
        "record the append-only transition history",
        "align the Claim ID prefix with the record's Idea ID",
        "define each Claim ID exactly once",
        "point the reference at a resolvable aggregation repository id",
        "record a POSIX repository-relative path",
        "normalize the path separator to POSIX '/'",
        "align the routing directory name with the record's Idea ID",
        "add the paired idea.md or routing-summary.md",
        "make the paired document and routing record agree on the Idea ID",
        "remove the duplicate allocation and rebase",
        "allocate the Idea ID in openxFactory/ideation/routing-index.yaml "
        "in the same change",
        "point the allocation at the committed routing record",
        "keep exactly one canonical routing record per idea",
        "define each Claim ID in exactly one canonical record",
        "progress the routing record or record an explicit deferral",
        "capture ideas in openxFactory or the owning DomainxFactory, never "
        "the aggregation repository",
        "materialize the pinned repository (git submodule update) and "
        "re-run the strict gate",
        "materialize the repository to resolve referenced paths, or run "
        "the strict organize/proposal gate",
        "replace the copied record with Source Idea IDs / Claim IDs / "
        "Routing records pointers",
        "keep a single Idea ID header, or use Source Idea IDs on a "
        "destination",
        "drop the singular Idea ID header on a consolidated destination",
        "create the canonical routing record or remove the Idea ID header",
        "point Source Idea IDs at real canonical routing records",
        "point Claim IDs at claims defined in a canonical routing record",
        "encode Routing records as the canonical compact JSON array",
        "use the canonical committed_reference object shape",
        "record ideation_provenance as a list of entries",
        "record each provenance entry as a mapping",
        "name a valid source Idea ID",
        "pin the proposal to a real canonical routing record",
        "name every selected Claim ID",
        "select only Claim IDs defined in the pinned routing record",
        "record a committed routing-record reference",
        "pin the full committed routing-record revision",
        "repair the routing-index YAML",
        "repair the routing-record YAML",
    }
    assert_actions_pinned(EXPECTED_ACTIONS, behavioral, static,
                          family="ideation-routing")
