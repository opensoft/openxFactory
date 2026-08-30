---
code_surface: openxFactory — a NEW additive `contracts/signed-execution-chain-anchoring/` family for opaque event commitments, permissioned consent-checkpoint/state-root envelopes, fixed-UTC batch manifests, retained Kaspa proof bundles, progressive multi-witness receipts, confirmation-profile records, and verification results; packaged positive and refusal fixtures; the canonical `scripts/validate-signed-execution-chain-anchoring.py`; and registration in `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, and the release digest inventory. These schemas, validators, and fixtures are CODE and release surface even though this change owns no deployable gateway, network client, node, scheduler, credential, or medical policy.
target_release: contract-v<next minor> — the next additive contract bundle, allocated and FRESH-COUNTED AT REALIZATION against `contracts/manifest.yaml` at that realization's tip per `docs/contract-versioning-policy.md`; this proposal reserves no minor number, and the current `contract-v2.3` declaration is evidence of why a remembered number cannot be carried forward.
Status: draft
---

## Why

Tranche one deliberately leaves unobserved transparency-log suffix truncation
uncovered until an external witness exists. This successor closes that declared
gap with privacy-preserving, dual-network evidence while keeping authorization
and sensitive records off public chains.

This change is explicitly gated on two predecessors named by the ratified
tranche-one packet: realization of `add-signed-execution-chain`, including its
contracts, transparency log, validator, and required-check evidence; and a real
PKI plane with durable `trust-anchor`-conformant issuance, verification,
revocation, and chain-custody evidence. Creating or seeding an OpenXPKI install
repository does not by itself prove that the PKI plane is real.

## What Changes

- Add a neutral anchoring contract family for opaque evidence leaves,
  checkpoints, asynchronous witness state, retained proofs, progressive
  receipts, and reference-verifier results.
- Keep provider-neutral off-chain policy gateways as the enforcement point.
  Public witnesses attest to committed bytes and timing; they do not authorize
  provider access or prove truth, consent, retention, or deletion.
- Restore the neutral governed permissioned consent-plane seam: consent and
  policy state remain off chain, while signed consent checkpoints and keyed
  commitments to their state roots enter the same witness lifecycle without
  carrying medical semantics.
- Make direct Kaspa L1 opaque keyed commitments the primary operational witness,
  with `anchor_pending`, distinct submitted and confirmed states, durable retry,
  and proof retention sufficient for verification after Kaspa pruning.
- Include every accepted event in one complete fixed-UTC 24-hour
  OpenTimestamps/Bitcoin durability batch. A window with no events still emits
  an empty continuity checkpoint, and Bitcoin durability is not confirmed until
  the timestamp proof is upgraded to confirmed Bitcoin evidence.
- Refuse public-chain material containing PHI, encrypted PHI, a plain hash, or a
  stable public identifier. Public artifacts carry only opaque, high-entropy
  keyed commitments and non-identifying continuity metadata.
- Give Toccata no production role in v1 beyond isolated experiments, and keep
  Kasplex and Igra out of v1. This change writes no future adoption trigger: any
  future governed change decides contract-code use on then-current merits and
  evidence.
- Hand the governed change to exactly one Speckit feature. That feature may
  realize openxFactory-owned contracts, examples, and reference validators, but
  not a deployable anchoring runtime, provider credentials, network operations,
  or medical policy.

## Capabilities

### New Capabilities

- `signed-execution-chain-anchoring`: Provider-neutral, privacy-preserving
  checkpoint anchoring and progressive dual-witness receipts for the realized
  signed execution chain.

### Modified Capabilities

None.

## Impact

- Adds a new neutral contract and reference-validation surface, including
  positive and refusal examples, to a future additive contract-bundle release.
- Depends on realized tranche-one signed-execution-chain artifacts and their
  append-only transparency log, plus realized PKI-plane evidence under the
  `trust-anchor` contracts; this proposal realizes neither dependency.
- Introduces reference semantics for direct Kaspa L1 witnessing and complete
  fixed-UTC daily OpenTimestamps/Bitcoin durability proofs without assigning
  network clients, nodes, credentials, schedulers, retries, archival operations,
  or monitoring to this repository.
- Domain and product repositories remain owners of event meaning,
  authorization, consent, provider access, and any medical or financial policy.
