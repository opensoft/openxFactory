# ontology Specification

## Purpose
Fixture canon for the two supersession negatives: a requirement rewritten by
a later archived change, and a requirement renamed by a later archived change.

## Requirements
### Requirement: Ontology scaffold
The scaffold SHALL be reproducible.

#### Scenario: The scaffold is rebuilt
- **WHEN** the scaffold is rebuilt
- **THEN** the output MUST be byte-identical

### Requirement: doxBench scoped view
The surface SHALL scope its view.

#### Scenario: A scope is chosen
- **WHEN** a scope is chosen
- **THEN** the view MUST follow it
