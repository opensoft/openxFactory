# Edge-Case and Scenario-Class Coverage Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation that the requirements cover all five scenario
classes — primary, alternate, exception/error, recovery, non-functional — and that
each named edge case is dispositioned rather than merely noticed.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## Primary and alternate flows

- [x] CHK1301 Is the primary flow (a domain publishes a truthful fragment and receives a real refusal when it understates) covered by requirements end to end? [Coverage, Spec §US1]
- [x] CHK1302 Is the alternate flow of provider-forced breadth covered as CONFORMANT rather than as an error? [Coverage, Spec §FR-009]
- [x] CHK1303 Is the alternate flow of a not-yet-created identity (`planned`) covered with both its guarantees? [Coverage, Spec §FR-013]
- [x] CHK1304 Is the alternate flow of a retired identity covered, and instantiated? [Coverage, Spec §FR-013] — FIXED this pass: a `retired` entry now exists in the packaged corpus (tasks §3.5).
- [x] CHK1305 Is the alternate flow of a single-act admission covered, given a rule requires a LIST? [Edge Case, plan §ratified-constraint row 7, ruling A-N3]
- [x] CHK1306 Is the alternate flow of a domain holding no client-tenant identities covered (publishes nothing; refused by nothing)? [Coverage, Spec §Edge Cases, §FR-022]
- [x] CHK1307 Is the alternate flow of a single-domain client covered for the cross-domain pass (skip with a reason, intra-repo gate unaffected)? [Coverage, Spec §Edge Cases, §US5-AS3]
- [x] CHK1308 Is the mixed corpus (some clients composable, others not) covered, so a skip cannot suppress real findings? [Edge Case, research §Decision 6]

## Exception and error paths

- [x] CHK1309 Is every named violation given an error path with its own rule name? [Coverage, Spec §FR-016, §SC-001]
- [x] CHK1310 Is the error path for a misplaced instance covered, including the case where the only validator that scans the tree skips unknown kinds? [Edge Case, Spec §Edge Cases, §FR-036]
- [x] CHK1311 Is the error path for an obligation naming a renamed or removed gate covered? [Edge Case, Spec §Edge Cases, §FR-011]
- [x] CHK1312 Is the error path for a citation that resolves to nothing covered, distinct from a citation that is absent? [Edge Case, Spec §FR-014]
- [x] CHK1313 Is the error path for a citation that resolves to an instrument NOT in force covered — for the entries the in-force test binds, and NOT for a `retired` entry, whose ended instrument is the expected state? [Edge Case, Spec §FR-014] — AMENDED by gate ruling G1: the path is now a DISCRIMINATION, not a bare error path. Repo fixture 8 (an `enrolled` entry citing a `terminated` instrument that resolves) is the refusal, and repo fixture 1's `retired` entry citing that same instrument is the clean partner; the refusal carries its own code, distinct from fixture 6's unresolvable-citation code.
- [x] CHK1314 Is the error path for an admission act that claims verification it cannot evidence covered? [Edge Case, Spec §FR-002] — FIXED this pass: the pair rule gives this path a predicate and a code.
- [x] CHK1315 Is the error path for an act on a surface the entry never declared covered? [Edge Case, Spec §FR-009] — FIXED this pass.
- [x] CHK1316 Is the error path for a mapping that answers for some surfaces and not others covered? [Edge Case, Spec §FR-008] — FIXED this pass.
- [x] CHK1317 Is the error path for a harness failure (as opposed to a finding) given its own exit code? [Exception, Spec §FR-015]
- [x] CHK1318 Is the error path for a corpus defect (probe without file, file without probe) treated as an error rather than a warning? [Exception, Spec §FR-018]
- [x] CHK1319 Is the boundary case of a free token used without a legend entry covered, and the case of a token declared twice? [Edge Case, Spec §FR-034]
- [x] CHK1320 Is the boundary case of two entries differing only in a free token covered on BOTH sides (genuine pair clean, alias pair refused)? [Edge Case, Spec §FR-038]
- [x] CHK1321 Is the boundary case of two clients with identical tuples covered? [Edge Case, Spec §FR-006] — FIXED this pass.
- [x] CHK1322 Is the boundary case of a provider whose narrowest permission spans surfaces covered as conformant when declared? [Edge Case, Spec §Edge Cases]
- [x] CHK1323 Is the boundary case of an identity on a surface outside the vocabulary covered as neither rosterable nor a finding? [Edge Case, Spec §Edge Cases]
- [x] CHK1324 Is the boundary case of an admission act verified long ago covered by an explicit no-decay decision rather than by silence? [Edge Case, Spec §FR-033]
- [x] CHK1325 Is the boundary case of an entry whose every act is unverified dispositioned (reach empty; not a finding in this release)? [Edge Case, Spec §FR-003, §FR-032] — Checked: exclusion is the specified behaviour, no completeness rule may fire on the resulting empty reach, and the refusal added this pass targets a CLAIMED verification rather than an absent one, so the permissive axis is untouched.

## Recovery and rollback

- [x] CHK1326 Where the feature mutates the tree (a bundle cut), is the failure mode fail-closed and the previous state intact? [Recovery, tasks §9.6, research §Registration mechanics]
- [x] CHK1327 Is the recovery path for a consumer pinned to the previous bundle addressed by additivity rather than by migration? [Recovery, Spec §FR-030, research §Decision 3]
- [x] CHK1328 Is the recovery path for a drifted identity stated as withholding OUR credential rather than as remediating THEIRS? [Recovery, Spec §FR-027, §FR-028]
- [x] CHK1329 Is the recovery path after consent withdrawal specified to reach the identity and its admission, not only the credential? [Recovery, Spec §FR-026]
- [x] CHK1330 Is the escalation path for the one precondition that can fail specified, including what must NOT be done instead? [Recovery, tasks §0.1]
- [x] CHK1331 Is the escalation path for an unreachable external checkout specified rather than left to a quiet skip? [Recovery, tasks §0.3]
- [x] CHK1332 Is the STOP condition for a killed-flaw regression stated as stopping the work rather than filing a finding? [Fail-closed, tasks §The two STOP conditions]

## Non-functional

- [x] CHK1333 Are determinism and hermeticity stated as requirements rather than as qualities? [Non-Functional, Spec §SC-011]
- [x] CHK1334 Is the absence of a performance requirement defensible (batch validators over a handful of YAML files; no latency budget in any ratified clause)? [Non-Functional, Scope] — Considered and dispositioned: no requirement, delta scenario or ruling states a time budget, and the corpus is bounded by the number of fragments a repo publishes.
- [x] CHK1335 Is the security-relevant non-functional surface covered elsewhere rather than omitted? [Non-Functional, see authority-safety.md]
- [x] CHK1336 Is the operational surface (what a reader of a report or a gate failure sees) covered elsewhere rather than omitted? [Non-Functional, see reporting-diagnostics.md]

## Notes

- Four items were fixed by edits made under other lenses (CHK1304, CHK1314, CHK1315,
  CHK1316, CHK1321). CHK1325 is the item worth re-reading at implementation: the pass
  deliberately did NOT make an all-unverified entry a finding, because that would be a
  completeness rule wearing a verification costume.
