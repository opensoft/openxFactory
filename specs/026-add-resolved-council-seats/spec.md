# Feature Specification: Resolved Council Seats

**Feature Branch**: `026-add-resolved-council-seats`

**Created**: 2026-08-28

**Status**: Draft

**Input**: User description: "Realize the ratified add-resolved-council-seats contract so a trusted domain producer resolves each convening's required seats from governed class rules and exact candidate facts, Hermes validates and freezes that roster before issuing seat jobs, and the producer/consumer cut over without a legacy protocol path."

## Delivery Boundary

This Speckit feature implements the domain-neutral openxFactory contract,
validator, conformance corpus, release registration, and successor handoff. The
requirements below describe the complete governed producer/consumer outcome.
Requirements that name Hermes runtime behavior or codexFactory production and
signing behavior remain blocking external acceptance gates until separately
identified successor features land in their owning repositories. Provider-local
completion MUST NOT be reported as end-to-end completion.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Admit the correct roster before work starts (Priority: P1)

A review operator can trust that every seat required for one candidate is known,
validated, and frozen before any seat receives work, including a conditional
company-policy seat only when its governed pull-in condition holds.

**Why this priority**: A convening started with the wrong roster cannot later
prove that its verdict represents every authority the governing rule required.

**Independent Test**: Submit standing-only and condition-triggered convenings
against the same governed class and verify that the admitted snapshots contain
the correct distinct rosters before any seat job is issued.

**Acceptance Scenarios**:

1. **Given** a candidate whose pull-in condition does not hold, **When** its convening is admitted, **Then** the frozen roster contains exactly the standing seats and one job is issued for each.
2. **Given** a candidate whose pull-in condition holds, **When** its convening is admitted, **Then** the frozen roster also contains the conditional seat and no job is issued before that roster is frozen.
3. **Given** a required roster that differs from evaluation of the cited rule and facts, **When** admission is attempted, **Then** the convening is refused and no seat jobs are issued.

---

### User Story 2 - Reproduce why each seat was required (Priority: P1)

A reviewer examining a convening can identify the exact candidate revision,
governed class rule, and candidate facts that produced its roster and can
reproduce the same answer without trusting an unsupported producer assertion.

**Why this priority**: Provenance is what turns a producer-selected list into a
governed roster rather than self-reported membership.

**Independent Test**: Re-evaluate the cited immutable rule against the recorded
facts and obtain the identical roster; then mutate or remove each provenance
input and verify admission refuses.

**Acceptance Scenarios**:

1. **Given** complete provenance bound to the candidate head, **When** the roster is reproduced, **Then** the derived and submitted seat sets are identical.
2. **Given** the candidate head changes after resolution, **When** admission is attempted, **Then** admission refuses and requests a fresh resolution.
3. **Given** an unavailable rule revision or missing condition fact, **When** admission is attempted, **Then** the system refuses rather than inferring a roster.

---

### User Story 3 - Complete only from the frozen roster (Priority: P2)

A reviewer receives a verdict only when every seat frozen at admission has
returned an admissible substantive result, and later policy edits or unexpected
seat returns cannot change that convening's electorate.

**Why this priority**: Completion integrity depends on using one roster from
admission through unanimity instead of recalculating membership at each stage.

**Independent Test**: Admit a valid roster, then test a missing required return,
an unlisted return, and a later rule revision; only the complete original roster
may participate in the verdict.

**Acceptance Scenarios**:

1. **Given** one frozen required seat has not returned, **When** completion is evaluated, **Then** no verdict completes and the candidate parks.
2. **Given** an unlisted seat submits a return, **When** the return is admitted, **Then** it is refused and does not affect counting or unanimity.
3. **Given** the governing rules change after admission, **When** the convening completes, **Then** it remains bound to its frozen rule revision and roster.

### Edge Cases

- The roster is absent, empty, malformed, contains duplicates, or names an undeclared seat.
- The roster omits a standing seat or includes a conditional seat whose condition is false.
- The producer records its conclusion but not the facts needed to reproduce it.
- The candidate is force-pushed between fact collection and admission.
- The governed rule revision is unavailable or its provenance resolves ambiguously.
- Two seat jobs attempt to use the same signing identity or private key material crosses a job boundary.
- A signed return wraps its outcome in a richer object rather than exposing a scalar verdict at the top level.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A trusted domain producer MUST resolve one `required_seats` roster before convening admission from the governed candidate-class rule and exact candidate facts.
- **FR-002**: The resolved roster MUST include all standing seats and exactly those conditional seats whose governed pull-in conditions hold.
- **FR-003**: The convening MUST carry provenance identifying the candidate repository, pull request, candidate head revision, matched class, governed rule location and immutable revision, and normalized facts used by the condition.
- **FR-004**: The admission boundary MUST reproduce the roster from the cited rule and facts and MUST refuse any mismatch or unevaluable input.
- **FR-005**: The admission boundary MUST reject absent, empty, malformed, duplicate, unknown, or standing-seat-incomplete rosters.
- **FR-006**: The validated roster and provenance MUST be frozen in the admission snapshot before any seat job is issued.
- **FR-007**: Exactly one seat job MUST be issued for each seat in the frozen roster, and a seat job MUST NOT add, remove, or independently derive membership.
- **FR-008**: Return admission, substantive-return counting, unanimity, and verdict completion MUST use only the frozen roster.
- **FR-009**: A missing required return MUST park the candidate; an unlisted return MUST be refused and excluded from the verdict.
- **FR-010**: Rich signed return objects MUST contribute their declared outcome value to unanimity without comparing unrelated signature or provenance fields.
- **FR-011**: Each seat MUST register and use its own ephemeral signing key within its corresponding job; private key material MUST NOT cross job boundaries.
- **FR-012**: Producer and consumer activation MUST be a coordinated hard cutover; an obsolete payload MUST NOT be reconstructed or accepted through a compatibility path.
- **FR-013**: Existing ordinary-review, manager-review, conditional-pull-in, substantive-return, unanimity, verdict-less failure, and open-run recovery behavior MUST remain unchanged except where the resolved roster determines membership.
- **FR-014**: Local evidence MUST be recorded separately from live GitHub OIDC, deployment, image, merged-commit, or release evidence and MUST NOT imply that an unavailable live act occurred.

### Key Entities

- **Resolved required-seat roster**: The unique seat identifiers required for one candidate at one immutable revision.
- **Roster provenance**: The governed rule identity and exact candidate facts from which the roster can be reproduced.
- **Frozen convening snapshot**: The immutable admission record binding candidate, roster, provenance, and issued seat jobs.
- **Seat return**: One seat's signed substantive result, whose outcome participates in verdict comparison while its signature proves the returning job identity.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In 100% of accepted convenings, the roster is validated and frozen before the first seat job is issued.
- **SC-002**: Standing-only and condition-triggered fixtures reproduce the submitted roster exactly, while every invalid-provenance fixture is refused before work begins.
- **SC-003**: A convening cannot complete when any of its frozen required seats lacks an admissible substantive return.
- **SC-004**: Zero unlisted seat returns contribute to substantive-return counts, unanimity, or verdict completion.
- **SC-005**: Zero seat signing private keys are persisted, shared between jobs, or included in a convening or return artifact.
- **SC-006**: All pre-existing ordinary-review, manager-review, recovery, and verdict-failure regression suites retain their prior verdicts.
- **SC-007**: Zero obsolete producer payloads pass the activated admission boundary.

## Assumptions

- Candidate-class rules remain authored and governed by the domain factory; openxFactory defines only the neutral handoff and admission obligations.
- The trusted producer can obtain authoritative candidate facts and bind them to an immutable candidate head before admission.
- Hermes can resolve the cited immutable rule revision for validation without becoming the rule author.
- Coordinated activation can temporarily park convenings if deployment ordering fails; this is safer than dual-protocol acceptance.
- Live GitHub and deployment proof may require operator credentials unavailable to local validation and will remain explicitly open when unavailable.
