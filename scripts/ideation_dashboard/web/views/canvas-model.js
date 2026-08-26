// Per-cluster cluster-canvas view-model (D12). PURE: no DOM, no I/O, no
// external imports — imported by canvas.js in the browser AND unit-tested from
// Python via node (tests/ideation-dashboard/test_canvas.py), exactly like
// model.js. The canvas reads ONLY the snapshot; this module derives the three
// panes and the possibles rail from snapshot fields and NEVER re-scores or
// re-derives anything the snapshot already carries verbatim.
//
// The cluster canvas is the war room where feat quality is decided (D11/D12).
// Its three panes, derived strictly from the snapshot:
//   MEMBER PANE     exactly the cluster's Topics-derived `document_edges`.
//                   Downstream artifacts (staged picks / proposals / realized)
//                   are the LINEAGE STRIP — never members (spec scenario 1).
//   EVIDENCE BOARD  the pinned passages of this cluster's possibles
//                   (`supporting_evidence`: document + section + passage hash).
//   GAP PROMPTS     actionable slots — a member document unclaimed by any of
//                   this cluster's possibles; a possible with no document
//                   support (spec scenario 2).
// plus the POSSIBLES RAIL grouped by `option_set.id` (T021).
//
// Draft CONTENT is authored server-side (canvas_drafts.py, through the
// interactivity boundary) — this module only produces the human-readable PLAN
// of a choose-one / composer draft for the on-screen confirmation (what will be
// drafted, and that a human commits it). The reason/citation wording MUST match
// canvas_drafts.py (locked by a cross-check in test_canvas.py).

// Shared HTML-escape (same discipline as funnel.js/board.js). Exported and
// node-tested so the DOM-safety proof is anchored on a real function; canvas.js
// itself binds every dynamic value via textContent, so this is belt-and-braces.
export function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

// The one wording the browser preview and the boundary-written draft share.
// canvas_drafts.SUPERSEDE_REASON MUST produce the identical string.
export function supersedeReason(chosenId) {
  return "Option-set sibling " + chosenId + " was chosen at the cluster canvas.";
}

// Where a committed draft lands — a run-local drafts dir under the boundary's
// declared allowlist (gitignored ideation/workbench/), NEVER the register.
// canvas_drafts.DRAFTS_DIR MUST match.
export const DRAFTS_DIR = "ideation/workbench/drafts/";

function docsById(snapshot) {
  const map = new Map();
  for (const d of snapshot.documents || []) map.set(d.id, d);
  return map;
}

// The possibles that CLAIM this cluster (many-to-many `claiming_clusters`).
function clusterPossibles(snapshot, clusterId) {
  return (snapshot.possibles || []).filter(
    (p) => (p.claiming_clusters || []).includes(clusterId));
}

// A lightweight per-cluster summary for the canvas picker (deterministic,
// snapshot order). memberCount/possibleCount from the tallies verbatim; gapCount
// is derived here so the picker can flag clusters that need work.
export function listCanvasClusters(snapshot) {
  const s = snapshot || {};
  return (s.clusters || []).map((c) => {
    const model = buildCanvasModel(s, c.id);
    return {
      id: c.id,
      name: c.name || c.id,
      memberCount: model.members.length,
      possibleCount: model.possibles.length,
      evidenceCount: model.evidence.length,
      gapCount: model.gaps.length,
    };
  });
}

// The full per-cluster canvas model. Returns null when the cluster is absent
// (a stale selection after regeneration) so the view degrades, never throws.
export function buildCanvasModel(snapshot, clusterId) {
  const s = snapshot || {};
  const cluster = (s.clusters || []).find((c) => c.id === clusterId);
  if (!cluster) return null;

  const byId = docsById(s);

  // MEMBER PANE — strictly the snapshot's Topics-derived document_edges, in
  // edge order. A member carries its matched topics and (when catalogued) its
  // document entry for the summary line. NOTHING downstream leaks in here.
  const members = (cluster.document_edges || []).map((e) => ({
    document: e.document,
    matchedTopics: e.matched_topics || [],
    doc: byId.get(e.document) || null,
  }));
  const memberIds = new Set(members.map((m) => m.document));

  // LINEAGE STRIP — the cluster's downstream progression, rendered SEPARATELY
  // from the member pane (spec scenario 1: downstream artifacts appear only in
  // the lineage strip). Verbatim from the snapshot's cluster.lineage.
  const lin = cluster.lineage || {};
  const lineage = {
    staged_picks: lin.staged_picks || [],
    proposals: lin.proposals || [],
    realized: lin.realized || [],
  };

  const possibles = clusterPossibles(s, clusterId);

  // EVIDENCE BOARD — the pinned passages of this cluster's possibles: each pin
  // carries its section reference and passage hash (D12). Rendered in a stable
  // order (possible order, then pin order).
  const evidence = [];
  const supportedMemberIds = new Set();
  for (const p of possibles) {
    for (const pin of p.supporting_evidence || []) {
      evidence.push({
        document: pin.document,
        section: pin.section || null,
        passage_sha256: pin.passage_sha256 || null,
        possibleId: p.id,
        possibleTitle: p.title || p.id,
      });
      if (memberIds.has(pin.document)) supportedMemberIds.add(pin.document);
    }
  }

  // GAP PROMPTS — two actionable-slot derivations, both from the snapshot:
  //   unclaimed-member : a member document no possible of this cluster pins as
  //                      evidence (a latent feat waiting to be named).
  //   unsupported-possible : a possible of this cluster with no evidence pin
  //                      (a claim with no document backing).
  const gaps = [];
  for (const m of members) {
    if (!supportedMemberIds.has(m.document)) {
      gaps.push({
        kind: "unclaimed-member",
        document: m.document,
        summary: m.doc && m.doc.summary ? m.doc.summary : null,
      });
    }
  }
  for (const p of possibles) {
    if (!(p.supporting_evidence || []).length) {
      gaps.push({
        kind: "unsupported-possible",
        possibleId: p.id,
        possibleTitle: p.title || p.id,
        state: p.state || "latent",
      });
    }
  }

  // POSSIBLES RAIL — grouped by option_set.id; possibles with no option set are
  // standalone. Option-set members are listed in the snapshot's possible order.
  const optionSetsById = new Map();
  const standalone = [];
  for (const p of possibles) {
    const os = p.option_set;
    if (os && os.id) {
      if (!optionSetsById.has(os.id)) {
        optionSetsById.set(os.id, { id: os.id, declaredMembers: os.members || [], members: [] });
      }
      optionSetsById.get(os.id).members.push(p);
    } else {
      standalone.push(p);
    }
  }
  const optionSets = [...optionSetsById.values()];

  return { cluster, members, lineage, possibles, evidence, gaps, optionSets, standalone };
}

// The on-screen PLAN of a choose-one draft (T021): the chosen option proceeds
// and each SIBLING is drafted `superseded` with the required reason + citation
// (the chosen member's id). Pure — the browser shows this as confirmation; the
// actual boundary-written artifact is canvas_drafts.build_supersede_draft, which
// this must agree with (test_canvas.py locks the reason string).
export function supersedePlan(snapshot, clusterId, optionSetId, chosenId) {
  const model = buildCanvasModel(snapshot, clusterId);
  if (!model) return null;
  const os = model.optionSets.find((o) => o.id === optionSetId);
  if (!os) return null;
  const siblings = os.members
    .filter((p) => p.id !== chosenId)
    .map((p) => ({ id: p.id, title: p.title || p.id, fromState: p.state || "latent" }));
  return {
    optionSetId,
    chosenId,
    siblings,
    reason: supersedeReason(chosenId),
    citation: chosenId,
    landsAt: DRAFTS_DIR + "supersede-" + optionSetId + "-" + chosenId + ".register.yaml",
  };
}

// The on-screen PLAN of a composer draft (T021): a new `latent` possible with
// provenance and any attached evidence pins. Pure preview; the artifact is
// canvas_drafts.build_composer_draft.
export function composerPlan(snapshot, clusterId, input) {
  const model = buildCanvasModel(snapshot, clusterId);
  if (!model) return null;
  const inp = input || {};
  const id = String(inp.id || "").trim();
  const attached = inp.evidenceDocuments || [];
  // provenance preview: first attached pin's doc, else the cluster's first member.
  let provenanceDoc = attached.length ? attached[0] : null;
  if (!provenanceDoc && model.members.length) provenanceDoc = model.members[0].document;
  return {
    id,
    title: (inp.title || "").trim(),
    claim: (inp.claim || "").trim(),
    state: "latent",
    clusterId,
    provenanceDoc,
    evidenceCount: attached.length,
    landsAt: DRAFTS_DIR + "possible-" + (id || "unnamed") + ".register.yaml",
  };
}
