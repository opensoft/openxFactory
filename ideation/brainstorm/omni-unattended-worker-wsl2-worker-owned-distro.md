# The WSL2 Distro Belongs to the Worker Account, Not to SYSTEM — Brainstorm

Status: brainstorm
Kind: architecture
Summary: WSL2 runs one utility VM per Windows user, so an Omni distro registered
to a dedicated deny-interactive worker account sits in its own VM and kernel
apart from the owner's WSL — and because the pinned WSL source rejects session
creation for LocalSystem, SYSTEM can never own or see that distro, which flips
the host app's step order so the worker identity is established BEFORE any
distro work and every registration, start, detection and retirement runs under
that identity with its profile loaded.
Topics: omni-unattended-worker, wsl2-worker-owned-distro, executor-ladder,
worker-execution, worker-host
Repository context: Omnigent-Install owns the host app steps and the WSL
substrate; CloudPC-Install's worker-host and service-rider packs carry the same
ownership question; openxFactory owns the neutral execution contract
Captured: 2026-09-05

## Possible feats

- **A worker-owned Linux environment on a personal machine** — an Omni distro
  that never touches, adopts or modifies the owner's own WSL installation.
- **Session-0 executor startup** — a Windows service logging on as the worker
  account, with its profile loaded, as the executor's home.
- **Worker-context detection** — a marker produced under the worker identity
  that a SYSTEM-run detection can read, replacing detection commands SYSTEM
  cannot execute.

## Focus

Who OWNS the Linux environment on a Windows host, and what follows mechanically
from that ownership for registration, startup, detection and teardown.

## Proposed model

**The boundary claim, stated precisely.** Two distros under ONE Windows user
share that user's utility VM and kernel and are not independent security
boundaries. ACROSS Windows users, WSL2 instantiates a separate utility VM per
user, so a distro owned by an Omni worker account does not share a kernel with
the owner's WSL. What is weaker than a dedicated Hyper-V VM is the MANAGEMENT
surface, not the VM boundary.

**The source finding, reported as a source finding.** The Microsoft WSL session
factory (`LxssUserSessionFactory.cpp` at commit `556440f3`) finds sessions by
the Windows user SID, the user-session object owns a utility-VM member, and the
factory REJECTS session creation for LocalSystem. This is read from source at a
pinned commit; it settles the architecture, not the behaviour of any particular
installed release, which remains a qualification item.

**Consequences, all accepted into the settled design.**

1. **SYSTEM can never own a distro.** The host app's existing `substrate_wsl`
   step runs in caller context — from a managed install that caller is SYSTEM —
   and therefore cannot register the worker's distro at all.
2. **The step order flips.** SYSTEM installs machine prerequisites and
   establishes the dedicated Windows executor identity FIRST; `worker_identities`
   moves BEFORE distro work. Registration, startup, reconciliation, detection and
   retirement then run under that identity.
3. **How SYSTEM runs work as that identity.** The estate already solves this:
   rotate-at-bind holds the account password transiently and binds per-worker
   scheduled tasks and the runner service to it. A Windows service logging on as
   the worker account loads its profile, and that service is the executor's home.
   `wsl --import` and every later `wsl.exe` call run there, never from the
   supervisor.
4. **`wsl.exe --user` does not help.** It selects a LINUX user inside the distro
   and never changes the Windows owner.
5. **Detection must be re-homed.** Intune detection runs as SYSTEM and therefore
   cannot call `wsl.exe --list --quiet` to see the worker's distro. Detection
   consults a marker or probe result produced under the worker identity. The
   existing detection questions in the worker-host and host-token-broker packs
   are wrong for this class.
6. **Per-attempt hygiene.** One attempt per VM boundary; `wsl --shutdown` as the
   worker account between attempts; one Omni-only Windows account per concurrent
   attempt, because a fresh distro under the SAME account still shares that
   account's running utility VM. Deleting one distro's writable disk is not a
   kernel reset. A failed cleanup makes capacity unavailable until repaired; it
   is never a reason to reuse a suspect environment.

**Management-surface weaknesses, stated plainly rather than settled by a
setting.** `[automount] enabled=false` prevents automatic mounting but does NOT
prohibit manual mounting or `fstab` entries; `appendWindowsPath=false` is not
the same switch as disabling interop. The Hyper-V firewall's WSL scope is
identified by a VM-creator id COMMON to WSL, and its documented
`LoopbackEnabled` behaviour permits host loopback outside ordinary rules — so
setting WSL's default outbound policy to Block is neither an Omni-only egress
boundary nor a complete denial of host access, and it would touch the owner's
unrelated WSL. That is why the `wsl2` class does NOT claim host-enforced egress
control and pushes enforcement Linux-side.

**On the governed rider host** the existing runner service account IS the worker
context, so the distro belongs to that account; rootful Docker remains
acceptable there because the rider is a governed node. The OWNERSHIP rule is the
same on both.

## Interfaces and boundaries

Consumes: a dedicated deny-interactive Windows account and its transient
credential at bind time; machine prerequisites installed by SYSTEM.

Emits: a registered worker-owned distro, its startup service, a worker-context
detection marker, and a retirement path.

Owns: the Windows-side ownership and lifecycle of the Linux environment.

Does NOT own: what runs INSIDE the distro or how it is hardened — that is
[rootless Docker hardening](omni-unattended-worker-rootless-docker-hardening.md)
— nor the owner's own WSL configuration, which is never touched.

## Alternatives and tensions

- **A SYSTEM-owned distro per host, with a root shim and an allowlisted docker
  subcommand set.** Proposed as a fallback in the first review pass, REJECTED in
  the next (an allowlist cannot exclude `--privileged`, host mounts, or daemon
  control, and it widens privilege at the exact moment the preferred design has
  failed), and now understood as INFEASIBLE rather than merely unwise if the
  source finding holds on the installed release. Both reasons are worth keeping:
  one is a policy judgment, the other a platform fact.
- **Per-account `.wslconfig` as the resource control.** It is read from the
  invoking user's profile, so a host-wide cap means one file per worker account
  written by the supervisor plus separate accounting for native processes — and
  per-user maxima do not sum into a host guarantee. See
  [aggregate budget](omni-unattended-worker-aggregate-budget-and-owner-controls.md).
- **One distro serving several logical workers** versus one Windows account per
  concurrent attempt. The first is cheaper and shares a kernel between mutually
  untrusted attempts; the second is the settled rule and costs accounts.
- **Trusting the source finding versus qualifying the release.** The design
  treats the source as architecture-settling and the release as unproven. If the
  installed build behaves differently, the step-order flip is still correct — it
  is simply less forced.

## Open questions

- Does a service logging on as the worker account start and keep its distro
  alive through the utility VM's idle shutdown, across a reboot, with nobody
  signed in? This is the first qualification measurement on both host classes.
- Do the Hyper-V firewall rules for WSL bind per user or per host on the
  supported builds?
- What exactly is the worker-context detection marker, and who writes it?
- How many concurrent Omni accounts is a personal machine willing to carry?
- Does the rider pack adopt the same ownership rule in its own amendment, and
  what are the four facts it must then state — Windows owner SID, distro, Linux
  execution user, engine endpoint?

## Relationships

- [Executor ladder](omni-unattended-worker-executor-ladder.md) — the class this
  serves.
- [Rootless Docker hardening](omni-unattended-worker-rootless-docker-hardening.md)
  — the Linux-side half of the same class.
- [Host manager topology](omni-unattended-worker-host-manager-topology.md) — the
  step machine whose order this flips.
- [Synthesis: sandboxed execution](omni-unattended-worker-synthesis-sandboxed-execution.md)
  — the cluster this belongs to.
- [Workstation App Shell](../staging/workstation-app-shell/workstation-app-shell.md)
  — the staged topic that already separates the human console's OS principal
  from the worker's on one machine.
