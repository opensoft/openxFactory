# Governed Practice Adoption Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Practice adoption is proposed as a traceable learning loop in which
Domain Hermes suggests, Client Hermes clears, Project Hermes realizes, and
outcome evidence updates future recommendations.
Topics: practice-adoption, practice-catalog, auto-clear-envelope, cost-accountability
Repository context: openxFactory cross-layer Hermes governance
Captured: 2026-07-28

## Possible feats

- **Three-layer practice adoption service** — structured suggestions,
  clearance routing, realization evidence, outcome accounting, and recurrence
  feedback.

## Motivation

The factory already contains practices, health evidence, review workflows,
and automation lanes, but improvement remains hand-wired. Direct autonomous
mutation would collapse observation, policy, implementation, and acceptance
into one unsafe actor.

## Goals

- Turn observed gaps into structured, deduplicable suggestions.
- Preserve the Domain-suggests, Client-clears, Project-realizes boundary.
- Reuse human-ratified clearance envelopes conservatively.
- Record implementation, spend, outcomes, and recurrence.
- Feed learning back without self-authorizing policy changes.

## Non-goals

- A nightly sweep does not merge changes.
- A domain suggestion does not bind a client or project.
- An auto-clear envelope cannot clear failed checks or forbidden risk classes.
- The ledger does not claim predicted savings as realized savings.

## What the system delivers

Operators receive a durable queue of evidence-bearing practice suggestions,
clearance decisions, project realization links, outcome records, and
anti-normalization alerts.

## System model

```text
practice catalog + observed gap
  → suggestion envelope
  → client clearance or escalation
  → project proposal and realization
  → outcome/cost evidence
  → domain learning and catalog revision
```

## Cluster map

- [Governed Practice Adoption Loop](practice-adoption-synthesis-governed-loop.md)
  — joins suggestion production to clearance, realization, and feedback.

## How it fits

Hermes supplies layer authority and observations. Omnigent may run bounded
scans and implementation jobs. OpenSpec and Speckit remain the governed
proposal and implementation path where changes cross their respective
boundaries.

## Key decisions and open questions

The loop requires separate identities for evidence production, clearance,
implementation, and approval. Open questions include ledger ownership,
auto-clear eligibility, cross-project learning, and cost-accounting
granularity.

## Document map

### Synthesis

- [Governed Practice Adoption Loop](practice-adoption-synthesis-governed-loop.md)

### Atomic explorations

- [Practice Suggestion Envelope](practice-adoption-suggestion-envelope.md)
- [Practice Clearance and Realization Ledger](practice-adoption-clearance-ledger.md)

### Related source leaves

- [Domain Practice Suggestion Generation](domain-practice-suggestion-generation.md)
- [Hermes-Governed Nightly Sweep](hermes-governed-nightly-sweep.md)
- [Practice Clearance and Project Realization](practice-clearance-and-project-realization.md)
- [Nightly-Sweep Council Clearance](nightly-sweep-council-clearance-rule.md)
- [Cost Accountability and Efficiency](cost-accountability-and-efficiency-model.md)
