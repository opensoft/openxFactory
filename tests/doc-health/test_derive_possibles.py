"""Derive-possibles worker (add-possibles-derivation-lane; change tasks
3.1-3.5; specs/004-derive-possibles).

Hermetic: a fake worker (a plain callable returning a dict or raising) stands
in for the model — NO test calls a real model — clusters/docs are built
inline or from the real openxFactory checkout read-only, every write lands
under a tmp root, and no test reads wall-clock time (``conftest.AS_OF``).
"""

from __future__ import annotations

import hashlib
import json
import os

import pytest

from pathlib import Path

from conftest import AS_OF, REPO_ROOT  # noqa: F401 (sys.path side effect)

from doc_health import corpus
from doc_health import derive_possibles as dp
from doc_health import ideation_readiness as ir


REV = "a7aac777bedfb83dbb957819a7753436bdabd334"

# harden-ideation-readiness-check. Spelled identically in
# `test_ideation_readiness.py` (which carries the full rationale) and in
# `test_readiness_dispatch.py`. The duplication is deliberate and tracked: the
# packet's Q3 / tasks § 5.1 — whether the three collapse into one shared
# fixture — is OPEN and is not decided by this realization. Edit one, edit all
# three.
ROOT_FALLBACK_MARKER = "[openxfactory-root] fallback"
INDEX_REL = Path("ideation") / "cross-reference.yaml"
SIBLING_INDEX_REL = Path("openxFactory") / INDEX_REL


def _openxfactory_root(under_test=None, *, fallback=None, announce=print):
    """Resolve the openxFactory checkout this run is a proof ABOUT: the
    REPOSITORY UNDER TEST first, then an explicit `fallback`, then
    `OPENXFACTORY_ROOT`, then the ancestor walk to a sibling `openxFactory/` —
    every rung past the first announcing which checkout it resolved and why.
    None when nothing is reachable."""
    base = Path(under_test or REPO_ROOT).resolve()
    if (base / INDEX_REL).is_file():
        return base

    why = f"the repository under test ({base}) carries no {INDEX_REL.as_posix()}"
    if fallback is not None and (Path(fallback) / INDEX_REL).is_file():
        resolved = Path(fallback).resolve()
        announce(f"{ROOT_FALLBACK_MARKER}: resolved {resolved} from the "
                 f"explicit argument because {why}")
        return resolved

    declared = os.environ.get("OPENXFACTORY_ROOT")
    if declared and (Path(declared) / INDEX_REL).is_file():
        resolved = Path(declared).resolve()
        announce(f"{ROOT_FALLBACK_MARKER}: resolved {resolved} from "
                 f"OPENXFACTORY_ROOT because {why}")
        return resolved

    for d in [base, *base.parents]:
        if (d / SIBLING_INDEX_REL).is_file():
            resolved = d / "openxFactory"
            announce(f"{ROOT_FALLBACK_MARKER}: resolved {resolved} by walking "
                     f"up from the repository under test because {why}")
            return resolved
    return None


def _openxfactory_root_or_skip(under_test=None):
    """The resolved checkout, or a skip whose reason names what was searched."""
    root = _openxfactory_root(under_test)
    if root is None:
        base = Path(under_test or REPO_ROOT).resolve()
        pytest.skip(f"proof NOT PERFORMED: no openxFactory checkout serves it "
                    f"— the repository under test ({base}) carries no "
                    f"{INDEX_REL.as_posix()}, OPENXFACTORY_ROOT names no "
                    f"checkout that does, and no ancestor of it holds "
                    f"{SIBLING_INDEX_REL.as_posix()}")
    return root


# --- builders ------------------------------------------------------------

def doc(path, *, status="staged", repo="openxFactory"):
    """A corpus.Doc whose body carries a stable, quotable passage."""
    text = (f"# {path.rsplit('/', 1)[-1]}\n\nStatus: {status}\n\n## Body\n\n"
            f"Body prose for {path} describing the recurring subject in "
            "enough depth to ground a derivation passage.\n")
    return corpus.Doc(repo, path, text, status, None)


def cluster(cid="cl-alpha", paths=("ideation/brainstorm/alpha-1.md",
                                   "ideation/brainstorm/alpha-2.md")):
    return {"id": cid, "name": cid, "topics": ["alpha"],
            "members": [{"path": p, "stage": "staged"} for p in paths]}


def index_with(clusters=None, register=None):
    idx = {"schema_version": 1, "kind": "ideation-cross-reference",
           "repository": "openxFactory",
           "generation": {"source_revision": REV,
                          "generator_version": "test"},
           "topic_entries": clusters if clusters is not None else [cluster()]}
    if register is not None:
        idx["possibles_register"] = register
    return idx


def docs_for(*clusters_):
    return [doc(m["path"]) for c in clusters_ for m in c["members"]]


def candidate(i=0, *, passage=None, path="ideation/brainstorm/alpha-1.md",
              **extra):
    out = {"title": f"Alpha surface {i}",
           "claim": f"The alpha cluster could become surface {i}.",
           "rationale": "the members converge on this",
           "path": path, "section": "Body",
           "passage": passage if passage is not None else
           ("Body prose for ideation/brainstorm/alpha-1.md describing the "
            "recurring subject in enough depth to ground a derivation "
            "passage.")}
    out.update(extra)
    return out


def fake_invoke(output):
    """A model stand-in returning ``output`` (dict, JSON string, or raising
    when given an exception). Never calls a real model."""
    def invoke(prompt, model):
        if isinstance(output, Exception):
            raise output
        return output
    return invoke


def payload_mock_invoke(n=1, **cand_extra):
    """A model stand-in that quotes a REAL passage parsed out of the
    untrusted payload's embedded documents, so evidence hashes a genuine
    section (mirrors the readiness suite's realistic mock)."""
    def invoke(prompt, model):
        payload = json.loads(
            prompt.rsplit("```json\n", 1)[1].split("\n```", 1)[0])
        cands = []
        for i in range(n):
            d = payload["documents"][i % len(payload["documents"])]
            passage = next(
                (s.strip() for s in d["content"].splitlines()
                 if s.strip() and not s.strip().startswith("#")
                 and not s.strip().endswith(":") and len(s.strip()) > 20),
                "the recurring subject")
            cand = {"title": f"{payload['cluster_id']} candidate {i}",
                    "claim": f"Cluster {payload['cluster_id']} could become "
                             f"capability {i}.",
                    "rationale": f"members of {payload['cluster_id']} "
                                 "converge here",
                    "path": d["path"], "section": "Body", "passage": passage}
            cand.update(cand_extra)
            cands.append(cand)
        return {"candidates": cands}
    return invoke


def run(index=None, docs=None, *, invoke, run_id="run-1", **kw):
    index = index if index is not None else index_with()
    docs = docs if docs is not None else docs_for(*index["topic_entries"])
    return dp.run_derivation(index, docs, source_revision=REV, as_of=AS_OF,
                             run_id=run_id, invoke=invoke, **kw)


# =========================================================================
# T001/T002 — change 3.1: versioned prompt + bounded single-shot invocation
# =========================================================================

def test_prompt_contract_version_parses():
    version, text = dp.load_prompt_contract()
    assert version >= 1
    assert "derive-possibles" in text
    assert dp.prompt_contract_string(version) == \
        f"derive-possibles-prompt-v{version}"


def test_worker_output_schema_forces_candidates():
    assert dp.WORKER_OUTPUT_SCHEMA["required"] == ["candidates"]


def test_envelope_is_deterministic_and_read_only():
    a = dp.envelope(AS_OF, "cl-alpha", "run-1", "m", 1)
    b = dp.envelope(AS_OF, "cl-alpha", "run-1", "m", 1)
    c = dp.envelope(AS_OF, "cl-beta", "run-1", "m", 1)
    assert a == b  # deterministic over the seed, never the wall clock
    assert a["job"]["id"] != c["job"]["id"]
    assert a["job"]["id"].startswith("DPOSS-")
    assert a["job"]["stop_conditions"]["max_repo_writes"] == 0
    assert a["job"]["auth_profile"] == "read_only_no_credentials"
    assert a["job"]["worker_selector"]["profile"] == "derive-possibles"


def test_build_analysis_input_embeds_members_and_register_context():
    cl = cluster()
    sources = {m["path"]: {"repository": "openxFactory", "content": "words"}
               for m in cl["members"]}
    existing = [{"title": "Old", "claim": "Old claim", "state": "rejected",
                 "origin": "ai-derived"}]
    text = dp.build_analysis_input("PROMPT", cl, sources, existing)
    assert text.startswith("PROMPT")
    assert "data" in text  # untrusted framing
    payload = json.loads(text.rsplit("```json\n", 1)[1].split("\n```", 1)[0])
    assert payload["cluster_id"] == "cl-alpha"
    assert payload["existing_possibles"] == [
        {"title": "Old", "claim": "Old claim", "state": "rejected"}]
    assert {d["path"] for d in payload["documents"]} == set(sources)
    assert payload["members"][0]["stage"] == "staged"


def test_parse_worker_output_accepts_dict_string_and_structured():
    out = {"candidates": []}
    assert dp.parse_worker_output(out) == out
    assert dp.parse_worker_output(json.dumps(out)) == out
    assert dp.parse_worker_output(
        {"structured_output": out}) == out
    with pytest.raises(ValueError):
        dp.parse_worker_output({"tiers": []})


# =========================================================================
# T004 — change 3.2: orchestration-stamped identity on every proposal
# =========================================================================

def test_derived_entry_carries_the_full_contract_shape():
    proposals, meta = run(invoke=fake_invoke({"candidates": [candidate()]}))
    assert meta.proposed == 1 and not meta.skipped_clusters
    entry = proposals[0]
    assert entry["origin"] == "ai-derived"
    assert entry["state"] == "latent"
    assert entry["id"].startswith("pos-derived-")
    wr = entry["derivation"]["worker_run"]
    assert wr["correlation_id"].startswith("DPOSS-")
    assert wr["worker_profile"] == "derive-possibles"
    assert wr["prompt_contract_version"] == "derive-possibles-prompt-v1"
    assert entry["derivation"]["disposition"] == "pending_review"
    assert entry["claiming_clusters"] == ["cl-alpha"]
    pin = entry["supporting_evidence"][0]
    assert pin["document"] == "ideation/brainstorm/alpha-1.md"
    expected = hashlib.sha256(
        " ".join(candidate()["passage"].split()).encode()).hexdigest()
    assert pin["passage_sha256"] == expected  # orchestration-computed
    assert entry["provenance"] == {
        "document": "ideation/brainstorm/alpha-1.md",
        "section": "derived-from cluster cl-alpha"}


def test_worker_supplied_identity_is_discarded():
    proposals, _ = run(invoke=fake_invoke(
        {"candidates": [candidate(id="worker-chose-this",
                                  correlation_id="worker-corr",
                                  count=7)]}))
    entry = proposals[0]
    assert entry["id"].startswith("pos-derived-")  # minted, never the worker's
    assert entry["derivation"]["worker_run"]["correlation_id"] != "worker-corr"
    assert "count" not in entry


def test_disagreeing_precision_value_voids_the_proposal():
    good_hash = hashlib.sha256(
        " ".join(candidate()["passage"].split()).encode()).hexdigest()
    proposals, meta = run(invoke=fake_invoke(
        {"candidates": [candidate(0, passage_sha256="deadbeef" * 8),
                        candidate(1, passage_sha256=good_hash)]}))
    # the mis-copied hash voids ONLY the affected proposal; the agreeing one
    # survives (the spec's "void the affected proposals")
    assert [p["title"] for p in proposals] == ["Alpha surface 1"]
    assert meta.voided and meta.voided[0][1] == "Alpha surface 0"
    assert "disagrees" in meta.voided[0][2]


def test_mint_id_is_readable_then_deterministically_suffixed():
    taken = set()
    a = dp.mint_id("WHEEL honesty rail", "cl-a", "claim one", taken)
    assert a == "pos-derived-wheel-honesty-rail"
    taken.add(a)
    b = dp.mint_id("WHEEL honesty rail", "cl-a", "claim two", taken)
    assert b.startswith("pos-derived-wheel-honesty-rail-") and b != a
    assert b == dp.mint_id("WHEEL honesty rail", "cl-a", "claim two", taken)


# =========================================================================
# T006 — change 3.3: the evidence contract enforced before persistence
# =========================================================================

def test_fabricated_passage_rejects_the_whole_cluster():
    _, meta = run(invoke=fake_invoke(
        {"candidates": [candidate(passage="this text exists nowhere")]}))
    assert meta.proposed == 0
    assert "must be real" in meta.skipped_clusters[0][1]


def test_non_member_path_rejected():
    _, meta = run(invoke=fake_invoke(
        {"candidates": [candidate(path="ideation/brainstorm/other.md")]}))
    assert meta.proposed == 0 and meta.skipped_clusters


def test_missing_path_is_unsourced_and_rejected():
    cand = candidate()
    del cand["path"]
    _, meta = run(invoke=fake_invoke({"candidates": [cand]}))
    assert meta.proposed == 0 and meta.skipped_clusters


def test_empty_prose_fields_rejected():
    _, meta = run(invoke=fake_invoke(
        {"candidates": [candidate(claim="  ")]}))
    assert meta.proposed == 0
    assert "claim" in meta.skipped_clusters[0][1]


def test_over_budget_output_rejected_whole_cluster():
    cands = [candidate(i) for i in range(dp.MAX_CANDIDATES_PER_CLUSTER + 1)]
    _, meta = run(invoke=fake_invoke({"candidates": cands}))
    assert meta.proposed == 0
    assert "budget" in meta.skipped_clusters[0][1]


def test_source_revision_must_be_committed():
    out, voided, rejects = dp.enforce_candidates(
        {"candidates": [candidate()]}, cluster(),
        {"ideation/brainstorm/alpha-1.md":
         {"repository": "openxFactory",
          "content": candidate()["passage"]}},
        source_revision="not-a-sha")
    assert out is None and "committed revision" in rejects[0]


def test_zero_candidates_is_a_valid_result():
    proposals, meta = run(invoke=fake_invoke({"candidates": []}))
    assert proposals == [] and not meta.skipped_clusters
    assert meta.envelopes  # the cluster WAS evaluated


def test_worker_failure_records_skip_never_raises():
    _, meta = run(invoke=fake_invoke(RuntimeError("simulated outage")))
    assert meta.proposed == 0
    assert "worker failed" in meta.skipped_clusters[0][1]


# =========================================================================
# T003 — selection: pending-review pile-up guard + duplicate suppression
# =========================================================================

def _derived(pid="pos-derived-old", *, cid="cl-alpha", claim="Old claim.",
             disposed=None, state="latent"):
    entry = {"id": pid, "title": "Old", "claim": claim, "state": state,
             "origin": "ai-derived",
             "provenance": {"document": "d", "section": "s"},
             "derivation": {"worker_run": {
                 "correlation_id": "DPOSS-x", "worker_profile":
                 "derive-possibles",
                 "prompt_contract_version": "derive-possibles-prompt-v1"},
                 "disposition": "pending_review"},
             "claiming_clusters": [cid],
             "supporting_evidence": [{"document": "d", "section": "s",
                                      "passage_sha256": "0" * 64}]}
    if disposed:
        entry["derivation"]["human_disposition"] = {
            "outcome": disposed, "authority": "openxFactory ideation gate"}
        if disposed == "rejected":
            entry.update(state="rejected", reason="why", citation="cite")
    return entry


def test_cluster_with_undisposed_derived_possible_is_skipped():
    calls = []

    def invoke(prompt, model):
        calls.append(1)
        return {"candidates": []}
    _, meta = run(index_with(register=[_derived()]), invoke=invoke)
    assert calls == []  # never invoked
    assert "undisposed" in meta.skipped_clusters[0][1]


def test_disposed_cluster_derives_but_duplicate_claim_is_suppressed():
    register = [_derived(disposed="rejected",
                         claim="The alpha cluster could become surface 0.")]
    proposals, meta = run(index_with(register=register),
                          invoke=fake_invoke(
                              {"candidates": [candidate(0), candidate(1)]}))
    # the rejected audit trail suppresses re-derivation of the same claim...
    assert [p["title"] for p in proposals] == ["Alpha surface 1"]
    assert any("never silently re-derived" in v[2] for v in meta.voided)


def test_same_run_cross_cluster_ids_stay_unique():
    cl_a = cluster("cl-alpha", ("ideation/brainstorm/alpha-1.md",
                                "ideation/brainstorm/alpha-2.md"))
    cl_b = cluster("cl-beta", ("ideation/brainstorm/beta-1.md",
                               "ideation/brainstorm/beta-2.md"))
    idx = index_with(clusters=[cl_a, cl_b])

    def invoke(prompt, model):
        payload = json.loads(
            prompt.rsplit("```json\n", 1)[1].split("\n```", 1)[0])
        d = payload["documents"][0]
        passage = next(s.strip() for s in d["content"].splitlines()
                       if len(s.strip()) > 20)
        return {"candidates": [{"title": "Shared title",
                                "claim": f"Claim for "
                                         f"{payload['cluster_id']}.",
                                "rationale": "r", "path": d["path"],
                                "section": "Body", "passage": passage}]}
    proposals, meta = run(idx, docs_for(cl_a, cl_b), invoke=invoke)
    assert meta.proposed == 2
    ids = [p["id"] for p in proposals]
    assert len(set(ids)) == 2  # collision re-minted deterministically


# =========================================================================
# T007 — change 3.4: concurrency-protected next-run merge
# =========================================================================

def _proposals(index=None):
    return run(index, invoke=fake_invoke({"candidates": [candidate()]}))


def test_merge_appends_and_touches_only_the_register_section():
    idx = index_with()
    proposals, meta = _proposals(idx)
    merged, added, skipped = dp.merge_register(
        idx, proposals, expected_fingerprint=meta.register_fingerprint)
    assert added == [proposals[0]["id"]] and skipped == []
    assert merged["topic_entries"] is idx["topic_entries"]  # untouched
    assert merged["generation"] is idx["generation"]
    assert idx.get("possibles_register") is None  # input never mutated
    assert [e["id"] for e in merged["possibles_register"]] == added


def test_merge_refuses_a_stale_register():
    idx = index_with()
    proposals, meta = _proposals(idx)
    idx["possibles_register"] = [_derived("pos-derived-raced",
                                          claim="A concurrent claim.")]
    with pytest.raises(dp.StaleRegisterError):
        dp.merge_register(idx, proposals,
                          expected_fingerprint=meta.register_fingerprint)


def test_remerging_the_same_proposals_adds_nothing():
    idx = index_with()
    proposals, meta = _proposals(idx)
    merged, added, _ = dp.merge_register(
        idx, proposals, expected_fingerprint=meta.register_fingerprint)
    again, added2, skipped2 = dp.merge_register(
        merged, proposals,
        expected_fingerprint=dp.register_fingerprint(
            merged["possibles_register"]))
    assert added2 == [] and skipped2
    assert len(again["possibles_register"]) == len(added)


def test_merge_reminting_preserves_id_uniqueness():
    idx = index_with(register=[_derived("pos-derived-alpha-surface-0",
                                        claim="A different claim.",
                                        disposed="accepted")])
    proposals, meta = _proposals(idx)
    # force the collision: the proposal minted against an empty same-run view
    proposals[0]["id"] = "pos-derived-alpha-surface-0"
    merged, added, _ = dp.merge_register(
        idx, proposals, expected_fingerprint=meta.register_fingerprint)
    ids = [e["id"] for e in merged["possibles_register"]]
    assert len(ids) == len(set(ids)) == 2


# =========================================================================
# T008 — change 3.4: one-way gate-console dispositions
# =========================================================================

def _merged_index():
    idx = index_with()
    proposals, meta = _proposals(idx)
    merged, added, _ = dp.merge_register(
        idx, proposals, expected_fingerprint=meta.register_fingerprint)
    return merged, added[0]


def test_accept_stays_latent_retaining_origin_and_records_the_verdict():
    idx, pid = _merged_index()
    out = dp.apply_disposition(idx, pid, outcome="accepted",
                               authority="openxFactory ideation gate",
                               at="2026-07-22", note="good candidate")
    entry = next(e for e in out["possibles_register"] if e["id"] == pid)
    assert entry["state"] == "latent"          # first-class latent possible
    assert entry["origin"] == "ai-derived"     # provenance retained
    hd = entry["derivation"]["human_disposition"]
    assert hd == {"outcome": "accepted",
                  "authority": "openxFactory ideation gate",
                  "at": "2026-07-22", "note": "good candidate"}
    # the machine field is immutable
    assert entry["derivation"]["disposition"] == "pending_review"
    # the input index was never mutated
    src = next(e for e in idx["possibles_register"] if e["id"] == pid)
    assert "human_disposition" not in src["derivation"]


def test_reject_requires_reason_and_citation_then_records_them():
    idx, pid = _merged_index()
    with pytest.raises(dp.DispositionError):
        dp.apply_disposition(idx, pid, outcome="rejected",
                             authority="gate")  # uncited rejection refused
    out = dp.apply_disposition(idx, pid, outcome="rejected",
                               authority="gate", reason="not viable",
                               citation="cl-alpha review 2026-07-22")
    entry = next(e for e in out["possibles_register"] if e["id"] == pid)
    assert entry["state"] == "rejected"
    assert entry["reason"] == "not viable"
    assert entry["citation"] == "cl-alpha review 2026-07-22"


def test_disposition_is_one_way_except_from_deferred():
    idx, pid = _merged_index()
    deferred = dp.apply_disposition(idx, pid, outcome="deferred",
                                    authority="gate")
    # a deferred entry may be re-disposed...
    accepted = dp.apply_disposition(deferred, pid, outcome="accepted",
                                    authority="gate")
    # ...but an accepted one is final
    with pytest.raises(dp.DispositionError):
        dp.apply_disposition(accepted, pid, outcome="rejected",
                             authority="gate", reason="r", citation="c")


def test_disposing_a_human_authored_or_unknown_entry_is_refused():
    idx = index_with(register=[{
        "id": "pos-human", "title": "Human", "claim": "c", "state": "latent",
        "provenance": {"document": "d", "section": "s"}}])
    with pytest.raises(dp.DispositionError):
        dp.apply_disposition(idx, "pos-human", outcome="accepted",
                             authority="gate")
    with pytest.raises(dp.DispositionError):
        dp.apply_disposition(idx, "pos-missing", outcome="accepted",
                             authority="gate")
    with pytest.raises(dp.DispositionError):
        dp.apply_disposition(idx, "pos-human", outcome="promoted",
                             authority="gate")  # unknown outcome
    with pytest.raises(dp.DispositionError):
        dp.apply_disposition(idx, "pos-human", outcome="accepted",
                             authority="  ")   # no authority


# =========================================================================
# T009/T010 — change 3.5: the non-mutating bound
# =========================================================================

def _write_fake_renderer(root: Path) -> Path:
    scripts = root / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "render-ideation-cross-reference.py").write_text(
        "def render_markdown(index):\n"
        "    return '# projection\\n'\n", encoding="utf-8")
    return root


def test_persist_writes_only_allowlisted_paths_through_the_boundary(
        tmp_path, monkeypatch):
    monkeypatch.setenv(
        "OPENXFACTORY_ROOT", str(_write_fake_renderer(tmp_path / "openx")))
    root = tmp_path / "repo"
    idx = index_with()
    proposals, meta = _proposals(idx)
    merged, added, skipped = dp.merge_register(
        idx, proposals, expected_fingerprint=meta.register_fingerprint)
    written, boundary = dp.persist(merged, meta, root=root, as_of=AS_OF,
                                   added=added, skipped_merge=skipped)
    assert boundary.refusals == []
    assert (root / "ideation/cross-reference.yaml").is_file()
    assert (root / "ideation/cross-reference.md").is_file()
    evidence = root / "health/derive-possibles/2026-07-09/run-1.yaml"
    assert evidence.is_file()
    written_paths = sorted(p.relative_to(root).as_posix()
                           for p in root.rglob("*") if p.is_file())
    assert all(p.startswith("ideation/cross-reference") or
               p.startswith("health/derive-possibles/")
               for p in written_paths)
    import yaml as yaml_mod
    record = yaml_mod.safe_load(evidence.read_text(encoding="utf-8"))
    assert record["kind"] == "derive_possibles_run"
    assert record["status"] == "record"
    assert record["register_fingerprint_read"] == meta.register_fingerprint
    assert record["register_fingerprint_written"] == dp.register_fingerprint(
        merged["possibles_register"])
    assert record["proposed"] == [{"id": added[0]}]


def test_any_other_write_path_is_refused_recorded_and_raised(tmp_path):
    from ideation_dashboard.boundary import BoundaryViolation
    boundary = dp.make_boundary(tmp_path)
    with pytest.raises(BoundaryViolation):
        boundary.write_output("ideation/brainstorm/alpha-1.md", "MUTATED")
    assert len(boundary.refusals) == 1
    assert boundary.refusals[0].kind == "outside-allowlist"


def test_source_documents_are_byte_unchanged_after_a_full_run(tmp_path):
    src = tmp_path / "ideation/brainstorm/alpha-1.md"
    src.parent.mkdir(parents=True)
    original = doc("ideation/brainstorm/alpha-1.md").text
    src.write_text(original, encoding="utf-8")
    (tmp_path / "ideation/brainstorm/alpha-2.md").write_text(
        doc("ideation/brainstorm/alpha-2.md").text, encoding="utf-8")
    docs = corpus.load_docs("openxFactory", tmp_path)
    idx = index_with()
    proposals, meta = dp.run_derivation(
        idx, docs, source_revision=REV, as_of=AS_OF, run_id="run-9",
        invoke=payload_mock_invoke())
    merged, added, skipped = dp.merge_register(
        idx, proposals, expected_fingerprint=meta.register_fingerprint)
    dp.persist(merged, meta, root=tmp_path, as_of=AS_OF, added=added,
               skipped_merge=skipped)
    assert src.read_text(encoding="utf-8") == original  # never mutated


def test_rendered_index_carries_both_lane_attributions():
    idx = index_with(register=[])
    text = dp.render_index_yaml(idx)
    assert "readiness scorer" in text        # the shared index header
    assert "derive-possibles lane" in text   # this lane's attribution line


# =========================================================================
# Pipeline proof (SC-1) — the REAL landed index + corpus, a deterministic
# mock worker, merge, and the pinned openxFactory validator. Skips when the
# sibling checkout is unreachable (standalone clone).
# =========================================================================

def test_pipeline_proof_derives_over_the_real_index_and_validates_clean(
        tmp_path):
    openx = _openxfactory_root_or_skip()
    import yaml as yaml_mod
    index = yaml_mod.safe_load(
        (openx / "ideation/cross-reference.yaml").read_text(encoding="utf-8"))
    docs = corpus.load_docs("openxFactory", openx)
    proposals, meta = dp.run_derivation(
        index, docs, source_revision=REV, as_of=AS_OF, run_id="proof-1",
        invoke=payload_mock_invoke(n=2))
    assert meta.proposed > 0  # the real clusters yield real proposals
    merged, added, skipped = dp.merge_register(
        index, proposals, expected_fingerprint=meta.register_fingerprint)
    assert len(added) == meta.proposed

    # every persisted derived entry satisfies the delta's derived-entry shape
    for entry in merged["possibles_register"]:
        assert entry["origin"] == "ai-derived"
        assert entry["derivation"]["disposition"] == "pending_review"
        assert entry["claiming_clusters"]
        assert entry["supporting_evidence"]

    candidate_file = tmp_path / "cross-reference.yaml"
    candidate_file.write_text(dp.render_index_yaml(merged), encoding="utf-8")
    ok, detail = dp.validate_index(candidate_file, repo=openx)
    if ok is None:
        pytest.skip(f"pinned validator unreachable: {detail}")
    assert ok, f"pinned validator rejected the merged index:\n{detail}"
