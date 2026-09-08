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

- [ ] CHK001 Are the boundaries between this openxFactory half's acts and the
      OpsxFactory twin's acts stated in every section of `spec.md` and
      `tasks.md` that could be read as authorizing work on the twin's behalf?
      [Consistency, Spec §Out of scope, FR-007]
- [ ] CHK002 Is the term "matched pair" defined precisely enough to say which
      artifacts belong to which half, or is a reader left to infer it from
      context scattered across `proposal.md` and `spec.md`? [Clarity, Proposal.md]
- [ ] CHK003 Are requirements defined for what this repository's notes may
      assert about the twin's RATIFICATION status, given "ratified but not yet
      landed on that repository's main" is a state this corpus does not
      otherwise define elsewhere? [Completeness, FR-007]
- [ ] CHK004 Is the twin's identity — the SAME working id shared across two
      repositories with two separate OpenSpec instances — disambiguated
      everywhere its notes cite it, so a reader cannot confuse the two
      `govern-archived-record-edits` packets? [Ambiguity, Proposal.md]
- [ ] CHK005 Are requirements defined for what this feature's cross-repository
      notes must say if PR #279 is closed WITHOUT merging, rather than merged?
      [Gap]
- [ ] CHK006 Can "ratified" as applied to the OpsxFactory twin be objectively
      verified from artifacts reachable inside this repository's clone, or does
      the claim require trusting an assertion this branch cannot itself
      resolve? [Measurability, FR-007]

## State Claims About the Twin and Their Freshness

- [ ] CHK007 Is the freshness of a claim about another repository's state (for
      example "PR #279, ratified, not yet merged") tied to a measured point in
      time, so a reader well after this branch lands can tell whether the claim
      is stale? [Completeness, FR-007]
- [ ] CHK008 Are requirements defined for HOW STALE a cross-repository note may
      become before it must be re-verified, or is "freshness" left wholly
      unquantified? [Ambiguity]
- [ ] CHK009 Is there a stated rule distinguishing a note that CITES another
      repository's artifact (change id, PR number) from a note that ASSERTS a
      fact about that artifact's current disposition, given the second requires
      re-verification the first does not? [Clarity, FR-007]
- [ ] CHK010 Are requirements defined for what a note may claim about the
      twin's state at the moment this branch is CUT versus what it may claim by
      the moment it LANDS, since the two are necessarily measured at different
      times? [Gap]
- [ ] CHK011 Is the prohibition on citing a merge sha for the twin ("no such
      sha exists") paired with a positive rule for what MUST be cited instead,
      so the absence of one permitted claim is not read as license to omit all
      provenance? [Completeness, FR-007]
- [ ] CHK012 Are requirements consistent between `spec.md`'s Clarifications §Q7
      answer and the OpenSpec packet's task 3.1 text on what a twin-referencing
      note must name (repository, change id, PR number) and must NOT name
      (merge sha)? [Consistency, Spec Clarifications Q7, OpenSpec Tasks §3.1]

## The Consent-Custody Packet (Task 3.3, Out of Scope Here)

- [ ] CHK013 Is the boundary between this feature's acts and
      `add-consent-custody-rederivation-record`'s acts stated precisely enough
      that naming that packet cannot be mistaken for performing its contract
      cut? [Clarity, OpenSpec Tasks §3.3]
- [ ] CHK014 Are requirements defined for what this feature's notes may say
      about that packet's 46-box, all-unticked state, given that state can
      change independently of this branch while this branch is open? [Completeness]
- [ ] CHK015 Is the merged commit `543d47a9` cited as the packet's LANDING fact
      only, with no requirement here implying that packet's WORK (the contract
      cut itself) is also complete? [Ambiguity, Proposal.md §Impact]
- [ ] CHK016 Are requirements defined for whether this feature's own task 3.3
      note must be refreshed if `add-consent-custody-rederivation-record`'s box
      count changes before this branch's final commit? [Gap]
- [ ] CHK017 Is it specified whose responsibility it is to notice if
      `add-consent-custody-rederivation-record` lands its contract cut WHILE
      this branch is open, and whether that changes any note this feature
      writes? [Coverage, Gap]

## The Estate-Wide Obligation (Task 3.5)

- [ ] CHK018 Is the scope of "every OTHER DomainxFactory" in task 3.5
      enumerated or bounded, or does the obligation rest on an open-ended and
      unenumerated set of future readers? [Ambiguity, OpenSpec Tasks §3.5]
- [ ] CHK019 Are requirements defined for what this feature's note beside task
      3.5 must say, given the task itself states only that the obligation is
      "named as owed; not surveyed here"? [Completeness]
- [ ] CHK020 Is there a stated mechanism by which a DomainxFactory OTHER than
      OpsxFactory learns that it owes this obligation, or does the requirement
      rely on that repository discovering the promoted capability unaided?
      [Gap]
- [ ] CHK021 Can "amends whatever is looser" (task 3.5's standard) be
      objectively measured by a repository with no archived-packet convention
      at all — the same condition openxFactory itself was measured to be in?
      [Measurability, Proposal.md §Impact]

## The Consumer Re-Pin Rule

- [ ] CHK022 Is the ratified scenario *A dependent pin lives in another
      repository* — which requires recording the owed consumer re-pin "by
      name, repository and instrument" — reflected consistently in this
      feature's own FR-008 measurement, given FR-008 finds NO in-repo pin
      naming the edited file? [Consistency, FR-008, Ratified Spec §document-lifecycle]
- [ ] CHK023 Are requirements defined for what this feature must do if the
      § 3.4 edit to `docs/document-lifecycle.md` were later found to BE a
      pinned target in a repository OTHER than this one, outside this
      repository's own visibility? [Gap]
- [ ] CHK024 Is "instrument" — one of the three required naming elements
      (name, repository, instrument) in the ratified scenario — defined
      anywhere this feature or the packet reaches, so a note-writer knows what
      value to supply? [Clarity, Ratified Spec §document-lifecycle]
- [ ] CHK025 Is the distinction between an IN-REPO pin (FR-008's scope) and a
      pin held by a CONSUMING repository (the ratified scenario's scope) stated
      clearly enough that the two measurements are not conflated in the
      evidence file? [Consistency, FR-008]

## Cross-Citation Resolution ("Once Both Heads Settle")

- [ ] CHK026 Is "the cross-citations are re-checked once both heads settle"
      (OpenSpec Tasks §3.1) specified precisely enough to say WHO performs the
      re-check, WHEN "settled" is measured, and WHAT artifact records the
      result — or does it stand as an unresolved instruction with no named
      actor? [Ambiguity, OpenSpec Tasks §3.1]
- [ ] CHK027 Is "settle" itself defined — does a head settle when its PR
      merges, when its packet archives, or when both conditions hold — or is
      the term left to the reader's judgment? [Ambiguity]
- [ ] CHK028 Are requirements defined for what happens if the two heads never
      settle in a way that makes the cross-citations resolve cleanly (for
      example, the twin's change id or PR number changes before it lands)?
      [Gap, Exception Coverage]
- [ ] CHK029 Is the re-check obligation of task 3.1 assigned to a party this
      feature can name, or does it fall to whichever future reader next opens
      the file — and if the latter, is that stated as a deliberate design
      choice rather than an oversight? [Completeness, Gap]
- [ ] CHK030 Does this feature's own task 3.1 NOT-OWED-YET note create any
      expectation that THIS feature will perform the re-check, and if not, is
      that non-expectation stated explicitly rather than left to be inferred
      from the "not owed here" framing? [Clarity, FR-007]

## Lane-Collision Obligations: This Feature's Versus the Lane's

- [ ] CHK031 Is the division between obligations this feature performs (Lane
      trailers on its own commits) and obligations the lane performs (claim,
      PR, LANDING/LANDED, archive) stated in one place a reader can find
      without cross-referencing the root-repository lane-collision protocol?
      [Consistency, Spec §Assumptions, FR-014, FR-015]
- [ ] CHK032 Are requirements defined for whether "claim before author" (the
      lane-collision protocol's first obligation) applies to this feature's own
      work inside the dedicated clone, given the clone is described as
      exclusive to this realization and never shared? [Gap]
- [ ] CHK033 Is the `Lane: opsXfactory-1` trailer requirement (FR-014)
      consistent with the wider protocol's requirement that the trailer appear
      "on every PR body, comment and commit trailer", given this feature is
      explicitly forbidden from opening a PR or posting a comment (FR-015)?
      [Consistency, FR-014, FR-015]
- [ ] CHK034 Are requirements defined for what happens if another lane posts a
      LANDING notice touching issue #630 or a related PR WHILE this feature's
      branch is still open, before the lane that owns this feature has
      claimed? [Gap, Exception Coverage]
- [ ] CHK035 Is it specified who discharges the CLAIMED comment on issue #630
      for this feature's own work, versus any separate claim needed for the
      lane's later PR and LANDING acts? [Ambiguity, Spec §Assumptions]

## Non-Functional: Traceability and Terminology Consistency

- [ ] CHK036 Is the vocabulary distinguishing "this openxFactory half", "the
      OpsxFactory twin", "another openxFactory packet", and "a further
      DomainxFactory" used consistently across `spec.md`, the OpenSpec packet's
      `tasks.md`, and `proposal.md`, or does any section substitute one term
      for another in a way that could blur the boundary? [Consistency]
- [ ] CHK037 Can a reader who has read ONLY this feature's `spec.md` and
      `tasks.md` — never the OpenSpec packet directly — correctly identify
      which of the 28 boxes are cross-repository claims versus in-repository
      claims? [Coverage, Independent Test]
- [ ] CHK038 Are the citation forms used for the twin (repository + change id +
      PR #279) and for the consent-custody packet (change id + merge sha
      `543d47a9`) each internally consistent wherever they recur in this
      feature's own artifacts? [Consistency]
- [ ] CHK039 Is there a single stated rule for how long a cross-repository
      citation in this feature's evidence file remains authoritative before it
      must be treated as possibly stale, or is that duration left unstated for
      every citation this feature writes? [Measurability, Gap]
