## 1. Proposal And Provenance

- [x] 1.1 Record explicit ad hoc proposal provenance and validate supporting-document hashes.
- [x] 1.2 Run strict OpenSpec validation before repository creation.

## 2. Private Repository Bootstrap

- [x] 2.1 Create `opensoft/xFactory-Installer` with private GitHub visibility and verify the remote owner and default branch.
- [x] 2.2 Add truthful repository, architecture, security, compatibility, release, ownership, and validation surfaces without placeholder application claims.
- [x] 2.3 Run repository validation and prohibited credential/package scanning against the bootstrap tree.

## 3. Initial Release

- [x] 3.1 Commit the validated repository bootstrap on `main` and push it to the private remote.
- [x] 3.2 Tag and push immutable bootstrap release `v0.1.0-bootstrap` and verify that the tag resolves to the validated commit.

## 4. Aggregation Integration

- [x] 4.1 Add the SSH submodule at `installs/xfactory-installer` and update the xFactory topology and current-submodule documentation.
- [x] 4.2 Verify private visibility, remote URL, exact gitlink, compatibility declaration, repository validation, and recursive checkout behavior.
- [x] 4.3 Commit and push only the installer proposal, new installer pin, and parent integration paths without including unrelated dirty work.

## 5. Completion

- [x] 5.1 Run repository validation, strict OpenSpec validation, parent diff checks, and final status verification.
- [x] 5.2 Record that WinUI implementation, Intune enrollment, Graph grants, signing, and Store submission remain successor work rather than bootstrap realization claims.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting exactly those two lines recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `219bf93` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
