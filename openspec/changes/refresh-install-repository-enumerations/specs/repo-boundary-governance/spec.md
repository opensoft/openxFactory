# repo-boundary-governance Specification (delta)

## MODIFIED Requirements

### Requirement: Install repository scope
`Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, and `OmniWorker-Install` SHALL be scoped to subsystem
install, operations, backup, restore, upgrade, verification, and disaster
recovery.

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
*"Worker-host aggregation pin is proposed"* scenario demands. This
enumeration is an index of admitted install
repositories; it neither widens nor narrows the scope each repository's own
`repo-boundary-governance` requirement fixes.

#### Scenario: Hermes runtime procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies Hermes runtime behavior
- **THEN** the implementation detail MUST live in `Hermes-Install`

#### Scenario: Omnigent worker procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies Omnigent/Polly worker behavior
- **THEN** the implementation detail MUST live in `Omnigent-Install`

#### Scenario: Worker-host runtime procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies worker-host runtime behavior
- **THEN** the implementation detail MUST live in `OmniWorker-Install`

**Removed from canon by refresh-install-repository-enumerations (2026-09-08):** `` `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, and `OpenXPKI-Install` SHALL be scoped to subsystem install, operations, backup, restore, upgrade, verification, and disaster recovery. `` — ONE unit, and one only. The enumeration sentence is REPLACED rather than deleted, by the sentence above it. **THE EDIT IS A LIST EXTENSION AND NOTHING ELSE:** `OpenXPKI-Install` gains a following comma and a fifth name is appended after canon's own conjunction, so the serial comma before the final `and` is PRESERVED and every other word is byte-identical. **NOTHING ELSE IN THIS REQUIREMENT IS NAMED, BECAUSE NOTHING ELSE IS ABSENT:** the 2026-08-21 admission sentence, the index sentence that follows it, and both routing scenarios are carried BYTE-IDENTICAL, and the fifth repository's own admission record and its routing scenario are APPENDED beside them — which adds units and removes none.

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
- **WHEN** `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install` or `OmniWorker-Install` needs to implement a factory policy
- **THEN** the install repo MUST link to the canonical `openxFactory` policy for neutral workflow concerns
- **AND** it MUST link to the owning DomainxFactory policy when implementing domain-specific execution behavior

**Removed from canon by refresh-install-repository-enumerations (2026-09-08):** ``**WHEN** `Hermes-Install` or `Omnigent-Install` needs to implement a factory policy`` — the bullet is REPLACED rather than deleted, by the widened trigger above it. **THE EDIT IS A LIST EXTENSION AND NOTHING ELSE:** the two names become five, in canon's own order, and every other word, the `or` and the surrounding grammar included, is byte-identical. Nothing else in this requirement changes: its body, its two other scenarios and this scenario's own two `THEN`/`AND` bullets are word for word what canon states.

### Requirement: Copy-first migration
Repo-boundary migration SHALL use copy-first migration until canonical
replacements, scope links, and validation checks are in place. Content
migration SHALL be dogfooded through OpenSpec, Hermes approval,
Omnigent/Polly decomposition, PR admission, merge council, and GitHub PRs.

#### Scenario: Canonical policy exists in an install repo
- **WHEN** policy currently lives in `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install` or `OmniWorker-Install`
- **THEN** the policy MUST be copied or summarized into `openxFactory` before the install repo copy is deleted or marked legacy

#### Scenario: Existing proof harness depends on current files
- **WHEN** a proposed move could break an existing proof harness or smoke test
- **THEN** the move MUST be deferred until a replacement location and validation path exist

#### Scenario: Content migration starts
- **WHEN** canonical policy or contract content is migrated after the repo-boundary pilot
- **THEN** the work MUST be proposed, decomposed, reviewed, admitted to PR, and merged using the factory workflow itself

**Removed from canon by refresh-install-repository-enumerations (2026-09-08):** `` **WHEN** policy currently lives in `Hermes-Install` or `Omnigent-Install` `` — the bullet is REPLACED rather than deleted, by the widened trigger above it. **THE EDIT IS A LIST EXTENSION AND NOTHING ELSE:** the two names become five, in canon's own order, and every other word, the `or` and the surrounding grammar included, is byte-identical. The copy-first obligation itself, its dogfooding sentence and the two other scenarios are word for word what canon states — this requirement is the one `implement-omniworker-install-repo`'s own migration clause cites by name, and nothing in it is narrowed here.

## ADDED Requirements

### Requirement: Install-repository enumerations are an index with a named authority
An install-repository enumeration SHALL be read as an INDEX and SHALL NOT be
read as the authority for which install repositories exist or are governed.
The authority for which repositories are ADMITTED AND MOUNTED is the top-level
xFactory aggregation's `installs/` mount list in its `.gitmodules`; the
authority for a repository's EXISTENCE, and for what it owns, is the reviewed
act that created it together with its own `repo-boundary-governance`
requirement. **EXISTENCE AND ADMISSION ARE DISTINCT AND SHALL NOT BE
CONFLATED** — this capability already separates them, requiring that adding a
repository to the aggregation be a separate reviewed change and that
*"repository creation SHALL NOT be treated as aggregation admission"* — so a
created, governed, not-yet-mounted install repository SHALL NOT be read as
non-existent because the mount list does not name it. A repository absent from
an enumeration it belongs in is an INDEX DEFECT, and its governance is
unaffected by the omission.

**THE MOUNT LIST AND THE INDEX ARE DIFFERENT SETS, and that is why the index is
not derived.** Measured on 2026-09-08, the aggregation mounts NINE paths under
`installs/` — `agenttower`, `cloudpc-install`, `hermes-install`,
`keycloak-install`, `medx-roottruth-install`, `omnigent-install`,
`omniworker-install`, `openxpki-install` and `xfactory-installer` — while the
install repositories this capability's *"Install repository scope"* requirement
indexes number FIVE. A change proposing to replace an index with a list
derived mechanically from the mount list SHALL declare which mounts are in
scope and on what test, and its derivation SHALL NOT select outside that
declared scope, because an unfiltered derivation enrols repositories no
reviewed act placed under this requirement and duplicates
`xFactory-Installer`, which its own *"Neutral installer repository
integration"* requirement already governs. **THE MEASUREMENT IS THE REASON,
NOT THE RULE:** the nine-against-five count is what makes the filter
necessary today, and a later topology in which the two sets coincide would
satisfy the same obligation rather than escape it — derivation is constrained
here, never foreclosed.

**AN INDEX IS REFRESHED BY A NAMED ACT, NOT BY A GENERATOR.** When a further
install repository is admitted to the aggregation, the admitting change SHALL
either refresh every promoted enumeration of install repositories or NAME the
successor that will, and the naming SHALL identify an issue or a change packet
rather than leave the refresh implicit. Deferring the refresh to avoid
colliding with another change that writes the same requirement is legitimate;
deferring it without naming where it went is what left three of these
enumerations two repositories behind and one of them four.

#### Scenario: A further install repository is admitted to the aggregation
- **WHEN** a reviewed change records the aggregation admission of an install repository not yet named in the promoted enumerations
- **THEN** that change MUST either refresh every promoted enumeration of install repositories or name the issue or change packet that will
- **AND** naming it MUST be a citation a later reader can follow, not a statement that a refresh is owed

#### Scenario: An admitted install repository is missing from an enumeration
- **WHEN** an admitted install repository is absent from one of these enumerations
- **THEN** the defect is the enumeration's and is repaired wherever it is found
- **AND** the repository's boundary, scope and obligations are unchanged by the omission, because the enumeration indexes them and does not confer them

#### Scenario: A change proposes deriving an enumeration from the mount list
- **WHEN** a change proposes replacing a hand-maintained enumeration with a list derived from the aggregation's `installs/` mount list
- **THEN** it MUST declare which mounts are in scope and the test that selects them
- **AND** a derivation whose SELECTED SET EXCEEDS ITS DECLARED SCOPE MUST be refused, the two sets being unequal by default rather than by accident: the mount list carried nine paths on 2026-09-08 against an indexed set of five, and the surplus held repositories governed by another capability, by their own requirement, or by nothing at all
