# Tasks: Wallet Validator CI Gate (S1)

**Feature**: 010-wallet-validator-ci | **Branch**: `010-wallet-validator-ci` | **Date**: 2026-08-23
**Input**: [spec.md](./spec.md) · [plan.md](./plan.md) · [research.md](./research.md) · [data-model.md](./data-model.md) · [quickstart.md](./quickstart.md)

Tests note: the validator's native layer-1 corpus assertion is exercised by every task
via real invocations; additionally, Phase 7 (convener-authorized hardening) added a
dedicated pytest suite `tests/wallet_yaml_syntax_gate/` for the FR-011 helper.

## Phase 1 — Setup

No project initialization required (existing repo, existing tooling).

## Phase 2 — Foundational

- [x] T001 Baseline proof: run `python3 scripts/validate-openxwallet.py` (self-test mode) and `python3 scripts/validate-openxwallet.py .` (sweep) from repo root; record both exit codes and any warning lines as implementation evidence. Confirms the tool being wired is green BEFORE wiring (plan.md R2, quickstart Scenarios 1–2).

## Phase 3 — User Story 1: A malformed grant can no longer enter the tree unnoticed (P1)

**Goal**: Every PR to main runs a check named exactly `wallet-validation` that fails on malformed live artifacts within the fail-closed budget.

**Independent test**: quickstart Scenario 4 (check present on PR, correct name/budget/permissions) plus Scenario 3 rehearsal proving detection of a de-headered negative specimen adjudicated as live.

- [x] T002 [US1] Create `.github/workflows/wallet-validation.yml` (as amended by review rounds: `permissions: contents: read`; dependency step installs pyyaml+jsonschema+rfc3339-validator; Phase 7 prepends the syntax-gate step): `name: wallet-validation`; trigger `on: pull_request` targeting `main` default types (drafts included); single UNNAMED job, `ubuntu-latest`, `timeout-minutes: 10`. No scoping logic, no `--strict` (R2/R4/R5; R5 partly superseded — see its header note).
- [x] T003 [US1] Rehearse detection locally per quickstart Scenario 3 (scratch copy under `/tmp/opencode/`, strip an expected-failure header, observe non-zero exit naming the file and rule); capture command output as evidence; clean up scratch. Validates FR-003 attribution and FR-006 fail-closed behavior end-to-end without opening a PR.

## Phase 4 — User Story 2: Conforming content passes with zero false positives (P2)

**Goal**: The check mirrors the manual verdict — green on today's tree, warnings never fatal.

**Independent test**: quickstart Scenario 2 green on this branch; warning lines (if any) logged only.

- [x] T004 [US2] Confirm sweep semantics on this branch: rerun `python3 scripts/validate-openxwallet.py .`; assert exit 0; assert that any warning output appears without failing; record observation count of skipped non-family kinds if printed. Evidence appended to implementation notes (FR-005, FR-010).

## Phase 5 — User Story 3: The check becomes un-bypassable at merge time (P3)

**Goal**: The operator can, in under a minute post-merge, mark `wallet-validation` required.

**Independent test**: README section alone suffices to execute Settings → Branches → main → require status checks → select `wallet-validation`.

- [x] T005 [US3] Add top-level `README.md` section titled `## Wallet validation gate`: states the check name literally (`wallet-validation`), that it runs on every PR to main including drafts, that it is ADVISORY until the operator marks it required, and the exact click-path — rulesets-first (Settings → Rules → Rulesets → ruleset targeting main → Require status checks → add `wallet-validation`) with classic branch-protection alternative (QA-verified: this repo enforces via rulesets) per FR-007; placed before `## Domain Implementations`.

## Phase 6 — Polish & Cross-Cutting

- [x] T006 Run repository gates per Constitution Principle V and record results: `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`; rerun both Scenario 1 and Scenario 2 commands as the affected-repo-validator evidence for this diff.
- [x] T007 Orchestrator cross-check against spec: walk FR-001…FR-010 and SC-001…SC-004 marking satisfied-by-evidence or explicitly deferred-to-PR-runtime (SC-001's N≥5 PRs, SC-004's UI refusal rehearsal are post-merge observations by definition); note deferrals in implementation notes, not as silent gaps.

## Dependencies

- T001 → T002 (never wire a red tool)
- T002 → T003, T004 (rehearsals exercise the wired invocation)
- T003, T004 → T006 (gates run after content settles)
- T005 independent of T002–T004 (docs-only); T007 last

## Parallel execution examples

- After T001: T002 and T005 can proceed in parallel ([P] candidates if delegated separately).
- T003 and T004 both depend only on T002; they may run in sequence or parallel once the workflow exists.

## Implementation strategy

MVP = T001–T003 (the gate exists, is named right, and provably catches malformations).
T004–T005 complete the ratified stories; T006–T007 close governance evidence.
(Historical delegation context from the original two-file build: T002+T005 were
delegated as one atomic unit before Phase 7 expanded scope.)
verification tasks are orchestrator-run commands, not code.

## Phase 7 — Convener-authorized hardening + enforcement-plane mitigation

- [x] T008 [P] Implement `scripts/wallet-yaml-syntax-gate.py` per research.md R7: importlib path-load `KIND_TO_SCHEMA` from `scripts/validate-openxwallet.py`; walk `<path>/**/*.y*ml`; for any file whose raw text contains a family kind string and whose `yaml.safe_load_all` raises, print ERROR with file+parse message and exit 1; else exit 0. Plus pytest pair under `tests/wallet_yaml_syntax_gate/` covering: broken wallet-kind file → gate fails naming file; broken non-wallet file → gate passes; valid wallet-kind example → passes; valid unrelated yaml → passes.
- [x] T009 [P] Create `.github/CODEOWNERS` routing `.github/workflows/** @brettheap`, `/scripts/validate-openxwallet.py @brettheap`, `/scripts/wallet-yaml-syntax-gate.py @brettheap` with a comment header noting routing-only per convener ruling 2026-08-23. Add one sentence to README 'Wallet validation gate' section noting these paths are owner-routed.
- [x] T010 Wire helper into `.github/workflows/wallet-validation.yml` as a step BEFORE the validator run: `python3 scripts/wallet-yaml-syntax-gate.py .`

## Dependencies (hardening phase)

T008 → T010 (gate must exist before wiring); T009 independent. All land before final QA/review round.

## Post-analyze record

- QA round 3 FAIL dispositions: MAJOR fixed (rulesets-first README); BLOCKER×2 resolved by convener rulings 2026-08-23 (hardening authorized → this phase; enforcement-plane → CODEOWNERS here + sibling changes).
- Reviewer round 1 REVISE → both MAJORs fixed (contents: read; full dependency install), clean-venv parity proven, APPROVE on re-review. Re-reviewed again after this phase lands.
