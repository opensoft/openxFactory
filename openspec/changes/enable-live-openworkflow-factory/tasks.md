## 1. Proposal And Governance

- [x] 1.1 Create proposal, design, task list, and runtime capability specs.
- [x] 1.2 Validate `enable-live-openworkflow-factory` with OpenSpec strict mode.
- [x] 1.3 Record Hermes approval to proceed with live runtime implementation.

## 2. Contract Pinning And Compatibility

- [ ] 2.1 Add or update Omnigent contract compatibility reference.
- [ ] 2.2 Add or update Hermes contract compatibility reference.
- [ ] 2.3 Add install validation for referenced `openWorkflow` commit and required contracts.
- [ ] 2.4 Confirm local compatibility copies are not deleted.
- [ ] 2.5 Record install repo PR evidence and update submodule pins where applicable.

## 3. Hermes Runtime Control Plane

- [ ] 3.1 Verify Hermes API supports jobs, runs, events, artifacts, approvals, and traceability.
- [ ] 3.2 Verify Hermes uses Postgres operational schema from canonical contract.
- [ ] 3.3 Add or update smoke test for create/query/control-plane lifecycle.
- [ ] 3.4 Record runtime evidence and stop-condition checks.

## 4. Omnigent Worker Event Bridge

- [ ] 4.1 Verify worker-side Hermes event client uses canonical event contract.
- [ ] 4.2 Verify marker fallback remains compatible.
- [ ] 4.3 Add idempotency check for duplicate bridge keys.
- [ ] 4.4 Add no-op behavior check when Hermes API environment is absent.
- [ ] 4.5 Record worker bridge evidence.

## 5. Spec Kit Stage Control And Clarification Routing

- [ ] 5.1 Verify all Spec Kit stage owners match canonical policy.
- [ ] 5.2 Verify clarification questions route to mapped authority roles.
- [ ] 5.3 Verify answer packets require Hermes approval before application.
- [ ] 5.4 Run Project Alfa reduced-agent clarify smoke.
- [ ] 5.5 Record Spec Kit control evidence.

## 6. Project Alfa Live Pilot

- [ ] 6.1 Select or confirm the low-risk Project Alfa pilot feature.
- [ ] 6.2 Run or replay decomposition, Spec Kit, branch, check, and review flow.
- [ ] 6.3 Verify changed-line budget and traceability.
- [ ] 6.4 Record pilot evidence bundle.

## 7. PR Admission, Merge Council, And Merge Master

- [ ] 7.1 Verify PR admission blocks missing checks, review, traceability, and over-budget changes.
- [ ] 7.2 Verify GitHub PR opens only after Hermes admission approval.
- [ ] 7.3 Verify Merge Council produces readiness report from GitHub evidence.
- [ ] 7.4 Verify Merge Master dry-run classifies low/medium/high risk and routes human review.
- [ ] 7.5 Record PR/merge evidence.

## 8. CloudPC Worker, Auth, Memory, And Operations

- [ ] 8.1 Verify CloudPC worker pack runbook and Docker Compose layout.
- [ ] 8.2 Verify auth profile restore/onboarding runbooks avoid committed secrets.
- [ ] 8.3 Verify worker memory rules treat memory as context, not canonical truth.
- [ ] 8.4 Verify operations and DR smoke sequence is documented.
- [ ] 8.5 Record operations readiness evidence.

## 9. Final Validation And Archive

- [ ] 9.1 Run OpenSpec strict validation.
- [ ] 9.2 Run contract and example syntax checks.
- [ ] 9.3 Run applicable install repo smoke tests.
- [ ] 9.4 Confirm all feature slices have evidence and merge readiness reports.
- [ ] 9.5 Archive the OpenSpec change after approved slices complete.
