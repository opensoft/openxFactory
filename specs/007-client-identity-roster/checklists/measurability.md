# Measurability Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation that every criterion is decided by a RUN rather
than by a reading — that "green" has a definition, that unmeasurable claims are
declared unmeasurable, and that each probe fails for its own reason.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## Criteria decide by running

- [x] CHK1201 Is each success criterion phrased so a run produces a verdict rather than a reader producing an opinion? [Measurability, Spec §SC-001–SC-014]
- [x] CHK1202 Is the green bar enumerated as commands with expected results, in one place? [Measurability, plan §The green bar]
- [x] CHK1203 Does each command in the green bar have a task that runs it? [Consistency, tasks §10.2–10.6]
- [x] CHK1204 Is "existing suites unaffected" defined as verdicts AND finding codes preserved, rather than as an exit code? [Measurability, Spec §FR-030, tasks §8.6]
- [x] CHK1205 Is the baseline that makes that comparison possible captured before the first edit, and kept out of the tracked tree? [Dependency, tasks §0.3]
- [x] CHK1206 For each modified capability, is the suite that proves it named — including the family that has no pytest suite at all? [Honesty, plan §Verification story]
- [x] CHK1207 Is the ONE measurement that could falsify the additivity claim identified as such? [Measurability, tasks §7.4]
- [x] CHK1208 Are the two STOP conditions stated with what triggers them? [Fail-closed, tasks §The two STOP conditions]

## Discriminations rather than assertions

- [x] CHK1209 Is the killed-flaw criterion a discrimination in one run rather than two separate assertions? [Measurability, Spec §SC-002]
- [x] CHK1210 Does each negative have a discrimination partner (a positive of the same shape without the defect)? [Measurability, plan §Cluster C, §Cluster D]
- [x] CHK1211 Is the blocking/reporting split measured as a pair over the same corpus? [Measurability, Spec §SC-006, ruling A-N4]
- [x] CHK1212 Is the misplacement criterion measured by a fixture placed where the rule is hardest (outside `credentials/` entirely)? [Measurability, Spec §SC-005]
- [x] CHK1213 Is the absence guarantee measured three ways including a source-level negative? [Measurability, Spec §SC-013]
- [x] CHK1214 Is the uniqueness rule's SCOPE measured, not only its content? [Measurability, Spec §FR-006] — FIXED this pass: repo fixture 1 now carries two clients' fragments with an identical tuple at exit 0.
- [x] CHK1215 Is the closed-vocabulary criterion measured per set, with no set left to a general claim? [Measurability, Spec §SC-014] — FIXED this pass: seven sets, seven probes.
- [x] CHK1216 Are the fixtures required to be authored so that a rule broader than intended FAILS the test rather than passing it? [Measurability, tasks §4.6]

## Unmeasurable claims are declared

- [x] CHK1217 Is the live refusal declared unmeasurable HERE, with the measured fact behind it and the follow-up that will measure it? [Honesty, Spec §SC-008]
- [x] CHK1218 Is nominal pack blocking declared, so "blocking" is not read as "firing in a domain's CI"? [Honesty, plan §Cluster F]
- [x] CHK1219 Is the pack's no-copy clause declared unprobed rather than implied to be tested? [Honesty, Spec §US3-AS3] — FIXED this pass in plan §Cluster F.
- [x] CHK1220 Is the cross-repository resolution of `evidence_ref` declared out of the validator's reach rather than left looking like a gap? [Honesty, Spec §FR-037]
- [x] CHK1221 Are claims about the estate that could go stale marked as preconditions to re-run rather than as facts? [Honesty, research §Decision 5, tasks §0.2]
- [x] CHK1222 Is the one pre-existing defect the feature declines to fix recorded with the reason? [Honesty, research §Decision 6]

## Probes fail for their own reason

- [x] CHK1223 Is "fails for the WRONG reason" a self-test failure mode rather than a review concern? [Measurability, Spec §FR-018]
- [x] CHK1224 Is a pinned detail substring required wherever a code alone could be satisfied incidentally? [Measurability, plan §Cluster B]
- [x] CHK1225 Is the named code required to appear even when a document is also schema-invalid? [Measurability, tasks §2.2] — FIXED this pass.
- [x] CHK1226 Is `red_proven` (suppress the code, watch the corpus go red) required per requirement row? [Measurability, tasks §10.1]
- [x] CHK1227 Is the reproduction of `red_proven` an existing procedure rather than a new script? [Clarity, tasks §10.1]
- [x] CHK1228 Are the self-test's five failure modes each distinguishable in output? [Observability, tasks §2.2]
- [x] CHK1229 Is determinism measured by comparing two runs' findings rather than by inspection? [Measurability, Spec §SC-011, tasks §6.6]
- [x] CHK1230 Is the vacuous-pass hazard that would make the determinism test meaningless called out where the test is specified? [Edge Case, ruling A-9, tasks §6.6]

## Notes

- Four items were fixed by edits made under other checklists in this pass (CHK1214,
  CHK1215, CHK1219, CHK1225); they are listed here because measurability is the lens
  under which each defect actually bites — a criterion whose probe does not exist, or
  whose probe cannot be read by the harness, is a criterion that will be claimed rather
  than met.
