# Graph Provider Contract — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A neutral graph-provider contract can let heterogeneous graph engines return interoperable, provenance-bearing, purpose-bound context through the existing xFactory Memory Gateway.
Topics: polyglot-graph-memory, graph-provider-contract, memory-gateway, provider-profile, context-packet, traceability, source-authority
Repository context: openxFactory (candidate neutral contract family extending existing memory-gateway provider and context seams)
Captured: 2026-07-30

## Possible feats

- **Graph provider profile** — declare graph capabilities, roles, scopes, freshness behavior, query classes, and companion requirements.
- **Graph query and context packet** — normalize a graph request and return only the bounded subgraph needed for one approved purpose.
- **Stable graph entity and edge references** — map provider-native identifiers to exact repository, document, contract, ontology, or runtime sources.
- **Graph projection manifest** — make rebuildable graph artifacts reproducible and freshness-checkable.

## Focus

This document isolates the common interface that allows provider diversity
without leaking provider semantics into Hermes or Omnigent. xFactory already
has product-neutral provider profiles, bindings, mappings, graph-store roles,
expert tool memory, and bounded context packets. A graph-specific family could
specialize those seams rather than create a second gateway.

## Proposed model

Candidate contract shapes:

```text
graph-provider-profile
graph-query-request
graph-context-packet
graph-entity-reference
graph-edge-with-provenance
graph-projection-manifest
```

### Provider profile

A profile could declare:

- provider and adapter identity;
- supported graph roles and layers;
- corpus and source kinds;
- query capabilities such as search, neighbors, path, impact, temporal, raw
  graph query, process, API-shape, or evidence support;
- read/write behavior;
- incremental, ref-pinned, and branch/worktree freshness behavior;
- deterministic and model-assisted extraction classes;
- source exposure and network behavior;
- required companion ports;
- unsupported content and query classes;
- erasure, retention, migration, cost, and license characteristics.

### Query request

A request could carry:

```yaml
purpose: implementation_impact
consumer_layer: domain_omnigent
provider_role: verifier
source_scope:
  repository: codexFactory
  ref: <exact-ref-or-worktree-id>
  revision: <expected-sha>
query:
  kind: blast_radius
  subject_ref: code://codexFactory@<sha>/path.py#symbol
limits:
  max_nodes: 50
  max_depth: 4
  max_source_bytes: 20000
required_evidence:
  - source_location
  - extraction_class
  - graph_revision
```

The request also inherits the gateway's caller, workflow, policy, budget,
credential-binding, audit, and allowed-use framing.

### Bounded graph context

The response should contain:

- query and provider identities;
- exact source and graph revisions;
- stable entity references;
- bounded nodes and edges;
- source locations or excerpts where allowed;
- `extracted`, `inferred`, `asserted`, or `approved` evidence class;
- confidence, coverage, truncation, and unresolved symbols;
- freshness and expiry;
- conflicts or verifier disagreement;
- allowed and prohibited uses;
- audit and usage references.

Illustrative stable references:

```text
code://codexFactory@<sha>/path.py#qualified.symbol
doc://openxFactory@<sha>/docs/file.md#heading
contract://openxFactory/memory-gateway/context-packet@v1
ontology://<package-id>@<digest>/<term-id>
runtime://<tenant>/<subject>/<object-id>@<version>
```

These are design sketches, not selected URI grammar.

### Composition

The gateway may invoke one primary and zero or more companion, verifier, or
fallback providers. It should merge findings only after identity mapping.
Provider disagreement remains explicit; a union is not automatically truth.

## Interfaces and boundaries

The contract extends the existing Memory Gateway rather than replacing it.
Provider bindings retain credential custody, allowed routes, and migration
state. Context packets remain purpose-bound and expire.

The graph contract does not:

- define ontology meaning;
- grant consent, authority, approval, or cross-layer access;
- require one storage or query model;
- expose provider credentials or unrestricted graph endpoints to workers;
- declare a provider result canonical;
- require all providers to implement every query kind.

The existing semantic-context block and graph context solve different
problems. Semantic context pins the meaning of terms. Graph context carries
bounded relationships among particular artifacts or instances. A packet may
carry both, and their pins must agree where ontology terms classify graph
entities.

## Alternatives and tensions

**Use each provider's MCP schema directly** avoids adapter work but pushes
provider-specific tool names, node identities, result shapes, and freshness
semantics into every worker.

**Normalize only at the prompt layer** is flexible but makes validation,
metering, migration, and audit dependent on prose.

**Choose a universal graph query language** simplifies provider access but
does not solve identity, provenance, scope, lifecycle, or authority. Cypher or
GraphQL may be an adapter-level capability without becoming the xFactory
contract.

A richly normalized graph can erase useful provider-specific evidence. The
common packet should therefore carry a small stable kernel plus typed
provider-extension artifacts when needed.

## Open questions

- Should graph context extend the current expert context packet or be a
  separately referenced artifact?
- Which stable reference grammars already exist and should be reused rather
  than introducing new schemes?
- Is raw graph query ever allowed for workers, or only for bounded verifier
  profiles?
- How should the gateway map two providers that resolve the same source symbol
  at different granularities?
- Which coverage and freshness fields are mandatory before a graph result may
  support admission evidence?

## Relationships

- [Graph Provider Portfolio](polyglot-graph-memory-provider-portfolio.md)
  supplies routing roles and admission concerns.
- [Derived Projection Authority](polyglot-graph-memory-projection-authority.md)
  supplies evidence classes and lifecycle rules.
- [Synthesis: Provider Routing and Governance](polyglot-graph-memory-synthesis-routing-and-governance.md)
  connects this interface to provider selection and promotion.
- Existing design context:
  [Hermes Retrieval Primitives](hermes-retrieval-primitives-contract.md) and
  [Ontology Semantic-Context Compilation](ontology-semantic-context-compilation.md).
