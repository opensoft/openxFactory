# Specialized Medical Worker Envelope — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Medical Omnigent workers should use a neutral execution kernel with
domain-specific task types, evidence tiers, safety constraints, permissions,
and clinician handoff requirements.
Topics: medical-domain, omnigent, medical-harness, worker-archetypes
Repository context: openxFactory neutral execution boundary informed by MedxFactory
Captured: 2026-07-28

## Possible feats

- **Medical worker overlay contract** — declare worker classes, task
  envelopes, evidence sources, tool permissions, stop conditions, and
  external clinician enforcement.
- **Clinical convergence packet** — assemble hypotheses, evidence,
  uncertainty, contradictions, safety flags, and required human actions.

## Focus

This document isolates how the neutral worker lane becomes medically useful
without importing software-specific job vocabulary or granting clinical
authority.

## Proposed model

The medical overlay maps neutral worker archetypes—frame, generate, verify,
challenge, assemble, external enforcement—to named medical workers. Each task
envelope declares:

- subject and purpose scope;
- permitted evidence tiers and sources;
- tools and write permissions;
- safety stop conditions and escalation targets;
- uncertainty and contradiction reporting;
- required convergence-packet fields;
- clinician or external-system acceptance step.

## Interfaces and boundaries

The detailed mapping originates in
[Medical Omnigent Harness Adaptation](medical-omnigent-harness-adaptation.md).
The neutral host and job lifecycle come from the
[Worker Execution packet](worker-execution-overview.md).

## Alternatives and tensions

- Domain-specific schemas improve safety while reducing portability.
- A neutral archetype kernel aids reuse but may hide clinical distinctions.
- More worker specialization can improve challenge coverage and raise
  orchestration complexity.

## Open questions

- Which evidence tier is required for each worker class?
- How is a medical worker battery qualified and renewed?
- What parts of a convergence packet may leave the care organization?

## Relationships

The [clinical execution synthesis](medical-domain-synthesis-clinical-execution.md)
joins this envelope to the authority boundary.
