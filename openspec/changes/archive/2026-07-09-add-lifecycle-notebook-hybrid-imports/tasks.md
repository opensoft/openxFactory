# Tasks: Add Lifecycle Notebook Hybrid Imports

## 1. Contract Documentation

- [x] 1.1 Update `docs/lifecycle-notebook-projection.md` to define hybrid
      analysis notebooks: one Canon release line plus one brainstorm or
      staged origin folder.
- [x] 1.2 Add the source-return workflow: any non-seed NotebookLM source in a
      hybrid returns to the origin folder; scratch notes remain in
      NotebookLM until converted to sources.
- [x] 1.3 Document seed-source exclusions and imported entry provenance:
      source workspace, source id, source title, L1 authority, and origin
      lifecycle status.
- [x] 1.4 Link or promote the staged
      `ideation/staging/lifecycle-notebook-hybrids/` process as the source
      of this ratified workflow.

## 2. codexFactory Implementation

- [x] 2.1 Extend `scripts/sync-notebooklm-books.py` with a dry-run-by-default
      import mode that accepts a hybrid notebook id/alias and an origin
      `--target-path`.
- [x] 2.2 Ensure the importer skips managed seed sources:
      `00 [charter]`, `00 [hybrid charter]`, `[brainstorm]`, `[staged]`,
      `[draft]`, `[ratified]`, `[standard]`, `[spec]`, and `[grounding]`.
- [x] 2.3 Ensure the importer writes imported material under the supplied
      brainstorm/staged origin folder with `Status`, `Kind`, workspace,
      source id, source title, and `Authority: L1 notebook synthesis`.
- [x] 2.4 Ensure imports are idempotent by NotebookLM source id.
- [x] 2.5 Keep any explicit `[export:*]` title path as compatibility only;
      the primary path imports all non-seed sources from the origin-scoped
      hybrid.

## 3. Tests And Validation

- [x] 3.1 Add unit tests for untagged converted-note sources importing to a
      brainstorm origin.
- [x] 3.2 Add unit tests for added non-note sources, such as web/research
      sources, importing to a staged origin.
- [x] 3.3 Add tests proving seed sources are skipped and already imported
      source ids are not duplicated.
- [x] 3.4 Include NotebookLM importer tests in codexFactory repo validation.
- [x] 3.5 Run local implementation tests before repo validation.
- [x] 3.6 Run codexFactory repo validation before OpenSpec validation.
- [x] 3.7 Run `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` from
      the openxFactory root.

## 4. Live Acceptance Evidence

- [x] 4.1 Use a live hybrid/test notebook to convert a NotebookLM note into a
      source, pull it back to the origin brainstorm folder, and record the
      source id/title in the imported file.
- [x] 4.2 Add or discover a non-note source in a hybrid notebook and verify
      the importer writes it to the same origin folder.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (a), an explicit ratification act named on the record: the ratify gate recorded on the archive commit `e55724c`, whose body opens "Ratify gate approved". No ratifier is named in prose anywhere on this record, so the date only is recorded and no approver is claimed. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
