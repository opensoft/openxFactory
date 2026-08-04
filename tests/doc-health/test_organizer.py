"""Non-mutating ideation-organizer worker module
(add-cross-factory-ideation-routing; change tasks 5.1-5.5).

Covers the organizer's selection, neutral job envelope,
whole-artifact output validation, catalog-signal eligibility, source/host
authorization, output-policy filtering, immutable evidence persistence, and —
above all — its STRUCTURAL non-mutation guarantees: it cannot move, promote,
delete, route, or approve content, cannot fabricate routing identity from a
catalog tag, and a worker failure can never block or corrupt the deterministic
pass.

All tests are hermetic: a fake worker (a plain callable returning a dict or
raising) stands in for the model, records/inventory are built inline or from
the read-only ``fixtures/ideation-routing/`` corpus, every write lands under a
tmp root, and no test reads wall-clock time (``conftest.AS_OF``)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from conftest import AS_OF, FIXTURES  # noqa: F401 (sys.path side effect)

from doc_health import catalog, organizer
from doc_health.families import FAMILIES

REV = "7fbf65c5250e7a866da552761ed5d02fa457c042"
REV2 = "5142065b2833a2b6d2ccbcb460bf164fd4e1e417"
IDEA = "XFI-2026-001"
SRC_REPO = "xFactories/MedxFactory"
SRC_PATH = "ideation/brainstorm/omni-clinic-hosting.md"


# --- builders -----------------------------------------------------------------

def routing_record(idea_id=IDEA, scope="unclassified", status="intake",
                   source_repo="openxFactory",
                   source_path=None, source_rev="pending_capture",
                   claims=None, transitions=None):
    path = source_path or f"ideation/brainstorm/inbox/{idea_id}/idea.md"
    return {
        "schema_version": 1, "kind": "xfactory_idea_routing_record",
        "idea_id": idea_id, "scope": scope, "routing_status": status,
        "sources": [{"repository": source_repo, "path": path,
                     "revision": source_rev}],
        "claims": claims or [],
        "transitions": transitions or [
            {"from": None, "to": "intake",
             "occurred_at": "2026-07-13T09:00:00Z"}],
    }


def aged_record(idea_id="XFI-2026-002", status="triaging"):
    return routing_record(
        idea_id=idea_id, scope="domain", status=status, source_rev="a" * 40,
        transitions=[
            {"from": None, "to": "intake", "occurred_at": "2026-04-01T00:00:00Z"},
            {"from": "intake", "to": "triaging",
             "occurred_at": "2026-04-02T00:00:00Z"}])


def selection(reason="changed", idea_id=IDEA, repo=SRC_REPO, path=SRC_PATH,
              revision=REV):
    return organizer.Selection(reason, repo, path, revision, idea_id, "x")


def worker_recommendation(cid="candidate-01", repo=SRC_REPO, path=SRC_PATH,
                          section="infrastructure-management",
                          passage="Every Client Hermes needs a liaison.",
                          **overrides):
    rec = {
        "claim_candidate_id": cid,
        "source_ref": {"repository": repo, "path": path,
                       "section": section, "passage": passage},
        "summary": "Every Client Hermes needs an infrastructure liaison.",
        "recommended_scope": "cross_domain",
        "proposed_owner": "openxFactory",
        "proposed_target": "ideation/staging/client-infrastructure-liaison",
        "alternatives": ["OpsxFactory"],
        "domain_local_exclusions": ["Intune execution policy"],
        "dependencies": [],
        "ambiguity": ["Whether the liaison owns retry policy."],
        "rationale": "Reusable client coordination recurs across domains.",
        "confidence": 0.86,
    }
    rec.update(overrides)
    return rec


def enforce(raw, sel=None, sources=None, source_revision=REV, as_of=AS_OF):
    sel = sel or selection()
    sources = sources or {(SRC_REPO, SRC_PATH): REV}
    job = organizer.envelope(as_of, sel, "run-1", organizer.DEFAULT_MODEL, 1)
    return organizer.enforce_contract(
        raw, sel, sources, job, source_revision=source_revision, as_of=as_of)


# --- 5.1: neutral job envelope ------------------------------------------------

def test_envelope_is_neutral_and_read_only():
    job = organizer.envelope(AS_OF, selection(), "run-1", "claude-sonnet-5",
                             1)["job"]
    # Neutral core (neutral-job-envelope capability): job_type is a string
    # owned by the ideation-routing vocabulary; no domain nouns are required;
    # scope is expressed via optional neutral references.
    assert job["job_type"] == "ideation_organizer_review"
    assert job["domain"] is None
    assert {"focal_item_ref", "gate_ref", "artifact_refs"} <= set(job)
    assert "repository" not in job and "feature" not in job
    assert job["worker_selector"]["profile"] == organizer.ORGANIZER_PROFILE
    assert job["auth_profile"] == "read_only_no_credentials"
    # Bounded read-only: zero repository writes.
    assert job["stop_conditions"]["max_repo_writes"] == 0


def test_envelope_id_is_deterministic_never_wall_clock():
    a = organizer.envelope(AS_OF, selection(), "run-1", "m", 1)["job"]["id"]
    b = organizer.envelope(AS_OF, selection(), "run-1", "m", 1)["job"]["id"]
    c = organizer.envelope(AS_OF, selection(), "run-2", "m", 1)["job"]["id"]
    assert a == b and a != c


def test_pre_gate_selection_sets_gate_ref():
    job = organizer.envelope(
        AS_OF, selection(reason="pre_gate"), "r", "m", 1)["job"]
    assert job["gate_ref"] == "organize_or_proposal_gate"
    assert organizer.envelope(
        AS_OF, selection(reason="changed"), "r", "m", 1)["job"]["gate_ref"] \
        is None


# --- 5.5: selection — changed / manual / aging / catalog-signal --------------

def test_changed_input_selection_of_unclassified_and_mixed():
    unclass = routing_record(idea_id="XFI-2026-014", scope="unclassified")
    mixed = routing_record(idea_id="XFI-2026-015", scope="mixed")
    domain = routing_record(idea_id="XFI-2026-016", scope="domain")
    records = [("openxFactory", "p1", unclass), ("openxFactory", "p2", mixed),
               ("openxFactory", "p3", domain)]
    sels = organizer.select(records, None, as_of=AS_OF)
    changed = {s.idea_id for s in sels if s.reason == "changed"}
    # unclassified and mixed qualify; a plain `domain` idea does not.
    assert changed == {"XFI-2026-014", "XFI-2026-015"}


def test_unchanged_idea_is_not_reselected_as_changed():
    rec = routing_record(idea_id="XFI-2026-014", scope="unclassified")
    records = [("openxFactory", "p1", rec)]
    # Same record last run -> no `changed` selection (SC: zero selection on an
    # unchanged idea).
    sels = organizer.select(records, records, as_of=AS_OF)
    assert [s for s in sels if s.reason == "changed"] == []


def test_materially_changed_idea_is_reselected():
    prev = routing_record(idea_id="XFI-2026-014", scope="unclassified")
    curr = routing_record(idea_id="XFI-2026-014", scope="mixed")  # scope moved
    sels = organizer.select([("openxFactory", "p", curr)],
                            [("openxFactory", "p", prev)], as_of=AS_OF)
    assert any(s.reason == "changed" and s.idea_id == "XFI-2026-014"
               for s in sels)


def test_manual_request_selection():
    rec = routing_record(idea_id="XFI-2026-002", scope="domain")
    sels = organizer.select([("openxFactory", "p", rec)], None, as_of=AS_OF,
                            manual_idea_ids={"XFI-2026-002"})
    assert any(s.reason == "manual" and s.idea_id == "XFI-2026-002"
               for s in sels)


def test_manual_beats_aging_for_same_idea():
    rec = aged_record(idea_id="XFI-2026-002")
    sels = organizer.select([("openxFactory", "p", rec)], None, as_of=AS_OF,
                            manual_idea_ids={"XFI-2026-002"})
    reasons = [s.reason for s in sels if s.idea_id == "XFI-2026-002"]
    assert reasons == ["manual"]  # deduped to the highest-priority reason


def test_aging_selection_follows_deterministic_threshold():
    rec = aged_record()  # triaging, latest transition ~ 3 months before AS_OF
    sels = organizer.select([("openxFactory", "p", rec)], None, as_of=AS_OF)
    assert any(s.reason == "aging" for s in sels)


def test_routed_record_does_not_age():
    rec = routing_record(idea_id="XFI-2026-002", scope="cross_domain",
                         status="routed", source_rev="a" * 40,
                         transitions=[
                             {"from": None, "to": "intake",
                              "occurred_at": "2026-01-01T00:00:00Z"},
                             {"from": "intake", "to": "routed",
                              "occurred_at": "2026-01-02T00:00:00Z"}])
    sels = organizer.select([("openxFactory", "p", rec)], None, as_of=AS_OF)
    assert [s for s in sels if s.reason == "aging"] == []


def test_pre_gate_selection():
    rec = routing_record(idea_id="XFI-2026-003", scope="cross_domain",
                         status="triaging", source_rev="a" * 40)
    sels = organizer.select([("openxFactory", "p", rec)], None, as_of=AS_OF,
                            pre_gate_idea_ids={"XFI-2026-003"})
    assert any(s.reason == "pre_gate" for s in sels)


def test_cross_domain_link_selection_has_no_idea_id():
    sels = organizer.select([], None, as_of=AS_OF,
                            cross_domain_links=[("xFactories/MedxFactory",
                                                 "ideation/brainstorm/x.md")])
    link = [s for s in sels if s.reason == "cross_domain_link"]
    assert len(link) == 1 and link[0].idea_id is None
    # A cross-domain link on an unrouted brainstorm is enqueue-only.
    assert organizer.dispatchable(sels) == []


def test_optional_catalog_signal_selection():
    sig = organizer.CatalogSignal("openxFactory", "docs/x.md", "h1",
                                  domain_contexts=("MedxFactory", "OpsxFactory"))
    sels = organizer.select([], None, as_of=AS_OF, catalog_signals=[sig])
    cat = [s for s in sels if s.reason == "catalog_signal"]
    assert len(cat) == 1 and cat[0].repository == "openxFactory"


def test_catalog_signal_attributed_to_existing_idea_when_a_source():
    rec = routing_record(idea_id="XFI-2026-014", scope="unclassified",
                         source_repo="openxFactory", source_path="docs/x.md")
    sig = organizer.CatalogSignal("openxFactory", "docs/x.md", "h1")
    sels = organizer.select([("openxFactory", "p", rec)], records_prev(rec),
                            as_of=AS_OF, catalog_signals=[sig])
    # The signal targets a document that is a source of XFI-2026-014, so the
    # (evidence-only) review is attributed to that idea — still without
    # creating any routing state.
    cat = [s for s in sels if s.reason == "catalog_signal"]
    assert len(cat) == 1 and cat[0].idea_id == "XFI-2026-014"


def records_prev(rec):
    """Same record as previous-run state (so it is not also `changed`)."""
    return [("openxFactory", "p", rec)]


# --- 5.3: catalog-signal eligibility (currentness + policy-blocked) ----------

def snapshot(entries, digest="d1", snapshot_id="snap1", repo="openxFactory"):
    return {"repos": {repo: {"run": {"inventory_snapshot_id": snapshot_id},
                             "taxonomy": {"digest": digest},
                             "entries": entries}}}


def live_entry(path="docs/x.md", content_hash="h1", snapshot_id="snap1",
               repo="openxFactory"):
    return {"repo": repo, "path": path, "content_hash": content_hash,
            "snapshot_id": snapshot_id}


def catalog_entry(path="docs/x.md", content_hash="h1", snapshot_id="snap1",
                  repo="openxFactory", domain_contexts=("MedxFactory",),
                  **extra):
    entry = {"repo": repo, "path": path, "content_hash": content_hash,
             "snapshot_id": snapshot_id,
             "facet_assignments": [{"facet": "domain_contexts",
                                    "values": list(domain_contexts),
                                    "state": "suggested"}]}
    entry.update(extra)
    return entry


def test_current_catalog_entry_is_eligible():
    sigs = organizer.eligible_catalog_signals(
        snapshot([catalog_entry()]), [live_entry()], "d1")
    assert len(sigs) == 1
    assert sigs[0].domain_contexts == ("MedxFactory",)


def test_stale_signal_rejected_on_content_hash_mismatch():
    # Live document changed after the catalog entry was recorded.
    assert organizer.eligible_catalog_signals(
        snapshot([catalog_entry(content_hash="old")]),
        [live_entry(content_hash="new")], "d1") == []


def test_stale_signal_rejected_on_snapshot_id_mismatch():
    assert organizer.eligible_catalog_signals(
        snapshot([catalog_entry(snapshot_id="snapOLD")], snapshot_id="snapOLD"),
        [live_entry(snapshot_id="snapNEW")], "d1") == []


def test_stale_signal_rejected_on_taxonomy_digest_mismatch():
    assert organizer.eligible_catalog_signals(
        snapshot([catalog_entry()], digest="OLD"),
        [live_entry()], "CURRENT") == []


def test_policy_blocked_entry_dispatch_decision_excluded():
    entry = catalog_entry(dispatch_policy={"state": "blocked"})
    assert organizer.eligible_catalog_signals(
        snapshot([entry]), [live_entry()], "d1") == []


def test_policy_blocked_facet_excluded():
    entry = catalog_entry()
    entry["facet_assignments"].append(
        {"facet": "topic_tags", "values": [], "state": "policy_blocked"})
    assert organizer.eligible_catalog_signals(
        snapshot([entry]), [live_entry()], "d1") == []


def test_opaque_entry_needs_authorized_resolver():
    loc = catalog.opaque_locator("openxFactory", "docs/secret.md")
    entry = {"repo": "openxFactory", "content_hash": "h2",
             "snapshot_id": "snap1", **loc,
             "facet_assignments": [{"facet": "domain_contexts",
                                    "values": ["MedxFactory"],
                                    "state": "suggested"}]}
    live = [live_entry(path="docs/secret.md", content_hash="h2")]
    snap = snapshot([entry])
    # No resolver: an opaque entry cannot be matched (defense in depth).
    assert organizer.eligible_catalog_signals(snap, live, "d1") == []
    # Authorized resolver whose path re-derives the recorded locator: admitted.
    sigs = organizer.eligible_catalog_signals(
        snap, live, "d1",
        resolver=lambda e: ("openxFactory", "docs/secret.md"))
    assert len(sigs) == 1 and sigs[0].path == "docs/secret.md"


def test_opaque_resolver_disagreeing_locator_is_rejected():
    loc = catalog.opaque_locator("openxFactory", "docs/secret.md")
    entry = {"repo": "openxFactory", "content_hash": "h2",
             "snapshot_id": "snap1", **loc, "facet_assignments": []}
    live = [live_entry(path="docs/other.md", content_hash="h2")]
    # Resolver names a path that does NOT re-derive the recorded opaque
    # locator -> rejected (never a guess).
    assert organizer.eligible_catalog_signals(
        snapshot([entry]), live, "d1",
        resolver=lambda e: ("openxFactory", "docs/other.md")) == []


# --- 5.3: PROVE a tag cannot create routing authority or lifecycle state -----

def test_catalog_signal_never_allocates_idea_id_or_routing_record():
    # An eligible signal on an ordinary document with NO routing record yields
    # only an enqueue-only selection: no Idea ID is fabricated, and the
    # selection is not dispatchable (spec "Current mixed-context tag is
    # observed": MUST NOT allocate an Idea ID or create a routing record).
    sig = organizer.CatalogSignal("openxFactory", "docs/x.md", "h1",
                                  domain_contexts=("MedxFactory", "OpsxFactory"))
    sels = organizer.select([], None, as_of=AS_OF, catalog_signals=[sig])
    cat = [s for s in sels if s.reason == "catalog_signal"]
    assert cat and all(s.idea_id is None for s in cat)
    assert organizer.dispatchable(sels) == []


def test_catalog_signal_carries_no_authority_fields():
    # The signal is inert evidence: it carries a document identity and the
    # observed tags, never an owner, destination, disposition, or Idea ID.
    sig = organizer.CatalogSignal("openxFactory", "docs/x.md", "h1",
                                  domain_contexts=("MedxFactory",))
    assert not hasattr(sig, "proposed_owner")
    assert not hasattr(sig, "disposition")
    assert not hasattr(sig, "idea_id")


# --- 5.2 / 5.1: output validation and stable evidence ------------------------

def test_valid_output_produces_pending_review_record():
    doc, rejects = enforce({"recommendations": [worker_recommendation()]})
    assert rejects == []
    assert doc["kind"] == organizer.RECOMMENDATION_KIND
    assert doc["status"] == "record"
    assert doc["idea_id"] == IDEA
    assert doc["source_revision"] == REV
    rec = doc["recommendations"][0]
    assert rec["disposition"] == "pending_review"
    # Every required evidence field is present (task 5.2).
    for name in ("claim_candidate_id", "source_ref", "rationale",
                 "confidence", "alternatives", "domain_local_exclusions",
                 "ambiguity"):
        assert name in rec
    sref = rec["source_ref"]
    assert set(sref) == {"repository", "path", "revision", "section",
                         "passage_sha256"}
    assert sref["revision"] == REV  # orchestration-supplied, not worker


def test_evidence_is_stable_and_raw_passage_dropped():
    raw = {"recommendations": [worker_recommendation(
        passage="  Every   Client\tHermes\nneeds a liaison.  ")]}
    a, _ = enforce(raw)
    b, _ = enforce(raw)
    # Deterministic digest over whitespace-normalized passage; identical runs
    # render byte-identically.
    assert a == b
    sref = a["recommendations"][0]["source_ref"]
    assert len(sref["passage_sha256"]) == 64
    # The raw passage text is NEVER persisted (only its digest).
    assert "passage" not in sref
    import hashlib
    expected = hashlib.sha256(
        "Every Client Hermes needs a liaison.".encode()).hexdigest()
    assert sref["passage_sha256"] == expected


def test_generated_at_is_derived_from_as_of_not_wall_clock():
    doc, _ = enforce({"recommendations": [worker_recommendation()]})
    assert doc["generated_at"] == f"{AS_OF.isoformat()}T00:00:00Z"


# --- 5.5: output rejection (whole-artifact) ----------------------------------

def test_output_rejected_when_not_an_object_with_recommendations():
    doc, rejects = enforce({"nope": []})
    assert doc is None and rejects


def test_empty_recommendations_rejected():
    doc, rejects = enforce({"recommendations": []})
    assert doc is None and "empty recommendations" in rejects[0]


def test_missing_passage_rejects_whole_artifact():
    raw = {"recommendations": [
        worker_recommendation(cid="candidate-01"),
        worker_recommendation(cid="candidate-02",
                              source_ref={"repository": SRC_REPO,
                                          "path": SRC_PATH,
                                          "section": "s"})]}  # no passage
    doc, rejects = enforce(raw)
    # Whole-artifact rejection: the valid candidate-01 is NOT rescued.
    assert doc is None and any("grounding passage" in r for r in rejects)


def test_non_numeric_confidence_rejected():
    doc, rejects = enforce(
        {"recommendations": [worker_recommendation(confidence="high")]})
    assert doc is None and any("confidence" in r for r in rejects)


def test_confidence_out_of_range_rejected():
    doc, rejects = enforce(
        {"recommendations": [worker_recommendation(confidence=1.5)]})
    assert doc is None and any("confidence" in r for r in rejects)


def test_boolean_confidence_rejected():
    doc, rejects = enforce(
        {"recommendations": [worker_recommendation(confidence=True)]})
    assert doc is None and any("confidence" in r for r in rejects)


def test_invented_source_rejected():
    doc, rejects = enforce({"recommendations": [worker_recommendation(
        repo="openxFactory", path="ideation/brainstorm/not-a-source.md")]})
    assert doc is None and any("not a committed source" in r for r in rejects)


def test_required_arrays_must_be_present():
    rec = worker_recommendation()
    del rec["ambiguity"]
    doc, rejects = enforce({"recommendations": [rec]})
    assert doc is None and any("ambiguity" in r for r in rejects)


def test_bad_recommended_scope_rejected():
    doc, rejects = enforce(
        {"recommendations": [worker_recommendation(recommended_scope="bogus")]})
    assert doc is None and any("recommended_scope" in r for r in rejects)


def test_duplicate_claim_candidate_id_rejected():
    raw = {"recommendations": [worker_recommendation(cid="dup"),
                               worker_recommendation(cid="dup")]}
    doc, rejects = enforce(raw)
    assert doc is None and any("duplicate" in r for r in rejects)


def test_non_committed_source_revision_rejected():
    doc, rejects = enforce({"recommendations": [worker_recommendation()]},
                           source_revision="pending_capture")
    assert doc is None and any("committed revision" in r for r in rejects)


def test_selection_without_idea_id_rejected_by_validator():
    sel = organizer.Selection("catalog_signal", "openxFactory", "docs/x.md",
                              None, None, "signal")
    doc, rejects = enforce({"recommendations": [worker_recommendation(
        repo="openxFactory", path="docs/x.md")]}, sel=sel,
        sources={("openxFactory", "docs/x.md"): REV})
    assert doc is None and any("Idea ID" in r for r in rejects)


# --- 5.1: STRUCTURAL non-mutation --------------------------------------------

def test_mutation_directive_top_level_key_rejected():
    doc, rejects = enforce({"recommendations": [worker_recommendation()],
                            "execute": True})
    assert doc is None and any("mutation directive" in r for r in rejects)


def test_mutation_directive_recommendation_key_rejected():
    doc, rejects = enforce(
        {"recommendations": [worker_recommendation(apply_move="openxFactory")]})
    assert doc is None and any("mutation directive" in r for r in rejects)


def test_mutation_directive_source_ref_key_rejected():
    rec = worker_recommendation()
    rec["source_ref"]["promote"] = True
    doc, rejects = enforce({"recommendations": [rec]})
    assert doc is None and any("outside the vocabulary" in r for r in rejects)


def test_verdict_disposition_rejected():
    # 5.5 "authorized disposition": the organizer cannot self-authorize a
    # verdict; only pending_review may ever be emitted.
    for verdict in ("accepted", "routed", "approved", "reviewed"):
        doc, rejects = enforce(
            {"recommendations": [worker_recommendation(disposition=verdict)]})
        assert doc is None and any("cannot emit a verdict" in r
                                   for r in rejects)


def test_worker_supplied_revision_is_ignored_not_trusted():
    rec = worker_recommendation()
    rec["source_ref"]["revision"] = "d" * 40  # worker tries to pin a revision
    doc, rejects = enforce({"recommendations": [rec]})
    assert rejects == []
    # Orchestration's committed revision wins, never the worker's echo.
    assert doc["recommendations"][0]["source_ref"]["revision"] == REV


def test_module_exposes_no_mutation_api():
    # Structural: the organizer module has no move/promote/approve/route/
    # allocate entry point at all.
    for banned in ("move", "promote", "delete", "supersede", "approve",
                   "route", "allocate_idea_id", "write_routing_record",
                   "accept"):
        assert not hasattr(organizer, banned)


# --- 5.4: source/host authorization (fail closed) ----------------------------

HOST = {"tenant_boundary": "t1", "data_boundary": "db1",
        "handling_classes": ["standard"]}


def test_authorized_full_dispatch():
    auth = organizer.authorize_dispatch(
        {"tenant_boundary": "t1", "data_boundary": "db1",
         "handling": "standard"}, HOST)
    assert auth.authorized and auth.mode == "full"


def test_handling_not_authorized_fails_closed():
    auth = organizer.authorize_dispatch(
        {"tenant_boundary": "t1", "data_boundary": "db1",
         "handling": "protected"}, HOST)
    assert not auth.authorized and auth.mode == "denied"
    assert auth.reason == "handling_not_authorized"


def test_tenant_boundary_mismatch_fails_closed():
    auth = organizer.authorize_dispatch(
        {"tenant_boundary": "tX", "data_boundary": "db1",
         "handling": "standard"}, HOST)
    assert not auth.authorized and auth.reason == "tenant_boundary_mismatch"


def test_data_boundary_mismatch_fails_closed():
    auth = organizer.authorize_dispatch(
        {"tenant_boundary": "t1", "data_boundary": "dbX",
         "handling": "standard"}, HOST)
    assert not auth.authorized and auth.reason == "data_boundary_mismatch"


def test_redaction_only_when_source_explicitly_permits():
    protected = {"tenant_boundary": "t1", "data_boundary": "db1",
                 "handling": "protected"}
    # Not permitted -> denied (never assume redaction makes dispatch ok).
    assert organizer.authorize_dispatch(protected, HOST).mode == "denied"
    # Explicitly permitted -> redacted.
    auth = organizer.authorize_dispatch(
        {**protected, "redaction_permitted": True}, HOST)
    assert auth.authorized and auth.mode == "redacted"


def test_missing_attestation_fails_closed():
    assert organizer.authorize_dispatch({}, HOST).mode == "denied"
    assert organizer.authorize_dispatch(
        {"tenant_boundary": "t1", "data_boundary": "db1",
         "handling": "standard"}, {}).mode == "denied"


# --- 5.4: output-policy filtering (protected-metadata suppression) -----------

def two_recommendation_doc():
    raw = {"recommendations": [
        worker_recommendation(cid="candidate-01"),
        worker_recommendation(cid="candidate-02", section="clinical",
                              passage="Protected clinical hosting detail.",
                              summary="SECRET clinical summary")]}
    doc, rejects = enforce(raw)
    assert rejects == []
    return doc


def test_protected_metadata_suppression_blanks_optional_fields():
    doc = two_recommendation_doc()
    policies = {(SRC_REPO, SRC_PATH): {"suppress": {"summary", "proposed_owner",
                                                    "domain_local_exclusions"}}}
    filtered, dropped, suppressed = organizer.filter_recommendations(
        doc, policies)
    assert dropped == []
    for rec in filtered["recommendations"]:
        assert rec["summary"] is None
        assert rec["proposed_owner"] is None
        assert rec["domain_local_exclusions"] == []
    assert ("candidate-01", "summary") in suppressed


def test_protected_path_drops_whole_recommendation():
    # A different source for candidate-02 so only it is path-protected.
    raw = {"recommendations": [
        worker_recommendation(cid="candidate-01"),
        worker_recommendation(cid="candidate-02", repo="openxFactory",
                              path="ideation/brainstorm/inbox/XFI/idea.md",
                              passage="p")]}
    sources = {(SRC_REPO, SRC_PATH): REV,
               ("openxFactory", "ideation/brainstorm/inbox/XFI/idea.md"): REV2}
    doc, rejects = enforce(raw, sources=sources)
    assert rejects == []
    policies = {("openxFactory", "ideation/brainstorm/inbox/XFI/idea.md"):
                {"path_protected": True}}
    filtered, dropped, _ = organizer.filter_recommendations(doc, policies)
    assert dropped == ["candidate-02"]
    assert [r["claim_candidate_id"] for r in filtered["recommendations"]] == \
        ["candidate-01"]


def test_filter_never_mutates_input_document():
    doc = two_recommendation_doc()
    before = catalog.render(doc)
    organizer.filter_recommendations(
        doc, {(SRC_REPO, SRC_PATH): {"suppress": {"summary"}}})
    assert catalog.render(doc) == before  # deep-copied; input untouched


def test_no_policy_is_identity_filter():
    doc = two_recommendation_doc()
    filtered, dropped, suppressed = organizer.filter_recommendations(doc, None)
    assert dropped == [] and suppressed == []
    assert filtered == doc


# --- 5.4: immutable evidence persistence -------------------------------------

def persistable_doc():
    doc, rejects = enforce({"recommendations": [worker_recommendation()]})
    assert rejects == []
    return doc


def test_persist_writes_only_under_evidence_boundary(tmp_path):
    path = organizer.persist_recommendations(
        tmp_path, AS_OF, IDEA, "run-1", persistable_doc())
    rel = path.relative_to(tmp_path).as_posix()
    assert rel == f"health/ideation-organizer/{AS_OF.isoformat()}/{IDEA}-run-1.yaml"
    assert path.is_file()


def test_persist_is_idempotent_for_identical_content(tmp_path):
    doc = persistable_doc()
    a = organizer.persist_recommendations(tmp_path, AS_OF, IDEA, "run-1", doc)
    b = organizer.persist_recommendations(tmp_path, AS_OF, IDEA, "run-1", doc)
    assert a == b


def test_persist_refuses_conflicting_write(tmp_path):
    doc = persistable_doc()
    organizer.persist_recommendations(tmp_path, AS_OF, IDEA, "run-1", doc)
    conflicting = dict(doc, source_revision="e" * 40)
    with pytest.raises(catalog.CatalogError):
        organizer.persist_recommendations(
            tmp_path, AS_OF, IDEA, "run-1", conflicting)


def test_persist_rejects_path_escaping_run_id(tmp_path):
    doc = persistable_doc()
    for bad in ("a/b", "..", ".hidden", "a\\b"):
        with pytest.raises(ValueError):
            organizer.persist_recommendations(tmp_path, AS_OF, IDEA, bad, doc)


def test_persist_rejects_invalid_idea_id(tmp_path):
    with pytest.raises(ValueError):
        organizer.persist_recommendations(
            tmp_path, AS_OF, "not-an-idea-id", "run-1", persistable_doc())


def test_persist_requires_record_status_and_kind(tmp_path):
    doc = persistable_doc()
    with pytest.raises(ValueError):
        organizer.persist_recommendations(
            tmp_path, AS_OF, IDEA, "run-1", dict(doc, status="draft"))
    with pytest.raises(ValueError):
        organizer.persist_recommendations(
            tmp_path, AS_OF, IDEA, "run-1", dict(doc, kind="something_else"))


# --- 5.5: bounded orchestration and failure isolation ------------------------

def sources_for(sel):
    return {(sel.repository, sel.path): {"revision": sel.revision,
                                         "content": "idea content"}}


def test_run_organizer_success_returns_document_and_meta():
    sel = selection()

    def invoke(prompt, model):
        return {"recommendations": [worker_recommendation()]}

    doc, meta = organizer.run_organizer(
        sel, sources_for(sel), as_of=AS_OF, run_id="run-1",
        source_revision=REV, invoke=invoke)
    assert doc is not None and meta.skipped_reason is None
    assert meta.recommendation_count == 1
    assert meta.idea_id == IDEA and meta.selection_reason == "changed"


def test_worker_exception_is_isolated_as_skip():
    sel = selection()

    def boom(prompt, model):
        raise RuntimeError("worker offline")

    doc, meta = organizer.run_organizer(
        sel, sources_for(sel), as_of=AS_OF, run_id="run-1",
        source_revision=REV, invoke=boom)
    # Never raises; records a skip; produces no recommendation.
    assert doc is None
    assert meta.skipped_reason and "worker offline" in meta.skipped_reason
    assert meta.recommendation_count == 0


def test_invalid_worker_output_is_isolated_as_skip():
    sel = selection()

    def bad(prompt, model):
        return {"recommendations": [worker_recommendation(confidence="high")]}

    doc, meta = organizer.run_organizer(
        sel, sources_for(sel), as_of=AS_OF, run_id="run-1",
        source_revision=REV, invoke=bad)
    assert doc is None and meta.rejects
    assert "rejected" in meta.skipped_reason


def test_run_organizer_never_writes_to_disk(tmp_path):
    # run_organizer is analysis-only; persistence is a separate explicit call.
    sel = selection()

    def invoke(prompt, model):
        return {"recommendations": [worker_recommendation()]}

    organizer.run_organizer(sel, sources_for(sel), as_of=AS_OF, run_id="run-1",
                            source_revision=REV, invoke=invoke)
    assert list(tmp_path.iterdir()) == []  # nothing written anywhere


def test_run_organizer_refuses_non_dispatchable_selection():
    sel = organizer.Selection("catalog_signal", "openxFactory", "docs/x.md",
                              None, None, "signal")
    with pytest.raises(ValueError):
        organizer.run_organizer(sel, {}, as_of=AS_OF, run_id="run-1",
                                source_revision=REV)


def test_organizer_failure_cannot_corrupt_deterministic_pass(tmp_path):
    # Concretely: the fourteenth deterministic family's findings over the
    # read-only routing fixture are identical before and after an organizer
    # worker failure, and the organizer writes nothing into the corpus
    # (organizer-and-sweep-contract "semantic failure does not suppress
    # deterministic health results").
    from test_ideation_routing import ctx_over, BASE
    fam = FAMILIES["ideation-routing"]
    before = sorted(f.rule for f in fam(ctx_over(BASE)))

    sel = selection(idea_id="XFI-2026-014", repo="openxFactory",
                    path="ideation/brainstorm/inbox/XFI-2026-014/idea.md")

    def boom(prompt, model):
        raise RuntimeError("organizer host offline")

    doc, meta = organizer.run_organizer(
        sel, sources_for(sel), as_of=AS_OF, run_id="run-1",
        source_revision=REV, invoke=boom)
    after = sorted(f.rule for f in fam(ctx_over(BASE)))
    assert doc is None and meta.skipped_reason
    assert before == after  # deterministic pass is unchanged
    # No organizer evidence dir was created anywhere in the fixture.
    assert not (BASE / "health" / "ideation-organizer").exists()


# --- prompt contract ----------------------------------------------------------

def test_prompt_contract_version_loads():
    version, text = organizer.load_prompt_contract()
    assert version == 1
    assert "Prompt-Contract-Version" in text
    assert "pending_review" in text  # the prompt fixes the disposition
