# Tasks: Refine Promotion Provenance

## 1. Process Doc

- [x] 1.1 Add the three rules (drafting ownership, provenance fields,
      mid-promotion authority) to
      `docs/domain-to-neutral-promotion-process.md` — a Domain Adoption
      subsection edit citing this change.

## 2. Contract Schema

- [x] 2.1 Add optional `promoted_from` and `specializes` fields to
      `contracts/schemas/xfactory-domain-stack.schema.yaml`.
- [x] 2.2 Record the addition in `contracts/CHANGELOG.md` per the contract
      versioning policy (backward-compatible optional fields).

## 3. Staged Topic Closure

- [x] 3.1 Update `ideation/staging/promotion-refinements/open-questions.md`:
      reference this change, note the standalone-vs-fold reversal, mark the
      topic's exit satisfied.

## 4. Validation

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate refine-promotion-provenance --strict`
      and `--all --strict` pass.
- [x] 4.2 `scripts/validate-domain-factory.py` still passes against a domain
      repo (schema fields optional, no breakage).

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting the two header lines plus a blank separator recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `55c314a` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
