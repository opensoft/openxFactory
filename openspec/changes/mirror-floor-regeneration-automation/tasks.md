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

**2.1 AND 2.2 STAY OPEN, AND NOT FOR WANT OF WORK HERE.** The packet is
ratified (codexFactory #235, merge commit `ffc090d0`); its REALIZATION is being
authored concurrently by a sibling lane on branch
`realize/add-floor-regeneration-automation`. Nothing in this repository waits on
it, and this lane claims none of it. Until it lands, the cycle is HALVED rather
than closed: the re-pin is proposed automatically and the regeneration is still
a hand act — stated without hedging, in the same terms the parent packet uses
about itself.

- [ ] 2.1 `codexFactory: add-floor-regeneration-automation` is ratified and
  realized: the regeneration lane runs the shipped generator at a LANDED
  openxFactory `main` commit and opens the regeneration pull request itself.
- [ ] 2.2 That lane's additions-only and block-confinement refusals are landed
  and tested there, not here.
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

- [ ] 5.1 A real `openspec/specs/**` promotion lands here and the advisory lane
  reports `pending_floor_extension` with a non-zero count — quoted verbatim.
- [ ] 5.2 The codexFactory regeneration pull request is opened BY THAT LANE, with
  no operator running the generator.
- [ ] 5.3 The re-pin pull request is opened BY THIS LANE, with no operator
  copying a digest; the five sites are verified by reading them back from the
  merged commit, not from the lane's own report.
- [ ] 5.4 The required suite judges that pull request GREEN with no exemption —
  and the byte-identity freshness verifier is confirmed to have RUN, by name, on
  it.
- [ ] 5.5 Both merge on a human word, and `covered-pending` returns to zero on
  the next main run — quoted verbatim from that run.
- [ ] 5.6 The end-to-end wall time is measured and recorded against the two hand
  cycles in `proposal.md` § Why (55 min and 77 min).
- [ ] 5.7 ONE observed refusal on a real run, of any kind (non-landed core, a
  site that did not move, an unresolved binding), quoted verbatim — or the box
  stays OPEN and says so rather than being ticked on a test-only observation.

## 6. Owner's acts (not an agent's)

- [ ] 6.1 Ratify or refuse this packet. The 2026-09-05 word authorized the
  PROPOSING, not the content.
  **2026-09-06 — TAKEN. Brett Heap ratified it in session, verbatim "ratify both
  when green, then land them" — a PAIR word over this companion and codexFactory
  #235 together, recorded 2026-09-06T01:18Z on PR #708 over head `e4ef8ade`, its
  `pytest-suite` condition met. The packet is now `Status: ratified` and the
  record is `review/ratification-2026-09-06.md`. The box is left UNTICKED
  deliberately — ticking an owner's-act box is a claim an agent may not make
  about the owner, and this dated note is how the act is recorded instead.**
- [ ] 6.2 Rule on the authoring decisions M-1 through M-7, and in particular on
  M-7 (the lane writes no comment-history paragraph, so eight advances of
  narrative in `contracts/review-lane-pin.yaml` stop accruing) and on M-1's
  schedule location.
  **2026-09-06 — STOOD. Under the ratification word, M-1 through M-7 stand as
  recommended and no veto was exercised; each remains one edit away. The box
  stays UNTICKED for the same reason 6.1's does.**
- [ ] 6.3 SEPARATE AND NOT ASKED FOR HERE: whether the merge-master low-risk
  envelope — live today only for the doc-health nightly lane — should ever be
  extended to this lane. The default is a human merge word, and it holds until
  this box is ruled. Named so the question is not silently assumed either way,
  and noting that `contracts/review-lane-pin.yaml` is itself a never-clearable
  floor entry whose stated ground is that a clearable pin *"would let a pull
  request choose its own judge"*.
- [ ] 6.4 Install or extend the App grant the binding in 3.8 names, if M-6 stands.
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
