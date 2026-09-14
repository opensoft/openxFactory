# review-authority-intake Specification

**DELTA CLASS: `## ADDED`, AND THE CHOICE IS FORCED RATHER THAN PREFERRED.**
This capability has **no promoted specification** — `openspec/specs/` carries
no `review-authority-intake/spec.md`, because the two changes that author it,
`add-wallet-carried-review-authority` (ratified 2026-08-23) and
`register-gate-rules-council-seats` (ratified 2026-09-06), are both ACTIVE and
neither has archived. There is therefore no requirement here to `## MODIFIED`:
the sentence this packet was raised against is not in canon, it is in an
operator runbook (`docs/governed-reissuance-runbook.md` §5.2 step 3) and in a
change-local design document that is being archived. These four requirements
are ADDED, they promote at THIS change's archive, and `proposal.md` § "Why the
delta is ADDED and not MODIFIED" states the consequence rather than leaving it
to be inferred.

## ADDED Requirements

### Requirement: A re-issuance's projection step exits on an observed projection, never on an admitted convening
A governed re-issuance's projection step SHALL exit only on a DIRECT
OBSERVATION of the published register projection's own declared provenance, and
SHALL NOT be exited on the strength of an admitted convening; an admission
establishes the materialized council content, the subject pin and the
once-per-pin discipline, and it establishes NOTHING about which revision of the
register the runtime is resolving authority against.

**The two projections are different artifacts and a re-issuance that conflates
them proves nothing.** The convening admission path resolves the DOMAIN-CONTENT
projection. The REGISTER projection — the one that carries grant state, and the
one whose age the declared revocation staleness bound bounds — is read at
VERDICT CONSUMPTION, which a lane that convenes no seat never reaches. An
admitted convening is therefore silent on the re-issued grant by construction,
not by accident, and the silence is not repaired by dispatching a second one.

**AND THE WRONG-MOMENT CASE IS WORSE THAN SILENCE.** Dispatched before the
projection has been re-derived, the same convening returns a GREEN ADMISSION
against a projection that predates the register act — a manufactured clearance
that reads exactly like the proof, which is the failure the governed
re-issuance discipline exists to refuse.

#### Scenario: An admitted convening is offered as the projection proof
- **WHEN** a re-issuance offers an admitted convening as evidence that the register projection carries the re-issued grant
- **THEN** the projection step is NOT exited, because the admission path does not resolve the register projection
- **AND** the record states the substitution in terms rather than reading the two checks as the same check

#### Scenario: The projection is observed carrying the act
- **WHEN** the published register projection's declared source revision is the register act's landed commit or a descendant of it
- **THEN** the projection step is satisfied, and the observation is recorded with the values it read

#### Scenario: No authorized observation is available
- **WHEN** no authorized observation of the register projection can be made
- **THEN** the step stays OPEN, any park stays in force, and the re-issuance MUST NOT be recorded as complete

### Requirement: The projection observation is a read-only act on a named operator's word, recorded with its values
An observation offered as a re-issuance's projection proof SHALL be performed
READ-ONLY, on a named human operator's word that names the EXECUTING LANE, and
SHALL be recorded in the re-issuance record with the commands run, the values
read verbatim, and the comparison that decides the exit — never as a bare
assertion that the projection was re-derived.

**The authority is a governance fact and not a convenience.** The register
projection is published where the governed repository cannot see it: no commit,
no check and no artifact in the repository carries its content, so the only
path to it crosses from the governed tree into a running system. That crossing
is an operator act, it names who performed it, and a re-issuance that treats it
as routine tooling has moved a human-only step into a lane's discretion.

#### Scenario: The record asserts the re-derivation without its values
- **WHEN** a re-issuance record states that the projection was re-derived and carries neither the values read nor the comparison
- **THEN** the assertion is not accepted as the projection step's evidence

#### Scenario: The observation uses a verb that could change state
- **WHEN** an observation offered as the projection proof uses any verb capable of changing the observed system
- **THEN** it is refused as a proof, because the evidence for a projection is a READ and a re-issuance never proves a state by moving it

#### Scenario: No operator word names an executing lane
- **WHEN** no operator's word names a lane to perform the observation
- **THEN** the step stays open and is recorded as OWED with the owner who can give that word

### Requirement: A projection observation follows a refresh that post-dates the register act, and the staleness bound does not stand in for one
A projection observation SHALL be taken only after a refresh cycle that
COMPLETED AFTER the register act landed, evidenced by the refresher's own
success record, and a projection within its declared staleness bound SHALL NOT
be read as carrying an act that post-dates the revision it was derived from.

**Currency and content are two different questions and the bound answers only
the first.** The declared revocation staleness bound governs how long a
revocation may go unhonoured; it is not a freshness proof for any particular
act. A projection derived minutes before the register act lands sits well
inside any sane bound and still carries the superseded grant, so the currency
gate passes it — which is precisely the route by which a pre-act projection
returns a green admission.

**A SCHEDULE IS NOT A CYCLE.** Naming a refresher's cadence states when a cycle
was DUE. The precondition is a cycle that ran and succeeded after the act, and
the evidence for it is the refresher's own record of that run.

#### Scenario: The projection is inside its bound but predates the act
- **WHEN** the published projection is well inside its declared staleness bound and its declared source revision does not contain the register act
- **THEN** the projection step is not exited, and the currency of the projection is not offered as the reason it passes

#### Scenario: The completed refresh cycle is evidenced
- **WHEN** the refresher's own success record shows a cycle that completed after the register act landed
- **THEN** that cycle is named in the record as the met precondition, rather than assumed from the schedule

#### Scenario: A cadence is cited in place of a cycle
- **WHEN** a record cites the refresher's schedule rather than an observed completed cycle
- **THEN** the precondition is NOT met, because a schedule states when a refresh was due and not that one happened

### Requirement: A projection observation states the limit of what it establishes
A projection observation SHALL state which fields it read and SHALL name the
fields it did NOT read as OWED with an owner, and the re-issuance record MUST
NOT be written as establishing more than the fields the observation names.

**An observation of provenance is not an observation of content.** Reading the
projection's declared source revision establishes that the published projection
was derived from a revision that contains the act. It does not read the
projected rows back, so the row-level confirmations — the authority row's
repointed grant reference, its matching expiry, and the staleness bound
travelling verbatim into the projection — follow only if the refresher is
faithful to its input. That is the refresher's whole job and it is not a thing
such an observation observed.

**RECORDING THE GAP IS THE REQUIREMENT, NOT CLOSING IT.** A re-issuance is not
blocked on reading every field; it is blocked on claiming to have read them.

#### Scenario: A provenance-only observation is recorded
- **WHEN** an observation reads the projection's declared source revision and not the projected row contents
- **THEN** the record states that the proof is BY SOURCE REVISION and names the unread row-level fields as owed, with the owner who next has cause to read them

#### Scenario: A record claims more than the observation read
- **WHEN** a re-issuance record states that the projection carries the re-issued grant on an observation that read only the provenance
- **THEN** the overclaim is itself a finding against the record, and the record is corrected by a dated append rather than by a rewrite

#### Scenario: The owed fields are read later
- **WHEN** a later authorized observation reads the row-level fields the earlier one named as owed
- **THEN** the result is recorded against the same re-issuance, whichever way it comes out
