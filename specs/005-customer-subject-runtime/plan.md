# Implementation Plan: Neutral Hermes Customer-Subject Runtime Contracts

Status: draft

**Branch**: `005-customer-subject-runtime` | **Date**: 2026-07-12 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/005-customer-subject-runtime/spec.md`

**Governed By**: `openspec/changes/add-hermes-customer-subject-runtime-contract/`

## Summary

Realize the openxFactory-neutral pattern in which one static Customer Hermes role template produces repeatable, isolated runtime Customer instances for domain-owned subjects such as projects, patients, and accounting client companies. The implementation adds a composable Draft 2020-12 schema family, fail-closed semantic validator and indexed fixtures, scoped PostgreSQL 15/16 operational contract with trusted-scope RLS and atomic migration/quarantine, reproducible release digest inventory and verifier, and content-addressed publication evidence. The exact reviewed release must land on `origin/main` before tagging; the existing Hermes Install feature then owns neutral interface alignment and the exact Gate G0 pin.

## Technical Context

**Language/Version**: Python 3.12 for validators/tests; YAML/JSON Schema Draft 2020-12 for contracts; PostgreSQL SQL compatible with majors 15 and 16; POSIX shell only for thin container/release entrypoints

**Primary Dependencies**: Python standard library, PyYAML 6.0.x, jsonschema 4.25.x with `referencing`, pytest 9.x, Git, Docker Engine, OpenSpec 1.5.x

**Storage**: Repository YAML/Markdown/SQL artifacts plus ephemeral PostgreSQL 15 and 16 containers for conformance; no deployed service state

**Testing**: pytest unit/contract/integration suites, self-describing fixture index, validator CLI subprocess tests, real PostgreSQL clean-apply/RLS/migration/concurrency tests, strict OpenSpec validation, supported DomainxFactory regression inventory

**Target Platform**: Linux development/CI environment with Git and Docker; offline consumer verification from locally available Git objects

**Project Type**: Domain-neutral contract family, standalone conformance CLI, release verifier, and database contract; no web service or UI

**Performance Goals**: Non-database schema/semantic suite completes within 30 seconds on `py-bench`; each PostgreSQL-major conformance run completes within 10 minutes; release and compatibility digest checks are linear in the inventoried file count

**Constraints**: Fail closed; no credentials, PII, tenant data, raw provider payloads, or host-absolute paths; v1 remains valid; one stack per G0 installation; no direct cross-layer table/blob access; raw Git blob digest identity; version allocated only at realization; exact main-line commit reviewed before tag; downstream Hermes edits remain outside this feature

**Scale/Scope**: One neutral contract family, one stack per installation, one Client and one Domain singleton, zero-to-many Customer instances, required two-Customer proof, three domain-alias examples, PostgreSQL 15/16, and the versioned supported-Domain regression set

## Constitution Check

*GATE: Passed before Phase 0 and re-checked after Phase 1 design.*

| Principle / constraint | Pre-research | Post-design | Evidence |
|---|---|---|---|
| I. Contract-First, Domain-Neutral Core | PASS | PASS | OpenSpec and feature spec use `customer_subject`; project/patient/client-company remain overlay examples only |
| II. Governed Change Flow | PASS | PASS | Strictly valid OpenSpec change is committed and handed one-to-one to this Speckit feature; OpenSpec tasks retain governance only |
| III. Document Lifecycle And Status | PASS | PASS | New canonical docs receive controlled status; proposal declares `code_surface` and `target_release`; feature docs remain Draft planning artifacts |
| IV. Schema And Artifact Discipline | PASS | PASS | Every YAML artifact will carry `schema_version` and `kind`; repository-relative paths only; README/manifest indices updated; no secrets or direct subject identifiers |
| V. Validation Gates | PASS | PASS | Existing validators, strict OpenSpec, self-describing fixtures, real PostgreSQL tests, release checks, and independent review are mandatory |
| VI. Versioned Content-Addressed Releases | PASS | PASS | Version allocated after final rebase; raw-blob digest inventory, exact main-line commit, matching manifest/changelog/tag, and downstream pins are explicit |
| VII. Fail-Closed Authority Boundaries | PASS | PASS | Closed states/actions/resources, trust-anchor grant chains, trusted scope, atomic operation authorization, quarantine, and negative matrices are specified |
| Shared-tree/worktree discipline | PASS | PASS | All feature work occurs on `005-customer-subject-runtime`; explicit-path staging only; release metadata integration serializes at final rebase |
| Runtime scope constraint | PASS | PASS | Only contracts, validators, fixtures, migrations, and test/reference tooling are added; no listening service or provider credential path |

No constitutional exception or complexity waiver is required.

## Project Structure

### Documentation (this feature)

```text
specs/005-customer-subject-runtime/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── acceptance-map.yaml
│   ├── postgres-conformance.md
│   ├── release-and-consumer-pin.md
│   ├── schema-inventory.md
│   └── validator-cli.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code And Canonical Artifacts (repository root)

```text
contracts/
├── hermes-runtime/
│   ├── README.md
│   ├── contract-index.yaml
│   ├── acceptance-map.yaml
│   ├── evidence-register.yaml
│   ├── *.schema.yaml
│   ├── hermes-operational-postgres-v2.sql
│   ├── migrations/
│   │   ├── v1-to-v2-mapping.schema.yaml
│   │   └── v1-to-v2.sql
│   └── fixtures/
│       ├── index.yaml
│       ├── domain-regression-inventory.yaml
│       ├── topology/
│       ├── references/
│       ├── pins/
│       │   └── consumer-receipt-wrong-repository.yaml
│       ├── authority/
│       ├── isolation/
│       ├── artifacts/
│       ├── approvals/
│       ├── traceability/
│       ├── jobs/
│       ├── postgres/
│       ├── migration/
│       ├── release/
│       └── regression/
├── schemas/
│   └── xfactory-domain-stack.schema.yaml
├── releases/
│   ├── release-digest-inventory.schema.yaml
│   └── <realized-bundle-tag>.digests.yaml
├── manifest.yaml
├── CHANGELOG.md
└── README.md

scripts/
├── validate-domain-factory.py
├── validate-hermes-runtime-contracts.py
├── validate-hermes-runtime-postgres.py
├── validate-contract-release.py
├── hermes-runtime-dataset-digest.py
├── run-hermes-runtime-postgres-tests.sh
└── hermes_runtime_validation/
    ├── loader.py
    ├── catalog.py
    ├── schema_registry.py
    ├── fixtures.py
    ├── acceptance.py
    ├── content.py
    ├── migration.py
    ├── domain_regression.py
    ├── release.py
    ├── consumer_handoff.py
    └── semantics/
        ├── topology.py
        ├── references.py
        ├── overlays.py
        ├── authority.py
        ├── evidence.py
        └── jobs.py

requirements/
├── hermes-runtime-contracts.in
└── hermes-runtime-contracts.lock

tests/hermes_runtime_contracts/
├── conftest.py
├── support.py
├── test_catalog_and_schema.py
├── test_fixture_index.py
├── test_acceptance_parity.py
├── test_content_resolution.py
├── test_validator_cli.py
├── test_topology_and_identity.py
├── test_topology_lifecycle.py
├── test_overlay_and_pins.py
├── test_authority_and_bindings.py
├── test_artifact_approval_trace.py
├── test_v2_jobs.py
├── test_release_inventory.py
├── test_domain_regression.py
├── test_consumer_handoff.py
└── postgres/
    ├── compose.yaml
    ├── images.lock.yaml
    ├── conftest.py
    ├── assertions/
    ├── evidence/
    ├── fixtures/
    ├── test_runner_contract.py
    ├── test_clean_apply.py
    ├── test_topology_lifecycle.py
    ├── test_roles_and_rls.py
    ├── test_scope_pooling.py
    ├── test_governed_evidence.py
    ├── test_authorization_races.py
    ├── test_migration.py
    ├── test_migration_recovery.py
    ├── test_quarantine.py
    └── test_ddl_drift.py

openspec/changes/add-hermes-customer-subject-runtime-contract/
├── proposal.md
├── design.md
├── evidence/
│   ├── provider-verification.yaml
│   ├── legacy-source-path-consumer-audit.md
│   ├── release-candidate-review.md
│   ├── release-publication.md
│   └── hermes-install-g0-handoff.yaml
├── specs/
└── tasks.md

docs/
├── xfactory-domain-factory-model.md
└── contract-versioning-policy.md
```

**Structure Decision**: Extend the repository's existing contract-family pattern rather than add an application package. Canonical data and schema artifacts live together under `contracts/hermes-runtime/`; pure validation/release CLIs stay under `scripts/`; executable acceptance belongs under one focused `tests/hermes_runtime_contracts/` suite. Speckit planning contracts describe the interfaces but do not duplicate canonical runtime schemas.

## Delivery Sequence

1. Build shared definitions and the topology/reference/overlay surface, then prove static-stack compatibility and two-Customer neutrality.
2. Add trust anchors, grants, bindings, operation authorization, artifacts, approvals, traceability, and the semantic fixture runner.
3. Add v2 PostgreSQL roles, trusted scope, RLS, append-only guards, governed operations, mapping contract, migration ledger, quarantine, and PostgreSQL 15/16 tests.
4. Add v2 job/run/event messages and unchanged-v1 compatibility evidence.
5. Add supported-Domain regression inventory, release inventory schema/verifier, consumer audit, documentation, and candidate metadata.
6. Rebase and allocate the next available bundle version, commit the exact candidate, run every gate and independent review, and merge without semantic drift.
7. Re-run the complete gate set on the exact `origin/main` commit if promotion changes the SHA, publish the matching annotated tag, and independently verify remote bytes.
8. Hand exact release evidence to the existing Hermes Install feature and keep G0/T009 closed until its exact landed revision and positive/negative pin evidence pass.

## Complexity Tracking

No constitution violation or exceptional subsystem is introduced. The breadth of schemas and tests reflects separate security authorities and durable record types required by the approved contract; combining them into an unconstrained generic record would weaken validation and fail closed behavior.
