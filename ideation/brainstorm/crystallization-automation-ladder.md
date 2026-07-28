# The Automation Ladder: Rungs Between Cold AI and Pure Code — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Crystallization is not AI-versus-code but a seven-rung spectrum —
cold solve, recall-assisted solve (today's ceiling), memoized results,
frozen playbook, specialist micro-agents, code with AI edges, pure code —
where each rung trades flexibility for marginal cost, every family has a
ceiling set by task nature, domain policy, and authority, the default motion
is one rung per promotion with evidence, and the frozen playbook (L3) is the
expected workhorse because planning tokens dominate many solves.
Topics: crystallization, automation-ladder, playbook, memoization,
micro-agents, distillation, caching, self-learning, domain-overlay,
recurrence
Repository context: openxFactory (neutral rung vocabulary; ceilings are
domain overlay policy)
Captured: 2026-07-28

## Possible feats

- **Neutral rung vocabulary** — a controlled `automation_rung` enum carried
  by capabilities, decisions, and dispatch records.
- **Playbook artifact kind (L3)** — a frozen, versioned plan record executed
  step-by-step without a planner; likely a workflow-contract instance.
- **Rung-ceiling declarations** — domain overlays cap rungs per task
  category (regulatory and judgment ceilings).
- **Per-instance rung selection** — dispatch may run a high-stakes instance
  at a lower rung than the family's best capability.

## Position in the packet

Second document of the invest/build arc: the
[economics decision](crystallization-economics.md) purchases a rung from
this ladder; [requirements mining](crystallization-requirements-mining.md)
and the [build pipeline](crystallization-build-pipeline.md) scale their
rigor to the rung; [dispatch](crystallization-dispatch-and-fences.md)
executes at it.

## The rungs

```text
L0  cold solve            full multi-agent reasoning, no memory assist
L1  recall-assisted solve TODAY'S CEILING: gateway context packets bring
                          prior episodes; the AI still plans and executes
L2  memoized result       identical (canonicalized) input → reuse prior
                          output; the task-result cache brainstorm owns
                          the mechanics; only for pure task classes
L3  frozen playbook       the PLAN crystallizes: fixed step sequence, AI
                          performs the steps; planner tokens eliminated
L4  specialist executors  playbook steps delegated to typed micro-agents
                          (smaller model, compiled semantic context, typed
                          I/O); later: distilled/tuned small models
L5  code with AI edges    deterministic core; AI handles input
                          normalization, ambiguity, and exception branches
L6  pure code             deterministic end-to-end; AI appears only in
                          sentinel sampling and drift review
```

Rung profiles (directional):

| Rung | Build cost | Marginal cost | Flexibility | Drift fragility | Auditability |
| --- | --- | --- | --- | --- | --- |
| L0 | none | highest | highest | n/a | narrative |
| L1 | none (exists) | high | highest | low | narrative |
| L2 | trivial | ~zero | none (exact hits) | high (key brittleness) | exact provenance |
| L3 | low | medium−  | medium (steps flex) | medium | plan is inspectable |
| L4 | medium | low | medium− | medium | typed contracts |
| L5 | high | very low | low (fenced) | medium+ | code + tests |
| L6 | highest | ~zero | lowest | highest | total |

## Where the value concentrates

The hypothesis to validate first with metering data: **planning is the
dominant token cost in most recurring multi-agent solves.** If true, L3 —
freeze the plan, keep flexible executors — captures most of the savings at a
fraction of L5/L6's build cost and fragility, and the packet's workhorse is
a *playbook library*, not a program library. L2 is nearly free where it
applies but applies narrowly (pure, exact-repeat tasks); it is owned by the
[result caching](ontology-compiled-context-and-result-caching.md) brainstorm
and appears here only as a rung. L4 is where
[micro-agents](omnigent-micro-agent-foundations.md) plug in: a playbook step
with typed I/O is exactly a micro-agent task.

## Ceilings

Not every family may climb:

- **Task nature** — is the output mechanically checkable? Is the world
  coupling stable? Judgment-laden tasks (a persuasion draft, a differential
  diagnosis) cap at L3/L4 — the steps can crystallize; the judgment must
  not.
- **Domain policy** — overlays declare rung ceilings per task category
  (e.g., Medx clinical-judgment categories cap where a regulator would see
  an autonomous medical decision; Ledgerx filings may require deterministic
  L5+ for arithmetic but human sign-off regardless).
- **Authority** — a rung may not grant the capability more authority than
  the AI configuration it replaces
  ([authority conservation](crystallization-authority-and-consent.md)).

So every family record carries `rung_ceiling` with a reason, and the ladder
is climbable only to the ceiling.

## Motion rules

- **Ratchet up on evidence** — default one rung per promotion, each with its
  proof obligations ([parity](crystallization-parity-and-cutover.md)).
  Skipping rungs requires an unusually strong forecast and a stated reason.
- **Demotion is an operation, not a failure** — drift response
  ([lifecycle](crystallization-drift-and-lifecycle.md)) demotes routinely;
  the AI path below is always intact.
- **Mixed rungs per family** — dispatch MAY run a high-stakes instance at a
  lower rung (or the AI path) even when a higher capability exists;
  risk-scored instance routing is a v2 refinement.

## Claims

- **AL-C1** — Crystallization is a spectrum of ~seven rungs; the spec's unit
  of decision, build, and dispatch is a rung, never an AI/code binary.
- **AL-C2** — `automation_rung` is a first-class controlled vocabulary
  carried by capability versions, decisions, and dispatch records.
- **AL-C3** — Every family has a declared, reasoned rung ceiling from task
  nature, domain policy, and authority conservation.
- **AL-C4** — Default motion is one rung per promotion with evidence;
  demotion is a routine, cheap operation because lower rungs never
  disappear.
- **AL-C5** — L3 frozen playbooks are the expected workhorse (planner cost
  dominance) — a hypothesis to confirm from metering before the heavy rungs
  get investment.

## Open questions

- **AL-Q1** — Is the rung taxonomy right-sized (merge L4 into L3-with-typed-
  executors? split L5 by AI-edge share?), and is it stable enough to be a
  schema enum?
- **AL-Q2** — Where do playbooks live: workflow-contract instances in the
  domain repo, practice-catalog entries, or a new artifact kind?
- **AL-Q3** — Does L1 recall quality change the economics enough that
  improving retrieval (cheap) should always be tried before any build
  (a mandatory "L1 tune-up" stage in the decision)?
- **AL-Q4** — Per-instance mixed-rung dispatch: v1 or deferred until
  risk-scoring exists?
- **AL-Q5** — Is model distillation (tuning a small model on episode
  corpora) a v1 rung or a later refinement of L4?

## Related

- [Ontology-Compiled Context and Result Caching](ontology-compiled-context-and-result-caching.md)
  — owns L2 mechanics.
- [Omnigent Micro-Agent Foundations](omnigent-micro-agent-foundations.md) —
  the L4 substrate.
- [Crystallization Economics](crystallization-economics.md) — purchases the
  rung.
