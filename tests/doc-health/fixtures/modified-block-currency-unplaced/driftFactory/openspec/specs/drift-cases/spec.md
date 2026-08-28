# drift-cases Specification

## Purpose
SYNTHESIZED. Three requirements with PLAIN titles, written so that the family's
arms fire and its class map places every finding they emit. The tree exercises
the FIFTH class only under an induced drift — one entry removed from
`_CLASS_PATTERNS` — because no corpus-supplied title can produce an unplaced
rule text while the map is complete.

## Requirements

### Requirement: Alpha boundary is declared
The alpha reader SHALL resolve its boundary before it answers. The alpha reader
SHALL record which boundary it resolved. The alpha reader SHALL refuse a
boundary it cannot resolve.

#### Scenario: An alpha boundary resolves
- **WHEN** the alpha reader opens its boundary
- **THEN** it MUST answer with the boundary it resolved

#### Scenario: An alpha boundary cannot be resolved
- **WHEN** the alpha reader finds no boundary to open
- **THEN** it MUST refuse to answer

### Requirement: Beta boundary is declared
The beta reader SHALL resolve its boundary before it answers. The beta reader
SHALL record which boundary it resolved. The beta reader SHALL refuse a
boundary it cannot resolve.

#### Scenario: A beta boundary resolves
- **WHEN** the beta reader opens its boundary
- **THEN** it MUST answer with the boundary it resolved

#### Scenario: A beta boundary cannot be resolved
- **WHEN** the beta reader finds no boundary to open
- **THEN** it MUST refuse to answer

### Requirement: Gamma boundary is declared
The gamma reader SHALL resolve its boundary before it answers. The gamma reader
SHALL record which boundary it resolved.

#### Scenario: A gamma boundary resolves
- **WHEN** the gamma reader opens its boundary
- **THEN** it MUST answer with the boundary it resolved

#### Scenario: A gamma boundary cannot be resolved
- **WHEN** the gamma reader finds no boundary to open
- **THEN** it MUST refuse to answer
