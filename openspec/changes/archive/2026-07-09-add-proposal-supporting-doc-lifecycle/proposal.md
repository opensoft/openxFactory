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
