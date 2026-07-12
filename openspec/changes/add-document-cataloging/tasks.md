## 1. Dependency And Contract Baseline

- [x] 1.1 Complete, realize, and archive `add-doc-health-semantic-sweep` without adding catalog scope, then verify the promoted doc-health spec contains twelve deterministic families plus its separate semantic pass. (Archived 2026-07-12 as `2026-07-12-add-doc-health-semantic-sweep`; promoted spec verified: "twelve check families" enumeration plus the eight promoted sweep requirements, no catalog scope added.)
- [x] 1.2 Rebase this change's doc-health delta onto that promoted wording, preserve `document-catalog` as the thirteenth deterministic family, and run strict OpenSpec validation. (Verified 2026-07-12: the delta's MODIFIED requirements restate the promoted sweep-outcome wording exactly, changing only the thirteenth-family addition and the semantic-analysis clause; `openspec validate add-document-cataloging --strict` passes.)
- [x] 1.3 Verify the proposal supporting-document manifest and hashes and keep proposal-origin policy out of this change pending `add-proposal-origin-contract`. (proposal-support verify ok 2026-07-12; origin policy untouched — the ratified origin contract's migration backfills this change's packet itself.)

## 2. Catalog Contracts And Validation

- [ ] 2.1 Add document-catalog snapshot, cataloger-recommendation, tag-registry, owner-override, opaque-locator, and handling-gate schemas with controlled vocabularies and transition rules.
- [ ] 2.2 Add valid and invalid examples for complete snapshots, suggested classifications, owner overrides, protected evidence, deletions, and pending-state transitions.
- [ ] 2.3 Implement strict openxFactory validators for catalog schema, complete coverage, unique identity, source freshness, taxonomy resolution, override standing, immutable paths, and baseline-mode exceptions.
- [ ] 2.4 Register every schema, template, and taxonomy in `contracts/manifest.yaml`, reconcile versions with `contracts/CHANGELOG.md`, update `contracts/README.md`, and add validator tests.
- [ ] 2.5 Update openxFactory document-lifecycle and doc-health guidance to reference the promoted catalog requirements without granting catalog values lifecycle or ownership authority.

## 3. Shared Inventory And Mechanical Catalog

- [ ] 3.1 Extract the shared inventory from `scripts/doc_health/semantic.py` into a reusable module while preserving one migration read path for the prior list-format inventory.
- [ ] 3.2 Extend inventory entries with `Kind`, `Repository context`, source-declared handling, artifact type, repository revision, content hash, and snapshot ID, and include promoted specs without expanding the v1 corpus.
- [ ] 3.3 Implement deterministic addition, modification, deletion, and rename-as-delete-plus-add diffs plus content-based taxonomy hashing, stable sorting, and byte-identical rendering for identical inputs.
- [ ] 3.4 Implement immutable full per-repository snapshots at `health/document-catalog/runs/YYYY-MM-DD/<run-id>/`, recommendation evidence paths, recursion exclusion, and concurrent-run protection.
- [ ] 3.5 Implement a repository-sharded, bounded, resumable full baseline with explicit progress mode and deterministic merge before complete-coverage enforcement can be enabled.

## 4. Domain Factory Adoption

- [ ] 4.1 Add reusable neutral tag-registry, owner-override, and catalog-review guidance and update `scripts/apply-domain-starter.py` so future DomainxFactories inherit the conventions.
- [ ] 4.2 Update AdxFactory, LedgerxFactory, MedxFactory, OpsxFactory, and codexFactory guides with catalog non-authority, review, override, protected-evidence, and classification-aging rules.
- [ ] 4.3 Re-pin each adopting DomainxFactory to the promoted contract and verify unchanged legacy documents gain external mechanical entries without source edits or fabricated classification history.

## 5. Thirteenth Deterministic Family

- [ ] 5.1 Add `scripts/doc_health/document_catalog.py` in codexFactory and register it as the thirteenth deterministic family in the registry, runner, configuration, and report output.
- [ ] 5.2 Implement coverage, unique-key, source hash/revision, artifact-type, taxonomy, capability/topic resolution, confidence/provenance, override-standing, immutable-path, recursion, and pending-aging checks.
- [ ] 5.3 Add deterministic fixtures and tests for baseline mode, ordinary documents without catalog YAML, deletions, stale classifications, invalid overrides, protected locators, safe normalization, and non-default thresholds.

## 6. Non-Mutating Document Cataloger

- [ ] 6.1 Add a separate codexFactory cataloging module, versioned prompt, bounded shard builder, selector, neutral job envelope, and output validator for baseline, new, changed, missing, pending, and stale entries.
- [ ] 6.2 Require controlled facets and source/taxonomy/classifier/model/prompt provenance, numeric confidence, opaque evidence, and `suggested` state; reject invented effective tags and safety-lowering output.
- [ ] 6.3 Persist validated classifier output with `status: record` under `health/document-catalog/recommendations/YYYY-MM-DD/<job-id>.yaml` and merge it only into a later immutable snapshot.
- [ ] 6.4 Implement owner-side reviewed and overridden dispositions, content-change invalidation, per-facet aging continuity, policy-approved redaction, and protected locator/tag/evidence filtering.
- [ ] 6.5 Add tests for first-run full selection, unchanged zero selection across unrelated commits, incremental add/edit/delete behavior, version invalidation, deterministic merge, no source mutation, no protected metadata leakage, and partial/offline isolation.

## 7. Cataloger Worker And Workload Readiness

- [ ] 7.1 Add the bounded read-only `document-cataloger` profile and capability in omnigent-install, reusing the existing document-analysis host with a distinct job envelope and artifact lane.
- [ ] 7.2 Add only cataloger-specific checks to the Cloud PC runbook and readiness preflight: runner eligibility, heartbeat freshness, profile/version, tenant/data boundary, handling authorization, shard limits, and absence of repository credentials.
- [ ] 7.3 Reference the neutral infrastructure-readiness contract for generic evidence, trust, expiry, remediation, and outage semantics rather than defining a competing readiness-result schema.
- [ ] 7.4 Add profile, envelope, handling, artifact-boundary, sharding, offline, restart, and recovery integration tests.

## 8. Workflow, Baseline, And Realization

- [ ] 8.1 Extend the xFactory nightly workflow so the main pass writes the deterministic catalog result and full mechanical snapshot before asynchronously dispatching an independent cataloger child.
- [ ] 8.2 Add baseline/manual and incremental inputs, immutable evidence commit handling under factory identity, next-run recommendation merge, and concurrency protection against stale overwrite.
- [ ] 8.3 Add a Document Catalog report section with snapshot links, coverage/state counts, add/edit/delete/stale/rejected counts, versions, evidence, skips, aging, and non-default configuration while keeping recommendations out of the Ranked Plan.
- [ ] 8.4 Add watchdog handling for children queued beyond ten minutes or running beyond thirty minutes and prove offline, unauthorized, partial, invalid, or failed semantic work cannot delay or suppress deterministic reporting.
- [ ] 8.5 Run the sharded full-corpus baseline and verify exactly one mechanically correct entry per governed v1 document before enabling complete-coverage enforcement.
- [ ] 8.6 Run strict catalog validation, codexFactory tests, deterministic snapshot reproduction, successful and skipped cataloger runs, and a full nightly workflow with no new critical/error regressions.
- [ ] 8.7 Record baseline and worker evidence, promote contracts and guidance, re-pin consumers, and archive this change with a verified supporting-document bundle.
