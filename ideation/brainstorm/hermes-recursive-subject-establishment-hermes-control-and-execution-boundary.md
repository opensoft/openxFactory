# Hermes Control and Execution Boundary — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Hermes should own recursive subject understanding and the durable evidence frontier while Omnigent, adapters, and external systems execute bounded transforms or authorized actions.
Topics: hermes-recursive-subject-establishment, hermes-control-execution-boundary, subject-hermes, omnigent, authority
Repository context: openxFactory neutral placement across Hermes, xFactory rails, Omnigent, adapters, and external enforcement
Captured: 2026-07-30

## Possible feats

- **Hermes recursive-establishment controller** — run bounded inference passes
  against Subject Hermes-owned episode state without creating a new Hermes
  layer or Omnigent archetype.
- **Typed establishment work request** — delegate OCR, extraction, retrieval,
  comparison, or approved outreach while preserving subject scope and lineage.

## Focus

The recursive strategy belongs logically in Hermes when the purpose is to
change xFactory's understanding of a subject. That does not imply that Hermes
should possess raw provider credentials, parse every modality itself, or
directly perform consequential external actions.

## Proposed model

```text
Subject Hermes
  owns purpose, partial subject model, frontier, gaps, readiness
       |
       v
Hermes RLM controller
  plans, selects evidence, asks bounded child questions, synthesizes
       |
       +--> tool-less reference model calls
       |
       +--> xFactory-gated work requests
               |
               +--> Omnigent transforms and specialist analysis
               +--> source adapters and retrieval brokers
               +--> authorized communication or record-request workflows
               +--> external enforcement and accountable humans
```

Reference model calls receive only bounded, redacted context and no tools. The
acting Hermes role may request tools only through the existing job, grant,
credential-reference, gate, and audit pathway. A child model answer is
evidence, not approval.

The RLM controller can adapt the next question based on results, but every
delegated job has explicit inputs, outputs, authority, budget, and stop
conditions. Child authority never exceeds the episode authority.

## Interfaces and boundaries

Hermes owns:

- the research or establishment purpose;
- which subject-model questions are open;
- the recursive frontier and stop rationale;
- candidate synthesis and readiness recommendation;
- requests to admit accepted knowledge into Subject Hermes objects.

Omnigent or adapters own:

- bounded computation over authorized source slices;
- modality-specific processing;
- provider calls under scoped grants;
- candidate artifacts with execution evidence.

External systems and accountable humans retain terminal authority for sending
records requests, changing ledgers or charts, making clinical decisions, or
applying subject setup.

This is a companion to the existing governed-recursive-inference position that
places task-local recursion inside an Omnigent worker. Both may reuse the same
typed context runtime, budget, trajectory, and coverage contracts while having
different roots and lifetimes.

## Alternatives and tensions

- Putting the entire loop in Omnigent preserves a simple execution architecture
  but makes a worker the de facto owner of subject memory and long-lived gaps.
- Putting every transform in Hermes makes layer ownership clear but overloads
  Hermes with parsing, sandbox, and provider concerns.
- A dedicated "Research Hermes" could centralize expertise but risks creating
  another authority-bearing layer and weakening per-subject isolation.

The leading position is a capability of each scoped Subject Hermes, not a new
global persona or service with standing access.

## Open questions

- Does the controller directly submit approved child templates or propose a
  task graph for validation?
- Which cheap deterministic operations can run within the Hermes context
  runtime without becoming Omnigent jobs?
- When should a domain expert Hermes join or challenge a Subject Hermes pass?
- Does one trajectory span both Hermes reasoning and delegated execution?

## Relationships

This boundary governs the [durable establishment episode](hermes-recursive-subject-establishment-durable-establishment-episode.md)
and composes with [authority, consent, and subject rights](hermes-recursive-subject-establishment-authority-consent-and-subject-rights.md).
The existing companion is the
[Governed Recursive Inference Overview](governed-recursive-inference-overview.md).

