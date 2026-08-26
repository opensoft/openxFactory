# Tasks: The First Wallet (wallet arc cold start)

**Feature**: 013-first-wallet | **Branch**: `013-first-wallet` | **Date**: 2026-08-24
**Input**: [spec.md](./spec.md) · [plan.md](./plan.md) · [research.md](./research.md) · [data-model.md](./data-model.md) · [quickstart.md](./quickstart.md)

Scope guard (ratified tasks §4): ONE wallet record, ONE kindless attestation
row, same-tree residency. NO grant, NO register, NO schema/manifest/CHANGELOG
bundle movement. Composition stays task 4.4 (codexFactory).

## Phase 1 — Grounding & packet

- [x] T001 Substrate research: §4 scope, day-one order, N7 residency, N13
      custody intent, unattested-custody cap, scanner mechanics, identifier
      grammars, schema requirements — verified against `origin/main`
      (`d95623ea`); recorded in research.md.
- [x] T002 Operator rulings recorded (key minting route, holder_class agent,
      drafted attestation, placement) — implementation-notes.md.
- [x] T003 Feature packet authored: spec / plan / research / data-model /
      quickstart / checklist / implementation-notes.

## Phase 2 — Live artifacts

- [x] T004 **[OPERATOR]** Mint ed25519 keypair operator-side; paste the raw
      public key only (hex). Blocks T005's key block. DISCHARGED 2026-08-24:
      Brett Heap supplied `7f51371…c24ab` (32 bytes); did:key derived from the
      public bytes only.
- [x] T005 Write `governance/review-authority/wallets/wal-agent-mrc-0001.yaml`
      — full record per data-model.md; did + multibase from T004; timestamps
      stamped at finalization.
- [x] T006 Write `governance/review-authority/attestations/custody-attest-wal-agent-mrc-0001.yaml`
      — kindless row per data-model.md; verifier confirms the drafted content.

## Phase 3 — Gates

- [x] T007x Gates: whole-checkout sweep exit 0 with the live record counted
      (FR-006/SC-001); packaged corpus unchanged at S2 baseline 17/36 across
      13/13 (SC-002); `pytest tests/wallet_yaml_syntax_gate/ -q`;
      `openspec validate --all --strict`; boundary proofs — contracts/scripts/
      .github diff empty and zero private material in the branch diff
      (SC-003). Evidence recorded in implementation-notes.md.
      ALL GREEN 2026-08-24 (see implementation-notes).

## Dependencies

T001–T003 (done) → T004 → T005 → T006 → T007x.
T006 needs the wallet ref fixed by T005's filename; both need placement dirs.

## Implementation strategy

Single cold-start act, no code path changes: placement skeleton → operator
mint → record → attestation → gates. Every committed tree stays green; the
PENDING did placeholder never reaches a commit.
