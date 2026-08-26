# Tasks: Neutralize Job Envelope

## 1. Canonical Schemas (openxFactory)

- [x] 1.1 Loosen envelope: repository/feature_id optional, job_type free
      string, add the seven neutral references.
- [x] 1.2 Loosen run/event schemas the same way (feature_id optional,
      engineering enums relaxed to strings where present).
- [x] 1.3 CHANGELOG contract-v1.5 (additive/loosening).

## 2. Engineering Overlay (cross-repo: codexFactory)

- [x] 2.1 Add schemas/engineering-job-envelope.overlay.schema.yaml
      re-tightening job_type enum and repository/feature requirements.
- [x] 2.2 Declare `specializes` in codexFactory stack.yaml.

## 3. Neutrality Test

- [x] 3.1 Validate every example envelope/run/event document in
      openxFactory against the loosened schemas (must pass unchanged) and
      the engineering examples against the overlay (must pass strictly).

## 4. Register

- [x] 4.1 DTN-003 -> openspec at proposal, -> adopted after 2.x and 3.x;
      staged topic exit recorded.

## 5. Validation

- [x] 5.1 openspec strict passes for this change and --all.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `7a0d5da` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
