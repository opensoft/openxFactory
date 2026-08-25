# Recursive Context Capsule — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A recursive worker should receive an immutable authorized context capsule that manifests content-addressed shards, rails, purpose, and allowed operations without loading the whole corpus into a model context or widening provider access.
Topics: governed-recursive-inference, context-capsule, context-packet, expert-context-packet, memory-gateway, source-authority, semantic-context, consent, tenant-isolation, feat-request
Repository context: openxFactory (neutral context artifact and memory-gateway seam); DomainxFactory repos (domain source classes and redaction profiles)
Captured: 2026-07-30

## Possible feats

- **Recursive context capsule contract** — manifest an authorized external
  corpus as immutable shards with digests, source authority, purpose, and TTL.
- **Capsule-view derivation record** — prove that every child task sees a
  subset of its parent's admitted corpus.
- **Context-packet capsule binding** — connect an existing customer or expert
  context packet to a larger external corpus without granting unrestricted
  provider access.
- **Capsule materialization service** — build, verify, expire, and revoke
  context capsules before worker execution.

## Focus

The defining RLM move is to keep a large corpus outside the neural context and
let a root model inspect it as an environment. In xFactory, that environment
cannot be an unbounded filesystem path, database connection, or vector-store
credential. It needs an authority-preserving artifact.

A **context capsule** is proposed as that artifact: a content-addressed,
purpose-bound manifest over exactly the material admitted to one job.

## Proposed model

```text
governed source requests
  -> memory/source rails
  -> redaction and source-authority filtering
  -> immutable shard materialization
  -> capsule manifest + digest
  -> recursive worker receives capsule handle
```

Illustrative, non-schema shape:

```yaml
context_capsule:
  id: capsule-...
  purpose: cross_repository_impact_analysis
  workflow_ref: ...
  issued_at: ...
  expires_at: ...
  owning_scope: ...
  parent_context_packet_refs: [...]
  semantic_context_ref:
    id: ctx-...
    digest: ...
  corpus:
    manifest_digest: ...
    shards:
      - id: shard-...
        content_digest: ...
        media_type: text/markdown
        source_ref: ...
        source_authority: source_backed
        sensitivity_class: internal
        byte_length: 12345
  allowed_operations:
    - inspect_manifest
    - search
    - read_slice
    - partition
  prohibited_operations:
    - direct_provider_query
    - unrestricted_filesystem_read
  audit_refs: [...]
```

The worker would see metadata and handles first. Actual shard bytes would enter
a model call only when the runtime selects an authorized slice.

## Relationship to current context packets

The current memory-gateway context packets already carry purpose, workflow,
subject refs, redaction class, source or memory refs, semantic-context identity,
trace refs, provider refs, and audit refs. Expert context packets add expert
profile, knowledge scopes, allowed and prohibited uses, source authority, and
usage refs.

The capsule would not replace those rails. It would specialize the externalized
large-corpus case:

```text
context packet
  proves the governed purpose and admitted context classes

context capsule
  manifests the immutable bytes and operations available to recursive compute
```

The existing packet schemas are closed shapes, so a first-class capsule binding
would require an explicit contract delta rather than an undeclared field. An
alternative is a separately referenced job input artifact whose authorization
is derived from the packet.

## Shard and manifest rules

Candidate properties:

- every shard has a stable identity, digest, length, media type, and source ref;
- the manifest itself is content-addressed;
- shard boundaries are deterministic or carry the materializer version;
- the capsule never contains provider credentials;
- source authority and sensitivity survive partitioning;
- duplicate bytes may deduplicate physically without crossing disclosure
  boundaries;
- authorization is checked before capsule lookup and before slice disclosure;
- a child view names the exact parent capsule and allowed shard/range subset;
- TTL, revocation, consent, or source-lifecycle changes may deny use even when
  immutable bytes still exist for audit or retention purposes.

## Materialization choices

### Snapshot bytes into an artifact store

Advantages: reproducible, digest-verifiable, independent of provider drift.
Costs: duplicates sensitive data and creates retention/custody obligations.

### Manifest live provider references

Advantages: less duplication and current-source access.
Costs: replay changes over time, every slice may require provider I/O, and
worker execution risks becoming indirect unrestricted provider access.

### Hybrid

Snapshot low-sensitivity immutable artifacts; use brokered live handles for
volatile or sensitive sources, with each read independently authorized and
recorded. The capsule manifest records which mode each shard uses.

## Semantic and evidentiary separation

The capsule may bind a worker-scoped semantic context, but ontology terms are
not the same as subject or source evidence:

```text
semantic context
  meaning needed to interpret a task

corpus shards
  evidence or artifacts examined by the task
```

The two identities should be pinned separately so an ontology update and a
source-byte update produce distinct invalidation and replay signals.

## Alternatives and tensions

- A capsule may be redundant if existing `source_refs` can identify every
  artifact precisely; however, plain refs do not necessarily express shard
  identity, allowed operations, coverage, or child-subset proofs.
- Very fine shards improve selective reads but increase manifest, routing, and
  evidence overhead.
- Very large shards recreate context rot at leaf calls.
- Snapshotting supports replay but can violate data-minimization goals.
- Search indexes speed navigation but are derived artifacts that need their own
  digest, version, and visibility rules.

## Open questions

- Is the capsule a memory-gateway artifact, a neutral job input artifact, or a
  distinct context-computation contract family?
- Which sources may be snapshotted, and which must remain live brokered views?
- What is the default shard unit: document, semantic section, fixed token
  window, source-native record, or a multi-resolution combination?
- Does a child subset view receive a new capsule ID and digest or a signed range
  declaration over the parent?
- How do erasure and legal holds interact with immutable execution evidence?
- Where do capsule indexes live, and can a worker query them without learning
  the existence of unauthorized content?

## Relationships

- [Typed Runtime](governed-recursive-inference-typed-runtime.md) consumes the
  capsule only through approved operations.
- [Evidence and Coverage](governed-recursive-inference-evidence-coverage.md)
  uses the manifest as the denominator for coverage claims.
- [Safety and Data Boundaries](governed-recursive-inference-safety-and-data-boundaries.md)
  governs sensitivity, injection, isolation, and disclosure.
- [Ontology Semantic-Context Compilation](ontology-semantic-context-compilation.md)
  supplies the separate meaning artifact.

