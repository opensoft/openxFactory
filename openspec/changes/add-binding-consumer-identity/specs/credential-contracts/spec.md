# credential-contracts (delta) — add-binding-consumer-identity

THE MODIFIED BLOCK'S BASIS IS `add-notebook-hosting-credential-custody`'s
OUTCOME, not canon. That requirement is ADDED by that active ratified change and
is not yet promoted, so this delta is declared relative to its outcome per
`release-realization`'s "Ordered deltas and branch vocabulary". The body and
five of its six scenarios are carried verbatim; the sixth — "The published
binding shape cannot yet express the access identity" — is REPLACED, because
this change is the successor that packet named and its arrival is what makes
that scenario false.

## MODIFIED Requirements

### Requirement: Each consuming system reaches a shared operated identity through its own binding
Where more than one system authenticates as the SAME operated identity, each consuming system SHALL reach that identity's credential through its OWN binding: its own access identity against the secret store, its own grant, its own rotation visibility, and its own audit trail. One identity MAY be shared; one AUTHORITY SHALL NOT. A system SHALL NOT borrow another system's binding, and SHALL NOT consume the identity through a session another system established.

Per-system bindings are what make the consequential acts separable. With one shared route, revoking either system's access revokes both, the store's access log cannot say which system read the secret, and a compromise of one is indistinguishable from a compromise of the other. Each binding SHALL therefore be revocable on its own, and revoking one SHALL NOT disturb the other's ability to fetch.

THE AUTHORITY IS A RECORD FACT, NOT AN ASSERTION ABOUT THE ESTATE. Each such binding SHALL declare, in its own record, the consuming system that holds it and the identity that system USES TO AUTHENTICATE to the secret store, so that which system a binding belongs to and what its revocation reaches are READ rather than inferred. A binding that declares neither is not thereby non-conforming while the declaration is optional under the contract's own migration posture, but the per-system authority it participates in is then unproven, and a change adopting this requirement SHALL NOT describe an undeclared pair as proven.

WHAT REVOCATION REACHES, STATED HONESTLY, because a shared bearer secret bounds it. Revoking a binding stops that system's FUTURE fetches and nothing more: it cannot un-disclose a password already fetched, and it cannot terminate a session already established with it. Evicting a consumer that has already read the secret requires ROTATING it, and rotation necessarily reaches EVERY consumer of that identity — the one act per-system bindings cannot make independent. A change adopting this requirement SHALL record that cost rather than let per-system bindings read as per-system containment, and SHALL NOT claim an isolation the credential class cannot deliver. Declaring the consuming system and its fetch identity SHALL NOT be read as narrowing that limit: it makes the revocable thing nameable, not the disclosed thing recallable.

A shared ambient session SHALL NOT be used as a substitute for a second binding. This restates, for operated identities, what this capability already refuses for worker credentials: a refreshable session-state credential is the wrong class to distribute, because an ephemeral copy's refresh silently stales the master. Two systems sharing one live session is that same defect with the copy left implicit.

#### Scenario: A second system needs the same identity
- **WHEN** a second system must authenticate as an operated identity a first system already uses
- **THEN** it is given its own binding — its own access identity, grant, rotation visibility and audit trail
- **AND** it does not reuse the first system's binding or its established session

#### Scenario: One system's access is revoked
- **WHEN** one consuming system's binding is revoked
- **THEN** that system can no longer FETCH the credential, the other system's binding is unaffected, and its lane keeps working
- **AND** the revocation is attributable to exactly one system

#### Scenario: A consumer that already holds the secret must be evicted
- **WHEN** a consuming system has already fetched the shared credential, or already established a session with it, and must be evicted
- **THEN** revoking its binding is insufficient — the credential is rotated, and the rotation reaches every consumer of that identity
- **AND** that shared cost is recorded rather than described as independent revocation

#### Scenario: The access log is asked which system read the secret
- **WHEN** the secret store's access log is examined after a fetch
- **THEN** it names which consuming system's identity performed it, because each has its own

#### Scenario: The binding shape expresses the consuming system and its fetch identity
- **WHEN** two bindings for one operated identity are recorded in the promoted binding-template shape
- **THEN** each names the consuming system that holds it and the identity it fetches with, so the per-system authority is READ from the record rather than asserted by the binding's owner and its estate wiring
- **AND** what the record proves stays bounded: it states the declared authority, and reconciling that declaration against the store's actual grants remains a live-estate act this shape does not perform

#### Scenario: A shared session is proposed instead of a second binding
- **WHEN** a second system proposes to consume the identity through a session the first system established
- **THEN** it is refused as the wrong credential class, on the same grounds this capability already refuses distributing refreshable session state

## ADDED Requirements

### Requirement: A credential binding declares the consuming system that holds it and the identity it fetches with
The canonical credential schema SHALL own an ADDITIVE OPTIONAL `consumer:` block on each entry of `credential_bindings` in `xfactory_credential_binding_template`, carrying the consuming system's HOLDER REFERENCE and the FETCH IDENTITY that system USES TO AUTHENTICATE to the secret store, and the block's member set SHALL be closed IN TWO STEPS — an undeclared member warns at the introducing minor and is refused at the next major.

THE TWO IDENTIFIERS ARE VOCABULARY THIS FAMILY ALREADY USES, and a second naming
scheme SHALL NOT be introduced for either. The holder reference is the
`holder_ref` spelling the identity-brokering contract family already ships in its
`credential_reference` block; a consuming system SHALL NOT be spelled as a
persona or as a broker actor subject, because non-human identity is kept out of
the persona population and its authority comes from credential grants and wallet
holders instead. The fetch identity is the "fetch-identity identifier" this
capability's own promoted text already names as one of the two bindings a
consuming lane receives — the other being the opaque secret reference the shape
already carries.

THE BLOCK MAY ALSO CARRY a reference to the requirement the binding resolves,
and an acknowledgment that the credential is deliberately reached by more than
one consumer. The acknowledgment SHALL be a DECLARED-OR-ABSENT token whose only
valid value is true, on the same reasoning this schema already applies to
issuance preconditions: a false-valued declaration reads as governance while
asserting nothing.

THE REQUIREMENT REFERENCE SHALL BE QUALIFIED, NOT A BARE IDENTIFIER, and it
SHALL take the shape the identity-brokering family already ships for exactly
this pointer: a requirement id TOGETHER WITH the requirements document that
declares it. A bare id resolves ambiguously — this schema requires only a string
`id` on a requirement and imposes no repository-wide uniqueness, while the
canonical validator scans a whole `credentials/` tree, so one id may match
records in several documents with DIFFERENT access modes. A reference that can
match two records with different meanings is not a reference, and any rule built
on it would vary with traversal order. Where a qualified reference resolves to
ZERO or to MORE THAN ONE requirement, the reference SHALL be reported and SHALL
NOT be treated as resolved.

THE BLOCK IS OPTIONAL AND ADDITIVE AT ITS INTRODUCING RELEASE, AND THE PHASING
IS THE VERSIONING POLICY'S RATHER THAN A PREFERENCE. A binding declaring no
`consumer:` block SHALL remain valid at that release and every consumer pinned
at the prior bundle SHALL remain conformant until it upgrades; the conformance
validator SHALL emit a WARNING naming the omission, and the omission SHALL
become an ERROR only at a MAJOR release, because the policy admits a newly
required field only in the breaking class and only after a full minor release
in which the old shape produced deprecation warnings. The removal version SHALL
be stated where a consumer upgrading across it will read it.

A BLOCK-SHAPED HOLE IS NOT A FIELD. The reason the block is DECLARED rather than
left to convention is that an undeclared key on this object already validates:
the binding object is not closed, so a `consumer:` key carrying anything at all
passes the pinned schema today, unenforceable and invisible to every consumer of
that contract. Declaring the block is what gives that hole a shape.

AND CLOSING IT IS THE SAME BREAKING ACT AS REQUIRING IT, SO IT PHASES THE SAME
WAY. Because the binding object is open TODAY, a domain may already hold a
binding carrying a locally shaped `consumer:` object, and that record validates
at the current major. Refusing it the moment this block lands would NARROW a
shape the current major accepts — the breaking class, however additive the new
members look — and the compatibility direction forbids a new release
retroactively invalidating an old pin. So the closure serves the same
deprecation the requiredness does: at the introducing minor an undeclared member
WARNS and the record stays VALID; at the next major it is REFUSED. A change that
declared the members and closed them in one minor would be a breaking change
wearing an additive label, which is the failure this sequencing exists to
prevent.

Closing the BINDING OBJECT around the block is a further, separate breaking act
and SHALL NOT ride this addition at all.

A TEMPLATE IS NOT AN INSTANTIATED BINDING. An instantiation stub — the
`.template.yaml` and `.example.yaml` shapes this family already treats as stubs
rather than records — declares no consuming system because none exists yet, and
the omission warning and the major's refusal SHALL NOT apply to one. The reason
is not convenience: a stub forced to satisfy the field would satisfy it with a
placeholder, and a placeholder that passes the identifier grammar is a
declaration that reads as an authority fact while naming nothing. Scaffolding
that manufactures conformance is worse than scaffolding that omits it, because
only the second is visible.

#### Scenario: A binding declares its consumer
- **WHEN** a credential binding declares a `consumer:` block naming a holder reference and a fetch identity
- **THEN** it validates, and which consuming system holds the binding and which identity it authenticates with are facts of the record

#### Scenario: A binding declares no consumer at the introducing release
- **WHEN** a credential binding carries no `consumer:` block at the release that introduces it
- **THEN** it remains VALID and the validator emits a warning naming the omission and the release at which it becomes an error
- **AND** a consumer pinned at the prior bundle remains conformant without changing anything

#### Scenario: A binding declares no consumer at the major that requires it
- **WHEN** a credential binding carries no `consumer:` block at the major release that requires it
- **THEN** the validator MUST report an error
- **AND** that release MUST have been preceded by a full minor in which the omission produced a warning, because a required field arriving without one is a breaking change served with no deprecation

#### Scenario: The block carries a member outside its declared set, at the introducing minor
- **WHEN** a `consumer:` block declares a member the shape does not declare, at the release that introduces the block
- **THEN** the record remains VALID and the validator emits a warning naming the declared set and the release at which the member becomes an error
- **AND** it is NOT refused, because the binding object is open on the current major and a locally shaped `consumer:` object validates there — refusing it now would narrow a shape the major accepts

#### Scenario: The block carries a member outside its declared set, at the major that closes it
- **WHEN** a `consumer:` block declares an undeclared member at the major release that closes the block
- **THEN** the validator MUST report an error naming the declared set, rather than accepting a local key riding a neutral schema that neither declares nor forbids it

#### Scenario: An existing record already carries a locally shaped consumer key
- **WHEN** a domain's binding already carries a `consumer:` object of its own shaping, written while the binding object was open
- **THEN** it stays VALID across this addition and is warned rather than refused, and the migration path to the declared members is stated where a consumer upgrading across the major will read it

#### Scenario: An instantiation stub carries no consumer
- **WHEN** a `.template.yaml` or `.example.yaml` instantiation stub carries a binding with no `consumer:` block
- **THEN** neither the omission warning nor the major's refusal applies, because a stub has no consuming system to name
- **AND** a stub that satisfied the field with a grammar-passing placeholder would be WORSE, because it would read as an authority declaration while naming nothing

#### Scenario: A consuming system is offered as a persona
- **WHEN** a binding names its consuming system by a broker persona or actor-subject reference
- **THEN** the record is NON-CONFORMING, because a workload is not a persona and its authority comes from this capability's grants and from wallet holders
- **AND** the refusal is the REQUIREMENT'S rather than the validator's wherever the identifier's form does not distinguish the two — a check offered against this scenario MUST state which shapes it actually detects and MUST NOT be described as deciding the general case

#### Scenario: The consumer is a wallet-carrying governed actor
- **WHEN** the consuming system is a governed actor that carries a wallet
- **THEN** its wallet's identifier is an admissible holder reference and nothing further is required
- **AND** a wallet reference MUST NOT be made the required type of the field, because the wallet family is consumed here at a pin rather than owned, and most consumers of a credential binding carry no wallet

#### Scenario: The acknowledgment is declared false
- **WHEN** a `consumer:` block declares the shared-credential acknowledgment with the value false
- **THEN** the validator MUST report an error — the token is declared or absent, and a false value reads as governance while asserting nothing

### Requirement: Two bindings on one secret are refused unless both declare distinct consumers and both acknowledge the sharing
Two bindings in one credential binding template that share a `secret_ref` SHALL be REFUSED by default, and that refusal SHALL be lifted ONLY where every one of five conditions holds together: both bindings declare a `consumer:` block; their holder references DIFFER; their fetch identities DIFFER; both declare the shared-credential acknowledgment; and both name a QUALIFIED requirement reference — a requirement id together with the requirements document declaring it — each resolving in the repository under validation to EXACTLY ONE requirement, whose access modes are equal and are not dispatch-only.

EVERY CONDITION FAILS CLOSED. An absent block, a shared holder reference, a
shared fetch identity, a one-sided or missing acknowledgment, a requirement
reference resolving to zero or to more than one record, and a mixed or
dispatch-only access mode each leave the default refusal standing. An unreadable
precondition makes the lift UNAVAILABLE and never merely UNCHECKED, because a
check that treats what it could not read as satisfied is the fail-open shape
this family has already had to repair once.

AMBIGUITY IS UNREADABILITY, AND IS TREATED AS SUCH. A bare requirement id cannot
carry this condition: the schema requires only a string `id` on a requirement,
imposes no repository-wide uniqueness, and the canonical validator scans a whole
`credentials/` tree, so one id may match records in several documents whose
access modes DIFFER. An implementation resolving a bare id could select a
non-dispatch match and lift the refusal while a dispatch-only match stood beside
it, and which one it found would depend on traversal order. The reference is
therefore QUALIFIED by its requirements document, on the shape the
identity-brokering family already ships for this pointer, and a reference
matching zero or more than one record SHALL be reported and SHALL NOT be treated
as resolved.

THE FIFTH CONDITION IS WHAT KEEPS THE ORIGINAL RULE INTACT, and it exists
because the lift would otherwise be the laundering route for the exact fault the
rule was built to refuse. This capability already forbids a dispatch-only
credential and a content-write credential collapsing into one identity; without
a resolvable requirement on both sides, a pair could declare that collapse to be
deliberate sharing and buy its way past. The requirement reference is therefore
REQUIRED FOR THE LIFT even though it is optional on the block, and it SHALL NOT
be inferred from the binding's map key: the key is a requirement id by
convention only, the shape enforces no key grammar, and a safety precondition
resting on an unenforced convention is not a precondition.

AND IT OVER-REFUSES DELIBERATELY. Excluding dispatch-only on both
sides means two consumers of ONE dispatch-only credential are refused too, which
nothing else in this capability forbids. That is a chosen conservatism, not an
oversight: the dispatch class is where serving-tier separation lives, and a rule
that refuses a shape no consumer currently needs is cheaper to relax on evidence
than a rule that admits one nobody checked. Relaxing it SHALL be a separate act
carrying its own case.

A REFUSAL SHALL NAME THE FAULT IT FOUND, AND NAME IT ONCE. Two bindings on one
secret whose FETCH IDENTITIES are the same SHALL be refused under a distinct
finding that names two systems sharing one authority, rather than under the
finding about two credentials collapsing into one. They are different faults
with different remedies, and a reader told about the wrong one repairs the wrong
thing. Where the distinct finding applies it REPLACES the default finding for
that pair rather than accompanying it: one fault SHALL produce one finding, or a
reader repairing the named fault is left with a second refusal describing the
same record.

THE COMPARISON IS WITHIN ONE RECORD. These conditions are evaluated across the
bindings of a single template by a validator that reads one repository, and
SHALL NOT be claimed to compare bindings held in different repositories. Where
an operated identity's consumers are declared in separate repositories — which
the residency model makes the ordinary case — the declaration is what makes the
authority readable at each site, and reconciling the sites is an estate-level
act this requirement does not perform.

#### Scenario: Two consuming systems reach one operated identity
- **WHEN** two bindings share a `secret_ref`, declare different holder references and different fetch identities, both declare the shared-credential acknowledgment, and both name requirements of the same non-dispatch access mode
- **THEN** the record validates, and it states two consumers of one deliberately shared credential rather than two credentials collapsed into one

#### Scenario: Two bindings on one secret share a fetch identity
- **WHEN** two bindings share a `secret_ref` and declare the same fetch identity
- **THEN** they MUST be rejected under a finding naming two systems on one authority, because one identity may be shared and one authority may not
- **AND** the finding MUST NOT be the one about two credentials collapsing into one, which would send the reader to the wrong repair

#### Scenario: One binding acknowledges the sharing and the other does not
- **WHEN** two bindings share a `secret_ref` and only one declares the shared-credential acknowledgment
- **THEN** the default refusal stands, because a one-sided declaration exempts a pair on one party's word

#### Scenario: A dispatch credential and a content credential declare themselves shared
- **WHEN** two bindings share a `secret_ref` and name requirements whose access modes differ, one of them dispatch-only
- **THEN** they MUST be rejected however they are declared, because the serving tier would hold key material capable of minting a content-write token and no acknowledgment can make that intentional

#### Scenario: The requirement reference cannot be resolved
- **WHEN** two bindings share a `secret_ref` and a named requirement reference resolves to nothing in the repository under validation
- **THEN** the lift is UNAVAILABLE and the default refusal stands
- **AND** the unresolvable reference is reported rather than treated as an absent condition that happens not to fail

#### Scenario: The requirement reference resolves to more than one record
- **WHEN** a named requirement reference matches requirement records in more than one document, or more than one record in a document
- **THEN** the lift is UNAVAILABLE and the ambiguity is reported, exactly as a reference resolving to nothing is
- **AND** an implementation MUST NOT resolve the ambiguity by picking one — the two matches may carry different access modes, and a rule whose outcome depends on which was found first is not a rule

#### Scenario: A bare requirement id is offered instead of a qualified reference
- **WHEN** a `consumer:` block names a requirement by id alone, with no requirements document
- **THEN** the reference does not satisfy the lift's condition, because a bare id is not unique in the tree the validator scans

#### Scenario: Two bindings share a secret and declare nothing
- **WHEN** two bindings share a `secret_ref` and neither declares a `consumer:` block
- **THEN** the existing refusal fires exactly as it does today, because this change tightens before it lifts and nothing that is refused today becomes accepted by silence

### Requirement: A declared consumer makes access revocation readable and does not make a bearer secret unshared
A consuming system's declaration on a binding SHALL be treated as establishing WHICH ACCESS is revoked and WHOSE FUTURE FETCHES stop, and SHALL NOT be treated as establishing containment of a credential a consumer has already obtained.

WHAT IT BUYS, precisely. With the consuming system and its fetch identity on the
record, an eviction decision resolves to a named grant at the secret store, its
effect is bounded to one consumer's future fetches, and the store's access log
becomes reconcilable against a declaration rather than against an assumption.
Before it, the same decision is an inference from estate wiring that no record
carries.

WHAT IT DOES NOT BUY, and this SHALL be stated by any change or document that
adopts the field. The credential is a shared BEARER secret. Revoking a fetch
identity's grant cannot un-disclose a value already read, cannot end a session
already established with it, and cannot prevent a consumer that copied it from
continuing to use it elsewhere. Evicting such a consumer still requires
ROTATION, and rotation still reaches every consumer of the identity. A record
that names consumers describes the authority structure; it does not change the
credential class.

THE FIELD SHALL NOT BE OFFERED AS EVIDENCE OF AN ENFORCED GRANT. A declared
fetch identity states what the binding's owner says the store's grant is. Where
the declaration and the store disagree, the store governs, and detecting that
disagreement is a live-estate reconciliation with its own home — the same
posture this family already takes for observed-versus-declared identity drift.

#### Scenario: A consumer must be denied further access
- **WHEN** an operator must stop one consuming system fetching a shared operated identity's credential
- **THEN** the binding's declared fetch identity names the grant to revoke and the revocation's reach is bounded to that consumer's future fetches
- **AND** the other consumers' bindings are undisturbed

#### Scenario: A consumer that already holds the secret must be evicted
- **WHEN** the consumer to be evicted has already fetched the credential or established a session with it
- **THEN** revocation is insufficient and the credential is rotated, reaching every consumer
- **AND** the declared consumer field MUST NOT be presented as having made that eviction independent

#### Scenario: The declaration and the store disagree
- **WHEN** a binding declares a fetch identity that holds no matching grant at the secret store, or the store grants access to an identity no binding declares
- **THEN** the store's actual grants govern, and the divergence is a reconciliation finding rather than a validation pass
- **AND** the schema-level check MUST NOT be described as having verified the grant

#### Scenario: An adopting document describes the field
- **WHEN** a change, runbook or contract document adopts the consumer field
- **THEN** it states both halves — revocation of access becomes readable, and a bearer secret already fetched stays shared until rotation
- **AND** a description carrying only the first half is non-conforming, because the omission is what turns a readability gain into a containment claim
