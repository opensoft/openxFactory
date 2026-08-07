---
code_surface: openxFactory (neutral contracts + schemas under contracts/, a validator under scripts/; no runtime)
target_release: implementation_pending
---

# Proposal: add-agent-wallet-identity

## Why

An agent cannot currently prove which agent it is.

Every agent act reaches an external platform through ONE shared service
credential. LedgerxFactory measured this on 2026-08-06: the agent that
created purchase invoice `LXRP0002` and the agent that posted it are the
same `userSecurityId` as far as Business Central is concerned. There is
nothing for the platform to compare, so segregation of duties is not a
control anyone is declining to enforce — it is a property the platform
cannot see.

That mattered the moment posting became agent-executed. The poster
identity gained real posting rights the same day, which the product
requires (an agent that cannot post cannot do the work), and the
platform's own refusal went with them. LedgerxFactory's estate record now
records that "agents never post" holds by POLICY rather than by platform
enforcement — one lock where there were two. The control Brett proposed to
earn the second lock back is segregation of duties: refuse a post when the
requesting agent is the agent that created the transaction. It needs a
per-agent identity that can be verified, and no such thing exists.

This is also the generalization of a rule the stack already practices on
outputs. When the document-cataloger's prompt contract went v1→v3, every
prior classification was invalidated: a judgment by prompt-v1 is not the
same classifier's judgment. The same reasoning applies to AUTHORITY, and
nothing enforces it — an agent's permission to act survives a change that
makes it a different agent.

## What Changes

- **ADD a neutral `agent-wallet-identity` capability** with four elements:
  an agent identity record (DID, key reference, declared composition,
  lifecycle state); a proof-of-control rule (an asserted identifier is
  never identity — a request claiming an agent must carry a verifiable
  signature); authority binding expressed against the EXISTING neutral job
  envelope `approval_policy` vocabulary rather than a new one; and
  declared-change decertification (a composition change ends authority
  immediately).
- **Declare the key-custody model per identity**, from a closed set, and
  bind the authority an identity may hold to what its custody model can
  actually prove. A host-held key and a hardware-backed key do not prove
  the same thing and the contract SHALL NOT pretend they do.
- **No runtime, no wallet infrastructure, no key material.** Contracts,
  schemas, and a validator. Issuance mechanics, wallet storage, and
  signing services are realizations for consuming installs.

Deliberately NOT in this change, each a named successor gated on a
consumer: certification batteries and measured drift; qualification levels
and autonomous-authority tiers; delegation chains; patient and
practitioner wallets.

## Impact

- New neutral capability composing with `roles-authority-model` (who may
  act) and `credential-contracts` (how access is brokered); reuses the
  neutral job envelope's `approval_policy` values as the authority
  vocabulary.
- First consumer is LedgerxFactory's posting segregation-of-duties control
  (`ledgerx:staging:posting-segregation-of-duties`), which cannot be built
  until this lands.
- Omnigent readiness heartbeats already attest `worker_version`,
  `profile_versions` and `policy_version` — the facts a composition hash
  consumes. Extending that attestation is a named successor in
  omnigent-install, not part of this change.
- **Two ratified MedxFactory specs constrain this and are respected rather
  than amended**: `patient-identity-and-assembly` (a wallet address MUST
  NOT be silently accepted as identity proof) and
  `patient-snapshot-ledger-custody` (custody stays topology and wallet
  neutral; wallet references MUST NOT become an identifier or a
  prerequisite for basic reconstruction). This capability is an AUTHORITY
  control, never an identity substrate, and no domain is required to adopt
  it to operate.
- No existing capability is modified. No secret, key, or credential is
  created by this change.

## Decisions this ratification must carry

Two questions are load-bearing enough that ratifying without answering
them would be ratifying a shape nobody chose. Both are recorded in the
staging fragment; recommendations are stated so a ruling is a yes or a
correction rather than an essay.

1. **Does the neutral contract REQUIRE proof of control, or admit an
   asserted identity as an interim?** An asserted wallet id still defeats
   the common failure — a bug or a loop doing both halves of a transaction
   — and would let the first consumer ship sooner.
   **Recommendation: require proof.** An asserted identity is a comment
   doing a rule's work, which is the shape LedgerxFactory's
   `modify-ledgerx-credential-contracts-for-test-asset-authority` was
   ratified to end. A domain needing an interim records a dated exception
   in its own records rather than the neutral rule being softened.

2. **Does the contract mandate a key-custody model, or declare it?**
   Mandating hardware backing would be safest and would stall every
   consumer; saying nothing would let a host-held key masquerade as proof
   of agent action.
   **Recommendation: declare it, and bind authority to it.** The identity
   record carries its custody model from a closed set, the contract states
   what each model proves, and the authority an identity may hold is
   capped by its custody. That is honest about the trust model instead of
   hiding it, and it lets a consumer start at a low tier without the
   contract lying about what its signature means.
