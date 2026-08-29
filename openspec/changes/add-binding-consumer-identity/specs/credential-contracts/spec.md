# credential-contracts (delta) — add-binding-consumer-identity

THE MODIFIED BLOCK'S BASIS IS `add-notebook-hosting-credential-custody`'s
OUTCOME, not canon. That requirement is ADDED by that active ratified change and
is not yet promoted, so this delta is declared relative to its outcome per
`release-realization`'s "Ordered deltas and branch vocabulary" — a citation
whose antecedent is *"already MODIFIED"* while the custody change ADDS, so it
is an EXTENSION of that rule to a shape no promoted requirement reaches, not an
application of it (LA-A3).

THE CARRIAGE, STATED AS MEASURED RATHER THAN AS SUMMARISED (LQ-A1). **ALL SIX**
scenarios are carried: five byte-identical, and the sixth — "The published
binding shape cannot yet express the access identity" — REPLACED, because this
change is the successor that packet named and its arrival is what makes that
scenario false. The body is carried IN FULL **with two additions, both named**:
a new paragraph ("THE AUTHORITY IS A RECORD FACT…") and one sentence appended to
the WHAT-REVOCATION-REACHES paragraph, which is otherwise a strict prefix of its
successor. Nothing is dropped. The earlier wording of this note said "the body
… carried verbatim", which the diff contradicts; the correction is recorded
because in the lossy-delta class the phrase "carried verbatim" is the sentence
that stops the next auditor looking.

## MODIFIED Requirements

### Requirement: Each consuming system reaches a shared operated identity through its own binding
Where more than one system authenticates as the SAME operated identity, each consuming system SHALL reach that identity's credential through its OWN binding: its own access identity against the secret store, its own grant, its own rotation visibility, and its own audit trail. One identity MAY be shared; one AUTHORITY SHALL NOT. A system SHALL NOT borrow another system's binding, and SHALL NOT consume the identity through a session another system established.

Per-system bindings are what make the consequential acts separable. With one shared route, revoking either system's access revokes both, the store's access log cannot say which system read the secret, and a compromise of one is indistinguishable from a compromise of the other. Each binding SHALL therefore be revocable on its own, and revoking one SHALL NOT disturb the other's ability to fetch.

THE AUTHORITY IS A RECORD FACT, NOT AN ASSERTION ABOUT THE ESTATE. Each such binding SHALL declare, in its own record, the consuming system that holds it and the identity that system USES TO AUTHENTICATE to the secret store, so that which system a binding belongs to and what its revocation reaches are READ rather than inferred. A binding that declares neither is not thereby non-conforming while the declaration is optional under the contract's own migration posture, but the per-system authority it participates in is then unproven, and a change adopting this requirement SHALL NOT describe an undeclared pair as proven. THAT LAST OBLIGATION IS THE REQUIREMENT'S AND NOT A CHECKER'S: whether a document "describes a pair as proven" is a judgment over prose, so any check offered against it MUST state which shapes it actually detects and MUST NOT be described as deciding the general case.

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
The canonical credential schema SHALL own an ADDITIVE OPTIONAL `consumer:` block on each entry of `credential_bindings` in `xfactory_credential_binding_template`, carrying the consuming system's HOLDER REFERENCE and the FETCH IDENTITY that system USES TO AUTHENTICATE to the secret store — and the block SHALL be DECLARED AT THE INTRODUCING MINOR AND CONSTRAINED AT THE MAJOR: at the minor the schema imposes no type, no member grammar, no requiredness and no closure on it, and every one of those arrives together at the next major.

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

THE BLOCK MAY ALSO CARRY a reference to the requirement the binding resolves, an
acknowledgment that the credential is deliberately reached by more than one
consumer, and a declaration that the record is an instantiation stub. The
acknowledgment and the stub declaration SHALL each be a DECLARED-OR-ABSENT token
whose only valid value is true, on the same reasoning this schema already applies
to issuance preconditions: a false-valued declaration reads as governance while
asserting nothing.

THE REQUIREMENT REFERENCE SHALL BE QUALIFIED, NOT A BARE IDENTIFIER, and it
SHALL take the shape the identity-brokering family already ships for this
pointer: a requirement id TOGETHER WITH the requirements document that declares
it. A bare id resolves ambiguously — this schema requires only a string `id` on a
requirement and imposes no repository-wide uniqueness, while the canonical
validator scans a whole `credentials/` tree, so one id may match records in
several documents with DIFFERENT access modes.

AND THE DOCUMENT REFERENCE SHALL CARRY A GRAMMAR AND A RESOLUTION RULE, because
the shape it borrows carries neither. In identity-brokering
`requirements_document_ref` is an unconstrained string that no script and no test
resolves; promoting it to a resolution input feeding a security precondition
without a grammar would rest that precondition on an unenforced convention —
which is the very objection this requirement raises against the map key. So:
the reference SHALL be a REPOSITORY-RELATIVE path to a YAML document, SHALL NOT
be absolute, SHALL NOT traverse upward, and SHALL NOT carry a foreign-repository
prefix; it SHALL resolve ONLY against `xfactory_credential_requirements` records
the validator itself discovered and schema-checked in the scanned tree; and the
validator SHALL NEVER OPEN A PATH TAKEN FROM A RECORD. A reference that is
ungrammatical, that names a repository other than the one under validation, or
that resolves to zero or to more than one requirement SHALL be reported and SHALL
NOT be treated as resolved.

THE PHASING IS THE VERSIONING POLICY'S RATHER THAN A PREFERENCE, AND IT COVERS
EVERY NARROWING VECTOR RATHER THAN ONE OF THEM. The binding object is OPEN on the
current major, so a `consumer:` key of any shape validates today. Three distinct
acts would each refuse a shape the current major accepts — requiring members
within the block, closing the block's member set, and imposing a grammar on the
members' values — and each is therefore the BREAKING class however additive the
new vocabulary looks. All three SHALL land together at the next MAJOR. At the
introducing minor the conformance validator SHALL emit WARNINGS instead —
naming a DISTINCT finding for EVERY shape the major will refuse, and every such
record SHALL REMAIN VALID. The set is ENUMERATED against the refusals rather than
summarised, and the enumeration is the requirement: a binding that declares no
block; a block that EXISTS but omits either identifier; a block carrying an
undeclared member; a member whose value does not match the identifier grammar; a
const-true token declared false; a `credential_bindings` MAP KEY outside the key
grammar; an `access_mode` outside the closed vocabulary; and a
`requirements_document_ref` outside the path grammar. **A WARNING SET THAT LEAVES
ANY REFUSED-AT-THE-MAJOR SHAPE UNWARNED DOES NOT SERVE THE DEPRECATION THE MAJOR
DEPENDS ON**, and the shapes that go missing are the ones no single arm happens
to look at — a block present but empty matches none of the first four, and a
constraint written on a neighbouring record matches none of them at all.

THE SAME PHASING GOVERNS EVERY NARROWING THIS CHANGE INTRODUCES, WHEREVER IT
SITS — on the block, on the map that holds the block, or on a neighbouring
record. Constraining the map key, closing `access_mode`, and constraining
`requirements_document_ref` each refuse a value the current major accepts, so
each warns at the minor and is enforced only at the major. **None is exempt for
sitting outside the block, and none is exempt for being a validator rule rather
than a schema rule**: the test is whether the current major accepts the value,
not where the refusal is written. The removal version SHALL be stated where a consumer
upgrading across it will read it, and it SHALL name EVERY act that lands there
rather than only the first.

A BLOCK-SHAPED HOLE IS NOT A FIELD, and DECLARING it is what this minor does.
The reason the block is declared rather than left to convention is that an
undeclared key on this object already validates: the binding object is not
closed, so a `consumer:` key carrying anything at all passes the pinned schema
today, unenforceable and invisible to every consumer of that contract. Declaring
it — as a named, described property of the pinned contract — gives the hole a
name, a meaning and a warning. CONSTRAINING it is the breaking half, and it waits
for the major. Closing the BINDING OBJECT around the block is a further, separate
breaking act and SHALL NOT ride either release.

A TEMPLATE IS NOT AN INSTANTIATED BINDING, AND ITS EXEMPTION SHALL BE A DECLARED
TOKEN RATHER THAN A FILENAME. An instantiation stub declares no consuming system
because none exists yet, and neither the omission warning nor the major's
requiredness SHALL apply to one. But the exemption SHALL be keyed on a
declared-or-absent const-true token IN THE RECORD, never on a `*.template.yaml`
or `*.example.yaml` path: a filename-keyed exemption is one the author writes by
naming, invisible in the bytes a pinned consumer validates, and it would let a
record carrying live values escape a required field by what it is called. The
declared token is also the only form that can reach the layer where the refusal
lands — a filename is invisible to a pinned schema, while a token is a property
the schema can condition on, so the exemption holds at the major as well as at
the minor. A stub SHALL NOT satisfy the field with a placeholder instead: a
grammar-passing sentinel reads as an authority declaration while naming nothing,
and scaffolding that manufactures conformance is worse than scaffolding that
omits it, because only the second is visible.

#### Scenario: A binding declares its consumer
- **WHEN** a credential binding declares a `consumer:` block naming a holder reference and a fetch identity
- **THEN** it validates, and which consuming system holds the binding and which identity it authenticates with are facts of the record

#### Scenario: A binding declares no consumer at the introducing minor
- **WHEN** a credential binding carries no `consumer:` block at the release that introduces it
- **THEN** it remains VALID and the validator emits a warning naming the omission and the release at which it becomes an error
- **AND** a consumer pinned at the prior bundle remains conformant without changing anything

#### Scenario: An existing record already carries a locally shaped consumer key
- **WHEN** a domain's binding already carries a `consumer:` value of its own shaping — an object with neither declared member, a scalar, or a list — written while the binding object was open
- **THEN** it stays VALID at the introducing minor and is warned rather than refused, in EVERY one of those shapes, because the schema constrains nothing about the block at that release
- **AND** the migration path is stated where a consumer upgrading across the major will read it

#### Scenario: A member's value does not match the identifier grammar, at the minor
- **WHEN** a `consumer:` block at the introducing minor carries a `holder_ref` or `fetch_identity` whose value does not match the identifier grammar
- **THEN** the record remains VALID and the validator warns, because imposing the grammar is one of the three breaking acts deferred to the major
- **AND** a release that imposed the grammar while declaring the block additive would be a narrowing wearing an additive label

#### Scenario: A consumer block is present but declares neither identifier
- **WHEN** a binding carries a `consumer:` block that exists and omits `holder_ref` or `fetch_identity`, at the introducing minor
- **THEN** it remains VALID and the validator emits its OWN warning for that shape, distinct from the no-block warning
- **AND** a warning set in which this shape matches nothing MUST be treated as incomplete, because it is refused at the major and would otherwise cross the whole minor unwarned

#### Scenario: The block is constrained at the major
- **WHEN** the major release that constrains the block is validated against
- **THEN** a `consumer:` value that is not an object, a block missing either identifier, a block carrying an undeclared member, and a member failing the identifier grammar are each an ERROR
- **AND** that release MUST have been preceded by a full minor in which every one of those produced a warning, because a required field or a narrowed shape arriving without one is a breaking change served with no deprecation

#### Scenario: A binding key does not match the grammar the lift depends on
- **WHEN** a `credential_bindings` map key does not match the identifier grammar
- **THEN** it WARNS at the introducing minor and remains VALID, and is refused only at the major — the map accepts arbitrary keys today, so constraining it is a narrowing like any other and is not exempt for sitting outside the block
- **AND** the lift's binding-link condition still holds at the minor, because it compares the reference's id to the key as a string and needs no grammar to do so

#### Scenario: A consuming system is offered as a persona
- **WHEN** a binding names its consuming system by a broker persona or actor-subject reference
- **THEN** the record is NON-CONFORMING, because a workload is not a persona and its authority comes from this capability's grants and from wallet holders
- **AND** the refusal is the REQUIREMENT'S rather than the validator's wherever the identifier's form does not distinguish the two — a check offered against this scenario MUST state which shapes it actually detects and MUST NOT be described as deciding the general case

#### Scenario: The consumer is a wallet-carrying governed actor
- **WHEN** the consuming system is a governed actor that carries a wallet
- **THEN** its wallet's identifier is an admissible holder reference and nothing further is required
- **AND** a wallet reference MUST NOT be made the required type of the field, because the wallet family is consumed here at a pin rather than owned, and most consumers of a credential binding carry no wallet

#### Scenario: A const-true token is declared false
- **WHEN** a `consumer:` block declares the shared-credential acknowledgment, or the instantiation-stub token, with the value false
- **THEN** it WARNS at the introducing minor and remains VALID, and is refused at the major — a false-valued token reads as governance while asserting nothing, but the binding object is open today so `{shared_credential_acknowledged: false}` validates on the current major and refusing it in a minor would narrow like any other act
- **AND** the lift is UNAVAILABLE to a pair carrying a false-valued acknowledgment at either release, because the lift requires the token DECLARED TRUE and a false value is not a declaration — withholding a lift is not the same act as refusing a record

#### Scenario: An instantiation stub declares itself
- **WHEN** a record that is an instantiation stub carries the const-true stub token and no identifiers
- **THEN** neither the omission warning nor the major's requiredness applies to it, and it validates at both releases
- **AND** a record carrying LIVE values MUST NOT declare the token, and a `*.template.yaml` filename alone MUST NOT exempt anything

#### Scenario: A document reference escapes the tree under validation
- **WHEN** a `requirement_ref` names a document reference that is absolute, that traverses upward, or that carries a foreign-repository prefix
- **THEN** it is ungrammatical, it is reported, and it is NOT treated as resolved
- **AND** the validator MUST NOT open the path — resolution is against records the validator itself discovered in the scanned tree, never against a path a record supplies

### Requirement: Two bindings on one secret are refused unless every pair declares distinct consumers, acknowledges the sharing, and names a requirement bound to the binding
Bindings in one credential binding template that share a `secret_ref` SHALL be REFUSED by default, and that refusal SHALL be lifted ONLY where every one of six conditions holds together, OVER EVERY PAIR that shares that reference: both bindings declare a `consumer:` block; their holder references DIFFER; their fetch identities DIFFER; both declare the shared-credential acknowledgment; both name a QUALIFIED requirement reference resolving, in the repository under validation, to EXACTLY ONE requirement whose ACCESS MODE IS A MEMBER OF THE DECLARED VOCABULARY, equal across the pair and not dispatch-only; and each reference's `requirement_id` EQUALS THE MAP KEY of the binding that carries it.

THE SIXTH CONDITION IS THE ONE THAT MAKES THE OTHER FIVE MEAN ANYTHING, and it
exists because the fifth alone is the author's own unverified word. Severing the
lift from the map key removed an unenforced convention and put nothing in its
place: the binding's author chooses which requirement the reference names, so a
pair may point both references at whichever requirement lets them through, and
the packaged negative that is this capability's only red proof of serving-tier
separation is admitted with four declarations added and its shared secret
untouched. THE REMEDY IS NOT TO TRUST THE KEY BUT TO ENFORCE IT: the schema SHALL
constrain the `credential_bindings` map key to the identifier grammar so the key
stops being a convention, and the reference SHALL be required to name the
binding it sits on. A precondition an author can satisfy by choosing where to
point is not a precondition — the same sentence this requirement already uses
against the map key, applied to its replacement. If no such binding link can be
specified, the lift SHALL NOT ship.

THE ACCESS MODE SHALL BE READABLE, AND UNREADABLE SHALL MEAN UNAVAILABLE. The
schema types the discriminator as an unconstrained string and one line of code
compares it to one exact spelling, so today an ABSENT access mode compares equal
to another absent one, and a variant spelling compares equal to itself — both
"equal, and not dispatch-only", both lifting. The schema SHALL therefore close
`access_mode` to a DECLARED VOCABULARY, and an access mode that is absent,
non-string, or outside that vocabulary on either resolved record SHALL make the
lift UNAVAILABLE rather than satisfied. This is the rule this capability's own
estate already learned from a fail-open drift check — an entry that cannot answer
the question is not a matching entry — applied to the field the lift turns on
rather than only to the reference that reaches it.

EVERY CONDITION FAILS CLOSED, and the list is the whole six rather than a sample:
an absent block, a shared holder reference, a shared fetch identity, a one-sided
or missing acknowledgment, a reference resolving to zero or to more than one
record, a reference whose id does not equal its binding's key, an ungrammatical
or escaping document reference, and an access mode that is absent, unrecognised,
mixed or dispatch-only each leave the default refusal standing. An unreadable
precondition makes the lift UNAVAILABLE and never merely UNCHECKED, because a
check that treats what it could not read as satisfied is the fail-open shape this
family has already had to repair once.

THE ARITY IS EVERY PAIR, NOT THE FIRST AGAINST THE REST. The predicate this rule
inherits keeps the FIRST binding seen for each secret reference and compares
every later one against it, so with three bindings on one secret the second and
third are never compared with each other — and a record in which those two share
a fetch identity carries the authority collapse and is accepted on both examined
pairs. The conditions above SHALL hold over EVERY PAIR sharing the reference, and
the inherited first-against-rest shape SHALL be REPLACED rather than extended.

THE FIFTH CONDITION'S ACCESS-MODE EXCLUSION OVER-REFUSES DELIBERATELY. Excluding
dispatch-only on both sides means two consumers of ONE dispatch-only credential
are refused too, which nothing else in this capability forbids. That is a chosen
conservatism, not an oversight: the dispatch class is where serving-tier
separation lives, and a rule that refuses a shape no consumer currently needs is
cheaper to relax on evidence than a rule that admits one nobody checked.
Relaxing it SHALL be a separate act carrying its own case.

A REFUSAL SHALL NAME THE FAULT IT FOUND, AND NAME IT ONCE. Two bindings whose
FETCH IDENTITIES are the same while their HOLDER REFERENCES DIFFER SHALL be
refused under a distinct finding that names two systems sharing one authority,
rather than under the finding about two credentials collapsing into one. They are
different faults with different remedies, and a reader told about the wrong one
repairs the wrong thing. Where the distinct finding applies it REPLACES the
default finding for that pair rather than accompanying it: one fault SHALL
produce one finding, or a reader repairing the named fault is left with a second
refusal describing the same record.

AND THAT FAULT IS NOT THE SHARED SECRET REFERENCE. Two different holders
declaring one fetch identity is the authority collapse WHATEVER their
`secret_ref`s, because a shared secret reference is a proxy for the rule and not
the rule; scoping the finding to a shared reference leaves the same collapse
unreported when two spellings name one secret. The finding SHALL be raised on the
holder/fetch-identity pair within one document, independently of the secret
reference. One holder reusing its own fetch identity across its own bindings is
NOT the fault and SHALL NOT be reported.

THE COMPARISON IS WITHIN ONE RECORD. These conditions are evaluated across the
bindings of a single template by a validator that reads one repository, and
SHALL NOT be claimed to compare bindings held in different repositories. Where
an operated identity's consumers are declared in separate repositories — which
the residency model makes the ordinary case — the declaration is what makes the
authority readable at each site, and reconciling the sites is an estate-level
act this requirement does not perform.

#### Scenario: Two consuming systems reach one operated identity
- **WHEN** two bindings share a `secret_ref`, declare different holder references and different fetch identities, both declare the shared-credential acknowledgment, and both name a qualified requirement whose id equals their own map key and whose access mode is the same declared non-dispatch member
- **THEN** the record validates, and it states two consumers of one deliberately shared credential rather than two credentials collapsed into one

#### Scenario: A pair points its references at a requirement neither binding is
- **WHEN** two bindings sharing a `secret_ref` name requirement references whose ids do not equal their own map keys — for instance both pointing at the content requirement so their access modes compare equal
- **THEN** the lift is UNAVAILABLE and the default refusal stands, because a condition the author satisfies by choosing where to point is no condition at all
- **AND** the packaged dispatch-versus-content negative MUST stay refused however many declarations are added to it

#### Scenario: A resolved requirement cannot answer the access-mode question
- **WHEN** a resolved requirement carries no access mode, a non-string access mode, or a spelling outside the declared vocabulary
- **THEN** the lift is UNAVAILABLE and the record is reported — never "equal, and not dispatch-only"
- **AND** two records that both cannot answer MUST NOT compare equal to each other

#### Scenario: Three bindings share one secret and two of them share an authority
- **WHEN** three bindings share a `secret_ref` and the second and third declare the same fetch identity while the first differs from both
- **THEN** the record MUST be refused, because the conditions hold over every pair and not merely over each pair containing the first binding
- **AND** an implementation carrying the inherited first-against-rest shape MUST be replaced rather than extended

#### Scenario: Two bindings on one secret share a fetch identity
- **WHEN** two bindings declare different holder references and the same fetch identity
- **THEN** they MUST be rejected under a finding naming two systems on one authority, because one identity may be shared and one authority may not
- **AND** the finding fires whether or not their `secret_ref`s are equal, and MUST NOT be the one about two credentials collapsing into one

#### Scenario: One holder reuses its fetch identity across its own bindings
- **WHEN** one holder reference declares the same fetch identity on more than one of its own bindings
- **THEN** nothing is reported, because a system legitimately authenticates as itself across the credentials it holds

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

AND WHAT IT PUBLISHES SHALL BE STATED, because the reach is honest in one
direction only until it is. The binding already carries the vault, the secret
reference and the owner; this block adds the principal that can fetch that secret
and the system that holds it, IN THE SAME OBJECT. The defensive gain and the
exposure are the same fact read from two sides: for an operator, "which grant do
I revoke" becomes a lookup rather than an inference — and for anyone who can read
the record, so does "which principal reaches this secret". That is not
speculative; the family this vocabulary is borrowed from already publishes live
estate principal names in its packaged, digest-pinned examples. At the major the
declaration becomes REQUIRED, so the disclosure stops being opt-in and becomes
estate-wide. The disclosure is worth accepting and the residency model bounds it
by keeping instance records in the consuming installs — but it SHALL be stated
rather than omitted, and a packaged fixture SHALL carry SYNTHETIC identifiers and
SHALL NOT carry a live fetch identity merely because a live one would be more
illustrative.

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

#### Scenario: The record is read by someone who should not reach the secret
- **WHEN** a binding declares a fetch identity beside its vault and secret reference
- **THEN** the record publishes, in one object, which principal reaches which secret — and an adopting change SHALL record that as a consequence of the declaration rather than describing only the revocation gain
- **AND** at the major, where the declaration is required, that publication is estate-wide rather than per-record

#### Scenario: A packaged fixture is offered a live fetch identity
- **WHEN** a fixture destined for the packaged, digest-pinned corpus would name a live install's fetch identity or holder reference
- **THEN** it SHALL use a SYNTHETIC value instead, because the corpus is distributed to every consumer that pins the contract and illustrative realism is not a reason to widen a disclosure
- **AND** the live identifiers remain in the consuming installs' own credential trees, where the residency model already places an estate fact and where the readership is the install's rather than every pinning consumer

#### Scenario: An adopting document describes the field
- **WHEN** a change, runbook or contract document adopts the consumer field
- **THEN** it states all three halves — revocation of access becomes readable, a bearer secret already fetched stays shared until rotation, and the record now publishes which principal reaches which secret
- **AND** a description carrying only the first is non-conforming, because the omission is what turns a readability gain into a containment claim
- **AND** THIS OBLIGATION IS THE REQUIREMENT'S RATHER THAN A CHECKER'S — whether arbitrary prose "states all three" is a judgment over unbounded document space, so any check offered against this scenario MUST state which shapes it actually detects and MUST NOT be described as deciding the general case
