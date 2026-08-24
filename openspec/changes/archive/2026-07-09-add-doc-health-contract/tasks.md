# Tasks: Add Doc-Health Contract

## 1. Contract Document

- [x] 1.1 Write `docs/doc-health.md` (`Status: ratified`, `Ratified by:`
      this change): the twelve check families, the report contract and
      ranked-plan item shape, severity levels and the regression rule,
      aging threshold defaults, and the ownership/hosting split —
      referencing `docs/document-lifecycle.md` for the `xspec:` marker
      grammar (never restating it).
- [x] 1.2 Link `docs/doc-health.md` from the README documentation index.

## 2. Ideation Pointers (staged -> proposed gate)

- [x] 2.1 Update `ideation/staging/doc-health-checks/nightly-run-shape.md`:
      reference this change as the first of its two declared exit changes;
      record the resolved open questions (aging thresholds, report format)
      pointing at this change's `design.md`.
- [x] 2.2 Update `ideation/staging/doc-health-checks/status-check-rules.md`:
      reference this change as the contract now carrying its checks.
- [x] 2.3 Update `ideation/staging/doc-health-checks/tag-hygiene-rules.md`:
      reference this change as the contract now carrying its checks (the
      grammar itself stays owned by `document-lifecycle`).

## 3. Implementation Handoff

- [x] 3.1 Write `ideation/staging/doc-health-checks/implementation-handoff.md`
      (staged fragment targeting the follow-on codexFactory change): what
      the implementation MUST include — checker scripts per family, report
      generator emitting the contract schema, reusable workflow in
      codexFactory plus the thin nightly caller and `health/reports/` home
      in the aggregation repo, issue automation for the regression rule,
      notebook dry-run integration (auth strategy open), and the archive-
      discipline decision that change must make as the release-flow pilot.

## 4. Validation

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate add-doc-health-contract
      --strict` and `openspec validate --all --strict` pass from the
      openxFactory root.
- [x] 4.2 Grep-verify the `xspec:` grammar is stated only by
      `docs/document-lifecycle.md` and the prose-tagging change artifacts —
      `docs/doc-health.md` references, never restates, it.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `a195244` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
