Status: ratified
Ratified: 2026-07-09 by Brett — record: the ratification commit `71c7028`, "Ratify proposal supporting-document lifecycle", whose body opens "Approved by Brett 2026-07-09"; the archive act followed the same day in `7b172d8`, "Archive proposal supporting-document lifecycle", which applied this change's four deltas into `openspec/specs/doc-health/spec.md`, `openspec/specs/document-lifecycle/spec.md`, `openspec/specs/lifecycle-notebook-projection/spec.md` and `openspec/specs/release-realization/spec.md`. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

Completed staged topics remain physically under `ideation/staging/` after an
OpenSpec proposal exists, so the staging tree no longer represents the actual
organized-work queue. OpenSpec preserves proposal, design, task, and spec-delta
artifacts, but it does not currently retain the staged source set as an owned,
verifiable proposal artifact.

## What Changes

- Make `openspec/changes/<change-id>/supporting-docs/` the proposal-stage home
  for organized source material selected from staging.
- Move selected staged files into the active change at the proposal gate,
  preserving history and leaving only unresolved material in staging.
- Require a machine-readable supporting-document manifest with source paths,
  source revision, file hashes, and NotebookLM workspace provenance when used.
- Extend hybrid NotebookLM source returns to active proposal supporting
  documents, with `draft` or `record` lifecycle status as appropriate.
- Add deterministic transition and archive-packaging tooling in codexFactory.
- Package supporting documents before archival as a deterministic compressed
  bundle beside the archived proposal, retaining a readable manifest and
  keeping canonical `openspec/specs/` free of historical binary bundles.
- Add doc-health checks for stale staged topics, incomplete proposal manifests,
  invalid supporting-document statuses, broken archive bundles, and misplaced
  bundles.
- Migrate completed staging topics into their corresponding active or archived
  OpenSpec records.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `document-lifecycle`: define proposal-owned supporting documents and the
  staged-to-proposed move/removal rules.
- `lifecycle-notebook-projection`: allow proposal supporting-document folders
  as hybrid origins and define proposal-stage imported-source provenance.
- `doc-health`: enforce proposal-supporting-document and archive-bundle
  lifecycle integrity.
- `release-realization`: require final source capture and deterministic
  supporting-document packaging before an OpenSpec change archives.

## Impact

- openxFactory: lifecycle, NotebookLM, doc-health, and release-realization spec
  deltas; workflow documentation; migration of completed staging topics.
- codexFactory: proposal transition command, archive wrapper, manifest and
  bundle verification, NotebookLM importer extension, doc-health checks, and
  tests.
- xFactory: validation of the updated codexFactory tooling through the pinned
  repository; no runtime service change.
- Existing active and archived changes: supporting material can be migrated
  without changing their canonical spec outcomes.

code_surface: codexFactory
target_release: implemented
