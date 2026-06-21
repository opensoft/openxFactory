# Merge Council and Readiness Reports

Hermes manages the merge council. GitHub remains the hard enforcement layer.

The merge council is the formal decision process that evaluates whether a pull request is ready to merge after Polly has implemented the feature, opened the PR, and GitHub checks have run.

The merge council does not replace GitHub branch protection, required reviews, status checks, CODEOWNERS, or merge queue. It produces a required readiness decision and records the reasoning behind that decision.

## Responsibility Split

```text
Polly / Omnigent
  -> implements feature branch
  -> runs local deterministic checks
  -> runs local branch review
  -> opens PR after Hermes admission
  -> fixes branch when council sends required fixes

Hermes
  -> convenes merge council
  -> applies project policy
  -> evaluates traceability
  -> records decision
  -> tells Polly what must be fixed
  -> publishes merge-readiness status

GitHub
  -> stores PR and review history
  -> runs CI and security checks
  -> enforces branch protection
  -> enforces merge queue
  -> performs final merge
```

## Council Timing

The merge council starts after:

- a PR exists
- GitHub Actions or required checks have produced results
- Polly has attached or linked the local branch admission packet
- Spec Kit artifacts are present
- implementation diff is available

The merge council should not be used before PR creation. Before a PR exists, Hermes is deciding PR admission, not merge readiness.

## Merge Council Flow

```text
1. Polly opens PR after Hermes PR admission.
2. GitHub Actions and PR review systems run.
3. Hermes gathers the PR packet.
4. Hermes assigns council reviewers.
5. Each reviewer returns a scoped decision.
6. Hermes synthesizes the merge readiness report.
7. If not ready, Hermes sends required fixes to Polly.
8. Polly fixes the PR branch and updates the PR.
9. GitHub checks rerun.
10. Hermes reconvenes council or reruns affected reviewers.
11. If ready, Hermes marks merge council check successful.
12. GitHub branch protection and merge queue decide final merge eligibility.
```

## Council Reviewers

The baseline council should include:

```yaml
merge_council:
  required:
    - spec_traceability_reviewer
    - security_reviewer
    - test_reviewer
    - architecture_reviewer
    - maintainability_reviewer
    - integration_reviewer
  optional:
    - ux_reviewer
    - data_migration_reviewer
    - performance_reviewer
    - compliance_reviewer
    - domain_expert_reviewer
```

Reviewers should have narrow jurisdictions. The council is stronger when reviewers answer focused questions instead of all giving broad opinions.

### Spec Traceability Reviewer

Checks:

- PR implements the exact approved feature scope.
- All acceptance criteria are covered.
- Implementation evidence is linked to acceptance criteria.
- Spec Kit artifacts match the implemented behavior.
- No unrelated changes are included.
- No implementation drift from the approved plan is present.

### Security Reviewer

Checks:

- authorization and authentication
- tenant isolation
- secrets handling
- injection risks
- unsafe deserialization
- sensitive data exposure
- dependency and supply-chain risks

### Test Reviewer

Checks:

- each acceptance criterion has test evidence or justified non-test evidence
- tests would fail without the change
- edge cases are covered
- integration boundaries are tested
- mocks are appropriate
- CI failures are understood

### Architecture Reviewer

Checks:

- implementation fits the existing architecture
- layering is preserved
- shared contracts are respected
- no unnecessary edits to shared/core files
- no hidden coupling to unmerged parallel features
- no duplicate or incompatible abstractions

### Maintainability Reviewer

Checks:

- complexity
- naming
- readability
- duplication
- dead code
- excessive generated bloat
- long-term operability

### Integration Reviewer

Checks:

- branch is current enough against main
- migrations are compatible
- APIs remain compatible
- feature dependencies are satisfied
- conflicts with recent parallel features are identified
- merge order remains valid

## Reviewer Result Format

Each council reviewer should return structured output.

```yaml
reviewer: security_reviewer
decision: block
blocking: true
severity: high
summary: "Invoice retrieval does not verify organization ownership."
findings:
  - id: SEC-001
    severity: high
    blocking: true
    file: apps/api/routes/invoices.ts
    issue: "Missing authorization check before invoice access."
    required_fix: "Verify organization ownership before returning invoice data."
    evidence:
      spec_ref: FEAT-014.AC-03
      code_ref: apps/api/routes/invoices.ts
```

Allowed decisions:

```text
pass
warn
block
not_applicable
```

Severity values:

```text
low
medium
high
critical
```

## Merge Readiness Decisions

Hermes synthesizes reviewer outputs into one readiness decision.

Allowed readiness decisions:

```text
READY
NOT_READY
READY_WITH_WARNINGS
DEFER
```

Decision rules:

- `READY`: no blocking findings, all required checks pass, acceptance criteria are covered.
- `READY_WITH_WARNINGS`: no blocking findings, but non-blocking risks or follow-up items exist.
- `NOT_READY`: one or more blocking findings exist.
- `DEFER`: decision cannot be made because required inputs are missing or external dependency state is unresolved.

## Required Inputs

The merge council should review:

- OpenSpec change proposal and delta specs
- Hermes feature approval record
- Spec Kit `spec.md`
- Spec Kit `plan.md`
- Spec Kit `tasks.md`
- implementation diff
- changed file list
- CI results
- local branch admission packet
- security scan
- test coverage
- architecture notes
- GitHub PR discussion and review comments
- dependency and migration notes, when applicable

## Merge Readiness Report Template

```markdown
# Merge Readiness Report

Feature: FEAT-014 Invoice Retrieval
PR: #238
Decision: NOT_READY
Council Run: HMC-2026-06-21-001

## Inputs Reviewed

- OpenSpec change proposal
- OpenSpec delta specs
- Hermes feature approval
- spec.md
- plan.md
- tasks.md
- implementation diff
- changed file list
- local branch admission packet
- CI results
- security scan
- test coverage
- architecture notes
- PR comments

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| FEAT-014.AC-01 | Yes | invoice-route.test.ts | |
| FEAT-014.AC-02 | Yes | invoice-service.ts | |
| FEAT-014.AC-03 | No | Missing | Cross-tenant denial missing |

## Council Results

| Reviewer | Decision | Blocking | Summary |
|---|---|---:|---|
| Spec Traceability | Block | Yes | AC-03 lacks evidence. |
| Security | Block | Yes | Organization ownership check missing. |
| Tests | Block | Yes | Cross-tenant denial test missing. |
| Architecture | Pass | No | Fits existing invoice service pattern. |
| Maintainability | Warn | No | Error naming could be clearer. |

## Blocking Findings

| ID | Reviewer | Severity | Finding | Required Fix |
|---|---|---|---|---|
| SEC-001 | Security | High | Missing organization ownership check. | Verify organization ownership before returning invoice data. |
| TEST-001 | Tests | High | Cross-tenant denial is not tested. | Add access-denied test for invoice owned by another organization. |
| SPEC-001 | Spec Traceability | High | FEAT-014.AC-03 has no implementation evidence. | Update evidence after implementing ownership check. |

## Required Fixes

1. Add organization ownership check.
2. Add cross-tenant access-denied test.
3. Update implementation evidence for AC-03.

## Non-Blocking Findings

1. Consider clearer naming for invoice access errors.

## Hermes Decision

Decision: NOT_READY

The PR must return to Polly for targeted fixes. Polly should only address the blocking findings above and avoid unrelated refactoring.
```

## Machine-Readable Report Shape

Hermes should store the merge readiness result in machine-readable form as well as Markdown.

```yaml
merge_readiness:
  council_run: HMC-2026-06-21-001
  feature_id: FEAT-014
  feature_title: Invoice Retrieval
  pr: 238
  decision: NOT_READY
  inputs_reviewed:
    - openspec_change
    - openspec_delta_specs
    - hermes_feature_approval
    - speckit_spec
    - speckit_plan
    - speckit_tasks
    - implementation_diff
    - changed_file_list
    - branch_admission_packet
    - ci_results
    - security_scan
    - test_coverage
    - architecture_notes
  acceptance_criteria:
    - id: FEAT-014.AC-01
      covered: true
      evidence:
        - invoice-route.test.ts
      notes: null
    - id: FEAT-014.AC-02
      covered: true
      evidence:
        - invoice-service.ts
      notes: null
    - id: FEAT-014.AC-03
      covered: false
      evidence: []
      notes: "Cross-tenant denial missing."
  council_results:
    - reviewer: spec_traceability
      decision: block
      blocking: true
      summary: "AC-03 lacks evidence."
    - reviewer: security
      decision: block
      blocking: true
      summary: "Organization ownership check missing."
    - reviewer: tests
      decision: block
      blocking: true
      summary: "Cross-tenant denial test missing."
    - reviewer: architecture
      decision: pass
      blocking: false
      summary: "Fits existing invoice service pattern."
    - reviewer: maintainability
      decision: warn
      blocking: false
      summary: "Error naming could be clearer."
  blocking_findings:
    - id: SEC-001
      reviewer: security
      severity: high
      finding: "Missing organization ownership check."
      required_fix: "Verify organization ownership before returning invoice data."
    - id: TEST-001
      reviewer: tests
      severity: high
      finding: "Cross-tenant denial is not tested."
      required_fix: "Add access-denied test for invoice owned by another organization."
    - id: SPEC-001
      reviewer: spec_traceability
      severity: high
      finding: "FEAT-014.AC-03 has no implementation evidence."
      required_fix: "Update evidence after implementing ownership check."
  required_fixes:
    - "Add organization ownership check."
    - "Add cross-tenant access-denied test."
    - "Update implementation evidence for AC-03."
  non_blocking_findings:
    - "Consider clearer naming for invoice access errors."
  next_action: send_to_polly_for_fix
```

## GitHub Status Check

Hermes should publish a required status check for merge council readiness.

Recommended check name:

```text
hermes/merge-council
```

Recommended statuses:

```text
success = READY or READY_WITH_WARNINGS
failure = NOT_READY
pending = council running
neutral = DEFER or not applicable
```

Branch protection should require this check along with normal CI and review checks.

Example required checks:

```text
ci/build
ci/test
lint
typecheck
security/codeql
speckit/traceability
polly/branch-admission
polly/cross-review
hermes/merge-council
```

## Fix Loop

When the council returns `NOT_READY`, Hermes should send Polly a targeted fix packet.

```yaml
fix_request:
  source: hermes_merge_council
  council_run: HMC-2026-06-21-001
  feature_id: FEAT-014
  pr: 238
  branch: feat/014-invoice-retrieval
  required_fixes:
    - id: SEC-001
      instruction: "Add organization ownership check before invoice data is returned."
    - id: TEST-001
      instruction: "Add cross-tenant access-denied test."
    - id: SPEC-001
      instruction: "Update AC-03 evidence after fix."
  constraints:
    - "Fix only the listed blockers."
    - "Do not introduce unrelated refactors."
    - "Rerun affected deterministic checks."
    - "Return updated evidence map."
```

Polly then fixes the PR branch, reruns relevant checks, and returns an updated packet to Hermes.

