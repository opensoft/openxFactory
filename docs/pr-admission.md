# PR Admission

PR admission is the Hermes-controlled gate between an Omnigent implementation
branch and a GitHub pull request. Omnigent prepares the evidence. Hermes
decides whether the PR may be opened.

## Source Provenance

Reviewed sources:

- `/home/brett/projects/Agents/Omnigent-Install/docs/runbooks/phase6-pr-admission.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/omnigent-implementation-plan.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/runbooks/live-pilot-plan.md`
- `docs/omnigent-constitution.md`
- `docs/merge-council.md`
- `docs/roles-and-authority.md`

The install repo source docs remain in place until a later migration feature
marks them as canonical links, legacy copies, or implementation runbooks.

## Boundary

PR admission happens before a GitHub PR exists. Merge Council happens after a
GitHub PR exists.

```text
Spec Kit implementation complete
  -> deterministic local checks
  -> local branch review
  -> branch admission packet
  -> Hermes PR admission decision
  -> GitHub PR may open only if approved
```

Omnigent must stop after generating the PR admission packet. It must not open a
GitHub PR until Hermes records an approval for PR admission.

## Responsibilities

```text
Omnigent / Polly
  -> records branch and commit evidence
  -> runs deterministic checks
  -> runs local branch review
  -> creates PR admission packet
  -> requests Hermes PR admission
  -> opens GitHub PR only after approval

Hermes
  -> validates the admission packet
  -> applies policy, risk, and traceability rules
  -> approves, blocks, or requests fixes
  -> records the admission decision

GitHub
  -> is not entered until PR admission passes
```

## Required Branch Admission Inputs

The PR admission packet must include:

- feature id and title;
- source OpenSpec change or approved feature record;
- Spec Kit artifact references;
- candidate branch name;
- base branch;
- commit SHA;
- changed files;
- changed line count;
- line budget result;
- deterministic local check results;
- local branch review findings;
- acceptance criteria coverage;
- traceability edges;
- risk notes;
- requested GitHub PR title/body draft;
- approval request id.

## Branch Review Lanes

Local branch review should use the same core lanes as Merge Council, but it is
pre-PR and may use local evidence only.

| Lane | Blocks PR Admission On |
|---|---|
| Spec Traceability | missing approved scope, missing Spec Kit artifacts, unrelated changes, acceptance criteria without evidence |
| Security | auth, tenant isolation, secrets, data exposure, unsafe dependencies, unreviewed security risk |
| Tests | failing checks, missing acceptance evidence, weak regression coverage |
| Architecture | boundary violations, incompatible contracts, hidden coupling, implementation drift |
| Maintainability | excessive complexity, unreviewable size, generated bloat, unclear ownership |
| Integration | dependency DAG violations, unsafe merge order, unresolved branch conflicts |

Blocking findings prevent PR admission. Warnings may be carried forward as PR
notes or Merge Council inputs.

## Admission Decisions

Allowed decisions:

```text
APPROVED
BLOCKED
NEEDS_FIXES
DEFER
```

Decision rules:

- `APPROVED`: required evidence exists, local checks pass or are explicitly
  waived, branch review has no blockers, traceability is complete, and line
  budget is within policy.
- `BLOCKED`: policy forbids the PR path, security risk is unacceptable, or
  evidence is contradictory.
- `NEEDS_FIXES`: targeted fixes are required before PR creation.
- `DEFER`: decision cannot be made because required inputs or external state
  are missing.

## PR Admission Packet Shape

```yaml
pr_admission_packet:
  schema_version: 1
  feature_id: FEAT-014
  feature_title: Invoice Retrieval
  repository: opensoft/project-alfa
  branch:
    name: feat/014-invoice-retrieval
    base: main
    commit: abc123
  line_budget:
    max_changed_lines: 10000
    changed_lines: 842
    result: pass
  artifacts:
    openspec_change: changes/invoice-retrieval
    speckit_spec: specs/014-invoice-retrieval/spec.md
    speckit_plan: specs/014-invoice-retrieval/plan.md
    speckit_tasks: specs/014-invoice-retrieval/tasks.md
  checks:
    deterministic: pass
    tests: pass
    lint: pass
  branch_review:
    decision: pass
    blocking_findings: []
    warnings: []
  acceptance_criteria:
    - id: FEAT-014.AC-01
      covered: true
      evidence:
        - invoice-route.test.ts
  approval_request_id: APR-FEAT-014-PR-ADMISSION-001
```

## Stop Conditions

PR admission must stop when:

- approved scope is missing;
- Spec Kit artifacts are missing or outside scope;
- deterministic checks fail without an approved waiver;
- local branch review has blocking findings;
- changed lines exceed the line budget without explicit approval;
- branch evidence is incomplete;
- Omnigent attempts to open a PR before approval;
- credentials, generated state, local workspaces, or runtime secrets would be
  included in the PR.

## Traceability

Hermes must record traceability edges from:

```text
OpenSpec change or approved feature
  -> Spec Kit artifacts
  -> implementation tasks
  -> candidate branch and commit
  -> branch review findings
  -> PR admission packet
  -> Hermes PR admission decision
  -> GitHub PR, after opened
```

The PR admission packet becomes a required Merge Council input after the PR
exists.
