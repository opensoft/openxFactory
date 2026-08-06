# consent-instrument Delta: The Root Of The Authority Chain

## ADDED Requirements

### Requirement: The Instrument Is A Neutral Governed Record
Every domain's rung-1↔rung-2 consent instrument SHALL instantiate the
neutral `xfactory_consent_instrument` shape: parties identified by
party-ladder rung — including third-party estate hosts whose
authorization a delegation needs — scope with stated out-of-scope,
delegation clauses carrying the technical access shape, an autonomy
position, a revocation right with SLA, signed-original custody, a status
lifecycle, and a declared instrument class.

#### Scenario: Existing instances conform by declaration

- **WHEN** a domain already holds a schema'd instrument (the Ledgerx
  engagement consent record, the Medx patient consent record)
- **THEN** it declares conformance with field and lifecycle mappings
- **AND** the record is not rewritten

#### Scenario: An estate host is a party, not a footnote

- **WHEN** a delegation requires authorization from a third party hosting
  the subject's estate (the Medxcorp pattern)
- **THEN** that party appears in the instrument's parties with its rung
- **AND** its authorization is part of the executed instrument, not an
  out-of-band arrangement

### Requirement: The Instrument Is The Authority-Chain Root
A consent citation on an authority-bearing artifact SHALL resolve to an
executed instrument whose purposes cover the requested purpose; an
artifact citing a non-existent, non-executed, or terminated instrument is
nonconformant.

#### Scenario: A grant's citation resolves

- **WHEN** a credential grant carries a consent citation
- **THEN** the citation resolves to an instrument in status `executed`
  or `amended`
- **AND** the grant's purpose resolves into the instrument's purposes

#### Scenario: Termination breaks the chain

- **WHEN** the cited instrument is `terminated`
- **THEN** the citation no longer verifies
- **AND** dependent artifacts fall due under the cascade requirement

### Requirement: Domain-Owned Instrument-Class Registries Under Neutral Constraints
Each domain SHALL declare a CLOSED registry of its instrument classes,
and every class SHALL declare its custody-anchor kind and its
execution-evidence kind; the neutral contract constrains what a class
declares, never which classes a domain may have.

#### Scenario: Both proven registries conform as-is

- **WHEN** Medx declares its four medical classes or Ledgerx declares
  `internal_beta_authorization`
- **THEN** each class is admitted by declaring custody-anchor and
  execution-evidence kinds
- **AND** no neutral class vocabulary constrains the domain's naming

#### Scenario: A class without evidence declaration is refused

- **WHEN** a domain registry entry omits the custody-anchor kind or the
  execution-evidence kind
- **THEN** the registry is nonconformant

### Requirement: The Lifecycle Enum Is Closed With Declared Aliases
The instrument status SHALL be the closed five-state lifecycle `draft →
pending_signatures → executed → amended → terminated`; a domain spelling
outside the enum maps via an alias DECLARED at conformance time, and a
class may skip `pending_signatures` only when its class declaration says
so — class-appropriate skipping, never silent.

#### Scenario: A domain alias maps at conformance time

- **WHEN** the Ledgerx record carries `status: active`
- **THEN** its conformance declaration maps `active` → `executed`
- **AND** the underlying record keeps its domain spelling

#### Scenario: A non-signature class enters executed directly

- **WHEN** a `portal_acceptance` instrument is accepted
- **THEN** it may enter `executed` without `pending_signatures` because
  its class declares no signature phase
- **AND** an undeclared skip is nonconformant

### Requirement: Authority Basis Is First-Class
The instrument SHALL carry the authority basis of its execution
first-class (the Medx enum precedent: `direct`, `guardian`, `delegated`,
`court_ordered`); signer and execution mechanics belong to domain policy,
and distinct signers across rungs SHOULD be used in related-party
engagements.

#### Scenario: A related-party engagement stays disclosed-and-consented

- **WHEN** one person controls multiple rungs of an engagement (the Meds
  Rx case)
- **THEN** the executed instrument records the authority basis per party
- **AND** a shared signer across rungs is a recorded SHOULD deviation,
  not a silent one

### Requirement: Amendments Are Transitions, Never New Instruments
An amendment SHALL be a status transition carrying its delta on the
existing instrument; a new instrument referencing a parent is
nonconformant, so every citation target stays stable across amendments.

#### Scenario: An amendment preserves the citation target

- **WHEN** an executed instrument's scope changes (the Ledgerx "AR by
  amendment" case)
- **THEN** the instrument transitions to `amended` carrying the delta
- **AND** every existing consent citation still resolves to the same
  instrument identifier

### Requirement: The Neutral Check Verifies Purpose Resolution Only
The canonical validator SHALL verify that a requested purpose resolves
into the record's purposes and that those resolve into the
domain-declared purpose model; it SHALL NOT re-check technical access
shapes on delegation clauses, which remain credential-contracts
enforcement.

#### Scenario: Purpose resolution passes and fails mechanically

- **WHEN** a requested purpose appears in (or resolves through) the
  record's purposes under the domain purpose model
- **THEN** the executed-instrument check passes
- **AND** a purpose that cannot resolve is a finding naming the missing
  link

#### Scenario: One enforcement truth per concern

- **WHEN** a delegation clause's technical access shape disagrees with a
  credential grant
- **THEN** that is a credential-contracts finding, not a
  consent-instrument finding

### Requirement: Termination Cascades Through Declared Dependent References
The instrument SHALL carry first-class dependent-artifact references
(derived consent profiles, credential grants, adapter activations), and
on termination or withdrawal each reference falls due under the record's
revocation SLA with an evidence obligation; cascade mechanics stay in the
owning contract families.

#### Scenario: Termination raises the whole chain

- **WHEN** an instrument enters `terminated`
- **THEN** every declared dependent reference must show cascade evidence
  within the record's revocation SLA
- **AND** an undeclared dependent discovered later is a conformance
  finding against the instrument, not the dependent

### Requirement: The Signed Original Never Enters A Product Repo
The signed original SHALL be referenced only by opaque locator plus
sha256 (the document-cataloging custody pattern); embedding original
content in a product repo is nonconformant, while record-INSTANCE
placement (repo tenant tree vs governed store) is declared domain policy
driven by data sensitivity.

#### Scenario: Custody is a pointer, not a payload

- **WHEN** an instrument record is committed
- **THEN** it carries locator + sha256 for the signed original and no
  original content
- **AND** Medx's governed-store mandate and Ledgerx's tenant-tree
  placement both conform because each is declared domain policy

### Requirement: The Consent-Profile Mapping Is Declared
An instrument whose engagement implies data-consent SHALL declare its
mapping to the memory-gateway consent-profile family — the instrument
authorizes ACTION, the derived profile governs DATA — and an instrument
with no data-consent implication declares that explicitly rather than
omitting the mapping.

#### Scenario: The Medx derivation is the reference

- **WHEN** a patient consent record derives a memory-gateway consent
  profile
- **THEN** the instrument declares the derived profile as a dependent
  reference with its derivation basis
- **AND** an instrument that declares `data_consent: none` carries no
  derived profile and the absence is conformant
