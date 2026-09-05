# Synthesis: Sandboxed Execution on Somebody Else's Machine — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The executor ladder, the worker-owned WSL distro, rootless Docker, the
host-manager topology and the aggregate budget combine into a single claim a
host can make about itself — "I can contain THIS class of code within THESE
limits, and here is the qualification record that says so" — where the platform
fact that SYSTEM cannot own a distro reorders the whole build sequence and the
machine-wide firewall scope decides which class may claim egress control at all.
Topics: omni-unattended-worker, sandboxed-execution, executor-ladder,
wsl2-worker-owned-distro, rootless-docker-hardening, host-manager-topology,
aggregate-budget, worker-execution, synthesis
Repository context: Omnigent-Install owns the host manager and executors;
CloudPC-Install and xFactory-Installer deliver them; openxFactory owns the
neutral containment and resource vocabulary
Captured: 2026-09-05

## Possible feats

- **A qualification record as the unit of trust** — a versioned, per-configuration
  artifact that dispatch reads instead of inferring safety from a backend name.
- **Unattended executor startup** — a sandbox created, run and destroyed with
  nobody signed in, on both a personal laptop and a Cloud PC.
- **Consent that reaches the residual** — an owner told which specific weakness
  their machine's class carries, before any job runs.

## Members and their joints

Atomic members:
[executor ladder](omni-unattended-worker-executor-ladder.md),
[WSL2 worker-owned distro](omni-unattended-worker-wsl2-worker-owned-distro.md),
[rootless Docker hardening](omni-unattended-worker-rootless-docker-hardening.md),
[host manager topology](omni-unattended-worker-host-manager-topology.md),
[aggregate budget and owner controls](omni-unattended-worker-aggregate-budget-and-owner-controls.md).

### A platform fact reorders a build sequence

The WSL session factory rejecting LocalSystem is a single source-level finding,
and it propagates through the whole cluster: the host app's SYSTEM-run substrate
step cannot register the distro; therefore the worker identity must exist first;
therefore `worker_identities` moves ahead of distro work; therefore a Windows
service logging on as that account becomes the executor's home; therefore
SYSTEM-run detection must read a marker instead of calling `wsl.exe`. None of
those follow from the executor ladder or the topology on their own. This is the
clearest example in the packet of an implementation detail with architectural
authority.

### The boundary is split across two owners, and neither half is sufficient

The `wsl2` class's boundary is half Windows-side (which account owns the distro,
one attempt per VM, `wsl --shutdown` between attempts) and half Linux-side
(rootless daemon, unprivileged job user, root-owned policy). Compromise either
half and the class fails: a perfectly hardened distro owned by the wrong Windows
account is reachable from the owner's session, and a correctly owned distro
running rootful Docker hands a job daemon control. The qualification record is
where the two halves are asserted TOGETHER, which is why it is the class's real
definition.

### The firewall's scope decides what the class may claim

Hyper-V firewall rules for WSL are identified by a creator id common to WSL and
carry a documented loopback exception, so any policy Omni sets there touches the
owner's own WSL. That single scoping fact removes host-enforced egress control
from the `wsl2` class's claims and pushes enforcement into root-owned nftables
INSIDE the distro — which in turn forces the owner-match requirement, because
rootless networking emits traffic as the rootless user rather than forwarding
it. A property of a Windows feature therefore determines a Linux firewall rule
shape.

### The budget is enforced by parts that enforce differently

One consented aggregate covers native processes, a utility VM per worker account
and containers inside it. The hypervisor class enforces memory and processor
ceilings; the WSL class enforces per-account configuration whose maxima do not
sum; the container layer enforces cgroup limits only where delegation is
available. So the manager's budget is the ONLY place a host-wide promise can
exist, and it exists as reservation plus admission control rather than as a
single enforced ceiling.

### One reconciler, or the owner's pause is not durable

Durable pause is an owner-controls property, and it survives only because
exactly one reconciler owns each resource. Two engines on one host — the
recorded rider-pack case — is the shape in which reconciliation silently undoes
an intentional stop. The invariant belongs to the topology; the guarantee
belongs to the owner.

## Emergent behavior

- **Home becomes serviceable.** No single atomic makes Windows Home viable; the
  combination — a worker-owned distro, Linux-side hardening, a narrowed workload
  and a disclosed residual — does, and it is the only path to the personal
  product the accepted intent puts first.
- **A class can be un-qualified.** Because the record is versioned and
  per-configuration, a Windows or WSL update can retire a class on a host without
  any code change, and the host simply stops receiving that class of job.
- **Containment and consent become one conversation.** The residual the `wsl2`
  class cannot close is exactly what the owner is asked to accept, so the
  security boundary and the consent text are derived from the same record.
- **Capacity and containment interact.** One attempt per VM boundary plus one
  Omni account per concurrent attempt means concurrency costs Windows accounts,
  so the budget's concurrency dial is bounded by an identity decision.

## Tensions to hold

- **Precision versus product.** Every honest weakness recorded here is a reason a
  cautious reader would ship only `hyperv_vm`; every one of them is also why the
  `wsl2` class is described in this much detail rather than named and trusted.
- **Two profiles of the container substrate** (rootful on governed nodes,
  rootless on personal ones) doubles the reconciliation surface and is the only
  way to serve both host classes honestly.
- **Source evidence versus release behaviour.** The architecture is settled by
  pinned source; the product is gated on measurements nobody has taken.
- **Owner authority versus fleet configuration.** The same control surface serves
  a personal owner who may not be overridden and a managed Cloud PC where the
  fleet sets the allocation.

## Recombination opportunities

- With [the device trust plane](omni-unattended-worker-synthesis-device-trust-plane.md)
  — worker registrations become executor-conditional Windows accounts.
- With [governed dispatch](omni-unattended-worker-synthesis-governed-dispatch.md)
  — the qualification record is the object gate 2 reads.
- With the estate's existing
  [governed worker execution](worker-execution-overview.md) host contract, which
  already describes enrolled hosts and digest-pinned benches.
- With the [workstation app shell](../staging/workstation-app-shell/workstation-app-shell.md)
  staged topic, which needs the same one-machine, two-principals separation for
  the human console.

## Open questions

- Does one qualification record cover a class, or does each executor+workload
  pair need its own?
- Who re-runs a qualification when Windows updates, and what happens to running
  work in the meantime?
- Can any Omni-scoped egress enforcement exist on the Windows side, or is
  Linux-side enforcement permanent for the `wsl2` class?
- What is the maximum concurrency a personal machine should be offered, given
  each attempt costs an account and a VM boundary?
