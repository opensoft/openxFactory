# Domain Ontology Maintenance and Drift — Brainstorm

Status: brainstorm
Kind: process
Summary: Domain Hermes should maintain an immutable active ontology through a
candidate queue triggered by authoritative-source changes, unknown terms,
mapping failures, workflow drift, quality degradation, and reviewed promotion
candidates, publishing only compatibility-classified successor packages with
historical pins preserved.
Topics: ontology, domain-ontology-lifecycle, domain-hermes,
ontology-maintenance, semantic-drift, source-change, unknown-terms,
mapping-failure, compatibility, supersession, quality-metrics
Repository context: openxFactory (Domain Hermes ontology stewardship and
maintenance lifecycle)
Captured: 2026-07-28

## Possible feats

- **Ontology maintenance trigger contract** — normalized observations that
  create candidates but do not mutate active meaning.
- **Compatibility-classified change record** — additive, clarifying, breaking,
  or retiring.
- **Semantic quality dashboard** — coverage, unknown-term rate,
  mapping-resolution rate, fixture accuracy, and drift.
- **Historical interpretation guarantee** — every artifact remains decodable
  under its original ontology pin.

## Maintenance modes

```text
seed        establish the first reviewed package
extend      add new concepts, relations, mappings or sub-domains
refresh     revisit terms after source change or expiry
reconcile   compare sources, mappings, usage and definitions
correct     supersede inaccurate meaning with evidence
deprecate   discourage new use while preserving resolution
retire      reject new use while retaining history
```

These are different operations. A source refresh that produces no semantic
change should record the check without publishing a new package. A correction
must not be disguised as an additive release.

## Drift signals

Domain Hermes should receive normalized observations such as:

- authoritative source revision or expiry;
- new terminology release;
- rising unknown-term frequency;
- ambiguous or conflicting mappings;
- repeated low-confidence classification;
- fixture accuracy regression;
- workflow states seen in operation but absent from the ontology;
- terms never used or never resolved;
- new domain subtype or source system;
- user appeal or expert correction;
- reviewed de-identified learning candidate from Tenant or Subject Hermes.

The observation is evidence for review, not a self-executing semantic update.

## Candidate lifecycle

```text
observed
  -> triaged
  -> proposed
  -> source and impact review
  -> fixture and compatibility review
  -> accepted | rejected | parked
  -> published in a new immutable package
  -> explicitly adopted by consumers
```

Rejection and parking are useful outcomes. They prevent the active ontology
from accumulating weak synonyms, one-tenant vocabulary, or source noise.

## Compatibility

| Class | Meaning | Expected evidence |
| --- | --- | --- |
| additive | new non-conflicting meaning | new fixtures and coverage |
| clarifying | labels/provenance improve without changing classification | before/after equivalence proof |
| breaking | identity, hierarchy, domain/range, or valid mapping changes | migration map and consumer impact |
| retiring | use is deprecated or stopped | replacement or rationale |

Consumers move only by explicit pin. Published packages are never edited or
retagged. A rollback changes the pin used for new work; historical claims and
artifacts keep their original package identity.

## Quality is part of stewardship

A healthy ontology needs measurable signals:

- coverage of representative domain questions;
- percentage of runtime terms resolved;
- exact versus broad/narrow/related mapping distribution;
- fixture accuracy and regression count;
- conflict backlog age;
- candidate acceptance and rejection rates;
- stale source or steward count;
- context-slice miss rate;
- semantic changes per release and consumer adoption lag.

Metrics should trigger investigation, not automatic publication.

## Role of small workers

Maintenance is well suited to a micro-agent fleet because most steps are
narrow: compare sources, find affected terms, replay fixtures, detect
collisions, and assemble an impact packet. Domain Hermes still owns candidate
disposition and publication. See
[Ontology Maintenance Micro-Agent Fleet](ontology-maintenance-micro-agent-fleet.md).

## Open questions

- Which drift signals are safe to collect without retaining tenant or subject
  content?
- What review cadence applies to a stable term whose source has not changed?
- How should contested meanings coexist within one domain package?
- When does a high unknown-term rate indicate an ontology gap versus bad
  upstream entity resolution?
- Who may declare that a breaking change is urgent enough to accelerate
  consumer migration?

## Related brainstorms

- [Domain Ontology Generation Pipeline](domain-ontology-generation-pipeline.md)
- [Ontology Semantic-Context Compilation](ontology-semantic-context-compilation.md)
- [Ontology Maintenance Micro-Agent Fleet](ontology-maintenance-micro-agent-fleet.md)
