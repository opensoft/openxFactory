# Contract Release and Document Lifecycle Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: The release-lifecycle packet proposes a traceable chain from stable
brainstorm evidence through explicit proposals and promoted specs to signed,
validated contract releases adopted by stack surfaces.
Topics: release-lifecycle, contract-release, document-lifecycle, provenance
Repository context: openxFactory governance and contract release exploration
Captured: 2026-07-28

## Possible feats

- **End-to-end release provenance service** — source pins, proposal claims,
  promoted specs, release manifests, conformance evidence, and consumer pins.

## Motivation

Document evidence evolves, proposals select only some ideas, contracts ship
through several package and stack surfaces, and tags alone do not prove which
schema, validator, or source a consumer adopted.

## Goals

- Preserve exact source evidence without making brainstorms normative.
- Require proposals to express accepted claims explicitly.
- Give every contract release one inspectable identity.
- Bind package, schema, validator, compatibility, and signer evidence.
- Let consumers prove which release they adopted.

## Non-goals

- This packet does not replace the ratified document lifecycle.
- Brainstorm pins do not make the pinned prose policy.
- A release manifest does not waive domain or consumer validation.
- The packet does not require all capabilities to release in lockstep.

## What the system delivers

A reader can traverse from a consumer's pinned contract release to validation
and conformance evidence, promoted requirements, the governing proposal, and
the exact brainstorm or supporting evidence reviewed during design.

## System model

```text
brainstorm evidence at stable path
  → proposal pin + explicit accepted delta
  → implementation and validation
  → promoted spec + signed release manifest
  → stack-surface conformance
  → consumer pin and adoption evidence
```

## Cluster map

- [Governed Source-to-Release Promotion](release-lifecycle-synthesis-governed-promotion.md)
  — joins immutable source identity to contract release admission.

## How it fits

The current ratified lifecycle remains in force. The immovable-leaf model and
release manifest are proposed refinements that require OpenSpec deltas before
tooling or policy changes. Existing archive bundles and manifests remain
historical evidence.

## Key decisions and open questions

Open choices include moving versus pinning source material, pin granularity,
release-manifest ownership, stack compatibility evidence, signer custody, and
emergency release handling.

## Document map

### Synthesis

- [Governed Source-to-Release Promotion](release-lifecycle-synthesis-governed-promotion.md)

### Atomic explorations

- [Contract Release Identity Gate](release-lifecycle-contract-identity-gate.md)
- [Immutable Source Provenance](release-lifecycle-immutable-source-provenance.md)

### Related source leaves

- [Contract Release and Stack-Surface Gaps](contract-release-and-stack-surface.md)
- [Immovable-Leaf Ideation Lifecycle](immovable-leaf-ideation-lifecycle.md)
