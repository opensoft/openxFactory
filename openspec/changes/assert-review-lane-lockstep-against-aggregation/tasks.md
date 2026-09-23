# Tasks: assert-review-lane-lockstep-against-aggregation

Status: draft
Kind: tasks

## 1. Ratification

- [ ] 1.1 Brett Heap's word on the requirement. **THE QUESTION IS WHICH SHAPE,
  NOT WHETHER** — the premise was verified by the lane on `#1136` and the pin
  file's own `reason:` paragraph records both remedies. This packet takes (b),
  the assertion, on the measurement at `design.md` D1: the lane has no reading of
  the aggregation, so under (a) it could only write `diverged` by inference, and
  that inference is already falsified by the fourth ceremony. (a) remains
  available and is not forbidden by this requirement.
- [ ] 1.2 On the word: `Status: ratified` + `Ratified:` in `proposal.md`,
  `Ratified by:` in `design.md` and this file, the `approved_by`/`approved_on`
  pair in `.openspec.yaml` (`scripts/doc_health/proposal_origin.py` REQUIRES the
  pair the moment the status claims approval), a record under `review/`, and the
  README Records row moved with it.

## 2. The delta

- [x] 2.1 `specs/review-lane-floor-mirror/spec.md` — ONE `## ADDED` requirement,
  SIX scenarios — an absent or foreign declared state, a stale `converged`, a
  stale `diverged`, surfaces disagreeing with each other, an unreadable
  aggregation, and the pure-function reproduction. The declared cross-repository lockstep state is MEASURED
  against the aggregation's own surfaces; the check runs at least at every
  proposed advance and its pull request; the read lives in the workflow and the
  comparison is a pure function; the check is SYMMETRIC; an unreadable
  aggregation is UNDETERMINED and never a pass; the declaration is not removed
  but becomes the subject of the measurement.
- [x] 2.2 No `## MODIFIED` block and no pairing marker — `design.md` D3. Three
  active changes carry deltas on this capability and none names this requirement
  or is named by it.

## 3. Measurement (each re-runnable, each taken on `main` `2e222d98`)

- [x] 3.1 `contracts/review-lane-pin.yaml`:714 declares `status: converged`;
  `core_commit`:60 is `b21f0100…`.
- [x] 3.2 `opensoft/xFactory` `main`: `merge-master-approval.yml`:152,
  `council-convening-lane.yml`:308 and `tests/test_merge_master_workflows.py`'s
  `MIGRATION_PIN`:72 all three return `b21f0100…`. Four sites, one commit — the
  declaration is TRUE today.
- [x] 3.3 `WRITABLE_PATHS` (`review_lane_repin.py`:196-197) is four files; within
  the pin file the lane rewrites only the regex-anchored `core_commit`,
  `floor_snapshot.sha256` and `floor_snapshot.entry_count`.
- [x] 3.4 `grep -c lockstep scripts/review_lane_repin.py` -> **0**.
- [x] 3.5 `grep -nE "opensoft/xFactory|MIGRATION_PIN|council-convening"
  scripts/review_lane_repin.py .github/workflows/review-lane-repin.yml` -> **no
  output**, and `MIGRATION_PIN` appears in no file under `scripts/` or
  `.github/workflows/`. **BEWARE THE SUBSTRING**: a bare `grep -c xFactory` on
  those two files answers 13 and 32, and every hit is `openxFactory`. The
  measurement above is the one that means anything.
- [x] 3.6 The guarding test asserts the field against a LITERAL in the test file
  (`test_the_pin_records_its_lockstep_state_with_the_aggregation_pin`), so it
  compares this repository's value to this repository's own constant.
- [x] 3.7 The 2026-09-18 false-`converged` window: `#1122` -> `38f826c2`
  (2026-09-18T20:53:37-04:00) to `#1123` -> `8184d74a` (21:27:43-04:00) =
  **34 minutes 6 seconds**, both first-parent on `main`.
- [x] 3.8 THE LIVE REPRODUCTION: `#1138` OPEN, not a draft, auto-merge armed,
  `core_commit` `b21f0100` -> `491fc54d`, four files, and
  `git diff main...bot/review-lane-repin | grep -cE "^[-+].*(lockstep|converged|diverged)"`
  -> **0**.

## 4. Gate

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate assert-review-lane-lockstep-against-aggregation --strict`.
- [x] 4.2 `validate-code-surface.py`, `validate-target-release.py`,
  `validate-sequenced-after.py`.
- [ ] 4.3 Required checks green at the head, Copilot review at the exact head
  read for its "Suppressed comments" block, every thread resolved.
- [x] 4.4 The ledger row seeded with `--moved-by '#1145'` by the sanctioned
  seeder: `active`, `sole`, `declares [mirror-floor-regeneration-automation]`,
  `depth: 2`. `sole` rather than `co-modifier` because this packet's only delta
  is a `## ADDED` requirement no other change in the corpus writes.

**§§ 1 and 4.3 KEEP A LITERAL `- [ ]` DELIBERATELY, and the archiving actor owes
them a tick.** `scripts/proposal-support.py`:4632 refuses an archive on any
remaining `^- \[ \]`. Those boxes — and every box in § 5, which is realization
work this packet declares and does not perform — are for acts that have not
happened yet, so they are ticked by the acts that perform them. Every box for
work this packet will NEVER do carries `[~]`, in § 6.

## 5. Realization, and it is NOT taken by this packet

The code surface is declared, not written. `release-realization` therefore holds
this packet's archive until merged PLUS green realization evidence.

- [ ] 5.1 The advance-side read: `.github/workflows/review-lane-repin.yml`
  obtains the aggregation's surfaces beside the source repository it already
  reads, and hands the values on as inputs, so the advance the lane proposes
  carries the measurement with it. **THE RESOLVED SHA IS WIRED AND THE WIRING IS
  TESTED** (Copilot `r4076474933`): the workflow resolves `opensoft/xFactory`'s
  DEFAULT BRANCH at run time and that branch to one commit FIRST — as
  `review-lane-repin.yml`:433-459 already resolves its source's, and never from
  an event payload, a pull-request head, a tag or a caller-supplied ref (Copilot
  `r4078009970`) — and a workflow-level test captures that resolved sha, asserts
  EVERY surface read names it, asserts the verdict names it and the branch, and
  asserts that no step takes the branch or the commit from an event payload or a
  workflow input.
  Value fixtures alone cannot catch a reader that takes each file from `main`
  independently — and that reader manufactures INCONSISTENT the moment a re-point
  lands between two calls, which is the one outcome nobody can check against
  anything. **ITS VERDICT IS RECORDED, AND THE GATE CARRIES ITS CONCLUSION**
  (Copilot `r4077837539`). The advance side publishes no check run of its own and
  gains no `checks: write`. It records the measured values, the resolved
  aggregation commit and the outcome in the pull-request body the lane already
  composes (`--body-out`, `review-lane-repin.yml`:597; `gh pr edit` /
  `gh pr create --body-file`, `:840-861`), and the CONCLUSION for that advance is
  the gate's, on the same head: the lane pushes with its App token, and an
  App-token push starts `pull_request_target` runs — measured on `#1138`, whose
  head carries a `merge-master-approval` run with event `pull_request_target`
  triggered by `openxfactory[bot]`. A second check run for one fact on one commit
  would be a second identity for one verdict, which § 5.1e forbids. Tests: the
  lane's body carries the verdict, and the gate's `pull_request_target` trigger
  covers `opened`, `synchronize` and `reopened`.
- [ ] 5.1a **THE PULL-REQUEST-SIDE HOST, AND IT IS A SECOND WORKFLOW THAT TAKES
  ITS OWN READING** (Copilot `r4075976980`, `r4076152645`). It is a SEPARATE
  WORKFLOW RUN and therefore cannot consume the scheduled run's step outputs, so
  it performs the same cross-repository read itself and passes the values to the
  same pure comparison; § 5.1's read serves the advance the lane proposes and
  nothing else. Two reads of one fact by two runs is the cost of the split, and
  it is cheaper than a shared artifact whose staleness would need its own rule. Measured: `review-lane-repin.yml`'s `on:` keys are exactly
  `['schedule', 'repository_dispatch', 'workflow_dispatch']` — the only
  `pull_request` string in that file is a comment at `:672`, which is why a
  line-oriented grep for it answers misleadingly. So § 5.1 alone leaves the
  requirement's *"and the pull request that carries it"* clause unrealized: the
  lane's own advance could open a pull request with no check running ON that
  pull request. The estate's own pattern answers it — a pin gate is its OWN
  workflow (`openspec-cli-pin-gate.yml`, `openreposhape-pin-gate.yml`) — so the
  realization adds one. **Its trigger is not theirs** (Copilot `r4076990021`):
  those two run on `pull_request` because neither holds a secret (zero `secrets.`
  references in either), while this gate holds a credential that reads a PRIVATE
  repository, so it runs on `pull_request_target` and never on `pull_request`
  (§ 5.1g). And `review-lane-repin.yml` does NOT gain a `pull_request` trigger,
  which would fire the advance logic on every pull request in the repository.
- [ ] 5.1c **THE ACCESS PATH, AND WITHOUT IT THE WHOLE PACKET IS INERT** (Copilot
  `r4076152594`). Measured: `opensoft/xFactory` is **PRIVATE**
  (`gh api repos/opensoft/xFactory --jq .visibility` -> `private`; an
  unauthenticated `raw.githubusercontent` read of a surface returns **404**), and
  `contracts/review-lane-repin-binding.template.yaml` declares
  `source_repository: codeXfactory/codexFactory` with `grants: [contents:read]`
  and nothing for the aggregation. **So on today's credentials the check would
  answer UNDETERMINED on every run** — a check that never concludes, which the
  requirement now forbids as a standing state. The realization declares a
  READ-ONLY binding for `opensoft/xFactory` in the same shape as the existing
  source-repository grant — `grants: [contents:read]`,
  `never_grants: [contents:write, actions:write, pull-requests:write]` — which is
  also what keeps the family's own rule intact: *"neither repository's lane may
  reach into the other's"*. The aggregation is READ and never written, by this
  packet or by its realization. **AND A MINT TO USE IT** (Copilot
  `r4077898366`): `review-lane-repin.yml` mints two tokens today, the codexFactory
  read and its own write (`:276-311`), so it gains a THIRD — `owner: opensoft`,
  `repositories: xFactory`, `permission-contents: read` — held by a test in the
  same shape as the other two. A grant with no mint leaves the advance-side read
  UNDETERMINED on every run.
  **AND BOTH RUNS NEED THE READ, NOT ONE** (Copilot `r4076254027`). § 5.1a's
  pull-request gate is a SEPARATE WORKFLOW RUN: it cannot reuse the advance lane's
  minted App token any more than it can reuse its step outputs, and the ambient
  `GITHUB_TOKEN` cannot read a private `opensoft/xFactory` at all — so a binding
  written for the repin identity alone would leave the PR-side check UNDETERMINED
  on every run, which is the very defect this box exists to close, one workflow
  over. The gate therefore mints its OWN token from the same App
  (`actions/create-github-app-token`, as `review-lane-repin.yml` already does at
  `:278` and `:303`) under a binding of its OWN (§ 5.1f), and a test asserts THE
  PULL-REQUEST SIDE's read succeeds rather than only the advance side's. **The
  two runs share an App identity and nothing else: no token, no outputs and no
  privilege set.**
- [ ] 5.1f **THE GATE'S CREDENTIAL IS A BINDING OF ITS OWN, NOT A SECOND CONSUMER
  UNDER THE ADVANCE LANE'S — REVISING THIS PACKET'S OWN EARLIER SHAPE** (Copilot
  `r4076368784`, then `r4076990082`). Measured:
  `contracts/review-lane-repin-binding.template.yaml` carries
  `consumer.holder_ref: "openxfactory:workflow:review-lane-repin"` (`:100`),
  `resolution.resolved_by: review_lane_repin_workflow_only` (`:167`) and a
  statement that the minted token is *"never passed to a second workflow"*
  (`:190`) — and, the part the earlier shape missed, its `privileges:` (`:109`)
  and `resolution.scoped_to` (`:180`) sit at the BINDING's top level, with
  `floored_repository` granting `contents:write`, `pull-requests:write` and
  `workflows:write` (`:154`). **So a second consumer entry would mint with the
  advance lane's write authority over this repository.** The gate gets its OWN
  binding template in the same shape: `privileges:` naming only the aggregation,
  `grants: [contents:read]` with the family's `never_grants:`;
  `resolution.scoped_to: [xFactory]`; `resolved_by` naming the gate's workflow id
  alone; and ONE mint step requesting exactly `owner: opensoft`,
  `repositories: xFactory` and `permission-contents: read` — the estate's own
  per-mint down-scoping, as `review-lane-repin.yml`:276-284 mints its source read.
  The never-passed statement holds on both bindings, because nothing is passed.
  **Tests:** the gate's binding and its mint name only `xFactory` and only
  `contents: read`, in the shape of
  `test_the_token_is_scoped_to_the_bindings_two_repositories`
  (`tests/review_lane_pin/test_repin_lane.py`:2371); and the advance lane's
  binding keeps its existing grants, gaining only § 5.1c's aggregation read.
- [ ] 5.1g **THE GATE USES `pull_request_target`, NEVER `pull_request`, AND
  TAKES NO HEAD CHECKOUT — REVERSING THIS PACKET'S OWN EARLIER DECISION**
  (Copilot `r4076368722`, then `r4076474882`). The earlier draft refused
  `pull_request_target` by name and scoped a plain `pull_request` gate to
  same-repository events. **That was wrong on this repository's own doctrine, and
  the doctrine is a RUNNING TEST**: `tests/review_lane_pin/test_review_lane_caller.py`
  `test_the_head_executing_trigger_is_absent` refuses a plain `pull_request`
  trigger on the secret-bearing caller, verbatim — *"a plain `pull_request`
  trigger would run the head's copy of this file with the App credential that
  reads a private repository in scope — the exfiltration shape the base-branch
  rule prevents"* — and `EXPECTED_TRIGGERS` is `{"pull_request_target",
  "workflow_dispatch"}`. A same-repository head-ref condition does not fix that,
  because under `pull_request` the head's copy of the WORKFLOW runs and can
  simply delete the condition. So the gate takes the estate's worked shape:
  **`pull_request_target`** (the BASE's copy of the workflow runs, so a head
  cannot rewrite it), **no checkout of `github.event.pull_request.head`** —
  mirroring `test_no_checkout_takes_the_pull_request_head`, and easy here because
  the check reads two repositories over the API and needs no candidate code at
  all — and an **allowlist**, refined below from a head ref to a triple, plus the
  same-repository condition as defence in depth, with a test that a
  same-repository NON-BOT pull request is skipped.
  **AND THE ALLOWLIST IS A TRIPLE, NOT A HEAD REF** (Copilot `r4076740158`): a
  head ref alone is a predicate anyone who can create or update that branch can
  satisfy, so the same writer could open a DIFFERENT pull request under the
  allowlisted name and run the base workflow with the token; and an unfiltered
  base would expose the same path on any branch. The estate already states the
  shape — `.github/merge-approval-envelope.yml`:70-74 requires `expected_author`,
  `expected_head_ref` AND `expected_base_ref` together, held by
  `tests/review_lane_pin/test_review_lane_caller.py`:780-789, whose own words
  call the exact head ref *"half of the fork defence"* — **half, which is the
  point**. The gate's condition is therefore the same triple: the advance lane's
  bot as author, the exact head ref, and `main` as base, each an exact value and
  none a pattern, with a test per predicate driving a pull request that satisfies
  the other two and fails this one. A fork event and a
  non-allowlisted head are both reported OUT OF SCOPE rather than UNDETERMINED:
  *not applicable* and *could not measure* are different answers, and this
  packet's whole subject is not conflating them.
- [ ] 5.1i **THE GATE READS THE CANDIDATE PIN, NOT THE BASE'S — AND THIS IS THE
  DEFECT `pull_request_target` INTRODUCED** (Copilot's *previously missed* item,
  round 8). Under `pull_request_target` the workflow runs from the BASE, so a
  gate that parses the checked-out `contracts/review-lane-pin.yaml` reads the
  commit ALREADY IN PLACE. Measured against the live reproduction: for `#1138`
  that is base `b21f0100` compared to the aggregation's `b21f0100` — **PASS,
  while the advance it exists to judge proposes `491fc54d` and is never seen.**
  The gate would have been decorative in exactly the case it was built for.
  The gate therefore FETCHES the candidate `contracts/review-lane-pin.yaml` as
  **INERT BYTES at the verified `head.sha`** — a file read over the API, not a
  checkout and not an execution — **parses it with BASE code**, and **re-reads
  `head.sha` after the fetch**, refusing where a force-push moved the ref between
  the two. The base-branch rule is kept exactly: no head CODE runs, and reading
  head DATA as bytes is what makes `pull_request_target` usable rather than
  merely safe. An end-to-end test drives a candidate whose pin differs from the
  base's and asserts the verdict names the CANDIDATE commit. **AND THE CANDIDATE
  IS JUDGED, NEVER FOLLOWED** (Copilot `r4077898334`): the gate takes from the
  candidate only `core_commit` and the declared state, and takes every path it
  reads in the aggregation from the BASE's `converged_with:` and its own fixed
  location for `MIGRATION_PIN` — because a candidate whose `converged_with:` chose
  the paths could turn the xFactory token on any file there and have its contents
  printed back as a surface's value. A test drives a candidate whose
  `converged_with:` names another path and asserts that no path from the
  candidate is read.
- [ ] 5.1h **THE NEUTRAL CONCLUSION NEEDS A WRITE PATH, AND IT IS A DIFFERENT
  TOKEN FROM THE READ** (Copilot's *previously missed* item, round 5). § 5.1e
  publishes through the check-run API and § 5.1c's aggregation binding grants
  `contents:read` only — measured, no workflow in this repository grants
  `checks: write` today (`merge-master-approval.yml`:453 grants `checks: read`)
  — so the publish would 403 and INCONSISTENT/UNDETERMINED could never be
  visible as `neutral`. **The gate's OWN job declares exactly the three
  `GITHUB_TOKEN` scopes its steps use** (Copilot `r4077837498`):
  `contents: read` for the base checkout and the candidate pin fetched as bytes,
  `pull-requests: read` for re-reading `head.sha` and the triple's author and
  refs, and `checks: write` for the verdict — because a declared `permissions:`
  block sets every undeclared scope to `none` (`merge-master-approval.yml`:448-449),
  so `checks: write` alone would leave the gate unable to reach the comparison.
  **The aggregation read token stays read-only and gains nothing**, because the
  thing being written is a check run in this repository and the thing being read
  is another repository. Tests: the job's block is exactly those three, and the
  published check-run path is exercised.
- [ ] 5.1d **A READ FAILURE IS AN INPUT, NEVER A FATAL STEP** (Copilot
  `r4076152544`). The advance workflow treats a non-404 API failure as step-fatal,
  so an auth error, a rate limit or a transport failure would abort before the
  pure comparison ever runs — and the UNDETERMINED scenario would be unreachable
  by the only route that reaches it. The realization makes every read outcome,
  including its failures, an INPUT to the comparison naming what could not be
  read, and a workflow-level test exercises that path.
- [ ] 5.1e **THE NEUTRAL CONCLUSION NEEDS A REPRESENTATION** (Copilot
  `r4076152473`). A GitHub Actions step exits 0 or non-zero, which is a green
  pass or a red failure and nothing else, so *"NEUTRAL, visible, not reported as
  a pass"* has no expression by exit code alone. The realization publishes the
  conclusion through the check-run API — conclusion `neutral`, with the state and
  the values read in its output — and a test asserts the published conclusion for
  each of the five outcomes rather than the process exit code, **because the
  contract this packet adds degrades silently to a green pass if nobody checks
  which of the two it published.** **AND THE PUBLISHED RUN IS THE GATE'S ONLY
  IDENTITY, ATTACHED TO THE CANDIDATE** (Copilot `r4076902144`, `r4077054569`;
  `design.md` D11). A published check run does not change the job's own, which
  GitHub names after the job id and which a `pull_request_target` run lands on
  the pull request's HEAD — measured, run `35788224200` on this packet's own pull
  request carries `head_sha` `918e30e3` with its job check `success` there — so a
  job that exits 0 after publishing `neutral` would leave a GREEN check on the
  commit being judged. The verdict check-run therefore carries a declared name
  that matches NO job id in the workflow, and that name, never a job id, is the
  gate's identity wherever a check is required or read; and it is created with
  `head_sha` set to the VERIFIED candidate `head.sha` of § 5.1i, never
  `github.sha`, which in a `pull_request_target` run is the base branch's last
  commit. Tests assert the create call's `head_sha` is the verified candidate
  head, and that the verdict's name matches no job id.
- [ ] 5.1b The wiring is TESTED and not assumed, ON THE GATE ITSELF (Copilot
  `r4076845535`). `test_the_head_executing_trigger_is_absent` reads
  `merge-master-approval.yml` and nothing else (`CALLER`,
  `tests/review_lane_pin/test_review_lane_caller.py`:85), so it cannot catch a
  regression in a new workflow. A test therefore reads the new gate's `on:` keys
  and requires `pull_request_target` PRESENT and `pull_request` ABSENT, and
  requires that no step check out `github.event.pull_request.head`; and a test
  reads `review-lane-repin.yml`'s `on:` keys and requires `pull_request` to be
  ABSENT from them — the negative control that keeps the advance lane out of the
  pull-request path.
- [ ] 5.2 The comparison: `scripts/review_lane_repin.py` gains a pure function
  over the declared state, `core_commit` and the surfaces' values, reaching no
  network, returning the five outcomes the scenarios name.
- [ ] 5.3 The proof: `tests/review_lane_pin/` gains a fixture for each of the
  SIX scenarios — an ABSENT or foreign declared state (the FAIL-without-comparison
  case), a stale `converged`, a stale `diverged`, surfaces disagreeing with each
  other, an unreadable aggregation — including surfaces that AGREE on a value that
  is not a commit, the empty string among them (`design.md` D16) — and the
  pure-function reproduction — **plus
  the POSITIVE case, a true `converged` and a true `diverged` each reported as
  agreeing**, so the check is proved to accept a correct declaration and not only
  to refuse a wrong one. **Each written to FAIL against the pre-fix reader and
  pass after**, so the regression is proved rather than asserted.
- [ ] 5.4 ONE real observation of the check running against a proposed advance
  **and CONCLUDING** — `converged`, `diverged` or a named contradiction, and NOT
  UNDETERMINED. That is the half that cannot be manufactured, and the conclusion
  is part of it: an observation of the check answering UNDETERMINED proves the
  access is missing, not that the check works.

## 6. Registered, not taken

- [~] 6.1 The `obligation:` field's clause *"Advance this pin only at such a
  ceremony"* is still in tension with the hourly lane, and the pin file says so:
  *"Narrowing that clause is the ratifier's act, not this diff's."* **Still true,
  and a DIFFERENT act.** This packet makes the state measurable, which is what
  lets that clause be narrowed on evidence rather than on argument. Not narrowed
  here.
- [~] 6.2 `converged_with:` names TWO surfaces and gains no third entry for the
  `MIGRATION_PIN` constant. The check reads all three (`design.md` D5), but
  promoting the constant to a converged-with member is the pin owner's call and
  the field has been through three cycles without it.
- [~] 6.3 The pin file's `reason:` narrative says a false status *"survives in
  EITHER direction until a human notices, and why 2026-09-18's took eleven
  days."* **This packet does not repeat that figure and does not correct it.**
  Measured here, the false-`converged` window on 2026-09-18 was 34 minutes 6
  seconds (§ 3.7); the eleven days is the interval between the 2026-09-10 and
  2026-09-21 convergences, which is a different quantity. The field is append-only
  and its dated paragraphs are records; correcting one is neither this packet's
  act nor its subject. Registered so the next reader of that sentence finds the
  arithmetic already done.
- [~] 6.4 `#1138` is not this packet's to land, hold or amend. It is cited as the
  live reproduction and nothing here asks for an act on it.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
