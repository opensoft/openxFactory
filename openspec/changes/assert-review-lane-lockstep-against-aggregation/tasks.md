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
  SIX scenarios — an absent or foreign declaration, a stale `converged`, a
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
  workflow input. **And each value is read at its selector** (review
  `5285753827`'s *previously missed* item): the `ref:` of each `converged_with:`
  workflow's step that checks out `codeXfactory/codexFactory`, parsed as YAML,
  and the `MIGRATION_PIN` assignment in `tests/test_merge_master_workflows.py`.
  Measured on `opensoft/xFactory` `main` `6e52e98e`, each of the three files
  carries exactly ONE 40-hex literal today (`:152`, `:308`, `:72`), so a
  file-wide match would happen to work until a comment carried a second; a
  fixture with a decoy 40-hex literal in a comment of each file asserts it is
  never the one read.
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
  realization adds one, `.github/workflows/review-lane-lockstep-gate.yml`, whose
  one job is `review-lane-lockstep-gate` (`design.md` D18 names the gate's whole
  identity once). **Its trigger is not theirs** (Copilot `r4076990021`):
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
  UNDETERMINED on every run. **And the tests and declarations that fix the lane
  at two move with it, in the same realization** (Copilot `r4078098133`):
  `test_the_token_is_scoped_to_the_bindings_two_repositories` asserts exactly two
  mints and derives the declared set from the keys `source_repository` and
  `floored_repository` (`tests/review_lane_pin/test_repin_lane.py`:2384, :2393);
  `test_each_mint_requests_exactly_its_repository_grants` indexes the same two
  keys (`:2409`); and the workflow's own comment reads *"TWO TOKENS, ONE PER
  REPOSITORY THE BINDING NAMES"* (`review-lane-repin.yml`:244). Each becomes
  three, the aggregation's key beside the other two, and none is loosened to a
  count that no longer means anything.
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
  binding template, `contracts/review-lane-lockstep-gate-binding.template.yaml`,
  in the same shape: `consumer.holder_ref:
  "openxfactory:workflow:review-lane-lockstep-gate"` and `consumer.fetch_identity:
  "github-actions:openxfactory:review-lane-lockstep-gate"`; `privileges:` naming
  only the aggregation, `grants: [contents:read]` with the family's
  `never_grants:`; `resolution.scoped_to: [xFactory]`;
  `resolution.resolved_by: review_lane_lockstep_gate_workflow_only`, its statement
  naming `.github/workflows/review-lane-lockstep-gate.yml` alone; and ONE mint
  step requesting exactly `owner: opensoft`,
  `repositories: xFactory` and `permission-contents: read` — the estate's own
  per-mint down-scoping, as `review-lane-repin.yml`:276-284 mints its source read.
  The never-passed statement holds on both bindings, because nothing is passed.
  **Tests:** the gate's binding and its mint name only `xFactory` and only
  `contents: read`, in the shape of
  `test_the_token_is_scoped_to_the_bindings_two_repositories`
  (`tests/review_lane_pin/test_repin_lane.py`:2371); the advance lane's
  binding keeps its existing grants, gaining only § 5.1c's aggregation read; and
  a test holds the gate's identity together — the binding's `holder_ref` and
  `resolved_by` statement name the gate's workflow, that workflow's one job id
  and its published check-run name are the ones `design.md` D18 names, and the
  mint step lives in that job.
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
  all — and **NO author, branch or origin predicate at all** (Copilot
  `r4078145229`, and review `5285808064`'s *previously missed* item),
  **REVERSING the allowlist this box carried through two refinements**
  (`r4076740158`'s triple, `r4078098160`'s literals). This capability's promoted
  *An automated pin advance is judged by the freshness checks that already exist,
  with no exemption* (`openspec/specs/review-lane-floor-mirror/spec.md`:314-328)
  forbids every check that judges a pin advance to branch on the pull request's
  author, branch or automated origin — *"an exemption of that shape is a defect
  rather than a policy"* — and an allowlist admitting only the bot's pull
  requests is that shape exactly: a hand-authored advance would leave
  `lockstep.status` as false and draw no verdict. So the gate runs for EVERY pull
  request that changes `contracts/review-lane-pin.yaml` — a `paths:` filter,
  keyed on what the pull request changes and never on who opened it, and
  EXACTLY that one path (Copilot `r4078252960`): with the allowlist gone the
  filter is the only boundary between the aggregation token and every other pull
  request, and a broader one would mint that token and publish the aggregation's
  commits on pull requests that do not touch the pin — and its
  safety rests on the properties that do not depend on the author: base code
  only; no head checkout; the event read for the pull request's number and
  `head.sha` alone, passed through `env:` and never interpolated into a `run:`
  script; the candidate fetched from THIS repository at that `head.sha`, never
  from the head repository the event names, and parsed as inert data, judged and
  never followed (§ 5.1i); the read plan fixed in the gate's own code (§ 5.1i);
  the aggregation token
  read-only and scoped to `xFactory`; and every value the verdict names drawn
  from its grammar or its vocabulary — a CANDIDATE value outside them, public
  already, named only as an inert, length-bounded code span, its line breaks and
  backticks replaced, and a SURFACE value outside them, private, never named at
  all but only classified (§ 5.1i; `design.md` D20). `design.md` D17 records the reversal and what a fork's
  run can publish. Tests: the trigger's `paths:` filter is EXACTLY
  `[contracts/review-lane-pin.yaml]` — one entry, no glob, and no
  `paths-ignore:` — and the trigger carries no condition on author, head ref,
  base ref or head repository; a hand-authored
  pull request that changes `core_commit` draws a verdict, and so does one whose
  event names a fork as the head repository, with no request made to that
  repository; no `run:` step interpolates an event field; and a declared state
  and a `core_commit` each carrying a backtick, a line break and a link are each
  named as one inert span of bounded length.
  **AND THE TOKEN IS MINTED ONLY FOR A PULL REQUEST THAT MOVES A JUDGED VALUE**
  (Copilot `r4078308120`). The filter fires on any edit to the pin file, while
  the check judges three things in it: `core_commit`, the declared state and the
  surfaces `converged_with:` declares. **THE CANDIDATE'S DECLARATION IS
  VALIDATED FIRST, AND ONLY A VALID ONE MAY BE SKIPPED** (Copilot
  `r4078425707`): the gate parses the candidate from its inert bytes and applies
  the requirement's first outcome before anything else — a declared state absent
  or outside its two words, a `core_commit` that is not forty lowercase
  hexadecimal characters (Copilot `r4078528147`), or a `converged_with:` other
  than the read plan's two workflow members (§ 5.1i), FAILS with no token minted
  and nothing read. **A candidate that
  cannot be parsed is that outcome too** (Copilot `r4078425733`): it declares
  nothing, so it counts as ABSENT and FAILS, the parse error named as an inert,
  length-bounded span. Only a valid candidate is compared with the base's three
  values; where none moved, as with an edit to `reason:` alone, the gate mints
  nothing, reads nothing in the aggregation, and publishes the verdict as
  `skipped`, naming the values unchanged. A skip therefore needs a valid
  candidate EQUAL to its base, which leaves no invalid declaration unjudged at
  either end, and the verdict's name is present on every pull request the filter
  admits, so § 6.5's approver always finds a verdict to read. The DECLARED STATE is
  in the comparison, and not only `core_commit`, because a pull request that
  moves only the declaration is exactly one the measurement exists to check:
  `#1123` moved `status` and not `core_commit`. Tests: a candidate changing only
  `reason:` over a valid base mints nothing, reads nothing and publishes
  `skipped`; the same edit over a base whose declared state, or whose
  `converged_with:`, is outside its vocabulary FAILS instead, because the
  candidate inherits it; a candidate changing only the declared state, one
  changing only `core_commit`, and one changing only `converged_with:` each draw
  a verdict; an unparseable candidate FAILS with a bounded message, no mint
  and no read in the aggregation; and a candidate whose `core_commit` is not a
  commit, declared `diverged`, FAILS rather than agreeing, because an inequality
  against any agreed commit would otherwise report it as agreeing.
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
  base's and asserts the verdict names the CANDIDATE commit, and a second drives
  the two `head.sha` reads to DIFFER — an API sequence answering one sha before
  the fetch and another after — and asserts the refusal: no verdict is published
  for it, the push that moved the ref starting a run of its own (Copilot
  `r4078098168`). **AND THE CANDIDATE
  IS JUDGED, NEVER FOLLOWED** (Copilot `r4077898334`): the gate takes from the
  candidate only the values under judgment, and takes every path it reads in the
  aggregation from a READ PLAN FIXED IN ITS OWN CODE — because a candidate whose
  `converged_with:` chose the paths could turn the xFactory token on any file
  there and have its contents printed back as a surface's value. **AND THE BASE
  IS DATA TOO** (Copilot `r4078365046`; `design.md` D19): the base's pin file is
  only the candidate an earlier pull request proposed, and the pin's own test
  checks nothing of `converged_with:` but its length
  (`tests/review_lane_pin/test_review_lane_caller.py`:648-649), so a pull request
  changing only that list could have installed any xFactory path for every later
  run to read. The plan is therefore the gate's code: two WORKFLOW MEMBERS, the
  workflows `converged_with:` names today (`contracts/review-lane-pin.yaml`:1019-1020),
  each read at the `ref:` of its step that checks out `codeXfactory/codexFactory`;
  and one ADDITIONAL fixed read, the `MIGRATION_PIN` assignment, which is never a
  `converged_with:` member (§ 6.2; Copilot `r4078528244`). The candidate's
  `converged_with:` is JUDGED against the plan's two workflow members and never
  followed: a FAIL naming both sets where they differ,
  before anything is read. The base is not judged separately, because a
  candidate inherits the base's list unless it changes it: a base's defect FAILS
  every candidate that carries it, and a candidate that repairs it is judged on
  what it proposes. Tests: a candidate whose `converged_with:` names another
  path, and a candidate that inherits such a list from its base, each FAIL
  naming both sets with no read made in the aggregation, and neither path is
  ever requested; a candidate that repairs its base's list draws a verdict on
  the repaired list; and the current pin's two-entry `converged_with:` passes the
  judgment — the positive case — while a list that adds the constant as a third
  member FAILS. **AND A PRIVATE VALUE IS NEVER PUBLISHED** (Copilot
  `r4078468841`; `design.md` D20): a surface value that is not a commit is
  named only by its classification — absent, empty or not a commit — in the
  verdict and in the run log alike, both public on this repository. Test: a
  fixture whose surface carries a credential-shaped string publishes `not a
  commit`, and the string appears in neither the verdict nor the log.
- [ ] 5.1h **THE NEUTRAL CONCLUSION NEEDS A WRITE PATH, AND IT IS A DIFFERENT
  TOKEN FROM THE READ** (Copilot's *previously missed* item, round 5). § 5.1e
  publishes through the check-run API and § 5.1c's aggregation binding grants
  `contents:read` only — measured, no workflow in this repository grants
  `checks: write` today (`merge-master-approval.yml`:453 grants `checks: read`)
  — so the publish would 403 and INCONSISTENT/UNDETERMINED could never be
  visible as `neutral`. **The gate's OWN job declares exactly the three
  `GITHUB_TOKEN` scopes its steps use** (Copilot `r4077837498`):
  `contents: read` for the base checkout and the candidate pin fetched as bytes,
  `pull-requests: read` for re-reading `head.sha`, and `checks: write` for the verdict — because a declared `permissions:`
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
  conclusion through the check-run API, EVERY OUTCOME MAPPED and none left to the
  exit code (Copilot `r4078058050`): `failure` for a declaration outside its
  vocabulary — an unparseable candidate, a non-commit `core_commit` and a
  foreign `converged_with:` among them — and for a declaration the measurement contradicts, `neutral` for
  INCONSISTENT and for UNDETERMINED, and `success` for a declaration the
  measurement agrees with — each with the state and the values read in its
  output, a surface's as its commit or, where it is not one, only as its
  classification (§ 5.1i); and, outside the five because nothing is compared, `skipped` for a
  pin change that moves neither judged value (§ 5.1g). A test asserts the
  published conclusion for each of the five outcomes and for that case, against
  that mapping, rather than the process exit code, **because the
  contract this packet adds degrades silently to a green pass if nobody checks
  which of the two it published.** **AND THE PUBLISHED RUN IS THE GATE'S ONLY
  IDENTITY, ATTACHED TO THE CANDIDATE** (Copilot `r4076902144`, `r4077054569`;
  `design.md` D11). A published check run does not change the job's own, which
  GitHub names after the job id and which a `pull_request_target` run lands on
  the pull request's HEAD — measured, run `35788224200` on this packet's own pull
  request carries `head_sha` `918e30e3` with its job check `success` there — so a
  job that exits 0 after publishing `neutral` would leave a GREEN check on the
  commit being judged. The verdict check-run therefore carries a declared name,
  `review-lane-lockstep-verdict`, that matches NO job id in any workflow under
  `.github/workflows/`, and that name, never a job id, is the gate's identity
  wherever a check is required or read; and it is created with
  `head_sha` set to the VERIFIED candidate `head.sha` of § 5.1i, never
  `github.sha`, which in a `pull_request_target` run is the base branch's last
  commit. Tests assert the create call's `head_sha` is the verified candidate
  head, and that the verdict's name is `review-lane-lockstep-verdict` and matches
  no job id and no job `name:` in any workflow here (review `5285930613`'s *previously missed*
  item; `design.md` D18). **AND OVERLAPPING RUNS ARE SERIALIZED** (Copilot
  `r4078468867`; `design.md` D20): the workflow declares a per-pull-request
  `concurrency:` group, `review-lane-lockstep-gate-` followed by the pull
  request's number, with `cancel-in-progress: true`, as
  `merge-master-approval.yml`:427-434 does for its own verdict; and the verdict
  is published only after a final re-read of `head.sha`, so an older run can
  neither outlive a newer one nor publish for a head the pull request no longer
  has. Tests: the block's group key and its cancellation, and a run whose head
  moved before publication publishes nothing.
- [ ] 5.1b The wiring is TESTED and not assumed, ON THE GATE ITSELF (Copilot
  `r4076845535`). `test_the_head_executing_trigger_is_absent` reads
  `merge-master-approval.yml` and nothing else (`CALLER`,
  `tests/review_lane_pin/test_review_lane_caller.py`:85), so it cannot catch a
  regression in a new workflow. A test therefore reads
  `.github/workflows/review-lane-lockstep-gate.yml`'s `on:` keys and requires `pull_request_target` PRESENT and `pull_request` ABSENT, and
  requires that no step check out `github.event.pull_request.head`; and a test
  reads `review-lane-repin.yml`'s `on:` keys and requires `pull_request` to be
  ABSENT from them — the negative control that keeps the advance lane out of the
  pull-request path.
- [ ] 5.2 The comparison: `scripts/review_lane_repin.py` gains a pure function
  over the declared state, `converged_with:` against the plan's workflow members, `core_commit`
  and the surfaces' values, reaching no
  network, returning the five outcomes the scenarios name.
- [ ] 5.3 The proof: `tests/review_lane_pin/` gains a fixture for each of the
  SIX scenarios — an ABSENT or foreign declaration, an unparseable candidate, a
  non-commit `core_commit` and a candidate `converged_with:` other than the read
  plan's workflow members among them (the FAIL-without-comparison case), a stale `converged`, a stale `diverged`, surfaces disagreeing with each
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
- [~] 6.5 **AN AUTOMATED APPROVER MUST WAIT FOR THE VERDICT, AND THAT OBLIGATION
  BELONGS TO THE CHANGES THAT WOULD ADMIT THIS LANE** (Copilot `r4078145216`). A
  verdict published by a parallel `pull_request_target` run is not seen by an
  approver that read the head's checks before it existed. Measured, no such
  approver judges a pin-changing pull request today:
  `.github/merge-approval-envelope.yml` admits one candidate,
  `intent-rolling-custody` (`expected_head_ref: intents/rolling`, `:73`), whose
  admitted paths are `ideation/dashboard/intents/**` and
  `ideation/dashboard/gate-records/**` (`:115-116`), so there is no race to test
  yet. The active `admit-review-lane-repin-to-merge-approval-envelope` and
  `extend-merge-master-envelope-to-floor-bot-lanes` would create one.
  **Registered for their realization:** an approver that admits a pin-changing
  pull request approves it ONLY where the latest verdict named
  `review-lane-lockstep-verdict` (§ 5.1e) on the VERIFIED head is `success`
  (Copilot `r4078528254`). `neutral`, `skipped`, `failure`, a verdict for
  another head and no verdict at all each PARK the approval: the requirement
  says a NEUTRAL conclusion is not a pass, and the envelope's own rule already
  parks every non-excluded check run whose latest completed run is not `success`
  (`.github/merge-approval-envelope.yml`:118-127). Tests: one that runs the
  approver ahead of the verdict and asserts that it waits, and one per
  non-`success` conclusion asserting that it parks. Requiring the verdict by that name in a ruleset is the other
  route, and a ruleset act this packet does not take.
- [~] 6.6 **A PATH FILTER HAS A PLATFORM LIMIT, AND IT IS THE ONE GAP THE EXACT
  FILTER LEAVES.** GitHub's workflow-syntax reference, under
  `on.<push|pull_request|pull_request_target>.<paths|paths-ignore>` → *Git diff
  comparisons*, states it verbatim: *"If the generated diff contains more than
  3,000 files and the files the workflow filter matches are not in the first
  3,000 returned by the filter, the workflow will **not** run."* A pull request
  that large which also changed the pin would draw no verdict. That is the platform's limit, not a condition this packet adds, and it
  is registered here rather than engineered around.
