# Feature Specification: Recover NotebookLM tooling hardening

**Feature Branch**: `036-recover-notebooklm-hardening`
**Created**: 2026-10-03
**Status**: Draft
**Input**: Implement the accepted recovery plan while preserving current main.

## User Scenarios & Testing

### User Story 1 — Preserve operators' workflows (Priority: P1)

An operator runs existing lifecycle, import, session, hosting, parity and sweep
commands after recovery and gets the same decisions, operations and results.

**Why this priority**: Recovery must retain fixes already relied on.
**Independent Test**: Replay current hermetic scenarios through the public path
and compare provider operations, persisted state and refusals.

**Acceptance Scenarios**:

1. **Given** a large source still ingesting, **When** sync applies, **Then**
   readiness and settled title checks use source identity; a stranded upload
   is adopted only after its content digest agrees.
2. **Given** pinned governed products and session worktrees, **When** discovery
   runs, **Then** current membership, titles and ownership are retained.
3. **Given** mismatched hosting/profile state, **When** an operator requests
   a provider act, **Then** current declaration resolution and refusal remain.

### User Story 2 — Maintain focused responsibilities (Priority: P2)

A maintainer can change a single responsibility and validate its boundaries
without navigating the combined implementation and test module.

**Why this priority**: Useful unpublished work should survive cleanup.
**Independent Test**: Exercise malformed provider data, profile drift and
unavailable optional integrations at the recovered boundaries.

**Acceptance Scenarios**:

1. **Given** malformed provider output, **When** reconciliation reads it,
   **Then** invalid required fields are rejected before mutation.
2. **Given** unavailable dashboard support, **When** a lifecycle-only command
   runs, **Then** current lazy loading and degradation remain available.

### User Story 3 — Prevent scoped quality debt (Priority: P3)

A maintainer runs one quality command and receives actionable findings for new
sync defects without unrelated repository debt obscuring them.

**Why this priority**: Recovery must remain verifiable after cleanup.
**Independent Test**: Introduce isolated quality defects and prove the command
fails, while the clean surface passes every required checker.

**Acceptance Scenarios**:

1. **Given** clean implementation/tests, **When** the gate runs, **Then** every
   declared checker reports zero findings.
2. **Given** a missing checker, **When** the gate runs, **Then** it refuses
   explicitly rather than claiming a complete pass.

### Edge Cases

Malformed provider envelopes; reverted rename titles; similarly named uploads
with different digests; profile drift; threshold-sized sources; absent optional
support; ambiguous/retired sessions; linked checkouts; hosting path overrides;
peer-owned dirty worktrees; unavailable quality tools.

## Requirements

### Functional Requirements

- **FR-001**: Preserve the public command path, flags, precedence, outputs,
  exits and directly consumed helper behavior.
- **FR-002**: Preserve readiness, settled-title verification, digest adoption
  and refusal without minting duplicate sources.
- **FR-003**: Preserve corpus membership, unique titles, workspace records,
  hosting resolution and session ownership/registration.
- **FR-004**: Validate provider/state boundaries before acting; preserve
  profile-drift refusal and optional-integration degradation.
- **FR-005**: Recover focused implementation/tests with acyclic dependencies
  and the governed module-size ceiling.
- **FR-006**: Enforce all declared quality checks with zero findings and refuse
  explicitly when any required checker is unavailable.
- **FR-007**: Retain both snapshots' meaningful scenarios and supported test
  discovery modes without invoking the live provider.
- **FR-008**: Record disposition/restoration evidence before deleting the
  superseded ref/worktree after the reviewed replacement lands.

### Key Entities

- **Notebook/source identity**: Provider identity, alias, title and content.
- **Projection state**: Desired membership, observed state and content hashes.
- **Hosting/session boundary**: Declaration, profile, repository, branch,
  worktree and registration owner.
- **Recovery snapshot**: Original ref/tip, preserved history and replacement
  realization evidence.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every current and recovered acceptance scenario passes without
  contacting the live provider.
- **SC-002**: Every declared quality check reports zero findings and negative
  probes produce actionable failures.
- **SC-003**: Recovered responsibilities meet their size ceiling with no cycle.
- **SC-004**: The original snapshot is independently restorable and no old ref
  or worktree is removed before the reviewed replacement lands.

## Assumptions

Existing lifecycle projection remains authoritative. Recovery introduces no
provider mutation policy, authentication migration, runtime dependency or
contract release. Current main is the compatibility baseline. Original
snapshots/working files remain in the verified external cleanup archive.
