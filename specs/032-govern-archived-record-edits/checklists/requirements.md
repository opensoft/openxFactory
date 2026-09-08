# Checklist: Requirements Quality — Govern Archived-Record Edits

**State**: written 2026-09-08, NOT YET RUN — this file is the gate instrument for the architect's refutation panel. The findings its authoring raised were resolved in the analyze loop and are recorded in [`../analysis.md`](../analysis.md).

Cross-cutting requirements-quality gate over `spec.md`'s 19 functional
requirements, 8 success criteria, three user stories and ten answered
clarifications for feature `032-govern-archived-record-edits`. Every item below
interrogates the WRITTEN REQUIREMENTS — never the doc-lifecycle bullet, the
`tasks.md` ticks, or the gate runs themselves. Audience: the release-gate
reviewer and the architect seat before this branch is handed to the lane for
the archive act. No-argument invocation — maximum coverage, no item cap.

## Requirement Completeness

- [ ] CHK001 Are requirements defined for every one of the 28 `tasks.md` boxes, or only for the groups FR-006/FR-007/FR-012 name (§0.1, §1, §2, §3.4, §4, §5.1)? [Completeness, Spec FR-006]
- [ ] CHK002 Is the disposition of every § 3 subtask (3.1, 3.2, 3.3, 3.5) stated in a requirement, or only in User Story 2's narrative and the Out of Scope list? [Completeness, Spec §Out of scope]
- [ ] CHK003 Are requirements defined for what happens if a § 4 gate FAILS (nonzero rc, an undispositioned finding), rather than only for the pass path FR-011 describes? [Gap, Spec FR-011]
- [ ] CHK004 Are requirements defined for the case where the doc-health finding-set diff (FR-011, SC-003) is NON-EMPTY? [Gap, Spec FR-011/SC-003]
- [ ] CHK005 Is the "STOP and report" behavior for a moved packet/canon (T002) promoted into spec.md as a requirement, or does it live only in tasks.md with no FR committing to that failure behavior? [Completeness, Tasks T002]
- [ ] CHK006 Are requirements defined for the case where the § 4.2 MODIFIED-block currency measurement (FR-012) finds the block is NOT current against promoted canon? [Gap, Spec FR-012]
- [ ] CHK007 Is a requirement stated for whether the § 4 gates must be re-run AGAIN if `main` moves and the branch merges forward after T029's single re-run, or does the spec leave a second forward-merge ungoverned? [Gap, Spec Edge Cases]
- [ ] CHK008 Are requirements defined for the CONTENT of the per-box dated notes (FR-006, FR-007) beyond "dated" and "naming the evidence/owner" — is a note format specified for the § 2 and § 5.1 boxes the way FR-006 specifies one for § 1? [Completeness, Spec FR-006/FR-007]
- [ ] CHK009 Is there a requirement for what happens if the twin (OpsxFactory PR #279) lands BEFORE this branch's evidence is finalized — does FR-007's "NOT-OWED-YET" language get revisited, or is that left to a future feature with no requirement bridging the gap? [Completeness, Spec Edge Cases]
- [ ] CHK010 Are requirements defined for VERIFYING that no archived file was touched (FR-009) — is a specific method (a diff, a path list) named as a requirement, or does it exist only as Tasks T003/T030 with no corresponding FR? [Completeness, Tasks T003/T030]
- [ ] CHK011 Is FR-010's "exactly three packet files" cross-checked against SC-007's five allowed path prefixes for consistency, or could a reader construct a case that satisfies one and violates the other? [Consistency, Spec FR-010/SC-007]
- [ ] CHK012 Are requirements defined for the evidence file's own internal structure (header contents) beyond FR-013's location and Tasks T011's "not a ruling, not a ratification, not a promotion"? [Gap, Tasks T011]

## Requirement Clarity

- [ ] CHK013 Is "minimal prose" (FR-005) quantified with a specific criterion (a line count, a sentence count, a character budget), or left to reviewer judgment? [Clarity, Spec FR-005]
- [ ] CHK014 Is "front-matter area" (FR-010) defined precisely enough to locate a single insertion point in `proposal.md`, or could two implementers place the note in different areas both defensibly called "front-matter"? [Clarity, Spec FR-010]
- [ ] CHK015 Is "purely additive" (FR-010, Plan Summary) defined with a testable boundary — e.g. zero characters removed, zero existing lines reflowed — or left as an unquantified adjective? [Clarity, Spec FR-010]
- [ ] CHK016 Is "verifiably DONE" (FR-006, Clarifications Q1) defined with an explicit test for EVERY box category it is applied to, or only illustrated by two precedent examples with no general rule extracted? [Clarity, Spec FR-006]
- [ ] CHK017 Is "in the shape the `govern-openspec-corpus-membership` bullet already uses" (FR-004) precise enough to check without opening that other bullet, or does it force a cross-reference to an external document to learn what "shape" means? [Clarity, Spec FR-004]
- [ ] CHK018 Is "the precedent form, WITHOUT a colon after the change name" (FR-003) demonstrated with the full exact string, or only described negatively (absence of a colon)? [Clarity, Spec FR-003]
- [ ] CHK019 Is "EXPLANATION... rather than as requirement text" (FR-005) given an objective test a reviewer could apply to a drafted sentence, or is the requirement/explanation boundary left to the author's judgment? [Ambiguity, Spec FR-005]
- [ ] CHK020 Is "the note is not the authorization for the edit" (FR-002) clarified as to what DOES authorize the edit, precisely enough that a reader cannot mistake the note itself for authorization? [Clarity, Spec FR-002]
- [ ] CHK021 Is "deliberately open" (FR-012) distinguished clearly from "incomplete" or "blocked", so a reader of the ticked/unticked record cannot mistake box 4.2's unticked state for an outstanding failure? [Clarity, Spec FR-012]
- [ ] CHK022 Is "governance text plus measured gate evidence... There is no code" (Plan Summary) precise enough to determine, for an arbitrary future edit to this feature, whether it counts as "code" requiring the `code_surface` declaration to change? [Clarity, Plan Summary]

## Requirement Consistency

- [ ] CHK023 Do FR-006 (tick § 1 `[OPERATOR]` boxes) and FR-017 (amend the three ratified "stays unticked" sentences) describe a single, non-contradictory sequence — is the internal order within "the SAME COMMIT" specified, or left open? [Consistency, Spec FR-006/FR-017]
- [ ] CHK024 Do FR-006 ("Boxes 3.1 and 4.2 are NOT ticked (FR-007, FR-012)") and FR-007 ("Task 3.1 stays unticked with a NOT-OWED-YET note") reconcile the "NOT OWED HERE" and "NOT-OWED-YET" labels as the same or a different note class, or is the difference left unexplained? [Conflict, Spec FR-006/FR-007]
- [ ] CHK025 Are FR-006, FR-007 and FR-012 consistent when read as a single table of the 28 boxes, or must a reader reconcile three separately worded requirements to reconstruct the full ticked/unticked disposition? [Consistency, Spec FR-006/FR-007/FR-012]
- [ ] CHK026 Does FR-010's "exactly three packet files" agree with FR-017's requirement to amend three ratified sentences WITHIN `tasks.md` — is it clear the amendments count as part of the one `tasks.md` file and not a fourth file? [Consistency, Spec FR-010/FR-017]
- [ ] CHK027 Is the citation form FR-003 prescribes ("Ratified by `govern-archived-record-edits` (2026-09-08)") distinguished from the citation form FR-006 prescribes (GitHub review id, timestamp, record path), so the difference reads as two note classes rather than an unexplained inconsistency? [Consistency, Spec FR-003/FR-006]
- [ ] CHK028 Does SC-006's "dated note" criterion for a § 4 box require citing the evidence file's path (matching FR-013), or could a bare date satisfy SC-006 while leaving FR-013 unreferenced? [Consistency, Spec SC-006/FR-013]
- [ ] CHK029 Do Clarifications Q6's answer and FR-012's text agree on WHY box 4.2 stays unticked, without requiring the reader to consult the "(reversed on review)" aside to know which of two readings prevailed? [Clarity, Spec Clarifications Q6/FR-012]

## Acceptance Criteria Quality

- [ ] CHK030 Can User Story 1 Acceptance Scenario 1 be verified by a single objective string match, or does "byte-for-byte as the ratified requirement states it" require opening the ratified requirement text with no citation of exactly which line to compare against? [Measurability, Spec US1 Scenario 1]
- [ ] CHK031 Is User Story 1 Acceptance Scenario 2's "names the recorded-ruling requirement" criterion measurable without ambiguity about WHICH requirement counts as "the recorded-ruling requirement"? [Ambiguity, Spec US1 Scenario 2]
- [ ] CHK032 Is User Story 2 Acceptance Scenario 3 ("no box is ticked whose act happened outside this branch and outside the record the packet already cites") checkable without a reviewer's independent, un-enumerated knowledge of which acts happened outside this branch? [Measurability, Spec US2 Scenario 3]
- [ ] CHK033 Is User Story 3 Acceptance Scenario 1's "zero undispositioned findings" checkable without also consulting an external disposition ledger not named in this spec? [Completeness, Spec US3 Scenario 1]
- [ ] CHK034 Does SC-001's floor ("the string appears... at least once") admit a technically-passing but wrongly placed occurrence that would satisfy SC-001 while failing FR-002's placement rule — is that gap closed anywhere? [Gap, Spec SC-001/FR-002]
- [ ] CHK035 Is SC-003's "diff-identical" defined precisely enough (ordering, whitespace, count-only vs full content) to be a repeatable pass/fail test rather than a judgment call? [Measurability, Spec SC-003]
- [ ] CHK036 Does SC-008's "recorded with a number" (singular) agree with Plan Phase 0's two named numbers (canon bytes carried, canon lines removed), or could an implementer record only one and still claim SC-008 satisfied? [Consistency, Spec SC-008/Plan Phase 0]
- [ ] CHK037 Is the spec explicit that User Story 2's acceptance criteria are NOT independently measurable before User Story 3 lands (FR-018's same-commit-or-neither rule), or is that ordering left implicit? [Dependency, Spec FR-018]

## Scenario Coverage

### Primary

- [ ] CHK038 Is the primary flow — doc bullet lands, evidence captured, `tasks.md` ticked truthfully, `proposal.md` note added, gates green, branch stops — expressed as one ordered acceptance path anywhere in spec.md, or must it be reconstructed from three separate user stories? [Coverage, Spec User Scenarios]

### Alternate

- [ ] CHK039 Is the alternate path where User Story 2 is delivered before User Story 3 explicitly named as FORBIDDEN, or only inferable from FR-018's general same-commit rule? [Alternate, Spec FR-018]
- [ ] CHK040 Is the alternate scenario where a box's cited evidence is later disputed (e.g., the § 1 review record found incomplete after the tick lands) addressed by any requirement, or left entirely unaddressed? [Gap, Spec FR-018]

### Exception/Error

- [ ] CHK041 Is the exception "T002's re-take of M1 finds the packet or canon HAS moved" resolved by a requirement in spec.md itself, or only by tasks.md's "STOP and report" with no FR committing to that outcome? [Exception, Tasks T002]
- [ ] CHK042 Is the exception "a § 4 gate exits non-zero" given a defined disposition (block landing, record failure, retry), or does FR-011 leave a failing run's consequence unstated? [Exception, Spec FR-011]
- [ ] CHK043 Is the exception "the § 3.4 bullet states more than the ratified requirement" (the Edge Cases "Explicit Delta Rule defect") given a concrete detection method as a requirement, or only named as a risk in Plan's risk table? [Exception, Spec Edge Cases/Plan Risks]
- [ ] CHK044 Is the exception "a commit is missing the `Lane:` trailer" (FR-014) given a defined remediation requirement, or only a verification task (T031) with no stated recovery step on failure? [Exception, Tasks T031]

### Recovery

- [ ] CHK045 If T003's freeze-verification fails at T028's re-check, is the recovery action (revert the offending edit, halt the feature) specified anywhere, or left unspecified? [Recovery, Tasks T003/T028]
- [ ] CHK046 If the doc-health finding-set diff is non-empty at the final gate re-run, is "the edit is reworked" (Edge Cases) specific enough to know WHAT reworking restores an empty diff, or is "reworked" left undefined? [Recovery, Spec Edge Cases]
- [ ] CHK047 Is a repair-after-the-fact procedure specified for a tick that already landed ahead of its evidence (a violation of FR-018 caught later), or does the spec state only the same-commit prevention rule with no correction path? [Recovery, Spec FR-018]

### Non-Functional

- [ ] CHK048 Is User Story 3's Independent Test ("re-run each named command at the named head and reproduce each stated result") specific enough that "named command" cannot be satisfied by a paraphrased command missing flags? [Non-Functional, Spec US3 Independent Test]
- [ ] CHK049 Is a non-functional requirement stated for auditing WHO performed which act (agent vs Brett Heap) without reading commit authorship metadata, or does that audit depend entirely on out-of-spec git history? [Non-Functional, Spec FR-006]

## Edge Case Coverage

- [ ] CHK050 Is "canon moves under the MODIFIED block while this feature is open" matched by a requirement with a SPECIFIC re-run trigger condition, or is "before archive" the only timing given anywhere? [Edge Case, Spec Edge Cases]
- [ ] CHK051 Is "another lane lands a substrate change first" fully resolved by a requirement, or does the spec only assert the merge-forward outcome as an Assumption with no acceptance scenario proving the path was exercised? [Edge Case, Spec Assumptions]
- [ ] CHK052 Is "a box's act is performed after this branch is cut" given a minimum content standard for the resulting dated note, beyond "leaves the dated note naming where the act lives"? [Edge Case, Spec Edge Cases]
- [ ] CHK053 Is "doc-health's finding set moves for a reason unrelated to this diff" given an objective test to distinguish an unrelated move from a caused one, or is that distinction left entirely to reviewer judgment? [Edge Case, Spec Edge Cases]
- [ ] CHK054 Is it stated which `main` commit is authoritative for SC-003's "diff-identical to main's" if `main` moves between T004's baseline capture and T029's final gate run? [Edge Case, Tasks T004/T029]

## Dependencies & Assumptions

- [ ] CHK055 Is "the packet is ratified AS WRITTEN and the three veto points were not exercised" independently verifiable by a reader of spec.md alone, or does it require trusting an external ratification record with no in-spec citation of how to verify non-exercise? [Assumption, Spec Assumptions]
- [ ] CHK056 Is the dependency on OpsxFactory PR #279 (FR-007) qualified with what happens to this feature's notes if PR #279 closes without merging or is superseded by a different PR number? [Dependency, Spec FR-007]
- [ ] CHK057 Does "the branch merges forward... and never rebases pushed commits" (Assumptions) reconcile with FR-014's explicit-path staging discipline for a merge commit specifically, or is that case left unaddressed? [Assumption, Spec Assumptions/FR-014]
- [ ] CHK058 Is the dependency on the pinned OpenSpec CLI 1.12.0 (Assumptions, Plan Technical Context) reflected as an FR anywhere, or does it live only outside the Functional Requirements section with nothing enforcing it there? [Gap, Plan Technical Context]
- [ ] CHK059 Does "the lane — not this feature — claims, opens the PR... and performs the archive act" (Assumptions) get cross-checked against FR-015's prohibition list so a reader cannot construe FR-015 as also forbidding the LANE from those later acts? [Consistency, Spec Assumptions/FR-015]
- [ ] CHK060 Are all five Out-of-scope items individually traceable to a requirement or scenario that respects the boundary, or could a reader of the Functional Requirements alone miss that Task 3.3 is out of scope? [Traceability, Spec Out of scope]

## Ambiguities & Conflicts

- [ ] CHK061 Does FR-009 ("no ratified requirement text may be reworded") conflict with FR-017 (amending three ratified `tasks.md` sentences) — is "requirement text" in FR-009 scoped precisely enough to exclude FR-017's target sentences? [Conflict, Spec FR-009/FR-017]
- [ ] CHK062 Is it stated whether "the packet's evidence file" and "this feature directory['s evidence]" (FR-008, FR-013) are two independent copies needing a consistency check, or one references the other? [Ambiguity, Spec FR-013]
- [ ] CHK063 Does the feature title ("performs its own acts under the archived-record-edit rule") state, in its own vicinity, whether "its own acts" excludes the archive act — or is that boundary recoverable only from FR-015 and Out of scope? [Ambiguity, Spec FR-015]
- [ ] CHK064 Could FR-016 ("write no checker... repair no broken pin") be read as forbidding the § 3.4 bullet itself, since it prescribes a note FORM future edits must follow — is that reading foreclosed anywhere? [Ambiguity, Spec FR-016]
- [ ] CHK065 Is every one of the ten architect-ruling questions (Q1–Q10) traced to at least one FR that encodes its answer, or does any Q-answer lack a landing requirement? [Traceability, Spec Clarifications]

## Traceability

- [ ] CHK066 Does every one of FR-001 through FR-019 carry an explicit cross-reference (a Q-number, a precedent commit, or a task ID) a reviewer can follow to its origin, or is any FR asserted with no stated basis? [Traceability, Spec Functional Requirements]
- [ ] CHK067 Does every one of SC-001 through SC-008 map to at least one FR it measures, so a reviewer can confirm no success criterion is free-floating? [Traceability, Spec Success Criteria]
- [ ] CHK068 Are the three "Architect rulings open to veto" each traced forward to the specific FR(s) they produced, so a veto's blast radius is knowable without re-deriving it from the full spec? [Traceability, Spec Architect rulings]
- [ ] CHK069 Is the Key Entities section's packet description (28 boxes, 1 MODIFIED + 2 ADDED, 18 scenarios) consistent with the same counts in research.md and plan.md, or could a reader find a discrepancy across the three documents? [Consistency, Spec Key Entities/Research]
