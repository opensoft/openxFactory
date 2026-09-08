# Rootless Docker as the Linux-Side Hardening Candidate — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Inside the Omni distro the job runs as an unprivileged Linux user under
a rootless Docker daemon while `wsl.conf`, the nftables egress policy and the
cgroup configuration stay root-owned and out of the workload's reach — a NEW
execution profile distinct from today's rootful container engine, whose honest
claim is "escaping requires another privilege escalation", not "requires a
kernel exploit".
Topics: omni-unattended-worker, rootless-docker-hardening, executor-ladder,
worker-execution, containment-class
Repository context: Omnigent-Install owns the container-engine substrate step
and would gain this profile; openxFactory owns the neutral containment
vocabulary the qualification record reports against
Captured: 2026-09-05

## Possible feats

- **A qualified Home containment profile** — public-input engineering work on a
  personal laptop with a boundary that was measured rather than named.
- **Root-owned policy inside a worker-owned VM** — configuration the workload
  can neither read around nor rewrite for the next start.
- **Boundary tests from an assumed-compromised account** — a qualification
  method that starts where the attacker starts, not inside an intact container.

## Focus

Given that the Omni distro is worker-owned and separate from the owner's WSL,
what must be true INSIDE it before arbitrary public engineering code may run
there.

## Proposed model

**The shape.** Rootless `dockerd` under the distro's unprivileged runtime user;
jobs execute as that unprivileged Linux user; `wsl.conf`, the nftables policy
and the cgroup/delegation configuration are owned by root and unreachable from
the workload. Compromising the rootless daemon does not confer distro root, so
the root-owned policy survives a container escape.

**The precise claim.** Escaping this profile "requires another privilege
escalation". It is not "requires a kernel exploit", and the difference matters
because the weaker phrasing is the one that gets quoted at an owner.

**Conditions, all accepted from the review pass that proposed them:**

1. **No alternative privilege path.** No sudo entitlement for the job user, no
   rootful Docker socket, no privileged management interface reachable from a
   job.
2. **Protect the Windows round trip.** A job must not reach Windows execution as
   the distro owner and then call `wsl.exe -u root`. Root-owned
   `[interop] enabled=false` and no drvfs mounts are essential, not optional.
   The qualification must also enumerate host loopback listeners reachable
   through the localhost relay, because the Hyper-V firewall's `LoopbackEnabled`
   setting is machine-wide and cannot be assumed off.
3. **Enforce the ACTUAL egress path.** Rootless networking translates container
   traffic into locally originated unprivileged socket calls made BY the
   rootless user, so the root-owned nftables policy must match that user's own
   traffic (an owner match), not only forwarded traffic. The policy must be
   active before any workload starts.
4. **Resource limits are a qualification item.** Rootless cgroup limits need
   cgroup v2 with systemd delegation; WSL's kernel command line in `.wslconfig`
   is something to verify per configuration, not a default to assume.
5. **This is a NEW execution profile.** The current substrate step enables the
   system Docker service as root. Rootless is not a configuration tweak of it;
   it is a second profile with its own step, its own detection and its own
   qualification.
6. **Test from an assumed-compromised runtime account.** The qualification runs
   its boundary tests as the compromised Linux user, not only from inside an
   intact container. Passing those tests is what makes the Home class
   defensible; rootless alone does not.

**What it still does not give.** No host-enforced egress control (that is the
machine-wide firewall problem the `wsl2` class declines to claim), no protection
of the owner's data from the owner's own administrator, and no assurance about
where a job actually executed.

## Interfaces and boundaries

Consumes: a worker-owned distro whose root the workload does not hold; a
root-owned network and cgroup policy; a signed base rootfs.

Emits: a qualification record naming the tested build, the policy in force and
the permitted workload class.

Owns: the in-distro privilege boundary.

Does NOT own: Windows-side ownership and startup — that is
[the distro atomic](omni-unattended-worker-wsl2-worker-owned-distro.md) — nor
input release, which is decided server-side before dispatch.

## Alternatives and tensions

- **Rootful Docker inside the worker distro.** What the estate does today, and
  acceptable on a governed node where administration is trusted. On a personal
  machine it puts daemon control one container escape away.
- **Hypervisor isolation instead** (`hyperv_vm`). Strictly stronger and
  unavailable on Home; the entire reason this profile is being qualified.
- **Gvisor, Kata, or a user-namespace runtime under a rootful daemon.** Not
  examined in the review lineage; a real option space this document deliberately
  leaves open rather than closing by omission.
- **Complexity versus assurance.** Rootless Docker inside WSL2 with systemd
  delegation and nftables owner-matching is a lot of moving parts to maintain on
  hardware nobody administers, and every part is a qualification item that can
  silently regress with a Windows or distro update.
- **Two profiles, one substrate step.** Carrying rootful and rootless profiles
  side by side doubles the reconciliation surface; collapsing them loses the
  governed node's simpler, faster path.

## Open questions

- Which host loopback listeners are reachable through the localhost relay on the
  supported builds, and does anything Omni installs add one?
- Does cgroup v2 with systemd delegation hold under the supported WSL kernels
  without a custom kernel command line?
- What is the exact boundary-test set run from the compromised runtime account,
  and who reviews its results?
- Does the base rootfs come from the same signed, digest-pinned pipeline the VM
  class needs, or a separate one?
- Is there a supported way to make egress enforcement Omni-scoped on the Windows
  side, or is Linux-side enforcement the permanent answer for this class?

## Relationships

- [WSL2 worker-owned distro](omni-unattended-worker-wsl2-worker-owned-distro.md)
  — the Windows-side half of the same class.
- [Executor ladder](omni-unattended-worker-executor-ladder.md) — where this
  qualification turns into an advertised class.
- [Three policy gates](omni-unattended-worker-three-policy-gates.md) — the gate
  that consumes the qualification.
- [Synthesis: sandboxed execution](omni-unattended-worker-synthesis-sandboxed-execution.md)
  — the cluster this belongs to.
