## 1. Semantic Inventory And Decisions

- [ ] 1.1 Inventory the neutral semantic concepts, relation vocabularies, lifecycle terms, and authoritative owners already present across xFactory schemas, policies, validators, and architecture documents.
- [ ] 1.2 Record collisions, overloaded terms, domain-specific leaks, duplicate definitions, and contracts that must be referenced rather than restated by the semantic kernel.
- [ ] 1.3 Finalize the stable core and domain namespace grammar, identifier immutability rules, the acyclic multi-parent specialization rule, and label/alias separation and in-namespace uniqueness with positive and negative examples.
- [ ] 1.4 Finalize the `additive`, `clarifying`, `breaking`, and `retiring` compatibility rubric — including parent addition/removal, relation domain/range widening and narrowing, alias collision as a validation error, and external-mapping refresh — plus migration, retention, two-pin coexistence, and in-flight rollback requirements.
- [ ] 1.5 Ratify the provider-neutral YAML/JSON canonical representation and record JSON-LD/RDF export as optional derivative interoperability unless first-release evidence justifies inclusion.
- [ ] 1.6 Record the cross-domain shared-concept decision (kernel promotion vs governed cross-domain import vs deliberate duplication with mappings) or its explicit deferral with pilot evidence.

## 2. Ontology Contract Family And Core Kernel

- [ ] 2.1 Create `contracts/domain-ontology/` with shared definitions and schemas for the ontology package manifest, concepts, relations, external mappings, source/steward references, candidate changes, releases/adoptions, migration maps, and bounded semantic context.
- [ ] 2.2 Define closed lifecycle, semantic-kind, mapping-kind, compatibility, fill/maintenance-mode, provenance, and finding-code vocabularies.
- [ ] 2.3 Implement package inventory, ontology-family-only inventory membership, raw-content digest, and published-version retention rules consistent with the existing contract release and overlay-manifest conventions.
- [ ] 2.4 Build the minimal xFactory core ontology from the approved inventory, with each term pointing to its authoritative contract, recording adoption evidence (two independent resolvable adopters, pending while draft and resolved via the pilot packages before publication), and adding no domain-owned nouns; record that openxFactory alone classifies kernel revisions.
- [ ] 2.5 Register the new schemas, core package, validators, and fixture indexes in the canonical contract manifest and documentation indexes without allocating a release number early.
- [ ] 2.6 Define the by-reference external-terminology mapping contract with license-class vocabulary, permitted-use recording, and refresh-as-mapping-revision semantics.

## 3. Canonical Semantic Validation

- [ ] 3.1 Implement a canonical domain-ontology validator for schema conformance, package/import closure, exact digests, namespace ownership, identifier uniqueness, label/alias uniqueness, foreign-kind inventory exclusion, retention of referenced superseded versions, and stable-ID reuse.
- [ ] 3.2 Add semantic checks for missing or circular specialization, multi-parent acyclicity, relation domain/range, lifecycle and supersession, mapping validity and mapping-target registration, kernel adoption evidence, steward/source completeness, and compatibility/migration evidence.
- [ ] 3.3 Add privacy and control-plane checks that reject subject or tenant instance material in packages, candidates, reports, fixtures, and quality signals; enforce the term-signal aggregation floor; and reject any ontology record carrying a field outside the closed vocabulary or naming a grant, credential, consent record, approval decision, cross-layer binding, provider binding, or route, without depending on label or definition prose.
- [ ] 3.4 Add cross-contract checks for ontology package, Domain Hermes content manifest, installation overlay, compiled semantic context (subset closure or recorded truncation, tenant-binding resolution), and memory context-packet pin agreement.
- [ ] 3.5 Create indexed positive fixtures for at least one medical and one software-engineering specialization of the same core plus a generated new-domain scaffold.
- [ ] 3.6 Create negative fixtures for digest drift, namespace collision, label/alias collision, ID reuse, invalid cycles, parent addition on a published concept, relation domain/range widening and mismatch, undeclared mappings, unregistered mapping targets, a foreign document inventoried as ontology content, missing sources/stewards, a deleted but still referenced superseded version, private-instance leakage, a below-floor term signal, an unclosed context subset, and semantic-authority bypass.
- [ ] 3.7 Add deterministic automated tests that reproduce every indexed finding and prove repeated validation produces identical results.
- [ ] 3.8 Add negative fixtures and validator findings for mirrored external terminologies and licensed source content beyond the recorded permitted use.

## 4. Domain Ontology Generation

- [ ] 4.1 Extend the domain pre-run questionnaire and its machine-readable answer model with subject/focal-item kinds, activities, states, outcomes, interventions, external terminologies, ontology sources, boundaries, stewards, reviewers, and unresolved semantic assumptions.
- [ ] 4.2 Add starter templates for `hermes/domain/ontology/`, including manifest, concepts, relations, mappings, source inventory, candidate register, coverage-gap report, review fixtures, and Domain Hermes stewardship metadata.
- [ ] 4.3 Extend `scripts/apply-domain-starter.py` to generate the ontology-aware draft scaffold for a new domain, record the ontology-aware starter version in the generated repository, and declare the package in the Domain Hermes content manifest.
- [ ] 4.4 Implement deterministic seeding from the taxonomy tuple, layer aliases, existing domain models, workflow catalogs, evidence types, and approved structured vocabulary imports, and prove the seeded scaffold is byte-reproducible from the same answer set and pinned sources.
- [ ] 4.5 Define a bounded candidate-ingest interface for model-assisted extraction that requires approved sources, provenance, confidence, ambiguity, conflicts, extraction-run identity, and draft review state; writes only to the candidate register; and never deletes, replaces, or resurrects an existing candidate or its recorded disposition.
- [ ] 4.6 Implement entity-resolution, deduplication, core-specialization mapping, unsupported-term, and coverage-gap reports without silently resolving conflicts.
- [ ] 4.7 Generate positive, negative, and representative labeled classification fixtures from the draft package for Domain Hermes review, carrying only de-identified or synthetic cases with their expected classification recorded.
- [ ] 4.8 Preserve active or domain-owned ontology content on starter rerun and extend the rerun report with conflicting and unresolved categories beside created, updated, and skipped artifacts.
- [ ] 4.9 Add starter tests for empty repositories, partial answer sets, idempotent reruns, a model-assisted rerun that proposes a different candidate set over unchanged sources, legacy repositories, conflicting domain content, and attempted active-package overwrite.

## 5. Domain Hermes Stewardship And Maintenance

- [ ] 5.1 Extend the Hermes domain content-manifest schema and canonical validator with the additive `domain_ontology` content kind and generated-domain completeness rules.
- [ ] 5.2 Add Domain Hermes templates for ontology steward assignments, review-council policy, source review cadence, candidate disposition, compatibility decision, release approval, and consumer adoption.
- [ ] 5.3 Define machine-readable workflows for `seed`, `extend`, `refresh`, `reconcile`, `correct`, `deprecate`, and `retire`, including required inputs, review evidence, outputs, and blocked states.
- [ ] 5.4 Implement candidate triggers and reports for source change/expiry, unknown terms, mapping failures, repeated low-confidence classification, conflicts, workflow drift, sub-domain expansion, appeals, and reviewed promotion candidates.
- [ ] 5.5 Implement append-only ontology candidate, decision, publication, supersession, deprecation, retirement, and adoption evidence with no in-place mutation of active packages, each publication naming the accountable steward identity and any worker-attributed publication failing validation.
- [ ] 5.6 Add generated-domain readiness checks that keep incomplete ontology scaffolds non-operational until sources, stewards, fixtures, ratification, publication, and exact pins pass.
- [ ] 5.7 Prove agents and Omnigent workers can prepare diffs, impact reports, and fixtures but cannot promote or publish a package under any worker profile.
- [ ] 5.8 Define the per-release quality report and governed quality-signal telemetry (intake-scope coverage, unknown-term rate, mapping resolution, classification fixture accuracy, open-candidate age), each declaring numerator, denominator, observation window, recorded procedure, and pinned fixture-set identity; keep pass/fail validator conformance separate from the accuracy ratio; wire domain thresholds into the maintenance triggers, the readiness baseline, and a publication block that only a recorded reviewed exception releases; and enforce the distinct-subject/distinct-tenant aggregation floor on term-level signals.

## 6. Semantic Context And Memory Gateway Integration

- [ ] 6.1 Implement deterministic compilation of a purpose-bounded semantic-context artifact from exact kernel, domain package, and approved tenant-binding pins, closing the term subset over specialization ancestors and relation domain/range concepts or emitting an itemized truncation record, and failing closed on an unresolvable or wrong-package tenant binding.
- [ ] 6.2 Extend customer and expert context-packet contracts to carry semantic-context ID/digest, exact ontology identities, lifecycle/freshness metadata, and the bounded term subset when semantics are included.
- [ ] 6.3 Integrate semantic-context validation into memory gateway preflight before provider I/O while retaining all existing consent, privacy, purpose, authority, redaction, promotion, and audit rails.
- [ ] 6.4 Require typed claims, workflow hypotheses, jobs, or derived artifacts that use domain semantics to retain their exact semantic-context or ontology package identity.
- [ ] 6.5 Add tests for context/package mismatch, stale, expired, or retired-package context, digest-verification failure, unrestricted ontology requests, tenant-binding mismatch, unclosed subsets, provider replacement, and cross-purpose reuse.
- [ ] 6.6 Add adversarial tests proving classification, equivalence, specialization, graph traversal, and inferred relations cannot grant access, approve work, promote data, create bindings, or authorize external action.
- [ ] 6.7 Define the neutral worker-archetype/worker-class semantic-context profile artifact inside this change's contract family and prove by fixture that compilation yields only the declared closed term subset per worker with the permission matrix unchanged; record omnigent overlay declaration and worker runtime wiring as the follow-up omnigent change.

## 7. Existing-Domain Migration And Cross-Domain Pilots

- [ ] 7.1 Build an explicit dry-run migration/report path that scaffolds ontology candidates beside an existing DomainxFactory without changing its content manifest or active runtime pin.
- [ ] 7.2 Pilot the generator and validator against MedxFactory and codexFactory, or two equivalently contrasting approved domain fixtures, and use the comparison to remove domain leakage from the core kernel.
- [ ] 7.3 Prove structured authoritative imports take precedence over model candidates and that unresolved conflicts remain review blockers in both pilots.
- [ ] 7.4 Record additive, clarifying, breaking, retiring, explicit adoption, two-pin coexistence, and rollback-with-in-flight-work exercises with historical interpretation preserved under the original ontology pin and superseded package bytes retained at their digests.
- [ ] 7.5 Produce downstream handoff packets for DomainxFactory and Hermes Install consumers; keep their implementation and pin updates in their owning governed changes.

## 8. Documentation, Verification, And Release

- [ ] 8.1 Update the architecture, domain-factory model, installation spine, knowledge lifecycle, memory gateway, domain starter, pre-run questionnaire, and contract README documents with the ratified ontology ownership and lifecycle, and update the machine-readable `contracts/policies/layer-vocabulary.yaml` role text so Domain Hermes ontology stewardship and Tenant Hermes semantic bindings do not drift from the promoted layer-vocabulary spec.
- [ ] 8.2 Document the semantic-plane/control-plane separation, generation pipeline, Domain Hermes stewardship model, maintenance triggers, compatibility rubric, migration path, and provider-neutral runtime consumption.
- [ ] 8.3 Run strict OpenSpec validation, schema and semantic fixture suites, domain-starter tests, domain-overlay validation, memory-gateway tests, privacy/isolation negatives, and existing repository regression checks.
- [ ] 8.4 Obtain independent architecture, security, privacy, domain-stewardship, migration, and adversarial review and resolve every blocking finding against the exact release candidate.
- [ ] 8.5 Allocate the next available additive contract bundle only after integration order is known, generate the exact digest inventory, publish the immutable reviewed commit/tag, and independently verify remote bytes and provenance.
- [ ] 8.6 Record consumer adoption or explicit deferral evidence and archive the change only after the implementation feature, release proof, and required downstream pins have landed.
