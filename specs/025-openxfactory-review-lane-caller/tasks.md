# Tasks: openxFactory review-lane caller (advisory)

**Input**: Design documents from `specs/025-openxfactory-review-lane-caller/`
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md)

## 1. Recon and pin selection

- [x] 1.1 Record the codexFactory commit the pin will name, and prove the two
      artifacts the caller depends on exist AT that commit and NOT at xFactory's
      `3c35ca8b`: `scripts/merge_master/repository_floor.py` and
      `scripts/merge_master/openxfactory-review-authority-floor.yaml`.
      (D2 — the divergence must be forced, not asserted.)
- [x] 1.2 Record the secret/variable reality for `opensoft/openxFactory`:
      which identifiers exist at repo level, which org secrets are
      visibility-`selected` and to which repositories. Do NOT create any
      secret. (D5.)

## 2. The pin artifact

- [x] 2.1 `contracts/review-lane-pin.yaml` — `schema_version: 1`,
      `kind: pinned_workflow`, `repository: opensoft/codexFactory`,
      `core_commit: <40 hex>`, `revision_kind: commit`, `declared_at`,
      the caller path the pin governs, the two pinned members the caller reads,
      and the lockstep note naming xFactory's two diverging surfaces.
      EXACTLY ONE 40-hex value in the file (D7).
- [x] 2.2 One `PinMember` in `scripts/doc_health/pin_class.py`'s `PIN_CLASS`:
      `paths=("contracts/review-lane-pin.yaml",)`, `key="core_commit"`,
      `key_form="field"`, `reproduction=MEASURED`,
      `locality=CROSS_REPOSITORY`, `presence=CURRENT`, with a note saying why a
      codexFactory commit must never be expected to resolve here.
      Follows `openxwallet-pin-product-commit` (D7).
- [x] 2.3 `.github/CODEOWNERS` — route `/contracts/review-lane-pin.yaml` to
      `@brettheap`, on the 2026-08-23 ruling's ground: a pull request that
      changes it changes the code a governance surface executes (FR-013).

## 3. The advisory caller

- [x] 3.1 `.github/workflows/merge-master-approval.yml`, ONE job whose id is
      exactly `merge-master-approval` (FR-001, FR-011). Triggers:
      `pull_request_target` `[opened, reopened, synchronize]`, plus
      `workflow_dispatch` with an optional `pr_number`. Serialized by a
      `concurrency` group. Permissions: `contents: read`, `pull-requests: read`
      and nothing that could approve or merge (FR-007).
- [x] 3.2 Preflight: resolve the decision-core read credential — the
      repository's own content App first, the org App second — and FAIL with
      the missing identifiers NAMED when neither is present (FR-010, D5).
- [x] 3.3 Checkout this repository from the base branch (no `ref:`), then
      checkout `opensoft/codexFactory` at the pinned `core_commit` into
      `.merge-master-core` (FR-002, FR-003).
- [x] 3.4 Runtime pin agreement: read `contracts/review-lane-pin.yaml` from the
      base checkout and refuse the run if its `core_commit` differs from the
      commit the workflow just checked out. The test is the primary guard; this
      is the second, so a hand-edited workflow cannot judge a pull request under
      a core the pin does not name.
- [x] 3.5 Resolve the candidate pull request from the event payload
      (`pull_request_target`) or from the dispatch input, and PARK with a named
      reason when no pull request can be resolved.
- [x] 3.6 Gather the changed-path set PROVABLY COMPLETE (FR-009, D6):
      authoritative `.changed_files` and head SHA from ONE read of the
      pull-request resource; paginated REST file listing with shape proof;
      `previous_filename` folded into the judged set; entry count compared
      against the declared total; head-SHA recheck after pagination. No
      failure masking anywhere — every gather failure parks with its reason.
- [x] 3.7 Evaluate the floor with the pinned core: import
      `merge_master.repository_floor`, load
      `.merge-master-core/scripts/merge_master`, select the floor whose
      `repository` is `opensoft/openxFactory`, supply the repository tree
      listing so an unreachable floor path is a named failure rather than
      silence, and compute the matched paths (FR-006).
- [x] 3.8 Render the advisory verdict to `$GITHUB_STEP_SUMMARY`: the pinned
      commit, the floor id, the changed-path count, the matched floored paths
      by name, and an explicit statement that nothing was approved and no
      ruleset consumes this check.
- [x] 3.9 Anti-vacuity assertion, mirroring
      `openxwallet-consumer-gate.yml`'s final step: fail unless the run
      positively evidenced that it read the floor from the pinned core — a
      POSITIVE conjunction, never "did not fail".
- [x] 3.10 Confirm by inspection that the file contains no step that mints an
      approving token, submits a review, calls merge, or enables auto-merge
      (FR-007). Absence is the mechanism; the test in §4 pins it.

## 4. The test

- [x] 4.1 `tests/review_lane_pin/test_review_lane_caller.py`. NO `pytest.skip`
      anywhere — the CI gate pins the suite's skip count EXACTLY, and a skip
      reports as a green bar (SC-006).
- [x] 4.2 Pin agreement: the workflow's pinned `ref:` equals the pin file's
      `core_commit`; the failure message names both values and the file to
      change (FR-005).
- [x] 4.3 Pin shape: `kind: pinned_workflow`, `repository`,
      `revision_kind: commit`, a 40-lowercase-hex `core_commit`, an ISO date
      `declared_at`, and the governed caller path — which must be the file that
      exists. Missing or malformed pin FAILS, never skips.
- [x] 4.4 Exactly ONE 40-hex value in the pin file, so the single declared
      pin-class member covers it (D7).
- [x] 4.5 The pin-class member exists and is declared `CROSS_REPOSITORY` with
      `key="core_commit"` and this pin's path.
- [x] 4.6 Caller invariants: parses as YAML; exactly one job; its id is exactly
      `merge-master-approval`; the trigger set is exactly the intended one;
      `pull_request` (the head-executing trigger) is ABSENT; no
      `permissions:` grant that could write a review or merge.
- [x] 4.7 The approval-shaped absence, asserted as a denylist over the file
      text: no `create-github-app-token` step naming the merge-master App, no
      `gh pr review`, no `gh pr merge`, no `pulls/.../reviews` POST, no
      `--auto`, no `enablePullRequestAutoMerge`.
- [x] 4.8 Embedded shell parses: every `run:` block that is bash passes
      `bash -n`. Not conditioned on a `which bash` probe (that would be a skip).
- [x] 4.9 CODEOWNERS routes the pin path.
- [x] 4.10 Negative controls in a scratch tree so each positive is one mutation
      from failing: a drifted `ref:`, a malformed pin, a two-job caller.

## 5. Validation and exit

- [x] 5.1 `python3 -m pytest tests/review_lane_pin -q` green, then the whole
      suite's collection is unbroken (`--collect-only -q` count) and the new
      module adds ZERO skips.
- [x] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green — this
      feature adds no OpenSpec change, so the assertion is that it breaks
      nothing.
- [x] 5.3 `actionlint` if obtainable; record explicitly if it is not available
      in this environment rather than implying it passed.
- [x] 5.4 The new YAML parses under the pinned wallet syntax gate, which runs
      on every pull request via the required `wallet-validation` check.
- [x] 5.5 Commit, push, open the pull request against `main`. Body states what
      the caller does and does NOT do, the pinned commit and why it diverges
      from xFactory's, and the exact secret status. Do NOT merge.
- [x] 5.6 Watch the pull request's checks. RECORD HONESTLY that
      `merge-master-approval` cannot report on this pull request, because
      `pull_request_target` runs the base-branch definition and this file is not
      on the base branch yet (D4) — and name the first pull request after the
      merge as where the live report appears.

## 6. Named follow-ups, not performed here

> **"Not performed HERE" means not by this feature — it does not mean not done.**
> As of 2026-08-28: **6.2 is COMPLETE** (in codexFactory, PR #125, merge
> `99fa3ffe`). **6.1, 6.4 and 6.5 remain OPEN.** **6.3 remains OPEN** and its
> gate is unchanged — the `gate_rules_council` convened 2026-08-28 and REFUSED
> the class proposed to it, so `add-substantive-review-lane` task 3.2 stays open
> and FR-008 stays gated. Each box below states its own current status.

- [ ] 6.1 Grant `opensoft/openxFactory` read access to the private decision
      core — either by adding it to the `selected` list for
      `XFACTORY_APP_ID` / `XFACTORY_APP_PRIVATE_KEY`, or by installing the
      repository's own content App on `opensoft/codexFactory`. Operator act;
      no secret is created by this feature.
- [x] 6.2 codexFactory side: add `contracts/review-lane-pin.yaml` to
      `scripts/merge_master/openxfactory-review-authority-floor.yaml`'s
      `never_clearable_paths`. It determines which core judges this repository,
      which is the same argument the wallet pin's entry already makes
      (NR-006).
      **DONE UPSTREAM 2026-08-28 — BUT NOT YET CONSUMED HERE.** The state is
      three-part and the tick covers only the first part; read all three before
      relying on this protection.

      **(i) The codexFactory-side act this task names is COMPLETE.**
      codexFactory PR **#125** *"Add the openxFactory review-lane pin to the
      never-clearable floor"*, merged `99fa3ffe` and reachable from
      `origin/main`. Verified rather than taken on report:
      `contracts/review-lane-pin.yaml` is present in that file's
      `never_clearable_paths` at `origin/main`, declared as a fourth entry
      grounded separately from the wallet-register trio — *"the review-lane pin
      selects which codexFactory commit's decision core judges this repository.
      Clearable, it would let a pull request choose its own judge."* The merge
      carries per-path behavioural tests in
      `tests/merge-master/test_repository_gate_floor.py` (+45), so the entry is
      pinned by executing code rather than by declaration alone.

      **(ii) NOT YET CONSUMED BY THIS REPOSITORY, so the protection is NOT live
      here.** This caller and `contracts/review-lane-pin.yaml` both still name
      `core_commit: 58bd3cf7…`, which **predates** the entry. Verified:
      `99fa3ffe` is **not** an ancestor of `58bd3cf7`, and the floor file at the
      pinned commit contains **zero** occurrences of `review-lane-pin.yaml`
      against one at `origin/main`. **Consequence, stated plainly: a pull request
      touching `contracts/review-lane-pin.yaml` today receives a ZERO-MATCH
      advisory verdict** — the lane reports that the candidate touches none of
      the never-clearable paths, because the core it runs does not yet know the
      entry exists. **Do not read the tick as "this path is protected here."**

      **(iii) Consumption happens at the next re-point ceremony — follow-up 6.5,
      deliberately deferred.** The re-point is CODEOWNERS-routed to a human
      (FR-013) and is a ceremony in its own right, so it is held until
      codexFactory **#126** (the convening record) and **#127** (the S-1/S-2
      guards) land. **One ceremony then converges the floor entry, the convening
      record and the new guards, instead of three.** Deferring is the choice, not
      an oversight.
- [ ] 6.3 `add-substantive-review-lane` task 3.2 — the `gate_rules_council`
      record defining openxFactory's candidate classes — remains the gate on
      any envelope instance here (FR-008).
      **UPDATED 2026-08-28 — STAYS UNTICKED, and the reason has changed.** The
      council CONVENED on 2026-08-28 and **REFUSED** the class proposed to it,
      unanimously 5/5: `openxfactory-proposal-review-advisory` over
      `openspec/changes/**` can never CONVENE, because its admitted surface lies
      wholly inside the canonical `GATE_INTEGRITY_FLOOR` (984 admitted paths,
      984 floored, 0 remaining; proven code-level). Record:
      `opensoft/codexFactory` →
      `hermes/domain/review-councils/records/2026-08-28-gate-rules-openxfactory-substantive-classes.md`
      (disposition §8).
      Brett Heap ruled the same day — *"1a, 2 leave open, 3 adopt, 4 adopt all
      three"* — so **task 3.2 remains OPEN and FR-008 remains GATED**: no
      envelope instance may exist here absent a future OPERABLE class. A record
      that refuses is still a record, and it does not discharge this gate.
      The ruled continuation is the council-reviewed-but-human-approved path,
      which needs no class and no flip, so it requires nothing of this feature.
      This entry is the REQUIRED pointer to that record (the council's Decision
      3, adopted): the gate lives in another repository, so the artifact
      carrying the dependency carries the reference.
- [ ] 6.4 Task 5.1's RULESET half stays owed, behind S3 and S5 of
      `add-wallet-carried-review-authority` and its own ratified ruleset change
      (NR-001, NR-002, NR-003, NR-007).
- [ ] 6.5 A future re-point ceremony should converge this pin with xFactory's
      two surfaces (D2).
      **IT ALSO CONSUMES 6.2.** The floor entry 6.2 records is live upstream but
      inert here until this ceremony advances `core_commit` past `99fa3ffe` —
      see 6.2 (ii). Held deliberately until codexFactory #126 and #127 land, so
      one ceremony converges the floor entry, the convening record and the S-1/S-2
      guards. The re-point is CODEOWNERS-routed to a human (FR-013).


## Evidence (recorded 2026-08-27)

- **1.1** `scripts/merge_master/` at xFactory's pinned `3c35ca8b` holds 9 files and
  contains NEITHER `repository_floor.py` NOR
  `openxfactory-review-authority-floor.yaml`; at `58bd3cf7` it holds 12 and
  contains both. The divergence is measured, not asserted.
- **1.2** Repo-level: `OPENXFACTORY_APP_ID`, `OPENXFACTORY_APP_PRIVATE_KEY`.
  Org, visibility `selected` to `opensoft/Omnigent-Install` +
  `opensoft/xFactory` ONLY: `XFACTORY_APP_ID`, `XFACTORY_APP_PRIVATE_KEY`,
  `MERGE_MASTER_APP_KEY`, `vars.MERGE_MASTER_APP_ID`. No secret was created.
- **§3–§4 end-to-end, run pre-merge because the check cannot report on its own
  pull request.** The workflow's inline evaluator was extracted VERBATIM (80
  lines, unedited) and executed against `opensoft/codexFactory@58bd3cf7`
  materialized at the pin, with this repository's live
  `git ls-tree -r --name-only HEAD` as `tree_paths`:
  * this pull request's own 9 changed paths -> `ok: true`,
    `floor_id: openxfactory-review-authority-register`, `matched_paths: []`,
    both per-repo rule documents resolved;
  * a candidate touching all three floored paths plus one unfloored path ->
    all three returned in `matched_paths`, the unfloored one absent.
  Posted on the pull request as its pre-merge evidence comment.
- **5.1** `pytest tests/review_lane_pin` — 33 passed, 18 subtests, 0 skipped.
  `pytest tests/doc-health/test_pin_reachability.py tests/review_lane_pin` — 86
  passed, 0 failed, 0 skipped. Whole-suite collection: 7196 selected (floor
  7090), 0 new skips, so `EXPECT_SKIPPED: "20"` is unchanged.
- **5.2** `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — 75 passed, 0
  failed. This feature adds no OpenSpec change; the assertion is that it breaks
  nothing.
- **5.3** `actionlint` was NOT on PATH; v1.7.7 was fetched from the release page
  and run — clean, exit 0. Recorded rather than implied.
- **5.4** `openXwallet/scripts/wallet-yaml-syntax-gate.py .` (the pinned gate the
  required `wallet-validation` check runs) — exit 0. The live check also passed
  on the pull request.
- **5.5** Pull request opened: `opensoft/openxFactory#439`. NOT merged.
- **5.6** `merge-master-approval` did NOT report on pull request #439, exactly as
  D4 predicted: `pull_request_target` evaluates the BASE-BRANCH definition and
  this file is not on `main` yet. `workflow_dispatch` cannot substitute (the
  platform resolves dispatchable workflows from the default branch). The first
  live report is the next openxFactory pull request after this lands.
- **Live checks on #439, both green.** `wallet-validation` pass (23s) — the
  required check, whose final step positively asserts the intake register was
  read. `pytest-suite` pass, including the selected/passed/skipped gate:
  `selected=7242 passed=7222 skipped=20 failures=0 errors=0`, i.e. margin 152
  over both floors and the skip count EXACTLY unchanged at 20, so this feature
  added tests and no skips.
