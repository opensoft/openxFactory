# Governed Worker Execution Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: The worker-execution packet proposes enrolled hosts, digest-pinned
toolchain benches, bounded job leases, observable execution, and external
acceptance as one neutral Omnigent lane.
Topics: worker-execution, omnigent-lane, tech-benches, worker-enrollment
Repository context: openxFactory neutral execution contracts and domain overlays
Captured: 2026-07-28

## Possible feats

- **Portable worker execution plane** — enrollment, bench inventory,
  scheduling, leases, job lifecycle, evidence, accounting, and closeout.

## Motivation

xFactory has worker definitions, toolchain benches, approval gates, and
emerging enrollment, but an autonomous lane needs an explicit host and job
lifecycle before Hermes can manage it safely.

## Goals

- Enroll and identify worker hosts.
- Advertise verified bench capabilities and health.
- Route one bounded task to a qualified worker and compatible host.
- Broker short-lived content and tool access.
- Collect evidence, spend, and failure state.
- Keep admission and external acceptance outside worker authority.

## Non-goals

- A host heartbeat does not authorize tenant access.
- A worker cannot approve or merge its own output.
- The neutral contract does not hard-code software job types.
- Self-hosting is not the first activation milestone.

## What the system delivers

Operators can see eligible hosts and benches, follow each governed job from
admission through closeout, inspect artifacts and cost, revoke access, and
route outputs to the proper domain enforcement.

## System model

```text
enroll host → verify benches and health
task + authority → route worker/bench/host
  → issue short-lived leases
  → execute and observe
  → collect artifacts/evidence/cost
  → external evaluation and enforcement
  → close and revoke
```

## Cluster map

- [Governed Worker Execution Lane](worker-execution-synthesis-governed-lane.md)
  — joins host eligibility to one externally enforced job lifecycle.

## How it fits

Hermes decides and routes governed intent. Omnigent executes. Domain overlays
define worker classes and evidence. The trust plane supplies identity and
custody decisions. Project workflows and external systems accept or reject
results.

## Key decisions and open questions

The central boundary is that execution never inherits acceptance authority.
Open questions include attestation, lease transport, retry identity,
multi-tenant host policy, self-hosting recovery, and cross-domain evidence
portability.

## Document map

### Synthesis

- [Governed Worker Execution Lane](worker-execution-synthesis-governed-lane.md)

### Atomic explorations

- [Governed Worker Host Contract](worker-execution-host-contract.md)
- [Governed Worker Job Lifecycle](worker-execution-governed-job-lifecycle.md)

### Related source leaves

- [Tech-Stack Benches](tech-stack-benches.md)
- [Omnigent Lane Activation](omnigent-lane-activation-path.md)
