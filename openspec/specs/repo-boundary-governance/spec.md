# repo-boundary-governance Specification

## Purpose
Defines how `openxFactory`, `Hermes-Install`, and `Omnigent-Install` assign
canonical workflow policy ownership, install repository scope, copy-first
migration rules, and guarded repo-boundary execution.
## Requirements
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
- **WHEN** `Hermes-Install` or `Omnigent-Install` needs to implement a factory policy
- **THEN** the install repo MUST link to the canonical `openxFactory` policy for neutral workflow concerns
- **AND** it MUST link to the owning DomainxFactory policy when implementing domain-specific execution behavior

### Requirement: Install repository scope
`Hermes-Install` and `Omnigent-Install` SHALL be scoped to subsystem install,
operations, backup, restore, upgrade, verification, and disaster recovery.

#### Scenario: Hermes runtime procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies Hermes runtime behavior
- **THEN** the implementation detail MUST live in `Hermes-Install`

#### Scenario: Omnigent worker procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies Omnigent/Polly worker behavior
- **THEN** the implementation detail MUST live in `Omnigent-Install`

### Requirement: Copy-first migration
Repo-boundary migration SHALL use copy-first migration until canonical
replacements, scope links, and validation checks are in place. Content
migration SHALL be dogfooded through OpenSpec, Hermes approval,
Omnigent/Polly decomposition, PR admission, merge council, and GitHub PRs.

#### Scenario: Canonical policy exists in an install repo
- **WHEN** policy currently lives in `Hermes-Install` or `Omnigent-Install`
- **THEN** the policy MUST be copied or summarized into `openxFactory` before the install repo copy is deleted or marked legacy

#### Scenario: Existing proof harness depends on current files
- **WHEN** a proposed move could break an existing proof harness or smoke test
- **THEN** the move MUST be deferred until a replacement location and validation path exist

#### Scenario: Content migration starts
- **WHEN** canonical policy or contract content is migrated after the repo-boundary pilot
- **THEN** the work MUST be proposed, decomposed, reviewed, admitted to PR, and merged using the factory workflow itself

### Requirement: Guarded pilot execution
The initial repo-boundary pilot SHALL be doc-only, start in `openxFactory`,
and avoid deletions, submodules, runtime code movement, secrets, credentials,
generated state, databases, and runtime workspaces. Later dogfood migration
features SHALL keep the same stop conditions unless Hermes approves a narrower
exception for a specific feature.

#### Scenario: First pilot feature is executed
- **WHEN** FEAT-RB-001 is implemented
- **THEN** it MUST touch `openxFactory` only and MUST NOT change install repo files, runtime code, or submodules

#### Scenario: Stop condition is encountered
- **WHEN** a change proposes deleting install repo files, touching secrets, combining submodules with file moves, or modifying runtime state
- **THEN** the pilot MUST stop until Hermes approves a separate scoped feature

#### Scenario: Dogfood migration feature reaches a stop condition
- **WHEN** a dogfood migration feature proposes deleting source docs, moving runtime code, changing submodule pointers, or touching generated state
- **THEN** the feature MUST stop and return to Hermes approval before implementation continues

### Requirement: Install repo scope links
Install repositories SHALL explicitly link back to `openxFactory` for canonical
factory workflow policy once their scope clarification feature is approved.

#### Scenario: Omnigent-Install scope is clarified
- **WHEN** the Omnigent install scope feature is implemented
- **THEN** its README MUST state that `openxFactory` owns factory workflow policy and that `Omnigent-Install` owns Omnigent/Polly install and DR

#### Scenario: Hermes-Install scope is clarified
- **WHEN** the Hermes install scope feature is implemented
- **THEN** its README MUST state that `openxFactory` owns factory workflow policy and that `Hermes-Install` owns Hermes install and DR

### Requirement: Neutral installer repository integration
The top-level xFactory aggregation repository SHALL pin the independently
released neutral installer implementation repository at
`installs/xfactory-installer`. The pin MUST reference an exact validated commit,
and repository intent MUST document remote, visibility, ownership, compatibility,
update, and rollback behavior before the pin is treated as supported.

#### Scenario: Installer repository is first integrated
- **WHEN** `opensoft/xFactory-Installer` is added to the aggregation workspace
- **THEN** GitHub visibility MUST be private
- **AND** the parent MUST record the SSH remote and exact validated bootstrap commit
- **AND** a recursive submodule checkout MUST reproduce the repository boundary

#### Scenario: Installer pin is updated
- **WHEN** xFactory adopts a later installer release
- **THEN** the installer repository MUST pass its validation at the proposed commit
- **AND** the parent change MUST record compatibility and rollback evidence

#### Scenario: Installer integration is rolled back
- **WHEN** an installer pin is incompatible or its repository boundary is withdrawn
- **THEN** xFactory MUST restore the previous gitlink or remove the gitlink and `.gitmodules` entry in a dedicated reviewed change
- **AND** immutable repository release evidence MUST remain available

### Requirement: Neutral avatar-client repository boundary
The reusable Flutter avatar implementation SHALL live in a private,
independently released repository named `xfactory-avatar-client`, created by
the `implement-avatar-client-lab` successor change. From creation it SHALL
own the Flutter application and packages, client bindings, pure reducers, UI
and platform adapters, the trusted local disclosure/media gate, constrained
control and media clients, and client tests. It SHALL pin the compatible
openxFactory bundle tag plus exact contract commit and digests and MUST NOT
contain a standard provider API key, server tool
handler, server provider configuration, or a copied neutral schema without
pin and fixture-conformance validation.

The openxFactory repository SHALL remain the canonical owner of contracts
and the reference server trust boundary. The future conventional web console
and its bindings SHALL remain outside the client repository until separately
approved.

#### Scenario: Client repository is created
- **WHEN** the successor change creates `xfactory-avatar-client`
- **THEN** it MUST be private and independently releasable, identify openxFactory as contract and server-control owner, and contain no provider keys or server tool handlers

#### Scenario: Privileged provider code is proposed in the client
- **WHEN** code would create provider calls with a standard key, configure server prompts or tools, execute functions, or attach privileged sideband control
- **THEN** repository-boundary validation MUST reject the code and route it to the server trust boundary

### Requirement: Avatar-client release evidence
Release evidence obligations SHALL activate at the internal-live gate, not
at repository creation: from that gate, every `xfactory-avatar-client`
release SHALL identify source revision, Flutter and platform versions, the
pinned openxFactory bundle tag, exact contract commit and digests, canonical
fixture-conformance results, dependency lock, secret-scan result, test
evidence, client integrity evidence appropriate to the surface (desktop code
signing or web deployment integrity/CSP), and rollback target, and release
automation SHALL fail when any of these is missing, a dependency is unpinned,
or a secret is detected.
Before the internal-live gate the client MAY consume contracts by
co-checkout path reference. SBOM, dependency-license review, and the formal
accessibility audit SHALL be required at the pilot gate rather than per
release.

#### Scenario: Client is released for internal live use
- **WHEN** a client version is proposed for the internal-live ring
- **THEN** its release evidence MUST contain the pinned contract, fixture-conformance, dependency-lock, secret-scan, client-integrity, test, and rollback references

#### Scenario: Trusted media adapter integrity is unproven
- **WHEN** an internal-live client cannot prove desktop signing or web deployment integrity for the code enforcing disclosure and local media gating
- **THEN** release validation MUST fail because the confidentiality trusted computing base is not established

#### Scenario: Client and server are incompatible
- **WHEN** the client contract pin or capability requirements do not match the deployed broker
- **THEN** preflight MUST block live media and governed commands and MUST offer only a compatible upgrade, text fallback, or handoff

### Requirement: Deferred aggregation and web-console integration
Adding `xfactory-avatar-client` to the top-level xFactory aggregation SHALL
require a separate reviewed change that records path, remote, visibility,
exact validated commit, checkout, compatibility, update, and rollback
behavior. The conventional web console SHALL require its own repository,
contract pin, authentication handoff, and ownership decision, and the
production deployment home for the avatar control runtime SHALL be decided
by the live-qualification successor change consistent with this
capability's routing of runtime operations to install repositories.

#### Scenario: Aggregation integration is proposed
- **WHEN** xFactory proposes pinning `xfactory-avatar-client`
- **THEN** a dedicated change MUST define and verify gitlink path, remote, commit, checkout, compatibility, update, and rollback behavior

#### Scenario: Web operations console begins
- **WHEN** a later slice implements dense administration or interactive workflow editing
- **THEN** it MUST define a separate web repository and binding boundary rather than extending the Flutter client

