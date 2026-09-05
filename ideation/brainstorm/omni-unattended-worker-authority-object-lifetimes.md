# Five Authority Objects and Their Nested Lifetimes — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Participation, workers, capacity and individual jobs are four different
permissions over one installation registration — installation registration, host
participation session, worker registration, execution slot and job attempt grant
— whose lifetimes nest, where every authority-bearing operation re-checks
current state rather than freezing it at handshake, and attempts are fenced
server-side so a superseded attempt's results are rejected.
Topics: omni-unattended-worker, authority-object-lifetimes, worker-enrollment,
worker-execution, roles-authority-model
Repository context: openxFactory owns the neutral lease and job-envelope
contracts; xFactory-Enrollment-Broker holds the records and their state machine
Captured: 2026-09-05

## Possible feats

- **A five-object authority model** — one vocabulary that distinguishes being
  registered, participating now, being an eligible worker, holding capacity, and
  being allowed to run one job.
- **Re-checked state at every operation** — an authorization model where a
  long-lived connection freezes nothing.
- **Attempt fencing** — server-side rejection of results from superseded
  attempts, so a reboot or a rerun cannot double-count.

## Focus

What each authority object means, what its existence permits, and how they nest
— so that "the device is enrolled" never silently means "this job may run".

## Proposed model

| Object | Identity and scope | What its existence permits |
| --- | --- | --- |
| Installation registration | Installation id and enrollment generation | Identifies an approved installation and its credential lifecycle |
| Host participation session | Installation, current policy epoch, expiry, aggregate limits | Allows participation and control exchange while eligible; one connection carries renewal and reporting |
| Worker registration | Stable logical worker under the installation, with profile and tenant/project scope | Names an eligible logical worker; may map onto an existing runner binding |
| Execution slot | Local capacity reserved for a profile | Supplies resources. It is NOT an identity and NOT an independent permission |
| Job attempt grant | Job, attempt, worker, generation, inputs, image, operations, limits, expiry | Allows ONE bounded attempt and its explicitly authorized input and output |

**Nesting.** A grant's permitted lifetime cannot exceed its parents'. Denying
the parent installation denies every child. Stopping one worker does not require
replacing the installation certificate.

**Current state, always.** Eligibility is re-checked on admission, renewal,
input release, credential issuance and result submission. A valid long-lived TLS
connection does not freeze authorization at handshake time, and possession of a
cached lease file is not authority. Admission and revocation serialize against
current state so a raced renewal cannot undo a deny.

**Bounded disconnection.** Each profile declares a maximum disconnection window
rather than inheriting an hourly timer as its security promise. A local
monotonic timer helps an honest host stop on expiry; the server rejects stale
authority regardless of the host's clock.

**After a reboot or a snapshot restore**, the host obtains current authority
BEFORE resuming dispatch, and either allocates a new attempt or receives explicit
authorization to continue the old one. Server-side fencing rejects results from
superseded attempts. Seeing an incomplete local job never authorizes re-executing
an external side effect — and the initial compute profiles hold no production
mutation authority at all.

**Revocation ordering.** Deny in the platform first — registration or worker
state, outstanding authority invalidated per policy — then durably request PKI
revocation and reconcile. Certificate status carries a declared freshness limit
and admission fails closed when the evidence is too stale. Revocation cannot
recall delivered data or stop a hostile owner's local computation; it prevents
further inputs, credentials, dispatch and accepted results. The estate-wide stop
remains a policy floor raise (`min_app_version`), which denies work everywhere.

**What the existing broker already has, and what it is not.** The broker's
`lease_engineer_machine_slot` invariant is a per-ENGINEER machine cap and stays
as it is; repurposing it as worker capacity conflates two invariants. The
existing one-active-lease-per-host row becomes the host participation session.

**On volunteered hardware these worker ids express server-enforced scopes**, not
attestations about local processes: a hostile administrator can simulate any
worker registered to that installation. The server still limits what each worker
can reach; it must not infer host integrity from the distinction.

## Interfaces and boundaries

Consumes: the authenticated installation identity; policy epochs; capacity
observations from the host.

Emits: the five records and their state transitions, each auditable.

Owns: the nesting and fencing rules.

Does NOT own: how a job is transported (that is the attempt grant's credential),
how it is contained, or whether its result is accepted.

## Alternatives and tensions

- **Leases keyed by `(device, worker)`** — the original design's model. It puts
  worker cardinality in the lease table and collides with the existing per-host
  lease constraint, which is the reported cardinality mismatch in the estate's
  in-flight enrollment client.
- **Reusing `slot_index` for worker capacity** — proposed once and WITHDRAWN as
  an error: it is the engineer machine cap. Recorded because it is an easy
  mistake to make twice.
- **Five objects is a lot for a first implementation.** The counter-pressure is
  real: every object is a table, a state machine and a migration. The argument
  for keeping them separate is that each one is already implicitly present, and
  the failures of conflating them (a slot that acts like an identity, a lease
  that grants a job) are exactly the ones that are invisible until they matter.
- **Server-side fencing versus host-side stop.** Both are kept deliberately: the
  honest host stops itself, and the server is the control that survives a
  modified host.

## Open questions

- What are the actual lifetimes — participation session, worker registration,
  attempt grant — per estate and per profile?
- Does the worker registration survive a generation change, or retire with it?
- How does a schema migration reach the existing lease rows without breaking the
  managed fleet's live leases?
- Is the execution slot a server-side record at all, or purely local capacity
  bookkeeping the server never sees?

## Relationships

- [Installation identity](omni-unattended-worker-installation-identity.md) — the
  root object everything else nests under.
- [Device certificate authentication](omni-unattended-worker-device-certificate-authentication.md)
  — how the caller of these operations is identified.
- [Ephemeral runner attempt grant](omni-unattended-worker-ephemeral-runner-attempt-grant.md)
  — the last object in the chain, and its credential.
- [Synthesis: device trust plane](omni-unattended-worker-synthesis-device-trust-plane.md)
  — the cluster this belongs to.
- Read-only context: the ratified
  [`contracts/worker-enrollment/` family](../../contracts/worker-enrollment/README.md),
  whose lease record is the object this model extends.
