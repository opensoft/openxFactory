# merge-master-approval Specification Delta

## MODIFIED Requirements

### Requirement: Tier-2 ships inactive with report-only classification
Tier-2 SHALL ship inactive.

#### Scenario: Activation requires a freshly accepted record
- **WHEN** activation is attempted
- **THEN** a freshly accepted record MUST exist

#### Scenario: Active without a verdict still parks
- **WHEN** no verdict is present
- **THEN** the run MUST park
