# live-runtime Specification Delta

## ADDED Requirements

### Requirement: Live factory pilot flow
The pilot SHALL run end to end.

#### Scenario: The pilot runs
- **WHEN** the pilot starts
- **THEN** it MUST complete

### Requirement: Approval gates
Approval SHALL gate the pilot.

#### Scenario: A gate holds
- **WHEN** approval is absent
- **THEN** the pilot MUST hold
