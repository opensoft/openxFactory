# Factory MCP Replay and Freshness — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Declare replay and observation freshness per tool rather than require idempotency everywhere.
Topics: factory-mcp, replay-freshness, idempotency, observation-freshness, failure-recovery
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Separate stable replayed results from fresh evaluations of changing state.

## Focus

When does repeating a tool call repeat an answer, and when should it re-observe the world?

## Proposed model and evidence

Existing inspect re-evaluates its fixed input/context. Existing verify uses its principal-scoped lease/replay contract and requires externally atomic coordination across replicas. Proposed DNS checks obtain a new observation for each call, with a host-pinned maximum age and deadline checked again before returning eligibility.

## Interfaces and boundaries

Request/correlation IDs are trace identifiers, not grants or idempotency keys. Cached evidence must retain its original timestamp. The first DNS slice does not accept idempotency_key, accept a caller freshness override, or claim exactly-once external observation.

## Alternatives and tensions

A retry of a read can legitimately see different state. A content-stable DNS plan digest and the separate timestamped observation evidence answer different questions and should not share one freshness claim.

## Open questions

Concrete host freshness limits are configuration values to pin during deployment; contract tests should use injected time, not wall-clock sleeps.

## Relationships

See [the related synthesis](factory-mcp-synthesis-evaluation-safety.md) and [the packet overview](factory-mcp-overview.md).
