Status: ratified
Ratified by: user approval of `add-hermes-customer-subject-runtime-contract` on 2026-07-12

## ADDED Requirements

### Requirement: Scoped v2 Hermes job lifecycle records
The canonical v2 Hermes job envelope, run, and event schemas SHALL require the same neutral scope tuple containing `installation_id`, `stack_id`, and `layer_id`. V2 required fields and enumerations MUST NOT encode Project, repository, feature, patient, company, or any other single domain's vocabulary. Domain overlays MAY re-tighten the neutral v2 core, while existing v1 schemas remain available during the compatibility bridge.

#### Scenario: Customer-subject job is issued
- **WHEN** a domain issues a v2 job for a customer subject
- **THEN** the envelope MUST identify the exact owning installation, stack, and layer
- **AND** no `project`, repository, feature, patient, or company field MUST be required by the neutral schema

#### Scenario: Run and event correlate to a job
- **WHEN** a run or event records lifecycle state for a v2 job
- **THEN** its scope MUST exactly match the referenced job and run scope

#### Scenario: Cross-layer operation is requested
- **WHEN** a job requests an operation involving another layer
- **THEN** the job MUST retain its owning scope
- **AND** the cross-layer resource reference MUST identify the exact source and target resources and binding required for transactional operation authorization by the customer-subject runtime contract

#### Scenario: Engineering overlay requires Project data
- **WHEN** codexFactory specializes the v2 envelope for an engineering workflow
- **THEN** its domain overlay MAY require project, repository, or feature references
- **AND** those nouns MUST NOT become required neutral v2 fields

#### Scenario: Existing v1 consumer remains pinned
- **WHEN** an existing adapter remains pinned to the published v1 schema path
- **THEN** the additive v2 bundle MUST NOT retroactively invalidate its v1 records
