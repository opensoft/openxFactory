# Tasks: extend-merge-master-envelope-to-floor-bot-lanes

Status: ratified

**RATIFIED 2026-09-07** — Brett Heap, in session at 2026-09-07T12:32:44Z,
verbatim *"ratify 746 and 272 as recommended when green, then land them"*; record
`review/ratification-2026-09-07.md`. **THE RATIFICATION PERFORMED NOTHING IN
THIS FILE.** Decisions N-1 through N-5 stand as recommended, and at that commit
every box below — including group 1's, whose work is what produced the packet
that was ratified — was UNTICKED and stayed so. **PAST TENSE DELIBERATELY: the
realization word below is what moved them, and this paragraph describes the
state it superseded rather than the state of the file you are reading.**

**REALIZED 2026-09-07** — Brett Heap, in session at 2026-09-07T19:19Z, verbatim
*"tick 5.0 in the amendment, then realize 6.3"*, recorded on openxFactory #745
and codexFactory #232. THE LATER WORD GROUPS 2 THROUGH 4 WAITED ON HAS NOW BEEN
GIVEN. Group 1 is ticked with its evidence; group 2's boxes are ticked WHERE THE
codexFactory COMPANION HAS REALIZED THEM, each naming the codexFactory pull
request and the file, with § 2.7 left OPEN and its refusal reasoned; group 3 is
behavioural evidence that cannot exist until a real bot pull request runs
against the landed enrolment, so every box in it stays open; group 4 archives on
that evidence and stays open with it; group 5 is the owner's and an agent may
not tick an owner's-act box at all.

**THE PARAGRAPH THIS REPLACES SAID EVERY BOX WAS UNTICKED AND NONE MAY BE TICKED
BY THIS PACKET.** That was true of the proposal, which enrolled nothing. What is
still true, and is repeated because it is the thing a reader will get wrong:
**NOTHING IS AUTONOMOUSLY APPROVED YET.** The Gate-Rules Council record is
DRAFTED AND UNSIGNED, `Require Code Owner Review` still has no bypass actor in
either repository, and no bot pull request has been approved by an envelope. The
enrolment is real and inert, in that order. And the openxFactory RE-PIN LANE IS
NOT ENROLLED and stays under a human merge word — decision N-1 standing as
recommended, asserted in
`tests/review_lane_pin/test_floor_bot_lane_enrolment.py`.

**SUPERSEDED IN PART, 2026-09-10 — APPENDED, NOT A REWRITE.** The paragraph
above is the 2026-09-07 state and is kept as written. Three of its four clauses
no longer hold, and the fourth holds for a reason it did not name: the
Gate-Rules Council record is **SIGNED** (`review/gate-rules-council-admitting-record-2026-09-10.md`,
Brett Heap 2026-09-10, verdict ADMIT); **two bot pull requests HAVE been
approved by the envelope** and merged (codexFactory #314 -> `b08958ae`, #325 ->
`df42f803`, the second with no human act at all); and `Require Code Owner
Review` **still has no bypass actor in either repository AND needs none** — the
admitted artifact was relocated off every CODEOWNERS prefix, so the requirement
is vacuous over it. What is still true is the sentence's spirit for THIS
repository: **the openxFactory re-pin lane is not enrolled and still waits for a
human merge word.** The whole measurement is the ADDENDUM at the foot of this
file.

Groups 2 through 4 are written for the RECOMMENDED scope of decision N-1 —
the codexFactory regeneration lane alone. Where a veto to N-1 (b) would add work,
the addition is named in the task rather than left to be discovered, and § 2.9
carries the whole of the wider scope in one place.

## 1. Proposal

- [x] 1.1 Author `proposal.md` with `code_surface:` and `target_release:`
  front-matter, a `Status:` header inside the first fifteen real lines (`draft` at
  authoring; `ratified` since 2026-09-07, with the `Ratified:` citation beside
  it), the origin citation to openxFactory #745 and codexFactory #232, and the
  explicit statement that the authorizing word authorized the PROPOSING and not
  the content.
  **2026-09-07 — DONE.** Both front-matter keys, the `Status:` header inside the
  first fifteen real lines (`ratified`, with the `Ratified:` citation), and the
  origin citations to #745 and codexFactory #232 with the explicit statement
  that the word authorized the PROPOSING.
- [x] 1.2 Author `design.md` measuring, in the working tree and against the live
  API, WHERE the envelope is declared, WHAT it evaluates, and WHAT stands between
  each bot lane and an autonomous approval — every claim cited `file:line`, and
  any place the governing brief's premise and the tree disagree written down as
  the tree has it and flagged as a difference.
  **2026-09-07 — DONE, AND ITS CENTRAL FINDING WAS A CORRECTION**, which is what
  the box asked for: § 1.1 of `design.md` records that the governing brief's
  premise was wrong for this repository (the enrolled candidate is
  `intent-rolling-custody`, not `doc-health-nightly`), and § 2.2a records the
  larger one — that neither lane is a configuration change, because both need a
  `## MODIFIED` to a promoted requirement.
- [x] 1.3 State decisions N-1 through N-5 (and N-1b, which the measurement
  forced) each with a recommendation, its alternatives, and what a veto costs —
  so that every one of them is one edit away from being overruled.
  **2026-09-07 — DONE.** N-1, N-1b, N-2, N-3, N-4 and N-5 each carry a
  recommendation, its alternatives and the cost of a veto; all six stood as
  recommended under the ratification word.
- [x] 1.4 Author the spec deltas: `roles-authority-model` for the neutral
  enrolment rules, `review-lane-floor-mirror` for the two named lanes. Every
  requirement SHALL on line one; every requirement at least one
  `#### Scenario:`.
  **2026-09-07 — DONE.** `roles-authority-model` carries 5 requirements and 10
  scenarios, `review-lane-floor-mirror` 3 and 7 — counted by `grep -c` in
  `review/ratification-2026-09-07.md` and RE-COUNTED at realization by
  `tests/review_lane_pin/test_floor_bot_lane_enrolment.py::...::test_every_ratified_scenario_is_accounted_for`,
  which reads both deltas and refuses if the total is not 17.
- [x] 1.5 Author `.openspec.yaml` with the ad-hoc origin, the reason the staging
  queue was checked and found not to name this, and the authorizing word recorded
  as admission-to-queue rather than as ratification.
  **2026-09-07 — DONE.** The ad-hoc origin, the checked-and-empty staging
  search, and the authorizing word recorded as admission-to-queue.
- [x] 1.6 Enter the change in the README "OpenSpec Records" active block, and
  seed its per-change sweep ledger row through the sanctioned writer
  (`scripts/validate-sequenced-after.py --seed-ledger`) with `--moved-on` in UTC.
  **2026-09-07 — DONE.** Both landed with the proposal; the ledger row is intact
  at `moved_by: "#745"`, `moved_on: "2026-09-07"`, `depth: 2`.
- [x] 1.7 Validate at the PINNED CLI: `--change` strict clean, and `--all
  --strict` with the failure set unchanged against `main`, both recorded on the
  pull request.
  **2026-09-07 — DONE at proposal, and RE-RUN at realization.** The realization
  figures are in the realization pull request body, verbatim, with the `main`
  baseline beside them.

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

- [x] 2.1 Propose the codexFactory companion change enrolling a SECOND candidate
  class in `.github/merge-approval-envelope.yml`, citing this packet and #745.
  The file's own rule is that "Adding a second is not a configuration change: it
  is a new grant, needing its own word or its own council record" — resolve
  OQ-2 (word or council) before authoring, not after.
  **2026-09-07 — DONE by the companion.** codexFactory
  `.github/merge-approval-envelope.yml` declares
  `openxfactory-floor-regeneration`. OQ-2 was resolved BEFORE authoring, as the
  box demands: the instrument is a Gate-Rules Council record, and it is DRAFTED
  AND UNSIGNED at codexFactory
  `openspec/changes/extend-merge-master-envelope-to-floor-bot-lanes/review/gate-rules-council-admitting-record-DRAFT.md`.
  Merging that enrolment IS the admitting act.
- [x] 2.1a **THE LOAD-BEARING ACT, AND IT IS A CANON CHANGE.** Carry a
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
  **2026-09-07 — DONE at authoring, and it is what was ratified.** The
  `## MODIFIED` block carries canon's whole requirement with ONE clause narrowed
  and BOTH of canon's scenario titles preserved; one scenario is added. It
  reaches canon only at archive.
- [x] 2.1b Record in the companion's own design why narrowing the requirement is
  preferred to option (e) of decision N-1 — moving the machine-generated block
  off the code-owner-gated surface, which would satisfy the requirement as
  written instead of narrowing it — or, if (e) is preferred on reflection, file
  it as the successor and refuse the narrowing.
  **2026-09-07 — DONE.** codexFactory `design.md` § 4 records why the narrowing
  is preferred to option (e) and states expressly that (e) is not foreclosed and
  is the successor to file if the narrowing is refused.
- [x] 2.2 Declare the candidate with the N-2 members and no others:
  `target_repos: [opensoft/codexFactory]`; `expected_author: openxfactory[bot]`;
  `expected_head_ref: floor/bot-regeneration` in the EXACT form, not the pattern
  form; `expected_base_ref: main`; `require_same_repository: true`;
  `require_all_checks: true`; `check_exclusions: [merge-master-approval]`;
  `revert_suffices: true`.
  **2026-09-07 — DONE by the companion**, with every member exactly as N-2 fixes
  it and no other. It validates against codexFactory's schema AND its runtime
  mirror.
  **AND THE CLASS AS RATIFIED CANNOT YET APPROVE — MEASURED 2026-09-07, and it
  is the substantive finding of this realization.** `envelope.py:710-713`
  refuses any non-excluded check NAME whose latest completed run concluded other
  than `success`. `lane-line` concludes **`skipped`** on every
  `floor/bot-regeneration` pull request, by design rather than by accident:
  codexFactory `.github/workflows/lane-line.yml:15` guards the job with
  `if: github.event.pull_request.user.type != 'Bot'`, and GitHub reports a job
  skipped by an `if:` as a COMPLETED check-run concluding `skipped`. Measured on
  all four observed pull requests — codexFactory #248, #254, #265, #273 — and
  `skipped` on all four. So N-2's conditions, realized exactly as ratified,
  produce a class that PARKS every time with `check-run 'lane-line' concluded
  'skipped'`. That is precisely what § 4.1 of this file warns about: an
  enrolment declared but never observed to fire proves nothing.
  **IT IS RECORDED RATHER THAN QUIETLY FIXED, AND THE REASON IS AUTHORITY** —
  adding `lane-line` to `check_exclusions` changes a member N-2 fixes BY NAME,
  and a lane realizing a ratified packet does not widen a ratified admission
  condition on its own judgment. Three ways out, each needing Brett's word and
  each enumerated in codexFactory's envelope file beside `require_all_checks`:
  (a) exclude `lane-line` for this candidate — one line, defensible because the
  check is EXEMPT for this author rather than failing; (b) make the exemption
  conclude SUCCESS by moving the guard from a job-level `if:` to an in-job early
  exit; (c) treat `skipped` as green in the decision core — refused, it would
  relax the condition for every class in every repository that core judges.
  Measured executably by codexFactory
  `test_the_shipped_class_PARKS_on_the_real_observed_check_set`, which reds the
  day it is fixed, beside `test_the_finding_is_ABOUT_lane_line_and_nothing_else`,
  which proves no other observed check would also have parked it.
- [x] 2.3 Declare `path_allowlist` as exactly two named paths and NO glob:
  `scripts/merge_master/openxfactory-review-authority-floor.yaml` and
  `tests/merge-master/test_repository_gate_floor.py`. Re-measure both against the
  most recent `floor/bot-regeneration` pull requests before writing them; do not
  copy them from this packet, which measured them on 2026-09-07.
  **2026-09-07 — DONE by the companion, AND RE-MEASURED rather than copied**, as
  the box demands. All four observed pull requests were re-read from the API on
  2026-09-07 — codexFactory #248, #254, #265 and #273 — and every one reports
  author `openxfactory[bot]`, head `floor/bot-regeneration`, base `main`, not
  cross-repository, and exactly one changed file
  (`scripts/merge_master/openxfactory-review-authority-floor.yaml`). The second
  enumerated path is the LS-A3 mirror, which moves only on a membership change;
  both are compared against the lane's own `OWNED_FILES` by a test.
- [x] 2.4 Record IN THE FILE, beside the candidate, that no diff-shape condition
  is declared because the envelope has none, and that the shape guarantees
  (additions-only, machine-generated-block-only, the LS-A3 mirror never
  narrowing) are supplied by the lane's own required checks which
  `require_all_checks: true` conjuncts in. Name those checks explicitly.
  **2026-09-07 — DONE by the companion**, with the judges named explicitly:
  `pytest-suite` (the additions-only and confinement refusals, the
  landed-source-commit rule, the single-flight rule and the LS-A3 mirror) and
  `validate`, with `merge-master-approval` the one exclusion.
- [x] 2.5 Record IN THE FILE why no `open_finding_title_prefixes` and no
  `open_finding_labels` are declared, on the ground the `intent-rolling-custody`
  candidate already records for itself — no finding class is ABOUT this derived
  tree, so a prefix would park the lane on unrelated repository-wide findings.
  **2026-09-07 — DONE by the companion**, on the ground `intent-rolling-custody`
  records for itself.
- [x] 2.6 Extend `tests/merge-master/test_enrolled_surface_config.py` to assert
  the new exact shape — two candidates, these exact paths, this exact author and
  head ref, `require_all_checks: true` — so that widening the class fails a test
  as well as needing a code owner.
  **2026-09-07 — DONE by the companion.** Five equality assertions in
  `tests/merge-master/test_enrolled_surface_config.py`, including the
  enumeration test that PROVES the refused `scripts/merge_master/**` spelling
  would have admitted `envelope.py`. One pre-existing test was repaired and
  TIGHTENED in the same commit.
- [ ] 2.7 Arm auto-merge in `.github/workflows/floor-regeneration.yml` on the
  pull request the lane opens. **This is not optional and it is not implied by
  the enrolment**: the merge-master lane submits a review and merges nothing
  (`merge-master-approval.yml` "NO MERGE, EVER"), so without this step an
  approved bot pull request sits exactly as long as an unapproved one.
  **2026-09-07 — NOT PERFORMED, AND REFUSED RATHER THAN FORGOTTEN. IT
  CONTRADICTS A RATIFIED REQUIREMENT OF A SIBLING PACKET.** codexFactory
  `add-floor-regeneration-automation` § *An automated floor regeneration only
  ever proposes* (ADDED, ratified 2026-09-06, merge `ffc090d0`, still active)
  says the lane *"MUST NOT dispose of it: it SHALL NOT merge, SHALL NOT approve,
  SHALL NOT push to the floored document's repository default branch"*, and its
  scenario adds *"takes no further action on it"*. Arming auto-merge is disposal,
  and `codexFactory tests/merge-master/test_floor_regeneration.py::test_R1_S1_the_lane_opens_a_pull_request_and_stops_there`
  enforces it by sweeping the lane and its driver for ten disposal spellings.
  Neither half of this ratified pair carries authority to narrow that
  requirement — both ratification records measure the deltas by `grep -c` and
  neither includes it.
  **THE GAP IS RECORDED, WHICH IS EXACTLY WHAT THIS PACKET'S OWN RATIFIED
  REQUIREMENT ASKS FOR**: `specs/roles-authority-model/spec.md` § *An autonomous
  approval is not a merge* — *"the gap is recorded rather than discovered when
  the first candidate does not land"*. It is recorded beside the candidate entry
  in codexFactory's envelope, in codexFactory's task 2.7, in this note, and in
  `test_S_an_approved_candidate_has_no_merge_mechanism_and_the_gap_is_recorded`,
  which measures both halves and reds when the conflict is resolved.
  **THE EXACT NEXT STEP:** a successor packet in codexFactory carrying a
  `## MODIFIED` on that requirement, narrowing "MUST NOT dispose" to admit
  arming auto-merge on the lane's OWN pull request while leaving the merge,
  approve and default-branch bars intact; the same narrowing applied to
  `test_R1_S1`'s disposal set; then the arming step. It needs its own word.
  **Or, more cheaply, decision N-1 (e)** — moving the machine-generated block
  off the code-owner-gated surface — after which the ordinary gate merges it and
  no narrowing is needed at all.
  **2026-09-10 — THE SUCCESSOR EXISTS AND BOTH ROUTES WERE TAKEN; THIS BOX STAYS
  UNTICKED AND THE REFUSAL ABOVE STANDS AS WRITTEN.** The arming successor is
  codexFactory `amend-floor-regeneration-merge-authority` (ratified 2026-09-08,
  merge `93f0f0d7`), which narrowed the requirement to *"SHALL NOT merge BY ITS
  OWN ACT"* and admits the lane arming the platform's auto-merge on its own pull
  request; `.github/workflows/floor-regeneration.yml` now arms it, and this
  repository's lockstep mirror is `amend-mirror-floor-regeneration-merge-authority`
  (ratified 2026-09-08). **N-1 (e) was ALSO taken**, separately —
  codexFactory `relocate-review-authority-floor` (#293) with its mirror
  `relocate-review-authority-floor-mirror` (#817), landed at codexFactory
  `d1f8bf1b` 2026-09-09. **This packet performed neither**, which is why the box
  is not ticked: a box ticks on the act this packet took, not on a successor's.
- [x] 2.8 Extend the approval record the lane already posts to carry the measured
  changed path set, the floor-matched count and the check names quantified over
  (decision N-4). Do not add a second record surface.
  **2026-09-07 — DONE by the companion, WITH ONE DIFFERENCE FROM N-4 THAT IS
  RECORDED RATHER THAN GLOSSED.** N-4 cited `merge-master-approval.yml:1740`,
  `:1767-1799` — THIS repository's caller, which posts one sticky comment on
  approve and on park. codexFactory's caller posts an approving REVIEW on
  approve and a sticky comment only on park, so "the record the lane already
  posts" is TWO records there and both were extended. No second surface was
  added. The floor-matched count is rendered as NOT COMPOSED rather than as `0`,
  because codexFactory composes no floor over its envelope (design § 2.3,
  re-grepped) and a `0` would assert a measurement nobody took.
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
  **2026-09-07 — NOT LIVE AND NOT PERFORMED.** N-1 stood as recommended, so
  there is no veto toward (b): no decision-core carve was authored, no
  openxFactory candidate class was declared, no auto-merge was armed in
  `review-lane-repin.yml`, no ruleset changed, and the pin was not advanced for
  a carve. Asserted rather than promised —
  `tests/review_lane_pin/test_floor_bot_lane_enrolment.py` reads the envelope
  and requires its candidate list to be exactly `['intent-rolling-custody']`,
  and reads the caller's floor refusal and requires it to name no candidate.

### ADDENDUM 2026-09-08 — finding (1) of § 2.2 RULED (a), realized in codexFactory

**APPENDED, NOT A REWRITE.** Everything above stands as written on 2026-09-07,
including § 2.2's finding in its original tense; it is the measurement the
ruling was given on. No box is ticked or un-ticked by this addendum, and no
mechanism in THIS repository changes.

**THE RULING. Brett Heap, 2026-09-08T03:23:15Z, verbatim:**

> rule (a) on finding 1, this lane realizes it

Recorded at `opensoft/openxFactory#745` (comment 5578623009) and
`opensoft/codexFactory#232` (comment 5578622812). Option **(a)** of the three
§ 2.2 enumerates: exclude `lane-line` for the `openxfactory-floor-regeneration`
candidate, because the check is EXEMPT for its single Bot author rather than
failing. Options (b) and (c) are NOT taken.

**REALIZED IN THE COMPANION, WHERE DECISION N-5 PUTS THE CODE:**
`opensoft/codexFactory#286`, by lane `openxfactory-2` (`openXfactory-2`).
codexFactory's `.github/merge-approval-envelope.yml` now declares
`check_exclusions: [merge-master-approval, lane-line]` on that candidate and on
no other; the executable measurement § 2.2 names is FLIPPED DELIBERATELY, as
that test's own docstring promised it would be, and is now
`test_the_shipped_class_approves_on_the_real_observed_check_set` — **the
fixture is unedited**, `lane-line` is still `skipped` in it, so the fix is
proven against the facts that proved the defect. The codexFactory behaviour
snapshot did NOT move
(`09a81fbbf94409dd868260e90ee291dd900c242c683d77594e8c4898d609731d`), so the
class stays PERMANENTLY ADVISORY.

**NOTHING IS OWED IN THIS REPOSITORY, AND THAT IS MEASURED RATHER THAN
ASSUMED.** `tests/review_lane_pin/test_floor_bot_lane_enrolment.py` binds
`ENVELOPE = ROOT / ".github" / "merge-approval-envelope.yml"` — **openxFactory's
OWN envelope, not codexFactory's**. It neither fetches nor vendors the
companion's config; its module docstring states the property outright ("needs no
network and needs no codexFactory checkout"), and its single `check_exclusions`
assertion is `assertNotIn("pytest-suite", ...)` over THIS repository's
candidates, whose list § 2.9 pins to exactly `['intent-rolling-custody']`. The
mirror therefore cannot observe the companion's exclusion list at any state —
before the companion lands, after it lands, or at the next re-pin — so there is
no assertion to update and no window in which one would go red. Confirmed green
unchanged: `python3 -m pytest tests/review_lane_pin -q`.

**ONE STALE REFERENCE IS NAMED RATHER THAN EDITED.** § 2.2 above cites
codexFactory `test_the_shipped_class_PARKS_on_the_real_observed_check_set` by
its old name; that test is the one the companion flipped, and it is now
`test_the_shipped_class_approves_on_the_real_observed_check_set` in the same
module. The line above is left as written because it is the 2026-09-07 record.

**WHAT THIS DOES NOT DISCHARGE.** The codexFactory lane still arms no
auto-merge, so an approved bot pull request there still waits for a human merge;
the Gate-Rules Council admitting record stays a DRAFT and UNSIGNED; the
`Require Code Owner Review` bypass actor is untaken. Of the three obstacles
§ 3.1 names, this discharges the third and only the third.

## 3. First envelope-approved landing of each admitted kind

- [ ] 3.1 Observe ONE codexFactory `floor/bot-regeneration` pull request reach
  `decision == approve` from the pinned core, with the approval record naming the
  candidate class and the measured facts. Record the run URL and the pull request
  number.
  **2026-09-07 — OPEN, AND IT CANNOT BE OBSERVED YET. THREE THINGS STAND IN THE
  WAY AND ALL THREE ARE NAMED:** (1) the Gate-Rules Council admitting record is
  DRAFTED AND UNSIGNED, so the enrolment has not lawfully landed; (2) `Require
  Code Owner Review` has no bypass actor on codexFactory, so an approval clears
  nothing (§ 5.3); (3) even with both taken, the class PARKS on `lane-line`
  concluding `skipped` for a Bot author (see § 2.2). This box needs a real bot
  pull request approved by the envelope AFTER all three are resolved, and no
  earlier. § 3.2's unattended merge additionally waits on § 2.7.
  **2026-09-10 — THE THREE OBSTACLES ARE GONE AND THE APPROVAL IS OBSERVED, BUT
  THE BOX STAYS OPEN ON ONE CLAUSE OF ITS OWN TEXT.** Observed twice:
  codexFactory [#314](https://github.com/codeXfactory/codexFactory/pull/314)
  (review 5160667178, `codexfactory[bot]` APPROVED 2026-09-09T22:49:36Z) and
  [#325](https://github.com/codeXfactory/codexFactory/pull/325) (review
  5161853361, APPROVED 2026-09-10T01:54:56Z, `commit_id` = head `c4e40f33`;
  merge-master runs
  [34425922954](https://github.com/codeXfactory/codexFactory/actions/runs/34425922954)
  and
  [34427337240](https://github.com/codeXfactory/codexFactory/actions/runs/34427337240)).
  **THE ORDER, SAID OUT LOUD SO NO READER HAS TO INFER IT: BOTH APPROVALS
  PREDATE THE SIGNATURE.** The approvals above are 2026-09-09T22:49:36Z and
  2026-09-10T01:54:56Z; the signature is Brett Heap's word of 2026-09-10
  ~17:2xZ; and the enrolment that made the approvals possible merged earlier
  still, at codexFactory `4c0053c3` on 2026-09-07T21:16:37Z. **The signature
  therefore RATIFIES APPROVALS ALREADY GIVEN — it did not authorize them in
  advance**, and nothing in this note should be read as putting the signing
  before the approving. The council record states the same inversion at its
  § 0.2 rather than smoothing it.
  The obstacles: (1) the council record is now SIGNED
  (`review/gate-rules-council-admitting-record-2026-09-10.md`) — signed AFTER
  these approvals, per the paragraph immediately above; (2) the bypass
  actor was never needed — the relocation took the artifact off every CODEOWNERS
  prefix (record § 3.2, § 4); (3) the `lane-line` park was ruled (a) and realized
  2026-09-08. **WHAT IS NOT SATISFIED:** this box requires the approval "with the
  approval record NAMING the candidate class", and both approval records render
  `Candidate class: unrecorded` — the class id is populated on the PARK path and
  not on the APPROVE path. That is a defect against this packet's own ratified
  `review-lane-floor-mirror` § *An autonomous approval of a floor bot lane
  records the facts it measured*; it is codexFactory's surface, it is recorded at
  § 3.5 (a) of the council record, and this box stays OPEN on it and on nothing
  else.
- [x] 3.2 Observe that same pull request MERGE with no human click — no review
  submitted by a person, no merge button pressed, no admin bypass exercised.
  Record the merge commit and the actor GitHub reports for the merge.
  **2026-09-10 — OBSERVED, AND EVERY CLAUSE OF THIS BOX IS SATISFIED ON ONE PULL
  REQUEST.** codexFactory
  [#325](https://github.com/codeXfactory/codexFactory/pull/325), head
  `c4e40f33a941c0d67f35c7d3008029f1a8d815b3`: opened 2026-09-10T01:32:58Z,
  **merge commit `df42f8033a2dee3fd6f49d435912e7f30eac24ec`**, merged
  2026-09-10T01:55:14Z, and the **actor GitHub reports for the merge is
  `openxfactory[bot]`** — the platform completing the auto-merge the lane armed,
  not a person. **22 minutes 16 seconds open to merge.** No review was submitted
  by a person: the only review on the pull request is 5161853361,
  `codexfactory[bot]`, APPROVED. No merge button was pressed and no admin bypass
  was exercised — both approval-bearing org rulesets' bypass lists are
  `OrganizationAdmin / always` and nothing else, and no organization admin acted
  on this pull request.
  **THE WHOLE TIMELINE IS READ OUT, BECAUSE "NO HUMAN CLICK" IS A CLAIM ABOUT AN
  ABSENCE AND AN ABSENCE IS ONLY PROVEN BY ENUMERATING WHAT IS THERE.** Every
  event on #325 between opening and merge, from the timeline API: `committed`;
  `auto_merge_enabled` by **`openxfactory[bot]`** at 01:33:02Z; `commented` by
  `github-actions[bot]` at 01:33:22Z; `commented` by `sonarqubecloud[bot]` at
  01:54:32Z; `reviewed` (5161853361, `codexfactory[bot]`, APPROVED, 01:54:56Z);
  `merged` and `closed` by **`openxfactory[bot]`** at 01:55:14Z. **Four actors,
  every one of them a Bot, and no human login appears anywhere in that window.**
  The one human login on the pull request at all is `brettheap`, whose earliest
  event is 02:13:57Z — **eighteen minutes AFTER the merge** — and every one of
  his is `referenced` or `cross-referenced`, the side effect of linking the pull
  request from elsewhere rather than an act upon it.
  **AND THAT SAME TIMELINE SETTLES THIS BOX'S ONE STATED PRECONDITION.** § 3.1's
  2026-09-07 note says *"§ 3.2's unattended merge additionally waits on § 2.7"*,
  and § 2.7 is UNTICKED — so the dependency is answered rather than passed over:
  what § 2.7 asks for is that auto-merge BE ARMED, and it was, by
  `openxfactory[bot]` four seconds after the pull request opened, under the
  successor `amend-floor-regeneration-merge-authority` named in § 2.7's own
  2026-09-10 note. The arming is a fact about the world; § 2.7's box is a claim
  about what THIS packet performed, and it performed none of it. **The box stays
  unticked because the act was a successor's, not because the arming is absent**
  — and this box's observation was possible precisely because the arming is not.
  It is the same pull request § 3.1 observes reaching `approve`; § 3.1 stays open
  only on its class-naming clause, which says nothing about the merge. Recorded
  on openxFactory #745 (comment 5611865800) and codexFactory #232.
- [ ] 3.3 Observe a park on a candidate that should NOT be approved, and confirm
  it parks for the stated reason rather than by accident. A negative control that
  measures nothing proves nothing — construct it so the SAME inputs the shipped
  condition reads are the ones the control varies.
  **2026-09-10 — TWO REAL PARKS ARE NOW ON THE RECORD AND NEITHER IS THIS BOX'S
  CONTROL, WHICH IS WHY IT STAYS OPEN.** (i) codexFactory
  [#302](https://github.com/codeXfactory/codexFactory/pull/302) parked with
  `gate_integrity_path: changed path(s) inside the never-clearable class:
  ['tests/merge-master/test_repository_gate_floor.py']`, outcome
  `parked_never_clearable`, and was closed by hand — but that is a park of a pull
  request whose paths this class EXPLICITLY ADMITS, refused by codexFactory's
  tier-2 never-clearable class before the tier-1 envelope is reached, so it is a
  finding about the class's real reach (council record § 3.5 (b)) rather than a
  control over a candidate that should not be approved. (ii) #325's FIRST
  evaluation, before its checks completed, parked with *"no per-repo gate rule
  declares applies_to.candidate_id for surface 'openxfactory-floor-regeneration';
  tier-1 evaluation alone"* — a real fail-closed park of the admitted class, but
  its rendered reason names the tier-2 fall-through rather than the tier-1
  condition that was actually unmet, so it does not confirm a park "for the
  stated reason". **The box asks for a CONSTRUCTED control and neither of these
  was constructed.** Both are recorded so the next author starts from evidence.
- [ ] 3.4 Confirm the openxFactory re-pin pull request of that same cycle still
  waits for a human word under the recommended scope, and that its
  merge-master-approval run reports the floor refusal rather than an envelope
  verdict — the property § 2.1 of `design.md` measured, observed live.
  **2026-09-10 — THE FIRST HALF IS CONFIRMED; THE SECOND HAS NO ARTIFACT IN THAT
  CYCLE, SO THE BOX STAYS OPEN.** The re-pin lane's last pull request is
  openxFactory [#764](https://github.com/opensoft/openxFactory/pull/764) (head
  `bot/review-lane-repin`, author `openxfactory[bot]`), and it was **merged by
  `brettheap` — a human — at 2026-09-07T16:52:54Z**, merge `8d92bfaf`. That is the
  human word the recommended scope leaves in place, measured rather than assumed.
  **But no `bot/review-lane-repin` pull request has been opened since**, so the
  2026-09-09/10 cycles have no re-pin artifact of "that same cycle" to read a
  merge-master-approval run off. The floor refusal itself is asserted in code
  (`tests/review_lane_pin/test_floor_bot_lane_enrolment.py`), not observed live,
  which is exactly the distinction this box exists to close.
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
  **2026-09-10 — TWO CYCLES MEASURED, NOT THREE, SO THE BOX STAYS OPEN AND THE
  FIGURE SO FAR IS RECORDED RATHER THAN ROUNDED UP.** Read from the API:
  codexFactory #314 -> `b08958ae` (2026-09-09T23:27:22Z; merged by
  `openxfactory[bot]`, one hand dispatch of the approval leg) and #325 ->
  `df42f803` (2026-09-10T01:55:14Z; merged by `openxfactory[bot]`, **no human act
  at all**). The BEFORE figure was two human merges per advance of the pinned
  core, one per repository; on #325's cycle the AFTER figure is **one** —
  openxFactory's re-pin half only, and that half is measured at § 3.4. A third
  consecutive cycle is what this box's own text requires before the benefit is a
  measurement, and codexFactory #302 is not it: it parked and was closed rather
  than merged (§ 3.3).
- [x] 4.3 Confirm no floor path was removed from
  `scripts/merge_master/openxfactory-review-authority-floor.yaml` by any act of
  this packet, and that `contracts/review-lane-pin.yaml` is still a declared
  never-clearable member. Under the recommended scope this is trivially true and
  the check is still run; under (b) it is the single most important thing to
  verify, because a carve that quietly became a removal is the failure this
  packet exists to prevent.
  **2026-09-07 — CONFIRMED, AND ASSERTED IN CODE RATHER THAN CHECKED ONCE.**
  Trivially true under the recommended scope, and run anyway. codexFactory
  `scripts/merge_master/openxfactory-review-authority-floor.yaml` is untouched
  by every commit of this realization (`git diff` against `main` names it
  nowhere), and `contracts/review-lane-pin.yaml` is still a declared
  never-clearable member — read from this repository's vendored copy,
  `contracts/review-lane-floor-snapshot.yaml:112`. Both halves are standing
  assertions now:
  `tests/review_lane_pin/test_floor_bot_lane_enrolment.py::TheFloorIsComposedOverTheEnvelope::test_a_ruled_carve_for_one_candidate`
  requires the member to remain declared AND the caller's floor refusal to name
  no candidate and admit no exception, and codexFactory's
  `test_S_a_ruled_carve_for_one_candidate_was_not_taken` requires the same of
  the floor document itself.
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
- [x] 5.3 **THE ENABLING ACT, AND WITHOUT IT NOTHING HERE CHANGES ANYTHING.**
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
  **2026-09-07 — NOT PERFORMED, AND AN AGENT MAY NOT PERFORM IT. WHAT BRETT MUST
  CHANGE, EXACTLY, AND IN WHICH REPOSITORY:** under the recommended scope only
  **`opensoft/codexFactory`** needs the act — on ruleset **`Require Code Owner
  Review`, id `18834180`**, add the merge-master GitHub App as a BYPASS ACTOR
  (Settings -> Rules -> Rulesets -> that ruleset -> Bypass list -> Add -> Apps ->
  the merge-master App; bypass mode `Always`). Change nothing else:
  `require_code_owner_review` stays `true` and no path leaves `.github/CODEOWNERS`.
  **openxFactory's identically named ruleset (same id) needs NOTHING**, because
  N-1 does not admit the re-pin lane; its act is § 2.9(e) and § 2.9 is not live.
  **UNTIL THE codexFactory ACT IS TAKEN THE ENROLMENT LANDS NOTHING**, which is
  stated in the envelope file beside the candidate. The box stays UNTICKED.
  **2026-09-10 — THE ACT WAS NEVER PERFORMED AND IS NOW MOOT: IT WAS NOT NEEDED.
  THE ENROLMENT LANDED SOMETHING ANYWAY, TWICE.** Shape (b) of this box —
  "remove the paths from CODEOWNERS", which the packet recommended REFUSING — was
  not taken either. What was taken is decision **N-1 (e)**, which the packet
  recorded as not foreclosed: codexFactory `relocate-review-authority-floor`
  (#293) with its mirror `relocate-review-authority-floor-mirror` (#817) moved the
  artifact from `scripts/merge_master/openxfactory-review-authority-floor.yaml` to
  **`floor/openxfactory-review-authority-floor.yaml`** (codexFactory `d1f8bf1b`,
  2026-09-09), and codexFactory `.github/CODEOWNERS` carries **no `/floor/`
  entry** — so `require_code_owner_review` is vacuous over the admitted path and
  no bypass actor is needed to clear it. **THE ids IN THIS BOX ARE ALSO STALE:**
  `18834180` was the `opensoft` org's; after the repository's move the active org
  rulesets are `Require Code Owner Review` **22655341**
  (`require_code_owner_review: true`, `required_approving_review_count: 0`) and
  `xFactory Tier-1 main protection (require PR + 1 approval)` **22655338**
  (`required_approving_review_count: 1`, `require_code_owner_review: false`) —
  and it is 22655338 that the merge-master App's APPROVE review satisfied. Both
  bypass lists remain `OrganizationAdmin / always` and nothing else; **no ruleset
  was changed by anyone.** Evidence: council record
  `review/gate-rules-council-admitting-record-2026-09-10.md` § 3.2, § 4, R-3.
  **THE BOX STAYS UNTICKED** for the reason 5.1's and 5.2's do — ticking an
  owner's-act box is a claim an agent may not make about the owner — and this
  dated note is how the act is recorded instead.
  **2026-09-10 — TICKED on Brett Heap's word, verbatim "tick 5.3 and 5.4"
  (2026-09-10, in session to lane openxfactory-2; his act, the lane's pen;
  recorded on openxFactory #745
  https://github.com/opensoft/openxFactory/issues/745#issuecomment-5625582236).
  Discharged as the signed record states (§ 4, R-3, § 8 item 5): the enabling
  act was never performed and was never needed — the relocation of the
  admitted artifact off every CODEOWNERS-scoped path made `Require Code Owner
  Review` vacuous over it, and the App's approval was satisfied instead by
  ruleset 22655338, not the code-owner-review ruleset this box named; the
  stale `opensoft`-org ruleset id `18834180` this box's 2026-09-07 note cites
  is corrected in the record to the `codeXfactory`-org ids 22655341/22655338.
  Ticked by PR #927.**
- [x] 5.4 Answer OQ-1 (is the bypass shape acceptable at all), OQ-2 (word or
  Gate-Rules Council record for the second codexFactory candidate — **this packet
  recommends the COUNCIL**, because § 2.2a of `design.md` shows the act is not a
  grant inside the rules but a `## MODIFIED` to a promoted requirement canon calls
  absolutely forbidden, and `add-substantive-review-lane` task 3.2 is still open)
  and OQ-3 (lanes arm auto-merge, versus teaching the merge-master lane to merge —
  this packet recommends the former and proposes nothing about the latter).
  **2026-09-07 — OQ-2 ANSWERED AS RECOMMENDED (the council), AND THE RECORD IS
  NOW DRAFTED AND UNSIGNED** at codexFactory
  `openspec/changes/extend-merge-master-envelope-to-floor-bot-lanes/review/gate-rules-council-admitting-record-DRAFT.md`;
  no council has convened. **OQ-3 IS ANSWERED BY THE TREE RATHER THAN BY A
  RULING, AND THE ANSWER IS NEITHER OPTION.** The packet recommended "the lanes
  arm auto-merge on their own side"; the regeneration lane MAY NOT, because
  `add-floor-regeneration-automation`'s ratified requirement forbids it (see
  § 2.7). So the live answer is that the pull request waits for a human merge,
  and a real ruling on OQ-3 is now owed alongside the successor § 2.7 names.
  **OQ-1 IS UNANSWERED** and is § 5.3's. The box stays UNTICKED.
  **2026-09-10 — OQ-2's INSTRUMENT IS NOW SIGNED, AND OQ-3 IS ANSWERED BY A
  SUCCESSOR.** The Gate-Rules Council admitting record is reconciled against the
  live tree and **SIGNED, verdict ADMIT**, at
  `review/gate-rules-council-admitting-record-2026-09-10.md` — Brett Heap,
  2026-09-10, in session to lane `openxfactory-2`, verbatim *"do 1 and 2, sign,
  file it, do 744"*, recorded on openxFactory
  [#745](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5622848416)
  (comment 5622848416, item 3). **HIS ACT, THE LANE'S PEN.** It is a direct
  convener disposition — **no seat was run** — on the precedent of codexFactory
  `records/2026-09-04-gate-rules-packaged-contract-floor-widening.md` § 0, and it
  **ratifies an act already taken**: the enrolment merged at codexFactory
  `4c0053c3` on 2026-09-07, before the record was signed, which the record states
  at its § 0.2 rather than smoothing. **OQ-3** ("lanes arm auto-merge, versus
  teaching the merge-master lane to merge") is answered by the FORMER, through
  the successor `amend-floor-regeneration-merge-authority` and its mirror, not by
  this packet — see the 2026-09-10 note under § 2.7. **OQ-1 is moot**: the bypass
  shape was never exercised (§ 5.3). **The box stays UNTICKED** for the reason
  5.1's does.
  **2026-09-10 — TICKED on Brett Heap's word, verbatim "tick 5.3 and 5.4"
  (2026-09-10, in session to lane openxfactory-2; his act, the lane's pen;
  recorded on openxFactory #745
  https://github.com/opensoft/openxFactory/issues/745#issuecomment-5625582236).
  Discharged as the signed record states (§ 5.1, § 8 item 5): OQ-2's
  instrument, the Gate-Rules Council record, is now SIGNED with verdict ADMIT
  at `review/gate-rules-council-admitting-record-2026-09-10.md`; OQ-3 (lanes
  arm auto-merge versus teaching merge-master to merge) is answered by the
  former, through the successor `amend-floor-regeneration-merge-authority`;
  OQ-1 (is the bypass shape acceptable) is moot because no bypass shape was
  ever exercised (§ 5.3). Ticked by PR #927.**
- [ ] 5.5a Rule on option (e) of N-1 — satisfy `Bounded autonomous surface` as
  written by moving the machine-generated floor block off the code-owner-gated
  surface, instead of narrowing the requirement. It is the only option on the
  page that buys the click without weakening a governance ground, it is
  codexFactory's architecture to decide, and if N-1 is refused on § 2.2a grounds
  it is the successor to file.
- [ ] 5.5 Give the realization word, separately, after 5.1 and 5.2. Ratification
  performs no realization: it ratifies the PROPOSAL, and every act in groups 2
  through 4 waits on its own word.
  **2026-09-07 — GIVEN. Brett Heap, in session at 2026-09-07T19:19Z, verbatim
  *"tick 5.0 in the amendment, then realize 6.3"*, recorded on openxFactory #745
  and codexFactory #232.** It is the word groups 2 through 4 waited on and it is
  what the ticks above rest on. It did NOT give § 5.3's ruleset act or the
  Gate-Rules Council record OQ-2 names, both of which remain the owner's and
  remain untaken. The box stays UNTICKED for the same reason 5.1's does.

## ADDENDUM 2026-09-10 — the live cycles, the SIGNED council record, and the boxes they move

**APPENDED, NOT A REWRITE.** Everything above stands as written on its own date,
including the 2026-09-07 tenses and the 2026-09-08 addendum; where a clause of
the header paragraph no longer holds, the dated supersession note beneath it
says so and the original text is kept. **No box is un-ticked by this addendum.
ONE box is ticked — § 3.2 — and every other box it touches is left open with the
clause of its own text that is not yet met named out loud.**

**THE WORD.** Brett Heap, 2026-09-10 ~17:2xZ, in session to lane
`openxfactory-2` (display `openXfactory-2`), verbatim **"do 1 and 2, sign, file
it, do 744"**, recorded on openxFactory
[#745](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5622848416)
(comment 5622848416). Item 3 of that comment is this work: *"§ 6.3 Gate-Rules
Council record in `extend-merge-master-envelope-to-floor-bot-lanes` — reconcile
box 4.2 against the live tree … then SIGN on his word 'sign'; the record's own
form governs how the signature is written."*

**THE RECORD.** `review/gate-rules-council-admitting-record-2026-09-10.md` —
`Status: record`, verdict **ADMIT**, signed by Brett Heap, a **direct convener
disposition with no seat run**, reconciling the DRAFT at codexFactory
`openspec/changes/extend-merge-master-envelope-to-floor-bot-lanes/review/gate-rules-council-admitting-record-DRAFT.md`
in **eight** named places (its § 7). The two the estate most needs:

1. **NO GOVERNANCE GROUND WAS SPENT.** The draft priced the admission at one —
   narrowing codexFactory's promoted `Bounded autonomous surface`. Decision
   **N-1 (e)** was taken instead: `relocate-review-authority-floor` (#293) and
   its mirror `relocate-review-authority-floor-mirror` (#817) moved the artifact
   to `floor/openxfactory-review-authority-floor.yaml` (codexFactory `d1f8bf1b`,
   2026-09-09), codexFactory `.github/CODEOWNERS` has **no `/floor/` entry**, and
   the promoted requirement is **unnarrowed on `main`** — so the live approvals
   are lawful under canon **as written**.
2. **THE SIGNATURE RATIFIES AN ACT ALREADY TAKEN.** The enrolment merged at
   codexFactory `4c0053c3` on 2026-09-07T21:16:37Z, before the record was signed,
   against the envelope file's own instruction that the merge "must not happen
   before that record is signed". The record says so at its § 0.2.

**THE BOXES, AND WHY EACH MOVED OR DID NOT.**

| Box | State | The clause that decided it |
|---|---|---|
| § 2.7 arm auto-merge | OPEN | this packet performed nothing; the successor `amend-floor-regeneration-merge-authority` (merge `93f0f0d7`) did, and is now named beneath the box |
| § 3.1 approval observed | OPEN | approve observed twice, but the approval record renders `Candidate class: unrecorded` — the box requires it to NAME the class |
| § 3.2 unattended merge | **TICKED** | #325 -> `df42f803`, merged by `openxfactory[bot]` 22 min 16 s after opening; no person reviewed, no button, no admin bypass |
| § 3.3 negative control | OPEN | two real parks recorded (#302's `gate_integrity_path`; #325's pre-greenness tier-2 fall-through) and neither is the CONSTRUCTED control the box asks for |
| § 3.4 re-pin still human | OPEN | #764 merged by `brettheap` confirms the human word, but no re-pin pull request exists in the 2026-09-09/10 cycles to read a run off |
| § 3.6 kill switch | OPEN | never thrown |
| § 4.1 archive evidence | OPEN | 3.1, 3.3 and 3.6 are open, so the set is not assembled |
| § 4.2 human cost after | OPEN | **two** consecutive cycles measured; the box requires **three** |
| § 5.3 enabling act | UNTICKED, DISCHARGED | never performed, and NOT NEEDED — the relocation made `require_code_owner_review` vacuous over the admitted path; ruleset ids corrected |
| § 5.4 OQ-2 instrument | UNTICKED, DISCHARGED | the council record is signed; OQ-3 answered by a successor; OQ-1 moot |

**TWO OWNER'S-ACT BOXES ARE DISCHARGED AND AN AGENT MAY NOT TICK THEM.** § 5.3
and § 5.4 are both satisfied on the evidence above, and this file's own rule —
stated at its head and honoured at 5.1, 5.2 and 5.5 — is that *"an agent may not
tick an owner's-act box at all"*, because ticking one is a claim an agent may not
make about the owner. **The ask, in one line: "tick 5.3 and 5.4".** Until that
word the dated notes beneath them carry the acts.

**TWO DEFECTS WERE FOUND BY RUNNING, NOT BY READING**, and both are codexFactory's
surface and are carried at § 8 of the record rather than fixed here: the approval
record's `Candidate class: unrecorded` (§ 3.1 above), and the fact that a cycle
in which floored membership changes still parks, because the class's SECOND
enumerated path sits inside codexFactory's tier-2 never-clearable class — so the
autonomy this class actually holds is over ONE of its two admitted paths
(codexFactory #302, closed by hand).

**WHAT IS OWED IN codexFactory, named rather than performed** (this lane holds no
write authority there): mirror the signed record into
`hermes/domain/review-councils/records/`, supersede the DRAFT, repair the
`unrecorded` rendering, and rule on the second enumerated path. Record § 8.

**2026-09-10 ~22:1xZ — SUPERSEDING STATUS (PR #927).** The addendum above
predates Brett Heap's word "tick 5.3 and 5.4" (2026-09-10 ~21:15Z, in session
to lane openxfactory-2; recorded on openxFactory #745
https://github.com/opensoft/openxFactory/issues/745#issuecomment-5625582236).
Boxes 5.3 and 5.4 are now TICKED on that word by this PR; the addendum's table
entries above ("UNTICKED, DISCHARGED") and its closing line ("Until that word
the dated notes beneath them carry the acts") read as history, not current
state. **The checklist state after PR #927:** ticked 1.1 through 1.7, 2.1,
2.1a, 2.1b, 2.2 through 2.6, 2.8, 3.2, 4.3, 5.3, 5.4; open by their own text
2.7, 2.9, 3.1, 3.3, 3.4, 3.5, 3.6, 4.1, 4.2; owner's-act boxes 5.1, 5.2, 5.5a
and 5.5 carry dated notes and stay untaken. **The packet is NOT archived** —
§ 4.4 (archive through `proposal-support`) is separately open by its own text
and this PR does not touch it.
