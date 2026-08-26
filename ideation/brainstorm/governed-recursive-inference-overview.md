# Governed Recursive Inference Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: xFactory can use Recursive Language Models as a governed adaptive context-computation strategy that externalizes large corpora while preserving typed tasks, monotone authority, finite budgets, coverage evidence, safety rails, and Hermes-owned decisions.
Topics: governed-recursive-inference, adaptive-context-runtime, recursive-language-models, omnigent, context-packet, memory-gateway, micro-agents, routing, audit, cost-accountability, feat-request
Repository context: openxFactory (neutral cross-factory architecture); Omnigent-Install and DomainxFactory repos (runtime and domain specialization)
Captured: 2026-07-30

## Possible feats

- **Adaptive context runtime** — a neutral capability selecting among direct,
  retrieval, compiled, deterministic, and recursive context computation.
- **Governed recursive inference contract family** — context capsule, runtime
  profile, subordinate task family, limits, trajectory, coverage, and assurance
  records.
- **codexFactory recursive evidence pilot** — prove the approach against a
  real large engineering corpus and strong non-recursive baselines.
- **Council-ready recursive evidence compiler** — assemble one cited,
  coverage-aware packet for independent Hermes review.
- **Domain adoption profiles** — progressively qualify OpsxFactory,
  LedgerxFactory, and MedxFactory task classes under their own stricter safety
  and evidence rules.

## Motivation

Modern model context windows are finite, expensive, and prone to degraded
reasoning as inputs become large or densely interconnected. xFactory routinely
works over corpora that can exceed a useful single prompt:

- multiple repositories, diffs, checks, review threads, and governance
  artifacts;
- fleet logs, configurations, tickets, and runbooks;
- ledgers, policies, reconciliations, and audit evidence;
- longitudinal records and large expert-source collections;
- the xFactory documentation lifecycle itself.

The Recursive Language Model (RLM) research pattern offers a promising
inference-time response: keep the large corpus in an external environment, let
a root model inspect and partition it programmatically, launch bounded model
calls over selected pieces, and assemble the result.

Research references:

- [Recursive Language Models](https://arxiv.org/abs/2512.24601)
- [Official RLM implementation](https://github.com/alexzhang13/rlm)
- [Think, But Don't Overthink: Reproducing Recursive Language Models](https://arxiv.org/abs/2603.02615)
- [Typed lambda-RLM exploration](https://arxiv.org/abs/2603.20105)

The research mechanism does not by itself supply xFactory's authority,
consent, tenant isolation, typed artifacts, coverage, budget, or admission
model. This packet explores the adaptation needed to combine them.

## Goals

- Process corpora larger or denser than one reliable model context.
- Let a worker adaptively discover useful partitions without gaining
  unrestricted provider, filesystem, memory, or network access.
- Preserve the five Omnigent archetypes and six-boolean permission boundary.
- Make every child call, context selection, reduction, and cost traceable.
- Distinguish cited evidence from corpus coverage.
- Route simple work through simpler strategies.
- Evaluate recursive inference by task-specific quality and cost per accepted
  result.
- Keep all outputs advisory or candidate artifacts until existing Hermes,
  human, and external-enforcement gates act.

## Non-goals

- No sixth `recursive` worker archetype.
- No RLM-owned approval, memory promotion, credential grant, or terminal action.
- No unrestricted Python or host-process REPL in a production governed lane.
- No direct worker access to memory, knowledge, vector, graph, or source
  providers.
- No assumption that recursion is better for every long input.
- No unbounded recursion, fan-out, retries, time, tokens, or spend.
- No automatic policy or profile rewriting from live trajectories.
- No first-wave autonomous Medx diagnosis, chart write, order, or treatment
  decision.
- No silent promotion of this brainstorm packet into a contract or
  implementation plan.

## What the system delivers

If the ideas prove out, a governed recursive task would provide:

- an immutable, purpose-bound context capsule over authorized source shards;
- a worker-scoped semantic context that supplies meaning separately from
  evidence;
- a typed context-computation runtime instead of unrestricted host code;
- subordinate child tasks restricted to approved profiles and narrower views;
- a shared family budget and depth/call/fan-out/time limits;
- coverage modes and a manifest-denominated coverage ledger;
- provenance-preserving claim and reduction artifacts;
- a structured trajectory with explicit replay expectations;
- sandbox, injection, data-isolation, provider, and disclosure controls;
- task-specific model topologies and strategy-routing evidence;
- an assurance packet suitable for verifier, challenger, council, Hermes, or
  human review.

## System model

```text
Subject / Tenant / Domain Hermes
  intent, policy, consent, budget, approval
                    |
                    v
xFactory rails
  workflow + source authority + memory gateway + routing + trace
                    |
                    v
authorized context capsule
  immutable shards + digests + purpose + TTL + sensitivity
                    |
                    v
strategy router
  direct | retrieval | compiled | deterministic | recursive
                                                    |
                                                    v
                              bounded Omnigent worker
                                existing archetype
                                recursive strategy
                                                    |
                              +---------------------+------------------+
                              |                                        |
                              v                                        v
                     typed context runtime                    global family limits
                     inspect/search/slice                     depth/calls/tokens
                     partition/map/reduce                     cost/time/output
                              |                                        |
                              +---------------------+------------------+
                                                    |
                                                    v
                                      subordinate micro-task family
                                      narrower context and authority
                                                    |
                                                    v
                                  claims + provenance + coverage + trajectory
                                                    |
                                                    v
                                    verify / challenge / assemble-for-admission
                                                    |
                                                    v
                                  Hermes / accountable human / external gate
```

The governing invariant is:

```text
child authority <= parent worker authority <= Hermes-approved job authority
```

## Cluster map

- [Synthesis: Runtime and Authority](governed-recursive-inference-synthesis-runtime-and-authority.md)
  — joins placement, context capsule, typed runtime, task lineage, and finite
  budgets.
- [Synthesis: Evidence and Safety](governed-recursive-inference-synthesis-evidence-and-safety.md)
  — relates admitted, inspected, and disclosed context to coverage,
  provenance, trajectory, replay, privacy, and containment.
- [Synthesis: Context Strategy and Recursive Economics](governed-recursive-inference-synthesis-context-strategy-and-economics.md)
  — positions recursion beside retrieval, semantic compilation, deterministic
  map/reduce, compression, caching, model topology, and cost-quality routing.
- [Synthesis: Adoption and Councils](governed-recursive-inference-synthesis-adoption-and-councils.md)
  — proposes codexFactory-first qualification, council evidence compilation,
  and progressively stricter domain activation.

## How it fits

### Reuses existing xFactory authority

Hermes continues to own intent, policy, consent, memory, budget approval, and
decision. The xFactory layer continues to own contracts, routing, gates,
traceability, source authority, and audit. Omnigent executes bounded work.
External systems and accountable humans retain terminal action.

### Extends context packets rather than bypassing them

The memory gateway already provides bounded customer and expert context
packets. A context capsule would represent the large externalized corpus case
under those same rails, either as a new referenced artifact or an explicit
contract extension.

### Reuses worker archetypes and micro-agent ideas

Recursive inference is a worker execution strategy. Child calls can reuse the
profile/task/result separation, typed handoffs, validation, stop, escalation,
and cost evidence proposed by the existing Omnigent micro-agent packet.

### Complements semantic-context compilation

Semantic compilation chooses the worker's bounded ontology neighborhood ahead
of time. Recursive inference explores the job-specific evidence corpus at
runtime. Meaning and evidence stay separately pinned.

### Complements retrieval

Search primitives remain the efficient path for sparse relevance. Recursive
inference is reserved for adaptive decomposition, dense aggregation, global
consistency, or hierarchical output.

### Sits above context compression

Compression optimizes provider transport after selection. Recursive inference
decides how to select and decompose context. Evidence-bearing slices may need
to bypass compression even when structural runtime output uses it.

### Feeds cost accountability and crystallization

The recursive task family provides a natural clock-in/out and cost unit.
Repeated stable recursive families may later become candidates for a
deterministic or crystallized capability, but only through the existing pattern
ledger, consent, build, and admission gates.

## Leading design positions

These positions appear strongest, but remain brainstorm proposals:

1. RLM is an inference strategy, not a new archetype or authority.
2. The adaptive RLM node lives inside an explicit typed workflow graph.
3. A capsule manifests authorized external context; it does not grant provider
   credentials.
4. A production lane uses typed combinators and a sandbox, not unrestricted
   host execution.
5. Child calls are subordinate micro-tasks whose scope can only narrow.
6. One root budget binds the whole family; depth one is the initial ceiling.
7. Coverage is separate from citations and confidence.
8. General telemetry, governed execution evidence, and exact egress evidence
   have different content and retention profiles.
9. Recursive routing must beat strong non-recursive baselines for one declared
   task class.
10. codexFactory is the first domain pilot; MedxFactory is a later
    high-assurance decision-support consumer, if qualified.

## Key decisions and open questions

### Capability shape

- Is the neutral capability `adaptive-context-runtime`,
  `governed-context-computation`, or a name explicitly containing RLM?
- Are capsule, task-family, trajectory, coverage, and assurance separate
  records or coordinated extensions of existing families?

### Runtime control

- Does the root invoke approved child templates directly or submit a child
  graph for validation?
- What minimal typed combinator library preserves the useful adaptive behavior?
- Is a governed runtime specialized from tech benches or separately manifested?

### Context and data

- Which sources are immutable snapshots versus brokered live handles?
- What is the right shard granularity and child subset proof?
- Which data classes are excluded from recursive inference?

### Evidence and replay

- Which task outputs require targeted, sampled, partitioned, or complete
  coverage?
- What replay level is required by each domain?
- Which evidence tier stores prompts, slices, outputs, and exact provider
  disclosure?

### Economics and rollout

- Which codexFactory task gives the strongest pilot ground truth?
- What improvement threshold justifies recursive activation?
- When does a repeated recursive family become a crystallization candidate?
- What evidence permits a move from codexFactory to OpsxFactory,
  LedgerxFactory, or MedxFactory?

## Document map

### Synthesis documents

- [Runtime and Authority](governed-recursive-inference-synthesis-runtime-and-authority.md)
- [Evidence and Safety](governed-recursive-inference-synthesis-evidence-and-safety.md)
- [Context Strategy and Recursive Economics](governed-recursive-inference-synthesis-context-strategy-and-economics.md)
- [Adoption and Councils](governed-recursive-inference-synthesis-adoption-and-councils.md)

### Atomic documents

- [Placement](governed-recursive-inference-placement.md)
- [Context Capsule](governed-recursive-inference-context-capsule.md)
- [Typed Runtime](governed-recursive-inference-typed-runtime.md)
- [Recursive Task Family](governed-recursive-inference-task-family.md)
- [Strategy Routing](governed-recursive-inference-strategy-routing.md)
- [Budget and Depth Control](governed-recursive-inference-budget-and-depth-control.md)
- [Evidence and Coverage](governed-recursive-inference-evidence-coverage.md)
- [Trajectory and Replay](governed-recursive-inference-trajectory-and-replay.md)
- [Safety and Data Boundaries](governed-recursive-inference-safety-and-data-boundaries.md)
- [Model Topology and Economics](governed-recursive-inference-model-topology-and-economics.md)
- [Domain Pilots](governed-recursive-inference-domain-pilots.md)

