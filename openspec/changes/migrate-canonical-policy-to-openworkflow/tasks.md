## 1. Proposal And Approval

- [x] 1.1 Validate proposal, design, specs, and tasks.
- [x] 1.2 Record Hermes approval to proceed with dogfood decomposition.
- [x] 1.3 Confirm migration uses copy-first feature slices and no direct bulk reshuffle.

## 2. FEAT-MIG-001 Roles And Authority

- [x] 2.1 Inventory source role docs from `Omnigent-Install` and `Hermes-Install`.
- [x] 2.2 Create `openWorkflow/docs/roles-and-authority.md`.
- [x] 2.3 Define PO, PM, CA, PA, LA, LE, LC, LQ, LI, LS, Merge Master, and Merge Council.
- [x] 2.4 Separate Hermes governance roles from Omnigent execution roles.
- [x] 2.5 Preserve source provenance and update `openWorkflow` README.
- [x] 2.6 Validate OpenSpec and record PR admission/merge readiness evidence.

## 3. FEAT-MIG-002 Spec Kit Stage Ownership And Clarification Routing

- [x] 3.1 Inventory clarification and Spec Kit stage source docs.
- [x] 3.2 Create `openWorkflow/docs/spec-kit-stage-ownership.md`.
- [x] 3.3 Define `/speckit.specify`, `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.analyze`, and `/speckit.implement` ownership.
- [x] 3.4 Define clarification routing from LE to PO, PM, PA, LS, LQ, LI, and LC.
- [x] 3.5 Add install repo link/update evidence.

## 4. FEAT-MIG-003 PR Admission, Merge Council, And Merge Master

- [x] 4.1 Inventory PR admission, merge council, merge master, and merge risk sources.
- [x] 4.2 Create `openWorkflow/docs/pr-admission.md`.
- [x] 4.3 Create `openWorkflow/docs/merge-master.md`.
- [x] 4.4 Update `openWorkflow/docs/merge-council.md` if canonical gaps remain.
- [x] 4.5 Add install repo link/update evidence.

## 5. FEAT-MIG-004 Feature Decomposition And Traceability

- [ ] 5.1 Inventory decomposition and traceability source docs/examples.
- [ ] 5.2 Update `openWorkflow/docs/feature-decomposition.md`.
- [ ] 5.3 Update `openWorkflow/docs/traceability-model.md`.
- [ ] 5.4 Preserve bug-to-feature mapping and PR size constraints.
- [ ] 5.5 Add source provenance and validation evidence.

## 6. FEAT-MIG-005 Shared Contract Migration

- [ ] 6.1 Inventory `Omnigent-Install/schemas` and policy YAML sources.
- [ ] 6.2 Copy canonical contracts into `openWorkflow/contracts`.
- [ ] 6.3 Add source, version, compatibility, and adapter ownership notes.
- [ ] 6.4 Validate contract syntax where applicable.
- [ ] 6.5 Confirm install repo schema copies are not deleted in this feature.

## 7. FEAT-MIG-006 Reference Pilot And Example Placement

- [ ] 7.1 Inventory Project Alfa, live pilot, merge master, and pilot-flow examples.
- [ ] 7.2 Add placement decision for `openWorkflow/examples`, `factory-lab`, or temporary status quo.
- [ ] 7.3 Copy only approved canonical reference examples.
- [ ] 7.4 Exclude generated state, credentials, databases, logs, and local workspaces.

## 8. FEAT-MIG-007 Mark Install Repo Policy Copies

- [ ] 8.1 Update migrated `Omnigent-Install` source docs with canonical links or legacy labels.
- [ ] 8.2 Update migrated `Hermes-Install` source docs with canonical links or legacy labels.
- [ ] 8.3 Run install repo validation and no-secret checks.
- [ ] 8.4 Record install repo PR evidence in OpenSpec.

## 9. FEAT-MIG-008 Removal Or Cleanup Decision

- [ ] 9.1 Decide whether legacy policy copies should be removed, archived, or kept.
- [ ] 9.2 If removals are approved, isolate them in dedicated PRs.
- [ ] 9.3 Confirm no runtime files, scripts, manifests, or generated adapters are removed by policy cleanup.
- [ ] 9.4 Document rollback path.

## 10. Final Validation And Archive

- [ ] 10.1 Validate `migrate-canonical-policy-to-openworkflow` with `openspec validate --all --strict`.
- [ ] 10.2 Confirm all feature slices have evidence and merge readiness reports.
- [ ] 10.3 Confirm install repos link to canonical policy.
- [ ] 10.4 Confirm no active stop conditions remain.
- [ ] 10.5 Archive the OpenSpec change after all approved slices complete.
