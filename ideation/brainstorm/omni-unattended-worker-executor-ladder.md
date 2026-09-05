# The Executor Ladder and Containment Classes — Brainstorm

Status: brainstorm
Kind: architecture
Summary: One host manager offers several executors, each qualified once per
supported configuration and advertised as a named containment class —
`hyperv_vm`, `wsl2`, `native_service_account` — with the job declaring the class
it requires and no silent downgrade or upgrade in either direction, so Windows
Home is served by a real class rather than by "profile unavailable".
Topics: omni-unattended-worker, executor-ladder, worker-execution,
containment-class, omnigent-lane
Repository context: openxFactory owns the neutral execution and job contracts;
Omnigent-Install owns the executor adapters and their qualification records
Captured: 2026-09-05

## Possible feats

- **Containment classes as first-class contract objects** — a job declares the
  class it needs, a host advertises the classes it has qualified, and dispatch
  matches them, instead of trusting a backend's name.
- **Versioned qualification records** — evidence per configuration, so a class
  means something measured on a build rather than asserted in prose.
- **A Home-capable personal product** — coverage for the machines the accepted
  product intent puts first.

## Focus

How one host manager can serve very different Windows machines without either
pretending they are equivalent or refusing the majority of them.

## Proposed model

Three classes today. Each is qualified once per supported configuration, and the
qualification record is versioned and names the actual permitted workloads.

| Class | Where it runs | The boundary it offers | The weakness recorded with it |
| --- | --- | --- | --- |
| `hyperv_vm` | Windows Pro/Enterprise with the Hyper-V role; Windows 365 Cloud PCs with nested virtualization enabled | One VM per job attempt from a signed, digest-pinned Ubuntu 24.04 base with docker-ce inside; fresh writable disk; no host mounts, clipboard, interop or host Docker socket; default-deny network with an allowlist enforced outside the guest. VM lifecycle belongs to the virtualization service, so a Windows service can create and start it with nobody signed in | Needs a base-image pipeline (build, sign, pin) that does not exist yet. Absent on Windows Home |
| `wsl2` | Windows Home, and any host without the Hyper-V role | A distro owned by a dedicated deny-interactive Omni Windows account, which places it in that account's own utility VM and kernel, separate from the owner's WSL; hardening is Linux-side and root-owned (see [the distro atomic](omni-unattended-worker-wsl2-worker-owned-distro.md) and [rootless Docker](omni-unattended-worker-rootless-docker-hardening.md)) | A wider management surface than a dedicated VM — interop, the 9P/drvfs file path, the localhost relay — and the Hyper-V firewall for WSL is machine-wide, so host-enforced egress control is NOT claimed for this class |
| `native_service_account` | Governed nodes only | The existing runner and rider services on managed hardware | Not a sandbox for arbitrary code on personal hardware, and never offered there |

**A job declares its required class.** A host that has not qualified that class
does not receive that job, and the owner UI says why. There is no silent
fallback DOWN to a weaker boundary and no silent promotion UP into a class the
job was not authorized for. This is the containment gate of the
[three policy gates](omni-unattended-worker-three-policy-gates.md) expressed as
a matching rule.

**Naming is not evidence.** An earlier draft called the WSL class
`wsl2_hardened`; the settled name is `wsl2`, because a class earns its
permitted-workload list from a qualification record, not from an adjective.

**Windows 365 nested virtualization is ONE prerequisite for BOTH VM classes.**
WSL2 is itself a Hyper-V utility VM, so on the managed path a single
prerequisite check serves `hyperv_vm` and `wsl2` alike. Supported SKU, region
and GPU exclusions still apply and belong in the qualification record.

**Brett's ruling, verbatim, for Windows Home:** "Documented partial WSL2 class."
Jobs admitted on Home carry public inputs and no secrets; the residual risk —
LAN reach from the VM, and standard-account reads after a kernel exploit — is
disclosed to the owner at consent; and Home is admitted only AFTER the
qualification record exists from a real Home laptop.

## Interfaces and boundaries

Consumes: host facts (edition, virtualization availability, TPM, memory); a
qualification record per class and configuration; the job's declared class.

Emits: the classes this host currently offers, as an observation on the
heartbeat — an observation, never a self-granted permission.

Owns: the class vocabulary and the matching rule.

Does NOT own: the internal hardening of any one class (each atomic owns its
own), nor the decision to release inputs to the host.

## Alternatives and tensions

- **Hyper-V only** (the earlier recommended architecture). Strongest single
  boundary, cleanest lifecycle story, and no personal product on Home. The
  review pass that recommended it said explicitly that essential Home coverage
  "changes the executor decision"; this is that change.
- **A ladder implies a total ordering.** The later review pass preferred an
  executor SET with per-class capabilities over a ladder of security levels,
  because the classes differ in kind — administration trust, backend type and
  containment guarantee are separate axes — not only in strength. The word
  "ladder" is kept for its no-silent-downgrade discipline; the matching is
  capability-based, and this tension is unresolved in the naming.
- **Qualify once per class versus per configuration.** Per configuration is
  honest and expensive; per class is cheap and overclaims. The settled position
  is per configuration, which makes the supported matrix a measured artifact.
- **Home coverage versus workload coverage.** Serving Home at all means
  admitting a class whose egress control is not host-enforced. The mitigation is
  a narrower admitted workload, not a stronger adjective.

## Open questions

- What exactly must a qualification record contain to admit a class — Windows
  build, kernel, image digest, network policy proof, privilege proof, cleanup
  proof, resource-control proof?
- Who signs a qualification record, and what expires it when a Windows build
  changes underneath it?
- Is there a fourth class for governed Linux hosts, or does that arrive with the
  deferred VPS option?
- How does a job express "any class at or above X" without re-introducing the
  total ordering the second review pass warned against?

## Relationships

- [WSL2 worker-owned distro](omni-unattended-worker-wsl2-worker-owned-distro.md)
  — the Windows-side ownership rule that makes the `wsl2` class possible.
- [Rootless Docker hardening](omni-unattended-worker-rootless-docker-hardening.md)
  — the Linux-side hardening the `wsl2` class is qualified on.
- [Host manager topology](omni-unattended-worker-host-manager-topology.md) — the
  process that owns these executors.
- [Three policy gates](omni-unattended-worker-three-policy-gates.md) — where the
  class is matched against a job's requirement.
- [Synthesis: sandboxed execution](omni-unattended-worker-synthesis-sandboxed-execution.md)
  — the cluster this belongs to.
- [Governed Worker Execution Overview](worker-execution-overview.md) and its
  [host contract](worker-execution-host-contract.md) — the estate's existing
  neutral execution vocabulary.
