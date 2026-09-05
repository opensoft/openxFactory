# Enrollment Authorization: Owner Consent and the Managed Route — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Two authorization routes produce the same installation identity — a
personal one where the owner signs in through Keycloak in an external browser
and the approval transaction is bound to the exact CSR digest, and a managed one
that reuses the Intune SCEP route already proven on a real Cloud PC — with a
narrowly scoped OpenXPKI registration authority doing the issuing and the
enrollment broker coordinating rather than holding certificate authority.
Topics: omni-unattended-worker, enrollment-authorization, worker-enrollment,
identity-brokering, workstation-intake, trust-anchor
Repository context: openxFactory owns the enrollment contract and the
workstation-intake capability; OpenXPKI-Install owns the registration-authority
workflow, Keycloak-Install the human authentication, OpsxFactory the tenant and
SCEP administration, xFactory-Enrollment-Broker the coordination
Captured: 2026-09-05

## Possible feats

- **Owner-authorized enrollment without device management** — a personal
  workstation joins without an Intune enrollment, on the owner's consent, with
  the consent bound to the exact key being certified.
- **A narrow registration authority** — one OpenXPKI workflow, one profile,
  server-assigned subject, rate limits and audit, so no component gains general
  issuance power.
- **Managed-route reuse with secret retirement** — the existing per-host secret
  is used once to bind the new key, then retired for that host.

## Focus

Who authorizes a machine to become an Omni installation, and how that
authorization is bound to a specific key so it cannot be substituted or
replayed onto a different device.

## Proposed model

**Personal route.** The app generates the key and CSR locally. The owner signs
in through Keycloak in an EXTERNAL browser using authorization code with PKCE
(the native-app pattern of RFC 8252). The resulting approval is an expiring
transaction bound to: the owner, the exact CSR or public-key digest, the
installation context, the requested profile, an expiry, and a single-use nonce.
The server assigns the certificate's identity fields — `CN=<installation_id>` —
rather than accepting a name from the request, and consumes the approval once.

This reduces substitution and replay. It does not prove that a remote person
physically possesses a particular PC, and the design should not claim it does.

**Managed route.** The Intune SCEP route that CloudPC-Install PR #13 reports as
proven on real hardware, against the same certificate authority, on the Cloud PC
recorded as CPC-brett-TUBV0 on 2026-08-31. Device IDs are authoritative there;
names are aliases, and the machine that holds the proven certificate is not
necessarily the machine the program targets — the dedicated Omni Cloud PCs are
different endpoints, and the fleet scope says which are legally assignable.

First contact on the managed route binds the new key's SPKI to the Entra device
id under the EXISTING `host_identity` secret, once; after that the host speaks
[device certificate mTLS](omni-unattended-worker-device-certificate-authentication.md)
and the secret is retired for that host. A reusable secret copied into every
installer is not an acceptable bootstrap.

**Issuance authority.** The registration authority is an OpenXPKI workflow with
its OWN identity, one allowed profile, server-assigned subject fields, rate
limits and an audit trail. The enrollment broker COORDINATES eligibility and
registration and calls that workflow holding a scope-limited RA client
credential; it holds no certificate authority beyond that call. Minting GitHub
runner registration tokens — which the broker already does — is not certificate
issuance authority, and the earlier claim that "the broker is the RA" was
withdrawn for that reason.

**Durability of the transaction.** Issuance can succeed while the network
response is lost. Transaction state must be durable enough that the same
approved result is retrievable without a duplicate registration or a second
human approval. Unactivated credentials expire or are revoked by reconciliation.

**Standing against the promoted capability.** The promoted `workstation-intake`
requirement says an eligible unmanaged workstation MUST select and launch the
approved Microsoft enrollment route. An owner-authorized route that does not
require device management is a MODIFIED requirement against that capability, on
Brett's ruling, and it should be carried as one openly rather than described as
an integration detail — the installer repository's first product is named on
the existing wording.

## Interfaces and boundaries

Consumes: owner consent (Keycloak) or fleet authorization (Intune/OpsxFactory);
a locally generated CSR; eligibility rules from the enrollment policy.

Emits: an authorized enrollment transaction; an issued certificate bound to a
server-assigned identity; an installation registration.

Owns: the binding between an approval and a key.

Does NOT own: certificate lifecycle after issuance, tenant administration, or
the local key's protection.

## Alternatives and tensions

- **Embedded-browser or device-code consent** instead of an external browser
  with PKCE. Simpler onboarding; weaker separation between the app and the
  credential, and against RFC 8252's guidance for native apps.
- **Requiring Intune enrollment for personal machines** — the currently promoted
  intake path. It preserves one enrollment story and one compliance surface, and
  it forecloses the personal product this design exists to deliver.
- **Broker-as-RA** versus **broker-calls-RA**. The first is fewer moving parts
  and one fewer credential; the second keeps issuance authority inside the PKI
  administration boundary. The settled position is the second.
- **Reusing the managed secret indefinitely** rather than retiring it per host.
  Retirement is cleaner; it also means a host that loses its certificate has no
  bootstrap left and must be re-authorized.
- **Evidence versus target.** The proven SCEP certificate and the dedicated Omni
  Cloud PCs are different machines. Treating the proof as coverage for the
  target is the specific mistake this section exists to prevent.

## Open questions

- What eligibility rules apply to a personal owner — any authenticated persona,
  or a member of a named group?
- How is the `workstation-intake` MODIFIED requirement carried, and what happens
  to the installer repository's stated first product?
- What is the approval transaction's expiry, and how many concurrent pending
  approvals may one owner hold?
- Does the personal route require attested key protection before issuing, or
  record the claim and let policy decide later?
- Who owns the RA workflow's own credential lifecycle?

## Relationships

- [Installation identity](omni-unattended-worker-installation-identity.md) — what
  the approval creates.
- [Device certificate authentication](omni-unattended-worker-device-certificate-authentication.md)
  — what the issued certificate is then used for.
- [Synthesis: device trust plane](omni-unattended-worker-synthesis-device-trust-plane.md)
  — the cluster this belongs to.
- Read-only context: the promoted
  [workstation-intake specification](../../openspec/specs/workstation-intake/spec.md)
  and the ratified
  [`contracts/worker-enrollment/` family](../../contracts/worker-enrollment/README.md).
