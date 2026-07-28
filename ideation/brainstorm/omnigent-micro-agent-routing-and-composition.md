# Omnigent Micro-Agent Routing and Composition — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Micro-agents should be composed by an observable orchestrator as a
typed acyclic task graph, using deterministic artifact and semantic routing
before model planning, parallelizing independent nodes, validating every edge,
and escalating ambiguity instead of allowing workers to call peers or broaden
their own scope invisibly.
Topics: omnigent, omnigent-domain-overlay, micro-agents, routing,
task-graph, typed-handoff, semantic-routing, parallel-execution,
failure-containment, escalation, model-tiering, feat-request
Repository context: openxFactory (neutral Omnigent routing and task-graph
contracts)
Captured: 2026-07-28

## Possible feats

- **Typed micro-agent task graph** — nodes are profile-bound tasks and edges are
  validated artifact types.
- **Deterministic pre-router** — route obvious work from declared input,
  output, purpose, and semantic types before invoking a planner.
- **Observable fan-out/fan-in** — parallel independent tasks with a distinct
  assembly or challenge step.
- **Escalation ladder** — retry, stronger model, challenge, broader worker, or
  Hermes review.

## Orchestrator-mediated composition

The default flow should be:

```text
Hermes-approved job
  -> deterministic task decomposition
  -> typed micro-task graph
  -> bounded workers
  -> edge validation
  -> challenge where policy requires it
  -> assemble-for-admission artifact
  -> Hermes decision
```

Direct free-form agent-to-agent conversation hides cost, context transfer,
scope growth, and failure lineage. If one worker's result feeds another, the
handoff should be a typed artifact through the orchestrator.

## Route cheap facts first

Many tasks can route without a model:

```text
input type + requested output type
+ ontology concept/relation IDs
+ purpose
+ required validations
-> compatible micro-agent profiles
```

An LLM planner is useful when the decomposition itself is ambiguous. It should
not be the default for a known `source_claim_set -> provenance_findings`
transformation.

## Task graph properties

The graph should be:

- acyclic for one bounded run;
- explicit about node inputs and output types;
- closed over approved profiles;
- versioned and traceable;
- deterministic where the same declarations imply the same structure;
- able to fan out independent items;
- able to fan in only through a declared assembler;
- bounded by job-level cost, time, and node ceilings.

Dynamic generation may instantiate more nodes from an approved template, but
it should not invent new worker profiles at runtime.

## Common composition patterns

### Map and reduce

```text
N source artifacts
  -> N parallel extractors
  -> one deduplicator
  -> one verifier
  -> one assembler
```

### Generate and challenge

```text
candidate generator
  -> independent challenger
  -> conflict-aware assembler
```

### Cascade by confidence

```text
cheap classifier
  -> accept high-confidence validated result
  -> route ambiguous result to stronger classifier
  -> route remaining conflict to Hermes review
```

### Deterministic guard around model work

```text
schema/digest preflight
  -> model transformation
  -> schema/semantic validator
```

## Failure containment

A failed node should invalidate only downstream nodes that depend on its
output. Independent branches may finish and preserve useful evidence.

Retry identity includes the exact task, input, profile, prompt, model,
toolchain, and semantic-context versions. A changed input or context is a new
attempt, not an identical retry.

The escalation ladder should be explicit:

1. deterministic retry for transient infrastructure failure;
2. one bounded repair for malformed output;
3. alternate or stronger compatible profile;
4. independent challenge or adjudication packet;
5. broader worker or Domain Hermes review.

## Prevent the agent zoo

Too many near-identical profiles create routing ambiguity and maintenance
cost. A new profile should prove:

- a distinct independently evaluable responsibility;
- a meaningfully smaller context or tool surface;
- better cost, latency, quality, or failure isolation;
- enough recurring volume to justify its lifecycle;
- no existing profile can cover the task through a typed parameter.

Profiles with low use or indistinguishable evaluation results should be
consolidation candidates.

## Open questions

- Which graph decisions belong to Hermes and which may be delegated to the
  Omnigent orchestrator after job approval?
- Can an assembler request one missing node, or must it return an incomplete
  packet for replanning?
- What graph width avoids saturating shared model and tool limits?
- When should a challenge worker see the generator's rationale versus only its
  claims and evidence?
- How should partial graph results be represented when the job escalates?

## Related brainstorms

- [Omnigent Micro-Agent Task Contract](omnigent-micro-agent-task-contract.md)
- [Ontology-Grounded Micro-Agent Routing](ontology-grounded-micro-agent-routing.md)
- [Ontology Maintenance Micro-Agent Fleet](ontology-maintenance-micro-agent-fleet.md)
