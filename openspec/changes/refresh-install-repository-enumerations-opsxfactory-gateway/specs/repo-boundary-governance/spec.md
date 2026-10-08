# repo-boundary-governance Specification (delta)

## MODIFIED Requirements

### Requirement: Canonical workflow authority
`openxFactory` SHALL be the canonical repository for domain-neutral factory
workflow policy, authority rules, role definitions, traceability rules,
admission concepts, merge authority concepts, and cross-system operating
contracts. Domain-specific execution policy SHALL live in the owning
DomainxFactory.

#### Scenario: Factory policy is introduced
- **WHEN** a new policy affects Hermes, Omnigent/Polly, OpenSpec, GitHub, merge council behavior, or more than one DomainxFactory at the domain-neutral workflow layer
- **THEN** the canonical policy MUST be created or updated in `openxFactory`

#### Scenario: Domain execution policy is introduced
- **WHEN** a policy defines software engineering Spec Kit mechanics, clinical review mechanics, operations runbook execution, accounting close workflow execution, marketing campaign execution, or another domain-specific workflow implementation
- **THEN** the canonical implementation policy MUST be created or updated in the owning DomainxFactory
- **AND** `openxFactory` MUST reference it only as a specialization of neutral workflow gates

#### Scenario: Install repo needs policy context
- **WHEN** `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, `OmniWorker-Install`, or `OpsxFactory-Gateway-Install` needs to implement a factory policy
- **THEN** the install repo MUST link to the canonical `openxFactory` policy for neutral workflow concerns
- **AND** it MUST link to the owning DomainxFactory policy when implementing domain-specific execution behavior

**Removed from canon by refresh-install-repository-enumerations-opsxfactory-gateway (2026-10-08):** ``**WHEN** `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, or `OmniWorker-Install` needs to implement a factory policy`` — the bullet is REPLACED rather than deleted, by the widened trigger above it. The edit is a list extension and nothing else: `OpsxFactory-Gateway-Install` is appended in canon's own order and canon's own spelling, and canon's own `or` moves to stand before the last name, as it did when the fifth name was added, so the serial comma is preserved and every other word is canon's. Nothing else in this requirement changes: its body, its other two scenarios and this scenario's own THEN and AND bullets are canon's words.

### Requirement: Install repository scope
The following install repositories SHALL be scoped to subsystem install,
operations, backup, restore, upgrade, verification, and disaster recovery:
`Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`,
`OmniWorker-Install`, and `OpsxFactory-Gateway-Install`.

`Keycloak-Install` (`opensoft/Keycloak-Install`, pinned at
`installs/keycloak-install`) and `OpenXPKI-Install`
(`opensoft/OpenXPKI-Install`, pinned at `installs/openxpki-install`) were
admitted to the top-level xFactory aggregation on 2026-08-21 by the
`admit-install-repos-to-aggregation` change, which recorded path, remote,
visibility, exact validated commit, checkout, compatibility, update, and
rollback behavior for each — the separate reviewed act their own boundary
requirements demand. `OmniWorker-Install` (`opensoft/OmniWorker-Install`,
pinned at `installs/omniworker-install`) was admitted on the same terms on
2026-09-05 by opensoft/xFactory#274 (merge commit
`648c8bd3fc4717e5b969cd95ea3e0207700e8925`), the record its own
*"Worker-host aggregation pin is proposed"* scenario demands. This enumeration
is an index of admitted install repositories; it neither widens nor narrows the
scope each repository's own `repo-boundary-governance` requirement fixes.

`OpsxFactory-Gateway-Install` (`opensoft/OpsxFactory-Gateway-Install`, pinned
at `installs/opsxfactory-gateway-install`) was admitted to the top-level
xFactory aggregation on 2026-10-06 by opensoft/xFactory#567 (merge commit
`651dd5c9450646a1d6e4a55ef04ddc5d53823cb4`, pinned commit
`26f53c96965336819ac3d852db935e89ea7ec143`), one reviewed change that recorded
path, remote, visibility, exact validated commit, checkout, compatibility,
update, and rollback behavior and is distinct from the repository's creation on
the same day. That change named opensoft/openxFactory#1259 as the successor
that refreshes this enumeration, as the sibling requirement on enumeration
authority asks of an admitting change.

#### Scenario: Hermes runtime procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies Hermes runtime behavior
- **THEN** the implementation detail MUST live in `Hermes-Install`

#### Scenario: Omnigent worker procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies Omnigent/Polly worker behavior
- **THEN** the implementation detail MUST live in `Omnigent-Install`

#### Scenario: Worker-host runtime procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies worker-host runtime behavior
- **THEN** the implementation detail MUST live in `OmniWorker-Install`

**Removed from canon by refresh-install-repository-enumerations-opsxfactory-gateway (2026-10-08):** ``The following install repositories SHALL be scoped to subsystem install, operations, backup, restore, upgrade, verification, and disaster recovery: `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, and `OmniWorker-Install`.`` — the sentence is REPLACED IN PLACE by the one above it. The edit is a list extension and nothing else: the subject and the modal still open the first body line, the sixth name is appended in canon's own order, and canon's own `and` moves to stand before the last name, the serial comma preserved. The admission paragraph for the sixth repository is ADDED as a paragraph of its own after the admission paragraph canon carries unchanged, and the three routing scenarios are carried unchanged and no fourth is added: the enumeration indexes the repository and confers no boundary on it.

### Requirement: Copy-first migration
Repo-boundary migration SHALL use copy-first migration until canonical
replacements, scope links, and validation checks are in place. Content
migration SHALL be dogfooded through OpenSpec, Hermes approval,
Omnigent/Polly decomposition, PR admission, merge council, and GitHub PRs.

#### Scenario: Canonical policy exists in an install repo
- **WHEN** policy currently lives in `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, `OmniWorker-Install`, or `OpsxFactory-Gateway-Install`
- **THEN** the policy MUST be copied or summarized into `openxFactory` before the install repo copy is deleted or marked legacy

#### Scenario: Existing proof harness depends on current files
- **WHEN** a proposed move could break an existing proof harness or smoke test
- **THEN** the move MUST be deferred until a replacement location and validation path exist

#### Scenario: Content migration starts
- **WHEN** canonical policy or contract content is migrated after the repo-boundary pilot
- **THEN** the work MUST be proposed, decomposed, reviewed, admitted to PR, and merged using the factory workflow itself

**Removed from canon by refresh-install-repository-enumerations-opsxfactory-gateway (2026-10-08):** `` **WHEN** policy currently lives in `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, or `OmniWorker-Install` `` — the bullet is REPLACED rather than deleted, by the widened trigger above it. The edit is a list extension and nothing else: `OpsxFactory-Gateway-Install` is appended in canon's own order and canon's own spelling, and canon's own `or` moves to stand before the last name, as it did when the fifth name was added, so the serial comma is preserved and every other word is canon's. The copy-first obligation, its dogfooding sentence and the two other scenarios are canon's words, and nothing in this requirement is narrowed.
