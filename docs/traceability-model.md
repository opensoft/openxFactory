# Traceability Model

The factory must document traceability from epic to merge.

## Trace Chain

```text
epic
  -> phase
    -> feature
      -> OpenSpec change
      -> Spec Kit feature artifacts
      -> implementation tasks
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
  traceability.json
  admissions/
  reviews/
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
merge_commit:
archive_ref:
```

