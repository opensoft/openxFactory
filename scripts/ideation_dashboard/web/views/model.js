// Snapshot -> funnel view-model derivation. PURE: no DOM, no I/O, no external
// imports — it is imported by funnel.js in the browser AND unit-tested from
// Python via node (tests/ideation-dashboard/test_renderer.py). The renderer
// reads ONLY the snapshot; this module NEVER re-derives tallies or readiness
// (those are carried through verbatim from the snapshot fields). It only lays
// out the six funnel columns and the per-hop edges between snapshot entities.
//
// Six-column docs-first funnel (spec "Realization funnel model"):
//   docs -> clusters -> possibles -> staged picks -> proposals -> realized
// Edge kinds match the mockup's SVG classes:
//   topic  doc->cluster and cluster->possible (many-to-many Topics claims)
//   pick   possible->staged (organize-gate pick edge)
//   flow   staged->change   (proposal/archive gate flow)

export const COLUMN_KEYS = ["docs", "clusters", "possibles", "staged", "proposals", "realized"];

function sanitize(id) {
  return String(id).replace(/[^a-zA-Z0-9_-]/g, "_");
}

// Deterministic, collision-free DOM ids. Column prefix rules out cross-column
// collisions; a numeric suffix disambiguates any within-column sanitize clash.
function domIdFactory() {
  const seen = new Set();
  return (columnKey, snapshotId) => {
    const base = columnKey + "-" + sanitize(snapshotId);
    let domId = base;
    let n = 2;
    while (seen.has(domId)) domId = base + "--" + n++;
    seen.add(domId);
    return domId;
  };
}

export function buildFunnelModel(snapshot) {
  const s = snapshot || {};
  const documents = s.documents || [];
  const clusters = s.clusters || [];
  const possibles = s.possibles || [];
  const stagedTopics = s.staged_topics || [];
  const changes = s.changes || [];

  const makeDomId = domIdFactory();
  const registry = new Map(); // `${columnKey}::${snapshotId}` -> node

  function register(columnKey, snapshotId, extra) {
    const domId = makeDomId(columnKey, snapshotId);
    const node = Object.assign({ column: columnKey, id: snapshotId, domId }, extra);
    registry.set(columnKey + "::" + snapshotId, node);
    return node;
  }
  function resolve(columnKey, snapshotId) {
    return registry.get(columnKey + "::" + snapshotId) || null;
  }

  const docNodes = documents.map((d) => register("docs", d.id, { document: d }));
  const clusterNodes = clusters.map((c) => register("clusters", c.id, { cluster: c }));
  const possibleNodes = possibles.map((p) => register("possibles", p.id, { possible: p }));
  const stagedNodes = stagedTopics.map((t) => register("staged", t.staging_id, { staged: t }));

  // A change is exactly one node: active -> proposals column, archived -> realized.
  const proposals = changes.filter((c) => c.status === "active");
  const realized = changes.filter((c) => c.status === "archived");
  const proposalNodes = proposals.map((c) => register("proposals", c.id, { change: c }));
  const realizedNodes = realized.map((c) => register("realized", c.id, { change: c }));
  const changeColumn = new Map();
  proposals.forEach((c) => changeColumn.set(c.id, "proposals"));
  realized.forEach((c) => changeColumn.set(c.id, "realized"));

  const edges = [];
  function link(fromNode, toNode, kind) {
    if (fromNode && toNode) {
      edges.push({
        from: fromNode.domId, to: toNode.domId, kind,
        fromColumn: fromNode.column, toColumn: toNode.column,
      });
    }
  }

  // doc -> cluster (topic): strictly the snapshot's Topics-derived document_edges
  for (const c of clusters) {
    for (const e of c.document_edges || []) {
      link(resolve("docs", e.document), resolve("clusters", c.id), "topic");
    }
  }
  // cluster -> possible (topic): the many-to-many claiming_clusters edges
  for (const p of possibles) {
    for (const cid of p.claiming_clusters || []) {
      link(resolve("clusters", cid), resolve("possibles", p.id), "topic");
    }
  }
  // possible -> staged (pick): the organize-gate pick edge
  for (const p of possibles) {
    const sid = p.pick && p.pick.staging_id;
    if (sid) link(resolve("possibles", p.id), resolve("staged", sid), "pick");
  }
  // staged -> change (flow): the proposal/archive gate flow
  for (const t of stagedTopics) {
    const cid = t.target_change;
    if (cid) link(resolve("staged", t.staging_id), resolve(changeColumn.get(cid), cid), "flow");
  }

  const columns = [
    { key: "docs", label: "source docs", gate: "Topics: header", collapsible: true, nodes: docNodes },
    { key: "clusters", label: "topic cluster", collapsible: false, nodes: clusterNodes },
    { key: "possibles", label: "possibles", gate: "→ organize gate", collapsible: false, nodes: possibleNodes },
    { key: "staged", label: "staged picks", gate: "→ proposal gate", collapsible: false, nodes: stagedNodes },
    { key: "proposals", label: "proposals", gate: "→ archive gate", collapsible: false, nodes: proposalNodes },
    { key: "realized", label: "realized", collapsible: false, nodes: realizedNodes },
  ];

  return { columns, edges, resolve, registry };
}

// The five-column collapse hides the docs column. Edges touching a hidden column
// vanish — the SAME rule the CSS collapse enacts (the funnel's offsetParent
// guard). Exposed purely so the collapse is testable without a DOM.
export function collapsedColumnKeys(collapsed) {
  return collapsed ? new Set(["docs"]) : new Set();
}

export function visibleEdges(model, opts) {
  const collapsed = !!(opts && opts.collapsed);
  const hidden = collapsedColumnKeys(collapsed);
  return model.edges.filter((e) => !hidden.has(e.fromColumn) && !hidden.has(e.toColumn));
}
