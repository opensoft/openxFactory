## 1. Proposal And Approval

- [x] 1.1 Review `proposal.md`, `design.md`, and specs with Hermes governance.
- [x] 1.2 Record Hermes approval to proceed with decomposition.
- [x] 1.3 Confirm the first implementation feature is doc-only and `openxFactory` only.

## 2. FEAT-RB-001 Canonical Boundary Policy

- [x] 2.1 Verify `docs/repo-boundary-audit.md` states canonical ownership for `openxFactory`, `Hermes-Install`, and `Omnigent-Install`.
- [x] 2.2 Verify `docs/repo-boundary-pilot-plan.md` states the doc-only guardrails and stop conditions.
- [x] 2.3 Add or update README links so the boundary policy and pilot plan are discoverable.
- [x] 2.4 Run local doc and OpenSpec validation for the feature.
- [x] 2.5 Record branch review and PR admission evidence for the feature.

## 3. FEAT-RB-002 Contract Home Placeholder

- [x] 3.1 Create `contracts/README.md` in `openxFactory`.
- [x] 3.2 List planned shared contracts and schema names.
- [x] 3.3 Document contract source-of-truth, version pinning, adapter, and generated-copy rules.
- [x] 3.4 Validate that no install repo files are changed in this feature.

## 4. FEAT-RB-003 Omnigent-Install Scope Link

- [x] 4.1 Update `Omnigent-Install` README to state its install, worker runtime, operations, and DR scope.
- [x] 4.2 Link `Omnigent-Install` to canonical `openxFactory` boundary and workflow policy.
- [x] 4.3 Mark duplicate policy material as implementation notes or legacy copies where appropriate.
- [x] 4.4 Run existing `Omnigent-Install` smoke checks.

## 5. FEAT-RB-004 Hermes-Install Scope Link

- [x] 5.1 Update `Hermes-Install` README to state its Hermes install, operations, backup, restore, upgrade, and DR scope.
- [x] 5.2 Link `Hermes-Install` to canonical `openxFactory` boundary and workflow policy.
- [x] 5.3 Document the unresolved `Hermes-Install` remote ownership decision.
- [x] 5.4 Verify no deployment scripts or manifests change in this feature.

## 6. FEAT-RB-005 Submodule Decision Record

- [x] 6.1 Add an `openxFactory` decision record for install repo submodules.
- [x] 6.2 Document proposed paths `installs/hermes-install` and `installs/omnigent-install`.
- [x] 6.3 Document update, rollback, and pinned-commit procedure.
- [x] 6.4 Record that Hermes submodule creation waits for the remote ownership decision.

## 7. FEAT-RB-006 First Actual Submodule Add

- [x] 7.1 Confirm FEAT-RB-001 through FEAT-RB-005 are merged.
- [x] 7.2 Confirm install repo scope docs are updated and approved.
- [x] 7.3 Add only the approved first install repo submodule.
- [x] 7.4 Validate fresh clone and submodule initialization.
- [x] 7.5 Record merge council readiness evidence before merge.

## 8. Final Validation

- [x] 8.1 Validate the OpenSpec change with `openspec validate restructure-factory-repo-boundaries --strict`.
- [x] 8.2 Confirm no secrets, credential profiles, generated databases, or runtime state are tracked.
- [x] 8.3 Confirm each implemented feature has acceptance evidence.
- [x] 8.4 Archive the OpenSpec change only after all approved feature slices are complete.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 1 and 2, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `7c4dacb` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
