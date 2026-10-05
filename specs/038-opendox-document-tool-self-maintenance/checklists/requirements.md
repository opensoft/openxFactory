# Specification Quality Checklist: openDox, the document tool and self-maintenance (release 2)

Status: draft

**Purpose**: check that the specification is complete and of good quality
before `/speckit.clarify` and `/speckit.plan`.
**Created**: 2026-10-05
**Feature**: [`spec.md`](../spec.md)

## Content quality

- [x] Every functional requirement names the #1144 requirement and the boxes it
      realizes (FR-001 to FR-025), so the packet stays the authority.
- [x] Nothing in spec.md restates, narrows or widens a ratified requirement or
      scenario. Contradictions go to Brett as R2Q1–R2Q24 instead, six of them
      marked as contradictions.
- [x] The user stories follow the release map: phase 4 (US1 submit, US2 land),
      phase 5 (US4 health, US5 the fix loop and exceptions, US6 packs), plus the
      invariant in every phase (US3).
- [x] Every mandatory section is complete: user scenarios, requirements,
      success criteria and assumptions.
- [x] Implementation names appear only where #1144's boxes name them (protocol,
      verb, route, file and migration names), because the boxes are the
      contract this feature realizes. No technology is chosen here that the
      packet does not already choose.

## Requirement completeness

- [ ] No `[NEEDS CLARIFICATION]` remains. **Open:** 24 questions are recorded in
      `clarify-questions.md`, and they await Brett Heap. The markers in spec.md
      each name the question that settles them, and every question is cited by
      at least one functional requirement. The same file defers 35
      design-level questions to the plan, each with a proposed default, and
      maps all 61 inventory candidates and this feature's own seven.
- [x] Every requirement can be tested. Each FR cites #1144's own falsifier
      (F6.1, F12.1, F12.2, F14.1, F15.1, F11.1) or a named test node.
- [x] The success criteria can be measured: each is a falsifier's exit status,
      a box count (37 release-2 boxes), or a zero count of a forbidden outcome.
- [x] The edge cases are listed, each tied to its box or its question.
- [x] The scope is bounded. Release 1's groups, Group 8, and F1–F4 are out. The
      release-2 boxes number 37: Group 6 has 4, Group 12 has 11, Group 14 has
      10 and Group 15 has 12.
- [x] Dependencies and assumptions are named: release 1's completion, the
      `doc_health` direction arc (R1Q6 (d), T008), the bundled store's
      ownership (R1Q16), the pins (9.5), and the live trees measured on
      2026-10-05. The risks are named too: the reference sandbox is
      unavailable by default on every target measured, 12.5 cannot pass in
      any environment measured, and three release-1 invariants stand in the
      way of three boxes.

## Feature readiness

- [x] Every functional requirement has acceptance criteria, through its user
      story's scenarios and its falsifier.
- [x] The user scenarios cover the primary flows: submit, land, see health,
      repair and accept, extend by packs, and the governed host unchanged.
- [ ] The feature meets the measurable outcomes in Success Criteria.
      **Pending:** realization, after the plan is ruled.
- [ ] `/speckit-analyze` has reported no CRITICAL finding. **Pending:** after
      clarify, plan and tasks.

## Notes

- The three unchecked items are open on purpose. The brief asks for
  `/speckit.specify` alone, and forbids resolving the questions by assumption.
  The constitution's gates (material ambiguities resolved before planning, and
  analyze clean before implementation) close in later steps.
- The stock template caps `[NEEDS CLARIFICATION]` at three markers. This
  feature follows the lane brief and the global clarify override (at most 25
  questions), because each marker stands for a point that #1144 or its rulings
  genuinely leave open. Round 1 uses 24 of the 25, and round 2 is empty.
