# credential-contracts (delta) — add-binding-access-identity

NO `## MODIFIED Requirements` BLOCK, DELIBERATELY. The sentence that says which
kinds and which fields the canonical schema owns lives in `Canonical credential
record shapes`, and `add-credential-escrow-checkout` is holding a LIVE MODIFIED
block on exactly that requirement today
(`openspec/changes/add-credential-escrow-checkout/specs/credential-contracts/spec.md:5`).
Two active changes holding two live deltas on one requirement text is the shape
`add-notebook-hosting-credential-custody` refused on purpose — "no requirement is
MODIFIED here precisely so that two active changes never hold two live deltas on
one requirement text"
(`openspec/changes/add-notebook-hosting-credential-custody/review/ratification-2026-08-23.md:46-48`)
— and the scenario-loss class that produced issues #329 and #330 is what happens
when that discipline lapses. The shape-ownership sentence is therefore OWED, not
dropped: tasks §2.3 carries it as a sequencing obligation on whichever of the two
packets archives SECOND, and this delta states the obligations themselves as
ADDED requirements that stand on their own terms.

## ADDED Requirements

### Requirement: A credential binding declares the consuming system and the access identity it presents
A credential binding SHALL be able to declare the CONSUMING SYSTEM it serves, the ACCESS IDENTITY that system presents to the secret store, and — where the credential authenticates an operated identity more than one system reaches — the OPERATED IDENTITY that binding consumes. All three declarations are ADDITIVE AND OPTIONAL: a binding that declares none remains valid unchanged, and a repository holding only such bindings remains conformant at its pinned bundle until it deliberately upgrades.

WHY THE FIELDS HAVE TO EXIST, stated as a gap this capability already admitted rather than as a preference. `credential-contracts` requires that each consuming system reach a shared operated identity through its OWN binding — its own access identity, its own grant, its own rotation visibility, its own audit trail — on the rule that ONE IDENTITY MAY BE SHARED AND ONE AUTHORITY SHALL NOT. The published shape could not express that: it required `provider`, `secret_ref`, `owner` and `rotation_policy` with an optional `vault`, named no consumer and no access identity, and the validator compared no authorities, so two bindings naming the same store principal validated cleanly. The invariant was held by review and by estate wiring, and the capability recorded that as owed to a successor extending the shape rather than leaving it implied as enforced. This requirement is that extension.

THE CONSUMING SYSTEM IS NAMED EXPLICITLY AND IS NOT INFERRED FROM THE MAP KEY. The `credential_bindings` map is keyed by REQUIREMENT ID, not by consuming system, so the key answers WHICH CREDENTIAL a binding resolves and never WHO CONSUMES IT. Two requirement-keyed bindings carrying distinct access identities would otherwise prove that two authorities exist while leaving unstated which system holds each, and attribution — the property this capability asks the store's access log to deliver — needs the name.

DECLARING IS NOT PROVING THE ESTATE. The record proves that two bindings CLAIM distinct authorities; it cannot prove that the two principals named are actually distinct in the store, that either exists, or that the grants behind them differ. What the declaration buys is that a claim now exists to check, is attributable, and is refusable when it contradicts itself — the estate half stays with the store and its operator, and this requirement SHALL NOT be read as evidence that the separation was verified against a live directory.

#### Scenario: A binding declares its consuming system and access identity
- **WHEN** a credential binding names the system it serves and the principal that system presents to the secret store
- **THEN** it validates, and the per-system authority the capability requires is stated in the record rather than asserted by its owner

#### Scenario: A binding predating the extension is revalidated
- **WHEN** an existing binding declaring none of the three fields is validated against the extended schema
- **THEN** it MUST validate unchanged, because all three are optional and additive and a pinned consumer is not obliged to move
- **AND** no finding is raised against it, because absence of a declaration is not a claim of anything

#### Scenario: Two systems reach one operated identity
- **WHEN** two bindings each declare the same operated identity, each names its own consuming system, and each declares its own distinct access identity
- **THEN** the shape the capability already requires is now representable in the record, and the two authorities are separately attributable to named systems

#### Scenario: A record written before the extension already carried one of the field names
- **WHEN** a binding authored before this extension already carried a key of one of these names, which the open binding object accepted as an inert extra property
- **THEN** the extension gives that key MEANING, so the record MAY newly be refused where the meaning contradicts a rule — and that is stated rather than denied, because the published shape never reserved the names
- **AND** the population of such records is MEASURED before the extension is cut rather than assumed empty

#### Scenario: The declaration is mistaken for verification of the estate
- **WHEN** a reader treats two declared distinct access identities as proof that the secret store actually holds two distinct principals with distinct grants
- **THEN** the reading is refused — the record carries the claim, the store carries the fact, and only the store's own access log can settle it

### Requirement: A shared secret reference is licit only between declared consumers of one operated identity
Two or more bindings in one binding template SHALL NOT share a `secret_ref` UNLESS every binding sharing it declares the SAME operated identity AND each declares a DISTINCT, NON-BLANK access identity. Where that condition does not hold, the shared reference is REFUSED, exactly as it is refused today.

THE DISCRIMINATION THIS SETTLES, WHICH IS THE PRECONDITION THIS CHANGE WAS TOLD TO DECIDE FIRST. The existing refusal reads one fact — two bindings, one `secret_ref` — and therefore cannot tell TWO CREDENTIALS COLLAPSED INTO ONE from TWO CONSUMERS OF ONE CREDENTIAL. The first is the defect the refusal exists to catch: a dispatch binding reusing a content credential's reference puts content-write key material in the serving tier. The second is the shape this capability's own operated-identity requirement MANDATES. Under one undiscriminating rule the conforming shape cannot be recorded at all, which is why the packaged fixture for it was declined when the requirement landed. The declaration is what separates them: two credentials collapsed into one declare no operated identity, because there is no one identity to declare.

DISTINCTNESS IS NOT A STRING COMPARISON ALONE. An empty or whitespace-only value is not a principal reference, and two different whitespace strings are pairwise distinct while naming no authority at all — which would let the conjunction be satisfied by records that identify nobody. Every declared identity SHALL therefore be a non-blank principal reference before distinctness is considered, and blankness SHALL be refused on its own terms rather than only where a reference is shared.

DEFAULT-REFUSE IS PRESERVED. Silence still refuses — a shared `secret_ref` with no operated-identity declaration is the collapsed-credential shape and stays refused on the same reasoning and the same finding. The extension widens what may be RECORDED, and the records it newly refuses are records making a claim the extension gives meaning to.

WHAT IS NOT LEGISLATED HERE. One access identity presenting for two bindings with DIFFERENT secret references is a privilege-aggregation question, not this one, and is left open rather than decided quietly: this requirement reaches only bindings that share a reference.

#### Scenario: Two credentials are collapsed into one reference
- **WHEN** two bindings share a `secret_ref` and neither declares an operated identity
- **THEN** it MUST be refused, unchanged in both outcome and reasoning — distinct credentials must be distinct bindings so the serving tier holds no content-write key material

#### Scenario: Two consumers of one operated identity share its reference
- **WHEN** two bindings share a `secret_ref`, both declare the same operated identity, and each declares its own distinct non-blank access identity
- **THEN** it MUST validate — this is the shape the capability's operated-identity requirement mandates, and it is now recordable

#### Scenario: One authority is shared along with the identity
- **WHEN** two bindings declare the same operated identity and the SAME access identity
- **THEN** it MUST be refused, because one identity may be shared and one authority may not, and a single principal reaching the secret for both systems is the shared authority the requirement forbids

#### Scenario: Only one of the sharing bindings declares the identity
- **WHEN** bindings sharing a `secret_ref` do not ALL declare the same operated identity
- **THEN** it MUST be refused, because a partial declaration leaves the shared reference unexplained and an unexplained share is the collapsed-credential shape

#### Scenario: A declared identity is blank or whitespace
- **WHEN** a binding declares an access identity or operated identity that is empty or consists only of whitespace
- **THEN** it MUST be refused wherever it appears, whether or not the binding shares a reference, because a blank value names no principal
- **AND** two bindings whose access identities differ only as distinct whitespace strings MUST NOT satisfy the distinctness condition

#### Scenario: A pre-extension repository declaring none of the fields is revalidated
- **WHEN** a repository whose bindings declare none of the three fields is validated against the extended validator
- **THEN** its findings are exactly the findings it had before, because every new refusal is reachable only through a declaration none of its records makes

### Requirement: An access identity is a principal reference and never credential material
A declared consuming system, access identity or operated identity SHALL name a PRINCIPAL or a system — a workload identity, service principal, machine account or equivalent store subject — and SHALL NOT carry credential material: no password, key, token, certificate, connection string or other value that would authenticate the principal it names.

THIS IS THE CORE RULE ARRIVING AT A NEW FIELD, NOT A NEW RULE. The repository's standing discipline is that machinery holds requirements, reference names, binding templates, approval policy, grant templates and audit rules, and that real secrets live in approved providers. A new field on the record most likely to be hand-edited is a new place for that discipline to be broken, and the existing refusal reads `secret_ref` alone — so extending the shape without extending the refusal would ship a governed-looking hole.

THE REFUSAL IS A NAMED-FORM REFUSAL AND IS NOT A PROOF OF ABSENCE. A detector recognises the forms it enumerates and no others; it cannot decide in general whether a string is a secret. The enumeration SHALL cover at least the forms this requirement names — including credential-bearing connection strings and URIs, key-value secret assignments, and structured bearer tokens — and SHALL be extended when a form escapes it. A field passing the refusal is therefore evidence that no ENUMERATED form was found, never evidence that the value is not credential material, and this requirement SHALL NOT be cited as the latter.

#### Scenario: A principal is named
- **WHEN** an access identity names a workload identity or service principal by its reference
- **THEN** it validates — naming the principal is exactly what the field is for

#### Scenario: Credential material in an enumerated form is placed in the field
- **WHEN** a declared consuming system, access identity or operated identity carries a value in one of the enumerated credential forms
- **THEN** it MUST be refused on the same terms a baked secret in a `secret_ref` is refused, because the core rule binds the record and not one of its fields

#### Scenario: A credential form escapes the enumeration
- **WHEN** credential material is placed in one of these fields in a form the detector does not enumerate
- **THEN** the record validates, and that outcome is a KNOWN LIMIT of the refusal rather than a judgement that the value is safe
- **AND** the remedy is to extend the enumeration and its fixtures, not to read the pass as an assurance

#### Scenario: The field is absent
- **WHEN** a binding declares no access identity
- **THEN** nothing is refused, because an undeclared field asserts nothing and this rule reaches declarations only
