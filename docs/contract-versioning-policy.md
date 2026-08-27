# Contract Versioning Policy

Status: ratified
Ratified by: add-release-inventory-drift-check

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

### Untagged Bundles After Enforcement Began — DISCHARGED 2026-08-25

Three bundles allocated AFTER mandatory tag publication began once carried a
changelog entry and a manifest version but NO published annotated tag:
`contract-v1.33`, `contract-v1.35` and `contract-v1.39`. Recorded here as an
undischarged gap when this policy was ratified, and **DISCHARGED on Brett's
ruling of 2026-08-25** by publishing each bundle's tag at the commit it was
actually realized at:

| bundle | realized commit | landed as |
|---|---|---|
| `contract-v1.33` | `71674ed58e338bf3f85a7b750b64f5f5ab6d02e1` | PR #190, 2026-08-15 |
| `contract-v1.35` | `78f8e016fbddcf1125c11b7f11234fb2478b0415` | PR #220, 2026-08-19 |
| `contract-v1.39` | `1f45e427bf7b2491aec09d2a9c9adeaaa5f99839` | PR #259, 2026-08-22 |

RETRO-PUBLISHED, NOT RE-DATED. Each tag names the commit its bundle was really
realized at; no release was reconstructed, re-cut, or altered, and no version
number was reused.

HOW THE REALIZED COMMIT WAS ESTABLISHED, recorded because the obvious method is
wrong. "The commit that introduced the bundle's changelog entry" reproduces only
five of the ten tags that already existed: where a release was COMPLETED by a
later commit — `contract-v1.31`, `contract-v1.36`, `contract-v1.37` — the tag
points at the completion, and where the work landed through a merge —
`contract-v1.32` — it points at the merge rather than at a branch-internal
commit. The rule actually used is:

> the EARLIEST FIRST-PARENT COMMIT on published `main` that DECLARES the bundle
> and at which `verify-commit` PASSES.

That rule reproduces **all ten** previously published tags exactly, including
`contract-v1.36`'s corrected target, which is why it was trusted for the three
that had none. `contract-v1.39` is the case that needed it: the commit
introducing its changelog entry is inside the change branch and is not a
landing, and tagging that commit would have named a target no other tag's shape
matches.

Every bundle from `contract-v1.7` — where mandatory publication begins — is now
tagged. The legacy `contract-v1.0`–`contract-v1.6` sequence remains untagged by
design, per the recovery recorded below.

THE RULE WAS NEVER ADVISORY, INCLUDING WHILE IT WAS BEING BROKEN. For the weeks
these three went untagged, "a bundle is not published until its tag exists" was
in force and simply unmet: they were a breach of the rule, never an exception to
it, and their having been consumed anyway is evidence of the cost of the gap
rather than a precedent. No reader may cite this subsection, or the period it
narrates, to treat an untagged bundle as released.

RECORDS DESCRIBING THE FORMER GAP STAND AS HISTORY. `docs/archive-record-discrepancies.md`
(`Status: record`) states that `contract-v1.33` and `contract-v1.35` are not git
tags. That was true when written and is deliberately NOT edited: a record is
immutable, exactly as an archived change packet is, and rewriting one to match
today's state would destroy the evidence of what was true then.

### Recovered Legacy Baseline

The historical `contract-v1.1` through `contract-v1.6` changelog entries were
created before tag enforcement and have no corresponding repository tags.
They are treated as an explicitly recovered, unpublished legacy sequence, and
`contract-v1.6` WAS the manifest baseline at the time of that recovery. (The
manifest baseline advances with every realized bundle and is whatever
`contracts/manifest.yaml` declares today; this sentence records the recovery,
not the current state.) The next realized contract change
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

### What a red `verify-commit` at HEAD means

`verify-commit` resolves the inventory to check from `contract_bundle_version`
AT THE COMMIT, deliberately, so that historical inventories from earlier
releases are ignored. A consequence follows that every reader of a red result
needs, and that this policy did not previously state:

**Between cuts, `verify-commit` at `HEAD` is EXPECTED to report mismatches on
the editorial members** — `contracts/CHANGELOG.md`, `contracts/manifest.yaml`
and `contracts/README.md`. A change that touches no contract still records
itself in the changelog and may still update a consumption rule or a per-file
digest, and the declared bundle's inventory was written before those edits
existed. The next cut re-baselines the inventory as part of the realization
order. A red result confined to those three members is therefore a bounded,
expected state and NOT a defect.

A mismatch on any OTHER member is a defect: a normative contract's bytes moved
while the repository went on declaring a bundle that describes different bytes.

**THE REMEDY IS A RELEASE CUT, NEVER A HAND-EDIT.** An inventory is a record of
what a release contained; editing one so that a check passes destroys the only
evidence that the release surface moved, and converts a detectable defect into
an undetectable one. The same applies to the manifest's `contract_bundle_version`:
it is advanced by a cut, not adjusted to make a comparison succeed.

`verify-commit` at a TAG is a different question and has no such allowance:
a published bundle must verify at its own commit exactly.

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

### contract-v1.36 Was Moved — a recorded breach, disposed of

`contract-v1.36` was published on 2026-08-21 at one commit and then deleted and
re-pushed to another, minutes later in the same session, to correct a cut whose
`contract_bundle_version` had been left at the previous release. That is a
breach of the rule immediately above, which forbids moving a published tag
**even for a defective release**. The tag today points at the corrected commit;
the superseded tag object and the reasoning are recorded in
`openspec/changes/add-release-inventory-drift-check/proposal.md` and in the
moving commit's own message.

**DISPOSITION — RECORD ONLY (Brett, 2026-08-24).** The breach stands recorded
and nothing further is owed.

TWO MOVES A LATER READER MUST NOT MAKE on discovering this:

1. **Do not move or re-point the tag again**, including to "restore" it to its
   original commit. A second move compounds the breach instead of repairing it,
   and the original commit does not carry a release that verifies.
2. **Do not cut a superseding release to "fix" it.** That is the sanctioned
   remedy for a DEFECTIVE RELEASE, and the release itself is not defective —
   it verifies at its tag. Spending a version number here would correct
   provenance that this record already carries accurately.

This subsection exists because the disposition would otherwise live only in a
change packet, which archives out of the path of anyone running `verify-tag`
and landing on the rule above (PR #319 review).

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
  style) — replaced by `hermes.layers`, whose role keys are
  `customer`/`client`/`domain`. THOSE KEYS ARE FROZEN MACHINE IDENTIFIERS, NOT
  THE CANONICAL VOCABULARY: the canonical Hermes layering has been Subject /
  Tenant / Domain since `adopt-subject-tenant-domain-vocabulary` was ratified
  2026-07-23, and the machine keys survive unrenamed precisely so that pinned
  consumers keep validating. The mapping between them is
  `contracts/policies/layer-vocabulary.yaml`; interpret the keys through it and
  never rename them ad hoc. Warned since contract-v1.1; removal target
  contract-v2.0.
- Layer/owner tokens beginning `openworkflow_` — replaced by `xfactory`.
  Warned since contract-v1.1; removal target contract-v2.0.
- The doxBench chat-turn v1 envelope family (`workbench-chat-turn`,
  `workbench-chat-turn-success`, `workbench-chat-turn-failure` in
  `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml`) — replaced by
  the co-resident widened `-v2` family that carries the outline plus every
  loaded document, the declared bound-buffer key on request and record, keyed
  observed hashes, a buffer-key proposal target, and the selected-model
  metadata. Deprecated at contract-v1.34; removal target contract-v2.0. The v1
  bytes are unchanged and keep validating until then.
- The eight openxWallet contracts (`openxwallet-record`,
  `openxwallet-custody-registry-schema`, `openxwallet-custody-registry`,
  `openxwallet-grant`, `openxwallet-grant-exercise`,
  `openxwallet-distinct-holder-constraint`, `openxwallet-subject-attestation` in
  `contracts/openxwallet/`, and `openxwallet-agent-composition` in
  `contracts/openxwallet-agent-profile/`) — their canonical home RELOCATES to
  `opensoft/openXwallet` at tag `wallet-v1.1`. Each manifest row carries a
  `relocating: {to, tag, since}` mapping, and
  `scripts/check-openxfactory-pin.py` emits a WARN-tier notice naming every
  relocating artifact when a domain pins a bundle that carries them. Migration is
  to read the artifacts from the target repository and pin them through
  `contracts/openxwallet-pin.yaml`, which arrives at the major; from the major
  forward this family's conformance validator is the pinned openXwallet
  `scripts/validate-openxwallet.py` at the digest that pin records. Deprecated at
  contract-v1.47; removal target contract-v2.0. The bytes are unchanged and keep
  validating until then.
