# doxBench Graphify Projection — Brainstorm

Status: brainstorm
Kind: architecture
Summary: doxBench can use Graphify as its primary semantic relationship engine while retaining the deterministic repository snapshot as the authority for lifecycle, freshness, and gate state.
Topics: polyglot-graph-memory, doxbench-graphify, ideation-dashboard, graphify, doc-management, doc-workflow, lifecycle-projection
Repository context: openxFactory (doxBench and ideation-dashboard projection; realization would span codexFactory and the xFactory aggregation snapshot source)
Captured: 2026-07-30

## Possible feats

- **doxBench semantic graph view** — traverse document, topic, schema, change, validator, and rationale relationships alongside the existing lifecycle views.
- **Graph projection publication lane** — publish a commit/ref-pinned Graphify projection beside each deterministic dashboard snapshot.
- **Inferred-edge review queue** — turn useful model-derived document relationships into cited, reviewable candidates without changing source state.

## Focus

This document isolates Graphify's place in doxBench. doxBench has two
different questions:

1. What documents and governed records exist, at what lifecycle state, and at
   which source revision?
2. How are their concepts, references, rationales, schemas, and decisions
   connected?

The current snapshot generator is suited to the first question. Graphify is
suited to the second because it spans code, documents, schemas, configuration,
and other artifacts and distinguishes directly extracted edges from inferred
ones. The product source is
[Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify).

## Proposed model

Run two sibling projections over the same repository/ref:

```text
repository @ ref
  |
  +-- deterministic dashboard generator
  |     -> lifecycle, status, freshness, possibles, picks, gates
  |
  +-- Graphify
        -> semantic concepts, communities, paths, rationale and references
                         |
                         v
                    doxBench UI
```

The doxBench renderer combines the projections without confusing their
authority:

- deterministic snapshot fields render governance and lifecycle state;
- Graphify `EXTRACTED` edges render as sourced relationships;
- Graphify `INFERRED` edges render with a visibly different class;
- inferred edges may seed a candidate or workbench but cannot change a source
  document, lifecycle state, readiness score, possible disposition, pick, or
  gate outcome.

Each semantic graph projection should name:

- repository and ref;
- exact source revision;
- Graphify and graph-schema versions;
- extraction configuration and included/excluded paths;
- graph content digest;
- generated-at and freshness metadata;
- counts of extracted and inferred nodes/edges;
- unresolved or truncated inputs;
- the deterministic snapshot identity with which it may be displayed.

The active repository-selector work already establishes the load-bearing
`(repository, ref)` seam. Graphify should be an additive successor projection,
not an expansion of that nearly realized selector change.

## Interfaces and boundaries

The Graphify lane consumes repository content through a read-only, confined
source. It emits a derived graph artifact and optional report. doxBench reads
that artifact beside the deterministic snapshot.

It does not:

- replace the snapshot schema or snapshot index;
- scan repositories from the browser;
- write, move, promote, ratify, or dispose source documents;
- make semantic similarity equivalent to an explicit `Topics:` or
  traceability edge;
- execute a gate;
- allow a stale graph to appear current when the deterministic snapshot has a
  newer revision.

Graphify's model-assisted pass over documents may require a configured model
backend. That call surface, source exposure, cost, and retention behavior must
be declared rather than inherited silently from an interactive assistant.

## Alternatives and tensions

**Graphify replaces the snapshot generator** would reduce duplicate extraction
but weaken deterministic lifecycle validation and mix inferred semantics with
controlled fields.

**Graphify only as an offline analyst tool** avoids runtime integration but
loses the graph as a first-class dashboard navigation surface.

**A custom Cytoscape-only graph from snapshot edges** is deterministic and
lightweight but cannot discover relationships across prose, schemas,
rationale, and code that are not already declared.

Committing `graphify-out/` could give teams a shared map, but xFactory already
has governed publication lanes and a dirty shared-tree discipline. A dedicated
derived publication location may be safer than letting developer installs add
graph outputs and merge drivers to each source repository.

## Open questions

- Is the Graphify artifact published per repository/ref beside snapshots, or
  generated only for an active doxBench workbench?
- Which Graphify edge types may render immediately and which require a
  candidate-review queue?
- How should the UI explain a conflict between an inferred semantic edge and a
  deterministic lifecycle or provenance edge?
- Should the hosted surface use a pre-generated graph only, or may it issue
  bounded server-side Graphify queries?
- What corpus size and graph-density ceilings keep the browser view useful?

## Relationships

- [Derived Projection Authority](polyglot-graph-memory-projection-authority.md)
  defines why this graph remains rebuildable and non-authoritative.
- [Hermes Layer Graph Placement](polyglot-graph-memory-hermes-layer-placement.md)
  distinguishes this development projection from runtime layer memory.
- [Synthesis: Surface and Layer Placement](polyglot-graph-memory-synthesis-surface-and-layer-placement.md)
  connects doxBench to the wider provider map.
- Existing design context:
  [Ideation Area Dashboard](ideation-dashboard.md).
