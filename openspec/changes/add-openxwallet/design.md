# Design: add-openxwallet

## Context

Organized from the `agent-certification-wallets` and
`git-native-record-vault` brainstorms (Brett, 2026-07-15/16) via the
staging topic `openxFactory:staging:agent-wallet-identity`, and
restructured on 2026-08-06 after Brett asked the question that exposed the
first draft's flaw: with both Medx and Ledgerx heading for wallets, is the
intersection in openxFactory?

It was not. The first draft defined `agent-wallet-identity` — a wallet
shaped like an agent. This draft defines a holder-agnostic core with the
agent as its first profile.

## Why the first draft was wrong

Two specific faults, both cheap to fix before ratification and expensive
after.

**It baked agent concepts into the neutral layer.** Composition hashing
and declared-change decertification are meaningful for an agent and
meaningless for a patient — a patient has no model version. A core
carrying them would have forced every future profile to explain why it
ignores half the contract.

**It expressed authority twice.** The draft bound authority to
`approval_policy` values: coarse, enumerated, not delegable. The vault
brainstorm binds it to attenuated capability grants with proof of
possession: fine-grained, delegable, revocable, and already the thing
`openxVault`'s gate is designed to consume. Landing both would have put
two authority models under one name — the precise outcome the question was
asked to avoid.

## Grants as the primitive

The decision (Brett, 2026-08-06) is that grants win, and `approval_policy`
survives as a legal scope vocabulary rather than a parallel mechanism. Four
properties follow, and each is a requirement rather than an aspiration:

**Raw keys are never the unit of access.** A raw key cannot expire and
cannot be revoked, and a shared key destroys attribution. This is the
vault brainstorm's cardinal rule, lifted verbatim into the core.

**Attenuation is monotonic.** A derived grant may narrow scope or lifetime
and may never widen either. Without this, delegation is just key-sharing
with extra steps.

**Possession, not presentation.** Exercising a grant requires a signature
from the holder's key, so a stolen grant is inert. This is what makes the
control survive a leaked token, which a bearer model does not.

**Revocation propagates and is checked at exercise.** Revoking a parent
kills its derivations; revoking a holder kills its grants. Checking only
at issuance would make revocation advisory.

## Segregation of duties belongs in the core

The Ledgerx consumer needs "the agent that created the transaction may not
post it". That is not an agent property — it is maker-checker, and it
applies equally to practitioners. So the core carries a DISTINCT-HOLDER
CONSTRAINT that a consuming capability may declare between two named acts,
and the agent profile inherits it rather than restating it.

It is opt-in by construction. A capability that declares no constraint is
not subject to one, because a silent default here would make every
two-step flow in the family suddenly require two actors.

## The custody question, and why it is still open

Three options were weighed and only one is recommended.

**Mandate hardware backing.** Safest, and it stalls every consumer
indefinitely — there is no key infrastructure in the stack today.

**Say nothing.** Lets a key readable by the holder's own execution context
masquerade as proof the holder acted. Worse than having no control,
because the audit record would assert something false.

**Declare it and cap authority by it** (recommended). The wallet carries
its custody model; the contract states what each model evidences; the
authority a wallet may hold is bounded by its custody. Honest about the
trust model instead of hiding it, and it lets a consumer start low without
the contract lying. The same move as `package_content_execution_mode`:
record the mode, let consumers read it, refuse claims the mode cannot
support.

## What this deliberately does not do

- No wallet infrastructure, issuance service, key storage, or signing
  implementation. Contracts and schemas only.
- No modification to any existing capability.
- No obligation on any domain: the non-substrate requirement adopts
  MedxFactory's two ratified constraints rather than working around them,
  so a domain must remain able to operate, reconstruct records and resolve
  subjects with no wallet present.
- No certification batteries, measured drift, or qualification tiers.
  Declared-change revocation is a hash comparison over facts Omnigent
  heartbeats already attest and catches the common case — somebody edited
  a prompt, a policy, or a tool manifest. Measured drift catches a hosted
  model changing beneath a pinned identifier, which is real but rarer and
  needs statistics nobody has settled.

## Risks

**The distinctness assumption.** Segregation of duties assumes independent
actors. Two agents from the same model, orchestrator and prompt are not
independent the way two humans are; the constraint defends against slips
and loops, not against a wrong policy applied consistently by both. The
composition hash gives an objective floor — different hash, different
holder — and whether that floor suffices is left to the consuming domain.

**Revocation noise.** If a composition hash covers a retrieval corpus that
changes hourly, revocation fires constantly and gets routed around. What
the component set covers must be settled before the schema is authored,
which is why the profile requires the set to be declared alongside the
hash rather than assumed.

**A control that proves less than it appears to.** Custody declaration is
what keeps this honest, and it works only if consumers declare truthfully.
A validator can check that a model is declared and that authority does not
exceed it; it cannot check that the declared model is the real one.
