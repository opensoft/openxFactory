# Synthesis: Provider Routing and Graph Governance — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A purpose-routed provider portfolio becomes safe and replaceable when a neutral graph contract preserves stable identity, provenance, freshness, authority class, and explicit disagreement through the Memory Gateway.
Topics: polyglot-graph-memory, graph-provider-routing, graph-provider-contract, graph-projection-authority, memory-gateway, source-authority, synthesis
Repository context: openxFactory (neutral routing, interoperability, authority, and lifecycle cluster)
Captured: 2026-07-30

## Possible feats

- **Federated graph gateway** — route graph queries to approved providers and emit one bounded, provenance-bearing context shape.
- **Graph provider conformance suite** — prove scope confinement, freshness, evidence classes, disagreement handling, and denial-before-provider-I/O.
- **Graph projection and promotion lifecycle** — govern how provider findings remain derived or nominate durable xFactory records.

## Members and their joints

Atomic members:
[Graph Provider Portfolio](polyglot-graph-memory-provider-portfolio.md),
[Graph Provider Contract](polyglot-graph-memory-provider-contract.md),
and
[Derived Graph Projection Authority](polyglot-graph-memory-projection-authority.md).

The
[Omnigent Code-Intelligence Graph Composition](polyglot-graph-memory-omnigent-code-intelligence.md)
atomic is a worked consumer of the combined model.

```text
purpose-bound request
  -> approved portfolio route
  -> provider-specific adapter/query
  -> identity + provenance normalization
  -> authority/freshness classification
  -> bounded graph-context packet
  -> advisory use or governed promotion candidate
```

### Routing depends on declared capability

The provider portfolio answers which approved product can perform the requested
query under the required scope, freshness, locality, cost, and evidence
constraints. It does not route by product preference alone.

The provider contract supplies a stable request and response kernel. An adapter
may use MCP tools, Cypher, a local library, JSON artifacts, or another native
surface internally without exposing that choice as the Hermes or Omnigent
contract.

### Identity makes composition possible

Two provider results can be compared only after they map to exact source
references. A symbol name without repository, revision, path, and qualified
identity is not enough. A document concept without its source location and
extraction method is not enough.

Identity mapping should happen before union, intersection, disagreement, or
promotion logic. Unmapped nodes remain provider-local evidence rather than
being merged by label similarity.

### Authority class controls use

The projection-authority model distinguishes canonical source objects,
governed durable edges, extracted edges, inferred edges, and transient context.
The gateway carries that distinction to the consumer.

A verifier may use an extracted call edge to target a source inspection. A
doxBench user may use an inferred document edge to form a workbench. Neither
action promotes the edge. Promotion creates a new governed record at the
appropriate destination and cites the provider finding as evidence.

### Disagreement is a first-class result

Multiple providers may disagree because of parser coverage, dynamic behavior,
stale revisions, different graph granularity, or model inference. The
composition layer should report:

- matched claims;
- conflicting claims;
- unique claims;
- missing coverage;
- revision or scope mismatch;
- the adjudication path selected.

Agreement is corroboration, not automatic authority. Disagreement is evidence
for targeted inspection, challenge, or Hermes review rather than a reason to
silently choose the larger graph.

### Migration preserves the caller

Provider routes may change without changing the graph request or bounded
context surface. Historical decisions retain the original provider and graph
projection identities. New work uses the new route after its conformance and
migration gates pass.

## Emergent behavior

This cluster turns a collection of graph products into a governed xFactory
capability. Providers compete and specialize behind a stable boundary;
workers and surfaces can request graph functions without inheriting storage
products; and useful findings can enter existing traceability, evidence,
ontology, document, or Pattern Ledger lifecycles without silent promotion.

## Tensions to hold

- A small normalization kernel preserves provider value but leaves more work
  to consumers; a rich kernel risks flattening distinctive evidence.
- Provider fallback improves availability but may change coverage or query
  semantics.
- Immutable retention supports audit but conflicts with erasure, privacy, and
  index cost.
- Raw graph query improves expert flexibility but increases scope and
  exfiltration risk.
- Model-assisted document graphs need different confidence treatment from
  deterministic source extraction.

## Recombination opportunities

- Attach semantic-context pins to graph-context packets so domain terms and
  instance relationships remain separately identifiable but mutually
  interpretable.
- Feed graph query usage, cost, and usefulness into the cost-accountability
  and provider-retirement loops.
- Use provider conformance fixtures as an Omnigent verifier task family.
- Add graph projection identities to traceability reports and admission
  evidence without making the whole graph permanent.

## Open questions

- Is graph-provider functionality an extension of `memory-gateway` or a new
  capability composed with it?
- What is the minimum identity kernel that works across code, document,
  ontology, evidence, and operational graphs?
- Which fallbacks are semantics-preserving enough to happen automatically?
- What retention rule applies when a gate cites a graph projection containing
  privacy-scoped content?
- Should provider comparison and disagreement evidence have a shared schema
  with other challenge/adjudication packets?
