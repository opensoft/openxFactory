# Omni Unattended Worker Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Omni is one signed host manager that lets a workstation owner or a
managed Cloud PC contribute bounded spare compute to xFactory — enrolled under a
durable installation identity with certificate authentication, running arbitrary
engineering code only inside a qualified, disposable executor, receiving work
through the estate's existing dispatch as a single-job ephemeral runner, and
returning candidates that governed infrastructure independently accepts.
Topics: omni-unattended-worker, worker-execution, worker-enrollment,
identity-brokering, workstation-intake, clearing-dispatch, worker-readiness,
omnigent-lane, trust-anchor
Repository context: openxFactory owns the neutral contracts; the design spans
OpsxFactory, Omnigent-Install, CloudPC-Install, xFactory-Enrollment-Broker,
Keycloak-Install, OpenXPKI-Install, xFactory-Installer, xFactory-Hermes-Install,
codexFactory and the xFactory aggregation
Captured: 2026-09-05

Provenance: captured from the 2026-09-05 design review lineage (Codex lane
`omni-gap-plan` original → Fable → gpt6-xhigh → Fable → gpt6Max → Brett's
rulings). This packet is non-normative design capture. Nothing here is ratified,
implemented, or a claim about a deployed system.

## Possible feats

- **One signed host manager with class-qualified disposable executors** across
  Home, Pro and Cloud PC hosts, with durable owner controls.
- **Installation identity with certificate authentication** to the enrollment
  broker, SPKI-bound credential versions, and separately scoped participation,
  worker and attempt authority.
- **Contributed engineering compute made useful** through explicit input release,
  ephemeral runners inside sandboxes, and independent acceptance on governed
  infrastructure.
- **A public volunteer contribution repository** whose token-visible material is
  releasable by construction.
- **A measured Windows support matrix** — versioned qualification records instead
  of a claim that every Windows machine is supported.

## Motivation

The preserved product intent, in the owner's terms: an owner downloads an
application, signs in, authorizes the contribution and selects how much of the
machine to share. They never create local accounts, configure Ubuntu or Docker,
paste tokens or run a shell. The same signed engine is delivered by OpsxFactory
through Intune to dedicated, already-enrolled Windows 365 Enterprise Cloud PCs
assigned to Omni001 and Omni002. Both resume after a reboot with nobody signed
in. Keycloak and OpenXPKI are existing components to integrate rather than
replace.

Three things make that harder than it sounds. A personal Windows workstation is
not in anyone's device-management tenant, so the enrollment route the estate has
does not apply to it. Most personal workstations run Windows Home, which has no
Hyper-V role, so the isolation backend the estate would prefer is unavailable
exactly where the personal product lives. And the machine's owner is its
administrator, so every input is readable, every result is forgeable, and no
certificate changes either fact.

## Goals

- A personal Windows workstation participates without device management, on its
  owner's consent, and survives reboot with no interactive login.
- A dedicated Cloud PC runs the same engine through managed delivery.
- Arbitrary engineering and test code runs only inside an executor whose
  containment was qualified for that class of code on that configuration.
- The owner's consented allocation and pause are durable against
  reconciliation, job completion and remote policy.
- Volunteer output is useful without being trusted: candidates accepted by
  governed infrastructure.
- Every credential a job can reach is approved before dispatch, not just the
  inputs it was handed.

## Non-goals

- Unused-license discovery, seat purchasing, Cloud PC provisioning and initial
  Intune enrollment stay deferred; the Cloud PCs in scope are already enrolled.
- VPS and Linux-server hosts are deferred.
- No organisational model credential is placed on volunteered hardware in this
  version.
- Private engineering work over private repositories stays a governed-node lane
  in this version.
- Microsoft Store distribution is a later channel, not a first delivery.
- This packet does not create a task list, a proposal, or a staged topic. The
  program roadmap it was captured from remains operator-local.

## What the system delivers

An owner-facing application and a host manager that together: enroll a machine
under a server-assigned installation identity; keep a device key and certificate
whose renewal disturbs nothing; authenticate every platform call as that
installation; qualify and advertise one or more containment classes; accept
bounded job attempts through the estate's existing dispatch; run each attempt in
a disposable sandbox with a single-job runner inside it; report per-worker
readiness over the authenticated channel; enforce one aggregate budget; and stop
— durably, locally, and on the server's word — when the owner or the platform
says so.

## System model

```text
  owner (Keycloak, external browser)        OpsxFactory / Intune (managed route)
              │ consent bound to CSR digest             │ SCEP, device-id bound
              └──────────────┬──────────────────────────┘
                             v
                 installation identity  ──  OpenXPKI RA workflow
                             │ mTLS (device_certificate, PROPOSED)
                             v
        enrollment broker ── participation session ── worker registrations
                             │                         │
        attempt-authorization record            heartbeat batch envelope
                             │                         └─> per-worker readiness
                             v
   host manager ──> executor (hyperv_vm | wsl2 | native_service_account)
                        └─> disposable sandbox ──> single-job ephemeral runner
                                                       │ artifacts
                                                       v
                                     quarantine ──> governed acceptance
```

Three server-side gates cut across that path: release (may these inputs be
disclosed to this device's administrator), containment (can this executor
contain this code), and acceptance (what evidence before the output affects a
decision).

## Cluster map

- [Synthesis: the device trust plane](omni-unattended-worker-synthesis-device-trust-plane.md)
  — how a machine is named, credentialed, authorized once, and denied at any
  instant.
- [Synthesis: sandboxed execution on somebody else's machine](omni-unattended-worker-synthesis-sandboxed-execution.md)
  — how a host makes, and evidences, a containment claim.
- [Synthesis: governed dispatch to untrusted hardware](omni-unattended-worker-synthesis-governed-dispatch.md)
  — how work, credentials and results cross the boundary safely.

## How it fits

**Reused as-is.** The enrollment broker and its ratified `worker-enrollment`
contract family, including the lease-not-registration inversion that already
makes control work on hardware nobody manages. The clearing-dispatch door and
its sealed bundles. The Hermes worker-readiness surface and its per-worker
store. The Omnigent-Install host app, its step machine and its reconciliation.
The Intune SCEP ceremony already proven on real Cloud PC hardware. The estate's
artifact-in/artifact-out lanes, restricted runner groups and workflow
allowlists. Keycloak for human authentication, OpenXPKI for issuance.

**Proposed changes, each named as a change rather than an integration detail.**
A third enrollment authentication mode, `device_certificate`, additive to the
ratified `host_identity` and `device_code`. An owner-authorized route for an
unmanaged workstation, which is a MODIFIED requirement against the promoted
`workstation-intake` capability and re-scopes the installer repository's stated
first product. Containment classes and qualification records as contract
objects. A batch heartbeat envelope and its projection into the existing
readiness read model. A new public contribution repository in the opensoft
organisation. An extension of broker minting to just-in-time runner
configuration, plus the attempt-authorization record that governs it.

**Adjacent work this packet links rather than duplicates.** The staged
[workstation app shell](../staging/workstation-app-shell/workstation-app-shell.md)
topic, which already separates the human console's OS principal from the
worker's on one machine; the
[governed worker execution](worker-execution-overview.md) and
[identity and custody](identity-custody-overview.md) packets, whose vocabulary
this reuses; and the ACTIVE
[add-worker-enrollment-broker](../../openspec/changes/add-worker-enrollment-broker/proposal.md)
change, cited here as read-only context.

## Key decisions and open questions

**Brett ruled two open decisions, verbatim.**

1. **"Documented partial WSL2 class."** Windows Home is served by a first-class
   `wsl2` executor with a versioned qualification record. Hardening is Linux-side
   and root-owned; admitted jobs carry public inputs and no secrets; the residual
   — LAN reach from the VM, and standard-account reads after a kernel exploit —
   is disclosed at owner consent; host-enforced egress control is NOT claimed,
   because the Hyper-V firewall for WSL is machine-wide; and Home is admitted
   only after the qualification record exists from a real Home laptop.
2. **"New public repo in opensoft."** A repository holding only the volunteer
   child workflows, pinned job schemas and a README, with `permissions: {}` by
   default and individually justified per-job grants, sealed-bundle inputs over
   the clearing contract, no organisation secrets, dispatch-only triggers, and a
   runner group admitting only that repository and its allowlisted workflows.
   Creation and naming are Brett's acts under the repo-shape conventions.

**Load-bearing choices carried from the review lineage.** Certificate-first
device access with Keycloak kept to humans. Installation identity in three
levels — installation and generation, SPKI-bound key versions, certificate
instances. Five nested authority objects with state re-checked at every
operation. Ephemeral runners inside the sandbox, with a separate server-side
attempt-authorization record because a just-in-time configuration is a credential
and not a grant. Compute-first placement, keeping model authority governed.

**Open questions that decide the shape of the product**, not merely its detail:

- Can a Windows service logging on as the worker account start and keep its WSL
  distro alive, with nobody signed in, across a reboot — on a Home laptop and on
  a Cloud PC? The pinned WSL source settles the architecture; the installed
  release is unmeasured.
- Can a Windows service create and start a Hyper-V VM on the dedicated Cloud PC
  with nested virtualization enabled, and which SKU, region and GPU exclusions
  apply?
- Do provider terms permit any unattended seat credential? Nothing in this design
  depends on the answer being yes.
- What are the actual numbers — status freshness, session and attempt lifetimes,
  drain bound, batch interval, budget defaults? Every one is currently unset.
- Who owns the base VM image pipeline, and the deployment of the broker itself?

## Staged path

The estate has one operator, so the sequence matters as much as the design, and
it is described here as prose rather than as a task list.

The first move changes two things that already exist: deploy the enrollment
broker, which is the owned prerequisite nobody had, and add certificate
authentication with SPKI-bound credential versions and an installation identity,
extending minting toward just-in-time runner configuration.

The second move is the feasibility proof, and it is deliberately blunt: bring up
the Hyper-V executor on the dedicated Cloud PC and the WSL2 executor on one
Windows Home laptop with a TPM, and answer the same question on both — does the
executor start from a service with nobody signed in, run a Docker job, and do it
again after a reboot, with an ephemeral runner inside the sandbox.

The third move is personal enrollment: the website installer, browser-based
consent bound to the certificate request, the narrow issuance workflow, and the
owner's controls.

The fourth move closes the loop: domain acceptance of volunteer candidates on
public inputs, the aggregate budget measured against a competing owner workload,
and the heartbeat and readiness changes that let a volunteer class report itself.

The earlier program plan this sequence condenses also carries a baseline step —
establish the exact deployed state of Keycloak, OpenXPKI, the broker and any
Cloud PC before assuming any of it — which remains the honest first act.

## Document map

**Overview**

- [Omni Unattended Worker Overview](omni-unattended-worker-overview.md) (this
  document).

**Syntheses**

- [Synthesis: the device trust plane](omni-unattended-worker-synthesis-device-trust-plane.md)
- [Synthesis: sandboxed execution on somebody else's machine](omni-unattended-worker-synthesis-sandboxed-execution.md)
- [Synthesis: governed dispatch to untrusted hardware](omni-unattended-worker-synthesis-governed-dispatch.md)

**Atomics — identity and authority**

- [Installation identity and credential versions](omni-unattended-worker-installation-identity.md)
- [Device certificate authentication at the enrollment broker](omni-unattended-worker-device-certificate-authentication.md)
- [Enrollment authorization: owner consent and the managed route](omni-unattended-worker-enrollment-authorization.md)
- [Five authority objects and their nested lifetimes](omni-unattended-worker-authority-object-lifetimes.md)

**Atomics — execution on the host**

- [The executor ladder and containment classes](omni-unattended-worker-executor-ladder.md)
- [The WSL2 distro belongs to the worker account, not to SYSTEM](omni-unattended-worker-wsl2-worker-owned-distro.md)
- [Rootless Docker as the Linux-side hardening candidate](omni-unattended-worker-rootless-docker-hardening.md)
- [Host manager topology: processes, steps and one writer per resource](omni-unattended-worker-host-manager-topology.md)
- [One aggregate budget and durable owner controls](omni-unattended-worker-aggregate-budget-and-owner-controls.md)

**Atomics — dispatch, evidence and placement**

- [Three independent policy gates: release, containment, acceptance](omni-unattended-worker-three-policy-gates.md)
- [Credential reach and the public contribution repository](omni-unattended-worker-credential-reach-and-contribution-repository.md)
- [Ephemeral runners and the attempt-authorization record](omni-unattended-worker-ephemeral-runner-attempt-grant.md)
- [The heartbeat becomes a batch envelope on the device channel](omni-unattended-worker-heartbeat-batch-envelope.md)
- [Compute first: model authority stays on governed hosts](omni-unattended-worker-compute-first-model-placement.md)
