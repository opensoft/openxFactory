# Data Model: The First Wallet (013)

**Feature**: 013-first-wallet | **Date**: 2026-08-24

## Live record: `governance/review-authority/wallets/wal-agent-mrc-0001.yaml`

Conforms to `contracts/openxwallet/openxwallet-record.schema.yaml` v1
(`kind: xfactory_wallet_record`).

| Field | Value | Why |
|---|---|---|
| `schema_version` | `1` | Shipped family version; no bump |
| `kind` | `xfactory_wallet_record` | Family record kind |
| `wallet_id` | `wal-agent-mrc-0001` | House pattern `wal-<holder>-<NNNN>`; referenced by future grants + the attestation row |
| `holder.holder_id` | `agent:merge-readiness-council` | Body identity, codexFactory council namespace style (`agent:<name>`) |
| `holder.holder_class` | `agent` | Operator ruling; OXWA profile's target class |
| `holder.display_label` | `codexFactory merge readiness council (body)` | Human-readable; the MVP's ONE holder |
| `key_reference.did` | `did:key:<operator-minted multibase>` | Pattern `^did:[a-z0-9]+:[A-Za-z0-9._:%-]+$` admits did:key; value supplied by operator mint (T003) |
| `key_reference.key_id` | `key-mrc-0001` | House `key-<holder>-<NNNN>` pattern |
| `key_reference.public_key_multibase` | `<multibase>` | Public key is not key material (schema comment); included so verifiers can check proofs |
| `key_reference.signature_algorithm` | `ed25519` | Mint choice; closed-set member; also the exercise-proof family's first-class curve |
| `custody.model` | `holder_readable` | Closed registry member; N13 |
| `custody.registry_version` | `1` | Canonical registry version |
| `custody.declared_at` / `created_at` | mint-day RFC3339 | Declared/created at finalization |
| `custody.declared_by` | `Brett.Heap` | `$defs/identifier` grammar has NO `@` — S2 widened ONLY grant `issued_by`; email anchor is not generalized |
| `state` | `active` | Cold start |
| `policy_version` | `1` | House example convention |

NOT present by design: composition block (belongs to agent-profile records;
core imposes composition on no class — task 4.4 lands it codexFactory-side),
any grant field, any key material.

## Attestation row: `governance/review-authority/attestations/custody-attest-wal-agent-mrc-0001.yaml`

DELIBERATELY KINDLESS — no `kind:` field, so `repo_scan` treats it as context,
not a family record. Inventing a schema here would be an unratified contract
release.

| Field | Value | Why |
|---|---|---|
| `attestation_id` | `attest-custody-wal-agent-mrc-0001` | Names wallet + subject matter |
| `subject_wallet_ref` | `wal-agent-mrc-0001` | Resolution to the record |
| `custody_model_attested` | `holder_readable` | What was attested |
| `verified_by.{name,role,standing}` | Brett Heap / responsible operator / HEC `docs/roles-and-authority.md:103-140` | Who, and under what standing |
| `verified_at` | mint-day RFC3339 | When |
| `verified_against.method` | `operator-minted ed25519 keypair` | Against what |
| `verified_against.basis` | private half retained operator-side outside every governed repo; only public half entered the tree | The honest verification statement |
| `verified_against.isolation_claimed` | `none` | holder_readable claims NO isolation — environment evidence |
| `compensating_control` | approval-before-apply at tier `act`, constitutional floor | Registry's own design intent (N13) |
| `cap_effect_if_absent` | grants cap at `request` | The ratified rule this row satisfies |
| `governing_task` | `add-wallet-carried-review-authority` tasks 4.3 | Traceability |

## Naming decisions

- `wal-agent-mrc-0001`: compact, sortable, house-patterned; full body name in
  `display_label`.
- Directory verbs mirror the arc: `wallets/` now, register joins this
  directory at S4 (N7 same-tree), exercises stay runtime-side (S3).
