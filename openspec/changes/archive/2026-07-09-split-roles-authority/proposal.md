# Split Roles And Authority

Status: ratified
Ratified: 2026-07-09 — record: the archive act, commit `7a0d5da` "Archive three DTN changes; remove accidentally swept proposal copy", which applied this change's spec delta into `openspec/specs/roles-authority-model/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. The commit body records the promotion in words: "Promote neutral-job-envelope, roles-authority-model, and credential-contracts to canonical specs (capabilities 12-14)". Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

`docs/roles-and-authority.md` claims to be canonical cross-factory
authority but is written for "the AI software development factory": it
embeds the engineering execution lead roles, an escalation table keyed to
them, and engineering Hermes group YAML (DTN-013, P0). Non-engineering
domains inherit prose that does not describe them, and the neutral repo
owns execution mechanics the reconcile change assigned to domains.

## What Changes

- Neutralize `docs/roles-and-authority.md`: keep authority layers, Hermes
  governance roles, escalation principles, ownership boundaries, and
  enforcement concepts; require each DomainxFactory to instantiate its
  execution lead roles; fix stale personal-path provenance.
- Move the engineering instantiation (execution lead table, role-keyed
  escalation routes, profiles/groups YAML, engineering rule-of-thumb) to
  `codexFactory/docs/engineering-roles-and-authority.md`.
- codexFactory declares `specializes` provenance for the roles model.

## Capabilities

### New Capabilities

- `roles-authority-model`: neutral ownership of cross-factory roles and
  escalation; domain instantiation of execution roles.

### Modified Capabilities

- None.

## Impact

- openxFactory: roles doc neutralized (loses ~40% of its lines to
  codexFactory); register and staging updates.
- codexFactory: new engineering roles doc + specializes entry.
- Doc-only; archives on landing.
