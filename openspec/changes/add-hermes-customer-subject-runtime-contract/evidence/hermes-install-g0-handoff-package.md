# Gate G0 Provider→Consumer Handoff Package — contract-v1.10

Status: record
Kind: handoff

**Change**: add-hermes-customer-subject-runtime-contract
**Feature**: 005-customer-subject-runtime · Task 5.1 / T082-precondition
**Date**: 2026-07-14

## 0. Purpose and ownership boundary

This package discharges OpenSpec task **5.1** — *hand the published bundle
evidence to the existing Hermes Install OpenSpec/Speckit feature*. Per **FR-038**,
downstream neutralization, checker implementation, and pinning remain owned by
that feature (`opensoft/xFactory-Hermes-Install`, change
`implement-three-layer-hermes-runtime-foundation` / Speckit feature
`001-three-layer-hermes-runtime`); openxFactory accepts the result **only as
external Gate evidence** (tasks 5.2/5.3, feature tasks T082–T084). This document
does not implement any consumer artifact — it specifies exactly what the
downstream must produce so the provider-side receipt validates on first try.

Gate G0 / T009 stay OPEN until both sides independently reproduce every digest
(SC-012). No provider file here closes the gate.

## 1. Pin target: contract-v1.10 (supersedes contract-v1.9)

contract-v1.9 was superseded by **contract-v1.10** on 2026-07-14 (it folded the
F-4/F-7..F-9 backlog and was published with Brett's explicit gate approval).
The v1.9 tag remains reproducible at its commit, but **G0 must pin the current
bundle, contract-v1.10.** All values below are verified against the published
tag.

| Item | Value |
|---|---|
| Provider repository | `opensoft/openxFactory` (`git@github.com:opensoft/openxFactory.git`) |
| Bundle tag (annotated object) | `contract-v1.10` → tag object `6cae9eb2bf564e076a738bfc11b634bc1abdb593` |
| Peeled / published commit | `727ca18b80ad1e9cbef1252e4e357e1cdc43249a` |
| Manifest path / digest | `contracts/manifest.yaml` / `sha256:664d89aabf9775943c2613e5132865b84688080efb1cd316f1a56d21446398ad` |
| Release inventory path / digest | `contracts/releases/contract-v1.10.digests.yaml` / `sha256:8d76e525b3852c4b05f0d76f7226d2a9deffabed2017aa57525004e4849883ed` |
| Inventory descriptor | `kind: openxfactory-contract-release-digest-inventory`, `bundle_tag: contract-v1.10`, `digest_algorithm: sha256`, `digest_source: raw_git_blob`, `path_order: bytewise_utf8`, **179 members**, self-excluded, no `commit` field |
| Manifest declares | `contract_bundle_version: contract-v1.10` |

Per-contract pin format (one entry per required member; drawn from the
inventory's 179 `entries[]`). Example:

```yaml
artifact_id: consumer-handoff-receipt
path: contracts/hermes-runtime/consumer-handoff-receipt.schema.yaml
type: schema
git_mode: "100644"
schema_id: consumer-handoff-receipt
schema_version: 1
digest: sha256:92977e5d1a56d87b5d2fa031eefbd55d01bac2c1fcd3fc70e937efb6cdeb0fc9
```

`digest_source: raw_git_blob` = `sha256:` + SHA-256 of the exact committed blob
bytes at commit `727ca18…` (no working-tree bytes).

## 2. What the downstream consumer MUST produce (all committed at one exact commit)

The provider receipt reads these ONLY as `commit:path` git objects at the
consumer's landed commit; working-tree bytes are never read. Paths are
consumer-chosen except `closure_packet.path` (fixed, §3). Fixture-observed
conventions in parentheses.

- **(a) Compatibility manifest** (`config/compatibility/contract-v1.10.yaml`) —
  FR-034: records repository, bundle tag `contract-v1.10`, exact commit
  `727ca18…`, manifest+inventory paths/digests (§1), and unique per-contract
  `{id, path, schema_version, digest}` entries drawn from the inventory. **FR-036:
  the manifest's OWN digest MUST be bound from external runtime/realization
  evidence — never self-recorded inside the manifest.**
- **(b) Compatibility checker** (`config/scripts/verify-contract-bundle.py`) —
  FR-035 / SC-010, two modes: **online** (tag `contract-v1.10` is annotated,
  published, dereferences to `727ca18…`; manifest+changelog declare the same
  version) and **offline** (reproduce every required digest from exact
  commit/tree/blob objects already present, no mutable working tree). MUST fail
  closed for branch refs, tag-only refs, duplicate IDs/paths, missing members,
  path traversal, symlink escape, version mismatch, digest drift, moved/incomplete
  pins.
- **(c) Runtime binding** (`config/runtime/contract-binding.yaml`,
  `kind: hermes-runtime-contract-binding`) — binds the runtime to the pinned
  bundle; recorded as a receipt artifact reference.
- **(d) Closure packet** — path is **mandatory and exact**:
  `evidence/gates/g0/contract-v1.10.yaml` (the receipt enforces
  `closure_packet.path == evidence/gates/g0/<bundle_tag>.yaml`; otherwise
  `HGR-HANDOFF-PACKET-PATH`). Validated downstream against the
  **consumer-owned** `config/schemas/g0-closure-evidence.schema.yaml`. Required
  contents (release-and-consumer-pin.md "Hermes Install Closure Packet"):
  openxFactory repository, annotated tag object, peeled commit, manifest/inventory
  paths+digests; every consumed contract id/path/schema-version/digest; the exact
  landed Hermes Install commit; repo-relative compatibility-manifest / checker /
  runtime-binding / evidence paths+digests; positive online/offline AND
  deliberate-drift command results plus evidence digests; strict OpenSpec and
  Speckit-analysis results. Suggested `kind: g0-closure-evidence`.
- **(e) Positive AND negative pin-check evidence** (committed logs). Minimum set:
  - positive[] (`outcome: pass`): `online-verify` (mode `online`),
    `offline-verify` (mode `offline`).
  - negative[] (`outcome: fail`): `deliberate-drift` (mode `offline`) — a mutated
    pinned blob detected → verification failed.
  - `check_id` pattern `^[a-z0-9]+(?:-[a-z0-9]+)*$`; `mode ∈ {online, offline}`.

## 3. The provider-side receipt the openxFactory feature will author (T082)

`openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/hermes-install-g0-handoff.yaml`,
validated against `contracts/hermes-runtime/consumer-handoff-receipt.schema.yaml`.
Required top-level fields (schema `additionalProperties: false`):

| Field | Constraint |
|---|---|
| `schema_version` | const `1` |
| `kind` | const `openxfactory-hermes-runtime-consumer-handoff-receipt` |
| `consumer_repository` | const `opensoft/xFactory-Hermes-Install` |
| `bundle_tag` | `^contract-v[0-9]+\.[0-9]+$` → `contract-v1.10` |
| `provider` | `{repository=opensoft/openxFactory, tag=contract-v1.10, commit=727ca18…, manifest_path=contracts/manifest.yaml, manifest_digest=sha256:664d89aa…, inventory_path=contracts/releases/contract-v1.10.digests.yaml, inventory_digest=sha256:8d76e525…}` |
| `consumer_commit` | 40-hex — the exact landed Hermes Install commit |
| `closure_packet` | `{path=evidence/gates/g0/contract-v1.10.yaml, digest}` |
| `compatibility_manifest`, `checker`, `runtime_binding`, `evidence` | each `{path (repo-relative), digest (sha256)}` |
| `check_results` | `{positive[] (minItems 1, outcome const pass), negative[] (minItems 1, outcome const fail)}` |

**Validation order** (`validate_handoff_receipt`): (1) `consumer_repository`
const check FIRST, before any object read — `FarHeap/Hermes-Install` returns
only `HGR-HANDOFF-CONSUMER-REPOSITORY` and short-circuits; (2) field-agreement
without git reads (`HGR-HANDOFF-PROVIDER`, `-TAG`, `-COMMIT`, `-PACKET-PATH`,
`-STRUCTURE`, `-CHECK-RESULTS`); (3) only if clean, reproduce each consumer
artifact + check-evidence blob at `consumer_commit` (`HGR-HANDOFF-PACKET-DIGEST`,
`-ARTIFACT-DIGEST`). Note: the receipt does **not** re-derive
`provider.manifest_digest`/`inventory_digest`/`commit` — those are recorded pins
reproduced by the downstream checker (§2b) and provider `verify-tag`/
`verify-promotion`; they must still be exactly correct.

Provider validation command (quickstart §9):

```
python scripts/validate-hermes-runtime-contracts.py \
  --handoff-receipt openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/hermes-install-g0-handoff.yaml \
  --consumer-repo "opensoft/xFactory-Hermes-Install=$HERMES_INSTALL_REPO" \
  --strict
```

Exit codes: `0` pass; `1` contract finding; `2` dependency (consumer repo/commit
unresolvable, missing git object, bad `--consumer-repo` mapping, unreadable
receipt). Alternative resolver: `--consumer-repo-root <mirror-root>`.

## 4. Full drift matrix the consumer checker + provider receipt must satisfy (SC-010)

| Case | Primary finding code | Expected |
|---|---|---|
| wrong repository (`FarHeap/Hermes-Install`) | `HGR-HANDOFF-CONSUMER-REPOSITORY` | fail (before any object read) |
| tag drift | `HGR-HANDOFF-TAG` | fail |
| commit drift | `HGR-HANDOFF-COMMIT` | fail |
| closure-packet path ≠ `evidence/gates/g0/<tag>.yaml` | `HGR-HANDOFF-PACKET-PATH` | fail |
| closure-packet digest drift | `HGR-HANDOFF-PACKET-DIGEST` | fail |
| artifact (manifest/checker/binding/evidence) digest drift | `HGR-HANDOFF-ARTIFACT-DIGEST` | fail |
| negative check recorded `outcome: pass` | `HGR-HANDOFF-CHECK-RESULTS` | fail |
| older valid pin (e.g. `contract-v1.6`) | — | pass (older valid pin remains conformant) |

## 5. Reconciliation with the downstream feature's existing model

The `001-three-layer-hermes-runtime` Speckit feature currently models
consumption as `config/compatibility-manifest.yaml` + a `realization-packet`
schema, and frames Gate G0 as *"openxFactory must first publish a neutral
multi-Project/layer-scope bundle"*. That bundle now exists — **contract-v1.10
is it** (multi-Customer topology, installation/stack/layer scope, cross-layer
bindings, immutable approvals + revocation, non-null artifact digests, scoped
traceability, migration, validator). To close G0 the downstream feature should:

1. Treat **contract-v1.10** as the bundle satisfying its Gate G0 / T009 (record
   its pin in `config/compatibility-manifest.yaml` using §1's values).
2. **Additionally** emit the provider-facing artifacts in §2 — specifically the
   `evidence/gates/g0/contract-v1.10.yaml` closure packet and the
   consumer-owned `config/schemas/g0-closure-evidence.schema.yaml` — so the
   provider receipt (§3) validates. The `realization-packet` model is
   complementary (live-run realization); the closure packet is the G0-specific
   artifact the provider receipt reproduces.
3. Own the final `config/schemas/g0-closure-evidence.schema.yaml` (fields per
   §2d); openxFactory does not define it.

## 6. Acceptance path (provider side, after the consumer lands)

- **T082 / 5.2**: openxFactory authors `hermes-install-g0-handoff.yaml` (§3) and
  runs the §3 command against the landed `consumer_commit` → exit 0.
- **T083**: final clean-clone provider/consumer quickstart + all validators
  (non-database 30s / per-major 10min budgets).
- **T084 / 5.3**: rerun strict OpenSpec + clean Speckit analysis; accept only
  externally reproduced downstream T009 closure; flip Gate acceptance **without
  editing the consumer repository**. Gate G0 / T009 closed only when both sides
  independently reproduce every digest (SC-012).

Governing: FR-034 (pin), FR-035 (online+offline, fail every drift), FR-036
(manifest digest externally bound), FR-038 (ownership), FR-043 (canonical
consumer, reject FarHeap, record exact commit + paths/digests + pos/neg),
SC-010, SC-012.
