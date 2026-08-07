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
export const VIEW_INTERSECTION = "intersection";

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
//   union         every item belonging to a visible repository;
//   intersection  only items whose identity exists in EVERY visible
//                 repository — "what do these repositories share?".
//
// Intersection FILTERS, it never merges: each repository's own copy stays its
// own row (badged, and openable in its own repo), which is what makes
// comparing two factories' takes on the same document possible. Clusters are
// merged afterwards by the union rule exactly as before, so filtering first
// and unioning second keeps tallies honest for the visible set.
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
    if (mode === VIEW_INTERSECTION && keep.size > 1) {
      const carriers = new Map();
      for (const item of kept) {
        const tail = itemTail(item);
        if (!carriers.has(tail)) carriers.set(tail, new Set());
        carriers.get(tail).add(String(item.repository));
      }
      kept = kept.filter((item) => carriers.get(itemTail(item)).size === keep.size);
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
