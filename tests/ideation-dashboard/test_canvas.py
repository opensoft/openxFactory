"""US5 cluster-canvas working surface tests (T022):

  * member-pane derivation exactness — the ACTUAL canvas-model.js run in node
    against the real fixture snapshot (mirroring test_renderer.py's model.js
    pattern): members are EXACTLY the cluster's Topics-derived document_edges,
    downstream artifacts live only in the lineage strip (never members);
  * both gap-prompt derivations (member unclaimed by any possible; possible
    with no document support) against the fixture corpus;
  * option-set grouping (possibles grouped by option_set.id; standalone kept
    separate);
  * choose-one draft output — the boundary-written artifact from
    canvas_drafts.py: the draft file lands under the declared output path,
    carries valid superseded transitions (reason + citation), validates clean
    against the pinned openxFactory validator AND as a legal register
    transition, the register is never written, and a register path is refused
    by the boundary;
  * composer draft validity — a latent register entry with provenance +
    attached evidence, validated clean by the pinned validator;
  * DOM-safety — esc() escapes markup (node), the model passes governance prose
    through as DATA (never pre-rendered HTML), and canvas.js binds every dynamic
    value via textContent (no dynamic innerHTML) — extending the node-side proof
    pattern.

All against the REAL fixture snapshot, generated in-test via the same FakeGit +
PINNED_REVISION substrate as the rest of the suite.
"""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit, find_openxfactory_validator

from ideation_dashboard import canvas_drafts as cd
from ideation_dashboard.boundary import BoundaryViolation, OutputBoundary
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
CANVAS_MODEL_JS = WEB / "views" / "canvas-model.js"
CANVAS_JS = WEB / "views" / "canvas.js"
NODE = shutil.which("node")
VALIDATOR = find_openxfactory_validator()


def _snapshot():
    return generate_snapshot(BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


# ----------------------------------------------------------------------------
# the ACTUAL canvas-model.js derivation, run in node against the fixture snapshot
# ----------------------------------------------------------------------------

_HARNESS = """
import {
  buildCanvasModel, listCanvasClusters, supersedePlan, composerPlan,
  esc, supersedeReason, DRAFTS_DIR,
} from './canvas-model.mjs';
import { readFileSync } from 'node:fs';
const snap = JSON.parse(readFileSync(process.argv[2], 'utf8'));

function compact(m) {
  if (!m) return null;
  return {
    clusterId: m.cluster.id,
    members: m.members.map(x => ({ document: x.document, matchedTopics: x.matchedTopics,
                                   summary: x.doc ? x.doc.summary : null })),
    lineage: m.lineage,
    evidence: m.evidence.map(e => ({ document: e.document, section: e.section,
                                     hash: e.passage_sha256, possibleId: e.possibleId,
                                     possibleTitle: e.possibleTitle })),
    gaps: m.gaps,
    optionSets: m.optionSets.map(o => ({ id: o.id, declaredMembers: o.declaredMembers,
                                         members: o.members.map(p => p.id) })),
    standalone: m.standalone.map(p => p.id),
  };
}

console.log(JSON.stringify({
  clusters: listCanvasClusters(snap),
  gov: compact(buildCanvasModel(snap, 'cl-ideation-governance')),
  avatar: compact(buildCanvasModel(snap, 'cl-avatar')),
  dtn: compact(buildCanvasModel(snap, 'cl-dtn')),
  missing: buildCanvasModel(snap, 'cl-nope'),
  supersede: supersedePlan(snap, 'cl-avatar', 'os-avatar-shape', 'pos-avatar-lab'),
  composer: composerPlan(snap, 'cl-ideation-governance',
    { id: 'regulated-traceability-profile', title: 't', claim: 'c',
      evidenceDocuments: ['ideation/staging/ideation-governance/README.md'] }),
  escaped: esc("<script>alert('x')</script>&\\""),
  reason: supersedeReason('pos-avatar-lab'),
  draftsDir: DRAFTS_DIR,
}));
"""


def _run_node(snapshot, tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(CANVAS_MODEL_JS, tmp_path / "canvas-model.mjs")
    (tmp_path / "harness.mjs").write_text(_HARNESS, encoding="utf-8")
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(snapshot), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "harness.mjs"), str(snap_path)],
        capture_output=True, text=True, cwd=tmp_path,
    )
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


# ---- member pane = Topics edges only; downstream only in the lineage strip ----

def test_member_pane_is_exactly_the_topics_document_edges(tmp_path):
    snap = _snapshot()
    r = _run_node(snap, tmp_path)
    gov = r["gov"]
    cluster = next(c for c in snap["clusters"] if c["id"] == "cl-ideation-governance")
    expected = [e["document"] for e in cluster["document_edges"]]
    assert [m["document"] for m in gov["members"]] == expected
    # matched topics carried through verbatim per edge
    for m, e in zip(gov["members"], cluster["document_edges"]):
        assert m["matchedTopics"] == e["matched_topics"]


def test_downstream_artifacts_are_in_the_lineage_strip_never_members(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    gov = r["gov"]
    member_ids = {m["document"] for m in gov["members"]}
    # the lineage strip carries downstream ids (staged picks + proposals) ...
    assert gov["lineage"]["staged_picks"] == ["ideation-governance"]
    assert gov["lineage"]["proposals"] == ["add-ideation-governance"]
    # ... and NONE of those downstream ids appear as a member document.
    assert "add-ideation-governance" not in member_ids
    for sid in gov["lineage"]["staged_picks"] + gov["lineage"]["proposals"]:
        assert sid not in member_ids


def test_evidence_board_carries_section_ref_and_passage_hash(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    gov = r["gov"]
    assert [e["document"] for e in gov["evidence"]] == [
        "ideation/brainstorm/doc-health-checks.md",
        "ideation/staging/ideation-governance/README.md",
    ]
    for pin in gov["evidence"]:
        assert pin["section"] == "Possible feats"
        assert pin["hash"] and len(pin["hash"]) == 64


def test_missing_cluster_degrades_to_null(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    assert r["missing"] is None


# ---- both gap-prompt derivations against the fixture corpus ----

def test_gap_unclaimed_member(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    gov_gaps = r["gov"]["gaps"]
    unclaimed = [g for g in gov_gaps if g["kind"] == "unclaimed-member"]
    # dtn-register.md is a member of cl-ideation-governance but no possible of
    # that cluster pins it as evidence.
    assert [g["document"] for g in unclaimed] == ["ideation/brainstorm/dtn-register.md"]
    assert len(gov_gaps) == 1  # no unsupported-possible gap here (both are supported)


def test_gap_unsupported_possible(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    avatar_gaps = r["avatar"]["gaps"]
    unsupported = [g for g in avatar_gaps if g["kind"] == "unsupported-possible"]
    # pos-avatar-inline claims cl-avatar but pins no evidence.
    assert [g["possibleId"] for g in unsupported] == ["pos-avatar-inline"]


def test_gap_both_kinds_on_one_cluster(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    kinds = sorted(g["kind"] for g in r["dtn"]["gaps"])
    # cl-dtn: its one member (dtn-register.md) is unclaimed AND its one possible
    # (pos-dtn-autopromote, rejected) has no document support.
    assert kinds == ["unclaimed-member", "unsupported-possible"]


# ---- option-set grouping ----

def test_option_set_grouping(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    avatar = r["avatar"]
    assert avatar["optionSets"] == [{
        "id": "os-avatar-shape",
        "declaredMembers": ["pos-avatar-lab", "pos-avatar-inline"],
        "members": ["pos-avatar-inline", "pos-avatar-lab"],
    }]
    assert avatar["standalone"] == []
    # a cluster with no option set groups everything as standalone
    gov = r["gov"]
    assert gov["optionSets"] == []
    assert sorted(gov["standalone"]) == ["pos-health-sweep", "pos-ideation-governance"]


# ---- JS/Python draft-wording cross-check (the one shared string + path) ----

def test_js_and_python_draft_constants_agree(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    assert r["reason"] == cd.supersede_reason("pos-avatar-lab")
    assert r["draftsDir"] == cd.DRAFTS_DIR


# ----------------------------------------------------------------------------
# choose-one draft — the boundary-written artifact (canvas_drafts.py)
# ----------------------------------------------------------------------------

def _validate_file(path: Path, *extra: str) -> subprocess.CompletedProcess:
    if VALIDATOR is None:
        pytest.skip("pinned openxFactory validator not reachable")
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *extra, str(path)],
        capture_output=True, text=True,
    )


def test_choose_one_draft_lands_under_the_declared_output_path(tmp_path):
    snap = _snapshot()
    boundary = OutputBoundary(tmp_path, [cd.DRAFTS_DIR])
    rel = cd.supersede_draft_path("os-avatar-shape", "pos-avatar-lab")
    written = cd.write_draft(boundary, rel, cd.build_supersede_draft(snap, "os-avatar-shape", "pos-avatar-lab"))
    assert written == (tmp_path / rel).resolve()
    assert written.is_file()
    # the only file written under the boundary root is the draft, under the dir.
    all_written = [p for p in tmp_path.rglob("*") if p.is_file()]
    assert all_written == [written]
    assert cd.DRAFTS_DIR in written.as_posix()


def test_choose_one_draft_contains_valid_superseded_transitions(tmp_path):
    snap = _snapshot()
    draft = cd.build_supersede_draft(snap, "os-avatar-shape", "pos-avatar-lab")
    entries = draft["possibles_register"]
    # the chosen member is NOT in the draft — only its siblings, superseded.
    ids = {e["id"] for e in entries}
    assert "pos-avatar-lab" not in ids
    assert ids == {"pos-avatar-inline"}
    for e in entries:
        assert e["state"] == "superseded"
        assert e["reason"] == cd.supersede_reason("pos-avatar-lab")
        assert e["citation"] == "pos-avatar-lab"
        assert e["provenance"]["document"] and e["provenance"]["section"]


def test_choose_one_draft_validates_against_the_pinned_validator(tmp_path):
    snap = _snapshot()
    boundary = OutputBoundary(tmp_path, [cd.DRAFTS_DIR])
    rel = cd.supersede_draft_path("os-avatar-shape", "pos-avatar-lab")
    written = cd.write_draft(boundary, rel, cd.build_supersede_draft(snap, "os-avatar-shape", "pos-avatar-lab"))
    proc = _validate_file(written)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_choose_one_draft_is_a_legal_register_transition(tmp_path):
    # Prove the draft is a legal move, not just a well-formed section: pair it
    # against a pre-choice "before" where the sibling is still latent.
    import yaml
    snap = _snapshot()
    draft = cd.build_supersede_draft(snap, "os-avatar-shape", "pos-avatar-lab")
    new_entry = draft["possibles_register"][0]
    old_entry = {k: v for k, v in new_entry.items() if k not in ("reason", "citation")}
    old_entry["state"] = "latent"
    (tmp_path / "old.yaml").write_text(yaml.safe_dump({"possibles_register": [old_entry]}, sort_keys=False))
    (tmp_path / "new.yaml").write_text(cd.render_draft(draft))
    if VALIDATOR is None:
        pytest.skip("pinned openxFactory validator not reachable")
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), "--transition", str(tmp_path / "old.yaml"), str(tmp_path / "new.yaml")],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_drafting_never_touches_the_register_and_a_register_path_is_refused(tmp_path):
    snap = _snapshot()
    register = BASE_REPO / "ideation" / "cross-reference.yaml"
    before = register.read_bytes()
    # A boundary allowlisting only the drafts dir refuses a write to the register.
    boundary = OutputBoundary(tmp_path, [cd.DRAFTS_DIR])
    draft = cd.build_supersede_draft(snap, "os-avatar-shape", "pos-avatar-lab")
    cd.write_draft(boundary, cd.supersede_draft_path("os-avatar-shape", "pos-avatar-lab"), draft)
    with pytest.raises(BoundaryViolation):
        cd.write_draft(boundary, "ideation/cross-reference.yaml", draft)
    # the refusal was recorded, not silent, and the real register is untouched.
    assert boundary.refusals and boundary.refusals[-1].kind == "outside-allowlist"
    assert register.read_bytes() == before


# ----------------------------------------------------------------------------
# composer draft validity
# ----------------------------------------------------------------------------

def test_composer_draft_is_a_valid_latent_entry(tmp_path):
    snap = _snapshot()
    draft = cd.build_composer_draft(
        snap, "cl-ideation-governance",
        id="regulated-traceability-profile",
        title="Regulated traceability profile",
        claim="A profile binding FDA SaMD traceability edges to possibles.",
        evidence_documents=["ideation/staging/ideation-governance/README.md"],
    )
    entry = draft["possibles_register"][0]
    assert entry["state"] == "latent"
    assert entry["id"] == "regulated-traceability-profile"
    assert entry["provenance"]["document"] == "ideation/staging/ideation-governance/README.md"
    assert entry["claiming_clusters"] == ["cl-ideation-governance"]
    # the attached pin was resolved from the cluster's evidence board (real hash)
    pin = entry["supporting_evidence"][0]
    assert pin["document"] == "ideation/staging/ideation-governance/README.md"
    assert len(pin["passage_sha256"]) == 64


def test_composer_draft_validates_against_the_pinned_validator(tmp_path):
    snap = _snapshot()
    boundary = OutputBoundary(tmp_path, [cd.DRAFTS_DIR])
    draft = cd.build_composer_draft(
        snap, "cl-ideation-governance",
        id="regulated-traceability-profile",
        title="Regulated traceability profile",
        claim="A profile binding FDA SaMD traceability edges to possibles.",
        evidence_documents=["ideation/staging/ideation-governance/README.md"],
    )
    written = cd.write_draft(boundary, cd.composer_draft_path("regulated-traceability-profile"), draft)
    proc = _validate_file(written)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_composer_draft_without_attached_evidence_derives_cluster_provenance(tmp_path):
    snap = _snapshot()
    draft = cd.build_composer_draft(
        snap, "cl-ideation-governance",
        id="unbacked-idea", title="Unbacked idea", claim="A claim with no pinned evidence yet.",
    )
    entry = draft["possibles_register"][0]
    # provenance falls back to the cluster's first member document.
    cluster = next(c for c in snap["clusters"] if c["id"] == "cl-ideation-governance")
    assert entry["provenance"]["document"] == cluster["document_edges"][0]["document"]
    assert "supporting_evidence" not in entry  # none attached


def test_composer_rejects_missing_required_fields(tmp_path):
    snap = _snapshot()
    with pytest.raises(ValueError):
        cd.build_composer_draft(snap, "cl-ideation-governance", id="", title="t", claim="c")
    with pytest.raises(ValueError):
        cd.build_composer_draft(snap, "cl-ideation-governance", id="x", title="", claim="c")


# ----------------------------------------------------------------------------
# DOM-safety — extend the node-side proof pattern
# ----------------------------------------------------------------------------

def test_esc_escapes_markup(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    assert r["escaped"] == "&lt;script&gt;alert('x')&lt;/script&gt;&amp;&quot;"


def test_model_passes_prose_through_as_data_not_html(tmp_path):
    # Inject markup into governance prose (a member doc summary and a possible
    # title). The pure model must carry it through VERBATIM as data — it never
    # pre-renders HTML — so canvas.js's textContent binding neutralises it.
    snap = copy.deepcopy(_snapshot())
    payload = "<script>alert('xss')</script>"
    for d in snap["documents"]:
        if d["id"] == "ideation/brainstorm/dtn-register.md":
            d["summary"] = payload
    for p in snap["possibles"]:
        if p["id"] == "pos-ideation-governance":
            p["title"] = payload
    r = _run_node(snap, tmp_path)
    gov = r["gov"]
    # the injected summary rides through the unclaimed-member gap as raw data
    gap = next(g for g in gov["gaps"] if g["kind"] == "unclaimed-member")
    assert gap["summary"] == payload
    # the injected possible title rides through the evidence board as raw data
    assert any(e["possibleTitle"] == payload for e in gov["evidence"])


def test_canvas_js_binds_dynamic_values_via_textcontent_only():
    # canvas.js's el() sets textContent (never innerHTML); the ONLY innerHTML
    # occurrences are clears (`= ""`). No dynamic value is ever concatenated
    # into innerHTML — the deliberate DOM-safety posture for the war room.
    import re
    text = CANVAS_JS.read_text(encoding="utf-8")
    for m in re.finditer(r"\.innerHTML\s*=\s*(.+)", text):
        rhs = m.group(1).strip().rstrip(";").strip()
        assert rhs == '""', f"non-clearing innerHTML assignment in canvas.js: {m.group(0)!r}"
    # and el() uses textContent for its text argument
    assert "node.textContent = text" in text
