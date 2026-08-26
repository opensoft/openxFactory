# Synthesis: Recursive Runtime and Authority — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A context capsule, typed runtime, subordinate task family, and monotone budget can give an Omnigent worker adaptive long-context computation while preserving the existing xFactory authority stack.
Topics: governed-recursive-inference, runtime-and-authority, context-capsule, typed-recursive-runtime, recursive-task-family, recursive-budget, authority-conservation, synthesis
Repository context: openxFactory (neutral runtime/control-plane relationship); Omnigent-Install (runtime realization)
Captured: 2026-07-30

## Possible feats

- **Governed recursive runtime contract family** — combine context admission,
  typed operations, subordinate tasks, and job-level limits without creating a
  new worker authority.
- **Recursive runtime preflight** — validate capsule, profile, task family,
  sandbox, budget, coverage, and model policy before the first model call.
- **Monotone descendant proof** — emit one machine-checkable record showing
  every child narrowed context and authority from the root.

## Members and their joints

Atomic members:

- [Placement](governed-recursive-inference-placement.md)
- [Context Capsule](governed-recursive-inference-context-capsule.md)
- [Typed Runtime](governed-recursive-inference-typed-runtime.md)
- [Recursive Task Family](governed-recursive-inference-task-family.md)
- [Budget and Depth Control](governed-recursive-inference-budget-and-depth-control.md)

```text
Hermes job authority
        |
        v
context capsule ---------> typed runtime profile
        |                         |
        |                         v
        +---------------> root Omnigent task
                                  |
                        validated child templates
                                  |
                                  v
                         subordinate task family
                                  |
                                  v
                         typed result candidate

One budget and trace bind the whole flow.
```

### Placement determines what recursion cannot become

The [placement document](governed-recursive-inference-placement.md) keeps
recursive inference inside an existing worker archetype. That means adaptive
decomposition cannot become a new approval, memory, credential, or terminal
action path.

This placement is what lets the other members specialize execution rather than
restate the xFactory authority model.

### The capsule turns authorization into a computable boundary

The [context capsule](governed-recursive-inference-context-capsule.md) converts
an approved purpose and governed source set into immutable handles that the
runtime can inspect. Without it, "external context" would likely mean a broad
filesystem mount or provider query surface.

The capsule binds runtime flexibility to a finite denominator:

```text
root can choose what to inspect
but only from what the capsule admits
```

Child views then prove subset containment rather than repeating the entire
authorization decision.

### The runtime turns model intent into validated operations

The [typed runtime](governed-recursive-inference-typed-runtime.md) stands
between model-generated control and external effects. It checks operation
types, capsule scope, child-profile compatibility, budgets, and output limits
before execution.

This creates a useful separation:

```text
model
  proposes context computation

runtime
  decides whether the proposed computation is valid to execute

Hermes
  already decided the job's authority and later decides what to do with output
```

### Child calls are execution records, not invisible API calls

The [recursive task family](governed-recursive-inference-task-family.md)
converts every sub-model invocation into a subordinate typed task. This allows
dynamic decomposition while preserving parentage, slice identity, result
validation, cost, and failure lineage.

It also prevents a common authority gap: a root cannot make a child more
powerful merely by wording a broader prompt.

### The family budget makes recursion finite

The [budget and depth document](governed-recursive-inference-budget-and-depth-control.md)
binds the root and descendants to one value envelope. Local per-call ceilings
remain useful, but the family-level ledger prevents fan-out, retries, or nested
recursion from multiplying spend beyond the job's approval.

Depth one is the cleanest initial relationship:

```text
root at depth 0
  -> bounded leaves at depth 1
  -> no descendant recursion
```

This is still recursive inference at the API/control level while keeping cost,
authority, and failure propagation understandable.

## End-to-end preflight

A combined preflight might verify:

1. the Hermes job and worker class are active and compatible;
2. the route permits recursive execution for this task class;
3. the context capsule is current, digest-valid, purpose-bound, and authorized;
4. the semantic context and capsule identities agree with the worker/task;
5. the sandbox/runtime image and combinator library are pinned;
6. child profile IDs form a closed allowed set;
7. the family budget reserves exploration, child, finalization, and validation
   capacity;
8. requested coverage and evidence profiles are realizable;
9. the provider and disclosure posture matches the data class.

Failure before step nine means no model or governed source I/O should occur
beyond what capsule materialization itself required.

## Error and escalation flow

```text
invalid capsule or authority
  -> deny before execution

invalid model operation
  -> return typed rejection to root
  -> bounded repair or stop

child failure
  -> invalidate dependent reduction
  -> preserve independent branches

budget or coverage failure
  -> partial result only if contract permits
  -> otherwise escalate

requested broader scope
  -> never auto-expand
  -> new Hermes-authorized job or human decision
```

## Emergent behavior

Together, these atomics create a worker that can adaptively navigate a corpus
far larger than one prompt while remaining:

- finite;
- purpose-bound;
- content-addressed;
- typed at every external operation;
- constrained to known worker profiles;
- attributable as one job and task family;
- unable to widen authority through recursion.

No individual atomic provides that result. The capsule alone is inert; the
runtime alone has no authorized corpus; the task tree alone can still explode;
the budget alone cannot prevent scope escape.

## Tensions to hold

- Direct brokered child calls preserve RLM adaptivity, while proposed-graph
  validation improves orchestration visibility.
- Typed combinators make termination and cost more analyzable, while arbitrary
  code may discover stronger decomposition strategies.
- Snapshot capsules support replay, while brokered live views better preserve
  data minimization.
- Depth one simplifies governance, while deeper recursion is closer to the
  unconstrained research vision.
- A separate context-capsule contract is clearer, while extending existing
  context packets may reduce record-family proliferation.

## Recombination opportunities

- Combine the runtime preflight with
  [governed tech benches](tech-stack-benches.md) for digest-pinned execution
  environments.
- Bind child profiles to
  [ontology-grounded routing](ontology-grounded-micro-agent-routing.md).
- Use [compiled semantic contexts](ontology-semantic-context-compilation.md)
  as immutable meaning inputs alongside capsule evidence.
- Feed task-family actuals into
  [cost accountability](cost-accountability-and-efficiency-model.md).

## Open questions

- Which record carries the inference strategy and recursive activation policy?
- Is the capsule materialized by the memory gateway, job orchestrator, or a
  dedicated context service?
- What subset proof is sufficient for child views over live brokered sources?
- Which runtime operations may execute without whole-plan validation?
- Does recursive preflight become one new contract or coordinated deltas to the
  job envelope, context packet, worker profile, and task result families?

