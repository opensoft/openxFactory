# Feature Decomposition Standard

Hermes requires Polly to decompose every approved epic into small, user-perceivable, traceable features before Spec Kit starts.

The goal is not just parallel implementation. The goal is to produce feature slices that match how users experience the product, how support will receive bugs, and how engineering will trace a defect back to the exact scope that introduced it.

## Source Provenance

Reviewed sources:

- `/home/brett/projects/Agents/Omnigent-Install/docs/runbooks/phase3-feature-decomposition.md`
- `/home/brett/projects/Agents/Omnigent-Install/examples/project-alfa-decomposition/decomposition-packet.example.yaml`
- `/home/brett/projects/Agents/Omnigent-Install/docs/omnigent-implementation-plan.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/project-master-plan.md`
- `docs/omnigent-constitution.md`
- `docs/traceability-model.md`

The install repo source docs remain in place until a later migration feature
marks them as canonical links, legacy copies, or implementation runbooks.

## Core Rule

Each feature must be:

- small enough for one PR
- user-perceivable
- independently testable
- traceable to specific epic acceptance criteria
- owned by a bounded set of paths and contracts
- understandable as a bug ownership unit
- limited to 10,000 changed lines or less per PR

Polly must not run `/speckit.specify` until the feature decomposition has passed Hermes approval.

## Size Limit

The hard PR size budget is:

```yaml
pr_size_policy:
  max_changed_lines: 10000
  target_changed_lines: 3000-6000
  preferred_review_size: under_3000
  oversized_action: split_feature_or_create_foundation_feature
```

The 10,000 line limit is a maximum, not a target. Polly should prefer smaller PRs when the feature can still remain user-perceivable and independently testable.

Changed lines include:

- production code
- tests
- generated files committed to the repo
- migrations
- fixtures
- documentation required by the feature
- Spec Kit artifacts when included in the PR

Polly should estimate size during decomposition and verify actual size before PR admission.

## User-Perceivable Feature Boundary

A feature should map to something a user, operator, administrator, support person, or domain expert can name.

Good feature names:

- Customer profile management
- Invoice retrieval
- Payment method vault
- Cross-tenant invoice access denial
- Import bank transactions
- Approve reimbursement request

Weak feature names:

- Backend invoice API
- Frontend invoice UI
- Database schema updates
- Shared utilities
- Refactor services
- Add endpoints

Technical work is allowed, but it should usually be framed as a foundation, contract, migration, or enablement feature with explicit downstream user-visible features.

## Bug Traceability Rule

Users report bugs in the language of perceived features. The feature model must support that.

If a user says:

```text
"Invoice retrieval is showing invoices from another organization."
```

Hermes and Polly should be able to map that report to:

```text
Feature: FEAT-014 Invoice Retrieval
Acceptance Criterion: FEAT-014.AC-03 Cross-tenant invoice denial
PR: #238
Merge Council Report: .factory/merge-council/FEAT-014/report.md
Tests: invoice-route.test.ts
Owned Paths:
  - apps/api/invoices/**
  - apps/web/invoices/**
```

If a bug cannot be mapped cleanly to one or two features, decomposition was probably too broad, too technical, or too poorly traced.

## Orthogonality and Encapsulation

Features should be both orthogonal and encapsulated.

Orthogonal means:

- features can be reasoned about independently
- parallel features do not require each other's unmerged code
- each feature has its own acceptance criteria
- each feature can be tested without hidden dependency on another feature branch
- shared contracts are explicit

Encapsulated means:

- the feature owns a coherent product behavior
- implementation paths are bounded
- the feature can be released, reverted, or debugged as a unit
- support and engineering can identify which feature owns a bug
- related UI, API, domain logic, and tests travel together when needed

Avoid decomposing by technical layer when the user-visible behavior spans layers. For example, "invoice retrieval" should usually include the API, service logic, UI surface, and tests required for the user to retrieve invoices safely.

## Vertical Slice Preference

Prefer vertical slices over horizontal technical slices.

Better:

```text
FEAT-014 Invoice Retrieval
  - invoice list UI
  - invoice retrieval API
  - authorization check
  - service query
  - tests for allowed and denied retrieval
```

Worse:

```text
FEAT-014 Invoice Backend
FEAT-015 Invoice Frontend
FEAT-016 Invoice Tests
```

Separate frontend/backend/test features only when they are independently valuable and independently testable.

## Foundation Features

Some work is not directly user-visible but is still necessary. Polly may create foundation features when needed.

Foundation features should be small and explicitly connected to downstream user-visible features.

Examples:

- Shared identity contract
- Tenant ownership middleware
- Invoice domain model skeleton
- Migration for immutable customer IDs
- Event envelope contract

Foundation features must declare:

- why they are needed
- which user-visible features depend on them
- exported contracts
- owned paths
- merge barrier behavior
- test evidence for the foundation itself

Example:

```yaml
id: FEAT-000
title: Tenant ownership contract
type: foundation
user_visible: false
reason: "Multiple user-visible features require the same tenant ownership check."
downstream_features:
  - FEAT-014
  - FEAT-021
contract_exports:
  - TenantScopedResource
  - assertTenantOwnership
merge_barrier: true
max_changed_lines: 3000
```

## Feature Types

Use feature type to make intent explicit.

```yaml
feature_types:
  user_visible:
    description: "A product behavior users can perceive and report bugs against."
  foundation:
    description: "A prerequisite contract or capability needed by later user-visible features."
  migration:
    description: "A data or schema transition with bounded behavior and rollback plan."
  integration:
    description: "A cross-feature or external-system connection."
  hardening:
    description: "Security, reliability, or correctness work tied to named user behavior."
```

Most features should be `user_visible`. Too many foundation, migration, or hardening features means the epic is drifting into technical batching.

## Decomposition Gates

Polly must evaluate every candidate feature against these gates:

```text
1. User-perceivable behavior is named.
2. Bug reports can map cleanly to the feature.
3. Acceptance criteria are feature-specific.
4. Feature can fit in one PR.
5. Estimated changed lines are <= 10,000.
6. Target changed lines are preferably <= 6,000.
7. Feature has bounded owned paths.
8. Shared contracts are explicit.
9. Dependencies are represented in the DAG.
10. Parallel implementation does not require unmerged code from another feature.
11. Tests can validate the feature independently.
12. Rollback/revert impact is understandable.
```

If a feature fails one of these gates, Polly must split it, mark it blocked, or create a smaller foundation feature.

## Oversized Feature Handling

If a candidate feature is likely to exceed 10,000 changed lines, Polly must not approve it for Spec Kit.

Polly should split oversized features by:

- user workflow step
- acceptance criterion group
- role or permission boundary
- domain sub-capability
- data lifecycle phase
- read path vs write path, only when each side is independently valuable
- foundation contract plus user-visible slices

Example split:

```text
Too large:
  FEAT-020 Billing Management

Better:
  FEAT-020 Customer billing profile
  FEAT-021 Payment method vault
  FEAT-022 Invoice retrieval
  FEAT-023 Invoice generation
  FEAT-024 Charge invoice
  FEAT-025 Billing activity audit log
```

## Bug Mapping Fields

Every feature must include fields that support future bug triage.

```yaml
bug_mapping:
  user_reported_names:
    - "invoice retrieval"
    - "view invoice"
    - "invoice details"
  visible_surfaces:
    - "Invoices page"
    - "Invoice detail drawer"
    - "GET /api/invoices/:id"
  primary_failure_modes:
    - "wrong invoice returned"
    - "invoice not found"
    - "cross-tenant invoice visible"
    - "invoice detail page fails to load"
  support_routing:
    owner_feature: FEAT-014
    owner_domain: billing
```

These fields let Hermes map support reports and production defects back to the feature graph.

## Feature DAG Shape

The feature DAG should include product, engineering, and bug-traceability metadata.

```yaml
features:
  - id: FEAT-014
    title: Invoice Retrieval
    type: user_visible
    phase: PHASE-002
    epic_refs:
      - EPIC-003.AC-07
      - EPIC-003.AC-08
    user_visible: true
    user_story: "As an authorized billing user, I can retrieve invoice details for my organization."
    bug_mapping:
      user_reported_names:
        - "invoice retrieval"
        - "view invoice"
      visible_surfaces:
        - "Invoices page"
        - "Invoice detail drawer"
        - "GET /api/invoices/:id"
      primary_failure_modes:
        - "wrong invoice returned"
        - "cross-tenant invoice visible"
    acceptance_criteria:
      - id: FEAT-014.AC-01
        text: "Authorized users can retrieve invoice details for their organization."
      - id: FEAT-014.AC-02
        text: "Missing invoices return a not-found response."
      - id: FEAT-014.AC-03
        text: "Invoices from another organization are denied."
    estimated_changed_lines: 4200
    max_changed_lines: 10000
    target_changed_lines: 6000
    owns_paths:
      - apps/api/invoices/**
      - apps/web/invoices/**
      - tests/invoices/**
    shared_paths:
      - packages/auth/tenant-ownership.ts
    shared_contracts_imported:
      - TenantId
      - InvoiceId
    shared_contracts_exported:
      - InvoiceDetail
    depends_on:
      - FEAT-000
    dependency_type: contract
    parallel_group: 1
    can_run_speckit_specify: true
    can_run_speckit_implement: true
    split_required: false
```

## Decomposition Packet Requirements

Polly must produce a decomposition packet before any feature enters Spec Kit.
The packet is a Hermes-reviewed artifact, not an implementation branch.

Minimum packet fields:

```yaml
decomposition_packet:
  id:
  schema_version:
  project:
  epic_id:
  source_type:
  source_path:
  produced_by: Polly
  approval_state: pending
  constitution:
    max_changed_lines_per_pr: 10000
    orthogonal_features_required: true
    encapsulated_features_required: true
    user_perceivable_feature_required: true
    bug_report_mapping_required: true
    no_speckit_before_hermes_approval: true
  phases: []
  features: []
  dependency_dag:
    nodes: []
    edges: []
  traceability:
    edges: []
```

Validation rules:

- every feature has a changed-line budget at or below 10,000;
- every feature is user-perceivable or explicitly marked as a foundation,
  migration, integration, or hardening feature;
- every feature has bug-report mapping;
- every feature has an encapsulation boundary;
- phases contain the full feature set exactly once;
- the dependency graph is acyclic;
- each approved feature enters Spec Kit at `/speckit.specify`;
- the job forbids Spec Kit, code edits, PR creation, and source mutation before
  Hermes approves the decomposition packet.

## Hermes-to-Polly Decomposition Prompt

Hermes should send Polly a standard decomposition job that includes this feature standard.

```text
Run pre-Spec-Kit decomposition for this epic.

Do not implement code.
Do not run /speckit.specify.

Decompose the epic into small, user-perceivable, traceable features.

Each feature must:
- fit in one PR
- stay at or below 10,000 changed lines
- target 3,000 to 6,000 changed lines when possible
- map to behavior a user or support person can name
- include bug-mapping fields
- include feature-specific acceptance criteria
- declare owned paths
- declare shared contracts
- declare dependency edges
- be independently testable
- identify whether it can run /speckit.specify now
- identify whether it can run /speckit.implement now

Prefer vertical slices that include UI, API, domain logic, and tests required for the behavior.
Do not split into backend/frontend/test-only features unless each slice is independently user-valuable.
If a feature is too large, split it before Spec Kit.
If shared contracts are needed, create a small foundation feature and mark it as a merge barrier.

Produce:
1. phase breakdown
2. feature DAG
3. acceptance criteria matrix
4. bug mapping index
5. estimated PR size report
6. orthogonality analysis
7. merge sequencing plan
8. list of features approved for /speckit.specify
9. list of features blocked or requiring split

Stop after producing artifacts and request Hermes approval.
```

## Bug Mapping Index

Each project should maintain a bug mapping index derived from the feature DAG.

```yaml
bug_mapping_index:
  - feature_id: FEAT-014
    title: Invoice Retrieval
    user_reported_names:
      - invoice retrieval
      - view invoice
      - invoice details
    visible_surfaces:
      - Invoices page
      - Invoice detail drawer
      - GET /api/invoices/:id
    primary_failure_modes:
      - wrong invoice returned
      - cross-tenant invoice visible
      - invoice detail fails to load
    owned_paths:
      - apps/api/invoices/**
      - apps/web/invoices/**
```

This index helps Hermes route bug reports, identify likely owner features, and retrieve the original OpenSpec, Spec Kit, PR, and merge council records.

## Approval Result

Hermes should approve decomposition only when the output includes:

- feature DAG
- PR size estimates
- bug mapping index
- acceptance criteria matrix
- orthogonality analysis
- split list for oversized or muddy features
- merge sequencing plan

Approval means Polly may proceed to `/speckit.specify` only for features explicitly marked ready.
