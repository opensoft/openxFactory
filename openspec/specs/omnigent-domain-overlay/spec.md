# omnigent-domain-overlay Specification

## Purpose
TBD - created by archiving change add-omnigent-domain-overlay. Update Purpose after archive.
## Requirements
### Requirement: Domain overlay home and pinned consumption
Each DomainxFactory SHALL author its Omnigent domain content in an `omnigent/` tree at its repository root, and install repositories SHALL consume that content only through digest-pinned overlay references.
The install repository owns runtime and generic configuration; openxFactory
owns the neutral contracts; the DomainxFactory owns the domain overlay. An
install repository MUST NOT fork, copy, or locally amend domain overlay
content, and a contradiction between the tiers stops work and raises an
openxFactory change.

#### Scenario: An install consumes a domain overlay
- **WHEN** an Omnigent install declares a domain overlay
- **THEN** the declaration carries the source repository, revision, and content digest of the overlay
- **AND** composition fails closed if the fetched content does not match the pinned digest

#### Scenario: An install repo forks domain content
- **WHEN** an install repository commits domain-owned overlay content directly instead of consuming it by pin
- **THEN** validation MUST reject the tree as an ownership-line violation

### Requirement: Overlay payload composition
The Omnigent domain overlay payload SHALL compose over core worker configuration using the `domain_installation_overlay` operations (`supplement`, `replace`, `constrain`, `veto`) with `stricter_rule_wins: true`.
The payload MAY carry worker-profile deltas, prompt packs, toolchain
container bindings, domain validators, methodology preseed deltas, and lane
or scaleout policy deltas. A domain overlay can tighten core constraints; it
can never loosen them.

#### Scenario: A domain tightens a core constraint
- **WHEN** a domain overlay constrains a core worker stop condition or lowers a core resource ceiling
- **THEN** the composed effective profile carries the stricter value

#### Scenario: A domain attempts to loosen a core constraint
- **WHEN** a domain overlay attempts to remove a core stop condition or raise a core ceiling
- **THEN** composition MUST reject the overlay under `stricter_rule_wins`

### Requirement: Neutral worker archetype vocabulary
Every worker class declared by an Omnigent domain overlay SHALL map to exactly one neutral worker archetype: `frame`, `generate`, `verify`, `challenge`, or `assemble_for_admission`.
The terminal action of any workflow is owned by the domain's external
enforcement layer and its human authority, never by a worker archetype.
Domain-facing class names are aliases over the archetypes, in the same
alias pattern the layer vocabulary uses.

#### Scenario: An engineering overlay maps its classes
- **WHEN** codexFactory declares `coding_agent` as `generate` and `pr_admission_agent` as `assemble_for_admission`
- **THEN** the overlay validates and the archetype is available to neutral tooling and routing

#### Scenario: A medical overlay maps its classes
- **WHEN** MedxFactory declares `dream_hypothesis_agent` as `generate`, `skeptic_agent` as `challenge`, and `convergence_packet_agent` as `assemble_for_admission`
- **THEN** the overlay validates with the same archetype semantics as the engineering overlay

#### Scenario: A worker class has no archetype
- **WHEN** an overlay declares a worker class without an archetype mapping or with more than one
- **THEN** validation MUST reject the overlay

### Requirement: Generalized worker permission matrix
Every worker class SHALL declare the six-boolean permission matrix `read_workspace`, `write_artifacts`, `run_validations`, `propose_admission`, `execute_final_action`, and `access_secrets`, and `execute_final_action` and `access_secrets` MUST be false for every worker class in every domain and every configuration.
The two constitutional booleans encode the Omnigent layer's authority
boundary: workers never perform the domain's terminal action (merge, order
signing, chart write, truth-model mutation) and never hold raw credentials.
Domain-specific permission names (for example `read_repo`, `open_pr`) are
overlay-level aliases of these neutral booleans, declared in the overlay.

#### Scenario: A conforming worker class is declared
- **WHEN** an overlay declares a worker class with all six booleans and both constitutional booleans false
- **THEN** the overlay validates

#### Scenario: A worker class claims the terminal action
- **WHEN** an overlay declares any worker class with `execute_final_action: true` or `access_secrets: true`
- **THEN** validation MUST reject the overlay regardless of domain, approval state, or configuration

### Requirement: Credential requirement tiers
Overlay credential requirement families SHALL be declared in the tiers `all_classes`, `by_class`, `unassigned_by_default`, and `never_assignable`, and a family listed as `never_assignable` MUST NOT be grantable to any worker identity under any approval path.
`never_assignable` is stronger than `unassigned_by_default`: it is not an
approval-gated default but a structural prohibition, existing so the
boundary between worker capability and human or external-enforcement
authority is machine-visible. Grants remain governed by the
`credential-contracts` capability (scoped, expiring, reference-only).

#### Scenario: A grant is requested against a never_assignable family
- **WHEN** any workflow requests a runtime capability grant for a worker identity in a family the domain overlay lists as `never_assignable` (for example medical `order_sign`, `chart_write`, `truth_model_write`)
- **THEN** the grant MUST fail closed with no approval path that can override it

#### Scenario: An unassigned_by_default family is granted with approval
- **WHEN** a workflow requests a grant in an `unassigned_by_default` family with the required approvals
- **THEN** the grant may proceed under the credential-contracts rules

