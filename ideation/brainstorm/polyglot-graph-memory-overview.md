# Polyglot Graph Memory Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: xFactory can use different graph engines across doxBench, Hermes layers, DomainxFactories, and Omnigent workers while preserving one neutral contract for identity, provenance, scope, routing, bounded context, and authority.
Topics: polyglot-graph-memory, graph-memory, graph-provider-routing, memory-gateway, ideation-dashboard, hermes, omnigent, graphify, codegraph, codebase-memory-mcp
Repository context: openxFactory (cross-factory graph-memory and graph-provider architecture)
Captured: 2026-07-30

## Possible feats

- **Polyglot graph-memory program** — define neutral provider, context,
  projection, and conformance contracts, then prove them through doxBench and
  codexFactory Omnigent pilots.
- **doxBench Graphify lane** — add semantic graph navigation beside the
  deterministic repository/ref snapshot.
- **Omnigent code-intelligence lane** — compose navigation, verification, and
  specialist graph providers by worker role.
- **Hermes layer graph profiles** — specialize graph roles and routes by
  layer, domain, tenant, and subject type.

## Motivation

xFactory already contains several graph-shaped systems:

- domain ontologies define reusable meaning;
- Subject Hermes evidence graphs preserve claims and uncertainty;
- traceability edges connect intent to execution and admission;
- Pattern Ledger records connect episodes, recurrence, forecasts, and
  candidates;
- doxBench renders document lifecycle and lineage;
- Omnigent workers need efficient structural understanding of code,
  configuration, and runtime systems.

These workloads should not be forced into one graph engine. Graphify is a
strong fit for document and cross-artifact discovery. CodeGraph and
codebase-memory-mcp are strong fits for code navigation and structural
analysis. GitNexus offers distinctive multi-repository, contract, API, and
program-dependence capabilities subject to its licensing boundary. Subject,
tenant, ontology, and operational graphs may require entirely different
providers.

The architecture therefore standardizes the graph boundary rather than the
graph product.

## Goals

- Let each surface, Hermes layer, DomainxFactory, and Omnigent worker use graph
  providers suited to its purpose.
- Keep provider selection declared, bounded, auditable, and replaceable.
- Preserve stable source identity and provenance across heterogeneous graph
  results.
- Distinguish canonical records and governed edges from extracted, inferred,
  and transient projections.
- Deliver bounded graph context rather than unrestricted provider access.
- Support independent verification and explicit provider disagreement.
- Reuse the existing Memory Gateway, semantic-context, traceability, ontology,
  and promotion boundaries.

## Non-goals

- Select one universal graph database or MCP server for xFactory.
- Combine all Hermes layers into a single physical knowledge graph.
- Make Graphify, CodeGraph, codebase-memory-mcp, GitNexus, or any provider a
  source of policy, consent, approval, ontology meaning, or final truth.
- Require all Omnigent workers to query multiple providers.
- Replace deterministic dashboard snapshots, canonical ontology packages,
  source claims, evidence graphs, or traceability records.
- Resolve commercial licensing or product procurement in brainstorm prose.

## What the system delivers

For developers and operators, doxBench can show both deterministic governance
state and semantic relationships among documents, changes, schemas, and
rationales.

For Omnigent, execution workers can receive compact code context from a primary
navigator, independent structural findings from a verifier, and specialist
analysis only when the task requires it.

For Hermes, each layer can bind graph providers to the truth it owns. A
software Project Hermes can use a code graph; Patient Hermes can use temporal
claims and evidence; Tenant Hermes can use organizational and operational
graphs; Domain Hermes can use ontology and reusable knowledge projections.

For xFactory governance, all those providers return stable, provenance-bearing
context through one policy and audit boundary. Findings remain derived until a
governed destination accepts them.

## System model

```text
canonical sources and governed records
  Git · OpenSpec · contracts · ontology · claims · runtime ledgers
                              |
                   provider-specific extraction
                              |
       +----------------------+----------------------+
       |                      |                      |
   Graphify              CodeGraph / CBM      domain-native graphs
 documents + rationale     code structure       evidence / ontology /
                                               operations / time
       +----------------------+----------------------+
                              |
               xFactory Memory Gateway boundary
          identity · provenance · purpose · scope · rails
              provider role · freshness · audit · cost
                              |
                    bounded graph context
                              |
       +----------------------+----------------------+
       |                      |                      |
    doxBench            Hermes layers          Omnigent workers
 navigation          owned truth/decisions     bounded execution
```

Canonical ontology meaning, source records, and approved traceability remain
outside provider authority. Provider graphs are projections that can be
rebuilt, compared, migrated, or retired.

## Cluster map

- [Synthesis: Surface and Layer Graph Placement](polyglot-graph-memory-synthesis-surface-and-layer-placement.md)
  — places Graphify, code-intelligence tools, domain-native graphs, Hermes
  ownership, and Omnigent consumption by function.
- [Synthesis: Provider Routing and Graph Governance](polyglot-graph-memory-synthesis-routing-and-governance.md)
  — connects the provider portfolio to a neutral contract, stable identity,
  projection authority, disagreement, promotion, and migration.

## How it fits

The proposal reuses several established xFactory seams:

- the Memory Gateway already defines provider profiles, bindings, mappings,
  graph-store and expert-tool-memory roles, bounded context, rails, audit, and
  migration;
- the domain ontology layer already requires storage and reasoner neutrality
  and prevents semantic inference from authorizing;
- the governed-derived-model pattern keeps derived artifacts pinned to
  canonical inputs;
- Subject Hermes already distinguishes claims, evidence graphs, current state,
  memory, and promotion candidates;
- traceability already defines durable typed edges with evidence;
- doxBench already treats the dashboard as a derived projection and has a
  `(repository, ref)` snapshot-source seam;
- Omnigent already has worker archetypes, typed task graphs, bounded semantic
  context, challenge, and assemble-for-admission roles.

The proposed change is a graph-specific interoperability layer and placement
model over those foundations. It does not require them to surrender ownership.

The current `add-dashboard-repo-selector` change should finish its existing
scope. A Graphify projection is a successor feat because it adds a new
semantic data lane rather than changing the selector's source seam.

## Key decisions and open questions

Load-bearing ideas captured here:

- use a provider portfolio, not a universal graph engine;
- select providers by surface, layer, domain, purpose, and worker role;
- permit different providers among the three Hermes layers and between Hermes
  and Omnigent;
- use Graphify as the main semantic graph candidate for doxBench while
  retaining deterministic lifecycle authority;
- use CodeGraph and codebase-memory-mcp as complementary Omnigent candidates,
  with roles determined by evaluation rather than branding;
- treat GitNexus as a specialist candidate whose current noncommercial license
  requires resolution before commercial adoption;
- standardize graph identity, provenance, scope, freshness, evidence class,
  bounded output, disagreement, and promotion behavior;
- preserve the authority firewall: graph traversal and inference never grant
  access or execute a gate.

Open decisions include:

- whether the first governed change extends `memory-gateway` or introduces a
  new graph-provider capability composed with it;
- the minimum stable entity/edge kernel across code, documents, ontology,
  evidence, and operational graphs;
- the first paired pilot and its evaluation corpus;
- which provider combinations truly add independent assurance;
- projection retention, privacy, erasure, and bitemporal requirements;
- whether provider products are fixed in overlays or selected per job from an
  approved capability set.

## Document map

### Tier 2: syntheses

- [Surface and Layer Graph Placement](polyglot-graph-memory-synthesis-surface-and-layer-placement.md)
- [Provider Routing and Graph Governance](polyglot-graph-memory-synthesis-routing-and-governance.md)

### Tier 1: atomic documents

- [Graph Provider Portfolio](polyglot-graph-memory-provider-portfolio.md)
- [doxBench Graphify Projection](polyglot-graph-memory-doxbench-graphify.md)
- [Omnigent Code-Intelligence Graph Composition](polyglot-graph-memory-omnigent-code-intelligence.md)
- [Hermes Layer Graph Placement](polyglot-graph-memory-hermes-layer-placement.md)
- [Graph Provider Contract](polyglot-graph-memory-provider-contract.md)
- [Derived Graph Projection Authority](polyglot-graph-memory-projection-authority.md)
