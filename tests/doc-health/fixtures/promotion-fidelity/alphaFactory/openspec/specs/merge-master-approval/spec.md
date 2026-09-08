# merge-master-approval Specification

## Purpose
Fixture canon reproducing the SHAPE of codexFactory's promoted
`merge-master-approval` spec as it stood before PR #85: the ratified
requirement title is present, four of its six ratified scenarios are not.

## Requirements
### Requirement: Tier-2 ships inactive with report-only classification
Tier 2 checks SHALL ship inactive and classified report-only.

#### Scenario: Tier 2 runs report-only
- **WHEN** a tier 2 check runs
- **THEN** it MUST publish findings without failing the gate

#### Scenario: Tier 2 stays inactive without a ruling
- **WHEN** no activation ruling exists
- **THEN** the check MUST remain inactive
