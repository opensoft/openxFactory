# runtime-foundation Specification

## Purpose
Fixture canon for the presumption cases. It carries ONE requirement, so every
archived packet in this fixture that is examined reports its own requirement as
absent, and every packet that is exempt reports nothing at all.

## Requirements
### Requirement: Runtime identity
The runtime SHALL declare its own identity.

#### Scenario: The runtime names itself
- **WHEN** the runtime starts
- **THEN** it MUST declare its identity
