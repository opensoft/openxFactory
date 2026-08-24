# Promote Credential Contracts

Status: ratified
Ratified: 2026-07-09 — record: the archive act, commit `7a0d5da` "Archive three DTN changes; remove accidentally swept proposal copy", which applied this change's spec delta into `openspec/specs/credential-contracts/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. The commit body records the promotion in words: "Promote neutral-job-envelope, roles-authority-model, and credential-contracts to canonical specs (capabilities 12-14)". Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

The credential access model is neutral doctrine, but its concrete record
shapes — broker contract, runtime capability grant, binding, requirements,
audit policy — exist only as OpsxFactory files, despite carrying neutral
`xfactory_*` kind names since scaffolding (DTN-004, P1). Every future
domain that touches credentials (Ledgerx tax portals, Medx EHR access)
would re-invent the shapes; the review's B-series flagged credential
machinery as the fleet's highest risk-to-implementation gap.

## What Changes

- Add `contracts/schemas/xfactory-credential-contracts.schema.yaml`: the
  five record kinds, discriminated by `kind`, shape-only.
- Add `scripts/validate-credential-contracts.py` (errors for structure and
  missing envelopes, out-of-scope kinds skipped with notice).
- OpsxFactory declares `promoted_from` (DTN-004); its policy kinds remain
  out of scope as a future candidate.

## Capabilities

### New Capabilities

- `credential-contracts`: canonical credential record shapes, domain
  content locality, and validation rules.

### Modified Capabilities

- None. (credential-access-model doctrine is referenced, not altered.)

## Impact

- openxFactory: schema + validator + CHANGELOG v1.6 + README conformance
  entry + register updates.
- OpsxFactory: provenance declaration only — zero content changes
  (neutrality test passed as-is).
- Doc+schema change; archives on landing.
