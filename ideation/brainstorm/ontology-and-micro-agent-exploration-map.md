# Ontology and Omnigent Micro-Agent Exploration Map — Brainstorm

Status: brainstorm
Kind: reference
Summary: This topic map separates the ontology and Omnigent micro-agent ideas
into small linked investigations, then identifies the three synthesis seams
where ontology-bounded context can make single-purpose workers faster, cheaper,
and more reliable without granting them authority.
Topics: ontology, xfactory-semantic-kernel, domain-ontology-lifecycle,
omnigent, omnigent-domain-overlay, micro-agents, semantic-context,
worker-archetypes, feat-request, doc-management, doc-workflow
Repository context: openxFactory (cross-factory ideation; future ontology and
Omnigent contract deltas)
Captured: 2026-07-28

## Possible feats

- **Ontology exploration cluster** — a coherent source set for refining
  `add-domain-ontology-layer` without turning brainstorm prose into policy.
- **Omnigent micro-agent contract** — a future `omnigent-domain-overlay`
  extension for small, typed, single-purpose worker profiles.
- **Worker-scoped semantic context** — compile only the ontology terms and
  relations a micro-agent needs for one task.
- **Semantic routing and caching** — select workers and reuse pure results by
  exact task, input, ontology, prompt, model, and toolchain identity.

## Why split the idea

"Add ontology" and "use small agents" are each too broad to reason about as one
artifact. Combining them too early hides several independent decisions:

- what the ontology means and who owns it;
- how a new domain fills and maintains it;
- what makes a worker a micro-agent rather than merely a short prompt;
- how micro-agents are selected, composed, measured, retried, and stopped;
- which semantic material belongs in each worker's context;
- when precomputation and caching are safe.

The document set keeps those questions separate and then reconnects them only
at the runtime seams where the combination creates leverage.

## Document map

### Foundations

- [Ontology Layer Foundations](ontology-layer-foundations.md) — meaning,
  strata, ownership, and the semantic/control-plane boundary.
- [Omnigent Micro-Agent Foundations](omnigent-micro-agent-foundations.md) —
  the definition and constitutional limits of a small single-purpose worker.

### Ontology-focused

- [Domain Ontology Generation Pipeline](domain-ontology-generation-pipeline.md)
  — how a newly generated domain gets a reviewable initial ontology.
- [Domain Ontology Maintenance and Drift](domain-ontology-maintenance-and-drift.md)
  — how Domain Hermes detects and governs semantic change.
- [Ontology Semantic-Context Compilation](ontology-semantic-context-compilation.md)
  — how a large ontology becomes a bounded runtime artifact.

### Micro-agent-focused

- [Omnigent Micro-Agent Task Contract](omnigent-micro-agent-task-contract.md)
  — typed inputs, outputs, permissions, tools, budgets, and stop rules.
- [Omnigent Micro-Agent Routing and Composition](omnigent-micro-agent-routing-and-composition.md)
  — deterministic routing, DAG composition, escalation, and failure
  containment.
- [Omnigent Micro-Agent Evaluation and Economics](omnigent-micro-agent-evaluation-and-economics.md)
  — quality, latency, token, cost, retry, and usefulness measurement.

### Combined speed and effectiveness

- [Ontology-Grounded Micro-Agent Routing](ontology-grounded-micro-agent-routing.md)
  — select a worker from semantic task and artifact types before invoking an
  LLM planner.
- [Ontology-Compiled Context and Result Caching](ontology-compiled-context-and-result-caching.md)
  — reuse bounded semantic packets and pure results under exact digest keys.
- [Ontology Maintenance Micro-Agent Fleet](ontology-maintenance-micro-agent-fleet.md)
  — a candidate-producing fleet that helps Domain Hermes maintain ontology
  quality without acquiring publication authority.

## Shared architectural spine

```text
Domain Hermes
  owns ontology meaning, review and release
        |
        v
xFactory semantic kernel + domain ontology package
        |
        v
purpose- and worker-scoped semantic context
        |
        v
Hermes-approved task graph
        |
        v
small Omnigent workers
  classify -> extract -> verify -> challenge -> assemble
        |
        v
typed artifacts + evidence + usage
        |
        v
Hermes decides; external enforcement acts
```

The shared invariant is that better semantic understanding improves selection
and execution, but never becomes authority.

## Questions that span the set

- Is a micro-agent a separately deployed profile, a parameterized worker
  template, or an ephemeral instance of either?
- How small can a semantic context become before missing relations reduce
  accuracy more than the smaller prompt improves speed?
- Which task classes are pure enough to cache?
- Which confidence and ambiguity signals require a stronger worker, a
  challenge worker, or Domain Hermes review?
- Should ontology-maintenance workers be a general Omnigent lane or a
  Domain-Hermes-specific worker fleet?

## Promotion posture

The ontology documents can refine the active
`add-domain-ontology-layer` proposal where they clarify generation,
maintenance, quality, or worker-scoped context. The general micro-agent
documents should remain a separate future proposal because they modify
Omnigent worker profiles, task routing, execution evidence, and efficiency
contracts beyond the ontology change's current scope.
