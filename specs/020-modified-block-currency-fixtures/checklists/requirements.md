# Specification Quality Checklist: The modified-block-currency regression-fixture catalogue

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-08-27
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
      *Judged against this feature's real subject.* The deliverable IS a test
      and fixture catalogue, so fixture paths, test-function names and the
      packet's own § 3 item numbers are the feature's VOCABULARY, not leaked
      implementation. What is deliberately absent: how any assertion is
      written, what any helper is called, and any change to the module under
      test. Same standard F1's spec was accepted under.
- [x] Focused on user value and business needs — the value is that two caught
      governance defects cannot recur unnoticed, and that a reader can tell
      which obligations were already discharged.
- [x] Written for non-technical stakeholders — every user story states the
      real defect it protects against before naming any artefact.
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain — zero were raised. Every
      candidate ambiguity was settled by the packet, the ratified delta, an
      orchestrator decision, or measured evidence, and each is recorded in
      Assumptions A1–A9 with what settles it.
- [x] Requirements are testable and unambiguous — FR-001..FR-028 each name a
      § 3 item or an orchestrator decision and an observable outcome.
- [x] Success criteria are measurable — SC-001..SC-012 name titles, units,
      counts of tests, and command outcomes.
- [x] Success criteria are technology-agnostic *(as far as this feature
      permits)* — SC-008/SC-009/SC-010 name the two gate commands and the diff
      boundary, which are the project's own ratified gates (Constitution
      Principle V) rather than incidental tooling.
- [x] All acceptance scenarios are defined — five user stories, thirteen
      acceptance scenarios.
- [x] Edge cases are identified — six, including the two that shaped the
      assertions (clause-count vs unit-count; the rendered finding's
      truncation).
- [x] Scope is clearly bounded — Out of Scope names F3, F4, § 7.1, § 7.2, the
      archive act, and re-testing satisfied items.
- [x] Dependencies and assumptions identified — F1 on `main` at `19e3f6b5`,
      the packet, this repository's git history, the conftest harness, and the
      promotion-fidelity precedent.

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows — the two reconstructions, the audit,
      the marker gap, the derivation gaps, and provenance/determinism.
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification — see the first item's
      note on this feature's vocabulary.

## Notes

- Validated in one iteration; no item required a spec edit beyond normalizing
  the § 3 item count (thirteen numbered items, fourteen rows with 3.3a).
- **A4 is the load-bearing assumption and it was VERIFIED before the spec was
  written**, not assumed: both histories were recovered from git and both
  reconstructions were run through the family, reproducing #351's two omitted
  titles and #329's seven exactly. The commits are recorded in A4.
- The `before_specify` git hook (`speckit.git.feature`) was NOT run: the
  feature branch `020-modified-block-currency-fixtures` and this feature
  directory already exist, created by the orchestrating session, and running
  the hook would allocate a second branch and feature number. Recorded here
  because a skipped mandatory hook should be visible.
