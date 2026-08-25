# Synthesis: Governed Domain Ontology Lifecycle — Brainstorm

Status: brainstorm
Kind: process
Summary: Domain ontology generation and drift maintenance form one governed
revision loop when evidence, authority, compatibility, and rollback remain
explicit at both ends.
Topics: domain-ontology, domain-ontology-lifecycle, generation, drift, synthesis
Repository context: openxFactory neutral contract for DomainxFactory ontologies
Captured: 2026-07-28

## Possible feats

- **Domain ontology revision pipeline** — generate a candidate, validate it,
  approve it, publish a pinned revision, monitor drift, and supersede safely.

## Members and their joints

Atomic members:
[Domain Ontology Generation Pipeline](domain-ontology-generation-pipeline.md)
and [Domain Ontology Maintenance and Drift](domain-ontology-maintenance-and-drift.md).

### Generation establishes the reviewable baseline

Generation turns governed sources and declared domain boundaries into a
candidate ontology with provenance, validation evidence, and unresolved
conflicts. It does not publish semantic authority by itself.

### Maintenance closes the loop

Runtime misses, source changes, usage patterns, and expert corrections create
drift observations. Maintenance evaluates those observations against the
pinned revision and enters accepted changes through the same generation and
approval gates.

## Emergent behavior

The joint lifecycle makes an ontology reproducible and renewable: every
revision explains its sources, compatibility, approval, and successor path.

## Tensions to hold

- Frequent revision improves freshness but increases context and cache churn.
- Domain experts own meaning, while automation is needed to make evidence and
  conflicts tractable.

## Recombination opportunities

The lifecycle can feed the
[ontology maintenance-agent synthesis](ontology-synthesis-lifecycle-and-agents.md)
without transferring approval authority to those agents.

## Open questions

- What compatibility promise exists between adjacent ontology revisions?
- Which drift signals justify an urgent revision versus a normal batch?
- How are contested terms represented while the domain decision is pending?
