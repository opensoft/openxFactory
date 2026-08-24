# Tasks: add-sops-ciphertext-ruling

Doc-only change (`code_surface: none`): archives when its artifacts land on
main. The QA runtime realization is tracked by omnigent-install's
`add-qa-subscription-environment` Amendment 3, not here.

## 1. Ruling record

- [x] 1.1 Ruling prose in `docs/credential-access-model.md` §1.1 (authored
      on this branch, PR #34; ratified by Brett Heap 2026-07-19).
- [x] 1.2 §1.1 cites this change as its ratification record.
- [x] 1.3 `credential-contracts` delta with the pattern requirement and its
      rejection/rotation scenarios; `--strict` validated.
- [x] 1.4 README OpenSpec Records entry.
- [x] 1.5 Archive on landing (PR #34 merge), promoting the delta into
      `openspec/specs/credential-contracts/`.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting exactly those two lines recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (a), an explicit ratification act named on the record: this change's own tasks.md 1.1, "ratified by Brett Heap 2026-07-19". The three-way floor is cleared on the APPROVER axis, the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
