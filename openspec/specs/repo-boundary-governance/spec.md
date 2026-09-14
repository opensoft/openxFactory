# repo-boundary-governance Specification

## Purpose
Defines how `openxFactory`, `Hermes-Install`, `Omnigent-Install`,
`Keycloak-Install`, `OpenXPKI-Install`, and `OmniWorker-Install` assign
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
- **WHEN** `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, or `OmniWorker-Install` needs to implement a factory policy
- **THEN** the install repo MUST link to the canonical `openxFactory` policy for neutral workflow concerns
- **AND** it MUST link to the owning DomainxFactory policy when implementing domain-specific execution behavior

**Removed from canon by refresh-install-repository-enumerations (2026-09-08):** ``**WHEN** `Hermes-Install` or `Omnigent-Install` needs to implement a factory policy`` — the bullet is REPLACED rather than deleted, by the widened trigger above it. **THE EDIT IS A LIST EXTENSION PLUS THE PUNCTUATION A LONGER LIST TAKES, AND NOTHING ELSE:** the two names become five, in canon's own order, keeping canon's own `or` and its surrounding grammar word for word, and a serial comma is added before that `or` because a five-item list takes one where canon's two-item list correctly did not. The style is MEASURED rather than preferred — `openspec/specs` carries 561 lines with a serial comma before a final `or` against 232 without, and this requirement's own body uses one before its final `and`. Nothing else in this requirement changes: its body, its two other scenarios and this scenario's own two `THEN`/`AND` bullets are word for word what canon states.

### Requirement: Install repository scope
The following install repositories SHALL be scoped to subsystem install,
operations, backup, restore, upgrade, verification, and disaster recovery:
`Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`,
and `OmniWorker-Install`.

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

#### Scenario: Hermes runtime procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies Hermes runtime behavior
- **THEN** the implementation detail MUST live in `Hermes-Install`

#### Scenario: Omnigent worker procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies Omnigent/Polly worker behavior
- **THEN** the implementation detail MUST live in `Omnigent-Install`

#### Scenario: Worker-host runtime procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies worker-host runtime behavior
- **THEN** the implementation detail MUST live in `OmniWorker-Install`

**Removed from canon by amend-repo-boundary-governance-scope-first-line (2026-09-11):** `` `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, and `OmniWorker-Install` SHALL be scoped to subsystem install, operations, backup, restore, upgrade, verification, and disaster recovery. `` — the sentence is REPLACED IN PLACE by the one above it and is not dropped, and every one of the five repository names is carried into it in canon's own order, canon's own spelling and canon's own serial comma. What moves is WHERE THE OBLIGATION STANDS INSIDE ITS OWN SENTENCE: the subject and the modal now open the first body line, which is the shape the other ten requirements of this specification already have, so a reader who reads one line and a parser that reads one line both meet the obligation there instead of meeting a list of names whose verb has not arrived. Four words of subject are added at the front, the enumeration moves behind the modal under a colon, and nothing else in the sentence changes: the same five repositories are scoped to the same seven activities, in the same words and the same order. Nothing this requirement obliges, admits or refuses moves, and the enumeration remains the INDEX the sibling requirement on enumeration authority says it is rather than becoming a claim about which install repositories exist. This reason carries no code span, so the marker names exactly one unit under the grammar it is written in.

### Requirement: Copy-first migration
Repo-boundary migration SHALL use copy-first migration until canonical
replacements, scope links, and validation checks are in place. Content
migration SHALL be dogfooded through OpenSpec, Hermes approval,
Omnigent/Polly decomposition, PR admission, merge council, and GitHub PRs.

#### Scenario: Canonical policy exists in an install repo
- **WHEN** policy currently lives in `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, or `OmniWorker-Install`
- **THEN** the policy MUST be copied or summarized into `openxFactory` before the install repo copy is deleted or marked legacy

#### Scenario: Existing proof harness depends on current files
- **WHEN** a proposed move could break an existing proof harness or smoke test
- **THEN** the move MUST be deferred until a replacement location and validation path exist

#### Scenario: Content migration starts
- **WHEN** canonical policy or contract content is migrated after the repo-boundary pilot
- **THEN** the work MUST be proposed, decomposed, reviewed, admitted to PR, and merged using the factory workflow itself

**Removed from canon by refresh-install-repository-enumerations (2026-09-08):** `` **WHEN** policy currently lives in `Hermes-Install` or `Omnigent-Install` `` — the bullet is REPLACED rather than deleted, by the widened trigger above it. **THE EDIT IS A LIST EXTENSION PLUS THE PUNCTUATION A LONGER LIST TAKES, AND NOTHING ELSE:** the two names become five, in canon's own order, keeping canon's own `or` and its surrounding grammar word for word, and a serial comma is added before that `or` because a five-item list takes one where canon's two-item list correctly did not. The style is MEASURED rather than preferred — `openspec/specs` carries 561 lines with a serial comma before a final `or` against 232 without, and this requirement's own body uses one before its final `and`. The copy-first obligation itself, its dogfooding sentence and the two other scenarios are word for word what canon states — this requirement is the one `implement-omniworker-install-repo`'s own migration clause cites by name, and nothing in it is narrowed here.

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
independently released repository named `openAvatar`, created on 2026-08-03 by
the DTN-022 subtree split that extracted the codexFactory
`apps/avatar-client-lab/` home that `implement-avatar-client-lab` had
ratified, which
`qualify-avatar-live-voice` records as having discharged this boundary's
creation obligation. From creation it SHALL
own the Flutter application and packages, client bindings, pure reducers, UI
and platform adapters, the trusted local disclosure/media gate, constrained
control and media clients, and client tests. It SHALL pin the compatible
openxFactory bundle tag plus exact contract commit and digests and MUST NOT
contain a standard provider API key, server tool
handler, server provider configuration, or a copied neutral schema without
pin and fixture-conformance validation.

The openxFactory repository SHALL remain the canonical owner of contracts
and the reference server trust boundary. The named future home for deployable
avatar server code SHALL be `openAvatar-server`, a repository created only by
whichever change first ships deployable server code and never in advance of it.
The future conventional web console
and its bindings SHALL remain outside the client repository until separately
approved.

#### Scenario: Client repository is created
- **WHEN** `openAvatar` stands as the created client repository, as DTN-022 created it on 2026-08-03
- **THEN** it MUST be private and independently releasable, identify openxFactory as contract and server-control owner, and contain no provider keys or server tool handlers

#### Scenario: Privileged provider code is proposed in the client
- **WHEN** code would create provider calls with a standard key, configure server prompts or tools, execute functions, or attach privileged sideband control
- **THEN** repository-boundary validation MUST reject the code and route it to the server trust boundary

### Requirement: Avatar-client release evidence
Release evidence obligations SHALL activate at the internal-live gate, not
at repository creation: from that gate, every `openAvatar`
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
Adding `openAvatar` to the top-level xFactory aggregation SHALL
require a separate reviewed change that records path, remote, visibility,
exact validated commit, checkout, compatibility, update, and rollback
behavior. The conventional web console SHALL require its own repository,
contract pin, authentication handoff, and ownership decision, and the
production deployment home for the avatar control runtime SHALL be decided
by the live-qualification successor change consistent with this
capability's routing of runtime operations to install repositories.

#### Scenario: Aggregation integration is proposed
- **WHEN** xFactory proposes pinning `openAvatar`
- **THEN** a dedicated change MUST define and verify gitlink path, remote, commit, checkout, compatibility, update, and rollback behavior

#### Scenario: Web operations console begins
- **WHEN** a later slice implements dense administration or interactive workflow editing
- **THEN** it MUST define a separate web repository and binding boundary rather than extending the Flutter client

### Requirement: OmniWorker install repository boundary

The worker-host product SHALL live in a private, independently released
repository named `OmniWorker-Install`, created as `opensoft/OmniWorker-Install`
by this change's realization on Brett Heap's ruling of 2026-09-05 that the
name `omniWorker` covers "the worker-host product only", and, when admitted,
pinned into the top-level xFactory aggregation at `installs/omniworker-install`.

From creation it SHALL own the worker host application that converges a Cloud
PC or workstation into a worker host, its deployment and detection scripts and
their test harnesses, the worker pack and the worker profiles and prompt sets a
host materializes, the worker-host manifest schema and the per-client host
manifests as `clients/<tenant>/worker-hosts/<host>.worker-host-manifest.yaml`,
the artifact-worker heartbeat schema and its reference publisher, and the
host-facing runbooks for Cloud PC licensing, worker-pack install, credential
auth profiles, and worker-persona credential onboarding. It SHALL pin the
compatible openxFactory contract bundle tag plus exact contract commit and
digests for the neutral contracts it consumes, and it SHALL name `openxFactory`
as the canonical owner of those contracts.

`Omnigent-Install` SHALL remain the orchestrator's install repository under its
own name and its own `repo-boundary-governance` requirement. It SHALL retain
the control-plane services, the container, compose and Kubernetes topology, the
agent and pilot flows, the intent inbox and dispatch minter, and the
`omnigent-install-manifest` realization. The split SHALL NOT rename
`Omnigent-Install`, SHALL NOT rename or re-digest the neutral
`contracts/omnigent/` contract family, and SHALL NOT alter the
`omnigent-domain-overlay` or `omnigent-install-manifest` specifications or the
per-domain `omnigent/` overlay directories that pin them.

The migration SHALL be copy-first under this capability's existing "Copy-first
migration" requirement: the worker-host paths SHALL be copied into
`OmniWorker-Install` with the proof harnesses that validate them and SHALL be
retired from `Omnigent-Install` only after every declared consumer has been
re-pinned in its own reviewed change and its validation path is green at the
new location. An active change whose declared `code_surface` consists entirely
of migrating paths SHALL be re-homed by an explicit named act — landing in the
source repository before the copy, or re-targeting to the new repository with
an amendment to its `code_surface` — and SHALL NOT arrive in the new
repository as an untracked side effect of a file copy.

`OmniWorker-Install` MUST NOT contain a model-provider credential, a runner
registration token, an enrollment lease secret, a Key Vault secret value, a
host-local service-account password, or any other credential value — each of
those is a `credential-contracts` record with declared custody, and the
repository holds only the prepared-profile and vault-reference SHAPES that
name them. It MUST NOT restate neutral contract meaning, which `openxFactory`
continues to own. It MUST NOT carry the orchestrator's control-plane services
or the governed administration workflow that the owning DomainxFactory owns.

Adding the repository to the aggregation SHALL be a separate reviewed change
that records path, remote, visibility, exact validated commit, checkout,
compatibility, update, and rollback behavior. Repository creation SHALL NOT be
treated as aggregation admission.

#### Scenario: Worker-host install repository is created

- **WHEN** this change's realization creates `opensoft/OmniWorker-Install`
- **THEN** it MUST be private and independently releasable, identify `openxFactory` as the owner of the neutral contracts it pins, and contain no credential values or key material
- **AND** the repository's README MUST state that `openxFactory` owns factory workflow policy and that `OmniWorker-Install` owns worker-host install, operations, and disaster recovery

#### Scenario: Worker-host paths are migrated out of the orchestrator repository

- **WHEN** a worker-host path is copied from `Omnigent-Install` into `OmniWorker-Install`
- **THEN** the proof harness or smoke test that validates it MUST be copied in the same change and MUST be green at the new location
- **AND** the source path MUST NOT be deleted from `Omnigent-Install` until every declared consumer has been re-pinned and verified

#### Scenario: A consumer still pins a migrated worker-host path

- **WHEN** a consumer repository names a migrating path — an aggregation submodule entry or workflow reference, a code-surface repository vocabulary, a sibling-checkout environment seam, or a derived-notebook projection
- **THEN** the consumer MUST be re-pinned to `OmniWorker-Install` in its own reviewed change before the retirement change lands
- **AND** a re-pin whose validation SKIPS when the target is absent MUST be verified by a run that does not skip, because a skipping check cannot distinguish a correct re-pin from a missing one

#### Scenario: Omnigent-Install is proposed for rename or emptying

- **WHEN** a change proposes renaming `Omnigent-Install`, retiring it, moving the control-plane services or the container, compose or Kubernetes topology out of it, or renaming the neutral `contracts/omnigent/` family or the `omnigent-domain-overlay` or `omnigent-install-manifest` specifications
- **THEN** the proposal MUST be rejected as outside the ruled scope "the worker-host product only", because `Omnigent-Install` remains the orchestrator repository under its own name

#### Scenario: Worker-host aggregation pin is proposed

- **WHEN** xFactory proposes pinning `installs/omniworker-install`
- **THEN** a dedicated reviewed change MUST define and verify gitlink path, remote, visibility, exact validated commit, checkout, compatibility, update, and rollback behavior
- **AND** the repository's own creation change MUST NOT be accepted as that record

#### Scenario: A credential value is proposed in the worker-host repository

- **WHEN** a change proposes committing a model-provider credential, a runner registration token, an enrollment lease secret, a Key Vault secret value, or a host service-account password
- **THEN** repository-boundary validation MUST reject it and route the material to a `credential-contracts` record with declared custody

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
