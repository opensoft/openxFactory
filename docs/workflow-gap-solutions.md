# Workflow Gap Solutions

This document proposes concrete solutions for the known workflow gaps in openxFactory.

The goal is to turn the current principles into executable contracts between Hermes, Omnigent/Polly, workers, Spec Kit, and GitHub.

## Summary

The main solution is to make every workflow boundary produce a structured artifact that the next boundary must validate before continuing.

```text
Hermes job envelope
  -> Polly constitution check
  -> decomposition review packet
  -> approved feature DAG
  -> Spec Kit feature artifacts
  -> implementation branch
  -> branch admission packet
  -> PR
  -> merge council report
  -> GitHub enforced merge
  -> archived traceability
```

Each artifact has:

- an owner
- required fields
- a storage location
- validation rules
- a next allowed action

## 1. Job Envelope Schema

### Problem

Hermes-to-Polly handoff can degrade into ad hoc natural-language prompts.

### Solution

Hermes must send Polly a versioned job envelope for every engineering workflow.

The job envelope is the only valid way to start an Omnigent/Polly engineering job.

### Owner

Hermes creates the job envelope. Polly validates it before acting.

### Location

```text
.factory/jobs/<job-id>/job.yaml
```

Hermes may also store the canonical copy in its control-plane database.

### Schema

```yaml
job:
  id: JOB-2026-06-21-0001
  schema_version: 1
  job_type: epic_decomposition_for_speckit
  created_at: "2026-06-21T00:00:00-07:00"
  created_by: hermes

  project:
    id: ledgerlink
    repo: github.com/opensoft/ledgerlink
    default_branch: main
    local_workspace_hint: null

  governance:
    omnigent_constitution: docs/omnigent-constitution.md
    constitution_version: "2026-06-21"
    openspec_change: openspec/changes/add-invoice-retrieval
    epic_ref: docs/epics/EPIC-003.md
    hermes_approval: HA-2026-06-21-014

  allowed_phase:
    name: decomposition_only
    may_run_speckit: false
    may_edit_code: false
    may_open_pr: false

  required_outputs:
    - .factory/jobs/JOB-2026-06-21-0001/constitution-check.yaml
    - .factory/decomposition/FEAT-DAG.yaml
    - .factory/decomposition/acceptance-matrix.yaml
    - .factory/decomposition/bug-mapping-index.yaml
    - .factory/decomposition/pr-size-estimates.yaml
    - .factory/decomposition/orthogonality-review.md
    - .factory/decomposition/merge-plan.md

  gates:
    require_constitution_check: true
    require_feature_dag: true
    require_bug_mapping_index: true
    require_pr_size_estimates: true
    require_decomposition_review: true
    require_hermes_approval_before_speckit: true

  worker_requirements:
    role: reviewer
    labels:
      - coder_light
    allow_heavy_commands: false

  budgets:
    max_changed_lines_per_pr: 10000
    target_changed_lines_per_pr: 6000
    max_model_cost_usd: 25
    max_wall_clock_minutes: 120

  callbacks:
    approval_required:
      - decomposition_complete
      - before_speckit_specify
    status_channel: hermes
```

### Validation Rules

Polly must reject the job if:

- `job_type` is unknown
- constitution path or version is missing
- OpenSpec scope is missing
- `allowed_phase` is missing
- required outputs are missing
- worker role is incompatible with requested work

## 2. Constitution Enforcement Hook

### Problem

The Omnigent constitution is binding in documentation, but no workflow step forces Polly to load and validate it.

### Solution

Every Polly job must start with a constitution enforcement hook.

### Workflow

```text
Hermes creates job envelope
  -> Polly loads constitution
  -> Polly validates job envelope against constitution
  -> Polly writes constitution-check.yaml
  -> Hermes or control service validates the check
  -> Polly continues only if status is pass
```

### Location

```text
.factory/jobs/<job-id>/constitution-check.yaml
```

### Schema

```yaml
constitution_check:
  job_id: JOB-2026-06-21-0001
  constitution_path: docs/omnigent-constitution.md
  constitution_version: "2026-06-21"
  status: pass
  checked_at: "2026-06-21T00:05:00-07:00"
  checked_by: polly
  allowed_phase:
    name: decomposition_only
    may_run_speckit: false
    may_edit_code: false
    may_open_pr: false
  required_rules:
    openspec_before_speckit: pass
    decompose_before_building: pass
    user_perceivable_features: pending
    bug_traceability: pending
    max_10000_changed_lines: pending
    branch_admission_before_pr: pass
  blockers: []
```

### Enforcement Rule

No `/speckit.*` command may run unless the latest constitution check explicitly allows the current phase.

## 3. Decomposition Review Gate

### Problem

Feature decomposition quality is the keystone of the system, but the review gate is not yet formal.

### Solution

Create a required decomposition review gate before Hermes approves any feature for Spec Kit.

### Workflow

```text
Polly produces decomposition artifacts
  -> decomposition reviewer checks feature quality
  -> orthogonality reviewer checks DAG and shared paths
  -> size reviewer checks 10K-line risk
  -> bug-mapping reviewer checks support traceability
  -> Hermes approves or rejects the feature DAG
```

### Location

```text
.factory/decomposition/reviews/
  decomposition-review.yaml
  orthogonality-review.yaml
  pr-size-review.yaml
  bug-mapping-review.yaml
```

### Review Schema

```yaml
decomposition_review:
  job_id: JOB-2026-06-21-0001
  decision: pass
  reviewers:
    - name: decomposition_reviewer
      decision: pass
    - name: orthogonality_reviewer
      decision: pass
    - name: pr_size_reviewer
      decision: warn
    - name: bug_mapping_reviewer
      decision: pass
  required_fixes: []
  warnings:
    - "FEAT-023 is estimated near the 10K limit and should target less than 6K during implementation."
```

### Approval Rule

Hermes may approve `/speckit.specify` only for features whose decomposition review is `pass` or explicitly exception-approved.

## 4. Branch Admission Packet

### Problem

Branch admission is required before PR creation, but the packet format is not defined.

### Solution

Polly must produce a branch admission packet after implementation and local review, before asking Hermes to open a PR.

### Location

```text
.factory/admissions/<feature-id>/branch-admission.yaml
.factory/admissions/<feature-id>/branch-admission.md
```

### Schema

```yaml
branch_admission:
  feature_id: FEAT-014
  branch: feat/014-invoice-retrieval
  job_id: JOB-2026-06-21-0042
  decision: pass
  recommendation: open_pr

  size:
    changed_lines: 4230
    under_10000_changed_lines: true
    files_changed: 18

  deterministic_checks:
    format: pass
    lint: pass
    typecheck: pass
    targeted_tests: pass
    changed_area_build: pass
    secrets_scan: pass

  traceability:
    openspec_change: openspec/changes/add-invoice-retrieval
    speckit_feature: specs/014-invoice-retrieval
    acceptance_criteria_evidence: .factory/traceability/FEAT-014/evidence.yaml
    spec_drift_check: pass

  local_reviews:
    opus: pass
    codex: pass
    non_anthropic: pass
    unresolved_blockers: []

  next_action: request_hermes_pr_approval
```

### Decision Values

```text
pass
fix_required
split_required
abandon
defer
```

## 5. Worker Command Policy

### Problem

Cloud PC capacity depends on keeping coder, tester, integrator, and reviewer roles separate. Without command policy, coder sessions may become heavy build/test sessions.

### Solution

Define role-based command policy and enforce it through Polly scheduling and worker labels.

### Location

```text
.factory/workers/command-policy.yaml
```

### Policy

```yaml
worker_command_policy:
  coder_light:
    allowed:
      - git_status
      - git_diff
      - git_branch
      - file_read
      - file_edit
      - formatter_changed_files
      - lint_changed_files
      - targeted_unit_tests
      - speckit_feature_commands
    denied:
      - full_test_suite
      - full_monorepo_build
      - docker_compose
      - browser_e2e
      - database_integration_suite
      - broad_dependency_audit

  tester_heavy:
    allowed:
      - full_test_suite
      - full_build
      - docker_compose
      - browser_e2e
      - database_integration_suite
      - migration_dry_run
      - dependency_audit

  integrator_medium:
    allowed:
      - git_fetch
      - git_rebase_check
      - merge_conflict_check
      - integration_branch
      - contract_compatibility_check
      - changed_area_regression
    denied:
      - broad_unrelated_refactor
      - direct_feature_scope_expansion

  reviewer_api:
    allowed:
      - diff_review
      - traceability_review
      - security_review
      - architecture_review
    denied:
      - code_modification_without_fix_job
      - full_test_suite
```

### Enforcement Rule

Polly must schedule jobs only to workers whose role allows the requested command class.

## 6. Artifact Storage Contract

### Problem

The plan names artifacts, but does not define canonical storage, ownership, update rules, or retention.

### Solution

Define an artifact contract with three storage classes.

### Storage Classes

```yaml
artifact_storage_classes:
  repo_committed:
    purpose: "Durable traceability and reproducible planning artifacts."
    examples:
      - feature DAG
      - bug mapping index
      - acceptance matrix
      - merge council report summary

  control_plane:
    purpose: "Hermes canonical operational state."
    examples:
      - approval records
      - job envelopes
      - worker registry state
      - status dashboard data

  object_storage:
    purpose: "Large generated artifacts and logs."
    examples:
      - full test logs
      - build artifacts
      - screenshots
      - coverage reports
      - raw reviewer transcripts
```

### Artifact Index

```yaml
artifact_index:
  - artifact: job_envelope
    owner: hermes
    storage: control_plane
    repo_copy: .factory/jobs/<job-id>/job.yaml
    mutable: false
    retention: permanent

  - artifact: feature_dag
    owner: polly
    storage: repo_committed
    path: .factory/decomposition/feature-dag.yaml
    mutable: until_hermes_approval
    retention: permanent

  - artifact: branch_admission_packet
    owner: polly
    storage: repo_committed
    path: .factory/admissions/<feature-id>/branch-admission.yaml
    mutable: append_only_after_approval
    retention: permanent

  - artifact: full_test_logs
    owner: tester_worker
    storage: object_storage
    path: artifacts/<job-id>/tests/
    mutable: false
    retention: 180_days
```

### Rule

Every gate must name the artifacts it requires and the location from which they are read.

## 7. GitHub Integration Contract

### Problem

GitHub is the final enforcement layer, but required checks and check publishers are not fully specified.

### Solution

Define a repo ruleset template and required status check ownership.

### Required Checks

```yaml
github_required_checks:
  - name: hermes/constitution
    publisher: hermes
    required_for: pr_open_policy

  - name: polly/decomposition
    publisher: polly
    required_for: pr_open_policy

  - name: polly/branch-admission
    publisher: polly
    required_for: branch_protection

  - name: polly/cross-review
    publisher: polly
    required_for: branch_protection

  - name: hermes/merge-council
    publisher: hermes
    required_for: branch_protection

  - name: ci/build
    publisher: github_actions
    required_for: branch_protection

  - name: ci/test
    publisher: github_actions
    required_for: branch_protection

  - name: security/codeql
    publisher: github_actions
    required_for: branch_protection
```

### Branch Protection Template

```yaml
branch_protection:
  require_pull_request: true
  required_approving_reviews: 1
  require_codeowners: true
  require_conversation_resolution: true
  require_linear_history: true
  require_merge_queue: true
  required_checks:
    - polly/branch-admission
    - polly/cross-review
    - hermes/merge-council
    - ci/build
    - ci/test
    - security/codeql
```

### Rule

No repository is considered factory-managed until it has the required ruleset or an explicit Hermes exception.

## 8. Failure and Retry Workflow

### Problem

The happy path is defined, but common failure modes need standard handling.

### Solution

Define failure classes, owners, and recovery action.

```yaml
failure_policy:
  spec_drift:
    owner: polly
    action: stop_and_return_to_hermes
    required_artifact: spec-drift-report.md

  feature_over_10000_lines:
    owner: polly
    action: split_feature_or_request_exception
    required_artifact: split-proposal.yaml

  worker_died:
    owner: polly
    action: reschedule_from_last_checkpoint
    required_artifact: worker-failure-report.yaml

  flaky_tests:
    owner: tester_worker
    action: rerun_with_flake_policy
    required_artifact: flake-report.yaml

  reviewer_disagreement:
    owner: hermes
    action: convene_tiebreak_review
    required_artifact: reviewer-disagreement.md

  merge_council_defer:
    owner: hermes
    action: collect_missing_inputs
    required_artifact: defer-reason.yaml

  github_checks_fail_after_approval:
    owner: polly
    action: fix_branch_and_reenter_merge_council
    required_artifact: post-approval-failure-report.md

  branch_stale:
    owner: integrator
    action: rebase_or_merge_main_and_rerun_required_checks
    required_artifact: stale-branch-report.yaml
```

### Retry Rule

Retries must be bounded and recorded.

```yaml
retry_policy:
  max_automatic_retries: 2
  require_hermes_after_retries_exhausted: true
  retry_log: .factory/jobs/<job-id>/retries.yaml
```

## 9. Human Approval UX

### Problem

Hermes approval is central, but approval records and decision scope are not formalized.

### Solution

Define a standard approval object for every human or Hermes approval gate.

### Location

```text
.factory/approvals/<approval-id>.yaml
```

### Schema

```yaml
approval:
  id: HA-2026-06-21-014
  type: decomposition_approval
  project: ledgerlink
  feature_ids:
    - FEAT-014
    - FEAT-015
  requested_by: polly
  approver: hermes
  decision: approved
  decided_at: "2026-06-21T10:15:00-07:00"
  scope:
    allowed:
      - run_speckit_specify
    denied:
      - run_speckit_implement
      - open_pr
  conditions:
    - "Only features in parallel_group 0 may proceed."
    - "No feature may exceed 10,000 changed lines."
  expires_at: "2026-06-28T10:15:00-07:00"
  audit_note: "Approved decomposition for initial invoice retrieval features."
```

### Decision Values

```text
approved
approved_with_conditions
rejected
deferred
expired
revoked
```

### Rule

Every gate transition that requires Hermes approval must reference an approval ID.

## 10. Bug Intake Loop

### Problem

The plan supports bug-to-feature traceability, but the actual bug intake loop is not defined.

### Solution

Define a bug intake workflow that maps user reports to feature records and creates the appropriate fix path.

### Workflow

```text
User reports bug
  -> Hermes captures report
  -> Hermes searches bug mapping index
  -> Hermes links likely feature, AC, PR, and merge council report
  -> Polly reproduces on worker
  -> Hermes creates GitHub issue or fix job
  -> Polly implements regression fix
  -> branch admission
  -> PR
  -> merge council
```

### Intake Record

```yaml
bug_intake:
  id: BUG-2026-06-21-001
  reported_by: customer_support
  report: "Invoice retrieval is showing invoices from another organization."
  project: ledgerlink
  suspected_features:
    - feature_id: FEAT-014
      confidence: high
      reason: "Report matches user_reported_names and primary failure mode."
  linked_acceptance_criteria:
    - FEAT-014.AC-03
  linked_prs:
    - 238
  linked_merge_council_reports:
    - .factory/merge-council/FEAT-014/report.md
  reproduction_status: pending
  next_action: create_reproduction_job
```

### Fix Classification

```yaml
bug_fix_classification:
  regression_fix:
    description: "Existing feature behavior is broken."
  missing_acceptance_criterion:
    description: "Bug reveals a requirement that was not captured."
  new_feature_request:
    description: "Report asks for behavior outside approved scope."
  support_or_data_issue:
    description: "No code change needed."
```

### Rule

If the bug reveals missing requirements, Hermes must create or update OpenSpec before Polly implements the fix.

## Implementation Order

Recommended order for turning these solutions into executable factory behavior:

1. Job envelope schema
2. Constitution enforcement hook
3. Decomposition review gate
4. Branch admission packet
5. Worker command policy
6. Artifact storage contract
7. Human approval object
8. GitHub integration contract
9. Failure and retry policy
10. Bug intake loop

This order builds the control path before adding broader operational automation.

