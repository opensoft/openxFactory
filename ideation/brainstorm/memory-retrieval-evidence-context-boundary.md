# Hermes Evidence-to-Context Boundary — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Hermes retrieval should transform tenant-scoped source evidence into
an advisory context packet while retaining authority, provenance, freshness,
ranking, and omission information.
Topics: memory-retrieval, evidence-rows, context-packet, source-authority
Repository context: openxFactory memory-gateway and Hermes retrieval exploration
Captured: 2026-07-28

## Possible feats

- **Evidence-to-context compiler** — assemble a minimized context packet with
  source citations, authority class, ranking explanation, freshness, policy
  checks, and explicit omissions.

## Focus

This document isolates the seam between stored or federated evidence and the
context a Hermes decider receives. It prevents retrieval synthesis from
silently becoming an answer or authority.

## Proposed model

The compiler accepts a purpose-bound query, tenant and subject scope, source
inventory, retrieval plan, and policy context. It emits selected evidence,
scores and rationale, source authority, relevant time bounds, conflict notes,
and a list of denied or unavailable evidence classes.

The packet pins the retrieval and adapter revisions needed for later audit.
Summaries remain traceable to evidence rows rather than replacing them.

## Interfaces and boundaries

The boundary consumes adapters and primitives described by
[Client Ingestion](client-ingestion-adapter-contract.md),
[Hermes Knowledge-Base Architecture](hermes-knowledge-base-architecture.md),
and [Hermes Retrieval Primitives](hermes-retrieval-primitives-contract.md).
It emits context to a decider, not a decision to an executor.

## Alternatives and tensions

- Returning raw evidence maximizes inspectability but increases context cost.
- Aggressive synthesis improves usability while risking lost nuance.
- Federated reads preserve source freshness but create availability coupling.

## Open questions

- What ranking explanation is sufficient for audit?
- How are conflicting authoritative sources represented?
- Which context packets may be cached, and for how long?

## Relationships

The [Consent Enforcement Boundary](memory-retrieval-consent-enforcement.md)
decides which evidence may enter this compiler.
