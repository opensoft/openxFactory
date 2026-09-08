# Device Certificate Authentication at the Enrollment Broker — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The host's device identity service authenticates to the enrollment
broker with mutual TLS using its OpenXPKI certificate, checked against issuer,
profile, validity, current key binding, current registration state and a
certificate status with a declared freshness limit that fails closed — a
PROPOSED third authentication mode, `device_certificate`, additive to the
ratified `host_identity` and `device_code`, with Keycloak left to authenticate
people.
Topics: omni-unattended-worker, device-certificate-authentication,
worker-enrollment, identity-brokering, trust-anchor
Repository context: openxFactory owns the `contracts/worker-enrollment/` family
this would extend; xFactory-Enrollment-Broker realizes the check and
Keycloak-Install and OpenXPKI-Install own the identity and PKI runtimes
Captured: 2026-09-05

## Possible feats

- **A third enrollment authentication mode** — `device_certificate`, so a
  machine can authenticate as itself without a standing shared secret and
  without a per-device OIDC client.
- **Retirement of a standing per-host secret** — `host_identity` is a secret
  escrowed at Intune time; a certificate-authenticated host does not need it
  after first contact.
- **Fail-closed freshness on revocation evidence** — a declared maximum age for
  certificate status, so a CA outage becomes a refusal instead of unbounded
  authorization.

## Focus

How the machine proves which installation it is, on every call, without a
standing shared secret and without making a human identity broker part of the
machine path.

## Proposed model

**Mutual TLS from the device identity service to the broker's device API.** On
each connection the broker checks, as separate facts:

- the certificate chains to the approved issuer and carries the approved
  profile and key usage;
- the certificate is inside its validity interval;
- its SPKI matches a currently authorized key version of the named installation
  (see [installation identity](omni-unattended-worker-installation-identity.md));
- the installation registration and its generation are currently active;
- certificate status (CRL or OCSP) is known and NOT older than a declared
  freshness limit. Beyond that limit admission FAILS CLOSED. Retry and caching
  policy must not silently convert a CA or broker outage into unbounded
  authorization.

**Ingress rules.** If TLS terminates at an ingress, downstream identity evidence
reaches the backend only over that authenticated path; external identity headers
are stripped, and the backend cannot be reached directly. A forwarded
certificate string from an arbitrary client is not authenticated identity.

**Relation to the ratified contract.** `contracts/worker-enrollment/` today
enumerates two authentication modes: `host_identity` (a per-host secret escrowed
at managed-enrollment time; `standing_secret_on_host: broker_access_only`) and
`device_code` (the engineer, interactively; `standing_secret_on_host: none`).
`device_certificate` is a THIRD mode, PROPOSED here and not ratified: adding it
is an explicit delta against that ratified family, and the volunteer estate's
"no standing credential" rule has to be read deliberately, because a
non-exportable device key with a bounded certificate is a different object from
an escrowed shared secret and the contract does not say so yet.

**Keycloak's place.** Keycloak authenticates PEOPLE: the owner's sign-in and
consent in the app, and the factory UI. There is no per-device Keycloak client
on this path. A machine-token adapter — Keycloak X.509 client authentication, or
RFC 8705 certificate-bound tokens — is introduced only when a concrete consumer
needs an OIDC token, with a documented issuer, audience, subject mapping and
lifecycle. It is an option, not an automatic property of mTLS.

**What this does NOT prove.** Device mTLS authenticates DELIVERY of a credential
to an installation. It does not bind a later runner session to the TPM key and
does not prove where a job executed. That is compatible with advisory volunteer
results only because no stronger claim is made.

## Interfaces and boundaries

Consumes: the installation's current certificate and key binding; the broker's
registration state; certificate status from the CA.

Emits: an authenticated caller identity (installation and generation) for every
device-API operation — participation renewal, attempt-grant fetch, heartbeat
delivery.

Owns: the transport-level identity check and its freshness policy.

Does NOT own: what that identity is permitted to DO — that is the authority
object model — nor human authorization, nor certificate issuance.

## Alternatives and tensions

- **Keycloak on the machine path (the original design).** A per-device Keycloak
  machine client with a registered public key, authenticating by
  `private_key_jwt`. Rejected here because it needs some component to hold
  Keycloak administrative authority and exercise it on every enrollment, adds a
  second key binding to keep consistent with certificate renewal, and adds a hop
  and a clock without adding a decision — the broker must check registration and
  revocation anyway. Preserved as an alternative because it is the path that
  most easily satisfies a future OIDC-only consumer.
- **A signed-challenge protocol instead of mTLS.** Rejected in favour of
  standard TLS client authentication rather than a bespoke signed-request
  protocol. The tension: mTLS is harder to terminate cleanly behind some
  ingress topologies, which is exactly why the header-stripping rule is stated.
- **Keeping `host_identity` indefinitely.** It works today on the managed fleet
  and needs no new mode. Its cost is a standing secret on every host and a
  bootstrap that a personal installation cannot use at all.
- **Freshness versus availability.** Fail-closed on stale revocation evidence is
  the right security posture and is also the behaviour most likely to strand
  honest hosts during a CA outage. The limit is a policy number nobody has set.

## Open questions

- What is the declared status-freshness limit, and is it the same for the
  managed and volunteer estates?
- Does `device_certificate` land as an additive delta inside the ACTIVE
  `add-worker-enrollment-broker` change or as a successor change?
- Does the volunteer estate's `standing_secret_on_host: none` declaration need
  amending, or does a non-exportable device key already sit outside it?
- Which consumer, if any, forces the machine-token adapter into existence?
- Where does TLS terminate in the deployed broker, and who verifies the
  header-stripping rule holds there?

## Relationships

- [Installation identity](omni-unattended-worker-installation-identity.md) — the
  identity this mechanism presents.
- [Enrollment authorization](omni-unattended-worker-enrollment-authorization.md)
  — how the first certificate is obtained before this mode can be used.
- [Heartbeat batch envelope](omni-unattended-worker-heartbeat-batch-envelope.md)
  — the first substantial payload carried over this channel.
- [Synthesis: device trust plane](omni-unattended-worker-synthesis-device-trust-plane.md)
  — the cluster this belongs to.
- [Keycloak Identity Brokering and the Single Persona](keycloak-identity-brokering.md)
  — the estate's existing human-identity direction, which this deliberately does
  not extend onto the machine path.
- Read-only context: the ratified
  [`contracts/worker-enrollment/` family](../../contracts/worker-enrollment/README.md)
  and the ACTIVE
  [add-worker-enrollment-broker](../../openspec/changes/add-worker-enrollment-broker/proposal.md)
  change.
