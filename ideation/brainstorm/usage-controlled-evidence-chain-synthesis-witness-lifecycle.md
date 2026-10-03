# Synthesis: Witness Lifecycle — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A stable evidence lifecycle can separate immediate operational witnessing from delayed durability while preserving one verifiable receipt for every owner-local event.
Topics: usage-controlled-evidence-chain, witness-lifecycle, anchor-kernel, dual-witness-cadence, synthesis
Repository context: openxFactory neutral evidence and anchoring composition
Captured: 2026-08-29

## Possible feats

- **Progressive multi-witness receipt** — expose explicit pending, submitted,
  confirmed, superseded, and failed states without changing event identity.

## Members and their joints

Atomic members: [Anchor Kernel](usage-controlled-evidence-chain-anchor-kernel.md),
[Dual-Witness Cadence](usage-controlled-evidence-chain-dual-witness-cadence.md),
[Kaspa Execution Surface Decision Study](usage-controlled-evidence-chain-execution-surface-decision.md).

```text
owner event -> signed leaf -> local checkpoint -> Kaspa proof
                              |
                              +-> daily batch -> OTS -> Bitcoin proof
                                                        |
                                                completed receipt
```

### Identity and progression

The owner event and evidence leaf receive stable identities before either
network accepts them. Witness updates append state to the same receipt rather
than creating competing event identities. A verifier can therefore distinguish
"authorized event, anchor pending" from "anchor missing" and "proof invalid."

### Completeness and failure

The daily manifest closes an exact leaf range. Reconciliation proves every leaf
in that range has a Merkle path and no leaf was silently selected out. A Kaspa
outage, Bitcoin delay, or OpenTimestamps proof-upgrade delay creates an explicit
operational state and escalation; it must not be converted into a false pass.

### Retention and verification

The receipt must retain enough data for independent later verification even if
a standard Kaspa node no longer serves the transaction. Long-horizon claims use
the Bitcoin path while the Kaspa path remains the fast operational witness.

## Emergent behavior

Together, the kernel and cadence allow owners to act on low-latency evidence
without pretending that it already has durable Bitcoin confirmation. They also
let a later auditor prove daily completeness and follow one event through both
witnesses.

## Tensions to hold

- Anchoring is valuable evidence but should not become a remote network
  dependency for otherwise authorized patient care.
- "Every item receives Bitcoin" requires complete batch reconciliation, not
  one transaction per item.
- A signed destruction event can be anchored through this lifecycle, but the
  anchor proves only the signed claim existed, not that every key or plaintext
  copy was destroyed.

## Recombination opportunities

This lifecycle can combine with wallet grant exercises, clinical-use events,
billing-retention events, factory execution attestations, and other owner-local
logs without teaching the neutral kernel their semantics.

## Open questions

- Which failures block closure and which carry into the next reconciliation?
- Who owns the operational service-level objective and incident response?
- How should verifier results express a valid Kaspa proof with a still-pending
  Bitcoin durability path?
