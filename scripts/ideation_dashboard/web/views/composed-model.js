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
