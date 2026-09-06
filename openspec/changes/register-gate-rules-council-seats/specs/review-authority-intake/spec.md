# review-authority-intake Specification

## ADDED Requirements

### Requirement: A second commissioned body enters the register as its own authority row
A body other than the one the MVP register commissions SHALL enter the intake
register as its OWN authority row — its own `row_id`, `holder_ref`,
`wallet_ref`, `grant_ref` and `expires_at` — and SHALL NOT be attached to
another body's row by sharing that row's wallet, grant or holder; the MVP's
single-row shape is a FIRST shape and this requirement is the named successor
its own text contemplates, so widening it is a ratified act and never an
incidental consequence of adding a seat.

#### Scenario: A second council is registered
- **WHEN** a second council body is commissioned for review authority over a governed object
- **THEN** the register carries a second authority row naming that body as `holder_ref`
- **AND** that row resolves to its own wallet, its own grant and its own custody attestation

#### Scenario: A second body is attached to the first body's row
- **WHEN** a seat of a second council is recorded against an authority row whose `holder_ref` is a different body
- **THEN** the entry is refused, because a key descending from another body's authority descends from authority that body never held

#### Scenario: The widening is not incidental
- **WHEN** a change adds a seat for a body the register does not already commission
- **THEN** the change MUST ratify the additional authority row explicitly, and MUST NOT treat the row as bookkeeping carried along by the seat

### Requirement: Seat identity in the register is the pair of council and seat, never the seat name alone
A per-seat entry's identity in the intake register SHALL be the PAIR
(`council_id`, `seat_id`) and uniqueness SHALL be enforced over that pair, never
over `seat_id` alone; two distinct bodies commonly seat the same role name, and a
reader that refuses the second one as a duplicate makes the register unable to
represent a second council at all — while a reader that silently accepts it would
let one body's key answer for another body's seat.

#### Scenario: Two councils seat the same role name
- **WHEN** two commissioned bodies each seat a role with the same `seat_id`
- **THEN** both entries are admitted, distinguished by their `council_id`
- **AND** neither is reported as a duplicate of the other

#### Scenario: One council names a seat twice
- **WHEN** one `council_id` records the same `seat_id` twice
- **THEN** the entry is refused rather than resolved by file order

#### Scenario: A key identifier collides across bodies
- **WHEN** two entries share a `key_id` or a `key_fingerprint`
- **THEN** the entries are refused regardless of their councils, because a key is one key and two bodies presenting it are two claims on one identity

### Requirement: A body with no declared composition is not issued review authority
A body SHALL NOT be issued a review-authority grant until its DECLARED
COMPOSITION exists in the domain repository that governs its roster — pinned to
exact model identifiers and never to a model family — because the ratified
drift-cascade rule revokes on any single declared component changing, and a
grant issued against a composition that does not exist has nothing to be revoked
against; a body whose roster carries no composition source map SHALL have that
map authored as a prerequisite act of its registration, and the registration
SHALL NOT proceed by declaring the composition absent.

#### Scenario: A council has no composition source map
- **WHEN** a council's roster declares seats but no composition source map, and no profile in the domain's agent mix names it
- **THEN** the grant is not issued, and authoring the map is a named prerequisite with an owner

#### Scenario: A composition is pinned to a family
- **WHEN** a body's declared composition names a model family rather than an exact identifier
- **THEN** the declaration is refused, per the standing ruling that exact model versions only are admitted

#### Scenario: One roster flip reaches two bodies
- **WHEN** two commissioned bodies draw their composition from one shared enrolled roster and that roster's model pin moves
- **THEN** both bodies' grants are revoked by the same event, and the re-issuance is a scheduled act for each body separately with its own record

### Requirement: A symbolic seat and a conditionally pulled-in persona are not registered until the council seats them by identifier
The register SHALL record a per-seat key only for a seat the council seats BY
IDENTIFIER, and SHALL NOT record one for a seat declared symbolic, unbound, or
named only as a persona pulled in by a condition; recording a key for a slot no
convening can present is recording authority nothing will ever exercise, and the
register's own text already refuses a seat the council does not seat.

#### Scenario: A roster carries a symbolic slot
- **WHEN** a council's roster declares a seat whose binding is symbolic until a later roster lands
- **THEN** no key is minted or recorded for it, and its registration is deferred to the act that binds it to a persona

#### Scenario: A persona is pulled in by a declared condition
- **WHEN** a council's roster names a persona that a declared condition seats as an additional voice, without giving it a seat identifier
- **THEN** no key is recorded for that persona until the roster names it as a seat with an identifier
- **AND** the deferral is recorded as an open question with an owner, not left silent

#### Scenario: A conditional seat carries an identifier
- **WHEN** a council's roster seats a conditional seat by identifier
- **THEN** its key is minted and recorded with the unconditional seats, so that the first convening the condition holds for is not the convening that discovers a missing key

### Requirement: The rule-setting body never clears a candidate that edits the register or the artifacts that confer its own authority
The body that SETS a repository's gate rules SHALL NOT be eligible to clear a
candidate that edits the intake register, the product pin that selects the reader
which opens it, or the grant, wallet and custody attestation that confer that
body's own review authority; where a gate enumerates never-clearable floor
members by exact path, the artifacts conferring a registered body's authority
SHALL be entered there BY NAME, and a change that registers a body in
directories the floor does not name SHALL record that gap with an owner rather
than inherit it silently.

#### Scenario: The rule-setting body is offered its own floor
- **WHEN** a candidate edits the intake register, or the gate rule naming that register as never-clearable, and the rule-setting council is convened over it
- **THEN** the candidate is human-only and no verdict clears it

#### Scenario: A body's own grant sits outside the floor
- **WHEN** a registration adds a grant, wallet or custody attestation in a directory the consuming repository's floor does not name by path
- **THEN** the registration records the reachability gap by name, with the owner who closes it
- **AND** the gap MUST NOT be treated as closed by the register file's own floor entry

#### Scenario: A council edits the pin that selects its reader
- **WHEN** a candidate moves the product pin that selects which reader opens the register
- **THEN** the candidate is never-clearable on the same ground as the register itself, because a body that may choose its own reader may choose one that admits it

### Requirement: A register act a pinned reader cannot represent is sequenced behind the reader and never worked around
A register act whose correct outcome the PINNED reader refuses SHALL be sequenced
BEHIND a reader that can represent it — the reader change in the repository that
owns the reader, then the consuming pin advance, then the act — and SHALL NOT be
landed against a refusing reader, nor made green by narrowing the act, splitting
it across states no ordering makes valid, or exempting the required check; where
such a refusal is discovered by an act already in flight, the discovery SHALL be
recorded as evidence about the reader rather than about the act.

#### Scenario: The reader refuses a correct act
- **WHEN** the pinned reader emits a finding on a register act that is correct by the ratified rules
- **THEN** the act is held until the reader is widened and the pin advances, and the finding is recorded as a reader defect with a named owner

#### Scenario: A workaround would make the gate green
- **WHEN** a narrowing of the act, or an exemption of the required check, would turn the gate green over the refusing reader
- **THEN** the workaround is refused and enumerated with the reason, so it is not re-proposed

#### Scenario: The consuming gate asserts literal counts
- **WHEN** a consuming repository's required check asserts LITERAL counts over the reader's notes
- **THEN** a registration that changes those counts MUST move the assertions in the same act, since a wildcard would let a register that lost a body pass the positive assertion

### Requirement: One revocation staleness bound governs the whole register
The intake register SHALL declare exactly ONE `revocation_staleness_bound`
covering every row it carries, and SHALL NOT declare a per-row or per-body bound;
the bound is how long a revocation may go unhonoured by the runtime's projection
of this file, which is one projection over one file, so a second commissioned
body inherits the declared bound unchanged and a registration act SHALL NOT
tighten or loosen it as a tidy-up.

#### Scenario: A second body is registered
- **WHEN** a second authority row is added to the register
- **THEN** the existing `revocation_staleness_bound` governs it unchanged, and the registering act does not move that line

#### Scenario: A per-body bound is proposed
- **WHEN** a proposal would give one body a tighter bound than another
- **THEN** it is refused, because the runtime resolves one projection whose age is one fact

#### Scenario: The bound is tightened
- **WHEN** the bound is tightened
- **THEN** it is tightened as its own governed edit to that line, justified by the projection refresh cadence that makes the tighter number meetable
