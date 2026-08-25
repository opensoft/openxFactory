# ontology Specification Delta

## ADDED Requirements

### Requirement: Ontology scaffold
The scaffold SHALL be reproducible.

#### Scenario: The scaffold is rebuilt
- **WHEN** the scaffold is rebuilt
- **THEN** the output MUST be byte-identical

#### Scenario: The initial scaffold is drafted before any package exists
- **WHEN** no package exists yet
- **THEN** the scaffold MUST still be draftable
