# Three-Layer Hermes Runtime Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: The Hermes runtime is proposed as a deterministically seeded
three-layer decision system whose authority, memory, personas, legal
constraints, retrieval, and learning loops remain separately inspectable.
Topics: hermes, three-layer-hermes-runtime, layer-content-seeding, memory-gateway
Repository context: openxFactory neutral Hermes runtime architecture
Captured: 2026-07-28

## Possible feats

- **Three-layer Hermes content runtime** — compose, validate, seed, retrieve,
  decide, and observe through pinned Domain, Client, and Project layers.

## Motivation

Structural Hermes layers are not useful until they carry governed content and
the runtime reliably loads it. Conversely, a monolithic prompt cannot expose
which layer supplied authority, memory, character, or a constraint.

## Goals

- Compose Domain, Client, and Project content with explicit precedence.
- Seed enforceable policy, memory bindings, and persona references
  deterministically.
- Keep character subordinate to authority.
- Retrieve evidence through consent, tenancy, and source-authority rails.
- Feed observed outcomes into non-mutating learning and practice suggestions.

## Non-goals

- Hermes does not execute Plane-2 jobs directly.
- Retrieval results do not become decisions by themselves.
- A persona does not gain authority from its prose.
- A nightly sweep cannot clear or realize its own suggestions.

## What the system delivers

For a pinned layer stack, Hermes can explain the active authorities and
constraints, retrieve governed context, convene the appropriate decider or
council, produce a decision record, and emit bounded observations for later
learning.

## System model

```text
Domain content + Client overlay + Project/Subject overlay
  → verify and seed
  → authority/policy + memory bindings + persona references
  → governed retrieval and deliberation
  → decision or escalation
  → bounded observations and suggestions
```

## Cluster map

- [Layer Content and Authority](hermes-synthesis-layer-content-and-authority.md)
  — joins content composition, seeding, persona, and legal boundaries.
- [Knowledge and Retrieval](hermes-synthesis-knowledge-and-retrieval.md)
  — joins federated evidence to governed context packets.
- [Governed Practice Loop](hermes-synthesis-governed-practice-loop.md)
  — joins seeded authority to a non-mutating improvement trigger.

## How it fits

openxFactory owns neutral layer and memory contracts. DomainxFactories author
reusable domain content; clients tune company policy; projects bind subject
scope and acceptance. Omnigent executes governed jobs; Hermes decides,
retrieves, escalates, and records.

## Key decisions and open questions

The central design decision is to seed typed, separately governed content
rather than concatenate prompts. Open questions include overlay conflict
resolution, re-seed consent, degraded operation, and the exact boundary
between retrieval synthesis and deliberation.

## Document map

### Syntheses

- [Layer Content and Authority](hermes-synthesis-layer-content-and-authority.md)
- [Knowledge and Retrieval](hermes-synthesis-knowledge-and-retrieval.md)
- [Governed Practice Loop](hermes-synthesis-governed-practice-loop.md)

### Atomic explorations

- [Three-Layer Hermes Content and Seeding](hermes-layer-content-seeding.md)
- [Hermes Layer Seeding Mechanism](hermes-layer-seeding-mechanism.md)
- [Hermes Persona Character Model](hermes-persona-character-model.md)
- [Hermes Legal and Compliance Model](hermes-legal-compliance-model.md)
- [Hermes Knowledge-Base Architecture](hermes-knowledge-base-architecture.md)
- [Hermes Retrieval Primitives](hermes-retrieval-primitives-contract.md)
- [Hermes-Governed Nightly Sweep](hermes-governed-nightly-sweep.md)
