# Ontology-Grounded Micro-Agent Routing — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Omnigent can route many micro-tasks without an LLM planner by matching
the task's exact ontology concept, relation, activity, input-artifact, and
requested-output types against prevalidated worker semantic signatures,
reserving model planning and stronger workers for ambiguous or unmatched work.
Topics: ontology, xfactory-semantic-kernel, omnigent,
omnigent-domain-overlay, micro-agents, semantic-routing, worker-selection,
task-signature, deterministic-router, model-tiering, feat-request
Repository context: openxFactory (semantic-kernel to Omnigent routing seam)
Captured: 2026-07-28

## Possible feats

- **Worker semantic signature** — declare accepted concept, relation, activity,
  input, and output types for each micro-agent profile.
- **Deterministic semantic router** — select compatible profiles before model
  planning.
- **Ambiguity-aware fallback** — route unmatched or contested semantics to a
  planner, challenger, or Hermes review.
- **Route explanation artifact** — record why a worker matched and which
  ontology/package version supplied the meaning.

## The central idea

A task often arrives with more routing information than a natural-language
prompt reveals:

```text
purpose: verify_provenance
input type: source_claim_set
output type: provenance_findings
semantic roots: claim, source, evidence
required relation: extracted_from
```

If worker profiles declare the same types, routing is a deterministic
compatibility query.

## Worker semantic signature

```yaml
semantic_signature:
  profile: citation-verifier
  purposes: [verify_provenance]
  accepts:
    artifacts: [source_claim_set]
    concepts: [xfactory:claim, xfactory:source]
    relations: [extracted_from, supported_by]
  emits:
    artifacts: [provenance_findings]
  context_profile: citation-verification
  ambiguity_policy: escalate
```

The signature describes competence and context needs. It does not grant access
to any instance of those types.

## Routing pipeline

```text
validate task and package pins
  -> resolve task semantic types
  -> filter profiles by purpose and input/output compatibility
  -> filter by active domain overlay and toolchain availability
  -> filter by permissions, budget, quality band and stop rules
  -> rank compatible profiles by measured cost/quality
  -> instantiate exact task
```

Only if no unambiguous route remains:

```text
bounded planner
  -> proposed decomposition or profile
  -> validate against active registry
  -> execute or escalate
```

The planner may choose among approved profiles. It cannot invent an
unregistered worker with new tools or permissions.

## Speed benefits

- no planning model call for routine transformations;
- no broad worker discovery prompt;
- precompiled semantic context profile is known at route time;
- compatible workers can be kept warm or scheduled near required tools;
- independent items can fan out immediately;
- cost/quality data can select the cheapest sufficient profile.

## Effectiveness benefits

- terms are interpreted under the exact domain ontology pin;
- a worker receives only tasks matching its declared competence;
- unknown or contested types are visible instead of guessed;
- routing explanations are reproducible;
- validators can reject output types or relations outside the signature;
- profile gaps become measurable ontology/worker candidates.

## Avoid semantic overreach

An ontology relation such as `patient has encounter` does not authorize the
patient record to be sent to an encounter classifier. Routing runs after the
existing job scope, grants, consent, memory rails, and context-packet rules
have selected the permitted evidence.

Similarly, a semantic match does not mean a worker is qualified for a
high-impact decision. It means only that the worker is compatible with the
bounded transformation.

## Ambiguity classes

- **unknown term** — ontology maintenance candidate;
- **multiple exact profile matches** — rank by domain policy and evaluation;
- **multiple semantic interpretations** — challenge or Domain Hermes review;
- **missing output type** — task contract error;
- **missing context profile** — worker-profile gap;
- **unavailable toolchain** — scheduling failure, not semantic failure.

## Open questions

- Should semantic signatures live in the domain overlay or in separate worker
  profile documents?
- How are subtype matches ranked against exact matches?
- When may one generic worker accept any subtype under a kernel parent?
- What route explanation is sufficient for audit without logging private task
  content?
- How should semantic routing interact with Hermes Mixture of Agents presets?

## Related brainstorms

- [Ontology Semantic-Context Compilation](ontology-semantic-context-compilation.md)
- [Omnigent Micro-Agent Routing and Composition](omnigent-micro-agent-routing-and-composition.md)
- [Ontology-Compiled Context and Result Caching](ontology-compiled-context-and-result-caching.md)
