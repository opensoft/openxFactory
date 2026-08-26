# Ontology Semantic-Context Compilation — Brainstorm

Status: brainstorm
Kind: architecture
Summary: xFactory should compile purpose- and worker-scoped semantic contexts
from exact kernel, domain ontology, and approved tenant-binding pins so a
runtime agent receives only the concepts, relations, examples, and constraints
needed for one task, reducing context cost while preserving reproducibility
and the existing authority rails.
Topics: ontology, xfactory-semantic-kernel, semantic-context,
context-compilation, worker-scoped-context, memory-gateway,
omnigent-domain-overlay, context-packet, prompt-efficiency, digest-pinning
Repository context: openxFactory (semantic-context compiler and memory-gateway
seam)
Captured: 2026-07-28

## Possible feats

- **Semantic-context profile** — declares the term roots, relation kinds,
  expansion depth, examples, and exclusions needed for a task or worker.
- **Deterministic context compiler** — materializes an exact bounded subgraph
  and digest.
- **Worker-scoped ontology packets** — each Omnigent profile receives only its
  semantic working set.
- **Semantic-context miss telemetry** — detect when an agent needed a term
  omitted by its profile.

## Why compile

Loading an entire domain ontology into every agent recreates the broad-agent
problem:

- more tokens and slower attention;
- more irrelevant terms and collisions;
- harder prompt and output evaluation;
- accidental use of concepts outside the task;
- fewer safe cache opportunities.

Most single-purpose workers need a shallow semantic neighborhood. A citation
verifier needs claim, source, evidence, authority level, and provenance
relations. It does not need every journey state or intervention class in the
domain.

## Compilation inputs

```text
exact xFactory kernel package
+ exact domain ontology package
+ optional approved tenant semantic binding
+ worker profile
+ workflow purpose
+ requested input and output semantic types
+ relation allowlist and expansion depth
+ freshness and redaction rules
= bounded semantic context
```

Subject claims and tenant-private records are not ontology terms. If a task
also needs them, the memory gateway supplies them as separately governed
evidence inside the broader context packet.

## Context profile sketch

```yaml
semantic_context_profile:
  id: citation-verification
  roots:
    - xfactory:claim
    - xfactory:source
    - xfactory:evidence
  relations:
    - supported_by
    - extracted_from
    - conflicts_with
    - supersedes
  expansion_depth: 1
  include_examples: reviewed_only
  exclude:
    - intervention_policy
    - tenant_private_aliases
```

The final artifact should include the resolved term set, exact input package
digests, compiler version, profile version, purpose, freshness, and its own
digest.

## Performance model

Compilation creates three potential gains:

1. **Smaller prompts** — fewer tokens sent on each run.
2. **Reusable packets** — one compiled slice can serve repeated pure tasks
   under the same exact pins.
3. **Deterministic preflight** — undeclared or mismatched semantic types fail
   before a model call.

Compilation itself has a cost. Common profiles should be precompiled at
package publication or worker activation; uncommon ad hoc slices can compile
on demand.

## Safety model

- Context compilation never widens visibility.
- Tenant bindings are included only when the caller and purpose permit them.
- Subject evidence passes the memory gateway rails independently.
- A missing term produces a visible miss or escalation, not an implicit
  full-ontology fallback.
- An expired or mismatched context is rejected.
- Semantic relations remain descriptive and cannot grant authority.

## Effectiveness risks

A context slice can be too small. Symptoms include repeated unknown concepts,
invalid relation attempts, low confidence, or excessive escalation. The
profile should then become an ontology-maintenance or worker-profile candidate,
not self-expand at runtime.

The compiler should support bounded expansion:

```text
root terms
  -> required parents
  -> allowed relation neighbors
  -> reviewed examples
```

It should not perform unbounded graph traversal.

## Open questions

- Should common slices be stored in the domain package or derived at install
  time?
- What is the right expansion depth per archetype?
- Can two profiles share one compiled packet without broadening either task?
- How is context-slice miss rate attributed: bad profile, ontology gap, or bad
  input classification?
- Which semantic context belongs in the job envelope versus the memory
  context packet?

## Related brainstorms

- [Ontology Layer Foundations](ontology-layer-foundations.md)
- [Ontology-Compiled Context and Result Caching](ontology-compiled-context-and-result-caching.md)
- [Ontology-Grounded Micro-Agent Routing](ontology-grounded-micro-agent-routing.md)
