# merge-master-approval Specification Delta

## MODIFIED Requirements

### Requirement: Tier-2 ships inactive with report-only classification
Tier 2 checks SHALL ship inactive and classified report-only, and SHALL
activate only on a freshly accepted clearance record.

#### Scenario: Tier 2 runs report-only
- **WHEN** a tier 2 check runs
- **THEN** it MUST publish findings without failing the gate

#### Scenario: Tier 2 stays inactive without a ruling
- **WHEN** no activation ruling exists
- **THEN** the check MUST remain inactive

#### Scenario: Activation requires a freshly accepted record
- **WHEN** activation is requested
- **THEN** a freshly accepted clearance record MUST exist

#### Scenario: Active without a verdict still parks
- **WHEN** the check is active and no verdict exists
- **THEN** the run MUST park

#### Scenario: Active with exact-head unanimous-ready evidence clears
- **WHEN** exact-head unanimous-ready evidence exists
- **THEN** the run MUST clear

#### Scenario: Removing verdict visibility fails closed
- **WHEN** verdict visibility is removed
- **THEN** the run MUST fail closed
