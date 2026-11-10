## ADDED Requirements

### Requirement: Hosted connectivity product ownership

An approved openXsoft.com product repository SHALL own entitlement, managed provisioning, attachment lifecycle, hosted onboarding and catalog admission. T001 SHALL require its approved repository identity, owner, file scope, release path and verification command.

#### Scenario: A customer cancels a factory subscription

- **WHEN** a factory subscription ends and the customer has an independent Hosted Headscale entitlement
- **THEN** the affected factory access SHALL be revoked
- **AND** unrelated access and the independent network SHALL remain available

### Requirement: Hosted pilot domain ownership and profile qualification

The pilot SHALL identify an accepting DomainxFactory maintainer and a synthetic profile before domain qualification. Customer catalog admission SHALL require current evidence for the exact domain and profile revision.

#### Scenario: A profile lacks current qualification

- **WHEN** the catalog receives missing, stale, or wrong-domain evidence
- **THEN** it SHALL deny customer catalog admission for that profile
- **AND** the common pilot SHALL provide no substitute for profile-specific evidence
