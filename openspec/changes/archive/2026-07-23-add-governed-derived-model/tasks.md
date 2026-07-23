# Tasks: add-governed-derived-model

## 1. Contract surface

- [x] 1.1 Author `contracts/schemas/xfactory-derived-model-conformance.schema.yaml`
      (kind `xfactory_derived_model_conformance`; family members with
      roles, tier, six dials; real-identity paired-subject declaration).
- [ ] 1.2 Register the schema in `contracts/manifest.yaml`
      (`adapter_owner: domain factory repos`, consumption rule pin-only)
      — at the contract-v1.16 bundle cut, per design.md (omnigent
      precedent: manifest entries land with their bundle release).
- [x] 1.3 Author `docs/governed-derived-model.md` (invariant vocabulary,
      tier definitions, promotion-by-new-object rule, `generation_seed`
      SHOULD, dial table with the three proof instantiations); link into
      the README doc index.

## 2. Validator

- [x] 2.1 Implement `scripts/validate-derived-models.py` (structural
      checks per spec: single-value enums + immutability, provenance
      forms, scope + person_modeling declarations, scenario output
      enums, calibrated writer separation).
- [x] 2.2 Positive fixtures: one per proof domain shape (Medx governed
      assumptions-forbidden; Adx calibrated synthetic-aggregate;
      Ledgerx calibrated real-entity two-object split).
- [x] 2.3 Negative fixtures: mutable authority_status; missing
      assumption register on assumption-permitting form; action value in
      a scenario output enum; calibrated family whose scenario writes
      its own calibration; identified_persons_under_policy without a
      policy ref.

## 3. Spec and guidance

- [x] 3.1 Land the `governed-derived-model` capability spec (spec.md
      draft in this folder). Promoted to
      `openspec/specs/governed-derived-model/` at archive (ratified
      2026-07-23).
- [x] 3.2 MODIFIED guidance section in `docs/xfactory-domain-factory-model.md`.
- [x] 3.3 `OPENSPEC_TELEMETRY=0 openspec validate add-governed-derived-model --strict`
      and `--all --strict` green.

## 4. Realization evidence (archive gate)

- [x] 4.1 MedxFactory: declaration-only conformance at `governed`
      (stack/declaration edit + validator green; no template changes).
      Landed 2026-07-23: `MedxFactory/models/derived-model-conformance.yaml`
      (commit 0987bca) — dream_simulation family, canonical validator
      green against the unchanged ratified templates, local
      `make validate` green.
- [x] 4.2 First of AdxFactory/LedgerxFactory object-model changes lands
      with a `calibrated` declaration + validator green.
      Landed 2026-07-23: AdxFactory `add-adx-object-model` ratified,
      realized, archived (commit eb98f84) —
      `models/derived-model-conformance.yaml`, persona_simulation family
      at calibrated tier, canonical validator green (first
      calibrated-tier conformer; exercises writer separation and the
      field-lock binding form).
- [x] 4.3 Update DTN-014 register entry to `implemented` → `adopted` as
      the re-pins complete. Set to `implemented` at archive
      (2026-07-23); flips to `adopted` when domain stack pins advance
      to a ref containing the schema (the contract-v1.16 cut, with
      task 1.2).

Archive-gate status: evidence complete (Medx governed declaration-only +
Adx calibrated, both validator-green). Ratified and archived 2026-07-23.
Deferred to the contract-v1.16 bundle cut: manifest entry (1.2) and the
register `adopted` flip (4.3).
