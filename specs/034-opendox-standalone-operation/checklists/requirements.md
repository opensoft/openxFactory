# Specification Quality Checklist: openDox standalone operation (release 1)

Status: draft

**Purpose**: check that the specification is complete and of good quality
before implementation starts.
**Created**: 2026-09-24
**Feature**: [`spec.md`](../spec.md)

## Content quality

- [x] Every requirement names the #1144 requirement and the boxes it realizes
      (FR-001 to FR-010), so the packet stays the authority.
- [x] Nothing in spec.md restates, narrows or widens a ratified requirement.
      Contradictions go to Brett as R1Q1–R1Q25 instead. A scenario text that
      an answer touches goes to him as RULING NEEDED (RN-1, plan.md).
- [x] The user stories are the release map's three phases, plus the
      invariant (US4).
- [x] Every mandatory section is complete: user scenarios, requirements,
      success criteria and assumptions.

## Requirement completeness

- [ ] No `[NEEDS CLARIFICATION]` remains. **Partly open.** The eleven
      questions phase 1 needed are answered (`#656` `5817152735`) and encoded
      in spec.md § Clarifications. Fourteen remain open:
      - R1Q10–R1Q13, R1Q15–R1Q19 and R1Q23, for phases 2–3. T009 (phase 2)
        and T069 (phase 3) encode them as they are answered.
      - R1Q14, R1Q24 and R1Q25, for phase 1's T061 and T043, raised or
        brought in by T005's re-measure and T006's analyze. T019 encodes
        them.
      - R1Q21, on process.

      Until then, phases 2–3, T061 and T043 are PROVISIONAL and authorize no
      implementation.
- [x] Every requirement can be tested. FR-001 to FR-010 each cite #1144's own
      falsifier. FR-011 is tested by AT-R1 (T095, T096), and FR-012 by each
      PR's review against its task's lines and its quoted falsifier output.
- [x] The success criteria can be measured. SC-001 to SC-005 are falsifier
      exit statuses, or AT-R1's verdict, and SC-001 also needs RN-1 ruled.
      SC-006 is a box count (`box_census.py`), and SC-007 is the state of
      openxFactory's required checks.
- [x] The acceptance test is defined term by term (spec.md § AT-R1), and its
      procedure is written (`quickstart.md`).
- [x] The edge cases are listed, each tied to the question, box or in-flight
      act that governs it.
- [x] The scope is bounded: release 2, Group 8 and F1–F4 are out, and the box
      accounting sums to 124.
- [x] Dependencies and assumptions are named: the 1.8 ratification record
      (landed, #1151), lane 4's C1, C3 and C4, and the pin chain.

## Feature readiness

- [x] Every release-1 box maps to a task (tasks.md § "Box accounting":
      69 = 63 + 1 + 1 + 4).
- [x] Every realization task names a repository, a falsifier, any question
      that blocks it, and the rulings it carries out. A task that runs a
      falsifier (T074, T077, T093) names that falsifier as its own. The
      every-phase procedures (T090, T091) name every repository they touch,
      and AT-R1's halves (T095, T096) name the repository their harness or
      evidence lands in. Phase 0's holder tasks and the three checkpoints name
      the evidence they record, or the falsifiers they run, instead.
- [x] Parallel slices, and files limited to a single writer, are declared
      (plan.md; tasks.md § "Phase 1 writer slices").
- [x] `/speckit-analyze` has reported no CRITICAL finding. T006's round-1a
      run found none (`evidence/analyze-round-1a.md`), and every finding it
      raised is dispositioned there. T009, T019 and T069 run it again for the
      parts they re-plan.

## Notes

- The unchecked item is the constitution's first gate: material ambiguities
  are resolved. It is open on purpose. The brief asked for the plan before the
  answers, and forbade resolving the questions by assumption. Phase 1's
  questions are now answered, and phases 2–3's remain open. So do the three
  on T061 and T043: R1Q14, R1Q24 and R1Q25. plan.md § Complexity Tracking
  records both deviations. The second gate, analyze, is clean for this
  revision (T006).
