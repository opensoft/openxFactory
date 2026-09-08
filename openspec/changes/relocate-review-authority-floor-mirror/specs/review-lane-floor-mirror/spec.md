# review-lane-floor-mirror (delta)

## MODIFIED Requirements

### Requirement: The automated advance re-copies the vendored snapshot and recomputes its witnesses from the bytes it wrote

An automated pin advance MUST obtain the vendored floor snapshot by COPYING the authoritative document from the source repository at the new core commit, and MUST compute the snapshot's declared digest and entry count from the bytes it actually wrote.

The lane SHALL NOT hand-edit, patch, or partially update the snapshot, and SHALL NOT carry the digest or the entry count forward from any report, pull-request body or message produced by the source repository: a witness restated from the party being witnessed is not a witness. Where the copy cannot be obtained, the lane SHALL refuse and open nothing rather than advance the other sites without it. This requirement composes with, and does not restate, the requirement "The grace changes what the lanes report and nothing they witness", which fixes the snapshot's status as a byte witness.

**MODIFIED BY `relocate-review-authority-floor-mirror` (2026-09-08) IN WHAT "OBTAIN" MEANS, AND IN NOTHING ELSE.** The copy, the byte-witness rule, the prohibition on carrying a digest forward and the refusal are all untouched. What changes is that the lane SHALL resolve the authoritative document through an ORDERED LIST of declared candidate paths in the source repository rather than through a single path, trying them in order and taking the FIRST one obtained; and the refusal SHALL fire only when EVERY candidate fails, naming every path tried. THE LIST EXISTS FOR ONE PURPOSE AND SHALL BE BOUNDED BY IT: a GOVERNED RELOCATION of the document in the source repository, which cannot be atomic across two repositories. So the list SHALL name the relocation that opened it, SHALL be ordered with the path in force FIRST so that adding a successor changes no behaviour on the day it lands, SHALL be returned to a single entry once one advance has been observed against the successor, and SHALL NOT be used to give the lane a standing choice of homes. A firing that resolves any entry but the FIRST SHALL say so in its report, so that a migration in progress is visible in the run and not only in the diff. THE LANE SHALL NOT SEARCH: it SHALL NOT locate the document by kind, by basename, by code search or by any other discovery, because a discovered file is one an author elsewhere can plant, and an explicit list that fails closed is what makes the read surface reviewable. The list SHALL be declared in the lane's own sources and in the credential binding's read surface, and the lane SHALL NOT read it from the binding at run time: a value read from the artifact it is used to check makes the check a tautology, and the agreement between the declarations SHALL instead be asserted.

#### Scenario: The snapshot is copied, not edited
- **WHEN** the lane advances the pin
- **THEN** the vendored snapshot is a byte copy of the authoritative document at the new core commit
- **AND** no line of it is edited in place

#### Scenario: The witnesses are computed from what was written
- **WHEN** the lane declares the snapshot's digest and entry count
- **THEN** both are computed from the bytes the lane wrote to the snapshot file
- **AND** neither is taken from a message or report produced by the source repository

#### Scenario: A missing copy refuses the whole advance
- **WHEN** the authoritative document cannot be obtained at the new core commit from any declared candidate path
- **THEN** the lane refuses and opens no pull request
- **AND** the other sites are not advanced without it, and the refusal names every path it tried

#### Scenario: The first candidate resolves and nothing is different
- **WHEN** the document is obtained at the first declared candidate path
- **THEN** the advance proceeds exactly as it would with a single declared path
- **AND** the run reports no migration

#### Scenario: A later candidate resolves during a governed relocation
- **WHEN** the first declared candidate path does not resolve and a later one does
- **THEN** the advance proceeds from the document obtained there
- **AND** the run reports which candidate resolved and names the relocation the list declares

#### Scenario: The list is returned to one entry
- **WHEN** one advance has been observed against the successor path
- **THEN** the superseded entry is removed and the list carries one path again
- **AND** the lane has no standing choice of homes for the document

#### Scenario: The document is never discovered
- **WHEN** the document is absent from every declared candidate path but present elsewhere in the source repository
- **THEN** the lane refuses rather than finding it
- **AND** no search by kind, basename or code search is performed

#### Scenario: The declarations are asserted to agree
- **WHEN** the candidate list is declared in more than one place
- **THEN** a test asserts that every declaration carries the same ordered list
- **AND** no declaration is read at run time from the artifact a check compares it against
