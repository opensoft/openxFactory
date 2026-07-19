code_surface: none
target_release: implemented

## Why

The credential access model's core rule — no repo stores raw credentials —
predates GitOps secret management. Flux-managed environments want the git
repository to be the single reconciled source of truth, including for
secrets, which is only possible if an encrypted representation of a secret
is *not* a raw credential. The xFactory QA environment adopted exactly this
pattern on 2026-07-19 (SOPS + age, one durable key in 1Password, design at
`omnigent-install docs/sops-secret-management-design.md`), and Brett ratified
the enabling ruling the same day. The ruling was initially recorded as a
direct edit to `docs/credential-access-model.md` (PR #34) — but ratification
is conferred by an OpenSpec change under the document lifecycle, and the
omnigent-install change record (its Amendment 3) already cites this ruling
as ratified. This change is that missing durable record.

## What Changes

- `credential-contracts` gains an ADDED requirement defining when SOPS
  ciphertext is not a raw credential and when SOPS plus an externally
  custodied decryption identity is an approved secret-provider pattern:
  ciphertext-only repositories, externally custodied private identities,
  per-environment recipients, pre-commit plaintext rejection,
  controller-compromise blast-radius accounting, and mandatory
  identity-plus-credential rotation on exposure (historical git ciphertext
  remains recoverable).
- `docs/credential-access-model.md` §1.1 carries the ruling prose and now
  cites this change as its ratification record.
- First approved realization: xFactory QA (omnigent-install
  `feat/qa-sops-secret-management`, Amendment 3 of
  `add-qa-subscription-environment`) — one QA-wide age identity, durable
  private copy only in 1Password, replaceable runtime projection
  `flux-system/sops-age`.

## Impact

- Affected specs: `credential-contracts` (ADDED requirement).
- Affected docs: `docs/credential-access-model.md` (§1.1 recorded-by
  citation; ruling prose already on this branch), `README.md` (OpenSpec
  Records entry).
- Doc-only in this repository (`code_surface: none`); the QA runtime
  realization is governed by omnigent-install's own change record. Archives
  on landing.
- Non-goals: no change to the five credential contract record kinds or
  their schema; no retroactive blessing of base64 or ad hoc encryption —
  those remain raw credentials.
