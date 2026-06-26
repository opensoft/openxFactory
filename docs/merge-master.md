# Merge Master

The Merge Master is a Hermes governance agent that converts Merge Council
readiness into the next GitHub review action. It does not bypass GitHub branch
protection, merge queues, status checks, CODEOWNERS, or required reviews.

## Source Provenance

Reviewed sources:

- `/home/brett/projects/Agents/Omnigent-Install/docs/runbooks/merge-master-implementation-plan.md`
- `/home/brett/projects/Agents/Omnigent-Install/policies/merge-risk-policy.yaml`
- `/home/brett/projects/Agents/Omnigent-Install/docs/hermes-governance-agents.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/runbooks/hermes-profiles-groups-implementation-plan.md`
- `docs/roles-and-authority.md`
- `docs/merge-council.md`
- `docs/pr-admission.md`

The install repo source docs remain in place until a later migration feature
marks them as canonical links, legacy copies, or implementation runbooks.

## Target Flow

```text
Omnigent implementation branch
  -> deterministic checks
  -> local branch review
  -> Hermes PR admission
  -> GitHub PR
  -> GitHub checks and review systems
  -> Hermes Merge Council
  -> Hermes Merge Master
      -> approve low risk
      -> request human review for medium/high risk
      -> block incomplete or contradictory evidence
  -> GitHub branch protection
  -> merge queue / merge
```

## Non-Negotiable Boundaries

- Merge Master must not bypass branch protection.
- Merge Master must not push code.
- Merge Master must not merge directly in v1.
- Omnigent must not approve its own merge path.
- Production Merge Master must use a dedicated GitHub App or bot identity, not
  a personal human token.
- GitHub remains the hard enforcement layer.

## Required Inputs

Hermes inputs:

- job envelope;
- traceability edges;
- PR admission packet;
- deterministic check artifacts;
- branch review artifacts;
- approval requests and approvals;
- Merge Council results;
- merge readiness report.

GitHub inputs:

- PR metadata;
- changed files and line count;
- status checks;
- review decision;
- existing reviewers;
- branch protection summary.

Policy inputs:

- merge risk policy;
- allowed auto-approval rules;
- human/team reviewer routing rules;
- blocked path rules.

## Decision Algorithm

```text
1. Load Hermes job or feature context.
2. Load linked GitHub PR artifact or PR number.
3. Verify required Hermes artifacts are present.
4. Verify PR admission is approved.
5. Verify Merge Council is ready.
6. Load GitHub PR state.
7. Classify risk using policy, changed files, and council results.
8. If evidence is missing or contradictory, decision = block.
9. If risk is low and checks pass, decision = approve.
10. If risk is medium or high, decision = request_human_review.
11. Write Merge Master decision artifact.
12. Execute GitHub action only if enabled.
13. Record GitHub action result back to Hermes.
```

## Risk Policy

Default changed-line budget:

```yaml
line_budget:
  default_max_changed_lines: 10000
```

Low risk if all are true:

- changed lines are under budget;
- no production behavior path is touched;
- no auth, security, tenant, data, payment, secret, or infrastructure path is
  touched;
- no destructive migration or data operation is present;
- GitHub checks pass or are explicitly waived by policy;
- Merge Council has no blocking lane;
- traceability is complete.

Medium risk if any are true:

- user-visible behavior changes;
- integration boundary changes;
- dependency upgrades with moderate blast radius;
- database migrations without data loss risk;
- non-blocking warnings remain and policy allows human review.

High risk if any are true:

- auth, authorization, tenant isolation, payments, secrets, infrastructure,
  data deletion, destructive migration, branch protection exception, or
  over-budget unreviewable refactor.

## Decisions And GitHub Actions

| Decision | Allowed Risk | GitHub Action |
|---|---|---|
| `approve` | low | Submit approving GitHub PR review when execution is enabled |
| `request_human_review` | medium, high | Request configured reviewers or teams and comment with rationale |
| `block` | low, medium, high | Comment with blockers and do not approve |

Human review is required for medium/high risk. The intent is not to make humans
review everything. The intent is for Hermes to act as a real review authority
for low-risk work and route risky reviews to the right people or teams.

## Decision Artifact Shape

```yaml
merge_master_decision:
  schema_version: 1
  decision_id: MMD-FEAT-014-001
  repository: opensoft/project-alfa
  pr_number: 238
  feature_id: FEAT-014
  risk: low
  decision: approve
  github_action: submit_approving_review
  rationale:
    - council_ready
    - checks_passed
    - traceability_complete
    - under_line_budget
    - documentation_only
  evidence:
    pr_admission: APR-FEAT-014-PR-ADMISSION-001
    merge_readiness_report: HMC-FEAT-014-001
    github_pr_state: ART-FEAT-014-GITHUB-PR-STATE
```

## Human Review Routing

Medium/high-risk PRs route through Hermes groups:

| Risk | Route |
|---|---|
| Architecture or contract risk | `opensoft/hermes-architecture` |
| Security, auth, tenant, or secret risk | `opensoft/hermes-security` |
| General product or delivery risk | `opensoft/hermes-governance` |
| Repo execution risk | `opensoft/omnigent-engineering` plus the owning Hermes group |

The Human Review Router may request GitHub team reviewers when mapped teams
exist and have repository access. If the GitHub team is not available yet,
Hermes still records the intended route and blocks automated approval.

## Acceptance Criteria

- Low-risk PRs may receive Merge Master approval only after PR admission,
  GitHub checks, and Merge Council readiness pass.
- Medium/high-risk PRs request human review and do not receive bot approval.
- Missing evidence blocks.
- Blocking council lanes block.
- Every Merge Master decision is stored as a Hermes artifact.
- GitHub branch protection remains final.
