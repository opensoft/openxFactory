# doc-health

## ADDED Requirements

### Requirement: The deterministic pass reads a document's lifecycle header by real lines
The deterministic pass SHALL locate a governed document's lifecycle header by counting the document's REAL lines — the three line endings CR, LF and CRLF — and MUST NOT count any other character as a line separator. The bounded header window is therefore a number of lines of the document rather than a number of fragments a wider splitting rule produced from it.

This SHALL hold for every reader of that header, so that the status a document carries and the status the pass reports are the same fact. A reader that splits more aggressively than the writer can fail to find a header the writer just wrote correctly, and then reports a document as lacking a status it plainly has — a FALSE finding, which costs more trust than a crash because it accuses a correct document and leaves the operator no recourse but to disbelieve the checker.

The line rule SHALL be shared with the writers of the same header rather than reimplemented per reader. Where the corpus cannot share an implementation across language boundaries, the divergence SHALL be held by an explicit agreement test rather than by convention.

#### Scenario: A header carrying an exotic separator is read
- **WHEN** the deterministic pass reads a governed document whose header region contains characters a wider splitting rule would treat as line breaks
- **THEN** the document's lifecycle status MUST be found if it is present within the header window counted in real lines
- **AND** the pass MUST NOT report the document as lacking a status it carries

#### Scenario: The header window is counted
- **WHEN** the deterministic pass applies its bounded header window to a document
- **THEN** the bound MUST count real lines of the document

#### Scenario: The reader and the writer are compared
- **WHEN** a lifecycle header is written by a governed action and then read by the deterministic pass
- **THEN** both MUST agree on where the document's lines begin and end

#### Scenario: The corpus is unchanged by the correction
- **WHEN** the deterministic pass runs over the governance corpus after this correction
- **THEN** its findings MUST be identical to the run before it
- **AND** any finding that does move MUST be explained rather than accepted, because a moved finding means a corpus document carries a separator the prior measurement did not see
