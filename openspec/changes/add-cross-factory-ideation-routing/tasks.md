## 1. Dependency And Contract Baseline

- [ ] 1.1 Complete, realize, and archive `add-doc-health-semantic-sweep` and `add-document-cataloging` without adding routing scope, then verify the promoted doc-health spec contains thirteen deterministic families plus its separate semantic pass.
- [ ] 1.2 Rebase this change's doc-health delta onto that promoted wording, preserve `ideation-routing` as the fourteenth deterministic family, and run strict OpenSpec validation.
- [ ] 1.3 Verify this change's staged-origin supporting-document manifest and hashes and leave general proposal-origin/archive-source-state policy to the staged `proposal-origin-contract` topic.

## 2. Neutral Routing Contracts

- [x] 2.1 Add canonical routing-record, `ideation/routing-index.yaml`, structured repository-reference, and organizer-recommendation schemas with controlled vocabularies, transition graphs, destination acceptance, numeric confidence, and evidence references.
- [x] 2.2 Add valid and invalid examples for unknown-owner intake, domain-origin expansion, multi-source routing, unresolved blockers, destination acceptance, and routed proposal provenance.
- [x] 2.3 Implement strict openxFactory validators for routing schema, central ID allocation, unique definitions, paired documents, legal transitions, accepted destinations, structured references, and prospective legacy compatibility.
- [ ] 2.4 Register every schema and template in `contracts/manifest.yaml`, reconcile versions with `contracts/CHANGELOG.md`, update `contracts/README.md`, and add contract/validator tests.
- [x] 2.5 Update openxFactory ideation, document-lifecycle, domain-to-neutral promotion, and doc-health guidance to reference promoted routing requirements without duplicating normative rules.

## 3. Domain Factory Adoption And Scaffolding

- [ ] 3.1 Add reusable neutral ideation/routing guidance and update `scripts/apply-domain-starter.py` so future DomainxFactories inherit capture, provenance, acceptance, and disposition conventions.
- [ ] 3.2 Update AdxFactory, LedgerxFactory, MedxFactory, OpsxFactory, and codexFactory ideation guides with known-domain capture, cross-domain routing pointers, destination acceptance, and owner-authorized disposition.
- [ ] 3.3 Re-pin each adopting DomainxFactory to the promoted routing contract and verify unchanged legacy brainstorms receive no fabricated Idea IDs, Claim IDs, or routing history.

## 4. Fourteenth Deterministic Family

- [ ] 4.1 Add `scripts/doc_health/ideation_routing.py` in codexFactory and register it as the fourteenth deterministic family in the registry, runner, configuration, and report output.
- [ ] 4.2 Implement schema/vocabulary, central Idea-ID and Claim-ID uniqueness, paired-document agreement, legal transition, blocker, destination acceptance, and 30/90-day aging checks.
- [ ] 4.3 Implement the repository ID/gitlink resolver with POSIX/path-traversal checks, xFactory backlog-boundary inspection, strict-gate materialization, and explicitly skipped nightly external-path results.
- [ ] 4.4 Implement lightweight source, destination, staged-fragment, and proposal provenance checks that distinguish canonical definitions from valid references and fenced examples.
- [ ] 4.5 Add deterministic fixtures and tests for ordinary documents without routing sidecars, duplicate IDs, invalid transitions, unresolved blockers, copied records, stale references, safe normalization, contested decisions, and non-default thresholds.

## 5. Non-Mutating Ideation Organizer

- [ ] 5.1 Add a separate codexFactory organizer module, versioned prompt, selector, neutral job envelope, and output validator for qualifying changes, manual requests, cross-domain links, aged items, and strict pre-gate review.
- [ ] 5.2 Require every recommendation to carry committed source revision, passage hash and section reference, rationale, confidence from 0 through 1, alternatives, exclusions, ambiguity, dependencies, and `pending_review` disposition.
- [ ] 5.3 Allow only current, non-policy-blocked catalog entries matching locator or authorized opaque resolver, content hash, inventory snapshot, and taxonomy digest to enqueue optional routing review; prove tags cannot create routing authority or lifecycle state.
- [ ] 5.4 Apply source handling and workload-specific host authorization before dispatch, fail closed when unauthorized, filter protected paths/tags/owners/destinations/summaries/evidence, and persist permitted recommendations with `status: record`.
- [ ] 5.5 Add tests for changed-input, manual, aging, and optional catalog-signal selection; stale-signal rejection; stable evidence; output rejection; authorized disposition; protected-metadata suppression; and organizer failure isolation.

## 6. Organizer Worker And Workload Readiness

- [ ] 6.1 Add the bounded read-only `ideation-organizer` profile and capability in omnigent-install, reusing the existing document-analysis host with a distinct job envelope and artifact lane.
- [ ] 6.2 Add only organizer-specific checks to the Cloud PC runbook and readiness preflight: runner eligibility, heartbeat freshness, profile/version, tenant/data boundary, handling authorization, and absence of repository credentials.
- [ ] 6.3 Reference the neutral infrastructure-readiness contract for generic evidence, trust, expiry, remediation, and outage semantics rather than defining a competing readiness-result schema.
- [ ] 6.4 Add profile, envelope, handling, artifact-boundary, offline, restart, stale-job, and recovery integration tests.

## 7. Aggregation Workflow And Reporting

- [ ] 7.1 Extend the xFactory nightly workflow so deterministic routing completes before asynchronously dispatching an independent organizer child for qualifying or manual inputs.
- [ ] 7.2 Persist validated organizer evidence immutably, link it from the next report, and append only authorized disposition evidence to canonical routing records without editing closed reports.
- [ ] 7.3 Add organizer selection, readiness, authorization, skip, queue, run, and recommendation counts to the report while keeping recommendations non-blocking and out of critical/error regression issues.
- [ ] 7.4 Add watchdog cancellation for children queued beyond ten minutes or running beyond thirty minutes and prove offline, unauthorized, stale-signal, invalid-output, or failed analysis cannot delay or suppress deterministic reporting.

## 8. Pilot, Realization, And Adoption

- [ ] 8.1 Pilot one new unknown-owner idea and one domain-origin mixed idea across neutral, domain, installer/runtime, and aggregation claims without automatic movement.
- [ ] 8.2 Record destination-owner acceptance, routed-claim provenance, organizer evidence, and an authorized accept/edit/reject disposition for each pilot.
- [ ] 8.3 Run strict routing validation, codexFactory tests, skipped/offline and successful organizer runs, protected-output tests, and the full nightly workflow with no new critical/error regressions.
- [ ] 8.4 Promote routing contracts and guidance, re-pin consumers, archive this change with its verified supporting-document bundle, and confirm untouched sources retain no fabricated history.
