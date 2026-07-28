# Ontology-Compiled Context and Result Caching — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Micro-agent latency and token spend can be reduced through two
separate content-addressed caches—precompiled semantic-context slices and
reusable pure task results—whose keys include every meaning- or behavior-
affecting package, input, profile, prompt, model, effort, toolchain, policy,
freshness, and validation version so stale or authority-sensitive work never
reuses an unsafe result.
Topics: ontology, semantic-context, omnigent, micro-agents, caching,
content-addressing, prompt-efficiency, latency, token-cost,
cache-invalidation, reproducibility, memory-gateway, feat-request
Repository context: openxFactory (semantic-context and Omnigent result-cache
contracts)
Captured: 2026-07-28

## Possible feats

- **Compiled semantic-context cache** — reuse common ontology slices under
  exact package/profile keys.
- **Pure micro-task result cache** — reuse independently valid results only
  when all behavior-affecting inputs match.
- **Cacheability classification** — `forbidden`, `request-local`,
  `package-local`, or `content-addressed`.
- **Cache evidence record** — prove origin, validation, freshness, and saved
  cost for every hit.

## Two caches, not one

```text
semantic-context cache
  caches meaning needed to run a class of task

task-result cache
  caches the output of one exact transformation
```

A semantic packet can often be reused even when task inputs differ. A task
result can be reused only if the transformation is pure enough and every
relevant input is identical.

## Semantic-context cache key

At minimum:

```text
kernel package digest
domain ontology package digest
tenant-binding digest, if included
semantic-context profile digest
purpose
term roots / relation allowlist / expansion depth
compiler version
freshness and redaction profile
```

Common packets can be compiled when an ontology package is published, a domain
overlay activates, or a worker profile is installed.

## Task-result cache key

At minimum:

```text
micro-task contract version
worker profile + prompt digest
model + reasoning effort
toolchain and validator versions
all input artifact digests
semantic-context digest
purpose and output type
policy/freshness class where it affects interpretation
```

Omitting a model or prompt version might still be valid for a deterministic
tool-only worker, but it is unsafe for a model transformation.

## Cacheability classes

| Class | Examples | Reuse |
| --- | --- | --- |
| forbidden | authorization, consent, approval, volatile current state, live external action | never |
| request-local | one workflow's redacted subject context normalization | only inside exact request scope |
| package-local | context compilation or ontology fixture evaluation | under exact package/profile pins |
| content-addressed | static artifact classification, digest verification, pure extraction over immutable bytes | across authorized requests with identical keys |

The fact that a result is content-addressed does not make its content visible
to another subject or tenant. Authorization is checked before cache lookup or
result disclosure using a response shape that does not leak existence.

## Invalidation

Content addressing means most changes produce misses rather than mutation:

- ontology update -> new semantic-context key;
- prompt/profile/model change -> new result key;
- input artifact change -> new result key;
- validator correction -> old result no longer satisfies the active gate;
- source freshness expiry -> miss or stale-degraded result as policy allows;
- consent or grant revocation -> deny use even if bytes remain cached.

Revocation changes usability, not necessarily physical cache existence.

## Speed and cost model

Track:

- compile time and packet size;
- prompt tokens saved per semantic packet hit;
- model/tool calls avoided by result hits;
- p50/p95 latency with and without cache;
- validation cost on cache hits;
- hit rate by worker profile;
- invalidation and stale-denial rate;
- cache storage cost;
- downstream correction rate of cached versus fresh results.

A cache that saves model calls but increases stale corrections is not
effective.

## Keep cache hits inspectable

A result hit should emit an execution record containing:

- original result and validation refs;
- cache key and lookup time;
- current authorization and freshness checks;
- exact task compatibility proof;
- saved token/time/cost estimate;
- current trace correlation.

The result remains evidence from its original run, not a newly generated
claim.

## Open questions

- Which micro-agent tasks are pure enough for cross-request reuse?
- Does a different reasoning effort always force a cache miss?
- Can a newer validator accept an old cached artifact after revalidation?
- Where should compiled contexts live: package artifact store, memory gateway,
  or worker host?
- How can result existence be hidden from unauthorized callers without losing
  physical deduplication?

## Related brainstorms

- [Ontology Semantic-Context Compilation](ontology-semantic-context-compilation.md)
- [Omnigent Micro-Agent Evaluation and Economics](omnigent-micro-agent-evaluation-and-economics.md)
- [Ontology-Grounded Micro-Agent Routing](ontology-grounded-micro-agent-routing.md)
