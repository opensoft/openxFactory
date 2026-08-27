# Specification Quality Checklist: F1 — the modified-block-currency family module and its registrations

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-08-27
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

Three checklist items are met in a form worth stating, because the honest
reading of them for THIS feature is not the generic one.

- **"No implementation details."** The deliverable is a check family inside an
  existing Python package whose module path, registration points and reused
  helper are all NORMATIVE in the ratified delta and in the packet's task list —
  the delta writes the unit derivation, the matching rule and the marker grammar
  itself, and § 2.8 names the reader to reuse. Naming
  `scripts/doc_health/modified_block_currency.py`, `FAMILIES`, `FAMILY_IDS` and
  `promotion_fidelity`'s disposition reader is therefore restating the
  requirement, not leaking a design. The spec names no data structure, no
  function, no algorithm and no library; those are the plan's contracts.
- **"Written for non-technical stakeholders."** The stakeholder here is the
  doc-health steward and the OpenSpec packet author — the two readers of the
  finding. Every user story is written from one of those two seats and states
  what they see, never how it is computed.
- **"Success criteria are technology-agnostic."** SC-006 through SC-008 name
  three gate commands. They are the gates the ratified packet's archive
  condition names verbatim, and the outcome they measure — this feature's own
  registration cannot land while it corrupts the requirement it moves — has no
  technology-free spelling. Kept deliberately.

Two further notes for the planning phase:

- The six assumptions A1–A6 are readings of the delta, each with the line that
  settles it. Any of them being wrong is a plan-level defect and each is owed a
  pinning test; none of them is an open question for Brett.
- FR-031 (RED-first behavioural pins) is an orchestrator decision for this
  feature rather than a line of the delta, and it is recorded as a requirement
  because the tasks list has to be dependency-ordered around it.
