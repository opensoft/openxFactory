# Synthesis: Governed Clinical-Domain Execution — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Clinical authority boundaries and specialized worker envelopes
combine into a medical reasoning lane that produces reviewable foundations
while preserving clinician, patient, and care-organization authority.
Topics: medical-domain, clinical-authority, medical-harness, safety, synthesis
Repository context: openxFactory neutral pattern informed by MedxFactory
Captured: 2026-07-28

## Possible feats

- **MedxFactory governed reasoning lane** — route clinical-domain tasks
  through qualified workers, safety review, convergence, and explicit human
  enforcement.

## Members and their joints

Atomic members:
[Clinical Authority Boundary](medical-domain-clinical-authority-boundary.md)
and [Specialized Medical Worker Envelope](medical-domain-specialized-worker-envelope.md).

### Domain Hermes frames and governs

Named personas own reasoning standards, evidence curation, verification,
safety, documentation, and escalation. They select bounded worker activity
without claiming human-only clinical acts.

### Workers produce inspectable foundations

The medical overlay runs evidence retrieval, hypothesis generation,
verification, skepticism, safety checks, and draft assembly under declared
task and permission envelopes.

### Humans and external systems enforce

Clinicians, patients, care organizations, and regulated systems retain
consent, chart, order, and care authority. The convergence packet makes the
handoff and unresolved uncertainty visible.

## Emergent behavior

The lane can improve evidence organization and reasoning challenge without
presenting autonomous output as diagnosis, treatment, or final documentation.

## Tensions to hold

- Rich assistance can amplify automation bias.
- Strong separation protects authority while increasing workflow friction.
- Learning from outcomes must not move PHI or local clinical policy into
  neutral stores.

## Recombination opportunities

The packet uses the neutral
[Worker Execution](worker-execution-overview.md),
[Identity and Custody](identity-custody-overview.md), and
[Hermes Memory and Retrieval](memory-retrieval-overview.md) packets.

## Open questions

- What empirical qualification is required before each worker class is used?
- Which failures force the whole lane to stop?
- How are local care-organization policies composed with domain defaults?
