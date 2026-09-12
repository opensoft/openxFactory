# review-authority-intake Specification

**DELTA CLASS: `## ADDED`, AND THE CHOICE IS FORCED RATHER THAN PREFERRED.**
This capability has **no promoted specification** — `openspec/specs/` carries no
`review-authority-intake/spec.md`, because the two changes that author it,
`add-wallet-carried-review-authority` (ratified 2026-08-23) and
`register-gate-rules-council-seats` (ratified 2026-09-06), are both ACTIVE and
neither has archived. There is therefore no requirement here to `## MODIFIED`:
the direction these seven requirements encode is not in canon, it is in a
ratified RULINGS RECORD
(`add-wallet-carried-review-authority/rulings-2026-08-29.md` § Packet 4) that
says of itself that none of it is enforced. These requirements are ADDED, they
promote at THIS change's archive, and `proposal.md` § "Open questions" OQ-1
states the consequence rather than leaving it to be inferred.

**ONE REQUIREMENT PER RULING, R6 THROUGH R12, IN THAT ORDER.** Every requirement
below carries the ruling it encodes by identifier, so a reader can hold the
requirement against the ruling's verbatim text in `proposal.md` and see that
nothing was extended, narrowed or invented.

## ADDED Requirements

### Requirement: A holder composition's model component digests the provider plane together with the exact published identifier
A holder composition's `model_version` component SHALL digest the PROVIDER PLANE
together with the exact published model identifier, and a composition that
digests the identifier alone SHALL be REFUSED as under-specified.

**THE PLANE SITS INSIDE THE DIGEST BECAUSE A PIN IS A PAIR** (R6). The same
immutable model does not carry the same string across planes, so an identifier
without its plane names a model only by accident of which plane the reader
happened to assume. Two holders pinned to "the same model" on different planes
are not pinned to the same thing, and a digest that cannot tell them apart
cannot detect the drift between them.

**EXECUTION AND DEPLOYMENT IDENTITY STAYS OUTSIDE THE COMPOSITION.** Account,
region, deployment, endpoint and authentication SHALL NOT be members of the
composition digest; they SHALL be carried by REFERENCE to the operator evidence
record that establishes the plane. This keeps the DRIFT blast radius where it
belongs: a region move or a credential rotation is not a composition change and
MUST NOT revoke a grant, while a plane change is one and MUST.

**GENERATION PARAMETERS ARE NOT THE MODEL.** Effort, reasoning and thinking
settings SHALL be carried under the Parameters component and SHALL NOT be
members of `model_version`.

**THIS REQUIREMENT BINDS PROSPECTIVELY** (`proposal.md` OQ-4). It governs
compositions declared or re-declared after its realization; it does not by
itself re-derive a composition digest an already-issued grant was bound to, and
it therefore revokes nothing on the day it lands.

#### Scenario: A composition declares an identifier with no plane
- **WHEN** a holder composition's `model_version` component names an exact published model identifier and does not name the provider plane
- **THEN** the composition is REFUSED as under-specified
- **AND** the refusal names the missing plane rather than reporting a digest mismatch, because nothing has yet been mis-computed

#### Scenario: The plane changes and the identifier does not
- **WHEN** a holder's exact published model identifier is unchanged and the provider plane it is served on changes
- **THEN** the composition digest changes, the holder's composition is CHANGED, and the shipped drift cascade applies to it as to any other composition change
- **AND** a new operator evidence record is required for the new plane, because a plane change is a new Operator record

#### Scenario: A deployment detail moves
- **WHEN** the account, region, deployment, endpoint or authentication binding moves and the plane and identifier do not
- **THEN** the composition digest does NOT change and no grant is revoked by that movement
- **AND** the change is recorded in the referenced operator evidence record rather than inside the composition

#### Scenario: A generation parameter is offered as part of the model component
- **WHEN** an effort, reasoning or thinking setting is declared inside `model_version`
- **THEN** the composition is REFUSED
- **AND** the refusal names the Parameters component as the member's home

### Requirement: One digest construction governs a holder composition, and it is the estate's existing one
A holder composition's digest SHALL be computed under the estate's canonical
JSON construction `xfc-jcs-sha256-1` — RFC 8785 JSON Canonicalization Scheme,
SHA-256, rendered `sha256:` plus 64 lowercase hexadecimal characters — taken by
reference to
`contracts/signed-execution-chain/digest-construction.schema.yaml`, and this
capability SHALL NOT declare a second construction beside it.

**THE CONSTRUCTION IS ADOPTED, NOT RE-DECLARED, AND THE ROUTE IS THE ONE THAT
FILE SANCTIONS IN WRITING** (R7). Realizing this requirement requires the holder
composition to be admitted as a SUBJECT of that construction's closed
`digest_subject` enumeration — a widening of SUBJECTS, never a second
construction. **Until that subject exists, this requirement is UNREALIZABLE as
written and SHALL NOT be reported as satisfied**, which is the same sentence
`add-cpc-clearing-boundary` wrote when it took the identical route from a
different capability.

**THE SUBJECT IS NAMED, BECAUSE READERS THAT AGREE ON HOW TO HASH CAN STILL
DISAGREE ON WHAT WAS HASHED.** The digest is taken over the DECLARED
COMPOSITION and over nothing else: not over the grant that cites it, not over
the register row that points at the grant, and not over the candidate
repository the holder reviews.

**THE PROFILE NAME AND ITS VERSION ARE RECORDED WITH EVERY VALUE**, and every
digest is ALGORITHM-TAGGED. **NO DIGEST-AGILITY MECHANISM AND NO DUAL-DIGEST
TRANSITION IS MINTED HERE** (`proposal.md` OQ-3): R7 assigned both to the
carrying change, and the carrying change decides that tagging plus a recorded
profile name and version is what makes a later migration a readable change,
while a transition mechanism with no second algorithm to transition to is a
widening nothing exercises. This is DECIDED, not overlooked.

#### Scenario: A composition digest is computed under another serialization
- **WHEN** a reader computes a holder composition digest under a serialization other than `xfc-jcs-sha256-1`
- **THEN** the value does not match and the composition is REFUSED
- **AND** the disagreement is reported as a construction mismatch rather than as composition drift, because nothing about the holder has changed

#### Scenario: A second construction is declared for compositions
- **WHEN** a realization declares a canonicalization profile for holder compositions beside `xfc-jcs-sha256-1`
- **THEN** it is REFUSED, whatever it is called, because one estate with two JCS profiles has no rule obliging them to agree

#### Scenario: The composition subject has not been admitted yet
- **WHEN** the construction's `digest_subject` enumeration does not yet carry the holder-composition subject
- **THEN** this requirement is reported as UNREALIZED rather than satisfied
- **AND** no composition digest computed outside the enumeration is admitted in the meantime

#### Scenario: A composition digest is carried untagged or unprofiled
- **WHEN** a record carries a composition digest with no algorithm tag, or without the canonicalization profile name and version
- **THEN** it is REFUSED, because an untagged or unprofiled digest cannot be migrated without silently changing meaning

### Requirement: A re-issuance act records five fields as a MINIMUM, and the floor is not a ceiling
A re-issuance act SHALL record at least the superseding grant reference, the
superseded grant reference, the composition hash it was issued against, the
ratifying human, and the effective time; a re-issuance record missing any of
the five SHALL be REFUSED.

**THESE FIVE ARE A FLOOR A LATER CHANGE MAY EXTEND, AND NOT A CEILING** (R8).
A record carrying further fields is conforming; a record carrying fewer is not.
**This change exercises no extension**: the five stand exactly as ruled, no
sixth field is minted here, and the permission to extend is recorded so that a
later change need not re-argue it.

**THE COMPOSITION HASH IS THE ONE THAT WAS ISSUED AGAINST, NOT THE ONE CURRENT
AT READ TIME.** A re-issuance record that names a composition the grant was not
issued against records a different act than the one performed.

#### Scenario: A re-issuance omits the superseded grant
- **WHEN** a re-issuance record names the superseding grant and does not name the grant it supersedes
- **THEN** the record is REFUSED, because a supersession with one end cannot be walked back to its predecessor

#### Scenario: A re-issuance records no ratifying human
- **WHEN** a re-issuance record carries no ratifying human
- **THEN** the record is REFUSED, because re-issuance is always an explicit human-ratified register act

#### Scenario: A re-issuance carries more than the five
- **WHEN** a re-issuance record carries the five required fields and further fields beside them
- **THEN** it is ADMITTED, because the five are a minimum and not a ceiling

### Requirement: A revoked holder parks the convening, and only a new human-ratified issuance resumes it
An exercise that detects a composition mismatch for a holder SHALL PARK the
convening with a NAMED refusal, and SHALL NOT honor an earlier admission stamp;
there is NO grandfathering.

**A PARKED CONVENING RESUMES ONLY UNDER A NEW HUMAN-RATIFIED ISSUANCE ACT** —
never by the runtime, never by elapsed time, and never by a retry (R9). Elapsed
time is the mechanism that most resembles a fix and repairs nothing: the
composition that mismatched is still the composition that mismatched.

**THE REFUSAL IS NAMED RATHER THAN GENERIC**, so an operator reading it can
tell a composition mismatch from an unreadable register, a stale projection or
an expired row — four different conditions with four different remedies, and a
single refusal code for all of them sends the operator to the wrong one.

#### Scenario: An admitted convening reaches an exercise after its holder is revoked
- **WHEN** a convening was admitted before the holder's grant was revoked and reaches the exercise afterwards
- **THEN** the convening PARKS with a named refusal and the earlier admission stamp is not honored
- **AND** no verdict is produced, because a verdict produced under revoked authority is not weakened by being nearly in time

#### Scenario: A parked convening is retried
- **WHEN** a parked convening is retried, or waited out, with no new issuance act performed
- **THEN** it PARKS again on the same named refusal
- **AND** the runtime performs no act that would resume it

#### Scenario: A new issuance is ratified
- **WHEN** a human ratifies a new issuance act against the holder's current composition
- **THEN** the parked convening may resume under that issuance
- **AND** the resumption names the issuance act it resumed under

### Requirement: Retrieval-corpus drift invalidates on identity or governing configuration, never on rows
A change to a retrieval corpus's IDENTITY or GOVERNING CONFIGURATION digest SHALL invalidate the composition,
and a row-level content change inside the same governed corpus SHALL NOT, by
itself, invalidate it.

**THE GOVERNING CONFIGURATION'S MEMBERS ARE REQUIRED AND NOT CLOSED**
(`proposal.md` OQ-9). Scope, selection configuration, admission policy and the
ontology package digest SHALL each be members of the governing configuration
digest, and a governed corpus MAY declare further members that likewise
invalidate. Reading the four as a closed set would let a corpus add a new
governing knob that silently never invalidates, which is the failure this rule
exists to refuse.

**THE BINDING IS TO THE PINNED SEAT PROMPT AND THE PINNED ONTOLOGY PACKAGE, AND
NEVER TO THE CANDIDATE REPOSITORY AT HEAD** (R10). A composition bound to a
moving HEAD would invalidate on every merge into the repository under review,
which is every repository the holder exists to review.

#### Scenario: A row's content changes inside a governed corpus
- **WHEN** the content of a row inside the pinned governed corpus changes, and corpus identity and governing configuration do not
- **THEN** the composition is NOT invalidated and no grant is revoked by that change

#### Scenario: The admission policy changes
- **WHEN** the corpus's admission policy, scope, selection configuration or ontology package digest changes
- **THEN** the governing configuration digest changes, the composition is INVALIDATED, and the drift cascade applies

#### Scenario: A corpus declares a further governing member
- **WHEN** a governed corpus declares a governing-configuration member beyond the four required ones and that member changes
- **THEN** the composition is INVALIDATED, because the four are required members and not a closed set

#### Scenario: The candidate repository advances
- **WHEN** the candidate repository under review advances its HEAD
- **THEN** the composition is NOT invalidated, because the binding is to the pinned seat prompt and pinned ontology package and never to that HEAD

### Requirement: Register is the only human-ratified act in the lifecycle, revoke waits on no human, and re-issue always requires one
The holder-composition lifecycle SHALL be `propose → approve → attest →
register → activate → revoke`, and REGISTER SHALL be the ONLY act in it that
requires human ratification.

**REVOKE REQUIRES NO HUMAN, AND THAT IS THE POINT OF A FAIL-CLOSED CASCADE**
(R11). A cascade that waits on a human is open for exactly as long as the human
is asleep, which is the window the cascade exists to close. Revocation is
therefore performable without a ratifying act and SHALL NOT be blocked on one.

**RE-ISSUANCE ALWAYS REQUIRES A HUMAN**, consistent with the 2026-08-26 Q8(a)
ruling that re-issuance is always an explicit register act. Revocation removes
authority and re-issuance confers it, and only the conferring direction needs a
human in it.

#### Scenario: A composition change is detected with no human available
- **WHEN** a composition change is detected and no human is available to ratify anything
- **THEN** the affected grant is REVOKED anyway, because revoke waits on no human
- **AND** the holder's convenings park until a new issuance is ratified

#### Scenario: A runtime attempts to re-issue
- **WHEN** any non-human actor attempts to perform a re-issuance
- **THEN** it is REFUSED, because re-issue always requires a human-ratified register act

#### Scenario: An act other than register claims human ratification as its gate
- **WHEN** a realization makes propose, approve, attest or activate conditional on a human ratification act
- **THEN** it is REFUSED as a second human gate, because register is the only human-ratified act in the lifecycle

### Requirement: An unsigned composition digest is admissible in the interim, and a holder MUST NOT attest its own composition
A composition digest MAY be recorded UNSIGNED in the register in the interim, and activation SHALL stay fail-closed on digest match regardless,
and a holder's own keys SHALL NOT be used to attest that holder's own
composition.

**THE DEFERRAL NARROWS WHAT IS CLAIMED RATHER THAN OPENING A WINDOW** (R12).
Admitting an unsigned digest removes the SIGNATURE and keeps the MATCH: an
unsigned digest that does not match still refuses activation, so the interim
state is weaker in what it can prove about WHO recorded the value and not in
what it enforces about WHICH value is in force.

**SELF-ATTESTATION IS REFUSED BECAUSE IT ATTESTS NOTHING AN INDEPENDENT PARTY
CAN RELY ON.** The per-seat Ed25519 keys minted 2026-08-28 are named in the
ruling as the keys this refusal covers, and a holder signing its own
composition is the holder asserting its own compliance with its own signature.

**THE SIGNER AND ENVELOPE ARE DEFERRED, BY NAME, TO `signed-execution-chain`.**
The envelope standard, key distribution, signature algorithm and
evidence-retention location are NOT decided here and SHALL NOT be inferred from
this requirement's silence.

#### Scenario: An unsigned composition digest is presented
- **WHEN** the register carries a composition digest with no attestation signature
- **THEN** it is ADMITTED in the interim, and activation still requires the digest to MATCH

#### Scenario: An unsigned digest does not match
- **WHEN** an unsigned composition digest does not match the holder's declared composition
- **THEN** activation is REFUSED fail-closed, because the deferral removed the signature and not the match

#### Scenario: A holder signs its own composition
- **WHEN** a composition attestation is presented that is signed by a key belonging to the holder it describes
- **THEN** it is REFUSED as self-attestation, and the record is treated as unsigned rather than as attested

#### Scenario: An envelope question is answered from this capability's silence
- **WHEN** a realization infers an envelope standard, key distribution scheme, signature algorithm or evidence-retention location from this requirement
- **THEN** the inference is REFUSED, because those questions travel with `signed-execution-chain` and are not decided here
