# Specification Quality Checklist: openDox, the document tool and self-maintenance (release 2)

Status: draft

**Purpose**: check that the specification is complete and of good quality
before `/speckit.plan`.
**Created**: 2026-10-05
**Re-run**: 2026-10-05, after clarify round 1 was answered (#656 `6003486656`);
notes updated 2026-10-06 for the plan ruling (#656 `6013547504`).
**Feature**: [`spec.md`](../spec.md)

## Content quality

- [x] Every functional requirement names the #1144 requirement and the boxes it
      realizes (FR-001 to FR-025), so the packet stays the authority.
- [x] Nothing in spec.md changes a ratified requirement or scenario.
      - Round 1's answers take effect in one of three ways: as readings,
        recorded in § Assumptions with their answer; as bookkeeping
        amendments to #1144's falsifiers and task lines, in FR-025; or as
        choices #1144 left to the realization.
      - R2Q19 and R2Q20, the only questions that asked whether to amend
        requirement text, were answered "keep as ratified".
- [x] The user stories follow the release map: phase 4 (US1 submit, US2 land),
      phase 5 (US4 health, US5 the fix loop and exceptions, US6 packs), plus the
      invariant in every phase (US3).
- [x] Every mandatory section is complete: user scenarios, requirements,
      success criteria and assumptions.
- [x] Implementation names appear only where #1144's boxes or round 1's answers
      name them (protocol, verb, route, file, migration and CI-runner names),
      because they are the contract this feature realizes. No technology is
      chosen here that the packet or an answer does not already choose.

## Requirement completeness

- [x] No `[NEEDS CLARIFICATION]` remains. Brett Heap answered all 25 round-1
      questions with option (a) (#656 `6003486656`).
      - spec.md § Clarifications records them as 25 `Q: … → A: …` bullets.
      - `clarify-questions.md` carries each answer inline.
      - Every requirement that a question held now states the ruled behaviour
        and cites its answer as `R2Qn (a)`. 18 of the 25 FRs changed.
      - The 34 design-level questions deferred to the plan keep their proposed
        defaults, for Brett to rule with the plan. None of them makes an FR
        conditional.
- [x] Every requirement can be tested. Each FR cites #1144's own falsifier
      (F6.1, F12.1, F12.2, F14.1, F15.1, F11.1), as amended where FR-025 records
      it, or a named test node, or AT-R2 (FR-024).
- [x] The success criteria can be measured. Each is one of:
      - a falsifier's exit status;
      - a box count (37 release-2 boxes);
      - a zero count of a forbidden outcome;
      - a pinned number (`EXPECT_SKIPPED` 11);
      - AT-R2's two halves (SC-008).
- [x] The edge cases are listed, each tied to its box or its answer.
- [x] The scope is bounded. Release 1's groups, Group 8, and F1–F4 are out, and
      so are the follow-ons the answers name: a standalone session opener and
      Save, a Seatbelt realization, a macOS CI job, and F2's `stack.yaml`
      lockstep check. The release-2 boxes number 37: Group 6 has 4, Group 12
      has 11, Group 14 has 10 and Group 15 has 12.
- [x] Dependencies and assumptions are named:
      - release 1's completion;
      - the `doc_health` direction arc (R1Q6 (d)): asked and RULED before
        planning, ARC-Q1 to ARC-Q4 all (a) (#656 `6003918488`; T006, T007);
        its realization (T070 to T077) gates F9.2, not 12.5, which F12.1 runs
        composed permanently (CF-5; Copilot's review of `c93ae88b`);
      - the bundled store's ownership (R1Q16);
      - feature 007's four named exceptions (R2Q6 (a));
      - the pins and the two owed cuts (9.5, R2Q22 (a), R2Q23 (a));
      - the live trees measured on 2026-10-05.
- [x] The risks are named:
      - the reference sandbox is unavailable by default, and CI is made capable
        by R2Q17 (a);
      - 12.5's 174 reds have a phase-4 repair slice (R2Q8 (a));
      - three invariants are met by named acts, which must land in their Rule 6
        window;
      - two texts go unrealized by Brett's acceptance (R2Q2 (a) with R2Q3 (a));
      - a repository with no `main` cannot land (R2Q7 (a)).

## Feature readiness

- [x] Every functional requirement has acceptance criteria, through its user
      story's scenarios and its falsifier.
- [x] The user scenarios cover the primary flows: submit, land, see health,
      repair and accept, extend by packs, and the governed host unchanged. They
      also cover the answers' added cases: the default branch refused, the
      served checkout fast-forwarded, a hosted install refused, evidence as
      locators, and no sandbox with the product's checks still running.
- [ ] The feature meets the measurable outcomes in Success Criteria.
      **Pending:** realization, after the plan is ruled.
- [ ] `/speckit-analyze` has reported no CRITICAL finding. **Pending:** round
      1's analyze (`evidence/analyze-round-1.md`) reported CRITICALs, all
      applied at `6847e99e`, and both reviewers' re-check found them landed as
      worded (`#656` `6013547504`). A fresh analyze of the ruled revision is
      T003, the holder's call; Brett's ruling started implementation.

## Notes

- The two unchecked items are open on purpose. The constitution's last gate,
  analyze clean before implementation, stands as the second item says, and the
  outcomes are measured on realization.
- The stock template caps `[NEEDS CLARIFICATION]` at three markers. This
  feature followed the lane brief and the global clarify override (at most 25
  questions): round 1 used all 25, round 2 was empty, and lane openXfactory-3
  checked the block twice before Brett answered it.
- Interplay between answers, reported to the holder, and since ruled with the
  plan (`#656` `6013547504`):
  - R2Q1 (a)'s "the same in every mode" against R2Q3 (a)'s "no host carries
    the verbs" (FR-004): CF-1, every governance mode under openDox's own
    profile;
  - R2Q7 (a)'s `main` against R2Q12 (a)'s baseline, which needed a run at
    `main`'s tip: I-2 (a), the baseline branch is `main`, else the branch HEAD
    names.
