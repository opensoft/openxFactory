# Factory MCP Effects and Authority — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Describe operational effects separately from the authority conferred by a result.
Topics: factory-mcp, effects-authority, roles-authority-model, credential-contracts, approval
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Make external reads, execution and persistence visible without treating evaluation as approval.

## Focus

What does authority_effect: none promise, and what does it not promise?

## Proposed model and evidence

All three first-slice tools produce advisory evidence. Inspect does not call ports; verify invokes checks and idempotency storage; DNS checking invokes an authorized observation port. A neutral declaration names external reads, execution, persistence and mutation separately from authority effect.

## Interfaces and boundaries

A positive finding does not approve or apply a change. DNS credential retrieval can itself alter vault access posture in an existing ceremony; calling the intended DNS operation read-only does not authorize that ceremony. The new capability requires an already-authorized reader and fails when one is unavailable.

## Alternatives and tensions

A boolean read_only label can hide meaningful effects. Fine-grained declarations are more useful, but declarations must be backed by implementation evidence rather than treated as enforcement.

## Open questions

Future mutating tools need a separately ratified authority profile; they are outside the initial advisory conformance profile.

## Relationships

See [the related synthesis](factory-mcp-synthesis-evaluation-safety.md) and [the packet overview](factory-mcp-overview.md).
