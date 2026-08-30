# Phase 0 Research: Resolved Council Seats

**Date**: 2026-08-28

**Feature**: `026-add-resolved-council-seats`

**Governed By**: `openspec/changes/add-resolved-council-seats/`

## Decision 1: Publish a focused neutral contract family

**Decision**: Add `contracts/council-convening/` with one closed Draft 2020-12
schema, an indexed conformance corpus, and a canonical validator. Do not widen
the copied `contracts/schemas/hermes-job-envelope.schema.yaml`.

**Rationale**: The copied envelope deliberately leaves domain job content open,
while roster resolution is now a versioned producer/consumer admission boundary
with stricter closure, provenance, and failure semantics. A focused family can be
pinned and tested without changing unrelated Hermes jobs.

**Alternatives considered**:

- Add fields directly to the copied v1 envelope: rejected because it makes every
  Hermes job consumer participate in a council-only change.
- Publish prose only: rejected because the hard cutover needs portable shape and
  negative-corpus evidence.
- Put the canonical schema in Hermes Install: rejected because Hermes consumes
  the neutral contract and does not own its meaning.

## Decision 2: Keep rule ownership domain-side and validation independent

**Decision**: The contract records the immutable rule locator, matched class,
normalized input facts, declared standing/conditional seat evaluation, and final
roster. The neutral validator checks shape, bindings, and deterministic roster
set arithmetic. Hermes independently resolves and evaluates the cited rule
through a consumer-owned adapter before admission; it never trusts a producer's
condition result alone.

**Rationale**: openxFactory can define the handoff without importing GitHub or
engineering candidate-class vocabulary. Independent producer and consumer
implementations are what detect drift.

**Alternatives considered**:

- Move GitHub fact gathering and class evaluation into Hermes: rejected because
  those are codexFactory domain mechanics.
- Share codexFactory evaluator code with Hermes: rejected because common code
  cannot detect its own semantic drift.
- Trust an authenticated producer assertion: rejected because stale or
  misconfigured trusted producers still produce invalid rosters.

## Decision 3: Record inputs and derivation, not a boolean conclusion

**Decision**: `required_seats_provenance` identifies the exact candidate and
governed rule revision and carries the normalized facts consumed by the matched
condition. Conditional evidence names the seat, rule condition reference, and
evaluated state, but cannot replace the cited rule or facts.

**Rationale**: A conclusion such as `conditional_seat_required: true` is not
reproducible. Repository/path/revision plus exact facts let admission obtain the
same immutable rule and independently derive the answer.

**Alternatives considered**:

- Opaque rule digest only: rejected because it does not identify a retrievable
  governed object.
- Producer identity plus final list: rejected because authentication does not
  prove freshness or internal consistency.
- Raw GitHub payload: rejected because it is provider-specific, high-cardinality,
  and larger than the normalized fact set the rule actually consumes.

## Decision 4: Freeze roster and provenance before job identity exists

**Decision**: Hermes creates the immutable admission snapshot from the validated
roster and provenance before allocating any `seat_job_ids`. Exactly one job is
then mapped to each frozen seat. Return admission and completion read only that
snapshot.

**Rationale**: Generating jobs first makes membership partially observable and
allows different jobs to derive different electorates. The snapshot is the one
atomic point shared by admission, dispatch, return counting, and completion.

**Alternatives considered**:

- Let each seat job re-evaluate membership: rejected because facts/rules can
  move between jobs.
- Re-evaluate at completion: rejected because a later policy edit must not
  rewrite an admitted electorate.
- Continue deriving from seeded `council.members`: rejected because that omits
  per-candidate conditional pull-in.

## Decision 5: Treat required seats as an ordered unique list with set semantics

**Decision**: The wire representation is an ordered, non-empty, unique list.
Validation compares it as a set against all standing seats plus exactly the
conditional seats whose conditions hold; the producer's stable order is retained
for deterministic artifacts and job issuance.

**Rationale**: Membership has set semantics, while deterministic order improves
reviewability and reproducible fixture output. Duplicate seats are always a
malformed roster rather than silently deduplicated.

**Alternatives considered**:

- Unordered mapping: rejected because it couples membership to unrelated seat
  configuration and makes canonical output less portable.
- Silent deduplication: rejected because it conceals a producer defect.
- Lexicographically reorder every roster: rejected because order is not
  authority and consumers need not rewrite a valid producer artifact.

## Decision 6: Publish reason-specific portable fixtures

**Decision**: Index every positive and negative case. Each case names the
requirements/scenarios it proves, its expected accept/refuse result, and one
stable primary finding code. Initial positives cover standing-only and triggered
conditional rosters. Initial negatives cover absent/duplicate/unknown/mismatched
rosters, opaque or unavailable provenance, missing facts, and stale candidate
heads.

**Rationale**: Producer and consumer implementations can run the same inputs
without sharing code. A negative must fail for the intended reason, not merely
for any error.

**Alternatives considered**:

- Inline pytest dictionaries only: rejected because downstream implementations
  cannot consume them portably.
- Outcome-only fixtures: rejected because wrong-reason failures hide drift.
- Live GitHub fixtures: rejected because mutable external state is not
  deterministic release evidence.

## Decision 7: Separate publication compatibility from activation compatibility

**Decision**: Register the new neutral family in the next available additive
contract bundle, allocated at realization. Coordinate downstream activation as a
hard cutover: codexFactory starts emitting the new block when Hermes starts
requiring it. Rollback restores both prior component versions; it never enables a
dual-protocol parser.

**Rationale**: Adding a previously absent canonical family is additive to the
openxFactory release surface. The operational protocol is nonetheless breaking
for the old uncontracted payload, exactly as the ratified change declares.

**Alternatives considered**:

- Reserve a bundle number during planning: rejected by the versioning policy.
- Add a compatibility parser reconstructing membership: rejected by the hard
  cutover requirement and because it restores the original split-brain defect.
- Deploy consumer-first or producer-first with live traffic: rejected because
  either order creates an ambiguous acceptance window.

## Decision 8: Keep signing changes in the codexFactory successor

**Decision**: The neutral family prohibits private-key material and records only
the roster/provenance boundary. The codexFactory successor creates one ephemeral
Ed25519 key inside each seat job, registers its public key under the runtime-
issued seat job identity and governed OIDC subject, signs that seat's return, and
drops the private key in-process.

**Rationale**: The current signer mints one key for a whole convening and relies
on register-recorded root secrets. That contradicts job-local isolation and
couples an implementation-specific signing protocol to the neutral roster shape.

**Alternatives considered**:

- One ephemeral key shared by every seat: rejected because one job can then
  impersonate another seat.
- Persist keys between workflow steps: rejected because private material crosses
  a job/process boundary.
- Define GitHub OIDC claims in the neutral schema: rejected because the neutral
  rule is job-local identity; the first domain binding belongs to codexFactory.

## Resolved Unknowns

All material planning decisions are resolved. The final bundle tag, release
commit, downstream feature numbers, deployment window, live OIDC evidence, and
merged successor commits are realization-time facts and must not be invented in
planning artifacts.
