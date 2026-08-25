// Composed-view MODEL (add-project-merged-projection, topic decisions
// D9/D10 + design D-f). PURE derivation over a composed snapshot — no DOM,
// no fetch, no imports — node-harness testable like the sibling models.
//
// A composed snapshot is the registry's aggregate composition: every item
// namespaced `repo::id`, every item carrying its `repository`, and
// `generation.composed_from` naming the member (repository, ref,
// source_revision) triples. THIS module owns the three view rules built on
// that substrate:
//
//   * D9  — the CLUSTER UNION: same-topic clusters from different member
//     repositories render as ONE merged tile; the composition's namespacing
//     is never touched (the union is a display grouping, not an identity
//     claim);
//   * D10 — the READ-ONLY plane: `readOnlyCaps` strips every acting
//     capability, so the one capability object the app shell hands the
//     views is what hides the affordances (no view grows its own check);
//   * D-f — the union KEY is the namespaced id's topic tail (`cl-…`), which
//     is generator-minted vocabulary, never free text.

// A composed snapshot is recognized by the block composition stamps — no
// second flag exists or is needed.
export function isComposed(snapshot) {
  return Array.isArray(snapshot?.generation?.composed_from);
}

// `repo::cl-topic` -> `cl-topic`; a plain id (non-composed data) is its own
// tail, so the same code path serves both planes.
export function topicTail(id) {
  const text = id == null ? "" : String(id);
  const at = text.indexOf("::");
  return at < 0 ? text : text.slice(at + 2);
}

// The member ref for a repository, from the composition stamps — the jump
// verb's target ref (D10). Default ref when the stamps do not name one.
export function memberRef(snapshot, repository) {
  const members = snapshot?.generation?.composed_from;
  if (!Array.isArray(members)) return "main";
  const member = members.find((m) => m && m.repository === repository);
  return (member && member.ref) || "main";
}

function sumTallies(clusters) {
  const out = {};
  for (const cluster of clusters) {
    for (const [key, value] of Object.entries(cluster.tallies || {})) {
      if (typeof value === "number") out[key] = (out[key] || 0) + value;
    }
  }
  return out;
}

// D9 — the union. Groups a composed snapshot's clusters by topic tail and
// merges each group into one tile-bearing cluster:
//   id       the TAIL (unnamespaced; unique across the union by construction)
//   name     the first member's name (same topic, same vocabulary)
//   document_edges  concatenated (they reference namespaced doc ids, which
//            exist verbatim in the composed documents collection)
//   tallies  summed per key
//   repositories    every contributing repository, member order
//   composed_members  the original clusters, untouched, for drill-in
// A single-member group keeps the merged SHAPE so both cases render through
// one path; non-cluster collections are never touched here.
export function unionClusters(clusters) {
  const groups = new Map();
  for (const cluster of clusters || []) {
    if (!cluster || typeof cluster !== "object") continue;
    const tail = topicTail(cluster.id);
    if (!groups.has(tail)) groups.set(tail, []);
    groups.get(tail).push(cluster);
  }
  const merged = [];
  for (const [tail, members] of groups) {
    const repositories = [];
    for (const member of members) {
      if (member.repository && !repositories.includes(member.repository)) {
        repositories.push(member.repository);
      }
    }
    merged.push({
      id: tail,
      name: members[0].name || tail,
      topics: members[0].topics,
      document_edges: members.flatMap((m) => m.document_edges || []),
      tallies: sumTallies(members),
      lineage: members[0].lineage,
      repositories,
      composed_members: members,
    });
  }
  return merged;
}

// The snapshot the VIEWS render: clusters unioned, everything else exactly
// the composition's output. A non-composed snapshot passes through untouched.
export function composedView(snapshot) {
  if (!isComposed(snapshot)) return snapshot;
  return { ...snapshot, clusters: unionClusters(snapshot.clusters) };
}

// ---- the VISIBLE set (topic D19, Brett's 2026-08-07 ruling) --------------

// The composed collections a visibility filter applies to. Every one of them
// carries per-item `repository` by construction of the composition, which is
// exactly what makes ONE uniform filter possible.
export const COMPOSED_COLLECTIONS = [
  "documents", "clusters", "possibles", "staged_topics", "changes",
  "keyword_index",
];

export const VIEW_UNION = "union";
// NOT "intersection": Brett's D20 refinement made the second mode SHARED —
// carried by two or more of the visible repositories, not by every one of
// them — because strict intersection over a real five-factory project keeps
// almost nothing, while the overlap is where the convergence lives. The name
// follows the rule so the code cannot claim a set operation it is not doing.
export const VIEW_SHARED = "shared";

// The item's cross-repository identity: the namespaced id's tail, or the
// unnamespaced key a collection uses instead (`staging_id`, `keyword`).
// `topicTail` returns a plain value unchanged, so one expression serves all.
export function itemTail(item) {
  if (!item || typeof item !== "object") return "";
  return topicTail(item.id != null ? item.id
    : (item.staging_id != null ? item.staging_id : item.keyword));
}

// D19 — the composed snapshot narrowed to the VISIBLE member repositories,
// under one of two set modes:
//
//   union    every item belonging to a visible repository;
//   shared   only items whose identity is carried by TWO OR MORE of the
//            visible repositories — "where do these repositories converge?".
//
// D20 (Brett, 2026-08-07) set the shared threshold at two rather than all:
// across the five-factory `domains` project, strict all-of-them keeps 2
// document identities while two-or-more surfaces the 8 cluster topics the
// factories actually converge on. With two repositories visible the rules
// coincide, so the refinement only shows above that — and narrowing to a
// pair remains the sharpest comparison, now one `none` + two ticks away.
//
// Shared FILTERS, it never merges: each repository's own copy stays its own
// row (badged, and openable in its own repo), which is what makes comparing
// two factories' takes on the same document possible. Clusters are merged
// afterwards by the union rule exactly as before, so filtering first and
// unioning second keeps tallies honest for the visible set.
//
// `visible` null/undefined means EVERY member (the composition's own answer).
// `generation.composed_from` is trimmed to the visible members so the
// freshness header states the view actually rendered, never the superset.
// A non-composed snapshot passes through untouched.
export function visibleSnapshot(snapshot, visible, mode) {
  if (!isComposed(snapshot)) return snapshot;
  const members = snapshot.generation.composed_from
    .map((m) => m && m.repository).filter(Boolean).map(String);
  const wanted = visible == null
    ? members
    : members.filter((r) => visible.map(String).includes(r));
  const keep = new Set(wanted);
  const out = { ...snapshot };
  for (const collection of COMPOSED_COLLECTIONS) {
    const items = snapshot[collection];
    if (!Array.isArray(items)) continue;
    let kept = items.filter(
      (item) => item && keep.has(String(item.repository)));
    if (mode === VIEW_SHARED && keep.size > 1) {
      const carriers = new Map();
      for (const item of kept) {
        const tail = itemTail(item);
        if (!carriers.has(tail)) carriers.set(tail, new Set());
        carriers.get(tail).add(String(item.repository));
      }
      kept = kept.filter((item) => carriers.get(itemTail(item)).size >= 2);
    }
    out[collection] = kept;
  }
  out.generation = {
    ...snapshot.generation,
    composed_from: snapshot.generation.composed_from.filter(
      (m) => m && keep.has(String(m.repository))),
  };
  return out;
}

// D10 — the read-only capability object for a composed render: every acting
// capability off, the probe's read-only facts (refresh binding, actor)
// untouched. The views already hide their affordances on these flags, so
// this ONE derivation is the whole gating.
export function readOnlyCaps(caps) {
  return {
    ...(caps || {}),
    actions: {
      ...(caps?.actions || {}),
      gate: false,
      notebook: false,
      session: false,
      edit: false,
    },
  };
}

// ---- the REPOSITORY VOCABULARY (D21, Brett's 2026-08-07 observation) ------
//
// "Our repo selector is now very similar to the lens function but for
// documents in repos vs keywords in documents." It is the same shape, and
// this projection is the whole adapter: the composed snapshot is re-expressed
// in the SHAPE the keyword lens already reads, so `buildLensModel` and
// `renderBullseye` serve the repository vocabulary unchanged.
//
//   keyword lens                 repository lens
//   ------------                 ---------------
//   keyword                      member repository
//   document                     document IDENTITY (one row per identity,
//                                carrying every repository that has it)
//   doc carries keyword          that repository carries that identity
//   ring N = matches N checked   ring N = carried by N visible repositories
//   centre = matches ALL         carried by EVERY visible repository
//   pin = require                only identities that repository carries
//
// Which also names what the D19/D20 modes have been all along: union is
// ring >= 1, shared is ring >= 2. `copies` keeps each identity's real
// per-repository document ids so a drill-in scopes back to actual documents
// rather than to the projection's synthetic rows.
export function repositoryVocabulary(snapshot) {
  if (!isComposed(snapshot)) return null;
  const members = snapshot.generation.composed_from
    .map((m) => m && m.repository).filter(Boolean).map(String);
  const byIdentity = new Map();
  for (const doc of snapshot.documents || []) {
    if (!doc || !doc.repository) continue;
    const identity = itemTail(doc);
    if (!identity) continue;
    if (!byIdentity.has(identity)) {
      byIdentity.set(identity, { repositories: [], copies: [], summary: null });
    }
    const row = byIdentity.get(identity);
    const repository = String(doc.repository);
    if (!row.repositories.includes(repository)) row.repositories.push(repository);
    row.copies.push(String(doc.id));
    if (!row.summary && doc.summary) row.summary = doc.summary;
  }
  const documents = [...byIdentity.entries()]
    .sort((a, b) => (a[0] < b[0] ? -1 : (a[0] > b[0] ? 1 : 0)))
    .map(([identity, row]) => ({
      id: identity,
      path: identity,
      // `topics` IS the vocabulary the lens reads — here, the carriers.
      topics: members.filter((m) => row.repositories.includes(m)),
      summary: row.summary,
      repositories: row.repositories,
      copies: row.copies,
    }));
  const counts = new Map(members.map((m) => [m, 0]));
  for (const doc of documents) {
    for (const repository of doc.topics) {
      counts.set(repository, (counts.get(repository) || 0) + 1);
    }
  }
  return {
    repository: snapshot.repository,
    generation: snapshot.generation,
    documents,
    keyword_index: members.map((m) => ({
      keyword: m, declared_doc_count: counts.get(m) || 0,
    })),
    clusters: [], possibles: [], staged_topics: [], changes: [],
  };
}

// D21 — the DRILL-IN target: the document identities behind one bullseye
// region. A SECTOR names an exact repository combination; the CENTRE names
// every checked repository. In both cases the identity qualifies only when
// the repositories carrying it — counted within the checked set — are exactly
// that combination, which is what makes a sector "these and no others".
export function identitiesFor(vocabulary, checked, region) {
  const inPlay = (checked || []).map(String);
  const carriers = new Set((region?.kind === "centre"
    ? inPlay : (region?.keywords || []).map(String)));
  if (!carriers.size) return [];
  const out = [];
  for (const doc of vocabulary?.documents || []) {
    const carried = (doc.topics || []).map(String).filter((r) => inPlay.includes(r));
    if (carried.length === carriers.size
        && carried.every((r) => carriers.has(r))) {
      out.push(String(doc.id));
    }
  }
  return out;
}

// D21 — the composed snapshot narrowed to a set of document identities. The
// scope is a DOCUMENT SET and every other plane keeps only what references
// it: a cluster survives when an edge lands on a kept document, a staged
// topic or change when one of its files is a kept path, a keyword when a kept
// document still declares it. Planes with no document relationship are left
// alone rather than silently emptied.
export function scopedSnapshot(snapshot, identities) {
  if (!snapshot || !Array.isArray(identities)) return snapshot;
  const wanted = new Set(identities.map(String));
  const documents = (snapshot.documents || []).filter(
    (d) => d && wanted.has(itemTail(d)));
  const keptIds = new Set(documents.map((d) => String(d.id)));
  const keptPaths = new Set(documents.map((d) => String(d.path || itemTail(d))));
  const touches = (files) => (files || []).some((f) => keptPaths.has(
    String(f && f.path ? f.path : f)));
  const out = { ...snapshot, documents };
  if (Array.isArray(snapshot.clusters)) {
    out.clusters = snapshot.clusters.filter((c) => (c?.document_edges || [])
      .some((e) => keptIds.has(String(e && e.document))));
  }
  for (const collection of ["staged_topics", "changes"]) {
    if (Array.isArray(snapshot[collection])) {
      out[collection] = snapshot[collection].filter((row) => touches(row?.files));
    }
  }
  if (Array.isArray(snapshot.keyword_index)) {
    const live = new Set();
    for (const doc of documents) for (const t of doc.topics || []) live.add(String(t));
    out.keyword_index = snapshot.keyword_index.filter(
      (k) => live.has(String(k && k.keyword)));
  }
  return out;
}
