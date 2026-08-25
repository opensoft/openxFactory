# Recursive Inference Strategy Routing — Brainstorm

Status: brainstorm
Kind: architecture
Summary: xFactory should route among direct context, deterministic retrieval, compiled semantic context, and recursive inference according to task complexity, corpus structure, exhaustiveness, risk, and measured cost-quality rather than making RLM the default path.
Topics: governed-recursive-inference, inference-strategy-routing, routing, retrieval, semantic-context, context-compression, micro-agents, cost-quality-frontier, feat-request
Repository context: openxFactory (neutral strategy vocabulary and routing evidence); DomainxFactory repos (domain thresholds and task classifications)
Captured: 2026-07-30

## Possible feats

- **Inference-strategy vocabulary** — distinguish `direct`, `retrieval`,
  `compiled_context`, and `recursive` execution modes.
- **Deterministic strategy router** — select obvious paths from declared task,
  corpus, risk, and output properties before invoking a model planner.
- **Recursive eligibility classifier** — require evidence that adaptive
  decomposition is likely to outperform simpler paths.
- **Route explanation artifact** — record why a strategy was selected and which
  policy/evaluation version controlled it.

## Focus

Recursive inference adds planning, sandbox, child-call, reduction, and evidence
overhead. It is valuable when a model must reason densely across a corpus whose
useful partitions are not known in advance. It can be counterproductive for
simple lookups, short contexts, or tasks already served by a precise
deterministic pipeline.

The central routing question is not "Can this task use an RLM?" but "What is the
least complex strategy that meets the required quality and evidence band?"

## Candidate strategy spectrum

| Strategy | Strong fit | Weak fit |
| --- | --- | --- |
| `direct` | small bounded input; one model can reason over it reliably | oversized or highly distractor-dense corpus |
| `retrieval` | sparse evidence; known query; top-k evidence is sufficient | exhaustive aggregation or cross-shard consistency |
| `compiled_context` | known worker purpose and semantic neighborhood; repeatable task class | unknown evidence location or corpus-specific decomposition |
| `recursive` | large corpus; adaptive partitioning; dense aggregation; global consistency | simple retrieval, low latency, or poorly bounded output |
| deterministic map/reduce | uniform shards and known transformation | irregular corpus requiring adaptive questions |

These strategies compose. A recursive root may use governed retrieval
primitives, and leaf tasks may receive compiled semantic context. The route
names the dominant control pattern, not every internal operation.

## Eligibility signals

Potential positive signals for recursive inference:

- corpus exceeds a configured safe direct-context size;
- task requires aggregation over many or all items;
- relevance cannot be expressed as one stable search query;
- evidence is distributed across heterogeneous source classes;
- cross-shard relationships or contradictions matter;
- output requires a hierarchical artifact larger than one model response;
- prior direct or retrieval runs show measurable context-rot or coverage
  failures;
- the task repeats often enough to justify runtime overhead and evaluation.

Potential negative signals:

- one exact lookup or digest comparison solves the task;
- deterministic tooling already implements the transformation;
- the required latency is below recursive setup cost;
- the corpus cannot be safely materialized or brokered;
- evidence obligations cannot tolerate adaptive sampling;
- budget or provider limits cannot support the minimum child-call plan;
- no compatible verifier or evaluation suite exists.

## Routing flow

```text
validate job and context authority
  -> classify task/output/coverage requirements
  -> estimate corpus size, structure, sensitivity, and volatility
  -> check deterministic/direct/retrieval eligibility
  -> check recursive runtime, profile, budget, and eval readiness
  -> rank allowed strategies by measured cost-quality
  -> emit route explanation
  -> execute or escalate
```

The router should be deterministic for declared task classes. A model planner
may propose a strategy for unknown or ambiguous work, but the proposal must
validate against the active registry and policy.

## Fallback behavior

Recursive inference can fail before or during execution:

- capsule materialization failure;
- sandbox or provider unavailability;
- insufficient budget;
- child-call format or validation failure;
- incomplete coverage;
- root unable to produce a valid result.

Fallback should be declared per task class:

```text
fail_closed
degrade_to_direct
degrade_to_retrieval
return_partial_with_coverage
escalate_to_broader_worker
escalate_to_Hermes_or_human
```

Falling back must not silently change the evidence claim. A partial retrieval
answer cannot be presented as an exhaustive recursive analysis.

## Relationship to compression and caching

Context compression is worker-lane middleware that reduces provider tokens
after content is selected. Recursive inference is a control strategy for
selecting and decomposing content. Compression may help with structural tool
output, but it can also hide exact evidence needed by a leaf call.

Likewise:

- semantic-context caching reuses meaning packets;
- task-result caching reuses exact pure transformations;
- recursive inference decides what work to perform now.

The router may account for these optimizations, but it should not conflate them.

## Alternatives and tensions

- A model-based router can recognize subtle task complexity but adds cost and
  may over-select an elaborate strategy.
- Fixed context-size thresholds are easy to implement but ignore task density,
  model capability, and evidence requirements.
- Route choice can learn from telemetry, but automatic policy mutation would
  conflict with reviewed configuration and evaluation governance.
- A task may begin as retrieval and discover that exhaustive recursive analysis
  is needed; mid-run escalation requires a new route record and budget check.

## Open questions

- Which neutral task properties are sufficient to route without a model?
- Should strategy selection happen at the Hermes job, Omnigent graph, or worker
  invocation level?
- Can one job contain multiple strategy nodes, each independently routed?
- What minimum eval evidence allows a domain to activate `recursive` for a task
  class?
- How should model context-window improvements change thresholds without
  invalidating old route explanations?
- Is "deterministic map/reduce" a separate strategy or a constrained recursive
  profile with no adaptive root?

## Relationships

- [Hermes Retrieval Primitives](hermes-retrieval-primitives-contract.md)
  defines the governed sparse-retrieval path.
- [Ontology Semantic-Context Compilation](ontology-semantic-context-compilation.md)
  defines ahead-of-time semantic shaping.
- [Context Compression Runtime](../staging/context-compression-runtime/context-compression-runtime.md)
  defines neighboring token middleware.
- [Model Topology and Economics](governed-recursive-inference-model-topology-and-economics.md)
  supplies cost-quality evidence for routing.

