# Omni Installation Identity and Credential Versions — Brainstorm

Status: brainstorm
Kind: architecture
Summary: An Omni installation is named by a server-assigned installation id and
enrollment generation, and everything cryptographic below it — authorized key
versions bound by SPKI hash, and certificate instances with their own issuer,
serial, validity and revocation state — is a replaceable credential attached to
that name, so renewal changes nothing the platform must re-bind while rotation,
recovery and reinstall stay explicit, recorded events.
Topics: omni-unattended-worker, installation-identity, identity-custody,
trust-anchor, worker-enrollment, credential-contracts
Repository context: openxFactory owns the neutral identity and enrollment
contracts; realization spans xFactory-Enrollment-Broker (registration records),
OpenXPKI-Install (issuance) and Omnigent-Install (the on-host key holder)
Captured: 2026-09-05

## Possible feats

- **Installation registration with generations** — a durable, server-assigned
  identity for a machine's participation that survives every credential change
  and cannot be resurrected by an old credential.
- **SPKI-bound credential versions** — a key binding that renewal does not
  disturb, so certificate lifecycle stops being a distributed-consistency
  problem across three stores.
- **A recorded credential-event vocabulary** — renewal, rotation, recovery and
  reinstall as four distinct events with four distinct authorizations, rather
  than one word ("re-enroll") covering all of them.

## Focus

What durably NAMES an Omni installation, and what is merely a credential
attached to that name. Every later decision — how the device authenticates,
what a lease is scoped to, what revocation reaches — depends on this one
distinction being made once and made explicitly.

## Proposed model

**Three levels, never collapsed.** The correction is from the gpt6Max review
pass and is accepted into the settled design:

1. **Installation and generation.** A server-assigned `installation_id` with an
   `enrollment_generation`. It owns the owner or fleet authorization that
   created it, the allowed profiles, the recorded device evidence, and a
   bounded set of credential versions. A hostname is display metadata. An Entra
   device id is an external binding for a managed device, not the identifier of
   a personal installation.
2. **Authorized key versions.** Each key version is identified by the hash of
   its subject public-key info (SPKI). This is the binding the platform stores
   and checks.
3. **Certificate instances.** Each certificate attached to a key version has
   its own issuer, serial, validity interval, extensions and revocation status.
   RFC 5280 defines those separately from the subject public-key information,
   and revocation identifies a certificate by serial under its issuer — so two
   certificates over one key are two objects, not one.

**Four events, four authorizations.**

| Event | What changes | What authorizes it |
| --- | --- | --- |
| Renewal | A new certificate instance over the SAME key version | Automatic under current policy; no human step; the key binding is untouched, but certificate inventory and audit are updated |
| Rotation | A new key version, proving possession of the replacement, with a bounded overlap before the old one retires | An explicit, recorded event under current registration state |
| Recovery | A new generation; the previous one retires | Fresh owner or fleet authorization — an expired or lost credential cannot authenticate its own recovery |
| Reinstall | A new installation registration unless the operator deliberately re-binds the existing one | The same authorization path as first enrollment |

**Key compromise disables the key binding**, not just the certificate. Otherwise
a second, otherwise-valid certificate over the same key restores access after
the compromise was reported. Disabling the generation is the stronger form.

**Every presented certificate is checked against all three levels** at every
authority-bearing operation: profile and issuer, validity, revocation status,
current key binding, and current registration generation. No token or
certificate may resurrect a retired generation.

**Key protection is evidence, not a label.** Physical TPM, virtual TPM, verified
attestation and an unverified client claim are four different facts. A CSR
proves possession of a key; server-verifiable hardware protection requires
additional evidence, and the server should only claim what it verified. The
original design's planning default required TPM for the pilot and named a
software-key fallback as a product decision needing an explicit lower-assurance
policy and equivalent lifecycle tests — that framing is preserved here, not
resolved.

## Interfaces and boundaries

Consumes: owner consent or fleet authorization (see
[enrollment authorization](omni-unattended-worker-enrollment-authorization.md));
a locally generated key and CSR; issuance from the certificate authority.

Emits: an installation registration record with its generation, credential
version inventory and recorded device evidence.

Owns: the meaning of "this is the same installation", and the retirement rules
for keys, certificates and generations.

Does NOT own: authentication at the device API (that is a separate mechanism
over this identity), worker identity, capacity, or job authority — those are
[separate authority objects](omni-unattended-worker-authority-object-lifetimes.md)
with their own lifetimes.

## Alternatives and tensions

- **Certificate fingerprint as the installation identity.** Proposed in the
  first review pass and WITHDRAWN as an error in the next: a fingerprint
  identifies one certificate, so renewal changes it even when the key does not,
  and pinning it re-creates the rotation problem inside the broker. Recorded
  because the reasoning, not just the conclusion, is worth keeping.
- **Hostname or Entra device id as the identifier.** Works for a managed fleet
  where a device-management authority already owns the record; fails for a
  personal installation that no tenant enrolled. Both remain useful as external
  bindings and as display metadata.
- **Three stores for one public key.** The original design bound the device key
  in the OpenXPKI certificate, a Keycloak machine client with a registered
  public key, AND the broker's device registration — and then had to invent
  coherence machinery (renewal must update the Keycloak binding with an overlap;
  signed-JWT client authentication does not check CA revocation) for a problem
  its own construction created. The tension is real either way: removing the
  Keycloak record simplifies the machine path but leaves any future OIDC
  consumer without one.
- **Stability versus disposability.** A durable installation identity is what
  makes revocation and history meaningful; it is also a durable correlator on a
  personal machine. The generation is the release valve — and how aggressively
  generations retire is unsettled.

## Open questions

- Is TPM protection required for the personal pilot, or is there a declared
  lower-assurance software-key tier with its own policy and job profile?
- How long is the rotation overlap, and what proves the replacement key?
- Is a generation retired automatically on recovery, or by an operator act with
  its own audit record?
- What device evidence is recorded at enrollment, and which parts of it does the
  server independently verify rather than accept as a client claim?
- Does reinstall on the same hardware re-bind the existing installation or
  always create a new one? The answer decides what an owner sees after a
  wipe-and-restore.

## Relationships

- [Device certificate authentication](omni-unattended-worker-device-certificate-authentication.md)
  — how this identity is presented and checked at the device API.
- [Enrollment authorization](omni-unattended-worker-enrollment-authorization.md)
  — how a generation comes into existence in the first place.
- [Authority object lifetimes](omni-unattended-worker-authority-object-lifetimes.md)
  — what nests underneath an installation registration.
- [Synthesis: device trust plane](omni-unattended-worker-synthesis-device-trust-plane.md)
  — the cluster this belongs to.
- [Identity and Custody Overview](identity-custody-overview.md) and
  [principal and agent binding](identity-custody-principal-and-agent-binding.md)
  — the estate's existing trust-plane vocabulary this reuses rather than forks.
