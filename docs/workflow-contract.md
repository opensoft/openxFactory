# Workflow Contract

This is the required factory workflow from approved epic through final merge.

## Required Workflow

1. Epic spec exists after constitution.
2. Hermes instructs Polly to do pre-Spec-Kit decomposition.
3. Polly decomposes epic into phases and small orthogonal features.
4. Polly creates traceability artifacts and a feature dependency DAG.
5. Only approved features proceed to `/speckit.specify`.
6. Sonnet implements small tasks and features by default.
7. Polly runs local deterministic checks.
8. Polly runs local pre-PR multi-model branch review.
9. Hermes approves whether the branch is allowed to open a PR.
10. Polly opens a PR only after local admission passes.
11. GitHub Actions and PR review systems run.
12. Hermes convenes merge council.
13. GitHub branch protection and merge queue enforce final merge rules.

## Handoff Rule

OpenSpec is used before Spec Kit.

```text
OpenSpec change approved by Hermes
  -> Polly accepts the feature
  -> Polly creates Spec Kit feature flow
  -> Sonnet implements tasks
  -> Polly checks and reviews branch
  -> Hermes admits branch to PR
  -> GitHub enforces final merge
```

## Non-Negotiable Gates

- No Spec Kit feature starts without Hermes-approved OpenSpec scope.
- No implementation branch opens a PR without local deterministic checks.
- No PR opens without local pre-PR branch review.
- No merge proceeds without Hermes merge council approval.
- No final merge bypasses GitHub branch protection.

## Model Assignment

- Sonnet is the default small-task implementation model.
- Opus, Codex, and non-Anthropic models are used for branch review and PR review.
- Review should prefer vendor diversity between the implementation model and the reviewing model.

## Initial Admission States

```text
proposed
approved-for-decomposition
decomposed
approved-for-speckit
speckit-ready
implementation-complete
local-checks-passed
branch-review-passed
approved-for-pr
pr-opened
merge-council-approved
merged
archived
```

