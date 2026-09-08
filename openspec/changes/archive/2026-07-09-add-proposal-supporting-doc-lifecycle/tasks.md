## 1. Lifecycle Contract And Documentation

- [x] 1.1 Update `docs/document-lifecycle.md` and `ideation/README.md` with the
      proposal-owned supporting-document transition and partial-promotion rule.
- [x] 1.2 Update `docs/lifecycle-notebook-projection.md` with proposal-stage
      hybrid origins, final source return, and retirement behavior.
- [x] 1.3 Update release-realization and doc-health documentation with archive
      packaging and integrity checks.
- [x] 1.4 Add this change to the openxFactory OpenSpec records index.

## 2. Proposal Transition Tooling

- [x] 2.1 Add a dry-run-by-default codexFactory command that moves selected
      staged files into an active change's `supporting-docs/` folder.
- [x] 2.2 Generate and validate `supporting-docs/manifest.yaml`, update lifecycle
      headers, and preserve partial-promotion remainder paths.
- [x] 2.3 Detect unsafe paths, symlinks, target collisions, and broken relative
      Markdown links before applying a transition.
- [x] 2.4 Add unit tests for complete, partial, dry-run, and rejected transitions.

## 3. Archive Packaging Tooling

- [x] 3.1 Add deterministic tar-gzip packaging with normalized metadata and a
      readable archive manifest containing bundle and per-file hashes.
- [x] 3.2 Add archive preflight checks and a wrapper that packages support before
      invoking the normal `openspec archive` command.
- [x] 3.3 Add verification mode for active manifests and archived bundles.
- [x] 3.4 Add unit and integration tests for reproducibility, checksum failures,
      path safety, and OpenSpec archive preservation.

## 4. NotebookLM Proposal Origins

- [x] 4.1 Extend the NotebookLM importer to accept active
      `openspec/changes/<change-id>/supporting-docs/` targets with `draft`
      imported status.
- [x] 4.2 Preserve source-id idempotence and proposal-origin provenance.
- [x] 4.3 Add tests for proposal imports, invalid archived targets, and existing
      brainstorm/staging behavior.

## 5. Doc-Health Enforcement

- [x] 5.1 Add deterministic checks for stale proposed material in staging,
      missing/invalid active manifests, and staged status under proposal support.
- [x] 5.2 Add archive checksum and misplaced canonical-bundle checks.
- [x] 5.3 Add focused doc-health tests for every new finding and clean cases.

## 6. Migration And Pilot

- [x] 6.1 Move the active semantic-sweep staged source into its proposal
      supporting-documents folder and create its manifest without changing its
      capability scope.
- [x] 6.2 Map completed staged files to their archived changes, package them,
      retain readable manifests, and remove completed staging folders.
- [x] 6.3 Update links and the ideation inventory; preserve any unresolved staged
      material explicitly.

## 7. Validation

- [x] 7.1 Run local transition, archive, NotebookLM, and doc-health tests.
- [x] 7.2 Run codexFactory repository validation.
- [x] 7.3 Run strict validation for this change and all OpenSpec changes/specs.
- [x] 7.4 Verify `ideation/staging/` contains only genuine unproposed material and
      every migrated archive bundle verifies.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 1 and 2, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (a), an explicit ratification act named on the record: the ratification commit `71c7028`, "Ratify proposal supporting-document lifecycle", whose body opens "Approved by Brett 2026-07-09" — a separate commit from the archive act `7b172d8` of the same day, which is cited as corroboration. The three-way floor is cleared on the APPROVER axis, the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
