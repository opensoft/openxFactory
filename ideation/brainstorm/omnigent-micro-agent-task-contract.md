# Omnigent Micro-Agent Task Contract — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A micro-agent run should be governed by three separate
content-addressed records—a reusable profile, an immutable task envelope, and
an immutable result—so one narrow transformation has explicit semantics,
scope, permissions, tools, budgets, validation, stop reasons, evidence, and
cost without giving the worker durable authority.
Topics: omnigent-micro-agent, omnigent, omnigent-domain-overlay, micro-agents, task-envelope,
worker-profile, result-contract, neutral-job-envelope, semantic-context,
permissions, stop-conditions, execution-evidence, feat-request
Repository context: openxFactory (neutral micro-agent profile, task and result
contracts)
Captured: 2026-07-28

## Possible feats

- **Micro-agent profile extension** — specialize existing Omnigent worker
  classes with purpose, semantic context, tool, limit, cache, and escalation
  fields.
- **Micro-task envelope** — immutable invocation contract over exact inputs and
  expected output.
- **Micro-task result** — typed output, findings, evidence, usage, and terminal
  reason.
- **Purity and cache classification** — state whether identical pinned inputs
  may reuse a prior result.

## Three records, three jobs

```text
profile
  what this class of worker is designed and allowed to do

task envelope
  what this exact invocation is asked to do

result
  what happened, what was emitted, and what it cost
```

Combining them into one mutable record makes retry, comparison, audit, and
cache identity ambiguous.

## Profile

A profile should declare:

- stable profile ID and version;
- exactly one neutral worker archetype;
- one responsibility statement;
- accepted and emitted artifact/semantic types;
- semantic-context profile;
- allowed tools and toolchain binding;
- permission matrix;
- stop conditions and escalation target;
- default runtime, token, cost, and output bounds;
- validation and evaluation suite refs;
- purity/cache posture;
- compatible model and reasoning-effort band.

The profile does not contain a subject ID, live source credential, or an
approval to run.

## Task envelope

An invocation binds the profile to exact work:

```yaml
micro_task:
  task_id: task-...
  job_scope_ref: ...
  profile_ref: ...
  purpose: verify_claim_provenance
  input_artifacts:
    - id: ...
      digest: sha256:...
  semantic_context_ref:
    id: ...
    digest: sha256:...
  expected_output_type: provenance_findings
  validation_refs: [...]
  limits:
    runtime_seconds: 60
    output_items: 100
  authority_refs: [...]
  trace_root: ...
```

The authority references authorize orchestration to invoke the bounded task;
they do not become visible worker credentials or grant the worker a broader
scope.

## Result

The result should distinguish:

```text
succeeded
failed
stopped
escalated
cache_hit
```

It records:

- task, profile, prompt, model, effort, toolchain, and semantic-context refs;
- output artifact ID and digest;
- evidence and source refs;
- confidence, ambiguity, and finding codes;
- validation results;
- start, end, token, wall-time, and normalized-cost usage;
- retry lineage;
- stop or escalation reason;
- cache provenance when reused.

A `succeeded` model call with an invalid output schema is a failed task result.

## Stop before repair loops grow

Micro-agents need closed stop conditions because their main benefit is bounded
work. Typical reasons:

- missing or digest-mismatched input;
- semantic context mismatch or missing required term;
- unauthorized source or tool request;
- ambiguity above threshold;
- output item or size ceiling;
- validation failure after one bounded repair attempt;
- budget or time exhaustion;
- conflict requiring a challenge worker or Hermes reviewer.

The orchestrator decides whether to retry, route to a stronger profile, add a
challenge step, or escalate. The worker should not recursively widen its own
mission.

## Input and output granularity

The contract should prefer one independently verifiable transformation:

```text
source claim set -> atomic claims
atomic claims -> relation candidates
relation candidates -> domain/range findings
artifact -> provenance findings
candidate set -> duplicate clusters
```

"Analyze the domain" is too broad. "Return one candidate relation record per
explicitly supported relation in these cited claims" is appropriately narrow.

## Open questions

- Does the existing neutral job envelope wrap micro-tasks, or do micro-tasks
  form a subordinate record family under one job?
- Which fields belong in the domain overlay versus runtime task records?
- How many bounded repair attempts preserve the meaning of micro-agent?
- Should model and effort be fixed by profile or selected within a declared
  compatibility band?
- Which result fields are required even for sub-second deterministic workers?

## Related brainstorms

- [Omnigent Micro-Agent Foundations](omnigent-micro-agent-foundations.md)
- [Omnigent Micro-Agent Routing and Composition](omnigent-micro-agent-routing-and-composition.md)
- [Omnigent Micro-Agent Evaluation and Economics](omnigent-micro-agent-evaluation-and-economics.md)
