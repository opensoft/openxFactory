# document-lifecycle Delta: The Canonical Supporting-Document Mover Comes Home

## ADDED Requirements

### Requirement: Canonical supporting-document mover
The canonical mover implementing the proposal-owned supporting-document and archive-retention requirements SHALL be owned by openxFactory as `scripts/proposal-support.py`.
It transitions selected staged material from `ideation/staging/<topic>/`
into an active change's `supporting-docs/` (status transitions, relative
link rewrites, a machine-readable manifest with per-file sha256 and source
snapshots), verifies the bundle, and packages the deterministic
`supporting-docs.tar.gz` + `supporting-docs.manifest.yaml` pair preserved
through OpenSpec archive. Doc-health family 5 (location conformance)
checks the artifacts it produces — with this adoption, producer and
checker live in the same repository.

#### Scenario: A staged doc cited by a proposal moves via the tool

- **WHEN** a staged topic's selected files transition into an active change through the tool
- **THEN** the files land under that change's `supporting-docs/` with statuses transitioned (`staged` becomes `draft` naming the change; `record` is retained), relative links rewritten to resolve from the new location, and a manifest recording origin path, source revision, transition date, selected files with hashes, and any material remaining staged
- **AND** the manifest verifies: each moved file's sha256 and source snapshot match, and a committed source revision's blob hashes reconcile

#### Scenario: Manifests survive archive

- **WHEN** a change with supporting documents reaches its archive gate
- **THEN** the tool packages the folder into a deterministic compressed bundle beside the archived change with a readable manifest carrying bundle and per-file hashes, and verification passes over the archived pair
- **AND** doc-health family 5 reports any checksum mismatch, incomplete archived support, or historical bundle misplaced under canonical `openspec/specs/`
