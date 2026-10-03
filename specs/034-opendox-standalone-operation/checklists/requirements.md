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
      Contradictions go to Brett as R1Q1–R1Q27 instead. A scenario text that
      an answer touches goes to him as RULING NEEDED (RN-1, plan.md).
- [x] The user stories are the release map's three phases, plus the
      invariant (US4).
- [x] Every mandatory section is complete: user scenarios, requirements,
      success criteria and assumptions.

## Requirement completeness

- [x] No `[NEEDS CLARIFICATION]` remains. All 27 questions are answered and
      encoded in spec.md § Clarifications: eleven on `#656` `5817152735`,
      which T004 encoded, fourteen on `5850003126`, which T019, T009 and T069
      encoded, and two on `5851950767`, which T067 encoded. RN-1 is ruled (a)
      and landed (#1170). No phase is provisional.
- [x] Every requirement can be tested. FR-001 to FR-010 each cite #1144's own
      falsifier. FR-011 is tested by AT-R1 (T095, T096), and FR-012 by each
      PR's review against its task's lines and its quoted falsifier output.
- [x] The success criteria can be measured. SC-001 to SC-005 are falsifier
      exit statuses, or AT-R1's verdict, and SC-001 also needs requirement
      3's text as RN-1 (a) amended it (#1170).
      SC-006 is a box count (`box_census.py`), and SC-007 is the state of
      openxFactory's required checks.
- [x] The acceptance test is defined term by term (spec.md § AT-R1), and its
      procedure is written (`quickstart.md`).
- [x] The edge cases are listed, each tied to the question, box or in-flight
      act that governs it.
- [x] The scope is bounded: release 2, Group 8 and F1–F4 are out, and the box
      accounting sums to 125 (124 until T007's batch M added 16.3a).
- [x] Dependencies and assumptions are named: the 1.8 ratification record
      (landed, #1151), lane 4's C1, C3 and C4, and the pin chain.

## Feature readiness

- [x] Every release-1 box maps to a task (tasks.md § "Box accounting":
      70 = 63 + 1 + 1 + 1 + 4, where one box, F9.2, closes after T008;
      batch M's 16.3a maps to T100).
- [x] Every realization task names a repository, a falsifier, any question
      that blocks it, and the rulings it carries out. A task that runs a
      falsifier (T074, T077, T093) names that falsifier as its own. The
      every-phase procedures (T090, T091) name every repository they touch,
      and AT-R1's halves (T095, T096) name the repository their harness or
      evidence lands in. Phase 0's holder tasks and the three checkpoints name
      the evidence they record, or the falsifiers they run, instead.
- [x] Parallel slices, and files limited to a single writer, are declared
      (plan.md; tasks.md's writer slices, one section per phase).
- [x] `/speckit-analyze` has reported no CRITICAL finding. T006's round-1a
      run found none (`evidence/analyze-round-1a.md`), and round 2's run over
      T019's, T009's and T069's re-plan found none either
      (`evidence/analyze-round-2.md`), nor did round 3's over T067's
      (`evidence/analyze-round-3.md`). Every finding each run raised is
      dispositioned in its record.

## Notes

- The constitution's first gate, material ambiguities resolved, was open on
  purpose until round 2: the brief asked for the plan before the answers, and
  forbade resolving the questions by assumption. Round 2 answered every
  question then open, none by assumption. Its analyze then found two more,
  R1Q26 and R1Q27, which went to Brett Heap in the same way, and he answered
  both on `5851950767`. T067 encoded them, so the item is ticked. The second
  gate, analyze, is clean for round 3's revision.
- T007's batch M (openxFactory#1219, RULED `5962785556`, item 2) added box
  16.3a and task T100 after round 3. No `/speckit-analyze` ran over that
  revision, and `evidence/analyze-round-3.md`, a record, still reads 90 tasks
  and 124 boxes. What ran instead is the plan's consistency checks, the
  persisted tools widened to batch M (brett-wip `712aedad`): 91 tasks, 104
  nodes and 233 edges, with no cycles, 0 chain gaps, 0 arrow mismatches, no
  phase gaps, the 4 known phase-1 NOT ORDERED pairs, and qcheck 27 of 27.
  A fresh analyze over T100 is the holder's to call. (That analyze has since
  run, as the next note records.)
- A `/speckit-analyze` pass ran on 2026-10-03 over `main` `ec9308c8`, after
  #1220 had added T099 and T101–T104, for lane openxfactory-4's holder. Its
  report went to the holder and is not a file of this feature. It found no
  CRITICAL finding, three HIGH, eight MEDIUM and nine LOW:
  - H1, the private copy's contract, is settled by T007's batch N (#1222 →
    `bdd0f586`);
  - H2, the help tree at 32, by `5970917267`, with the plan side in T086,
    T094, T100 and research R8, and #1144's side in a later batch, O;
  - H3, AT-R1's commit against the published one, by the holder's
    P-against-X step in T099 and T096 and quickstart.md's `RELEASE1_TIP`.

  The MEDIUM on what "usable" means is settled by `5971834845`. At `ec9308c8`
  the batch-M tools read 96 tasks, 109 nodes and 267 edges, with no cycles,
  0 chain gaps, 0 arrow mismatches, no phase gaps, the same 4 NOT ORDERED
  pairs, and qcheck 27 of 27. Once tasks.md's P3-E row names T075's
  `pyproject.toml` edit (openDox-code#73, landed), `sharedfiles.py` reports
  a fifth NOT ORDERED pair, P3-I against P3-E. It is benign in the same way:
  T072 is the only P3-I task that writes that file, T075 is After T072, and
  both have landed.
