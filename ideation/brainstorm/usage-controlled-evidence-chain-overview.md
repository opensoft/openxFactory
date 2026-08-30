# Usage-Controlled Evidence Chain Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: openxFactory can provide a neutral, privacy-preserving evidence chain in which owner-local events receive immediate Kaspa witnessing and complete daily Bitcoin durability proofs.
Topics: usage-controlled-evidence-chain, signed-execution-chain, kaspa, bitcoin, transparency-log, multi-anchor-receipt
Repository context: openxFactory whole neutral evidence-chain picture and cross-repository handoff
Captured: 2026-08-29

## Possible feats

- **Neutral anchoring contract family** — publish opaque evidence,
  checkpoint, receipt, and verification contracts for domain and product
  consumers.

## Motivation

Factory and domain systems need an independent witness for signed acts without
placing their sensitive records, policy, or granular access metadata on a
public chain. The MedxChain notes preserved by
[PR #509](https://github.com/opensoft/openxFactory/pull/509) provide early
medical-record fidelity motivation; the signed-execution-chain work supplies
the later privacy and dual-witness corrections.

## Goals

- Keep the authoritative event and sensitive payload with its owning system.
- Make checkpoint history append-only and omission-evident.
- Use Kaspa as the fast operational witness.
- Include every accepted event in a 24-hour Bitcoin/OpenTimestamps durability
  batch.
- Retain proofs that remain verifiable after upstream pruning or service loss.
- Keep receipt formats independent of medical, financial, or other domain
  vocabulary.

## Non-goals

- Storing PHI, financial data, encrypted sensitive payloads, or stable subject
  identifiers on a public chain.
- Defining wallet grants, clinical consent, reimbursement policy, or retention
  periods.
- Claiming an anchor proves truth, authorization, storage, or deletion.
- Assigning deployable nodes, credentials, or production operations to
  openxFactory without a separate runtime decision.

## What the system delivers

Consumers receive a stable evidence leaf, an immediate Kaspa witness, a
retained inclusion proof, a path into a complete daily batch, an eventually
confirmed Bitcoin timestamp proof, and a verifier result that states exactly
which links are present or pending.

## System model

```text
OWNER REPOSITORY
  authoritative event + policy decision
            |
            v
OPENXFACTORY EVIDENCE KERNEL
  opaque leaf -> signed log -> linked checkpoint
            |                    |
            v                    v
      KASPA NOW          24-HOUR OTS BATCH
 operational witness       -> BITCOIN
            |                    |
            +-------- receipt ---+
```

## Cluster map

- [Synthesis: Witness Lifecycle](usage-controlled-evidence-chain-synthesis-witness-lifecycle.md)
  — relates opaque evidence, receipt progression, Kaspa proof retention, and
  complete daily Bitcoin batching.

## How it fits

The packet refines, but does not replace, the existing signed-execution-chain
topic. Its witness ordering follows the later Q3 ruling recorded on
`origin/main` by commit `9c501df6`, which reversed the older study ordering
still visible in this detached checkout: Kaspa first as the operational witness,
under its corroborating-only and proof-retention conditions, and Bitcoin via
OpenTimestamps on every item for durability. It gives the user's new 24-hour
cadence an explicit brainstorm home and separates neutral contracts from a
future deployable anchoring service. Domain repositories emit events; wallet
products supply authority evidence; openxFactory defines how opaque checkpoints
are witnessed.

## Key decisions and open questions

The intended ordering is Kaspa first and Bitcoin durability for every item.
The exact UTC window, confirmation depths, empty-window behavior, adapter code
home, archival operation, and network-outage service levels remain proposal-
stage decisions.

## Document map

### Synthesis documents

- [Witness Lifecycle](usage-controlled-evidence-chain-synthesis-witness-lifecycle.md)

### Atomic documents

- [Anchor Kernel](usage-controlled-evidence-chain-anchor-kernel.md)
- [Dual-Witness Cadence](usage-controlled-evidence-chain-dual-witness-cadence.md)
