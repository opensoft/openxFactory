# Graph Provider Portfolio — Brainstorm

Status: brainstorm
Kind: architecture
Summary: xFactory should select graph providers by surface, layer, domain, worker function, and evidence need instead of imposing one graph engine across the stack.
Topics: polyglot-graph-memory, graph-provider-portfolio, memory-gateway, provider-binding, routing, graph-memory
Repository context: openxFactory (neutral graph-provider selection across xFactory surfaces, Hermes layers, DomainxFactories, and Omnigent)
Captured: 2026-07-30

## Possible feats

- **Graph provider portfolio registry** — declare approved graph products, their roles, supported scopes, licensing constraints, and companion requirements.
- **Purpose-bound provider routing** — select a graph provider from the requested function and context profile rather than from a stack-wide default.
- **Provider comparison harness** — replay representative graph questions against alternative providers and retain quality, latency, freshness, and cost evidence.

## Focus

This document isolates the provider-selection principle: xFactory benefits from
several graph engines because its graph workloads do not share one corpus,
authority, query shape, update cadence, or privacy boundary.

The architectural choice is not between Graphify, CodeGraph,
codebase-memory-mcp, GitNexus, or a domain-native graph for the entire stack.
The choice is which provider role each product may fill for one bounded
purpose.

## Proposed model

Treat graph providers as a portfolio behind xFactory contracts:

```text
graph request
  -> purpose + layer + domain + source scope
  -> required query and evidence capabilities
  -> freshness + privacy + locality constraints
  -> provider-role selection
  -> bounded graph context
```

A provider may be assigned one of four composition roles:

| Role | Meaning |
| --- | --- |
| `primary` | First provider for the declared purpose and source scope. |
| `companion` | Supplies a capability the primary lacks, such as source authority, temporal evidence, or visualization. |
| `verifier` | Independently checks a structural, impact, lineage, or coverage claim. |
| `fallback` | Serves a declared degraded path when the primary is unavailable or unsuitable. |

These roles do not establish a universal ranking. Graphify may be primary for
document relationship discovery, CodeGraph primary for an implementation
worker, and a subject evidence store primary for a clinical case. The same
provider may occupy a different role in another domain or workflow.

Provider selection should consider:

- corpus: code, documents, schemas, ontology, claims, runtime topology;
- query: search, traversal, blast radius, evidence support, temporal state;
- lifecycle: immutable release, commit-scoped projection, live state;
- locality: workstation, workbench, tenant runtime, hosted control plane;
- authority: descriptive, inferred, reviewed, or canonical;
- isolation: subject, tenant, domain, repository, project group;
- freshness and branch/ref behavior;
- deterministic versus model-assisted extraction;
- cost, license, operational footprint, and migration support.

## Interfaces and boundaries

The portfolio consumes provider profiles and purpose-bound graph requests. It
emits a selected route and the provider identities used. The xFactory Memory
Gateway remains the natural policy and audit boundary because its existing
vocabulary already recognizes graph stores and expert tool memory.

The portfolio does not:

- make a provider graph authoritative merely because it was selected;
- allow a worker to choose an unrestricted graph at runtime;
- merge provider databases into one physical global graph;
- let provider-native identifiers replace stable xFactory source references;
- require Hermes layers, DomainxFactories, or Omnigent workers to share one
  backend.

## Alternatives and tensions

**One graph engine everywhere** simplifies operations and identity mapping but
forces document, code, ontology, evidence, and live-state workloads through one
provider's strengths and assumptions.

**Unrestricted per-agent choice** maximizes local flexibility but makes
provenance, costs, credentials, staleness, and reproducibility difficult to
govern.

**An xFactory-built graph engine** could fit the contracts exactly, but would
duplicate mature parsing, indexing, visualization, and query products. A
provider-neutral contract plus adapters preserves replacement leverage.

Provider plurality also creates real costs: duplicate indexes, competing node
identities, inconsistent edges, installation hooks, operational overhead, and
license review. The portfolio needs admission and retirement criteria so it
does not become a provider zoo.

## Open questions

- Which provider capabilities are required before a product can be admitted as
  `primary` rather than `verifier` or `experimental`?
- Are routes fixed in installation overlays, selected per job from an approved
  set, or both?
- Which measurements determine that two providers are redundant enough to
  retire one?
- Does commercial licensing status belong in the provider profile or in a
  companion software-bill-of-materials policy?
- Which provider failovers may happen automatically without changing the
  interpretation of returned graph context?

## Relationships

- [Graph Provider Contract](polyglot-graph-memory-provider-contract.md) defines
  the common request, response, identity, and composition shapes.
- [Derived Projection Authority](polyglot-graph-memory-projection-authority.md)
  separates provider output from governed truth.
- [Synthesis: Provider Routing and Governance](polyglot-graph-memory-synthesis-routing-and-governance.md)
  connects portfolio selection to the gateway and authority boundary.
