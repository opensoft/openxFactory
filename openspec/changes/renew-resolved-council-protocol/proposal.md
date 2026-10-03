---
code_surface: contracts/council-convening, canonical validators and conformance fixtures; successor producer and consumer implementations have their own packets
target_release: implementation_pending — versions allocated at realization; archive on merged, green provider realization and linked successor evidence
---
# Renew the resolved council protocol

Status: ratified
Ratified: 2026-10-03 by Brett Heap — "ratify all three as disclosed"; [exact reviewed heads and scope](review/ratification-2026-10-03.md).
Proposed: 2026-10-03
Commission: Brett Heap directed "implement this" after the seven-item comparison of codexFactory draft 017; this commissions preparation, not ratification of this newly authored packet.

Decision update (2026-10-03): the header and [ratification record](review/ratification-2026-10-03.md) now record ratification as disclosed. The original commission and preparation statements are retained as history; implementation, publication, deployment and activation are not claimed complete.

## Why

Conditional seats are resolved after commissioning while admission derives a standing roster, leaving no single independently checked membership answer across the boundary. The old `add-resolved-council-seats` candidate never merged: [PR #517](https://github.com/opensoft/openxFactory/pull/517) closed on Brett's word with instructions to re-propose against the current bundle.

## What Changes

- Require the trusted producer to submit ordered required seats and reproducible immutable rule/candidate/fact provenance before admission.
- Require the consumer to verify and freeze that answer, issue one assignment per seat, and use the frozen roster through completion.
- Bind public-key registration and returns to independently authenticated seat assignments; private keys stay local to their individual jobs.
- **BREAKING**: at the removal major, reject roster-less and root-authorized old-protocol requests. First publish a deprecation minor as required by `docs/contract-versioning-policy.md`; allocate neither version here.
- Publish a shared positive/negative corpus for separately implemented producer and consumer evaluators. Keep domain class ownership in the producer and admission ownership in Hermes.

## Capabilities

### New Capabilities

None. The contract family realizes existing neutral authority ownership.

### Modified Capabilities

- `roles-authority-model`: add resolved membership, reproducible provenance, assignment-bound signing, and versioned migration requirements.

## Impact

Implementation handoff (2026-10-03): this packet's sole feature is [`035-renew-resolved-council-protocol`](../../../specs/035-renew-resolved-council-protocol/spec.md); its [handoff](implementation-handoff.md) records current readiness. The original proposal's future-tense preparation statements are retained as history.

Provider contracts, canonical validators, release inventory, and the domain regression denominator change through this packet's one future Speckit feature. Two separate successor packets are `codeXfactory/codexFactory:realize-resolved-council-protocol` and `opensoft/xFactory-Hermes-Install:admit-resolved-council-protocol`; each hands off to exactly one feature in its own repository.

No release, deployment, credential provisioning, lane assignment, or ratification is performed by this proposal. Decisions ready for Brett are in [decision-packet.md](decision-packet.md); the concrete boundary and activation design is in [design.md](design.md).
