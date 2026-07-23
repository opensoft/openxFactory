---
code_surface: openxFactory (contracts/hermes-domain-overlay/ schemas + fixtures, scripts/validate-hermes-domain-overlay.py); consumers pin at realization (hermes-install seeding, DomainxFactory validate chains)
target_release: contract-v1.15 (allocated and released at realization, 2026-07-23; annotated tag verified)
Status: ratified
Ratified by: user approval of `add-hermes-domain-overlay-contract` on 2026-07-23
---

# Proposal: add-hermes-domain-overlay-contract

## Why

The hermes-install seeding runtime (capability `layer-content-seeding`,
realized 2026-07-22) loads a domain's `hermes/domain/overlay.yaml` with only
a **minimal structural check**, because no neutral `hermes_domain_overlay`
schema exists in openxFactory contracts — a gap flagged in the change's own
design and carried as an open item ever since. Two conventions currently hold
the load path together by agreement rather than contract: the overlay's
*shape* (what a valid domain overlay contains) and the **role→path rule**
(domain role → `hermes/domain/overlay.yaml`), which the seeder hard-codes.
codexFactory now ships a real, full overlay instance (37 staked authorities,
landed by `add-domain-hermes-roles-and-policies`) to validate the schema
against, and seeding increment 2 (materialization) should not be proposed
against an informal shape. This change makes both conventions contract.

## What Changes

- **`contracts/hermes-domain-overlay/hermes-domain-overlay.schema.yaml`** —
  the neutral schema for `kind: hermes_domain_overlay`: `schema_version`,
  domain identity (`id`, `display_name`), `approval_scope_kinds` (non-empty),
  `required_approval_fields` (non-empty), and `authority_boundaries` with a
  domain-owned list (`<domain>_owns`), `xfactory_owns`, and
  `repository_owns` — each non-empty, no overlaps between the three. Additive
  and domain-neutral: every DomainxFactory validates the same way.
- **`contracts/hermes-domain-overlay/overlay-descriptor.schema.yaml`** — the
  machine-readable role→path declaration (`kind:
  hermes_overlay_descriptor`): a domain repo MAY ship
  `hermes/overlay-descriptor.yaml` declaring, per layer role, the overlay
  document path within the repo (e.g. `domain: hermes/domain/overlay.yaml`).
  A missing descriptor falls back to the documented convention the seeder
  ships today; a declared role the seeder doesn't recognize fails closed.
  The role→path rule stops being convention the moment a descriptor exists.
- **`scripts/validate-hermes-domain-overlay.py`** — the canonical validator
  (schema check + no-overlap rule + descriptor cross-check that every
  declared path exists), consumed by domain validate chains the same way as
  the other canonical validators; positive/negative fixtures under the
  contract dir, with codexFactory's live overlay as the realization proof.
- **Published as a versioned additive contract bundle** (per
  `docs/contract-versioning-policy.md`) so hermes-install can pin it and
  seeding increment 2 replaces the runtime's minimal structural check with
  schema validation against the pinned contract.

## Capabilities

### New Capabilities

- `hermes-domain-overlay`: the neutral contract for a domain's seedable
  Hermes overlay — schema, role→path descriptor, canonical validator, and
  versioned publication.

## Impact

- **New code**: one validator script + two schemas + fixtures; no runtime
  changes here (hermes-install adoption is seeding increment 2's job).
- **Unblocks**: seeding increment 2 (validates against the pinned contract);
  every non-codex domain (Medx/Ledgerx/Opsx/Adx author overlays against a
  contract, not a convention).
- **Provenance**: staged topic
  `openxFactory:staging:layer-content-materialization` (first of its two
  exits); design basis `ideation/brainstorm/hermes-layer-seeding-mechanism.md`
  (Decided 2026-07-22).
