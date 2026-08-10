// STAGING WORKBENCH view-model derivation (openxFactory `add-staging-workbench`,
// design D3/D4/D7; change tasks 4.1). PURE: no DOM, no I/O, no imports — it is
// imported by staging-workbench.js in the browser AND unit-tested from Python
// via node (tests/ideation-dashboard/test_staging_workbench.py), exactly like
// lens-model.js / explorer.js, both of which are copied ALONE into the node
// harness and therefore carry no sibling imports either.
//
// NAMING — two different "workbench"es, deliberately kept apart (design D5):
//   * WORKBENCH REFERENCE SETS are the promoted capability's user-assembled
//     document SETS, persisted as `kind: ideation-workbench` manifests under
//     `ideation/workbench/` by scripts/ideation_dashboard/workbench.py. Nothing
//     in THIS module touches that family.
//   * the STAGING WORKBENCH (this module) is a scoped READ-ONLY view over one
//     already-existing topic-bearing tile. It assembles no set, persists no
//     manifest, and writes nothing.
//
// The whole derivation is a filter over snapshot fields the generator ALREADY
// materializes (cluster `document_edges`, a possible's `supporting_evidence` and
// `claiming_clusters`, a staged topic's `files`, and `documents[].destinations`).
// Nothing is inferred from text, nothing is re-scored, and no signal is
// computed here: `completeness` rides along VERBATIM on each document entry so
// the renderer can only ever display what the generator emitted (design D7 — a
// document the snapshot does not score renders with NO bar, never a zero one).
//
// THE ONE DISTINCTION THAT MATTERS (design D4): a possible's CITED evidence is a
// recorded pin; the member documents of its claiming clusters are an INFERENCE
// from the cluster. They are returned as two separately-labelled sections and
// are kept disjoint, because merging them would silently upgrade an inference
// into evidence.

export const WORKBENCH_KINDS = ["cluster", "possible", "staged"];

// The five completeness signals, in the emission/spec order the `docs` panel
// renders them in. The renderer walks THIS list and skips a signal the snapshot
// does not carry — it never substitutes a zero.
export const SIGNAL_KEYS = [
  "structure", "length", "open_markers", "keyword_coverage", "link_degree",
];

// Per-section chrome. `inherited: true` is what the renderer keys its
// separately-labelled treatment off, so the distinction cannot be lost in the
// DOM either.
//
// `owned: true` is the OTHER distinction, and it is the one a WRITE depends on
// (T092 acceptance sweep, defect 1): whose material is this section? Exactly one
// section holds documents the tile itself owns — a staged topic's own staging
// folder. Everything else is context: a cluster's members and a possible's
// evidence belong to whoever authored them, an inbound `declaring` document
// merely names this topic as a destination, and the two `inherited` sections say
// in their own notes that they are inferred rather than the topic's material.
// `rewritableDocuments` is the one reader, and without this flag the rewrite
// picker offered every one of them — which is how a tile's session came to
// overwrite another topic's staged document.
const SECTION_META = {
  members: {
    label: "cluster documents",
    note: "the cluster's own snapshot document edges",
  },
  cited: {
    label: "cited supporting evidence",
    note: "recorded evidence pins — a governed citation",
  },
  inherited: {
    label: "inherited from claiming clusters",
    note: "membership INFERRED from the claiming clusters — not cited evidence",
    inherited: true,
  },
  folder: {
    label: "topic folder documents",
    note: "the corpus documents that live in this staging folder — the topic's own material",
    owned: true,
  },
  declaring: {
    label: "documents declaring this topic",
    note: "documents whose declared destinations name this staging topic — inbound context",
  },
  // Brett's 2026-07-25 dogfood ruling: a staged topic's docs panel additionally
  // lists the member documents of the topic's LINKED clusters as a THIRD,
  // separately labelled cluster-neighbourhood section — styled like the
  // possible's `inherited` section (the same `inherited: true` flag drives the
  // separated DOM treatment), inferred VIA CLUSTERS and never conflated with the
  // topic's own folder/declaring material. It is context only: it is NOT an
  // input to the topic's health or the readiness gate, which stay folder-scoped.
  neighbourhood: {
    label: "cluster neighbourhood",
    note: "member documents of the topic's linked clusters — inferred via clusters, not the topic's own material",
    inherited: true,
  },
};

export const SECTION_KEYS = Object.keys(SECTION_META);

function asId(value) {
  return value == null ? "" : String(value);
}

// documents[] indexed by BOTH id and path (they are the same string today, but
// the explorer already matches on `path` and the projection is free to diverge).
function buildIndex(snapshot) {
  const byId = new Map();
  for (const d of snapshot?.documents || []) {
    const id = asId(d?.id);
    if (id && !byId.has(id)) byId.set(id, d);
    const path = asId(d?.path);
    if (path && !byId.has(path)) byId.set(path, d);
  }
  return byId;
}

// Order-preserving de-duplicated string list (declared topic vocabularies).
function uniqueStrings(list) {
  const out = [];
  const seen = new Set();
  for (const raw of list || []) {
    const value = asId(raw);
    if (!value || seen.has(value)) continue;
    seen.add(value);
    out.push(value);
  }
  return out;
}

// One document section, in the SNAPSHOT'S OWN order (the generator sorts member
// docs, evidence pins keep their recorded order, `files` is sorted): stable by
// construction, never re-sorted here.
//
// `seen` is shared across a scope's sections, which is what keeps them DISJOINT
// — a cited document never reappears as inherited, and a staged topic's folder
// document never reappears as a destination-declaring one (the generator stamps
// every in-folder document with that destination, so without this the two
// sections would be near-duplicates).
//
// `requireResolved` drops references that are not catalogued corpus documents.
// It is on for a staged topic's `files` (a folder carries manifests and other
// non-documents) and OFF for evidence/edge references, where an unresolvable id
// is a real finding the human should see rather than a row silently dropped.
function buildSection(key, refs, { byId, seen, requireResolved = false }) {
  const meta = SECTION_META[key];
  const documents = [];
  for (const raw of refs || []) {
    const id = asId(raw);
    if (!id || seen.has(id)) continue;
    const doc = byId.get(id) || null;
    if (requireResolved && !doc) continue;
    seen.add(id);
    documents.push({
      id,
      path: asId(doc?.path) || id,
      doc,
      resolved: !!doc,
      // the completeness object VERBATIM (absent on an excluded document and on
      // any pre-growth snapshot) — the renderer's only source for the bar
      completeness: doc?.completeness || null,
    });
  }
  return {
    key,
    label: meta.label,
    note: meta.note,
    inherited: !!meta.inherited,
    // whose material this section holds (T092 defect 1) — carried on the section
    // itself, so a consumer never has to re-derive it from the key
    owned: !!meta.owned,
    documents,
  };
}

// The outline material of a scope, as a (stagingId, file list) pair the caller
// resolves through the wheel's EXISTING `primaryFragmentPath` selector — this
// module deliberately does not re-implement that path rule.
function stagedOutline(topic, from) {
  if (!topic) return null;
  return {
    from,
    stagingId: asId(topic.staging_id),
    files: (topic.files || []).map(asId),
  };
}

// A possible's outline, when the register records a PICK into a staging topic.
// That pick is snapshot-recorded data (the wheel already draws it as an
// `indexed` edge), not an inference — so the possible's outline is that topic's
// fragment. A possible with no pick carries no outline and the panel says so.
function pickedOutline(snapshot, possible) {
  const sid = asId(possible?.pick?.staging_id);
  if (!sid) return null;
  const topic = (snapshot.staged_topics || [])
    .find((t) => asId(t?.staging_id) === sid);
  return stagedOutline(topic, "picked-topic");
}

function finishScope(scope) {
  const documents = [];
  for (const section of scope.sections) documents.push(...section.documents);
  return {
    ...scope,
    documents,
    counts: {
      documents: documents.length,
      scored: documents.filter((row) => !!row.completeness).length,
      unresolved: documents.filter((row) => !row.resolved).length,
      inherited: scope.sections
        .filter((s) => s.inherited)
        .reduce((n, s) => n + s.documents.length, 0),
    },
  };
}

// THE REWRITE PICKER'S OPTION SET (T092 acceptance sweep, defect 1).
//
// `scope.documents` is every section flattened into one list — the right shape
// for a READ (the docs panel, the counts, the outline) and the wrong shape for a
// WRITE. The rewrite picker used it directly, so a staged tile's session was
// offered another topic's staged document, an `ideation/brainstorm/` capture and
// every cluster-neighbourhood row, and submitting one REPLACED it on this tile's
// branch with a gate-action record that read as authorised.
//
// The rule, and it is the route's rule too (`gate_routes.foreign_document_refusal`
// — the picker is UI, the route is the boundary, and they are deliberately the
// same sentence): a session may rewrite the tile's OWN material, plus what it
// CREATED in this session. `created` is the page-lifetime overlay of paths this
// page's creates landed (swb-session.js `createdDocuments`), which is what keeps
// a just-created document editable in the same sitting — including on a
// cluster/possible tile, which owns no folder and therefore inherits nothing.
//
// Unresolved rows are dropped as before: a path with no catalogued document
// behind it is a finding to READ, never a rewrite target.
export function rewritableDocuments(scope, created) {
  const out = [];
  const seen = new Set();
  const push = (path) => {
    const value = asId(path);
    if (!value || seen.has(value)) return;
    seen.add(value);
    out.push(value);
  };
  for (const section of (scope && scope.sections) || []) {
    if (!section.owned) continue;
    for (const row of section.documents || []) if (row.resolved) push(row.path);
  }
  // A created document is rewritable whether or not the snapshot has caught up
  // with it: the create's own response named the path, and the session worktree
  // is where it landed.
  for (const path of created || []) push(path);
  return out;
}

// THE derivation. `kind` is one of WORKBENCH_KINDS; `id` is the cluster id, the
// possible id, or the staging_id. Returns null when the kind is unrecognized or
// the id does not resolve against this snapshot (a stale click after a
// regeneration, or a synthesized demo possible) — the view then states that
// plainly instead of rendering an empty scope as if it were real.
//
//   cluster   its `document_edges` documents
//   possible  its `supporting_evidence` documents, PLUS the member documents of
//             its claiming clusters in a separate `inherited` section
//   staged    the folder's corpus documents, PLUS every document whose
//             `destinations.staged_topics` names the topic, PLUS (Brett's
//             2026-07-25 ruling) the member documents of the topic's LINKED
//             clusters in a separate `neighbourhood` section, deduped against
//             the first two and never conflated with the topic's own material
export function workbenchScope(snapshot, kind, id) {
  const s = snapshot || {};
  const wanted = asId(id);
  if (!wanted) return null;
  const byId = buildIndex(s);
  const seen = new Set();

  if (kind === "cluster") {
    const cluster = (s.clusters || []).find((c) => asId(c?.id) === wanted);
    if (!cluster) return null;
    return finishScope({
      kind, id: wanted, title: cluster.name || wanted, ref: cluster,
      keywords: uniqueStrings(cluster.topics),
      sections: [buildSection("members",
        (cluster.document_edges || []).map((e) => e?.document), { byId, seen })],
      outline: null,
    });
  }

  if (kind === "possible") {
    const possible = (s.possibles || []).find((p) => asId(p?.id) === wanted);
    if (!possible) return null;
    const cited = buildSection("cited",
      (possible.supporting_evidence || []).map((e) => e?.document), { byId, seen });
    const clusterById = new Map(
      (s.clusters || []).map((c) => [asId(c?.id), c]));
    const inheritedRefs = [];
    const keywords = [];
    for (const cid of (possible.claiming_clusters || []).map(asId)) {
      const cluster = clusterById.get(cid);
      if (!cluster) continue;
      for (const edge of cluster.document_edges || []) inheritedRefs.push(edge?.document);
      for (const topic of cluster.topics || []) keywords.push(topic);
    }
    return finishScope({
      kind, id: wanted, title: possible.title || wanted, ref: possible,
      keywords: uniqueStrings(keywords),
      sections: [cited, buildSection("inherited", inheritedRefs, { byId, seen })],
      outline: pickedOutline(s, possible),
    });
  }

  if (kind === "staged") {
    const topic = (s.staged_topics || [])
      .find((t) => asId(t?.staging_id) === wanted);
    if (!topic) return null;
    const folder = buildSection("folder", topic.files || [],
      { byId, seen, requireResolved: true });
    const declaringRefs = (s.documents || [])
      .filter((d) => (d?.destinations?.staged_topics || []).map(asId).includes(wanted))
      .map((d) => asId(d?.id) || asId(d?.path));
    const declaring = buildSection("declaring", declaringRefs, { byId, seen });
    const keywords = [];
    for (const row of folder.documents) {
      for (const topicName of row.doc?.topics || []) keywords.push(topicName);
    }
    // The cluster-neighbourhood section: the SAME clusters->staged adjacency the
    // wheel draws — a cluster whose `lineage.staged_picks` names this topic —
    // then those clusters' member documents. Built LAST so `seen` dedupes it
    // against the folder + declaring sections. Absent entirely when the topic
    // has no linked clusters (rather than an empty labelled section).
    const sections = [folder, declaring];
    const linkedClusters = (s.clusters || [])
      .filter((c) => (c?.lineage?.staged_picks || []).map(asId).includes(wanted));
    if (linkedClusters.length) {
      const neighbourRefs = [];
      for (const cluster of linkedClusters) {
        for (const edge of cluster.document_edges || []) neighbourRefs.push(edge?.document);
      }
      sections.push(buildSection("neighbourhood", neighbourRefs, { byId, seen }));
    }
    return finishScope({
      kind, id: wanted, title: wanted, ref: topic,
      keywords: uniqueStrings(keywords),
      sections,
      outline: stagedOutline(topic, "staged-topic"),
    });
  }

  return null;
}

// The minimal doxBench client projection used for parity with the independent
// server authority. This remains a PRESENTATION projection: the browser may use
// it to label owned/contextual rows, but the server re-derives every path before
// disclosure or Save.
//
// `outlinePathFor` is injected so this import-free module continues to reuse the
// wheel's existing `primaryFragmentPath` rule at composition time instead of
// copying that rule here. The Node parity harness injects the actual wheel
// function as well.
export function doxbenchScopeProjection(snapshot, kind, id, options = {}) {
  const scope = workbenchScope(snapshot, kind, id);
  if (!scope) return null;

  const contextPaths = [];
  const contextSeen = new Set();
  const pushContext = (path) => {
    const value = asId(path);
    if (!value || contextSeen.has(value)) return;
    contextSeen.add(value);
    contextPaths.push(value);
  };
  for (const section of scope.sections || []) {
    for (const row of section.documents || []) {
      if (row.resolved) pushContext(row.path);
    }
  }
  // FR-043 (T107): a session-created document is CONTEXT as well as editable, so
  // it appears here too — appended AFTER the sections, which is where the server
  // appends it (`doxbench_scope._projection`), because the two derivations are
  // compared as ordered lists on the shared fixture. `createdDocuments` is the
  // page's own overlay and this remains PRESENTATION: the server derives its own
  // created record from the session worktree and never reads this one.
  for (const path of options.createdDocuments || []) pushContext(path);

  let outlinePath = null;
  if (scope.outline && typeof options.outlinePathFor === "function") {
    outlinePath = asId(options.outlinePathFor(scope.outline)) || null;
  }
  const editablePaths = rewritableDocuments(scope, options.createdDocuments || []);
  const editableSeen = new Set(editablePaths);
  // T104 F2, byte-for-byte the server's own rule (doxbench_scope._projection --
  // the two derivations are compared as ordered lists on the shared fixture):
  //
  //   * an outline this tile's own scope does not contain is not this tile's
  //     outline. It rides EVERY turn, and the FR-015 guard requires a non-null
  //     outline path to be in-scope AND editable, so publishing one that fails
  //     that refuses every turn on the tile. The case is a PICKED possible,
  //     whose outline resolves into ANOTHER tile's staged folder;
  //   * candidates are what that same guard would ACCEPT -- the intersection,
  //     never every readable path -- minus the outline itself, because offering
  //     the outline as the active DOCUMENT is two independent working copies of
  //     one file and two Save rows for one document.
  if (outlinePath !== null
      && !(editableSeen.has(outlinePath) && contextSeen.has(outlinePath))) {
    outlinePath = null;
  }
  const candidates = contextPaths.filter(
    (path) => editableSeen.has(path) && path !== outlinePath);
  const sourceRevision = options.sourceRevision == null
    ? asId(snapshot?.generation?.source_revision)
    : asId(options.sourceRevision);

  return {
    key: {
      repository: asId(options.repository),
      ref: asId(options.ref),
      tile_kind: scope.kind,
      tile_id: scope.id,
    },
    title: asId(scope.title),
    keywords: [...(scope.keywords || [])],
    source_revision: sourceRevision,
    sections: (scope.sections || []).map((section) => ({
      key: section.key,
      label: section.label,
      note: section.note,
      inherited: !!section.inherited,
      owned: !!section.owned,
      documents: (section.documents || []).map((row) => ({
        id: row.id,
        path: row.path,
        resolved: !!row.resolved,
      })),
    })),
    context_paths: contextPaths,
    editable_paths: editablePaths,
    outline_path: outlinePath,
    active_document_candidates: candidates,
  };
}

// The SCOPED snapshot the `lens` panel hands to the EXISTING keyword-lens
// derivation (`lens-model.js` buildLensModel) — a projection, not a new
// analysis and not a new snapshot read (design D4, change task 4.4):
//   * `documents` is the scope's own resolved document entries, so every count
//     the lens derives (universe, rings, matrix) is bounded to the tile;
//   * `keyword_index` is the snapshot's OWN seed filtered to the keywords the
//     scope actually touches, so each rail row's `declared_doc_count` stays the
//     snapshot's corpus-wide number VERBATIM — the panel labels it as such
//     rather than quietly recounting it inside the scope.
// Keeping the seed verbatim is the point: the workbench introduces no number
// the rest of the dashboard cannot show you.
export function lensScopeSnapshot(snapshot, scope) {
  const s = snapshot || {};
  const documents = (scope?.documents || [])
    .filter((row) => row.resolved)
    .map((row) => row.doc);
  const touched = new Set();
  for (const keyword of scope?.keywords || []) touched.add(keyword);
  for (const doc of documents) {
    for (const topic of doc?.topics || []) touched.add(asId(topic));
  }
  const keyword_index = (s.keyword_index || [])
    .filter((entry) => touched.has(asId(entry?.keyword)));
  return { documents, keyword_index };
}

// The lens rail's default check set: the scope's declared keywords, narrowed to
// the ones the scoped rail actually offers (an undeclared keyword is dropped
// rather than added to the rail — the same rule lens.js's `focusKeywords` uses).
export function lensSeedKeywords(scopedSnapshot, scope) {
  const rail = new Set();
  for (const entry of scopedSnapshot?.keyword_index || []) {
    rail.add(asId(entry?.keyword));
  }
  if (!rail.size) {
    for (const doc of scopedSnapshot?.documents || []) {
      for (const topic of doc?.topics || []) rail.add(asId(topic));
    }
  }
  return (scope?.keywords || []).filter((k) => rail.has(k));
}

// ==========================================================================
// LENS SESSION STATE (add-workbench-bullseye-and-create, design D4)
//
// The checked-keyword selection is WORKBENCH-SESSION state, not `draw()`-local:
// the panel used to rebuild `new Set(lensSeedKeywords(...))` on every mount, so
// `lens -> docs -> lens` silently destroyed the set the human had just built —
// and that set is now also the `Topics:` seed for a create, which makes losing
// it a correctness problem rather than an annoyance. The rule is expressed HERE,
// purely, so it is unit-testable from the node harness: the same scope keeps the
// selection; a DIFFERENT scope reseeds from the scope's own keywords.
// ==========================================================================

// The scope's identity for session purposes — kind + id, so two tiles never
// share a selection (a checked set is a statement about ONE scope's keywords).
export function scopeKey(scope) {
  return asId(scope?.kind) + "|" + asId(scope?.id);
}

// `previous` is the session ({key, checked}) the shell is holding, or null.
// Returns the session to use for THIS draw: unchanged when the scope is the same
// (a tab switch), freshly seeded when it is not (or on the first draw).
export function lensSessionSeed(previous, scopedSnapshot, scope) {
  const key = scopeKey(scope);
  if (previous && previous.key === key && Array.isArray(previous.checked)) {
    return previous;
  }
  return { key, checked: lensSeedKeywords(scopedSnapshot, scope) };
}

// Check/uncheck one keyword, returning a NEW list (the panel writes it back into
// the session the shell owns). Order-preserving: a re-checked keyword returns to
// the end rather than jumping back to its old slot, so the recipe line reads in
// the order the human built it.
export function toggleKeyword(checked, keyword) {
  const kw = asId(keyword);
  const list = (checked || []).map(asId);
  return list.includes(kw) ? list.filter((k) => k !== kw) : [...list, kw];
}

// ==========================================================================
// CREATE-DOCUMENT SEEDING (add-workbench-bullseye-and-create, design D7)
//
// Each tab seeds the create dialog from the material THAT TAB is showing, and
// every seeded value stays editable before the create fires. The seeding exists
// to stop the human retyping what the workbench already knows — it does NOT
// exist to guess: `title` and `summary` have no honest machine seed and are
// deliberately empty here (a generated summary would be prose the dashboard
// invented — Track C territory).
//
// `Status:` is `brainstorm` in EVERY area — Brett's 2026-07-25 ruling on design
// open question 1, "these are brainstorm docs". It is NOT derived from the area
// (an earlier pass did that and the ruling REVERSED it). What ties a created
// document to a staging packet is its PLACEMENT: `createArea()` below still puts
// a staged-tile create inside `ideation/staging/<topic>/`, which is exactly what
// that topic's folder-scoped health and readiness derivations read, while a
// cluster or possible create lands in `ideation/brainstorm/` and is tied to its
// neighbours only through `Topics:`. Placement carries the relationship; the
// status carries the lifecycle stage, and a just-captured thought is
// `brainstorm` wherever it sits. The field stays editable in the dialog and the
// route defaults identically, so a hand-rolled request lands the same header.
// ==========================================================================

export const BRAINSTORM_AREA = "ideation/brainstorm/";
export const STAGING_AREA = "ideation/staging/";
export const CREATE_TABS = ["docs", "lens", "outline"];
export const STATUS_BRAINSTORM = "brainstorm";
export const CREATE_ROUTE = "/actions/gate/create-document";
export const CREATE_CLI = "python3 scripts/ideation_dashboard/cli.py";

// A staged scope writes into its OWN topic folder; a cluster or a possible has
// no topic folder, so it writes into the brainstorm area (design D7). The area
// is editable in the dialog, and the create is create-only — a wrong area costs
// one file in the wrong folder, never a lost document.
export function createArea(scope) {
  if (scope?.kind === "staged" && asId(scope.id)) {
    return STAGING_AREA + asId(scope.id) + "/";
  }
  return BRAINSTORM_AREA;
}

// The `Source:` citation. For `docs`/`outline` it names the workbench scope by
// kind and id. For `lens` it names the RECIPE — the checked (and pinned)
// keywords — at the snapshot's `source_revision`, so the membership that
// motivated the document re-derives from the record rather than from wall-clock
// state ("a brainstorm born with machine-checkable provenance about WHY it
// exists" — the brainstorm's own goal).
// An activated bullseye SECTOR (Brett's 2026-07-25 ruling on open question 2)
// adds `· bullseye sector <a ∧ b>` to the citation. The recipe itself still
// records the FULL checked and pinned sets at the source revision — that is what
// makes the membership re-derivable — and the sector line records which of its
// combinations the human actually acted on. Naming only the subset as "checked"
// would misreport what the human had checked.
export function createSource(snapshot, scope, tab, opts) {
  const o = opts || {};
  const where = "staging workbench scope: " + asId(scope?.kind) + " " + asId(scope?.id);
  if (tab !== "lens") return where;
  const checked = (o.checked || []).map(asId);
  const pinned = (o.pinned || []).map(asId);
  const revision = asId(snapshot?.generation?.source_revision) || "unknown";
  const subset = uniqueStrings(o.subset || []);
  return where + " · keyword-lens recipe: checked " +
    (checked.length ? checked.join(", ") : "none") + " · pinned " +
    (pinned.length ? pinned.join(", ") : "none") +
    " · at source_revision " + revision +
    (subset.length ? " · bullseye sector " + subset.join(" ∧ ") : "");
}

// The full create seed for one tab. `opts.checked` / `opts.pinned` carry the
// LIVE lens selection (the `lens` tab's topics seed); the other tabs seed topics
// from the tile's own declared keywords. `opts.subset` — an activated bullseye
// SECTOR's matched keyword combination (open question 2's ruling) — narrows the
// `lens` topics seed to exactly that combination without touching the recipe
// citation; the centre region and the labelled button pass no subset, so they
// seed the whole checked set.
export function createSeed(snapshot, scope, tab, opts) {
  const o = opts || {};
  const area = asId(o.area) || createArea(scope);
  const subset = uniqueStrings(o.subset || []);
  const topics = tab === "lens"
    ? (subset.length ? subset : uniqueStrings(o.checked || []))
    : uniqueStrings(scope?.keywords || []);
  return {
    tab,
    area,
    title: "",
    summary: "",
    topics,
    repositoryContext: asId(snapshot?.repository),
    // The REPOSITORY THIS PAGE IS LOOKING AT, carried so the route can refuse a
    // write it cannot honour (PR #49 review finding 8, leg a). Distinct from
    // `repositoryContext` above, which is a DOCUMENT HEADER field the human can
    // edit in the dialog: this one is the selected snapshot's identity and is
    // never a form value.
    repository: asId(snapshot?.repository),
    kind: asId(o.kind) || "note",
    status: STATUS_BRAINSTORM,     // every area; the ruling — never area-derived
    source: createSource(snapshot, scope, tab, o),
    scopeKind: asId(scope?.kind),
    scopeId: asId(scope?.id),
  };
}

// The `outline` affordance is HIDDEN — not disabled — for cluster and possible
// scopes: there is no staging topic folder to write a fragment into, and a
// disabled button would imply a missing precondition the human could satisfy
// from here, which they cannot (design D7 consequence).
export function createOffered(scope, tab) {
  if (!scope) return false;
  if (!CREATE_TABS.includes(tab)) return false;
  return tab !== "outline" || scope.kind === "staged";
}

// The tile's scope kind as the SESSION resolves it (007-workbench-branch-sessions
// T023a). The workbench spells a staged tile `staged`; the session's scope
// vocabulary spells it `staged-topic` (the branch namespace is `draft/`), so the
// two are mapped here rather than at the transport — one definition, in the pure
// module, pinned from both sides like every other payload rule above.
export const SESSION_SCOPE_KINDS = {
  staged: "staged-topic",
  cluster: "cluster",
  possible: "possible",
};

export function sessionScopeKind(kind) {
  return SESSION_SCOPE_KINDS[asId(kind)] || "";
}

// The request body the create sends (and the shape the route validates). Kept
// here, in the pure module, so the payload contract has ONE definition that the
// node harness and the Python route tests both pin.
//
// `scope_kind` / `scope_id` (T023a) carry the TILE's identity, which is what the
// route resolves the branch session from: without them a create inside a session
// has no input and would land on the served checkout instead of the branch
// (FR-001, FR-018). Both are OMITTED when the scope cannot be resolved, so a
// scope-less body stays byte-identical to the pre-session one.
//
// `continuation` (T082) is the human's ANSWER to the FR-025 resume-or-new report.
// It is ALWAYS present and `null` until they answer, so the payload has ONE shape
// rather than two — and `null` is exactly what the route's
// `normalize_continuation` already reads as "no answer; show me the choice".
export function createRequest(seed, values) {
  const v = values || {};
  const merged = { ...seed, ...v };
  const body = {
    area: merged.area,
    title: merged.title,
    summary: merged.summary,
    topics: (merged.topics || []).map(asId),
    repository_context: merged.repositoryContext,
    kind: merged.kind,
    status: merged.status,
    source: merged.source,
  };
  // the selected repository, when the page knows one — the route refuses a
  // mismatch rather than writing into whichever repository it happens to serve
  if (asId(merged.repository)) body.repository = asId(merged.repository);
  const scopeKind = sessionScopeKind(merged.scopeKind);
  const scopeId = asId(merged.scopeId);
  if (scopeKind && scopeId) {
    body.scope_kind = scopeKind;
    body.scope_id = scopeId;
  }
  body.continuation = normalizeContinuation(merged.continuation);
  return body;
}

// Shell-quote one descriptor value so the emitted command is copy-pasteable
// VERBATIM — the promise the descriptors make, and the one they broke.
//
// POSIX SINGLE quotes, and every interpolated value goes through here (PR #49
// review finding 15). The previous spelling wrapped values in DOUBLE quotes,
// which preserve `$` and backtick expansion, and roughly half the slots
// (`--scope-id`, `--actor`, `--area`, `--status`, `--kind`, `--session-ref`, the
// workspace root) were interpolated with no quoting at all. Both halves of the
// harm are real: a backtick in ordinary engineering prose ("use `git log`") in a
// human-typed `--reason` silently MUTATED the pasted command, and `$(…)`,
// backticks and bare metacharacters also arrive from snapshot- and
// corpus-derived slots — merged corpus content reaching the human's shell in the
// served checkout.
//
// Inside single quotes a POSIX shell expands NOTHING, so the only character
// needing care is `'` itself, closed and re-opened around an escaped literal
// (`'\''`). Enum-mapped and validated values are quoted too: costing nothing,
// it removes the standing question of which slots were safe.
function q(value) {
  return "'" + asId(value).split("'").join("'\\''") + "'";
}

// The GATE-OFF affordance (design D8): the exact `cli.py gate create-document`
// invocation with the seeded values filled in, carried to where the authority
// lives. A descriptor is strictly more useful than a greyed-out button, and it
// is the established house posture (the gate bar, the lens plan panel). Unfilled
// human values render as `<...>` placeholders, exactly like gate.js's commands.
export function createDocumentCommand(seed, opts) {
  const o = opts || {};
  const s = seed || {};
  // The scope flags ride the descriptor too (T023a): they are what resolves the
  // branch session, so a descriptor without them would be a command that writes
  // somewhere else than the button does — the descriptor must be the SAME action.
  const scopeKind = sessionScopeKind(s.scopeKind);
  const scopeId = asId(s.scopeId);
  const scope = (scopeKind && scopeId)
    ? ["--scope-kind", q(scopeKind), "--scope-id", q(scopeId)] : [];
  const parts = [
    CREATE_CLI, "gate", "create-document",
    "--repo-root", q("."),
    "--actor", q(asId(o.actor) || "<you>"),
    ...scope,
    "--area", q(asId(s.area) || BRAINSTORM_AREA),
    "--title", q(s.title || "<title>"),
    "--summary", q(s.summary || "<one-sentence summary>"),
    "--topics", q((s.topics || []).join(", ")),
    "--repository-context", q(s.repositoryContext || "<repo>"),
    "--status", q(asId(s.status) || STATUS_BRAINSTORM),
    "--kind", q(asId(s.kind) || "note"),
    "--source", q(s.source || ""),
  ];
  // The resume-or-new ANSWER rides the descriptor only once it has been given
  // (T082, FR-025): the first invocation deliberately sends none and is SHOWN the
  // choice, so a descriptor carrying a default answer would answer for the human.
  const continuation = normalizeContinuation(s.continuation);
  if (continuation) parts.push("--continuation", q(continuation));
  return parts.join(" ");
}

// ==========================================================================
// BRANCH SESSIONS — the surface's PURE half
// (007-workbench-branch-sessions, FR-044–FR-046; plan Constraint 11; research R6)
//
// Everything a session affordance needs to DECIDE lives here, and nothing that
// TALKS to the network does. That split is not stylistic: `test_renderer.py:130`
// pins the bundle's set of same-origin request call sites and
// `test_staging_workbench.py`
// pins this module transport-free and import-free (it is copied ALONE into a
// node harness), so the route constants, the request bodies, the CLI descriptors,
// and the posture derivation are all here while the ONE request site lives in
// the sibling `swb-session.js`.
//
// A BRANCH SESSION is derived state (design D10): it IS its branch, its worktree,
// its snapshot-registry entry, and its tile-derived notebook alias — there is no
// descriptor to read. So the page derives it the same way, from two things it
// already has: the ACTIVE (repository, ref) key, and the serving index's roster,
// where a live session is an ORDINARY (repository, ref) row (FR-014). No second
// liveness signal is invented here, and none should be: the registry entry is
// the authority (FR-008), and the roster is that authority projected.
//
// NOT to be confused with the UI-lifetime "workbench session" above
// (`lensSessionSeed`, design D14) — that one scopes the checked-keyword
// selection and dies with the overlay. Neither derivation carries the other's
// keys, which is what makes them impossible to conflate in a view.
// ==========================================================================

// WHAT YOU ALREADY HAVE ON THIS TOPIC (Brett, 2026-08-10: "if same keywords,
// then we want to list it in the doxBench too. so the user knows he now has two
// of this topic").
//
// The reason this is worth a panel rather than a note: every create-only refusal
// tonight was the same shape — a document on this topic already existed and the
// draft screen did not say so, so the human pressed save and read
// `corpus documents are create-only` as the outcome of their work. The engine's
// refusal is correct and arrives too late to be useful; the fact belongs on
// screen BEFORE the save.
//
// `topics` is the seed's own shared-term set. A document counts as "already on
// this topic" when it declares ANY of them, and the STRONGEST signal is a
// document in the very folder this create is aiming at — that one will refuse.
// Pure, so the panel and the tests read the same derivation.
export function existingOnTopic(snapshot, topics, area) {
  const wanted = new Set(uniqueStrings(topics));
  const folder = asId(area);
  const rows = [];
  for (const doc of snapshot?.documents || []) {
    const path = asId(doc?.path || doc?.id);
    if (!path) continue;
    const shared = (doc.topics || []).filter((t) => wanted.has(asId(t)));
    const inFolder = !!folder && path.startsWith(folder);
    if (!shared.length && !inFolder) continue;
    rows.push({
      path,
      title: asId(doc.title) || path.split("/").pop(),
      status: asId(doc.status),
      shared: uniqueStrings(shared),
      // this one occupies the ground the create is aiming at: a create here is
      // refused create-only, and it is the row the human most needs to see
      inFolder,
    });
  }
  // the folder collisions first, then the most shared terms
  rows.sort((a, b) => (Number(b.inFolder) - Number(a.inFolder))
    || (b.shared.length - a.shared.length)
    || a.path.localeCompare(b.path));
  return rows;
}

export const MAIN_REF = "main";

// The three routes the session surface addresses. Constants HERE (never literals
// in the transport) so the wire contract has one definition the Python route
// tests read too.
export const EDIT_DOCUMENT_ROUTE = "/actions/gate/edit-document";
export const OPEN_PR_ROUTE = "/actions/gate/open-pr";
// 010-doxbench-editor-chat T080: the first-Save gate verb. A CANVAS seam, not
// a session-bar affordance -- deliberately absent from SESSION_AFFORDANCES.
export const FIRST_EDIT_ROUTE = "/actions/gate/first-edit";
export const ABANDON_SESSION_ROUTE = "/actions/gate/abandon-session";

// THE HUMAN-CONSOLE HEADER (FR-019's third clause; PR #49 review finding 2).
// The serve mints a token at start-up and publishes it on `/capabilities`, the
// one route this page reads same-origin and no cross-origin page can read; every
// session write presents it, and a write that cannot is refused BEFORE the body
// is parsed. Defined here, in the pure model, so the header name has ONE
// definition that the transport, the node harness, and the Python route tests
// all read — exactly like the routes above.
export const CONSOLE_TOKEN_HEADER = "X-XF-Console-Token";
export const CONSOLE_TOKEN_FIELD = "console_token";

export function consoleHeaders(caps) {
  const headers = { "Content-Type": "application/json" };
  const token = asId(caps && caps[CONSOLE_TOKEN_FIELD]);
  if (token) headers[CONSOLE_TOKEN_HEADER] = token;
  return headers;
}

// ---- A STRANDED PAGE REPAIRS ITSELF (Brett, 2026-08-09) --------------------
//
// Every serve start mints a NEW token, and the page reads `/capabilities` ONCE,
// at load. So a tab that outlives a restart keeps presenting the old token and
// every guarded write is refused — and the refusal fires exactly where it costs
// most: the human has typed a title, a summary and a body, and pressed create.
//
// THE REPAIR IS A RE-READ, NOT A RELOAD. `location.reload()` would fix the
// header by throwing away the textarea, the selection and the drafted seed —
// the work the refusal interrupted. So the page re-probes `/capabilities`,
// takes the new token, and sends the SAME request again. This only became
// necessary when the shell started re-rendering IN PLACE (Brett, 2026-08-09,
// "get rid of the flash"): before that most actions navigated, and a navigation
// quietly re-read the token on the way past.
//
// WHY AN AUTOMATIC RETRY IS SAFE FOR THESE TWO CODES AND NOTHING ELSE. Both are
// emitted by `serve.py`'s `_not_the_human_console()` gate, which runs BEFORE the
// request body is read and before any write: the server did nothing, so sending
// the request again cannot double anything. That is the whole membership rule —
// a refusal that might have half-landed stays with the human, so this list is
// these two codes and never "any 403".
export const CONSOLE_REFUSAL_CODES = Object.freeze([
  "agent_invocation",   // /actions/gate/* and /actions/edit
  "console_required",   // the doxBench model-catalog and chat-turn routes
]);

export function consoleRefusal(payload) {
  return !!payload && payload.ok !== true
    && CONSOLE_REFUSAL_CODES.includes(asId(payload.error));
}

// What a page that could NOT repair itself says. The wire refusal is a
// four-clause statement of FR-019 — true, and no use to someone who only wants
// their create to land, so it is not surfaced.
export const CONSOLE_STRANDED_MESSAGE =
  "this page was loaded against an earlier serve — reload to continue";

export function strandedRefusal() {
  return { ok: false, error: "console_stranded",
           message: CONSOLE_STRANDED_MESSAGE };
}

// `send()` once; on a console refusal, `repair()` and `send()` once more. Never
// a third attempt and never a loop: a second identical refusal means the token
// was not the problem, and a page that retried forever would hide that instead
// of saying it. A retry that refuses for some OTHER reason returns that refusal
// verbatim — the engine's own answer still reaches the human unchanged.
export async function withConsoleRepair(send, repair) {
  const first = await send();
  if (!consoleRefusal(first)) return first;
  const repaired = typeof repair === "function" ? await repair() : false;
  if (!repaired) return strandedRefusal();
  const second = await send();
  return consoleRefusal(second) ? strandedRefusal() : second;
}

export const SESSION_EDIT = "edit";
export const SESSION_FIRST_EDIT = "first-edit";
export const SESSION_SAVE = "save";
export const SESSION_ABANDON = "abandon";
export const SESSION_REFRESH_NOTEBOOK = "refresh-notebook";

// FR-044's four affordances, and the split FR-046 + spec C10 impose on them:
// three are LIVE where the gate capability is present, and the notebook re-sync
// is DESCRIPTOR-ONLY in BOTH postures. It is not a gate route and not a `gate`
// subcommand — no artifact declares a transport for it — so giving it one here
// would invent an FR-020 parity obligation and `fetch` arithmetic that no
// ratified text asks for.
export const SESSION_AFFORDANCES = [SESSION_EDIT, SESSION_SAVE, SESSION_ABANDON,
                                    SESSION_REFRESH_NOTEBOOK];
export const LIVE_SESSION_AFFORDANCES = [SESSION_EDIT, SESSION_SAVE, SESSION_ABANDON];
export const DESCRIPTOR_ONLY_AFFORDANCES = [SESSION_REFRESH_NOTEBOOK];

const SESSION_ROUTES = {
  [SESSION_EDIT]: EDIT_DOCUMENT_ROUTE,
  [SESSION_SAVE]: OPEN_PR_ROUTE,
  [SESSION_ABANDON]: ABANDON_SESSION_ROUTE,
  [SESSION_FIRST_EDIT]: FIRST_EDIT_ROUTE,
};

// affordance -> the gate verb it IS, which is also the `cli.py gate <verb>` name
// (FR-020's parity is one vocabulary, not two).
export const SESSION_VERBS = {
  [SESSION_EDIT]: "edit-document",
  [SESSION_SAVE]: "open-pr",
  [SESSION_ABANDON]: "abandon-session",
};

export const SESSION_LABELS = {
  [SESSION_EDIT]: "✎ rewrite a document in this session",
  [SESSION_SAVE]: "⇪ save — open the pull request",
  [SESSION_ABANDON]: "⌧ abandon this session",
  [SESSION_REFRESH_NOTEBOOK]: "↻ re-sync the session notebook",
};

export const NOTEBOOK_SYNC_CLI = "python3 scripts/sync-notebooklm-books.py";
export const WORKSPACE_ROOT_PLACEHOLDER = "<workspace root>";

export function sessionRoute(affordance) {
  return SESSION_ROUTES[asId(affordance)] || null;
}

// FR-025's two continuations and the ONLY two — spelled from the same tokens
// `branch_session.CONTINUATIONS` declares, because the report the human is
// answering names them literally.
export const CONTINUATION_RESUME = "resume";
export const CONTINUATION_NEW = "new";
export const CONTINUATIONS = [CONTINUATION_RESUME, CONTINUATION_NEW];

export function normalizeContinuation(value) {
  const text = asId(value).trim().toLowerCase();
  return CONTINUATIONS.includes(text) ? text : null;
}

// Whether SESSION writes are live on this plane. Two questions, one answer:
// FR-046 keys live-vs-descriptor on the GATE capability, and FR-048 requires a
// plane that advertises `session: false` to have none regardless — the hosted
// plane, whose refusal is structural because the push identity is the invoking
// engineer's personal credential (FR-034, D22). An older server that reports no
// `session` key at all is the local plane before this feature: the gate leg
// answers, which is what keeps the degradation honest rather than silent.
export function sessionActionsLive(caps) {
  const actions = (caps && caps.actions) || {};
  if (actions.session === false) return false;
  return !!actions.gate;
}

// Whether the session SURFACE exists on this plane at all — the FR-046/FR-048
// tension, resolved (PR #49 review finding 14).
//
// `sessionActionsLive` collapses two different "no" answers into one boolean:
// "this plane has no authority, here is the CLI to run in your own checkout"
// (FR-046) and "this plane has no sessions AT ALL" (FR-048). The hosted plane
// got the FIRST answer, so it announced that a session was live, named its
// branch, and printed its three verbs — exactly what FR-048 and US7 acceptance
// scenario 1 forbid.
//
// The discriminator is the capability's OWN statement, which is why FR-048 made
// the probe state it separately: `session: false` is the HOSTED plane declaring
// it has none. FR-046's descriptor path is kept for the plane that declares
// nothing about sessions — an older serve, or the static bundle whose
// `/capabilities` 404s and degrades to `{actions:{notebook:false}}` — where a
// human IS at their own machine and the CLI is a real remedy.
export function sessionSurfaceHidden(caps) {
  const actions = (caps && caps.actions) || {};
  return actions.session === false;
}

// ---- the session branch name (mirrors branch_session.session_branch) --------
//
// The page derives a branch name for the posture line and for every descriptor,
// so this MUST agree with `branch_session.session_branch` — a drift would name a
// branch nobody is on. Pinned against the real Python derivation in
// `test_the_session_branch_derivation_agrees_with_the_python_side`.
export const SESSION_BRANCH_NAMESPACES = {
  staged: "draft",
  cluster: "cluster",
  possible: "possible",
};

// A colon-qualified corpus staging id reduces to its final segment (research R2:
// `git check-ref-format` rejects `:`), and a path-shaped id derives NOTHING
// rather than a branch in another namespace (FR-002).
export function reduceScopeId(scopeId) {
  const reduced = asId(scopeId).trim().split(":").at(-1).trim();
  return reduced.includes("/") ? "" : reduced;
}

export function sessionBranchBase(scope) {
  const namespace = SESSION_BRANCH_NAMESPACES[asId(scope && scope.kind)];
  const reduced = reduceScopeId(scope && scope.id);
  if (!namespace || !reduced) return null;
  return namespace + "/" + reduced;
}

// Which ordinal of `base`'s family `ref` is, or null when it is not a member at
// all — `branch_session.ordinal_of`'s strictness, deliberately: `-02` is not the
// ratified `-2` spelling, and `-and-more` / `ical` are different tiles.
export function sessionOrdinal(ref, base) {
  const name = asId(ref);
  const stem = asId(base);
  if (!stem) return null;
  if (name === stem) return 1;
  if (!name.startsWith(stem + "-")) return null;
  const tail = name.slice(stem.length + 1);
  if (!/^[0-9]+$/.test(tail)) return null;
  const value = Number(tail);
  return value >= 2 && String(value) === tail ? value : null;
}

// The non-`main` refs the serving index advertises for one repository. Filtered
// BY REPOSITORY because two repositories can carry the same tile id, so a branch
// alone is not a session key (FR-037, spec C9).
export function sessionRefs(index, repository) {
  const entries = (index && Array.isArray(index.entries)) ? index.entries : [];
  const wanted = asId(repository);
  const out = [];
  for (const entry of entries) {
    if (!entry || !entry.repository) continue;
    if (wanted && asId(entry.repository) !== wanted) continue;
    const ref = asId(entry.ref).trim() || MAIN_REF;
    if (ref === MAIN_REF || out.includes(ref)) continue;
    out.push(ref);
  }
  return out;
}

// Every tile the SNAPSHOT advertises, as `{kind, id}` — the page's half of
// `branch_session.TileInventory` (FR-026, G12). The three registers the engine's
// `discover_tile_inventory` unions are the three collections the snapshot already
// carries, and this reads them and nothing else.
export function advertisedTiles(snapshot) {
  const s = snapshot || {};
  const out = [];
  for (const topic of s.staged_topics || []) {
    const id = asId(topic && topic.staging_id);
    if (id) out.push({ kind: "staged", id });
  }
  for (const cluster of s.clusters || []) {
    const id = asId(cluster && cluster.id);
    if (id) out.push({ kind: "cluster", id });
  }
  for (const possible of s.possibles || []) {
    const id = asId(possible && possible.id);
    if (id) out.push({ kind: "possible", id });
  }
  return out;
}

// `branch -> the OTHER advertised tile whose DETERMINISTIC branch that is`, i.e.
// `TileInventory.other_branches(tile)`. The G12 question, asked on the page: is
// this ref a name another tile owns?
export function otherTileBranches(snapshot, scope) {
  const mine = tileKey(scope);
  const out = new Map();
  for (const tile of advertisedTiles(snapshot)) {
    if (tileKey(tile) === mine) continue;
    const branch = sessionBranchBase(tile);
    if (branch && !out.has(branch)) out.set(branch, tile);
  }
  return out;
}

// The separator is an escaped NUL, written as `\u0000` rather than as the raw
// byte it used to be (2026-08-03). A NUL is the RIGHT separator here — it is
// the one character that cannot occur in a kind or an id, so no two scopes can
// collide on a composed key. Embedding it literally was the problem, not the
// choice: it made this file BINARY to grep, which then answered "no match" for
// text that was plainly present, and editors render it as a space, so the
// source read as if it joined on " " — a separator a space-bearing id breaks.
function tileKey(scope) {
  return asId(scope?.kind) + "\u0000" + asId(scope?.id);
}

// The tile's own ordinal family among `refs`, in ordinal order. A tile has ONE
// session, and after a NEW continuation it lives at the HIGHEST ordinal.
//
// OWNERSHIP-BLIND on purpose: this is the FAMILY, the same set
// `branch_session.tile_branch_family` computes before any exclusion is applied.
// Whether a member of it is really THIS tile's session is `sessionPosture`'s
// question, and it is where the G12 exclusion belongs (finding 18) — a `-2` ref is
// this tile's second session AND tile `<id>-2`'s first, and the family cannot tell
// those apart.
export function tileSessionRefs(refs, scope) {
  const base = sessionBranchBase(scope);
  if (!base) return [];
  const family = [];
  for (const ref of refs || []) {
    const ordinal = sessionOrdinal(ref, base);
    if (ordinal !== null) family.push({ ordinal, ref });
  }
  family.sort((a, b) => a.ordinal - b.ordinal);
  return family.map((member) => member.ref);
}

// THE POSTURE (FR-045). Three separate honesties, never collapsed into one
// boolean: whether a branch session is ACTIVE on this tile, WHICH branch it is
// on, and whether THIS view is a draft view. The last one is the ACTIVE ref's
// question and nothing else's — a workbench reading a session entry IS reading
// unmerged work, and the shared surfaces (wheel, funnel, board) are still on
// `main` because they fetch with no key (FR-014a).
//
// TWO PAGE-LIFETIME OVERLAYS, because the roster was fetched at BOOT and the human
// changes things after that. Without both, the indicator is stale in exactly the
// two moments it matters most:
//
//   `opts.opened` — the ref a `create-document` OPENED (or joined) during this
//     page's life. The roster does not know it yet, so without this the bar would
//     read "no branch session" one click after opening one.
//   `opts.ended` — a save that came back `merged: true` or an abandon ENDED the
//     session (Phase 7 note 4), so the affordances must re-derive rather than stay
//     open against a session that is over. An ended ref is NOT simply struck out:
//     that would make the tile's own branch look like a stranger's the moment it
//     ended, and a page sitting ON that ref would be told it was viewing "another
//     tile's session". It is reported as `endedBranch`, still named, `live: false`.
//
// Both are session-local and derived-state-only: nothing in the snapshot or the
// registry is mutated here, and a reload replaces both with the server's answer.
//
// THE G12 EXCLUSION IS APPLIED HERE (PR #49 second-review finding 18). The
// posture used to take `family[family.length - 1]` off the raw ordinal family, so
// in exactly the state the mandatory T049(c) test builds — tile `<id>-2` live at
// `draft/<id>-2`, tile `<id>` with no session — the card for tile `<id>` announced
// a live session on ANOTHER tile's branch and handed the human a copyable
// `sync-notebooklm-books.py … --session-ref draft/<id>-2 --apply` pointed at that
// other tile's worktree, while the engine refused every session verb on the tile
// with `NoActiveSession`. The page cannot know WHOSE session a ref is — the engine
// reads that from the owner the OPEN recorded, which is not projected — so the
// honest answer for a ref that is also another advertised tile's deterministic
// name is AMBIGUOUS: it is reported as such, it is never claimed as this tile's
// live session, and no command is built against it.
export function sessionPosture(scope, opts) {
  const o = opts || {};
  const active = o.active || null;
  const activeRef = asId(active && active.ref).trim() || MAIN_REF;
  const repository = asId((active && active.repository) || o.repository);
  const base = sessionBranchBase(scope);
  const ended = (o.ended || []).map(asId);
  const others = o.otherTiles instanceof Map
    ? o.otherTiles : otherTileBranches(o.snapshot, scope);
  const inFamilyRefs = tileSessionRefs(
    uniqueStrings([...sessionRefs(o.index, repository), ...(o.opened || [])]),
    scope);
  // a family member that is another advertised tile's OWN deterministic branch
  const ambiguous = inFamilyRefs.filter((ref) => others.has(ref));
  const advertised = inFamilyRefs.filter((ref) => !others.has(ref));
  const ambiguousRef = ambiguous.length ? ambiguous[ambiguous.length - 1] : null;
  const ambiguousTile = ambiguousRef ? (others.get(ambiguousRef) || null) : null;
  const ambiguousOwner = ambiguousTile ? asId(ambiguousTile.id) : null;
  const endedFamily = advertised.filter((ref) => ended.includes(ref));
  const family = advertised.filter((ref) => !ended.includes(ref));
  const draft = activeRef !== MAIN_REF;
  const ownTile = draft && family.includes(activeRef);
  const inFamily = draft && advertised.includes(activeRef);
  const live = family.length > 0;
  const endedBranch = endedFamily.length
    ? endedFamily[endedFamily.length - 1] : null;
  const branch = ownTile
    ? activeRef
    : (live ? family[family.length - 1] : endedBranch);
  const ambiguityDetail = ambiguousRef
    ? (" The ref " + ambiguousRef + " is in this tile's ordinal family AND is " +
       "tile " + ambiguousOwner + "'s own session branch, so which tile's session " +
       "it is cannot be read from this page — only the engine, which recorded " +
       "which tile OPENED it, can say. Nothing here treats it as this tile's.")
    : "";
  let label;
  let detail;
  if (draft && ambiguous.includes(activeRef)) {
    label = "DRAFT VIEW · " + activeRef + " · AMBIGUOUS session";
    detail = "the page is on the draft ref " + activeRef + ", which is BOTH a " +
      "member of this tile's ordinal family and tile " + ambiguousOwner +
      "'s own session branch. This view is reading UNMERGED work either way; " +
      "session affordances here resolve THIS tile's session through the engine, " +
      "which refuses rather than guessing if it cannot tell (FR-002, G12).";
  } else if (ownTile) {
    label = "DRAFT VIEW · " + activeRef;
    detail = "this workbench is reading UNMERGED session work on branch " +
      activeRef + ". The wheel, the funnel, and the board still render " +
      MAIN_REF + " — a draft never appears in a shared surface.";
  } else if (inFamily) {
    label = "session ENDED · " + activeRef;
    detail = "this tile's session on " + activeRef + " ended during this page's " +
      "life, and the view is still its draft snapshot. Reload to return to " +
      MAIN_REF + " and see the tile's current state.";
  } else if (draft) {
    label = "DRAFT VIEW · " + activeRef + " · another tile's session";
    detail = "the page is on the draft ref " + activeRef + ", which is not this " +
      "tile's session branch" + (base ? " (" + base + ")" : "") +
      ". Session affordances here still resolve THIS tile's session, and the " +
      "engine refuses if it has none.";
  } else if (live) {
    label = "session live · " + branch + " · this view is " + MAIN_REF;
    detail = "a branch session is open on " + branch +
      ", and this view is the shared " + MAIN_REF +
      " projection. Switch to that ref to read the session's own drafts." +
      ambiguityDetail;
  } else if (ambiguousRef) {
    // the finding-18 state itself: the ONLY family ref on the roster is one
    // another tile owns, so "session live" would be a claim about someone else's
    // session and "no branch session" would be a claim this page cannot make
    label = "session AMBIGUOUS · " + ambiguousRef + " · also tile " +
      ambiguousOwner + "'s branch";
    detail = "a session is live on " + ambiguousRef + ", which is a member of " +
      "this tile's ordinal family AND tile " + ambiguousOwner + "'s own session " +
      "branch — so this page cannot say whose it is, and does not guess. Ask the " +
      "engine: a session verb here resolves THIS tile's session and refuses, " +
      "naming both tiles, if the answer is genuinely ambiguous (FR-002, G12). No " +
      "command on this card is built against that ref.";
  } else if (endedBranch) {
    label = "session ended · " + endedBranch + " · this view is " + MAIN_REF;
    detail = "this tile's session on " + endedBranch + " ended during this " +
      "page's life. Reload to see the tile's current state — the roster this " +
      "page loaded still advertises the ref.";
  } else {
    label = "no branch session · this view is " + MAIN_REF;
    detail = "no branch session is open on this tile. The first recorded write " +
      "opens one on " + (base || "the tile's derived branch") +
      "; nothing here has moved the served checkout.";
  }
  return { activeRef, repository, base, family, endedFamily, endedBranch, branch,
           draft, ownTile, live, label, detail,
           // the G12 answer, carried so a consumer can say WHY there is no branch
           // to build a command against (finding 18)
           ambiguous, ambiguousRef, ambiguousOwner };
}

// ---- the request bodies (the shapes contracts/gate-routes.md validates) -----
//
// One definition per verb, here, so the node harness and the Python body parsers
// pin the SAME payload from both sides. `null` for an affordance that has no
// body at all — the notebook re-sync, which has no route (spec C10).
export function sessionRequest(affordance, scope, values) {
  const v = values || {};
  const verb = SESSION_VERBS[asId(affordance)];
  const scopeKind = sessionScopeKind(scope && scope.kind);
  const scopeId = asId(scope && scope.id);
  if (!verb || !scopeKind || !scopeId) return null;
  const body = { scope_kind: scopeKind, scope_id: scopeId };
  // THE REPOSITORY IDENTITY, CARRIED (PR #49 review finding 8, leg a). The body
  // used to name only the tile, so the server keyed the session off whichever
  // entry happened to be ACTIVE — which the client-side repository selector does
  // NOT move. A page reading repoB could therefore drive a session in repoA.
  // Present only when the page knows its repository, so the pre-existing shape is
  // what an older client still sends.
  if (asId(v.repository)) body.repository = asId(v.repository);
  if (affordance === SESSION_EDIT) {
    body.document = asId(v.document).trim();
    // the FULL replacement text, untrimmed: trailing whitespace is the
    // document's, not this function's to decide
    body.content = typeof v.content === "string" ? v.content : "";
    if (asId(v.notes).trim()) body.notes = asId(v.notes).trim();
    return body;
  }
  if (affordance === SESSION_SAVE) {
    // both OPTIONAL (contracts/gate-routes.md): an unfilled title is omitted so
    // the engine's own default names the branch and its tile
    if (asId(v.title).trim()) body.title = asId(v.title).trim();
    if (asId(v.body).trim()) body.body = asId(v.body).trim();
    return body;
  }
  body.reason = asId(v.reason).trim();
  return body;
}

// ---- the descriptors (FR-046, contracts/cli.md) -----------------------------
//
// The gate-off affordance is the REAL `cli.py gate <verb>` invocation, filled in
// for this tile, as copyable text — the same posture the create affordance and
// the gate bar already take. Asserted by PARSING each one with the real CLI
// parser, so a descriptor the terminal would reject cannot ship.
export function sessionCommand(affordance, opts) {
  const o = opts || {};
  if (asId(affordance) === SESSION_REFRESH_NOTEBOOK) return notebookRefreshCommand(o);
  const verb = SESSION_VERBS[asId(affordance)];
  const scope = o.scope || null;
  const scopeKind = sessionScopeKind(scope && scope.kind);
  const scopeId = asId(scope && scope.id);
  if (!verb || !scopeKind || !scopeId) return null;
  const parts = [
    CREATE_CLI, "gate", verb,
    "--repo-root", q("."),
    // EVERY value is quoted, including the enum-mapped scope kind and the
    // validated scope id: `git config user.name` is routinely two words, and a
    // snapshot-derived scope id carrying `;` or `$(…)` used to reach the pasting
    // human's shell unquoted (PR #49 review finding 15).
    "--actor", q(asId(o.actor) || "<you>"),
    "--scope-kind", q(scopeKind),
    "--scope-id", q(scopeId),
  ];
  if (affordance === SESSION_EDIT) {
    parts.push("--document", q(asId(o.document) || "<path in the session worktree>"));
    // `--content-file`, never inline text, so a shell cannot mangle a document
    parts.push("--content-file", q(asId(o.contentFile) || "<file holding the replacement>"));
    if (asId(o.notes).trim()) parts.push("--notes", q(o.notes));
  } else if (affordance === SESSION_SAVE) {
    // optional, and NOT invented when unfilled: a pull request titled `<title>`
    // is nobody's intent, and the engine's default names the branch and the tile
    if (asId(o.title).trim()) parts.push("--title", q(o.title));
    if (asId(o.bodyFile).trim()) parts.push("--body-file", q(o.bodyFile));
  } else {
    parts.push("--reason", q(asId(o.reason).trim() || "<why this exploration stopped>"));
  }
  return parts.join(" ");
}

// FR-040's notebook re-sync: the ONE affordance that is a descriptor in BOTH gate
// postures (spec C10). Rendered WITHOUT `--apply` by default — the script's own
// dry-run-first discipline, which prints the op list for a human to eyeball — and
// with it on the second, explicit line.
export function notebookRefreshCommand(opts) {
  const o = opts || {};
  const branch = asId(o.branch) || asId(o.posture && o.posture.branch);
  const parts = [
    NOTEBOOK_SYNC_CLI,
    q(asId(o.workspaceRoot) || WORKSPACE_ROOT_PLACEHOLDER),
    // the branch is DERIVED from a tile id the page did not author, so it is a
    // snapshot-controlled value in a shell line (PR #49 review finding 15)
    "--session-ref", q(branch || "<branch>"),
  ];
  if (o.apply) parts.push("--apply");
  return parts.join(" ");
}

// ---- the presentation posture (010-doxbench-editor-chat T090) -----------
//
// ONE derivation names the posture the presentation is in, so omitting a
// control is a stated decision (FR-040) rather than a scatter of independent
// conditionals, and the inline explanation (T091) and the shell's own
// canvas-offering logic read the SAME answer. Pure: capability facts in,
// {kind, canvas, note} out. `note: null` means nothing needs explaining.
//
// The ladder is ordered by authority, most-restrictive first: a gate-off or
// hidden surface must never be described by a lesser condition ("no model")
// that would understate what is withheld. `approvedModelCount` is honestly
// ZERO until the released model catalog is pinned and its browser transport
// lands (T005-T008 / T052-T054) — so a capable local console today states
// that chat is unavailable while both editors stay usable (FR-025, US5
// acceptance scenario 2), which is the truth of this build.
export function presentationPosture(input) {
  const facts = input || {};
  const gateLive = !!facts.gateLive;
  const surfaceHidden = !!facts.surfaceHidden;
  const keyed = !!facts.repository && !!facts.ref;
  const sourceAvailable = facts.sourceAvailable !== false;
  const approvedModels = Number.isFinite(facts.approvedModelCount)
    ? facts.approvedModelCount : 0;
  if (surfaceHidden) {
    return {
      kind: "hosted-hidden", canvas: false,
      note: "read-only surface: editing, chat, Apply, and Save are not " +
        "offered on this plane — docs, lens, and outline stay readable.",
    };
  }
  if (!gateLive) {
    return {
      kind: "gate-off", canvas: false,
      note: "read-only: the create/edit gate is off here, so editing, chat, " +
        "and Save are not offered — retained context stays readable.",
    };
  }
  if (!keyed) {
    return {
      kind: "unkeyed", canvas: false,
      note: "no active repository and ref are resolved, so the authoring " +
        "canvas is not offered yet.",
    };
  }
  if (!sourceAvailable) {
    return {
      kind: "source-unavailable", canvas: true,
      note: "source content is unavailable right now: snapshot-backed " +
        "context stays usable and source-dependent content reports its " +
        "state inline.",
    };
  }
  // T104 F10-1: the catalog-FAILURE rungs, above editor-only because a
  // failed catalog also reports zero approved models — the count alone
  // cannot tell "nothing is configured" from "the answer could not be
  // read", and those are different facts with different remedies. Two fixed
  // postures, matching the transport's two distinguished markers: the
  // pre-identity console refusal is RECOVERABLE (R-3's reload vocabulary),
  // everything else is the unreadable catalog. The canvas stays offered in
  // both — chat is what failed, not editing (FR-025).
  if (facts.catalogFailure === "console_required") {
    return {
      kind: "console-token-stale", canvas: true,
      note: "chat is unavailable — this page's console token is stale; " +
        "reload the page to continue. Both editors remain fully usable.",
    };
  }
  if (facts.catalogFailure) {
    return {
      kind: "catalog-unreadable", canvas: true,
      note: "chat is unavailable — the model catalog could not be read; " +
        "both editors remain fully usable.",
    };
  }
  if (approvedModels === 0) {
    return {
      kind: "editor-only", canvas: true,
      note: "chat is unavailable — no approved model is configured; both " +
        "editors remain fully usable.",
    };
  }
  return { kind: "capable-local", canvas: true, note: null };
}

// ---- the first-edit wire mappings (010-doxbench-editor-chat T080) --------
//
// Pure both ways, so the wire vocabulary is derived and testable without a
// transport: the BODY speaks the gate verb's language (scope_kind/scope_id,
// base_hash as the HEX spelling the server parameter takes), and the VERDICT
// speaks the Save seam's (the verb's `commit` is the seam's `revision`; the
// STRUCTURED content identity passes through untouched, because that is the
// shape the state module validates at adoption). Keeping both maps here also
// keeps the `kind:`-bearing body out of app.js entirely.
export function firstEditBody(repository, key, request) {
  const identity = request.base_hash;
  const hex = typeof identity === "string"
    ? identity
    : (identity && typeof identity.hex === "string" ? identity.hex : null);
  const body = {
    repository,
    // T100 run-3 blocker: the SESSION vocabulary spells this kind
    // `staged-topic` (branch_session.SCOPE_KINDS), not the tile vocabulary's
    // `staged` — the mapping existed above (SESSION_SCOPE_KINDS) and is now
    // APPLIED on the Save path too, where it had been forwarded verbatim.
    scope_kind: sessionScopeKind(key.tile_kind),
    scope_id: key.tile_id,
    document: request.document,
    content: request.content,
  };
  if (hex) body.base_hash = hex;
  return body;
}

export function firstEditVerdict(payload) {
  if (!payload || payload.ok !== true) {
    // T104 F5-1: NO action field here, deliberately. The route's refusals
    // carry no `verb` at all (only the success body does), and the Save
    // seam's reader keeps the client's own plan row for a refused buffer —
    // so an action on this branch was dead weight that additionally
    // dereferenced `payload.verb` AFTER the `!payload` guard had matched,
    // turning a payload-less transport into a TypeError instead of the
    // mapped fixed refusal below.
    return {
      ok: false,
      message: (payload && typeof payload.message === "string")
        ? payload.message
        : "the Save transport returned no verdict for this buffer",
    };
  }
  return {
    ok: true,
    // Triage item 13, landed on the RIGHT branch by T104 F5-1: the server's
    // OWN create-vs-edit resolution rides the SUCCESS payload as `verb`
    // (gate_routes.first_edit_response reports `outcome.action` there), and
    // doxbench-save's readVerdict adopts `answer.action` only into a
    // COMMITTED row — so this is the only place surfacing it lets the
    // server's answer override the client's prediction.
    action: typeof payload.verb === "string" ? payload.verb : null,
    ref: payload.ref,
    revision: payload.commit,
    content_hash: payload.content_hash,
    document: payload.document,
    record: payload.record,
    session: payload.session,
  };
}

// THE DOCUMENT ABSTRACT (operator annotation vibe_1785602331813_gvku9sh2s):
// "the top half ... shows the doc selected distilled summary abstract ... an
// abstract that surfaces the key items delivered by doc."
//
// SCOPE RULED (Brett, 2026-08-03): "header + structure, honestly labelled" —
// the facts the snapshot ALREADY indexes for this document. It is NOT an AI
// distillation, and nothing built from it may caption it as one; a surface
// that claims an analysis nobody ran is worse than one that shows less.
//
// The five completeness signals travel WITH the score deliberately: 0.65 says
// nothing a reader can act on, while "open_markers count 3" says which part is
// thin. `destinations` is the closest thing the snapshot has to "what this
// document delivers" — the capabilities and topics it feeds.
//
// Pure: reads one document object, touches no DOM, fetches nothing.
export function documentAbstract(doc) {
  if (!doc || typeof doc !== "object") return null;
  const path = typeof doc.path === "string" ? doc.path : "";
  const title = path ? path.split("/").pop() : (doc.id || "(unnamed)");
  const completeness = doc.completeness && typeof doc.completeness === "object"
    ? doc.completeness : null;
  const SIGNALS = ["structure", "length", "open_markers",
                   "keyword_coverage", "link_degree"];
  const signals = [];
  if (completeness) {
    for (const name of SIGNALS) {
      const entry = completeness[name];
      if (entry && typeof entry === "object") {
        signals.push(Object.freeze({
          name, value: entry.value, count: entry.count,
        }));
      }
    }
  }
  const lands = [];
  const destinations = doc.destinations && typeof doc.destinations === "object"
    ? doc.destinations : {};
  for (const [kind, names] of Object.entries(destinations)) {
    for (const name of (Array.isArray(names) ? names : [])) {
      lands.push(kind + ": " + name);
    }
  }
  const topics = Array.isArray(doc.topics) ? doc.topics.slice() : [];
  const summary = typeof doc.summary === "string" && doc.summary
    ? doc.summary : null;
  // An absence is STATED, never rendered as an empty box: a document the
  // snapshot carries no derivation for looks identical to one with nothing to
  // say unless the surface says which it is.
  const note = (!summary && !topics.length && !signals.length && !lands.length)
    ? "this document is referenced but not catalogued in this snapshot, so "
      + "there is nothing derived to show"
    : null;
  return Object.freeze({
    path, title, summary, topics,
    stage: doc.stage || null,
    kind: doc.kind || null,
    score: completeness && typeof completeness.score === "number"
      ? completeness.score : null,
    signals: Object.freeze(signals),
    lands: Object.freeze(lands),
    note,
  });
}

// ---- the docs pane's wheel ---------------------------------------------------
//
// A DRUM IS ONE REEL, and the docs pane groups its documents into sections (the
// tile's own topic folder, then whatever it inherits from the scope above it).
// Putting the wheel in the lower half therefore means flattening those sections
// into one ordered list.
//
// The section is not decoration to be dropped in the flattening: an INHERITED
// document is not this tile's own, and that distinction is the whole reason the
// headings existed. So every entry carries the section it came from and whether
// it was inherited, and the wheel renders that on the tile's sub-line — the slot
// where the deck shows a link degree. Nothing the headings said is lost; it just
// travels with the tile instead of sitting above a group of them.
export function docWheelEntries(scope) {
  const out = [];
  for (const section of scope?.sections || []) {
    for (const row of section.documents || []) {
      out.push(docWheelEntry(section, row));
    }
  }
  return out;
}

// ONE tile's worth of it. Split out of the loops above so each half stays
// readable: the loops are about flattening sections, this is about what a
// single document contributes.
function docWheelEntry(section, row) {
  const path = typeof row.path === "string" ? row.path : "";
  const score = row.completeness?.score;
  return Object.freeze({
    path,
    label: path ? path.split("/").pop() : "(unnamed)",
    section: section.label || "",
    inherited: !!section.inherited,
    // `resolved` is absent on rows the snapshot fully catalogued; only an
    // explicit false means "not a catalogued corpus document".
    resolved: row.resolved !== false,
    stage: row.doc?.stage || null,
    kind: row.doc?.kind || null,
    // THE SCORE TRAVELS ONTO THE TILE. The flat list this wheel replaces drew a
    // completeness bar on every row, which is how a human spotted the thin
    // document without opening any of them. The abstract above shows the
    // selected document's score AND its five signals, so the DETAIL is not
    // lost — but comparison across documents would be, and that was the bar's
    // real job. It rides in the slot the deck's tiles use for link degree. A
    // document the snapshot never scored keeps a null here and renders the
    // deck's "·", never a zero-width bar.
    score: typeof score === "number" ? score : null,
    row,
  });
}
