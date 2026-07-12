# document-lifecycle Delta: Possible Feats Declaration

## ADDED Requirements

### Requirement: Possible feats declaration
A brainstorm document that enumerates candidate feats SHALL declare them in
a `Possible feats:` section, seeded by the author at capture, so unpicked
possibles are durable backlog rather than evaporating prose. Each declared
possible carries a register state — `latent`, `picked`, `rejected`, or
`superseded` — governed by the `ideation-cross-reference` register
contract; the canonical consolidated register is the cross-reference index,
and no third standalone register file exists. Legacy documents without the
section are valid and MUST NOT have possibles fabricated for them; only the
designated worked examples are backfilled as renderer fixtures.

#### Scenario: A new brainstorm is captured
- **WHEN** an author captures a brainstorm that names things the topic could become
- **THEN** those candidates are seeded in a `Possible feats:` section at capture

#### Scenario: A possible is picked at the organize gate
- **WHEN** staging picks a declared possible
- **THEN** its state becomes `picked` citing the staged topic's staging ID
- **AND** the citation inherits the change ID when the topic crosses the proposal gate

#### Scenario: A legacy document has no section
- **WHEN** a document written before this requirement carries no `Possible feats:` section
- **THEN** lifecycle validation MUST NOT report it and no history is fabricated
