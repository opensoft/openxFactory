# roles-authority-model — client-tenant routing delta

## MODIFIED Requirements

### Requirement: GitHub App identity tiers
Any GitHub App identity operating on Opensoft's own vendor build org SHALL be assigned to exactly one of two tiers and MUST NOT hold both. A **content-tier** identity SHALL perform ordinary factory work (reports, review-record pull requests, pin-sync commits) under the existing rules and MUST NOT hold any permission capable of modifying a structural human-review gate (rulesets, branch protection, required-reviewer configuration). An **administration-tier** identity SHALL hold the permissions capable of modifying those gates, MUST NOT perform ordinary content or workflow actions, and MUST apply only rules-as-code configuration that has passed the governed review lane and ratify gate. This tiering governs identities operating on Opensoft's own vendor build org; it does not govern GitHub identities operating on a client tenant's own infrastructure — client-tenant infrastructure execution SHALL instead be coordinated as a `client_infrastructure_request` under the Client Infrastructure Liaison model (the `client-infrastructure-liaison` and `client-infrastructure-request` capabilities), whose coordinating role never receives tenant-administration authority and whose executing identity is the request's approved execution owner under its binding.

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

#### Scenario: Client-tenant execution routes through the liaison
- **WHEN** a factory needs a change on a client tenant's own infrastructure (including a client-tenant GitHub organization or a customer repo administered under client authority)
- **THEN** the need MUST be coordinated as a `client_infrastructure_request` under an approved execution binding and MUST NOT be executed via the vendor-org content- or administration-tier App identity
- **AND** the executing identity is the binding's approved execution owner, never the coordinating liaison
