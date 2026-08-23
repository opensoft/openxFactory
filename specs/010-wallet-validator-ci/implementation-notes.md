# Implementation Notes — 010-wallet-validator-ci

Running record of execution rounds, evidence, and dispositions. Realization of S1 of
`add-wallet-carried-review-authority` (@ 89b11ec).

## Round 1 — Build (coder, ox-alpha)

T002+T005 atomically. Files: `.github/workflows/wallet-validation.yml` (new),
`README.md` (+7 lines). Coder's structural YAML asserts exit 0. Deviations accepted:
job id `wallet-validation` with no `name:` key (display-name construction per research
R5); comment header mirroring house style; section placed before `## Domain
Implementations` per delegation override.

## Round 2 — Orchestrator verification (T001/T003/T004/T006)

- Self-test mode: exit 0 — corpus 17 positives, **33 negative confirmations** across
  11/11 requirements (file count 29; several specimens assert multiple expectations).
- Whole-tree sweep: exit 0 — **0 live openxwallet artifacts** validated, 1528 documents
  skipped as other kinds. Matches ratified cold start ("zero wallet instances exist").
- Adversarial probe (de-headered negative copied as a live artifact): validator exit 1,
  finding `[custody-ceiling-unresolved]`, full path + rule attribution. FR-003/FR-006
  detection path proven.
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: 68 passed, 0 failed.

## Round 3 — QA (gpt-5.6-sol, high) — VERDICT: FAIL → dispositions

QA independently re-ran all evidence plus GitHub API checks. Findings and dispositions:

1. **[MAJOR→FIXED] FR-007 click-path**: repo enforces via RULESETS, not classic branch
   protection (QA verified via API). README rewritten rulesets-first with classic as
   alternative; spec FR-007, tasks T005, quickstart Scenario 5 trued up to match.
2. **[BLOCKER→ESCALATED] Fail-open on syntactically invalid YAML**: layer 2 classifies
   unparseable files as "another kind" and skips them, so a PR adding a syntactically
   broken live grant passes the sweep. Pre-existing validator semantics surfaced by
   wiring — NOT fixed here (FR-002 forbids validator changes; Clarification Q5 forbids
   duplicating discovery logic in the check layer). Escalated to convener with options:
   (a) ship S1 with this declared known gap + file upstream validator defect;
   (b) block S1 on an upstream fix; (c) authorize minimal check-layer YAML hardening,
   amending Q5.
3. **[BLOCKER→ESCALATED] Enforcement-plane boundary**: `pull_request` workflows execute
   merge-commit code, so a PR could edit the workflow or validator while keeping the
   check name; no CODEOWNERS guards those paths today. Same enforcement-plane problem
   the ratified change assigns to sibling work (`add-substantive-review-lane` pilot +
   assembly-plane separation), same class as direct-push/admin-merge boundaries ruled
   out of S1 in Clarification Q4. Escalated with optional mitigation (CODEOWNERS review
   routing) for convener decision.

## Round 4 — QA re-verdict after README fix

See QA output in session log; residual risks carried as escalated items above.

## Deferrals (explicit, per T007)

- SC-001 (N≥5 PR observation), SC-004 (UI-refusal rehearsal): post-merge runtime acts.
- Draft-PR trigger rendering and live timeout behavior: require a real PR run.

## Round 5 — Reviewer (gpt-5.6-terra, high) — REVISE → fixed → APPROVE

Reviewer's two MAJORs, both verified real before fixing:

1. `permissions: {}` would deny checkout its token on private repos → now
   `contents: read` (still least-privilege).
2. **CI-killer caught**: validator hard-requires `jsonschema>=4.18` (line 183) and
   `rfc3339-validator` (lines 240–241); local runs passed only because both were
   installed globally. Dependency step now installs all three packages.

**Decisive evidence**: clean venv containing ONLY the workflow's dependency set ran
both layers → exit 0 / exit 0.

Coder endpoint note: ox-alpha returned repeated network_errors on this micro-revision
(loaded free tier); re-routed to a GPT worker with the identical fully-specified prompt.

## Final state

- QA: PASS-WITH-NOTES (round 4) · Reviewer: APPROVE · Gates: openspec 68/68 strict,
  sweep + self-test green in clean venv.
- Diff: `.github/workflows/wallet-validation.yml` (new), `README.md` (+7 lines),
  spec artifacts under `specs/010-wallet-validator-ci/`.
- Two convener escalations open (invalid-YAML skip semantics; enforcement-plane
  boundary) — recorded above with options; not blocking per QA round-4 ruling.

## Round 6 — Convener-authorized hardening + CODEOWNERS (Phase 7)

Convener rulings 2026-08-23 encoded as Clarification Q6 / FR-011 / research R7.
Coder delivered (response stream timed out post-completion; deliverables verified
directly by orchestrator):

- `scripts/wallet-yaml-syntax-gate.py` — kind-aware syntax gate, vocabulary imported
  from the validator via importlib (no parallel copy), fail-closed exit-2 on harness
  error, UTF-8-decode failures treated as findings.
- `tests/wallet_yaml_syntax_gate/test_gate.py` — 4/4 passing.
- `.github/CODEOWNERS` — three gate paths routed to @brettheap (routing-only).
- Workflow wires the gate BEFORE the sweep; README notes owner-routing.

Orchestrator verification: clean-tree gate exit 0 · red probe (broken kind-bearing
file) exit 1 WITH file+error attribution — **hole closed** · isolated broken
non-kind file still skipped (exit 0) · venv parity green for both tools ·
openspec strict 68/68.

Awaiting round-7 QA/review verdicts.

## Residual risks ledger

- Lexically-encoded kind spellings (`kind: "xfactory_wallet_gr\u0061nt"`) evade the
  raw-text containment prefilter by design wording (QA round 7). A future upstream
  validator fix or stricter gate can close it; recorded, accepted for S1.
- Full pytest collection failures across tests/ are pre-existing on base HEAD
  (QA reproduced twice); not caused by this feature's files.
- `.omo/` and `.opencode/` session dirs excluded locally via module git info/exclude —
  must never enter the feature commit.

## Round 8 — Doc-consistency sweep + final verdicts

QA round-7 MINORs resolved: plan/research/tasks/quickstart stale claims purged via
asserted replacements (R5 SUPERSEDED-IN-PART header; tasks header reconciled; quickstart
prerequisites corrected to all three packages; Scope/Structure updated); clarify Q5/Q6
mirrored; spec Assumptions count fixed 18→29; `.omo/` excluded locally.
Residual risks ledger appended (encoded-kind spellings; pre-existing pytest collection).

Final gates: QA PASS-WITH-NOTES (round 7) · Reviewer **APPROVE**, no findings (round 4) ·
openspec strict 68/68 · gate+sweep+self-test green in clean venv · red/green probes
correct (broken kind-file fails with attribution; unrelated broken file still skipped).

## Round 7 — Merge + Path B (council lane) verification

- **PR #274 admin-merged** on convener's explicit order (ruleset code-owner requirement
  bypassed; parent change preserves `--admin` as inherited control). main @ `b88ada4`.
- **Path B finding: the council lane was already registered** — App ID var+secrets
  (`4397053`), all six §4 variables, stale `HERMES_RUNTIME_TOKEN` correctly absent.
  The 2026-07-26 first-version App work stands per the runbook's own table; the
  2026-07-27 QA-stack rehearsal recorded in `add-council-clearance-lane-wiring`
  covers the Entra federation and principal row.
- **§6.1 PASS by construction**: `vars.COUNCIL_LANE_APP_ID` set → the "transport
  unverifiable" warning precondition is false. Live dispatch of
  `merge-master-approval` succeeded (early-exit "no governed head refs" — expected,
  nothing open at dispatch time).
- **§6.2 configuration guard PASSED**: dispatching `council-convening-lane` with
  pr_number=274 showed `HAS_APP_ID/KEY: true` and all runtime vars loaded before
  failing on wrong-target lookup — #274 is an **openxFactory** PR while this lane's
  installation resolves candidates in **opensoft/xFactory** only.
- **Follow-up decisions surfaced**: (a) extend lane App installation (+ target support)
  if openxFactory-repo PRs are to receive verdict check-runs directly; (b) choose the
  first live commissioning candidate among open aggregation PRs (#141/#22/#21/#5);
  (c) confirm intended tier-2 activation state (job label reads "tier 2, active";
  runbook §7 and the `activate-nightly-sweep-council-clearance` proposal describe the
  gate-flip as its own recorded event).
