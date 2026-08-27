# Specification Quality Checklist: The modified-block-currency self-gate

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

**Two items are held deliberately, and the reasons are recorded rather than
waved through.**

1. **"No implementation details" is satisfied in the sense that matters and
   knowingly bent in one.** The subject of this feature IS a check family and
   its report, so the named subjects (`add-composed-view-authoring`,
   `Gate verbs hide on a composed view`, `openspec/specs/doc-health/spec.md`)
   and the one CLI flag (`--skip-family modified-block-currency`) are the
   feature's *domain vocabulary*, not its implementation. A spec that said
   "assert the findings by name" without naming them would be untestable, which
   is the checklist item one row down. No language, framework, module path or
   function name appears in a requirement.

2. **The corpus figures are dated, not asserted as permanent.** FR-006/FR-007
   name subjects measured at `76a2ad27`; the Assumptions section says so and
   FR-016 requires every such assertion to fail with the re-measure
   instruction. This is the only honest shape for a gate whose subject is a live
   corpus, and it is why SC-001 is about the failure message rather than about
   the passing state.

**No [NEEDS CLARIFICATION] markers were needed.** The three questions that
could have been asked were settled by the orchestrator's reconciliation ruling
before authoring (the stale § 4.1 count, the stale § 4.2 basis, and whether
§ 4.3–4.5 are tests or gates); they are recorded as decisions in `plan.md`,
flagged for veto, rather than put to the user twice.
