"""US6 keyword-lens set-builder tests (T025):

  * lens-model.js geometry — the ACTUAL module run in node against the real
    fixture snapshot (mirroring test_canvas.py's model pattern): ring index =
    match count (radius monotonic, innermost = all-checked), subset sectoring
    (docs sharing a matched subset share a sector angle), pin = require hard-
    filter, and the deterministic co-occurrence hint math;
  * matrix parity — the flat matrix view carries EXACTLY the bullseye membership
    (same documents, same rings), and the matrix is ALWAYS rendered;
  * override flow end-to-end — a manual include/exclude with a reason lands a
    schema-valid manifest through the boundary; a reasonless override is REFUSED
    by the engine (overrides are evidence, never a silent set edit);
  * recipe re-run — growing the corpus (a second doctored snapshot) surfaces the
    newly-matching doc as a new_candidate WITHOUT altering recorded overrides,
    and the result stays disjoint from members ∪ excluded (validator rule);
  * add-as-cluster — a recipe-seeded manifest is created + validated clean by the
    pinned validator, the attempt is recorded in action_history, and the pending
    queue-proposal note is surfaced (no queue schema invented);
  * DOM-safety — esc() escapes markup, the model/summaries pass governance prose
    through as DATA, and lens.js binds every dynamic value via textContent;
  * asset/no-fetch — the lens bundle files add NO external URL, NO fetch, NO
    dynamic import; JS/Python persistence constants agree byte-for-byte.

All against the REAL fixture snapshot generated in-test via FakeGit +
PINNED_REVISION, exactly like the rest of the suite.
"""

from __future__ import annotations

import copy
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit, find_openxfactory_validator

from ideation_dashboard import human_seen as hs
from ideation_dashboard import lens
from ideation_dashboard import workbench as wb
from ideation_dashboard.boundary import OutputBoundary
from ideation_dashboard.generator import generate_snapshot
from ideation_dashboard.workbench import WorkbenchError

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
LENS_MODEL_JS = WEB / "views" / "lens-model.js"
LENS_JS = WEB / "views" / "lens.js"
NODE = shutil.which("node")
VALIDATOR = find_openxfactory_validator()
XREF_VALIDATOR = hs.find_cross_reference_validator(REPO_ROOT)
NOW = "2026-07-14T08:00:00Z"

# A valid, complete human-seen submission over the fixture corpus — the full
# organizer evidence contract (proposer + committed revision + passage hash +
# section + rationale + confidence + alternatives). `over` patches any field.
def _submission(**over):
    fields = {
        "proposer": "brett",
        "repository": "fixture-repo",
        "path": "ideation/brainstorm/dtn-register.md",
        "revision": PINNED_REVISION,
        "section": "Notes",
        "passage_sha256": "b0f04c299263dd2496c601fbbd812d645ebade162c5a9aa15e8fe8b7a656bc7a",
        "rationale": "Two governance notes describe the same cluster; grouping them for review.",
        "confidence": 0.6,
        "alternatives": ["Fold into an existing governance cluster instead."],
    }
    fields.update(over)
    return hs.HumanSeenSubmission(**fields)


def _snapshot():
    return generate_snapshot(BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


def _boundary(root: Path, *extra: str) -> OutputBoundary:
    return OutputBoundary(root, [wb.WORKBENCH_DIR, *extra])


def _base(doc: str) -> str:
    return doc.split("/")[-1]


# ----------------------------------------------------------------------------
# the ACTUAL lens-model.js derivation, run in node against the fixture snapshot
# ----------------------------------------------------------------------------

_HARNESS = """
import {
  buildLensModel, evaluateRecipe, coOccurrenceHints, esc, recipeLine,
  savePlan, clusterPlan, manifestRelpath, slug,
  docSummaries, PENDING_PROPOSAL_NOTE, WORKBENCH_DIR,
} from './lens-model.mjs';
import { readFileSync } from 'node:fs';
const snap = JSON.parse(readFileSync(process.argv[2], 'utf8'));

function dot(d) {
  return { document: d.document, matchCount: d.matchCount, subsetKey: d.subsetKey,
           angleBase: d.angleBase, radius: d.radius, ringRadius: d.ringRadius,
           declared: d.declared };
}

const gov = buildLensModel(snap, { checked: ['ideation-governance', 'doc-health'], pinned: [] });
const pinned = buildLensModel(snap, { checked: ['ideation-governance', 'doc-health'], pinned: ['doc-health'] });

// W1: pinning a keyword not in checked must throw.
let w1 = null;
try { evaluateRecipe(snap, ['a'], ['b']); } catch (e) { w1 = 'threw'; }

console.log(JSON.stringify({
  gov: {
    checked: gov.checked,
    universe: gov.universe,
    matched: gov.matched,
    rings: gov.rings,
    dots: gov.dots.map(dot),
    matrix: gov.matrix.map(r => ({ document: r.document,
      cells: r.cells.map(c => c.present), ring: r.ring })),
    recipeLine: gov.recipeLine,
  },
  pinnedUniverse: pinned.universe,
  coocc: coOccurrenceHints(snap, ['ideation-governance'], []).map(
    h => ({ keyword: h.keyword, pulledInward: h.pulledInward, newDocs: h.newDocs, hint: h.hint })),
  w1,
  escaped: esc("<script>alert('x')</script>&\\""),
  summaries: docSummaries(snap),
  savePlanKind: savePlan(gov, 'fixture-repo', 'lens set').kind,
  clusterPlan: (() => { const p = clusterPlan(gov, 'fixture-repo', 'lens set');
    return { kind: p.kind, pendingNote: p.pendingNote, landsAt: p.landsAt }; })(),
  manifestRel: manifestRelpath('lens ideation-governance doc-health'),
  slug: slug('Lens Recipe Set!!'),
  note: PENDING_PROPOSAL_NOTE,
  dir: WORKBENCH_DIR,
  recipeLineOverrides: recipeLine(['a', 'b'], ['a'], { 'x': 'r' }, {}),
}));
"""


def _run_node(snapshot, tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.mjs")
    (tmp_path / "harness.mjs").write_text(_HARNESS, encoding="utf-8")
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(snapshot), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "harness.mjs"), str(snap_path)],
        capture_output=True, text=True, cwd=tmp_path,
    )
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


# ----------------------------------------------------------------------------
# the gate-verb REQUEST builders (add-lens-gate-verbs): recipeRequest /
# clusterRequest map a confirmed PLAN to the POST body its verb route re-
# evaluates server-side. Run in node against the fixture snapshot.
# ----------------------------------------------------------------------------

_REQUEST_HARNESS = """
import {
  buildLensModel, savePlan, clusterPlan,
  recipeRequest, clusterRequest, LENS_SAVE_ROUTE, LENS_CLUSTER_ROUTE,
} from './lens-model.mjs';
import { readFileSync } from 'node:fs';
const snap = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const model = buildLensModel(snap, {
  checked: ['ideation-governance'], pinned: [],
  includes: { 'ideation/brainstorm/avatar-client-lab.md': 'belongs here' },
  excludes: { 'ideation/brainstorm/dtn-register.md': 'tracked elsewhere' },
});
const save = savePlan(model, 'fixture-repo', 'lens set');
const cluster = clusterPlan(model, 'fixture-repo', 'lens set');
const req = recipeRequest(save);
const creq = clusterRequest(cluster, { proposer: 'brett', revision: 'deadbeef' });
console.log(JSON.stringify({
  req, creqEvidence: creq.evidence,
  creqRecipeMatchesSave: JSON.stringify({ ...creq, evidence: undefined }) ===
                         JSON.stringify({ ...recipeRequest(save), evidence: undefined }),
  saveRoute: LENS_SAVE_ROUTE, clusterRoute: LENS_CLUSTER_ROUTE,
}));
"""


def _run_request_node(snapshot, tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(LENS_MODEL_JS, tmp_path / "lens-model.mjs")
    (tmp_path / "reqharness.mjs").write_text(_REQUEST_HARNESS, encoding="utf-8")
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(snapshot), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "reqharness.mjs"), str(snap_path)],
        capture_output=True, text=True, cwd=tmp_path,
    )
    assert proc.returncode == 0, f"node request harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def test_recipe_request_carries_recipe_and_reasoned_overrides(tmp_path):
    r = _run_request_node(_snapshot(), tmp_path)
    req = r["req"]
    # the body carries the human's INPUTS (recipe + reasons), never a member list
    # — the server re-evaluates membership from these keywords.
    assert "members" not in req and "excluded" not in req
    assert req["name"] == "lens set" and req["repository"] == "fixture-repo"
    assert req["checked"] == ["ideation-governance"] and req["pinned"] == []
    # the manual-include override travels as {document: reason}; likewise exclude.
    assert req["includes"] == {"ideation/brainstorm/avatar-client-lab.md": "belongs here"}
    assert req["excludes"] == {"ideation/brainstorm/dtn-register.md": "tracked elsewhere"}


def test_cluster_request_is_the_recipe_plus_evidence(tmp_path):
    r = _run_request_node(_snapshot(), tmp_path)
    # add-as-cluster posts the SAME recipe body plus the human-seen evidence block.
    assert r["creqRecipeMatchesSave"] is True
    assert r["creqEvidence"] == {"proposer": "brett", "revision": "deadbeef"}
    assert r["saveRoute"] == "/actions/gate/lens-save-recipe"
    assert r["clusterRoute"] == "/actions/gate/lens-add-as-cluster"


# ---- ring index = match count (geometry) ----

def test_ring_index_equals_match_count(tmp_path):
    r = _run_node(_snapshot(), tmp_path)["gov"]
    # checked = [ideation-governance, doc-health]: doc-health-checks matches both
    # (centre ring, match 2); dtn-register + gov README match one (outer ring).
    by_doc = {_base(d["document"]): d for d in r["dots"]}
    assert by_doc["doc-health-checks.md"]["matchCount"] == 2
    assert by_doc["dtn-register.md"]["matchCount"] == 1
    assert by_doc["README.md"]["matchCount"] == 1
    # innermost (match 2) dot sits at a SMALLER radius than the outer (match 1).
    assert by_doc["doc-health-checks.md"]["radius"] < by_doc["dtn-register.md"]["radius"]
    # ring metadata: the all-checked ring is the centre and the smallest.
    rings = {ring["matchCount"]: ring for ring in r["rings"]}
    assert rings[2]["isCenter"] is True
    assert rings[2]["outerRadius"] < rings[1]["outerRadius"]
    assert rings[2]["docCount"] == 1 and rings[1]["docCount"] == 2


def test_matched_membership_is_the_innermost_ring(tmp_path):
    r = _run_node(_snapshot(), tmp_path)["gov"]
    # `matched` (recipe membership) is exactly the docs matching ALL checked.
    assert [_base(d) for d in r["matched"]] == ["doc-health-checks.md"]


# ---- subset sectoring ----

def test_subset_sectoring(tmp_path):
    r = _run_node(_snapshot(), tmp_path)["gov"]
    by_doc = {_base(d["document"]): d for d in r["dots"]}
    # the two match-1 docs share the same matched subset -> same sector angle.
    assert by_doc["dtn-register.md"]["subsetKey"] == "ideation-governance"
    assert by_doc["README.md"]["subsetKey"] == "ideation-governance"
    assert by_doc["dtn-register.md"]["angleBase"] == by_doc["README.md"]["angleBase"]
    # the centre doc's subset differs, so it occupies a different sector.
    assert by_doc["doc-health-checks.md"]["subsetKey"] != by_doc["dtn-register.md"]["subsetKey"]
    # v1 renders declared (solid) dots.
    assert all(d["declared"] for d in r["dots"])


# ---- pin = require (hard filter) ----

def test_pin_hard_filters_the_universe(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    # pinning doc-health drops every doc that does not carry it — only
    # doc-health-checks survives (dtn-register / gov README carry only governance).
    assert [_base(d) for d in r["pinnedUniverse"]] == ["doc-health-checks.md"]


def test_w1_pinned_must_be_subset_of_checked(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    assert r["w1"] == "threw"  # evaluateRecipe(['a'], ['b']) rejects the stray pin
    # and the Python engine enforces the same rule.
    snap = _snapshot()
    with pytest.raises(WorkbenchError):
        lens.evaluate_recipe(snap, ["a"], ["b"])


# ---- co-occurrence hint math ----

def test_co_occurrence_hint_math(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    hints = {h["keyword"]: h for h in r["coocc"]}
    # checked = [ideation-governance]; universe = the 3 governance docs.
    # doc-health co-occurs with 1 universe doc (doc-health-checks) -> pulls 1 in.
    assert (hints["doc-health"]["pulledInward"], hints["doc-health"]["newDocs"]) == (1, 0)
    # ideation-dashboard is carried only by 3 non-universe docs -> brings 3 new.
    assert (hints["ideation-dashboard"]["pulledInward"], hints["ideation-dashboard"]["newDocs"]) == (0, 3)
    assert (hints["avatar"]["pulledInward"], hints["avatar"]["newDocs"]) == (0, 1)
    assert (hints["dtn"]["pulledInward"], hints["dtn"]["newDocs"]) == (1, 0)
    assert "pulls 1 inward" in hints["doc-health"]["hint"]
    assert "brings 3 new" in hints["ideation-dashboard"]["hint"]


# ---- matrix parity with the bullseye ----

def test_matrix_membership_equals_bullseye(tmp_path):
    r = _run_node(_snapshot(), tmp_path)["gov"]
    matrix_docs = {row["document"] for row in r["matrix"]}
    bullseye_docs = {d["document"] for d in r["dots"]}
    assert matrix_docs == bullseye_docs == set(r["universe"])
    # each matrix row's ring label agrees with its dot's match count.
    dot_ring = {d["document"]: d["matchCount"] for d in r["dots"]}
    for row in r["matrix"]:
        mc = dot_ring[row["document"]]
        expected = "all 2" if mc == 2 else str(mc)
        assert row["ring"] == expected


# ----------------------------------------------------------------------------
# Python recipe evaluation (mirror of the JS derivation)
# ----------------------------------------------------------------------------

def test_python_evaluate_recipe_matches_the_js(tmp_path):
    snap = _snapshot()
    js = _run_node(snap, tmp_path)["gov"]
    ev = lens.evaluate_recipe(snap, ["ideation-governance", "doc-health"])
    assert ev.universe == js["universe"]
    assert ev.matched == js["matched"]


# ----------------------------------------------------------------------------
# override flow end-to-end
# ----------------------------------------------------------------------------

def test_manual_include_and_exclude_land_a_valid_manifest(tmp_path):
    snap = _snapshot()
    # checked = [ideation-governance]: matches the 3 governance docs.
    w = lens.build_workbench_from_recipe(
        "fixture-repo", "Governance lens", ["ideation-governance"], [], snap,
        includes={"ideation/brainstorm/avatar-client-lab.md": "avatar work belongs with governance"},
        excludes={"ideation/brainstorm/dtn-register.md": "tracked under the DTN register instead"},
        now=NOW)
    members = w.member_documents()
    # the manual-include (a NON-matching doc) is present; the excluded matching
    # doc is dropped from members and recorded as negative evidence.
    assert "ideation/brainstorm/avatar-client-lab.md" in members
    assert "ideation/brainstorm/dtn-register.md" not in members
    assert [e["document"] for e in w.data["excluded"]] == ["ideation/brainstorm/dtn-register.md"]
    # the include carries its recorded reason (evidence, never silent).
    inc = next(m for m in w.data["members"] if m["document"].endswith("avatar-client-lab.md"))
    assert inc["via"] == "manual-include" and inc["reason"]


@pytest.mark.skipif(VALIDATOR is None, reason="pinned openxFactory validator not reachable")
def test_override_manifest_validates_clean(tmp_path):
    snap = _snapshot()
    w = lens.build_workbench_from_recipe(
        "fixture-repo", "Governance lens", ["ideation-governance"], [], snap,
        includes={"ideation/brainstorm/avatar-client-lab.md": "belongs here"},
        excludes={"ideation/brainstorm/dtn-register.md": "tracked elsewhere"}, now=NOW)
    written = wb.save(w, _boundary(tmp_path), validate=True, validator=VALIDATOR)
    proc = subprocess.run([sys.executable, str(VALIDATOR), str(written)],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_override_without_a_reason_is_refused():
    snap = _snapshot()
    # a bare manual-include (no reason) is refused by the engine.
    with pytest.raises(WorkbenchError):
        lens.build_workbench_from_recipe(
            "fixture-repo", "no-reason include", ["ideation-governance"], [], snap,
            includes={"ideation/brainstorm/avatar-client-lab.md": ""}, now=NOW)
    # a bare exclude (no reason) is likewise refused.
    with pytest.raises(WorkbenchError):
        lens.build_workbench_from_recipe(
            "fixture-repo", "no-reason exclude", ["ideation-governance"], [], snap,
            excludes={"ideation/brainstorm/dtn-register.md": ""}, now=NOW)


# ----------------------------------------------------------------------------
# recipe re-run — new_candidates without altering overrides
# ----------------------------------------------------------------------------

def _grow(snapshot, doc_id, topics):
    """A second doctored snapshot: the same corpus plus one new document."""
    grown = copy.deepcopy(snapshot)
    grown["documents"].append({
        "id": doc_id, "path": doc_id, "stage": "brainstorm", "kind": "note",
        "topics": list(topics),
    })
    return grown


def test_recipe_rerun_surfaces_new_candidate_without_touching_overrides():
    snap = _snapshot()
    w = lens.build_workbench_from_recipe(
        "fixture-repo", "Governance lens", ["ideation-governance"], [], snap,
        includes={"ideation/brainstorm/avatar-client-lab.md": "manual include"},
        excludes={"ideation/brainstorm/dtn-register.md": "negative evidence"}, now=NOW)
    members_before = copy.deepcopy(w.data["members"])
    excluded_before = copy.deepcopy(w.data["excluded"])

    grown = _grow(snap, "ideation/brainstorm/new-gov.md", ["ideation-governance"])
    new_candidates = lens.rerun_recipe(grown, w, now="2026-07-14T09:00:00Z")

    # the brand-new matching doc surfaces as a candidate ...
    assert new_candidates == ["ideation/brainstorm/new-gov.md"]
    # ... and NEITHER the members NOR the excluded overrides changed.
    assert w.data["members"] == members_before
    assert w.data["excluded"] == excluded_before
    # new_candidates is disjoint from members ∪ excluded (the validator rule):
    # the excluded matching doc never re-surfaces as a candidate.
    member_docs = set(w.member_documents())
    excluded_docs = {e["document"] for e in w.data["excluded"]}
    assert not (set(new_candidates) & (member_docs | excluded_docs))
    assert "ideation/brainstorm/dtn-register.md" not in new_candidates
    # last_run anchors on the grown snapshot's revision.
    assert w.data["recipe"]["last_run"]["source_revision"] == PINNED_REVISION


@pytest.mark.skipif(VALIDATOR is None, reason="pinned openxFactory validator not reachable")
def test_manifest_with_new_candidates_validates_clean(tmp_path):
    snap = _snapshot()
    w = lens.build_workbench_from_recipe(
        "fixture-repo", "Governance lens", ["ideation-governance"], [], snap,
        excludes={"ideation/brainstorm/dtn-register.md": "negative evidence"}, now=NOW)
    grown = _grow(snap, "ideation/brainstorm/new-gov.md", ["ideation-governance"])
    lens.rerun_recipe(grown, w, now="2026-07-14T09:00:00Z")
    written = wb.save(w, _boundary(tmp_path), validate=True, validator=VALIDATOR)
    proc = subprocess.run([sys.executable, str(VALIDATOR), str(written)],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr


# ----------------------------------------------------------------------------
# add-as-cluster — recipe-seeded manifest + human-seen submission (T028 wiring)
# ----------------------------------------------------------------------------

@pytest.mark.skipif(VALIDATOR is None or XREF_VALIDATOR is None,
                    reason="pinned openxFactory validator(s) not reachable")
def test_add_as_cluster_creates_manifest_and_submits_human_seen(tmp_path):
    snap = _snapshot()
    w = lens.build_workbench_from_recipe(
        "fixture-repo", "Governance lens", ["ideation-governance"], [], snap, now=NOW)
    boundary = _boundary(tmp_path)
    res = lens.add_as_cluster(
        w, boundary, snap, _submission(), now=NOW,
        validate=True, validator=VALIDATOR, xref_validator=XREF_VALIDATOR)
    # (1) the recipe-seeded manifest lands under the gitignored workbench dir.
    assert wb.WORKBENCH_DIR in res.manifest_path.as_posix()
    assert w.data["seed"]["kind"] == wb.SEED_RECIPE
    assert w.data["recipe"]["checked"] == ["ideation-governance"]
    # (2) the human-seen submission lands under the gitignored cross-reference
    # queue (also under ideation/workbench/, so on the same declared allowlist).
    assert hs.QUEUE_DIR in res.queue_path.as_posix()
    assert res.queue_relpath.startswith(hs.QUEUE_DIR)
    # exactly two files were written under the boundary root: manifest + queue entry.
    written = sorted(p for p in tmp_path.rglob("*") if p.is_file())
    assert written == sorted([res.manifest_path, res.queue_path])
    # (3) the add-as-cluster action is recorded under its own HONEST action name,
    # referencing the queue entry the submission wrote (no longer recorded-only).
    action = next(a for a in w.data["action_history"] if a["action"] == wb.ACTION_ADD_AS_CLUSTER)
    assert action["reference"] == res.queue_relpath
    assert res.note == lens.PENDING_PROPOSAL_NOTE
    # (4) the intake is a pending_review human-seen topic entry, and validates
    # clean on BOTH pinned validators (manifest -> dashboard, queue -> xref).
    entry = res.intake["topic_entries"][0]
    assert entry["origin"] == "human-seen"
    assert entry["human_seen"]["disposition"] == "pending_review"
    assert entry["human_seen"]["evidence"]["disposition"] == "pending_review"
    assert res.intake["kind"] == "ideation-cross-reference"
    m = subprocess.run([sys.executable, str(VALIDATOR), str(res.manifest_path)],
                       capture_output=True, text=True)
    assert m.returncode == 0, m.stdout + m.stderr
    q = subprocess.run([sys.executable, str(XREF_VALIDATOR), str(res.queue_path),
                        "--repo", str(XREF_VALIDATOR.resolve().parents[1])],
                       capture_output=True, text=True)
    assert q.returncode == 0, q.stdout + q.stderr


def test_add_as_cluster_action_is_recorded_in_the_persisted_manifest(tmp_path):
    # The add-as-cluster action must be present in the SAVED manifest on disk, not
    # just the in-memory workbench: the action is recorded BEFORE the manifest is
    # written, so reloading the file surfaces it (previously the action was
    # appended after save, leaving the persisted manifest without the entry).
    snap = _snapshot()
    w = lens.build_workbench_from_recipe(
        "fixture-repo", "Governance lens", ["ideation-governance"], [], snap, now=NOW)
    boundary = _boundary(tmp_path)
    res = lens.add_as_cluster(w, boundary, snap, _submission(), now=NOW)
    reloaded = wb.Workbench.load(res.manifest_path)
    actions = [a for a in reloaded.data.get("action_history", [])
               if a["action"] == wb.ACTION_ADD_AS_CLUSTER]
    assert actions, "the persisted manifest must record the add-as-cluster action"
    assert actions[-1]["reference"] == res.queue_relpath


def test_add_as_cluster_refuses_incomplete_evidence_before_any_write(tmp_path):
    snap = _snapshot()
    w = lens.build_workbench_from_recipe(
        "fixture-repo", "Governance lens", ["ideation-governance"], [], snap, now=NOW)
    boundary = _boundary(tmp_path)
    # a submission missing its passage hash is refused BEFORE persistence — no
    # manifest and no queue entry are written (spec "A submission lacks evidence").
    bad = _submission(passage_sha256="")
    with pytest.raises(hs.SubmissionRefused):
        lens.add_as_cluster(w, boundary, snap, bad, now=NOW)
    assert not [p for p in tmp_path.rglob("*") if p.is_file()]
    assert not boundary.refusals


def test_add_as_cluster_queue_stays_on_the_declared_allowlist(tmp_path):
    snap = _snapshot()
    w = lens.build_workbench_from_recipe(
        "fixture-repo", "Governance lens", ["ideation-governance"], [], snap, now=NOW)
    # the boundary allowlists only ideation/workbench/ (the queue lives under it),
    # so the submission has NO route to any off-allowlist path.
    boundary = _boundary(tmp_path)
    lens.add_as_cluster(w, boundary, snap, _submission(), now=NOW)
    from ideation_dashboard.boundary import BoundaryViolation
    with pytest.raises(BoundaryViolation):
        boundary.write_output("ideation/staging/human-seen.yaml", "x: 1")
    assert boundary.refusals and boundary.refusals[-1].kind == "outside-allowlist"


# ----------------------------------------------------------------------------
# DOM-safety
# ----------------------------------------------------------------------------

def test_esc_escapes_markup(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    assert r["escaped"] == "&lt;script&gt;alert('x')&lt;/script&gt;&amp;&quot;"


def test_model_passes_prose_through_as_data(tmp_path):
    # inject markup into a document summary; docSummaries must carry it VERBATIM
    # as data (never pre-rendered HTML), so lens.js's textContent binding neutralises it.
    snap = copy.deepcopy(_snapshot())
    payload = "<img src=x onerror=alert(1)>"
    for d in snap["documents"]:
        if d["id"] == "ideation/brainstorm/dtn-register.md":
            d["summary"] = payload
    r = _run_node(snap, tmp_path)
    assert r["summaries"]["ideation/brainstorm/dtn-register.md"]["summary"] == payload


def test_lens_js_binds_dynamic_values_via_textcontent_only():
    text = LENS_JS.read_text(encoding="utf-8")
    for m in re.finditer(r"\.innerHTML\s*=\s*(.+)", text):
        rhs = m.group(1).strip().rstrip(";").strip()
        assert rhs == '""', f"non-clearing innerHTML assignment in lens.js: {m.group(0)!r}"
    assert "node.textContent = text" in text  # el() binds its text arg via textContent


# ----------------------------------------------------------------------------
# asset / no-fetch (extends the bundle-wide boundary to the lens files)
# ----------------------------------------------------------------------------

def test_lens_bundle_files_present():
    assert LENS_JS.is_file() and LENS_MODEL_JS.is_file()


def test_lens_files_have_no_network_primitive():
    # no fetch, no dynamic import, no external URL beyond the SVG XML namespace.
    external = re.compile(
        r"https?://(?!www\.w3\.org)|unpkg|jsdelivr|googleapis|cdnjs|"
        r"XMLHttpRequest|WebSocket|EventSource|navigator\.sendBeacon", re.IGNORECASE)
    for path in (LENS_JS, LENS_MODEL_JS):
        body = path.read_text(encoding="utf-8")
        assert "fetch(" not in body, f"fetch in {path.name}"
        assert "import(" not in body, f"dynamic import in {path.name}"
        offenders = [ln for ln in body.splitlines() if external.search(ln)]
        assert not offenders, f"external network primitive in {path.name}: {offenders}"


def test_js_and_python_persistence_constants_agree(tmp_path):
    r = _run_node(_snapshot(), tmp_path)
    assert r["note"] == lens.PENDING_PROPOSAL_NOTE
    assert r["dir"] == wb.WORKBENCH_DIR
    assert r["manifestRel"] == wb.manifest_relpath("lens ideation-governance doc-health")
    assert r["slug"] == wb.slug("Lens Recipe Set!!")
    assert r["clusterPlan"]["pendingNote"] == lens.PENDING_PROPOSAL_NOTE
    assert r["clusterPlan"]["kind"] == "add-as-cluster"
    assert r["savePlanKind"] == "save-recipe"
