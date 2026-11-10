## ADDED Requirements

### Requirement: Headscale install custody

An approved install repository SHALL own Headscale packaging, instance deployment, and the install release. OpsxFactory SHALL own operator workflow and recovery authorization. Any repository creation, inventory admission, and aggregation admission SHALL follow their respective review processes.

#### Scenario: A candidate repository is proposed

- **WHEN** the Headscale install repository is proposed
- **THEN** T001 SHALL require the approved owner, verified repository, authorized scope, release path, and verification command before dispatch

### Requirement: Isolated install and recovery qualification

A managed installation SHALL verify isolated state and effective deny-by-default policy before enrollment. Recovery SHALL fence the prior instance and verify current revocations before restoring service.

#### Scenario: A backup predates a revocation

- **WHEN** an operator restores that backup
- **THEN** the instance SHALL remain quarantined until current revocations are reconciled
- **AND** the neighboring boundary SHALL retain service
