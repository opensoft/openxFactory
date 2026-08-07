---
code_surface: openxFactory (neutral contracts + schemas under contracts/, a validator under scripts/; no runtime, no key material)
target_release: implementation_pending
---

# Proposal: add-openxwallet

## Why

Two domains need wallets and neither has one, which is the moment to
define one view rather than the moment after two have diverged.

**LedgerxFactory** needs an agent to prove which agent it is. Every agent
act reaches an external platform through ONE shared service credential —
measured 2026-08-06, when the agent that created purchase invoice
`LXRP0002` and the agent that posted it turned out to be the same
`userSecurityId`. Segregation of duties is therefore not a control anyone
is declining to enforce; it is a property the platform cannot see. That
became load-bearing the same day, when posting went agent-executed and the
platform's own refusal went with it.

**MedxFactory** has already ruled on the shape from the other side. Its
promoted `patient-identity-and-assembly` states a wallet address MUST NOT
be silently accepted as identity proof, and `patient-snapshot-ledger-custody`
requires custody to stay wallet-neutral and reconstructable with no wallet
available. Those are ratified constraints about wallets, not a wallet.

The intersection is already named and designed. `openxWallet` was named
2026-07-16 as the neutral identity/authorization capability — patient,
practitioner and agent wallets — with `openxVault` as its custody sibling
whose gate CONSUMES wallet grants. The vault brainstorm articulates the
model most fully, and it is subject-class agnostic: a wallet is a
device-bound signing key anchored to a DID; raw keys are never handed out,
because a raw key can be neither expired nor revoked; access travels as
attenuated capability grants; both ends of a grant are wallet-held keys, so
a stolen grant is useless without proof of possession; every use is
key-attributed.

## What Changes

- **ADD the neutral `openxwallet` capability** — the core, holder-class
  agnostic: a wallet as a key reference with a declared custody model
  (never key material); authority carried by ATTENUATED CAPABILITY GRANTS
  rather than by key access; exercise requiring proof of possession rather
  than presentation; custody declared and capping what a signature
  evidences; key-attributed audit; revocation propagating through
  derivation; distinct-holder constraints expressible so segregation of
  duties lives in the grant model instead of being reimplemented per
  domain; and the non-substrate rule that keeps wallets optional for every
  domain.
- **ADD `openxwallet-agent-profile`** — the first profile, carrying only
  what is agent-specific: the declared composition and its component set,
  declared-change revocation, and agent authority expressed as GRANT SCOPE
  admitting the job envelope's `approval_policy` values.
- **No runtime, no wallet infrastructure, no key material, no issuance
  service.** Contracts, schemas, and a validator.

The core/profile split is the substance of this proposal. Patient and
practitioner profiles are named successors, each gated on a consumer, and
each a NEW capability over the same core rather than a modification of it —
so the seam is structural rather than a promise.

Also deliberately deferred, each gated on a consumer: certification
batteries and measured drift; qualification levels and autonomous-authority
tiers; delegation-chain policy beyond the core's monotonic attenuation.

## Impact

- Two new neutral capabilities; no existing capability is modified.
- Composes with `roles-authority-model` (who may act) and
  `credential-contracts` (how access is brokered); reuses the neutral job
  envelope's `approval_policy` values as grant-scope terms.
- `openxVault`, when it lands, consumes these grants — the boundary Brett
  recorded 2026-07-16 is preserved rather than re-litigated.
- First consumer is LedgerxFactory's posting segregation-of-duties control
  (`ledgerx:staging:posting-segregation-of-duties`), which cannot be built
  until this lands and which needs the core's distinct-holder constraint
  plus the agent profile.
- Omnigent readiness heartbeats already attest `worker_version`,
  `profile_versions` and `policy_version` — the facts a composition hash
  consumes. Extending that attestation is a named successor in
  omnigent-install, not part of this change.
- MedxFactory's two ratified constraints are adopted as a core requirement
  rather than worked around. No domain is obliged to adopt wallets.

## Decisions carried into this proposal

**Grants are the primitive** (Brett, 2026-08-06). An earlier draft bound
authority to `approval_policy` values directly, which would have produced
two authority models under one name: coarse enumerated postures here, and
the vault brainstorm's attenuated, delegable, revocable grants there. One
mechanism wins, and it is grants — `approval_policy` survives as a legal
scope vocabulary, so nothing is discarded and the job envelope still
composes.

**The core is holder-class agnostic** (Brett, 2026-08-06). The earlier
draft was a wallet shaped like an agent, which would have baked
composition hashing into the neutral layer where it is meaningless for a
patient. The core now knows only holders, keys, custody and grants.

## Decision still open for the ratification gate

**Does the contract mandate a key-custody model, or declare it?**
Mandating hardware backing is safest and stalls every consumer — there is
no key infrastructure in the stack today. Saying nothing lets a key
readable by the holder's own execution context masquerade as proof the
holder acted, which is worse than no control, because the audit record
would assert something false.

**Recommendation: declare it, and cap authority by it.** The wallet
carries its custody model from a closed set, the contract states what each
model evidences, and the authority a wallet may hold is bounded by its
custody. A consumer can start at a low tier without the contract lying
about what its signature means, and raising authority becomes a custody
question rather than a trust assertion — the same move as the
`package_content_execution_mode` field LedgerxFactory ratified in August.
