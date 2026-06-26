## 1. Proposal And Approval

- [x] 1.1 Review `proposal.md`, `design.md`, and specs with Hermes governance.
- [x] 1.2 Record Hermes approval to proceed with decomposition.
- [x] 1.3 Confirm the first implementation feature is doc-only and `openWorkflow` only.

## 2. FEAT-RB-001 Canonical Boundary Policy

- [x] 2.1 Verify `docs/repo-boundary-audit.md` states canonical ownership for `openWorkflow`, `Hermes-Install`, and `Omnigent-Install`.
- [x] 2.2 Verify `docs/repo-boundary-pilot-plan.md` states the doc-only guardrails and stop conditions.
- [x] 2.3 Add or update README links so the boundary policy and pilot plan are discoverable.
- [x] 2.4 Run local doc and OpenSpec validation for the feature.
- [x] 2.5 Record branch review and PR admission evidence for the feature.

## 3. FEAT-RB-002 Contract Home Placeholder

- [x] 3.1 Create `contracts/README.md` in `openWorkflow`.
- [x] 3.2 List planned shared contracts and schema names.
- [x] 3.3 Document contract source-of-truth, version pinning, adapter, and generated-copy rules.
- [x] 3.4 Validate that no install repo files are changed in this feature.

## 4. FEAT-RB-003 Omnigent-Install Scope Link

- [x] 4.1 Update `Omnigent-Install` README to state its install, worker runtime, operations, and DR scope.
- [x] 4.2 Link `Omnigent-Install` to canonical `openWorkflow` boundary and workflow policy.
- [x] 4.3 Mark duplicate policy material as implementation notes or legacy copies where appropriate.
- [x] 4.4 Run existing `Omnigent-Install` smoke checks.

## 5. FEAT-RB-004 Hermes-Install Scope Link

- [x] 5.1 Update `Hermes-Install` README to state its Hermes install, operations, backup, restore, upgrade, and DR scope.
- [x] 5.2 Link `Hermes-Install` to canonical `openWorkflow` boundary and workflow policy.
- [x] 5.3 Document the unresolved `Hermes-Install` remote ownership decision.
- [x] 5.4 Verify no deployment scripts or manifests change in this feature.

## 6. FEAT-RB-005 Submodule Decision Record

- [x] 6.1 Add an `openWorkflow` decision record for install repo submodules.
- [x] 6.2 Document proposed paths `installs/hermes-install` and `installs/omnigent-install`.
- [x] 6.3 Document update, rollback, and pinned-commit procedure.
- [x] 6.4 Record that Hermes submodule creation waits for the remote ownership decision.

## 7. FEAT-RB-006 First Actual Submodule Add

- [x] 7.1 Confirm FEAT-RB-001 through FEAT-RB-005 are merged.
- [x] 7.2 Confirm install repo scope docs are updated and approved.
- [x] 7.3 Add only the approved first install repo submodule.
- [x] 7.4 Validate fresh clone and submodule initialization.
- [ ] 7.5 Record merge council readiness evidence before merge.

## 8. Final Validation

- [x] 8.1 Validate the OpenSpec change with `openspec validate restructure-factory-repo-boundaries --strict`.
- [x] 8.2 Confirm no secrets, credential profiles, generated databases, or runtime state are tracked.
- [x] 8.3 Confirm each implemented feature has acceptance evidence.
- [ ] 8.4 Archive the OpenSpec change only after all approved feature slices are complete.
