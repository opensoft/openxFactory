# Tasks: Exclude Worktrees From Notebook Projection

## 1. Contract (openxFactory)

- [x] 1.1 Add the corpus scan scope requirement to `lifecycle-notebook-projection` and pass strict OpenSpec validation.
- [x] 1.2 Update the `docs/lifecycle-notebook-projection.md` scope line to match the promoted wording.

## 2. Implementation (codexFactory)

- [x] 2.1 Filter `*-worktrees` containers out of the repository base list and prune documents below a nested `.git` entry in `scan()`.
- [x] 2.2 Add regression tests (worktree container excluded, nested clone excluded, governed doc still projects, no `-worktrees` repo title) and run the notebooklm test suite green.

## 3. Reconciliation And Evidence

- [x] 3.1 Verify the workspace dry-run reports zero worktree-derived operations (backlog dropped 230 -> 194 legitimate operations).
- [x] 3.2 Apply the accumulated reconciliation backlog and confirm a clean follow-up dry-run (194 + 1 rolling-drift operations applied 2026-07-12, zero errors, follow-up dry-run reports zero pending; canon 34 / drafts 114 / ideation 32 desired sources).
- [x] 3.3 Sync the aggregation repo's codexFactory and openxFactory submodule pointers (xFactory 2bc34dd).

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting exactly those two lines recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (a), an explicit ratification act named on the record: the archive commit `1efa575`, whose body opens "Brett ratified all three active changes 2026-07-12" and names this change first. The three-way floor is cleared on the APPROVER axis and the DATE axis, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
