# Recursive Model Topology and Economics — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Recursive inference should select root, leaf, reducer, and verifier models as an evaluated topology and judge total cost per accepted result against simpler baselines rather than assuming recursion, smaller models, or more calls are inherently cheaper.
Topics: governed-recursive-inference, model-topology, cost-accountability, token-budget, evaluation, model-tiering, cost-quality-frontier, caching, latency, feat-request
Repository context: openxFactory (neutral usage and evaluation evidence); DomainxFactory repos (task-specific quality thresholds and fixtures); Tenant Hermes (spend policy)
Captured: 2026-07-30

## Possible feats

- **Recursive model-topology profile** — declare compatible root, leaf,
  reducer, challenger, and verifier bands.
- **Cost-per-accepted-result evaluation** — compare recursive topologies to
  direct, retrieval, and deterministic baselines.
- **Branch-yield telemetry** — measure unique evidence, accepted claims, and
  coverage gained per child call.
- **Topology retirement signal** — identify recursive profiles that add cost or
  latency without measurable quality benefit.

## Focus

An RLM is not necessarily one model calling identical copies of itself.
xFactory can combine different models, efforts, and worker profiles across the
root, leaves, reducer, and verifier. That creates optimization opportunities
and a large configuration space.

The relevant economic unit is the accepted task result, including retries,
failed branches, verification, escalation, and downstream correction.

## Candidate topologies

### Homogeneous

One model and effort for root, leaves, and reduction. Simple to evaluate and
replay; may waste strong-model capacity on routine extraction.

### Strong root, cheap leaves

A stronger root plans partitions and synthesizes; cheaper leaves perform
bounded extraction or classification. This is the most obvious first economic
hypothesis.

### Cheap root, specialist leaves

A deterministic or small planner routes work to domain-specialized profiles.
Useful when decomposition is easy and leaf interpretation is hard.

### Tiered cascade

Cheap leaf attempts first; malformed, ambiguous, or low-confidence partitions
escalate to stronger compatible profiles.

### Generate/challenge

One topology produces candidate claims; an independent model/profile checks
coverage, contradictions, or source support before assembly.

## What to measure

Per family and topology:

- first-pass valid-result rate;
- claim correctness and source support;
- coverage completion and conflict recall;
- false-confidence and downstream correction rates;
- root, child, reduction, validation, and escalation tokens;
- model/provider monetary cost;
- sandbox, gateway, and tool cost;
- p50/p95 latency and queue time;
- parallelism and provider-rate-limit pressure;
- branch yield and duplicate-work ratio;
- partial, failed, stopped, and escalated rates;
- cache-hit savings where reuse is allowed;
- cost per valid result and cost per accepted result.

Quality thresholds belong to the domain and task band. The cheapest topology
that fails the required quality is not efficient.

## Required baselines

Every pilot should compare recursive inference against:

```text
direct long-context model
governed retrieval plus synthesis
compiled semantic context plus one bounded worker
deterministic map/reduce where applicable
current human or agent workflow
```

The RLM paper reports strong gains on several long-context tasks, including
inputs beyond base context windows. A later reproduction reports that depth one
can help some complex aggregation tasks while harming simple retrieval and
that deeper recursion can sharply increase latency. These are research signals,
not proof for xFactory workloads.

References:

- [Recursive Language Models](https://arxiv.org/abs/2512.24601)
- [Official RLM implementation](https://github.com/alexzhang13/rlm)
- [Think, But Don't Overthink: Reproducing Recursive Language Models](https://arxiv.org/abs/2603.02615)
- [Typed lambda-RLM exploration](https://arxiv.org/abs/2603.20105)

## Caching

Possible cache layers:

- compiled semantic contexts;
- deterministic capsule indexes;
- pure child-task results over immutable slices;
- validated reduction outputs;
- full recursive task results.

A result-cache key may need:

```text
task/profile/prompt/model/effort
runtime/combinator/toolchain/validator versions
all input and capsule-view digests
semantic-context digest
purpose, policy, freshness, and coverage mode
```

Authorization still precedes lookup and disclosure. A different topology or
model may require a miss even when input bytes match.

Initial pilots should measure without broad cross-request result reuse so cache
savings do not hide the true execution cost or introduce stale semantics.

## Latency and parallelism

Recursive work can reduce model context size but increase wall time through
planning and multiple calls. Parallel leaves reduce latency until provider,
network, sandbox, or rate limits saturate.

The optimum graph width is likely task- and provider-specific. Evaluation
should include:

- serial root overhead;
- batch and parallel child-call behavior;
- slowest-partition tail latency;
- cancellation of low-yield branches;
- final verification and assembly time;
- comparison with one long-context call.

## Cost attribution

Each child clocks in/out under the root task family. The family clocks out to
the directing Hermes persona and tenant/subject accounting chain with:

- total usage;
- allocation by root/leaf/reducer/verifier;
- accepted output and coverage band;
- avoided or duplicated work;
- estimated baseline cost;
- downstream acceptance or correction when known.

The runtime enforces limits; reviewed policy changes routing/topology based on
evidence.

## Alternatives and tensions

- Cheap leaves can increase total cost if they frequently fail or trigger
  expensive repair.
- Strong roots can plan better but spend heavily before reading evidence.
- Heterogeneous providers improve specialization but expand data-egress,
  residency, billing, and replay complexity.
- Caching improves economics but complicates authorization and evaluation.
- Parallel fan-out lowers latency but can create correlated failure and rate
  spikes.

## Open questions

- Which normalized cost unit compares hosted models, local inference, tools,
  sandbox compute, and human review?
- Must the profile pin exact models or compatible quality/cost bands?
- How much evaluation volume is needed before a topology becomes routable?
- Should branch-yield estimates influence allocation during a run?
- When is a stronger single long-context model preferable even if its token
  price is higher?
- Which cached results remain valid after a model or validator change?

## Relationships

- [Recursive Budget and Depth Control](governed-recursive-inference-budget-and-depth-control.md)
  enforces the economic envelope.
- [Recursive Strategy Routing](governed-recursive-inference-strategy-routing.md)
  chooses whether recursion is justified.
- [Omnigent Micro-Agent Evaluation and Economics](omnigent-micro-agent-evaluation-and-economics.md)
  supplies the narrow worker evaluation pattern.
- [Ontology-Compiled Context and Result Caching](ontology-compiled-context-and-result-caching.md)
  supplies the content-addressed cache distinction.

