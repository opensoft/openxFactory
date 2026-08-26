# Implementation Plan: The First Wallet (wallet arc cold start)

**Branch**: `013-first-wallet` | **Date**: 2026-08-24 | **Spec**: [spec.md](./spec.md)

**Input**: Tasks §4.1–4.3 of ratified `add-wallet-carried-review-authority`.

## Summary

Cold start of the wallet world: ONE live wallet record for codexFactory's
`merge_readiness_council` as a body — holder class `agent`, custody
`holder_readable` (ceiling `act`; approval-before-apply already constitutional)
— plus its kindless custody attestation row (who / against what / when), both
under `governance/review-authority/` where S4's register will land. The core
validator imposes composition on no class, so the record mints legally ahead
of task 4.4's codexFactory-side composition mapping. No grant, no register, no
contract bytes. The `[OPERATOR]` leg of 4.1 (key minting) is discharged by
Brett minting an ed25519 keypair operator-side; only the public half enters
this repository.

## Technical Context

**Language/Version**: YAML data records; no code changes.

**Primary Dependencies**: `contracts/openxwallet/openxwallet-record.schema.yaml`
(v1); `scripts/validate-openxwallet.py` layer-2 `repo_scan`; S1's CI gate
(`wallet-validation`, required post-S1); S2's issuer-anchor semantics (not yet
exercised — no grant here).

**Storage**: Two new live-instance files under `governance/review-authority/`.
This is the declared narrow exception to "openxFactory ships no instance
records" (N7: cross-repo audience wallets have no resolution path; the MVP's
single holder must resolve in-tree).

**Testing**: Whole-checkout `--strict` sweep (live record counted);
packaged-corpus self-test unchanged at S2 baseline; pytest
`tests/wallet_yaml_syntax_gate/`; `openspec validate --all --strict`.

**Constraints**: No `examples/` residency (scanner excludes it); identifier
grammar has no `@`, so `custody.declared_by` uses `Brett.Heap` — the email
anchor token remains a GRANT `issued_by` semantic only (S2 widening scope);
attestation row deliberately carries no family `kind:`.

**Scale/Scope**: Ten files: eight spec-packet documents, two live YAML records.
Zero code, zero schema, zero corpus fixtures.

## Constitution Check

| Principle | Verdict | Notes |
|---|---|---|
| I. Contract-first neutral core | PASS | Consumes shipped v1 schemas; adds none |
| II. Governed change flow | PASS | Realizes §4 of the RATIFIED change; operator rulings recorded |
| III. Document lifecycle/status | PASS | Packet under specs/013-first-wallet/ |
| IV. Schema & artifact discipline | PASS | Live instances outside contracts/; kindless attestation is not a contract surface |
| V. Validation gates | PASS by construction | Sweep + self-test + pytest + openspec strict |
| VI. Versioned releases | PASS | No manifest entry, no CHANGELOG line, no bundle cut |
| VII. Fail-closed boundaries | PASS | Closed-set custody/class enums; no key material admitted |

## Project Structure

### Documentation (this feature)

```text
specs/013-first-wallet/
├── spec.md                  # this feature's specification
├── plan.md                  # this file
├── research.md              # verified substrate facts behind every choice
├── data-model.md            # exact field values + naming decisions
├── quickstart.md            # commands to verify the lane
├── tasks.md                 # dependency-ordered, [OPERATOR] marked
├── checklists/requirements.md
└── implementation-notes.md  # operator rulings + gate evidence (as landed)
```

No clarify round: scope is dictated by ratified tasks §4 and four operator
rulings (2026-08-24) recorded in implementation-notes.

### Source (repository root)

```text
governance/review-authority/
├── wallets/wal-agent-mrc-0001.yaml                 # FR-001/002 — live record
└── attestations/custody-attest-wal-agent-mrc-0001.yaml   # FR-003 — kindless row
```

**Avoid touching**: `contracts/**` (schemas, manifest, CHANGELOG, examples),
`scripts/**`, `.github/**`, README active-changes list.

## Implementation Sequence

Packet + placement skeleton → operator mint (T003, blocks T004's key block) →
wallet record finalized → attestation row finalized → gates (FR-005/006 proof)
→ PR.

## Key Technical Decisions

1. **Holder class `agent`** (operator ruling): a council body is software
   deliberation; the OXWA agent-profile exists for exactly this class. Core
   imposes composition on no class, so minting precedes 4.4 legally.
2. **Custody `holder_readable`** (ratified N13): the registry designed this
   tier for a no-key-infrastructure consumer reaching `act`; ceiling `act`,
   environment-evidence posture acknowledged in the attestation.
3. **Kindless attestation row**: no family schema exists; §4 authorizes none.
   Inventing one would be an unratified contract release. Structured YAML,
   resolved by wallet ref.
4. **Placement `governance/review-authority/`** (operator ruling): namespace
   reads cleanly for S4's floor-entry naming (tasks 5.4); outside every
   packaged `examples/` path so `repo_scan` treats the record as live.
5. **`declared_by: Brett.Heap`**: identifier grammar admits no `@`; the
   email-form anchor token is scoped to grant `issued_by` by S2's authorized
   widening and is not generalized here.
