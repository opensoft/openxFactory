## ADDED Requirements

### Requirement: Current publication metadata is explicit

A registry body that CLAIMS PRIMARY-SOURCE VERIFICATION SHALL carry the complete
current-publication record — a stable body id, steward, term kind, current
version, primary source URL, verification date, and confidence — and the registry
SHALL keep such a body distinguishable from one whose record predates
verification. The verification date IS the claim: a body that declares one is
asserting that its current-publication facts were read from the body's own
material on that date, and a body that declares none is making no such assertion
and SHALL NOT have one invented for it. Historical body ids and records SHALL
remain resolvable and SHALL NOT be silently renamed.

**Why the obligation is keyed to the claim and not to `status: current`.**
Measured on the registry this requirement governs, 2026-09-03: of 45 bodies, 32
carry `status: current` and exactly 3 carry a verification date — the three this
change read against primary sources. The other 29 are the entries the registry's
own header discloses as "drawn from working knowledge, not verified against each
body's current publication", an asymmetry it calls "deliberate rather than
hidden". An obligation written over `status: current` would therefore be FALSE of
29 records on the day it was promoted, and the only two ways to make it true are
to backfill 29 verification dates nobody performed — which is the fabrication the
sourcing caveat exists to forbid — or to demote records whose currency is not in
doubt. Keying the obligation to the CLAIM makes it true of every record that
makes one, enforceable on every record added or amended from here, and silent
about records that assert nothing. Re-verifying the 29 is real work owed to a
successor change; it is named here rather than pretended away.

#### Scenario: A body claiming verification carries a complete source record

- **WHEN** a registry body declares a verification date
- **THEN** it carries `current_version`, `source_url` and `confidence`, each
  tied to that body's own primary source

#### Scenario: A half-verified record is rejected

- **WHEN** a body declares a verification date but omits its current version,
  its primary source URL, or its confidence
- **THEN** registry validation rejects the record with a named finding
- **AND** the omission is never repaired by dropping the verification date to
  move the body out of scope

#### Scenario: An unverified legacy record is left as it stands

- **WHEN** a body carries `status: current` and declares no verification date
- **THEN** registry validation reports nothing against it
- **AND** no verification date, current version or confidence is invented for it

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
