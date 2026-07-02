## ADDED Requirements

### Requirement: Contract-pinned Hermes and Omnigent integration
Hermes and Omnigent install repos SHALL record the `openxFactory` contract
version they implement.

#### Scenario: Install repo validates contract compatibility
- **WHEN** an install repo validation runs
- **THEN** it MUST verify the referenced `openxFactory` commit and required
  contract files exist

#### Scenario: Local compatibility copy differs
- **WHEN** an install repo keeps a local schema or policy copy that differs from
  the canonical `openxFactory` contract
- **THEN** the install repo MUST declare an allowed adapter delta or fail
  validation

### Requirement: Hermes control-plane API
Hermes SHALL expose or provide runtime operations for live factory jobs, runs,
events, artifacts, approvals, and traceability.

#### Scenario: Worker reports progress
- **WHEN** an Omnigent worker emits a job event or artifact
- **THEN** Hermes MUST record it with stable job, run, feature, artifact, and
  traceability identifiers where applicable

#### Scenario: Approval request is created
- **WHEN** a worker reaches an approval gate
- **THEN** Hermes MUST record the approval request and expose it for approval,
  rejection, or escalation

### Requirement: Structured event bridge
Omnigent workers SHALL report meaningful runtime progress to Hermes through
structured events or compatible marker fallback.

#### Scenario: Hermes API environment is configured
- **WHEN** `HERMES_API_URL` and `HERMES_JOB_ID` are present
- **THEN** the worker-side event client MUST post events to Hermes

#### Scenario: Hermes API environment is absent
- **WHEN** a direct local test runs without Hermes API environment
- **THEN** the event client MUST safely no-op instead of failing the local test
