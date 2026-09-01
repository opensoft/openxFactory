# Readiness Dispatch Evidence: add-clearing-dispatch-boundary

Status: record
Filed: 2026-09-01
Filed by: Claude Fable 5, on Brett's instruction, against verified GitHub API
state and the composed operation report
Covers: `tasks.md` §4 (operator console acts) and §5 (dispatch readiness on
both lanes)

**THE FIRST OPERATION EVER THROUGH THE CLEARING DOOR.** `readiness-diagnostic`
was dispatched through `clearing-dispatch.yml` on both lanes and ran green:
opensoft/xFactory run `33512287539`
(https://github.com/opensoft/xFactory/actions/runs/33512287539), dispatched
`2026-09-01T13:15:22Z` by `brettheap` via `workflow_dispatch` on
`clearing-dispatch.yml@refs/heads/main` (sha `72562233`), operation
`readiness-diagnostic`, `lane=both`, dispatch ledger id
`cd-33512287539-1`. All four jobs succeeded — the clearing gate, both lane
jobs, and `operation-report` — with `clearing.dispatch.outcome=success`. A
single `lane=both` dispatch discharges both `tasks.md` 5.1 (coding lane) and
5.2 (artifact lane) in the one run.

**PRIMARY ARTIFACT AND ITS RETENTION CAVEAT.** The run URL above is the
primary artifact of record. GitHub Actions run logs expire under the
repository's retention policy; they are not a durable citation on their own.
The evidence lines quoted verbatim in this record are the durable copy — read
them here, not by re-opening a log that may already be gone.

## 1. The console acts this dispatch depended on (§4)

Three console acts, all measured against the provider API on 2026-09-01,
preceded and gated this dispatch:

1. **§4.1 — the permanent allowlist entry.**
   `opensoft/xFactory/.github/workflows/clearing-dispatch.yml@refs/heads/main`
   added to `selected_workflows` of group `xfactory-artifact-workers` (id 5)
   and group `xfactory-execution-lane-workers` (id 7). One entry per group,
   as required.
2. **§4.3 and §4.4 — the residual closed, and the baseline re-read.**
   `opensoft/codexFactory` removed from group `xfactory-artifact-workers`'s
   (id 5) repository admissions. Re-read from the provider API after 4.1 and
   4.3: **both groups now admit `opensoft/xFactory` alone — zero widenings,
   the first green single-door reading.** That reading is filed here as the
   baseline the future §7.1 attestation compares against.
3. **§4.5 — the required status check.** New `opensoft/xFactory` ruleset
   `22015321`, `"required-checks-main"` — active, targeting the default
   branch, required check `validate` pinned to the GitHub Actions integration
   `15368`. This is what turns the L4 guard from a check that runs into a
   check that gates, subject to the operator-bypass residual §4.5 already
   records.

## 2. Per-gap disposition (§5.3)

Three gaps were named at authoring so the reports would be read against a
question rather than skimmed. This run closes two and leaves one open.

**Gap 1 — the coding lane's first isolated live round trip. CLOSED.**
Every prior exercise of `xfactory-coding-cpc-brett01` was as a child of real
work; this is the first isolated confirmation that the host claims a job,
executes, and returns. Verbatim from the composed report:

```
clearing.report.coding.runner.identity=CONFIRMED (name xfactory-coding-cpc-brett01, Windows X64 self-hosted)
```

with `sha256_check`, `arithmetic_check`, and `round_trip` all `PASS`.

**Gap 2 — the artifact lane's service account against the provisioning
record. CLOSED.** The measurement matches `cloudpc-worker-handoff-prompt.md`'s
declared hidden local standard account. Verbatim:

```
clearing.report.artifact.whoami=svc-omniworker / username / userprofile C:\Users\svc-omniworker
```

Service account `svc-omniworker` confirmed, matching design. (The coding lane
reports its own, distinct account for comparison:
`clearing.report.coding.whoami=svc-omnicoder`, `userprofile
C:\Users\svc-omnicoder` — the two lanes run under two distinct service
accounts, as designed.)

**Gap 3 — the `artifact-only` label hazard, and its symmetry. STILL OPEN.**
This run confirms group/label routing was correct regardless of the stray
label (the operation reached the right host on the right lane both times),
so the label is not a live routing breach today — but the label itself is
unresolved. It remains an operator label-cleanup item, now carried forward
as `tasks.md` §4.6 rather than only in this record's prose.

## 3. New finding: same-host topology (not one of the original three gaps)

Both lane reports carry the same host identity:

```
hostname / COMPUTERNAME / compute.node = CPC-brett-TUBV0, NUMBER_OF_PROCESSORS=8
```

on **both** the coding and the artifact lane. The two runners are two
services on **one** Cloud PC — separate installs
(`C:\actions-runner-coding` vs. `C:\actions-runner-artifact`) under separate
service accounts (`svc-omnicoder` vs. `svc-omniworker`), not two separate
machines. Lane isolation, as provisioned today, is service-account
isolation, not machine isolation. This plausibly explains the coding
runner's copy-pasted `artifact-only`/`rider` labels (Gap 3 above) — a
same-host clone of the artifact runner's label set.

This is an operator decision, not a defect this record can close on its own:
is single-host-with-service-account-isolation the design, or an interim
state pending a second host. Carried forward as `tasks.md` §4.7, since no
existing task item captured it.

## 4. Version-skew note (tool print-backs, EXE-6-relevant)

The two lanes' print-backs diverge on Claude Code's own version:

- coding lane: `claude 2.1.207`
- artifact lane: `claude 2.1.206`

Both lanes agree on `python3 3.12.10`, and both resolve `claude` at
`~/.local/bin/claude` inside their respective service account's home. This is
recorded as a fact of the composed report; no disposition is filed here
beyond noting the skew exists.

## 5. Report composition, for completeness

Both lane jobs forwarded `forwarded_lines=39`; the `operation-report` job
composed the single structured report from those forwarded outputs per the
report-carrier design (`tasks.md` §5, preamble). `clearing.operation.result
=success`, `check=PASS`.

## Pointers

- Run: https://github.com/opensoft/xFactory/actions/runs/33512287539
- Ledger id: `cd-33512287539-1`
- `tasks.md` items discharged by this record: 4.1, 4.3, 4.4, 4.5, 5.1, 5.2,
  5.3, 5.4.
- `tasks.md` items opened by this record: 4.6 (artifact-only/rider label
  cleanup), 4.7 (same-host topology decision).
- Still open and unaffected by this record: `tasks.md` §8.3 (the dark-lane
  dispositions for `ideation-organizer-worker.yml` and
  `review-lane-worker.yml`, and the nine grandfather retirements generally)
  — this dispatch neither closes nor changes that item; it is named here
  only so a reader does not mistake this record's silence on it for closure.

## Correction (2026-09-01, admin read-back)

Gap 3 above (§2, filed as "STILL OPEN") is corrected. Per Brett Heap's
infrastructure admin's read-back, verified in the xFactory tree, the
`artifact-only` flag was a MISDIAGNOSIS: `artifact-only` on
`xfactory-coding-cpc-brett01` is CONTRACT-REQUIRED vocabulary describing the
coding lane's security posture (sealed bundle in, no repository credentials,
patch artifact out), required by the coding-patch-worker profile's
`runner_labels` — not a stray or leftover label. It stays on both runners
permanently.

`rider` is a distinct mechanism and is not part of the misdiagnosis: it is
the host-class label for `service_rider`, mapped by xFactory
`scripts/worker_readiness.py`'s `HOST_CLASS_LABELS = {"service_rider":
"rider", "dedicated_omni": "omni-artifact"}`, and readiness FAILS CLOSED
(`host_class_label_missing`) when the GitHub label set disagrees with the
heartbeat's published `host_class`. Deleting it live would desync
runner/profile/heartbeat and leave jobs queued indefinitely. It is stale only
because §4.7 ruled the CPC a dedicated governed node for QA, and is replaced
ONLY via a coordinated host-class migration (`service_rider` →
`governed_node`, label `governed-node`) — never by deleting the live label
first.

**New status:** Gap 3 is **RESOLVED as a misdiagnosis for `artifact-only`**
(no action — the label is correct and required); **`rider` is carried
forward, not resolved here, to the migration tracked at
`opensoft/xFactory#195`** (https://github.com/opensoft/xFactory/issues/195,
admin's 8-step plan, requires an OpenSpec change before implementation).
`tasks.md` §4.6 carries a superseding annotation reflecting this correction
and stays open only for that migration's label-swap and readiness
re-verification steps (its steps 6-7).
