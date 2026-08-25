# Synthesis: Governed Micro-Agent Execution — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A small-agent fleet becomes governable when task envelopes, routing,
composition, evaluation, and economics share one bounded execution record.
Topics: omnigent-micro-agent, micro-agents, routing, evaluation, economics, synthesis
Repository context: openxFactory and Omnigent domain-overlay exploration
Captured: 2026-07-28

## Possible feats

- **Micro-agent execution record** — bind task contract, route, composition
  graph, evidence, evaluation, spend, and disposition for one run.

## Members and their joints

Atomic members:
[Micro-Agent Foundations](omnigent-micro-agent-foundations.md),
[Micro-Agent Task Contract](omnigent-micro-agent-task-contract.md),
[Micro-Agent Routing and Composition](omnigent-micro-agent-routing-and-composition.md),
and [Micro-Agent Evaluation and Economics](omnigent-micro-agent-evaluation-and-economics.md).

### The task contract bounds specialization

Foundations keep an agent single-purpose; the task contract supplies typed
inputs, allowed tools, scope, budget, and acceptance conditions. Routing may
choose or compose agents only within that envelope.

### Evaluation closes routing without granting authority

Outcome, evidence quality, latency, and spend feed later route selection.
Evaluation may recommend a different agent or composition, but it cannot
widen permissions or silently change the task contract.

## Emergent behavior

The fleet can improve selection and economics while every run remains
replayable, inspectable, and subordinate to external acceptance.

## Tensions to hold

- Finer specialization can improve quality but increase orchestration cost.
- Adaptive routing needs outcome data without becoming self-authorizing.
- Composition improves coverage while making provenance and failure
  attribution harder.

## Recombination opportunities

The execution record can consume the
[ontology semantic-execution synthesis](ontology-synthesis-semantic-execution.md)
and run inside the
[worker-execution packet](worker-execution-overview.md).

## Open questions

- What is the smallest portable task-envelope kernel?
- Which evaluator outcomes are comparable across domains?
- When should several micro-agents be replaced by a crystallized capability?
