# Usage-Controlled Evidence Anchor Kernel — Brainstorm

Status: brainstorm
Kind: architecture
Summary: openxFactory could standardize a domain-neutral evidence checkpoint and multi-witness receipt kernel without learning the sensitive payload or the policy that authorized its use.
Topics: usage-controlled-evidence-chain, anchor-kernel, signed-execution-chain, transparency-log, multi-anchor-receipt
Repository context: openxFactory neutral contracts and reference verification boundaries
Captured: 2026-08-29

## Possible feats

- **Opaque evidence checkpoint contract** — define leaves, checkpoint roots,
  consistency links, anchor requests, and verification results without domain
  vocabulary.
- **Chain-agnostic receipt verifier** — verify retained Kaspa and Bitcoin proof
  material through one stable interface.

## Focus

This document isolates the neutral machinery between an owner-local use event
and its public witnesses. A clinical read, billing disclosure, factory merge,
or other governed act remains owned by the system that performed it. The
kernel receives only an opaque commitment and evidence metadata safe for the
shared layer.

This extends the staged `signed-execution-chain` direction and should retain
the corrected MedxChain boundary recorded in
[openxFactory PR #509](https://github.com/opensoft/openxFactory/pull/509):
granular access events stay in an off-chain signed log while public chains see
only privacy-reviewed checkpoints.

## Proposed model

The candidate neutral artifact sequence is:

```text
owner-local use event
  -> evidence leaf
  -> append-only transparency log
  -> checkpoint with prior-checkpoint consistency link
  -> witness-specific anchor requests
  -> witness proofs
  -> multi-witness receipt
  -> verification result
```

An evidence leaf could bind an event digest, owner repository and contract
version, event time, predecessor or session reference, commitment algorithm,
and the signing authority. It must not carry PHI, financial details, stable
subject identifiers, grant scopes, or domain purpose labels.

The checkpoint should commit to an ordered leaf range and its predecessor.
That continuity makes omission, reordering, and a silently restarted log
detectable. Each witness entry should retain the submitted transaction or
commitment, its inclusion proof, the relevant header or durable timestamp
proof, confirmation state, and verifier version.

## Interfaces and boundaries

openxFactory owns the shared artifact shapes, reference verifier, consistency
rules, adapter interface, and fail-closed validation behavior. The event owner
owns whether an act was authorized and what the event means. openXwallet owns
grants and signatures. A future install/runtime repository owns network
clients, nodes, credentials, schedulers, retries, and operational monitoring.

An anchor proves that committed bytes existed no later than a witnessed point
and have not silently changed relative to the retained proof. It does not prove
that an event was truthful, legally authorized, clinically correct, retained,
or deleted.

## Alternatives and tensions

- One universal event schema would simplify indexing but leak domain semantics
  into the neutral layer. Opaque owner-signed event digests preserve ownership.
- A receipt can embed complete proofs or reference retained evidence. Kaspa's
  pruning makes complete proof retention at anchor time the safer baseline.
- Network publication can be synchronous or asynchronous. Keeping public
  anchoring outside care and business critical paths favors a durable pending
  state with bounded escalation.

## Open questions

- Which minimum event metadata is safe and useful across domains?
- Does the neutral release include executable adapters or only adapter ports
  and reference verification?
- What proof format can survive provider changes without weakening witness-
  specific verification?

## Relationships

The witness ordering and timing are explored in
[Dual-Witness Cadence](usage-controlled-evidence-chain-dual-witness-cadence.md).
Their combined lifecycle is described in
[Synthesis: Witness Lifecycle](usage-controlled-evidence-chain-synthesis-witness-lifecycle.md).
