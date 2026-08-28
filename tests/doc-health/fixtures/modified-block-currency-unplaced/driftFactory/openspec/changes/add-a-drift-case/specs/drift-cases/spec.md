# drift-cases Specification Delta

## MODIFIED Requirements

### Requirement: Zeta boundary is declared
The zeta reader SHALL resolve its boundary before it answers. The zeta reader
SHALL refuse a boundary it cannot resolve.

#### Scenario: A zeta boundary resolves
- **WHEN** the zeta reader opens its boundary
- **THEN** it MUST answer with the boundary it resolved

#### Scenario: A zeta boundary cannot be resolved
- **WHEN** the zeta reader finds no boundary to open
- **THEN** it MUST refuse to answer
