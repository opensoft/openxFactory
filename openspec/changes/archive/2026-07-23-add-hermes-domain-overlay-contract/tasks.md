# Tasks — add-hermes-domain-overlay-contract

## 1. Schemas

- [x] 1.1 Author `contracts/hermes-domain-overlay/hermes-domain-overlay.schema.yaml`
      (identity, approval scopes, required fields, authority boundaries,
      no-overlap rule).
- [x] 1.2 Author `contracts/hermes-domain-overlay/overlay-descriptor.schema.yaml`
      (per-role path declaration; documented convention fallback).
- [x] 1.3 Contract README documenting shape, fallback rule, and consumers.

## 2. Validator + fixtures

- [x] 2.1 Implement `scripts/validate-hermes-domain-overlay.py` (schema check,
      no-overlap, descriptor path existence; repo-path argument like the
      other canonical validators).
- [x] 2.2 Fixtures: one positive (modeled on codexFactory's live overlay),
      negatives for missing block, empty list, overlapping boundaries,
      dangling descriptor path.
- [x] 2.3 Prove against the real consumer: validator passes on
      `xFactories/codexFactory` unmodified.

## 3. Publication + close out

- [x] 3.1 Register in `contracts/manifest.yaml`; version per
      `docs/contract-versioning-policy.md` (additive bundle allocated at
      realization).
- [x] 3.2 `OPENSPEC_TELEMETRY=0 openspec validate
      add-hermes-domain-overlay-contract --strict` and the openxFactory
      validator suite green.
- [x] 3.3 README OpenSpec Records entry; staging INDEX
      (`layer-content-materialization`) updated; note the hermes-install
      adoption handoff (seeding increment 2 pins the released bundle).
