## 1. Proposal And Governance

- [x] 1.1 Create proposal, design, task list, and runtime capability specs.
- [x] 1.2 Validate `enable-live-openworkflow-factory` with OpenSpec strict mode.
- [x] 1.3 Record Hermes approval to proceed with live runtime implementation.

## 2. Contract Pinning And Compatibility

- [x] 2.1 Add or update Omnigent contract compatibility reference.
- [x] 2.2 Add or update Hermes contract compatibility reference.
- [x] 2.3 Add install validation for referenced `openWorkflow` commit and required contracts.
- [x] 2.4 Confirm local compatibility copies are not deleted.
- [x] 2.5 Record install repo PR evidence and update submodule pins where applicable.

## 3. Hermes Runtime Control Plane

- [x] 3.1 Verify Hermes API supports jobs, runs, events, artifacts, approvals, and traceability.
- [x] 3.2 Verify Hermes uses Postgres operational schema from canonical contract.
- [x] 3.3 Add or update smoke test for create/query/control-plane lifecycle.
- [x] 3.4 Record runtime evidence and stop-condition checks.

## 4. Omnigent Worker Event Bridge

- [x] 4.1 Verify worker-side Hermes event client uses canonical event contract.
- [x] 4.2 Verify marker fallback remains compatible.
- [x] 4.3 Add idempotency check for duplicate bridge keys.
- [x] 4.4 Add no-op behavior check when Hermes API environment is absent.
- [x] 4.5 Record worker bridge evidence.

## 5. Spec Kit Stage Control And Clarification Routing

- [x] 5.1 Verify all Spec Kit stage owners match canonical policy.
- [x] 5.2 Verify clarification questions route to mapped authority roles.
- [x] 5.3 Verify answer packets require Hermes approval before application.
- [x] 5.4 Run Project Alfa reduced-agent clarify smoke.
- [x] 5.5 Record Spec Kit control evidence.

## 6. Project Alfa Live Pilot

- [x] 6.1 Select or confirm the low-risk Project Alfa pilot feature.
- [x] 6.2 Run or replay decomposition, Spec Kit, branch, check, and review flow.
- [x] 6.3 Verify changed-line budget and traceability.
- [x] 6.4 Record pilot evidence bundle.

## 7. PR Admission, Merge Council, And Merge Master

- [x] 7.1 Verify PR admission blocks missing checks, review, traceability, and over-budget changes.
- [x] 7.2 Verify GitHub PR opens only after Hermes admission approval.
- [x] 7.3 Verify Merge Council produces readiness report from GitHub evidence.
- [x] 7.4 Verify Merge Master dry-run classifies low/medium/high risk and routes human review.
- [x] 7.5 Record PR/merge evidence.

## 8. CloudPC Worker, Auth, Memory, And Operations

- [x] 8.1 Verify CloudPC worker pack runbook and Docker Compose layout.
- [x] 8.2 Verify auth profile restore/onboarding runbooks avoid committed secrets.
- [x] 8.3 Verify worker memory rules treat memory as context, not canonical truth.
- [x] 8.4 Verify operations and DR smoke sequence is documented.
- [x] 8.5 Record operations readiness evidence.

## 9. Final Validation And Archive

- [x] 9.1 Run OpenSpec strict validation.
- [x] 9.2 Run contract and example syntax checks.
- [x] 9.3 Run applicable install repo smoke tests.
- [x] 9.4 Confirm all feature slices have evidence and merge readiness reports.
- [x] 9.5 Archive the OpenSpec change after approved slices complete.
