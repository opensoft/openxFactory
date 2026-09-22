# Kaspa and Bitcoin Dual-Witness Cadence — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Each accepted checkpoint could receive an immediate Kaspa operational witness and inclusion in a complete 24-hour Bitcoin/OpenTimestamps durability batch.
Topics: usage-controlled-evidence-chain, dual-witness-cadence, kaspa, bitcoin, opentimestamps
Repository context: openxFactory neutral anchoring policy and witness sequencing
Captured: 2026-08-29

## Possible feats

- **Kaspa-first operational receipt** — return a low-latency witness while
  retaining the full transaction and DAG inclusion proof.
- **Daily Bitcoin durability checkpoint** — include every accepted leaf in a
  24-hour OpenTimestamps batch with no per-item selectivity.

## Focus

This document isolates the proposed witness profile: Kaspa is the primary
operational witness, while Bitcoin is the durability witness. "Primary" means
first operational answer, not sole evidentiary weight. The design turns the
currently unspecified "hours" batching language into a proposed 24-hour
cadence.

The ordering follows the later Q3 ruling recorded on `origin/main` by commit
`9c501df6` (Kaspa first, Bitcoin-via-OpenTimestamps on every item), not the
earlier chain-selection recommendation still visible in older detached
checkouts. Kaspa retains the ruling's corroborating-only evidentiary condition;
Bitcoin remains the basis for long-horizon durability claims. The 24-hour
cadence is a new proposed clarification rather than part of that prior ruling.

## Proposed model

Every accepted evidence leaf enters both witness paths:

```text
leaf accepted
  -> Kaspa submission now: kaspa_submitted
  -> confirmation policy satisfied: kaspa_confirmed
  -> retain transaction + DAG inclusion proof
  -> operational receipt updated

same leaf
  -> daily ordered Merkle batch
  -> OpenTimestamps submission
  -> Bitcoin confirmation and proof upgrade
  -> durability receipt: bitcoin_confirmed
```

The daily batch should include every leaf accepted during its declared window,
bind the previous batch root, and publish a manifest with first and last leaf
sequence, count, root, window boundaries, close reason, and late-arrival
handling. A leaf receipt carries its Merkle path into that batch.

The proposed default is one fixed UTC checkpoint window per 24 hours. A later
governed policy could choose a rolling maximum-age service level, but a fixed
window is easier to reconcile and audit. Empty windows need an explicit choice:
publish a continuity heartbeat or record a signed no-events statement off
chain and link the next non-empty checkpoint across the gap.

## Interfaces and boundaries

The neutral profile specifies ordering, completeness, proof states, and timing.
It does not own token funding, fee accounts, node operation, chain keys, or
calendar hosting. Those are deployable runtime concerns.

Kaspa's pruned transaction history requires retained proof material and an
archival evidence strategy. Bitcoin/OpenTimestamps supplies durable
timestamping of the batch root; it does not store the underlying events or
prove their truth.

## Alternatives and tensions

- Per-event Kaspa anchoring gives the clearest operational receipt; per-minute
  Kaspa batches reduce transaction count but change what "immediate" means.
- A fixed UTC close is deterministic; a rolling 24-hour ceiling reduces worst-
  case latency but complicates completeness reconciliation.
- Daily Bitcoin anchoring creates an acknowledged durability gap for the open
  batch. The Kaspa receipt and signed local log cover that window operationally.
- Public OpenTimestamps calendars reduce cost; a self-operated calendar gives
  more control but adds operational ownership.

## Open questions

- Is the 24-hour rule a fixed UTC close or a maximum age for every leaf?
- What confirmation depth changes a witness from submitted to confirmed?
- How are late events assigned without rewriting a closed batch?
- Must an empty day produce a Bitcoin heartbeat?

## Relationships

The neutral receipt shape is explored in
[Anchor Kernel](usage-controlled-evidence-chain-anchor-kernel.md). The complete
state sequence is described in
[Synthesis: Witness Lifecycle](usage-controlled-evidence-chain-synthesis-witness-lifecycle.md).
