# Staged: OpenSpec Proposal Origin Contract

Status: staged
Kind: architecture
Repository context: openxFactory
Staging ID: openxFactory:staging:proposal-origin-contract
Source: Brett review of the archived
`add-proposal-supporting-doc-lifecycle` change, 2026-07-09.
Target capabilities: `document-lifecycle` (MODIFIED), `doc-health` (MODIFIED),
and `release-realization` (MODIFIED).
Regulatory rationale: [FDA SaMD Traceability Rationale](fda-samd-traceability-rationale.md).

## Problem

The proposal-supporting-document lifecycle records `origin_path` only after a
staged folder is moved. The OpenSpec proposal packet itself does not identify a
staging source and does not declare when a proposal was intentionally created
ad hoc. Consequently, a proposal can bypass brainstorm and staging without a
machine-checkable exception, as the bootstrap
`add-proposal-supporting-doc-lifecycle` change did.

## Proposed Contract

Every OpenSpec proposal MUST declare exactly one origin in `.openspec.yaml`.
The origin is part of the proposal packet and remains unchanged when the change
archives.

### Staged Origin

```yaml
origin:
  kind: staged
  id: openxFactory:staging:proposal-origin-contract
  path: ideation/staging/proposal-origin-contract
```

Rules:

1. `id` uses `<repo>:staging:<topic-slug>` and is durable after the folder
   moves or is compressed.
2. `path` names the original repository-relative staging folder.
3. The folder MUST contain a document whose `Staging ID:` equals `origin.id`.
4. At the proposal gate, selected material moves to the active change's
   `supporting-docs/` folder.
5. `supporting-docs/manifest.yaml` MUST repeat `origin.kind`, `origin.id`, and
   `origin.path`; the values must match `.openspec.yaml`.

### Ad-Hoc Origin

```yaml
origin:
  kind: ad_hoc
  id: openxFactory:adhoc:2026-07-09-001
  reason: Direct user-approved bootstrap correction
  approved_by: Brett
  approved_on: 2026-07-09
```

Rules:

1. `id` uses `<repo>:adhoc:<date>-<sequence-or-slug>` and is durable.
2. `reason`, `approved_by`, and `approved_on` are required.
3. Ad-hoc status is an explicit exception, not a substitute for staging when
   organized source material exists.
4. A proposal MUST NOT declare both staged and ad-hoc origin fields.
5. Supporting evidence MAY still live under `supporting-docs/`, but it MUST NOT
   claim a fabricated staging source.

## Proposal Gate

The gate rejects a proposal when:

- `origin` is missing
- `origin.kind` is not `staged` or `ad_hoc`
- a staged ID/path does not resolve before transition
- the staged document ID, proposal origin, and support manifest disagree
- an ad-hoc origin lacks reason or approval provenance
- both origin forms are declared

The transition tool should write the staged origin block automatically. Ad-hoc
origin creation should require explicit command arguments for reason and
approval rather than silently defaulting.

## Archive Gate

The archive gate verifies that `.openspec.yaml` still contains the original
origin declaration. For staged proposals, the compressed support manifest MUST
retain the same ID and path. For ad-hoc proposals, the archive MUST retain the
reason and approval provenance even when no support bundle exists.

## Doc-Health Enforcement

Doc-health should report:

- an active or archived proposal with no origin declaration
- an unknown or malformed origin kind or ID
- a staged origin without matching support provenance
- a mismatch among staging header, proposal packet, and manifest
- an ad-hoc origin without complete approval provenance
- mutation of an origin declaration after ratification

## Migration

1. Amend the archived `add-proposal-supporting-doc-lifecycle` packet with:

   ```yaml
   origin:
     kind: ad_hoc
     id: openxFactory:adhoc:2026-07-09-proposal-support-lifecycle-bootstrap
     reason: The origin contract did not exist when this bootstrap change was created
     approved_by: Brett
     approved_on: 2026-07-09
   ```

2. Backfill proposals with existing support manifests as `staged`, deriving the
   durable ID from the recorded repository and staging topic.
3. Classify proposals with no historical staging source as `ad_hoc`; do not
   fabricate staging folders or source history.
4. Keep migration provenance reviewable in a dedicated task or evidence file.

## Required Tests

- staged origin accepted and copied into the support manifest
- ad-hoc origin accepted with complete approval provenance
- missing origin rejected
- both origin kinds rejected
- staged ID/path/header mismatch rejected
- active-to-archive origin identity preserved
- archived bootstrap exception remains resolvable

## Exit

Create one OpenSpec change, recommended ID `add-proposal-origin-contract`, that
ratifies the proposal-origin fields, validator behavior, migration, and
doc-health checks. At that proposal gate this file MUST move into:

```text
openspec/changes/add-proposal-origin-contract/supporting-docs/origin-contract.md
```

The resulting `.openspec.yaml` MUST declare this topic's staged ID and path.
That self-application is the acceptance proof that the origin contract works.

This change establishes proposal provenance only. It MUST NOT claim FDA/SaMD
compliance. The linked regulatory rationale defines the additional trace graph,
profile, QMS, electronic-record, validation, and release controls required
before xFactory evidence can support such a claim.
