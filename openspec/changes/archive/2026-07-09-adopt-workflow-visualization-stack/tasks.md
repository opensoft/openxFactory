# Tasks: Adopt Workflow Visualization Stack

## 1. Standard Doc

- [x] 1.1 Write `docs/workflow-visualization-standard.md` (Status: ratified,
      citing this change): the stack table with roles, the MIT rule, the
      nine-view checklist, and the relation to the avatar-first UI standard.
- [x] 1.2 Link it from the README documentation index and from
      `docs/avatar-first-ui-standard.md` as the conventional-UI companion.

## 2. Staged Topic Closure

- [x] 2.1 Update `ideation/staging/workflow-visualization/validation-ui-tooling.md`
      to reference this change as its exit.

## 3. Validation

- [x] 3.1 `OPENSPEC_TELEMETRY=0 openspec validate adopt-workflow-visualization-stack --strict`
      and `--all --strict` pass.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `55c314a` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
