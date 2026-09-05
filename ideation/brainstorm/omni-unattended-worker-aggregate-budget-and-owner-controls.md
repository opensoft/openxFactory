# One Aggregate Budget and Durable Owner Controls — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The owner consents to ONE aggregate contribution budget per host, owned
by the host manager, with host-service and virtualization overhead reserved
first and every executor declaring which limits it ENFORCES versus merely
MEASURES — and the owner's controls are durable desired state, so pause survives
reconciliation, job completion and remote policy, and no remote act can raise
the consented allocation.
Topics: omni-unattended-worker, aggregate-budget, owner-controls,
worker-execution, consent, cost-accountability
Repository context: Omnigent-Install owns the host manager and its enforcement;
xFactory-Installer owns the owner-facing surface; openxFactory owns the neutral
resource and consent contracts
Captured: 2026-09-05

## Possible feats

- **A whole-host contribution budget** — one number the owner sets that covers
  every worker, container, distro and native process Omni runs.
- **Enforced-versus-measured declared per executor** — an honest capability
  statement instead of a slider that promises more than the runtime delivers.
- **Durable pause** — an owner decision that reconciliation, job completion,
  updates and remote policy cannot undo.

## Focus

What the owner actually gets to decide, and what the runtime can actually
enforce — kept as two statements that must be reconciled rather than one that
is assumed.

## Proposed model

**One budget per host, owned by the manager.** Host-service and virtualization
overhead is reserved FIRST; images, writable disks, caches, downloads, logs and
retained artifacts are accounted inside the disk budget. If an overhead spike
exhausts the reserve, the manager reduces admission or stops work rather than
overrunning the owner's consent.

**Units are stated, always.** A processor allocation is a COUNT, not a
percentage; a guest-RAM ceiling excludes some host overhead; a bandwidth target
is not a hard cap unless the adapter enforces one. Per-user maxima do not sum
into a host guarantee. Mapping any of these to an owner-visible "percentage of
my machine" requires measurement, and until it is measured the UI should not
show one.

**Each executor declares what it enforces.** VM memory and processor ceilings on
the hypervisor class; per-account WSL configuration on the WSL class; cgroup
limits inside the distro subject to their own delegation prerequisites. What an
executor only MEASURES is reported as a measurement, never as a guarantee.

**Durable states**, visible to the owner and to dispatch: `available`,
`draining`, `paused`, `stopped`, `repairing`, `enrollment-required`. Normal pause
denies admission and drains running work within a visible bound. Stop-now cancels
and destroys the current attempts. Local controls work with no network.
Reconciliation, updates and remote policy MUST NOT silently undo a pause or
raise the consented allocation — the estate has already recorded pause being
undone by job completion and reconciliation as a real defect class, not a
hypothetical one.

**Personal defaults are conservative**: battery-aware, schedule-aware, and never
waking a sleeping machine unless the owner enabled it. GPU work is offered only
for profiles whose access, isolation and resource limits are qualified — CPU
support never implies GPU support.

**Installed, enrolled, connected and ready are four different states.** Readiness
requires current authority AND a working, eligible executor; model access is
required only for profiles that use it. When a profile is unavailable, the UI
says which of those four is missing and why.

**Removal.** Stops admission and execution, disables services, removes owned keys
and execution state, and preserves the owner's unrelated software and data. An
online removal also retires the server-side registration and outstanding
authority; an offline one cannot, so outstanding permissions remain bounded by
their expiry and the owner's web control can revoke independently. Deleting a
local cache is not secure erasure.

## Interfaces and boundaries

Consumes: the owner's consented allocation and schedule; per-executor capability
declarations; measured overhead.

Emits: admission decisions, durable state, capacity advertisement, and the
reasons a profile is unavailable.

Owns: the aggregate budget and the durability of owner intent.

Does NOT own: what a job is allowed to see (gate 1) or where it runs (the
executor's own limits), and it never grants a containment class.

## Alternatives and tensions

- **Per-container or per-distro caps as the control.** What is easiest to
  implement and what the original design was warned about: a cap on one
  container is not a host-wide limit.
- **A single owner-facing percentage.** Best product surface, least honest
  mapping. The alternative — counts, ceilings and a measured matrix — is truthful
  and harder to present.
- **Owner authority versus fleet policy.** On a personal machine owner intent
  wins and remote policy may not raise the allocation. On a dedicated managed
  Cloud PC the fleet configures the allocation, and "the owner" is an
  administrator. The same control surface serves two different authority models,
  and the boundary between them is not fully drawn here.
- **Drain bounds versus job length.** A visible drain bound and a long-running
  job are in direct tension; the resolution is either a maximum job runtime per
  profile or a cancellation the owner can accept, and neither is settled.

## Open questions

- What are the actual default allocations, and what is the minimum viable
  contribution below which a host should not be admitted?
- What is the visible drain bound, and what happens to an attempt that exceeds
  it?
- Which limits does each executor genuinely enforce on the supported builds —
  the measurement that turns this from design into a matrix?
- How is the owner's consent to the `wsl2` class's disclosed residual recorded,
  and re-confirmed when the qualification changes?
- Does the managed path share this control surface, or does the fleet get a
  different one?

## Relationships

- [Executor ladder](omni-unattended-worker-executor-ladder.md) — the classes
  whose enforcement capabilities this depends on.
- [Host manager topology](omni-unattended-worker-host-manager-topology.md) — the
  process that owns the budget and the reconciler that must not undo pause.
- [Heartbeat batch envelope](omni-unattended-worker-heartbeat-batch-envelope.md)
  — how state and capacity are reported.
- [Synthesis: sandboxed execution](omni-unattended-worker-synthesis-sandboxed-execution.md)
  — the cluster this belongs to.
- [Tenant Project Catalog and Engineer Workstation Projection](tenant-project-catalog-and-workstation-cache.md)
  — the neighbouring rule that a workstation keeps only scoped local state.
