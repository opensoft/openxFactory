# Synthesis: Trusted Evaluation Without Authority Escalation — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Combine trusted scope, declared effects, bounded evidence and per-tool repetition into an advisory evaluation boundary.
Topics: factory-mcp, trusted-context, effects-authority, results-evidence, replay-freshness, synthesis
Repository context: openxFactory; cross-factory design, with domain ownership retained
Captured: 2026-09-07

Lane: mcp-family-contract

## Possible feats

- Make tool outcomes comparable without treating successful evaluation as permission to act.

## Members and their joints

Atomic members: [trusted context](factory-mcp-trusted-context.md),
[effects and authority](factory-mcp-effects-authority.md),
[results and evidence](factory-mcp-results-evidence.md), and
[replay and freshness](factory-mcp-replay-freshness.md).

### Trust precedes operational work

A caller names the desired subject. The host verifies identity and resolves
permitted scope before external access. Registry and policy facts are trusted
inputs, never caller assertions. DNS credential retrieval is a separate ceremony:
a request to check DNS cannot start it merely because the eventual read is
non-mutating.

### Effects and results answer different questions

Verification can execute checks and persist replay state while granting no
authority. DNS can read a provider while granting no authority. A completed
negative domain finding is useful evidence; inability to evaluate is a failure.
A positive finding is neither an approval nor an apply instruction.

### Evidence has a source and an age

The result identifies evaluated input and trusted context under the domain's
disclosure rules. Codex path suppression does not become a blanket ban on useful
authorized DNS record references. Hashes identify content but do not make
guessable names private. Host audit references require a real resolving sink
before they can claim durable auditability.

### Repetition depends on the capability

Codex verification preserves its principal-scoped lease/replay semantics.
A DNS retry requests a new observation and can legitimately return a different
finding. The original observation time survives any caching, and host-pinned
freshness and deadlines are checked at the return boundary. Request IDs are
correlation values, not idempotency keys or grants.

## Emergent behavior

An agent can distinguish a blocked proposal, an unavailable observation, a replay
and a fresh evaluation without acquiring authority from any of those outcomes.

## Tensions to hold

A declaration documents behavior; it does not enforce it. A runtime whose
bindings freeze at startup must not claim live revocation. Cancellation must be
proved by an operational reader before a hosted DNS tool can claim it.

## Recombination opportunities

Apply these rules to the [three-tool comparison](factory-mcp-synthesis-three-tool-fit.md).
A future medical tool would supply its own purpose, consent and disclosure
mapping; this packet does not define medical semantics.

## Open questions

Live revocation, audit retention, identity register resolution and operational
reader cancellation belong to later host/runtime designs.

See the [overview](factory-mcp-overview.md).
