# Hermes Memory and Retrieval Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Hermes memory and retrieval form a proposed governed path from
source evidence through per-query consent and minimized context packets to an
advisory decider.
Topics: memory-retrieval, memory-gateway, consent, source-authority
Repository context: openxFactory neutral memory and subject-recall boundary
Captured: 2026-07-28

## Possible feats

- **Governed Hermes recall service** — adapters, evidence rows, per-query
  authorization, context compilation, audit, revocation, and explanation.

## Motivation

Hermes needs organizational and subject context, but copying source systems
into an opaque memory store loses authority, consent, correction, and
deletion semantics. Retrieval also risks being mistaken for a decision.

## Goals

- Preserve source authority and tenant scope from ingestion through recall.
- Re-evaluate consent and purpose on every private query.
- Minimize and explain evidence admitted to context.
- Keep retrieval advisory to Hermes authority.
- Make access, denial, revocation, and derived artifacts auditable.

## Non-goals

- The memory gateway is not an unrestricted data lake.
- A search score is not truth or decision authority.
- Cached context cannot outlive current authorization silently.
- This packet does not choose one vector database or search provider.

## What the system delivers

A purpose-bound query yields either an explained denial or a context packet
containing permitted evidence, provenance, authority, ranking rationale,
conflicts, freshness, and omissions. The operation records a correlated audit
trail.

## System model

```text
source systems → governed adapters → evidence rows/indexes
  → per-query consent and policy gate
  → retrieve, rank, minimize, explain
  → advisory context packet
  → Hermes deliberation and audited use
```

## Cluster map

- [Governed Evidence Recall](memory-retrieval-synthesis-governed-recall.md)
  — joins consent authorization to evidence-to-context construction.

## How it fits

The ratified memory gateway supplies tenant, provider, consent, and audit
rails. Client Hermes declares source and memory policy; Project or Subject
Hermes supplies scope and consent; the Hermes runtime deliberates over the
result.

## Key decisions and open questions

The load-bearing boundary is that source evidence and derived context retain
different authority. Open questions include cache invalidation, subject audit
visibility, deletion propagation, and safe cross-worker transport.

## Document map

### Synthesis

- [Governed Evidence Recall](memory-retrieval-synthesis-governed-recall.md)

### Atomic explorations

- [Evidence-to-Context Boundary](memory-retrieval-evidence-context-boundary.md)
- [Consent Enforcement at Recall](memory-retrieval-consent-enforcement.md)

### Related source leaves

- [Client Ingestion-Adapter Contract](client-ingestion-adapter-contract.md)
- [Hermes Knowledge-Base Architecture](hermes-knowledge-base-architecture.md)
- [Hermes Retrieval Primitives](hermes-retrieval-primitives-contract.md)
- [Subject Recall and Consent Path](subject-recall-and-consent-path.md)
