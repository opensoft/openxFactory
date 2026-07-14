## MODIFIED Requirements

### Requirement: Structural parking in external enforcement
Where a domain's external enforcement system supports required human review, parked human-decision gates SHALL be encoded there as enforcement rules — named or counted required reviewers scoped to the surfaces that demand them — so that parking is fail-closed against agent misbehavior and the enforcement configuration is the machine-readable declaration of where a human gate exists. Any identity capable of modifying that enforcement configuration SHALL be authority-separated from any identity that performs ordinary content or workflow actions on the same surface, so that no identity able to do routine work can also weaken or remove the gate it is subject to.

#### Scenario: Engineering merge gate is structural
- **WHEN** codexFactory encodes its human merge gates
- **THEN** branch protection or rulesets require the named human review (via code-owner path scoping for human-gated surfaces), and the pull request cannot merge while that gate is pending

#### Scenario: Privileged deployment gate is structural
- **WHEN** a deploy or production action is policy-gated on explicit human approval
- **THEN** the enforcement system's deployment-approval mechanism (e.g. environment required reviewers) holds the action until the approval act occurs

#### Scenario: Pending structural gate is a park
- **WHEN** a required human review is pending in the enforcement system
- **THEN** the workflow is parked at that gate with its decision-ready packet attached to the work item
- **AND** no interrupt is issued for the pending review itself

#### Scenario: Autonomous lane coexists
- **WHEN** an enforcement action is inside the low-risk envelope on surfaces not scoped to a human gate
- **THEN** the Merge Master identity may satisfy the enforcement system's review requirement without human involvement, where deployment policy allows

#### Scenario: Enforcement identity is authority-separated
- **WHEN** a structural human-review gate is encoded as GitHub branch protection or rulesets
- **THEN** the identity performing ordinary content or workflow actions on that repository MUST NOT hold the permission to modify that branch protection or ruleset configuration
- **AND** only a separate, administration-tier identity may hold that permission

## ADDED Requirements

### Requirement: GitHub App identity tiers
Any GitHub App identity operating on Opensoft's own vendor build org SHALL be assigned to exactly one of two tiers and MUST NOT hold both. A **content-tier** identity SHALL perform ordinary factory work (reports, review-record pull requests, pin-sync commits) under the existing rules and MUST NOT hold any permission capable of modifying a structural human-review gate (rulesets, branch protection, required-reviewer configuration). An **administration-tier** identity SHALL hold the permissions capable of modifying those gates, MUST NOT perform ordinary content or workflow actions, and MUST apply only rules-as-code configuration that has passed the governed review lane and ratify gate. This tiering governs identities operating on Opensoft's own vendor build org; it does not govern GitHub identities operating on a client tenant's own infrastructure.

#### Scenario: Content identity cannot modify enforcement
- **WHEN** the content-tier App identity's installed permissions are evaluated
- **THEN** it MUST NOT include repository or organization administration permissions capable of changing rulesets or branch protection

#### Scenario: Administration identity performs no content actions
- **WHEN** the administration-tier App identity is invoked
- **THEN** it MUST NOT open, push to, or merge a pull request, or perform any other content-write action
- **AND** its only permitted actions are reading and applying rules-as-code enforcement configuration

#### Scenario: Administration identity applies unreviewed configuration
- **WHEN** a ruleset or branch-protection change has not passed the governed review lane and ratify gate
- **THEN** the administration-tier identity MUST NOT apply it

### Requirement: Administration-tier credential custody
An administration-tier GitHub App identity's private key SHALL be held under the canonical `credential-contracts` record shapes (requirement, binding, runtime capability grant, and audit) with least-authority defaults: a vaulted key custody binding, short-lived and workflow-scoped runtime grants, human and domain approval before grant issuance, and an audit record for every action with an evidence reference to the reviewed configuration change that authorized it.

#### Scenario: Administration action is granted and audited
- **WHEN** the administration-tier identity performs a rules-as-code apply
- **THEN** a runtime capability grant and a credential access audit record are produced
- **AND** the audit record's evidence reference identifies the reviewed configuration change that authorized the apply

#### Scenario: Grant issuance without approval
- **WHEN** a runtime capability grant for the administration-tier identity is requested without human and domain approval recorded
- **THEN** grant issuance MUST be rejected

#### Scenario: Grant scope exceeds workflow need
- **WHEN** a requested grant's scope is broader than the specific rules-as-code apply workflow requires
- **THEN** the credential broker MUST reject or narrow the grant to the exact effective scope needed
