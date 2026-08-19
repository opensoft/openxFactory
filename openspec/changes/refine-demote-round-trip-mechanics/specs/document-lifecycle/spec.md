# document-lifecycle

## ADDED Requirements

### Requirement: The proposal gate records its authorship once per document, not once per attempt
When the promotion gate moves staged material into a change's supporting documents it records which change proposed that material on the document itself. That record SHALL be UPDATED where one already exists rather than added beside it, so a document that makes the round trip more than once carries exactly one such line naming the most recent attempt.

A document may legitimately reach proposal, be demoted, be worked, and reach proposal again — the round-trip guarantee exists precisely so that lap is normal. Appending a fresh authorship line each time turns a normal lap into visible cruft, and worse, into an ambiguous record: several lines each claiming to name the proposing change say nothing about which one is current.

The obligation sits on the gate that WRITES the line. The reverse transition MUST NOT be made to remove or rewrite it, because the reverse transition's own refresh is bounded to the round-trip provenance slots and the marked proposal-element sections and MUST leave every other byte of a live fragment unchanged; widening that boundary to tidy a header would trade a data-loss guarantee for neatness.

#### Scenario: A document reaches proposal for the second time
- **WHEN** staged material that already carries a proposing-change record is moved into a change's supporting documents
- **THEN** the existing record MUST be updated to name the current change
- **AND** the document MUST carry exactly one such record

#### Scenario: A document reaches proposal for the first time
- **WHEN** staged material carrying no proposing-change record is moved into a change's supporting documents
- **THEN** the record MUST be added

#### Scenario: The reverse transition returns a document carrying the record
- **WHEN** the reverse transition returns a document that carries a proposing-change record
- **THEN** it MUST NOT remove or rewrite that record
- **AND** the bounded-refresh guarantee over a live fragment MUST remain intact
