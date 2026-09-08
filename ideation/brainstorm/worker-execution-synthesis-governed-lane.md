# Synthesis: Governed Worker Execution Lane — Brainstorm

Status: brainstorm
Kind: architecture
Summary: An enrolled host and an externally enforced job lifecycle combine
into a portable execution lane that can run autonomous work without owning
its admission or acceptance decision.
Topics: worker-execution, worker-host, job-lifecycle, omnigent-lane, synthesis
Repository context: openxFactory neutral worker execution plane
Captured: 2026-07-28

## Possible feats

- **Governed execution-lane runtime** — enroll hosts, advertise benches,
  schedule bounded jobs, broker leases, collect evidence, and hand results to
  external enforcement.

## Members and their joints

Atomic members:
[Governed Worker Host Contract](worker-execution-host-contract.md)
and [Governed Worker Job Lifecycle](worker-execution-governed-job-lifecycle.md).

### Enrollment makes a host eligible

The broker establishes host identity and supported enforcement features. A
current inventory shows which pinned benches and resources are ready.

### Admission binds one job

Routing matches task requirements to a qualified worker, compatible bench,
and healthy host. Authorization issues only the content and tool leases needed
for that job.

### External enforcement accepts or rejects outputs

The worker may frame, generate, verify, or challenge artifacts. CI, councils,
Hermes authorities, clinicians, or humans perform the acceptance action
appropriate to the domain.

## Emergent behavior

The same neutral lane can support software, medical, and other domain
overlays while each domain keeps its worker vocabulary, evidence, and
external enforcement.

## Tensions to hold

- General portability competes with domain-specific safety.
- Warm benches reduce latency while increasing patch and drift management.
- High autonomy requires stronger evidence and recovery, not fewer gates.

## Recombination opportunities

The lane can execute
[Omnigent micro-agents](omnigent-micro-agent-overview.md), consume the
[identity and custody trust plane](identity-custody-overview.md), and host
the medical domain overlay (MOVED 2026-09-07 to `MedxSoft/MedxFactory@74bed502`,
`ideation/brainstorm/medical-domain-overview.md`).

## Open questions

- What minimum host attestation is portable across deployment types?
- Which job records are tenant-private versus domain-learning evidence?
- What recovery path remains when the lane manages its own infrastructure?
