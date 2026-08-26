# Recursive Trajectory and Replay — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Every recursive run should emit a content-addressed execution trajectory that reconstructs its call tree, context selections, versions, validations, costs, and terminal reasons while separating replay evidence from sensitive corpus retention.
Topics: governed-recursive-inference, recursive-trajectory, replay, audit, traceability, observability, content-addressing, execution-evidence, feat-request
Repository context: openxFactory (neutral trajectory and replay expectations); Omnigent-Install (runtime logging); DomainxFactory repos (retention and review profiles)
Captured: 2026-07-30

## Possible feats

- **Recursive trajectory record** — capture root iterations, operations, child
  calls, outputs, validations, and budget events under one trace.
- **Replay-level vocabulary** — distinguish exact, structural, and semantic
  replay expectations.
- **Sensitive trajectory profile** — retain hashes and governed refs without
  leaking corpus or model content into general telemetry.
- **Trajectory visualizer projection** — present the task tree, coverage,
  failures, costs, and evidence links to operators and reviewers.

## Focus

A recursive result is produced by a trajectory, not one request/response pair.
Debugging and audit require enough information to explain why the root selected
some context, how children transformed it, where reduction occurred, and what
failed.

At the same time, storing every prompt and output can duplicate private,
regulated, or copyrighted corpus content into the wrong audit plane.

## Proposed trajectory contents

Run identity:

- Hermes job, root task, task-family, trace-root, tenant/subject scope refs;
- runtime, combinator-library, sandbox image, worker profile, prompt, model,
  effort, semantic-context, capsule, validator, and routing-policy versions;
- start/end time, terminal status, and final result refs.

Root iterations:

- observation metadata;
- proposed operation or bounded plan;
- runtime validation result;
- budget before and after;
- operation output ref or digest;
- stop/continue/finalize decision.

Child calls:

- parent, depth, child profile, slice/view refs, typed purpose and output;
- model/provider policy and request digest;
- response artifact and validation refs;
- token, time, cost, retry, cancellation, and terminal reason.

Reduction and evidence:

- reducer identity and inputs;
- structured claims, conflicts, citations, and coverage refs;
- schema/semantic validator results;
- final assembler and admission artifact.

## Replay levels

### Exact-mechanical replay

Re-execute the same bytes, runtime image, prompts, model snapshot, parameters,
and operation sequence. This is often impossible with hosted nondeterministic
models or retired provider versions.

### Structural replay

Re-run the same context program and child graph against the same capsule with
current compatible models. This tests control flow and validation but does not
promise identical text.

### Semantic replay

Re-run the task under the same purpose, coverage, and acceptance requirements,
allowing a new route or plan. This tests whether the current system reaches an
equivalent accepted result.

The trajectory should state which level is promised. "Replayable" without a
level is ambiguous.

## Content-addressed evidence

Hashes can establish identity and detect drift without placing raw content in
every log:

```text
general telemetry
  identifiers, digests, sizes, timings, costs, statuses

governed execution evidence
  prompts, selected slices, child outputs, validations

enhanced disclosure record
  exact provider-bound bytes and timing where policy requires
```

Access control and retention differ across these tiers. The trajectory links
them; it does not duplicate all content into one record.

## Comparison and diagnosis

Trajectory identity supports:

- comparing direct, retrieval, and recursive strategies;
- locating high-cost or low-yield branches;
- attributing missing coverage to routing, child failure, or reduction;
- detecting repeated operations and overthinking;
- evaluating root versus leaf model combinations;
- replaying failed validators;
- preserving evidence when a final artifact is rejected;
- generating candidates for reviewed prompt/profile or combinator changes.

The running fleet does not rewrite its own policy from trajectory data.

## Interaction with existing audit tiers

The staged context-compression topic distinguishes:

1. Hermes envelope evidence;
2. lane harness transcript containing uncompressed originals;
3. optional exact egress capture.

Recursive trajectories fit primarily into tier two. They add structure to the
harness transcript: call tree, capsule slices, operations, and budget/coverage
events. Tier three remains necessary when a domain must prove the exact bytes
sent to a model provider.

## Alternatives and tensions

- Full raw transcripts maximize debugging value but increase data duplication,
  breach surface, retention cost, and erasure complexity.
- Digest-only logs protect content but may be insufficient to investigate a
  semantic failure.
- Provider model snapshots may be unavailable, preventing exact replay despite
  complete local evidence.
- Visualizers help humans but can become unauthorized content-disclosure
  surfaces.
- High-volume leaf calls make one-record-per-event expensive; chunked or
  hierarchical storage complicates integrity verification.

## Open questions

- Which trajectory fields belong in canonical audit events versus referenced
  execution artifacts?
- What content must be retained to support regulated review without creating a
  second uncontrolled corpus?
- How are streamed outputs and cancellations represented?
- Does the root's private reasoning belong in evidence, or only its declared
  operations and results?
- How should trajectories be compacted while keeping content hashes and child
  lineage verifiable?
- Which replay level is required for each domain and quality band?

## Relationships

- [Recursive Task Family](governed-recursive-inference-task-family.md) supplies
  the lineage represented by the trajectory.
- [Evidence and Coverage](governed-recursive-inference-evidence-coverage.md)
  supplies the evidentiary outcomes.
- [Context Compression Runtime](../staging/context-compression-runtime/context-compression-runtime.md)
  supplies the neighboring three-tier audit model.
- [Synthesis: Evidence and Safety](governed-recursive-inference-synthesis-evidence-and-safety.md)
  joins trajectory retention to safety and assurance.

