# Domain Ontology Generation Pipeline — Brainstorm

Status: brainstorm
Kind: process
Summary: A newly generated DomainxFactory should receive a deterministic draft
ontology scaffold filled from taxonomy intake, approved structured
terminologies, existing domain artifacts, and provenance-bound candidate
extraction, then remain non-operational until Domain Hermes resolves gaps,
reviews fixtures, and publishes an immutable package.
Topics: ontology, domain-ontology-lifecycle, xfactory-semantic-kernel,
domain-generation, domain-starter, domain-hermes, ontology-seeding,
source-authority, candidate-extraction, semantic-fixtures
Repository context: openxFactory (domain starter, questionnaire, ontology
generation and readiness)
Captured: 2026-07-28

## Possible feats

- **Ontology-aware domain questionnaire** — collect semantic inputs before
  scaffolding.
- **Draft ontology starter tree** — manifest, concepts, relations, mappings,
  sources, candidates, gaps, and fixtures.
- **Deterministic source import lane** — structured terminology and existing
  artifact imports before model extraction.
- **Ontology readiness gate** — prevent a generated scaffold from claiming a
  reviewed active ontology.

## Inputs

The generator should begin with facts already needed to instantiate a domain:

- factory type and subtype;
- target domain and subtype;
- Subject, Tenant, and Domain aliases;
- customer-subject and focal-item kinds;
- primary activities, workflows, states, outcomes, and interventions;
- evidence types and source-authority families;
- external terminology and local code-system references;
- prohibited interpretations and domain boundaries;
- accountable stewards and required reviewers;
- unresolved assumptions and answer quality.

The generator should refuse to infer live tenant details, subject facts,
credentials, licensed source payloads, or accountable approvers.

## Fill order

```text
1. bind taxonomy and layer aliases
2. import exact xFactory kernel
3. seed neutral specializations
4. inspect existing domain models and workflow catalogs
5. import approved structured vocabulary references
6. extract source-bound candidate terms and relations
7. resolve identity, duplicates and mappings
8. preserve conflicts and unknowns
9. generate representative and negative fixtures
10. assemble a Domain Hermes review packet
11. validate and publish only after review
```

Structured authoritative imports should precede model-assisted extraction.
This makes extraction a gap-filling tool instead of the default source of
meaning.

## Candidate-producing roles

The pipeline can later use separate small workers, but their outputs remain
candidates:

| Role | Narrow output |
| --- | --- |
| model inventory reader | candidate source artifacts |
| concept extractor | atomic concept candidates |
| relation extractor | domain/range relation candidates |
| lifecycle extractor | state and transition candidates |
| terminology mapper | exact/broader/narrower mapping candidates |
| entity resolver | duplicate and collision findings |
| provenance verifier | source and license findings |
| ambiguity challenger | unresolved interpretation set |
| fixture generator | positive and negative examples |
| coverage evaluator | unrepresented domain questions |

No role can mark its own candidate active.

## Generated tree

```text
hermes/domain/ontology/
  manifest.yaml
  concepts.yaml
  relations.yaml
  mappings.yaml
  sources.yaml
  stewards.yaml
  candidates.yaml
  coverage-gaps.yaml
  fixtures/
    positive/
    negative/
```

The actual contract may split or combine files differently. The important
property is that every term, relationship, source, steward, fixture, and
unresolved gap is inspectable and versionable.

## Domain Hermes gate

The first generated package should be `draft`, not `active`. Domain Hermes:

1. confirms source authority and licensing;
2. assigns concept and field stewards;
3. resolves identity collisions and disputed meanings;
4. reviews safety- or authority-sensitive relations;
5. runs representative classification fixtures;
6. records remaining exclusions;
7. classifies the package compatibility line;
8. publishes an immutable package and consumer pin.

High-impact domains may require licensed or accountable human approval within
the Domain Hermes gate.

## Rerun behavior

The generator should be idempotent:

- create missing scaffold files;
- update only recognized placeholder sections;
- preserve domain-owned definitions;
- produce candidates beside active content;
- report conflicts instead of choosing silently;
- leave the active content manifest and runtime pin unchanged.

## Open questions

- Which questionnaire answers are hard blockers versus permitted draft gaps?
- How should licensed terminology sources expose mappings without copying
  restricted content?
- Should the generator compile a first semantic context before ratification,
  or only generate fixtures over the draft package?
- What minimum domain-question coverage is required before ontology readiness?
- Which two unlike domains best test that the kernel remains neutral?

## Related brainstorms

- [Ontology Layer Foundations](ontology-layer-foundations.md)
- [Domain Ontology Maintenance and Drift](domain-ontology-maintenance-and-drift.md)
- [Ontology Maintenance Micro-Agent Fleet](ontology-maintenance-micro-agent-fleet.md)
