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

### Requirement: Crystallized Executor Bindings Conserve Authority
A worker class marked `crystallized` SHALL carry a `capability_ref`, an
`automation_rung` from the frozen L0–L6 vocabulary, a
`replaces_configuration` reference to the worker configuration whose work
the capability absorbs, and a young-capability throttle schedule; such a
class SHALL map to one of the existing five neutral archetypes (the
archetype vocabulary is unchanged), SHALL declare the six-boolean
permission matrix like any worker class — so the promoted constitutional
requirement (`execute_final_action` and `access_secrets` false for every
worker class) binds it verbatim — and its effective permissions and
credential requirement families MUST be a subset of the replaced
configuration's, checked mechanically, never by judgment.

#### Scenario: A conforming crystallized binding validates

- **WHEN** an overlay declares a crystallized class mapped to `generate`,
  with all six booleans declared, both constitutional booleans false,
  permissions and credential families a subset of its
  `replaces_configuration`, and a throttle schedule
- **THEN** the overlay validates

#### Scenario: Widening is rejected mechanically

- **WHEN** a crystallized class declares any permission true, or any
  credential family, that its `replaces_configuration` does not hold
- **THEN** validation MUST reject the overlay — crystallization is never a
  privilege-escalation path

#### Scenario: No new archetype may be invented

- **WHEN** a crystallized class declares an archetype outside the five
  neutral values
- **THEN** validation MUST reject the overlay

#### Scenario: A binding without its baseline is rejected

- **WHEN** a crystallized class omits `replaces_configuration`
- **THEN** validation MUST reject the overlay — the conservation subset
  check has no baseline without it

### Requirement: Rung Ceilings Are Declared Per Task Category
A `rung_ceilings` declaration SHALL list, per task category, a ceiling
from the L0–L6 vocabulary and a stated reason, and where a family's task
category carries no declared ceiling the effective ceiling SHALL default
to L3: the code rungs (L4–L6) are reachable only through an explicit,
reasoned overlay declaration, which is where a domain's regulatory
posture lives.

#### Scenario: A declared ceiling binds decisions

- **WHEN** an overlay declares ceiling L3 with a reason for a task
  category
- **THEN** a crystallization decision for a family in that category MUST
  NOT value or fund above L3

#### Scenario: Undeclared means the conservative default

- **WHEN** a family's task category has no declared ceiling
- **THEN** the effective ceiling is L3
- **AND** funding L4–L6 requires the overlay to declare a ceiling first

#### Scenario: A ceiling without a reason is rejected

- **WHEN** an overlay declares a rung ceiling with no reason
- **THEN** validation MUST reject the overlay

### Requirement: Worker semantic-context declaration
A worker class MAY declare the worker-scoped semantic-context profile it runs under, and a declaration SHALL name identity only — `profile_id` plus the domain ontology `package_id` — never a digest.
Package pins belong to consumers and compiled artifacts, so an overlay
declaration stays valid across compatible ontology releases. When the
domain repository carries an ontology package tree, the canonical
omnigent validator SHALL resolve every declared profile to an inventoried
`xfactory_semantic_context_profile` document whose `package_id` equals
the declared one and whose `worker_scope` matches the declaring worker —
either `worker_archetype` equal to the worker's archetype or
`worker_class` equal to the worker's id — and SHALL fail an unresolved or
scope-mismatched declaration. The declaration SHALL NOT change any
permission: the block carries no permission field, the six-boolean matrix
is unchanged, and `execute_final_action`/`access_secrets` remain
constitutionally false for every class with or without semantic context.

#### Scenario: A verify worker declares its profile
- **WHEN** a worker class with archetype `verify` declares `semantic_context` naming a profile whose `worker_scope.worker_archetype` is `verify` in the domain's ontology package
- **THEN** the overlay validates, and the worker's compiled context is bounded to that profile's term subset with the permission matrix untouched

#### Scenario: A declared profile does not resolve
- **WHEN** a worker class declares a `profile_id` that is not an inventoried profile of the declared package in the domain repository's ontology tree, or whose `worker_scope` names a different archetype and a different worker class
- **THEN** repo-mode validation MUST fail naming the worker and the profile

#### Scenario: A declaration attempts to carry authority
- **WHEN** a `semantic_context` declaration carries any field beyond the profile and package identity
- **THEN** schema validation MUST reject it — semantic context never widens a permission or credential surface

