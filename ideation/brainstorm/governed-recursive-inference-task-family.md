# Recursive Task Family — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A recursive run should be represented as one authorized root task plus immutable subordinate child tasks whose scope, permissions, context, budgets, and output types can only narrow from their parent.
Topics: governed-recursive-inference, recursive-task-family, micro-agents, task-envelope, routing, traceability, authority-conservation, typed-handoff, feat-request
Repository context: openxFactory (neutral subordinate-task and lineage contract); Omnigent-Install (orchestrator and child-call broker)
Captured: 2026-07-30

## Possible feats

- **Recursive task-family record** — bind one root and all descendants under a
  shared job, trace, budget, and policy identity.
- **Subordinate micro-task envelope** — represent each child call as an
  immutable typed invocation rather than a hidden model API call.
- **Monotone authority validator** — prove that child scope, context,
  permissions, and tool access are subsets of the parent.
- **Dynamic-template instantiation** — let a root choose partitions and
  questions while the orchestrator restricts child nodes to approved
  templates.

## Focus

RLM implementations often expose a simple `llm_query()` function inside a
REPL. For xFactory, every such invocation is execution with cost, evidence, and
scope consequences. The child-call tree needs a first-class identity without
turning every leaf into an independently approved Hermes job.

The proposed unit is a **recursive task family**.

## Proposed hierarchy

```text
Hermes job envelope
  └─ root micro-task
       ├─ child task A
       ├─ child task B
       │    └─ grandchild B1, only if policy permits depth > 1
       └─ child task C
```

All members share:

- the owning job and trace root;
- the activation policy and runtime profile;
- a global budget ledger;
- the root's capsule identity;
- retention and audit policy;
- the terminal result contract.

Each child adds:

- parent task ID and depth;
- exact child profile, prompt, model, and effort;
- exact capsule subset or slice refs;
- one bounded purpose and expected output type;
- its local debit limits;
- retry identity and terminal reason.

## Monotone authority

The key invariant is:

```text
child authority <= parent authority <= Hermes-approved job authority
```

For candidate fields:

```text
child capsule shards       subset of parent capsule view
child allowed uses         subset of parent allowed uses
child tools                subset of parent/runtime allowlist
child permissions          no wider than parent worker permissions
child sensitivity ceiling  no higher than parent admission
child output types         approved by the selected child profile
child budget               debited from parent/global remaining budget
child lifetime             no longer than parent/capsule lifetime
```

A child cannot request a new provider route, credential family, tenant,
subject, purpose, or worker profile. A need outside the family becomes an
escalation or a new Hermes-authorized job.

## Dynamic decomposition without an agent zoo

The root may adaptively choose:

- how to partition admitted shards;
- which approved child profile processes each partition;
- which bounded question or transformation each child receives;
- when enough evidence exists to reduce;
- whether one allowed challenge or repair template should run.

The root may not:

- define a new child profile or prompt family;
- alter permissions or toolchain bindings;
- create cycles or unbounded fan-out;
- turn a child result into durable truth;
- ask a child to perform the terminal action.

This makes dynamic decomposition an instantiation of a closed template family,
not free-form worker creation.

## Direct versus orchestrator-mediated calls

### Direct brokered call

The root invokes a runtime function; the broker validates and executes it
immediately. This closely matches RLM behavior and minimizes control latency.

### Proposed child graph

The root emits a child graph; the Omnigent orchestrator validates, schedules,
and returns result refs. This provides stronger graph visibility and resource
control but adds planning overhead.

### Hybrid

The root can launch bounded map calls directly from a declared template, while
new reducer, challenge, or repair nodes require graph validation. This may
preserve fast common paths while keeping semantic branching visible.

## Result and failure propagation

Each child result should distinguish at least:

```text
succeeded
failed
stopped
escalated
cache_hit
```

The parent reducer receives typed result refs, not just response strings.
Failed children invalidate only dependent reductions. Independent branches may
finish and preserve useful evidence. The root may emit an incomplete result
only if the output contract and coverage mode allow it; otherwise it escalates.

Retries preserve lineage. A changed prompt, slice, profile, model, effort,
semantic context, or toolchain is a new attempt, not an identical retry.

## Relationship to existing micro-task ideas

The existing micro-agent packet proposes three records: reusable profile,
immutable task envelope, and immutable result. Recursive inference does not
need a competing record family. It may need:

- a root/parent/depth extension;
- capsule-view identity;
- job-level and remaining-budget references;
- recursive activation policy;
- coverage contribution;
- child-call trajectory references.

Whether those are extensions or subordinate companion records remains open.

## Alternatives and tensions

- Treating every child as a full neutral job maximizes audit clarity but creates
  approval, routing, and storage overhead that can erase RLM economics.
- Treating children as opaque provider calls is cheap but loses traceability,
  budget attribution, typed validation, and subset proofs.
- A closed child-profile registry limits model creativity but prevents
  permission and tool drift.
- Depth greater than one is conceptually recursive but greatly complicates
  authority proofs, failure propagation, and cost prediction.

## Open questions

- Is a recursive task family a new record or an extension of the proposed
  micro-task envelope/result family?
- Which child actions may execute immediately and which require orchestrator
  graph validation?
- Can an assembler request one missing child, or must it return an incomplete
  packet to the root planner?
- How is partial success represented at the family level?
- Are cached child results family members with original-run provenance or
  references to external evidence?
- Does depth zero mean the root, making the first ordinary child depth one?

## Relationships

- [Omnigent Micro-Agent Task Contract](omnigent-micro-agent-task-contract.md)
  supplies the reusable profile/task/result separation.
- [Routing and Composition](omnigent-micro-agent-routing-and-composition.md)
  supplies typed DAG and failure-containment principles.
- [Budget and Depth Control](governed-recursive-inference-budget-and-depth-control.md)
  governs shared and local ceilings.
- [Trajectory and Replay](governed-recursive-inference-trajectory-and-replay.md)
  records the family execution.

