# Host Manager Topology: Processes, Steps and One Writer per Resource — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The Omni host manager is the existing host app evolved into four
processes with distinct privileges — a SYSTEM supervisor holding no assigned
key, a device identity service that is the sole principal with the key ACL,
executors behind a narrow prepare/start/inspect/cancel/destroy interface, and an
unprivileged owner UI — with two new executor steps, worker identities
established BEFORE any distro work, and exactly one reconciler per local
resource so two tools can never rotate the same account.
Topics: omni-unattended-worker, host-manager-topology, worker-host,
worker-execution, omnigent
Repository context: Omnigent-Install owns the host app and its step machine;
CloudPC-Install and xFactory-Installer are delivery wrappers; openxFactory owns
the neutral host contract
Captured: 2026-09-05

## Possible feats

- **A four-process host manager** — privilege separation that survives a
  compromised job and an accidental credential exposure.
- **Executors behind one narrow interface** — new containment classes added
  without touching the supervisor.
- **One reconciler per resource, enforced** — the invariant that stops two
  packages repairing each other's intentional stop.

## Focus

Which local process holds which privilege, in what order the host is built, and
who is allowed to write each local resource.

## Proposed model

**Four processes.**

| Process | Runs as | Holds | Exposes |
| --- | --- | --- | --- |
| Supervisor | SYSTEM | No assigned key; a minimal operation set and few input parsers | Reconciliation of desired state |
| Device identity service | Its own service identity | The ONLY key ACL | Fixed operations to SID-authenticated callers: renew participation, fetch an attempt grant, post a heartbeat |
| Executors | Per class; the WSL class runs as the worker account with its profile loaded | The sandbox lifecycle | `prepare`, `start`, `inspect`, `cancel`, `destroy` |
| Owner UI | Unprivileged | Nothing | Authenticated local control operations |

**Honest statements about that separation.** A SYSTEM component is part of the
trusted host and is never a workload runner, but it must not be described as
holding no secrets merely because it holds no assigned key — it can still
reconfigure a service or cause authorized key use, so its exposed operations and
input parsers are deliberately small. Normal key ACLs restrict which services
may invoke the key; they do not exclude SYSTEM or a hostile local administrator
from the host trust boundary. The service boundary protects against job code and
accidental exposure; it cannot make an owner-controlled machine an independently
trusted principal. And a caller-SID check alone is insufficient if a job inherits
its runner's SID — caller isolation and a bounded operation set are both
required.

**No remote command path into the Windows supervisor.** Arbitrary project code
runs only inside a qualified sandbox. The manager accepts jobs from the
authorized control plane and applies the owner's current policy AGAIN before
starting them. A compromised guest agent is untrusted input to the host adapter;
artifact export checks paths, symlinks, sizes and archive expansion.

**Step-machine changes.** Two new steps, `executor_hyperv` and `executor_wsl2`,
each covering qualification, image or distro, and network policy. The existing
`worker_identities` step becomes executor-CONDITIONAL — the VM class needs no
Windows account per logical worker, the WSL class needs one — and is ORDERED
BEFORE distro work, because
[the distro belongs to the worker account](omni-unattended-worker-wsl2-worker-owned-distro.md)
and SYSTEM cannot register it. The container-engine step gains a second,
rootless profile rather than being reconfigured in place.

**One writer per resource.** Every local resource — a service, an account, a VM,
a directory, a rotation schedule — has exactly one reconciler. Two tools must
never own the same one. The concrete case in the estate: the service-rider pack
is a second engine with its own account, rights, heartbeat task, runner service
and seal, and it is compatible today only because it binds a different host
class. Its disposition rides with the recorded rider-to-governed-node migration
issue, and it must not be left as a standing second engine.

**Delivery wrappers, not second engines.** The managed Intune package and the
website installer both lay down the SAME signed package plus a profile and start
the supervisor. Store distribution via the MSI/EXE route is a later channel:
feasible, unproven, not first.

**Update, recovery and removal.** Updates are signed, digest-pinned and subject
to schema and minimum-version policy. An independently maintainable
recovery/updater path exists so quarantining execution does not prevent repair;
recovery permits signed repair material, never resumption of jobs. Drain before
replacing an executor or changing limits. Rollback only to versions current
policy still permits, and package recovery must never restore a revoked
generation or undo owner settings.

## Interfaces and boundaries

Consumes: the signed package and its profile; authorized desired state; the
owner's current controls.

Emits: reconciled local state, executor lifecycle operations, and the local
control API.

Owns: process privilege separation, step order, and resource ownership.

Does NOT own: server-side authority, gate decisions, or the containment
guarantees of any class.

## Alternatives and tensions

- **Merging the rider pack into the host app** versus keeping the products
  separate and enforcing the one-writer invariant contractually. The invariant is
  the requirement; a product merger is one means to it.
- **A single privileged service** doing everything. Fewer parts, simpler
  installation, and no boundary between the key holder and the reconciler.
- **Store distribution first.** Attractive for a personal product; the engine
  installs a service, creates accounts, edits logon rights and enables optional
  features, so the packaging question is real even though the MSI/EXE route
  exists. Priority, not possibility, is why it waits.
- **Executor steps in the host app versus a separate executor product.** Keeping
  them in the step machine reuses reconciliation that already exists and grows a
  component that is already large.

## Open questions

- What is the exact local IPC boundary, and how does it distinguish a runner
  from a child job with the same SID?
- Does the supervisor hold the worker account's credential only transiently at
  bind time, and what proves that?
- What is the disposition of the service-rider pack, and who decides it?
- Which package owns the base VM image pipeline — build, sign, pin?
- How is "one writer per resource" verified rather than asserted, once two
  packages can land on one host?

## Relationships

- [Executor ladder](omni-unattended-worker-executor-ladder.md) — the classes
  behind the executor interface.
- [WSL2 worker-owned distro](omni-unattended-worker-wsl2-worker-owned-distro.md)
  — the finding that reorders the step machine.
- [Aggregate budget and owner controls](omni-unattended-worker-aggregate-budget-and-owner-controls.md)
  — the desired state this reconciler must never undo.
- [Synthesis: sandboxed execution](omni-unattended-worker-synthesis-sandboxed-execution.md)
  — the cluster this belongs to.
- [Governed worker execution host contract](worker-execution-host-contract.md) —
  the estate's existing neutral host vocabulary.
