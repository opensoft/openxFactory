# Tasks

**NO REALIZATION IS STARTED BY THE AUTHORING OF THIS PACKET, AND NO BOX IS
TICKED BY IT.** This is a PROPOSAL: groups 2 through 5 are realization work and
begin only after ratification. **Group 1 is the exception and is deliberate** —
it lists the PROPOSAL's own acts, the ones this packet performs, and its boxes
are still unticked, because authoring a proposal is not discharging it and a box
that moved on authorship would be a false completion the moment a ratification
did not follow. Group 6 is the owner's, and its boxes stay unticked even once
taken: an agent may not tick an owner's-act box, so those acts are recorded as
dated notes beneath them instead.

**2026-09-06 — THE PARAGRAPH ABOVE IS THE RECORD OF THIS FILE AT AUTHORING AND
IS KEPT UNCHANGED; what follows is its state now.** The packet was RATIFIED
(Brett Heap, "ratify both when green, then land them"), and the realization has
been performed and is proposed at openxFactory PR
[#715](https://github.com/opensoft/openxFactory/pull/715). Group 1's boxes are
therefore ticked: the condition the paragraph named — *"the moment a
ratification did not follow"* — did not occur, so they are no longer false
completions. Groups 3 and 4 are ticked with their evidence. **Group 5 stays
entirely unticked and Group 6 stays unticked by rule**; each says why in its own
place, and NOTHING IS ARCHIVED — `release-realization` archives a code surface
only on merged plus green realization evidence, and this packet's own
`target_release:` names ONE COMPLETE CYCLE OBSERVED UNATTENDED as that
evidence.

**2026-09-06, LATER THE SAME DAY — THE TWO PARAGRAPHS ABOVE ARE KEPT UNCHANGED
AND ARE STILL THE RECORD; what follows is the state now.** The realization
LANDED (PR [#715](https://github.com/opensoft/openxFactory/pull/715), squash
`1897f282`), a defect the first cycle then found in it was repaired (PR
[#726](https://github.com/opensoft/openxFactory/pull/726), squash `0f9361e0`),
both lanes ran unattended on their own hourly schedules, and **the first cycle
was OBSERVED**. Group 5 is therefore no longer entirely unticked. **Boxes 5.2, 5.3, 5.4 and 5.7
are ticked**, each on the run ids, pull requests and merge commits named on
its own line. **Boxes 5.1, 5.5 and 5.6 stay open**, each saying why in its
own place; none is open for want of work here, and 5.6 records its measurement
and says why that figure is not yet the one the box asks for. **Group 6 still stays unticked by rule**;
6.4's act was taken and is recorded as a dated note beneath it, the way 6.1's
and 6.2's are. Nothing is archived by this file: the archive is a separate word.

## 1. The proposal itself

- [x] 1.1 Author the packet — `proposal.md`, `design.md`, the
  `review-lane-floor-mirror` delta and this file — with every factual claim about
  running code verified in a clone and cited `file:line`, and every authoring
  decision stated with the alternative it beat.
  **DONE — PR [#708](https://github.com/opensoft/openxFactory/pull/708), merged
  `7b8460f5`.** Every `file:line` claim was read in a clone at openxFactory
  `0e47acc2` and codexFactory `8a406b10`, and the seven authoring decisions are
  stated with the alternative each beat under § Authoring decisions.

- [x] 1.2 `OPENSPEC_TELEMETRY=0 openspec validate mirror-floor-regeneration-automation
  --strict` and `--all --strict` green at the CLI version
  `contracts/openspec-cli-pin.yaml` names, with this repository's pre-existing
  failures unchanged in count and identity.
  **DONE, and RE-MEASURED at this realization's head.**
  `python3 scripts/validate-openspec-cli-pin.py --all --strict` — the one
  entrypoint the pin governs — reports `Totals: 94 passed, 2 failed (96 items)`
  and `0 UNDISPOSITIONED failures` at `@fission-ai/openspec@1.12.0` verified
  against its content address. The two failures are the pre-existing
  dispositioned findings `add-chain-attestation` and
  `add-composed-view-authoring`, accepted by Brett Heap 2026-09-05 "take exit
  2". **The same command on `origin/main` (`b5dbfb23`) reports the identical
  line and the identical two findings**, so the failure set is unchanged in
  count and identity.

- [x] 1.3 List the change in this repository's README "OpenSpec Records" active
  block.
  **DONE.** `README.md` § OpenSpec Records carries the change in its active
  block, with the ratification and its record named.

- [x] 1.4 The codexFactory primary `add-floor-regeneration-automation` is open
  and names this change as its companion.
  **DONE.** codexFactory `add-floor-regeneration-automation` was ratified and
  merged as `ffc090d0` (codexFactory PR #235) and names this change as its
  companion under § "The companion change, named rather than authored", listing
  the same two halves this packet claims.

- [x] 1.5 Post the packet for review, with the Codex and Copilot rounds run to
  exhaustion and every thread resolved on a measurement.
  **DONE.** Four review threads on #708, **all four resolved**
  (`reviewThreads` on the merged pull request: `resolved: true, n: 4`), and the
  Copilot rounds ran to exhaustion on the codexFactory parent as well (round 3
  `ee86015` corrected the `pull-requests` permissions spelling and an
  overclaiming tasks header).

## 2. codexFactory's half — NOT DONE HERE

**[2026-09-06 RECORD — SUPERSEDED 2026-09-09, KEPT VERBATIM. Both boxes below
are now TICKED; the paragraph is retained because it is the honest account of
why they were open, not because it is still true. Read it in the past tense.]**

**2.1 AND 2.2 STAY OPEN, AND NOT FOR WANT OF WORK HERE.** The packet is
ratified (codexFactory #235, merge commit `ffc090d0`); its REALIZATION is being
authored concurrently by a sibling lane on branch
`realize/add-floor-regeneration-automation`. Nothing in this repository waits on
it, and this lane claims none of it. Until it lands, the cycle is HALVED rather
than closed: the re-pin is proposed automatically and the regeneration is still
a hand act — stated without hedging, in the same terms the parent packet uses
about itself.

**2026-09-09 — THE PARAGRAPH ABOVE IS THE RECORD OF THIS GROUP AS IT STOOD ON
2026-09-06 AND IS KEPT UNCHANGED. Both boxes are now TICKED on acts that have
happened, each citing the pull request, merge commit or run it was read from.**

- [x] 2.1 `codexFactory: add-floor-regeneration-automation` is ratified and
  realized: the regeneration lane runs the shipped generator at a LANDED
  openxFactory `main` commit and opens the regeneration pull request itself.
  **RATIFIED, REALIZED, AND OBSERVED AT A LANDED COMMIT THREE TIMES — the last
  of them on the real promotion cycle of 2026-09-09.**
  **RATIFIED:** codexFactory PR
  [#235](https://github.com/codeXfactory/codexFactory/pull/235), merge commit
  `ffc090d0c0c5d4bacc526f54dae9283ba0cafe80` (2026-09-06T02:04:36Z).
  **REALIZED:** codexFactory PR
  [#242](https://github.com/codeXfactory/codexFactory/pull/242), merge commit
  `55acd2943326a12d904ea23a5409ec7aa92e4246` (2026-09-06T08:48:24Z), shipping
  `.github/workflows/floor-regeneration.yml`,
  `scripts/merge_master/floor_regeneration.py`,
  `credentials/floor-regeneration-bot-binding.template.yaml`,
  `docs/repository-gate-floor-repair-runbook.md` and
  `tests/merge-master/test_floor_regeneration.py`.
  **THE LANE RUNS THE SHIPPED GENERATOR AT A LANDED openxFactory COMMIT AND
  OPENS THE PULL REQUEST ITSELF** — read from the run logs, not from a report
  about them. Run `34024535671` (2026-09-06T09:23:54Z, `event: schedule`)
  opened codexFactory #248 at `1897f282` (the same run 5.2 cites). Run
  **`34389386288`** (2026-09-09T18:30:10Z, success) — *"regenerated at
  b075fd91 (refs/remotes/origin/main): 60 -> 61 entries, added
  ['openspec/specs/ideation-intent-plane/spec.md']; owed because
  membership_changed (covered-pending: 1)"* — updated the open bot pull request
  #302. Run **`34407444737`** (2026-09-09T21:32:00Z, success) — *"regenerated
  at 424e2913 (refs/remotes/origin/main)"*, *"open-or-update decision: open"* —
  opened codexFactory
  [#314](https://github.com/codeXfactory/codexFactory/pull/314), author
  `app/openxfactory`, **files: `floor/openxfactory-review-authority-floor.yaml`
  ONLY**, merged at `b08958aed1d704f29f29c666142d15e653537724`
  (2026-09-09T23:27:22Z), floor block 60 -> 61.
  **"AT A LANDED COMMIT" IS MEASURED RATHER THAN ASSERTED:** each of
  `1897f282`, `b075fd91` and `424e2913` answers
  `git merge-base --is-ancestor <sha> origin/main` on this tree, checked for
  this tick.
- [x] 2.2 That lane's additions-only and block-confinement refusals are landed
  and tested there, not here.
  **LANDED THERE BY #242 (`55acd294`), AND ABSENT HERE — both halves checked
  rather than assumed.** In codexFactory
  `tests/merge-master/test_floor_regeneration.py`, read at
  `codeXfactory/codexFactory@main` through the contents API:
  `REQUIREMENT 3 — additions-only` carries
  `test_R3_S1_a_removed_path_stops_the_run`,
  `test_R3_S2_additions_alone_proceed`,
  `test_R3_S3_a_mixed_regeneration_is_refused_whole_not_split` and the
  anti-vacuity control
  `test_ANTI_VACUITY_the_additions_only_assertion_can_fail` (that repository's
  task 3.6); `REQUIREMENT 4 — the diff is confined to the machine-generated
  block` carries `test_R4_S1_a_change_outside_the_markers_refuses`,
  `test_R4_S2_the_declared_tolerance_is_never_touched_by_a_machine` and
  `test_R4_S3_the_hand_reasoned_entries_survive_every_automated_run`.
  **NOT HERE, and that is the half a tick could quietly get wrong:**
  `grep -rniE 'additions_only|additions-only|assert_confined|confinement'` over
  `tests/review_lane_pin/` and `scripts/review_lane_repin.py` returns nothing,
  so this repository asserts neither refusal and claims neither.
- [x] 2.3 No codexFactory file is edited by this change or by its realization,
  and this packet claims no authority over one.
  **DONE, and it is measurable rather than promised: this realization's diff
  touches no path outside this repository.** The lane holds `contents: read` on
  codexFactory and the binding declares `never_grants: [contents:write,
  actions:write, pull-requests:write]` there, so it cannot acquire the ability
  either.

## 3. openxFactory realization — the re-pin lane

- [x] 3.1 Add `.github/workflows/` lane `floor-repin`: mint the App token; read
  codexFactory `main`; compare the floor document there against
  `contracts/review-lane-floor-snapshot.yaml`; act only on a disagreement.
  **DONE as `.github/workflows/review-lane-repin.yml`.** **NAMED DIFFERENTLY
  FROM THIS TASK, deliberately and recorded rather than quietly:** the task
  says `floor-repin`, the lane ships as `review-lane-repin`, because everything
  it touches is already spelled `review-lane-` (`contracts/review-lane-pin.yaml`,
  `contracts/review-lane-floor-snapshot.yaml`, `tests/review_lane_pin/`) and a
  sixth spelling would have been the only `floor-` name in the family. Nothing
  else about the task changed. The lane mints the App token, resolves
  codexFactory's default branch and head with two `gh api` reads, fetches the
  floor document at that commit, and acts only on a byte disagreement with
  `contracts/review-lane-floor-snapshot.yaml`.

- [x] 3.2 The landed-core refusal (requirement 2): verify the candidate
  codexFactory commit is reachable from codexFactory's default branch, resolved
  at run time, never taken from an event payload; refuse and open nothing
  otherwise.
  **DONE, and the refusal is a unit test rather than a shell grep.**
  `plan_advance` refuses at stage `source_commit_not_landed` unless the caller
  passed `--candidate-reachable true`, and the tri-state is `is not True`, so an
  UNMEASURED reachability refuses exactly as a failed one does
  (`test_an_unmeasured_reachability_is_refused_too`). The candidate is resolved
  from `GET /repos/opensoft/codexFactory` and `…/commits/<branch>` at run time
  and the answer is re-checked with `…/compare/<branch>...<sha>`; the payload is
  never read, asserted as an absence over the workflow and over the module's
  whole interface (`test_the_lane_resolves_the_source_default_branch_itself`).

- [x] 3.3 Move the FIVE sites in ONE commit — `contracts/review-lane-pin.yaml`
  `core_commit`; `.github/workflows/merge-master-approval.yml`'s
  `PINNED_CORE_COMMIT`; that workflow's core checkout `ref:`;
  `.github/workflows/pytest-suite.yml`'s core checkout `ref:`; and
  `contracts/review-lane-floor-snapshot.yaml` re-copied — then **RE-READ ALL
  FIVE from disk** and require each to equal the new core commit before
  committing (requirement 3).
  **DONE. `PINNED_SITES` is the enumeration, in one list, and the re-read is
  `verify_advance`, which reads from DISK.** All four commit sites plus the
  snapshot's two derived witnesses resolve to exactly one value each in the
  shipped tree, measured by
  `test_every_declared_site_resolves_in_the_real_tree`. A site that does not
  move discards the whole run: `main()` converts it into a
  `partial_advance_discarded` refusal and exits **1**, proven end to end by
  `test_the_cli_turns_a_partial_advance_into_a_refusal` with
  `pytest-suite.yml`'s `ref:` broken the way a real drift would break it.
  **And a sixth site cannot appear unnoticed:**
  `test_no_pinned_site_exists_outside_the_declared_list` sweeps every tracked
  file for a pin-shaped VALUE line naming the core commit and requires the set
  it finds to equal the declared sites exactly.

- [x] 3.4 Re-copy the snapshot from the codexFactory checkout and recompute
  `floor_snapshot.sha256` and `floor_snapshot.entry_count` FROM THE BYTES
  WRITTEN, never from a codexFactory report or pull-request body
  (requirement 4).
  **DONE.** The snapshot is written with `write_bytes(floor_bytes)` — a byte
  copy, asserted byte-for-byte by `test_the_snapshot_is_copied_not_edited` — and
  `witnesses_of` derives `sha256` and `entry_count` from those bytes and from
  nothing else. **The structural half is asserted too:**
  `inspect.signature(witnesses_of).parameters == ["document_bytes"]` and
  `plan_advance` accepts no `sha256`, `digest`, `entry_count`, `payload` or
  `report` parameter, so there is no interface through which a codexFactory
  claim could arrive (`test_no_witness_can_be_supplied_from_outside`). A stale
  digest put back after the write is caught by the re-read
  (`test_a_stale_supplied_digest_is_caught`, paired with its positive).

- [x] 3.5 Compose the pull-request body from the witnesses in requirement 6,
  including the evidence that the pinned commit is reachable from codexFactory's
  default branch.
  **DONE.** `render_pr_body` emits every witness requirement 6 enumerates, both
  before and after, plus the reachability evidence string the workflow captured
  from the API and the three commands a reviewer runs to repeat it.
  **`test_no_value_only_the_lane_could_know_appears` measures the body rather
  than reading it**: every 40-hex and 64-hex token in it must be one of the
  values recomputable from the two repositories at the named commits.

- [x] 3.6 Trigger (M-1): the scheduled sweep is the MECHANISM and must be
  sufficient alone; any codexFactory-side notification leg is an accelerator.
  **Decide and record WHERE the schedule lives** — this repository has no
  `schedule:` in any workflow today (the nightly is scheduled by a thin caller in
  the xFactory aggregation repository and reaches here through
  `workflow_call`), so a schedule here is a first for this repository and a
  schedule there puts the credential in a third repository. Both consequences to
  be stated, one chosen.
  **DONE — DECIDED AND RECORDED: the schedule lives HERE**, as
  `cron: "17 * * * *"`, and **it is this repository's first `schedule:`**. Both
  consequences are stated in the workflow's own header rather than left
  implicit: scheduling it here makes the cron unprecedented and worth watching,
  but keeps the App key in the two repositories that already hold it;
  scheduling it in the xFactory aggregation caller would add no cron here but
  would put a privileged identity into a THIRD repository merely to set a
  cadence, refused on the same ground the packet refuses a `|| github.token`
  fallback. **The sweep is the MECHANISM and the dispatch is only a nudge:**
  nothing in the file reads `github.event.client_payload`, so a hand-authored
  codexFactory regeneration — the only path a REMOVAL can take, and one that
  sends no dispatch — is still picked up. Cadence declared against the ruled
  tolerance of 3 and the measured worst case (five floored paths in 11.5 hours
  on 2026-09-04): hourly clears a landed regeneration well inside it.

- [x] 3.7 Idempotence: at most one open re-pin pull request; a firing that finds
  one updates its branch; nothing to move is a clean named no-op.
  **DONE.** `decide_idempotent_action` is pure and driven by four fixtures
  (`test_a_second_firing_does_not_open_a_second_pull_request`): none open →
  open; one open on the lane's branch → update it; two → update the lowest;
  **an open pull request on somebody else's branch → open, never adopt it.**
  The workflow's lookup is scoped `--head "${BOT_BRANCH}"`, the concurrency
  group is fixed with `cancel-in-progress: false` so a firing that has already
  opened a pull request finishes reporting it, and the update path pushes a
  two-parent `commit-tree` whose FIRST parent is the current remote tip — a
  fast-forward, **so no force push exists anywhere in the lane**. Nothing owed
  is a named no-op that writes nothing and exits 0
  (`test_the_no_op_writes_nothing_and_exits_zero`).

- [x] 3.8 Declare the credential binding as a TEMPLATE with placeholder
  references only, and make the lane FAIL LOUD when it does not resolve — no
  `|| github.token` fallback anywhere in this lane.
  **DONE — `contracts/review-lane-repin-binding.template.yaml`**, with
  `provider`/`vault` as `<per-install-…>` placeholders, the two GitHub secret
  NAMES as references, and `degraded_mode_permitted: false`. The lane's FIRST
  step reads both references and exits 1 naming the file.
  **There is no `|| github.token` anywhere in the lane and a test asserts it**
  as a regex over the file with its prose stripped, because the header names the
  pattern in order to refuse it (`test_a_missing_binding_fails_loudly`). The
  template is swept for key material, `ghp_`/`github_pat_` prefixes and any
  64-hex value; all absent.

- [x] 3.9 The workflow declares least privilege: `contents: write` and
  `pull-requests: write` on the job that opens the pull request, nothing wider,
  and no write privilege over codexFactory.
  **DONE, and the grant is held EQUAL to the binding rather than merely
  checked.** File-level `permissions: contents: read`; the one job that opens
  the pull request declares `contents: write` + `pull-requests: write` and
  nothing else; and
  `test_the_workflow_grants_exactly_what_the_binding_declares` requires the
  job's permissions to equal the binding's `floored_repository.grants` exactly,
  so a workflow that widened itself past its own declaration would fail. No
  privilege over codexFactory is granted anywhere in the file, and none could
  be: the App's read access there comes from its installation, which this block
  cannot widen.

**NOTE ON THE OUTBOUND LEG, WHICH IS NOT TAKEN AND IS NOT THIS PACKET'S.**
The realization brief asked additionally for a DISPATCHER on this side — a step
in the main-branch run that fires `floor-regeneration-requested` at codexFactory
when the floor report shows pending ≥ 1, which is codexFactory's authoring
decision E-1 leg (ii). **It is deliberately not built here, on three measured
grounds, and it is named so the omission is visible rather than discovered:**

1. **It is outside this packet's declared surface.** `proposal.md`'s
   `code_surface:` enumerates the re-pin lane, the binding template and the
   `tests/review_lane_pin/` assertions, and enumerates what is NOT the surface.
   An outbound dispatcher is in neither list, and M-1 makes any notification leg
   an accelerator rather than the mechanism on THIS side.
2. **It would need a write privilege this packet's own requirement forbids.**
   `POST /repos/{owner}/{repo}/dispatches` requires `contents: write` on the
   TARGET, so an openxFactory identity that could nudge codexFactory would hold
   write there — and requirement 8's third scenario is that the binding "grants
   no write privilege over the source repository", declared as
   `never_grants: [contents:write, actions:write, pull-requests:write]`. A
   second identity would be a second, unratified binding, and the cost is the
   one codexFactory's own design names: *"minting a dispatch credential would
   widen an identity for a mere nudge"* (the Gate-Rules Council's 2026-08-22
   ruling, quoted in that packet's `design.md` § 2).
3. **Its stated premise does not hold at this commit, and this is a measurement
   rather than an objection.** codexFactory's `design.md` § 2 locates the signal
   in "openxFactory's main-branch run" at
   `merge-master-approval.yml:1031-1042`. **That workflow's triggers are
   `pull_request_target` and `workflow_dispatch` only** — it does not run on
   `main` — and `pytest-suite.yml`, which does run on `push: branches: [main]`,
   computes no `pending_floor_extension` report at all (the string appears
   nowhere in it). So there is today no main-branch run to add the step to; a
   conforming dispatcher would have to MEASURE completeness on `main` first,
   which is a new surface of its own.

**Nothing is blocked by the omission.** codexFactory's sweep is the mechanism on
that side too, and E-1 records the alternative a reviewer may prefer on identity
cost: *"a much more frequent codexFactory-side schedule (hourly), which needs no
openxFactory-side dispatch identity at all"*. **The exact next step, if the leg
is wanted:** a separate proposal declaring the main-branch measurement and a
second, narrower binding — not an edit to this packet.

## 4. openxFactory realization — tests, and the judge left alone

- [x] 4.1 `tests/review_lane_pin/`: a workflow-shape test pinning the lane's
  trigger legs, the absence of any merge or approve call, the absence of any
  `|| github.token` fallback, and the declared permissions.
  **DONE — `tests/review_lane_pin/test_repin_lane.py`, 47 tests, 0 skips.** The
  workflow-shape tests pin all three trigger legs and the dispatch `types:`;
  the absence of `gh pr merge`, `gh pr review`, `gh pr close`, `--auto`,
  `--admin`, `--method PUT`, `/reviews` and any `gh api …pulls/…/merge`; the
  absence of any `|| github.token`; and both `permissions:` blocks.
  **Every absence assertion is made against the file with whole-line comments
  stripped**, because the lane argues its own case in its header and names the
  very patterns it refuses — a naive `assertNotIn` would go red on the prose
  that promises the behaviour it checks.

- [x] 4.2 NEGATIVE — a candidate core commit not reachable from codexFactory's
  default branch refuses and moves no site.
  **DONE — `test_a_commit_not_on_the_source_default_branch_is_refused`.** The
  refusal names both the commit and the branch, and **no site moves: every site
  value is re-read after the decision and required to be what it was.** Its
  anti-vacuity partner is `test_a_reachable_commit_is_not_refused` (same
  fixture, one input flipped).

- [x] 4.3 NEGATIVE — a run in which any one of the five sites does not read the
  new core commit after the write discards the advance and opens nothing.
  **DONE — `test_a_site_that_did_not_move_discards_the_run`**, which breaks each
  of the four commit sites IN TURN, in a copy of the shipped bytes, by renaming
  the key the way a real drift would (`core_commit:` → `core_committ:`,
  `ref: "` → `reff: "`). Each break is detected and each names itself.
  `test_a_site_the_verifier_finds_stale_discards_the_run` covers the other half
  — the write succeeded and something put a site back — which only a re-read
  from disk can catch. Partner: `test_an_unbroken_tree_reports_nothing_outstanding`.

- [x] 4.4 NEGATIVE — the snapshot's digest and entry count are computed from the
  written bytes: a fixture in which a stale digest is supplied must be caught.
  **DONE — `test_a_stale_supplied_digest_is_caught`**: the advance is applied
  and then the pin's declared digest is put back to the OLD value, exactly the
  fixture this task asks for. The re-read catches it and names
  `pin.floor_snapshot.sha256`. Partner:
  `test_a_fresh_digest_passes_the_same_assertion`.

- [x] 4.5 ANTI-VACUITY — each of 4.2, 4.3 and 4.4 is proven capable of failing:
  the positive fixture passes the same assertion the negative fixture reds.
  **DONE, and it is why the fixtures copy the REAL files.** Each of 4.2, 4.3
  and 4.4 has a named positive that passes the same assertion its negative
  reds. The controls MEASURE: `_TreeFixture` copies the four shipped files into
  a temp tree and runs the real regexes over the real bytes, so a control
  cannot pass while measuring nothing — **which is precisely how `#699` exposed
  two hard-coded-empty controls in this family's previous packet
  (`ca9fafe6`)**. The mapping itself is measured too:
  `test_every_ratified_scenario_has_a_test` reads the 24 scenario titles out of
  the ratified delta and fails on any that no docstring claims.

- [x] 4.6 **NO CHANGE** to `tests/review_lane_pin/test_floor_snapshot.py`'s LQ-A7
  assertion, its two negative controls, the byte-identity freshness verifier, its
  named-testcase watch, or `EXPECT_SKIPPED`. Assert this by diff: the realization
  pull request must touch none of them.
  **DONE, and asserted by diff.** This realization's changed-file set contains
  neither `tests/review_lane_pin/test_floor_snapshot.py` nor
  `.github/workflows/pytest-suite.yml`: LQ-A7, its two negative controls, the
  byte-identity verifier, its named-testcase watch and `EXPECT_SKIPPED: "21"`
  are all untouched. **`EXPECT_SKIPPED` does not move because the new tests add
  no skip** — none of the 47 is conditional. Two further assertions hold it
  from the other side: `test_the_bots_pull_request_meets_the_same_bar` pins
  `EXPECT_SKIPPED: "21"` and the verifier's name as VALUES in the required
  suite, and `test_no_author_keyed_exemption_exists` requires the lane's
  branch, its bot lane line and its workflow name to appear NOWHERE in either
  judge file — an exemption keyed on the author would look exactly like a
  mention of the author inside the judge.

- [x] 4.7 `python3 -m pytest tests/review_lane_pin -q` green, and green a second
  time with a codexFactory checkout on disk.
  **DONE.** `python3 -m pytest tests/review_lane_pin -q` → **121 passed, 2
  skipped, 33 subtests passed**; the 2 skips are pre-existing and are the
  byte-identity verifier's own, unchanged by this work. **And the lane runs
  that same suite itself before it proposes anything**: a step checks
  codexFactory out at the CANDIDATE commit into `.merge-master-core`, sets
  `PINNED_CORE_CHECKOUT`, and runs `pytest tests/review_lane_pin -q`
  unmodified — no `-k`, no `--deselect`, no `--ignore`. The ref is the
  candidate rather than the old pinned core deliberately: comparing a new
  snapshot against the old document would red every honest advance.
  `test_the_lane_submits_itself_to_the_judge_before_proposing` holds the step,
  its ref, and its position before the opener.

## 5. The first UNATTENDED cycle, observed end to end

**EVERY BOX IN THIS GROUP STAYS UNTICKED, AND THE REASON IS THE GROUP'S OWN
HEADING: it is what has been OBSERVED, not what has been built.** The lane is
realized and tested; no unattended cycle has run, because a cycle needs a real
`openspec/specs/**` promotion and a codexFactory regeneration to follow it.
Ticking any of these on a test-only observation would be exactly the false
completion 5.7 was written to refuse — *"or the box stays OPEN and says so
rather than being ticked on a test-only observation"*. **The floor at
codexFactory `main` is byte-identical to the vendored snapshot at this head
(`b4dcf676…`, verified with `cmp`), so there is nothing owed to observe right
now**: the lane's correct behaviour today is the named no-op, and the first
cycle will have to wait for a real promotion.

**2026-09-06 — THE PARAGRAPH ABOVE IS THE RECORD OF THIS GROUP BEFORE THE FIRST
CYCLE AND IS KEPT UNCHANGED; what follows is what was OBSERVED.** The cycle ran
on 2026-09-06 and is recorded box by box below, every claim carrying the run id,
pull request or merge commit it was read from, and every quotation taken from
the run log or the pull-request body rather than from a report about it. Two
facts about the cycle are stated here rather than left to be inferred from the
boxes:

1. **It was NOT the cycle 5.1 describes, and that is the RULING's doing rather
   than a shortfall.** Brett Heap ruled the pin-only reading on codexFactory
   [#232](https://github.com/opensoft/codexFactory/issues/232) at
   2026-09-06T08:43Z, verbatim *"merge both when green, pin-only reading
   stands"*: a regeneration whose only movement is `generated_at` IS a
   regeneration the lane proposes. What ran was exactly that — block
   `entry_count` 60 → 60, `added []`, and **no `openspec/specs/**` promotion
   anywhere in the chain**. 5.1 and 5.5 each need a promotion to have happened,
   so each stays open. The `target_release:` line in `proposal.md` names *"a
   real `openspec/specs/**` promotion here"* as part of its archive evidence
   and is NOT edited by this file; whether the ruled pin-only cycle discharges
   it is the archive word's question, not this record's.
2. **The cycle found THREE defects, one of them here, and all three were found
   by RUNNING rather than by review.** codexFactory's tests carried a live-pin
   literal that reddened every bot regeneration (fix codexFactory #252 →
   `91fc95f5`); codexFactory's regeneration lane force-pushed its update path
   into a `non_fast_forward` ruleset (fix codexFactory #260 → `f430cf7e`); and
   **this repository's own lane minted a token with no `workflows` permission
   although two of its five pinned sites are workflow files** (fix
   [#726](https://github.com/opensoft/openxFactory/pull/726) → `0f9361e0`).
   Each is named on the box whose evidence it belongs to.

- [x] 5.1 A real `openspec/specs/**` promotion lands here and the advisory lane
  reports `pending_floor_extension` with a non-zero count — quoted verbatim.
  **OBSERVED 2026-09-09. The promotion is real, the count is non-zero, and the
  path the report names is the one the promotion created.**
  **THE PROMOTION:** openxFactory PR
  [#832](https://github.com/opensoft/openxFactory/pull/832) — *"Archive
  add-ideation-intent-plane with promotion (Path A PR-5: 4.4/5.1/5.2 ticked on
  the D-2 evidence)"* — merge commit
  `56e69a11c59d473da23eab455cb9848dc083fac3`, 2026-09-09T07:49:06Z, which
  CREATED `openspec/specs/ideation-intent-plane/spec.md`. It is a corpus event
  no lane manufactured: another lane archived its own packet, and this box's
  wait ended as a side effect of that.
  **THE ADVISORY READING, QUOTED VERBATIM** from the step `Evaluate the
  openxFactory repository gate floor` of `merge-master-approval` run
  [34417309342](https://github.com/opensoft/openxFactory/actions/runs/34417309342)
  (2026-09-09T23:31:45Z, `pull_request_target`, `success`, candidate head
  `1c640a5b`):

  ```
  stage:                 pending_floor_extension
  floor entries:         68
  reachable matches:     0
  unreachable entries:   0
    caused by candidate: 0
    already dead:        0
  tracked under prefix:  61 (openspec/specs)
  uncovered by floor:    0
  covered-pending:       1 (tolerance 3, pin measured)
    PENDING (added_to_base_after_pin): openspec/specs/ideation-intent-plane/spec.md
  floor evaluated: 0 never-clearable path(s) touched
  ```

  **THREE THINGS IN THAT BLOCK ARE WHY IT SATISFIES THE BOX AND THE FIRST
  CYCLE'S READING DID NOT.** The stage is `pending_floor_extension` rather than
  `floor_complete`. The count is **1**, not the `0` this box refused to tick on
  in 2026-09-06 (run 34066687712, quoted below in the record kept above). And
  it is `pin measured`, not the B1 fail-safe, with the per-path reason
  `added_to_base_after_pin` — the path entered `main` AFTER the snapshot's
  pinned core `4b12ba83`, which is exactly the class this box was written to
  observe. The count is 1 against `tolerance 3`, so the grace holds and nothing
  is refused; what DISCHARGES the pending path is the re-pin, which is 5.5's
  question and deliberately not this box's.
  **[2026-09-06 RECORD — SUPERSEDED BY THE OBSERVATION ABOVE, KEPT VERBATIM
  FROM HERE TO THE END OF THIS BOX. The box is now TICKED; what follows is the
  honest account of why it stayed open for three days, and is to be read in the
  past tense.]**
  **STAYS OPEN, AND NOT FOR WANT OF A CYCLE.** The first observed cycle carried
  no `openspec/specs/**` promotion at all — see the group note above — so there
  was never a non-zero count to quote. codexFactory bot PR
  [#248](https://github.com/opensoft/codexFactory/pull/248), the regeneration
  that opened the cycle, witnesses it in its own body: *"block `entry_count`:
  60 → 60"* and *"The covered-pending set this regeneration discharges: None.
  No entry this block adds was covered-pending in the measured window."* The
  advisory reading taken on the re-pin pull request itself (openxFactory run
  [34066687712](https://github.com/opensoft/openxFactory/actions/runs/34066687712),
  step `Evaluate the openxFactory repository gate floor`) is
  `covered-pending:       0 (tolerance 3, pin measured)`. The box waits on a
  real promotion, which is a corpus event no lane can manufacture and which
  this record will not simulate.
- [x] 5.2 The codexFactory regeneration pull request is opened BY THAT LANE, with
  no operator running the generator.
  **OBSERVED 2026-09-06T09:24:11Z.** codexFactory `floor-regeneration` run
  [34024535671](https://github.com/opensoft/codexFactory/actions/runs/34024535671)
  — `event: schedule`, `conclusion: success`, 09:23:54Z → 09:24:16Z (22 s) —
  opened codexFactory PR
  [#248](https://github.com/opensoft/codexFactory/pull/248) *"Regenerate the
  openxFactory review-authority floor block at
  1897f282af4558244f79a5cc2415d3623803a425 (60 -> 60 entries)"*, author
  `app/openxfactory` (a bot, not a person), head `floor/bot-regeneration`, body
  line 1 `Lane: floor-regeneration-bot`. **No operator ran the generator, and
  the pull request says how the commit was chosen rather than leaving it to be
  trusted:** *"`refs/remotes/origin/main`, resolved by the lane at run time. No
  trigger payload named it; this CLI carries no `--ref`."* The run's own trigger
  is the `17 * * * *` sweep — the mechanism M-1 required to be sufficient alone
  — and no dispatch was sent to it by this repository, because none is built
  here (§ 3's note on the outbound leg).
- [x] 5.3 The re-pin pull request is opened BY THIS LANE, with no operator
  copying a digest; the five sites are verified by reading them back from the
  merged commit, not from the lane's own report.
  **OBSERVED 2026-09-06T23:22:06Z, AND READ BACK FROM THE MERGED COMMIT.**
  `review-lane-repin` run
  [34066668104](https://github.com/opensoft/openxFactory/actions/runs/34066668104)
  — `event: schedule`, 23:21:43Z → 23:22:11Z (28 s), `success` — minted both
  tokens, resolved codexFactory's default branch for itself (`resolved
  opensoft/codexFactory@main = 19f2ab0c9f04d4cf24af11c2551cb1a19263e41b (compare
  status identical)`), measured the disagreement, advanced the five sites,
  re-read them, and opened [#732](https://github.com/opensoft/openxFactory/pull/732)
  (*"Advance the pinned decision core to 19f2ab0c…"*, author `app/openxfactory`,
  head `bot/review-lane-repin`, 4 files +7/-7, body line 1 `Lane:
  review-lane-repin-bot`). **No operator copied a digest**: the body says the
  snapshot's `sha256` is computed from the bytes the lane wrote and gives the
  one-line command to recompute it. **The five sites, read back from the MERGED
  commit `9ffc62529859a9e8dfba2ada8017f46e22ab3936` and not from the lane's
  report:** `contracts/review-lane-pin.yaml` l.60 `core_commit:
  "19f2ab0c9f04d4cf24af11c2551cb1a19263e41b"`, l.630 `sha256:
  "1a0bff1b5a636f815452aa8c3c7ceffdddc33e76653925fc431a6f956d668907"`, l.631
  `entry_count: 68`; `.github/workflows/merge-master-approval.yml` l.410
  `PINNED_CORE_COMMIT: "19f2ab0c…"` and l.525 `ref: "19f2ab0c…"`;
  `.github/workflows/pytest-suite.yml` l.397 `ref: "19f2ab0c…"`. The vendored
  snapshot's bytes at that commit hash to `1a0bff1b5a63…` (`sha256sum` over the
  raw file), equal to codexFactory's floor document at `19f2ab0c` hashed the same
  way — the byte copy is a byte copy.
- [x] 5.4 The required suite judges that pull request GREEN with no exemption —
  and the byte-identity freshness verifier is confirmed to have RUN, by name, on
  it.
  **OBSERVED.** `pytest-suite` run
  [34066687673](https://github.com/opensoft/openxFactory/actions/runs/34066687673)
  on #732's head `7a7b5764`: `9967 passed, 21 skipped, 338 deselected, 9
  warnings, 93 subtests passed in 1381.80s`; the pinned triple `selected=10081
  passed=10060 skipped=21 failures=0 errors=0` — `skipped==21` is the pinned
  count, unchanged, so no exemption was taken; and the verifier BY NAME, printed
  by the workflow's own named-testcase watch: `freshness verifier
  (tests.review_lane_pin.test_floor_snapshot.TheFreshnessVerifier::test_the_snapshot_is_byte_identical_to_the_pinned_core):
  passed`, run against the candidate core the step `Check out the pinned
  decision core (freshness verifier only)` fetched at
  `19f2ab0c9f04d4cf24af11c2551cb1a19263e41b`. The other seven checks were green;
  `lane-line` skipped by design for a bot author.
- [x] 5.5 Both merge on a human word, and `covered-pending` returns to zero on
  the next main run — quoted verbatim from that run.
  **HALF OBSERVED, HALF NOT OBSERVABLE ON THIS CYCLE — STAYS OPEN.** Both halves
  merged on a human word: codexFactory #248 → `7f147070a8497038e96040ced403ee84d4044bd1`
  (2026-09-06T11:26:25Z, *"merge 248, then report the re-pin sweep when it
  lands"*); #254 → `307d38f10705033e3e095270d81b37f12844d970` (20:25:18Z,
  *"granted workflows, merge 254, then report the re-pin sweep when it lands"*);
  this repository's #732 → `9ffc62529859a9e8dfba2ada8017f46e22ab3936` (23:46:27Z,
  *"merge 732 when green, then tick section 5 in both packets"*). But
  `covered-pending` cannot RETURN to zero on a cycle in which it never left zero
  (5.1): the advisory reading on #732 itself was `covered-pending:       0 (tolerance 3, pin measured)` (run
  [34066687712](https://github.com/opensoft/openxFactory/actions/runs/34066687712)).
  Ticks on the first cycle that starts from a non-zero count, and not before.

  **2026-09-09 — THE CYCLE THAT STARTS FROM A NON-ZERO COUNT IS RUNNING, HALF
  ONE IS SUPERSEDED RATHER THAN UNMET, AND HALF TWO HAS NOT HAPPENED YET. THE
  BOX STAYS OPEN.**
  **(a) *"Both merge on a human word"* is SUPERSEDED for the codexFactory half
  by a later RATIFIED mechanism, and the superseding is recorded here rather
  than the clause being deleted.** `amend-floor-regeneration-merge-authority`
  (codexFactory [#289](https://github.com/codeXfactory/codexFactory/pull/289),
  realized by #292) arms auto-merge on the regeneration pull request, and on
  2026-09-09 codexFactory
  [#314](https://github.com/codeXfactory/codexFactory/pull/314) merged at
  `b08958aed1d704f29f29c666142d15e653537724` (23:27:22Z) with `mergedBy:
  app/openxfactory` and `author: app/openxfactory`. Bot author, bot arming
  (08:32:34Z on the #302 lineage, re-armed on #314 at 21:32Z), bot approval
  (`codexfactory[bot]` APPROVED at 22:49:36Z on `fcb2bd13`, merge-master run
  34414078939), platform merge. **No human word was given on that candidate
  and, by the ratified amendment, none was owed.** Disclosed operator acts on
  the PATH but not on the candidate's content: closing #302 after #310 made its
  update path conflict, and one hand `workflow_dispatch` of
  `merge-master-approval` at 22:49Z because the first evaluation ran while
  checks were still pending.
  **(b) THIS REPOSITORY'S HALF OF THE CYCLE HAS NOT RUN, so `covered-pending`
  has not returned to zero and no run can be quoted for it.** The floor moved on
  `codeXfactory/codexFactory` `main` at 23:27:22Z; the `review-lane-repin` sweep
  before it — run
  [34416680260](https://github.com/opensoft/openxFactory/actions/runs/34416680260)
  (2026-09-09T23:22:59Z, success) — was five minutes early and correctly found
  nothing owed. **The next `17 * * * *` tick is the first firing that can see
  the moved floor**, and what it should open is this repository's first
  ARMED-INERT advance (`amend-mirror-floor-regeneration-merge-authority` box
  1.3: the arming is inert by ruling until the enrolment successor lands), which
  a human then merges. **Half two ticks on the first ADVISORY run over a base
  that includes that re-pin, quoting `covered-pending: 0` from it, and not
  before. That is an event, not a judgement, and this record will not simulate
  it.**
  **WHICH RUN, PRECISELY — because the box's own words "the next `main` run"
  name a trigger that DOES NOT EXIST, and § 3's finding 3 above already measured
  that rather than this note discovering it.** `merge-master-approval.yml` is
  the only workflow that PRINTS a `covered-pending` reading — `grep -ln
  covered-pending .github/workflows/*.yml` names it and `review-lane-repin.yml`,
  and the re-pin lane's occurrence is a DESIGN COMMENT (line 94, on the
  cadence-versus-tolerance argument) rather than output: that lane reports its
  own `action` and `reason` and renders no floor report at all. Its triggers are
  `pull_request_target` (opened / reopened / synchronize) and
  `workflow_dispatch` — it does not run on a push to `main`; `pytest-suite.yml`,
  which DOES run on `push: branches: [main]`, computes no
  `pending_floor_extension` report at all. **So the evidence run for half two is
  an advisory run whose BASE carries the landed re-pin** — exactly how 5.1's own
  evidence was produced: run 34417309342 is a `pull_request_target` run on the
  unrelated pull request #874, reading a base that already carried #832. It
  arrives on the next pull request opened or synchronised after the re-pin
  lands, or on a hand `workflow_dispatch`. **The box's phrase is READ as "the
  next advisory run over a base that includes the re-pin", and this note is that
  reading written down rather than a silent substitution.**
  **THE MERGE WORD FOR THAT RE-PIN IS BRETT HEAP'S AND HAS NOT BEEN GIVEN.**
  **2026-09-10 — TICKED, AND THE TICK IS THE LANE'S RULING ON BRETT HEAP'S
  DELEGATION, verbatim: "same word for the mirror's six on #745" (extending
  "tick 6.1, 6.2, 6.4 and 6.3; rule on the rest")
  ([#745, comment 5618883586](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5618883586)).**
  Four of the six boxes his word reaches are owner's acts in § 6 and this one is
  not: it is one of the two he delegated with *"rule on the rest"*, and what
  follows is the ruling, with the run and merge citations it rests on read back
  from the API rather than restated.
  **EVERYTHING ABOVE THIS DATED NOTE IS THE RECORD OF 2026-09-06 AND
  2026-09-09, KEPT VERBATIM, AND EXACTLY TWO OF ITS SENTENCES ARE SUPERSEDED —
  named here rather than struck out, which is how every earlier disposition in
  this file was written.** They are *"HALF OBSERVED, HALF NOT OBSERVABLE ON
  THIS CYCLE — STAYS OPEN"* and *"THE BOX STAYS OPEN"*: both were true of the
  cycle each was written about, and neither is true of cycle three. Every other
  sentence above stands, the supersession of the human-word clause at (a)
  included. **BOTH CLAUSES ARE OBSERVED ON CYCLE
  THREE**, the first cycle that ran with a non-zero starting count (5.1).
  **CLAUSE (a) — *"both merge on a human word"*.** This repository's half
  merged on his word *"merge both"*:
  [#883](https://github.com/opensoft/openxFactory/pull/883) →
  `e916f0ea89265223c2f00c11395b90a41f376920`, `mergedBy: brettheap`. The
  codexFactory half's human word is SUPERSEDED — not unmet, and recorded here
  rather than the clause being deleted — by the ratified
  `amend-floor-regeneration-merge-authority`: codexFactory
  [#325](https://github.com/codeXfactory/codexFactory/pull/325) (*"Regenerate
  the openxFactory review-authority floor block at `e32d580a` (61 -> 62
  entries)"*) merged at `df42f8033a2dee3fd6f49d435912e7f30eac24ec` at
  2026-09-10T01:55:14Z with `mergedBy: app/openxfactory`, **and by that
  amendment no human word was owed on it**. This is the same supersession the
  2026-09-09 note above recorded on cycle two, carried unchanged and instanced
  again; nothing in that note is withdrawn.
  **CLAUSE (b) — `covered-pending` returns to zero — UNDER THE BOX'S OWN
  RECORDED READING and not a silent substitution.** The 2026-09-09 note above
  already measured that this box's literal phrase *"the next `main` run"* names
  a trigger that DOES NOT EXIST (§ 3 finding 3: `merge-master-approval.yml` is
  the only workflow that prints the reading and it runs on
  `pull_request_target` / `workflow_dispatch`; `pytest-suite.yml`, which does
  run on `push: branches: [main]`, computes no `pending_floor_extension` report
  at all), and READ the phrase as *"the next advisory run over a base that
  includes the re-pin"*. That run is
  [34475347536](https://github.com/opensoft/openxFactory/actions/runs/34475347536)
  — `merge-master-approval`, event `pull_request_target`, created
  **2026-09-10T12:11:42Z**, the FIRST advisory run after the 11:57:17Z merge,
  its step `Checkout decision core (codeXfactory/codexFactory, pinned)` reading
  `ref: b594ef2ad86ebdefffc497c571c8a84044f6ec10`, which is the pin #883
  landed. Its step `Evaluate the openxFactory repository gate floor` prints,
  verbatim:

  ```
  covered-pending:       0 (tolerance 3, pin measured)
  ```

  Runs
  [34475672967](https://github.com/opensoft/openxFactory/actions/runs/34475672967)
  (12:15:07Z) and
  [34477475011](https://github.com/opensoft/openxFactory/actions/runs/34477475011)
  (12:34:19Z) print that line byte for byte. It is `pin measured`, not the B1
  fail-safe, and the count is `0` on a base whose predecessor read `1`.
  **5.1's non-zero reading → #883 → 0 IS THE ROUND TRIP THIS BOX ASKS FOR, and
  it is closed in this repository.** What the box refused to tick on in
  2026-09-06 — a `0` that had never left `0` — is not what is ticked here.
  **ONE FIGURE IN THE RULING IS CORRECTED BY RE-READING RATHER THAN CARRIED:**
  the #745 comment gives the #883 merge as 11:57:22Z; `mergedAt`,
  `mergeCommit.committedDate` and the `MergedEvent` all read
  **2026-09-10T11:57:17Z**, five seconds earlier. Nothing in either clause turns
  on it — 12:11:42Z is after both — and the correction is recorded here rather
  than by editing the ruling.
- [x] 5.6 The end-to-end wall time is measured and recorded against the two hand
  cycles in `proposal.md` § Why (55 min and 77 min).
  **MEASURED AND RECORDED — NOT YET THE FIGURE THE BOX ASKS FOR, SO IT STAYS
  OPEN.** From the regeneration lane's first firing (run 34024535671,
  2026-09-06T09:23:54Z) to #732's merge (23:46:27Z): **14 h 22 min 33 s**. From
  the floor's last movement on codexFactory `main` (#254 → `307d38f1`, 20:25:18Z)
  to #732's merge: **3 h 21 min 09 s**, of which about three hours were this
  lane's mint refusing until the owner's grant landed (§ 6.4, 5.7). The lane's own
  unattended latency once it could mint: sweep 23:21:43Z → pull request
  23:22:06Z (23 s) → merged 23:46:27Z. Against the 55 min and 77 min HAND cycles
  in `proposal.md` § Why: LANE TIME — an operator authoring the advance — was
  ZERO in this cycle, which is the claim; WALL TIME was attended by three repairs
  and one grant wait, so the comparable unattended figure is owed on the first
  repair-free cycle.

  **2026-09-09 — THE FIGURE IS STILL OWED; THE 2026-09-09 CYCLE DOES NOT SUPPLY
  IT EITHER. THE BOX STAYS OPEN.** Two reasons, both measured:
  **(a) THE CYCLE IS NOT END-TO-END YET.** The box asks for an END-TO-END wall
  time and the end is this repository's re-pin merge, which has not happened
  (5.5 (b)). The codexFactory half alone ran promotion `56e69a11`
  (2026-09-09T07:49:06Z) -> first owed regeneration run 34389386288 (18:30:10Z)
  -> #314 opened 21:32:00Z -> merged `b08958ae` 23:27:22Z: **15 h 38 min 16 s**,
  which is a half-cycle figure and not the one asked for.
  **(b) IT WAS NOT REPAIR-FREE, and by a wider margin than the first cycle
  was.** The path was cleared by codexFactory #306, #307, #308 and #310, by a
  hand `workflow_dispatch` of the merge-master, and by an operator closing #302
  — on top of the openxFactory-side org-move repairs (#801) that reddened both
  lanes from ~13:1xZ to 15:40Z. **LANE TIME — an operator authoring the advance
  — was again ZERO, which is the packet's actual claim**; the comparable
  UNATTENDED wall time remains owed on the first cycle that runs clean end to
  end in both repositories.
  **2026-09-10 — TICKED ON THE RECORDING, AND THE FIGURE THIS BOX ASKS FOR IS
  NAMED AS STRUCTURALLY OWED ELSEWHERE. The tick is the lane's ruling on Brett
  Heap's delegation, verbatim: "same word for the mirror's six on #745"
  (extending "tick 6.1, 6.2, 6.4 and 6.3; rule on the rest")
  ([#745, comment 5618883586](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5618883586)).**
  **EVERYTHING ABOVE THIS DATED NOTE IS THE RECORD OF 2026-09-06 AND
  2026-09-09, KEPT VERBATIM, AND EXACTLY TWO OF ITS SENTENCES ARE SUPERSEDED —
  named here rather than struck out.** They are *"MEASURED AND RECORDED — NOT
  YET THE FIGURE THE BOX ASKS FOR, SO IT STAYS OPEN"* and *"THE BOX STAYS
  OPEN"*. Everything else above stands, and the central finding of both earlier
  notes — that the figure asked for is still owed — is not superseded but
  CARRIED: it is restated below, with the successor it is owed to named.
  **WHAT WAS MEASURED, on cycle three, every timestamp read back from the API.**
  End to end: promotion `62935437fc59436f92b919654b42df9a0f0cbd9f`
  (`openspec/specs/repository-identity/spec.md`, 2026-09-10T00:38:27Z) → last
  merge `e916f0ea` (11:57:17Z) = **11 h 18 min 50 s**. On § Why's own measure —
  *first open to last merge* — codexFactory #325 opened 01:32:58Z → 11:57:17Z =
  **10 h 24 min 19 s**. Against the two HAND cycles in `proposal.md` § Why,
  **55 min** (cxF #212 → oxF #689) and **77 min** (cxF #226 → oxF #702). (The
  #745 ruling states these as 11 h 18 min 55 s and 10 h 24 min 24 s off an
  11:57:22Z merge; the merge reads 11:57:17Z on `mergedAt`,
  `mergeCommit.committedDate` and the `MergedEvent` alike, so the two spans are
  five seconds shorter. The correction is recorded, not edited into the ruling,
  and it moves no conclusion.)
  **THAT IS NOT THE REPAIR-FREE UNATTENDED FIGURE, AND THIS NOTE SAYS WHY
  RATHER THAN OFFERING IT AS ONE.** The two halves behaved differently and the
  average of them would describe neither.
  **(a) THE REGENERATION HALF WAS UNATTENDED END TO END.** codexFactory #325
  opened 01:32:58Z by `app/openxfactory` and merged 01:55:14Z by
  `app/openxfactory` — **22 min 16 s, with no human actor anywhere in it**.
  **(b) THE RE-PIN HALF WAS STRUCTURALLY REFUSED FOR ROUGHLY TEN HOURS, on a
  ONE-TIME step this packet does not own.** Twelve consecutive `review-lane-repin`
  firings failed at the step `Submit the advance to the checks that will judge
  it` —
  [34423536950](https://github.com/opensoft/openxFactory/actions/runs/34423536950)
  (00:58:18Z), 34425967673, 34429979539, 34433600395, 34437425134, 34441038243,
  34446277741, 34450161402, 34455871542, 34460859575, 34466086328 and
  [34471122863](https://github.com/opensoft/openxFactory/actions/runs/34471122863)
  (11:24:25Z) — every one on the same assertion,
  `tests/review_lane_pin/test_repin_lane.py::TheDeclaredCandidateList::test_the_pinned_core_declarations_name_the_document_at_the_pinned_commit`,
  whose own message names the cause: *"If `core_commit` has just advanced past
  codexFactory's relocation (`8165d1f3`), this is M-1 step (3) box 4.2 falling
  due"* — `relocate-review-authority-floor-mirror` box 4.2, the one-time
  relocation of the floor document from `scripts/merge_master/` to `floor/`.
  (The #745 ruling counts eleven of these; the run list counts **twelve**,
  00:58:18Z through 11:24:25Z inclusive, and the twelve ids are given above so
  the count can be re-taken rather than believed.) The advance was then
  **driver-produced BY HAND** as #883 and merged on a human word. The tick
  after it — run
  [34477749947](https://github.com/opensoft/openxFactory/actions/runs/34477749947),
  schedule, 12:37:16Z, success — was a clean named no-op, verbatim from its
  step `Report a clean no-op`:

  ```
  nothing is owed: `contracts/review-lane-floor-snapshot.yaml` is byte-identical to `floor/openxfactory-review-authority-floor.yaml` at codeXfactory/codexFactory@main (34fc5a8fd1d94e21da11bf1dc9a4b933651c61ef); the pin stays at b594ef2ad86ebdefffc497c571c8a84044f6ec10
  ```

  So the lane was healthy the moment the one-time relocation was carried, which
  is what makes the ten hours a property of that step and not of this one.
  **LANE TIME — AN OPERATOR AUTHORING THE ADVANCE — REMAINS ZERO ON A ROUTINE
  ADVANCE, WHICH IS THIS PACKET'S ACTUAL CLAIM**, and cycle one measured it:
  sweep 23:21:43Z → pull request 23:22:06Z, **23 s** (recorded above and not
  re-derived here). Cycle three's re-pin was not a routine advance; it was a
  schema relocation the lane is designed to refuse until a human carries it.
  **AND THE FIGURE THE BOX LITERALLY ASKS FOR DOES NOT EXIST YET — SAID PLAINLY
  RATHER THAN APPROXIMATED.** **No repair-free, unattended, two-repository
  end-to-end wall time has been observed on any of the three cycles run**, and
  none can be while THIS repository's merge is a human act by ruling (6.3): the
  clock would be measuring how long Brett Heap took to type *"merge both"*,
  which is not a property of the automation. **It is therefore STRUCTURALLY
  OWED ELSEWHERE, and the successor is named:** the enrolment successor
  `admit-review-lane-repin-to-merge-approval-envelope`
  (`amend-mirror-floor-regeneration-merge-authority` box 4.3, UNFILED and
  needing Brett Heap's own word). The first cycle after that lane's merge stops
  being human is the first cycle that can produce the figure. **It is owed to
  that successor and not to this box**, and this box is ticked on the recording
  of everything it could measure plus the named owing of what it could not —
  not on a substitute figure presented as the one asked for.
- [x] 5.7 ONE observed refusal on a real run, of any kind (non-landed core, a
  site that did not move, an unresolved binding), quoted verbatim — or the box
  stays OPEN and says so rather than being ticked on a test-only observation.
  **OBSERVED — TWO KINDS, on eleven of this lane's own scheduled runs, neither
  of them test-only.**

  1. **DELIVERY REFUSED, seven consecutive runs** (34033398015 12:32Z,
     34035893707, 34038978080, 34042099357, 34045360684, 34048314680 and
     34051714881 18:26Z — every one failing at the step `Open or update the
     single automated advance`). Everything upstream had worked on a real
     advance; the push was refused, quoted verbatim from run 34033398015's log:

     ```
      ! [remote rejected]   bot/review-lane-repin -> bot/review-lane-repin (refusing to allow a GitHub App to create or update workflow `.github/workflows/merge-master-approval.yml` without `workflows` permission)
     ```

     This is defect 3, and it is a defect of THIS packet's realization: two of
     the five pinned sites are workflow files and the mint asked for no
     `workflows` permission. Repaired by
     [#726](https://github.com/opensoft/openxFactory/pull/726) → `0f9361e0`.

  2. **THE BINDING'S OWN FAIL-LOUD REFUSAL — the kind this box names — on four
     consecutive hourly firings** (34054557033 19:19Z, 34057874428 20:24Z,
     34060823926 21:21Z, 34063839864 22:22Z, every one failing at the step
     `Mint the lane's App token`, with the codexFactory READ token already
     minted one step earlier). Quoted verbatim from run 34054557033's log:

     ```
     ##[error]The permissions requested are not granted to this installation. - https://docs.github.com/rest/reference/apps#create-an-installation-access-token-for-an-app
     ```

     **Nothing downstream ran and nothing was half-written**: the run's step
     list stops at the mint. This is task 3.8's *"FAIL LOUD when it does not
     resolve"* observed on real runs rather than asserted in a test — the lane
     refused for four hours rather than degrading, and it refused **because
     #726 had just made the mint ask out loud for the permission it needs**, so
     the repair to defect 3 turned a silent push failure into a named refusal
     at the first step. It cleared only when the owner's grant landed (§ 6.4).

## 6. Owner's acts (not an agent's)

- [x] 6.1 Ratify or refuse this packet. The 2026-09-05 word authorized the
  PROPOSING, not the content.
  **2026-09-06 — TAKEN. Brett Heap ratified it in session, verbatim "ratify both
  when green, then land them" — a PAIR word over this companion and codexFactory
  #235 together, recorded 2026-09-06T01:18Z on PR #708 over head `e4ef8ade`, its
  `pytest-suite` condition met. The packet is now `Status: ratified` and the
  record is `review/ratification-2026-09-06.md`. The box is left UNTICKED
  deliberately — ticking an owner's-act box is a claim an agent may not make
  about the owner, and this dated note is how the act is recorded instead.**
  **2026-09-09 — THE ACT IS DONE AND ONLY THE TICK IS OWED, and the tick is
  Brett Heap's.** Nothing about this box waits on work in either repository: the
  ratification happened on 2026-09-06 and is cited above with its word, its head
  and its record. Carried into the archive ledger below as NEEDS-BRETT (tick
  only), not as unfinished realization.
  **2026-09-10 — TICKED on Brett Heap's word, verbatim: "same word for the
  mirror's six on #745" (extending "tick 6.1, 6.2, 6.4 and 6.3; rule on the
  rest") ([#745, comment 5618883586](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5618883586)).**
  The act this box names happened on 2026-09-06 and is cited three lines above
  with its word, its head and its record — *"ratify both when green, then land
  them"*, recorded 2026-09-06T01:18Z on PR
  [#708](https://github.com/opensoft/openxFactory/pull/708) over head
  `e4ef8ade` with its `pytest-suite` condition met, record
  `review/ratification-2026-09-06.md` — and what was owed was only the tick.
  **THE `[x]` IS LANE `openxfactory-2`'S PEN AND THE ACT IS HIS**: the § 6
  convention that an agent may not tick an owner's-act box is not waived here,
  it is SATISFIED — the owner gave the tick, in the words quoted above, and the
  lane wrote the character he authorized. Nothing else about this box moved.
- [x] 6.2 Rule on the authoring decisions M-1 through M-7, and in particular on
  M-7 (the lane writes no comment-history paragraph, so eight advances of
  narrative in `contracts/review-lane-pin.yaml` stop accruing) and on M-1's
  schedule location.
  **2026-09-06 — STOOD. Under the ratification word, M-1 through M-7 stand as
  recommended and no veto was exercised; each remains one edit away. The box
  stays UNTICKED for the same reason 6.1's does.**
  **2026-09-09 — UNCHANGED: no veto has been exercised on M-1..M-7 in the three
  days since, and M-1's schedule location has been exercised on every hourly
  tick since 2026-09-06 with no operator dispatch. The act is done and only the
  tick is owed; carried into the archive ledger below as NEEDS-BRETT (tick
  only).**
  **2026-09-10 — TICKED on Brett Heap's word, verbatim: "same word for the
  mirror's six on #745" (extending "tick 6.1, 6.2, 6.4 and 6.3; rule on the
  rest") ([#745, comment 5618883586](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5618883586)).**
  M-1 through M-7 STOOD — they stood as recommended under the 2026-09-06
  ratification word, no veto has been exercised on any of the seven in the four
  days since (M-7 included, the one that names a real loss), and M-1's schedule
  location has been exercised on every hourly firing since 2026-09-06 with no
  operator dispatch, including the twelve refusals and the clean no-op recorded
  at 5.6 above, so the decision is not merely unvetoed but observed working.
  **THE `[x]` IS THE LANE'S PEN AND THE RULING IS HIS**; the box records his
  act, not the lane's judgement of it, and each of M-1..M-7 remains one edit
  away exactly as the 2026-09-06 note said.
- [x] 6.3 SEPARATE AND NOT ASKED FOR HERE: whether the merge-master low-risk
  envelope — live today only for the doc-health nightly lane — should ever be
  extended to this lane. The default is a human merge word, and it holds until
  this box is ruled. Named so the question is not silently assumed either way,
  and noting that `contracts/review-lane-pin.yaml` is itself a never-clearable
  floor entry whose stated ground is that a clearable pin *"would let a pull
  request choose its own judge"*.
  **2026-09-09 — THE SUCCESSOR IS NAMED AND FILED, AND THE QUESTION IS ANSWERED
  FOR THE OTHER REPOSITORY BUT NOT FOR THIS LANE.**
  **NAMED AND FILED:** `openspec/changes/extend-merge-master-envelope-to-floor-bot-lanes/`
  is an ACTIVE change in this repository, governed by
  [#745](https://github.com/opensoft/openxFactory/issues/745) and opened on
  Brett Heap's 2026-09-07 ~02:0xZ multiple-choice ruling, verbatim *"Propose the
  extension now"*. Under the 2026-09-06 owed-successor ruling — an owed
  successor's task box ticks when the successor is NAMED — this box is
  TICKABLE. **It is left UNTICKED because § 6 is the owner's-acts section and
  the tick is his, for the same reason 6.1's and 6.2's are.**
  **ANSWERED THERE, NOT HERE:** codexFactory's side of the envelope was extended
  (candidate class `openxfactory-floor-regeneration`, codexFactory #282/#308)
  and PROVEN on 2026-09-09 — `codexfactory[bot]` approved #314 and that App
  approval satisfied the count-1 rulesets. **THIS LANE'S TWIN IS NOT ENROLLED.**
  `amend-mirror-floor-regeneration-merge-authority` realized the arming here
  INERT BY RULING (its box 1.3), and the enrolment successor
  `admit-review-lane-repin-to-merge-approval-envelope` (that packet's box 4.3)
  is UNFILED and needs its own word. **So the default this box names — a human
  merge word on the re-pin pull request — still holds, and holds until this box
  is ruled.**
  **2026-09-10 — TICKED on Brett Heap's word, verbatim: "same word for the
  mirror's six on #745" (extending "tick 6.1, 6.2, 6.4 and 6.3; rule on the
  rest") ([#745, comment 5618883586](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5618883586)).**
  **THE TICK IS ON THE NAMING, AND THE DEFAULT THIS BOX NAMES IS NOT
  DISTURBED BY IT — both halves of that sentence are load-bearing.** The
  successor is NAMED AND FILED:
  `openspec/changes/extend-merge-master-envelope-to-floor-bot-lanes/` is an
  ACTIVE change in this repository, governed by
  [#745](https://github.com/opensoft/openxFactory/issues/745) and opened on his
  2026-09-07 word *"Propose the extension now"*, so under the 2026-09-06
  owed-successor ruling — an owed successor's box ticks when the successor is
  NAMED — this box is discharged by that filing and by nothing else. **AND THE
  DEFAULT HOLDS FOR THIS LANE.** A human merge word on the re-pin pull request
  remains the rule here: `amend-mirror-floor-regeneration-merge-authority`
  realized the arming **INERT BY RULING** (its box 1.3), and it stays inert
  until the enrolment successor
  `admit-review-lane-repin-to-merge-approval-envelope` (that packet's box 4.3,
  **UNFILED**, needing his own word) is filed AND realized. The tick therefore
  records that the question has a named forum, not that the envelope has been
  extended to this lane — it has not — and 5.5 (a) and 5.6 both depend on that
  reading: #883 merged on his word *"merge both"* precisely because this
  default was in force on 2026-09-10, and the unattended two-repository wall
  time 5.6 cannot supply is owed to that same enrolment successor. codexFactory's
  side is separately enrolled and proven (candidate class
  `openxfactory-floor-regeneration`, codexFactory #282/#308; the App approval
  satisfied the count-1 rulesets on #314 and again on #325), which is what makes
  the asymmetry deliberate rather than an oversight.
  **THE `[x]` IS THE LANE'S PEN AND THE RULING IS HIS.**
- [x] 6.4 Install or extend the App grant the binding in 3.8 names, if M-6 stands.
  **BRETT'S ACT, AND IT IS THE ONE THING BETWEEN THIS LANE AND A FIRST FIRING.**
  The lane refuses loudly until it resolves, so nothing silently half-works. The
  App is the one already installed in both repositories
  (`secrets.OPENXFACTORY_APP_ID` / `secrets.OPENXFACTORY_APP_PRIVATE_KEY`, used
  by six workflows here). What it needs, in the APP INSTALLATION vocabulary:
  on `opensoft/codexFactory` — `contents: read`; on `opensoft/openxFactory` —
  `contents: write` and `pull_requests: write`. (The workflow `permissions:`
  spelling of the last one is `pull-requests`, hyphenated; both spellings name
  the same capability and both appear in this packet on purpose.) **It needs no
  write privilege over codexFactory and the binding declares that it must not
  have one.** No box is ticked here: an agent may not tick an owner's-act box.
  **2026-09-06 — TAKEN, IN TWO PARTS, AND THE BOX STAYS UNTICKED for the reason
  6.1's and 6.2's do.** (a) The grant this box actually names was ALREADY in
  place when the lane first fired: openxFactory run
  [34024566099](https://github.com/opensoft/openxFactory/actions/runs/34024566099)
  (schedule, 09:24Z, success) minted both tokens and ran to the correct named
  no-op, so nothing was owed on the wording above. (b) **A grant this box did
  NOT name turned out to be needed** — `workflows: write` on the openxFactory
  installation, because two of the five pinned sites are workflow files (defect
  3, recorded at 5.7). Brett Heap gave it on codexFactory
  [#232](https://github.com/opensoft/codexFactory/issues/232) at
  2026-09-06T20:25:29Z, verbatim **"granted workflows, merge 254, then report
  the re-pin sweep when it lands"**. The installation's acceptance lagged the
  word — the API still reported the old four-permission set at 22:42Z — and the
  MINT, not the API, is the ground truth: run
  [34066668104](https://github.com/opensoft/openxFactory/actions/runs/34066668104)
  (23:21Z) minted successfully and opened
  [#732](https://github.com/opensoft/openxFactory/pull/732). What the App holds
  and what the lane asks for were made equal again by
  [#726](https://github.com/opensoft/openxFactory/pull/726) → `0f9361e0`, which
  moved the binding template's grants and the mint together, the test holding
  them equal moving with them.

  **2026-09-09 — A THIRD PART, and it is why the box's own subject moved:** the
  transfer of `opensoft/codexFactory` to `codeXfactory/codexFactory` (~13:1xZ)
  voided the cross-organization read grant, and both floor lanes fail-closed at
  the mint for three hourly ticks. Brett Heap installed the App on the new
  organization at **2026-09-09T14:42:32Z** (installation `160352673`, all
  repositories, contents / pull_requests / workflows write), and the first
  `review-lane-repin` run to mint with `owner: codeXfactory` and succeed was
  [34376977439](https://github.com/opensoft/openxFactory/actions/runs/34376977439)
  (16:28:48Z, success). **THE ACT IS DONE — three times over — AND ONLY THE TICK
  IS OWED**, which is Brett Heap's; carried into the archive ledger below as
  NEEDS-BRETT (tick only).
  **2026-09-10 — TICKED on Brett Heap's word, verbatim: "same word for the
  mirror's six on #745" (extending "tick 6.1, 6.2, 6.4 and 6.3; rule on the
  rest") ([#745, comment 5618883586](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5618883586)).**
  The App grant this box names is INSTALLED AND PROVEN BY USE, not by an API
  read: the three parts recorded above — the original installation, the
  `workflows: write` addition of 2026-09-06T20:25:29Z, and the
  `codeXfactory` installation `160352673` of 2026-09-09T14:42:32Z after the
  organization move — are each evidenced by a MINT that succeeded and a run
  that went on to do its work, and the proof continued after the ruling: run
  [34477749947](https://github.com/opensoft/openxFactory/actions/runs/34477749947)
  (2026-09-10T12:37:16Z) minted both tokens and reported a clean named no-op,
  so the binding at 3.8 is resolving on the live lane on the day of this tick.
  **THE `[x]` IS THE LANE'S PEN AND THE INSTALLATION IS HIS ACT** — three
  times over, as the note above records — and the box is ticked on his word
  rather than on the lane's own reading of the installation.

## Archive assessment — 2026-09-09, NOT ARCHIVED, and the ledger that says why

**THE WORD WAS GIVEN AND THE ARCHIVE WAS NOT TAKEN, and the second fact is not
a refusal of the first.** Brett Heap, 2026-09-09 ~23:3xZ, in session, verbatim
**"archive the option-(b) packets, this lane authors it"**, over the real cycle
observed that evening: openxFactory promoted `openspec/specs/ideation-intent-plane/spec.md`
(PR [#832](https://github.com/opensoft/openxFactory/pull/832), `56e69a11`,
07:49:06Z) -> codexFactory's scheduled lane found the regeneration owed and
opened the bot pull request (#302 08:32Z, superseded by
[#314](https://github.com/codeXfactory/codexFactory/pull/314) at 21:32Z once
#310 made the diff floor-only) -> the lane armed auto-merge -> the merge-master
minted and `codexfactory[bot]` APPROVED (22:49:36Z, run 34414078939) -> the App
approval satisfied the count-1 rulesets -> auto-merge completed at
`b08958aed1d704f29f29c666142d15e653537724`, 23:27:22Z. Bot author, bot arming,
bot approval, platform merge; floor block 60 -> 61.

**THIS PACKET'S OWN `target_release:` NAMES EVIDENCE THAT DOES NOT YET EXIST,
AND THAT IS THE WHOLE REASON.** `proposal.md` declares the archive condition in
its own words — *"ONE COMPLETE CYCLE OBSERVED UNATTENDED — a real
`openspec/specs/**` promotion here, followed by a bot-opened codexFactory
regeneration pull request **and a bot-opened re-pin pull request in this
repository**, both carrying their witnesses, both merged"*. **The codexFactory
half of that sentence is now satisfied. This repository's half is not**: the
floor moved at 23:27:22Z, five minutes after the `review-lane-repin` sweep of
23:22:59Z (run 34416680260) had correctly found nothing owed, so the first
firing that can see the moved floor is the next `17 * * * *` tick. Under
`release-realization` a code-surface packet archives only on merged + green
realization evidence, and **archiving on evidence that has not been produced is
the one thing this packet has refused to do at every earlier step** (5.1 stayed
open for three days rather than tick on a `covered-pending: 0`). It is
consistent to refuse it here too.

**THE LEDGER — every box that is still open, what act it names, and whether the
act has happened.**

| Box | The act it names | Happened? | Disposition |
|---|---|---|---|
| 5.5 | Both halves merge on a human word; `covered-pending` returns to zero, quoted verbatim from the run that re-reads it. The box's own words say *"on the next main run"*; that phrase resolves to NO RUN (see below), and the reading actually arrives on the first ADVISORY `merge-master-approval` run over a base that includes the landed re-pin — the next pull request opened or synchronised after it, or a hand `workflow_dispatch` | **PART** | (a) the human-word clause is SUPERSEDED for the codexFactory half by `amend-floor-regeneration-merge-authority` — #314 merged with `mergedBy: app/openxfactory`, no human word owed; (b) this repository's re-pin has NOT opened, so there is no such base yet and no run can be quoted for `covered-pending: 0`. **Waits on an EVENT, then on Brett Heap's merge word.** |
| 5.6 | End-to-end wall time measured against the 55 min / 77 min hand cycles | **NO** | The end of the cycle is this repository's re-pin merge. The codexFactory half alone is 15 h 38 min 16 s and was attended by four repairs (#306/#307/#308/#310), a hand dispatch and an operator closing #302. LANE TIME was again ZERO. **Waits on the same event.** |
| 6.1 | Ratify or refuse this packet | **YES — 2026-09-06** | Brett Heap, *"ratify both when green, then land them"*, PR #708, head `e4ef8ade`; record `review/ratification-2026-09-06.md`. **NEEDS-BRETT (tick only)** — an agent may not tick an owner's-act box. |
| 6.2 | Rule on authoring decisions M-1..M-7 | **YES — 2026-09-06** | Stood as recommended under the ratification word; no veto in the three days since. **NEEDS-BRETT (tick only).** |
| 6.3 | Whether the merge-master low-risk envelope should ever be extended to THIS lane | **NO (successor NAMED)** | `extend-merge-master-envelope-to-floor-bot-lanes` is an ACTIVE change here, opened on the 2026-09-07 word *"Propose the extension now"*. Under the 2026-09-06 owed-successor ruling the box is TICKABLE ON THE NAMING; it sits in § 6, so the tick is his. The default — a human merge word on the re-pin — HOLDS. **NEEDS-BRETT (ruling or tick).** |
| 6.4 | Install or extend the App grant the 3.8 binding names | **YES — three times** | (a) already in place at first firing; (b) `workflows: write` granted 2026-09-06T20:25:29Z; (c) the `codeXfactory` installation `160352673` at 2026-09-09T14:42:32Z after the org move. **NEEDS-BRETT (tick only).** |

**NOT ONE OF THE SIX IS UNDONE REALIZATION OF THIS CHANGE.** Four (6.1, 6.2,
6.3, 6.4) are owner's acts, three of them already TAKEN and recorded above with
their words and dates; two (5.5, 5.6) are observations of an event that has not
occurred. **No box was ticked to satisfy a gate, none was deleted, and the
superseded human-word clause at 5.5 (a) is recorded with its superseding
mechanism rather than struck out.**

**WHAT WOULD MAKE THE ARCHIVE TAKEABLE, in order:** (1) the next `17 * * * *`
`review-lane-repin` tick opens this repository's first ARMED-INERT advance
(inert by the 1.3 ruling in `amend-mirror-floor-regeneration-merge-authority`,
which stays ACTIVE by its own gate and is untouched by this pull request);
(2) Brett Heap merges it; (3) the first ADVISORY run over a base that includes that re-pin quotes
`covered-pending: 0`, which ticks 5.5, and the completed cycle supplies 5.6's
end-to-end figure. **That run is a `merge-master-approval` run on the next pull
request opened or synchronised after the re-pin lands, or a hand
`workflow_dispatch` of it — NOT a `main`-push run, because no such run exists**:
that workflow's triggers are `pull_request_target` and `workflow_dispatch` only,
and `pytest-suite.yml`, the workflow that does run on `push: branches: [main]`,
computes no `pending_floor_extension` report (§ 3 finding 3 measured this; 5.5
(b) carries the same reading). Step (3) therefore rides ordinary pull-request
traffic, which this repository has continuously, and needs no new surface; (4) Brett Heap ticks 6.1, 6.2, 6.4 and rules or ticks 6.3.
**Then the archive is a bookkeeping act rather than a claim** — through
`scripts/proposal-support.py . archive mirror-floor-regeneration-automation`,
promoting `specs/review-lane-floor-mirror/` into
`openspec/specs/review-lane-floor-mirror/spec.md`, on the precedent of PR
[#699](https://github.com/opensoft/openxFactory/pull/699) (`b5eddaa3`).

## Archive taken — 2026-09-10, and what changed in the ledger above

**THE SECTION ABOVE IS THE RECORD OF 2026-09-09 AND IS KEPT UNCHANGED, HEADING
INCLUDED.** It says `NOT ARCHIVED` and it was right on the day it was written;
what follows is the state now, appended rather than substituted, which is the
same shape every earlier disposition in this file took.

**ALL SIX OPEN BOXES ARE CLOSED, AND NONE OF THEM ON A CLAIM THIS LANE MADE FOR
ITSELF.** Four are owner's acts ticked on Brett Heap's word of 2026-09-10,
verbatim **"same word for the mirror's six on #745"**, extending his **"tick
6.1, 6.2, 6.4 and 6.3; rule on the rest"** ([#745, comment 5618883586](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5618883586)):
6.1, 6.2, 6.3 and 6.4. Two — 5.5 and 5.6 — are the lane's rulings on the
delegation contained in *"rule on the rest"*, and each is written above with
the runs, merges and timestamps it rests on. **THE `[x]` IS THIS LANE'S PEN IN
ALL SIX CASES; the acts behind four of them are his.**

**THE FOUR-STEP CONDITION THE 2026-09-09 LEDGER SET FOR ITSELF IS MET, IN ITS
OWN ORDER.** (1) This repository's advance was produced — not by the `17 * * * *`
tick, which refused twelve times on the one-time floor relocation
(`relocate-review-authority-floor-mirror` box 4.2, measured at 5.6), but BY
HAND as [#883](https://github.com/opensoft/openxFactory/pull/883), and that
difference is recorded at 5.6 rather than smoothed over. (2) Brett Heap merged
it on his word *"merge both"* → `e916f0ea`, 2026-09-10T11:57:17Z. (3) The
first advisory run over a base carrying that re-pin —
[34475347536](https://github.com/opensoft/openxFactory/actions/runs/34475347536),
12:11:42Z — read `covered-pending:       0 (tolerance 3, pin measured)`,
repeated on two later runs, which ticks 5.5; and the completed cycle supplied
5.6 with every figure it could measure plus the named owing of the one it could
not. (4) He ticked 6.1, 6.2, 6.4 and ruled 6.3.

**WHAT THIS ARCHIVE DOES NOT CLAIM.** It does not claim a repair-free
unattended two-repository wall time — 5.6 says in its own words that none
exists yet and names the successor it is owed to. It does not claim this lane
is enrolled in the merge-master low-risk envelope — 6.3 says the arming is
INERT by ruling and the default human merge word HOLDS. It does not touch
`amend-mirror-floor-regeneration-merge-authority`, which stays ACTIVE on its
own gate with its box 4.1 waiting on the enrolment successor
`admit-review-lane-repin-to-merge-approval-envelope`, still unfiled and still
needing his word. And it deletes nothing: the superseded human-word clause at
5.5 (a), the `NOT ARCHIVED` heading above, and every earlier dated note stay
exactly as they were written.

**THE ACT ITSELF** is `python3 scripts/proposal-support.py . archive
mirror-floor-regeneration-automation --yes` from the repository root — never a
bare `openspec archive` — promoting the eight `## ADDED Requirements` in
`specs/review-lane-floor-mirror/` into
`openspec/specs/review-lane-floor-mirror/spec.md` and moving this packet to
`openspec/changes/archive/2026-09-10-mirror-floor-regeneration-automation/`,
on the precedent of PR
[#699](https://github.com/opensoft/openxFactory/pull/699) (`b5eddaa3`) that
the ledger above already named.
