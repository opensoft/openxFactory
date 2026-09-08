## 1. Proposal And Approval

- [x] 1.1 Validate proposal, design, specs, and tasks.
- [x] 1.2 Record Hermes approval to proceed with dogfood decomposition.
- [x] 1.3 Confirm migration uses copy-first feature slices and no direct bulk reshuffle.

## 2. FEAT-MIG-001 Roles And Authority

- [x] 2.1 Inventory source role docs from `Omnigent-Install` and `Hermes-Install`.
- [x] 2.2 Create `openxFactory/docs/roles-and-authority.md`.
- [x] 2.3 Define PO, PM, CA, PA, LA, LE, LC, LQ, LI, LS, Merge Master, and Merge Council.
- [x] 2.4 Separate Hermes governance roles from Omnigent execution roles.
- [x] 2.5 Preserve source provenance and update `openxFactory` README.
- [x] 2.6 Validate OpenSpec and record PR admission/merge readiness evidence.

## 3. FEAT-MIG-002 Spec Kit Stage Ownership And Clarification Routing

- [x] 3.1 Inventory clarification and Spec Kit stage source docs.
- [x] 3.2 Create `openxFactory/docs/spec-kit-stage-ownership.md`.
- [x] 3.3 Define `/speckit.specify`, `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.analyze`, and `/speckit.implement` ownership.
- [x] 3.4 Define clarification routing from LE to PO, PM, PA, LS, LQ, LI, and LC.
- [x] 3.5 Add install repo link/update evidence.

## 4. FEAT-MIG-003 PR Admission, Merge Council, And Merge Master

- [x] 4.1 Inventory PR admission, merge council, merge master, and merge risk sources.
- [x] 4.2 Create `openxFactory/docs/pr-admission.md`.
- [x] 4.3 Create `openxFactory/docs/merge-master.md`.
- [x] 4.4 Update `openxFactory/docs/merge-council.md` if canonical gaps remain.
- [x] 4.5 Add install repo link/update evidence.

## 5. FEAT-MIG-004 Feature Decomposition And Traceability

- [x] 5.1 Inventory decomposition and traceability source docs/examples.
- [x] 5.2 Update `openxFactory/docs/feature-decomposition.md`.
- [x] 5.3 Update `openxFactory/docs/traceability-model.md`.
- [x] 5.4 Preserve bug-to-feature mapping and PR size constraints.
- [x] 5.5 Add source provenance and validation evidence.

## 6. FEAT-MIG-005 Shared Contract Migration

- [x] 6.1 Inventory `Omnigent-Install/schemas` and policy YAML sources.
- [x] 6.2 Copy canonical contracts into `openxFactory/contracts`.
- [x] 6.3 Add source, version, compatibility, and adapter ownership notes.
- [x] 6.4 Validate contract syntax where applicable.
- [x] 6.5 Confirm install repo schema copies are not deleted in this feature.

## 7. FEAT-MIG-006 Reference Pilot And Example Placement

- [x] 7.1 Inventory Project Alfa, live pilot, merge master, and pilot-flow examples.
- [x] 7.2 Add placement decision for `openxFactory/examples`, `factory-lab`, or temporary status quo.
- [x] 7.3 Copy only approved canonical reference examples.
- [x] 7.4 Exclude generated state, credentials, databases, logs, and local workspaces.

## 8. FEAT-MIG-007 Mark Install Repo Policy Copies

- [x] 8.1 Update migrated `Omnigent-Install` source docs with canonical links or legacy labels.
- [x] 8.2 Update migrated `Hermes-Install` source docs with canonical links or legacy labels.
- [x] 8.3 Run install repo validation and no-secret checks.
- [x] 8.4 Record install repo PR evidence in OpenSpec.

## 9. FEAT-MIG-008 Removal Or Cleanup Decision

- [x] 9.1 Decide whether legacy policy copies should be removed, archived, or kept.
- [x] 9.2 If removals are approved, isolate them in dedicated PRs.
- [x] 9.3 Confirm no runtime files, scripts, manifests, or generated adapters are removed by policy cleanup.
- [x] 9.4 Document rollback path.

## 10. Final Validation And Archive

- [x] 10.1 Validate `migrate-canonical-policy-to-openxfactory` with `openspec validate --all --strict`.
- [x] 10.2 Confirm all feature slices have evidence and merge readiness reports.
- [x] 10.3 Confirm install repos link to canonical policy.
- [x] 10.4 Confirm no active stop conditions remain.
- [x] 10.5 Archive the OpenSpec change after all approved slices complete.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 1 and 2, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `d7b66d7` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
