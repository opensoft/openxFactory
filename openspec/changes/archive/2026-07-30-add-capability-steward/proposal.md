code_surface: openxFactory (contracts/schemas crystallized-capability-registry / crystallization-dispatch / capability-health record family + canonical validator scripts/validate-capability-steward.py — contracts, examples, validators only; the runtime junction (hermes-install admission per D9), derived-index regeneration, proof orchestration, and sweep/accounting lanes are successor realizations)
target_release: contract-v1.21
Status: ratified
Ratified by: Brett's approval of `add-capability-steward` on 2026-07-29, on the recurrence-crystallization staging decision record D1–D11 + V1–V2 carried as design context — notably D9 (neutral dispatch contract; hermes-install admission is the first realization), D10 (artifacts digest-pinned while authority status is live-read: demotion bites at the next junction decision), D11 (v1 admits only pure/idempotent effect classes), the L2 cache-behind-the-junction seam rule, the one-adjudication-kind lean (LC-Q5: parity and sentinels share the record), and the steward synthesis rulings SYC-C1..C3 (the steady state is a governed blend with the AI path as permanent infrastructure; renewal write-backs are contractual; sentinel ε is the packet's most load-bearing policy number, floored above zero); the carried open points (shadow-window statistics, replay-only promotion for low-risk L3, steward role-vs-contract, dashboard surfacing, degraded-as-status) are deliberately deferred to implementation and realization.

## Why

The first two waves are canon: the pattern ledger senses repetition and
nominates (`contract-v1.19`), and the crystallizer decides, specifies,
builds, and binds authority (`contract-v1.20`) — but a built capability
still has nowhere governed to live, no junction to serve through, no proof
ladder to climb, and no health surface to keep it honest. This change adds
the operating plane that closes the flywheel: the registry as the single
source dispatch may read, the dispatch junction as the single entry before
planning with deterministic fences and the AI path always intact, the
replay → shadow → canary proof ladder with demotion triggers armed at
promotion, mandatory sentinel sampling so drift detection and savings
claims stay falsifiable, the cost-ordered drift response ladder, and
sentinel-anchored accounting whose exhaust flows back to the pattern
ledger. Without it, crystallized capabilities would be scripts on a shelf;
with it, they are governed executors whose authority is provable,
revocable at the next dispatch decision, and permanently audited.

## What Changes

- Add `crystallized-capability-registry`: one governed record per
  capability (identity, family refs, fence ref, rung, artifact digest +
  packaging + residence, provenance ref, permission binding, consent
  scope, cost profile, health snapshot, owner, dry-run declaration) with
  the status spine `candidate → building → shadow → canary → active →
  degraded → retired` deliberately mirroring the document lifecycle;
  git-resident truth with a derived dispatch index (governed-derived-model
  discipline); records reference evidence by digest and never embed
  payloads; **D10**: artifact digests are pinned with deliberate re-pin
  while authority status is live-read — a demotion takes effect at the
  next dispatch decision, never waiting for a consumer re-pin; field
  writes follow a declared authority matrix (build writes identity once,
  proof gates advance status, the steward writes health, accounting writes
  cost).
- Add `crystallization-dispatch`: the junction at job admission, BEFORE
  planning, as the single entry to every crystallized capability —
  fingerprint → registry lookup → deterministic fence → instance risk
  check → execute at rung → post-conditions → emit with provenance;
  ambiguity resolves to the AI path (a classifier may veto toward
  fallback, never extend past the fence); **D11 enforcement**: v1 admits
  only `pure`/`idempotent` effect classes; every fallback is recorded with
  a cause from the controlled taxonomy and accumulates in the family's
  frontier queue; dispatch overhead is budgeted and metered; the L2 result
  cache executes BEHIND the junction (a cache reachable outside dispatch
  is a conformance violation); run records are path-invariant in shape —
  provenance is the only difference an auditor sees.
- Add `capability-health`: the proof ladder (replay → shadow → canary,
  each a workflow-gate-contract instance with rung-scaled profiles) with
  demotion trigger bundles armed at promotion; bidirectional adjudication
  (capability, historical episode, or spec may be the one corrected — one
  record kind shared between parity and sentinels); **mandatory sentinel
  sampling** while a capability holds authority (adaptive ε, nonzero
  floor, per-family mode, declared exploration expense); the cost-ordered
  drift response ladder with hysteresis (observe → shrink fence →
  regenerate → demote → retire), regeneration-first; health findings split
  auto-actionable vs contested (doc-health's sibling); disuse retirement
  preserving lineage; sentinel-anchored accounting (no self-graded
  savings; every ex-ante prediction scored on maturity; automation share
  as the headline metric); and the contractual renewal write-backs —
  fallbacks, adjudications, sentinel episodes, and scores flow back to the
  pattern ledger, closing the flywheel.
- Add the canonical validator and examples completing the MVP corpus: the
  packet-capture capability's registry record in `shadow`, served /
  fallback / sentinel dispatch records, the ε=0.20-no-decay sentinel
  policy, an adjudication, a health report, and a sentinel-anchored
  savings entry.

## Capabilities

### New Capabilities

- `crystallized-capability-registry`: the record spine, status lifecycle,
  derived-index discipline, pins-vs-live-authority rule, and the field
  authority matrix.
- `crystallization-dispatch`: the junction contract, fences and effect-
  class admission, fallback taxonomy and frontier queue, overhead
  metering, the L2 seam rule, and audit-shape parity.
- `capability-health`: proof ladder, adjudication, sentinel regime, drift
  responses, finding classes, retirement, accounting discipline, and the
  renewal write-backs.

### Modified Capabilities

- None. `workflow-gate-contract` (proof stages as gate instances),
  `release-realization`, `credential-contracts`, `governed-derived-model`
  (the derived dispatch index), and the promoted crystallizer contracts
  are consumed as-is. **V2 stands**: dispatch fingerprints from existing
  envelope fields; the optional `family_hint` remains a later-wave
  MODIFIED `neutral-job-envelope` candidate.

## Out of Scope

- The runtime junction realization (hermes-install admission per D9), the
  derived-index regeneration lane, proof orchestration, and the
  sweep/accounting lanes — successor realizations in their owning repos.
- Cross-tenant pooling, the platform registry federation, and any T3
  consumer (later wave; the registry record's consent scope carries the
  frozen tier regardless).
- Per-instance mixed-rung dispatch and risk-scored rung selection (AL-Q4,
  a v2 refinement; the junction's risk check may only route to the AI
  path in v1).
- L2 result-cache mechanics (ontology packet) — this change binds only
  its seam: behind the junction, never beside it.

## Dependencies and Sequencing

Third and final exit of the topic. Consumes the promoted `pattern-ledger`
(`contract-v1.19`: episodes, families, candidates it writes back to) and
crystallizer contracts (`contract-v1.20`: decisions carry the proof
obligations this change discharges; specs carry the fences and effect
classes it enforces; bindings carry the throttles it applies). After this
change archives, the recurrence-crystallization topic's staged remainder
is the dials register (feeding all three waves as declared dials) and the
out-of-wave cross-tenant fragment in brainstorm.
