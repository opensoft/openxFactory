# Tasks: Neutral Hermes Customer-Subject Runtime Contracts

Status: draft

**Input**: Design documents from `specs/005-customer-subject-runtime/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, and completed checklists

**Tests**: Required. The ratified contract demands deterministic positive/negative fixtures, real PostgreSQL 15/16 conformance, exact Git-object release evidence, and regression proof. Test tasks precede their implementation tasks.

**Organization**: Tasks are grouped by independently testable user story. Shared catalogs and entrypoints have one integrator owner so parallel experts do not collide.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Safe to execute in parallel because the task owns different files and has no dependency on unfinished work
- **[Story]**: `US1`, `US2`, `US3`, or `US4` from `spec.md`; setup/foundation/final gates have no story label
- Every task names exact repository-relative paths

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the isolated validator/test surface without changing shared runtime behavior.

- [x] T001 Create validator package, semantic-module package, fixture directories, test package markers, and Docker-context exclusions in `scripts/hermes_runtime_validation/__init__.py`, `scripts/hermes_runtime_validation/semantics/__init__.py`, `tests/hermes_runtime_contracts/__init__.py`, `tests/hermes_runtime_contracts/postgres/__init__.py`, and `.dockerignore`
- [x] T002 Define Python 3.12 validator/test dependencies and generate the reviewed hash-locked environment in `requirements/hermes-runtime-contracts.in` and `requirements/hermes-runtime-contracts.lock`
- [x] T003 [P] Create deterministic pytest fixtures, temporary Git-object helpers, and subprocess helpers in `tests/hermes_runtime_contracts/conftest.py` and `tests/hermes_runtime_contracts/support.py`
- [x] T004 [P] Create PostgreSQL subprocess, Compose-project, evidence-redaction, and cleanup helpers in `tests/hermes_runtime_contracts/postgres/conftest.py`

---

## Phase 2: Foundational Validator And PostgreSQL Harness

**Purpose**: Build shared fail-closed loading, catalog, fixture, evidence, Git-object, CLI, and digest-pinned database harnesses.

**Critical gate**: No user-story implementation starts until T019 passes.

- [x] T005 [P] Write failing duplicate-safe YAML, JSON-compatibility, schema-annotation, canonical-ID, alias-rejection, and offline-reference tests in `tests/hermes_runtime_contracts/test_catalog_and_schema.py`
- [x] T006 Implement strict YAML loading, canonical contract membership, and Draft 2020-12 offline registry behavior in `scripts/hermes_runtime_validation/loader.py`, `scripts/hermes_runtime_validation/catalog.py`, and `scripts/hermes_runtime_validation/schema_registry.py`
- [x] T007 [P] Write failing fixture-index tests for unique paths, dependency closure, fixed evaluation time, stable primary finding codes, and wrong-reason rejection in `tests/hermes_runtime_contracts/test_fixture_index.py`
- [x] T008 Implement self-describing fixture loading, dependency ordering, deterministic result sorting, and expected-finding evaluation in `scripts/hermes_runtime_validation/fixtures.py`
- [x] T009 [P] Write failing exact Git commit/tree/blob, normalized-path, file-mode, missing-object, symlink, submodule, and digest tests in `tests/hermes_runtime_contracts/test_content_resolution.py`
- [x] T010 Implement repository-relative fixture and exact Git-object content resolvers with fail-closed exit-2 dependency errors in `scripts/hermes_runtime_validation/content.py`
- [x] T011 [P] Write failing 17-requirement/85-scenario acceptance and evidence parity tests for missing, duplicate, dangling, and skipped mappings in `tests/hermes_runtime_contracts/test_acceptance_parity.py`
- [x] T012 Implement OpenSpec requirement/scenario extraction and exact acceptance/evidence parity evaluation in `scripts/hermes_runtime_validation/acceptance.py`
- [x] T013 [P] Implement canonical IDs, scopes, digests, Git pins, resource references, timestamps, and extension boundaries in `contracts/hermes-runtime/shared-definitions.schema.yaml`
- [x] T014 Create the initial canonical family catalogs and indexed harness metadata in `contracts/hermes-runtime/contract-index.yaml`, `contracts/hermes-runtime/acceptance-map.yaml`, `contracts/hermes-runtime/evidence-register.yaml`, and `contracts/hermes-runtime/fixtures/index.yaml`
- [x] T015 [P] Write failing CLI selection, deterministic human/JSON output, candidate/realization mode, resolver-option, warning escalation, and exit-code tests in `tests/hermes_runtime_contracts/test_validator_cli.py`
- [x] T016 Implement the thin structural/semantic CLI orchestration and stable finding shape in `scripts/validate-hermes-runtime-contracts.py`
- [x] T017 [P] Write failing PostgreSQL 15/16 image-lock, no-host-port, ephemeral-secret redaction, teardown, and JSON-evidence tests in `tests/hermes_runtime_contracts/postgres/test_runner_contract.py`
- [x] T018 Implement the digest-pinned PostgreSQL 15/16 Compose harness, explicit image-lock refresh, in-memory ephemeral authentication, and EXIT cleanup in `scripts/run-hermes-runtime-postgres-tests.sh`, `tests/hermes_runtime_contracts/postgres/compose.yaml`, and `tests/hermes_runtime_contracts/postgres/images.lock.yaml`
- [x] T019 Run the foundational red-to-green suite for loader/catalog/schema registry, fixture index, acceptance parity, content resolution, CLI, and PostgreSQL runner contracts in `tests/hermes_runtime_contracts/test_catalog_and_schema.py`, `tests/hermes_runtime_contracts/test_fixture_index.py`, `tests/hermes_runtime_contracts/test_acceptance_parity.py`, `tests/hermes_runtime_contracts/test_content_resolution.py`, `tests/hermes_runtime_contracts/test_validator_cli.py`, and `tests/hermes_runtime_contracts/postgres/test_runner_contract.py`

**Checkpoint**: Shared validator and real-database harnesses are independently usable; canonical story contracts remain intentionally incomplete.

---

## Phase 3: User Story 1 — Instantiate Customer Hermes Per Subject (Priority: P1) MVP

**Goal**: One static Customer role template yields repeatable, durable, domain-neutral Customer-subject runtime instances with governed lifecycle and exact assembly pins.

**Independent Test**: One installation with singleton Client/Domain and two Customer instances passes; project/patient/client-company examples use one neutral shape; every invalid cardinality, reference, lifecycle, reuse, static-role, extension-evasion, and overlay case fails for its indexed reason.

### Tests And Fixtures For User Story 1

- [x] T020 [P] [US1] Write failing topology cardinality, neutral identity, pseudonymous reference, tombstone, idempotency, static-role, alias, and extension-evasion tests in `tests/hermes_runtime_contracts/test_topology_and_identity.py`
- [x] T021 [P] [US1] Write failing exact single-file pin, recursive overlay membership, ordering, traversal, exclusion, symlink, submodule, branch/tag-only, and digest-drift tests in `tests/hermes_runtime_contracts/test_overlay_and_pins.py`
- [x] T022 [P] [US1] Write failing immutable registration, predecessor-chain, projection-reconciliation, direct-mutation, event-fork, suspended-recovery, and terminal-retirement tests in `tests/hermes_runtime_contracts/test_topology_lifecycle.py`

### Schemas And Semantic Implementation For User Story 1

- [x] T023 [P] [US1] Implement governed UUIDv4/UUIDv7 and approved keyed-token subject-reference policy attestations in `contracts/hermes-runtime/customer-subject-reference-profile.schema.yaml`
- [x] T024 [P] [US1] Implement immutable one-stack topology registrations and predecessor-linked lifecycle contracts in `contracts/hermes-runtime/runtime-topology.schema.yaml`, `contracts/hermes-runtime/installation-lifecycle-event.schema.yaml`, `contracts/hermes-runtime/stack-lifecycle-event.schema.yaml`, and `contracts/hermes-runtime/layer-lifecycle-event.schema.yaml`
- [x] T025 [P] [US1] Implement complete bytewise-sorted directory-overlay inventories and closed exclusion rules in `contracts/hermes-runtime/overlay-manifest.schema.yaml`
- [x] T026 [P] [US1] Add the complete indexed topology/lifecycle, provisioning, neutrality, reference-policy, and assembly-pin matrix in `contracts/hermes-runtime/fixtures/topology/installing-no-customers.yaml`, `contracts/hermes-runtime/fixtures/topology/configured-no-customers.yaml`, `contracts/hermes-runtime/fixtures/topology/operational-two-customers.yaml`, `contracts/hermes-runtime/fixtures/topology/operational-zero-customers.yaml`, `contracts/hermes-runtime/fixtures/topology/suspended-preserves-registrations.yaml`, `contracts/hermes-runtime/fixtures/topology/failed-recovered-layer.yaml`, `contracts/hermes-runtime/fixtures/topology/retired-all-layers.yaml`, `contracts/hermes-runtime/fixtures/topology/duplicate-singleton.yaml`, `contracts/hermes-runtime/fixtures/topology/extension-customer-evasion.yaml`, `contracts/hermes-runtime/fixtures/topology/retired-identity-reuse.yaml`, `contracts/hermes-runtime/fixtures/topology/lifecycle-fork.yaml`, `contracts/hermes-runtime/fixtures/topology/current-state-mutation.yaml`, `contracts/hermes-runtime/fixtures/topology/retired-transition.yaml`, `contracts/hermes-runtime/fixtures/topology/provision-retry-same-key.yaml`, `contracts/hermes-runtime/fixtures/topology/provision-key-subject-conflict.yaml`, `contracts/hermes-runtime/fixtures/topology/codex-project-hermes.yaml`, `contracts/hermes-runtime/fixtures/topology/medx-patient-hermes.yaml`, `contracts/hermes-runtime/fixtures/topology/ledgerx-client-company-hermes.yaml`, `contracts/hermes-runtime/fixtures/references/uuidv4-subject.yaml`, `contracts/hermes-runtime/fixtures/references/uuidv7-subject.yaml`, `contracts/hermes-runtime/fixtures/references/keyed-token-subject.yaml`, `contracts/hermes-runtime/fixtures/references/uuidv1-subject.yaml`, `contracts/hermes-runtime/fixtures/references/uuidv3-subject.yaml`, `contracts/hermes-runtime/fixtures/references/uuidv5-subject.yaml`, `contracts/hermes-runtime/fixtures/references/unsafe-derivation.yaml`, `contracts/hermes-runtime/fixtures/references/missing-attestation.yaml`, `contracts/hermes-runtime/fixtures/pins/overlay-manifest-valid.yaml`, `contracts/hermes-runtime/fixtures/pins/overlay-manifest-missing-member.yaml`, `contracts/hermes-runtime/fixtures/pins/overlay-manifest-digest-drift.yaml`, `contracts/hermes-runtime/fixtures/pins/overlay-path-traversal.yaml`, `contracts/hermes-runtime/fixtures/pins/overlay-tree-symlink.yaml`, `contracts/hermes-runtime/fixtures/pins/overlay-tree-submodule.yaml`, `contracts/hermes-runtime/fixtures/pins/assembly-branch-only.yaml`, and `contracts/hermes-runtime/fixtures/pins/assembly-tag-only.yaml`
- [x] T027 [P] [US1] Implement lifecycle graphs, cardinality, tombstones, subject uniqueness, extension evasion, projection reconciliation, and provisioning idempotency in `scripts/hermes_runtime_validation/semantics/topology.py`
- [x] T028 [P] [US1] Implement reference-policy, sentinel, exact-overlay, closed-exclusion, ordering, and digest semantics in `scripts/hermes_runtime_validation/semantics/references.py` and `scripts/hermes_runtime_validation/semantics/overlays.py`
- [x] T029 [US1] Add neutral `per_customer_subject`, retain supported isolation aliases, clarify static template meaning, and preserve duplicate-role rejection in `contracts/schemas/xfactory-domain-stack.schema.yaml` and `scripts/validate-domain-factory.py`
- [x] T030 [US1] Register every US1 schema, fixture, HCS scenario, and deterministic evidence binding in `contracts/hermes-runtime/contract-index.yaml`, `contracts/hermes-runtime/fixtures/index.yaml`, `contracts/hermes-runtime/acceptance-map.yaml`, and `contracts/hermes-runtime/evidence-register.yaml`
- [x] T031 [P] [US1] Document neutral Customer-subject specialization, lifecycle-event authority, static-template compatibility, and controlled ratified provenance in `contracts/hermes-runtime/README.md` and `docs/xfactory-domain-factory-model.md`
- [x] T032 [US1] Run and make green the independently testable US1 structural/semantic/static compatibility slice in `tests/hermes_runtime_contracts/test_topology_and_identity.py`, `tests/hermes_runtime_contracts/test_topology_lifecycle.py`, and `tests/hermes_runtime_contracts/test_overlay_and_pins.py`

**Checkpoint**: The neutral multi-Customer topology is real and testable without authority, migration, or release realization.

---

## Phase 4: User Story 2 — Isolate Subjects And Govern Cross-Layer Work (Priority: P1)

**Goal**: Subject records are default-deny and cross-layer work occurs only through exact, revocable, transactionally evidenced authority.

**Independent Test**: Actual non-owner identities for Customer A and B on PostgreSQL 15/16 cannot read, enumerate, write, delete, probe, or retain pooled scope across layers; one exact governed projection succeeds atomically and every altered authority/evidence case fails.

### Tests And Fixtures For User Story 2

- [x] T033 [P] [US2] Write failing principal, database-binding, trust-anchor, issuer-chain, grant/revocation, binding-direction, and as-of rotation tests in `tests/hermes_runtime_contracts/test_authority_and_bindings.py`
- [x] T034 [P] [US2] Write failing artifact immutability/oracle, approval requester/reviewer/policy/supersession/conflict, target-drift, and trace-authority tests in `tests/hermes_runtime_contracts/test_artifact_approval_trace.py`
- [x] T035 [P] [US2] Write failing immutable topology projection, non-owner role, `session_user` binding, forged-GUC, forced-RLS, pooled-scope, artifact/approval/trace immutability, anti-oracle, digest-reverification, supersession/conflict, and atomic commit/rollback database tests in `tests/hermes_runtime_contracts/postgres/test_topology_lifecycle.py`, `tests/hermes_runtime_contracts/postgres/test_roles_and_rls.py`, `tests/hermes_runtime_contracts/postgres/test_scope_pooling.py`, and `tests/hermes_runtime_contracts/postgres/test_governed_evidence.py`
- [x] T036 [P] [US2] Write failing operation-versus-revocation and grant/binding lock-order race tests in `tests/hermes_runtime_contracts/postgres/test_authorization_races.py`
- [x] T037 [P] [US2] Add indexed positive and reason-specific negative principal, trust-anchor, grant, binding, revocation, and operation-authorization fixtures under `contracts/hermes-runtime/fixtures/authority/` and `contracts/hermes-runtime/fixtures/isolation/`
- [x] T038 [P] [US2] Add indexed positive and reason-specific negative artifact, approval, supersession, and trace fixtures under `contracts/hermes-runtime/fixtures/artifacts/`, `contracts/hermes-runtime/fixtures/approvals/`, and `contracts/hermes-runtime/fixtures/traceability/`

### Contracts And Portable Semantics For User Story 2

- [x] T039 [P] [US2] Implement Principal, lifecycle, authenticated database binding, and binding-revocation contracts in `contracts/hermes-runtime/principal.schema.yaml`, `contracts/hermes-runtime/principal-lifecycle-event.schema.yaml`, `contracts/hermes-runtime/database-principal-binding.schema.yaml`, and `contracts/hermes-runtime/database-principal-binding-revocation.schema.yaml`
- [x] T040 [P] [US2] Implement genesis trust-anchor, anchor-event, authority-grant, and grant-revocation contracts in `contracts/hermes-runtime/installation-trust-anchor.schema.yaml`, `contracts/hermes-runtime/installation-trust-anchor-event.schema.yaml`, `contracts/hermes-runtime/authority-grant.schema.yaml`, and `contracts/hermes-runtime/authority-grant-revocation.schema.yaml`
- [x] T041 [P] [US2] Implement exact cross-layer binding, binding-revocation, and operation-authorization contracts in `contracts/hermes-runtime/cross-layer-binding.schema.yaml`, `contracts/hermes-runtime/cross-layer-binding-revocation.schema.yaml`, and `contracts/hermes-runtime/operation-authorization.schema.yaml`
- [x] T042 [P] [US2] Implement immutable artifact record and lifecycle-event contracts in `contracts/hermes-runtime/artifact-record.schema.yaml` and `contracts/hermes-runtime/artifact-lifecycle-event.schema.yaml`
- [x] T043 [P] [US2] Implement approval request, decision-policy, actual-reviewer decision, and authority-bound supersession contracts in `contracts/hermes-runtime/approval-request.schema.yaml`, `contracts/hermes-runtime/approval-decision-policy.schema.yaml`, `contracts/hermes-runtime/approval-decision.schema.yaml`, and `contracts/hermes-runtime/approval-supersession-event.schema.yaml`
- [x] T044 [P] [US2] Implement immutable digest-bound traceability edges in `contracts/hermes-runtime/traceability-edge.schema.yaml`
- [x] T045 [US2] Implement authority-chain, as-of anchor, exact source/target resource, expiry/revocation, binding, and atomic-operation semantics in `scripts/hermes_runtime_validation/semantics/authority.py`
- [x] T046 [P] [US2] Implement artifact, anti-oracle, approval aggregation/supersession, target drift, and trace semantics in `scripts/hermes_runtime_validation/semantics/evidence.py`

### PostgreSQL Isolation For User Story 2

- [x] T047 [P] [US2] Add deterministic two-Customer identities, grants, bindings, revocations, pool-reuse barriers, content bodies/records, approvals/decisions/supersessions, traces, conflict policies, digest drift, anti-oracle probes, and commit/rollback SQL assertions under `tests/hermes_runtime_contracts/postgres/fixtures/isolation/` and `tests/hermes_runtime_contracts/postgres/assertions/isolation/`
- [x] T048 [US2] Implement authoritative/API/quarantine namespaces, NOLOGIN role classes, immutable registrations/events, governed lifecycle projections, composite scoped keys, Principal bindings, forced RLS, and `session_user` trusted scope in `contracts/hermes-runtime/hermes-operational-postgres-v2.sql`
- [x] T049 [US2] Implement append-only artifact/approval/trace tables and guards, anti-oracle admission, body digest/size reverification, authority-bound supersession/conflict handling, atomic trust/grant/binding checks, canonical lock ordering, governed target writes, operation authorization, trace insertion, rollback, and matching revocation entrypoints in `contracts/hermes-runtime/hermes-operational-postgres-v2.sql`
- [x] T050 [US2] Register all US2 schemas, fixtures, portable tests, PostgreSQL cases, HGR scenarios, and evidence bindings in `contracts/hermes-runtime/contract-index.yaml`, `contracts/hermes-runtime/fixtures/index.yaml`, `contracts/hermes-runtime/acceptance-map.yaml`, and `contracts/hermes-runtime/evidence-register.yaml`
- [x] T051 [US2] Run and make green the portable authority/evidence suite and digest-pinned PostgreSQL 15/16 isolation, lifecycle, pooling, artifact/approval/trace persistence, immutability, anti-oracle, digest drift, supersession/conflict, atomic commit/rollback, and authorization-race matrix through `scripts/validate-hermes-runtime-contracts.py` and `scripts/run-hermes-runtime-postgres-tests.sh`

**Checkpoint**: Two Customer subjects are demonstrably isolated in one real database, with only exact governed cross-layer projections permitted.

---

## Phase 5: User Story 3 — Upgrade Legacy Operational Evidence Safely (Priority: P2)

**Goal**: Clean v2 initialization and v1 migration are deterministic, drift-aware, atomic, recoverable, and incapable of promoting unverifiable legacy evidence.

**Independent Test**: PostgreSQL 15 and 16 clean apply/reapply, one/two-subject migration, concurrent write, crash/retry, identical concurrent runner, changed input, reconciliation, security drift, and quarantine matrices all yield the specified exact outcomes.

### Tests For User Story 3

- [x] T052 [P] [US3] Write failing preflight/apply/postflight clean-apply, verified-reapply-without-repair, fresh-v2/v1-cutover profile, and independent missing/extra/altered table, column, constraint, index, policy, function, trigger, role, membership, ownership, ACL, RLS, search-path, PUBLIC, trusted-schema, durable-v1-freeze, quarantine, and dependency-guard fingerprint tests in `tests/hermes_runtime_contracts/postgres/test_clean_apply.py` and `tests/hermes_runtime_contracts/postgres/test_ddl_drift.py`
- [x] T053 [P] [US3] Write failing detached mapping-payload/authority-envelope schema and digest tests; exact binary framing golden vectors; forged/revoked/wrong-scope `run_migration` authority and inactive trust-chain tests; canonical-JSON staging handoff; logical-versus-physical boundary behavior; one/two-subject/default-map; all-twelve-table exactly-one compatibility-history/quarantine row and ID preservation; and PostgreSQL-major parity tests in `tests/hermes_runtime_contracts/postgres/test_migration.py`
- [x] T054 [P] [US3] Write failing pre-lock/post-lock concurrent-v1-write and durable-freeze tests; installation-plus-migration-ID session-lock concurrency; crash/abandon/retry; committed-success-before-client-ack; changed payload/authority/logical-boundary; permitted changed physical snapshot after rollback; terminal success; and reconciliation tests in `tests/hermes_runtime_contracts/postgres/test_migration_recovery.py`
- [x] T055 [P] [US3] Write failing quarantine read/reference/promotion and authoritative-FK/view boundary tests in `tests/hermes_runtime_contracts/postgres/test_quarantine.py`

### Migration And Drift Implementation For User Story 3

- [x] T056 [P] [US3] Implement the typed detached expected-content mapping payload, separately digest-bound `run_migration` authority envelope, source catalog/count/dataset expectations, subject and installation-admin mappings, target topology, single-default proof, and exact binary digest-profile contract in `contracts/hermes-runtime/migrations/v1-to-v2-mapping.schema.yaml`
- [x] T057 [P] [US3] Implement canonical payload/authority-envelope normalization and digests; exact `xfactory-v1-dataset-binary-v1` magic/tag/u64-length framing with closed column type/nullability/primary-key-position metadata, bytewise table/framed-PK ordering, schema-ordinal typed values, exact timestamp/binary/arbitrary-precision-JSON rules; logical-boundary derivation; active approver-grant/policy/scope/anchor verification; and validated canonical-JSON staging handoff plus golden vectors in `scripts/hermes_runtime_validation/migration.py`, `scripts/hermes-runtime-dataset-digest.py`, and `tests/hermes_runtime_contracts/postgres/fixtures/digest-golden-vectors.yaml`
- [x] T058 [P] [US3] Implement the closed non-authoritative legacy quarantine record contract in `contracts/hermes-runtime/legacy-quarantine-record.schema.yaml`
- [x] T059 [US3] Implement the base v2 `legacy_jobs`, `legacy_job_runs`, `legacy_job_events`, `legacy_workers`, `legacy_groups`, `legacy_profiles`, `legacy_group_memberships`, `legacy_github_team_mappings`, migration staging/attempt/event/reconciliation, and quarantine security structures; validated-staging-only input; one session advisory lock on installation plus migration ID across attempt/authoritative/recovery transactions; SERIALIZABLE fixed-order locks over the exact twelve v1 tables; database-recomputed logical boundary and physical cutover envelope; scoped non-authorizing compatibility-history migration; all-row exactly-one reconciliation; durable successful v1 write freeze; exact retry convergence; and changed payload/authority/logical-boundary rejection in `contracts/hermes-runtime/hermes-operational-postgres-v2.sql`, `contracts/hermes-runtime/migrations/v1-to-v2.sql`, and `scripts/run-hermes-v1-to-v2-migration.sh`
- [x] T060 [US3] Implement quarantine-only preservation for unverifiable legacy artifact/approval-request/approval/trace rows, immutable closed records, no runtime/control/audit direct access, no authoritative FK/view/materialized-view/function/gate dependency, DDL dependency rejection, no in-place promotion, and new-governed-record-only exit rules in `contracts/hermes-runtime/migrations/v1-to-v2.sql`
- [x] T061 [US3] Implement the locked preflight/apply/postflight boundary plus deterministic fresh-v2 and v1-cutover PostgreSQL catalog fingerprinting and missing/extra/altered readiness for tables, columns, constraints, indexes, policies, functions, triggers, role attributes/memberships, owners/ACLs, RLS flags, security-definer/search-path configuration, PUBLIC privileges, trusted-schema writability, migration/compatibility-history/quarantine objects, durable v1 freeze, and quarantine grants/dependency guard in `scripts/apply-hermes-runtime-postgres-v2.py` and `scripts/validate-hermes-runtime-postgres.py`
- [x] T062 [P] [US3] Add deterministic all-twelve-table v1 seeds, detached payload/authority envelopes, logical/physical boundary vectors, compatibility-history and quarantine classifications, session-lock concurrency barriers, before/after-lock writes, durable-freeze probes, crash/ack-loss points, drift mutations, quarantine dependency inputs, and expected SQL assertions under `tests/hermes_runtime_contracts/postgres/fixtures/migration/` and `tests/hermes_runtime_contracts/postgres/assertions/migration/`
- [x] T063 [US3] Run and make green the complete clean-apply, drift, migration, recovery, and quarantine matrix on both digest-pinned PostgreSQL majors through `scripts/run-hermes-runtime-postgres-tests.sh`
- [x] T064 [US3] Register migration mapping/quarantine schemas, migration SQL, lifecycle, recovery, image-lock, structural/security drift cases, and evidence in `contracts/hermes-runtime/contract-index.yaml`, `contracts/hermes-runtime/fixtures/index.yaml`, `contracts/hermes-runtime/acceptance-map.yaml`, and `contracts/hermes-runtime/evidence-register.yaml`
- [x] T065 [US3] Run the combined US1/US2/US3 strict validator, non-PostgreSQL pytest, PostgreSQL 15/16 matrix, and OpenSpec gate documented in `specs/005-customer-subject-runtime/quickstart.md`

**Checkpoint**: Fresh and legacy installations have deterministic, fail-closed PostgreSQL realization evidence.

---

## Phase 6: User Story 4 — Publish And Consume An Exact Contract Bundle (Priority: P1)

**Goal**: Publish one additive raw-Git-blob-addressed bundle from an exact reviewed `origin/main` commit and accept only an exact landed pin from `opensoft/xFactory-Hermes-Install`.

**Independent Test**: Candidate, exact-commit, promotion, tag, Domain regression, v1 bridge, and downstream-receipt checks pass for exact evidence and reject every altered repository, tag, commit, path, version, digest, missing object, and working-tree spoof.

### Tests For User Story 4

- [ ] T066 [P] [US4] Write failing scoped v2 envelope/run/event, retired-layer new-job rejection, preserved retired-layer artifact/approval/trace/audit access, and unchanged-v1 compatibility tests in `tests/hermes_runtime_contracts/test_v2_jobs.py`
- [ ] T067 [P] [US4] Write failing exact Domain inventory, duplicate-Customer, dirty-working-tree, missing-object, and deterministic mirror-resolution tests in `tests/hermes_runtime_contracts/test_domain_regression.py`
- [ ] T068 [P] [US4] Write failing release inventory build, exact-commit, promotion-race, annotated-tag, closed-membership, host-path, symlink/submodule, and raw-blob digest tests in `tests/hermes_runtime_contracts/test_release_inventory.py`
- [ ] T069 [P] [US4] Write failing canonical-consumer, wrong-product, exact-landed-commit, packet/path digest, missing-object, authenticated-fetch, and working-tree-spoof tests in `tests/hermes_runtime_contracts/test_consumer_handoff.py`

### Contracts And Verifiers For User Story 4

- [ ] T070 [P] [US4] Implement scoped v2 envelope, run, append-only event, retired-layer new-job rejection, and preserved retired evidence semantics plus indexed `retired-layer-new-job.yaml` and `retired-layer-evidence-preserved.yaml` fixtures without changing v1 files in `contracts/hermes-runtime/hermes-job-envelope-v2.schema.yaml`, `contracts/hermes-runtime/hermes-job-run-v2.schema.yaml`, `contracts/hermes-runtime/hermes-job-event-v2.schema.yaml`, `contracts/hermes-runtime/fixtures/jobs/retired-layer-new-job.yaml`, and `contracts/hermes-runtime/fixtures/jobs/retired-layer-evidence-preserved.yaml`
- [ ] T071 [US4] Implement shared-scope, job/run/event correlation, terminal-layer new-job denial, and retained artifact/approval/trace/audit evidence semantics in `scripts/hermes_runtime_validation/semantics/jobs.py`
- [ ] T072 [P] [US4] Implement the supported-Domain denominator schema and exact five-repository instance with explicit LegalxFactory exclusion in `contracts/hermes-runtime/domain-regression-inventory.schema.yaml` and `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`
- [ ] T073 [US4] Implement exact `commit:path`, deterministic `--domain-repo`/`--domain-repo-root`, missing-object exit-2, and duplicate-Customer derived-negative behavior in `scripts/hermes_runtime_validation/domain_regression.py`
- [ ] T074 [P] [US4] Implement the closed release digest inventory schema plus build, exact-commit, pre-tag promotion, and annotated-tag verification in `contracts/releases/release-digest-inventory.schema.yaml`, `scripts/hermes_runtime_validation/release.py`, and `scripts/validate-contract-release.py`
- [ ] T075 [P] [US4] Implement the `opensoft/xFactory-Hermes-Install`-constant handoff receipt, indexed wrong-product fixture, and exact downstream Git-object reproduction in `contracts/hermes-runtime/consumer-handoff-receipt.schema.yaml`, `contracts/hermes-runtime/fixtures/pins/consumer-receipt-wrong-repository.yaml`, and `scripts/hermes_runtime_validation/consumer_handoff.py`
- [ ] T076 [P] [US4] Document the v2/v1 bridge, Domain denominator, release inventory, immutable-tag correction policy, external xFactory Hermes ownership, and controlled lifecycle provenance in `contracts/hermes-runtime/README.md`, `docs/contract-versioning-policy.md`, `docs/xfactory-domain-factory-model.md`, and `docs/terminology-and-repo-topology.md`
- [ ] T077 [US4] Register all US4 schemas/fixtures/scenarios/evidence and wire candidate, realization, Domain resolver, and handoff resolver modes in `contracts/hermes-runtime/contract-index.yaml`, `contracts/hermes-runtime/fixtures/index.yaml`, `contracts/hermes-runtime/acceptance-map.yaml`, `contracts/hermes-runtime/evidence-register.yaml`, and `scripts/validate-hermes-runtime-contracts.py`
- [ ] T078 [US4] Run every provider gate and record `schema_version`/`kind`, commands, exact revision, results, and redacted pre-release evidence in `openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/provider-verification.yaml`

### Serialized Realization And External Gate For User Story 4

- [ ] T079 [US4] After final fetch/rebase and release lock, record the supported-consumer audit as `Status: record`, allocate only the next available additive version, update release metadata, remove only audited unsupported host-local metadata, and generate the realized inventory in `openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/legacy-source-path-consumer-audit.md`, `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, `contracts/README.md`, and `contracts/releases/<realized-bundle-tag>.digests.yaml`
- [ ] T080 [US4] Commit candidate C, verify exact commit bytes, rerun every gate and independent expert review, and record the unchanged candidate identity/results with `Status: record` in `openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/release-candidate-review.md`
- [ ] T081 [US4] Promote the exact reviewed candidate to published `origin/main`, rerun all gates if promotion changes the commit, run pre-tag promotion checks, publish/verify the immutable annotated tag from an independently refreshed checkout, and record remote evidence with `Status: record` in `openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/release-publication.md`
- [ ] T082 [US4] After the external xFactory Hermes feature lands, add and validate the `schema_version`/`kind` exact consumer receipt, closure packet, compatibility manifest, checker, runtime binding, and positive/negative evidence in `openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/hermes-install-g0-handoff.yaml`
- [ ] T083 [US4] Run the final clean-clone provider/consumer quickstart, diff/status hygiene, all repo-local validators, strict OpenSpec, PostgreSQL 15/16, Domain regression, release/tag, and handoff checks; record the non-database 30-second and per-major 10-minute budgets documented in `specs/005-customer-subject-runtime/quickstart.md`
- [ ] T084 [US4] After T083 succeeds, rerun strict OpenSpec and clean Speckit analysis, accept only externally reproduced downstream T009 closure, and update Gate acceptance checkboxes without editing the consumer repository in `openspec/changes/add-hermes-customer-subject-runtime-contract/tasks.md`

**Checkpoint**: Gate G0 is closed only after both provider publication and the exact landed xFactory Hermes consumer pin independently reproduce every digest.

---

## Dependencies And Execution Order

### Phase Dependencies

- **Setup (T001–T004)**: no prior dependency; T003 and T004 may run in parallel after T001.
- **Foundation (T005–T019)**: depends on Setup; RED tests T005/T007/T009/T011/T015/T017 precede their corresponding implementations, including T005→T006/T013; T019 blocks all user stories.
- **US1 (T020–T032)**: depends on Foundation and is the smallest demonstrable neutral-runtime slice.
- **US2 (T033–T051)**: depends on Foundation plus US1 scope/topology identities; portable schema/evidence lanes may proceed in parallel before the single PostgreSQL SQL owner integrates them.
- **US3 (T052–T065)**: depends on the US2 v2 PostgreSQL base; test, mapping, digest, quarantine, and fixture lanes may start in parallel.
- **US4 (T066–T084)**: portable jobs, Domain, release, handoff, and docs lanes may begin after Foundation/US1, but provider realization T078–T081 depends on US1–US3 completion and external receipt T082 depends on the separate landed xFactory Hermes feature.

### Within-Story Dependencies

- **US1**: T020–T022 must exist and fail for intended missing behavior before T023–T029; T030 depends on T023–T029; T032 depends on T030–T031.
- **US2**: T033–T038 precede T039–T049; T045 depends on T037 and T039–T041; T046 depends on T038 and T042–T044; T048 precedes T049; T050 depends on all US2 contract/semantic/SQL work; T051 depends on T050.
- **US3**: T052–T055 precede implementation; T059 depends on T056–T057 and the US2 SQL base; T060 follows T059; T061 depends on the realized base/migration security surface; T063 depends on T056–T062; T064 follows passing evidence; T065 follows T064.
- **US4**: T066→T070→T071; T067→T072→T073; T068→T074; T069→T075; T076 may run after shapes stabilize; T077 depends on T071/T073–T076; T078 depends on T077 and T065; T079→T080→T081 are serialized; T082 depends on T081 plus the external landed consumer revision; T083 depends on T082; final Gate closure T084 depends on successful T083.

### Shared-File Ownership

- The **catalog integrator** alone edits `contracts/hermes-runtime/contract-index.yaml`, `contracts/hermes-runtime/fixtures/index.yaml`, `contracts/hermes-runtime/acceptance-map.yaml`, and `contracts/hermes-runtime/evidence-register.yaml` in T014/T030/T050/T064/T077.
- The **validator integrator** alone edits `scripts/validate-hermes-runtime-contracts.py` in T016/T077.
- The single **PostgreSQL/migration owner** alone edits `contracts/hermes-runtime/hermes-operational-postgres-v2.sql` in T048→T049 and T059, `contracts/hermes-runtime/migrations/v1-to-v2.sql` in T059→T060, and the dedicated migration runner in T059; no parallel lane edits either production SQL file.
- The **release integrator** exclusively owns `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, realized inventory, release evidence, promotion, and tagging from T079 onward.
- No provider task edits `opensoft/xFactory-Hermes-Install`; its separate OpenSpec/Speckit feature produces the external input consumed by T082.

---

## Parallel Execution Examples

### User Story 1

```text
Topology tests: T020
Overlay tests: T021
Lifecycle tests: T022
Then schema owners: T023, T024, T025
Then semantic/fixture lanes: T026, T027, T028, T029
```

### User Story 2

```text
Portable authority lane: T033, T037, T039, T040, T041, T045
Portable evidence lane: T034, T038, T042, T043, T044, T046
PostgreSQL test lane: T035, T036, T047
Single SQL owner after RED tests: T048 then T049
```

### User Story 3

```text
Security drift lane: T052 then T061
Mapping/digest lane: T053, T056, T057
Recovery lane: T054, T059
Quarantine lane: T055, T058, T060
Fixture/assertion lane: T062
```

### User Story 4

```text
Jobs lane: T066, T070, T071
Domain regression lane: T067, T072, T073
Release verifier lane: T068, T074
Consumer handoff lane: T069, T075
Documentation lane: T076
Integrator/release lane after all provider stories: T077 through T084
```

---

## Implementation Strategy

### MVP First

1. Complete Setup and Foundation.
2. Complete US1 and prove the two-Customer neutral topology plus three domain mappings.
3. Stop for the US1 independent checkpoint. This is a demonstrable contract slice, not Gate G0 closure or a deployable runtime.

### Incremental Provider Delivery

1. US1 establishes repeatable neutral identity/lifecycle.
2. US2 adds real isolation and governed cross-layer authority.
3. US3 makes fresh/legacy PostgreSQL realization safe.
4. US4 adds v2 job compatibility, exact Domain regressions, and serialized publication.
5. The separate xFactory Hermes feature consumes the published bundle; only then do T082–T084 close G0.

### Swarm Allocation

- Start test/schema/fixture experts on disjoint `[P]` tasks.
- Keep shared catalogs, validator entrypoint, PostgreSQL SQL, migration SQL, and release metadata under the explicit single owners above.
- Require every expert handoff to include changed paths, targeted test output, unresolved risk, and the exact next dependency.
- Integrate and commit at story checkpoints; run Speckit analysis before implementation begins and again against the exact release candidate.

## Notes

- `[P]` means safe file ownership, not permission to ignore dependencies.
- Tests must fail for the intended missing behavior before implementation and must pass without weakening the fixture expectation.
- Docker/image or required Git-object unavailability is a failed gate, never a skip.
- Version allocation, release metadata, `origin/main` promotion, and tagging are serialized realization work only.
- Gate G0 remains open until T084; completion of US1 alone does not authorize codexFactory multi-Project implementation.
