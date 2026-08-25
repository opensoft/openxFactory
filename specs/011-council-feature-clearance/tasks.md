# Tasks: Council Review for Feature PRs (Lane Intake)

**Feature**: 011-council-feature-clearance | **Branch**: `011-council-feature-clearance` | **Date**: 2026-08-23
**Input**: [spec.md](./spec.md) · [plan.md](./plan.md) · [research.md](./research.md) · [data-model.md](./data-model.md) · [quickstart.md](./quickstart.md)

Cross-repo note: executable widening lands in **opensoft/xFactory** (aggregation root,
branch `011-council-feature-clearance` cut there); explicit-path staging only — the
root checkout carries unrelated operator WIP (`.azure/plan.md`, `installs/cloudpc-install`).

## Phase 1 — Setup

- [x] T001 Baseline evidence: current envelope parses and contains exactly one candidate (`doc-health-nightly`); approval-workflow dispatch succeeds with early-exit "No governed head refs"; lane config guard passes (`HAS_APP_ID/KEY: true`) on wrong-target dispatch. Recorded in implementation notes.

## Phase 2 — User Story 3: coverage extends beyond a single repository (P3, safe subset)

- [x] T002 [US3] Parameterize `.github/workflows/council-convening-lane.yml` (opensoft/xFactory): add optional `pr_repo` string input (default empty → resolves to `${{ github.repository }}`), replacing the three hardwired `REPO:` values (lines ~140/~308/~370); byte-identical behavior when unset; emission token scope continues to derive from the resolved target repo.
- [x] T003 [US3] Add a coverage/intake section to opensoft/xFactory `README.md` adjacent to the existing tier-2 section: covered repositories and classes AFTER this change, the per-effort intake procedure (add one reviewed exact-ref envelope entry at effort-open), the advisory-only posture statement, the floor statement (assembly classes permanently human-only), and the second-repo prerequisite (operator extends lane App installation before emission can succeed there).
- [x] T004 [P] [US3] Append a COMMENTED template block to `.github/merge-approval-envelope.yml` documenting the per-effort candidate-entry shape (id / target_repos / expected_author / expected_head_ref / path_allowlist) with a header note that entries are added by reviewed edit at effort-open and removed by deleting one block. Comments only — parsed document unchanged (schema regression proof required).

## Phase 3 — User Story 1: recorded verdicts on feature PRs (P1)

**ESCALATED — blocked on convener classification-mechanics ruling (research.md R4).**
Under ACTIVE tier-2, a human-authored feature candidate whose facts prove clearable
could be autonomously approved by the merge-master App; advisory-first intent cannot
be encoded in the envelope (schema fact). Options (a)/(b)/(c) presented to the
convener. No live candidate entry for any human-authored PR lands until ruled.

- [ ] T005 [US1] **(ESCALATED)** Add the pilot exact-ref envelope entry (proposed subject: existing low-risk PR #22 or the next qualifying effort branch), rehearse Scenario 3 end-to-end: awaiting_verdict → auto-commission → identity-bound verdict check-run.
- [ ] T010 [US1] **(ESCALATED)** Observe and record the first real verdict artifact (SC-001 completion evidence).

## Phase 4 — User Story 2: floor refusals stay loud (P2)

- [ ] T006 [US2] **(ESCALATED, shares T005's gate)** Rehearse the named-refusal path on an assembly-class candidate (#141 proposed): dispatch → configuration guard passes → preflight refuses with never-clearable outcome → zero runtime jobs; idempotent re-dispatch. Requires the class entry from the same ruling.

## Phase 5 — Polish & Cross-Cutting

- [x] T007 Gates: openspec validate --all --strict (openxFactory side, 68/68 at plan time — rerun at close); envelope instance validated against codexFactory schema v1 locally (python jsonschema) before and after template-block append; nightly classification regression fixture unchanged.
- [x] T008 Orchestrator cross-check: FR-001…FR-008 / SC-001…SC-003 walk marking satisfied-by-evidence vs escalated-deferred (T005/T006/T010 carry the deferral flags; nothing silent).

## Dependencies

- T002 → T003/T004 independent of each other; T005/T006 blocked by convener ruling (not by code); T007 after all landing moves; T008 last.

## Parallel execution examples

- T002 ∥ T003 ∥ T004 touch disjoint files (lane workflow / README / envelope comments).

## Implementation strategy

Safe scaffolding (T001–T004, T007–T008) lands and is review-gated immediately; the
live-entry pair (T005/T006/T010) executes in one focused pass once the convener rules
on classification mechanics — estimated Quick (<1h) including both rehearsals.
