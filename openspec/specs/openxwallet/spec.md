# openxwallet Specification

## Purpose
TBD - created by archiving change add-openxwallet. Update Purpose after archive.
## Requirements
### Requirement: A wallet is a key, never a record of a key

openxFactory SHALL define a neutral wallet as a signing key anchored to a
decentralized identifier and held by a HOLDER, where a holder is any
subject class the family recognises — a person, a practitioner, an
organisation, or an agent. The wallet record carries the holder's
identifier, a reference to the key, and the key's custody model; it never
carries key material, and no capability may require key material to be
disclosed to it.

#### Scenario: the record references, never contains

- WHEN a wallet record is validated
- THEN it carries a key reference and a declared custody model
- AND a record containing private key material is a validation failure

#### Scenario: holders are not restricted to one subject class

- WHEN a domain declares a wallet holder
- THEN the holder may be a person, practitioner, organisation, or agent
- AND no requirement in this capability assumes a particular class

### Requirement: Authority travels as attenuated grants, never as keys

openxFactory SHALL express every authority a wallet confers as a capability
GRANT rather than as access to the key itself, because a raw key can be
neither expired nor revoked and a shared key destroys attribution. A grant
names its audience, its scope, and its expiry; derivation from a grant is
MONOTONICALLY NARROWING, so a derived grant may reduce scope or lifetime
and may never widen either.

#### Scenario: a raw key is never the unit of access

- WHEN a holder authorises another party to act
- THEN a grant is issued naming audience, scope and expiry
- AND handing over the key itself is refused as unrepresentable

#### Scenario: attenuation only narrows

- WHEN a grant is derived from a parent grant
- THEN its scope and lifetime are within the parent's
- AND a derived grant exceeding its parent in either is invalid

### Requirement: Use requires proof of possession, not presentation

openxFactory SHALL require that exercising a grant carries a signature from
the holder's wallet key over the request, so that possession of the grant
alone is insufficient. A grant presented without proof of possession is
refused, and the refusal names the missing proof rather than the missing
grant, because the grant was supplied and is not what was lacking. A
verification failure SHALL be recorded distinctly from an unauthenticated
request, since the two describe different events.

#### Scenario: a stolen grant is useless

- WHEN a grant is presented without a verifiable signature from its audience
- THEN the request is refused with the missing proof named
- AND no authority is conferred by presentation alone

#### Scenario: failed verification is not absence

- WHEN a signature is present but does not verify
- THEN the failure is recorded as a verification failure
- AND that record remains distinguishable from an unauthenticated request

### Requirement: Custody is declared and bounds what a signature evidences

openxFactory SHALL require every wallet to declare its key-custody model
from a closed set, SHALL state what each model evidences, and SHALL cap the
authority a wallet may hold by that model. A signature proves only what its
custody permits: a key readable by the holder's own execution context
evidences that the ENVIRONMENT acted, and only custody isolating the key
from that context evidences that the HOLDER acted. These SHALL NOT be
presented as equivalent.

#### Scenario: custody caps authority

- WHEN a wallet requests authority beyond what its custody model evidences
- THEN the request is refused with the custody ceiling named
- AND raising authority requires changing custody, not asserting trust

#### Scenario: the audit says what was evidenced

- WHEN an act is audited
- THEN the record carries the custody model in force at the time
- AND a reader can tell whether the holder or its environment was evidenced

### Requirement: Every exercise is key-attributed

openxFactory SHALL record, for every exercise of a grant, the key that
presented it alongside the grant and the act, so attribution is
cryptographic rather than inferred from a shared account. An act
attributable only to a shared credential SHALL be recorded as
unattributed rather than assigned to a holder.

#### Scenario: shared credentials do not launder attribution

- WHEN an act reaches an external platform through a shared service credential
- THEN the presenting wallet key is recorded as the actor
- AND the shared credential is recorded as transport, never as the actor

#### Scenario: an unattributable act says so

- WHEN no wallet key can be established for an act
- THEN the act is recorded as unattributed
- AND it is not assigned to a holder on the strength of the credential used

### Requirement: Revocation propagates through the chain

openxFactory SHALL make revocation effective through derivation: revoking a
grant revokes everything derived from it, and revoking a holder's standing
revokes that holder's outstanding grants, in both cases without waiting for
expiry. A capability consuming grants SHALL check revocation at exercise
rather than trusting issuance.

#### Scenario: revoking a parent kills the chain

- WHEN a grant is revoked
- THEN every grant derived from it is revoked at the same moment
- AND an exercise attempt against any of them is refused

#### Scenario: revocation is checked at use

- WHEN a grant is exercised after its holder's standing was revoked
- THEN the exercise is refused
- AND issuance-time validity is not accepted as evidence of current validity

### Requirement: Distinct-holder constraints are expressible

openxFactory SHALL allow a consuming capability to require that the holder
exercising a grant for an act is DISTINCT from the holder recorded for a
named prior act on the same object, so that segregation of duties is
expressible in the grant model rather than reimplemented per domain. The
constraint is available, never implied: a capability that does not declare
it is not subject to it.

#### Scenario: a domain requires two distinct holders

- WHEN a capability declares a distinct-holder constraint between two acts
- THEN an exercise naming the same holder for both is refused with the
  constraint named
- AND the prior act's recorded holder is the comparison basis

#### Scenario: the constraint is opt-in

- WHEN a capability declares no distinct-holder constraint
- THEN grants are exercised without one
- AND no default distinctness is inferred

### Requirement: The capability is an authority control, never an identity substrate

openxFactory SHALL keep wallets composable and optional for domains: a
wallet SHALL NOT become a prerequisite for reconstructing a record,
resolving a subject, or operating a domain, and a wallet identifier SHALL
NOT become a subject identifier. This preserves the ratified constraints in
MedxFactory's `patient-identity-and-assembly` (a wallet address is not
identity proof) and `patient-snapshot-ledger-custody` (custody stays
wallet neutral and reconstructable with no wallet available).

#### Scenario: a domain operating without wallets is conformant

- WHEN a domain adopts no wallets
- THEN its records remain reconstructable and its subjects resolvable
- AND no capability refuses it for the absence

#### Scenario: a wallet identifier never becomes a subject identifier

- WHEN a subject or record carries an optional wallet reference
- THEN the reference is attestation, not identity
- AND resolution treating it as the identifier is a validation failure

