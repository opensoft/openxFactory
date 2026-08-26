# Tasks: Promote Workflow Gate Contract

## 1. Canonical Artifacts

- [x] 1.1 Write `contracts/schemas/xfactory-workflow.schema.yaml` per the
      staged neutralization draft (envelope, workflow object, gate record
      with both blocking styles, owner-layer constraint).
- [x] 1.2 Write `scripts/validate-workflow-contracts.py <domain-repo>`
      validating `workflows/*.yaml` against the schema (errors/warnings per
      the capability).
- [x] 1.3 Record contract-v1.4 in `contracts/CHANGELOG.md`.
- [x] 1.4 Link the schema from the README Conformance section.

## 2. Neutrality Test

- [x] 2.1 Run the validator against all five domains; the four evidence
      workflows pass unchanged; capture the codexFactory envelope errors as
      expected adoption findings.

## 3. Register And Staging

- [x] 3.1 Move DTN-001 and DTN-002 to `openspec` status referencing this
      change; close the staged topic with its exit.

## 4. Adoption (cross-repo; gates register `adopted`, not archival)

- [x] 4.1 **CROSS-REPO (codexFactory)** Add `schema_version`/`kind`
      envelopes to its workflow YAMLs; validate clean.
- [x] 4.2 **CROSS-REPO (all five domains)** Declare `promoted_from`
      (candidate ids DTN-001, DTN-002) in each `stack.yaml`; re-validate;
      move register entries to `adopted`.

## 5. Validation

- [x] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate promote-workflow-gate-contract --strict`
      and `--all --strict` pass.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `a1a2802` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
