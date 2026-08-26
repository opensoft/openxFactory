# repo-boundary-governance Specification (delta)

## MODIFIED Requirements

### Requirement: Install repository scope
`Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, and `OpenXPKI-Install` SHALL be scoped to subsystem
install, operations, backup, restore, upgrade, verification, and disaster
recovery.

`Keycloak-Install` (`opensoft/Keycloak-Install`, pinned at
`installs/keycloak-install`) and `OpenXPKI-Install`
(`opensoft/OpenXPKI-Install`, pinned at `installs/openxpki-install`) were
admitted to the top-level xFactory aggregation on 2026-08-21 by the
`admit-install-repos-to-aggregation` change, which recorded path, remote,
visibility, exact validated commit, checkout, compatibility, update, and
rollback behavior for each — the separate reviewed act their own boundary
requirements demand. This enumeration is an index of admitted install
repositories; it neither widens nor narrows the scope each repository's own
`repo-boundary-governance` requirement fixes.

#### Scenario: Hermes runtime procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies Hermes runtime behavior
- **THEN** the implementation detail MUST live in `Hermes-Install`

#### Scenario: Omnigent worker procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies Omnigent/Polly worker behavior
- **THEN** the implementation detail MUST live in `Omnigent-Install`
