# Tasks: Promote Credential Contracts

- [x] 1.1 Add contracts/schemas/xfactory-credential-contracts.schema.yaml.
- [x] 1.2 Add scripts/validate-credential-contracts.py.
- [x] 1.3 CHANGELOG contract-v1.6; README Conformance entry; reference from
      docs/credential-access-model.md.
- [x] 2.1 Neutrality test: all OpsxFactory credential contracts validate
      unchanged; other domains trivially pass.
- [x] 3.1 CROSS-REPO (OpsxFactory): declare promoted_from (DTN-004).
- [x] 4.1 Register DTN-004 -> adopted; staged topic exit recorded.
- [x] 5.1 openspec strict passes (this change and --all).

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `7a0d5da` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
