# Medical Domain Hermes and Omnigent Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: The medical-domain packet proposes a MedxFactory authority and worker
overlay that supports evidence-grounded reasoning while reserving consent,
clinical decisions, orders, and chart authority for humans and external
systems.
Topics: medical-domain, medxfactory, domain-hermes, omnigent
Repository context: openxFactory neutral/domain exploration informed by MedxFactory
Captured: 2026-07-28

## Possible feats

- **MedxFactory domain overlay** — clinical personas, task and worker
  contracts, evidence tiers, permission matrices, safety gates, and clinician
  handoff.

## Motivation

The Omnigent execution pattern is reusable beyond software, but medical work
has higher evidence, consent, safety, and human-authority requirements.
Software job names and merge gates cannot simply be relabeled as clinical
decisions.

## Goals

- Define the medical domain's decision and escalation roles.
- Map neutral worker archetypes into bounded medical workers.
- Preserve source trace, evidence tier, uncertainty, and contradiction.
- Enforce never-assignable human and external acts.
- Produce transparent convergence packets for clinical review.

## Non-goals

- This packet is not medical advice or a clinical protocol.
- Autonomous workers cannot diagnose, prescribe, sign orders, or write final
  charts.
- Domain Hermes does not own patient consent or care-organization policy.
- The packet does not claim the drafted roster is ratified.

## What the system delivers

MedxFactory could seed a domain roster and worker overlay, route bounded
reasoning jobs, collect evidence and safety review, assemble a decision
foundation, and hand it to the responsible clinician or system with unresolved
issues visible.

## System model

```text
subject scope + consent + care-org policy
  → Medx Domain Hermes authority and task framing
  → bounded medical worker fleet
  → evidence, verification, challenge, safety
  → convergence packet
  → clinician/external enforcement
```

## Cluster map

- [Governed Clinical-Domain Execution](medical-domain-synthesis-clinical-execution.md)
  — joins clinical authority to the medical worker envelope.

## How it fits

openxFactory owns neutral contracts; MedxFactory owns medical meaning and
overlays; Hermes supplies domain decisions and cross-layer routing; Omnigent
executes bounded tasks; clinicians and regulated systems retain clinical
authority.

## Key decisions and open questions

The non-negotiable is external enforcement for human-only clinical acts.
Open questions include roster ratification, qualification batteries,
care-organization overlays, evidence-tier requirements, and safe learning.

## Document map

### Synthesis

- [Governed Clinical-Domain Execution](medical-domain-synthesis-clinical-execution.md)

### Atomic explorations

- [Clinical Authority Boundary](medical-domain-clinical-authority-boundary.md)
- [Specialized Medical Worker Envelope](medical-domain-specialized-worker-envelope.md)

### Related source leaves

- [MedxFactory Domain Roster](medxfactory-domain-roster-draft.md)
- [Medical Omnigent Harness Adaptation](medical-omnigent-harness-adaptation.md)
