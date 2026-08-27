# Phase 1 Data Model: openxwallet deprecation minor (P2.5)

Three data shapes change or appear. None is a runtime entity; all are release
metadata read by tooling and by humans.

---

## 1. `relocating` — the per-row relocation declaration (NEW)

A mapping added as the last key of a `contracts` entry in
`contracts/manifest.yaml`.

```yaml
  - id: openxwallet-record
    path: contracts/openxwallet/openxwallet-record.schema.yaml
    source_path: openxFactory/contracts/openxwallet/openxwallet-record.schema.yaml
    type: schema
    schema_version: 1
    sha256: 2012ef432616e73ddaead17c5e79aefacef712c2049ff649c15d7230b1d4eb08
    compatibility: canonical_openxfactory_contract
    adapter_owner: openxFactory
    consumption_rule: >-
      … unchanged …
    relocating:
      to: opensoft/openXwallet
      tag: wallet-v1.1
      since: contract-v1.46
```

| field | type | required | meaning |
|---|---|---|---|
| `to` | string, `owner/repo` | yes | the repository that becomes this artifact's canonical home |
| `tag` | string | yes | the tag in `to` a consumer should migrate to |
| `since` | string, `contract-vN.M` | yes | the openxFactory bundle from which this declaration is in force |

**Deliberately absent**: any removal-version field. `docs/contract-versioning-policy.md:246-248`
puts the removal version in the CHANGELOG, and `tasks.md` 5.2 forbids putting it
on the row. A row that carried a removal version would either duplicate the
changelog or contradict it.

**Validation rules**
- Present on exactly the eight openxwallet rows; on no other row.
- All three sub-keys present, all non-empty strings.
- Must NOT contain a `path` or `sha256` key — `scripts/validate-manifest-digests.py`
  walks nested mappings and treats the co-presence of those two as an artifact
  entry (research R1).
- Adding it must not alter any other byte of the row.

**Lifecycle**
```
absent  ──(this feature, contract-v1.46)──▶  present
present ──(P3, the next major)───────────▶  row deleted entirely
present ──(reversal, a following minor)──▶  absent
```
There is no "expired" or "removed_at" state on the row: the row's own removal IS
the terminal transition, and it happens in P3, not here. A published bundle is
never unpublished, so the reversal arrow is a NEW minor, never a revert of the
cut (`tasks.md` 5.10).

---

## 2. `RelocatingRow` — the checker's in-memory projection (NEW, transient)

What `scripts/check-openxfactory-pin.py` extracts from the pinned manifest. Not
persisted anywhere.

| field | source | used for |
|---|---|---|
| `artifact_id` | the row's `id` | naming the artifact in the notice |
| `to` | `relocating.to` | naming the target repository |
| `tag` | `relocating.tag` | naming the successor tag |

**Ordering**: manifest order, preserved. Deterministic (the manifest is a file)
and it keeps the eight reading as the single authored block they are.

**Cardinality**: 0..N. Zero is the overwhelmingly common case and must produce no
output at all.

**Absence is distinct from emptiness**: an unreadable or unparseable manifest
yields *no projection and no notice*, which is not the same as a manifest that
parses to zero relocating rows — but both produce identical output (nothing), so
the distinction is internal only and never reported. This is the
release-inventory family's doctrine reused: "a question that could not be asked"
is not a finding.

---

## 3. The release inventory (EXISTING shape, new instance)

`contracts/releases/contract-v1.46.digests.yaml`, generated. Shape is fixed by
`contracts/releases/release-digest-inventory.schema.yaml` and emitted by
`release.build_release_inventory`:

```yaml
schema_version: 1
kind: openxfactory-contract-release-digest-inventory
bundle_tag: contract-v1.46
repository: opensoft/openxFactory
digest_algorithm: sha256
digest_source: raw_git_blob
path_order: bytewise_utf8
entries:
- artifact_id: contracts-changelog.md
  path: contracts/CHANGELOG.md
  type: changelog
  git_mode: '100644'
  digest: sha256:…
  … 192 entries, bytewise-sorted by path, excluding this file …
```

**What this instance must satisfy**
- `bundle_tag` equals `contracts/manifest.yaml`'s `contract_bundle_version`
  equals the newest `contracts/CHANGELOG.md` heading equals this file's basename.
- 192 entries — the same membership as `contract-v1.45`. This feature adds no
  release-surface member and removes none.
- The eight openxwallet registrations still present (FR-017), TRANSITIVELY:
  membership is catalog-driven from
  `contracts/hermes-runtime/contract-index.yaml`, so the eight artifact FILES are
  not inventory members and never were — not at `contract-v1.45` either
  (research R11). What the inventory records is the digest of
  `contracts/manifest.yaml`, which still carries all eight rows. At P3 that same
  member's digest will record a manifest with none, which is how the inventory
  distinguishes the two surfaces.
- Three members' digests DO change relative to `contract-v1.45`:
  `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, and
  `docs/contract-versioning-policy.md` — the three files this feature edits. A
  fourth, `scripts/validate-hermes-runtime-contracts.py`, changes relative to the
  v1.45 inventory because of **pre-existing** drift at the base commit
  (research R8); this cut records its true bytes and thereby discharges that
  standing error.

---

## Relationships

```
contracts/manifest.yaml
  ├── contract_bundle_version ──── must equal ────▶ CHANGELOG newest heading
  │                             └── must equal ────▶ releases/<tag>.digests.yaml basename + bundle_tag
  │
  └── contracts[8].relocating
        ├── read by ──▶ scripts/check-openxfactory-pin.py  (at the consumer's PINNED commit)
        │                    └── emits ──▶ the WARN-tier relocation notice
        ├── points at ─▶ opensoft/openXwallet @ wallet-v1.1
        └── explained by ─▶ contracts/CHANGELOG.md § contract-v1.46
                                  └── removal version + migration path
                                        └── mirrored in ─▶ docs/contract-versioning-policy.md
                                                            § Deprecations Currently In Force
```

The only *machine-checked* edge is the three-way bundle-name agreement, enforced
by `scripts/doc_health/release_inventory.py`. Every other edge is a human
obligation the changelog section and the policy-doc entry exist to make legible —
which is the whole reason D5 put the marker in the manifest rather than in a
validator.
