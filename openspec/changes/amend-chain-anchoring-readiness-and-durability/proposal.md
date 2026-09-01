---
code_surface: openxFactory — additive amendments to the ratified `chain-anchoring` contract family and its canonical validator; no deployable gateway, chain client, scheduler, or credential surface
target_release: next additive contract minor, allocated at realization by merge order
---

# Amend Chain-Anchoring Readiness and Durability

Status: draft

## Why

The repository owner selected the already-ratified `add-chain-anchoring` packet
as the surviving tranche-three change and retired the stale competing
`add-signed-execution-chain-anchoring` draft. The surviving packet is stronger
on receipt integrity, timing, privacy, and witness failure, but the comparison
found three useful contract obligations that must not disappear with the
superseded draft: an operational-PKI realization gate, deterministic fixed-UTC
durability membership, and an explicit distinction between network submission
and independently verified confirmation.

## What Changes

- Add a fail-closed realization prerequisite requiring the already-realized
  signed-execution-chain contracts, the live REQUIRED
  `signed-execution-chain-gate` plus broken-chain canary, and an operational,
  `trust-anchor`-conformant PKI plane before `chain-anchoring` implementation is
  commissioned.
- Add a fixed-UTC durability profile whose trusted log acceptance time and
  atomic admission transaction determine one immutable daily batch, including
  deterministic dedupe, late-arrival treatment, a closed non-recursive event
  denominator, complete event inclusion, and empty-day continuity checkpoints.
  The closed daily root is the anchored item sent to both witnesses, preserving
  the existing one-root multi-anchor receipt.
- Require witness state to distinguish submission from confirmation. Kaspa
  interface acceptance is not Kaspa confirmation; OpenTimestamps submission is
  not Bitcoin confirmation; long-horizon claims require the latter. Confirmation
  transitions are governed by immutable versioned operator-approved profiles,
  not implementation-selected thresholds.
- Preserve the surviving packet's existing receipt/state split, timing model,
  configured-witness binding, privacy boundary, and claim-not-factory failure
  semantics unchanged.
- Record the disposition of the superseded draft: its provider-neutral gateway
  enforcement text belongs to consumer/runtime governance and is not imported
  into the neutral anchoring capability; its remaining requirements are already
  covered or strengthened by `add-chain-anchoring`.
- Link this amendment and its unrealized ratified basis to one shared Speckit
  feature and release; archive the basis first and this amendment second.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `chain-anchoring`: Add realization readiness, fixed-UTC complete durability
  batches, deterministic dedupe/lateness rules, and submitted-versus-confirmed
  witness semantics without changing the ratified witness configuration.

## Impact

- **openxFactory contracts:** realization will add only additive schema,
  example, refusal-fixture, and validator rules under the not-yet-released
  `chain-anchoring` family through the basis packet's same realization.
- **Runtime owners:** must provide operational PKI evidence and the declared
  scheduling, persistence, retry, and network adapters; those runtime surfaces
  remain outside this repository.
- **Consumers:** receive one stable capability id, `chain-anchoring`, and can
  pin exact release/version/digest evidence without relying on the superseded
  draft id.
- **MedxFactory:** its draft usage-control packet can reference the surviving
  capability while keeping executable conformance blocked until the amended
  contracts are released and consumer conformance passes.
- **Compatibility:** additive first-release path only while this amendment and
  `add-chain-anchoring` realize and release together. If the basis releases
  first, compatibility and version class must be re-evaluated before this packet
  proceeds; no released receipt is silently reinterpreted.
