# Tasks: Add Lifecycle Notebook Projection

## 1. Workflow Documentation

- [x] 1.1 Write `docs/lifecycle-notebook-projection.md` — the full NotebookLM
      workflow: the three books, projection table, exclusions, grounding set,
      title prefixes, charter text, chat framing, sync cadence and manifest,
      stage-transition behavior, and operator runbook (auth, dry-run, apply,
      artifact generation). Status: ratified, citing this change.
- [x] 1.2 Link the doc from the README documentation index.
- [x] 1.3 Add a relation note in `docs/notebooklm-source-workspaces.md`
      pointing to the projection doc for lifecycle-derived workspaces.

## 2. Regularize The Pilot Implementation

- [x] 2.1 Update `codexFactory/scripts/sync-notebooklm-books.py` docstring to
      cite this capability as the contract it conforms to, and align any
      drifted constants (books, prefixes, charter, chat prompt) with the doc.
- [x] 2.2 Commit the script in codexFactory (it currently exists uncommitted)
      and sync the aggregation pin.
- [x] 2.3 Register the three notebooks as `external_source_workspace` records
      (source-workspaces model §6) under `openxFactory/examples/` or a
      workspace registry location chosen in 1.1.

## 3. Validation

- [x] 3.1 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` passes.
- [x] 3.2 Run the sync dry-run twice after a no-op: second run reports zero
      adds/deletes (idempotence proof).
- [x] 3.3 Move one doc between states, run sync, verify the source moved
      books, then restore (stage-transition proof).

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `a195244` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
