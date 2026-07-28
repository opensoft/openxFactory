# Ontology Maintenance Micro-Agent Fleet — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Domain Hermes can maintain ontology quality with a fixed fleet of
single-purpose Omnigent workers that observe sources, extract and map
candidates, detect conflicts, replay fixtures, measure coverage, and assemble
change packets, while every worker remains candidate-only and Domain Hermes
alone accepts meaning and publishes successor packages.
Topics: ontology, domain-ontology-lifecycle, domain-hermes, omnigent,
omnigent-domain-overlay, micro-agents, maintenance-fleet, semantic-drift,
candidate-pipeline, ontology-quality, feat-request
Repository context: openxFactory (Domain Hermes ontology maintenance and
Omnigent worker integration)
Captured: 2026-07-28

## Possible feats

- **Ontology maintenance worker pack** — fixed single-purpose profiles for
  observation, extraction, mapping, verification, challenge, evaluation, and
  assembly.
- **Candidate-only write boundary** — workers can write immutable candidate
  artifacts but never active ontology records.
- **Scheduled reconciliation graph** — replay sources, mappings, fixtures, and
  quality metrics under an exact package pin.
- **Domain Hermes ontology review packet** — one assembled impact and
  compatibility artifact for accountable disposition.

## Fleet shape

| Worker | Archetype | Narrow responsibility |
| --- | --- | --- |
| source revision watcher | frame | emit changed-source observations |
| unknown-term triager | frame | cluster unresolved runtime terms |
| concept candidate extractor | generate | emit atomic concept candidates |
| relation candidate extractor | generate | emit typed relation candidates |
| terminology mapper | generate | propose exact/broader/narrower mappings |
| identity resolver | verify | find duplicates, collisions, and split risks |
| provenance/license verifier | verify | check source and use constraints |
| fixture replay worker | verify | run classifications against package pins |
| semantic drift challenger | challenge | surface changed interpretation and missing counterexamples |
| coverage evaluator | verify | measure representative-question coverage |
| change impact tracer | verify | identify affected profiles, contexts, artifacts, and consumers |
| review packet assembler | assemble_for_admission | produce the Domain Hermes decision packet |

The table is intentionally a fleet of narrow transformations, not a set of new
governing personas.

## Two operating lanes

### Event-driven lane

```text
source update / unknown term / mapping failure / appeal
  -> observation
  -> narrow candidate workers
  -> verify + challenge
  -> impact packet
  -> Domain Hermes queue
```

### Scheduled reconciliation lane

```text
active package pin
  -> source freshness checks
  -> mapping revalidation
  -> fixture replay
  -> coverage and unknown-term metrics
  -> no-change evidence or candidate packet
```

A clean sweep records that no change is required. It should not republish the
same ontology merely to create activity.

## Context specialization

Each worker receives a different compiled semantic slice:

- extractor: target parent concepts, permitted relation kinds, examples;
- mapper: source terminology references and mapping vocabulary;
- verifier: source, steward, lifecycle, and compatibility terms;
- challenger: candidate plus counterexample and contested-meaning context;
- impact tracer: semantic dependency graph and consumer profiles;
- assembler: all verified candidate artifacts, not the raw source corpus.

This is where ontology and micro-agents reinforce one another: the ontology
defines the worker's exact semantic neighborhood, and the worker produces
typed evidence about that ontology.

## Candidate-only authority boundary

Workers may:

- read approved immutable sources and the active ontology pin;
- emit observations, candidates, findings, fixtures, metrics, and packets;
- request escalation for ambiguity or missing source authority.

Workers may not:

- edit or replace the active ontology;
- mark their own candidate accepted;
- select the accountable steward;
- declare a breaking change compatible;
- move a consumer pin;
- import raw tenant or subject data into the package;
- publish a release.

Domain Hermes performs those decisions under its review policy.

## Efficiency controls

- deterministic source and digest checks before model work;
- one extractor per candidate type instead of a broad ontology analyst;
- parallel extraction over independent source partitions;
- cached semantic contexts for fixed worker profiles;
- content-addressed reuse for immutable source analysis where safe;
- cheap first-pass triage, stronger models only for ambiguity;
- scheduled reconciliation based on risk and source cadence;
- retirement of profiles that do not improve coverage or review quality.

## Effectiveness controls

- every candidate cites source and exact package context;
- independent challenger sees candidates and counterexamples;
- fixtures are generated and replayed before review;
- impact tracer covers worker contexts and downstream consumers;
- unresolved disagreement is preserved;
- review packet distinguishes facts, model proposals, conflicts, exclusions,
  and required human decisions.

## Open questions

- Does Domain Hermes directly schedule this fleet, or approve a standing
  maintenance envelope executed by the Omnigent orchestrator?
- Which source watchers are deterministic adapters versus micro-agents?
- Should the challenger use a distinct model family or only an independent
  prompt and context?
- How is runtime unknown-term telemetry de-identified before triage?
- Which package changes always require two independent verification workers?

## Related brainstorms

- [Domain Ontology Maintenance and Drift](domain-ontology-maintenance-and-drift.md)
- [Omnigent Micro-Agent Routing and Composition](omnigent-micro-agent-routing-and-composition.md)
- [Ontology Semantic-Context Compilation](ontology-semantic-context-compilation.md)
- [Ontology and Omnigent Micro-Agent Exploration Map](ontology-and-micro-agent-exploration-map.md)
