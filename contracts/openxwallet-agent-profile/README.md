# openxWallet Agent Profile Contract Family

Status: ratified
Ratified by: add-openxwallet (approved Brett Heap 2026-08-07; registered in
`contracts/manifest.yaml` + `contracts/CHANGELOG.md` at `contract-v1.31`,
per [Contract Versioning Policy](../../docs/contract-versioning-policy.md))
Kind: reference
Repository context: openxFactory owns the neutral capability; the first
consumer is LedgerxFactory's posting segregation-of-duties control

The **first profile** over the holder-agnostic core in
[`contracts/openxwallet/`](../openxwallet/README.md), carrying only what is
agent-specific.

It is a NEW capability over that core rather than a modification of it, which
is why it lives in its own family directory. Patient and practitioner profiles
are named successors and arrive the same way, each gated on a consumer of its
own. That seam is the substance of the change this realizes: an earlier draft
was a wallet shaped like an agent, and it would have forced every future
profile to explain why it ignores half the contract.

## What is agent-specific

**An agent is its composition.** A holder of class `agent` declares the
composition that constitutes its identity as a hash over a DECLARED COMPONENT
SET — and the set is part of the declaration, so a reader can tell what a
matching hash was actually asserting. A hash without its component set is a
validation failure: it asserts agreement about something it refuses to name.

**A declared change revokes immediately.** Any change to the declared
composition ends that agent's certified identity, and its outstanding grants
are revoked at once through the core's revocation-propagation rule — no
tolerance band, no grace period, no threshold consulted. Resuming requires
re-issuance against the changed composition. This generalizes to AUTHORITY an
invalidation the family already applies to OUTPUTS: a prompt-contract version
bump invalidated every prior classification, because a judgment by prompt-v1
is not the same classifier's judgment.

**Authority is grant scope, not a second vocabulary.** What an agent may do is
the SCOPE of a grant it holds, and approval terms come from the neutral job
envelope's `approval_policy` properties. The validator reads that property set
out of `contracts/schemas/hermes-job-envelope.schema.yaml` at run time rather
than restating it, because restating it would recreate the parallel vocabulary
the requirement exists to forbid.

## What the component set covers — the decision this feature settled

The change ratified on 2026-08-07 required the component set to be DECLARED
and deliberately left WHAT IT COVERS to the implementing feature. The tension
was real in both directions: including a fast-changing retrieval corpus fires
revocation constantly and gets routed around, while excluding it lets an
agent's behaviour change without its identity changing.

The resolution is that "the corpus" is two things, not one. Every declared
component carries a **binding mode**:

| binding mode | what enters the hash | used for |
|---|---|---|
| `content` | the component's own digest | model version, prompt contract, tool manifest, policy version, parameters |
| `reference` | the component's identity and its GOVERNING CONFIGURATION | retrieval corpora |

So the hash covers WHICH corpus, WHAT may be retrieved from it, and UNDER WHAT
RULES it is consulted. Swapping the corpus, widening the retrieval scope, or
changing the selection or admission configuration all change identity and
revoke. Documents arriving in an already-governed corpus do not — the agent's
AUTHORITY has not changed, and the corpus has its own governance; borrowing
this mechanism to police it would be the wrong control in the wrong place.

This is not "exclude the corpus with extra words". The excluded thing is
narrow and named: row-level contents of a corpus whose identity and governing
configuration ARE covered. An agent cannot change what it may retrieve, or
from where, without changing its identity.

Both binding modes stay available for every component, so a domain wanting
content binding on a slow-moving corpus may declare it. The contract makes the
choice visible and checkable; it does not make it for anyone.

## The record kind

| Kind | Purpose |
|---|---|
| `xfactory_wallet_agent_composition` | The composition hash, the component set it covers with each component's binding mode, the attested hash, and the grants state that follows from comparing them. |

A record of this kind must resolve to a wallet whose holder class is `agent` —
a composition naming a wallet that does not resolve is refused rather than
passed over, because an unresolvable wallet is a class check that never runs.
The core imposes composition on no class, and a holder of another class is
required to declare none.

## What this family deliberately does not do

No certification batteries, measured drift, or qualification tiers. Declared-
change revocation is a hash comparison over facts Omnigent readiness
heartbeats already attest — `worker_version`, `profile_versions`,
`policy_version` — and catches the common case: somebody edited a prompt, a
policy, or a tool manifest. Measured drift catches a hosted model changing
beneath a pinned identifier, which is real but rarer and needs statistics
nobody has settled. Extending the heartbeat attestation is a named successor
in omnigent-install, not part of this change.

It also does not decide whether two agents are sufficiently INDEPENDENT for
segregation of duties. Two agents from the same model, orchestrator and prompt
are not independent the way two humans are. The composition hash gives an
objective floor — different hash, different holder — and whether that floor
suffices is left to the consuming domain, which is why the core's constraint
declares its `distinctness_floor` rather than fixing one.

## Validation

Covered by the core family's validator, which loads both families:

```sh
python3 scripts/validate-openxwallet.py
```
