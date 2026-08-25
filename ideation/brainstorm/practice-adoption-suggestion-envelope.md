# Practice Suggestion Envelope — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A practice suggestion should be a non-mutating evidence packet that
names the observed gap, proposed capability, expected benefit, affected
layers, cost estimate, and authority required for disposition.
Topics: practice-adoption, suggestion-record, practice-catalog, gap-scan
Repository context: openxFactory three-layer practice-adoption exploration
Captured: 2026-07-28

## Possible feats

- **Practice-suggestion schema** — capture source profile, gap evidence,
  proposed adoption, expected effect, confidence, cost range, and next
  authority without authorizing implementation.

## Focus

This document isolates the handoff between autonomous observation and
governed clearance. The suggestion must be useful to Client and Project
Hermes while remaining incapable of approving itself.

## Proposed model

A suggestion envelope carries:

- a stable suggestion and recurrence identity;
- the practice profile and promoted capability being considered;
- pinned observations and the declared gap;
- affected tenant, repositories, and project subjects;
- expected quality, risk, and cost effects;
- compatibility and prerequisite notes;
- the proposing worker and layer-content revisions;
- a recommended disposition authority and expiry.

The envelope remains `suggested` until an authorized client or human process
clears, parks, rejects, or requests more evidence.

## Interfaces and boundaries

The envelope consumes read-only gap-scan and practice-catalog output. It emits
a proposal-shaped record to the clearance queue. It neither edits policy nor
creates an implementation branch.

Related sources:
[Domain Practice Suggestion Generation](domain-practice-suggestion-generation.md)
and [Hermes-Governed Nightly Sweep](hermes-governed-nightly-sweep.md).

## Alternatives and tensions

- A free-form narrative is easier to generate but harder to deduplicate and
  disposition.
- A rigid schema improves automation but may exclude novel practices.
- Confidence scores can aid triage yet imply precision the evidence does not
  support.

## Open questions

- Which fields are mandatory before client clearance?
- Does recurrence update one suggestion or create a linked observation?
- When should a stale suggestion be re-evaluated rather than expired?

## Relationships

Clearance and realization evidence are recorded by the
[Practice Clearance Ledger](practice-adoption-clearance-ledger.md).
