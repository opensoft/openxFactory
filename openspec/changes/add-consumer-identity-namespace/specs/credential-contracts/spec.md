# credential-contracts

## MODIFIED Requirements

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

THE BLOCK MAY ALSO CARRY the NAMESPACE the fetch identity is issued in, a
reference to the requirement the binding resolves, an acknowledgment that the
credential is deliberately reached by more than one consumer, and a declaration
that the record is an instantiation stub. The
acknowledgment and the stub declaration SHALL each be a DECLARED-OR-ABSENT token
whose only valid value is true, on the same reasoning this schema already applies
to issuance preconditions: a false-valued declaration reads as governance while
asserting nothing.

A FETCH IDENTITY IS A NAME, AND A NAME IS UNIQUE ONLY INSIDE THE DIRECTORY THAT
ISSUED IT. The block SHALL therefore carry an ADDITIVE OPTIONAL
`identity_namespace` naming the ISSUING DIRECTORY, ACCOUNT OR TENANT WITHIN THE
PROVIDER that mints the fetch identity, and WHERE BOTH SIDES OF A COMPARISON
DECLARE ONE the authority a binding names is THE PAIR rather than the bare
string. Two genuinely different principals, in two tenants of one provider, may
both be called `runtime_identity`; before this member the record had no way to
say so, and the only escape from the refusal that follows was to RENAME one
fetch identity in the record while the principal kept its real name in the
provider. That makes the record FALSE, it is the misrepresentation this family
has already refused once, and A REFUSAL WHOSE ONLY ESCAPE IS A LIE IS WORSE THAN
THE OVER-REPORT IT PREVENTS.

THE MEMBER IS OPTIONAL AND ITS ABSENCE FAILS CLOSED, and those are one design
rather than two. Where either side declares no namespace — or declares one that
does not match its grammar — the comparison FALLS BACK to the bare fetch
identity and the finding is still REPORTED. An estate SHALL NOT be able to
silence a real shared authority by OMISSION: absence never clears, it only
declines to distinguish. What the member buys runs the other way and is the
whole of the gain — a pair that is reported today and is not in fact one
authority goes silent only when BOTH bindings say, in their own bytes, which
directory issued the identity they name.

THE NAME IS SETTLED AGAINST TWO SPELLINGS THIS ESTATE HAS ALREADY SPENT.
`tenant` and `tenant_ref` are NOT available: `adopt-subject-tenant-domain-vocabulary`
reserves `tenant` for the TENANT-OPERATOR LAYER
(`contracts/policies/layer-vocabulary.yaml`), and giving a ratified word a second
sense inside one contract family is how a vocabulary stops being one. `realm` is
Keycloak's word for one product's instance of this idea, and a provider-neutral
shape SHALL NOT name a provider-specific concept. `identity_namespace` collides
with nothing and follows the compound idiom this repository's contracts already
write in `policy_namespace`.

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
grammar; an `access_mode` outside the closed vocabulary; a
`requirements_document_ref` outside the path grammar; and an
`identity_namespace` outside the identifier grammar — NINE shapes now, and the
ninth SHALL carry a code of ITS OWN rather than joining the member-grammar code,
because its consequence is not the other members'. An ungrammatical namespace is
SKIPPED by the authority comparison and the pair falls back to the bare
identity, so a reader told only that a member failed a grammar would not learn
that the scoping they declared is not in force. **A WARNING SET THAT LEAVES
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

#### Scenario: A binding declares the namespace its fetch identity is issued in
- **WHEN** a credential binding declares a `consumer:` block carrying an `identity_namespace` beside its holder reference and its fetch identity
- **THEN** it validates, and WHICH DIRECTORY ISSUED the identity is a fact of the record rather than an inference from the vault the binding happens to name
- **AND** the member is OPTIONAL at the release that declares it, so a binding that omits it draws no omission warning and is refused nothing

#### Scenario: A namespace value does not match the identifier grammar, at the minor
- **WHEN** a `consumer:` block at the introducing minor carries an `identity_namespace` whose value does not match the identifier grammar
- **THEN** the record remains VALID and the validator warns under the NAMESPACE'S OWN code, distinct from the code naming a `holder_ref` or `fetch_identity` grammar fault
- **AND** the warning MUST say that the value is NOT READ AS A NAMESPACE, because the authority comparison skips it and a reader who is not told that will believe a scoping they declared is in force

#### Scenario: The namespace is one of the members the block closes around at the major
- **WHEN** the major release that constrains the block is validated against
- **THEN** `identity_namespace` is a DECLARED member — a block carrying it is not an undeclared-member refusal — and a value outside the identifier grammar is an ERROR
- **AND** that release MUST have been preceded by a full minor in which the same value produced a warning, on exactly the terms every other member of the block is served by

#### Scenario: A block declares a namespace and neither identifier
- **WHEN** a `consumer:` block carries an `identity_namespace` and omits `holder_ref` or `fetch_identity`, at the introducing minor
- **THEN** the incomplete-block finding fires unchanged, because a namespace scopes an identity and does not stand in for one
- **AND** the namespace MUST NOT be read as satisfying either identifier, on the same ground a grammar-passing sentinel is refused as a repair: a record that names a directory and no principal names no authority at all

### Requirement: Two bindings on one secret are refused unless every pair declares distinct consumers, acknowledges the sharing, and names a requirement bound to the binding
Bindings in one credential binding template that share a `secret_ref` SHALL be REFUSED by default, and that refusal SHALL be lifted ONLY where every one of six conditions holds together, OVER EVERY PAIR that shares that reference: both bindings declare a `consumer:` block; their holder references DIFFER; their fetch AUTHORITIES DIFFER — the fetch identity read WITH the `identity_namespace` that issued it where BOTH declare a grammatical one, and the bare fetch identity otherwise; both declare the shared-credential acknowledgment; both name a QUALIFIED requirement reference resolving, IN THE ONE REQUIREMENTS DOCUMENT THAT REFERENCE NAMES, to EXACTLY ONE requirement whose ACCESS MODE IS A MEMBER OF THE DECLARED VOCABULARY, equal across the pair and not dispatch-only; and each reference's `requirement_id` EQUALS THE MAP KEY of the binding that carries it.

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
an absent block, a shared holder reference, a shared fetch authority, a one-sided
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
FETCH AUTHORITIES are the same while their HOLDER REFERENCES DIFFER SHALL be
refused under a distinct finding that names two systems sharing one authority,
rather than under the finding about two credentials collapsing into one. They are
different faults with different remedies, and a reader told about the wrong one
repairs the wrong thing. Where the distinct finding applies it REPLACES the
default finding for that pair rather than accompanying it: one fault SHALL
produce one finding, or a reader repairing the named fault is left with a second
refusal describing the same record.

AND THAT FAULT IS NOT THE SHARED SECRET REFERENCE. Two different holders
declaring one fetch AUTHORITY is the authority collapse WHATEVER their
`secret_ref`s, because a shared secret reference is a proxy for the rule and not
the rule; scoping the finding to a shared reference leaves the same collapse
unreported when two spellings name one secret. The finding SHALL be raised on the
holder/fetch-authority pair within one document, independently of the secret
reference. One holder reusing its own fetch identity across its own bindings is
NOT the fault and SHALL NOT be reported.

AND THE AUTHORITY IS THE IDENTITY READ WITH THE NAMESPACE THAT ISSUED IT, because
a bare string comparison refuses a shape that is not the fault. A principal name
is unique only inside its issuing directory, so two bindings naming
`runtime_identity` in two tenants of ONE provider are two principals and not one
authority — and a finding raised on them is a FALSE REFUSAL THE RECORD CANNOT
ESCAPE, since the only workaround available before the namespace member existed
was to write a name the provider does not use. The comparison SHALL therefore be
made on the PAIR of `identity_namespace` and `fetch_identity`, and a pair whose
namespaces are both declared, both grammatical, and DIFFERENT SHALL NOT be
reported.

AND THE FALLBACK SHALL REPORT RATHER THAN CLEAR. Where either side declares no
namespace, or declares a value outside the identifier grammar, the comparison
SHALL fall back to the bare fetch identity and the finding SHALL still be
raised. The reason is the whole reason a security rule has a default: an estate
that could clear a real shared authority by OMITTING a member on one side would
hold a refusal it can silence without ever writing anything false, which is a
worse instrument than the over-report this member exists to end. THE REPORT SHALL
NAME THE NAMESPACE WHERE ONE IS PRESENT, so a reader can see whether the scoping
they declared was read, and the remedy for a one-sided declaration is to declare
the namespace on BOTH bindings rather than to remove it from the one that has it.

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
- **WHEN** two bindings declare different holder references and the same fetch identity, and they declare no `identity_namespace` or declare the same one
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
- **WHEN** a named requirement reference matches more than one requirement record in the requirements document the reference names
- **THEN** the lift is UNAVAILABLE and the ambiguity is reported, exactly as a reference resolving to nothing is
- **AND** an implementation MUST NOT resolve the ambiguity by picking one — the two matches may carry different access modes, and a rule whose outcome depends on which was found first is not a rule

#### Scenario: A bare requirement id is offered instead of a qualified reference
- **WHEN** a `consumer:` block names a requirement by id alone, with no requirements document
- **THEN** the reference does not satisfy the lift's condition, because a bare id is not unique in the tree the validator scans

#### Scenario: Two bindings share a secret and declare nothing
- **WHEN** two bindings share a `secret_ref` and neither declares a `consumer:` block
- **THEN** the existing refusal fires exactly as it does today, because this change tightens before it lifts and nothing that is refused today becomes accepted by silence

#### Scenario: Two tenants of one provider name their principals the same
- **WHEN** two bindings declare different holder references and the same fetch identity, and each declares a DIFFERENT grammatical `identity_namespace`
- **THEN** nothing is reported, because these are two directories' identically-labelled principals rather than two systems on one authority
- **AND** the distinction MUST be READ FROM THE DECLARATION and never inferred from the vault, the provider or the owner — those differ freely between bindings that DO collapse two systems onto one authority, which is why the finding has always ignored them

#### Scenario: One side declares a namespace and the other does not
- **WHEN** two bindings declare different holder references and the same fetch identity, and exactly one of them declares an `identity_namespace`
- **THEN** the comparison FALLS BACK to the bare fetch identity and the finding is still REPORTED
- **AND** the remedy is to declare the namespace on BOTH bindings, never to delete it from the one that carries it — a rule an estate could silence by omitting a member is not a rule

#### Scenario: A declared namespace does not match the grammar
- **WHEN** one of two bindings that declare different holder references and the same fetch identity carries an `identity_namespace` outside the identifier grammar
- **THEN** the value is NOT read as a namespace, the comparison falls back to the bare fetch identity, and the shared-authority finding is REPORTED
- **AND** the record ALSO draws the namespace's own grammar warning, the two answering different questions — whether this value is well formed, and whether these two bindings are one authority — which is two faults in one record rather than one fault named twice
