## Context

The ratified substantive-review lane defines a standing domain-seat roster and
a bounded exception that pulls `company-policy-lead` into one pull request's
merge-readiness council when a class-defined condition holds. Today the
codexFactory workflow evaluates that condition after Hermes has admitted the
convening, while Hermes derives its required roster from the members already in
the admission stamp. The two systems therefore have no shared, provenance-bound
answer to "which seats are required for this convening?"

The contract crosses three ownership boundaries. openxFactory owns the neutral
authority rule, codexFactory owns engineering-domain class evaluation and
GitHub candidate facts, and Hermes owns admission, seat-job issuance, and
verdict conformance. The payload is a trust-boundary input and must fail closed.

## Goals / Non-Goals

**Goals:**

- Establish one resolved roster before admission and use it for the entire
  convening.
- Preserve the existing standing seats and conditional pull-in semantics.
- Make roster derivation reproducible from a pinned rule revision and the exact
  candidate facts used by the producer.
- Keep every per-seat signing key ephemeral and local to its corresponding job.
- Cut producers and consumers to the new shape without a legacy protocol path.

**Non-Goals:**

- Defining engineering candidate classes or pull-in predicates in openxFactory.
- Moving GitHub fact collection or class evaluation into Hermes.
- Changing unanimity, substantive-return, ordinary-review, manager-review, or
  human-escalation policy.
- Claiming live OIDC, deployment, image, merged-commit, or release evidence.

## Decisions

### 1. The trusted producer resolves the roster before admission

The codexFactory prepare/commission job resolves the candidate class from the
governed default-branch gate rules, fetches candidate facts from GitHub, evaluates
the class's declared pull-in condition, and submits the final ordered set as
`council_convening.required_seats`.

Resolution happens once in the trusted preparation job, not independently in
each seat job. This prevents different jobs from observing different candidate
facts or rule revisions. Evaluating only inside Hermes was rejected because the
engineering-domain rule vocabulary and GitHub fact acquisition belong to
codexFactory. Evaluating inside each seat job was rejected because it cannot
produce one atomic roster.

### 2. Provenance accompanies the resolved value

The same `council_convening` block carries
`required_seats_provenance`, containing at least the candidate repository, pull
request number, candidate head SHA, matched candidate-class identifier, the
governed rules repository/path/revision, and the normalized candidate facts used
by the matched condition. The provenance records inputs, not merely the
producer's conclusion.

An opaque rules digest alone was rejected because it cannot identify which
governed object to retrieve. A producer assertion such as
`conditional_seat_required: true` was rejected because it is the conclusion the
consumer must be able to check.

### 3. Hermes validates and freezes before issuing seat jobs

Hermes admits the convening only after it has established that the roster is
non-empty, unique, composed of declared seats, includes every standing seat,
matches evaluation of the cited rule revision against the cited candidate
facts, and is bound to the candidate head being admitted. It then records the
roster and provenance in the immutable convening snapshot before issuing any
`seat_job_ids`.

Validation does not transfer rule ownership to Hermes: Hermes evaluates the
cited, pinned rule as an admission check and does not author or infer a class.
Trusting only the producer identity was rejected because an authenticated
producer can still be stale, misconfigured, or internally inconsistent.

### 4. The frozen roster is the sole completion roster

Seat-job issuance, return admission, substantive-return counting, unanimity,
and verdict completion all use the frozen roster. A later rule change or
candidate update cannot mutate an admitted convening; it requires a new
convening. A result from an unlisted seat is not counted, and a missing listed
seat parks the candidate.

This preserves the existing verdict policy while removing the split-brain
between early admission and late conditional evaluation.

### 5. Producer identity is workflow-bound and seat keys remain job-local

The first codexFactory realization binds the producer OIDC expectation to
`opensoft/codexFactory/.github/workflows/council-lane-reusable.yml@refs/heads/main`.
Repository and SHA claims identify the reviewed openxFactory candidate. Each
seat job registers its own ephemeral Ed25519 public key and signs its own return;
private keys never cross job boundaries or enter the convening payload.

### 6. Migration is a coordinated hard cutover

The neutral change lands before either realization. Hermes and codexFactory may
land dormant implementation separately, but activation is coordinated: the
producer begins emitting the required fields when the consumer begins requiring
them. There is no parser branch for the obsolete shared-key/root-authorized
shape. Rollback restores both components to the preceding versions; it does not
enable dual-protocol acceptance.

## Risks / Trade-offs

- **Rule revision becomes unavailable** -> Hermes refuses admission and names
  the unresolved provenance instead of trusting an unverifiable roster.
- **Candidate changes between resolution and admission** -> the candidate head
  SHA binding fails and a new resolution is required.
- **Producer and consumer activation are misordered** -> convenings park during
  the cutover; coordinated activation and an explicit rehearsal bound the risk.
- **Independent validation duplicates a small evaluator surface** -> keep the
  neutral predicate vocabulary closed and test producer/consumer conformance
  from shared fixtures rather than sharing domain implementation code.
- **A frozen roster outlives a policy edit** -> immutability is intentional;
  policy edits affect new convenings and cannot rewrite an in-flight record.

## Migration Plan

1. Ratify and land this neutral requirement delta.
2. Add shared positive and negative conformance fixtures for the resolved roster
   and provenance shape.
3. Land Hermes admission support and tests with activation disabled.
4. Land codexFactory preparation, per-seat registration, and signing support
   with activation disabled.
5. Rehearse valid, conditional, absent-seat, stale-head, and invalid-provenance
   cases, then activate both sides in one cutover window.
6. Roll back both activations together if the rehearsal-equivalent production
   path fails; do not restore the obsolete protocol as a fallback.

## Open Questions

None. Domain-specific candidate classes and deployment timing remain successor
implementation decisions within the constraints above.
