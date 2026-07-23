# governed-derived-model

## ADDED Requirements

### Requirement: Conformance declaration

A domain factory SHALL declare each governed derived model family in a
single `xfactory_derived_model_conformance` declaration listing its
member object kinds with `role: model` or `role: scenario`, its
conformance `tier` (`governed` or `calibrated`), and all six dials
(identity, scope, truth_store, calibration source, promoting_authority,
person_modeling). Scenario members are optional; model members are not.

#### Scenario: family with model and scenario members

- WHEN a domain declares a family with one model kind and one scenario kind
- THEN the declaration validates only if both kinds exist in the domain's templates
- AND each member's role-specific invariants are checked

#### Scenario: model-only family

- WHEN a domain declares a family with no scenario member
- THEN the declaration is valid and scenario invariants are not required

### Requirement: Non-authoritative by construction

A conforming model object SHALL carry `authority_status` as the
single-value enum `[non_authoritative]`, and the domain SHALL NOT define
any mechanism that mutates a derived object into an authoritative one —
promotion happens only by creating a new object of a different kind
through the domain's review workflow.

#### Scenario: single-value authority enum

- WHEN the validator inspects a declared model kind's template
- THEN `authority_status` exists, is required, and enumerates exactly `non_authoritative`

#### Scenario: in-place authority promotion forbidden

- WHEN a template defines a transition that changes `authority_status`
- THEN validation fails with an authority-mutation finding

### Requirement: Full provenance

A conforming model object SHALL tag every fact with provenance — an
evidence trace with source references, or a declared assumption in a
required assumption register — and a domain MAY instead forbid
assumptions entirely by declaring the assumptions-forbidden form
(evidence trace with minimum one item plus a single-value
no-invented-facts enum).

#### Scenario: assumption-permitting form

- WHEN a model template permits assumption-tagged facts
- THEN an assumption register field is required on the template

#### Scenario: assumptions-forbidden form

- WHEN a model template declares the assumptions-forbidden form
- THEN the validator requires an evidence-trace field with min_items 1 and a single-value invented-facts `[none]` enum

### Requirement: Read-only truth store and zero action authority

A conforming model or scenario object SHALL carry single-value
`[read_only]` access to the family's declared truth store and
single-value `[none]` fields for every declared action-authority class,
and a scenario member SHALL bind to an immutable truth snapshot when the
declared truth store supports snapshots.

#### Scenario: action authority is unrepresentable

- WHEN the validator inspects a scenario kind's output status enum
- THEN no enum value represents an order, launch, posting, or other external action

### Requirement: Declared scope and cross-scope review

A conforming family SHALL declare `scope: domain | subject`, and the
domain SHALL route any data crossing that scope — inbound subject facts
into a domain-scoped model, or outbound subject-scoped intelligence to
another subject — through governed review.

#### Scenario: subject-scoped isolation declared

- WHEN a family declares `scope: subject`
- THEN the declaration names the isolation boundary (e.g. per_advertiser, per_client) consistent with the stack's tenancy isolation map

### Requirement: Human-gated promotion

A conforming scenario member SHALL express outputs only as hypotheses
(`hypothesis_proposed | no_signal | discarded`), and the family SHALL
name a human promoting authority through which any hypothesis becomes
action or truth.

#### Scenario: promoting authority declared

- WHEN a family is declared
- THEN `promoting_authority` names a human role resolvable in the domain's roles/authority model

### Requirement: Calibrated tier

A family declaring `tier: calibrated` SHALL name a designated
calibration-writer workflow distinct from the model and scenario kinds,
SHALL derive `confidence` from calibration history only, and SHALL
downgrade confidence and flag re-modeling on repeated refuted
calibrations.

#### Scenario: writer separation

- WHEN the validator inspects a calibrated family
- THEN the calibration-writer workflow is not a member of the family
- AND no model or scenario template grants itself calibration write access

### Requirement: Person-modeling declaration

A conforming family SHALL declare `person_modeling` as one of
`synthetic_only`, `aggregated_only`, `identified_organizations_only`, or
`identified_persons_under_policy`, and a declaration of
`identified_persons_under_policy` SHALL reference the domain policy that
authorizes it.

#### Scenario: identified persons require policy

- WHEN a family declares `person_modeling: identified_persons_under_policy`
- THEN validation fails unless the referenced domain policy document exists
