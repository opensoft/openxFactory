# Contract: the manifest rows

**Feature**: `017-openxwallet-carve` · **Authority**: tasks 3.11–3.15, design D7 (N8)

## Owned member — the shape all eight share

```yaml
- id: <VERBATIM from openxFactory>
  path: <VERBATIM>
  source_path: openXwallet/<path>          # the ONLY rewritten field
  type: <VERBATIM: schema | registry>
  schema_version: <VERBATIM: 1>
  sha256: <VERBATIM — this is the byte-identity floor>
  compatibility: canonical_openxfactory_contract   # VERBATIM
  adapter_owner: openxFactory                      # VERBATIM (R2 freezes machine keys in v1)
  consumption_rule: <VERBATIM prose>
```

**Acceptance**: for each of the eight, `sha256sum <path>` in the carved tree
equals this row's `sha256`, and that value equals openxFactory's row at the carve
commit.

## Consumed member — the one row that is not owned

```yaml
- id: hermes-job-envelope
  path: contracts/schemas/hermes-job-envelope.schema.yaml
  source_path: openxFactory/contracts/schemas/hermes-job-envelope.schema.yaml
  type: schema
  schema_version: 1
  sha256: <computed over the pinned bytes at CARVE_COMMIT>
  compatibility: canonical_openxfactory_contract
  adapter_owner: openxFactory
  consumption_rule: <read-only at the pinned digest; rule (g) reads the
    approval-scope vocabulary out of it>
  member_class: consumed
  release_surface: false
  pinned_openxfactory_bundle: contract-v1.44
```

**Acceptance**

1. All nine publisher fields present (`shared-contract-ownership:142` — all
   markers together).
2. `member_class: consumed` — openXwallet does not claim ownership.
3. `release_surface: false` — excluded from `wallet-vN.M.digests.yaml` by DECLARED
   FIELD.
4. `sha256` equals `contract_pin.yaml`'s recorded digest for the same path, so the
   verifier and the manifest cannot disagree.

## Release-surface selection contract

```
release members  ==  { row | row.member_class == "owned" }
```

Never `{ row | not row.path.startswith("contracts/schemas/") }` — that heuristic
breaks the day openXwallet publishes a schema of its own there.

## Manifest header contract

```yaml
schema_version: 1
kind: contract_manifest
contract_bundle_version: wallet-v1.0
carved_from:
  repository: opensoft/openxFactory
  commit: <40-hex>
```

`carved_from` is the machine-read provenance record. A bare `CARVE_COMMIT` file is
forbidden.
