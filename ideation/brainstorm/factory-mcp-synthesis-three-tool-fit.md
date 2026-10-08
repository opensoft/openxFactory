# Synthesis: Three Tools Test the Shared Boundary — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Use two existing codex tools and a proposed Ops DNS evaluator to test common semantics before extracting transport code.
Topics: factory-mcp, codex-mapping, dns-check, implementation-boundaries, synthesis
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Validate a neutral declaration and a second domain's callable contract with explicit compatibility gaps.

## Members and their joints

Atomic members: [codex mapping](factory-mcp-codex-mapping.md),
[DNS check](factory-mcp-dns-check.md), and
[implementation boundaries](factory-mcp-implementation-boundaries.md).

### Common semantics surround different payloads

| Concern | Patch inspection (existing) | Candidate verification (existing) | DNS check (proposed) |
| --- | --- | --- | --- |
| Caller payload | Patch, worker result, binding and trace IDs | Patch-inspection payload plus idempotency key | Binding, zone, proposed record changes and trace IDs |
| Trusted subject | Repository and base | Repository, base and check profile | Registered zone, permitted records and observation reader |
| Operational effects | Pure evaluation | Host checks and replay storage | Authorized observation |
| Outcome | Eligible or blocked | Eligible or blocked | Eligible or blocked, or typed evaluation failure |
| Repetition | Re-evaluate | Existing lease/replay rules | Fresh observation per call |
| Authority effect | None | None | None |

The shared surface describes these choices. It does not erase patches, record
types or domain refusals into one generic job argument.

### The second domain reveals extraction limits

Descriptors and lossless result mapping may become reusable. The engineering domain's
check-execution port is not a DNS observation port, and an idempotency store is not obligatory for a
fresh read. Domain-independent synthetic fixtures belong in the neutral
validator; executable DNS fixtures and policy adapters belong in OpsxFactory.

### Evidence qualifies compatibility

The codex mapping records what source actually implements and explicitly names
scope-tuple, revocation and artifact-provenance gaps. Domain objects remain
verbatim in structuredContent. A declared profile cannot retroactively certify
the codex deployment or change a result digest.

### Realization proceeds through two owned changes

The neutral change would deliver a schema, semantic validator, fixtures and
mapping guidance. The Ops change would deliver request/result/error contracts,
an injected observation interface, reuse of existing DNS planning rules, tool
descriptor/result mapping, deterministic tests and an integration runbook.
Existing codex contract and adapter work remains with its current lane.

## Emergent behavior

These examples can falsify an overly broad shared abstraction before it becomes
a library or a deployed service.

## Tensions to hold

Tests with an injected reader prove the callable boundary. They cannot prove
live provider access, bounded cancellation or a deployment's readiness.
Realization is distinct from release acceptance and consumer pin advancement.

## Recombination opportunities

Use [domain services](factory-mcp-synthesis-family-surface.md) for ownership and
[evaluation safety](factory-mcp-synthesis-evaluation-safety.md) for runtime obligations.

## Open questions

A shared transport package requires evidence from a second real adapter.
Operational DNS reader provenance and resource identity require their own
reviewed integrations.

See the [overview](factory-mcp-overview.md).
