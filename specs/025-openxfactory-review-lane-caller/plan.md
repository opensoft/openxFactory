# Implementation Plan: openxFactory review-lane caller (advisory)

**Branch**: `025-openxfactory-review-lane-caller` | **Date**: 2026-08-27 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/025-openxfactory-review-lane-caller/spec.md`

## Summary

Land openxFactory's own `merge-master-approval` workflow instance — the
workflow-instance half of `add-substantive-review-lane` task 5.1 — as an
ADVISORY reporter. One `pull_request_target` job named exactly
`merge-master-approval` checks out `opensoft/codexFactory` at a recorded pin,
gathers the pull request's changed paths provably complete, evaluates the
`repository_gate_floor` the pinned core declares for `opensoft/openxFactory`,
and renders the verdict. It approves nothing, mints no approving identity, and
changes no ruleset. A committed pin (`contracts/review-lane-pin.yaml`,
`kind: pinned_workflow`) plus a pytest drift test makes the "which core judged
this" question answerable and its answer non-silent.

## Technical Context

**Language/Version**: GitHub Actions workflow YAML; embedded `bash` (POSIX
`set -euo pipefail`) and Python 3.x for the floor evaluation; pytest for the
static/drift test.
**Primary Dependencies**: `opensoft/codexFactory` at the pin, for
`scripts/merge_master/repository_floor.py` and
`scripts/merge_master/openxfactory-review-authority-floor.yaml`. PyYAML.
`actions/checkout@v4`, `actions/create-github-app-token@v2`,
`actions/setup-python@v5`.
**Storage**: N/A — the run writes a step summary and nothing else.
**Testing**: `python3 -m pytest tests/ -q -m "not postgres"` (whole-suite; new
directories are auto-collected). Zero new skips, because the CI gate pins the
skip count EXACTLY.
**Target Platform**: `ubuntu-latest` GitHub-hosted runner.
**Project Type**: governance tooling in a contracts repository.
**Performance Goals**: a run completes inside a few minutes; the whole job is
API reads plus one small Python evaluation.
**Constraints**: no ruleset change; no head-content execution; single job; the
check name is fixed by governance, not by preference.
**Scale/Scope**: one workflow, one pin file, one pin-class member, one test
module, one CODEOWNERS line.

## Constitution Check

- **Rules read from the base branch.** `pull_request_target` plus
  `actions/checkout` with no `ref:` for this repository. The pinned core is a
  second checkout at an exact commit. Nothing head-authored is read or run.
- **Fail-closed, never vacuously green.** Every unobtainable fact is a named
  park or a named failure. There is no `|| echo '[]'` anywhere: a failed or
  rate-limited API read must not become a clean empty fact set.
- **The enforcer originates no judgment.** This caller has no approval path at
  all, so the constitutional floor is met structurally rather than by
  configuration.
- **Permanently human-only surfaces stay human-only.** The register, the wallet
  pin, and the `openXwallet` gitlink are the floor's three entries; this feature
  reads that floor and never authors it.
- **Declared, not silent.** The pin is a committed artifact, code-owner-routed,
  test-asserted, and a declared derivation-pin-class member.

## Project Structure

### Documentation (this feature)

```text
specs/025-openxfactory-review-lane-caller/
├── plan.md              # This file
├── spec.md              # Feature specification
├── tasks.md             # Ordered task list
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
.github/
├── CODEOWNERS                              # + one line routing the pin
└── workflows/
    └── merge-master-approval.yml           # NEW — the advisory caller
contracts/
└── review-lane-pin.yaml                    # NEW — kind: pinned_workflow
scripts/doc_health/
└── pin_class.py                            # + one PinMember (CROSS_REPOSITORY)
tests/review_lane_pin/
└── test_review_lane_caller.py              # NEW — pin drift + static floors
```

**Structure Decision**: The workflow, the pin, and the test mirror the shapes
this repository already uses. `.github/workflows/openxwallet-consumer-gate.yml`
is the local authoring precedent (job id chosen for the check token, an
anti-vacuity assertion step, a long "why / what was rejected" header).
`contracts/openxwallet-pin.yaml` + `tests/openxwallet_pin/` +
`.github/CODEOWNERS:9` is the pin precedent, followed member for member.

## Key design decisions

### D1 — The precedent is xFactory's `merge-master-approval.yml`, not its `review-lane.yml`

The feature request named `.github/workflows/review-lane.yml` and its
`uses: opensoft/codexFactory/.github/workflows/review-lane-reusable.yml@<sha>`
line as the thing to mirror. That is the wrong precedent for the stated goal,
and the reason is worth recording so nobody re-derives it:

- `review-lane-reusable.yml` produces a governed substantive review as an
  artifact and a review-record pull request. It reports no check named
  `merge-master-approval`, and its caller in xFactory is `workflow_dispatch`
  ONLY — it never runs on a pull request.
- The `merge-master-approval` check-run name comes from a JOB ID. GitHub names a
  called-workflow's check-runs `<caller job>/<called job>`, so a caller that
  `uses:` a reusable can never produce a check named exactly
  `merge-master-approval` — only `merge-master-approval / prepare` and friends.
  A future ruleset requiring the literal token would not match.
- The workflow that actually produces that check is a single non-reusable job:
  codexFactory's own `.github/workflows/merge-master-approval.yml` and
  xFactory's aggregation caller of the same name. Both are
  `pull_request_target`. That is the shape mirrored here.

Consequence for the pin: there is no `uses: ...@<sha>` line to assert, so the
pin governs a checkout `ref:` instead. The recorded-pin-plus-test discipline is
unchanged; only the line it points at differs.

### D2 — The pin is codexFactory `origin/main` at declaration, and the divergence is forced

xFactory pins `3c35ca8b` (2026-08-21) in BOTH its merge-master surfaces and
calls advancing it a recorded re-point ceremony. Pinning the same commit here
would have been the lockstep-preserving choice, and it is impossible: at
`3c35ca8b`, `scripts/merge_master/` contains neither `repository_floor.py` nor
`openxfactory-review-authority-floor.yaml`. Both landed later — the floor
arrived with codexFactory's `015-widen-review-authority-floor` work. Since the
floor evaluation is the ONLY thing this caller does, the older pin cannot run
it.

So the divergence is a consequence of the feature, not a preference for
freshness, and it is recorded as such in the pin file. The obligation it creates
is stated there too: a future re-point ceremony should converge the three
surfaces, and the pin file names the two xFactory surfaces it is out of step
with so the convergence is a lookup rather than an archaeology exercise.

### D3 — No envelope config, and therefore no tier-1 evaluation

codexFactory's envelope schema requires `candidates` with `minItems: 1`, and
`envelope.py` mirrors that at runtime (`config.candidates must be a non-empty
list`). openxFactory has no ratified candidate class:
`add-substantive-review-lane` task 3.2 owes a `gate_rules_council` record
defining them, and it does not exist. There is therefore no legal empty
envelope, and a placeholder candidate would be inventing the enrollment that
task 3.2 exists to grant. The caller ships no envelope instance and evaluates
no tier-1 decision.

What is left is not nothing, which is the point: the floor is real, it is
openxFactory-specific, it is already committed in codexFactory, and no code in
openxFactory reads it today.

### D4 — `pull_request_target`, accepting that this feature cannot demo itself

`pull_request_target` runs the workflow definition from the BASE branch. A
workflow absent from the base branch does not run — so this feature's own pull
request will carry no `merge-master-approval` check. `workflow_dispatch` does
not rescue it either: the platform resolves dispatchable workflows from the
default branch.

The alternative, `pull_request`, WOULD run on this pull request, and is refused:
it runs the head's copy of this file with the secret that reads a private
repository in scope, so a same-repository pull request could rewrite the file to
exfiltrate the token. Trading the base-branch rule for a demo is the wrong
trade, and the ONE thing that makes the trade tempting — seeing the check on
this pull request — is available for free on the next pull request after this
lands.

What replaces the demo, pre-merge: the static test asserts the trigger set, the
single-job invariant, the exact job id, the pin agreement, and the ABSENCE of
every approval-shaped step.

### D5 — The failure mode is red, not skipped

openxFactory is not in the selected-repository list for the org secrets that can
read the private core (`XFACTORY_APP_ID` / `XFACTORY_APP_PRIVATE_KEY` are
`selected` to `opensoft/Omnigent-Install` and `opensoft/xFactory` only). The
repository's own content App (`OPENXFACTORY_APP_ID` /
`OPENXFACTORY_APP_PRIVATE_KEY`) is present and is TRIED FIRST — if that App's
installation can read codexFactory, the lane works today with no org change at
all.

codexFactory's own caller treats absent App config as a green "pre-registration"
notice. That is right THERE, where the check is a required gate and a red check
would wedge every pull request. It is wrong HERE: this check gates nothing, so a
green run that read no core is a check that manufactures the appearance of
review. The run therefore FAILS with the missing identifiers named. Because no
ruleset requires the check, the red blocks nobody.

### D6 — The changed-path gather keeps the precedent's hardening verbatim in spirit

The floor is exact set membership over changed paths, so a truncated file
listing produces a FALSE CLEAN verdict — the worst available outcome. The
gather therefore keeps the precedent's proven discipline: the authoritative
total from the pull-request RESOURCE (never GraphQL `totalCount`, which clamps
to 3000 and reports "complete" on a 6181-file pull request; never
`gh pr view --json files`, hard-coded to `first: 100` with no truncation
signal; never the compare endpoint, capped at 300 with no total), paginated REST
with `previous_filename` folded in so a rename into an unfloored path cannot
launder the source path, an entry-count-versus-total comparison, and a head-SHA
recheck after pagination.

### D7 — One 40-hex value in the pin file, one pin-class member

`contracts/review-lane-pin.yaml` carries exactly ONE commit-shaped value, under
the key `core_commit`. A key the sweep vocabulary does not know is taught by
declaring the member — the `carve_commit` precedent says so in as many words —
and one value means one member, declared `CROSS_REPOSITORY` because a
codexFactory commit must never be expected to resolve here. xFactory's diverging
pin is named in the workflow header instead of the pin file, so the file does
not acquire a second cross-repository value needing its own member.

## Complexity Tracking

| Item | Why it is not simpler | Simpler alternative rejected because |
| --- | --- | --- |
| Full provably-complete path gather | The floor is exact set membership; a truncated listing yields a false clean verdict | A single unpaginated page is 3 lines and silently wrong above 100 files |
| A pin file + a test + a pin-class member for one sha | openxFactory has no codexFactory gitlink, so nothing structural ties the workflow to a recorded value | A comment beside the `ref:` is not checkable and drifts silently |
| Trying the repo App before the org App | If the repo App can read the core, the lane works with no org secret change | Requiring the org grant first leaves the lane dead on landing for no reason |
