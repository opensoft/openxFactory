## ADDED Requirements

### Requirement: A convening carries one resolved required-seat roster
Before a per-candidate council is admitted, the trusted domain producer SHALL
resolve every required seat from the governed candidate-class rules and the
candidate facts for the exact candidate revision being reviewed, and SHALL
submit that result as `council_convening.required_seats`. The roster MUST include
every standing seat and each conditional seat whose class-defined pull-in
condition holds, MUST exclude a conditional seat whose condition does not hold,
and MUST NOT be resolved independently by individual seat jobs.

#### Scenario: No pull-in condition holds
- **WHEN** the matched candidate class declares no pull-in condition, or its declared condition does not hold for the candidate facts
- **THEN** `council_convening.required_seats` contains exactly the standing per-candidate council seats

#### Scenario: A pull-in condition holds
- **WHEN** the matched candidate class's governed pull-in condition holds for the exact candidate revision
- **THEN** `council_convening.required_seats` contains every standing seat and the conditionally required seat

#### Scenario: Seat jobs do not derive membership
- **WHEN** the resolved convening is dispatched to its required seat jobs
- **THEN** each job receives its assigned seat from the admitted roster and MUST NOT add, remove, or independently re-evaluate roster membership

### Requirement: A resolved roster is provenance-bound and reproducible
The `council_convening` block SHALL carry provenance sufficient to reproduce the
required-seat resolution, including the candidate repository, pull request,
candidate head revision, matched candidate-class identifier, governed rules
repository, rules path and immutable rules revision, and the normalized
candidate facts consumed by the matched condition. A roster conclusion without
those inputs MUST NOT be treated as provenance.

#### Scenario: Resolution is reproduced
- **WHEN** an admission validator loads the cited governed rule revision and evaluates it against the recorded candidate facts
- **THEN** it derives the same `required_seats` value submitted by the producer

#### Scenario: Candidate revision changed
- **WHEN** the current candidate head differs from the head revision bound into the roster provenance
- **THEN** admission is refused and a new roster resolution is required

#### Scenario: Provenance is unavailable or opaque
- **WHEN** the cited rule revision cannot be resolved, a fact used by the condition is absent, or the producer supplies only its conclusion
- **THEN** admission is refused rather than trusting or inferring the roster

### Requirement: The consumer validates and freezes the roster before seat work
The convening consumer SHALL validate the required-seat roster and its
provenance before issuing any seat job, and SHALL freeze both in the immutable
admission snapshot. Validation MUST refuse an absent, malformed, empty,
duplicated, unknown, unreproducible, or rule-inconsistent roster. After
admission, seat-job issuance, return admission, substantive-return counting,
unanimity, and verdict completion SHALL all use that same frozen roster.

#### Scenario: Valid roster is admitted
- **WHEN** the roster is unique, names only declared seats, includes every standing seat, matches the reproduced governed condition, and is bound to the admitted candidate head
- **THEN** the consumer freezes the roster and provenance before issuing exactly one job for each required seat

#### Scenario: Required roster is absent after cutover
- **WHEN** a producer submits a convening without `council_convening.required_seats`
- **THEN** admission is refused with no compatibility path that reconstructs membership from the obsolete payload

#### Scenario: A required seat does not return
- **WHEN** any seat in the frozen roster has no admissible substantive return
- **THEN** the convening cannot complete and the candidate is parked rather than decided from the remaining seats

#### Scenario: An unlisted seat returns
- **WHEN** a return identifies a seat that is not in the frozen roster
- **THEN** that return is refused and MUST NOT affect substantive-return counting, unanimity, or verdict completion

#### Scenario: Rules change after admission
- **WHEN** the governing candidate-class rules change after the roster has been frozen
- **THEN** the admitted convening continues against its frozen rule revision and roster, while a later convening uses the new revision
