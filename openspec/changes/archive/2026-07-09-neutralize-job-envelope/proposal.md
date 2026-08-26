# Neutralize Job Envelope

Status: ratified
Ratified: 2026-07-09 — record: the archive act, commit `7a0d5da` "Archive three DTN changes; remove accidentally swept proposal copy", which applied this change's spec delta into `openspec/specs/neutral-job-envelope/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. The commit body records the promotion in words: "Promote neutral-job-envelope, roles-authority-model, and credential-contracts to canonical specs (capabilities 12-14)". Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

The canonical hermes-job schemas are engineering-shaped: the envelope
requires `repository` and `feature_id` and enumerates only engineering
`job_type` values, so no other domain can express a governed job without
fake fields (DTN-003, P0). Medx and Ops evidence shows the need for
subject, client, workflow, focal-item, gate, and artifact references.

## What Changes

- Loosen the neutral core (additive, contract-v1.5): `repository` and
  `feature_id` optional; `job_type` a free string owned by domain
  vocabularies; new optional neutral references (`domain`, `subject_ref`,
  `client_ref`, `workflow_ref`, `focal_item_ref`, `gate_ref`,
  `artifact_refs`).
- codexFactory keeps its rigor via an engineering overlay schema that
  re-tightens exactly what the core relaxed, and declares `specializes`
  provenance — the field's first use.
- Copy-consumers (omnigent-install) remain valid against their pinned ref;
  they adopt at their next deliberate re-pin.

## Capabilities

### New Capabilities

- `neutral-job-envelope`: neutral core rules, domain overlay pattern, and
  compatibility guarantees for job envelope/run/event schemas.

### Modified Capabilities

- None.

## Impact

- openxFactory: three schema edits (loosening only), CHANGELOG v1.5,
  register update, staged topic closure. All existing examples must
  validate unchanged (neutrality test).
- codexFactory: new overlay schema + `specializes` declaration.
- No runtime or credential impact; doc+schema change, archives on landing.
