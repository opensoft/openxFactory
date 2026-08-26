# Synthesis: Surface and Layer Graph Placement — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Graphify-centered document navigation, role-specific Omnigent code intelligence, and purpose-specific Hermes graph bindings form one coherent placement model when each surface receives only the graph suited to its owned work.
Topics: polyglot-graph-memory, graph-surface-placement, doxbench-graphify, omnigent-code-intelligence, hermes-layer-placement, synthesis
Repository context: openxFactory (cross-surface placement across doxBench, three-layer Hermes, and Omnigent)
Captured: 2026-07-30

## Possible feats

- **xFactory graph placement map** — declare which graph functions belong to each development surface, Hermes layer, DomainxFactory, and Omnigent worker class.
- **Domain graph-binding overlays** — specialize the neutral placement map without changing the gateway contract.
- **Graph-context handoff map** — show how a surface or worker receives bounded graph context from the owning layer.

## Members and their joints

Atomic members:
[doxBench Graphify Projection](polyglot-graph-memory-doxbench-graphify.md),
[Omnigent Code-Intelligence Graph Composition](polyglot-graph-memory-omnigent-code-intelligence.md),
and
[Hermes Layer Graph Placement](polyglot-graph-memory-hermes-layer-placement.md).

```text
development/document surface       governed runtime layers

doxBench                           Domain / Tenant / Subject Hermes
  Graphify + deterministic data      own meaning, policy, facts, evidence
       |                                      |
       +----------- bounded context ----------+
                                              |
                                         Omnigent workers
                                   navigate -> generate -> verify
```

### Surface follows question

doxBench asks how governance documents, topics, changes, schemas, and
rationales relate. Graphify can be its main semantic graph while the
deterministic dashboard snapshot continues to answer lifecycle and freshness
questions.

Omnigent asks what code, configuration, routes, types, or processes a bounded
job touches. CodeGraph or codebase-memory-mcp can answer the common execution
questions, while a licensed specialist such as GitNexus may answer narrower
cross-repository, API, data-dependence, or taint questions.

The product names are secondary to the functional separation.

### Ownership follows layer

Hermes does not inherit a graph because a nearby surface or worker uses it.
The owning layer chooses an approved provider route for its truth:

- Subject Hermes owns subject-specific evidence and state;
- Tenant Hermes owns local organizational systems, policy, and mappings;
- Domain Hermes owns reusable ontology and reviewed knowledge;
- Omnigent receives bounded context for execution but owns none of those
  authority boundaries.

The same physical provider may serve several isolated roles, but the requests,
bindings, scopes, policies, and packets remain distinct.

### Domain specialization follows subject

Project Hermes in codexFactory has a natural use for code graphs because its
subject is a repository or project. Patient Hermes needs temporal claims and
evidence instead. Managed System Hermes benefits from service, resource, and
dependency graphs. A neutral layer contract must permit these differences
rather than encode software-engineering assumptions into every domain.

### Handoff follows purpose

A layer or development surface should send workers only the subgraph needed
for an approved purpose. Provider databases do not become common shared
memory merely because several actors can query them.

For example, a codexFactory verification packet may combine:

- Domain Hermes ontology and practice context;
- Project Hermes repository/ref identity and current graph projection;
- Tenant Hermes policy and integration boundaries;
- CodeGraph navigation evidence;
- codebase-memory-mcp verification evidence.

Each contribution retains its owner and source.

## Emergent behavior

The combined placement model allows xFactory to exploit specialized graph
products without introducing a universal graph dependency. Surfaces can evolve
independently, DomainxFactories can choose appropriate graph families, and
workers can gain independent structural checks while the layer model remains
stable.

It also creates an intelligible migration path: a provider can be replaced for
one function without changing every Hermes layer or doxBench.

## Tensions to hold

- Provider specialization improves fit but increases operational and identity
  complexity.
- Shared physical infrastructure can reduce cost but may weaken isolation.
- Independent verification improves assurance but may duplicate parser errors
  or indexing cost.
- doxBench benefits from semantic inference, while governance views must not
  imply that inference changed lifecycle state.
- Domain specialization must remain possible without losing cross-domain
  observability and conformance.

## Recombination opportunities

- Combine the doxBench graph with workbench sets so a user can query or
  visualize only a selected document cluster.
- Combine Domain Hermes ontology profiles with graph-provider selection so
  workers receive both semantic meaning and instance/code relationships.
- Combine Omnigent provider disagreement with the existing challenge and
  assemble-for-admission archetypes.
- Combine Tenant Hermes project catalogs with multi-repository graph groups
  after licensing and source-isolation questions are resolved.

## Open questions

- Does the first proof target doxBench, codexFactory Omnigent, or a paired
  pilot that tests both sides of the placement model?
- Which placement choices are neutral defaults versus domain overlay
  decisions?
- Can one graph-context packet compose contributions from several owning
  layers without obscuring their distinct rails?
- Which provider capabilities should be visible in a dashboard for operators
  to understand routing and degraded modes?
