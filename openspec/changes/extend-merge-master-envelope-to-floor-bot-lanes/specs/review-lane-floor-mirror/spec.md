# review-lane-floor-mirror — delta

## ADDED Requirements

### Requirement: Each floor bot lane's admission conditions are measured, not asserted
Each floor bot lane admitted to an autonomous approval envelope SHALL be admitted under conditions that were READ OFF ITS OBSERVED PULL REQUESTS — the exact author identity, the exact head reference, the base reference, the same-repository predicate, and the exact writable path set enumerated by name — and SHALL NOT be admitted under any condition the envelope cannot itself evaluate.

Where a lane's correctness rests on the SHAPE of its diff — additions only, machine-generated block only, pin values only — the enrolment SHALL rely on the lane's own required checks to prove that shape and SHALL record that it does so, rather than declaring a shape condition the envelope does not measure.

#### Scenario: Admission conditions taken from observed pull requests
- **WHEN** a floor bot lane is enrolled as a candidate class
- **THEN** its author, head reference and writable path set are the values its already-observed pull requests carried
- **AND** each writable path is named exactly rather than matched by a directory-wide pattern

#### Scenario: A shape guarantee the envelope cannot measure
- **WHEN** a lane's admission would depend on the diff being additions-only or confined to a machine-generated block
- **THEN** the enrolment requires every non-excluded check on the head to be green, so the lane's own judge of that shape is a condition of approval
- **AND** no shape condition is declared on the envelope itself

#### Scenario: The lane writes a path its class does not name
- **WHEN** a floor bot lane's pull request changes any path outside the enumerated writable set
- **THEN** the approval parks and the pull request waits for a human merge word

### Requirement: A re-pin is approved only against the source repository's default-branch head
An autonomous approval of a pull request advancing the pinned decision core SHALL be reachable only where the proposed core commit is the head of the source repository's default branch at the time the lane resolved it, so that a re-pin can never be approved ahead of the regeneration it consumes, and the lane SHALL refuse to pin at any reference supplied by its trigger payload.

#### Scenario: The re-pin follows the regeneration
- **WHEN** the re-pin lane runs
- **THEN** it resolves the source repository's default branch at run time and proposes that head and no other commit
- **AND** a commit named by the trigger payload, a tag, a branch or a pull-request head is refused

#### Scenario: The regeneration has not landed
- **WHEN** a floor regeneration has been opened in the source repository but has not landed on its default branch
- **THEN** the re-pin lane proposes the unchanged prior core and opens nothing, rather than pinning the unlanded commit

### Requirement: An autonomous approval of a floor bot lane records the facts it measured
Every autonomous approval or park of a floor bot lane's pull request SHALL be recorded on that pull request itself, carrying the candidate class it matched, the decision, the reason the deciding core produced, the changed path set it measured, the floor-matched count, and the check names the all-green condition quantified over — so that a reader of the pull request can reconstruct why it was approved without consulting any other artifact.

#### Scenario: An approval is recorded on the artifact
- **WHEN** a floor bot lane's pull request is autonomously approved
- **THEN** a comment on that pull request names the candidate class, the measured changed paths, the floor-matched count and the checks quantified over
- **AND** the record lives on the pull request rather than in a separate register a person must remember to write

#### Scenario: A park is recorded with the same facts
- **WHEN** such a pull request parks instead of being approved
- **THEN** the same record is written, naming the condition that failed
- **AND** the pull request waits for a human merge word
