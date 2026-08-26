# crystallization-consent Delta: Three Tiers And The Approval Braid

## ADDED Requirements

### Requirement: Consent Is Three Separately Grantable Tiers
Crystallization consent SHALL consist of three independently grantable,
independently revocable tiers with default deny: `episode_use` (mining a
tenant's solved runs into families, forecasts, and corpora; per tenant),
`automation` (serving a family category without fresh AI judgment; per
family category), and `pooling` (cross-tenant aggregation; defined in the
vocabulary now, with no consumer until the cross-tenant wave).

#### Scenario: Absence is denial

- **WHEN** no `crystallization_consent` grant exists for a tier
- **THEN** every consumer of that tier MUST behave as if consent were
  explicitly denied

#### Scenario: The pooling tier is frozen but consumer-less

- **WHEN** a pooling-tier grant is recorded this wave
- **THEN** the record validates against the vocabulary
- **AND** no wave-one consumer may act on it

### Requirement: Automation Consent Is Scoped And May Carry Conditions
An `automation` grant SHALL be scoped to a family category, never global,
and MAY carry a declared condition (for example a human spot-check rate)
that consuming decisions and, later, dispatch MUST honor as part of the
grant's meaning.

#### Scenario: A category grant does not leak

- **WHEN** a tenant grants `automation` for family category `doc-workflow`
- **THEN** a decision funding a family in a different category MUST NOT
  cite that grant

#### Scenario: A condition travels with the grant

- **WHEN** an `automation` grant carries a spot-check condition
- **THEN** any decision citing the grant MUST record the condition among
  its proof obligations

### Requirement: Subject-Affecting Automation Is Subject-Visible
Provenance SHALL be visible on the subject-facing surface where a
crystallized capability's work is subject-affecting, the subject consent
path applies there, and automation consent by the tenant alone SHALL NOT
suffice for subject-affecting family categories.

#### Scenario: A subject-affecting category needs the subject path

- **WHEN** a family category is declared subject-affecting and only a
  tenant `automation` grant exists
- **THEN** a decision funding that family MUST be rejected until the
  subject-consent obligation is recorded

### Requirement: The Approval Braid Cannot Be Collapsed
Funding SHALL require all three strands — the Domain's fitness approval
(spec quality, corpus adequacy, ceiling), the Tenant's money-and-policy
approval (budget or clearance plus the consent tiers), and the Subject
transparency obligations where applicable — and no single layer's approval
SHALL be able to substitute for another's.

#### Scenario: Fitness alone cannot fund

- **WHEN** a decision carries the Domain fitness reference but no tenant
  budget/consent references
- **THEN** the decision is invalid and MUST be rejected

#### Scenario: Money alone cannot fund

- **WHEN** a decision carries tenant budget and consent references but no
  Domain fitness reference
- **THEN** the decision is invalid and MUST be rejected
