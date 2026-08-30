# credential-contracts (delta) — extend-credential-binding-authority

## MODIFIED Requirements

### Requirement: Dispatch-only credential least privilege and serving-tier separation
A dispatch-only credential — one that exists to TRIGGER execution (a workflow dispatch or job kickoff) — SHALL be scoped to exactly the minimal permission required to trigger its one named target and nothing more (for a GitHub-hosted factory, `actions: write` on the single repository that owns the workflow), carrying no repository-contents authority. It SHALL be a DISTINCT binding from any content-write credential the same capability uses, and a zero-write-authority serving surface holding a dispatch-only credential MUST NOT hold — nor hold key material capable of minting — a content-write credential.

THE CHECK THAT ENFORCES THE DISTINCT-BINDING HALF COMPARES QUALIFIED SECRET
REFERENCES, AND THIS REQUIREMENT SAYS SO RATHER THAN LEAVING IT TO THE
REQUIREMENT THAT CHANGED IT. `shared-secret-identity` groups bindings on
`(provider, vault, secret_ref)`, so two bindings naming one label in two
different vaults are two secrets and are not a collision. Where the
qualification is NOT established — any member of a matching
`(provider, secret_ref)` set omitting `vault` — the grouping SHALL fall back to
the bare `secret_ref`, so a dispatch binding and a content-write binding sharing
a reference remain REFUSED whether or not either declares its vault. The
serving-tier separation this requirement exists for SHALL NOT be escapable by
omitting an optional field.

#### Scenario: A dispatch credential requests contents authority
- **WHEN** a dispatch-only credential requirement or binding grants repository-contents write, or any scope beyond triggering its one named target
- **THEN** the validator MUST report an error

#### Scenario: A dispatch credential reuses the content credential's identity
- **WHEN** a dispatch binding names the same App or key identity as a content-write binding
- **THEN** it MUST be rejected, because the serving tier would then hold key material capable of minting a content-write token

#### Scenario: A correctly separated dispatch credential
- **WHEN** a dispatch-only credential is scoped to trigger exactly one named workflow on one repository, held as a binding distinct from the content-write credential
- **THEN** it is valid

#### Scenario: A dispatch and content binding share a reference with one vault undeclared
- **WHEN** a dispatch binding and a content-write binding share a secret reference under one provider, and only one of them declares its vault
- **THEN** it MUST still be rejected, because the grouping falls back to the bare reference where the qualification is unestablished
- **AND** the accompanying `authority-scope-indeterminate` warning does not stand in place of that refusal

## ADDED Requirements

### Requirement: The credential binding record declares the authority that reaches the secret
A credential binding SHALL be able to declare, IN THE RECORD rather than in review, the four facts that make its authority readable: the CONSUMING SYSTEM that reaches the credential through this binding, the IDENTITY that consumer authenticates to the secret store with, the NAMESPACE that issues that identity, and the CREDENTIAL REQUIREMENT the binding resolves. Until it can, two bindings naming the same store principal are indistinguishable from two bindings naming different ones, and every rule about per-system authority is unenforceable by construction.

THE SPELLINGS ARE THE ESTATE'S OWN, a record SHALL use them, and no second
vocabulary is introduced.
The consuming system is `consumer`; the store identity is `fetch_identity`,
which is already this family's word — the promoted requirements say the lane
receives "an opaque secret reference and a fetch-identity identifier" and that
delivery by reference is "a vault URI plus the runtime's own fetch identity",
and a shipped record of THIS RECORD KIND already carries the key
(`contracts/avatar-client/broker-server-key-binding.template.yaml`); the
requirement is `requirement_id`, matching the runtime capability grant's
existing field of that name rather than coining a `_ref` variant beside it.
"Access identity", as used in this capability's operated-identity requirement
and in the projection documentation, NAMES THE SAME THING as `fetch_identity`;
the prose synonym stands and the RECORD has exactly one spelling.

ALL FOUR FIELDS ARE OPTIONAL AT THE MINOR THAT INTRODUCES THEM, AND EXACTLY TWO
OF THEM — `consumer` AND `fetch_identity` — BECOME REQUIRED AT THE NEXT MAJOR
VERSION. `identity_namespace` AND `requirement_id` REMAIN OPTIONAL ACROSS THAT
BOUNDARY, and for the same reason in both cases: neither one's ABSENCE EVER
WARNS, so no major may require it without breaking a shape no minor ever
deprecated. `identity_namespace`'s absence is not a defect to be migrated away —
it is a record declining to make a distinction, which the identity comparison
already handles by falling back to `provider` alone and REPORTING. A field whose
omission is a conforming answer cannot be made mandatory by a later release. A binding that does not
declare BOTH a `consumer` AND a `fetch_identity` SHALL raise a validator
WARNING naming whichever is missing, SHALL remain valid throughout the CURRENT
MAJOR LINE (every `contract-v2.x` bundle), and SHALL be refused at the next
MAJOR VERSION. That sequence is what the change classes require: an optional
field plus a new validator warning is the ADDITIVE class, while a required field
is the BREAKING class, which owes at least one full minor release of deprecation
warnings first. The warning IS the migration path, and the removal version SHALL
be stated in the changelog entry that introduces it.

THE WARNING FIRES ON EITHER ABSENCE, NOT ONLY ON BOTH, because the two fields
become required together. A record declaring one and omitting the other would
otherwise pass silently through every minor of the current line and break at the
next major version with no notice — the same defect this requirement refuses one
paragraph below for `requirement_id`, reached from the other direction. A
deprecation that skips half the shapes it will refuse is not a migration path.

`requirement_id` IS DELIBERATELY NOT ON THAT PATH, and the asymmetry is a
consequence of the deprecation rule rather than an omission. Its absence never
warns, because a binding that is the only one resolving its requirement already
carries that fact in its map key and would gain nothing but redundancy; so a
major that made it required would be a breaking change no minor had ever warned
about, which the versioning policy forbids. `requirement_id` stays optional
across the major boundary too, and is obligatory only where a record CLAIMS the
shared-secret exemption — a condition of that claim, stated in the requirement
that grants it, and not a property of every binding.

A NAME IS SCOPED BY THE NAMESPACE THAT ISSUES IT, NEVER GLOBAL, AND THE TWO
NAMES IN THIS RECORD ARE ISSUED BY DIFFERENT NAMESPACES. `provider` and `vault`
are per-binding and unconstrained, so bare string equality SHALL NOT be treated
as evidence of a shared authority or a shared secret. But the qualification
differs by field and SHALL NOT be uniform:

- `fetch_identity` is a name in an IDENTITY NAMESPACE and SHALL be compared on
  `(provider, identity_namespace, fetch_identity)`. It SHALL NOT be qualified by
  `vault`. One principal granted on two vaults is ONE AUTHORITY, and folding
  the vault into the identity key would report two — which is precisely the
  shared authority the per-system obligation exists to forbid, made invisible.
- `identity_namespace` names the DIRECTORY, ACCOUNT OR TENANT WITHIN THE PROVIDER
  that issues the identity — the boundary inside which a principal name is
  unique. `provider` alone is too coarse: two directories of one provider may
  each hold a principal called `runtime_identity`, and they are two authorities.
- `secret_ref` is a name in a VAULT and SHALL be compared on
  `(provider, vault, secret_ref)`. The same label in two vaults is two secrets.
- `requirement_id` SHALL NOT be qualified at all: a requirement is a sibling
  record in the same domain's own contract tree, not a name in a third party's
  namespace.

THE ASYMMETRY IS THE POINT AND NOT AN INCONSISTENCY. A vault is where a secret
lives; it is not where an identity lives. Qualifying both names the same way
reads as tidiness and buys a silent false negative on the one rule whose whole
purpose is to catch an authority serving two systems.

THE MAP KEY IS A BINDING IDENTIFIER AND `requirement_id` IS THE DECLARED
RELATION, which resolves an ambiguity the shape has carried unstated. Every
packaged record so far keys `credential_bindings` BY the requirement id, so the
key has been doing two jobs by convention with nothing declaring it. Where
`requirement_id` is declared it SHALL be authoritative for which requirement the
binding resolves; existing records whose key is the requirement id stay correct
and unambiguous, because the convention and the declaration agree wherever both
are present. The key must remain free to be a binding identifier, because two
bindings resolving ONE requirement — the whole subject of this capability's
per-system authority obligation — cannot both be keyed by it.

WHAT THE DECLARATION IS, STATED HONESTLY. It is an ASSERTION BY THE BINDING'S
OWNER, not a proof about the store. Nothing here reads the vault's grants, so a
record naming two fetch identities that are in fact one principal is
conforming-and-wrong. What changes is that the claim becomes CHECKABLE and
ATTRIBUTABLE instead of unwritten: before, the record could not even state the
thing that would be wrong.

THE SHAPE DOES NOT REFUSE A SECOND SPELLING AT THIS MINOR, and that is a limit
rather than an oversight. The binding object does not close its properties, so
a record spelling the field `access_identity` validates silently; closing the
object is a NARROWING and belongs to the next major version. Until then the single spelling
is held by this requirement and by review, which is the same posture — named,
not hidden — that this capability took for the invariant this packet is
retiring.

#### Scenario: A binding declares its authority
- **WHEN** a credential binding declares its consumer, its fetch identity, and the requirement it resolves
- **THEN** it validates, and the per-system authority resolves FROM THE RECORD rather than from the binding owner's estate wiring

#### Scenario: A binding declares no authority
- **WHEN** a credential binding declares neither a consumer nor a fetch identity
- **THEN** it remains VALID for every bundle on the current major line, because the fields are optional and nothing previously conforming is invalidated
- **AND** the validator raises a warning naming both fields, so the absence is visible rather than silent

#### Scenario: A binding declares one of the two and omits the other
- **WHEN** a credential binding declares a fetch identity but no consumer, or a consumer but no fetch identity
- **THEN** the validator raises the same warning, naming the one that is missing
- **AND** it is not passed over as partially migrated, because both fields are refused together at the next major version and a shape that never warned cannot be broken there

#### Scenario: The next major arrives
- **WHEN** the next MAJOR VERSION — the release that ends the deprecation — lands
- **THEN** a binding not declaring BOTH `consumer` and `fetch_identity` is REFUSED, the requirement having served at least one full minor release of warnings and the changelog having named the removal version
- **AND** a binding declaring no `requirement_id` is NOT refused, because its absence never warned and a major may not break what no minor deprecated

#### Scenario: A record uses a second spelling for the store identity
- **WHEN** a binding declares `access_identity` instead of `fetch_identity`
- **THEN** it is non-conforming to this requirement, which admits ONE record spelling
- **AND** the published shape does not itself refuse the key at this minor, because refusing unknown keys narrows what was valid and is reserved for the next major version — so the refusal is a review act until then, and is recorded as one

#### Scenario: A shipped record already carries the identity outside the binding
- **WHEN** an existing record of this kind carries a fetch identity in a document-level block rather than per binding
- **THEN** it REMAINS VALID, because this change adds fields and narrows nothing
- **AND** reconciling it to the per-binding declaration is recorded as owed to the change that owns that record, not performed by this one

### Requirement: One operated identity may be shared, but one fetch identity may not
Two credential bindings SHALL NOT declare the same QUALIFIED `fetch_identity` — the same identity name in the same issuing namespace, compared on `(provider, identity_namespace, fetch_identity)` and NEVER qualified by `vault` — while naming DIFFERENT consumers; the validator SHALL report `shared-fetch-identity` when they do. This does not restate the obligation that each consuming system reaches a shared operated identity through its own binding — it makes that obligation CHECKABLE, by giving the record the field whose collision is the obligation's exact violation.

ONE SYSTEM REACHING TWO CREDENTIALS THROUGH ONE FETCH IDENTITY IS NOT THIS
FAULT and SHALL NOT be reported as one. A consumer holds one identity against
the store and legitimately fetches more than one secret with it; the fault is
one identity serving TWO CONSUMERS, because that is what makes revocation
non-separable and the access log unable to say which system read the secret.

WHERE THE RECORD CANNOT ADJUDICATE, THE VALIDATOR SHALL NOT INVENT A VERDICT.
Two bindings sharing a fetch identity with a consumer undeclared on either side
are not comparable on this rule, and SHALL raise no `shared-fetch-identity`
finding; the `binding-authority-undeclared` warning already stands on those bindings and
is the correct report. Silence on the shared identity is therefore never a
clearance — it is the warning saying the record does not yet answer.

SAMENESS IS DECIDED ON THE IDENTITY NAMESPACE, NOT ON THE STRING AND NOT ON THE
VAULT. Two bindings naming `runtime_identity` against different providers are two
identities that happen to share a label, and refusing them would be a false
collision invented by the checker. Two bindings naming ONE principal under ONE
provider are one authority WHETHER OR NOT they point at the same vault, and a
rule that let the vault split them would report nothing on the exact record this
requirement exists to refuse. The comparison is therefore always determinate:
`provider` is required by the published shape, so the identity key is always
fully formed and no case arises in which the record cannot say.

WHERE `identity_namespace` IS ABSENT THE COMPARISON FALLS BACK TO `provider`
ALONE, AND THAT FALLBACK ERRS TOWARD REPORTING. An undeclared namespace does not
excuse the comparison: two identically-named principals under one provider with
no namespace declared SHALL still be reported, because the record does not say
they are different and a rule for catching a shared authority may not read
silence as distinctness. Declaring DISTINCT namespaces is what makes them
distinct, and it is a real escape rather than a rhetorical one precisely because
the field now exists to carry it.

THE TWO FALLBACKS POINT THE SAME WAY, WHICH IS THE PROPERTY TO CHECK. The secret
comparison falls back to the BARE reference where `vault` is unestablished, so it
refuses rather than clears; the identity comparison falls back to `provider`
alone where `identity_namespace` is unestablished, so it reports rather than
clears. Neither absence buys silence. An earlier draft of this packet had these
two pointing OPPOSITE ways — the secret side clearing on an omitted field while
the identity side reported — and that incoherence is corrected here rather than
left for a reader to notice.

WHAT QUALIFICATION DOES NOT BUY, said plainly. A binding that MISDECLARES its
provider escapes the comparison, and no check here detects that, because nothing
reads the store. Qualification removes false refusals; it does not defend against
a false record, which stays exactly what the record-is-an-assertion limit above
already says it is.

THE COMPARISON IS SCOPED TO ONE TEMPLATE DOCUMENT, and that bound SHALL be
recorded rather than implied away. Bindings held in separate documents are not
compared, so an estate that splits two consumers across two files defeats this
rule without any record saying so. Cross-document comparison needs a scan the
validator does not perform and is named as owed to a successor.

#### Scenario: Two consuming systems share one fetch identity
- **WHEN** two bindings name different consumers and declare the same fetch identity under the same provider
- **THEN** the validator MUST report `shared-fetch-identity`, because one authority is serving two systems

#### Scenario: One principal granted on two different vaults
- **WHEN** two bindings name different consumers and declare the same fetch identity under the same provider, but point at DIFFERENT vaults
- **THEN** the validator MUST still report `shared-fetch-identity`, because one principal granted on two vaults is one authority and the vault it reaches does not divide it
- **AND** a rule that qualified the identity by vault would report nothing here, which is why it does not

#### Scenario: The same identity label under different providers
- **WHEN** two bindings name different consumers and declare the same fetch-identity string, but their providers differ
- **THEN** no collision is reported, because the label names a principal in each provider's own namespace and the two are not the same authority

#### Scenario: Two namespaces of one provider hold a same-named principal
- **WHEN** two bindings under the same provider declare the same fetch identity but DISTINCT `identity_namespace` values
- **THEN** no collision is reported, because the record now states that the two principals are issued by different directories and are two authorities

#### Scenario: A same-named principal with no namespace declared
- **WHEN** two bindings under the same provider declare the same fetch identity and neither declares an `identity_namespace`
- **THEN** the validator REPORTS the collision, because the record does not say the two are distinct and silence is not read as distinctness
- **AND** the remedy is to declare the namespaces, which the shape now carries — the escape is a field the operator can actually use rather than an instruction with nowhere to record it

#### Scenario: Two consuming systems each hold their own
- **WHEN** two bindings name different consumers and declare different fetch identities
- **THEN** they validate, and the record shows two authorities rather than asserting them

#### Scenario: One system reaches two credentials
- **WHEN** two bindings name the SAME consumer and declare the same fetch identity
- **THEN** they validate, because one consumer holding one store identity across its own credentials is not the shared-authority fault

#### Scenario: A shared fetch identity with the consumer undeclared
- **WHEN** two bindings declare the same fetch identity and at least one of them names no consumer
- **THEN** no `shared-fetch-identity` finding is raised, because the record cannot distinguish one consumer from two
- **AND** the `binding-authority-undeclared` warning stands on the binding that omitted its consumer, so the silence is not read as a clearance

#### Scenario: Two consumers are split across two documents
- **WHEN** two bindings sharing one fetch identity are held in separate template documents
- **THEN** the rule does not compare them, and that document scope is a recorded limit of the check rather than a statement that the estate conforms

### Requirement: A shared secret reference is conforming only where the record shows one requirement and distinct authorities
A shared QUALIFIED `secret_ref` — the same secret name under the same `provider` and the same `vault` — SHALL remain a `shared-secret-identity` refusal EXCEPT where every binding sharing it declares the SAME `requirement_id` AND pairwise-DISTINCT `consumer` AND pairwise-DISTINCT QUALIFIED `fetch_identity` values — compared on `(provider, identity_namespace, fetch_identity)`, `vault` playing no part, EXCEPT that where ANY member of a compared pair omits `identity_namespace` the two SHALL be compared on `(provider, fetch_identity)` alone, and the exemption SHALL NOT open on an indeterminate qualification; where any of those three conditions is unmet or undeclared, the refusal stands exactly as it stood before this requirement existed. This is what lets the record carry a deliberately shared operated identity — one account, two systems, two authorities — without weakening the check that keeps two different credentials from collapsing into one.

THE EXEMPTION SHALL NOT BE KEYED ON DISTINCT CONSUMERS ALONE, and the reason is
executable rather than theoretical. The fault this check exists to catch — a
dispatch credential and a content-write credential resolved to one secret — HAS
distinct consumers: a zero-write serving tier and a privileged apply lane. Under
the dispatch-only separation requirement those two MUST also hold distinct
identities. So an exemption satisfied by distinct consumers and distinct fetch
identities would admit the exact record the check was written to refuse. Only
the SAME `requirement_id` separates one key serving TWO PURPOSES, which is the
fault, from one key serving TWO CONSUMERS OF ONE PURPOSE, which is the estate
shape.

THE DISPATCH AND CONTENT REFUSAL IS UNCHANGED BY THIS REQUIREMENT. Those two
bindings resolve two different credential requirements, so the exemption's first
condition is never satisfied for them, and the promoted dispatch-only separation
requirement keeps its full force with none of its text modified.

NOTHING PREVIOUSLY REFUSED BECOMES CONFORMING BY DEFAULT. A record declaring
none of the exemption's three declared conditions is adjudicated exactly as before, because every
condition of the exemption is a positive declaration that such a record does not
make. The exemption is opened by saying more, never by saying nothing.

THE EXEMPTION IS NEVER DECIDED ON AN INDETERMINATE QUALIFICATION, AND THAT IS A
STATED RULE RATHER THAN A CONSEQUENCE OF THE GROUPING. An earlier revision
argued it followed from the grouping alone: members of a group share the
qualified secret key, so `provider` is equal, so the comparison reduces to the
namespace and the identity name, "both of which the record either states or does
not." **That reasoning was wrong, and the record it lets through is the one this
requirement exists to refuse.** Two bindings on one secret and one requirement,
with distinct consumers and the SAME `fetch_identity`, with
`identity_namespace` declared on ONE SIDE ONLY, have DIFFERENT triples — so a
literal reading calls them "distinct", opens the exemption, and DROPS the
shared-secret refusal entirely. A one-sided namespace does not make two
identities distinct; it makes their distinctness UNKNOWN, and the earlier
sentence mistook the second for the first.

So the rule is written where the comparison is made, in the same either-side
form the collision rule already uses: where any member of a compared pair omits
`identity_namespace`, the identities are compared on `(provider, fetch_identity)`
alone. Two bindings naming ONE identity are then not distinct, the exemption
does not open, and the refusal stands. A reader checking whether a record could
claim the exemption while its authority distinctness is merely unestablished
will find that it cannot — now because a rule says so, not because a paragraph
asserted it.

THE SECRET COMPARISON IS QUALIFIED TOO, ON ITS OWN NAMESPACE RATHER THAN ON THE
IDENTITY'S. `secret_ref` is a name in a VAULT, so two bindings carrying `api-key`
against two different vaults are two secrets and refusing them was always a false
collision — a defect this requirement inherits rather than introduces, since the
published check groups by the bare reference today. Fixing it in one place and
not the other would leave the exemption resting on a qualified identity test and
an unqualified secret test, which is the shape that lets one half of a rule
contradict the other. The two keys are therefore both qualified and DELIBERATELY
DIFFERENT: `(provider, identity_namespace, fetch_identity)` for the authority,
and `(provider, vault, secret_ref)` for the secret — the first falling back to
`provider` alone where the namespace is undeclared, the second falling back to
the BARE reference where the vault is undeclared, and BOTH fallbacks erring
toward reporting.

`vault` IS OPTIONAL, SO THE SECRET COMPARISON — AND ONLY THAT ONE — CAN BE
INDETERMINATE, AND WHERE IT IS THE GROUPING SHALL FALL BACK RATHER THAN
DISSOLVE. Where any member of a matching `(provider, secret_ref)` set omits
`vault`, the qualification is not established for that set, and the validator
SHALL group that set by the BARE `secret_ref` — the grouping in force before this
requirement existed — and adjudicate it on those terms. `authority-scope-indeterminate`
SHALL be raised as a WARNING that ACCOMPANIES whatever verdict the fallback
reaches; it SHALL NOT REPLACE a refusal. The identity comparison never reaches
this state, because `provider` is required.

THE FALLBACK IS WHAT KEEPS THE REFINEMENT ADDITIVE, AND IT IS NOT A CAUTION —
IT IS A CORRECTION. Qualifying unconditionally does not merely fail to catch a
case: it TAKES AWAY a refusal that stands today. A record with two bindings on
one provider and one `secret_ref`, with `vault` declared on one side only,
is REFUSED by the published check now; under an unconditional qualified key its
group would split, nothing would collide, and a warning would stand where an
error stood. The packaged dispatch/content negative is ONE OPTIONAL LINE from
being exactly that record. Falling back where the qualification is unestablished
keeps every genuine narrowing this refinement exists for — two declared vaults,
two declared providers — while refusing nothing that is refused today, which is
the property the ADDITIVE classification depends on.

SILENCE IS NEVER THE INDETERMINATE VERDICT. Because the fallback adjudicates
rather than abstains, an unestablished qualification produces a refusal AND a
warning, or a clean record AND a warning — never a warning alone standing in for
a check that did not run.

A RECORD THAT FAILS THIS RULE AND THE SHARED-FETCH-IDENTITY RULE TOGETHER SHALL
HEAR BOTH, and the overlap is deliberate rather than an unnoticed duplication.
Bindings sharing a secret reference, a requirement and a fetch identity fail the
distinctness condition here AND collide there, and the two findings answer
different questions — whether this shared key is accounted for, and whether this
authority is shared. Collapsing them would make a record with two defects report
one.

AN EXEMPTION MARKER WHOSE ONLY EFFECT IS TO SILENCE THE CHECK SHALL NOT BE
ADDED. A boolean that turns a refusal off asserts nothing a reader can verify
and reads as governance while binding no one — the defect this capability's
closed issuance-precondition vocabulary already refuses in the same schema, and
the species of the ratified refusal to carry an escrow discriminator on an axis
that cannot express it. The discriminator must be a fact the record would carry
anyway.

#### Scenario: Two systems consume one operated identity
- **WHEN** two bindings share a secret reference, declare the same requirement, and declare distinct consumers and distinct fetch identities
- **THEN** they validate, because the record now shows one credential reached by two authorities

#### Scenario: A dispatch credential reuses the content credential's secret
- **WHEN** a dispatch binding and a content-write binding share one secret reference under the same provider and vault
- **THEN** the validator MUST still report `shared-secret-identity`, because they resolve different credential requirements and the exemption's first condition is unmet

#### Scenario: The same secret label in two different vaults
- **WHEN** two bindings carry the same secret-reference string but name different vaults, or different providers
- **THEN** no collision is reported, because they name two secrets that share a label rather than one secret reached twice

#### Scenario: The record cannot establish which vault a secret is in
- **WHEN** two bindings match on provider and on the bare secret reference, and one declares a vault while the other omits it
- **THEN** the set is grouped by the BARE secret reference — the grouping in force before this requirement — so the verdict is whatever that grouping reaches, and a shared reference is still REFUSED
- **AND** `authority-scope-indeterminate` is raised as a WARNING that ACCOMPANIES that verdict rather than replacing it
- **AND** the identity comparison never reaches this state, because `provider` is required by the published shape

#### Scenario: The packaged dispatch negative loses one optional line
- **WHEN** the packaged dispatch/content negative has `vault` deleted from one of its two bindings
- **THEN** it is STILL REFUSED, because the fallback grouping adjudicates it on the bare reference exactly as the published check does today
- **AND** a qualified key applied unconditionally would have turned it green, which is why the fallback is a condition of this requirement rather than a refinement of it

#### Scenario: Distinct consumers and identities but different requirements
- **WHEN** two bindings share a secret reference and declare distinct consumers and distinct fetch identities, but name different requirements or name none
- **THEN** the refusal stands, because distinct consumers alone is the discriminator this requirement refuses

#### Scenario: The exemption is claimed on a one-sided namespace
- **WHEN** two bindings share a secret reference and a requirement, name distinct consumers, declare the SAME `fetch_identity`, and only one of them declares an `identity_namespace`
- **THEN** the exemption does NOT open and `shared-secret-identity` is REFUSED, because the pair is compared on `(provider, fetch_identity)` where either side omits the namespace and is therefore not distinct
- **AND** a one-sided namespace makes distinctness UNKNOWN rather than established, so it may not buy the exemption that distinctness would

#### Scenario: A record declaring none of the new fields
- **WHEN** two bindings share a secret reference and declare no consumer, fetch identity or requirement
- **THEN** the verdict is exactly what it was before this requirement existed, because the exemption opens only on positive declarations

#### Scenario: A marker is proposed to switch the check off
- **WHEN** a discriminator is proposed whose only effect is to suppress `shared-secret-identity`
- **THEN** it MUST be rejected, because a declaration that asserts nothing verifiable reads as governance while binding no one
