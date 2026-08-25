# Omnigent Micro-Agent System Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Omnigent micro-agents are proposed as narrowly scoped workers
selected and composed through typed task envelopes, then evaluated without
inheriting decision authority.
Topics: omnigent-micro-agent, omnigent, micro-agents, worker-execution
Repository context: openxFactory neutral exploration and domain overlays
Captured: 2026-07-28

## Possible feats

- **Governed micro-agent runtime contract** — define agent identity, task
  envelope, routing, composition, evaluation, and accounting interfaces.

## Motivation

Large general workers are flexible but expensive and difficult to qualify for
repeatable narrow work. Small agents can be cheaper and more testable only if
their boundaries and compositions remain explicit.

## Goals

- Keep each agent single-purpose and independently evaluable.
- Carry scope, tools, budget, and acceptance in a typed task envelope.
- Make routing and composition explainable.
- Feed outcomes into later selection without widening authority.

## Non-goals

- Micro-agents do not replace Hermes deciders or human authorities.
- This packet does not fix one model vendor or orchestration engine.
- A lower token cost is not sufficient evidence of acceptable quality.

## What the system delivers

The runtime can select a qualified narrow worker or a bounded composition,
record every handoff and artifact, evaluate the outcome, and expose cost and
quality evidence for future routing.

## System model

```text
typed task → eligible agents → route/composition → artifacts/evidence
     ↑                                               ↓
     └──────── policy and evaluation ← disposition ─┘
```

## Cluster map

- [Governed Micro-Agent Execution](omnigent-micro-agent-synthesis-governed-execution.md)
  — joins foundations, task contracts, routing, evaluation, and economics.

## How it fits

Omnigent supplies execution and external enforcement. Ontology compilation
may improve semantic routing. Crystallization may later replace stable,
recurrent micro-agent paths with governed software while retaining fallback.

## Key decisions and open questions

The key boundary is that route adaptation never changes permissions. Open
questions include cross-domain task portability, evaluator calibration, and
the threshold for composition versus a larger worker.

## Document map

### Synthesis

- [Governed Micro-Agent Execution](omnigent-micro-agent-synthesis-governed-execution.md)

### Atomic explorations

- [Micro-Agent Foundations](omnigent-micro-agent-foundations.md)
- [Micro-Agent Task Contract](omnigent-micro-agent-task-contract.md)
- [Micro-Agent Routing and Composition](omnigent-micro-agent-routing-and-composition.md)
- [Micro-Agent Evaluation and Economics](omnigent-micro-agent-evaluation-and-economics.md)
