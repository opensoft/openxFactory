## MODIFIED Requirements

### Requirement: Canonical stage and merge policy
`openxFactory` SHALL own canonical domain-neutral stage, review, admission,
merge authority, escalation, and traceability policy. DomainxFactory repositories
SHALL own domain-specific execution mechanics that specialize those neutral
stages for their domain.

#### Scenario: Domain-neutral stage policy is migrated
- **WHEN** workflow stages such as approved intent, decomposition, execution, validation, review, admission, external enforcement, or archive are defined across DomainxFactories
- **THEN** their canonical neutral meaning, gate expectations, state transitions, and traceability requirements MUST live in `openxFactory`

#### Scenario: Engineering Spec Kit ownership is defined
- **WHEN** `/speckit.specify`, `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.analyze`, or `/speckit.implement` ownership is defined for software engineering work
- **THEN** the canonical engineering-domain ownership and consultation policy MUST live in `codexFactory`
- **AND** `openxFactory` MUST contain only the neutral execution-gate requirement or a pointer to the owning DomainxFactory policy

#### Scenario: Engineering PR admission is defined
- **WHEN** PR admission packet format, branch review mechanics, deterministic code checks, merge readiness packet format, or engineering merge sequencing rules are defined
- **THEN** the canonical software implementation policy MUST live in `codexFactory`
- **AND** `openxFactory` MUST own only the neutral admission, review, traceability, and external enforcement concepts

#### Scenario: Merge authority is cross-factory
- **WHEN** merge authority, merge risk, or human escalation rules apply across factory workflow governance rather than one domain implementation
- **THEN** the canonical policy MUST live in `openxFactory`
- **AND** domain-specific packet formats or review lanes MUST live in the owning DomainxFactory
