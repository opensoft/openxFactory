# Practice Clearance and Realization Ledger — Brainstorm

Status: brainstorm
Kind: register
Summary: A practice-adoption ledger should preserve each suggestion's
clearance, realization, cost, outcome, recurrence, and escalation history
without conflating recommendation with authority.
Topics: practice-adoption, practice-clearance, project-realization, cost-accountability
Repository context: openxFactory three-layer practice-adoption exploration
Captured: 2026-07-28

## Possible feats

- **Practice-adoption state ledger** — record suggest, clear, park, reject,
  realize, observe, revise, and retire transitions with actor and evidence.
- **Repeated-clearance sentinel** — detect recurring exceptions and require
  the policy or generator to be reconsidered.

## Focus

This document isolates the durable state and accounting surface after a
suggestion exists. It separates who recommends, who clears, who realizes, and
who evaluates the result.

## Proposed model

Each ledger entry binds:

- suggestion identity and exact revision;
- client clearance outcome and envelope evidence;
- any human acknowledgement or council verdict;
- project realization change, branch, and acceptance evidence;
- estimated and actual spend;
- observed quality, savings, regressions, and rollback;
- repeated-clearance and policy-normalization flags.

The state machine is append-only from the perspective of historical evidence.
Later corrections supersede a disposition rather than erasing it.

## Interfaces and boundaries

The ledger consumes the
[Practice Suggestion Envelope](practice-adoption-suggestion-envelope.md),
client policy decisions, project workflow evidence, and cost records. It does
not perform a merge or decide whether a project accepts the practice.

Related sources:
[Practice Clearance and Project Realization](practice-clearance-and-project-realization.md),
Nightly-Sweep Council Clearance (MOVED 2026-09-07 to `opensoft/codexFactory@83c9c35a`,
`ideation/brainstorm/nightly-sweep-council-clearance-rule.md`),
and [Cost Accountability and Efficiency](cost-accountability-and-efficiency-model.md).

## Alternatives and tensions

- A single cross-layer ledger improves traceability but needs strict tenant
  and subject visibility rules.
- Append-only evidence aids audit while correction and erasure duties may
  require redacted successor records.
- Counting savings can reward adoption volume rather than actual outcomes.

## Open questions

- Which layer owns the canonical ledger?
- How are project-private outcome details summarized for domain learning?
- What recurrence threshold triggers a generator or policy repair?

## Relationships

The [governed adoption-loop synthesis](practice-adoption-synthesis-governed-loop.md)
joins this ledger to suggestion production.
