# Specification Quality Checklist: openxFactory consumes openXwallet and sheds the wallet paths (P3)

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-08-27
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs) — *with one
      deliberate exception class: this spec REALIZES a ratified change whose
      design names files, refusal codes and invocation strings as NORMATIVE. Those
      are requirements here, not implementation leakage; a spec that abstracted
      them would lose the very properties the council ratified.*
- [x] Focused on user value and business needs — the users are the openxFactory
      operator, the reviewer who must answer "which reader ran?", and the one live
      consumer.
- [x] Written for non-technical stakeholders — as far as a contract-governance
      change permits; every requirement states WHY.
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain — four questions arose and all four
      were answerable from measurement or from the ratified design, so they are
      recorded as a resolved Clarifications session rather than left as markers.
- [x] Requirements are testable and unambiguous — FR-001…FR-020, each with a
      named artifact or a named refusal code.
- [x] Success criteria are measurable — SC-001…SC-010.
- [x] Success criteria are technology-agnostic — *deliberately NOT, and this is
      the honest entry: SC-001 names a check token, SC-005 names refusal codes.
      A gate's success criterion IS the gate's name. Abstracting it would make the
      criterion unverifiable.*
- [x] All acceptance scenarios are defined — four user stories, thirteen scenarios.
- [x] Edge cases are identified — five, including the register row's 2026-11-23
      expiry, the unenforceable shared-tree freeze, and the pre-P3 checkout.
- [x] Scope is bounded — `tasks.md` §7 verbatim, 33 tasks, twelve path sets of
      which nine are deleted and three are named exceptions.
- [x] Dependencies and assumptions identified — including the two that gate merge
      (P5a.2 first; the operator's tag) and the one that had to be measured before
      anything was written (App reachability).

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria — eight of
      ten discharged locally at authoring; SC-001, SC-003 and SC-004 require CI
      and are recorded as they land.
- [x] No implementation details leak into specification — beyond the ratified
      normative ones noted above, which are declared rather than smuggled.

## Notes

- Two checklist items are answered NO-in-substance and marked with the reason
  rather than silently ticked: the ratified design's file names, refusal codes and
  invocation strings ARE requirements for this feature, and the success criteria
  that name a check token cannot be technology-agnostic without becoming
  unverifiable. Recording the tension is the point of the checklist; pretending it
  is absent would be the failure.
- Items requiring CI to close are listed in `tasks.md` Phase 9 and are not ticked
  here.
