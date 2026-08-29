# Feature Specification: Intent Compliance Contract

**Feature Branch**: `015-intent-compliance-contract`

**Created**: 2026-08-26

**Status**: Draft

**Input**: Realize the ratified `add-standing-policy-compliance-contract`
change as a released neutral contract family with executable conformance
evidence.

## User Scenarios & Testing

### User Story 1 - Validate governed intent evidence (Priority: P1)

A domain implementer can create each governed intent-compliance record and
receive deterministic acceptance or a specific refusal before relying on it.

**Why this priority**: The records cannot protect dispatch unless conformers
interpret the same authority, allowance, revocation, and decision states.

**Independent Test**: Validate the packaged conforming records and every
single-fault counterexample through the public family validation command.

**Acceptance Scenarios**:

1. **Given** a complete five-record family with current authority evidence,
   **When** the family is validated, **Then** every record is accepted.
2. **Given** one invalid authority, reference, digest, limit, outcome, or
   evidence condition, **When** the family is validated, **Then** it fails for
   the indexed contract reason.

---

### User Story 2 - Detect stale authority before dispatch (Priority: P2)

A policy authority can revoke an allowance so that a later static evaluation
detects evidence conditioned on an older trusted registry snapshot.

**Why this priority**: Neutral evidence must never present an older registry
head as current authority. Runtime dispatch serialization remains domain-owned.

**Independent Test**: Exercise current allowance resolution, revocation, reused
identifier rejection, and static evidence conditioned on a superseded registry
head.

**Acceptance Scenarios**:

1. **Given** a current authorized covering allowance, **When** all findings are
   satisfied, **Then** the decision may allow the governed intent.
2. **Given** static dispatch evidence conditioned on registry head N, **When**
   the trusted snapshot resolves head N+1, **Then** the evidence is stale and a
   current-state evaluation is required; invocation prevention is domain-owned.

---

### User Story 3 - Consume a pinned additive release (Priority: P3)

A domain repository can pin one additive openxFactory bundle and discover all
five schemas, their examples, validator, and exact release digests.

**Why this priority**: The first conformer needs an immutable neutral dependency
before it can implement domain-specific veto classes and runtime gates.

**Independent Test**: Verify the published release inventory against its exact
commit and run the public validator from a refreshed checkout.

**Acceptance Scenarios**:

1. **Given** the final release commit, **When** its inventory and manifest are
   verified, **Then** every family artifact resolves with the published digest.
2. **Given** a changed released byte or omitted artifact, **When** release
   verification runs, **Then** promotion fails.

### Edge Cases

- An allowance identifier reappears in a later registry revision.
- A revocation event names an unauthorized principal or incomplete authority.
- Approval, dispatch, and admission claim different allowance-reference sets.
- Classifier limits are absent, exceeded, timed out, or report an error.
- A higher review layer attempts to erase a deterministic block.
- Static evidence names a registry head older than the trusted snapshot.
- Evidence contains raw intent, provider payloads, credentials, or unbounded
  identifiers.

## Requirements

### Functional Requirements

- **FR-001**: The contract family MUST define exactly five independently typed
  record kinds: veto vocabulary, allowance approval, allowance revocation,
  allowance registry, and compliance decision.
- **FR-002**: Every record kind MUST use a closed, versioned envelope and MUST
  have a safe instantiation template and neutral example.
- **FR-003**: Validation MUST resolve authority and ratification evidence from
  immutable references rather than trusting self-reported digests.
- **FR-004**: Validation MUST prove immutable allowance approval, authenticated
  additive revocation, predecessor-linked registry state, and lifetime-unique
  allowance identifiers.
- **FR-005**: Validation MUST prohibit copied allowance payloads and require
  current-state resolution of registry-qualified identifier references.
- **FR-006**: Decisions MUST bind canonical content and policy identities, the
  canonically compared allowance-reference set, resolved record digests, and
  bounded redacted evidence.
- **FR-007**: Classifier evidence MUST use closed triggers, closed results, hard
  limits, and fail-closed outcome composition.
- **FR-008**: Dispatch conformance evidence MUST detect when its conditioned
  registry head differs from the head in the coherent trusted snapshot; it MUST
  NOT claim runtime invocation or atomic token consumption.
- **FR-009**: Every required behavior MUST have a conforming example or a
  single-fault counterexample with deterministic requirement attribution.
- **FR-010**: The family MUST be registered and published in one additive
  contract bundle with a complete immutable digest inventory.
- **FR-011**: The release MUST identify codexFactory as the first conformer
  without embedding engineering-specific veto vocabulary in openxFactory.

### Key Entities

- **Veto-class vocabulary**: Authority-bound identifiers and domain-owned
  detection metadata for policy classes.
- **Policy allowance**: Immutable approval facts for one vocabulary-bound class
  and neutral scope.
- **Policy allowance revocation**: Authenticated append-only event targeting an
  allowance approval.
- **Policy allowance registry**: Current append-only resolution state with
  lifetime-stable allowance identifiers.
- **Compliance decision**: Closed, digest-bound, bounded evidence emitted for
  every evaluation outcome.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All five record kinds have a schema, template, neutral example,
  and manifest registration in the released bundle.
- **SC-002**: One hundred percent of packaged conforming records pass the public
  validator and one hundred percent of indexed counterexamples fail for their
  intended requirement.
- **SC-003**: The conformance harness rejects static dispatch evidence
  conditioned on a registry head older than the coherent trusted snapshot.
- **SC-004**: Full repository validation introduces zero new failures.
- **SC-005**: The release inventory verifies every published family byte at the
  exact tagged commit.
- **SC-006**: A consuming domain can pin the released bundle and identify all
  required artifacts without relying on unpublished repository state.

## Assumptions

- The ratified OpenSpec change is the authoritative behavioral boundary.
- Concrete veto classes, detector rules, classifier prompts, runtime registry
  instances, and worker integration remain domain-owned.
- The next bundle number is allocated only after refreshing release tags.
- Release and archive claims are recorded only after their corresponding
  commits and remote tag are verifiably published.
