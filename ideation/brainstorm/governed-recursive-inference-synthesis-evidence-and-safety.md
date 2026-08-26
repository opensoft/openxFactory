# Synthesis: Recursive Evidence and Safety — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Recursive inference becomes reviewable only when capsule-denominated coverage, provenance-preserving reductions, structured trajectories, and descendant-wide safety controls describe both what the system learned and what it exposed or failed to inspect.
Topics: governed-recursive-inference, evidence-and-safety, evidence-coverage, recursive-trajectory, recursive-inference-safety, context-capsule, audit, privacy, synthesis
Repository context: openxFactory (neutral assurance relationship); DomainxFactory repos (domain evidence, privacy, and disclosure thresholds)
Captured: 2026-07-30

## Possible feats

- **Recursive assurance packet** — join coverage, claims, source trace,
  trajectory, safety findings, validation, and disclosure refs for review.
- **Coverage-to-disclosure reconciliation** — compare admitted, inspected, and
  provider-disclosed material without conflating the three sets.
- **Independent recursive-run verifier** — validate lineage, subset proofs,
  coverage, provenance, stop behavior, and evidence-tier completeness.

## Members and their joints

Atomic members:

- [Context Capsule](governed-recursive-inference-context-capsule.md)
- [Evidence and Coverage](governed-recursive-inference-evidence-coverage.md)
- [Trajectory and Replay](governed-recursive-inference-trajectory-and-replay.md)
- [Safety and Data Boundaries](governed-recursive-inference-safety-and-data-boundaries.md)

```text
admitted corpus
  capsule manifest
        |
        +------> inspected-set coverage ledger
        |
        +------> provider-disclosed slice events
        |
        +------> excluded / failed / revoked units

child results + provenance
        |
        v
validated reduction
        |
        v
assurance packet
  claims + coverage + trajectory + safety + disclosure refs
```

### The capsule defines three related but different sets

The [context capsule](governed-recursive-inference-context-capsule.md) is the
admitted set. The root may inspect only part of it, and the runtime may send
only some inspected slices to a provider.

```text
provider-disclosed set <= inspected set <= admitted capsule set
```

These inclusions are expected, not failures. The evidence needs to identify
each set so reviewers can answer different questions:

- what was authorized for the task;
- what the system actually examined;
- what left the governed runtime for model inference.

### Coverage governs the result claim

The [coverage ledger](governed-recursive-inference-evidence-coverage.md) uses
the capsule manifest as a denominator. It prevents a targeted exploration from
being described as a complete corpus analysis and preserves excluded, failed,
or unresolved units.

Coverage is an output property with its own validation. It cannot be inferred
from the number of citations or the root's confidence.

### Trajectory explains how coverage and claims arose

The [trajectory](governed-recursive-inference-trajectory-and-replay.md) records
the operations, slices, child calls, reductions, validations, and budget events
that produced the coverage and final artifact.

This allows diagnosis:

```text
missing claim
  -> shard never selected?
  -> child failed?
  -> child result malformed?
  -> reducer dropped provenance?
  -> validator missed it?
```

The trajectory links to governed content artifacts rather than copying every
sensitive byte into general telemetry.

### Safety constrains every evidence transition

The [safety document](governed-recursive-inference-safety-and-data-boundaries.md)
binds admission, inspection, child disclosure, caching, reduction, and
retention. It keeps source text in the data role even when that text contains
instructions aimed at the model.

The same source-authority and sensitivity labels must survive:

```text
capsule shard
  -> slice
  -> child task
  -> child claim
  -> reducer output
  -> final evidence packet
```

Repeated low-authority claims do not become authoritative by aggregation.

## Assurance packet shape

An eventual assurance packet might reference:

- job, root task, task family, route, and runtime profile;
- capsule and semantic-context identities;
- final output artifact and validator results;
- atomic claim/evidence/conflict records;
- requested and achieved coverage modes;
- coverage denominator and unresolved units;
- trajectory and replay-level refs;
- sandbox, injection, authority, and secret-scan findings;
- admitted, inspected, and disclosed set summaries;
- audit-tier and exact-egress refs where required;
- cost, time, model, and provider summaries;
- final status and escalation reason.

This is review evidence, not approval.

## Retention and access layering

```text
general metering/telemetry
  no corpus content
  cost, size, status, timing, digests

governed execution evidence
  selected slices, prompts, child outputs, validations
  access scoped to the task/tenant/domain

enhanced disclosure evidence
  exact provider-bound bytes and sequence
  most sensitive retention and access profile
```

Coverage metadata can itself be sensitive because filenames, record counts, or
source existence may reveal protected information. Even content-free records
need scope-aware access.

## Independent verification

A deterministic verifier can check:

- all task-family members descend from the approved root;
- all child views are subsets of the capsule/parent;
- every final claim resolves to source-backed child evidence;
- coverage arithmetic matches the manifest and required mode;
- prohibited operations or providers were never used;
- budgets and stop conditions were respected;
- the expected audit tier is present;
- digests and pins are internally consistent.

A challenge worker then evaluates semantic concerns that deterministic checks
cannot settle: selective framing, missed contradiction classes, evidence
quality, unsupported causal inference, or suspiciously confident reduction.

## Emergent behavior

Together these records allow xFactory to review not just a recursive answer,
but its epistemic and operational shape:

- what evidence space existed;
- how much of it was covered;
- how the model navigated it;
- which sources support or conflict with each finding;
- what data was disclosed;
- where uncertainty, exclusion, or failure remains.

That makes recursive inference compatible with councils, regulated review, and
post-run diagnosis without granting the run authority.

## Tensions to hold

- Complete evidence improves assurance while increasing sensitive-data
  retention.
- Exact replay may be impossible even when structural and semantic replay are
  strong.
- Item-level coverage can be prohibitively large; aggregated coverage can hide
  misses.
- Exact egress capture proves disclosure but creates a high-value sensitive
  store.
- Injection defenses must not erase source instructions that are legitimate
  analysis targets.

## Recombination opportunities

- Feed assurance packets to Hermes `panel_synthesis`, `scored_vote`, or
  `deliberative_council` profiles.
- Reuse the staged
  [three-tier compression audit](../staging/context-compression-runtime/context-compression-runtime.md)
  for recursive provider traffic.
- Combine coverage findings with doc-health or ontology-maintenance candidate
  flows.
- Use trajectories as curated evaluation evidence, never automatic
  self-modification.

## Open questions

- What is the minimum assurance packet for low-risk codexFactory work?
- Which domains require exact provider egress rather than slice/digest
  evidence?
- How can high-volume coverage records be compacted without hiding unresolved
  units?
- Which evidence is visible to council reference agents versus only the acting
  Hermes role?
- How do erasure, legal hold, and audit retention interact across the three
  evidence tiers?

