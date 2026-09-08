# Tasks: amend-mirror-floor-regeneration-merge-authority

Status: ratified
Ratified by: amend-mirror-floor-regeneration-merge-authority — 2026-09-08, Brett Heap,
verbatim "merge 292 when green, then ratify 807" (openxFactory #745 comment
5586895152; record `review/ratification-2026-09-08.md`)
Kind: tasks

`code_surface: openxFactory`, `target_release:` a code surface — so under
`release-realization` this packet archives on merged-plus-green realization
evidence and not on landing.

**THIS PULL REQUEST PERFORMS NOTHING BUT THE PROPOSING AND THE RATIFYING.** No
workflow is edited, no test is flipped, no envelope byte moves, no ruleset is
touched, no pin or snapshot byte moves, and no box in any other packet is ticked.
**EXACTLY ONE BOX IS TICKED — 1.1, by the ratifying commit of 2026-09-08 — AND NO
BOX IS "OPEN FOREVER": each one names the act that ticks it.**
The acts are, in order: Brett Heap's ratification; the realization landing green;
the enrolment successor being FILED (which ticks on the successor being NAMED,
per the tick-on-the-recording rule of 2026-09-06); one cheap precondition
measurement, Brett Heap's word on the completion path and a codexFactory carve;
and one observed live cycle.

**AMENDED 2026-09-08 AT RATIFICATION, RATHER THAN LEFT TO CONTRADICT THE TREE.**
As authored this paragraph read that the tick discipline is the parent's and the
twin's and that this packet "follows both" with every box unticked. TWO THINGS
WERE WRONG WITH IT and both are corrected here rather than papered over: the
parent `mirror-floor-regeneration-automation` did ratify with every box unticked,
but codexFactory's twin `amend-floor-regeneration-merge-authority` did NOT — it
ticked 1.1 and 1.2 and disclosed the deviation; and the sentence stopped being
true of THIS pull request the moment the ratification landed inside it. **What
actually happened: box 1.1 alone is ticked**, on the landing lane's instruction
to tick only the box this packet's own rule says ratification ticks. **1.2's
stated condition IS answered** by `review/ratification-2026-09-08.md` § *Which
decisions stand* (M-A..M-G, one line each, none vetoed) and the box is
nevertheless left open; say the word and it ticks in one edit. The commissioning
word — *"rule on finding 3, do the mirror packet too"* — ruled a finding in the
OTHER repository and commissioned this authoring; it ratified no text here. The
RATIFYING word is *"merge 292 when green, then ratify 807"*, and **it still
realizes nothing**.

## 1. Ratification — Brett Heap's acts

- [x] 1.1 **Ratify or refuse this packet.** The word of 2026-09-08T13:22:40Z
      (*"rule on finding 3, do the mirror packet too"*, openxFactory
      [#745](https://github.com/opensoft/openxFactory/issues/745) comment
      5585824802) commissioned the authoring; it did not ratify this text.
      **What ticks it:** a ratification record committed to
      `review/ratification-<date>.md` quoting Brett Heap's verbatim word, the
      head it was given over, and this box citing that record; and
      `proposal.md`/`design.md`/this file moving from `Status: draft` to
      `Status: ratified` with a `Ratified by:` citation, as
      `document-lifecycle`'s ratified-provenance rule requires.
      **2026-09-08 — RATIFIED, and this box is ticked by the act that satisfies
      its own stated condition.** Brett Heap, in session, verbatim *"merge 292
      when green, then ratify 807"* (#745 comment 5586895152, 2026-09-08T14:39Z),
      the second act of a two-act word whose first act landed codexFactory #292
      at merge commit `406a2afb`. Record: `review/ratification-2026-09-08.md`,
      naming the word, the head it was given over (`b910e97d`, all checks green,
      0 unresolved threads), what it ratifies, and what it does NOT decide.
      `proposal.md` carries `Ratified:`; `design.md` and this file carry
      `Ratified by:`. **Nothing is realized by it.**
- [ ] 1.2 **Veto or let stand M-A through M-G** (`design.md` § 3). Each carries a
      recommendation; ratifying without vetoing adopts them as written, the same
      shape M-1..M-7 and N-1..N-5 were ratified in. **The three worth reading
      before the word is given, because each departs from its codexFactory
      counterpart on a measurement of THIS repository: M-B** (merge method — all
      three are permitted here, so the method is a choice; squash is recommended
      on PR #732's observed precedent), **M-C** (a driver-side control must be
      ADDED, because this repository's sweep reads only the workflow's shell),
      and **M-D** (four refusals, not one, so the remedy is a named successor
      packet rather than an owner's single click). **What ticks it:** the
      ratification record naming which decisions stand and which are vetoed —
      one line each, including "none vetoed" if that is the answer.
- [ ] 1.3 **Rule whether the realization lands INERT or waits for the successor**
      (`design.md` M-A, last alternative; M-G's split). The recommendation is to
      land it inert with the inertness declared and reported. Refusing that means
      this packet is ratified as canon and its realization deferred until
      `admit-review-lane-repin-to-merge-approval-envelope` lands. **What ticks
      it:** the answer recorded on #745 and in the ratification record. **Both
      answers are conforming** — the requirement admits the inert state by name
      — so this is a sequencing choice, not a correctness one.

## 2. The amendment — the canon text this pull request carries

These boxes describe what the pull request already contains. **A ratification
says the text is the RIGHT text; what PROVES each box is the realization landing
green against it** — the flipped sweep, the controls and the witness lines all
read this requirement's words. **What ticks § 2: the realization pull request
landing with `tests/review_lane_pin/` green against this text.** Until then the
boxes are the statement of what the realization must not drift from.

- [ ] 2.1 `specs/review-lane-floor-mirror/spec.md` carries ONE
      `## MODIFIED Requirements` block restating *"An automated pin advance only
      ever proposes"* **in full**, with the MUST/SHALL on the FIRST line of the
      body as the strict parser requires.
- [ ] 2.2 **Every ratified sentence of the parent's requirement is carried**: the
      propose-as-a-pull-request duty, the approve bar, the default-branch bar,
      the no-authority-beyond-the-hand-act clause, and the second body paragraph
      (*"The pull request SHALL move the pin and nothing else …"*) **word for
      word**, including its composes-with clause naming *"The mirror is inert
      until the pin carries the rule, and the pin moves as one act"*.
- [ ] 2.3 **The narrowing is exactly one clause, in lockstep with codexFactory's**
      (`amend-floor-regeneration-merge-authority`, main `93f0f0d7`): "SHALL NOT
      merge" becomes "SHALL NOT merge **by its own act**", and the lane "MAY arm
      the platform's auto-merge on that same pull request, so that the merge
      completes only when (a) the merge-master envelope approval for that exact
      head stands and (b) every required check has succeeded". "SHALL NOT
      approve" is untouched; "SHALL NOT push to this repository's default branch"
      is untouched.
- [ ] 2.4 **The grant is bounded IN THE REQUIREMENT, not left to the
      implementation**: no other path to the merge; the default-branch bar
      restated as a bar on the lane's own writes; an unsatisfiable rule leaving
      the arming inert with no widening, no self-granted bypass, no floor removal
      and no self-enrolment; **the inert state named as a CONFORMING state**; the
      releasing approval another party's and bound to the head it names; and the
      arming reported where the run is read.
- [ ] 2.5 **SEVEN SCENARIOS ADDED, ONE CARRIED WITH NARROWED BULLETS, TWO
      CARRIED VERBATIM — ten in the block.** Added: the envelope-approved fully
      green merge with no human act; a park does not merge; **a further advance
      owed while the armed pull request is parked UPDATES it and re-arms**; a
      moved head is not merged on the old approval; the lane never posts an
      approval; **no mechanism can release the arming, and the lane says so**;
      the arming is reported. Narrowed: *The lane opens a pull request and stops
      there*. Verbatim: *The lane never writes to the default branch*, *The
      advance carries nothing but the advance*. Nothing retitled, nothing loses a
      bullet, no requirement removed.
      **AMENDED 2026-09-08, and the count moved because the TEXT did.** As first
      drafted this box said six added and nine in the block, which was true of
      the delta as it then stood. Codex's review (P1) found that the block's
      *"no second act after the arming"* forbade the single-flight UPDATE the
      parent's *The automated advance lane is triggered by the pinned core's own
      movement and every firing is idempotent* REQUIRES; the prohibition was
      narrowed to *"no second act TOWARD THE MERGE"* and the update-and-re-arm
      scenario was added with it. Copilot then found this box still reading nine,
      which is the defect that matters here: a checklist that describes a delta
      it no longer matches is a false witness to its own packet. The count is
      re-read from the delta rather than adjusted by arithmetic.
- [ ] 2.6 `proposal.md` states the commissioning ruling **verbatim** with its
      comment id, the parent sentence **verbatim** as this repository ratified
      it, what does NOT change, the four-refusal realization gate with the
      successor NAMED and its measured shape written out, and this repository's
      own ruleset / auto-merge / merge-method facts measured rather than copied
      from codexFactory.
- [ ] 2.7 `design.md` carries **M-A through M-G, each with a recommendation
      marked**, each refused alternative with a reason apiece, and the three
      departures from D-1..D-7 flagged as departures rather than presented as
      transcription.
- [ ] 2.8 The README **OpenSpec Records** entry is added at the head of the
      active-changes list, naming the commissioning word, the one requirement
      modified, what is admitted, what stays forbidden, and the four-refusal
      realization gate.
- [ ] 2.9 `.openspec.yaml` declares `kind: ad_hoc` with drafting provenance
      (`proposed_by`/`proposed_on`, no approval pair, per
      `add-drafted-proposal-origin`) and the staging check **recorded rather
      than assumed** — `ideation/staging/` enumerated and `INDEX.md` read on
      2026-09-08: no topic names this lane, the merge-approval envelope, the
      review-lane pin or bot merge authority.
- [ ] 2.10 The `sequenced_after:` declaration validates and the per-change sweep
      ledger row is seeded from the live corpus with
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by
      '#<PR>' --moved-on <UTC date>` (the UTC date passed explicitly — the seeder
      defaults to the LOCAL date).

## 3. Realization — A LATER WORD, NOT THIS PULL REQUEST

**What ticks this group:** Brett Heap's realization word, given separately after
§ 1, and then the diffs it authorizes landing green.

- [ ] 3.1 **Arm auto-merge in `.github/workflows/review-lane-repin.yml`**, in the
      existing "Open or update the single automated advance" step, on the same
      App token, as `gh pr merge --auto --squash "${BOT_BRANCH}"`, idempotently
      on BOTH the `gh pr create` path and the `gh pr edit` path (M-A, M-B).
- [ ] 3.2 **Flip
      `test_repin_lane.py::AnAutomatedPinAdvanceOnlyEverProposes::test_the_lane_opens_a_pull_request_and_stops_there`
      exactly as M-C prescribes**: `gh pr merge` and `--auto` admitted only in the
      exact arming form, asserted by EQUALITY (the arming appears exactly twice,
      once per delivery path; no `gh pr merge` occurrence lacks `--auto`); the
      other eight terms and the raw-API merge-endpoint regex still refused.
- [ ] 3.3 **Three negative controls that MEASURE** (the `mirror-floor-addition-grace`
      lesson, `ca9fafe6`): one asserting the lane still names no approval verb
      under any identity, varying the same input the shipped sweep reads; one
      that reds if a THIRD `gh pr merge` occurrence appears in the workflow; and
      **one that sweeps `scripts/review_lane_repin.py` for all ten disposal terms**
      — the driver has never been measured here, and the narrowing's blast-radius
      bound must be created before it can be claimed.
- [ ] 3.4 **`EveryRatifiedScenarioHasATest` re-read, not re-pinned.** Its literal
      scenario count and its `RATIFIED_DELTA` reading must account for this
      packet's block as well as the parent's, and every new scenario needs a test
      docstring quoting its title.
- [ ] 3.5 **The witness lines land with the arming** (M-E): the
      `auto-merge ARMED on #<N> at <head>` notice including the inertness clause
      while it is true, the corrected delivery/summary sentences in place of the
      ones the narrowing makes untrue, and the following firing's line saying what
      became of the armed pull request. Every value recomputable by another party.
- [ ] 3.6 **Nothing else moves**: no envelope byte, no floor composition, no
      `merge-master-approval.yml`, no `pytest-suite.yml`, no pin or snapshot byte,
      no LQ-A7 or freshness-verifier change, no `EXPECT_SKIPPED` movement, no
      ruleset, no credential, no schema. Asserted by the realizing pull request's
      own diff.
- [ ] 3.7 **Suite green and strict validation measured on BOTH sides**:
      `python3 -m pytest tests/review_lane_pin -q` and the full `pytest-suite`
      on the realizing head AND on `origin/main` in a separate clone, so any
      pre-existing failure is shown unchanged rather than claimed; `openspec
      validate … --strict` and `--all --strict` at the pinned CLI
      (`contracts/openspec-cli-pin.yaml`) with the failure set compared to main;
      `python3 scripts/validate-sequenced-after.py .` and `--ledger-diff` clean.

## 4. Evidence and the acts this packet DEPENDS ON but does not take

- [ ] 4.1 **ONE real `bot/review-lane-repin` pull request observed ARMED,
      APPROVED and MERGED with no human act** (M-G half two). Recorded: the run
      id and the head armed at; the pull request number and the merge commit; the
      actor GitHub reports for the merge; and a reviews-API measurement that the
      only approving review is the merge-master identity's. **What ticks it:**
      that observation. **It is not reachable until 4.3, 4.4, 4.5 and 4.6 are
      taken** — an enrolment with no completion mechanism is an approval that
      lands nothing — and `target_release:` makes the archive wait on it.
- [ ] 4.2 **A deliberate park observed to NOT merge while armed**, constructed so
      it varies the same inputs the shipped condition reads. **What ticks it:**
      the recorded park with its reason and the pull request still open after it.
- [ ] 4.3 **THE ENROLMENT SUCCESSOR IS FILED** —
      `admit-review-lane-repin-to-merge-approval-envelope`, whose measured shape
      is written out in `proposal.md` § The realization gate. **What ticks it:**
      the successor being NAMED — its openxFactory issue or packet id recorded
      here — on the tick-on-the-recording rule of 2026-09-06. **This packet does
      not author it**, and filing it re-opens a question ratified decision **N-1**
      answered the other way (this lane stays on a human merge word), so the
      filing itself needs Brett Heap's word.
- [ ] 4.4 **THE PRECONDITION MEASUREMENT: does auto-merge fire at all on a
      rulesets-only `main`?** `GET /repos/opensoft/openxFactory/branches/main/protection`
      returns `404 "Branch not protected"`, and **zero** of the last 60 closed
      pull requests here carry a non-null `auto_merge` — the configuration
      community discussion #162623 reports auto-merge does not fire in. The same
      measurement settles whether `gh pr merge --auto` even succeeds at open time
      or 422s until requirements are met (#190610). **What ticks it:** ONE
      throwaway pull request, armed and observed, with the result recorded on
      #745 — the arming call's exit status and body, and whether the merge
      completed once its requirements were met. It is cheap and it is a
      precondition for every completion shape.
- [ ] 4.5 **THE COMPLETION-PATH WORD — Brett Heap's, and NO BYPASS IS PROPOSED.**
      `design.md` M-D enumerates seven shapes with their costs and recommends
      taking 4.4 first and holding the rest. **NOT recommended in any form: a
      bypass actor on ruleset `18834180`** — codexFactory's D-4 (i) was WITHDRAWN
      on 2026-09-08 (codexFactory #232 comment `5585989018`), and here the grant
      would be worse: `18834180` is an ORGANIZATION ruleset over `~ALL`
      repositories and it is what gives THIS repository its code-owner gate, so
      an entry on it would lift the gate on `contracts/review-lane-pin.yaml`
      estate-wide while, on the reported evidence, not being honoured by the
      async merge path anyway. **Also measured and recorded as UNAVAILABLE:**
      codexFactory's relocate-off-CODEOWNERS shape, because two of this lane's
      four sites are workflow files that cannot leave `.github/workflows/`.
      **An agent may not take any of these shapes.** **What ticks it:** Brett
      Heap's word naming a shape, recorded on #745.
- [ ] 4.6 **THE CARVE, in codexFactory's decision core** — the **N-1b (ii)** shape
      of `extend-merge-master-envelope-to-floor-bot-lanes`: the floor composition
      at this repository's `merge-master-approval.yml:1504` stops refusing for ONE
      named enrolled candidate whose floor-matched set is exactly
      `{contracts/review-lane-pin.yaml}`, with the path staying never-clearable for
      every other candidate and author. **Authored in codexFactory, consumed here
      at a re-pin.** **What ticks it:** the carve landed in codexFactory's core and
      this repository re-pinned onto it. **It is not asked for by this packet**;
      N-1 ruled the other way and reversing that is Brett Heap's.

## 5. Successors and the archive

- [ ] 5.1 **Record the lockstep on the codexFactory side.** codexFactory
      `amend-floor-regeneration-merge-authority` `tasks.md` box **5.1** ticks on
      this packet being NAMED there. **What ticks THIS box:** this packet's id and
      pull request recorded on codexFactory #232 and openxFactory #745, so the two
      halves each carry the other's referent.
- [ ] 5.2 **Archive `amend-mirror-floor-regeneration-merge-authority`** through
      `python3 scripts/proposal-support.py . <command>` and never bare
      `openspec`, on a later word, **after** `mirror-floor-regeneration-automation`
      archives — the ordering `sequenced_after` declares and the ordering the delta
      needs, since the parent is what promotes the requirement this packet
      modifies. **What ticks it:** the archive landing on box 4.1's evidence,
      which `target_release:` requires.
