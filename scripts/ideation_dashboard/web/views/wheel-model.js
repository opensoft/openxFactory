// Snapshot -> WHEEL view-model derivation (THE WHEEL locked interaction spec,
// Track C, Brett-approved 2026-07-16; ideation-dashboard brainstorm). PURE: no
// DOM, no I/O, no external imports — it is imported by wheel.js in the browser
// AND unit-tested from Python via node (tests/ideation-dashboard/
// test_wheel_model.py), exactly like model.js.
//
// REALIZATION DATA CONTRACT (the locked spec's last clause + the
// add-possibles-derivation-lane delta "Derived possibles are a distinct class
// until disposed"): the wheel consumes MATERIALIZED cross-class edges — never
// token-overlap inference — each carrying a class field that drives thread
// styling:
//   indexed     solid teal   a relation the snapshot carries as governed data
//   inferred    dashed teal  an UNDISPOSED ai-derived possible's edges (the
//                            delta's non-`indexed` rule; an ACCEPTED derived
//                            possible is real register data -> indexed)
//   synthesized dashed brass demo placeholders under the possibles honesty
//                            rule (register empty), never confusable with
//                            indexed data
//
// Six wheels in funnel order: documents -> clusters -> possibles -> staged ->
// active -> archived. Every relation is read from snapshot fields the
// generator already materializes (document_edges, claiming_clusters, pick,
// lineage.staged_picks, origin_staging_id); nothing is re-derived from text.

export const WHEEL_KEYS = ["documents", "clusters", "possibles", "staged", "active", "archived"];

export const WHEEL_LABELS = {
  documents: "documents",
  clusters: "clusters",
  possibles: "possibles",
  staged: "staged",
  active: "active",
  archived: "archived",
};

const MAX_DEMO_POSSIBLES = 6;

function basename(path) {
  return String(path).split("/").at(-1) || String(path);
}

// An undisposed ai-derived possible: origin ai-derived and no human verdict
// yet (a deferred verdict keeps it awaiting => still undisposed for the
// distinct-class rule; only an ACCEPT makes it first-class register data).
export function isUndisposedDerived(possible) {
  if (possible?.origin !== "ai-derived") return false;
  const human = possible.derivation?.human_disposition;
  return !human || human.outcome === "deferred";
}

// The possibles honesty rule: while the register carries no possibles the
// wheel MAY show synthesized placeholders derived from real clusters — each
// demo-tagged and threaded in dashed brass, never confusable with indexed
// data. Deterministic: top clusters by document-link tally, id order tiebreak.
export function synthesizeDemoPossibles(clusters) {
  const ranked = [...(clusters || [])].sort((a, b) => {
    const ta = a.tallies?.document_links || 0;
    const tb = b.tallies?.document_links || 0;
    return tb - ta || String(a.id).localeCompare(String(b.id));
  });
  return ranked.slice(0, MAX_DEMO_POSSIBLES).map((c) => ({
    id: "demo-" + c.id,
    title: "Possible: " + (c.name || c.id),
    state: "latent",
    demo: true,
    claiming_clusters: [c.id],
  }));
}

// The possibles tile's sub-line, by precedence: demo > pending review > state.
function possibleSub(p) {
  if (p.demo) return "demo";
  if (isUndisposedDerived(p)) return "pending review";
  return p.state || "";
}

// Edge class for a cluster->possible claim (the distinct-class rule):
// demo => synthesized; undisposed derived => inferred; else indexed.
function possibleEdgeClass(p) {
  if (p.demo) return "synthesized";
  if (isUndisposedDerived(p)) return "inferred";
  return "indexed";
}

// One wheel-item list per wheel key, derived from the snapshot collections.
function buildItems({ documents, clusters, possibles, stagedTopics, active, archived }) {
  return {
    documents: documents.map((d) => ({
      id: d.id, label: basename(d.id), sub: d.status || "", ref: d,
    })),
    clusters: clusters.map((c) => ({
      id: c.id, label: c.name || c.id,
      sub: (c.tallies?.document_links || 0) + " docs", ref: c,
    })),
    possibles: possibles.map((p) => ({
      id: p.id, label: p.title || p.id,
      sub: possibleSub(p),
      demo: !!p.demo, derivedPending: isUndisposedDerived(p), ref: p,
    })),
    staged: stagedTopics.map((t) => ({
      id: t.staging_id, label: t.staging_id,
      sub: ((t.files || []).length) + " files", ref: t,
    })),
    active: active.map((c) => ({
      id: c.id, label: c.id, sub: ((c.files || []).length) + " files", ref: c,
    })),
    archived: archived.map((c) => ({
      id: c.id, label: c.id, sub: ((c.files || []).length) + " files", ref: c,
    })),
  };
}

// Every cross-wheel edge, resolved through the per-wheel id indexes.
function buildEdges({ clusters, possibles, changes, index, changeWheel }) {
  const edges = [];
  function link(fromKey, fromId, toKey, toId, cls) {
    const fi = index[fromKey]?.get(fromId);
    const ti = index[toKey]?.get(toId);
    if (fi === undefined || ti === undefined) return;
    edges.push({ from: [fromKey, fi], to: [toKey, ti], cls });
  }
  // documents -> clusters: the Topics-derived member edges (indexed).
  for (const c of clusters) {
    for (const e of c.document_edges || []) {
      link("documents", e.document, "clusters", c.id, "indexed");
    }
  }
  // clusters -> possibles: many-to-many claims, class-coded.
  for (const p of possibles) {
    const cls = possibleEdgeClass(p);
    for (const cid of p.claiming_clusters || []) {
      link("clusters", cid, "possibles", p.id, cls);
    }
  }
  // possibles -> staged: the organize-gate pick edge (a pick is a human act;
  // a demo possible never carries one).
  for (const p of possibles) {
    const sid = p.pick?.staging_id;
    if (sid) link("possibles", p.id, "staged", sid, "indexed");
  }
  // clusters -> staged: the lineage staged_picks (topic-matched progression).
  for (const c of clusters) {
    for (const sid of c.lineage?.staged_picks || []) {
      link("clusters", c.id, "staged", sid, "indexed");
    }
  }
  // staged -> active/archived: the change's recorded origin staging id.
  for (const c of changes) {
    if (c.origin_staging_id) {
      link("staged", c.origin_staging_id, changeWheel.get(c.id), c.id, "indexed");
    }
  }
  return edges;
}

// Per-item total degree (the tile's degree pill) + adjacency for alignment.
function buildDegreesAndAdjacency(items, edges) {
  const degrees = {};
  for (const key of WHEEL_KEYS) degrees[key] = items[key].map(() => 0);
  const adjacency = new Map(); // `${key}:${i}` -> Map(otherKey -> Set(idx))
  function adj(aKey, ai, bKey, bi) {
    const k = aKey + ":" + ai;
    if (!adjacency.has(k)) adjacency.set(k, new Map());
    const byWheel = adjacency.get(k);
    if (!byWheel.has(bKey)) byWheel.set(bKey, new Set());
    byWheel.get(bKey).add(bi);
  }
  for (const e of edges) {
    const [fk, fi] = e.from;
    const [tk, ti] = e.to;
    degrees[fk][fi] += 1;
    degrees[tk][ti] += 1;
    adj(fk, fi, tk, ti);
    adj(tk, ti, fk, fi);
  }
  return { degrees, adjacency };
}

export function buildWheelModel(snapshot) {
  const s = snapshot || {};
  const documents = s.documents || [];
  const clusters = s.clusters || [];
  const realPossibles = s.possibles || [];
  const stagedTopics = s.staged_topics || [];
  const changes = s.changes || [];

  const demoMode = realPossibles.length === 0;
  const possibles = demoMode ? synthesizeDemoPossibles(clusters) : realPossibles;

  const active = changes.filter((c) => c.status === "active");
  const archived = changes.filter((c) => c.status === "archived");

  const items = buildItems({ documents, clusters, possibles, stagedTopics, active, archived });

  const index = {};
  for (const key of WHEEL_KEYS) {
    index[key] = new Map(items[key].map((it, i) => [it.id, i]));
  }
  const changeWheel = new Map();
  active.forEach((c) => changeWheel.set(c.id, "active"));
  archived.forEach((c) => changeWheel.set(c.id, "archived"));

  const edges = buildEdges({ clusters, possibles, changes, index, changeWheel });
  const { degrees, adjacency } = buildDegreesAndAdjacency(items, edges);

  const wheels = WHEEL_KEYS.map((key) => ({
    key, label: WHEEL_LABELS[key], items: items[key], degrees: degrees[key],
  }));
  return { wheels, edges, adjacency, demoMode };
}

// The connections of one focused item, grouped per wheel:
// { wheelKey: [itemIndex, ...] } (sorted). Used for the elastic alignment,
// the teal linked-tile edging, and the focused tile's per-class chips.
export function connectionsOf(model, wheelKey, itemIndex) {
  const byWheel = model.adjacency.get(wheelKey + ":" + itemIndex);
  const out = {};
  if (!byWheel) return out;
  for (const [key, set] of byWheel) out[key] = [...set].sort((a, b) => a - b);
  return out;
}

// ---- second-degree connections (Brett 2026-07-25: always-on second-degree,
// dimmed) ------------------------------------------------------------------
//
// Brett's ruling (2026-07-25, live): when a tile is focused, the wheel
// ADDITIONALLY shows its SECOND-degree connections — always on, dimmed — so
// e.g. focusing a draft document that links 15 clusters also shows those
// clusters' OTHER member documents (and generally: every item one hop beyond
// the focused item's direct links). This walks `model.adjacency` exactly one
// hop past `connectionsOf`, from each first-degree item — it never invents a
// relation (the file-header contract: the wheel consumes MATERIALIZED edges
// only), it only follows the SAME adjacency the first degree already reached,
// one link further.
//
// Returns the connectionsOf shape `{ wheelKey: [itemIndex, ...] }` (sorted,
// deduped — a second-degree item reached through several first-degree paths
// appears once), PLUS an `edges` array for the renderer's dimmed connectors:
// each entry is `{ from: [wheelKey, itemIndex], to: [wheelKey, itemIndex] }`,
// the REAL graph edge from a first-degree item to its second-degree
// neighbour — never from the focused tile itself, matching how the
// adjacency was actually walked. A second-degree item reached via several
// distinct first-degree items keeps one edge per real path (edges are not
// deduped the way the index lists are — each is a genuine materialized
// relation). Both the focused item and every first-degree item are excluded
// from the second-degree result, whichever wheel they land in.
export function secondDegreeOf(model, wheelKey, itemIndex) {
  const first = connectionsOf(model, wheelKey, itemIndex);
  const excluded = new Set([wheelKey + ":" + itemIndex]);
  for (const [key, idxs] of Object.entries(first)) {
    for (const i of idxs) excluded.add(key + ":" + i);
  }
  const sets = {}; // wheelKey -> Set(itemIndex)
  const edges = [];
  const seenEdge = new Set();
  for (const [fromKey, idxs] of Object.entries(first)) {
    for (const fromIdx of idxs) {
      const byWheel = model.adjacency.get(fromKey + ":" + fromIdx);
      if (!byWheel) continue;
      for (const [toKey, set] of byWheel) {
        for (const toIdx of set) {
          const tag = toKey + ":" + toIdx;
          if (excluded.has(tag)) continue; // the focus itself, or already first-degree
          (sets[toKey] || (sets[toKey] = new Set())).add(toIdx);
          const edgeTag = fromKey + ":" + fromIdx + ">" + tag;
          if (seenEdge.has(edgeTag)) continue;
          seenEdge.add(edgeTag);
          edges.push({ from: [fromKey, fromIdx], to: [toKey, toIdx] });
        }
      }
    }
  }
  const out = {};
  for (const key of WHEEL_KEYS) {
    if (sets[key]) out[key] = [...sets[key]].sort((a, b) => a - b);
  }
  const order = (k) => WHEEL_KEYS.indexOf(k);
  edges.sort((a, b) =>
    order(a.from[0]) - order(b.from[0]) || a.from[1] - b.from[1] ||
    order(a.to[0]) - order(b.to[0]) || a.to[1] - b.to[1]);
  out.edges = edges;
  return out;
}

// ---- gathering: first + second degree fold into one reel window (Brett
// 2026-07-25) --------------------------------------------------------------
//
// Brett's dogfood ruling (2026-07-25, live): a focused tile's wheel-GATHERING
// — the spin/reorder + elastic alignment that brings a linked wheel's tiles
// into the visible window — now ALSO folds in that wheel's SECOND-degree tiles,
// so first- and second-degree tiles come to rest NEAR EACH OTHER in the reel
// window. Before this, only first-degree tiles (`connectionsOf`) drove the
// reorder/alignment; a wheel reached ONLY at second degree (e.g. the documents
// wheel from a focused STAGED topic, whose docs hang off its linked clusters)
// stayed put while its dimmed connectors dangled off-screen. Now it spins.
//
// PRIORITY (the ruling's judgement guidance): first-degree tiles keep priority
// — the wheel POSITIONS on them (`align`) so they land nearest the focus line,
// and second-degree tiles gather AROUND/behind them. The full `gather` set is
// what the reorder seats contiguously (so the whole neighbourhood is packed
// into as few reel slots as possible); a wheel with NO first-degree link
// positions on its second-degree set instead, so it still comes into view.
//
// Returns `{ wheelKey: { first, second, gather, align } }` for every OTHER
// wheel the focus reaches (the focus wheel's own key is naturally skipped by
// the caller). All four are sorted, deduped index lists:
//   first    the first-degree indices (connectionsOf) — priority
//   second   the second-degree indices (secondDegreeOf) not already first
//   gather   first ∪ second — the set the reorder packs contiguously
//   align    first when the wheel has any, else second — the set the wheel
//            positions on, so first-degree tiles rest on the line
// This invents no relation: it is a pure union of the two existing adjacency
// walks, so it consumes only MATERIALIZED edges (the file-header contract).
// No cap: a hub focus with a large gather set relies on the SAME banding/
// parking the reorder already applies to large first-degree sets — the block
// is seated contiguously and the reel's own edge-fade retires the overflow.
export function gatherOf(model, wheelKey, itemIndex) {
  const first = connectionsOf(model, wheelKey, itemIndex);
  const second = secondDegreeOf(model, wheelKey, itemIndex);
  const out = {};
  for (const key of WHEEL_KEYS) {
    const f = first[key] || [];
    const fSet = new Set(f);
    const s = (second[key] || []).filter((i) => !fSet.has(i));
    if (!f.length && !s.length) continue;
    const gather = [...f, ...s].sort((a, b) => a - b);
    out[key] = { first: [...f], second: s, gather, align: f.length ? [...f] : s };
  }
  return out;
}

// ---- elastic alignment target (the round-2 refinement that locked the spec)
//
// A wheel's POSITION p means the tile at fractional index p sits on the brass
// focus line; a linked tile i then rests at offset (i - p) steps. The soft
// turn rests linked tiles BALANCED around the centre, never dead on it — a
// tile sitting exactly on the line collapses its thread into a flat line.
// Ported VERBATIM from the locked prototype's `balancedTarget` (THE WHEEL
// mockup, Brett-approved 2026-07-16): a single linked tile parks ~0.8 step
// off-centre (below, unless it sits too near the top edge); a group rests on
// its centroid, nudged 0.45 step AWAY from the nearest linked tile when that
// tile would land within 0.35 of the line. Pure and deterministic —
// unit-tested from Python.
export function alignTarget(linkedIndices) {
  const idxs = (linkedIndices || []).filter((i) => Number.isFinite(i));
  if (!idxs.length) return null; // no pull: the wheel keeps its position
  if (idxs.length === 1) {
    const i = idxs[0];
    return i >= 0.8 ? i - 0.8 : i + 0.8;
  }
  // Span midpoint, not centroid (Brett-approved delta 2026-07-23): the
  // midpoint maximises how much of the linked SPAN fits the visible window,
  // so banded tiles come into view rather than clustering the average.
  let c = (Math.min(...idxs) + Math.max(...idxs)) / 2;
  const near = idxs.reduce((a, b) => (Math.abs(b - c) < Math.abs(a - c) ? b : a));
  if (Math.abs(near - c) < 0.35) c += near >= c ? -0.45 : 0.45;
  return c;
}

// Draw-distance for a LINKED tile on a pulled wheel (Brett-approved
// 2026-07-23, band tightened 2026-07-24): within ~1.8 steps of the line the
// reel geometry is verbatim; beyond it the tile parks on a tanh curve capped
// at ~2.5 steps — INSIDE the edge-fade band, so the outermost reel rows keep
// their fade-off and the 3D cylinder read. Order preserved; parked links stay
// visible, threaded, clickable.
export function linkedDrawDistance(d) {
  const ad = Math.abs(d);
  if (ad <= 1.8) return d;
  return Math.sign(d) * (1.8 + Math.tanh((ad - 1.8) * 0.35) * 0.7);
}

function clamp(v, lo, hi) {
  return Math.min(hi, Math.max(lo, v));
}

// The permutation seating `linkedIdxs` in consecutive slots as close to
// `mid` as the range allows; remaining items keep their relative order.
// (Brett 2026-07-24: when a focus links MANY tiles in one wheel the parking
// curve above stacked them on top of each other, so the pulled wheel
// REARRANGES instead — linked items take consecutive display slots at the
// centre; everything else fills the leftover slots in original order.)
// Returns the permutation both ways: sBy (item index -> display slot) and
// iAt (its inverse), plus the block's low slot and size.
export function computeReorder(n, linkedIdxs, mid) {
  const L = [...linkedIdxs].filter((i) => i >= 0 && i < n).sort((a, b) => a - b);
  const k = L.length;
  const blockLo = clamp(Math.round(mid) - Math.floor((k - 1) / 2),
    0, Math.max(0, n - k));
  const sBy = new Map(), iAt = new Map();
  L.forEach((idx, r) => { sBy.set(idx, blockLo + r); iAt.set(blockLo + r, idx); });
  let s = 0;
  for (let idx = 0; idx < n; idx++) {
    if (sBy.has(idx)) continue;
    while (s >= blockLo && s < blockLo + k) s++;
    sBy.set(idx, s); iAt.set(s, idx); s++;
  }
  return { sBy, iAt, blockLo, k };
}

// ---- the expanded tile: gesture reducer + per-wheel action table ---------------
//
// The EXPAND gesture (Brett 2026-07-25) EXTENDS the locked click gesture rather
// than replacing it: clicking an unfocused tile focuses it exactly as before
// (focus still TRANSFERS across wheels), while clicking the tile that is
// ALREADY focused AND seated on the line expands it IN PLACE so its per-wheel
// actions are reachable inside the tile instead of in the badge rail. At most
// ONE tile is expanded across the whole deck.
//
// The reducer is PURE so the trigger matrix is unit-tested from Python rather
// than re-read out of the DOM. Events:
//   { type: "tile", key, i, centred }  a click (or Enter/Space) on one tile
//   { type: "spin", key }              a user spin of that wheel
//   { type: "collapse" }               Escape · focus change · reorder
//                                      choreography · paging · teardown
// `current` and the return value are both `{ key, i } | null`.
export function nextExpanded(current, event) {
  const ev = event || {};
  const at = current && Number.isFinite(current.i) ? current : null;
  if (ev.type === "tile") {
    if (at && at.key === ev.key && at.i === ev.i) return null; // second click collapses
    if (!ev.centred) return null;              // any other tile: plain focus
    return { key: ev.key, i: ev.i };           // the focused centre tile expands
  }
  if (ev.type === "spin") return at && at.key === ev.key ? null : at;
  if (ev.type === "collapse") return null;
  return at;                                   // unknown event: state untouched
}

export function isExpandedTile(expanded, key, i) {
  return !!expanded && expanded.key === key && expanded.i === i;
}

// THE extension point for the expanded tile's action row. Adding a per-wheel
// verb is ONE row here plus ONE entry in wheel.js's ACTION_MOUNTERS (the DOM +
// transport side deliberately stays out of this pure module).
//   id       the mounter key, and the stable name the tests assert on
//   label    the row's fallback label (the mounter owns the real chrome)
//   visible(item, env)  PURE predicate over the wheel item and the session env
//     env = { gate:        the loopback gate capability is live,
//             commissioned: this item was already commissioned this session,
//             applied:     a verdict applied to this item this session | null,
//             notebook:    the loopback NotebookLM action capability is live }
// Rows sit in FUNNEL order (documents -> \u2026 -> archived), the order the deck
// itself reads in. Verbs with no `visible` predicate are READ-ONLY navigation /
// read verbs: they carry no gate, so they are offered on the deployed static
// image too (where the /source pass-through simply 404s and the target surface
// degrades with its own inline message, exactly as the viewer already does).
//
// The NotebookLM verb stays SET-LEVEL (Brett 2026-07-25): it is the EXISTING
// "Open in NotebookLM" action (POST /actions/notebook) surfaced on the wheels
// whose tiles carry a document SET, and nothing more \u2014 no new tile kind, no new
// backend. Its capability is its OWN (`env.notebook`, the /capabilities probe),
// not the gate's, and it maps 1:1 to notebook_action.py's TILE_KINDS:
//   clusters -> "cluster"   staged -> "staged"   active -> "proposal"
// documents (a single doc, not a set) and archived ("the action is for live
// governance material") are excluded BY DESIGN and grow no row here.
const notebookRow = {
  id: "notebook",
  label: "\u25c7 notebook",
  visible: (item, env) => !!env.notebook,
};

// The STAGING WORKBENCH verb (add-staging-workbench design D6): a full-screen
// read-only surface scoped to ONE topic-bearing tile \u2014 a cluster, a possible, or
// a staged topic. It carries NO `visible` predicate, exactly like `read` /
// `lens` / `canvas` / `packet` / `landed`, because it writes NOTHING: gating a
// read verb on a write capability would hide it from every viewer of the hosted
// dashboard, which is precisely the audience that most needs a read-only
// surface. So it is offered on the deployed static image too, where the
// content-dependent `outline` panel degrades inline like the viewer already
// does.
//
// ONE row, shared by the three topic-bearing wheels \u2014 the wheels whose tiles are
// NOT topic-bearing (documents \u00b7 active \u00b7 archived) grow nothing.
//
// NAMING: the id is `workbench` because that is the mounter key and Brett's
// user-facing name for the verb is "open workbench". It has nothing to do with
// the promoted capability's WORKBENCH REFERENCE SETS (`ideation/workbench/`
// manifests, scripts/ideation_dashboard/workbench.py) \u2014 see design D5; the two
// senses are deliberately kept apart and this verb persists nothing.
const workbenchRow = {
  id: "workbench",
  label: "\u25a3 open workbench",
};

// 011 add-wheel-action-verbs \u2014 the gate-capability shape every commissioning
// row shares. `commissioned` is resolved PER VERB by `actionsFor` (see
// `commissionedFor`), so this literal shape means "this verb, this tile, this
// session". A refused dispatch never sets it, so the verb stays offered.
const gatedAndNotYetActed = (item, env) => !!env.gate && !env.commissioned;

// The possibles column's client-side PROMOTABILITY approximation (FR-010a).
// Computed only from facts the snapshot ALREADY projects onto a tile, so no
// snapshot contract grows for this feature (NG-011):
//   * `state` is the projected register state \u2014 only `latent` is promotable;
//   * `derivedPending` is the item builder's undisposed-derived flag, which
//     already treats a `deferred` verdict as undisposed;
//   * `demo` marks a synthesized honesty-rule placeholder with no register
//     entry at all.
// This is an APPROXIMATION. The engine re-reads the pinned checkout and is
// authoritative (FR-023): a stale tile may offer a verb the engine refuses.
// The register state lives on the tile item's `ref` (the projected snapshot
// possible) — NOT at the top level. The item builder above emits
// `{id, label, sub, demo, derivedPending, ref}`, and reading `item.state`
// silently yields undefined, which made this predicate permanently false and
// hid `promote-to-staging` from the real dashboard entirely. Found by driving
// the page, not by unit test, because the unit fixtures had invented a flat
// item shape (2026-08-02).
const tileState = (item) => item?.ref?.state;

const isPromotableTile = (item) =>
  tileState(item) === "latent" && !item?.derivedPending && !item?.demo;

// Has a human recorded a CLOSING verdict on this possible?
//
// `research-brief` is a PRE-VERDICT verb in the view: FR-032/FR-018a scope its
// visibility to an UNDISPOSED possible — "legal before disposition; the view
// hides it once disposed". The ENGINE stays permissive on purpose (clarify
// Q22's engine-permissive / view-tidy split), so this is a view rule only and
// a route call on a disposed possible is still legal.
//
// `deferred` does NOT close the window: `isUndisposedDerived` above already
// rules that a deferred verdict "keeps it awaiting", and the same reading holds
// here. Only an accept or a reject ends the pre-verdict period. A possible with
// no disposition recorded at all — every human-authored one — is undisposed.
const hasClosingVerdict = (item) => {
  const outcome = item?.ref?.derivation?.human_disposition?.outcome;
  return !!outcome && outcome !== "deferred";
};

export const WHEEL_ACTIONS = {
  documents: [{
    id: "read",
    label: "\u25a4 read",
  }],
  clusters: [
    { id: "lens", label: "\u25ce lens" },
    { id: "canvas", label: "\u25a6 canvas" },
    {
      // commissions a CLUSTER-SCOPED run of the ratified derivation lane. The
      // console derives nothing: it records who asked, and the lane's own
      // contract (ai-derived, pending_review, human disposition) is unchanged.
      id: "derive-possibles",
      label: "\u2726 derive possibles",
      visible: gatedAndNotYetActed,
    },
    notebookRow,
    workbenchRow,
  ],
  // The possibles wheel's FIRST table row: its dispose verbs live in the badge
  // rail's tray (a possible is disposed, not worked), but a possible IS
  // topic-bearing \u2014 its cited evidence and its claiming clusters' members are a
  // document set at a scope \u2014 so the read-only workbench applies to it.
  possibles: [
    {
      // commissions the organization of an ACCEPTED possible into a staging
      // fragment. Offered only when the tile looks promotable; the engine
      // re-checks the register and is the authority.
      id: "promote-to-staging",
      label: "▲ promote to staging",
      visible: (item, env) => gatedAndNotYetActed(item, env) && isPromotableTile(item),
    },
    {
      // commissions a PRE-VERDICT evidence brief. The view hides it once the
      // possible is disposed; the ENGINE deliberately carries no state guard at
      // all (FR-018a), so engine-permissive / view-tidy is intentional here and
      // the two must not be conflated.
      id: "research-brief",
      label: "✻ research brief",
      visible: (item, env) => gatedAndNotYetActed(item, env)
        && !item?.demo && !hasClosingVerdict(item)
        && (tileState(item) === "latent" || !!item?.derivedPending),
    },
    workbenchRow,
  ],
  staged: [
    // the SAME read verb as the documents wheel (one id, one label, one mounter):
    // on a staged tile it opens the topic's PRIMARY fragment
    // (`primaryFragmentPath`), the file whose text the expanded tile also
    // summarises. Read-only, so it carries no gate.
    { id: "read", label: "\u25a4 read" },
    {
      id: "propose",
      label: "\u25b6 draft proposal",
      // add-propose-verb: the same capability gate as the dispose tray, and it
      // retires for the session once the commission is recorded.
      visible: (item, env) => !!env.gate && !env.commissioned,
    },
    notebookRow,
    workbenchRow,
  ],
  active: [
    // review the proposal packet: the change's own files, grouped by
    // `packetGroups`, each one a jump into the read-only viewer. Read-only, so no
    // gate \u2014 the active wheel now has a verb even on the deployed static image.
    { id: "packet", label: "\u25a9 packet" },
    {
      // sends the proposal back to staging. PLAN + RECORD only \u2014 the dashboard
      // never moves a file; the corpus transition is a separate, deliberately
      // human-run execution of the recorded plan.
      //
      // `active` ONLY. Archived tiles also carry a change id, but the demotion
      // planner refuses any change that is not `active`, so the column choice
      // is enforced by the engine rather than by styling.
      //
      // Retirement matters more here than anywhere else: demote carries NO
      // engine-side duplicate guard, so this is the only thing standing between
      // an accidental double-click and a second full artifact set.
      id: "demote",
      label: "\u25c0 demote",
      visible: gatedAndNotYetActed,
    },
    notebookRow,
  ],
  archived: [{
    id: "landed",
    label: "\u2713 landed",
  }],
};

// THE TABLE/VIEW ENVIRONMENT SEAM (011 FR-033b; add-wheel-action-verbs task
// 3.1). Session retirement is per (VERB, TARGET), not per tile: with two
// commission verbs on the possibles column, a tile-wide flag would retire both
// when either fired, contradicting the (verb, target) duplicate rule.
//
// The VIEW supplies `env.commissioned` as a per-verb lookup; `actionsFor`
// resolves it to a plain boolean for each row BEFORE that row's predicate runs.
// So every row keeps the literal `!!env.gate && !env.commissioned` shape and
// simply means "THIS verb's act is recorded for this tile this session".
//
// Backward-compatible on purpose: a plain boolean keeps its old tile-wide
// meaning, so `propose` — the only verb on its column — is unaffected, as is
// every pre-existing caller and test.
function commissionedFor(value, verbId) {
  if (value == null || value === false) return false;
  if (value === true) return true;                  // legacy: tile-wide
  if (typeof value === "function") return !!value(verbId);
  if (value instanceof Set) return value.has(verbId);
  if (typeof value === "object") return !!value[verbId];
  return !!value;
}

// The action descriptors an expanded tile shows, in table order.
export function actionsFor(wheelKey, item, env) {
  if (!item) return [];
  const e = env || {};
  return (WHEEL_ACTIONS[wheelKey] || [])
    .filter((a) => !a.visible
      || a.visible(item, { ...e, commissioned: commissionedFor(e.commissioned, a.id) }))
    .map((a) => ({ id: a.id, label: a.label }));
}

// Is a MOUNTED action row out of date against what the table now offers?
//
// The wheel's redraw used to leave any already-mounted row completely alone, so
// a mounter's own post-success state survived the redraw. That preserved the
// right things (an open reason form, a control re-enabled after a refusal) and
// the wrong one: a RETIRED verb stayed on screen as a disabled control, when
// FR-033 requires retirement to REMOVE the row entry.
//
// So the redraw reconciles instead of skipping, and this is the decision it
// asks. A SET comparison, deliberately: order is the table's business, and
// rebuilding on a reorder would throw away form/focus state for nothing.
export function actionRowIsStale(mountedIds, desiredIds) {
  const mounted = new Set(mountedIds || []);
  const desired = new Set(desiredIds || []);
  if (mounted.size !== desired.size) return true;
  for (const id of desired) if (!mounted.has(id)) return true;
  return false;
}

// The expanded tile's magnification: strictly MORE than the focused centre
// tile's 1.35 (see tileScale) so expanding always reads as growth. Its HEIGHT
// growth lives in CSS (.wheeltile.wheelexpanded) — wheel.js places the box by
// its centre, so the height is not part of the geometry math here.
export const EXPANDED = { scale: 1.38 };

// ---- the archived wheel's "landed" summary (pure parser) ----------------------
//
// WHAT LANDED from a realized change is not in the snapshot: the snapshot
// carries the archived change's FILE LIST, and the requirements themselves live
// in that change's spec-delta files. The `landed` verb reads those files through
// the read-only `/source/<path>` pass-through (wheel.js owns the transport) and
// hands the TEXT to this pure parser, which extracts the OpenSpec delta shape:
// `### Requirement: <title>` headings under a `## ADDED|MODIFIED|REMOVED
// Requirements` section. Nothing is inferred from prose — a heading outside a
// declared delta section, or inside a fenced example, is not a landed
// requirement.
export const LANDED_KINDS = ["ADDED", "MODIFIED", "REMOVED"];

const DELTA_SECTION_RE = /^##\s+(ADDED|MODIFIED|REMOVED)\s+Requirements\s*$/;
const OTHER_HEADING_RE = /^#{1,2}\s+/;
const REQUIREMENT_RE = /^###\s+Requirement:\s*(\S.*?)\s*$/;
const FENCE_RE = /^\s*(?:```|~~~)/;
// A change folder's spec delta, by the OpenSpec change-folder convention
// (`.../specs/<capability>/spec.md`) — the same shape explorer.js groups under
// "spec deltas".
const DELTA_PATH_RE = /(?:^|\/)specs\/([^/]+)\/spec\.md$/;

export function isSpecDeltaPath(path) {
  return DELTA_PATH_RE.test(String(path || ""));
}

// The spec-delta subset of a change item's `files` — the ONLY paths the landed
// verb fetches (proposal/design/tasks/supporting docs are never read).
export function specDeltaPaths(files) {
  return (files || []).filter((path) => isSpecDeltaPath(path));
}

function capabilityOf(path) {
  const m = DELTA_PATH_RE.exec(String(path || ""));
  return m ? m[1] : "";
}

// `files` is a list of `{ path, text }` pairs (the fetched delta files, in
// snapshot order). Returns
//   { files: [parsed path, ...],
//     groups: { ADDED: [req], MODIFIED: [req], REMOVED: [req] },
//     total }
// where req = { title, capability, path }. Non-delta paths and non-string bodies
// are IGNORED rather than guessed at, so a malformed or partial fetch yields a
// smaller honest summary instead of a wrong one.
export function landedFromDeltas(files) {
  const groups = {};
  for (const kind of LANDED_KINDS) groups[kind] = [];
  const parsed = [];
  for (const file of files || []) {
    const path = file?.path;
    const text = file?.text;
    if (!isSpecDeltaPath(path) || typeof text !== "string") continue;
    parsed.push(String(path));
    const capability = capabilityOf(path);
    let kind = null;
    let fenced = false;
    for (const line of text.split(/\r?\n/)) {
      if (FENCE_RE.test(line)) { fenced = !fenced; continue; }
      if (fenced) continue;
      const section = DELTA_SECTION_RE.exec(line);
      if (section) { kind = section[1]; continue; }
      // any other h1/h2 ends the delta section (a following requirement heading
      // would belong to that other section, not to a delta)
      if (OTHER_HEADING_RE.test(line)) { kind = null; continue; }
      const req = REQUIREMENT_RE.exec(line);
      if (req && kind) groups[kind].push({ title: req[1], capability, path: String(path) });
    }
  }
  const total = LANDED_KINDS.reduce((n, kind) => n + groups[kind].length, 0);
  return { files: parsed, groups, total };
}

// ---- the staged wheel: fragment path + 3-line summary (pure) -------------------
//
// A staged topic tile carries the topic's FILE LIST (snapshot `staged_topics[].
// files`), not its text. The expanded tile's summary and its `read` verb both
// need ONE of those files — the topic's PRIMARY fragment, the feat-spec-shaped
// document the staging folder is named for. Selection is deterministic and
// path-only (never content-sniffed):
//   1. the markdown file whose basename is `<staging_id>.md`
//   2. else the SHALLOWEST markdown file (a topic-root fragment beats an
//      `openspec/` draft, which is a proposal in progress, not the topic)
//   3. else nothing — the caller then offers no summary and a disabled verb
export function primaryFragmentPath(stagingId, files) {
  const mds = (files || []).filter((p) => /\.md$/i.test(String(p)));
  if (!mds.length) return "";
  const named = stagingId ? basename(String(stagingId)) + ".md" : "";
  const exact = named ? mds.find((p) => basename(p).toLowerCase() === named.toLowerCase()) : null;
  if (exact) return String(exact);
  let best = String(mds[0]);
  let bestDepth = best.split("/").length;
  for (const p of mds.slice(1)) {
    const depth = String(p).split("/").length;
    if (depth < bestDepth) { best = String(p); bestDepth = depth; }
  }
  return best;
}

// The expanded staged tile's summary, extracted from the primary fragment's TEXT
// (wheel.js owns the /source read; this is the pure extraction). The tile already
// shows the topic id, so the summary must be the topic's own SUBSTANCE:
//   * a leading YAML frontmatter block is stripped
//   * markdown headings are SKIPPED (the h1 restates the title)
//   * a controlled header block (`Status:`/`Kind:`/`Summary:`/`Topics:` — the
//     document-lifecycle header the staging fragments carry) yields its
//     `Summary:` field when it has one, and is otherwise skipped as metadata
//   * failing that, the first meaningful PARAGRAPH is used verbatim
// Whitespace collapses to one line of prose (the tile clamps it to three display
// lines in CSS) and inline markdown emphasis is unwrapped. Never throws: a blank,
// non-string, or heading-only fragment yields "".
const SUMMARY_MAX = 240;
const FRONTMATTER_RE = /^---\s*$/;
const HEADING_RE = /^\s{0,3}#{1,6}\s+/;
const SETEXT_RE = /^\s{0,3}(?:=+|-{2,})\s*$/;
const HEADER_FIELD_RE = /^([A-Z][A-Za-z0-9 ()/&'’-]{0,40}):\s*(.*)$/;

function tidySummary(text) {
  const flat = String(text)
    .replace(/\s+/g, " ")
    .replace(/`+/g, "")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/\*([^*]+)\*/g, "$1")
    .trim();
  if (flat.length <= SUMMARY_MAX) return flat;
  const cut = flat.slice(0, SUMMARY_MAX);
  const space = cut.lastIndexOf(" ");
  return (space > SUMMARY_MAX * 0.6 ? cut.slice(0, space) : cut).trimEnd() + "…";
}

// A blank-line-separated block of the fragment body, headings and fenced code
// already dropped. Returns [{ lines }] in document order.
function fragmentBlocks(text) {
  const lines = String(text).split(/\r?\n/);
  let start = 0;
  if (lines.length && FRONTMATTER_RE.test(lines[0])) {
    const end = lines.findIndex((l, i) => i > 0 && FRONTMATTER_RE.test(l));
    start = end > 0 ? end + 1 : lines.length; // unterminated frontmatter: no body
  }
  const blocks = [];
  let current = [];
  let fenced = false;
  for (const line of lines.slice(start)) {
    if (FENCE_RE.test(line)) { fenced = !fenced; continue; }
    if (fenced) continue;
    if (!line.trim()) { if (current.length) { blocks.push(current); current = []; } continue; }
    if (SETEXT_RE.test(line)) {
      // an underline turns the line ABOVE it into a heading (or is a thematic
      // break, when nothing sits above): drop that line, keep the rest
      current.pop();
      if (current.length) { blocks.push(current); current = []; }
      continue;
    }
    if (HEADING_RE.test(line)) {
      if (current.length) { blocks.push(current); current = []; }
      continue;                                  // a heading is never summary prose
    }
    current.push(line.trim());
  }
  if (current.length) blocks.push(current);
  return blocks;
}

// The `Summary:` field of a controlled header block, or "" when the block has
// none. A field runs until the next `Key: value` line, so a wrapped Summary
// keeps its continuation lines.
function headerSummary(block) {
  let field = null;
  const parts = [];
  for (const line of block) {
    const m = HEADER_FIELD_RE.exec(line);
    if (m) {
      field = m[1].toLowerCase();
      if (field === "summary" && m[2]) parts.push(m[2]);
      continue;
    }
    if (field === "summary") parts.push(line);
  }
  return parts.join(" ");
}

export function fragmentSummary(text) {
  if (typeof text !== "string" || !text.trim()) return "";
  for (const block of fragmentBlocks(text)) {
    if (HEADER_FIELD_RE.test(block[0])) {
      const summary = headerSummary(block);
      if (summary.trim()) return tidySummary(summary);
      continue;                                  // metadata only: keep looking
    }
    return tidySummary(block.join(" "));
  }
  return "";
}

// ---- the staged wheel: health chrome (pure; add-staging-workbench D10) ---------
//
// A staged topic's snapshot entry MAY carry a `health` aggregate (the generator
// emits it; a PRE-GROWTH snapshot does not). The tile surfaces it at exactly the
// two interaction levels Brett named: a compact tri-state indicator on the
// FOCUSED (centred, first-click) face, and the full block — status, standing
// open items with each blocker document's count, score min/mean, the blockers
// list — on the EXPANDED (second-click) tile. Resting drum faces stay unadorned
// (that is wheel.js's rendering rule; these helpers only shape the data).
//
// VERBATIM, NEVER RECOMPUTED: both helpers read the snapshot's own numbers and
// return null for a topic with no health object, so a pre-growth snapshot shows
// no indicator and no block rather than a client-side reconstruction. And the
// display NEVER GATES — allowing or refusing stays with the server-side
// readiness gate (evaluated LIVE against the checkout), whose refusal message
// is the authoritative account when the snapshot has drifted; nothing here may
// suppress or restate it.

export const HEALTH_STATUSES = ["ready", "developing", "stub"];

// The compact indicator's per-status glyph, legible at drum scale: `ready` a
// filled dot, `developing` a half dot, `stub` a hollow one — shape-coded as
// well as colour-coded, so the tri-state survives any palette.
const HEALTH_GLYPHS = { ready: "●", developing: "◐", stub: "○" };

// The FOCUSED tile face's indicator: { status, glyph, label, title } — or null
// when the snapshot carries no health (pre-growth) or an unknown status (never
// guess a state the contract does not define).
export function healthIndicator(health) {
  const status = health?.status;
  if (!HEALTH_STATUSES.includes(status)) return null;
  const standing = health.standing_open_items;
  const standingNote = Number.isFinite(standing)
    ? " · " + standing + " standing open item" + (standing === 1 ? "" : "s")
    : "";
  return {
    status,
    glyph: HEALTH_GLYPHS[status],
    label: status,
    title: "health: " + status + standingNote,
  };
}

// One blocker as one display line, VERBATIM from the snapshot's own fields —
// the same facts the gate's live refusal cites, so the tile and the refusal can
// never disagree about WHY (design D8). An unknown blocker kind is still shown
// (named, not dropped): hiding a blocker would make the indicator dishonest.
function blockerLine(blocker) {
  const document = blocker?.document || "<unnamed document>";
  if (blocker?.kind === "standing_open_items") {
    const count = blocker.count;
    return document + " — " + count + " standing open item" + (count === 1 ? "" : "s");
  }
  if (blocker?.kind === "below_ready_threshold") {
    return document + " — score " + blocker.score + " < threshold " + blocker.threshold;
  }
  return document + " — blocked (" + (blocker?.kind || "unknown") + ")";
}

// The EXPANDED tile's full health block: null on a pre-growth snapshot, else
// { status, glyph, lines, blockers } for wheel.js to render textContent-only.
// Every number is the snapshot's own; nothing is computed here.
export function healthBlock(health) {
  const indicator = healthIndicator(health);
  if (!indicator) return null;
  return {
    status: indicator.status,
    glyph: indicator.glyph,
    lines: [
      "standing open items: " + health.standing_open_items,
      "doc score min " + health.doc_score_min + " · mean " + health.doc_score_mean,
    ],
    blockers: (health.blockers || []).map(blockerLine),
  };
}

// ---- the active wheel: proposal-packet grouping (pure) -------------------------
//
// The active wheel's `packet` verb reviews a proposal packet: the change's own
// files, grouped the way a reviewer reads them — the three OpenSpec packet
// documents first (in authoring order, labelled by basename), then the spec
// deltas (labelled by the CAPABILITY each targets, since every one of them is
// named `spec.md`), then everything else the folder carries. Paths are shown
// RELATIVE to the change folder when the snapshot records one. Pure: the flyout's
// DOM and the openDoc jump are wheel.js's.
const PACKET_DOCS = ["proposal.md", "design.md", "tasks.md"];

function packetRelative(path, folder) {
  const p = String(path);
  const f = String(folder || "").replace(/\/+$/, "");
  return f && p.startsWith(f + "/") ? p.slice(f.length + 1) : basename(p);
}

export function packetGroups(files, folder) {
  const docs = [], deltas = [], other = [];
  for (const raw of files || []) {
    const path = String(raw);
    const name = packetRelative(path, folder);
    if (PACKET_DOCS.includes(basename(path))) docs.push({ path, name });
    else if (isSpecDeltaPath(path)) deltas.push({ path, name: capabilityOf(path) || name });
    else other.push({ path, name });
  }
  docs.sort((a, b) => PACKET_DOCS.indexOf(basename(a.path)) - PACKET_DOCS.indexOf(basename(b.path)));
  return [
    { label: "packet", files: docs },
    { label: "spec deltas", files: deltas },
    { label: "other files", files: other },
  ].filter((g) => g.files.length);
}

// Spring–damper constants (locked): the user-driven wheel has real inertia;
// pulled wheels trail so the threads visibly drag them.
export const SPRING = {
  driven: { k: 0.020, damping: 0.84 },
  pulled: { k: 0.008, damping: 0.90 },
};

// Reel geometry, ported VERBATIM from the locked prototype: 58px whole-tile
// spacing, a tanh bulge of 15px applied ONLY to the focused wheel, and a
// 6-tile visibility window either side of the focus line.
export const REEL = { spacing: 58, bulge: 15, visible: 6 };

// One tile's rest offset from the focus line at signed distance ``d`` steps
// (the locked prototype's `d*SPACING + tanh(d)*bulge`).
export function tileOffset(d, focused) {
  return d * REEL.spacing + Math.tanh(d) * (focused ? REEL.bulge : 0);
}

// One tile's scale: the FOCUSED wheel magnifies continuously toward 1.35 at
// the centre (`.92 + .43*(1-|d|)`); pulled wheels keep flat .95 tiles.
export function tileScale(d, focused) {
  return focused ? 0.92 + 0.43 * Math.max(0, 1 - Math.abs(d)) : 0.95;
}

// One tile's opacity: solid on the line, fading with distance, floored.
export function tileOpacity(d) {
  const ad = Math.abs(d);
  return ad < 0.5 ? 1 : Math.max(0.22, 0.82 - ad * 0.14);
}

// ---- the rendered box, and what is actually IN the reel window ---------------
// (T092 acceptance sweep, defects 6 and 14. Pure: wheel.js owns the DOM, these
// own the arithmetic, and the node harness can measure both at real scale.)
//
// wheel.js places a tile with `translate(0, ty) scale(sx, sy)` about a CENTRED
// transform-origin, so the rendered box is NOT the element's static box and
// cannot be read off the style. `tileBox` reproduces exactly the two postures
// wheel.js writes:
//
//   resting   ty = y - (H/2)·squash, scale (s, s·squash)
//             -> centre = H/2 + ty, half = (H/2)·s·squash
//   expanded  ty = y, then translateY(-50%) (self-relative, so the growth
//             animates about the drum axis), scale EXPANDED.scale
//             -> centre = y, half = (H/2)·EXPANDED.scale
//
// `y` and `squash` are the cylinder projection's own outputs; `tileH` is the
// tile's UNSCALED CSS height in the current `--wheel-scale`.
export function tileBox({ y, squash = 1, tileH, scale = 1, expanded = false,
  expandedScale = EXPANDED.scale }) {
  const halfBox = tileH / 2;
  if (expanded) {
    const half = halfBox * expandedScale;
    return { centre: y, half, top: y - half, bottom: y + half, translateY: y };
  }
  const translateY = y - halfBox * squash;
  const centre = halfBox + translateY;
  const half = halfBox * scale * squash;
  return { centre, half, top: centre - half, bottom: centre + half, translateY };
}

// Is this box inside the reel window it is drawn in?
//
// DEFECT 6. Each column renders ~31 tiles but the window holds 7: the drum
// places the rest at y = winH/2 + R·sin θ, which for R = winH runs from
// -winH/2 to 3·winH/2, i.e. far outside the box. `.wheelport`'s overflow and
// `.wheelwin`'s clip-path stop them PAINTING and stop the mouse reaching them —
// the sweep's hit test found 9 of 31 reachable — but neither clip touches the
// TAB ORDER, and every one of them kept `tabindex=0`. A keyboard user tabbed
// through 25 tiles whose focus landed somewhere invisible, and 45 Tab presses
// never reached the second of six columns.
//
// So this is the ONE predicate wheel.js drives focusability, `aria-hidden` and
// pointer-events from, and mouse and keyboard cannot disagree about what is
// visible again. A tile past the drum's horizon (`over`) is out whatever its
// box says — it is drawn at opacity 0.
export function inReelWindow(box, winH, over = false) {
  if (over) return false;
  return box.bottom > 0 && box.top < winH;
}

// ---- thread anchors ---------------------------------------------------------
// DEFECT 14a. Threads anchor at the FACING EDGES of the two tiles they join
// (the locked prototype), and wheel.js computed that edge as half the RESTING
// tile width — while the endpoint it was anchoring to is magnified: 1.35x when
// focused, EXPANDED.scale when expanded. So the teal cluster-edge bundle
// started ~37px INSIDE the expanded card, crossing its left border and striking
// through the health line, hiding the first characters of "standing open
// items: 6". The sweep read it as a z-order fault; the geometry says otherwise —
// drive3 found every child inside the tile rect, because the thread is not a
// child. An edge that terminates at the endpoint's REAL edge cannot enter it.
export function threadAnchorX(centreX, goRight, tileW, scale = 1) {
  return centreX + (goRight ? 1 : -1) * (tileW / 2) * scale;
}

// The horizontal scale of one thread endpoint: the expanded box, else the same
// `tileScale` the tile itself is laid out with. One definition, so the anchor
// and the card can never drift apart.
export function endpointScale(d, focusWheel, expanded) {
  return expanded ? EXPANDED.scale : tileScale(d, focusWheel);
}

// ---- the focused tile's badge rail ------------------------------------------
// DEFECT 14b. The rail ("15 clusters") is parked below the focused centre tile
// at `50% + 46px` — correct clearance for the 1.35x focused box, whose bottom
// is at 37.8px — but the next tile on the reel starts at only ~43.7px
// (`tileOffset(1, true)` = 69.4 less its own 25.8px half-box), so the chips land
// on top of a neighbour and cover its sub-line. Reserving the 13px would mean
// moving Brett's locked reel spacing, which this change does not do.
//
// Instead the rail is treated the way an already-precedented collision is: a
// PARKED link "draws on top of whatever tile owns that slot — fade the covered
// tile so the link floats readably instead of colliding". This returns the
// rail's own band so wheel.js can apply that same rule, and the chips gain the
// solid backdrop the expanded posture already gives them. Nothing legible is
// hidden behind chips any more; the covered tile is visibly ceded to the rail.
export const BADGE_RAIL = { offset: 46, height: 13, expandedClearance: 8 };

export function badgeRailBand(winH, scaleF = 1, expandedH = null) {
  const top = winH / 2 + (expandedH === null
    ? BADGE_RAIL.offset * scaleF
    : (expandedH * 0.69 + BADGE_RAIL.expandedClearance) * scaleF);
  return { top, bottom: top + BADGE_RAIL.height * scaleF };
}

// Do two vertical bands overlap? (Bands touching at an edge do not.)
export function bandsOverlap(a, b) {
  return a.bottom > b.top && a.top < b.bottom;
}

// ---- the drum-radius knob ("wheel diameter", settings panel) -----------------
// The cylinder projection's radius is `wheel-window height × factor`. The factor
// is the ONE tunable the settings panel exposes: 0.3 puts the drum's horizon
// inside the window (the classic slot-drum wrap), 1 is the gentle ~±30° wrap
// (Brett's opening spec), 2 flattens back toward the old flat reel. Bounds,
// step, and default live HERE beside the rest of the wheel's pure geometry so
// settings.js, wheel.js, and the pytest node harness read one source of truth.
export const DRUM = { min: 0.3, max: 2.0, step: 0.05, default: 1 };

// One candidate factor, parsed defensively: `raw` may be a URL query value, a
// localStorage string, a number, or absent/corrupt. A candidate COUNTS only when
// it parses to a finite POSITIVE number; a counting candidate is CLAMPED into
// the bounds (`?drum=9` -> 2.0) rather than discarded, so a stale tuning URL
// still renders a legible wheel. Everything else — absent, non-numeric, zero,
// negative — returns null, meaning "no opinion": the next precedence source
// decides.
export function drumCandidate(raw) {
  const v = Number.parseFloat(raw);
  if (!Number.isFinite(v) || v <= 0) return null;
  return Math.min(DRUM.max, Math.max(DRUM.min, v));
}

// Load-time precedence, PURE: an explicit `?drum=` URL param wins (it is the
// compare-by-URL tuning tool), else the saved setting, else the default.
export function drumFactor(urlRaw, storedRaw) {
  const fromUrl = drumCandidate(urlRaw);
  if (fromUrl !== null) return fromUrl;
  const fromStored = drumCandidate(storedRaw);
  return fromStored !== null ? fromStored : DRUM.default;
}

// ---- the cylinder projection itself -----------------------------------------
// THE projection every drum in this app is placed by, lifted out of wheel.js
// unchanged (2026-08-03) when the doc wheel became a second caller. Each wheel
// is a spinning drum seen edge-on whose RADIUS is `winH × drumF`: a tile `d`
// steps from the focus line sits at arc angle θ = arc/R, lands at y = R·sin θ,
// and foreshortens vertically by cos θ, so tiles wrap over the drum's horizon
// instead of sliding a flat list.
//
// It lives here rather than in wheel.js because there are now TWO drums — the
// six-column deck and the docs pane's single-column wheel, which the operator
// asked for as "the same wheel ... at .4 the size of the subpane". Same wheel
// has to mean same arithmetic, or the two drift the first time either is
// tuned; one exported function is what makes that true by construction, and it
// is the first time this projection has been reachable from a test at all.
//
// The arc length is the locked prototype's reel offset INCLUDING the focused
// wheel's tanh bulge (`bulged`) — dropping the bulge here let neighbours
// overlap the magnified centre tile by ~6px.
export function drumProject({ d, bulged = false, winH, drumF, scaleF = 1 }) {
  const R = winH * drumF;
  const theta = (tileOffset(d, !!bulged) * scaleF) / R;
  const t = Math.min(Math.PI / 2, Math.max(-Math.PI / 2, theta));
  return {
    y: R * Math.sin(t),
    squash: Math.max(Math.cos(t), 0.05),
    over: Math.abs(theta) > Math.PI / 2, // past the horizon: hidden
  };
}
