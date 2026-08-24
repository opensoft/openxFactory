# Tasks: Concretize Prose Tagging Syntax

## 1. Canonical Document

- [x] 1.1 Update the "The Explicit Delta Rule" section of
      `docs/document-lifecycle.md` with the concrete `xspec:` marker
      grammar (candidate fences and supersedes marker), the block-level-only
      candidacy rule, and the structural rules (no nesting, no
      heading-spanning), citing this change.

## 2. Ideation Pointers (staged -> proposed gate)

- [x] 2.1 Update `ideation/staging/prose-tagging/tag-syntax.md`: reference
      this change as its proposal, and record the resolved open questions
      (HTML comments; no nesting or heading-spanning) pointing at this
      change's `design.md`.
- [x] 2.2 Update the prose-tagging pointer line in
      `ideation/brainstorm/doc-health-pipeline.md` to reference this change,
      and note that the doc-level `Status: spec-candidate` idea was dropped
      at the proposal gate.

## 3. Doc-Health Handoff

- [x] 3.1 Add `ideation/staging/doc-health-checks/tag-hygiene-rules.md`
      (companion to `status-check-rules.md`): the grep contract
      (`grep -rn 'xspec:' --include='*.md'`), the canonical grammar, and
      the hygiene checks the deterministic pass MUST implement
      (well-formedness, target resolution, fence structure, `change=`
      aging), sourced from this change.

## 4. Validation

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate
      concretize-prose-tagging-syntax --strict` and
      `openspec validate --all --strict` pass from the openxFactory root.
- [x] 4.2 Grep-verify: every `xspec:` occurrence in the repo parses against
      the canonical grammar, and no `Status:` header anywhere uses
      `spec-candidate`.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `a195244` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
