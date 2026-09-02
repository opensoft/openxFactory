# standards-body-registry Specification

## Purpose
TBD - created by archiving change update-standards-body-current-publications. Update Purpose after archive.
## Requirements
### Requirement: Current publication metadata is explicit

The standards-body registry SHALL identify the current publication for every
body marked current with a stable body id, steward, term kind, current version,
primary source URL, verification date, and confidence. Historical body ids and
records SHALL remain resolvable and SHALL NOT be silently renamed.

#### Scenario: A current body has a complete source record

- **WHEN** a registry body has `status: current`
- **THEN** it carries `current_version`, `source_url`, `confidence`, and a
  verification date tied to a primary source

#### Scenario: A historical ITIL id remains resolvable

- **WHEN** a consumer resolves the historical `itil4` id
- **THEN** the registry returns the preserved ITIL 4 record rather than
  redirecting it to `itil5`

### Requirement: Licensing posture and overrides are distinguishable

Each registry body SHALL state whether its material is permitted in product
configuration, prohibited, or conditionally permitted. An operator override that
disagrees with primary licensing evidence SHALL carry the approver, decision
date, rationale, conflicting source, and an explicit unverified status; the
override SHALL NOT be rendered as steward-granted permission.

#### Scenario: An unverified SFIA override remains visibly exceptional

- **WHEN** the SFIA record carries a product-config permission override without
  written steward permission
- **THEN** the registry preserves the official restrictive source and records
  the operator override as unverified with its named approver and date

#### Scenario: An incomplete override is rejected

- **WHEN** an override omits its approver, date, rationale, or conflict source
- **THEN** registry validation rejects the record with a named finding

### Requirement: APQC conditional reuse carries attribution

The APQC PCF 8.0 registry record SHALL identify its current publication and
conditional reuse grant. Any later domain configuration that embeds APQC terms
or identifiers SHALL carry the required APQC attribution and SHALL state that
the crosswalk is descriptive rather than an authority grant.

#### Scenario: APQC current metadata is accepted

- **WHEN** the APQC record identifies Cross-Industry PCF 8.0 and its primary
  source
- **THEN** validation accepts it only when the conditional attribution
  requirement is present

#### Scenario: A crosswalk never becomes worker authority

- **WHEN** a domain maps a worker to an APQC process term
- **THEN** the mapping remains descriptive and does not change the worker's
  archetype, permissions, credential tier, or terminal-action authority

### Requirement: Registry ids resolve for descriptive crosswalks

A terminology crosswalk SHALL reference only body ids present in the standards-
body registry, with at most one mapping per body for a worker. A missing,
renamed, or unregistered body id SHALL fail closed rather than being treated as
an omitted mapping.

#### Scenario: A registered current id resolves

- **WHEN** a domain crosswalk references `itil5`, `sfia`, or `apqc_pcf`
- **THEN** the registry resolves the id and exposes its term kind and licensing
  posture to the validator

#### Scenario: An unknown body id fails closed

- **WHEN** a domain crosswalk references a body id absent from the registry
- **THEN** validation rejects the crosswalk with an unresolved-body finding

