# Tasks: openxFactory review-lane caller (advisory)

**Input**: Design documents from `specs/025-openxfactory-review-lane-caller/`
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md)

## 1. Recon and pin selection

- [ ] 1.1 Record the codexFactory commit the pin will name, and prove the two
      artifacts the caller depends on exist AT that commit and NOT at xFactory's
      `3c35ca8b`: `scripts/merge_master/repository_floor.py` and
      `scripts/merge_master/openxfactory-review-authority-floor.yaml`.
      (D2 — the divergence must be forced, not asserted.)
- [ ] 1.2 Record the secret/variable reality for `opensoft/openxFactory`:
      which identifiers exist at repo level, which org secrets are
      visibility-`selected` and to which repositories. Do NOT create any
      secret. (D5.)

## 2. The pin artifact

- [ ] 2.1 `contracts/review-lane-pin.yaml` — `schema_version: 1`,
      `kind: pinned_workflow`, `repository: opensoft/codexFactory`,
      `core_commit: <40 hex>`, `revision_kind: commit`, `declared_at`,
      the caller path the pin governs, the two pinned members the caller reads,
      and the lockstep note naming xFactory's two diverging surfaces.
      EXACTLY ONE 40-hex value in the file (D7).
- [ ] 2.2 One `PinMember` in `scripts/doc_health/pin_class.py`'s `PIN_CLASS`:
      `paths=("contracts/review-lane-pin.yaml",)`, `key="core_commit"`,
      `key_form="field"`, `reproduction=MEASURED`,
      `locality=CROSS_REPOSITORY`, `presence=CURRENT`, with a note saying why a
      codexFactory commit must never be expected to resolve here.
      Follows `openxwallet-pin-product-commit` (D7).
- [ ] 2.3 `.github/CODEOWNERS` — route `/contracts/review-lane-pin.yaml` to
      `@brettheap`, on the 2026-08-23 ruling's ground: a pull request that
      changes it changes the code a governance surface executes (FR-013).

## 3. The advisory caller

- [ ] 3.1 `.github/workflows/merge-master-approval.yml`, ONE job whose id is
      exactly `merge-master-approval` (FR-001, FR-011). Triggers:
      `pull_request_target` `[opened, reopened, synchronize]`, plus
      `workflow_dispatch` with an optional `pr_number`. Serialized by a
      `concurrency` group. Permissions: `contents: read`, `pull-requests: read`
      and nothing that could approve or merge (FR-007).
- [ ] 3.2 Preflight: resolve the decision-core read credential — the
      repository's own content App first, the org App second — and FAIL with
      the missing identifiers NAMED when neither is present (FR-010, D5).
- [ ] 3.3 Checkout this repository from the base branch (no `ref:`), then
      checkout `opensoft/codexFactory` at the pinned `core_commit` into
      `.merge-master-core` (FR-002, FR-003).
- [ ] 3.4 Runtime pin agreement: read `contracts/review-lane-pin.yaml` from the
      base checkout and refuse the run if its `core_commit` differs from the
      commit the workflow just checked out. The test is the primary guard; this
      is the second, so a hand-edited workflow cannot judge a pull request under
      a core the pin does not name.
- [ ] 3.5 Resolve the candidate pull request from the event payload
      (`pull_request_target`) or from the dispatch input, and PARK with a named
      reason when no pull request can be resolved.
- [ ] 3.6 Gather the changed-path set PROVABLY COMPLETE (FR-009, D6):
      authoritative `.changed_files` and head SHA from ONE read of the
      pull-request resource; paginated REST file listing with shape proof;
      `previous_filename` folded into the judged set; entry count compared
      against the declared total; head-SHA recheck after pagination. No
      failure masking anywhere — every gather failure parks with its reason.
- [ ] 3.7 Evaluate the floor with the pinned core: import
      `merge_master.repository_floor`, load
      `.merge-master-core/scripts/merge_master`, select the floor whose
      `repository` is `opensoft/openxFactory`, supply the repository tree
      listing so an unreachable floor path is a named failure rather than
      silence, and compute the matched paths (FR-006).
- [ ] 3.8 Render the advisory verdict to `$GITHUB_STEP_SUMMARY`: the pinned
      commit, the floor id, the changed-path count, the matched floored paths
      by name, and an explicit statement that nothing was approved and no
      ruleset consumes this check.
- [ ] 3.9 Anti-vacuity assertion, mirroring
      `openxwallet-consumer-gate.yml`'s final step: fail unless the run
      positively evidenced that it read the floor from the pinned core — a
      POSITIVE conjunction, never "did not fail".
- [ ] 3.10 Confirm by inspection that the file contains no step that mints an
      approving token, submits a review, calls merge, or enables auto-merge
      (FR-007). Absence is the mechanism; the test in §4 pins it.

## 4. The test

- [ ] 4.1 `tests/review_lane_pin/test_review_lane_caller.py`. NO `pytest.skip`
      anywhere — the CI gate pins the suite's skip count EXACTLY, and a skip
      reports as a green bar (SC-006).
- [ ] 4.2 Pin agreement: the workflow's pinned `ref:` equals the pin file's
      `core_commit`; the failure message names both values and the file to
      change (FR-005).
- [ ] 4.3 Pin shape: `kind: pinned_workflow`, `repository`,
      `revision_kind: commit`, a 40-lowercase-hex `core_commit`, an ISO date
      `declared_at`, and the governed caller path — which must be the file that
      exists. Missing or malformed pin FAILS, never skips.
- [ ] 4.4 Exactly ONE 40-hex value in the pin file, so the single declared
      pin-class member covers it (D7).
- [ ] 4.5 The pin-class member exists and is declared `CROSS_REPOSITORY` with
      `key="core_commit"` and this pin's path.
- [ ] 4.6 Caller invariants: parses as YAML; exactly one job; its id is exactly
      `merge-master-approval`; the trigger set is exactly the intended one;
      `pull_request` (the head-executing trigger) is ABSENT; no
      `permissions:` grant that could write a review or merge.
- [ ] 4.7 The approval-shaped absence, asserted as a denylist over the file
      text: no `create-github-app-token` step naming the merge-master App, no
      `gh pr review`, no `gh pr merge`, no `pulls/.../reviews` POST, no
      `--auto`, no `enablePullRequestAutoMerge`.
- [ ] 4.8 Embedded shell parses: every `run:` block that is bash passes
      `bash -n`. Not conditioned on a `which bash` probe (that would be a skip).
- [ ] 4.9 CODEOWNERS routes the pin path.
- [ ] 4.10 Negative controls in a scratch tree so each positive is one mutation
      from failing: a drifted `ref:`, a malformed pin, a two-job caller.

## 5. Validation and exit

- [ ] 5.1 `python3 -m pytest tests/review_lane_pin -q` green, then the whole
      suite's collection is unbroken (`--collect-only -q` count) and the new
      module adds ZERO skips.
- [ ] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green — this
      feature adds no OpenSpec change, so the assertion is that it breaks
      nothing.
- [ ] 5.3 `actionlint` if obtainable; record explicitly if it is not available
      in this environment rather than implying it passed.
- [ ] 5.4 The new YAML parses under the pinned wallet syntax gate, which runs
      on every pull request via the required `wallet-validation` check.
- [ ] 5.5 Commit, push, open the pull request against `main`. Body states what
      the caller does and does NOT do, the pinned commit and why it diverges
      from xFactory's, and the exact secret status. Do NOT merge.
- [ ] 5.6 Watch the pull request's checks. RECORD HONESTLY that
      `merge-master-approval` cannot report on this pull request, because
      `pull_request_target` runs the base-branch definition and this file is not
      on the base branch yet (D4) — and name the first pull request after the
      merge as where the live report appears.

## 6. Named follow-ups, not performed here

- [ ] 6.1 Grant `opensoft/openxFactory` read access to the private decision
      core — either by adding it to the `selected` list for
      `XFACTORY_APP_ID` / `XFACTORY_APP_PRIVATE_KEY`, or by installing the
      repository's own content App on `opensoft/codexFactory`. Operator act;
      no secret is created by this feature.
- [ ] 6.2 codexFactory side: add `contracts/review-lane-pin.yaml` to
      `scripts/merge_master/openxfactory-review-authority-floor.yaml`'s
      `never_clearable_paths`. It determines which core judges this repository,
      which is the same argument the wallet pin's entry already makes
      (NR-006).
- [ ] 6.3 `add-substantive-review-lane` task 3.2 — the `gate_rules_council`
      record defining openxFactory's candidate classes — remains the gate on
      any envelope instance here (FR-008).
- [ ] 6.4 Task 5.1's RULESET half stays owed, behind S3 and S5 of
      `add-wallet-carried-review-authority` and its own ratified ruleset change
      (NR-001, NR-002, NR-003, NR-007).
- [ ] 6.5 A future re-point ceremony should converge this pin with xFactory's
      two surfaces (D2).
