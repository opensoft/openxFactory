# Domain Ontology Lifecycle Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: A DomainxFactory ontology is proposed as a versioned governed
artifact generated from authoritative sources and renewed through an
evidence-bearing drift loop.
Topics: domain-ontology, domain-ontology-lifecycle, domain-hermes
Repository context: openxFactory neutral lifecycle; DomainxFactories own meaning
Captured: 2026-07-28

## Possible feats

- **Domain ontology lifecycle contract** — define candidate generation,
  approval, publication, compatibility, drift, and retirement records.

## Motivation

Domain meaning changes as evidence, practice, terminology, and regulation
change. A one-time ontology export becomes stale, while an automatically
mutating ontology cannot serve as stable execution authority.

## Goals

- Produce traceable candidate ontologies from declared sources.
- Keep domain authority distinct from generation automation.
- Detect and disposition semantic drift.
- Publish pinned revisions with compatibility and rollback evidence.

## Non-goals

- This packet does not define any particular domain's concepts.
- It does not authorize neutral xFactory infrastructure to decide domain truth.
- It does not require one graph database or interchange syntax.

## What the system delivers

A DomainxFactory can publish a reviewed ontology revision, use it in semantic
context compilation, observe gaps and conflicts, and propose a successor
without rewriting the history of previous executions.

## System model

```text
governed sources → candidate generation → domain review → pinned revision
       ↑                                                   ↓
       └──────── drift evidence ← governed use ←───────────┘
```

## Cluster map

- [Governed Domain Ontology Lifecycle](domain-ontology-synthesis-governed-lifecycle.md)
  — joins candidate generation to evidence-driven maintenance.

## How it fits

The neutral contract can define lifecycle records and validation seams.
Domain Hermes supplies domain authority; the ontology execution packet
consumes pinned revisions; Omnigent agents may gather evidence but do not
approve semantic changes.

## Key decisions and open questions

Compatibility levels, approval roles, emergency correction, and contested
meaning remain open. These choices should be domain-configurable within a
neutral lifecycle envelope.

## Document map

### Synthesis

- [Governed Domain Ontology Lifecycle](domain-ontology-synthesis-governed-lifecycle.md)

### Atomic explorations

- [Domain Ontology Generation Pipeline](domain-ontology-generation-pipeline.md)
- [Domain Ontology Maintenance and Drift](domain-ontology-maintenance-and-drift.md)
