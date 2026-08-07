# Staged: openxWallet — agent identity with proof of control

Status: staged
Kind: capability-proposal
Summary: Give every agent a wallet (DID + signing key) so that an agent can
PROVE which agent it is when it asks to do something irreversible, and so
that authority can be bound to a specific, stable agent identity rather
than to whichever service credential happened to carry the call. Organized
2026-08-06 from the `agent-certification-wallets` brainstorm (Brett,
2026-07-15/16) at the point a concrete consumer named itself: LedgerxFactory
needs to refuse a ledger post when the agent requesting it is the same agent
that created the transaction, and today the platform cannot tell them apart
because every agent reaches Business Central through one application user.
Scoped deliberately BELOW the brainstorm: identity and proof first,
certification levels and drift-triggered recertification sequenced after.
Topics: openxwallet, agent-identity, did, proof-of-control, verifiable-credentials, segregation-of-duties, authority-binding, decertification
Repository context: openxFactory owns the neutral capability; the first consumer is LedgerxFactory (`ledgerx:staging:posting-segregation-of-duties`), enforced in the LedgerLinc BC extension; omnigent-install already attests the version facts a config hash would need
Staging ID: `openxFactory:staging:agent-wallet-identity`
Source: `ideation/brainstorm/agent-certification-wallets.md` (Brett, 2026-07-15/16, naming decided 2026-07-16) + the LedgerxFactory session of 2026-08-06 that made posting agent-executed and then asked for the control back
Target capabilities: ADDED neutral `agent-wallet-identity` (agent DID record, proof-of-control verification rule, authority binding); composes with `roles-authority-model`, `credential-contracts`, and the neutral job envelope's `approval_policy`; MODIFIED `omnigent-domain-overlay` only if the config-hash attestation lands in the same wave

## Why this is staged now

A brainstorm is promoted by a consumer, not by enthusiasm. This one has
been sitting since 2026-07-15 with nothing forcing it. On 2026-08-06 that
changed:

LedgerxFactory's poster identity gained real posting rights, which the
product requires — an agent that cannot post cannot do the work. What went
with it was Business Central's own refusal, so "agents never post" now
holds by policy rather than platform enforcement. Brett's answer was
segregation of duties: the posting API carries the wallet of the agent
asking to post, checks an explicit permission against it, and refuses when
that wallet is the one that created the transaction.

That control cannot be built today, and the reason is precisely this
capability's absence: **every agent act reaches the platform through one
shared credential**, so there is no per-agent identity to compare. The
wallet is the enabling primitive, not a nicety.

## The scope decision (the substance of this fragment)

The brainstorm covers wallets, verifiable credentials, qualification
levels, autonomous-authority scope, delegation chains, drift-triggered
recertification, and certification batteries. Proposing that as one change
would be a mistake — it is at least three capabilities, and the battery
design alone carries unresolved statistical questions.

**First exit carries only what a consumer can use:**

1. An **agent identity record** — DID, signing key reference, the agent's
   declared composition (model version, prompt contract, tool manifest,
   policy version, parameters), and lifecycle state.
2. A **proof-of-control rule** — a request asserting an agent identity is
   accepted only with a verifiable signature over that request. A claimed
   identifier is never identity.
3. **Authority binding** — what this agent may do, expressed against the
   existing `approval_policy` vocabulary rather than a new one.
4. **Declared-change decertification** — any change to the composition
   hash ends the identity's authority immediately. This is cheap: it is a
   hash comparison against facts Omnigent readiness heartbeats already
   attest (`worker_version`, `profile_versions`, `policy_version`).

**Deferred to later waves, deliberately:**

- **Measured drift and certification batteries.** Expensive and
  statistically unresolved (band calibration, battery authorship, whether
  batteries are themselves versioned artifacts). The declared-change
  trigger above catches the common case — a config edit — at almost no
  cost. Measured drift catches the provider silently changing a pinned
  model, which is real but rarer and can follow.
- **Qualification levels and autonomous-authority tiers.** These need the
  battery to mean anything.
- **Delegation chains.** Wanted, but no consumer has named itself.
- **Patient and practitioner wallets.** Same primitive, different subject,
  and constrained differently (see below). Not in this wave.

## Claims

1. **Proof of control, never a claimed identifier.** This domain has
   already ruled on the weaker form. MedxFactory's promoted
   `patient-identity-and-assembly` states that "demographic similarity,
   repository address and wallet address MUST NOT be silently accepted as
   identity proof". If a wallet address cannot prove a patient's identity,
   it cannot prove an agent's authority over an irreversible ledger post.
   The capability's load-bearing requirement is therefore verification, not
   registration.

2. **The capability must never become a prerequisite for basic operation.**
   MedxFactory's promoted `patient-snapshot-ledger-custody` requires
   custody to remain "topology and wallet neutral" and forbids wallet,
   signature and attestation references from becoming the patient
   identifier or a prerequisite for basic reconstruction. A neutral wallet
   capability that quietly becomes load-bearing for record reconstruction
   would contradict a ratified spec. It must be composable where a domain
   wants it and absent where a domain does not — an authority control, not
   an identity substrate.

3. **Authority dies with the identity.** An agent is its composition. If
   the composition changes, the certified agent no longer exists and its
   authority ends instantly — no percentage, no grace. The precedent is
   already in the stack: the document-cataloger's prompt-contract version
   bump invalidated every prior classification, because a judgment by
   prompt-v1 is not the same classifier's judgment. This generalizes that
   from an agent's OUTPUTS to its AUTHORITY.

4. **Signing composes with what already exists.** Agents already mark
   their work with a `Co-Authored-By` trailer, which is an assertion.
   Wallet signing upgrades that to evidence without inventing a parallel
   mechanism, and agent access to time-boxed capability grants rides the
   same broker machinery practitioners use.

## Open questions

1. **Where does the key live, and who holds custody?** A signing key that
   an agent can read is a signing key an agent can exfiltrate. Passkey /
   HSM / vault-held with a signing service are different trust models with
   different failure modes, and this is the hardest question in the
   fragment — it determines whether the signature proves the AGENT acted
   or merely that the HOST did.
2. **Does the first exit require signing, or admit an asserted identity
   as an explicit interim?** An asserted wallet still defeats the common
   failure (a bug or loop doing both halves of a transaction) and could
   ship far sooner. But `modify-ledgerx-credential-contracts-for-test-asset-authority`
   was ratified in part to end "a comment doing a rule's work", and an
   asserted identity is that shape. Recommend: the contract requires
   proof, and any interim is a recorded, dated exception in the consuming
   domain rather than a softening of the neutral rule.
3. **What is the composition hash over, exactly?** The brainstorm names
   model version + prompt contract + tool manifest + policy version +
   parameters + retrieval corpus. Retrieval corpora change constantly;
   including them may make decertification fire so often it is ignored,
   and excluding them may let an agent's behaviour change without its
   identity changing.
4. **Who issues, and is issuance always a human gate?** The brainstorm
   asks whether a sufficiently-certified certifier agent may issue lower
   certs. For the first exit, human issuance is the safe default, but it
   should be stated rather than assumed.
5. **Where does the registry live?** Per tenant, per estate, or neutral
   and central? The LedgerxFactory consumer wants the permission decision
   readable in the CLIENT's own system (a BC-side registry) so an auditor
   finds it where they would look — which argues for a neutral contract
   with domain-local projections rather than one central store.
6. **What makes two agents sufficiently distinct?** Segregation of duties
   assumes independence. Two agents from the same model, same orchestrator
   and same prompt are not independent the way two humans are. Does the
   contract define a distinctness floor — different composition hash is
   the obvious candidate — or leave it to the consuming domain?

## Exit path

One ADDED neutral capability carrying the four first-exit elements above,
composing with `roles-authority-model` and `credential-contracts` and
reusing the job envelope's `approval_policy` vocabulary for authority
scope. Certification levels, batteries, measured drift and delegation
chains are named successors, each gated on a consumer.

Gated on: open question 1 (key custody), which decides what a signature
actually proves, and open question 2 (proof-required versus asserted
interim), which decides whether the first LedgerxFactory consumer can ship
against it or must wait. The brainstorm remains in place as provenance and
carries the deferred material.
