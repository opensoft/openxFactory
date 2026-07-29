# Synthesis: Hermes Knowledge and Retrieval — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Federated evidence architecture and governed retrieval primitives
combine into advisory context packets that preserve source authority,
consent, and tenant boundaries.
Topics: hermes, knowledge-base, retrieval, memory-gateway, context-packet, synthesis
Repository context: openxFactory Hermes knowledge and memory-gateway exploration
Captured: 2026-07-28

## Possible feats

- **Governed context-packet API** — return ranked evidence, source authority,
  consent disposition, omissions, provenance, and freshness for one query.

## Members and their joints

Atomic members:
[Hermes Knowledge-Base Architecture](hermes-knowledge-base-architecture.md)
and [Hermes Retrieval Primitives](hermes-retrieval-primitives-contract.md).

### Federation supplies evidence rows

The knowledge architecture keeps authoritative source systems in place,
normalizes evidence with structure and provenance, and builds derived indexes
without pretending the index is the source of truth.

### Retrieval returns primitives, not decisions

Search, source-specific search, who-knows, and recall operations assemble a
context packet. Planner, executor, and synthesizer stages remain advisory;
Hermes or a downstream authority decides.

## Emergent behavior

The combined system can answer why evidence was selected, what was excluded,
and which authority and consent limits apply before a decider uses it.

## Tensions to hold

- Hybrid ranking improves recall while making score explanation harder.
- Age decay helps freshness but may suppress durable authoritative records.
- Federated queries preserve authority but create latency and availability
  coupling.

## Recombination opportunities

The detailed consent boundary lives in the
[Hermes memory and retrieval packet](memory-retrieval-overview.md).

## Open questions

- Which retrieval steps may execute in parallel without weakening policy?
- How is source deletion reflected in cached context packets?
- What ranking evidence is retained for later audit?
