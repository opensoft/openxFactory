---
code_surface: openxFactory (contracts/council-convening, canonical validators and conformance fixtures; successor producer and consumer implementations have their own packets)
target_release: deferred-allocation — versions allocated at realization; archive on merged, green provider realization and linked successor evidence
---
# Renew the resolved council protocol

Status: ratified
Ratified: 2026-10-03 by Brett Heap — "ratify all three as disclosed"; [exact reviewed heads and scope](review/ratification-2026-10-03.md).
Proposed: 2026-10-03
Commission: Brett Heap directed "implement this" after the seven-item comparison of codexFactory draft 017; this commissions preparation, not ratification of this newly authored packet.
Amended: 2026-10-08 — gate conformance only; no requirement, decision, scope, task or design text changes. On Brett Heap's ruling of 2026-10-08T17:43:04Z, first-hand to lane `codeXfactory-2` (a multiple-choice selection of the recommended option, label verbatim *"Approve both (Recommended)"*; opensoft/brett-wip `lanes/log/codeXfactory-2.md` line 181, commit `20d534cc`), three edits bring the ratified text into line with gates that landed on main after it was authored. (1) `code_surface:` gains the head `openxFactory`, and the ratified text becomes its parenthesized gloss, word for word. (2) `target_release:` changes its token from `implementation_pending` to `deferred-allocation`, the vocabulary's value for a bundle whose number is allocated at the cut; the gloss is unchanged. (3) `.openspec.yaml` gains an `origin: kind: ad_hoc` block, recorded on the same word in `openspec/origin-dispositions.yaml`. `design.md` and `specs/` stay byte-identical to the ratified head; the record is [`review/ratification-2026-10-03.md`](review/ratification-2026-10-03.md) § ADDENDUM 2026-10-08. *Also 2026-10-08:* § Impact carries a dated allocation record, on Brett Heap's ruling verbatim *"Dated correction + tick 2.2 (Recommended)"* (the same log, RULED 23:03:35Z), replacing a 2026-10-03 note, and packet task 2.2 is ticked on the same ruling; neither changes any requirement, decision, scope or design text.

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

Allocation record (2026-10-08): this packet's sole feature is [`035-renew-resolved-council-protocol`](../../../specs/035-renew-resolved-council-protocol/spec.md), owned by lane codeXfactory-2 (claimed 2026-10-07, builder ruled 2026-10-08); see the [handoff's allocation record](implementation-handoff.md#allocation-record-2026-10-08). Recorded under Brett Heap's ruling of 2026-10-08, "Dated correction + tick 2.2 (Recommended)", replacing a 2026-10-03 note. The original proposal's future-tense preparation statements are retained as history.

Provider contracts, canonical validators, release inventory, and the domain regression denominator change through this packet's one future Speckit feature. Two separate successor packets are `codeXfactory/codexFactory:realize-resolved-council-protocol` and `opensoft/xFactory-Hermes-Install:admit-resolved-council-protocol`; each hands off to exactly one feature in its own repository.

No release, deployment, credential provisioning, lane assignment, or ratification is performed by this proposal. Decisions ready for Brett are in [decision-packet.md](decision-packet.md); the concrete boundary and activation design is in [design.md](design.md).
