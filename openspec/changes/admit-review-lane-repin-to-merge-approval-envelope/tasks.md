# Tasks: admit-review-lane-repin-to-merge-approval-envelope

Status: draft
Kind: tasks

`code_surface: openxFactory` (three files), `target_release:` a code surface — so
under `release-realization` this packet archives on merged-plus-green
realization evidence and not on landing.

**THIS PULL REQUEST PERFORMS NOTHING BUT THE FILING.** No envelope byte moves,
no workflow is edited, no test is flipped, no ruleset is touched, no floor is
carved, no pin or snapshot byte moves. **EXACTLY ONE BOX IS TICKED ANYWHERE, AND
IT IS NOT IN THIS FILE:** `amend-mirror-floor-regeneration-merge-authority`
`tasks.md` box **4.3**, whose own tick condition is *"the successor being NAMED
— its openxFactory issue or packet id recorded here"*, on the
tick-on-the-recording rule of 2026-09-06 and on Brett Heap's word *"file it"*.
**EVERY BOX BELOW IS OPEN AND EACH NAMES THE ACT THAT TICKS IT.** No box is
"open forever" and no box is ticked by an agent that is an owner's act.

## 1. Pre-ratification asks — Brett Heap's acts, and no agent may take them

- [ ] 1.1 **RE-OPEN RATIFIED DECISION N-1, or refuse to.** `extend-merge-master-envelope-to-floor-bot-lanes`
      decision **N-1**, ratified 2026-09-07 under *"ratify 746 and 272 as
      recommended when green, then land them"*, admits the codexFactory
      REGENERATION lane ONLY and leaves this lane on a human merge word. This
      packet asks for that decision's own recorded alternative **N-1 (b), admit
      BOTH**, with its condition **N-1b (ii)**, the named carve. **The filing
      does not re-open it; only a word does.** **What ticks it:** Brett Heap's
      word on this packet, recorded on openxFactory #745, either re-opening N-1
      toward (b) or declining. **A DECLINE IS A CONFORMING OUTCOME** and costs
      nothing already spent: `amend-mirror-floor-regeneration-merge-authority`
      box 4.3 ticks on this packet being NAMED, not on it being ratified, and
      the arming stays inert exactly as it is today.
- [ ] 1.2 **Ratify or refuse this packet's TEXT.** Separate from 1.1: a word may
      re-open N-1 and still refuse this text, or ratify this text having
      re-opened N-1. **What ticks it:** the word applied to a named head with its
      checks green, recorded on #745 and in a `review/ratification-<date>.md`
      carrying `Status: ratified`. Until then every document here stays
      `Status: draft` and carries no `Ratified by:` line.
- [ ] 1.3 **Veto or let stand D-1 through D-8** (`design.md` § Authoring
      decisions). Each carries a recommendation and each is one edit away.
      **What ticks it:** the ruling, or a recorded "stand as recommended".
- [ ] 1.4 **Rule the merge method for an autonomously landed advance** (D-4).
      This repository permits merge, squash AND rebase, so unlike codexFactory
      the method is a CHOICE. The recommendation is SQUASH, on the lane's own
      observed precedent: PR #732 merged 2026-09-06T23:46:28Z as `9ffc6252` with
      ONE parent. **What ticks it:** his word, or a recorded "stand".
- [ ] 1.5 **Rule whether the enrolment lands INERT or waits for the carve**
      (D-6). Both answers are conforming — the requirement admits the inert
      state by name — so this is a sequencing choice, not a correctness one, and
      it is the same choice `amend-mirror-floor-regeneration-merge-authority`
      box 1.3 answered "land inert" for the arming. **What ticks it:** the answer
      recorded on #745 and in the ratification record.

## 2. The filing — what this pull request contains

These boxes describe what the pull request already carries. **What ticks § 2:
the ratification landing against this text**, since a ratification says the text
is the RIGHT text and nothing here is proven by being written.

- [ ] 2.1 `specs/review-lane-floor-mirror/spec.md` carries FOUR `## ADDED`
      requirements and no `## MODIFIED` block, so no sibling-pairing declaration
      is owed and no archive ordering is forced beyond `sequenced_after:`.
- [ ] 2.2 **The N-1 re-opening is stated in the proposal's own second heading**,
      with both of Brett Heap's 2026-09-10 § 6.3 rulings quoted verbatim from
      their recordings (openxFactory #745 comment 5618883586; codexFactory #232
      comment 5618469628) and both declared to STAND until this proposal is
      ratified.
- [ ] 2.3 **The never-clearable ground is confronted, not routed around**:
      `proposal.md` § *The design problem* quotes the floor comment verbatim,
      quotes the running park at `merge-master-approval.yml:1504`, and answers
      it with four measured safeguards plus a stated residual risk.
- [ ] 2.4 **Every admission condition is a MEASUREMENT with its command
      recorded**, not an assertion: `expected_author: openxfactory[bot]`
      (`gh api repos/opensoft/openxFactory/pulls/732 --jq .user.login`),
      `expected_head_ref: bot/review-lane-repin`, `expected_base_ref: main`, and
      the four writable files read out of `scripts/review_lane_repin.py:153-156`.
- [ ] 2.5 **No bypass actor is proposed anywhere, in any form**, and the
      proposal says why the grant would be worse here than the one codexFactory
      withdrew on 2026-09-08.
- [ ] 2.6 `.openspec.yaml` declares `kind: ad_hoc` with drafting provenance
      only — no `approved_by`, no `approved_on` — per `add-drafted-proposal-origin`.
- [ ] 2.7 The README **OpenSpec Records** entry is added at the head of the
      active list in house form.
- [ ] 2.8 The `sequenced_after:` declaration validates and the per-change sweep
      ledger carries this change's own row.

## 3. Realization — NOT PERFORMED BY THIS PULL REQUEST

**Each box below is gated on § 1 and on § 4, and none may be taken by an agent
before the word that authorizes it.**

- [ ] 3.1 **Add the second candidate class to `.github/merge-approval-envelope.yml`** —
      `id: openxfactory-review-lane-repin`; `target_repos: [opensoft/openxFactory]`;
      `expected_author: openxfactory[bot]`; `expected_head_ref: bot/review-lane-repin`;
      `expected_base_ref: main`; `path_allowlist` naming EXACTLY
      `contracts/review-lane-pin.yaml`, `contracts/review-lane-floor-snapshot.yaml`,
      `.github/workflows/merge-master-approval.yml`,
      `.github/workflows/pytest-suite.yml`; `require_all_checks: true`;
      `check_exclusions: [merge-master-approval, lane-line]`; `revert_suffices`
      recorded with its reasoning rather than copied. **The existing
      `intent-rolling-custody` entry does not move, byte for byte.**
      **What ticks it:** that edit landed green.
- [ ] 3.2 **Replace `sole_candidate()` in `tests/review_lane_pin/test_review_lane_caller.py`
      with a per-class shape assertion pinning BOTH classes exactly.** The
      helper refuses anything but one candidate today, in terms — *"a second
      entry is a NEW GRANT rather than a configuration change"* — so this is the
      load-bearing edit of the realization and not a consequence of it. The
      replacement keeps that sentence's force: each class is pinned by id, and a
      THIRD class fails the assertion. **What ticks it:** the replacement landed
      with `tests/review_lane_pin/` green.
- [ ] 3.3 **Drop the second sentence of `ARMED_TAIL` in
      `.github/workflows/review-lane-repin.yml:789` AND NOTHING ELSE** — the
      clause the file's own comment at `:783-788` says must go "the day it stops
      being true", replaced by a clause naming what is still missing where the
      carve has not landed. **What ticks it:** the witness text landing and one
      real run's log read back carrying it.
- [ ] 3.4 **Nothing else moves**: no floor composition, no floor member, no
      ruleset, no pin byte, no snapshot byte, no driver line, no credential and
      no second envelope entry beyond 3.1. **What ticks it:** the realization
      pull request's changed-file list read from the API.
- [ ] 3.5 **Suite green and strict validation measured**: `python3 -m pytest -q`,
      the pinned-CLI `--strict` run over this change and over `--all`, and
      `python3 scripts/doc-health.py --single-repo .`. **What ticks it:** the
      recorded exit statuses.

## 4. Evidence and the acts this packet DEPENDS ON but does not take

- [ ] 4.1 **THE CARVE, in codexFactory's decision core** — the **N-1b (ii)**
      shape of `extend-merge-master-envelope-to-floor-bot-lanes`: the floor
      composition at this repository's `.github/workflows/merge-master-approval.yml:1504`
      stops refusing for ONE named enrolled candidate whose floor-matched set is
      exactly `{contracts/review-lane-pin.yaml}`, with the path staying
      never-clearable for every other candidate and every other author.
      **Authored in codexFactory, consumed here at a later re-pin.** **What ticks
      it:** the carve landed in codexFactory's core and this repository re-pinned
      onto it. **NOT ASKED FOR BY THIS PULL REQUEST'S TEXT ALONE** — it is asked
      for by 1.1 and written by codexFactory.
- [ ] 4.2 **THE `Bounded autonomous surface` NARROWING, in codexFactory's
      promoted canon** — its `openspec/specs/merge-master-approval/spec.md`
      forbids autonomously approving any CODEOWNERS-scoped path, and all four of
      this lane's writable files are CODEOWNERS-routed here
      (`.github/CODEOWNERS:2`, `:20`, `:27`). `extend-merge-master-envelope-to-floor-bot-lanes`
      narrowed that requirement for the codexFactory regeneration lane only.
      **What ticks it:** the corresponding narrowing ratified and landed in
      codexFactory, or a recorded ruling that it is not needed with the ground
      stated. **It is codexFactory's text and no openxFactory packet may move
      it.**
- [ ] 4.3 **THE PRECONDITION MEASUREMENT: does auto-merge fire at all on a
      rulesets-only `main`?** Carried here from
      `amend-mirror-floor-regeneration-merge-authority` box 4.4, unticked there:
      `GET /repos/opensoft/openxFactory/branches/main/protection` returns
      `404 "Branch not protected"`, and ZERO of the last 60 closed pull requests
      here carry a non-null `auto_merge`. **Until it is settled, every completion
      shape is premature.** **What ticks it:** ONE throwaway pull request, armed
      and observed, with the arming call's exit status and body and whether the
      merge completed once its requirements were met, recorded on #745.
- [ ] 4.4 **THE COMPLETION-PATH WORD — Brett Heap's, and NO BYPASS IS PROPOSED.**
      Code-owner review is required on `main` by ORGANIZATION ruleset `18834180`
      (`repository_name: ~ALL`, `ref_name: ~DEFAULT_BRANCH`), a GitHub App cannot
      be named in CODEOWNERS, and codexFactory's relocate-off-CODEOWNERS escape
      is measured UNAVAILABLE here because two of the four sites are workflow
      files that cannot leave `.github/workflows/`. **An agent may not take any
      ruleset act.** **What ticks it:** his word naming a shape, recorded on #745.
- [ ] 4.5 **ONE real `bot/review-lane-repin` pull request observed ARMED,
      APPROVED and MERGED with no human act.** Recorded: the run id and the head
      armed at; the pull request number and the merge commit; the actor GitHub
      reports for the merge; and a reviews-API measurement that the only
      approving review is the merge-master identity's. **It is not reachable
      until 4.1, 4.2, 4.3 and 4.4 are taken**, and `target_release:` makes the
      archive wait on it. **What ticks it:** that observation.
- [ ] 4.6 **A deliberate park observed to NOT merge while the class is enrolled**,
      constructed so it varies an input the shipped condition reads — a fifth
      path in the diff, or a red required check. **What ticks it:** the recorded
      park with its reason and the pull request still open after it.

## 5. Successors and the archive

- [ ] 5.1 **Tick `amend-mirror-floor-regeneration-merge-authority` box 4.3 on the
      recording.** Performed BY THIS PULL REQUEST, on Brett Heap's word *"file
      it"* and on the tick-on-the-recording rule of 2026-09-06: the box ticks on
      the successor being NAMED, and the dated note names this packet id and this
      pull request. **What ticks THIS box:** that note landed. **It is the only
      box this pull request ticks anywhere.**
- [ ] 5.2 **Record the referent on both issues.** This packet's id and pull
      request recorded on openxFactory #745 and on codexFactory #232, so the two
      repositories each carry the other's referent for the enrolment question.
      **What ticks it:** those comments posted, verified by their printed URLs.
- [ ] 5.3 **Archive `admit-review-lane-repin-to-merge-approval-envelope`**
      through `python3 scripts/proposal-support.py . <command>` and never bare
      `openspec`, on a later word, **after** `extend-merge-master-envelope-to-floor-bot-lanes`
      and `amend-mirror-floor-regeneration-merge-authority` archive — the
      ordering `sequenced_after:` declares. **What ticks it:** the archive landing
      on box 4.5's evidence, which `target_release:` requires.
