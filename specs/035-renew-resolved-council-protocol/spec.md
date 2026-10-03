# Feature Specification: Neutral resolved council protocol

**Feature Branch**: `035-renew-resolved-council-protocol`
**Created**: 2026-10-03
**Status**: Draft
**Input**: Brett Heap: "implement this"; then "ratify all three as disclosed".
**Governing change**: [renew-resolved-council-protocol](../../openspec/changes/renew-resolved-council-protocol/proposal.md)
**Ratification**: [exact reviewed revisions and owner word](../../openspec/changes/renew-resolved-council-protocol/review/ratification-2026-10-03.md)
**Owned behavior**: Canonical neutral contract, validation and shared conformance corpus. Domain interpretation and runtime admission remain owned by the successor repositories.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Agree on membership before work (Priority: P1)

The operator needs the producer and consumer to agree independently on the exact authorized membership and its authentic inputs before assigning work.

**Why this priority**: All later authority depends on the membership decision.
**Independent Test**: Evaluate the shared standing/conditional corpus independently; prove refusals produce zero submissions or zero admission writes at the relevant boundary.

**Acceptance Scenarios**:

1. **Given** an authorized immutable rule and authentic exact-head facts, **When** evaluated independently, **Then** both sides obtain the same ordered, nonempty, unique membership with reproducible consumed provenance.
2. **Given** unknown predicates/classes, unauthorized or unavailable rules, false/incomplete facts, malformed paths, secrets or invalid membership, **When** commission/admission is attempted, **Then** it refuses before new work or assignments.
3. **Given** head drift across gathering or immediately before submission, **When** submission is attempted, **Then** zero submissions occur with a named failure; drift after producer verification is refused independently at admission with zero assignments.
4. **Given** an admitted candidate, **When** retried identically, **Then** the same frozen snapshot and assignments return; a conflicting retry or transaction failure cannot partially replace them.

### User Story 2 - Accept only independently assigned seat returns (Priority: P1)

The operator needs each seat to hold only its own authority and completion to verify the exact admitted identities.

**Why this priority**: Equal seat counts and shared credentials do not establish individual authority.
**Independent Test**: Execute distinct seats, then exercise wrong-principal, shared-key, replay, challenge, missing/extra/duplicate return and isolation refusals.

**Acceptance Scenarios**:

1. **Given** frozen assignments, **When** seats execute, **Then** each isolated job obtains only its own authority and key; coordinator transport contains only public assignments and signed outputs.
2. **Given** correct possession proof from the wrong principal, expired/consumed challenge, shared fingerprint, cross-seat authority or old root authorization, **When** registration/return is attempted under the new protocol, **Then** it refuses atomically.
3. **Given** every required valid return, **When** completion is requested, **Then** the existing verdict is computed; a missing, duplicate, unlisted or same-count/wrong-identity return set cannot complete.
4. **Given** later head/rule changes, **When** existing work completes, **Then** the original frozen roster still governs; later work needs a new convening.

### User Story 3 - Activate and recover the matched pair (Priority: P2)

The operator needs an explicit staged release, matched switch and recoverable history.

**Why this priority**: A shared authority protocol cannot be safely switched on one side.
**Independent Test**: Rehearse dormant behavior, old/new historical audit, explicit selection, pause/drain, matched switch and paired rollback with evidence retained.

**Acceptance Scenarios**:

1. **Given** a deprecation minor then removal major, compatible published pins and verified identity, **When** the owner records a successful matched rehearsal and activation, **Then** the selected pair uses exactly one new protocol.
2. **Given** rejection or mismatched configuration, **When** processing is attempted, **Then** no fallback protocol is selected.
3. **Given** a failed switch, **When** rolled back, **Then** intake stays paused until both old configurations are verified, and signed new evidence remains verifiable under its own protocol.
4. **Given** local implementation tests only, **When** progress is reported, **Then** publication, credentials, deployment, merge and activation remain separately evidenced acts.

### Edge Cases

Empty/duplicate/reordered/same-count wrong membership; unsupported predicate/path/class; immutable rule accessible but unauthorized; false, truncated, changing-total or unused facts; both rename paths; head drift before/after POST; concurrent exact/conflicting retries; transaction rollback; wrong principal with valid proof; shared keys; expired/consumed challenges; cross-seat/cross-protocol replay; missing/extra/duplicate return; changed rule after freezing; insufficient broker capability; one-sided switch and rollback; old records after removal.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST define one explicitly selected protocol with council identity, subject pin, packet references and ordered, nonempty, unique required seats. (D1)
- **FR-002**: System MUST require full immutable candidate/rule references, matched class, typed predicates and consumed normalized facts; refuse unknown fields, mutable references, Boolean-only conclusions, unused inputs and secrets. (D1)
- **FR-003**: System MUST specify independent producer/consumer reproduction and independent verification of rule authority and fact authenticity; accessible immutable content alone is insufficient authority. (D1–D2)
- **FR-004**: System MUST require live-head verification and full validation before writes, then atomic frozen membership/provenance with exactly one durable assignment per seat, identical retry idempotency and conflicting retry refusal. (D2)
- **FR-005**: System MUST require frozen exact identities throughout execution/registration/completion; refuse same-count wrong identities, duplicate, missing or extra returns, and require a new convening for changed rules or heads. (D2)
- **FR-006**: System MUST require separate isolated jobs, distinct ephemeral keys and only each seat's authority; the coordinator receives only public assignments and signed outputs. (D3)
- **FR-007**: System MUST require registration to prove possession and independently authenticated, runtime-prebound assignment authority, with bounded one-use challenges; caller labels, shared workflow identity and all-seat credentials are insufficient. (D3–D4)
- **FR-008**: System MUST bind signed contexts to protocol, assignment, seat, council, candidate and digest using existing governed digest construction; refuse shared fingerprints, replay and old root authorization under the new protocol. (D3)
- **FR-009**: System MUST use the current governed repository identity and verified issuer/audience/subject/workflow revision/job evidence; distinguish workflow claims from subject and park activation without full broker enforcement. (D4)
- **FR-010**: System MUST publish shared positive and negative cases for separate producer/consumer implementations, including race, isolation, retry and authorization refusals; retain existing wallet trust controls outside worker registration. (D1–D4)
- **FR-011**: System MUST deprecate old shapes in a minor before breaking removal; explicitly select one active protocol without fallback and retain verification of historical records under their recorded protocol. (D5)
- **FR-012**: System MUST define matched pause/drain, activation rehearsal and paired rollback with evidence retained; keep version allocation/publication, pins, credentials, deployment and activation as distinct recorded owner acts. (D5)

### Key Entities *(include if feature involves data)*

- **Resolution**: immutable candidate, governed rule/class, consumed typed facts and ordered required seats.
- **Convening snapshot**: selected protocol, council, subject pin, packet references and frozen resolution.
- **Seat assignment**: one immutable seat authority per convening, authenticated holder and bounded lifecycle.
- **Registration and return**: public key/fingerprint, bounded proof/challenge and assignment-bound signed result.
- **Activation evidence**: compatible revisions, verified authority, disposed in-flight work, matched configuration and rollback disposition.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every shared positive/negative conformance case has the expected outcome in the producer and consumer's separate implementations.
- **SC-002**: Every admitted convening has exactly one immutable assignment per required seat; every refused admission or failed transaction leaves zero new assignments.
- **SC-003**: Every accepted return belongs to its required seat and assignment; every shared-key, wrong-principal, replay, missing/extra/duplicate-seat case refuses.
- **SC-004**: A full matched-switch and paired-rollback rehearsal preserves historical evidence and permits intake only after both sides are verified, with each operational act independently recorded.

## Assumptions

- The disclosed design and handoff matrix govern this specification. The scope contains no new unresolved policy decision.
- This session works outside a registered lane and makes no assignment or claim on behalf of codeXfactory-2 or another live lane.
- Canonical shape/corpus remains provider-owned; runtime implementations are independent and consume reviewed exact revisions.
- Deterministic corpus, race, isolation, authorization and migration verification are required. Consumer persistence acceptance uses real database transactions; simulations do not prove deployment.
- Versions are allocated at governed realization. Publication, pins, credentials, deployment and activation remain separate owner acts.
- Original 017 remains preserved until its accepted handoff, ownership release, recovery verification and durable publication conditions hold.
