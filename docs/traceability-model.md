# Traceability Model

The factory must document traceability from epic to merge.

## Source Provenance

Reviewed sources:

- `/home/brett/projects/Agents/Omnigent-Install/docs/runbooks/phase3-feature-decomposition.md`
- `/home/brett/projects/Agents/Omnigent-Install/examples/project-alfa-decomposition/decomposition-packet.example.yaml`
- `/home/brett/projects/Agents/Omnigent-Install/docs/hermes-job-status-schema.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/runbooks/hermes-api.md`
- `docs/feature-decomposition.md`
- `docs/pr-admission.md`
- `docs/merge-council.md`

The install repo source docs remain in place until a later migration feature
marks them as canonical links, legacy copies, or implementation runbooks.

## Trace Chain

```text
epic
  -> phase
    -> feature
      -> OpenSpec change
      -> Spec Kit feature artifacts
      -> implementation tasks
      -> bug mapping index
      -> branch
      -> local deterministic check report
      -> local branch review report
      -> pull request
      -> GitHub checks
      -> Hermes merge council decision
      -> merge commit
      -> archived OpenSpec change
```

## Suggested Repo Artifacts

Each managed repo should keep OpenSpec state in the standard OpenSpec location:

```text
openspec/
  specs/
  changes/
```

Factory coordination artifacts should live separately:

```text
.factory/
  epic.yaml
  phases.yaml
  features.yaml
  dependency-dag.yaml
  bug-mapping-index.yaml
  traceability.json
  admissions/
  reviews/
  merge-council/
```

## Feature Handoff Shape

Polly should receive a Hermes-approved feature contract before invoking Spec Kit.

```yaml
feature_id: OPW-0001
openspec_change: add-example-capability
approved_by: hermes
approval_id: hermes-admission-2026-06-21-001
target_repo: opensoft/example
scope:
  must:
    - Implement only the approved feature behavior.
  must_not:
    - Expand scope without a new Hermes approval.
acceptance_refs:
  - openspec/changes/add-example-capability/specs/example/spec.md
```

## Minimum Traceability Fields

```yaml
epic_id:
phase_id:
feature_id:
openspec_change:
speckit_feature:
branch:
implementation_model:
review_models:
local_checks:
branch_review:
pr:
merge_council_decision:
merge_council_report:
merge_commit:
archive_ref:
```

## Traceability Edge Contract

Traceability edges should be machine-readable and durable. At minimum, an edge
records:

```yaml
traceability_edge:
  from_type:
  from_id:
  relation:
  to_type:
  to_id:
  evidence:
    artifact_id:
    path:
```

Core relations:

| Relation | Meaning |
|---|---|
| `decomposes_to` | epic to phase, or phase to feature |
| `approves` | Hermes approval to decomposition, Spec Kit entry, PR admission, or merge decision |
| `produces` | job, worker, or agent produces an artifact |
| `implements` | branch, task, or PR implements a feature or acceptance criterion |
| `verifies` | test, review, or check verifies an acceptance criterion |
| `blocks` | finding or decision blocks progression |
| `must_precede` | one feature must merge or complete before another |
| `references` | artifact links to another artifact without ownership |

Required decomposition edges:

```text
epic -> phase
phase -> feature
feature -> feature dependency, when ordering exists
decomposition approval -> decomposition packet
approved feature -> Spec Kit entry
```

Required implementation and merge edges:

```text
feature -> Spec Kit spec/plan/tasks/analyze artifacts
Spec Kit tasks -> implementation branch
branch -> deterministic checks
branch -> branch review
branch review -> PR admission packet
PR admission approval -> GitHub PR
GitHub PR -> GitHub checks
GitHub PR -> Merge Council report
Merge Council report -> Merge Master decision
Merge Master decision -> GitHub review action
GitHub PR -> merge commit
OpenSpec change -> archived OpenSpec change
```

## Traceability Report

Every feature should have a traceability report that connects approved intent to implementation and merge evidence.

```markdown
# Feature Traceability Report

Feature: FEAT-014 Invoice Retrieval
OpenSpec Change: add-invoice-retrieval
Spec Kit Feature: 014-invoice-retrieval
Branch: feat/014-invoice-retrieval
PR: #238

## Source Intent

- Epic: EPIC-003 Billing Operations
- Phase: PHASE-002 Invoice Workflows
- OpenSpec change: openspec/changes/add-invoice-retrieval
- Hermes approval: HA-2026-06-21-014

## Spec Kit Artifacts

- spec.md
- plan.md
- tasks.md
- analysis report

## Acceptance Criteria Evidence

| AC | Spec Source | Implementation Evidence | Test Evidence | Status |
|---|---|---|---|---|
| FEAT-014.AC-01 | spec.md | invoice-service.ts | invoice-route.test.ts | Covered |
| FEAT-014.AC-02 | spec.md | invoice-route.ts | invoice-service.test.ts | Covered |
| FEAT-014.AC-03 | spec.md | Missing | Missing | Not Covered |

## Review Evidence

- Local deterministic checks: .factory/admissions/FEAT-014/checks.md
- Local branch review: .factory/reviews/FEAT-014/branch-review.md
- Merge council report: .factory/merge-council/FEAT-014/report.md

## Final State

Decision: NOT_READY
Next Action: return to Polly for targeted fixes
```

## Acceptance Criteria Evidence Rules

Acceptance criteria should be tracked individually. A feature is not traceable if it only has a general statement such as "tests added" or "implemented in service."

Each acceptance criterion should include:

- criterion ID
- source artifact
- implementation evidence
- test evidence
- reviewer evidence, when applicable
- status
- notes

Allowed statuses:

```text
covered
partially_covered
not_covered
not_applicable
deferred
```

Machine-readable example:

```yaml
acceptance_criteria_evidence:
  - id: FEAT-014.AC-01
    source: specs/invoices/spec.md
    implementation_evidence:
      - apps/api/invoices/invoice-service.ts
    test_evidence:
      - apps/api/invoices/invoice-route.test.ts
    status: covered
    notes: null

  - id: FEAT-014.AC-03
    source: specs/invoices/spec.md
    implementation_evidence: []
    test_evidence: []
    status: not_covered
    notes: "Cross-tenant denial missing."
```

## Bug-to-Feature Traceability

The traceability model must support user-reported bug routing.

Users usually report bugs by perceived feature, not by epic, PR, service, package, or file path. Hermes should maintain a bug mapping index so a report like "invoice retrieval is showing another company's invoice" maps cleanly to the owning feature, acceptance criterion, PR, tests, and merge council history.

Minimum bug mapping fields:

```yaml
bug_mapping:
  feature_id:
  user_reported_names:
  visible_surfaces:
  primary_failure_modes:
  owned_paths:
  acceptance_criteria:
  prs:
  merge_council_reports:
```

## Merge Council Artifact Location

Merge council reports should be stored under:

```text
.factory/merge-council/<feature-id>/
  report.md
  result.yaml
  reviewer-results/
    spec-traceability.yaml
    security.yaml
    tests.yaml
    architecture.yaml
    maintainability.yaml
    integration.yaml
```

The Markdown report is for human review. The YAML result is for dashboards, GitHub checks, and Hermes memory.
