# Synthesis: Context Strategy and Recursive Economics — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Recursive inference is one adaptive context strategy in a larger xFactory spectrum, and its route should be earned by task-specific evidence that the chosen model topology beats direct, retrieval, compiled-context, and deterministic alternatives at the required quality band.
Topics: governed-recursive-inference, context-strategy-and-economics, inference-strategy-routing, model-topology, context-capsule, typed-recursive-runtime, retrieval, semantic-context, context-compression, synthesis
Repository context: openxFactory (neutral context-strategy and evaluation relationship); DomainxFactory repos (task thresholds and eval suites)
Captured: 2026-07-30

## Possible feats

- **Adaptive context strategy registry** — register direct, retrieval,
  compiled, deterministic map/reduce, and recursive profiles with task-specific
  evaluation evidence.
- **Strategy cost-quality frontier** — rank compatible context strategies by
  accepted-result quality, coverage, latency, and total cost.
- **Recursive route calibration loop** — propose reviewed threshold changes
  from measured task-family outcomes.

## Members and their joints

Atomic members:

- [Strategy Routing](governed-recursive-inference-strategy-routing.md)
- [Model Topology and Economics](governed-recursive-inference-model-topology-and-economics.md)
- [Context Capsule](governed-recursive-inference-context-capsule.md)
- [Typed Runtime](governed-recursive-inference-typed-runtime.md)

Neighboring existing ideas:

- [Hermes Retrieval Primitives](hermes-retrieval-primitives-contract.md)
- [Ontology Semantic-Context Compilation](ontology-semantic-context-compilation.md)
- [Ontology-Compiled Context and Result Caching](ontology-compiled-context-and-result-caching.md)
- [Context Compression Runtime](../staging/context-compression-runtime/context-compression-runtime.md)

## Context work happens at several different layers

```text
source admission
  memory gateway / consent / source authority

meaning selection
  compiled semantic context

evidence access
  direct packet | retrieval | context capsule

context computation
  deterministic map/reduce | recursive runtime

provider transport
  optional compression

result reuse
  exact authorized caches
```

These mechanisms are complementary. Treating one as a replacement for all the
others would discard useful boundaries.

### Semantic compilation is ahead-of-time

A worker profile can know in advance which ontology terms, relations,
constraints, and reviewed examples it needs. Compiling that semantic
neighborhood reduces irrelevant meaning and makes runtime interpretation
reproducible.

Recursive inference is different: the system does not necessarily know which
source evidence matters until the root explores the particular corpus.

### Retrieval is sparse selection

Governed search is ideal when one or a few queries retrieve enough evidence.
It is weak for exhaustive aggregation, cross-shard consistency, or tasks where
the query itself evolves after evidence inspection.

An RLM may call retrieval primitives, but the recursive strategy adds adaptive
partitioning, child transformations, and reduction over an authorized corpus.

### A context capsule is external memory, not a strategy

The [capsule](governed-recursive-inference-context-capsule.md) can support a
deterministic map/reduce program as easily as an RLM. It defines what can be
computed over; the [strategy router](governed-recursive-inference-strategy-routing.md)
defines how.

### Compression optimizes transport

Headroom-style compression reduces provider-visible tool output. It does not
decide corpus scope, prove coverage, or replace recursive decomposition.
Evidence-bearing slices may need a no-compression policy even when structural
runtime output is compressible.

### Caching reuses prior artifacts

Semantic-context, index, child-result, and full-result caches can avoid work
under exact identities. Recursive routing decides whether uncached work should
be adaptive. Authorization, freshness, and validation still bind cache hits.

## Economic routing loop

```text
task classification + corpus profile + quality band
  -> compatible strategies
  -> historical eval and runtime evidence
  -> cheapest strategy meeting quality/coverage threshold
  -> execute under fixed route explanation
  -> record accepted-result outcome and cost
  -> propose reviewed calibration change
```

The loop changes policy only through reviewed configuration or contract
updates. A live worker cannot route itself into a more permissive strategy
because its recent run was difficult.

## Topology is part of the strategy

The same recursive control pattern can have very different economics:

```text
strong root + cheap leaves
homogeneous model
cheap root + specialist leaves
cheap-first cascade
generate + independent challenge
```

The route should identify the evaluated topology or compatible band, not just
the word `recursive`. Coverage, child count, provider mix, and verifier posture
are equally load-bearing.

## Strategy comparisons

Candidate evaluation matrix:

| Dimension | Direct | Retrieval | Compiled | Deterministic map/reduce | Recursive |
| --- | --- | --- | --- | --- | --- |
| setup overhead | low | medium | amortized compile | medium | high |
| adaptive evidence navigation | low | query-limited | low | low | high |
| exhaustive coverage | context-limited | weak by default | context-limited | strong for uniform tasks | possible with ledger |
| predictability | medium | high | high | high | lower |
| audit complexity | low | medium | medium | medium | high |
| best corpus | small | sparse relevance | known semantic slice | uniform partitions | large irregular/dense |

This is a hypothesis table, not benchmark evidence.

## Emergent behavior

Together, the context-strategy members create a system that can:

- avoid recursion for simple work;
- activate it only on approved task classes;
- choose a model topology supported by evals;
- combine worker-scoped semantics with corpus-specific exploration;
- preserve the same capsule and evidence boundaries across strategies;
- compare cost per accepted result rather than cost per model call;
- recalibrate through reviewed policy instead of model self-modification.

## Tensions to hold

- Stable deterministic routing improves reproducibility while model planning may
  recognize novel complexity.
- A single strategy vocabulary simplifies reporting while real workflows may
  combine several mechanisms.
- Cross-provider topologies may improve cost/quality but complicate privacy,
  billing, and replay.
- Compression and caching can make a recursive pilot look cheaper without
  proving the underlying strategy is efficient.
- As base context windows and models improve, recursive thresholds may move or
  some task classes may retire.

## Recombination opportunities

- Use ontology-grounded task signatures to route known transformations before
  invoking any strategy planner.
- Attach strategy and topology to the proposed micro-agent profile/task/result
  records.
- Feed accepted-result economics into the Domain Hermes efficiency mandate and
  Tenant/Subject accounting chain.
- Crystallize repeated recursive task families into deterministic or cheaper
  capabilities when the pattern ledger and consent gates justify it.

## Open questions

- Is `adaptive-context-runtime` the neutral capability, or is the strategy
  registry an extension of routing and worker-profile contracts?
- Which measurements are neutral enough for every domain?
- How are route thresholds updated when model providers change context windows,
  prices, or behavior?
- Should deterministic map/reduce be modeled beside recursion or as a
  zero-adaptivity recursive profile?
- When does a repeated recursive task become a crystallization candidate?

