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

## Release Digest Inventory

The per-file digest identity (item 4 above) is realized as a canonical
release digest inventory at `contracts/releases/<bundle-tag>.digests.yaml`,
validated against `contracts/releases/release-digest-inventory.schema.yaml`.

- Every digest is the SHA-256 of the raw Git blob bytes at the release
  commit, encoded lowercase as `sha256:<64hex>`. Text canonicalization,
  checkout-filtered bytes, working-tree reads, symlinks, and submodule
  gitlinks are all invalid digest sources.
- Entries list unique repository-relative regular-file paths in bytewise
  UTF-8 order, each with an artifact ID, type, Git file mode, and optional
  schema ID and version.
- Membership is closed over the release surface: the Hermes runtime contract
  family, its indexed fixtures, the validators, the hash-locked requirements
  files, the PostgreSQL image lock, the inventory schema, the contracts
  manifest, changelog, and README, and every modified normative contract or
  versioning document. Missing, extra, duplicate, out-of-order, symlink,
  submodule, traversing, and host-absolute members all fail validation.
- The inventory excludes exactly itself and carries no commit field. Either
  would be circular; the annotated tag and the downstream compatibility
  manifest anchor the commit and the inventory digest instead.

`scripts/validate-contract-release.py` enforces this identity with four
subcommands: `build --tag <tag> --output <path>` writes a candidate
inventory from exact bytes; `verify-commit --commit <sha>` reproduces every
digest from the pinned commit's Git objects; `verify-promotion --commit
<sha> --remote <name> --tag <tag>` proves, before tagging, that the tag is
absent, the version is the next available, the reviewed candidate is
reachable from remote main, and no release-surface blob drifted; and
`verify-tag --remote <name> --tag <tag>` proves the published annotated tag
dereferences to the exact commit. Exit codes: 0 pass, 1 findings, 2
dependency/harness failure.

## Bundle Realization Order

Contract-bundle realization is serialized and allocates versions late:

1. Fetch and rebase onto the final integration point, then immediately
   recheck bundle/tag availability and allocate the next available version.
2. Update every release surface — manifest, changelog, realized digest
   inventory — atomically with the contract files in one candidate commit.
3. Run every gate and independent review against that exact unchanged
   candidate commit.
4. Land the exact reviewed commit on published `origin/main`. If promotion
   creates a different commit, that commit becomes the new candidate and
   every gate and review reruns before tagging.
5. Publish the annotated tag pointing at the exact published commit and
   verify it from an independently refreshed checkout.

Release metadata rejects host-absolute paths, and the legacy
`local_source_path` field is removed only after a recorded
supported-consumer audit proves no supported consumer requires it.

## Immutable Tag Correction

A published annotated tag is immutable: it is never moved, deleted, or
re-tagged, not even for a defective release. A release found defective after
tagging is corrected by a superseding release — allocate the next available
version through the same realization order, record the defect and its
migration guidance in `contracts/CHANGELOG.md`, and let consumers upgrade by
pinning the new bundle. The defective tag and its digest inventory remain in
place as immutable provenance: nothing retroactively invalidates the
evidence of consumers that verified against it, and its version number is
never reused.

## Supported-Domain Regression Denominator

Publication is gated on a versioned regression inventory, never on an
implicit "all current domains" scan.
`contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` names
every supported DomainxFactory repository with an exact published commit,
`stack.yaml` path, raw-blob digest, and expected contract pin — currently
`opensoft/AdxFactory`, `opensoft/LedgerxFactory`, `opensoft/MedxFactory`,
`opensoft/OpsxFactory`, and `opensoft/codexFactory`, with
`opensoft/LegalxFactory` recorded as an explicit exclusion until it carries
a canonical `stack.yaml`. Before a bundle publishes, every inventoried pin
must revalidate from exact `commit:path` Git objects resolved through
deterministic mappings (`--domain-repo <canonical-repo>=<checkout>`, or
`--domain-repo-root` under which `owner/repo` resolves only to
`<root>/<owner>/<repo>` or `<root>/<owner>/<repo>.git`); missing objects are
dependency failures, not skips. The denominator is release evidence about
supported consumers; it does not invert the compatibility direction restated
below — openxFactory still never pins domain repos as a dependency.

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
