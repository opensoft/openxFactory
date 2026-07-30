# Hermes Layer Graph Placement — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Subject, Tenant, and Domain Hermes may each use multiple graph providers selected by their owned truth, domain, and purpose, without requiring provider symmetry between layers.
Topics: polyglot-graph-memory, hermes-layer-placement, subject-hermes, tenant-hermes, domain-hermes, graph-memory, memory-gateway
Repository context: openxFactory (neutral three-layer Hermes placement with domain-specific provider bindings)
Captured: 2026-07-30

## Possible feats

- **Layer graph-binding profiles** — declare graph roles, scopes, providers, and companion rails for each Hermes layer.
- **Domain-specific graph placement map** — specialize neutral roles for codexFactory, MedxFactory, OpsxFactory, LedgerxFactory, and AdxFactory.
- **Cross-layer graph promotion rules** — distinguish scoped graph facts from de-identified reusable patterns and ontology candidates.

## Focus

This document isolates where graph capabilities belong in the three Hermes
layers. Layer topology should not imply provider symmetry. The layers own
different truth at different scopes and cadences:

- Subject Hermes owns private subject instances, evidence, current state, and
  active context.
- Tenant Hermes owns organizational policy, local systems, operating
  vocabulary, projects, and tenant memory.
- Domain Hermes owns reusable domain meaning, knowledge, practices, review
  standards, and promoted learning.

One layer may need several graphs, while another may need no code graph at all.

## Proposed model

Choose a graph from the owned truth and requested function:

| Layer | Common graph functions | Illustrative providers |
| --- | --- | --- |
| Subject Hermes | evidence, claims, state, timelines, subject-specific structure | domain-native temporal/evidence store; CodeGraph or codebase-memory-mcp when the subject is a software project |
| Tenant Hermes | policies, systems, repositories, staff, deployments, local mappings, project portfolios | Graphify for policy/docs; multi-repository code graph; CMDB/resource/deployment graph |
| Domain Hermes | ontology, source authority, reusable knowledge, domain patterns, semantic drift | pinned ontology projection; Graphify for corpus discovery; domain knowledge/evidence graph |

The mapping changes by DomainxFactory:

```text
codexFactory
  Subject Hermes = Project Hermes
    -> repository code graph is directly relevant

MedxFactory
  Subject Hermes = Patient Hermes
    -> temporal claims and evidence graph are relevant
    -> a code graph is normally irrelevant to patient truth

OpsxFactory
  Subject Hermes = Managed System Hermes
    -> infrastructure, dependency and service-health graphs are relevant

Domain Hermes in every domain
    -> reusable ontology and reviewed domain knowledge
    -> never raw subject instances
```

Even within Domain Hermes, different functions can use different providers:

```text
ontology stewardship       -> pinned ontology graph projection
document/source discovery  -> Graphify
software-practice analysis -> code graph in codexFactory
promotion review           -> traceability and evidence graph
```

The provider boundary follows the function, while layer ownership controls
which records and scopes the provider may see.

## Interfaces and boundaries

Layer profiles consume the neutral provider contract and specialize:

- allowed source and knowledge scopes;
- provider roles and routes;
- privacy and retention class;
- required source-authority companion;
- query purposes;
- promotion targets;
- fail and degraded modes.

The profiles do not:

- move subject facts into tenant or domain graphs;
- let semantic or structural traversal authorize access;
- force all subjects in one domain to share a physical graph;
- make a Tenant Hermes local mapping redefine the Domain Hermes ontology;
- require a Hermes layer and the Omnigent workers it governs to use the same
  provider.

Hermes owns decisions and memory boundaries. Omnigent consumes bounded
contexts for execution. A provider used by both still participates through
different requests, scopes, and context packets.

## Alternatives and tensions

**One provider per Hermes layer** gives a simple operational diagram but
confuses a layer with a storage product and suppresses legitimate
purpose-specific providers.

**One provider per DomainxFactory** respects domain specialization but still
collapses subject, tenant, and domain ownership.

**A physically unified cross-layer graph** makes traversal easy but creates
privacy, consent, promotion, retention, and authority hazards. Federation
through bounded queries preserves separation.

**Layer-local provider autonomy** can improve fit but may fragment identifiers
and make cross-layer promotion hard. Stable xFactory references and explicit
promotion records are therefore shared requirements.

## Open questions

- Which graph roles belong in neutral layer scaffolds versus DomainxFactory
  overlays?
- Can one provider instance host several isolated layer partitions, or should
  physical separation be required for some privacy classes?
- What is the smallest useful Subject Hermes graph contract across radically
  different domains?
- Which Tenant Hermes graph relationships may be promoted as reusable domain
  patterns after consent and de-identification?
- Does a layer profile select exact products, capability classes, or both?

## Relationships

- [Graph Provider Portfolio](polyglot-graph-memory-provider-portfolio.md)
  explains why provider symmetry is unnecessary.
- [Derived Projection Authority](polyglot-graph-memory-projection-authority.md)
  distinguishes scoped facts from provider projections.
- [Synthesis: Surface and Layer Placement](polyglot-graph-memory-synthesis-surface-and-layer-placement.md)
  relates the three layers to doxBench and Omnigent.
- Existing design context:
  [Ontology Layer Foundations](ontology-layer-foundations.md) and
  [Hermes Knowledge-Base Architecture](hermes-knowledge-base-architecture.md).
