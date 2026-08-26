# Omnigent Micro-Agent Evaluation and Economics — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Each micro-agent profile should have a narrow evaluation suite and a
per-run cost ledger measuring validity, semantic accuracy, evidence support,
latency, tokens, retries, escalation, cache utility, and downstream acceptance,
so routing can favor the cheapest profile that meets the required quality
without training on private live subject data.
Topics: omnigent-micro-agent, omnigent, omnigent-domain-overlay, micro-agents, evaluation,
cost-accountability, latency, token-budget, quality-metrics, routing-policy,
cache-utility, model-tiering, feat-request
Repository context: openxFactory (worker evaluation, spend evidence and routing
feedback)
Captured: 2026-07-28

## Possible feats

- **Per-profile evaluation manifest** — fixtures, metrics, thresholds, and
  required negative cases for one narrow responsibility.
- **Micro-agent clock-in/out record** — task, model, effort, tokens, time,
  normalized cost, result, and acceptance.
- **Cost-quality frontier** — select the cheapest compatible profile that meets
  the workflow's quality threshold.
- **Profile retirement signal** — identify workers that add cost without
  measurable quality or containment benefit.

## Evaluate the narrow skill

Broad agent evaluation hides which capability failed. A micro-agent should be
tested on the transformation it owns:

| Worker | Primary metric |
| --- | --- |
| concept classifier | type accuracy and unknown detection |
| relation extractor | precision/recall over supported relations |
| citation verifier | supported/unsupported finding accuracy |
| entity resolver | merge/split accuracy |
| ambiguity challenger | material conflict recall |
| context compiler | required-term coverage and irrelevant-term ratio |
| result assembler | completeness without invented evidence |

Schema validity is necessary but not sufficient. A perfectly shaped
unsupported claim is still wrong.

## Per-run evidence

Every run should clock in and out with:

- task/profile/model/effort versions;
- input and semantic-context digests;
- output and validator results;
- token, time, tool-call, retry, and normalized cost;
- confidence and ambiguity;
- cache hit or miss;
- escalation path;
- downstream acceptance, rejection, or correction when available.

The evidence supports Domain Hermes efficiency review and Tenant/Subject cost
reporting without giving the worker authority over its own budget.

## Quality bands

Routing can use declared bands:

```text
routine
  cheap model, low/medium effort, deterministic validation

important
  stronger model or independent verification

contested
  challenge pair or council-style review

high impact
  artifact assembly for accountable Hermes/human decision
```

The domain defines thresholds. Worker profiles do not self-label a task as
low risk.

## Cost-quality frontier

The best profile is not always the cheapest invocation. It is the cheapest
profile that reliably meets the task's quality and escalation requirements.

Useful measures:

- cost per valid result;
- cost per accepted result;
- p50/p95 latency;
- first-pass schema and semantic validity;
- retry and escalation rate;
- false-confidence rate;
- downstream correction rate;
- cache-hit savings;
- context tokens per accepted result;
- marginal quality from challenge or stronger effort.

This makes it possible to detect a "cheap" worker that frequently escalates or
creates expensive downstream repairs.

## Feedback without unsafe self-modification

Evaluation may propose:

- a routing threshold change;
- a different model/effort band;
- a prompt or semantic-context profile revision;
- a new validation fixture;
- profile consolidation or retirement;
- an ontology gap candidate.

Those are reviewed configuration or ontology changes. The running fleet should
not rewrite its own profiles or active ontology from live outcomes.

Training or optimization data should use curated fixtures and reviewed,
de-identified patterns. Private subject data must not become a general worker
evaluation corpus by default.

## Open questions

- What normalized cost unit compares models, tools, benches, and human review?
- How long should downstream acceptance signals remain attributable to one
  micro-agent result?
- Which metrics are neutral versus domain-specific?
- How much volume is needed before changing a route or retiring a profile?
- Should challenge workers be evaluated for disagreement quality, final
  correctness, or both?

## Related brainstorms

- [Cost Accountability and Efficiency Model](cost-accountability-and-efficiency-model.md)
- [Omnigent Micro-Agent Task Contract](omnigent-micro-agent-task-contract.md)
- [Ontology-Compiled Context and Result Caching](ontology-compiled-context-and-result-caching.md)
