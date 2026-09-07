# Tasks: extend-merge-master-envelope-to-floor-bot-lanes

Status: ratified

**RATIFIED 2026-09-07** — Brett Heap, in session at 2026-09-07T12:32:44Z,
verbatim *"ratify 746 and 272 as recommended when green, then land them"*; record
`review/ratification-2026-09-07.md`. **THE RATIFICATION PERFORMS NOTHING IN THIS
FILE.** Decisions N-1 through N-5 stand as recommended, and every box below —
including group 1's, whose work is what produced the packet that was ratified —
remains UNTICKED.

**EVERY BOX BELOW IS UNTICKED AND NONE MAY BE TICKED BY THIS PACKET.** Group 1
is the authoring that produced the packet you are reading; groups 2 through 4 are
realization and its evidence, which is a LATER WORD AND HAS NOT BEEN GIVEN —
nothing is enrolled, no envelope file is edited, no floor path moves and no
ruleset changes; group 5 is the owner's, and an agent may not tick an owner's-act
box at all — where such an act is taken, it is recorded as a dated note beneath
the box and the box stays unticked. § 5.1 (the ratification) was TAKEN on
2026-09-07 and its box stays unticked for exactly that reason.

Groups 2 through 4 are written for the RECOMMENDED scope of decision N-1 —
the codexFactory regeneration lane alone. Where a veto to N-1 (b) would add work,
the addition is named in the task rather than left to be discovered, and § 2.9
carries the whole of the wider scope in one place.

## 1. Proposal

- [ ] 1.1 Author `proposal.md` with `code_surface:` and `target_release:`
  front-matter, a `Status:` header inside the first fifteen real lines (`draft` at
  authoring; `ratified` since 2026-09-07, with the `Ratified:` citation beside
  it), the origin citation to openxFactory #745 and codexFactory #232, and the
  explicit statement that the authorizing word authorized the PROPOSING and not
  the content.
- [ ] 1.2 Author `design.md` measuring, in the working tree and against the live
  API, WHERE the envelope is declared, WHAT it evaluates, and WHAT stands between
  each bot lane and an autonomous approval — every claim cited `file:line`, and
  any place the governing brief's premise and the tree disagree written down as
  the tree has it and flagged as a difference.
- [ ] 1.3 State decisions N-1 through N-5 (and N-1b, which the measurement
  forced) each with a recommendation, its alternatives, and what a veto costs —
  so that every one of them is one edit away from being overruled.
- [ ] 1.4 Author the spec deltas: `roles-authority-model` for the neutral
  enrolment rules, `review-lane-floor-mirror` for the two named lanes. Every
  requirement SHALL on line one; every requirement at least one
  `#### Scenario:`.
- [ ] 1.5 Author `.openspec.yaml` with the ad-hoc origin, the reason the staging
  queue was checked and found not to name this, and the authorizing word recorded
  as admission-to-queue rather than as ratification.
- [ ] 1.6 Enter the change in the README "OpenSpec Records" active block, and
  seed its per-change sweep ledger row through the sanctioned writer
  (`scripts/validate-sequenced-after.py --seed-ledger`) with `--moved-on` in UTC.
- [ ] 1.7 Validate at the PINNED CLI: `--change` strict clean, and `--all
  --strict` with the failure set unchanged against `main`, both recorded on the
  pull request.

## 2. Realization — the codexFactory companion (a LATER WORD, and a change authored THERE)

**None of this is openxFactory's to author.** § 2.1 through § 2.8 describe a
codexFactory change that must be proposed, ratified and realized in that
repository under its own governance; this packet names the surface so the two
halves cannot drift, exactly as the option-(b) pair did.

**§ 2.1, § 2.1a and § 2.1b ARE AUTHORED — as draft
[codexFactory #272](https://github.com/opensoft/codexFactory/pull/272)**, filed
alongside this packet by the same lane on the same word, carrying the
`## MODIFIED` narrowing, recommending a Gate-Rules Council record as its
instrument (its OQ-C1) and deferring the two-writers declaration against the
sibling `add-regular-pr-council-clearance` with its measured reason (its OQ-C2).
The boxes stay unticked because that packet is a PROPOSAL and its ratification is
owed. § 2.2 through § 2.8 are its realization and are authored nowhere yet.

- [ ] 2.1 Propose the codexFactory companion change enrolling a SECOND candidate
  class in `.github/merge-approval-envelope.yml`, citing this packet and #745.
  The file's own rule is that "Adding a second is not a configuration change: it
  is a new grant, needing its own word or its own council record" — resolve
  OQ-2 (word or council) before authoring, not after.
- [ ] 2.1a **THE LOAD-BEARING ACT, AND IT IS A CANON CHANGE.** Carry a
  `## MODIFIED Requirements` block on codexFactory
  `openspec/specs/merge-master-approval/spec.md` § *Bounded autonomous surface*,
  narrowing its CODEOWNERS-scoped prohibition to admit ONE NAMED machine-derived
  candidate class while leaving it absolute for every other candidate and every
  human author. **Without this the enrolment is void as declared**: the promoted
  requirement says "MUST NOT approve any pull request on a surface scoped to a
  human gate (a CODEOWNERS-scoped path)", and the lane's single writable path is
  code-owner scoped. Preserve every scenario the current requirement carries — a
  `## MODIFIED` requirement replaces the whole block, and the archive gate
  refuses a dropped scenario. Reconcile with the `## MODIFIED` block the active
  `add-regular-pr-council-clearance` already holds on the same requirement,
  whose proposal states the position being narrowed as "CODEOWNERS-scoped
  governance paths remain absolutely forbidden" — the two blocks must not
  disagree about what the requirement says.
- [ ] 2.1b Record in the companion's own design why narrowing the requirement is
  preferred to option (e) of decision N-1 — moving the machine-generated block
  off the code-owner-gated surface, which would satisfy the requirement as
  written instead of narrowing it — or, if (e) is preferred on reflection, file
  it as the successor and refuse the narrowing.
- [ ] 2.2 Declare the candidate with the N-2 members and no others:
  `target_repos: [opensoft/codexFactory]`; `expected_author: openxfactory[bot]`;
  `expected_head_ref: floor/bot-regeneration` in the EXACT form, not the pattern
  form; `expected_base_ref: main`; `require_same_repository: true`;
  `require_all_checks: true`; `check_exclusions: [merge-master-approval]`;
  `revert_suffices: true`.
- [ ] 2.3 Declare `path_allowlist` as exactly two named paths and NO glob:
  `scripts/merge_master/openxfactory-review-authority-floor.yaml` and
  `tests/merge-master/test_repository_gate_floor.py`. Re-measure both against the
  most recent `floor/bot-regeneration` pull requests before writing them; do not
  copy them from this packet, which measured them on 2026-09-07.
- [ ] 2.4 Record IN THE FILE, beside the candidate, that no diff-shape condition
  is declared because the envelope has none, and that the shape guarantees
  (additions-only, machine-generated-block-only, the LS-A3 mirror never
  narrowing) are supplied by the lane's own required checks which
  `require_all_checks: true` conjuncts in. Name those checks explicitly.
- [ ] 2.5 Record IN THE FILE why no `open_finding_title_prefixes` and no
  `open_finding_labels` are declared, on the ground the `intent-rolling-custody`
  candidate already records for itself — no finding class is ABOUT this derived
  tree, so a prefix would park the lane on unrelated repository-wide findings.
- [ ] 2.6 Extend `tests/merge-master/test_enrolled_surface_config.py` to assert
  the new exact shape — two candidates, these exact paths, this exact author and
  head ref, `require_all_checks: true` — so that widening the class fails a test
  as well as needing a code owner.
- [ ] 2.7 Arm auto-merge in `.github/workflows/floor-regeneration.yml` on the
  pull request the lane opens. **This is not optional and it is not implied by
  the enrolment**: the merge-master lane submits a review and merges nothing
  (`merge-master-approval.yml` "NO MERGE, EVER"), so without this step an
  approved bot pull request sits exactly as long as an unapproved one.
- [ ] 2.8 Extend the approval record the lane already posts to carry the measured
  changed path set, the floor-matched count and the check names quantified over
  (decision N-4). Do not add a second record surface.
- [ ] 2.9 ONLY UNDER A VETO OF N-1 TOWARD (b) — the whole of the wider scope, in
  one place so its cost is legible: (a) the codexFactory decision-core carve of
  N-1b(ii), naming the enrolled re-pin class and the exact floor member set
  `{contracts/review-lane-pin.yaml}` it may touch, with its own tests, and NOT a
  removal of the member from the floor; (b) an openxFactory re-pin candidate in
  `.github/merge-approval-envelope.yml` with its N-2 members measured off
  `bot/review-lane-repin` pull requests; (c) its shape assertion in
  `tests/review_lane_pin/test_review_lane_caller.py`; (d) auto-merge armed in
  `.github/workflows/review-lane-repin.yml`; (e) the openxFactory ruleset act of
  § 5.3; and (f) an advance of `contracts/review-lane-pin.yaml` to the core
  carrying the carve — which is itself a re-pin cycle, and is the reason (b) is
  not one act but a sequence.

## 3. First envelope-approved landing of each admitted kind

- [ ] 3.1 Observe ONE codexFactory `floor/bot-regeneration` pull request reach
  `decision == approve` from the pinned core, with the approval record naming the
  candidate class and the measured facts. Record the run URL and the pull request
  number.
- [ ] 3.2 Observe that same pull request MERGE with no human click — no review
  submitted by a person, no merge button pressed, no admin bypass exercised.
  Record the merge commit and the actor GitHub reports for the merge.
- [ ] 3.3 Observe a park on a candidate that should NOT be approved, and confirm
  it parks for the stated reason rather than by accident. A negative control that
  measures nothing proves nothing — construct it so the SAME inputs the shipped
  condition reads are the ones the control varies.
- [ ] 3.4 Confirm the openxFactory re-pin pull request of that same cycle still
  waits for a human word under the recommended scope, and that its
  merge-master-approval run reports the floor refusal rather than an envelope
  verdict — the property § 2.1 of `design.md` measured, observed live.
- [ ] 3.5 ONLY UNDER A VETO TOWARD (b): the same three observations for one
  openxFactory `bot/review-lane-repin` pull request.
- [ ] 3.6 Exercise the kill switch once, deliberately, on a scheduled cycle:
  remove the candidate entry, confirm the next bot pull request parks for a
  human, restore it, confirm approval resumes. A switch never thrown is a switch
  nobody knows works.

## 4. Archive evidence

- [ ] 4.1 `code_surface:` is not `none`, so per `release-realization` this packet
  archives only on merged and green realization evidence. Assemble it: the
  codexFactory companion merged and green; § 3.1, § 3.2 and § 3.3 observed with
  their run URLs; § 3.6 exercised.
- [ ] 4.2 Record the per-cycle human cost AFTER the change, measured the same way
  the before figure was measured — merges per advance of the pinned core, read
  from the API over at least three consecutive cycles — so the benefit claimed is
  a measurement and not an expectation.
- [ ] 4.3 Confirm no floor path was removed from
  `scripts/merge_master/openxfactory-review-authority-floor.yaml` by any act of
  this packet, and that `contracts/review-lane-pin.yaml` is still a declared
  never-clearable member. Under the recommended scope this is trivially true and
  the check is still run; under (b) it is the single most important thing to
  verify, because a carve that quietly became a removal is the failure this
  packet exists to prevent.
- [ ] 4.4 Archive through `proposal-support`, never bare `openspec`, and with no
  open box that is not an owner's-act note.

## 5. Owner's acts (not an agent's)

- [ ] 5.1 Ratify or refuse this packet. The 2026-09-07 ~02:05Z word authorized the
  PROPOSING, not the content.
  **2026-09-07 — TAKEN. Brett Heap ratified it in session at 2026-09-07T12:32:44Z,
  verbatim "ratify 746 and 272 as recommended when green, then land them" — a PAIR
  word over this packet and codexFactory #272 together, recorded on openxFactory
  #745 and applied at head `6ebd7b24`, all nine checks green and no open thread.
  The packet is now `Status: ratified` and the record is
  `review/ratification-2026-09-07.md`. The box is left UNTICKED deliberately —
  ticking an owner's-act box is a claim an agent may not make about the owner, and
  this dated note is how the act is recorded instead.**
- [ ] 5.2 Rule on N-1 (scope), N-1b (the carve, live only if N-1 goes to (b)),
  N-2 (admission conditions), N-3 (ordering), N-4 (observability and kill
  switch) and N-5 (realization surface). N-1 is the one that changes the shape of
  everything below it; the rest stand as recommended unless vetoed.
  **2026-09-07 — STOOD. Under the ratification word, N-1 through N-5 stand as
  recommended and no veto was exercised — N-1 admits the codexFactory
  REGENERATION lane only, so N-1b stays dormant and the openxFactory re-pin lane
  stays under a human merge word; (d) and (e) are recorded as not taken rather
  than foreclosed. OQ-2 is answered as recommended: the admitting act is a
  Gate-Rules Council record, and it has NOT been performed. Each remains one edit
  away. The box stays UNTICKED for the same reason 5.1's does.**
- [ ] 5.3 **THE ENABLING ACT, AND WITHOUT IT NOTHING HERE CHANGES ANYTHING.**
  Ruleset `Require Code Owner Review` is ACTIVE on both repositories with
  `require_code_owner_review=true`, and every path either bot lane writes is
  code-owner gated to a single human. A GitHub App cannot be named in CODEOWNERS,
  so the merge-master App's approval cannot clear that requirement. Decide the
  shape: (a) add the merge-master App as a bypass actor on that ruleset in the
  repository concerned — recommended, narrow, visible, reversible in one click,
  and it lifts only that ruleset for that App; (b) remove the paths from
  CODEOWNERS — this packet recommends refusing it, since it weakens the gate for
  every author and not just the bot; or (c) decline, in which case the honest
  outcome is N-1 (d) and this packet should be refused rather than realized into
  an enrolment that cannot land anything.
- [ ] 5.4 Answer OQ-1 (is the bypass shape acceptable at all), OQ-2 (word or
  Gate-Rules Council record for the second codexFactory candidate — **this packet
  recommends the COUNCIL**, because § 2.2a of `design.md` shows the act is not a
  grant inside the rules but a `## MODIFIED` to a promoted requirement canon calls
  absolutely forbidden, and `add-substantive-review-lane` task 3.2 is still open)
  and OQ-3 (lanes arm auto-merge, versus teaching the merge-master lane to merge —
  this packet recommends the former and proposes nothing about the latter).
- [ ] 5.5a Rule on option (e) of N-1 — satisfy `Bounded autonomous surface` as
  written by moving the machine-generated floor block off the code-owner-gated
  surface, instead of narrowing the requirement. It is the only option on the
  page that buys the click without weakening a governance ground, it is
  codexFactory's architecture to decide, and if N-1 is refused on § 2.2a grounds
  it is the successor to file.
- [ ] 5.5 Give the realization word, separately, after 5.1 and 5.2. Ratification
  performs no realization: it ratifies the PROPOSAL, and every act in groups 2
  through 4 waits on its own word.
