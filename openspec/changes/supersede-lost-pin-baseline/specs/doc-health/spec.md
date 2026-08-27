# doc-health Specification Delta

## ADDED Requirements

### Requirement: A declared unrecoverable pin loss is discharged by a superseding record, never by deleting its declaration
A declared loss of a pinned commit SHALL stay declared and reported for as long
as the pin stands committed, and the verification SHALL treat that loss as
answered ONLY where a superseding record naming it is committed and readable —
never on the strength of the declaration having been removed.

WHY THIS NEEDS SAYING AT ALL, and why in this capability. The obligation to
issue a superseding record where a pinned object is unrecoverable is stated
where the pin obligation lives, and nothing here restates or moves it. What that
obligation does not say is what the VERIFICATION does afterwards, and the
verification is this capability's. Between the two there was exactly one route
from "this class carries a permanently lost pin" to "this class is fully
verified", and it ran through deleting the declaration. That route is a
silencing: it discards the measurement that established the loss, it makes the
next reader unable to tell a repository that never had the defect from one that
erased it, and it converts the one condition in this class that no code change
can repair into background noise. The route this requirement states instead is
that the governance act lands, the declaration CITES it, and the verification
goes and reads it.

THE LOSS IS NEVER SILENCED BY ITS DISCHARGE, and the two halves are separate
questions. "Is this pin reachable?" is answered LOST for ever: the object is
gone, no ref reaches it, and every run says so with the measurement that
established it. "Has the class been left with an unanswered obligation?" is
answered by whether the superseding record exists. A discharged loss therefore
still reports as a declared unrecoverable loss, still carries its measurement,
and is still re-measured — because the day such an object turns out to be
recoverable, retention becomes the route and the declaration is stale.

THE CITATION IS READ, NOT BELIEVED. A declaration naming a superseding record
SHALL be satisfied only by committed state at the revision under test: the
record present at the path the declaration names, and naming the pin it claims
to supersede. A citation of a record nobody committed, a record deleted after
the fact, or a stub that never mentions the lost object is a dangling citation,
and a dangling citation is worse than a blank one because it reads as
discharged.

THE DISPOSITION IS RECORDED WHERE THE REPORT IS PRODUCED. The standing report of
an unrecoverable loss is not a deterministic check-family finding and MUST NOT be
disposed as one: this verification registers no check family, emits no family
finding, and therefore offers no (family, repo, path) tuple for a finding
disposition to match. Its disposition SHALL be carried by the loss declaration
itself, citing the superseding record — the same place the measurement and the
outstanding act are already carried, so a reader who can see the report can see
its disposition without a second lookup that could drift from it.

THIS ADDS NO DETERMINISTIC CHECK FAMILY, and the enumeration and its numerals in
the "Deterministic check families" requirement are deliberately untouched and
unrestated. The verification this governs adds none, for the reasons that
verification's own requirement states; a discharge mechanism inside it adds none
either, and a `MODIFIED` block over a requirement every new family must restate
in full is exactly the hazard this capability now carries a family to police.

#### Scenario: The superseding record has not landed
- **WHEN** a pin declared unrecoverable stands committed and no superseding record for it is committed
- **THEN** the verification MUST NOT report the class as fully verified, and MUST report the loss with the measurement that established it and the governance act still owed
- **AND** the run MUST NOT fail on that loss alone, because no code change repairs it and reddening every unrelated change on a standing governance obligation is enforcement arriving by the back door

#### Scenario: The superseding record lands
- **WHEN** a superseding record naming that pin is committed at the path the declaration cites
- **THEN** the verification MUST report the class as fully verified again if nothing else is outstanding, because the obligation that held it open has been met
- **AND** the loss MUST still be reported as a declared unrecoverable loss, with its measurement, in every run

#### Scenario: The declaration cites a record the repository does not carry
- **WHEN** a declaration names a superseding record that is not committed at the revision under test, or names one that does not mention the pin it claims to supersede
- **THEN** the loss MUST be treated as still awaiting its record, exactly as if nothing were cited
- **AND** the citation MUST NOT be accepted on the strength of being written, because a discharge nobody can read is not a discharge

#### Scenario: The declaration is deleted instead of discharged
- **WHEN** a change removes the declaration of an unrecoverable loss while the pin it describes still stands committed
- **THEN** the pin MUST be reported as an orphaned pin — a repairable defect that fails the run — rather than passing silently, so deletion cannot be used to obtain a clean report
- **AND** the measurement the declaration carried MUST NOT be treated as superseded by its own removal
