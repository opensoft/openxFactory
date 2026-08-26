# Implementation Plan: Council Review for Feature PRs (Lane Intake)

**Branch**: `011-council-feature-clearance` | **Date**: 2026-08-23 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/011-council-feature-clearance/spec.md`

## Summary

Convert the verified-live council lane from single-candidate rehearsal posture to
covering feature PRs on both engineering repos (`opensoft/xFactory`,
`opensoft/openxFactory`), ADVISORY-only, via the intake-per-effort mechanism ruled in
Clarifications Q1/Q2: each feature effort records one reviewed exact-ref envelope
entry; the lane auto-commissions on qualifying candidates; floor classes are refused
with named outcomes. Delivered artifacts: envelope entries (pilot subject + commented
template), lane repository-parameterization, README coverage/intake documentation in
both repos, and the first live convening rehearsed against an existing low-risk PR.

## Technical Context

**Language/Version**: GitHub Actions YAML; Python 3.12 (existing cores); no new runtime deps

**Primary Dependencies**: Existing verified lane stack — `merge-master-approval.yml`,
`council-convening-lane.yml` (xFactory), Hermes QA runtime (`hermes-opensoft-qa`),
lane App `4397053`, envelope schema v1 (codexFactory-owned, UNCHANGED)

**Storage**: N/A (verdicts remain SHA-bound check-runs; principal store untouched)

**Testing**: Real-dispatch rehearsals against existing open PRs (#22 pilot subject,
#141 floor-refusal demo) plus regression proof on the nightly fixture; pytest N/A

**Target Platform**: GitHub Actions (xFactory aggregation workflows)

**Project Type**: Governance wiring — reviewed rules-as-code widening + lane parameterization

**Performance Goals**: Classification within normal approval-run duration; commission
within one workflow_run signal of `awaiting_verdict`

**Constraints**: Envelope read from BASE branch only (entry live post-merge);
validator semantics locked (FR-002 analog: tier-1/tier-2 fact pipeline unchanged);
advisory-only posture (Q1); floor refusals idempotent (FR-004); App install on
second repo is an operator prerequisite (FR-008)

**Scale/Scope**: One envelope file + one lane workflow + two README sections
(xFactory, openxFactory) + spec artifacts. Nothing else.

## Constitution Check

*GATE: PASS before Phase 0; re-checked after Phase 1 design.*

| Principle | Verdict | Notes |
|---|---|---|
| I. Contract-first neutral core | PASS | Widening consumes codexFactory schema v1 as-is; no contract bytes change |
| II. Governed change flow | PASS | This feature IS the ratified intake act for lane extension (roles-authority-model MODIFIED delta) |
| III. Document lifecycle/status | PASS | Advisory posture documented; no gate-flip claimed (activation already recorded ACTIVE in xFactory README) |
| IV. Schema & artifact discipline | PASS | Envelope entry follows schema v1 required fields; no credentials; repo-relative paths |
| V. Validation gates | PASS by construction | Evidence = real dispatches: classification outputs, commission/emit logs, refusal rehearsals |
| VI. Versioned releases | PASS | No contracts/ bundle change (schema consumed at pinned version) |
| VII. Fail-closed boundaries | PASS | Refusals named + idempotent; emission fail-closed names missing App installation |

**Worktree/shared-tree discipline**: openxFactory artifacts on feature worktree;
cross-repo realization edits staged EXPLICIT PATH ONLY in the xFactory root checkout
(known unrelated WIP present: `.azure/plan.md`, `installs/cloudpc-install`) on a
dedicated branch cut from current main.

## Project Structure

### Documentation (this feature)

```text
specs/011-council-feature-clearance/
├── plan.md / research.md / quickstart.md / data-model.md
├── clarify-questions.md / checklists/ / tasks.md
```

### Source Code (repository root — CROSS-REPO)

```text
opensoft/xFactory (aggregation):          # realized on branch 011-council-feature-clearance THERE
├── .github/merge-approval-envelope.yml   # MODIFIED — pilot entry (#22) + commented template block
├── .github/workflows/council-convening-lane.yml  # MODIFIED — optional pr_repo input (default unchanged)
└── README.md                             # MODIFIED — coverage + per-effort intake procedure
opensoft/openxFactory (this worktree):    # spec artifacts only (this directory)
```

**Structure Decision**: All executable widening lands in the aggregation repo where
the governed surfaces live; this openxFactory feature carries the intake record and
spec governance. `contracts/` skipped — no interface contract change; the interface
is the existing envelope schema consumed unchanged.

## Complexity Tracking

No constitution violations — table intentionally empty.
