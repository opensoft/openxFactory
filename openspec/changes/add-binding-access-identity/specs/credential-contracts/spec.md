# credential-contracts (delta) — add-binding-access-identity

NO `## MODIFIED Requirements` BLOCK, DELIBERATELY. The sentence that says which
kinds and which fields the canonical schema owns lives in `Canonical credential
record shapes`, and `add-credential-escrow-checkout` is holding a LIVE MODIFIED
block on exactly that requirement today
(`openspec/changes/add-credential-escrow-checkout/specs/credential-contracts/spec.md:5`).
Two active changes holding two live deltas on one requirement text is the shape
`add-notebook-hosting-credential-custody` refused on purpose — "no requirement is
MODIFIED here precisely so that two active changes never hold two live deltas on
one requirement text" (`review/ratification-2026-08-23.md:24-27`) — and the
scenario-loss class that produced issues #329 and #330 is what happens when that
discipline lapses. The shape-ownership sentence is therefore OWED, not dropped:
tasks §2.3 carries it as a sequencing obligation on whichever of the two packets
archives SECOND, and this delta states the obligations themselves as ADDED
requirements that stand on their own terms.

## ADDED Requirements

### Requirement: A credential binding declares the access identity its consuming system presents
A credential binding SHALL be able to declare the ACCESS IDENTITY its consuming system presents to the secret store, and — where the credential authenticates an operated identity more than one system reaches — the OPERATED IDENTITY that binding consumes. Both declarations are ADDITIVE AND OPTIONAL: a binding that declares neither remains valid unchanged, and a repository holding only such bindings remains conformant at its pinned bundle until it deliberately upgrades.

WHY THE FIELD HAS TO EXIST, stated as a gap this capability already admitted rather than as a preference. `credential-contracts` requires that each consuming system reach a shared operated identity through its OWN binding — its own access identity, its own grant, its own rotation visibility, its own audit trail — on the rule that ONE IDENTITY MAY BE SHARED AND ONE AUTHORITY SHALL NOT. The published shape could not express that: it required `provider`, `secret_ref`, `owner` and `rotation_policy` with an optional `vault`, named no consumer and no access identity, and the validator compared no authorities, so two bindings naming the same store principal validated cleanly. The invariant was held by review and by estate wiring, and the capability recorded that as owed to a successor extending the shape rather than leaving it implied as enforced. This requirement is that extension.

DECLARING IS NOT PROVING THE ESTATE. The record proves that two bindings CLAIM distinct authorities; it cannot prove that the two principals named are actually distinct in the store, that either exists, or that the grants behind them differ. What the declaration buys is that a claim now exists to check, is attributable, and is refusable when it contradicts itself — the estate half stays with the store and its operator, and this requirement SHALL NOT be read as evidence that the separation was verified against a live directory.

#### Scenario: A binding declares its access identity
- **WHEN** a credential binding names the principal its consuming system presents to the secret store
- **THEN** it validates, and the per-system authority the capability requires is stated in the record rather than asserted by its owner

#### Scenario: A binding predating the extension is revalidated
- **WHEN** an existing binding declaring neither an access identity nor an operated identity is validated against the extended schema
- **THEN** it MUST validate unchanged, because both fields are optional and additive and a pinned consumer is not obliged to move
- **AND** no finding is raised against it, because absence of a declaration is not a claim of anything

#### Scenario: Two systems reach one operated identity
- **WHEN** two bindings each declare the same operated identity and each declares its own distinct access identity
- **THEN** the shape the capability already requires is now representable in the record, and the two authorities are separately attributable

#### Scenario: The declaration is mistaken for verification of the estate
- **WHEN** a reader treats two declared distinct access identities as proof that the secret store actually holds two distinct principals with distinct grants
- **THEN** the reading is refused — the record carries the claim, the store carries the fact, and only the store's own access log can settle it

### Requirement: A shared secret reference is licit only between declared consumers of one operated identity
Two or more bindings in one binding template SHALL NOT share a `secret_ref` UNLESS every binding sharing it declares the SAME operated identity AND each declares a DISTINCT access identity. Where that condition does not hold, the shared reference is REFUSED, exactly as it is refused today.

THE DISCRIMINATION THIS SETTLES, WHICH IS THE PRECONDITION THIS CHANGE WAS TOLD TO DECIDE FIRST. The existing refusal reads one fact — two bindings, one `secret_ref` — and therefore cannot tell TWO CREDENTIALS COLLAPSED INTO ONE from TWO CONSUMERS OF ONE CREDENTIAL. The first is the defect the refusal exists to catch: a dispatch binding reusing a content credential's reference puts content-write key material in the serving tier. The second is the shape this capability's own operated-identity requirement MANDATES. Under one undiscriminating rule the conforming shape cannot be recorded at all, which is why the packaged fixture for it was declined when the requirement landed. The declaration is what separates them: two credentials collapsed into one declare no operated identity, because there is no one identity to declare.

DEFAULT-REFUSE IS PRESERVED AND NOTHING PREVIOUSLY VALID BECOMES INVALID. Silence still refuses — a shared `secret_ref` with no operated-identity declaration is the collapsed-credential shape and stays refused on the same reasoning and the same finding. The refusal for two bindings declaring the SAME access identity is likewise unreachable by any record written before this extension, because no such record can declare a field that did not exist. The extension therefore widens what may be RECORDED and never narrows what was already valid.

WHAT IS NOT LEGISLATED HERE. One access identity presenting for two bindings with DIFFERENT secret references is a privilege-aggregation question, not this one, and is left open rather than decided quietly: this requirement reaches only bindings that share a reference.

#### Scenario: Two credentials are collapsed into one reference
- **WHEN** two bindings share a `secret_ref` and neither declares an operated identity
- **THEN** it MUST be refused, unchanged in both outcome and reasoning — distinct credentials must be distinct bindings so the serving tier holds no content-write key material

#### Scenario: Two consumers of one operated identity share its reference
- **WHEN** two bindings share a `secret_ref`, both declare the same operated identity, and each declares its own distinct access identity
- **THEN** it MUST validate — this is the shape the capability's operated-identity requirement mandates, and it is now recordable

#### Scenario: One authority is shared along with the identity
- **WHEN** two bindings declare the same operated identity and the SAME access identity
- **THEN** it MUST be refused, because one identity may be shared and one authority may not, and a single principal reaching the secret for both systems is the shared authority the requirement forbids

#### Scenario: Only one of the sharing bindings declares the identity
- **WHEN** bindings sharing a `secret_ref` do not ALL declare the same operated identity
- **THEN** it MUST be refused, because a partial declaration leaves the shared reference unexplained and an unexplained share is the collapsed-credential shape

#### Scenario: A pre-extension repository is revalidated
- **WHEN** a repository whose bindings predate this extension is validated against the extended validator
- **THEN** its findings are exactly the findings it had before, because every new refusal is reachable only through a field no earlier record could carry

### Requirement: An access identity is a principal reference and never credential material
A declared access identity or operated identity SHALL name a PRINCIPAL — a workload identity, service principal, machine account or equivalent store subject — and SHALL NOT carry credential material: no password, key, token, certificate, connection string or other value that would authenticate the principal it names.

THIS IS THE CORE RULE ARRIVING AT A NEW FIELD, NOT A NEW RULE. The repository's standing discipline is that machinery holds requirements, reference names, binding templates, approval policy, grant templates and audit rules, and that real secrets live in approved providers. A new field on the record most likely to be hand-edited is a new place for that discipline to be broken, and the existing refusal reads `secret_ref` alone — so extending the shape without extending the refusal would ship a governed-looking hole.

#### Scenario: A principal is named
- **WHEN** an access identity names a workload identity or service principal by its reference
- **THEN** it validates — naming the principal is exactly what the field is for

#### Scenario: Credential material is placed in the field
- **WHEN** a declared access identity or operated identity carries a value bearing the marks of credential material
- **THEN** it MUST be refused on the same terms a baked secret in a `secret_ref` is refused, because the core rule binds the record and not one of its fields

#### Scenario: The field is absent
- **WHEN** a binding declares no access identity
- **THEN** nothing is refused, because an undeclared field asserts nothing and this rule reaches declarations only
