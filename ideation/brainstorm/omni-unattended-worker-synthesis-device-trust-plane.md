# Synthesis: The Device Trust Plane — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Installation identity, enrollment authorization, certificate
authentication and the five nested authority objects combine into one plane
whose emergent property is that a machine can be named durably, credentialed
replaceably, authorized once by a human, and then denied at any instant —
without any of those four acts depending on the others staying still.
Topics: omni-unattended-worker, device-trust-plane, installation-identity,
enrollment-authorization, device-certificate-authentication,
authority-object-lifetimes, identity-custody, worker-enrollment, synthesis
Repository context: openxFactory owns the neutral identity, enrollment and lease
contracts; xFactory-Enrollment-Broker, OpenXPKI-Install and Keycloak-Install
realize them
Captured: 2026-09-05

## Possible feats

- **A revocation act that actually reaches** — one deny in the platform that
  invalidates participation, workers and attempts together, with PKI revocation
  reconciled behind it.
- **Zero-churn credential maintenance** — automatic renewal that touches no
  binding, with rotation and recovery as the only events anyone must notice.
- **An enrollment ceremony that survives a lost response** — durable transaction
  state, one human approval, no duplicate registrations.

## Members and their joints

Atomic members:
[installation identity](omni-unattended-worker-installation-identity.md),
[enrollment authorization](omni-unattended-worker-enrollment-authorization.md),
[device certificate authentication](omni-unattended-worker-device-certificate-authentication.md),
[authority object lifetimes](omni-unattended-worker-authority-object-lifetimes.md).

```text
human or fleet authorization ──> enrollment transaction (bound to CSR digest)
                                        │
                                        v
                    installation id + generation ──> key versions ──> certificates
                                        │                                  │
                                        │                     mTLS at the device API
                                        v                                  │
        participation session ──> worker registration ──> slot ──> attempt grant
```

### Authorization creates identity; identity never re-creates authorization

The enrollment transaction is the only place a human decision enters the plane,
and it is consumed once. Everything afterwards — renewal, rotation, reconnection
after a reboot — is machine-to-machine and adds no authority. The one exception
is deliberate: recovery, which requires a NEW human or fleet authorization
precisely because the credential that would otherwise speak for the machine is
gone. This is the joint that makes "an expired credential cannot authenticate
its own recovery" a structural property rather than a rule someone must remember.

### Certificates are checked against records, and the records are the authority

Authentication reads three things that live in different places: the certificate
(PKI), the key binding (registration), and the registration state (broker). The
plane deliberately does NOT make any one of them sufficient. A valid certificate
over a retired generation fails; a current registration with a revoked
certificate fails; a certificate whose status evidence is stale beyond the
declared limit fails closed. The cost is that three systems must be reachable
and consistent at admission time, which is exactly the availability tension the
freshness limit encodes.

### Nesting turns one deny into many

Because participation, worker registration, slot and attempt all descend from
the installation registration and cannot outlive their parents, a single
platform-side deny propagates without a distributed cascade. The plane does not
need to hunt down in-flight authority; it needs only to refuse at the next
authority-bearing operation, which the "re-check current state" rule guarantees
happens soon. What it CANNOT do is stop something already delivered or already
running elsewhere — which is why the runner side has its own cancellation path
in the dispatch cluster.

### Renewal is invisible on purpose, and that is a design choice with a cost

SPKI-bound key versions make renewal a no-op for every consumer of the binding.
The cost, named by the review that corrected the earlier draft, is that
certificate instances still have their own issuer, serial, validity and
revocation state, so "nothing changed" is true of the binding and false of the
inventory. The plane keeps both statements by holding three levels instead of
two.

## Emergent behavior

- **Denial without re-enrollment.** Stopping one worker, or the whole host, never
  requires replacing a certificate — an operational property none of the four
  atomics provides alone.
- **A personal machine and a managed Cloud PC become the same object.** Two
  different authorization routes produce one installation-registration shape, so
  every downstream rule — leases, attempts, revocation, audit — is written once.
- **Freshness becomes the availability dial.** With state re-checked everywhere
  and status evidence failing closed, the single number that decides how the
  plane behaves during a CA or broker outage is the freshness limit. Nothing in
  any one atomic makes that visible; the combination does.
- **The plane's honesty ceiling.** Together these four say precisely what
  authentication proves — which installation received a credential — and nothing
  about where code ran or whether a result is true. Every stronger claim later in
  the system must come from acceptance, not from identity.

## Tensions to hold

- **One human approval versus continuous consent.** The plane is designed so a
  single consent starts a durable relationship; the owner-controls atomic in the
  execution cluster is where continuing consent actually lives. Whether an
  installation should periodically re-ask is unresolved.
- **Durable identity as a durable correlator.** The same property that makes
  revocation meaningful makes a personal machine trackable across generations.
- **Keycloak's absence from the machine path** simplifies the plane and leaves a
  future OIDC-only consumer unserved; the machine-token adapter is deferred
  rather than designed.
- **Three checks at admission** is either defence in depth or three availability
  dependencies, depending on the day.

## Recombination opportunities

- With the estate's existing identity-and-custody trust plane
  ([overview](identity-custody-overview.md)) — an Omni installation is another
  principal class in that plane rather than a private scheme.
- With the trust-anchor and certificate custody work: installation identity is a
  candidate consumer of an already-realized anchor rather than a new root.
- With [the sandboxed execution cluster](omni-unattended-worker-synthesis-sandboxed-execution.md)
  — worker registrations map onto executor accounts, and the mapping is
  executor-conditional.
- With [the governed dispatch cluster](omni-unattended-worker-synthesis-governed-dispatch.md)
  — the attempt grant is the seam where this plane hands over.

## Open questions

- Does the plane's revocation ordering (platform first, PKI reconciled) meet the
  managed fleet's compliance expectations, or does a tenant require CA-first?
- Which of the three admission checks may degrade during an outage, if any?
- How does an installation prove hardware key protection strongly enough for the
  server to record it as verified rather than claimed?
- What audit record ties an enrollment approval, a certificate serial and a
  registration generation together for a later reader?
