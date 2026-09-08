# ontology Specification Delta

## MODIFIED Requirements

### Requirement: Ontology scaffold
The ontology SHALL carry a scaffold, and the scaffold SHALL be versioned.

#### Scenario: A scaffold is present
- **WHEN** the ontology loads
- **THEN** a scaffold MUST be present

#### Scenario: A scaffold carries a version
- **WHEN** the ontology loads
- **THEN** the scaffold MUST carry a version
