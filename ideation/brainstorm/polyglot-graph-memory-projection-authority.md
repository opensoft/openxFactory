# Derived Graph Projection Authority — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Graph-provider output should be classified by source, extraction method, scope, time, and review state so rebuildable projections and inferred edges never silently become ontology, evidence, policy, or approval.
Topics: polyglot-graph-memory, graph-projection-authority, governed-derived-model, source-authority, traceability, provenance, authority-conservation
Repository context: openxFactory (neutral graph projection, evidence, promotion, and authority boundaries)
Captured: 2026-07-30

## Possible feats

- **Graph projection manifest** — pin sources, extraction recipe, provider, graph schema, digest, freshness, and coverage.
- **Graph evidence-class vocabulary** — distinguish extracted, inferred, asserted, reviewed, and canonical relationships.
- **Graph edge promotion path** — turn useful inferred or derived relationships into governed candidates, traceability edges, ontology changes, or subject claims.
- **Temporal graph evidence contract** — retain valid-time, observation-time, supersession, and conflict metadata where history matters.

## Focus

This document isolates the authority problem. A graph is persuasive because it
looks connected and complete. That visual coherence must not allow parser
resolution, model inference, similarity, or traversal to acquire authority the
underlying sources do not have.

Provider output can be highly useful and still remain a rebuildable projection.

## Proposed model

Classify graph material before it reaches a user or worker:

| Class | Meaning | Example |
| --- | --- | --- |
| canonical semantic package | Immutable, governed reusable meaning | Published domain ontology term and relation |
| canonical source object | Source-owned record at an exact identity/version | Contract, source claim, repository file, approval record |
| governed durable edge | Explicit reviewed relationship retained for traceability | Requirement `implemented_by` commit |
| extracted projection edge | Deterministically found in source material | Function `calls` function; manifest `pins` package |
| inferred projection edge | Resolver- or model-derived relationship | Document concepts appear related; dynamic dispatch candidate |
| transient context edge | Purpose-bound relationship assembled for one job | Bounded path returned to an Omnigent verifier |

The classes form no automatic promotion ladder. An inferred edge does not
become extracted through repetition, and an extracted edge does not become a
governed durable edge merely because several providers agree.

Every provider edge should carry, directly or through its projection manifest:

- stable source references and locations;
- source revision or object version;
- provider and extractor version;
- extraction class and method;
- graph schema and projection digest;
- owning layer and isolation scope;
- observed/indexed time;
- valid-from and valid-to where source truth is temporal;
- confidence, coverage, and truncation;
- conflict, supersession, and invalidation references;
- review or promotion record if the edge has crossed a governance gate.

### Promotion destinations

A useful provider result must nominate the correct governed destination:

```text
document relationship
  -> cross-reference or catalog candidate

implementation relationship
  -> traceability edge or validation evidence

subject fact
  -> source claim / evidence graph candidate

reusable semantic relationship
  -> ontology candidate under Domain Hermes review

recurring execution pattern
  -> Pattern Ledger episode/family/candidate path
```

The promotion process preserves the provider result as provenance but creates
a new governed object with its own identity and decision record.

### Freshness and invalidation

A current-state code or document graph should be rejected or visibly degraded
when its repository/ref/revision differs from the request. Historical context
remains interpretable under its original pin; a rebuild does not rewrite the
graph that an earlier decision cited.

Subject and operational graphs need stronger temporal treatment. They should
preserve conflicting evidence and distinguish when a fact was valid from when
the system observed or recorded it. Current-state flattening is unsuitable for
audit-sensitive decisions.

## Interfaces and boundaries

Projection authority composes with:

- the governed-derived-model principle that derivative artifacts identify
  their canonical inputs;
- the ontology authority firewall;
- source-authority levels and memory promotion;
- traceability edges and exact evidence;
- document lifecycle and candidate disposition;
- Pattern Ledger's derived, candidate-only sensing posture.

It does not require one physical graph database. The same projection may be
materialized in a property graph, relational tables, JSON, an in-memory graph,
or another provider if identifiers and evidence remain stable.

## Alternatives and tensions

**Trust deterministic extraction as truth** is tempting for code and manifests,
but parsers can miss reflection, generation, dynamic dispatch, conditional
configuration, and cross-system effects.

**Treat every edge as merely advisory** is safe but discards the value of
explicit source-owned relations and governed traceability records.

**Overwrite projections on every rebuild** is simple operationally but breaks
historical interpretation when a decision cited an earlier graph.

**Retain every graph forever** preserves history but can be expensive and
privacy-sensitive. Durable decisions need cited projection identities; routine
uncited indexes may follow a shorter retention policy.

## Open questions

- Which projection artifacts require immutable retention once cited by a gate
  or decision?
- What confidence vocabulary can work across parsers, resolvers, and
  model-assisted document extraction without implying false comparability?
- When provider agreement exists, does it increase confidence, coverage, or
  only corroboration count?
- Which graph classes require bitemporal fields in the neutral kernel?
- How should an erasure or consent withdrawal affect retained graph evidence
  that was previously cited?

## Relationships

- [Graph Provider Contract](polyglot-graph-memory-provider-contract.md)
  carries projection and edge evidence to consumers.
- [doxBench Graphify Projection](polyglot-graph-memory-doxbench-graphify.md)
  applies extracted-versus-inferred display rules.
- [Hermes Layer Graph Placement](polyglot-graph-memory-hermes-layer-placement.md)
  applies scope and promotion boundaries.
- [Synthesis: Provider Routing and Governance](polyglot-graph-memory-synthesis-routing-and-governance.md)
  connects authority class to route and context behavior.
