# Ontology Layer Foundations — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The xFactory ontology layer should be a small neutral semantic kernel
specialized by Domain-Hermes-owned packages, with tenant mappings and
subject-instance graphs kept separate so meaning can guide retrieval and
classification without becoming policy, evidence, memory, or authority.
Topics: ontology, xfactory-semantic-kernel, domain-ontology-lifecycle,
domain-hermes, tenant-hermes, subject-hermes, semantic-plane,
knowledge-graph, taxonomy, schema, authority-boundary
Repository context: openxFactory (semantic-kernel and domain-ontology
architecture)
Captured: 2026-07-28

## Possible feats

- **Neutral semantic kernel** — stable cross-factory concept and relation IDs
  that reference existing contracts rather than duplicate them.
- **Domain ontology package** — a content-addressed, Domain-Hermes-owned
  specialization of the kernel.
- **Tenant semantic binding** — local source-system terms and field mappings
  that cannot redefine domain meaning.
- **Subject knowledge graph** — isolated instances, claims, evidence, and
  state interpreted under exact ontology pins.

## The distinction that keeps the layer healthy

```text
taxonomy        chooses or classifies a template
schema          constrains the shape of a record
ontology        declares shared meaning and valid relationships
knowledge graph records instances, claims and evidence
policy          constrains what an actor may do
```

An ontology is valuable because the same neutral relationship can appear in
many domains:

```text
xfactory:subject       <- medx:patient
xfactory:focal_item    <- medx:treatment
xfactory:interaction   <- medx:encounter

xfactory:subject       <- codex:project
xfactory:focal_item    <- codex:feature
xfactory:interaction   <- codex:review_event
```

The kernel creates semantic alignment without forcing openxFactory to own the
meaning of patient, treatment, project, or feature.

## Four strata

| Stratum | Owner | Contains | Must not contain |
| --- | --- | --- | --- |
| xFactory semantic kernel | openxFactory | neutral anchors, extension grammar, validation | domain truth |
| Domain ontology package | Domain Hermes | reusable concepts, relations, activities, state models, mappings | tenant or subject instances |
| Tenant semantic binding | Tenant Hermes | local codes, source fields, aliases, operating vocabulary | new domain-wide truth without promotion |
| Subject knowledge graph | Subject Hermes | private instances, claims, evidence, snapshots | reusable published domain definitions |

Each stratum changes at a different cadence. A kernel term should be extremely
stable. A domain mapping may change when a terminology or practice changes. A
tenant binding changes when an organization replaces software. Subject facts
change continuously.

## Stable identity before rich reasoning

The first useful ontology does not need a large reasoner. It needs:

- immutable semantic identifiers independent of display labels;
- exact package and import digests;
- explicit specialization;
- relation domain and range;
- provenance and steward references;
- lifecycle and supersession;
- deterministic validation.

Rich inference can be added later as a derivative service. Starting with
identity, ownership, and deterministic relationships makes historical
interpretation reproducible and keeps the operational contract provider
neutral.

## The authority firewall

The semantic plane may say:

```text
medx:patient specializes xfactory:subject
medx:encounter concerns medx:patient
```

It may not say:

```text
therefore worker X may read patient Y
therefore this source establishes consent
therefore this classification approves an intervention
```

Those decisions remain with exact grants, policies, consent profiles,
approvals, promotion gates, and external enforcement. An ontology can improve
understanding; it cannot create permission.

## Minimum useful kernel

A plausible first inventory is deliberately small:

- layers and parties: subject, tenant, domain;
- work: workflow, activity, state, transition, gate, artifact;
- subject interaction: focal item, interaction, journey state, outcome,
  intervention;
- knowledge: source, claim, evidence, observation, hypothesis, knowledge atom;
- governance references: policy, consent, authority, approval, trace.

Each term should link to the schema or policy that owns its operational
meaning. The ontology is the connective semantic index, not a replacement
contract.

## Open questions

- What cross-domain evidence is sufficient to promote a term into the kernel?
- Which relation characteristics can be deterministic in the first release?
- Should external terminology equivalence be exact, broader, narrower, or
  related-only by default?
- How should a domain expose competing schools of meaning without pretending
  that one definition is settled?
- Which semantic queries must work before a graph projection becomes
  justified?

## Related brainstorms

- [Domain Ontology Generation Pipeline](domain-ontology-generation-pipeline.md)
- [Domain Ontology Maintenance and Drift](domain-ontology-maintenance-and-drift.md)
- [Ontology Semantic-Context Compilation](ontology-semantic-context-compilation.md)
- [Ontology and Omnigent Micro-Agent Exploration Map](ontology-and-micro-agent-exploration-map.md)
