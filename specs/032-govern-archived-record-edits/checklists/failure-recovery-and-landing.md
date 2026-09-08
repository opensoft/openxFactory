# Checklist: Failure Recovery and Landing

**State**: written 2026-09-08, NOT YET RUN — this file is the gate instrument for the architect's refutation panel. The findings its authoring raised were resolved in the analyze loop and are recorded in [`../analysis.md`](../analysis.md).

**Purpose**: Interrogate the QUALITY of the written requirements for every
mid-flight failure this feature names, the rollback story each failure implies,
the sequencing of landing and archive acts, and the stop condition — never the
implementation of any recovery.
**Created**: 2026-09-08
**Feature**: [spec.md](../spec.md)
**Lane**: opsXfactory-1

## Canon Drift Under the MODIFIED Block

- [x] CHK001 Are requirements defined for what this feature must do if
      `git log 3504287a..HEAD` over the packet, promoted canon and the § 3.4
      target is NOT empty when T002 re-measures it at the branch head?
      [Exception Coverage, Tasks T002]
- [ ] CHK002 Is the STOP instruction at T002 ("STOP and report") specified with
      enough detail that a reader knows what the report must CONTAIN, or does
      it name only the action without its content? [Ambiguity, Tasks T002] **— OPEN:** T002's "STOP and report" names the action but not what the report must CONTAIN. **FIX:** add to T002 what the stop report must contain — the `git log` output showing what moved, and a note that the plan's premises need re-reading before any task proceeds.
- [ ] CHK003 Are requirements defined for whether this feature resumes after a
      T002 stop once canon settles again, or whether the whole plan must be
      re-authored against the moved canon? [Gap] **— OPEN:** no statement says whether the feature resumes once canon re-settles or must be re-authored from scratch. **FIX:** add a sentence to T002 or a new edge case naming whether the feature resumes measurement in place once canon is re-verified unmoved, or must re-run Phase 0 research in full.
- [x] CHK004 Is the MODIFIED-block currency re-check (task 4.2, FR-012)
      specified to run MORE than once if canon moves a second time between
      S6's re-run and the eventual archive act? [Completeness, FR-012]
- [ ] CHK005 Are requirements defined for what the evidence file must record
      if the currency measurement finds the block is NO LONGER current — a
      byte-level divergence rather than the "canon bytes carried, canon lines
      removed" measurement SC-008 expects on success? [Exception Coverage, SC-008] **— OPEN:** only the success-path currency measurement (canon bytes carried, lines removed) is described; no record format is given for a divergence finding. **FIX:** extend FR-012/T013 to state that a divergence finding is recorded as a byte-level measurement (not the success numbers), with FR-020's blocker rule then applying.

## Doc-Health Finding-Set Regression

- [x] CHK006 Are requirements defined for what this feature does if gate 4.4's
      diff against `main`'s finding set is NON-EMPTY after the § 3.4 bullet
      lands? [Exception Coverage, Tasks T016]
- [x] CHK007 Is "explained or the edit is reworked" (Spec Edge Cases) specified
      precisely enough to say WHO decides between explaining a residual
      difference and reworking the edit, and by what criterion the choice is
      made? [Ambiguity, Spec Edge Cases]
- [x] CHK008 Are requirements defined for how many rework attempts this
      feature may make before a non-empty finding-set diff is treated as a
      blocking failure rather than a retryable one? [Gap]
- [x] CHK009 Is the baseline captured at T004 (from `main`, before any edit)
      protected against silent invalidation if `main` moves during this
      feature's own execution, given `main` is stated to move "hourly"?
      [Consistency, Tasks T004, Spec Edge Cases]
- [x] CHK010 Are requirements defined for whether a doc-health finding-set
      change caused by `main` moving (not by this feature's own diff) is
      distinguished in the record from one caused by the § 3.4 edit itself?
      [Clarity, Spec Edge Cases]

## Gate Failure at the Final Head

- [x] CHK011 Are requirements defined for the specific remedy when ANY ONE of
      the remaining § 4 gates (4.1, 4.3, 4.5) fails at the final head, distinct
      from the MODIFIED-block and doc-health failures already named?
      [Gap, Exception Coverage]
- [x] CHK012 Is it specified whether a failing gate at T029's final re-run
      requires reverting T027/T028's commits, amending them, or authoring a
      fix commit — three materially different recovery paths the tasks do not
      distinguish between? [Ambiguity, Tasks T029]
- [x] CHK013 Are requirements defined for what the STOP-(B) gate report
      (plan.md Implementation sequence) contains when the report is of a
      FAILURE rather than a clean pass, or does the plan describe only the
      success-path report? [Completeness, Plan Implementation sequence]
- [ ] CHK014 Can a reader distinguish, from the tasks and spec alone, between a
      gate failure that blocks THIS feature's completion and a gate failure
      that is pre-existing on `main` and therefore not this feature's to fix?
      [Clarity, Gap] **— OPEN:** FR-020 treats every failing gate uniformly as this feature's blocker without distinguishing a NEWLY introduced failure from one already present on `main`. **FIX:** add a general baseline-comparison clause (paralleling SC-002's dispositioned-count comparison) so a pre-existing `main` failure is named and carried forward rather than treated as this feature's own blocker.

## Main Moving Under the Branch

- [ ] CHK015 Is "merge forward, never rebase pushed commits" (Spec Edge Cases,
      Plan Risks) accompanied by a requirement for WHEN the merge-forward must
      happen relative to the gate re-run, so a merge-forward does not silently
      invalidate T029's already-recorded results? [Completeness, Spec Edge Cases] **— OPEN:** no stated timing requires a merge-forward to happen before, rather than after, T029's final gate re-run. **FIX:** add a sentence to plan.md's Risks table or T029 requiring any merge-forward to complete before T029's final gate re-run runs.
- [ ] CHK016 Are requirements defined for what happens if `main` moves in a way
      that touches one of the FROZEN paths this feature must not edit
      (`design.md`, `.openspec.yaml`, the spec delta, `archive/`), forcing a
      merge conflict this feature is forbidden to resolve by editing those
      files? [Gap, Exception Coverage] **— OPEN:** no scenario covers `main` moving in a way that touches a FROZEN path, forcing a conflict this feature is forbidden to resolve by editing that file. **FIX:** add an edge case naming this scenario and its resolution — STOP under FR-020's blocker discipline, since resolving the conflict would itself violate the freeze.
- [ ] CHK017 Is the interaction between "`main` moves hourly" (task 5.1) and
      SC-007's exact path-list assertion specified for the case where a
      merge-forward commit itself appears in `git diff main...HEAD --stat` and
      could be misread as an out-of-scope edit? [Ambiguity, SC-007] **— OPEN:** no sentence reassures that the triple-dot diff in SC-007 is taken against the merge-base, so a merge-forward cannot introduce `main`'s own commits into the checked path set. **FIX:** add a sentence to SC-007 or the Edge Cases explaining the triple-dot diff is taken against the merge-base, so merging `main` forward does not introduce `main`'s own commits into the checked diff.

## Another Lane Landing a Substrate Change First

- [ ] CHK018 Is "re-derive at the union if another lane's substrate claim
      lands first" (task 5.1, Rule 7) specified with enough detail — what "the
      union" means for a README Records block carrying two independently
      authored rows — that two lanes converge on the same resulting file
      rather than each overwriting the other? [Ambiguity, OpenSpec Tasks §5.1] **— OPEN:** spec.md's Out of Scope names "the lane's act at landing" for the README union but never defines what "the union" means for two independently-authored rows. **FIX:** cite the lane-collision-protocol's Rule 7 union procedure explicitly in the Out of Scope bullet, or state the union rule inline.
- [ ] CHK019 Are requirements defined for WHO re-derives the union when a
      collision is detected — the lane whose branch is older, the lane whose PR
      opens first, or whichever lane notices first? [Gap] **— OPEN:** no statement names WHICH lane performs the union re-derivation when a collision is detected. **FIX:** cross-reference the lane-collision protocol's actual assignment rule, or state explicitly that the union is the landing lane's own judgment call.
- [ ] CHK020 Since this feature explicitly does NOT perform § 5.1's landing
      acts (Spec §Out of scope), is it specified whether this feature's OWN
      evidence or notes are invalidated if a later union re-derivation changes
      a file this feature has already measured (for example the sweep-ledger
      row)? [Consistency, Spec §Out of scope] **— OPEN:** no statement says whether this feature's own measured evidence (e.g. the sweep-ledger row) is treated as invalidated or as superseded by a later union re-derivation. **FIX:** add a note applying FR-021's forward-only discipline explicitly here: the recorded measurement stands as a dated read at its own head, and a later union change is the lane's own separately dated measurement.

## Partial Commit / Tick-Ahead-of-Evidence Failure

- [x] CHK021 Is FR-018's rule ("a box MUST be ticked in the same commit that
      records its evidence, or neither happens") paired with a stated RECOVERY
      for the case where such a violation is discovered AFTER the fact — for
      example after a merge-forward exposes a split commit? [Gap, FR-018]
- [ ] CHK022 Are requirements defined for what the record must say if T027
      (the single combined tick-and-note commit) is found to be malformed —
      partially staged, or missing one box's note — before it is pushed?
      [Exception Coverage, Tasks T027] **— OPEN:** no pre-push verification step confirms T027's combined commit is fully staged (no box ticked without its note) before it is pushed. **FIX:** add a pre-push verification sub-step to T027 (e.g. `git diff --cached`) confirming every ticked box's note is staged in the same commit before it is pushed.
- [x] CHK023 Is it specified whether an already-PUSHED commit that violates
      FR-018 must be corrected by a follow-up commit naming the defect, or by
      history rewrite — given this feature is also bound to "never rebase
      pushed commits"? [Ambiguity, FR-018, Spec Edge Cases]
- [ ] CHK024 Are requirements defined for how a reader distinguishes, after the
      fact, a box that is ticked with its evidence properly co-committed from
      one that merely LOOKS co-committed because both landed in the same PR
      but in different commits? [Measurability, FR-018] **— OPEN:** no verification method (e.g. `git blame`/`git log -p` on the specific lines) is named to confirm a tick's evidence landed in the SAME COMMIT rather than merely the same PR. **FIX:** add a verification task using `git log -p`/`git blame` on the tick-and-note lines to confirm same-commit co-location objectively.

## Rollback and Post-Failure Record State

- [x] CHK025 Is a rollback procedure stated for the § 3.4 doc bullet
      specifically — what is reverted, in what order, and what the record then
      says — if T009's local verification or gate 4.4 finds the bullet
      defective after S1's commit lands? [Gap]
- [x] CHK026 Is a rollback procedure stated for the evidence file and captured
      gate outputs (S2/S3) if a LATER gate re-run at T029 invalidates an
      earlier-recorded result — is the earlier record struck, superseded in
      place, or left standing beside the new one? [Gap]
- [ ] CHK027 Is a rollback procedure stated for the `tasks.md` ticks (S4) if a
      tick is later found to violate FR-018 or FR-006's evidence requirement —
      does the box revert to unticked, or does a correcting note stand beside
      the original tick? [Gap] **— OPEN:** FR-021's "struck, never deleted" convention is stated for evidence entries; no parallel mechanic (revert to unticked vs. a correcting note beside the original) is named for a defective `tasks.md` tick. **FIX:** extend FR-021 (or add a sentence) stating the same "never deleted, dated correcting note" convention applies to `tasks.md` ticks.
- [ ] CHK028 For EVERY named failure mode in the Spec's Edge Cases section, is
      there a corresponding statement of what the `tasks.md` or evidence-file
      record says AFTER the failure is handled, or do the edge cases describe
      only the trigger and the immediate response? [Completeness, Spec Edge Cases] **— OPEN:** only one of the five named Edge Cases (the late-performed box) states what the record says AFTER the situation is handled; the other four describe trigger and response only. **FIX:** add, to each remaining Edge Case bullet, an explicit statement of what the `tasks.md`/evidence-file record says once the situation is resolved.
- [x] CHK029 Is there a single, stated convention for how a superseded or
      reverted claim is marked in this feature's artifacts (struck through, a
      dated amendment, a new note) consistent with the corpus precedent FR-017
      cites (commit `3b530009`'s "name the superseded sentence") — or does each
      rollback scenario risk inventing its own form? [Consistency, FR-017]

## Landing Act Sequencing

- [x] CHK030 Is the sequence of landing acts — claim, open PR, post LANDING,
      merge, post LANDED, discharge issue claims, archive — stated in ONE place
      a reader of this feature's artifacts can find, or must it be assembled
      from `spec.md`'s Assumptions, `plan.md`, and the root lane-collision
      protocol separately? [Completeness, Spec §Assumptions]
- [x] CHK031 Are requirements consistent between `spec.md`'s Assumptions ("the
      lane... claims, opens the PR, posts LANDING/LANDED, discharges the
      claims... and performs the archive act") and OpenSpec Tasks §5.2/§5.3/§6.3
      on who performs each landing act? [Consistency, Spec §Assumptions, OpenSpec Tasks §5.2-6.3]
- [x] CHK032 Is it specified what this feature's own STOP-(B) report must
      contain for the lane to perform the landing sequence WITHOUT re-deriving
      any of this feature's measurements itself? [Completeness, Tasks T032]
- [ ] CHK033 Are requirements defined for the case where the lane that claims
      issue #630 and opens the PR is a DIFFERENT session from the one that ran
      this feature to STOP (B) — is a handoff artifact named, or is the report
      alone assumed sufficient? [Gap] **— OPEN:** no statement names the evidence file plus the STOP (B) report as the designated handoff artifact for a DIFFERENT session to perform landing. **FIX:** add a sentence to FR-013 or the Assumptions section naming the evidence file and STOP (B) report as the complete handoff, or name a further handoff document if one is required.
- [ ] CHK034 Is the ordering constraint between "merge" and "archive" (archive
      happens only after the artifacts land, per §6.1's "archive WHEN ITS
      ARTIFACTS LAND") stated consistently with the constraint that box 4.2
      must be re-verified "continuously until archive" — that is, does the
      sequencing specify WHERE the final 4.2 re-check falls relative to the
      merge? [Consistency, OpenSpec Tasks §4.2, §6.1] **— OPEN:** neither FR-012 nor the packet's own §4.2/§6.1 text pins WHERE the final currency re-check falls relative to the merge — pre-merge only, or repeated post-merge before archive. **FIX:** add a sentence stating the final 4.2 re-check occurs after the branch merges into `main` and immediately before the archive act, not merely as this feature's last pre-merge measurement.

## Archive Preconditions and the Deliberately-Open Box

- [x] CHK035 Is the precondition set for §6.1 (archive) stated completely —
      that only box 3.4 gates the archive among §3's boxes, with
      3.1/3.2/3.3/3.5 named but NON-gating — in a form that could not be
      misread as ALL of §3 gating the archive? [Clarity, OpenSpec Tasks §6.1]
- [x] CHK036 Is it explicit that box 4.2 is DELIBERATELY left unticked for the
      archive act (FR-012) rather than merely incomplete, so that a future
      reader auditing "every box ticked or dated" (SC-006) does not mistake 4.2
      for an oversight? [Clarity, FR-012, SC-006]
- [x] CHK037 Are requirements defined for what the archive act itself must do
      with box 4.2 — re-run the currency check one final time, or accept this
      feature's last-recorded measurement — given FR-012 says the box stays
      open "for the archive act" but does not say what act discharges it?
      [Gap, FR-012]
- [x] CHK038 Is there a stated requirement that box 3.1's cross-citation
      re-check (task 3.1) resolves BEFORE §6.1's archive, or could the packet
      archive while 3.1 is still unresolved, given nothing in §6.1 names 3.1 as
      gating? [Ambiguity, OpenSpec Tasks §3.1, §6.1]
- [x] CHK039 Are the archive preconditions this feature measures (box 3.4
      ticked, gates green, 4.2 measured) distinguished from the preconditions
      §6.1 itself lists (only 3.4 gates), so a reader cannot conflate "this
      feature's own completion criteria" with "the archive act's own
      criteria"? [Consistency, SC-006, OpenSpec Tasks §6.1]

## Post-Branch Veto Handling

- [ ] CHK040 Are requirements defined for what happens to the § 3.4 doc bullet
      if Brett Heap exercises the second flagged veto (declining the § 1
      `[OPERATOR]` ticks) AFTER this branch is built, given the doc bullet is
      independent of the tick policy but was authored under the same architect
      ruling round? [Exception Coverage, Spec §Architect rulings open to veto] **— OPEN:** no statement says the three veto reversal acts are mutually independent, so a reader must infer that declining ruling #2 (the `[OPERATOR]` ticks) leaves the § 3.4 doc bullet untouched. **FIX:** add an explicit independence sentence to the "Architect rulings open to veto" section stating the three reversal acts touch disjoint files and do not affect one another.
- [x] CHK041 Are requirements defined for what happens to the S4 commit
      (T019–T027) if that veto is exercised — must the five `[OPERATOR]` ticks
      and the three sentence amendments be reverted together, mirroring
      FR-017's and FR-018's same-commit discipline, or is a partial reversion
      permitted? [Gap, FR-017, FR-018]
- [x] CHK042 Are requirements defined for what happens to the `proposal.md`
      additive note (T028) if the first flagged veto (declining the
      enumeration note) is exercised — is the note removed, and is that
      removal itself an archived-record-edit question given `proposal.md` is a
      governance document under the very capability this packet realizes?
      [Gap, Spec §Architect rulings open to veto]
- [ ] CHK043 Are requirements defined for what happens to the two explanatory
      sentences (T007) if the third flagged veto is exercised — does the doc
      bullet revert to the note-form-only shape (Q2b option i), and is that
      reversion itself subject to the doc-health finding-set re-diff (gate 4.4)
      the same way the original edit was? [Gap, FR-005] **— OPEN:** the third reversal act (delete the two explanatory sentences) does not say whether that reversion must also pass through gate 4.4's re-diff the way the original edit did. **FIX:** add a sentence requiring any veto reversal touching a gated file to be followed by a full § 4 gate re-run before the branch is considered settled, mirroring T029's discipline.
- [ ] CHK044 Is it specified WHO notices that a veto has been exercised and
      WHEN — before the branch reaches STOP (B), after the PR opens, or after
      Brett Heap reviews the PR — given the three rulings are stated as "open
      to veto" with no named trigger for when veto exposure closes? [Ambiguity,
      Spec §Architect rulings open to veto] **— OPEN:** no statement names WHO notices a veto or WHEN in the pipeline the "open to veto" window closes. **FIX:** add a sentence naming the trigger point (e.g. any time before the archive act) and naming who is responsible for acting on a veto once exercised.
- [ ] CHK045 If more than one of the three flagged vetoes is exercised
      together, are the three recovery paths (doc bullet, S4 commit,
      `proposal.md` note) specified as independent of each other, or could
      reverting one require reverting another that depends on it? [Gap, Consistency] **— OPEN:** the same independence question as CHK040 recurs for the case of more than one veto exercised together, and is left to inference rather than stated. **FIX:** apply the same independence statement proposed for CHK040 to cover the multiple-veto case explicitly.

## The Stop Condition

- [ ] CHK046 Is the stop condition — STOP at the gate report, no PR, no
      comment, no merge, no archive — stated in exactly ONE place across
      `spec.md`, `plan.md` and `tasks.md`, or does it recur in multiple
      wordings that could drift out of sync with each other? [Consistency,
      FR-015, Plan Implementation sequence, Tasks T032] **— OPEN:** the stop condition is restated in FR-015, plan.md, and tasks.md T034 in three separate wordings rather than stated once and cited elsewhere. **FIX:** designate FR-015 as the authoritative statement of the stop condition, and have plan.md and T034 cite it by name instead of restating the prohibition list.
- [x] CHK047 Is "no comment" in the stop condition (FR-015) specific enough to
      cover BOTH a GitHub pull-request comment and a comment on issue #630, or
      could a narrow reading permit one while the rule intends to forbid both?
      [Ambiguity, FR-015]
- [x] CHK048 Is the stop condition's scope over "no PR" consistent with the
      Assumptions section's statement that the LANE opens the PR — that is, is
      it unambiguous that this feature stopping short of a PR is a boundary
      rule and not merely a scheduling fact that a later session could read as
      already satisfied by someone else's PR? [Consistency, FR-015, Spec §Assumptions]
- [ ] CHK049 Can the stop condition be objectively verified from repository
      state alone (absence of a PR, absence of a merge, absence of an archive
      commit), or does verifying it require trusting an unaudited claim made in
      the report itself? [Measurability, FR-015] **— OPEN:** no task verifies the negative claim (no PR/merge/archive occurred) as a checkable repository-state fact at STOP (B); it is asserted by the report rather than checked. **FIX:** add a verification sub-step to T034 confirming the absence of a PR/merge/archive marker, or state explicitly that the proof rests on the session's own command log rather than repo state.

## Evaluation — 2026-09-08

**Tally**: 27 passed / 22 open / 0 deferred (total 49).

### Open items
- CHK002 — T002's "STOP and report" names the action but not the report's required content → state what the T002 stop report must contain.
- CHK003 — no statement on resuming in place vs. re-authoring after a T002 stop → add a resume-or-re-author rule.
- CHK005 — no record format for a currency-check divergence (only the success-path measurement is described) → extend FR-012/T013 for the failure case.
- CHK014 — no distinction between a newly-introduced gate failure and one pre-existing on `main` → add a baseline-comparison clause paralleling SC-002.
- CHK015 — no timing rule for merge-forward relative to T029's final gate re-run → require merge-forward before T029.
- CHK016 — no scenario for `main` moving to touch a FROZEN path and forcing a forbidden conflict resolution → add that edge case and its STOP resolution.
- CHK017 — no reassurance that a merge-forward commit can't spoil SC-007's diff check → explain the triple-dot/merge-base mechanics in SC-007 or Edge Cases.
- CHK018 — "the union" (README row merge) is never defined → cite the lane-collision protocol's Rule 7 or define it inline.
- CHK019 — no statement of which lane performs a union re-derivation → cross-reference the protocol's assignment rule or state it's the landing lane's call.
- CHK020 — no statement on whether this feature's own evidence is invalidated by a later union re-derivation → apply FR-021's forward-only discipline explicitly.
- CHK022 — no pre-push verification that T027's combined commit is fully co-staged → add a pre-push check to T027.
- CHK024 — no method to verify a tick's evidence landed in the SAME commit vs. same PR → add a `git blame`/`git log -p` verification task.
- CHK027 — FR-021's "struck, never deleted" convention isn't extended to defective `tasks.md` ticks → state the same convention applies to ticks.
- CHK028 — only 1 of 5 Edge Cases states the post-handling record content → add that statement to the remaining four.
- CHK033 — no statement naming the evidence file + STOP (B) report as the cross-session handoff artifact → add that naming to FR-013 or Assumptions.
- CHK034 — no pinned sequencing of the final 4.2 re-check relative to the merge → state it occurs after merge, before archive.
- CHK040 — no stated independence of the § 3.4 bullet from veto #2's reversal → add an explicit independence sentence.
- CHK043 — the third veto's reversal doesn't require a gate 4.4 re-run → add that requirement.
- CHK044 — no stated trigger/owner for noticing an exercised veto → name the trigger point and the responsible party.
- CHK045 — the multi-veto independence question is left to inference → state the three reversal acts are independent.
- CHK046 — the stop condition recurs in three separately-worded places (FR-015, plan.md, T034) → designate FR-015 authoritative and have the others cite it.
- CHK049 — no task checks the negative claim (no PR/merge/archive) as repository state → add a verification sub-step to T034.

### Deferred items
- None.
