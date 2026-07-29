# omnigent-domain-overlay Delta: Crystallized Executors And Rung Ceilings

## ADDED Requirements

### Requirement: Crystallized Executor Bindings Conserve Authority
A worker class marked `crystallized` SHALL carry a `capability_ref`, an
`automation_rung` from the frozen L0–L6 vocabulary, a
`replaces_configuration` reference to the worker configuration whose work
the capability absorbs, and a young-capability throttle schedule; such a
class SHALL map to one of the existing five neutral archetypes (the
archetype vocabulary is unchanged), SHALL declare the six-boolean
permission matrix like any worker class — so the promoted constitutional
requirement (`execute_final_action` and `access_secrets` false for every
worker class) binds it verbatim — and its effective permissions and
credential requirement families MUST be a subset of the replaced
configuration's, checked mechanically, never by judgment.

#### Scenario: A conforming crystallized binding validates

- **WHEN** an overlay declares a crystallized class mapped to `generate`,
  with all six booleans declared, both constitutional booleans false,
  permissions and credential families a subset of its
  `replaces_configuration`, and a throttle schedule
- **THEN** the overlay validates

#### Scenario: Widening is rejected mechanically

- **WHEN** a crystallized class declares any permission true, or any
  credential family, that its `replaces_configuration` does not hold
- **THEN** validation MUST reject the overlay — crystallization is never a
  privilege-escalation path

#### Scenario: No new archetype may be invented

- **WHEN** a crystallized class declares an archetype outside the five
  neutral values
- **THEN** validation MUST reject the overlay

#### Scenario: A binding without its baseline is rejected

- **WHEN** a crystallized class omits `replaces_configuration`
- **THEN** validation MUST reject the overlay — the conservation subset
  check has no baseline without it

### Requirement: Rung Ceilings Are Declared Per Task Category
A `rung_ceilings` declaration SHALL list, per task category, a ceiling
from the L0–L6 vocabulary and a stated reason, and where a family's task
category carries no declared ceiling the effective ceiling SHALL default
to L3: the code rungs (L4–L6) are reachable only through an explicit,
reasoned overlay declaration, which is where a domain's regulatory
posture lives.

#### Scenario: A declared ceiling binds decisions

- **WHEN** an overlay declares ceiling L3 with a reason for a task
  category
- **THEN** a crystallization decision for a family in that category MUST
  NOT value or fund above L3

#### Scenario: Undeclared means the conservative default

- **WHEN** a family's task category has no declared ceiling
- **THEN** the effective ceiling is L3
- **AND** funding L4–L6 requires the overlay to declare a ceiling first

#### Scenario: A ceiling without a reason is rejected

- **WHEN** an overlay declares a rung ceiling with no reason
- **THEN** validation MUST reject the overlay
