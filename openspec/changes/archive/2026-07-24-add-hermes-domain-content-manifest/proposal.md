---
code_surface: openxFactory (contracts/hermes-domain-overlay/ content-manifest schema + fixtures, contracts/memory-gateway/ memory-binding schema + fixtures, validator extensions); consumers pin at realization (hermes-install seeding increment 4b)
target_release: contract-v1.18 (allocated and released at realization, 2026-07-24; annotated tag verified)
Status: ratified
Ratified by: user approval of `add-hermes-domain-content-manifest` on 2026-07-24
---

# Proposal: add-hermes-domain-content-manifest

## Why

Seeding increment 4a (hermes-install `add-domain-content-materialization`,
ratified + live-proven 2026-07-24) loads the domain's authored content set —
roles, policies, councils, escalation rules, mixes, memory boundaries, the
practice catalog — by CONVENTION: a hard-coded well-known-path list, the same
convention-then-contract path increment 1 took with role→path before the
overlay descriptor made it contract. The deferral was recorded in that
change's proposal. Separately, seeding increment 3
(`add-memory-gateway-binding`, ratified 2026-07-24) derives `memory_binding`
records — the rails input the future gateway consumes — as a runtime
convention (v1) whose neutral formalization was explicitly deferred to this
batch. Both conventions now have live-proven consumers and real instances to
validate against (the codexFactory archive at the live pin; the materialized
opensoft bindings), which is the house bar for turning convention into
contract. Decided 2026-07-24 (hermes-layer-seeding-mechanism.md §Decided):
4b is slim — this manifest contract, then hermes-install render provenance.

## What Changes

- **`contracts/hermes-domain-overlay/content-manifest.schema.yaml`** — the
  neutral schema for `kind: hermes_domain_content_manifest`: a domain repo
  MAY ship `hermes/domain/content-manifest.yaml` declaring its content set —
  per `content_kind`, a `path` (single document) or `directory` (per-file
  aggregate) within the archive, drawn from the ratified content-kind
  vocabulary (`role_authority`, `policy_position`, `escalation_rule`,
  `deliberation_mix`, `review_council`, `memory_boundary`,
  `practice_adoption`) plus the Omnigent overlay cross-check path. A missing
  manifest falls back to the documented convention the seeder ships today
  (the 4a set); a declared path missing from the archive fails closed; an
  undeclared kind never loads silently.
- **`contracts/memory-gateway/memory-binding.schema.yaml`** — the neutral
  schema for `kind: hermes_memory_binding` (formalizing increment 3's derived
  record): `layer_role`, `scopes[]` (per-scope `subject_scope`, optional
  promotion block whose `gateway` MUST be `customer_memory_gateway` and whose
  `accepted_authority_level` MUST be in the ratified `authority_levels`
  vocabulary, optional `write_authority` / bucket constraint fields),
  `denied_scopes[]`, `invariants[]`, optional `consent_profile`,
  `derived_from: memory_boundary`, and `vocabulary_bundle_tag` provenance.
- **Validator extensions** — `scripts/validate-hermes-domain-overlay.py`
  validates a content manifest when present (schema + declared-kind
  vocabulary); `scripts/validate-memory-gateway.py` covers the memory-binding
  schema; positive/negative fixtures under both contract dirs, with the live
  codexFactory content set and the live-derived opensoft bindings as the
  realization anchors.
- **Published as a versioned additive contract bundle** so hermes-install can
  pin both files and increment 4b replaces the runtime's convention list and
  binding-shape convention with contract validation.

## Capabilities

### Modified Capabilities

- `hermes-domain-overlay`: one ADDED requirement — the domain content set is
  declarable via a manifest, with the documented convention as fallback.
- `memory-gateway`: one ADDED requirement — derived memory bindings validate
  against the neutral schema.

## Impact

- **New code**: two schemas + fixtures + validator extensions; no runtime
  changes here (hermes-install adoption is increment 4b's second change).
- **Unblocks**: hermes-install 4b (manifest honored with convention fallback;
  memory_binding validated against the pinned contract instead of code
  convention); non-codex domains authoring content sets against a contract.
- **Provenance**: deferrals recorded in
  `add-domain-content-materialization` and `add-memory-gateway-binding`
  (hermes-install); design basis
  `ideation/brainstorm/hermes-layer-seeding-mechanism.md` (Decided
  2026-07-22 + 2026-07-24).
