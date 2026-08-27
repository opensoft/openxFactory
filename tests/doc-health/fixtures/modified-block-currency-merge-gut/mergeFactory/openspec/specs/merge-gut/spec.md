# merge-gut Specification

## Purpose
SYNTHESIZED. Two requirements: a merge that guts its source, and the same
merge declaring the bullets it made redundant.

## Requirements

### Requirement: A merge that guts its source
The merge rule holds for this requirement.

#### Scenario: The old shape
- **WHEN** the old shape runs
- **THEN** it MUST do the first thing
- **AND** it MUST do the second thing
- **AND** it MUST do the third thing

#### Scenario: A scenario that survives untouched
- **WHEN** the surviving case runs
- **THEN** it MUST survive

### Requirement: A merge that declares its redundant bullets
The merge rule holds for this requirement too.

#### Scenario: The declared old shape
- **WHEN** the declared old shape runs
- **THEN** it MUST do the first declared thing
- **AND** it MUST do the second declared thing, citing `openxFactory` by name
- **AND** it MUST do the third declared thing

#### Scenario: Another scenario that survives untouched
- **WHEN** the other surviving case runs
- **THEN** it MUST survive too
