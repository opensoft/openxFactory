---
code_surface: openxFactory (a NEW `governance/factory-identity/` register family — `register.yaml` plus `wallets/`, `grants/`, and `attestations/` records mirroring the review-authority intake register's four-file shape and its deliberately-kindless register discipline — and the register-reader invocation that reads it inside the REQUIRED `wallet-validation` check; plus, if the manifest is schema'd here rather than referenced, a `contracts/clearing-boundary/` sealed-bounded-request manifest schema with packaged positive and negative examples and its canonical validator, registered in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive bundle cut). The xFactory clearing workflow, the codexFactory hosted packaging and sign-on-return workflows, the retirement of codexFactory's worker jobs, and every execution-group authorization edit are successor realization changes named in the impact map, NOT this change's surface.
target_release: next additive contract bundle (allocated at realization per `docs/contract-versioning-policy.md`; no minor is reserved here)
Status: draft
Proposed: 2026-09-01
Origin: Operator ruling, Brett Heap, 2026-09-01, recorded in the operator workspace as `cpc-clearing-boundary-ruling-2026-09-01.md` and on `opensoft/codexFactory` issue #156, together with its same-day extension comment on that issue (gateway confirmed; seat-return signing resolved to option (b), sign-on-return; per-factory origin keys). The ruling commissioned this contract by name as its next lane.
---

# Proposal: add-cpc-clearing-boundary

## Why

An originating factory needed work executed on shared execution hardware it
does not own. The shape that suggested itself — authorize the factory's
repository at the execution surface and let it dispatch — was refused by the
operator on 2026-09-01, and the refusal is the contract this change writes
down.

The refused shape fails on five counts, all of them neutral: the execution
estate would receive repository credentials it has no business holding; the
execution target would clone a repository it has no business reading; the set
of things that can reach the hardware would grow with every factory instead of
staying small and reviewed; a single compromised workflow in ANY authorized
factory would become arbitrary command execution on shared hardware; and there
would be no one place that holds provenance, policy, audit, throttling, and
emergency shutdown, because there would be as many places as there are
factories.

The sanctioned shape inverts it. Work crosses the boundary as a SEALED BOUNDED
REQUEST: a hosted packaging step in the originating factory seals selected
source files — no credentials, ever — under a signed manifest carrying hashes
and a source revision; a CLEARING BOUNDARY owned by the estate verifies that
manifest against the hosting platform's authoritative API rather than
believing it, records the dispatch, and selects the exact execution target;
the target receives ONLY the sealed bundle, recomputes its digest, and runs
one permitted operation with no repository and no credential in reach; and the
returned result is validated on hosted infrastructure before it may affect any
repository at all.

That contract scales to more factories without widening access to the
hardware, which is the property the refused shape could not have. It is also
domain-neutral: nothing in it is engineering-specific, and the same boundary
serves any factory that needs bounded execution in an estate it does not own.

The ruling's same-day extension added the two identity halves this change also
owns. First, per-factory ORIGIN KEYS: each factory holds one Ed25519 key whose
private half stays in its hosted environment and whose public half is
registered here, so "this request came from factory X" becomes a verifiable
claim rather than an inference from platform metadata alone. Second,
SIGN-ON-RETURN: where a result must be attested by the originating factory,
the execution target produces UNSIGNED results and the factory's own hosted
workflow signs them after verifying the sealed return — which means attestation
keys never need to enter the execution estate, no key is re-minted, and
existing key placement becomes exactly right rather than something to redo.

## What Changes

- **NEW capability `clearing-boundary`** — the neutral contract for admitting
  bounded work into an execution estate that the originating factory does not
  own:

  - **One admission point.** Cross-boundary work reaches an execution estate
    only as a sealed bounded request admitted by a clearing boundary. Broad
    standing authorization for an originating factory is refused; a narrower
    grant, if ever made, is one exact workflow path on a protected branch —
    never a repository.
  - **An enumerated manifest.** Originating repository and workflow; source
    commit revision; unique job id and expiration; selected-file manifest with
    per-file hashes; bundle digest; permitted operation; required worker
    profile; exact execution group and unique dispatch label; output schema;
    data-handling classification; origin signature. Missing any field is a
    refusal. No credential is ever a bundle member.
  - **Verification against the platform, not the bundle.** The clearing
    boundary checks provenance against the hosting platform's authoritative
    API. Bundle fields are untrusted input. Platform provenance and origin
    signature are BOTH required; neither substitutes for the other.
  - **Single-use, expiring, label-bound dispatch.** A job id clears once, an
    expired request is refused, and exactly one execution target can claim the
    dispatch under its unique label.
  - **A short-lived sealed job object, never a committed folder.** The bundle
    expires with the dispatch; the durable record is the audit record and the
    digests it names.
  - **The target receives only the bundle.** No clone, no checkout, no
    repository credential, no attestation key. The digest and every per-file
    hash are RECOMPUTED before execution, and execution is confined to the
    permitted operation.
  - **Hosted validation before any repository is touched.** The sealed return
    validates against its declared output schema, and passes the operation's
    required tests, on hosted infrastructure first.
  - **Proven workspace wipe** on every terminal state, failure and timeout
    included; a wipe that cannot be proven is a finding.
  - **Sign-on-return.** Attestation is produced on the originating factory's
    hosted infrastructure after the sealed return verifies. Attestation keys
    never enter the execution estate.
  - **Audit, throttle, shutdown in one place.** Every decision — admission and
    refusal alike — is recorded; halting the boundary halts all cross-boundary
    execution in that estate.
  - **Readiness is the lane's first operation**, not a second authorized path;
    the estate's authorization surface converges to ONE permanent entry per
    execution group.

- **NEW capability `factory-origin-identity`** — one Ed25519 origin key per
  originating factory, registered in a SIBLING register:

  - `governance/factory-identity/register.yaml`, a sibling of the
    review-authority intake register rather than an extension of it (design
    D1), reusing that family's discipline: public key references only, custody
    declared from the closed registry, authority carried by an attenuated
    grant, a declared revocation staleness bound, and a permanently human-only
    surface entered into gate floors BY NAME.
  - **Distinct acts, structurally.** Origin attestation and review or seat
    attestation are different acts on different keys in different registers. A
    key registered for one is REFUSED for the other, and a reader for one act
    cannot resolve identities from the other's register.
  - **Custody in the factory's hosted environment**, declared and attested;
    undeclared custody caps authority exactly as it does for review wallets.
  - **Revocation under the ratified wallet lifecycle**, re-checked AT CLEARING
    rather than trusted from an admission stamp; a stale, unreadable, or
    absent projection refuses rather than proceeds.

- **NOT in this change**: the xFactory clearing workflow, the codexFactory
  hosted packaging and sign-on-return workflows, the retirement of
  codexFactory's worker jobs, and every execution-group authorization edit —
  each is a named dependent realization in the impact map and in `tasks.md`.
  No key is minted here, no register row is issued here, and no workflow is
  written here.

## Capabilities

### New Capabilities

- `clearing-boundary`: the neutral contract for the sealed bounded request —
  its manifest, its verification against platform truth, its single-use
  dispatch, its short-lived carrier, the execution target's isolation and
  digest recomputation, hosted output validation, proven workspace wipe,
  sign-on-return attestation, audited decisions with one shutdown point, and
  readiness as the lane's first operation.
- `factory-origin-identity`: the neutral contract for per-factory origin keys
  — one registered Ed25519 identity per originating factory in a sibling
  register, hosted-environment custody, act distinctness from review and seat
  attestation, revocation under the ratified lifecycle re-checked at clearing,
  and a permanently human-only register surface.

## Impact

- **New contract surface (this change)**: the `governance/factory-identity/`
  register family and its reader invocation; the sealed-bounded-request
  manifest schema if OQ2 resolves to schema-it-here. No workflow, no key, no
  row, no deployment.
- **Affected existing capabilities**: `credential-contracts` (the bundle
  carries no credential, and the clearing dispatch credential is dispatch-only
  by that capability's existing rule); `roles-authority-model` (the human-only
  register surface and its accountable issuer); `neutral-job-envelope` (OQ2 —
  whether it carries or merely references the bundle manifest);
  `review-authority-intake` (the sibling relationship and the act-distinctness
  refusal, which that register's reader must also honour in the other
  direction).
- **Dependent realizations** (named here, authored in their own repositories):
  1. **xFactory** — the clearing workflow: verify manifest against the
     platform API, record the dispatch, select execution group and unique
     label, expose readiness as the lane's first operation, and become the ONE
     permanent authorization entry per execution group as the standalone
     readiness diagnostic from xFactory PR #188 retires into it.
  2. **codexFactory** — the hosted packaging workflow that seals bounded
     requests and signs their manifests with the factory origin key, and the
     sign-on-return workflow that verifies the sealed return's provenance and
     digest and then signs seat results where the seat signing keys already
     live.
  3. **codexFactory** — retirement of the worker jobs that reached the
     execution surface directly, which are unclaimable by design under the
     ruling and retire with the clearing slice.
  4. **codexFactory draft PR #165** (`adopt-bundle-shaped-deliberation`) — the
     deliberation-lane half, being revised to DEPEND on this change; its OQ-A
     (which party is the single gateway) is resolved by the ruling in favour of
     the estate's clearing boundary, and its bundle shape must conform to the
     manifest this change enumerates rather than declare its own.
- **Unblocks**: cross-factory execution on shared hardware without widening
  authorization per factory, and the deliberation lane that PR #165 parked.
- **Supersedes**: the per-path readiness authorization approach — superseded by
  the ruling on 2026-09-01 in favour of readiness as the clearing lane's first
  operation.
