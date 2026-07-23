# Proposal (draft): add-governed-derived-model

Status: draft
Draft slice of: ../governed-derived-model.md
Target repo at promotion: openxFactory `openspec/changes/add-governed-derived-model/`
code_surface: openxFactory (contracts/schemas/ + docs/ + scripts/ validator)
target_release: next contract bundle (contract-v1.16 candidate)

## Why

Three domains independently converged on the same safety-critical object
shape — MedxFactory Dream Object / Simulation Scenario (ratified),
AdxFactory Persona / Campaign Simulation (staged), LedgerxFactory
Counterparty Health Profile / Financial Scenario (staged): a model
derived from evidence that must never be mistaken for truth or act on
the world. Each domain re-derives the invariants by hand; nothing checks
them. The intersection is five verified invariants (line-verified against
the Medx ratified templates 2026-07-23) plus a calibration loop two of
the three add. DTN-014.

## What Changes

- **`contracts/schemas/xfactory-derived-model-conformance.schema.yaml`**
  (ADDED) — the conformance declaration, kind
  `xfactory_derived_model_conformance`: one declaration per model
  family; members with `role: model | scenario` (scenario optional);
  `tier: governed | calibrated`; the six dials (identity
  synthetic|synthetic_aggregate|real_entity, scope domain|subject,
  truth_store ref, calibration source — required iff tier calibrated,
  promoting_authority human-role ref, person_modeling
  synthetic_only|aggregated_only|identified_organizations_only|
  identified_persons_under_policy with policy ref required for the
  last). Real-identity families declare the paired authoritative
  identity subject kind (two-object split).
- **`docs/governed-derived-model.md`** (ADDED) — invariant vocabulary
  and guidance: the five `governed` invariants, the `calibrated` tier
  additions (designated writer separation, derived-only confidence,
  miss-downgrade), promotion-by-new-object rule, `generation_seed`
  SHOULD, and the dial table with the three proof-domain instantiations.
- **`scripts/validate-derived-models.py`** (ADDED, never-copy
  consumption rule like the other canonical validators) — structural
  checks: single-value enum presence/immutability (`authority_status`,
  truth-store access, action-authority fields), provenance shape +
  assumption-register presence (or declared assumptions-forbidden),
  scope + person_modeling declarations (policy ref where required),
  hypothesis-only output enums on scenario members, calibrated-tier
  writer separation.
- **`openspec/specs/governed-derived-model/`** (ADDED capability) — see
  spec delta draft.
- **`docs/xfactory-domain-factory-model.md`** (MODIFIED, guidance) —
  short section pointing domain authors at the conformance declaration
  when they model synthetic cases, personas, or counterparty
  assessments.
- **`contracts/manifest.yaml`** — register the new schema
  (`adapter_owner: domain factory repos`).

## Impact

- New capability: `governed-derived-model`.
- No existing contract is modified structurally; guidance-only touch to
  the domain-factory model doc.
- Domain adoption is declaration + validation, no template rewrites:
  Medx conforms at `governed` declaration-only (verified); Adx and
  Ledgerx declare `calibrated` when their object-model changes land.
- Archive criterion (release-realization): merged + green validator
  runs for at least two domains at `governed` or above, one of them
  `calibrated`.
