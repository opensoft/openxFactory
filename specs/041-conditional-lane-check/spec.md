# Feature Specification: Conditional Lane Check

**Feature Branch**: `041-conditional-lane-check`
**Created**: 2026-11-10
**Status**: Draft
**Input**: Restore Amendment 21 through the governed repository process.

## User Scenarios & Testing

### User Story 1 - Outside-lane documentation can be reviewed (Priority: P1)

An author working outside a lane opens an ordinary PR without fabricating a lane.

**Independent Test**: Run the actual workflow body validator against absent, empty and ordinary prose bodies; each succeeds.

**Acceptance Scenarios**:
1. **Given** an author outside a lane, **When** the body contains no declaration, **Then** the lane check succeeds.
2. **Given** an empty body, **When** the check runs, **Then** no attribution is demanded.

### User Story 2 - Real lane declarations remain meaningful (Priority: P1)

A lane-bound author supplies its actual lane in the established location and format.

**Independent Test**: Valid declarations pass; malformed, misplaced and duplicate declarations fail.

**Acceptance Scenarios**:
1. **Given** one valid first declaration, **When** the check runs, **Then** it succeeds.
2. **Given** a malformed or later declaration, **When** the check runs, **Then** it fails.

### Edge Cases

CRLF, whitespace-only leading lines, optional suffixes, duplicates, lowercase or indented labels, invalid names, prose mentions and shell-like text.

## Requirements

### Functional Requirements

- **FR-001**: An absent lane declaration MUST pass without lane enrollment.
- **FR-002**: Supplied declarations MUST be unique and valid in the first nonempty line.
- **FR-003**: Bot exemptions, protection requirements, events and permissions MUST remain unchanged.
- **FR-004**: PR body text MUST remain inert input and MUST NOT be re-emitted as a workflow command.
- **FR-005**: Regression checks MUST execute the actual validation logic.

### Key Entities

PR body, optional lane declaration, validation result. No persistent state or credential is introduced.

## Success Criteria

- **SC-001**: Every declared absent/valid case succeeds and every malformed/misplaced/duplicate case fails.
- **SC-002**: Untrusted body text causes zero command execution and zero protection changes.
- **SC-003**: Previously blocked design PRs receive a passing lane-line result after adopting the correction.

## Assumptions and Scope

Actual launch/binding determines lane membership under Amendment 21. This feature does not attest it. The existing global decision supplies policy; the local proposal records its authorized realization.
