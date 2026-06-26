## ADDED Requirements

### Requirement: Worker lane preflight
Each Omnigent worker lane SHALL pass preflight checks before receiving live
factory jobs.

#### Scenario: Worker registers with Hermes
- **WHEN** a worker lane registers
- **THEN** it MUST report role, capacity, auth mode, capabilities, and health
  sufficient for Hermes routing decisions

#### Scenario: Worker auth is invalid
- **WHEN** required Claude, Codex, GitHub, Spec Kit, or Omnigent auth/tooling is
  missing for the assigned job
- **THEN** the worker MUST fail preflight and refuse the job

### Requirement: Subscription auth profile safety
Coder workers SHALL use subscription auth profiles by default and MUST NOT fall
back to provider API keys unless explicitly approved.

#### Scenario: Subscription worker starts
- **WHEN** a coder worker starts under subscription auth
- **THEN** provider API key environment variables that would switch billing
  modes MUST be empty, unset, or explicitly approved

#### Scenario: Runtime home is materialized
- **WHEN** auth profiles are copied into worker containers
- **THEN** each container MUST receive its own writable runtime home instead of
  sharing one writable provider profile

### Requirement: CloudPC worker packaging
The worker runtime SHALL provide a repeatable CloudPC worker pack before scale
out.

#### Scenario: CloudPC is rebuilt
- **WHEN** a new CloudPC worker is rebuilt from docs
- **THEN** it MUST be able to restore allowed auth profiles, start worker
  containers, register with Hermes, and report capacity without committed
  secrets
