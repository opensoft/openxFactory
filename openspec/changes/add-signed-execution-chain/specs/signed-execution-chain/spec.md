# signed-execution-chain Specification (delta)

Tranche one of the staged topic `signed-execution-chain`: the chain's root and
its constitution. Links 4–10 of the topic's ten-link model are named successors
and no requirement below reaches them.

## ADDED Requirements

### Requirement: A governed ratification enters a signed execution chain only as a key-attributed grant exercise whose proof of possession was verified

A governed ratification SHALL enter a signed execution chain only where it is
recorded as an exercise of a wallet-carried authority whose proof of possession
was PRESENTED AND VERIFIED, whose attribution is key-attributed to the presenting
wallet key, and whose revocation was checked AT EXERCISE rather than inherited
from issuance. Authority travels as an attenuated grant and by nothing else, per
`review-authority-intake`'s requirement *"Review authority is held as an
openxwallet grant and by nothing else"*; possession of a grant is not its
exercise, per the pinned openXwallet requirement *"Use requires proof of
possession, not presentation"*, whose refusal names the MISSING PROOF and not a
missing grant. What a signature EVIDENCES is bounded by the declared custody of
the key that made it, and this capability SHALL derive that bound from the
custody declaration rather than restating a custody model of its own.

Where the ratifying authority holds standing authority with no wallet and no
grant — the root-issuer case `review-authority-intake` expressly permits, in
which the responsible operator's authority is standing under the Human Escalation
Contract and "requires no wallet and no grant of its own" — the chain SHALL
DECLARE its origin as standing authority rather than treating the absent
signature as an exemption, and such a chain SHALL NOT be presented as, or
accepted for, an assurance that requires a signature-rooted origin. A chain
declaring no origin SHALL be read as the weaker of the two, never the stronger.

A standing-authority origin SHALL NOT be self-asserted. It is admissible only for
an authority whose standing is already anchored OUTSIDE the record it writes into
— the root-issuer anchor `review-authority-intake` requires — and an actor
claiming it without that anchor SHALL be refused, because an origin anyone may
declare is not a declaration but a bypass.

#### Scenario: A grant is presented without proof of possession

- **WHEN** a ratification offers a grant with no signature over the request from the audience wallet
- **THEN** the ratification is refused and no chain begins
- **AND** the refusal names the missing proof of possession rather than a missing grant

#### Scenario: A signature is present and does not verify

- **WHEN** a ratification carries a signature that fails verification
- **THEN** it is refused and recorded as a verification failure
- **AND** that record stays distinguishable from a request that carried no signature at all, because the two describe different events

#### Scenario: The act is attributable only to a shared credential

- **WHEN** no wallet key can be established for the ratifying act and it reached its surface through a shared installation credential
- **THEN** the act is recorded as unattributed and the shared credential as transport
- **AND** no chain begins, because an unattributed act is not assigned to a holder

#### Scenario: The grant was revoked between issuance and ratification

- **WHEN** the grant, an ancestor of it, or the holder's standing was revoked before the ratifying exercise
- **THEN** the exercise is refused and no chain begins
- **AND** issuance-time validity is not accepted as evidence of current validity

#### Scenario: A standing authority with no wallet ratifies

- **WHEN** the ratifying authority is the root issuer acting under standing authority with no wallet and no grant
- **THEN** the chain records its origin as standing authority
- **AND** the chain is refused wherever a signature-rooted origin is required, rather than being accepted as though it carried one

#### Scenario: An actor declares a standing-authority origin for itself

- **WHEN** an actor whose standing is not anchored outside the record it writes into declares its chain's origin as standing authority
- **THEN** the declaration is refused
- **AND** the absence of a wallet is not accepted as a reason to admit the act

### Requirement: Ratification and chain enrollment are one atomic act, and neither half stands alone

A ratification and the CHAIN ENROLLMENT of what it ratifies SHALL be one signed
act, and neither half SHALL stand alone: there is no ratified object without its
chain and no chain without the ratification it descends from. The enrollment
declaration SHALL be covered by the ratifying signature — bound before signing,
never attached after it — so the two halves are two views of ONE signed object
rather than two facts that could diverge. A ratified-but-unenrolled state and an
enrolled-but-unratified state are each a REFUSING state and SHALL NOT be recorded
as a partial success.

A ratification whose genesis link is not present in the evidence plane SHALL NOT
be presented as ratified, because a ratification's standing is DERIVED from its
link and is never stored beside it. Recovery from a failed record SHALL be
re-recording the same signed bytes, which is idempotent on the chain identity; a
fresh signature produces a DIFFERENT chain and SHALL NOT be presented as recovery
of the first. A chain whose ratification cannot be resolved
or does not verify SHALL NOT be repaired by producing a ratification afterwards;
the remedy is a new handshake producing a new chain, and the broken chain stays
broken on the record.

#### Scenario: The signature verifies and the genesis link cannot be written

- **WHEN** a ratifying signature verifies but the genesis link cannot be recorded in the evidence plane
- **THEN** nothing is presented as ratified and the act is refused as a whole
- **AND** the recovery is to re-record the same signed bytes, which yields the same chain rather than a second one

#### Scenario: A ratified marker is written before the link lands

- **WHEN** an implementation records a ratified standing beside the object rather than deriving it from the presence of the genesis link
- **THEN** the implementation is nonconforming, because it reintroduces the divergence this requirement exists to make impossible

#### Scenario: A chain names a ratification that does not verify

- **WHEN** a chain's genesis link names a ratifying exercise that cannot be resolved or whose signature does not verify
- **THEN** the chain is refused at its root
- **AND** producing the missing ratification afterwards does not repair it, because a signature made after the fact over an object already claiming to descend from it is the fabrication this capability refuses

#### Scenario: The enrollment declaration is attached after signing

- **WHEN** a chain enrollment is recorded as a separate act outside the bytes the ratifier signed
- **THEN** it is refused, because an unsigned enrollment is exactly the second act that could diverge

### Requirement: The chain identity is the digest of the signed ratification, fixed once at chain enrollment

A signed execution chain SHALL be identified by the digest of the signed
ratification that begins it, computed over the signed bytes at CHAIN ENROLLMENT
and immutable thereafter. The identity SHALL be COMPUTED by every reader and
never accepted as asserted: a link whose claimed chain identity does not equal the
digest of the signed ratification it carries SHALL be refused. Because the
identity is that digest, one ratification yields exactly one identity and two
distinct ratifications cannot share one — those two properties hold BY
CONSTRUCTION and SHALL NOT be restated as separate refusals a reader might expect
a validator to enforce independently. Re-ratifying an object SHALL begin a NEW
chain with a new identity and SHALL NOT re-use, extend, or re-point an existing
one.

The signed bytes carry the enrollment DECLARATION and never the identity derived
from them, so the identity is a consequence of the signature rather than an input
to it.

#### Scenario: The same signed bytes are recorded twice

- **WHEN** a genesis link is re-recorded after a failed write
- **THEN** the chain identity is unchanged and one chain exists
- **AND** the second record is recognized as the same enrollment rather than as a new chain

#### Scenario: A link asserts an identity its own bytes do not produce

- **WHEN** a link claims a chain identity that is not the digest of the signed ratification it carries
- **THEN** it is refused
- **AND** the claimed value is not adopted, because the identity is computed by the reader and never accepted as asserted

#### Scenario: An object is ratified a second time

- **WHEN** an object that already carries a chain is ratified again
- **THEN** a new chain begins with its own identity
- **AND** the earlier chain is neither extended nor re-pointed at the new ratification

### Requirement: Every link signs the chain identity and its predecessor's digest

Every link of a signed execution chain after the genesis link SHALL cover, WITHIN
the bytes it signs, both the chain identity and the digest of the link that
immediately precedes it, so that a chain is hash-linked rather than a collection
of signatures about the same subject. A verifier SHALL check that continuity and
not merely the presence of the required signatures: individually valid links
produced by DIFFERENT executions SHALL NOT assemble into one chain, and a link
whose own signature verifies but which does not bind the chain identity and its
predecessor SHALL be refused despite verifying.

#### Scenario: Valid links from different executions are assembled

- **WHEN** links that each verify individually, but which name different chain identities or do not form one predecessor sequence, are offered as one chain
- **THEN** the assembly is refused
- **AND** the refusal names the broken continuity rather than reporting a signature failure, because every signature was valid

#### Scenario: A link signs only its own content

- **WHEN** a successor link's signed bytes cover its content but neither the chain identity nor its predecessor's digest
- **THEN** the link is refused
- **AND** the validity of its signature does not admit it

#### Scenario: A verifier checks signatures only

- **WHEN** a verifier accepts a chain on the strength of every link's signature verifying
- **THEN** the verifier is nonconforming, because it has verified a collection of signatures and not a chain

### Requirement: The chain travels with the work as a carried contract, verifiable at the point of use

A signed execution chain SHALL travel WITH the work it governs as a carried
artifact, so that a consumer can verify it at the point of use without resolving a
mutable external table, and the carried copy SHALL be verifiable against the chain
identity so that a substituted or altered copy is detected rather than trusted. A
consumer that can only resolve the chain by lookup SHALL record that it verified a
lookup and SHALL NOT record that it verified a carried contract, because the two
differ in exactly what an attacker who controls the table can do.

#### Scenario: A consumer verifies at the point of use

- **WHEN** work reaches a consumer that must decide whether to proceed
- **THEN** the chain accompanies that work and is verified there
- **AND** proceeding does not depend on a lookup against a table the consumer does not control

#### Scenario: A carried copy has been altered

- **WHEN** a carried chain's bytes do not reproduce the chain identity they claim
- **THEN** the copy is refused rather than reconciled against a stored version

#### Scenario: Only a lookup is available

- **WHEN** a consumer can resolve the chain only through an external table
- **THEN** it records that it verified a lookup
- **AND** it MUST NOT report that as verification of a carried contract

### Requirement: A gap in the links a chain is required to carry is refused as a fraud signal, never downgraded

A consumer that validates a signed execution chain SHALL determine the links the
chain is REQUIRED to carry at that point from its OWN DECLARED EXPECTATION, never
from the set of links it was handed, and SHALL validate every one of them; a link
that is missing, unverifiable, or not bound to the chain SHALL be refused and
reported as a FRAUD SIGNAL rather than downgraded to a warning, an advisory, or a
degraded pass — a gap means either the
act did not happen or something is misrepresenting that it did, and both are
refusals. A consumer that CANNOT evaluate the chain SHALL refuse rather than
proceed, because an unevaluable answer is never permission, and every refusal
SHALL name which link failed and why. A consumer holding NO declared expectation
SHALL refuse rather than accept whatever it was handed, because a chain judged
against the links it supplied is complete by definition and can never be found
short.

This requirement binds what a validating consumer must DO. It creates, names and
requires no enforcement point, and SHALL NOT be read as asserting that any gate,
check, or lane validates chains today; where no such point exists for a surface,
the capability records that surface as unenforced rather than describing it as
governed.

#### Scenario: A required link is absent

- **WHEN** a chain is offered carrying fewer links than the consumer's declared expectation requires at that point
- **THEN** the absent links are refused as MISSING and reported as a fraud signal naming each one
- **AND** the supplied set is not accepted as evidence that no more were required
- **AND** the consumer does not proceed with a warning

#### Scenario: A consumer holds no declared expectation

- **WHEN** a consumer validates a chain without a declared expectation of the links required at that point
- **THEN** it refuses
- **AND** it does not accept the chain on the strength of every supplied link verifying

#### Scenario: The chain cannot be evaluated

- **WHEN** the evidence plane is unreachable, the carried contract unparseable, or a signature algorithm unavailable
- **THEN** the consumer refuses
- **AND** the inability to evaluate is never recorded as a pass

#### Scenario: The requirement is read as an enforcement claim

- **WHEN** a statement of this capability is offered as evidence that some gate validates chains
- **THEN** the statement is corrected, because this requirement binds validating consumers and names no gate

### Requirement: The evidence plane is an append-only signed log in the governed store, and it is the record

Every link of a signed execution chain SHALL be written as a signed leaf of an
APPEND-ONLY log held inside the governed store, and that log SHALL be THE record
of the chain: its evidentiary standing SHALL NOT depend on any external witness,
later publication, or subsequent republication of its contents anywhere else. A
design in which some external witness is the record, rather than a witness TO the
record, is nonconforming.

A leaf SHALL NOT be rewritten or removed once written; a correction is a NEW leaf
that supersedes an earlier one and names it, so that the history of a chain
remains readable rather than being replaced by its latest state.

#### Scenario: A link is written

- **WHEN** a chain link is created
- **THEN** it is appended to the log as a signed leaf
- **AND** the log's own record is sufficient to verify the chain with no external source consulted

#### Scenario: A leaf is corrected

- **WHEN** a recorded leaf is found to be wrong
- **THEN** a new leaf supersedes it and names the leaf it supersedes
- **AND** the earlier leaf is neither rewritten nor removed

#### Scenario: An external witness is offered as the record

- **WHEN** a realization proposes that an external publication of chain digests be treated as the authoritative record
- **THEN** the proposal is refused, because the log is the record and any external publication is a witness to it

### Requirement: The chain names no identity, certificate or custody term of its own

This capability SHALL express holders, wallets, grants, custody, exercises and
attribution in the pinned openXwallet vocabulary; the actor behind a signature in
`identity-brokering`'s stable opaque subject; and certificates, issuance authority
and declared chain custody in `add-trust-anchor`'s vocabulary — and SHALL NOT
define a parallel term for anything one of those already names. Where tranche one
needs something none of them provides, the need SHALL be recorded as a NAMED
DEPENDENCY on the owning capability rather than respelled here, because a second
vocabulary for one concept is the "two records of one decision" defect at contract
scale.

A term this capability introduces SHALL be qualified so that it cannot be read as
another capability's term: in particular, the act of admitting a ratification to a
chain SHALL always be spelled CHAIN ENROLLMENT and never bare "enrollment", which
`worker-enrollment-broker` already owns for a worker joining a fleet.

#### Scenario: A chain record would carry its own actor identifier

- **WHEN** a chain link would name its actor by a display name, an email address, an upstream account name, or an identifier this capability invents
- **THEN** it is refused, and the broker-issued stable opaque subject is required instead

#### Scenario: A needed field has no owner

- **WHEN** a link needs a field that no composed capability provides
- **THEN** the need is recorded as a named dependency on the capability that would own it
- **AND** a local term is not minted to fill the gap

#### Scenario: A record schema owned elsewhere would need a new field

- **WHEN** a chain would require a field on a record kind published by another repository and consumed here at a pin
- **THEN** the chain record REFERENCES that record rather than extending it
- **AND** any extension is raised in the publishing repository followed by a pin bump, never authored here

#### Scenario: The act is written as bare enrollment

- **WHEN** a document of this capability calls chain enrollment simply "enrollment"
- **THEN** the wording is corrected, because a reader cannot tell which of two governed enrollments is meant

### Requirement: The ratify-and-enroll handshake is performed outside the clearance pipeline

The ratify-and-enroll handshake SHALL be performed OUTSIDE the substantive-review
clearance pipeline, by a human authority, and its record SHALL NOT be presented
as, or counted as, a clearance. The placement follows from the SURFACE the
handshake writes and not from which instrument the authority holds, so it binds
equally a wallet-carried exercise and the standing-authority origin of R1. The placement is
forced rather than preferred: codexFactory's `gate_rules_council` returned a
unanimous 5/5 refusal on 2026-08-28 of a candidate class over
`openspec/changes/**` on the ground that such a class can NEVER commission a
council — that surface lies inside the canonical `GATE_INTEGRITY_FLOOR`, which is
evaluated before any clearable classification, so every candidate parks
`parked_never_clearable` and the convening lane bails on that outcome. The finding
is code-level, not document-level: declaring the floor block, omitting it, and
supplying no rule document at all all park identically
(codexFactory
`hermes/domain/review-councils/records/2026-08-28-gate-rules-openxfactory-substantive-classes.md`,
§2; ruled at §8.2, "no class over `openspec/changes/**` under this or any adjacent
id").

Because the handshake confers no clearance, it SHALL NOT be used to admit work
that a clearance lane would otherwise judge, and a realization SHALL NOT route a
candidate around a lane by enrolling it in a chain.

#### Scenario: The handshake is proposed as a gated act

- **WHEN** a realization proposes to route the ratify-and-enroll handshake through a clearance class over the proposal surface
- **THEN** the proposal is refused with the never-convenable finding cited
- **AND** the handshake stays an out-of-pipeline act of a human authority

#### Scenario: A chain record is offered as a clearance

- **WHEN** a chain link is offered as evidence that a candidate was cleared
- **THEN** the offer is refused, because the handshake confers no clearance

#### Scenario: A chain is used to bypass a lane

- **WHEN** work that a clearance lane would judge is admitted on the strength of its chain alone
- **THEN** the admission is refused, because this capability adds a proof of descent and removes no review

### Requirement: The chain confers and refuses nothing until a named reader runs as a required check

This capability SHALL confer and refuse nothing until a NAMED validator that
reads its records runs as a REQUIRED check on the repository that holds them, and
until that check is required its records SHALL be treated as documentation that
governs nothing. No statement of this capability SHALL describe a rule inside a
validator as though the description were the enforcement, and any statement of
what the chain enforces SHALL NAME the check that enforces it; where no such check
exists, the requirement is UNMET rather than partially met. The rule is carried
here rather than inherited by implication from
`review-authority-intake`'s *"A grant with no reader in a required check confers
nothing"*, because a rule relied on by implication is a rule nobody checks.

#### Scenario: The validator exists in no required check

- **WHEN** the chain validator is present in the repository but appears in no workflow that is a required check
- **THEN** every chain record confers nothing, and the capability states so rather than asserting the chain's properties in the present tense

#### Scenario: A described control is offered as an existing one

- **WHEN** a requirement of this capability is stated as satisfied by a rule inside a validator
- **THEN** the statement MUST name the required check under which that validator executes
- **AND** where no such check exists the requirement is UNMET, not partially met

#### Scenario: The capability is promoted before any reader exists

- **WHEN** this capability's requirements reach the promoted specification and no reader is yet required anywhere
- **THEN** the capability is recorded as conferring nothing yet, with the reader named as the outstanding realization obligation
