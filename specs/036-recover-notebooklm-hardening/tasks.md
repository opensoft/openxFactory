# Recovery implementation tasks

## Baseline and foundations

- [x] T001 Record current main and historical branch identities and scenario inventory (FR-007/008).
- [x] T002 Reconcile OpenSpec scope/authorization and create the single feature (FR-008).
- [x] T003 Recover verified original checker provenance and record baseline collection (FR-006/007).
- [x] T004 Recover typed models/provider state, package and compatibility wrapper (FR-001/004/005).

## US1 — Current behavior

- [x] T005 Preserve current corpus/root products, title disambiguation and workspace records (FR-003).
- [x] T006 Preserve readiness, settled rename and digest-matched adoption with current regression tests (FR-002).
- [x] T007 Preserve hosting path order, scope, optional imports and session registration (FR-003/004).
- [x] T008 Preserve current CLI modes, errors and patchable helper seams (FR-001).

## US2 — Boundaries

- [x] T009 Recover focused typed tests and merge the union of current/historical scenarios (FR-004/007).
- [x] T010 Enforce acyclic responsibility boundaries and module size ceiling (FR-005).

## US3 — Quality

- [x] T011 Recover scoped quality gate/config, fix all findings without suppressions and prove negative probes (FR-006).
- [x] T012 Run pytest and guarded unittest, collection, CLI probes and affected validators; record exact evidence (FR-001/007).

## Landing and disposition

- [ ] T013 Resolve the recorded pre-push strict gate, publish the verified code head, seed the governance ledger with that real PR identity, publish the prepared packet, request exact-head Codex review, pass required CI and land (FR-008).
- [ ] T014 Verify exact old snapshot restoration, preserve any working files and remove superseded ref/worktree only after landing (FR-008).
- [ ] T015 Record final disposition and archive/promote the governed change after landing (FR-008).

Dependencies: T004 follows baseline; T005–T008 follow foundations; T009 merges
scenarios after behavioral reconciliation; T010/T011 complete before T012;
T013–T015 are sequential. Each story can be validated hermetically on its own
boundary. No publication task bypasses the recorded strict-validation blocker.
