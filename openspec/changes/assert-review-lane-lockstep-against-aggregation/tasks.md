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
  five scenarios. The declared cross-repository lockstep state is MEASURED
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
  TESTED** (Copilot `r4076474933`): the workflow resolves the aggregation's
  branch to one commit FIRST, and a workflow-level test captures that resolved
  sha, asserts EVERY surface read names it, and asserts the verdict names it too.
  Value fixtures alone cannot catch a reader that takes each file from `main`
  independently — and that reader manufactures INCONSISTENT the moment a re-point
  lands between two calls, which is the one outcome nobody can check against
  anything.
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
  `pull_request`-triggered workflow (`openspec-cli-pin-gate.yml`,
  `openreposhape-pin-gate.yml`), each a required check — so the realization adds
  one, and `review-lane-repin.yml` does NOT gain a `pull_request` trigger, which
  would fire the advance logic on every pull request in the repository.
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
  packet or by its realization.
  **AND THE BINDING COVERS BOTH RUNS, NOT ONE** (Copilot `r4076254027`). § 5.1a's
  pull-request gate is a SEPARATE WORKFLOW RUN: it cannot reuse the advance lane's
  minted App token any more than it can reuse its step outputs, and the ambient
  `GITHUB_TOKEN` cannot read a private `opensoft/xFactory` at all — so a binding
  written for the repin identity alone would leave the PR-side check UNDETERMINED
  on every run, which is the very defect this box exists to close, one workflow
  over. The gate therefore mints its OWN token from the same App
  (`actions/create-github-app-token`, as `review-lane-repin.yml` already does at
  `:278` and `:303`) under the same read-only scope, the binding NAMES BOTH
  CONSUMERS, and a test asserts THE PULL-REQUEST SIDE's read succeeds rather than
  only the advance side's. **The two runs share an identity and a scope; they
  share no token and no outputs.**
- [ ] 5.1f **THE BINDING IS STRUCTURALLY SINGLE-CONSUMER AND THE SECOND
  CONSUMER IS A SECOND ENTRY, NOT A SHARED TOKEN** (Copilot `r4076368784`).
  Measured: `contracts/review-lane-repin-binding.template.yaml` carries
  `consumer.holder_ref: "openxfactory:workflow:review-lane-repin"` (`:100`),
  `resolution.resolved_by: review_lane_repin_workflow_only` (`:167`) and a
  statement that the minted token is *"never passed to a second workflow"*
  (`:190`). Saying the binding "names both consumers" without saying HOW would
  let an implementation add the privilege under a contract that still denies it.
  **The representation is a SECOND CONSUMER ENTRY with its own `holder_ref`
  (`openxfactory:workflow:<the gate>`) and its own mint**, `resolved_by` widened
  to name both workflows by id, and the never-passed statement **carried
  UNCHANGED** — because nothing is passed: each workflow mints its own token from
  the same App under the same read-only scope. The statement is honoured by the
  design rather than amended around. Its tests move with it.
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
  all — and a **head-ref allowlist** (`bot/review-lane-repin`) plus the
  same-repository condition as defence in depth, with a test that a
  same-repository NON-BOT pull request is skipped. A fork event and a
  non-allowlisted head are both reported OUT OF SCOPE rather than UNDETERMINED:
  *not applicable* and *could not measure* are different answers, and this
  packet's whole subject is not conflating them.
- [ ] 5.1h **THE NEUTRAL CONCLUSION NEEDS A WRITE PATH, AND IT IS A DIFFERENT
  TOKEN FROM THE READ** (Copilot's *previously missed* item, round 5). § 5.1e
  publishes through the check-run API and § 5.1c's aggregation binding grants
  `contents:read` only — measured, no workflow in this repository grants
  `checks: write` today (`merge-master-approval.yml`:453 grants `checks: read`)
  — so the publish would 403 and INCONSISTENT/UNDETERMINED could never be
  visible as `neutral`. The gate's OWN job grants least-privilege `checks: write`
  in its `permissions:` block; **the aggregation read token stays read-only and
  gains nothing**, because the thing being written is a check run in this
  repository and the thing being read is another repository. A test exercises the
  published check-run path.
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
  each of the four outcomes rather than the process exit code, **because the
  contract this packet adds degrades silently to a green pass if nobody checks
  which of the two it published.**
- [ ] 5.1b The wiring is TESTED and not assumed: a test reads the new gate's
  `on:` keys and its job id, and a test reads `review-lane-repin.yml`'s `on:`
  keys and requires `pull_request` to be ABSENT from them — the negative control
  that keeps the advance lane out of the pull-request path.
- [ ] 5.2 The comparison: `scripts/review_lane_repin.py` gains a pure function
  over the declared state, `core_commit` and the surfaces' values, reaching no
  network, returning the four outcomes the scenarios name.
- [ ] 5.3 The proof: `tests/review_lane_pin/` gains a fixture for each of the
  FIVE scenarios — stale `converged`, stale `diverged`, surfaces disagreeing with
  each other, unreadable aggregation, and the pure-function reproduction — **plus
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
