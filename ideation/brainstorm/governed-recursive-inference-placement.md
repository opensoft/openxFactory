# Governed Recursive Inference Placement — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Recursive Language Models fit xFactory as a governed inference strategy inside a bounded Omnigent worker, not as a sixth worker archetype, a new authority layer, or a replacement for the typed workflow graph.
Topics: governed-recursive-inference, recursive-inference-placement, omnigent, omnigent-domain-overlay, worker-archetypes, micro-agents, inference-strategy, feat-request
Repository context: openxFactory (neutral placement and authority boundary); Omnigent-Install (runtime realization); DomainxFactory repos (domain use profiles)
Captured: 2026-07-30

## Possible feats

- **Adaptive context runtime capability** — define a neutral execution
  strategy family in which `recursive` is one selectable strategy.
- **Worker inference-strategy declaration** — let an existing Omnigent worker
  profile select a governed recursive runtime without creating a new
  archetype.
- **Recursive inference activation policy** — state which job classes may use
  the strategy and which authority, sensitivity, and evidence conditions bind
  it.

## Focus

This document isolates where Recursive Language Models (RLMs) belong in the
xFactory stack. Here, RLM means the inference pattern described by Zhang,
Kraska, and Khattab: a root language model treats a large input corpus as an
external environment, examines and partitions it programmatically, and launches
sub-model calls over selected pieces before assembling a result. It does not
mean the unrelated use of RLM for "reasoning language model."

The placement question matters because the same mechanism can be described
misleadingly as a model, an agent, an orchestrator, a retrieval system, or a
runtime. Each description implies a different authority and contract boundary.

## Proposed placement

The strongest xFactory fit is:

```text
Hermes-approved job
  -> xFactory routing and context rails
  -> bounded Omnigent worker
       inference_strategy: recursive
       external authorized context
       constrained child calls
  -> typed result artifact
  -> verify / challenge / assemble-for-admission
  -> Hermes or accountable human decision
```

Recursive inference would be a way an existing worker computes. The worker
still maps to exactly one neutral archetype:

```text
frame
generate
verify
challenge
assemble_for_admission
```

Examples:

- a `frame` worker recursively explores a large corpus to identify the
  evidence-bearing partitions and propose a decomposition;
- a `generate` worker recursively builds a cross-corpus impact analysis;
- a `verify` worker recursively checks whether claims hold across every
  relevant artifact;
- an `assemble_for_admission` worker reduces typed child results into a cited
  packet.

The strategy does not create permission. It inherits the worker's existing
six-boolean permission matrix, constitutional `execute_final_action: false`
and `access_secrets: false` limits, toolchain binding, context profile, stop
conditions, and escalation path.

## Why the RLM should usually live inside one graph node

The current micro-agent direction treats a workflow as an explicit typed DAG.
An RLM introduces adaptive context navigation and task decomposition. Letting
that adaptive mechanism replace the whole DAG would hide cost, lineage,
validation edges, and scope growth.

A safer composition is:

```text
deterministic preflight
  -> recursive evidence-compiler node
  -> typed evidence packet
  -> independent verifier
  -> conflict-aware assembler
```

The RLM node may instantiate subordinate tasks from approved templates, but the
surrounding workflow remains explicit. This contains the nondeterministic part
of the system behind typed inputs and outputs.

## Ownership boundaries

| Surface | Proposed owner |
| --- | --- |
| Neutral recursive-inference contract and invariants | openxFactory |
| Sandboxed runtime, child-call broker, and trajectory capture | Omnigent-Install |
| Domain worker profiles, prompts, allowed task classes, and evals | Each DomainxFactory |
| Job authorization, context admission, budgets, and approval | Hermes plus xFactory rails |
| Scheduling and worker-host placement | Runtime/worker control plane, potentially AgentTower |
| Terminal action | Accountable human or external enforcement system |

The xFactory aggregation repository would pin compatible versions; it would not
own the mechanism.

## Non-authorities

Recursive inference would not:

- become a Hermes decision maker;
- create a sixth Omnigent archetype;
- grant direct access to memory or knowledge providers;
- bypass context-packet, consent, source-authority, or tenant-isolation rails;
- invent new worker profiles, credentials, or tools at runtime;
- write durable Domain, Tenant, or Subject truth;
- approve its own result or perform a terminal action.

## Alternatives and tensions

### Treat RLM as a new worker archetype

This makes routing easy to name but confuses responsibility with computation.
The same recursive mechanism can support framing, generation, verification, or
assembly, so one new archetype would cut across the existing vocabulary.

### Treat RLM as the Omnigent orchestrator

This preserves the research pattern's flexibility but conflicts with
orchestrator-mediated typed handoffs and makes dynamic scope growth harder to
govern. It may be acceptable in a low-risk exploratory lane, but it is a poor
default contract.

### Treat RLM as a model-provider wrapper

This offers drop-in adoption, but provider middleware cannot see the full
xFactory authority, source, coverage, and evidence semantics. A wrapper may
realize the compute, while the xFactory contract must remain above it.

### Name the neutral capability after RLM

`recursive-language-model-runtime` is recognizable but binds a long-lived
contract to one research label. `adaptive-context-runtime` or
`governed-context-computation` would leave room for typed, reflective, or
non-recursive implementations while still declaring `recursive` explicitly.

## Open questions

- Should inference strategy live on a worker profile, task envelope, routing
  policy, or all three at different levels?
- Is recursive inference allowed for every archetype, or should early
  activation be limited to `frame`, `generate`, and `verify`?
- Does the root worker execute child calls directly through a broker, or emit
  a proposed child graph that the orchestrator validates and runs?
- What neutral capability name survives changes in the RLM research landscape?
- Which control plane owns scheduling without acquiring authority over the
  recursive task's semantics?

## Relationships

- [Context Capsule](governed-recursive-inference-context-capsule.md) defines
  the external context admitted to the worker.
- [Typed Runtime](governed-recursive-inference-typed-runtime.md) constrains how
  the worker explores that context.
- [Recursive Task Family](governed-recursive-inference-task-family.md) keeps
  child calls subordinate and traceable.
- [Synthesis: Runtime and Authority](governed-recursive-inference-synthesis-runtime-and-authority.md)
  combines these placement decisions into one control flow.

