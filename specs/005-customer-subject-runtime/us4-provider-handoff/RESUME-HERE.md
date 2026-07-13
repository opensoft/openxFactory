# US4 Provider-Side Handoff: Gate G0 T066–T078 — RESUME POINT

Status: record

## 0. What this is

Crash-safe resume point for the US4 provider-side session (started 2026-07-13,
immediately after the US3 checkpoint `66b1406` landed and was independently
verified green). If this session is interrupted, a fresh session resumes from
this directory exactly as the US3 session resumed from `us3-swarm-handoff/`.

## 1. Mission and scope (Brett-approved plan)

Complete as much of User Story 4 as possible **up to the release gate**:

- IN SCOPE: T066–T069 (four failing non-postgres test modules), T070–T076
  (v2 job schemas/fixtures/semantics, domain-regression inventory + resolver,
  release digest inventory + verifier CLI, consumer handoff receipt +
  resolver, documentation), T077 (register everything in the four catalogs +
  wire validator modes), T078 (run every provider gate, record
  `openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/provider-verification.yaml`),
  Speckit analysis, adversarial P1/P2 review, ONE squashed US4-provider
  checkpoint commit on `005-customer-subject-runtime`. Then STOP.
- OUT OF SCOPE / PARKED FOR BRETT AT THE GATE: T079 (release lock + version
  allocation), T080 (candidate commit + independent expert review), T081
  (promotion to origin/main, push, annotated tag), T082 (external
  xFactory-Hermes-Install receipt), T083–T084, all OpenSpec acceptance
  checkboxes, any push/tag/merge, the aggregation-repo pin update.

## 2. Hard constraints (violating these invalidates evidence or races a peer)

1. **Do not edit any of the 78 PostgreSQL-evidence source-inventory members**
   (the `source_paths`/`test_modules`/`seed_scripts`/`assertion_scripts`
   lists on the database case in `contracts/hermes-runtime/fixtures/index.yaml`).
   Notably: `shared-definitions.schema.yaml`, `hermes-operational-postgres-v2.sql`,
   `migrations/v1-to-v2.sql`, `scripts/hermes_runtime_validation/{fixtures,loader,migration}.py`,
   all `tests/hermes_runtime_contracts/postgres/**` test modules/fixtures.
   The frozen evidence (source identity `sha256:b2ef44a9…`, 161 tests/major)
   must stay valid — US4 work is NEW files plus the four catalogs and the
   validator CLI, none of which are inventory members.
2. **A concurrent session owns the P3 backlog** (F-4, F-7..F-9 fold-in via
   isolated-copy agents) and the uncommitted edit to
   `us3-swarm-handoff/us3-review-findings.md`. Leave both alone.
3. Shared-tree discipline: explicit-path staging only (never `git add -A`);
   check `git status -sb` branch before every commit; WIP-commit early.
4. No push, no tag, no version allocation, no origin fetch/rebase, no edits
   to `opensoft/xFactory-Hermes-Install`, no OpenSpec acceptance ticks, no
   archive.

## 3. Current state

- Branch `005-customer-subject-runtime`, HEAD `66b1406` (US3 checkpoint).
- T001–T065 `[x]`; T066–T084 `[ ]`.
- Phase 0 (coordination guardrails) done; Phase 1 scout in flight: five
  parallel readers over (a) Speckit planning contracts, (b) validator wiring +
  four catalogs, (c) schema/semantics conventions + shared-definitions $defs,
  (d) non-PG test-suite conventions, (e) OpenSpec delta requirement/scenario
  IDs for US4 + the five local DomainxFactory repos for the regression
  inventory (DOMAIN_REPO_ROOT mirrors to be built from
  `/workspace/projects/xFactory/xFactories/*` — offline, no network).
- Next artifact: `shared-interface-contract.md` in this directory (the US4
  SIC), then `integration-decisions.md`, then the lane swarm.

## 3.1 State after the FIRST interrupt (2026-07-13, ~19:20 UTC reset)

The five-lane swarm (run `wf_ea3432f0-c5c`) hit the session limit. Landed and
WIP-committed as `5a32640` on top of the handoff WIP `6b5be8a`:

- **Lane DOC (T076) COMPLETE-VERIFIED**: README + three docs updated; strict
  validator counts unchanged; 337 non-PG tests green.
- **Lane J**: `tests/hermes_runtime_contracts/test_v2_jobs.py` RED suite only
  (673 lines; schemas/fixtures/semantics NOT written).
- **Lane H**: `tests/hermes_runtime_contracts/test_consumer_handoff.py` RED
  suite only (499 lines; schema/fixtures/module NOT written).
- **Lanes R and D**: nothing landed.
- Wire stage correctly skipped by the completion guard.

The workflow was resumed from `resumeFromRunId: wf_ea3432f0-c5c` with
audit-and-complete resume context appended to the four code-lane prompts
(DOC replays from cache). If THIS resume is also killed: re-survey the
working tree, WIP-commit whatever landed, and resume the same run id again
with updated resume context; the script lives under the session workflows
dir and is reconstructable from the SIC lane definitions.

## 3.2 State after the Opus rerun COMPLETED (2026-07-13)

The four code lanes + T077 wiring completed on Opus (run `wf_35d18c7b-e20`,
all 5 agents done, 0 errors). WIP-committed as `f3d12cd` on top of `5a32640`.
All provider gates GREEN (independently re-verified by the coordinator):

- OpenSpec strict 24/0; strict validator ZERO findings (39 contracts,
  32 schemas, 110 fixtures, 17 req, 85 scen, 796 nodes); non-PG pytest
  478 passed; black/compileall/git-diff clean.
- PG-evidence inventory intersection EMPTY; source identity `b2ef44a9…`
  unchanged — the frozen both-majors matrix is NOT re-run.
- T077 wiring: 5 schemas registered, 31 fixture cases added, 20 planned
  evidence entries flipped to bound (all node IDs collect), the
  HRC-MODE-NOT-REALIZED stub replaced with real candidate/realization/
  domain/consumer dispatch (decision U7 behaviors verified: candidate+mirrors
  → exit 1 HGR-RELEASE-INVENTORY-MISSING; candidate w/o resolver → exit 2;
  handoff w/o consumer → exit 2; standard strict → exit 0).
- T078 provider gates recorded at
  `openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/provider-verification.yaml`;
  live domain resolution proven offline against bare mirrors of the five
  local DomainxFactory checkouts (scratchpad `domain-repo-root/`).

REMAINING before the single US4 checkpoint: adversarial P1/P2 review
(run `wf_189afdf0-0eb`, in flight) → fix any confirmed finding → flip
T066-T078 checkboxes in tasks.md → squash `6b5be8a`+`5a32640`+`f3d12cd`
(and the review-fix WIP if any) into ONE US4 checkpoint commit on top of
`66b1406` → STOP. T079-T084 parked for Brett at the release gate.

## 3.3 FINAL: single US4 provider checkpoint landed (2026-07-13)

Supersedes §3.2. The adversarial review completed (run `wf_189afdf0-0eb`,
4 lenses + per-finding verify): 3 confirmed, 1 refuted. The two P2 fail-opens
were FIXED (F-U1 cross-layer full-scope comparison; F-U2 handoff structural
guard replacing an uncaught KeyError) with regression tests; the one P3
(F-U3, latent) is documented for T079+. Dispositions in
[us4-review-findings.md](us4-review-findings.md).

The three WIP baselines (`6b5be8a`, `5a32640`, `f3d12cd`) plus the review
fixes were squashed into ONE US4 provider checkpoint commit (this commit) on
top of the US3 checkpoint `66b1406`. Final gates (confirmed against committed
HEAD): OpenSpec 24/0; strict validator ZERO findings (39 contracts,
32 schemas, 110 fixtures, 17 req, 85 scen, 803 nodes); non-PG pytest
485 passed; black/compileall/git-diff clean; PG-evidence intersection EMPTY
(frozen matrix untouched, source identity `b2ef44a9…`). T066-T078 checkboxes
flipped; T079-T084 unchecked.

STOPPED per the mission at the release gate: no version allocation, no
candidate commit, no promotion, no tag, no push, no external consumer
receipt, no Gate G0 closure, no aggregation-repo pin update. Those
(T079-T084) are parked for Brett's go-ahead. The only working-tree change
left is the concurrent session's uncommitted `us3-swarm-handoff/
us3-review-findings.md`, deliberately untouched.

## 4. Resume recipe (fresh session)

1. Read this file, then `shared-interface-contract.md` and
   `integration-decisions.md` if they exist (they pin every cross-lane name).
2. `git status -sb`; expect branch `005-customer-subject-runtime`; respect §2.
3. If a WIP commit exists on top of `66b1406`, it is this session's partial
   US4 work — read its message and continue from the lane states it records.
4. The plan of record is §1; the combined gate is the US3 T065 gate
   (us3-swarm-handoff/RESUME-HERE.md §7) plus the new US4 surfaces, with
   `--domain-repo-root` now required for the strict validator.
5. Finish with ONE squashed US4 checkpoint commit; keep this directory as
   `Status: record` or delete it before the clean commit (coordinator call).
