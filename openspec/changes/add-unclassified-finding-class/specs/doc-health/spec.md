# doc-health Specification Delta

## ADDED Requirements

### Requirement: A modified-block-currency finding its own class map cannot place is itself a finding
The modified-block-currency family SHALL emit ONE ADDITIONAL `warning` finding
per run for each DISTINCT SHAPE of rule text its own class map does not place,
naming how many of that run's findings carry that shape and, verbatim, the rule
text of the first of them in the family's own report order, and carrying that
first finding's repository and delta path. Where the map places every finding
the family emits, no such finding SHALL be emitted.

Two unplaced findings SHALL be treated as ONE SHAPE where their rule texts are
equal after every single-quoted span, every double-quoted span and every run of
digits has been replaced by a fixed placeholder.

The finding's action line SHALL name both remedies and where the first is
applied: "extend the class map in `scripts/doc_health/modified_block_currency.py`,
or fix the drifted rule text the finding names".

The finding SHALL itself be placed by the class map, in a FIFTH class of the
family's own registry carrying the `warning` band and that action line, so that
it is never counted by the residual it reports.

The pattern that places that class SHALL be anchored at the start of the rule
text, this finding carrying a quoted rule text that may itself begin in the shape
of an arm's.

The family's residual row SHALL continue to render whenever its count is
nonzero.

The family SHALL remain absent from `FAMILY_RESOLUTION`, so that a finding
designed to stop being emitted as soon as the map is extended is never classified
`contested` and its disappearance is never reported as an uncited resolution.

This requirement adds no deterministic check family: the finding is emitted by
the modified-block-currency family under its own id, and the enumeration and its
numerals in the "Deterministic check families" requirement are untouched and
unrestated.

#### Scenario: Every finding the family emits is placed by its map
- **WHEN** a run of the modified-block-currency family emits findings and the class map places every one of them
- **THEN** no additional finding MUST be emitted, the map and the arms agreeing being the state this requirement exists to leave alone
- **AND** the family's rendered class counts MUST still sum to the rows the report prints for it

#### Scenario: A rule text the class map does not place
- **WHEN** a run of the modified-block-currency family emits one or more findings whose rule text no pattern of its class map matches
- **THEN** the run MUST emit exactly one additional `warning` finding for each distinct shape among them, naming the number of that run's findings carrying that shape and, verbatim, the rule text of the first of them in the family's own report order
- **AND** each such finding MUST carry the repository and delta path of that first finding, and the action line this requirement states
- **AND** each such finding MUST itself be placed by the map into the fifth class, so that it is never counted by the residual it reports and the rendered counts still sum to the rows

#### Scenario: Two unplaced findings differ only in a title and a count
- **WHEN** two unplaced findings have rule texts that are equal after every quoted span and every run of digits is replaced by a fixed placeholder
- **THEN** ONE additional finding MUST be emitted for both, naming the count two, one drifted rule shape being one remedy
- **AND** two unplaced findings whose rule texts differ outside their quoted spans and digit runs MUST yield two additional findings, being two remedies

#### Scenario: The quoted rule text begins in the shape of an arm
- **WHEN** an unplaced rule text itself begins with the phrase an arm's rule texts begin with, and this finding quotes it
- **THEN** this finding MUST be placed in the fifth class and MUST NOT be placed under the class its quotation resembles
- **AND** the unplaced finding it names MUST still be counted by the residual row, the two being counted apart

#### Scenario: The warning is worked from the ranked plan
- **WHEN** a report is rendered for a run that emitted the additional finding
- **THEN** the finding MUST appear in the ranked plan as a ready-to-stage work item stating its severity, repository, path and action, on the same terms as every other finding
- **AND** the family's residual row MUST still render in the family's own report block, the row and the finding being two readings of one fact rather than alternatives

#### Scenario: The class map grows the pattern the drift named
- **WHEN** the class map is extended with a pattern that places the rule text the finding named, and the family is run again over the same tree
- **THEN** the additional finding MUST NOT be emitted, and the residual row MUST NOT render
- **AND** the disappearance MUST NOT be reported as an uncited resolution, the family being deliberately absent from `FAMILY_RESOLUTION` and its findings therefore never classified `contested`
