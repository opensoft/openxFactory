## 1. Hard Spec Reconciliation

- [x] 1.1 Update canonical `canonical-policy-migration` requirements so `openxFactory` owns neutral stage/admission policy and `codexFactory` owns software Spec Kit and PR admission implementation.
- [x] 1.2 Update canonical `repo-boundary-governance` requirements so domain execution policy belongs in the owning DomainxFactory.
- [x] 1.3 Update canonical `shared-contract-ownership` requirements so shared contracts remain in `openxFactory` while domain-specific artifact schemas may live in DomainxFactories.

## 2. openxFactory Documentation Split

- [x] 2.1 Narrow `docs/roles-and-authority.md` so it contains cross-factory authority and points to DomainxFactory implementation policy instead of embedding Spec Kit mechanics.
- [x] 2.2 Narrow `docs/traceability-model.md` to a domain-neutral traceability chain and point engineering traceability to `codexFactory`.
- [x] 2.3 Verify `docs/spec-kit-stage-ownership.md`, `docs/pr-admission.md`, and `docs/workflow-contract.md` use neutral wording and point to domain implementations.

## 3. codexFactory Implementation Contracts

- [x] 3.1 Add machine-readable workflow YAML gate contracts for each existing `codexFactory/workflows/*.md` workflow.
- [x] 3.2 Add a `codexFactory` tenant example that references the software-team profile.
- [x] 3.3 Add a scaffolded `memory_gateway` block to `codexFactory/stack.yaml` that satisfies strict validation without selecting a production provider.

## 4. Memory Gateway Promotion

- [x] 4.1 Promote the completed memory-gateway requirements into canonical `openspec/specs/memory-gateway/spec.md`.
- [x] 4.2 Archive `openspec/changes/add-customer-memory-gateway-architecture` to the dated archive directory.
- [x] 4.3 Update `openxFactory/README.md` OpenSpec active, archived, and canonical spec lists.

## 5. Validation

- [x] 5.1 Run OpenSpec validation for all specs and active changes.
- [x] 5.2 Run openxFactory memory gateway validation.
- [x] 5.3 Run strict `codexFactory` domain validation and pin validation.
- [x] 5.4 Run `codexFactory` docs validation.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 1 and 2, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the promoting act, because no explicit ratification act appears anywhere on the record: commit `d5ada44` (2026-07-08) applied this change's spec delta into the canonical specs one day before the archive commit `a195244` (2026-07-09) moved the folder, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

**One reading a later reader should not have to re-derive.** The promotion and the archive are ONE DAY APART on this record: `d5ada44` (2026-07-08) proposed this change and applied its three deltas in the same commit, and `a195244` (2026-07-09) moved the folder, its body saying so — "reconcile deltas were already synced". The by-construction reasoning is unaffected; the date recorded is the archive act's.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
