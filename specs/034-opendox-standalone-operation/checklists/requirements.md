# Specification Quality Checklist: openDox standalone operation (release 1)

**Purpose**: check that the specification is complete and of good quality
before implementation starts.
**Created**: 2026-09-24
**Feature**: [`spec.md`](../spec.md)

## Content quality

- [x] Every requirement names the #1144 requirement and the boxes it realizes
      (FR-001 to FR-010), so the packet stays the authority.
- [x] Nothing in spec.md restates, narrows or widens a ratified requirement.
      Contradictions go to Brett as R1Q1–R1Q22 instead.
- [x] The user stories are the release map's three phases, plus the
      invariant (US4).
- [x] Every mandatory section is complete: user scenarios, requirements,
      success criteria and assumptions.

## Requirement completeness

- [ ] No `[NEEDS CLARIFICATION]` remains. **Open:** 22 questions are recorded
      in `clarify-questions.md`, and they await Brett Heap. T004 encodes the
      answers.
- [x] Every requirement can be tested. Each FR cites #1144's own falsifier.
- [x] The success criteria can be measured: every one is a falsifier's exit
      status, or AT-R1's.
- [x] The acceptance test is defined term by term (spec.md § AT-R1), and its
      procedure is written (`quickstart.md`).
- [x] The edge cases are listed, each tied to its question.
- [x] The scope is bounded: release 2, Group 8 and F1–F4 are out, and the box
      accounting sums to 124.
- [x] Dependencies and assumptions are named: the 1.8 ratification record
      (landed, #1151), lane 4's C1, C3 and C4, and the pin chain.

## Feature readiness

- [x] Every release-1 box maps to a task (tasks.md § "Box accounting":
      69 = 63 + 1 + 1 + 4).
- [x] Every task names a repository, a falsifier, and any question that blocks
      it.
- [x] Parallel slices, and files limited to a single writer, are declared
      (plan.md; tasks.md § "Phase 1 writer slices").
- [ ] `/speckit-analyze` has reported no CRITICAL finding. **Pending:** T006,
      after the answers.

## Notes

- The two unchecked items are the constitution's own gates: material
  ambiguities are resolved, and analyze is clean. They are open on purpose.
  The brief asks for the plan before the answers, and forbids resolving the
  questions by assumption. plan.md § Complexity Tracking records the
  deviation.
