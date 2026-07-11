# Contract Versioning Policy

Status: draft

This policy governs how openxFactory contracts change and how DomainxFactory
repos upgrade. It closes the gap where everything was `schema_version: 1`
pinned to a single commit with no defined upgrade path.

## Version Identity

A contract release is identified by five coordinated values:

1. `contract_schema_version` — an integer on each contract file and on the
   contract set as a whole. Incremented only for breaking changes.
2. `contract_bundle_version` in `contracts/manifest.yaml` — the aggregate
   release version allocated at realization after merge order is known.
3. An annotated git tag on openxFactory of the form
   `contract-v<major>.<minor>` (for example `contract-v1.0`). Minor increments
   are additive and non-breaking; major increments occur together with
   `contract_schema_version`.
4. The exact release commit plus per-file SHA-256 digests — the
   content-addressed identity consumers pin. A movable branch or tag alone is
   not a sufficient compatibility pin.
5. `contracts/CHANGELOG.md` — one entry per release listing every contract
   added, changed, or deprecated, with migration notes for breaking changes.

The manifest version, changelog heading, and annotated tag MUST match. The
manifest and changelog update SHALL be committed atomically with the contract
files; the tag SHALL point to that realized commit. A proposed change MUST NOT
reserve a minor number before merge order is known, and a bundle is not
published until its tag exists. Consumers record the human-readable bundle
tag while pinning the exact commit and required file digests.

### Recovered Legacy Baseline

The historical `contract-v1.1` through `contract-v1.6` changelog entries were
created before tag enforcement and have no corresponding repository tags.
They are treated as an explicitly recovered, unpublished legacy sequence with
`contract-v1.6` as the manifest baseline. The next realized contract change
allocates the next available minor version and begins mandatory annotated-tag
publication; historical tags MUST NOT be fabricated retroactively.

## Change Classes

- **Additive (minor)** — new optional fields, new contracts, new validator
  warnings. Domain repos on the same major version remain conformant
  without changes.
- **Deprecating (minor)** — a field or shape is marked deprecated; the
  conformance validator emits warnings but still accepts it. Deprecations
  must state the removal version and a migration path in the CHANGELOG.
- **Breaking (major)** — a required field is added, a shape is removed, or
  role/vocabulary semantics change. Requires: a CHANGELOG migration note,
  at least one full minor release where the old shape produced deprecation
  warnings, and an update to the conformance validator that accepts the new
  shape and rejects the old one only at the new major version.

## Domain Upgrade Runbook

1. Read `contracts/CHANGELOG.md` between the pinned ref and the target ref.
2. Update `stack.yaml` `xfactory.contract_ref` (and `contract_schema_version`
   if major) to the exact target release commit, record the matching bundle
   tag, and update required per-file digests.
3. Run `openxFactory/scripts/validate-domain-factory.py <domain-repo> --strict`
   from the target checkout. Fix every error; triage every warning.
4. Record the upgrade in the domain repo (commit message referencing the
   contract tag), then update the tenant records that pin versions.

## Compatibility Direction (restated)

Compatibility flows from DomainxFactory to openxFactory. openxFactory never
pins domain repos. A domain repo remains valid against its pinned version
until it explicitly upgrades; nothing in a new openxFactory release may
retroactively invalidate an old pin.

## Deprecations Currently In Force

- `hermes` flat keys (`subject_overlay`, `subject_layer_name`,
  `care_organization_overlay`, `client_overlay`/`customer_overlay` flat
  style) — replaced by `hermes.layers` with canonical roles
  customer/client/domain. Warned since contract-v1.1; removal target
  contract-v2.0.
- Layer/owner tokens beginning `openworkflow_` — replaced by `xfactory`.
  Warned since contract-v1.1; removal target contract-v2.0.
