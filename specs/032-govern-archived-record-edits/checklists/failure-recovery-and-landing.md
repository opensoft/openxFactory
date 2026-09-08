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

- [ ] CHK001 Are requirements defined for what this feature must do if
      `git log 3504287a..HEAD` over the packet, promoted canon and the § 3.4
      target is NOT empty when T002 re-measures it at the branch head?
      [Exception Coverage, Tasks T002]
- [ ] CHK002 Is the STOP instruction at T002 ("STOP and report") specified with
      enough detail that a reader knows what the report must CONTAIN, or does
      it name only the action without its content? [Ambiguity, Tasks T002]
- [ ] CHK003 Are requirements defined for whether this feature resumes after a
      T002 stop once canon settles again, or whether the whole plan must be
      re-authored against the moved canon? [Gap]
- [ ] CHK004 Is the MODIFIED-block currency re-check (task 4.2, FR-012)
      specified to run MORE than once if canon moves a second time between
      S6's re-run and the eventual archive act? [Completeness, FR-012]
- [ ] CHK005 Are requirements defined for what the evidence file must record
      if the currency measurement finds the block is NO LONGER current — a
      byte-level divergence rather than the "canon bytes carried, canon lines
      removed" measurement SC-008 expects on success? [Exception Coverage, SC-008]

## Doc-Health Finding-Set Regression

- [ ] CHK006 Are requirements defined for what this feature does if gate 4.4's
      diff against `main`'s finding set is NON-EMPTY after the § 3.4 bullet
      lands? [Exception Coverage, Tasks T016]
- [ ] CHK007 Is "explained or the edit is reworked" (Spec Edge Cases) specified
      precisely enough to say WHO decides between explaining a residual
      difference and reworking the edit, and by what criterion the choice is
      made? [Ambiguity, Spec Edge Cases]
- [ ] CHK008 Are requirements defined for how many rework attempts this
      feature may make before a non-empty finding-set diff is treated as a
      blocking failure rather than a retryable one? [Gap]
- [ ] CHK009 Is the baseline captured at T004 (from `main`, before any edit)
      protected against silent invalidation if `main` moves during this
      feature's own execution, given `main` is stated to move "hourly"?
      [Consistency, Tasks T004, Spec Edge Cases]
- [ ] CHK010 Are requirements defined for whether a doc-health finding-set
      change caused by `main` moving (not by this feature's own diff) is
      distinguished in the record from one caused by the § 3.4 edit itself?
      [Clarity, Spec Edge Cases]

## Gate Failure at the Final Head

- [ ] CHK011 Are requirements defined for the specific remedy when ANY ONE of
      the remaining § 4 gates (4.1, 4.3, 4.5) fails at the final head, distinct
      from the MODIFIED-block and doc-health failures already named?
      [Gap, Exception Coverage]
- [ ] CHK012 Is it specified whether a failing gate at T029's final re-run
      requires reverting T027/T028's commits, amending them, or authoring a
      fix commit — three materially different recovery paths the tasks do not
      distinguish between? [Ambiguity, Tasks T029]
- [ ] CHK013 Are requirements defined for what the STOP-(B) gate report
      (plan.md Implementation sequence) contains when the report is of a
      FAILURE rather than a clean pass, or does the plan describe only the
      success-path report? [Completeness, Plan Implementation sequence]
- [ ] CHK014 Can a reader distinguish, from the tasks and spec alone, between a
      gate failure that blocks THIS feature's completion and a gate failure
      that is pre-existing on `main` and therefore not this feature's to fix?
      [Clarity, Gap]

## Main Moving Under the Branch

- [ ] CHK015 Is "merge forward, never rebase pushed commits" (Spec Edge Cases,
      Plan Risks) accompanied by a requirement for WHEN the merge-forward must
      happen relative to the gate re-run, so a merge-forward does not silently
      invalidate T029's already-recorded results? [Completeness, Spec Edge Cases]
- [ ] CHK016 Are requirements defined for what happens if `main` moves in a way
      that touches one of the FROZEN paths this feature must not edit
      (`design.md`, `.openspec.yaml`, the spec delta, `archive/`), forcing a
      merge conflict this feature is forbidden to resolve by editing those
      files? [Gap, Exception Coverage]
- [ ] CHK017 Is the interaction between "`main` moves hourly" (task 5.1) and
      SC-007's exact path-list assertion specified for the case where a
      merge-forward commit itself appears in `git diff main...HEAD --stat` and
      could be misread as an out-of-scope edit? [Ambiguity, SC-007]

## Another Lane Landing a Substrate Change First

- [ ] CHK018 Is "re-derive at the union if another lane's substrate claim
      lands first" (task 5.1, Rule 7) specified with enough detail — what "the
      union" means for a README Records block carrying two independently
      authored rows — that two lanes converge on the same resulting file
      rather than each overwriting the other? [Ambiguity, OpenSpec Tasks §5.1]
- [ ] CHK019 Are requirements defined for WHO re-derives the union when a
      collision is detected — the lane whose branch is older, the lane whose PR
      opens first, or whichever lane notices first? [Gap]
- [ ] CHK020 Since this feature explicitly does NOT perform § 5.1's landing
      acts (Spec §Out of scope), is it specified whether this feature's OWN
      evidence or notes are invalidated if a later union re-derivation changes
      a file this feature has already measured (for example the sweep-ledger
      row)? [Consistency, Spec §Out of scope]

## Partial Commit / Tick-Ahead-of-Evidence Failure

- [ ] CHK021 Is FR-018's rule ("a box MUST be ticked in the same commit that
      records its evidence, or neither happens") paired with a stated RECOVERY
      for the case where such a violation is discovered AFTER the fact — for
      example after a merge-forward exposes a split commit? [Gap, FR-018]
- [ ] CHK022 Are requirements defined for what the record must say if T027
      (the single combined tick-and-note commit) is found to be malformed —
      partially staged, or missing one box's note — before it is pushed?
      [Exception Coverage, Tasks T027]
- [ ] CHK023 Is it specified whether an already-PUSHED commit that violates
      FR-018 must be corrected by a follow-up commit naming the defect, or by
      history rewrite — given this feature is also bound to "never rebase
      pushed commits"? [Ambiguity, FR-018, Spec Edge Cases]
- [ ] CHK024 Are requirements defined for how a reader distinguishes, after the
      fact, a box that is ticked with its evidence properly co-committed from
      one that merely LOOKS co-committed because both landed in the same PR
      but in different commits? [Measurability, FR-018]

## Rollback and Post-Failure Record State

- [ ] CHK025 Is a rollback procedure stated for the § 3.4 doc bullet
      specifically — what is reverted, in what order, and what the record then
      says — if T009's local verification or gate 4.4 finds the bullet
      defective after S1's commit lands? [Gap]
- [ ] CHK026 Is a rollback procedure stated for the evidence file and captured
      gate outputs (S2/S3) if a LATER gate re-run at T029 invalidates an
      earlier-recorded result — is the earlier record struck, superseded in
      place, or left standing beside the new one? [Gap]
- [ ] CHK027 Is a rollback procedure stated for the `tasks.md` ticks (S4) if a
      tick is later found to violate FR-018 or FR-006's evidence requirement —
      does the box revert to unticked, or does a correcting note stand beside
      the original tick? [Gap]
- [ ] CHK028 For EVERY named failure mode in the Spec's Edge Cases section, is
      there a corresponding statement of what the `tasks.md` or evidence-file
      record says AFTER the failure is handled, or do the edge cases describe
      only the trigger and the immediate response? [Completeness, Spec Edge Cases]
- [ ] CHK029 Is there a single, stated convention for how a superseded or
      reverted claim is marked in this feature's artifacts (struck through, a
      dated amendment, a new note) consistent with the corpus precedent FR-017
      cites (commit `3b530009`'s "name the superseded sentence") — or does each
      rollback scenario risk inventing its own form? [Consistency, FR-017]

## Landing Act Sequencing

- [ ] CHK030 Is the sequence of landing acts — claim, open PR, post LANDING,
      merge, post LANDED, discharge issue claims, archive — stated in ONE place
      a reader of this feature's artifacts can find, or must it be assembled
      from `spec.md`'s Assumptions, `plan.md`, and the root lane-collision
      protocol separately? [Completeness, Spec §Assumptions]
- [ ] CHK031 Are requirements consistent between `spec.md`'s Assumptions ("the
      lane... claims, opens the PR, posts LANDING/LANDED, discharges the
      claims... and performs the archive act") and OpenSpec Tasks §5.2/§5.3/§6.3
      on who performs each landing act? [Consistency, Spec §Assumptions, OpenSpec Tasks §5.2-6.3]
- [ ] CHK032 Is it specified what this feature's own STOP-(B) report must
      contain for the lane to perform the landing sequence WITHOUT re-deriving
      any of this feature's measurements itself? [Completeness, Tasks T032]
- [ ] CHK033 Are requirements defined for the case where the lane that claims
      issue #630 and opens the PR is a DIFFERENT session from the one that ran
      this feature to STOP (B) — is a handoff artifact named, or is the report
      alone assumed sufficient? [Gap]
- [ ] CHK034 Is the ordering constraint between "merge" and "archive" (archive
      happens only after the artifacts land, per §6.1's "archive WHEN ITS
      ARTIFACTS LAND") stated consistently with the constraint that box 4.2
      must be re-verified "continuously until archive" — that is, does the
      sequencing specify WHERE the final 4.2 re-check falls relative to the
      merge? [Consistency, OpenSpec Tasks §4.2, §6.1]

## Archive Preconditions and the Deliberately-Open Box

- [ ] CHK035 Is the precondition set for §6.1 (archive) stated completely —
      that only box 3.4 gates the archive among §3's boxes, with
      3.1/3.2/3.3/3.5 named but NON-gating — in a form that could not be
      misread as ALL of §3 gating the archive? [Clarity, OpenSpec Tasks §6.1]
- [ ] CHK036 Is it explicit that box 4.2 is DELIBERATELY left unticked for the
      archive act (FR-012) rather than merely incomplete, so that a future
      reader auditing "every box ticked or dated" (SC-006) does not mistake 4.2
      for an oversight? [Clarity, FR-012, SC-006]
- [ ] CHK037 Are requirements defined for what the archive act itself must do
      with box 4.2 — re-run the currency check one final time, or accept this
      feature's last-recorded measurement — given FR-012 says the box stays
      open "for the archive act" but does not say what act discharges it?
      [Gap, FR-012]
- [ ] CHK038 Is there a stated requirement that box 3.1's cross-citation
      re-check (task 3.1) resolves BEFORE §6.1's archive, or could the packet
      archive while 3.1 is still unresolved, given nothing in §6.1 names 3.1 as
      gating? [Ambiguity, OpenSpec Tasks §3.1, §6.1]
- [ ] CHK039 Are the archive preconditions this feature measures (box 3.4
      ticked, gates green, 4.2 measured) distinguished from the preconditions
      §6.1 itself lists (only 3.4 gates), so a reader cannot conflate "this
      feature's own completion criteria" with "the archive act's own
      criteria"? [Consistency, SC-006, OpenSpec Tasks §6.1]

## Post-Branch Veto Handling

- [ ] CHK040 Are requirements defined for what happens to the § 3.4 doc bullet
      if Brett Heap exercises the second flagged veto (declining the § 1
      `[OPERATOR]` ticks) AFTER this branch is built, given the doc bullet is
      independent of the tick policy but was authored under the same architect
      ruling round? [Exception Coverage, Spec §Architect rulings open to veto]
- [ ] CHK041 Are requirements defined for what happens to the S4 commit
      (T019–T027) if that veto is exercised — must the five `[OPERATOR]` ticks
      and the three sentence amendments be reverted together, mirroring
      FR-017's and FR-018's same-commit discipline, or is a partial reversion
      permitted? [Gap, FR-017, FR-018]
- [ ] CHK042 Are requirements defined for what happens to the `proposal.md`
      additive note (T028) if the first flagged veto (declining the
      enumeration note) is exercised — is the note removed, and is that
      removal itself an archived-record-edit question given `proposal.md` is a
      governance document under the very capability this packet realizes?
      [Gap, Spec §Architect rulings open to veto]
- [ ] CHK043 Are requirements defined for what happens to the two explanatory
      sentences (T007) if the third flagged veto is exercised — does the doc
      bullet revert to the note-form-only shape (Q2b option i), and is that
      reversion itself subject to the doc-health finding-set re-diff (gate 4.4)
      the same way the original edit was? [Gap, FR-005]
- [ ] CHK044 Is it specified WHO notices that a veto has been exercised and
      WHEN — before the branch reaches STOP (B), after the PR opens, or after
      Brett Heap reviews the PR — given the three rulings are stated as "open
      to veto" with no named trigger for when veto exposure closes? [Ambiguity,
      Spec §Architect rulings open to veto]
- [ ] CHK045 If more than one of the three flagged vetoes is exercised
      together, are the three recovery paths (doc bullet, S4 commit,
      `proposal.md` note) specified as independent of each other, or could
      reverting one require reverting another that depends on it? [Gap, Consistency]

## The Stop Condition

- [ ] CHK046 Is the stop condition — STOP at the gate report, no PR, no
      comment, no merge, no archive — stated in exactly ONE place across
      `spec.md`, `plan.md` and `tasks.md`, or does it recur in multiple
      wordings that could drift out of sync with each other? [Consistency,
      FR-015, Plan Implementation sequence, Tasks T032]
- [ ] CHK047 Is "no comment" in the stop condition (FR-015) specific enough to
      cover BOTH a GitHub pull-request comment and a comment on issue #630, or
      could a narrow reading permit one while the rule intends to forbid both?
      [Ambiguity, FR-015]
- [ ] CHK048 Is the stop condition's scope over "no PR" consistent with the
      Assumptions section's statement that the LANE opens the PR — that is, is
      it unambiguous that this feature stopping short of a PR is a boundary
      rule and not merely a scheduling fact that a later session could read as
      already satisfied by someone else's PR? [Consistency, FR-015, Spec §Assumptions]
- [ ] CHK049 Can the stop condition be objectively verified from repository
      state alone (absence of a PR, absence of a merge, absence of an archive
      commit), or does verifying it require trusting an unaudited claim made in
      the report itself? [Measurability, FR-015]
