# Checklist: Cross-Repository Integration and Boundary Claims

**State**: written 2026-09-08, NOT YET RUN — this file is the gate instrument for the architect's refutation panel. The findings its authoring raised were resolved in the analyze loop and are recorded in [`../analysis.md`](../analysis.md).

**Purpose**: Interrogate the QUALITY of the written requirements governing the
matched pair, the other in-flight openxFactory packets this feature names, the
estate-wide obligation, the consumer-re-pin rule, and the lane-collision
obligations — never the implementation of any of them.
**Created**: 2026-09-08
**Feature**: [spec.md](../spec.md)
**Lane**: opsXfactory-1

## The Matched Pair and Boundary Definition

- [x] CHK001 Are the boundaries between this openxFactory half's acts and the
      OpsxFactory twin's acts stated in every section of `spec.md` and
      `tasks.md` that could be read as authorizing work on the twin's behalf?
      [Consistency, Spec §Out of scope, FR-007]
- [x] CHK002 Is the term "matched pair" defined precisely enough to say which
      artifacts belong to which half, or is a reader left to infer it from
      context scattered across `proposal.md` and `spec.md`? [Clarity, Proposal.md]
- [ ] CHK003 Are requirements defined for what this repository's notes may **— OPEN:** FR-007 governs what a twin note may NOT cite (a merge sha) but states no rule for how the note may characterize the twin's RATIFICATION status itself, a state this corpus does not define elsewhere. **FIX:** Add a clause to FR-007 stating the twin note's ratification claim is scoped to what proposal.md's own header states as of the note's date, and is not re-verified by this feature.
      assert about the twin's RATIFICATION status, given "ratified but not yet
      landed on that repository's main" is a state this corpus does not
      otherwise define elsewhere? [Completeness, FR-007]
- [x] CHK004 Is the twin's identity — the SAME working id shared across two
      repositories with two separate OpenSpec instances — disambiguated
      everywhere its notes cite it, so a reader cannot confuse the two
      `govern-archived-record-edits` packets? [Ambiguity, Proposal.md]
- [ ] CHK005 Are requirements defined for what this feature's cross-repository **— OPEN:** No requirement addresses what this feature's cross-repository notes must say if PR #279 is closed WITHOUT merging rather than merged. **FIX:** Add an Edge Case to spec.md naming this contingency and stating the note is corrected forward under FR-021 if it occurs before this branch's final commit.
      notes must say if PR #279 is closed WITHOUT merging, rather than merged?
      [Gap]
- [ ] CHK006 Can "ratified" as applied to the OpsxFactory twin be objectively **— OPEN:** Nothing states that "ratified" as applied to the OpsxFactory twin cannot be objectively verified from inside this repository's clone (this feature may not run gh, per FR-015), so the claim rests on asserted, out-of-band knowledge. **FIX:** Add a sentence to FR-007 or Key Entities stating the twin's status is asserted from the architect's own knowledge at authoring time and is not independently verified by any gate in this feature.
      verified from artifacts reachable inside this repository's clone, or does
      the claim require trusting an assertion this branch cannot itself
      resolve? [Measurability, FR-007]

## State Claims About the Twin and Their Freshness

- [x] CHK007 Is the freshness of a claim about another repository's state (for
      example "PR #279, ratified, not yet merged") tied to a measured point in
      time, so a reader well after this branch lands can tell whether the claim
      is stale? [Completeness, FR-007]
- [ ] CHK008 Are requirements defined for HOW STALE a cross-repository note may **— OPEN:** No requirement states how stale a cross-repository note may become before it needs re-verification; "freshness" is wholly unquantified for the twin note, the consent-custody note, or any other cross-repo citation. **FIX:** Add a sentence (e.g., to FR-023 or a new FR) stating these notes are point-in-time citations valid as of their dated line and are never re-verified by this feature after commit.
      become before it must be re-verified, or is "freshness" left wholly
      unquantified? [Ambiguity]
- [ ] CHK009 Is there a stated rule distinguishing a note that CITES another **— OPEN:** No stated rule distinguishes a note that CITES another repository's artifact (change id, PR number) from one that ASSERTS a fact about that artifact's current disposition, though only the second needs re-verification. **FIX:** Add this distinction to FR-007, alongside the fix proposed for CHK003.
      repository's artifact (change id, PR number) from a note that ASSERTS a
      fact about that artifact's current disposition, given the second requires
      re-verification the first does not? [Clarity, FR-007]
- [ ] CHK010 Are requirements defined for what a note may claim about the **— OPEN:** FR-007 says notes cite the twin's state "at this date" but never distinguishes what a note may claim about the twin's state AT BRANCH CUT from what it may claim BY THE TIME THE BRANCH LANDS. **FIX:** Add a clause to FR-007 stating the note is authored once, dated to that authoring date, and is not updated for any twin-state change between cut and landing.
      twin's state at the moment this branch is CUT versus what it may claim by
      the moment it LANDS, since the two are necessarily measured at different
      times? [Gap]
- [x] CHK011 Is the prohibition on citing a merge sha for the twin ("no such
      sha exists") paired with a positive rule for what MUST be cited instead,
      so the absence of one permitted claim is not read as license to omit all
      provenance? [Completeness, FR-007]
- [x] CHK012 Are requirements consistent between `spec.md`'s Clarifications §Q7
      answer and the OpenSpec packet's task 3.1 text on what a twin-referencing
      note must name (repository, change id, PR number) and must NOT name
      (merge sha)? [Consistency, Spec Clarifications Q7, OpenSpec Tasks §3.1]

## The Consent-Custody Packet (Task 3.3, Out of Scope Here)

- [x] CHK013 Is the boundary between this feature's acts and
      `add-consent-custody-rederivation-record`'s acts stated precisely enough
      that naming that packet cannot be mistaken for performing its contract
      cut? [Clarity, OpenSpec Tasks §3.3]
- [ ] CHK014 Are requirements defined for what this feature's notes may say **— OPEN:** No requirement addresses whether this feature's task-3.3 note must be refreshed if add-consent-custody-rederivation-record's 46-box count changes before this branch's final commit. **FIX:** Add a sentence to FR-007 (or T029) requiring a re-check of the cited box count at the final-head gate re-run, consistent with the treatment other measurements get at T029.
      about that packet's 46-box, all-unticked state, given that state can
      change independently of this branch while this branch is open? [Completeness]
- [x] CHK015 Is the merged commit `543d47a9` cited as the packet's LANDING fact
      only, with no requirement here implying that packet's WORK (the contract
      cut itself) is also complete? [Ambiguity, Proposal.md §Impact]
- [ ] CHK016 Are requirements defined for whether this feature's own task 3.3 **— OPEN:** Same gap as CHK014: nothing requires the task-3.3 note to be refreshed if the cited packet's state changes before this branch's final commit. **FIX:** Fold into a single re-verification requirement covering both the twin and consent-custody notes at T029, per CHK014's fix.
      note must be refreshed if `add-consent-custody-rederivation-record`'s box
      count changes before this branch's final commit? [Gap]
- [ ] CHK017 Is it specified whose responsibility it is to notice if **— OPEN:** No requirement names WHOSE responsibility it is to notice if add-consent-custody-rederivation-record lands its contract cut while this branch is open, or whether that changes any note this feature writes. **FIX:** Add a sentence to spec.md's Out of scope or FR-007 naming this as the lane's noticing responsibility at PR/landing time, mirroring FR-015's assignment of other cross-cutting obligations to the lane.
      `add-consent-custody-rederivation-record` lands its contract cut WHILE
      this branch is open, and whether that changes any note this feature
      writes? [Coverage, Gap]

## The Estate-Wide Obligation (Task 3.5)

- [x] CHK018 Is the scope of "every OTHER DomainxFactory" in task 3.5
      enumerated or bounded, or does the obligation rest on an open-ended and
      unenumerated set of future readers? [Ambiguity, OpenSpec Tasks §3.5]
- [ ] CHK019 Are requirements defined for what this feature's note beside task **— OPEN:** T023 gives exact required wording for the 3.1 and 3.3 NOT-OWED notes but not for 3.2 or 3.5, so a reader does not know what those two notes must say beyond "one dated NOT-OWED line." **FIX:** Add explicit wording (or a wording template) for the 3.2 and 3.5 notes to T023, matching the specificity already given for 3.1 and 3.3.
      3.5 must say, given the task itself states only that the obligation is
      "named as owed; not surveyed here"? [Completeness]
- [x] CHK020 Is there a stated mechanism by which a DomainxFactory OTHER than
      OpsxFactory learns that it owes this obligation, or does the requirement
      rely on that repository discovering the promoted capability unaided?
      [Gap]
- [ ] CHK021 Can "amends whatever is looser" (task 3.5's standard) be **— OPEN:** Task 3.5's "amends whatever is looser" standard presumes a local convention exists to compare against; nothing states what the standard means for a DomainxFactory with NO convention at all — the same condition openxFactory itself was measured to be in. **FIX:** Add a sentence to spec.md's Out of scope stating that "amends whatever is looser" reduces to "adopts the neutral minimum" for a repository with no convention, mirroring task 3.4's own resolution.
      objectively measured by a repository with no archived-packet convention
      at all — the same condition openxFactory itself was measured to be in?
      [Measurability, Proposal.md §Impact]

## The Consumer Re-Pin Rule

- [ ] CHK022 Is the ratified scenario *A dependent pin lives in another **— OPEN:** FR-008 measures only IN-REPO pins and never explicitly connects that scope limit to the ratified "A dependent pin lives in another repository" scenario, so the evidence file does not state that the cross-repository case is structurally unmeasured rather than resolved. **FIX:** Add a sentence to FR-008 stating that a consuming-repository pin, if any exists, falls outside this measurement's in-repo scope and remains that repository's own obligation to detect.
      repository* — which requires recording the owed consumer re-pin "by
      name, repository and instrument" — reflected consistently in this
      feature's own FR-008 measurement, given FR-008 finds NO in-repo pin
      naming the edited file? [Consistency, FR-008, Ratified Spec §document-lifecycle]
- [ ] CHK023 Are requirements defined for what this feature must do if the **— OPEN:** No requirement addresses what this feature must do if the § 3.4 edit were later found to be a pinned target in another repository, outside this repository's visibility. **FIX:** Add a sentence to FR-008 or Out of scope stating this possibility is unmeasurable from this repository and is accepted as a residual risk the consuming repository's own gates must catch.
      § 3.4 edit to `docs/document-lifecycle.md` were later found to BE a
      pinned target in a repository OTHER than this one, outside this
      repository's own visibility? [Gap]
- [ ] CHK024 Is "instrument" — one of the three required naming elements **— OPEN:** The ratified scenario's third required naming element, "instrument," is never defined generically anywhere this feature or the packet reaches; the term only appears attached to "consent instruments" in one context. **FIX:** Note this as an inherited ambiguity in the ratified text that this feature does not need to resolve because M2 found no dependent pin, and state that explicitly in FR-008 rather than leaving it silent.
      (name, repository, instrument) in the ratified scenario — defined
      anywhere this feature or the packet reaches, so a note-writer knows what
      value to supply? [Clarity, Ratified Spec §document-lifecycle]
- [x] CHK025 Is the distinction between an IN-REPO pin (FR-008's scope) and a
      pin held by a CONSUMING repository (the ratified scenario's scope) stated
      clearly enough that the two measurements are not conflated in the
      evidence file? [Consistency, FR-008]

## Cross-Citation Resolution ("Once Both Heads Settle")

- [x] CHK026 Is "the cross-citations are re-checked once both heads settle"
      (OpenSpec Tasks §3.1) specified precisely enough to say WHO performs the
      re-check, WHEN "settled" is measured, and WHAT artifact records the
      result — or does it stand as an unresolved instruction with no named
      actor? [Ambiguity, OpenSpec Tasks §3.1]
- [x] CHK027 Is "settle" itself defined — does a head settle when its PR
      merges, when its packet archives, or when both conditions hold — or is
      the term left to the reader's judgment? [Ambiguity]
- [ ] CHK028 Are requirements defined for what happens if the two heads never **— OPEN:** No requirement addresses what happens if the twin's change id or PR number changes before it lands, preventing the two heads' cross-citations from ever resolving cleanly. **FIX:** Add an Edge Case naming this failure mode and stating it is corrected forward under FR-021 whenever noticed, by whichever actor notices it.
      settle in a way that makes the cross-citations resolve cleanly (for
      example, the twin's change id or PR number changes before it lands)?
      [Gap, Exception Coverage]
- [x] CHK029 Is the re-check obligation of task 3.1 assigned to a party this
      feature can name, or does it fall to whichever future reader next opens
      the file — and if the latter, is that stated as a deliberate design
      choice rather than an oversight? [Completeness, Gap]
- [x] CHK030 Does this feature's own task 3.1 NOT-OWED-YET note create any
      expectation that THIS feature will perform the re-check, and if not, is
      that non-expectation stated explicitly rather than left to be inferred
      from the "not owed here" framing? [Clarity, FR-007]

## Lane-Collision Obligations: This Feature's Versus the Lane's

- [x] CHK031 Is the division between obligations this feature performs (Lane
      trailers on its own commits) and obligations the lane performs (claim,
      PR, LANDING/LANDED, archive) stated in one place a reader can find
      without cross-referencing the root-repository lane-collision protocol?
      [Consistency, Spec §Assumptions, FR-014, FR-015]
- [ ] CHK032 Are requirements defined for whether "claim before author" (the **— OPEN:** spec.md's Assumptions state the dedicated clone is exclusive and never shared, but do not say whether "claim before author" (which targets the governing ISSUE, not the clone) still applies to this feature's own commits before the lane's later claim. **FIX:** Add a sentence to spec.md's Assumptions clarifying whether this feature's commits are authored before or after the lane's claim on issue #630, or stating that the clone's exclusivity does not exempt this feature from that rule.
      lane-collision protocol's first obligation) applies to this feature's own
      work inside the dedicated clone, given the clone is described as
      exclusive to this realization and never shared? [Gap]
- [x] CHK033 Is the `Lane: opsXfactory-1` trailer requirement (FR-014)
      consistent with the wider protocol's requirement that the trailer appear
      "on every PR body, comment and commit trailer", given this feature is
      explicitly forbidden from opening a PR or posting a comment (FR-015)?
      [Consistency, FR-014, FR-015]
- [ ] CHK034 Are requirements defined for what happens if another lane posts a **— OPEN:** No requirement addresses what happens if another lane posts a LANDING notice touching issue #630 or a related PR while this feature's branch is still open, before this feature's owning lane has claimed. **FIX:** Add a sentence to spec.md's Out of scope or Assumptions naming this collision as the lane's own responsibility to detect and resolve per the root lane-collision protocol.
      LANDING notice touching issue #630 or a related PR WHILE this feature's
      branch is still open, before the lane that owns this feature has
      claimed? [Gap, Exception Coverage]
- [x] CHK035 Is it specified who discharges the CLAIMED comment on issue #630
      for this feature's own work, versus any separate claim needed for the
      lane's later PR and LANDING acts? [Ambiguity, Spec §Assumptions]

## Non-Functional: Traceability and Terminology Consistency

- [x] CHK036 Is the vocabulary distinguishing "this openxFactory half", "the
      OpsxFactory twin", "another openxFactory packet", and "a further
      DomainxFactory" used consistently across `spec.md`, the OpenSpec packet's
      `tasks.md`, and `proposal.md`, or does any section substitute one term
      for another in a way that could blur the boundary? [Consistency]
- [x] CHK037 Can a reader who has read ONLY this feature's `spec.md` and
      `tasks.md` — never the OpenSpec packet directly — correctly identify
      which of the 28 boxes are cross-repository claims versus in-repository
      claims? [Coverage, Independent Test]
- [x] CHK038 Are the citation forms used for the twin (repository + change id +
      PR #279) and for the consent-custody packet (change id + merge sha
      `543d47a9`) each internally consistent wherever they recur in this
      feature's own artifacts? [Consistency]
- [ ] CHK039 Is there a single stated rule for how long a cross-repository **— OPEN:** No single rule states how long a cross-repository citation in the evidence file remains authoritative before it must be treated as possibly stale; every citation this feature writes is silent on this. **FIX:** Add one FR or evidence-file header requirement stating all cross-repository citations are point-in-time as of their dated line and are never re-verified after commit, consistent with the fix proposed for CHK008.
      citation in this feature's evidence file remains authoritative before it
      must be treated as possibly stale, or is that duration left unstated for
      every citation this feature writes? [Measurability, Gap]
## Evaluation — 2026-09-08

**Tally**: 21 passed / 18 open / 0 deferred (total 39).

### Open items
- CHK003 — FR-007 governs what a twin note may NOT cite (a merge sha) but states no rule for how the note may characterize the twin's RATIFICATION status itself, a state this corpus does not define elsewhere. → Add a clause to FR-007 stating the twin note's ratification claim is scoped to what proposal.md's own header states as of the note's date, and is not re-verified by this feature.
- CHK005 — No requirement addresses what this feature's cross-repository notes must say if PR #279 is closed WITHOUT merging rather than merged. → Add an Edge Case to spec.md naming this contingency and stating the note is corrected forward under FR-021 if it occurs before this branch's final commit.
- CHK006 — Nothing states that "ratified" as applied to the OpsxFactory twin cannot be objectively verified from inside this repository's clone (this feature may not run gh, per FR-015), so the claim rests on asserted, out-of-band knowledge. → Add a sentence to FR-007 or Key Entities stating the twin's status is asserted from the architect's own knowledge at authoring time and is not independently verified by any gate in this feature.
- CHK008 — No requirement states how stale a cross-repository note may become before it needs re-verification; "freshness" is wholly unquantified for the twin note, the consent-custody note, or any other cross-repo citation. → Add a sentence (e.g., to FR-023 or a new FR) stating these notes are point-in-time citations valid as of their dated line and are never re-verified by this feature after commit.
- CHK009 — No stated rule distinguishes a note that CITES another repository's artifact (change id, PR number) from one that ASSERTS a fact about that artifact's current disposition, though only the second needs re-verification. → Add this distinction to FR-007, alongside the fix proposed for CHK003.
- CHK010 — FR-007 says notes cite the twin's state "at this date" but never distinguishes what a note may claim about the twin's state AT BRANCH CUT from what it may claim BY THE TIME THE BRANCH LANDS. → Add a clause to FR-007 stating the note is authored once, dated to that authoring date, and is not updated for any twin-state change between cut and landing.
- CHK014 — No requirement addresses whether this feature's task-3.3 note must be refreshed if add-consent-custody-rederivation-record's 46-box count changes before this branch's final commit. → Add a sentence to FR-007 (or T029) requiring a re-check of the cited box count at the final-head gate re-run, consistent with the treatment other measurements get at T029.
- CHK016 — Same gap as CHK014: nothing requires the task-3.3 note to be refreshed if the cited packet's state changes before this branch's final commit. → Fold into a single re-verification requirement covering both the twin and consent-custody notes at T029, per CHK014's fix.
- CHK017 — No requirement names WHOSE responsibility it is to notice if add-consent-custody-rederivation-record lands its contract cut while this branch is open, or whether that changes any note this feature writes. → Add a sentence to spec.md's Out of scope or FR-007 naming this as the lane's noticing responsibility at PR/landing time, mirroring FR-015's assignment of other cross-cutting obligations to the lane.
- CHK019 — T023 gives exact required wording for the 3.1 and 3.3 NOT-OWED notes but not for 3.2 or 3.5, so a reader does not know what those two notes must say beyond "one dated NOT-OWED line." → Add explicit wording (or a wording template) for the 3.2 and 3.5 notes to T023, matching the specificity already given for 3.1 and 3.3.
- CHK021 — Task 3.5's "amends whatever is looser" standard presumes a local convention exists to compare against; nothing states what the standard means for a DomainxFactory with NO convention at all — the same condition openxFactory itself was measured to be in. → Add a sentence to spec.md's Out of scope stating that "amends whatever is looser" reduces to "adopts the neutral minimum" for a repository with no convention, mirroring task 3.4's own resolution.
- CHK022 — FR-008 measures only IN-REPO pins and never explicitly connects that scope limit to the ratified "A dependent pin lives in another repository" scenario, so the evidence file does not state that the cross-repository case is structurally unmeasured rather than resolved. → Add a sentence to FR-008 stating that a consuming-repository pin, if any exists, falls outside this measurement's in-repo scope and remains that repository's own obligation to detect.
- CHK023 — No requirement addresses what this feature must do if the § 3.4 edit were later found to be a pinned target in another repository, outside this repository's visibility. → Add a sentence to FR-008 or Out of scope stating this possibility is unmeasurable from this repository and is accepted as a residual risk the consuming repository's own gates must catch.
- CHK024 — The ratified scenario's third required naming element, "instrument," is never defined generically anywhere this feature or the packet reaches; the term only appears attached to "consent instruments" in one context. → Note this as an inherited ambiguity in the ratified text that this feature does not need to resolve because M2 found no dependent pin, and state that explicitly in FR-008 rather than leaving it silent.
- CHK028 — No requirement addresses what happens if the twin's change id or PR number changes before it lands, preventing the two heads' cross-citations from ever resolving cleanly. → Add an Edge Case naming this failure mode and stating it is corrected forward under FR-021 whenever noticed, by whichever actor notices it.
- CHK032 — spec.md's Assumptions state the dedicated clone is exclusive and never shared, but do not say whether "claim before author" (which targets the governing ISSUE, not the clone) still applies to this feature's own commits before the lane's later claim. → Add a sentence to spec.md's Assumptions clarifying whether this feature's commits are authored before or after the lane's claim on issue #630, or stating that the clone's exclusivity does not exempt this feature from that rule.
- CHK034 — No requirement addresses what happens if another lane posts a LANDING notice touching issue #630 or a related PR while this feature's branch is still open, before this feature's owning lane has claimed. → Add a sentence to spec.md's Out of scope or Assumptions naming this collision as the lane's own responsibility to detect and resolve per the root lane-collision protocol.
- CHK039 — No single rule states how long a cross-repository citation in the evidence file remains authoritative before it must be treated as possibly stale; every citation this feature writes is silent on this. → Add one FR or evidence-file header requirement stating all cross-repository citations are point-in-time as of their dated line and are never re-verified after commit, consistent with the fix proposed for CHK008.

### Deferred items
- None — every item in this checklist interrogates the WRITTEN requirements' quality, never an execution result, so no item qualifies for deferral.
