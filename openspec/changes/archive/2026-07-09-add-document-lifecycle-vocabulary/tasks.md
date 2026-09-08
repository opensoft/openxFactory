# Tasks: Add Document Lifecycle Vocabulary

## 1. Vocabulary Artifact

- [x] 1.1 Write `docs/document-lifecycle.md` stating the lifecycle spine, the
      `Status:`/`Kind:` taxonomy, and the transition gates, referencing this
      change's design mapping table.
- [x] 1.2 Link the new doc from the README documentation index.

## 2. Ratify Existing Process Docs

- [x] 2.1 Move `docs/domain-to-neutral-promotion-process.md` from draft to
      `ratified` status, citing this change.
- [x] 2.2 Move `docs/domain-neutralization-candidate-register.md` to
      `staged` + `Kind: register` and define its alias statuses in terms of
      the lifecycle spine.
- [x] 2.3 Remove the draft caveat from `ideation/README.md` and update both
      ideation brainstorm docs' statuses to taxonomy values.

## 3. Status Header Sweep (openxFactory)

- [x] 3.1 Migrate every `Status:` header in `openxFactory/docs/` to the
      controlled taxonomy per the design mapping table, adding `Kind:` where
      useful.
- [x] 3.2 Demote each "shared xFactory standard" claim to `draft` unless a
      promoted spec backs it; list the demotions in the commit message.
- [x] 3.3 Mark generated reports and simulations as `record`.

## 4. Status Header Sweep (DomainxFactories)

- [x] 4.1 Sweep `xFactories/codexFactory` docs to the taxonomy.
- [x] 4.2 Sweep `xFactories/MedxFactory` docs to the taxonomy.
- [x] 4.3 Sweep `xFactories/OpsxFactory`, `xFactories/LedgerxFactory`, and
      `xFactories/AdxFactory` docs to the taxonomy.
- [x] 4.4 Seed an `ideation/` area (README only) in each DomainxFactory.

## 5. Validation

- [x] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` passes.
- [x] 5.2 Grep-verify no doc outside promoted-spec backing claims `standard`
      status and no free-form status values remain in swept repos.
- [x] 5.3 Record the status-checking rules as requirements input for the
      doc-health pipeline implementation proposal (codexFactory).

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `a195244` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
