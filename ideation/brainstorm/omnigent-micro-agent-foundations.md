# Omnigent Micro-Agent Foundations — Brainstorm

Status: brainstorm
Kind: architecture
Summary: An Omnigent micro-agent should be an ephemeral or tightly scoped
worker profile with one responsibility, typed inputs and outputs, a minimal
tool and semantic-context set, explicit budgets and stop rules, and no
decision or enforcement authority, allowing larger workflows to compose many
cheap verifiable steps instead of relying on one broad agent.
Topics: omnigent-micro-agent, omnigent, omnigent-domain-overlay, micro-agents, single-purpose-agent,
worker-profile, worker-archetypes, typed-artifacts, task-envelope,
failure-containment, cost-accountability, feat-request
Repository context: openxFactory (neutral Omnigent worker and overlay
contracts)
Captured: 2026-07-28

## Possible feats

- **Micro-agent profile contract** — one purpose, input family, output family,
  semantic context profile, tool set, budget, cache rule, and escalation path.
- **Typed micro-task envelope** — exact scope, artifacts, expected output,
  ontology pin, validation, and stop conditions.
- **Ephemeral worker instances** — no durable authority or implicit memory
  between tasks.
- **Micro-agent composition graph** — orchestrated typed handoffs with
  validation at every edge.

## Working definition

A micro-agent is not merely an agent with a short prompt. It is a constrained
execution unit:

```text
one responsibility
+ one accepted input family
+ one emitted output family
+ one bounded semantic context
+ one small tool allowlist
+ one budget
+ explicit stop and escalation rules
= micro-agent
```

The profile is reusable; the worker instance is short-lived. One profile may
run many isolated instances over different artifacts.

## Fit with the existing Omnigent model

The ratified Omnigent overlay maps every worker class to one neutral archetype:

```text
frame
generate
verify
challenge
assemble_for_admission
```

A micro-agent specializes one archetype; it does not introduce a sixth kind of
authority. Examples:

| Micro-agent | Archetype | Typed result |
| --- | --- | --- |
| claim atomizer | frame | atomic claim candidates |
| relation extractor | generate | relation candidates |
| citation verifier | verify | provenance findings |
| ambiguity challenger | challenge | contested interpretations |
| candidate packet assembler | assemble_for_admission | review packet |

The terminal action still belongs to Hermes, an accountable human, or the
external enforcement system.

## Why small agents can be better

- Less context reduces prompt tokens and irrelevant attention.
- Narrow tools reduce discovery and unsafe action surface.
- Typed outputs make deterministic validation practical.
- Small steps can run in parallel when their inputs are independent.
- Failures affect one step instead of invalidating a long opaque run.
- Different steps can use different model/effort tiers.
- Pure results can sometimes be cached by exact inputs and versions.
- Evaluation can measure one skill instead of a blended end-to-end outcome.

The trade-off is orchestration overhead. A workflow split into dozens of
trivial agents can become slower and harder to understand than one bounded
worker. The useful unit is the smallest independently verifiable semantic
transformation, not the smallest possible prompt.

## Constitutional boundary

Every micro-agent remains an Omnigent worker:

- it advises or produces artifacts;
- it receives no raw secrets;
- it cannot execute the domain's final action;
- it cannot approve its own output;
- it cannot broaden task scope;
- it cannot treat ontology inference as authority;
- it cannot silently write durable Domain, Tenant, or Subject truth.

Any durable update is a candidate routed to the owning Hermes layer.

## Candidate profile shape

```yaml
micro_agent:
  id: relation-extractor
  archetype: generate
  purpose: extract_declared_relation_candidates
  accepts: [source_claim_set]
  emits: [relation_candidate_set]
  semantic_context_profile: relation-extraction
  tools: [structured-reader]
  permissions:
    read_workspace: true
    write_artifacts: true
    run_validations: false
    propose_admission: false
    execute_final_action: false
    access_secrets: false
  limits:
    max_runtime_seconds: 90
    max_output_items: 200
  stop_conditions:
    - source_scope_missing
    - semantic_context_mismatch
    - ambiguity_above_threshold
  escalation_target: ontology-review-router
```

This is an illustration, not a proposed schema.

## Open questions

- Should micro-agent be a first-class overlay type or a constrained profile of
  the existing worker class?
- When is direct typed worker-to-worker handoff safe, and when must the
  orchestrator mediate every edge?
- What is the minimum useful execution evidence for a very cheap task?
- How should profile version, prompt version, model, reasoning effort, and
  toolchain participate in cache identity?
- Which tasks should always receive an independent challenge step?

## Related brainstorms

- [Omnigent Micro-Agent Task Contract](omnigent-micro-agent-task-contract.md)
- [Omnigent Micro-Agent Routing and Composition](omnigent-micro-agent-routing-and-composition.md)
- [Omnigent Micro-Agent Evaluation and Economics](omnigent-micro-agent-evaluation-and-economics.md)
- [Ontology and Omnigent Micro-Agent Exploration Map](ontology-and-micro-agent-exploration-map.md)
