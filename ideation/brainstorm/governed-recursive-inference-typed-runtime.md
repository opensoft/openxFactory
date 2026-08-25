# Typed Recursive Runtime — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Production recursive inference should replace unrestricted model-written host code with a sandboxed, allowlisted context-computation runtime whose typed combinators make control flow, termination, cost, and evidence observable.
Topics: governed-recursive-inference, typed-recursive-runtime, sandbox, toolchain-bindings, tech-benches, omnigent, context-computation, containment, feat-request
Repository context: openxFactory (neutral runtime invariants); Omnigent-Install (sandbox and call-broker realization); OpsxFactory (worker-host and containment realization)
Captured: 2026-07-30

## Possible feats

- **Typed context-combinator contract** — define the operations a recursive
  root may invoke over an authorized capsule.
- **Recursive runtime sandbox profile** — pin environment image, limits,
  network policy, mounts, and module/tool allowlists.
- **Sub-model call broker** — expose child calls as a budgeted function without
  disclosing provider credentials to the runtime.
- **Exploratory and governed runtime modes** — permit a freer research lane
  while keeping production lanes typed and constrained.

## Focus

The original RLM pattern gives a model a REPL and a function that launches
sub-model calls. That flexibility is useful for research, but unrestricted
model-written code is difficult to verify and unsafe around untrusted corpus
content, shared worker hosts, credentials, and governed data.

The proposed xFactory adaptation is a typed runtime: the root model may compose
a small library of prevalidated context operations, while the harness controls
execution.

## Runtime surface

Candidate combinators:

```text
inspect_manifest(filters?) -> shard metadata
search(query, scope, limit) -> cited matches
read_slice(shard_ref, range) -> bounded bytes
partition(shard_ref, strategy, limits) -> child slice refs
map_subtask(profile_ref, slice_refs, task) -> child result refs
reduce_results(reducer_ref, result_refs) -> typed aggregate
join_results(key, result_sets) -> typed joined records
validate_artifact(validator_ref, artifact_ref) -> validation result
emit_evidence_packet(artifact_ref, coverage_ref) -> result candidate
```

These are illustrative. The important property is that each operation has:

- a typed input and output;
- a declared maximum output size;
- an authorization and capsule-subset check;
- a budget charge;
- deterministic validation where possible;
- a trace and evidence event;
- a terminal error vocabulary.

## Root-model interaction

The root model would receive:

- the user or job query;
- capsule metadata, not the full corpus;
- its worker responsibility and output schema;
- available combinators and child profile IDs;
- global and remaining budgets;
- required coverage mode;
- stop and escalation rules.

It could choose a sequence or construct a bounded expression/plan. The runtime,
not the model, would parse, validate, and execute it.

```text
root proposes operation
  -> syntax/type check
  -> authority and budget check
  -> execute in sandbox or broker
  -> bounded observation returned
  -> root continues or emits final artifact
```

## Sandbox boundary

A production sandbox would ideally have:

- no provider API key or raw credential;
- no host filesystem beyond an ephemeral scratch area;
- capsule material exposed through a broker, not a mounted unrestricted corpus;
- no general outbound network, with model subcalls routed through a host-side
  broker;
- a digest-pinned runtime or bench image;
- CPU, memory, process, file-size, cell-time, and wall-time ceilings;
- no package installation;
- no durable worker-local memory by default;
- a per-run ephemeral workspace destroyed or retired by policy.

The existing governed tech-bench direction offers a natural realization
surface, but a recursive sandbox needs a narrower manifest than a general
engineering bench.

## Typed plans versus typed expressions

Two plausible control forms:

### Validated action loop

The root emits one typed action at a time. This preserves adaptivity but may
increase turns and makes global termination harder to analyze.

### Bounded context program

The root emits a whole plan or expression over preverified combinators. The
runtime can estimate cost, reject cycles, and display the plan before
execution. It is less adaptive unless the program includes bounded conditional
branches.

A hybrid could let the root propose a first plan, then permit a small number of
validated revisions when results expose missing evidence.

## Exploratory versus governed modes

```text
exploratory
  isolated arbitrary code
  low-sensitivity public or synthetic corpus
  no credentials or durable outputs without admission

governed
  typed combinators
  approved child profiles
  exact limits and evidence

high-assurance
  preflighted bounded program
  complete-coverage obligations
  independent verification
  enhanced disclosure capture
```

These are possible operating profiles, not settled conformance tiers.

## Alternatives and tensions

- Arbitrary Python is maximally expressive and matches the research
  implementation; typed combinators may remove strategies the model discovers.
- A rich combinator library can become a second programming language with its
  own attack surface and versioning burden.
- One-action-at-a-time validation is observable but can be slow and expensive.
- Whole-plan validation improves predictability but may perform poorly when
  corpus structure is initially unknown.
- Cloud sandboxes simplify isolation but introduce new providers, data-egress
  boundaries, latency, and residency questions.

## Open questions

- What is the minimum combinator set that preserves the RLM advantage?
- Should reducers be deterministic functions, model profiles, or either under
  explicit type distinctions?
- Does the root ever receive a general expression language, or only structured
  tool calls?
- Which runtime profiles may read regulated or tenant-private capsules?
- Can the existing bench-manifest contract specialize cleanly enough, or is a
  dedicated recursive-runtime manifest needed?
- Who curates and versions the combinator library?

## Relationships

- [Recursive Context Capsule](governed-recursive-inference-context-capsule.md)
  supplies the only corpus visible to the runtime.
- [Recursive Task Family](governed-recursive-inference-task-family.md) governs
  the child calls launched by `map_subtask`.
- [Budget and Depth Control](governed-recursive-inference-budget-and-depth-control.md)
  bounds the runtime.
- [Tech-Stack Benches](tech-stack-benches.md) provides the neighboring
  governed-toolchain pattern.

