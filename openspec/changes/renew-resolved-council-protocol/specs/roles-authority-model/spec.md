## ADDED Requirements

### Requirement: Replacement convenings carry a resolved roster before admission
The replacement council protocol SHALL require a trusted producer to resolve and submit one ordered, nonempty, unique required-seat roster before admission; every standing seat and exactly the conditional seats whose governed conditions hold MUST appear, and an unevaluable condition MUST refuse commissioning rather than become false.

#### Scenario: A conditional seat is required
- **WHEN** the governed condition holds for the exact candidate
- **THEN** the submitted roster contains that seat and every standing seat exactly once

#### Scenario: A condition is false or unavailable
- **WHEN** the condition is false
- **THEN** the conditional seat is absent
- **AND** a missing input or unknown predicate instead refuses before submission

### Requirement: Replacement roster provenance identifies reproducible governed inputs
The replacement protocol SHALL carry normalized consumed facts, the exact candidate repository/pull/head, matched class, and immutable governed rule repository/path/revision; the consumer MUST independently verify rule authority, fact provenance and ordered roster reproduction, refusing an absent, unavailable, malformed, secret-bearing or inconsistent input before any admission write.

#### Scenario: Reproduction succeeds
- **WHEN** the referenced governed rule and exact candidate facts are available and verified
- **THEN** independent evaluation produces exactly the submitted ordered roster

#### Scenario: A conclusion replaces an input
- **WHEN** provenance contains only an opaque digest or asserted pull-in result
- **THEN** admission refuses as unreproducible

#### Scenario: A real but unauthorized rule is cited
- **WHEN** the immutable revision exists but is not an admitted governed rule
- **THEN** admission refuses rather than equating availability with authority

### Requirement: Replacement membership is frozen with exact seat assignments
The replacement protocol SHALL validate and freeze roster/provenance before issuing exactly one durable assignment per required seat, and issuance, registration, completeness and unanimity MUST use that frozen roster rather than reevaluate membership; duplicate/conflicting assignments and unlisted returns MUST refuse.

#### Scenario: Equal counts hide different seats
- **WHEN** a reported bench has the expected count but replaces or duplicates a required seat
- **THEN** completion refuses exact-membership mismatch

#### Scenario: A rule changes after admission
- **WHEN** the current governing rule changes
- **THEN** the admitted roster stays immutable and only new convenings use the new rule

### Requirement: Replacement resolution binds the candidate across submission and admission
The producer SHALL recheck the candidate's current head immediately before submission and the consumer MUST independently verify that same candidate/head at admission; a missing or mismatched head MUST refuse without assignment writes, while a later head MUST require a new convening.

#### Scenario: Head moves between producer check and admission
- **WHEN** the producer recheck succeeds but the head changes before admission
- **THEN** the consumer refuses the stale resolution

### Requirement: Replacement signing proves independent assignment authority
Each required seat SHALL execute in an isolated job with its own ephemeral private key and independently authenticated assignment-scoped authority; registration MUST verify the assigned principal and key possession, and every signature MUST bind protocol, assignment, seat, council, candidate and return digest; shared keys, root-authorization payloads, cross-seat authority and key transport MUST refuse under the replacement protocol.

#### Scenario: A different seat's principal registers a key
- **WHEN** a valid key-possession proof is presented by a principal assigned to another seat
- **THEN** registration refuses before recording the key

#### Scenario: Keys and returns are replayed
- **WHEN** a key is reused across seats or a return is replayed into another assignment or protocol
- **THEN** registration or completion refuses

### Requirement: Replacement producer identity is enforced by verified workflow binding
The producer's admission authority SHALL be bound to the current governed repository identity and verified issuer, audience, subject and permitted workflow/job claims; a workflow-reference string MUST NOT be treated as the OIDC subject, and a broker unable to enforce the complete binding MUST refuse activation rather than accept an approximation.

#### Scenario: The former repository owner or another workflow is presented
- **WHEN** an assertion names an alternate owner or workflow not admitted by the binding
- **THEN** no producer authority is minted

### Requirement: Replacement removal follows versioned coordinated migration
The replacement protocol SHALL follow the provider's deprecation-minor then removal-major policy with versions allocated at realization; one active binding MUST select one protocol and MUST NOT fall back after rejection, and activation/rollback MUST stop intake and coordinate both producer and consumer while retaining historical protocol evidence.

#### Scenario: A roster-less payload reaches the active replacement
- **WHEN** the removal major is activated and an old roster-less or root-authorized payload arrives
- **THEN** it refuses without reconstruction or an old-protocol retry

#### Scenario: Paired rollback is needed
- **WHEN** the activation rehearsal fails
- **THEN** commissioning stays paused until both prior components and bindings are restored and verified
- **AND** historical new-protocol records are not reinterpreted as old records
