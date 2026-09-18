# ideation-dashboard Specification (delta)

## ADDED Requirements

### Requirement: The doxBench chat-turn v1 envelope family is REMOVED at contract-v3.0
The three doxBench chat-turn v1 envelope kinds — `workbench-chat-turn`, `workbench-chat-turn-success` and `workbench-chat-turn-failure` — SHALL be removed at `contract-v3.0`, together with their `$defs` in `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml`, their entries in that file's top-level `oneOf`, the file's whole `deprecated_envelopes` block, their kind constants and dispatch arms in the runtime and the contract validator, their packaged instances, and the committed byte-identity baseline that exists to prove the deprecated bytes never moved.

THE PHASING IS SERVED AND MEASURED. The family was deprecated at
`contract-v1.34` with the deprecation stated MACHINE-READABLY — a top-level
`deprecated_envelopes` block carrying `superseded_by`, `deprecated_in` and
`removal_target` per kind — and the contract validator has WARNED on every
instance of it since, which is the only one of issue #522's three entries whose
warning actually fires. Thirteen minors and one major have passed. The Breaking
class's *"at least one full minor release where the old shape produced
deprecation warnings"* is discharged many times over, so no new deprecation
window is owed.

THE BASELINE TEST RETIRES WITH THE FAMILY, AND ITS RETIREMENT IS NAMED RATHER
THAN PERFORMED SILENTLY. The committed baseline asserts that the v1 `$defs` and
the shared definitions they `$ref` are byte-identical to their `contract-v1.31`
bytes. That assertion exists to protect a shape consumers are pinned to; when
the shape leaves the published surface, the assertion has no subject. Deleting
it as an incidental casualty of a schema edit would be indistinguishable from
deleting it because it had become inconvenient, so the removal states what the
test was for and why it ends.

THE SHARED DEFINITIONS DO NOT LEAVE WITH THE ENVELOPES. `content_hash`,
`confined_path`, `scope_key`, `buffer_state`, `transcript_turn` and
`typed_proposal` are `$ref`-ed by the v1 envelopes AND reachable from the
surviving family; only definitions reachable from the removed envelopes ALONE
may be removed, and each such removal is measured from the surviving family's
own reference closure rather than assumed.

#### Scenario: A v2 turn meets the new major
- **WHEN** a client submits a turn in the surviving `workbench-chat-turn-v2` family at `contract-v3.0`
- **THEN** it MUST validate and be served exactly as before, with no field added, removed or renamed by this removal
- **AND** the surviving family's reference closure MUST still resolve, every shared definition it reaches being retained

#### Scenario: A v1 turn meets the new major
- **WHEN** a client submits a turn carrying one of the three removed v1 kinds against a runtime at `contract-v3.0`
- **THEN** it MUST be refused, no schema branch, no kind constant and no dispatch arm remaining that accepts it
- **AND** the refusal MUST be answered under the unrecognized-kind rule below, never by a surviving copy of the removed family

#### Scenario: A consumer pinned below the removal validates a v1 instance
- **WHEN** a consumer pinned below `contract-v3.0` validates a v1 chat-turn instance against the schema bytes it pins
- **THEN** it MUST still validate, and MUST still receive the deprecation warning it received before, because compatibility flows from the consumer and no new release reaches backwards into an old pin

#### Scenario: The packaged corpus is retired with the family
- **WHEN** the removal lands
- **THEN** every packaged instance declaring a removed kind MUST be retired with it — including the NEGATIVE fixtures, which outnumber the positive ones
- **AND** any refusal case those negatives covered that has no equivalent in the surviving family's corpus MUST be either re-expressed against the surviving family or recorded as a stated coverage loss, never dropped in silence

#### Scenario: The machine-readable deprecation block is removed
- **WHEN** the three kinds leave the schema
- **THEN** the file's `deprecated_envelopes` block MUST be removed with them, because a block declaring the deprecation of kinds the file no longer defines names nothing
- **AND** the deprecation record MUST NOT vanish with it: the entry MUST move to `docs/contract-versioning-policy.md` § Deprecations Executed, where a consumer upgrading across the removal can still read the migration path

#### Scenario: The validator's deprecation warnings after the removal
- **WHEN** the contract validator is run over a clean checkout at `contract-v3.0`
- **THEN** it MUST report ZERO chat-turn deprecation warnings, where a default run before the removal reported four, all naming a spent removal target
- **AND** `--strict` MUST stop failing on the packaged chat-turn fixtures for that reason

#### Scenario: Prose that survives its own subject
- **WHEN** documentation states that a condition holds "until the removal target `contract-v2.0` retires the fixtures with the family"
- **THEN** it MUST be repaired in the same cut as the removal, that sentence having been false since `contract-v2.0` shipped on 2026-08-27 and nothing having noticed

### Requirement: An unrecognized chat-turn kind is refused in the SURVIVING family, never coerced into a removed one
An unrecognized or absent chat-turn `kind` SHALL be answered in the SURVIVING envelope family's failure shape, carrying an explicit unknown-kind error code, and MUST NOT be coerced into any family the release has removed; where the request carries no wire-valid turn identity, the existing pre-identity refusal shape SHALL be used unchanged, because the surviving failure envelope requires a `client_turn_id` and no identity may be invented to obtain one.

THIS IS A REDESIGN, NOT A DELETION, AND THE DIFFERENCE IS THE WHOLE POINT. While
two families were served, the route read the family off the request's own `kind`
and answered in the family the request arrived in — with the v1 family as the
DEFAULT for anything unrecognized, on the stated reason that *"a request that
never named a family it could be answered in gets the posture it would have got
before this release"*. That reason dies with v1: after the removal the default
names a family that does not exist, and a realization that merely deleted the v1
arm would leave the `else` branch dispatching to a parser and an envelope builder
that are gone.

THE SURVIVING FAILURE ENVELOPE CAN CARRY THE CODE, AND THAT IS A MEASUREMENT.
The released `workbench-chat-turn-v2-failure` shape requires
`schema_version`, `kind`, `client_turn_id`, `error` and `message`, and constrains
`error` only by a lowercase-identifier PATTERN — no enum at the schema layer, and
the delegated validator that judges it applies no code vocabulary either. A new
explicit code is therefore contract-permitted without widening anything. The
CLOSED list is the server's own error catalog, which maps code to status and to
a fixed message; the new code is registered there in the same cut, or the refusal
path raises instead of refusing.

THE ALTERNATIVE IS RECORDED RATHER THAN LEFT UNSAID. The other honest posture is
to refuse every unrecognized kind OUTSIDE any contract envelope, in the
pre-identity shape, whatever identity the request supplied. It is simpler and
asserts less. It is not taken because it discards an identity the request DID
supply, hands the client a body carrying no `kind` its own dispatch can route,
and makes the refusal invisible to the contract corpus — three costs paid to
avoid registering one error code.

#### Scenario: An unrecognized kind arrives with a wire-valid turn identity
- **WHEN** a chat-turn request carries a `kind` that is not the surviving family's request kind, and a wire-valid `client_turn_id`
- **THEN** it MUST be refused in the surviving family's failure envelope, carrying an explicit unknown-kind error code and that turn identity
- **AND** the envelope MUST be self-validated against the released schema before it is sent, exactly as every other refusal in this family is

#### Scenario: An unrecognized kind arrives with no wire-valid turn identity
- **WHEN** a chat-turn request carries an unrecognized `kind` and no wire-valid `client_turn_id`
- **THEN** the existing pre-identity refusal shape MUST be used, unchanged
- **AND** no turn identity MUST be invented in order to reach the contract envelope

#### Scenario: A realization deletes the fallback instead of redesigning it
- **WHEN** a realization removes the v1 family and leaves the kind-discrimination default naming it
- **THEN** it MUST be rejected — the default would dispatch to a parser and an envelope builder that no longer exist, turning an unrecognized kind into a server fault rather than a refusal

#### Scenario: The new code is not registered
- **WHEN** an unknown-kind code is answered without being registered in the server's closed error catalog
- **THEN** the refusal path raises instead of refusing, so the registration MUST land in the same cut as the code

#### Scenario: A removed kind is treated as merely unrecognized
- **WHEN** the unrecognized kind is one of the three the release removed
- **THEN** it MUST take exactly this path and no other, because after the removal a retired kind and a kind that never existed are the same fact about the wire

## MODIFIED Requirements

### Requirement: The chat-turn contract release carries the bound buffer and the model
This capability's widened turn SHALL be carried by a RELEASED chat-turn contract, and the release SHALL be additive: the currently released envelopes SHALL remain valid and byte-identical, and the widened shape SHALL be introduced as a co-resident envelope family rather than by mutating a closed envelope, so nothing that validates today stops validating. The released widened family SHALL carry, at minimum: the outline plus every loaded document buffer, the BOUND BUFFER's key on both the request and the durable record, the per-buffer observed hashes keyed by buffer, a proposal target expressed as a buffer key, and the SELECTED-MODEL metadata that lets a record state which model answered. The release version SHALL be ALLOCATED AT REALIZATION under the repository's contract-versioning policy and MUST NOT be reserved by this proposal, because a reserved number is a claim about a merge order nobody knows yet. The release SHALL record its change class, its migration note, and the removal target for anything it deprecates, and the older family SHALL keep working for at least one full published release after it is deprecated. The runtime SHALL keep resolving its pinned wire schemas from the checkout it runs in and MUST keep refusing before consulting any provider when a pinned contract cannot be read; a release MUST NOT relax that refusal. A field the released envelope has no room for MUST NOT be carried as a server-side-only value that no reader can consult, and MUST NOT be inferred from an adjacent field that answers a different question — the record either names the thing or the gap stays stated.

**THE ADDITIVE OBLIGATIONS ABOVE DESCRIBE THE WIDENING RELEASE AND ARE
DISCHARGED BY IT; THEY ARE NOT A PERPETUAL GUARANTEE.** The v1 family kept
validating, kept being served, and kept its `contract-v1.31` bytes from
`contract-v1.34` through `contract-v2.5` — thirteen minors and one major, far
past the *"at least one full published release"* floor this requirement sets.
The same release also recorded, as this requirement's own text requires, the
removal target for what it deprecated. This amendment EXECUTES that recorded
target rather than lifting it: at `contract-v3.0` the v1 family is removed, and
the scenario "An older client sends a released v1 turn" below states what the
WIDENING release owed and delivered, not an obligation that outlives the removal
the same release announced.

**A CO-RESIDENT FAMILY THAT IS NEVER REMOVED IS NOT A DEPRECATION, IT IS A
SECOND CONTRACT.** The requirement above obliges a release to record "the
removal target for anything it deprecates". A target recorded and never reached
makes that recording ornamental, and the estate has now demonstrated the failure
mode: this family's target was `contract-v2.0`, that major shipped on
2026-08-27, and the only thing that noticed was a validator warning nobody was
reading. Recording the target and reaching it are one obligation, not two.

**AND THE POSTURE FOR AN UNRECOGNIZED KIND IS A DECISION THIS AMENDMENT OWES
RATHER THAN A CONSEQUENCE IT INHERITS.** While two families were served, an
unrecognized `kind` was answered in the DEPRECATED family, deliberately and with
a stated reason. Removing that family removes the reason. The removal therefore
carries a redesigned posture — refusal in the surviving family with an explicit
unknown-kind code, and the pre-identity shape where no wire-valid identity
exists — and MUST NOT arrive as a deleted branch.

#### Scenario: An older client sends a released v1 turn
- **WHEN** a client submits a turn in the previously released envelope shape
- **THEN** it MUST still validate and MUST still be served
- **AND** the older shape's bytes MUST be unchanged by this release

#### Scenario: The release version is reserved early
- **WHEN** a proposal would reserve the release's version number before merge order is known
- **THEN** it MUST be rejected — the version is allocated at realization

#### Scenario: A record is asked which model answered
- **WHEN** a reader consults a turn record for the model that produced it
- **THEN** the record MUST name it from the released envelope's own metadata

#### Scenario: A field has no room in the envelope
- **WHEN** a needed field does not fit the released envelope
- **THEN** it MUST NOT be carried as an unreadable server-side-only value or inferred from a field that answers a different question
- **AND** the obligation MUST be recorded against the release that will carry it

#### Scenario: The removal target the release recorded is reached
- **WHEN** the declared bundle reaches the removal target a release recorded for a family it deprecated
- **THEN** the removal MUST be executed in that release, or the target MUST be restated with the reason it was not
- **AND** a target that is recorded and then never reached MUST NOT be treated as satisfying this requirement's obligation to record one

#### Scenario: A client sends a v1 turn after the removal
- **WHEN** a client submits a turn in the removed v1 envelope shape against a runtime at `contract-v3.0` or later
- **THEN** it MUST be refused, in the SURVIVING family's failure envelope with an explicit unknown-kind code
- **AND** it MUST NOT be answered in the removed family, which no longer exists to answer in

#### Scenario: A consumer pinned below the removal
- **WHEN** a consumer pinned below `contract-v3.0` validates a v1 instance against the schema bytes its pin names
- **THEN** it MUST still validate, unchanged, because compatibility flows from the consumer and no new release reaches backwards into an old pin
- **AND** the "byte-identical" promise above is kept for that consumer by the immutability of the bytes it pins, not by their continued presence on the current surface
