# Recursive Budget and Depth Control — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Recursive inference needs one monotone job budget with explicit depth, call, fan-out, token, cost, time, and output ceilings so no child can create unbounded spend or continue after the authorized value envelope is exhausted.
Topics: governed-recursive-inference, recursive-budget, token-budget, cost-accountability, recursion-depth, stop-conditions, metering, failure-containment, feat-request
Repository context: openxFactory (neutral resource and stop contract); DomainxFactory and Tenant Hermes policy (risk and spend thresholds); Omnigent-Install (enforcement)
Captured: 2026-07-30

## Possible feats

- **Recursive budget envelope** — bind total and per-level ceilings to a task
  family.
- **Monotone debit ledger** — reserve and charge every child call against the
  root's remaining budget.
- **Depth-one default policy** — prohibit child recursion beyond one level
  unless an experimental or reviewed profile explicitly enables it.
- **Budget-aware partial-result contract** — distinguish valid partial evidence
  from failed exhaustive work when a ceiling is reached.

## Focus

Recursion changes the cost shape from one bounded model call to a branching
tree. A root can generate many children, children can be slow or verbose, and
retries can multiply. A per-call token maximum is insufficient because no
single child sees the total spend.

The governing unit should be the whole recursive task family.

## Budget dimensions

Candidate root envelope:

```yaml
recursive_limits:
  max_depth: 1
  max_child_calls: 24
  max_parallel_calls: 6
  max_root_iterations: 12
  max_repair_attempts: 1
  max_input_tokens: ...
  max_output_tokens: ...
  max_normalized_cost: ...
  max_wall_time_seconds: ...
  max_runtime_cpu_seconds: ...
  max_materialized_bytes: ...
  max_output_items: ...
```

The values are illustrative. Domains and tenants may tighten them; workers
cannot widen them.

## Monotone debit model

```text
job budget
  -> root reserves minimum finalization budget
  -> each child request declares an upper bound
  -> broker checks and reserves remaining capacity
  -> actual usage settles the reservation
  -> unused capacity returns to the family
  -> no descendant can create new budget
```

Reserving finalization capacity prevents the root from spending everything on
exploration and then lacking enough budget to reduce, validate, or emit a
usable result.

Budget identity should cover:

- provider/model tokens and monetary cost;
- sandbox compute;
- memory-gateway/provider operations;
- tool calls;
- wall time and scheduling occupancy;
- human or council escalation when a workflow prices those downstream costs.

## Recursion depth

Depth is not the same as graph length. A root at depth zero can call ordinary
leaf models at depth one; those leaves cannot launch further subcalls under a
depth-one policy.

Reasons to begin at depth one:

- simpler authority-subset proof;
- predictable fan-out ceiling;
- fewer role and format confusions;
- easier coverage accounting;
- easier cost modeling;
- published reproduction evidence suggests deeper recursion can increase
  latency and degrade quality for some models and tasks.

Depth greater than one could remain an explicit experimental profile with
synthetic or public corpora until it proves a domain-specific advantage.

## Stop conditions

Candidate family-level terminal reasons:

```text
completed
completed_partial
budget_exhausted
depth_limit_reached
call_limit_reached
wall_time_exhausted
coverage_unsatisfied
validation_failed
authority_violation
capsule_expired_or_revoked
provider_unavailable
root_loop_detected
escalated
```

A child stop should propagate only to dependent nodes unless the job requires
complete coverage or the stopped child carried a mandatory partition.

## Loop and overthinking detection

Possible safeguards:

- exact repeated operation detection;
- semantically equivalent repeated query detection;
- unchanged coverage after N iterations;
- diminishing unique-evidence yield;
- repeated self-verification without new evidence;
- duplicate child-task identity;
- root plan revisions above a fixed count;
- predicted remaining work exceeding remaining budget.

These signals may trigger stop, partial completion, a stronger assembler, or
escalation. They should not let the runtime silently fabricate closure.

## Spend authority

Hermes and tenant policy approve the value envelope. The runtime enforces it.
The root may allocate within it but cannot decide that more spend is justified.

Quality bands may carry different ceilings:

```text
routine
important
contested
high_impact
experimental
```

The worker does not self-label its task into a cheaper or more permissive band.

## Alternatives and tensions

- Hard ceilings contain cost but may terminate just before useful completion.
- Adaptive budgeting can shift capacity toward productive branches but depends
  on uncertain model-reported value signals.
- Reserving worst-case cost for every parallel child can underutilize provider
  capacity; loose reservation risks budget overshoot.
- Monetary budgets are provider-specific; normalized credits improve comparison
  but may hide real billing differences.
- Human escalation cost is important to total economics but difficult to price
  synchronously.

## Open questions

- What minimum finalization reserve is required by output type?
- Are budget ceilings fixed in the job envelope or referenced through a
  versioned policy?
- How are provider-side cached tokens, batch discounts, and failed calls
  normalized?
- Can the root cancel low-yield in-flight children, and how is cancellation
  evidence recorded?
- Which stop reasons permit `completed_partial`?
- What proof should be required before a domain enables recursion depth two?

## Relationships

- [Recursive Task Family](governed-recursive-inference-task-family.md) provides
  the accounting and lineage unit.
- [Model Topology and Economics](governed-recursive-inference-model-topology-and-economics.md)
  evaluates whether the envelope produces value.
- [Cost Accountability](cost-accountability-and-efficiency-model.md) supplies
  the broader layer-by-layer spend chain.
- [Synthesis: Runtime and Authority](governed-recursive-inference-synthesis-runtime-and-authority.md)
  joins budgets to task and runtime control.

