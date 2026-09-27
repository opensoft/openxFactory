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

- [x] No `[NEEDS CLARIFICATION]` remains. All 25 questions are answered and
      encoded in spec.md § Clarifications: eleven on `#656` `5817152735`,
      which T004 encoded, and fourteen on `5850003126`, which T019, T009 and
      T069 encoded. RN-1 is ruled (a) and landed (#1170). No phase is
      provisional.
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
      run found none (`evidence/analyze-round-1a.md`), and round 2's run over
      T019's, T009's and T069's re-plan found none either
      (`evidence/analyze-round-2.md`). Every finding either raised is
      dispositioned in its record.

## Notes

- The constitution's first gate, material ambiguities resolved, was open on
  purpose until round 2: the brief asked for the plan before the answers, and
  forbade resolving the questions by assumption. Every question is now
  answered by Brett Heap, none by assumption, so the item is ticked. The
  second gate, analyze, is clean for this revision (round 2).
