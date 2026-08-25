# Synthesis: Governed Evidence Recall — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Per-query memory consent enforcement and evidence-to-context compilation
combine into minimized, explainable recall that remains advisory to Hermes.
Topics: memory-retrieval, consent, context-packet, memory-gateway, synthesis
Repository context: openxFactory governed retrieval exploration
Captured: 2026-07-28

## Possible feats

- **Governed recall primitive** — authorize, retrieve, rank, minimize,
  explain, and audit one purpose-bound memory query.

## Members and their joints

Atomic members:
[Evidence-to-Context Boundary](memory-retrieval-evidence-context-boundary.md)
and [Consent Enforcement at Recall](memory-retrieval-consent-enforcement.md).

### Consent precedes evidence admission

The recall gate evaluates the requester, subject, purpose, scope, source
authority, and current consent. Only allowed evidence classes enter retrieval
and synthesis.

### Context construction preserves the decision trail

The compiler selects and ranks permitted evidence, records omissions and
conflicts, and emits a context packet. Hermes then deliberates under its own
authority; retrieval does not choose the outcome.

### Audit closes the accountability loop

Authorization, queries, source accesses, packet construction, and downstream
use share a correlation identity. Revocation and deletion can therefore find
affected derived artifacts.

## Emergent behavior

The system can provide useful private-memory recall while explaining not only
what was found, but why access was allowed and what was deliberately omitted.

## Tensions to hold

- Better recall can increase privacy exposure.
- Full provenance improves audit at storage and latency cost.
- Context caching improves performance while complicating revocation.

## Recombination opportunities

Project or person subjects from the
[Project Hermes packet](project-overview.md) provide scope and consent
authority; the [Hermes runtime](hermes-overview.md) consumes the result.

## Open questions

- How does revocation invalidate derived summaries and caches?
- Which audit fields are visible to the subject versus operators?
- Can a context packet cross a worker boundary without re-authorization?
