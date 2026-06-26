## ADDED Requirements

### Requirement: PR admission before GitHub PR
Omnigent SHALL NOT open a GitHub PR until Hermes approves PR admission.

#### Scenario: PR admission evidence is incomplete
- **WHEN** deterministic checks, branch review, traceability, line budget, or
  acceptance coverage evidence is missing or blocking
- **THEN** Hermes MUST block PR admission

#### Scenario: PR admission is approved
- **WHEN** Hermes records PR admission approval
- **THEN** Omnigent MAY open a GitHub PR and MUST attach PR metadata back to
  Hermes

### Requirement: Merge Council after GitHub evidence
Hermes SHALL convene Merge Council after a GitHub PR exists and relevant GitHub
checks or explicit not-configured evidence are available.

#### Scenario: Council finds blockers
- **WHEN** any required council lane returns a blocking finding
- **THEN** Hermes MUST mark merge readiness as not ready and return required
  fixes to Omnigent

#### Scenario: Council passes
- **WHEN** required council lanes pass or warn without blockers
- **THEN** Hermes MAY produce a ready or ready-with-warnings merge readiness
  report

### Requirement: Merge Master respects GitHub enforcement
Merge Master SHALL choose review actions without bypassing GitHub protection.

#### Scenario: PR is low risk and ready
- **WHEN** Merge Council is ready, checks pass, traceability is complete, and
  risk policy classifies the PR as low risk
- **THEN** Merge Master MAY approve in dry-run or through the configured bot/App
  identity when execution is explicitly enabled

#### Scenario: PR is medium or high risk
- **WHEN** risk policy classifies the PR as medium or high risk
- **THEN** Merge Master MUST request human or team review and MUST NOT submit an
  automated approval

#### Scenario: Merge is attempted
- **WHEN** a PR is ready for final merge
- **THEN** GitHub branch protection and merge queue MUST remain the final
  enforcement layer
