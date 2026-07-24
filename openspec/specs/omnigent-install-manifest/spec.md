# omnigent-install-manifest Specification

## Purpose
TBD - created by archiving change add-omnigent-domain-overlay. Update Purpose after archive.
## Requirements
### Requirement: Shared stack identity
An Omnigent install manifest SHALL digest-pin the Hermes runtime manifest of its stack as the single source of stack identity and MUST NOT declare a parallel independent identity document.
The Omnigent manifest adds only overlay-resolution and subject-workload
sections over the pinned identity. Both installs of one stack therefore
resolve the same tenant, domain, and subject-workload identity at a
verifiable revision.

#### Scenario: Identity is resolved from the pinned manifest
- **WHEN** the Omnigent install resolves its stack identity
- **THEN** tenant, domain, and subject-workload identity come from the digest-pinned Hermes runtime manifest revision

#### Scenario: Identity drift is detected
- **WHEN** the pinned Hermes runtime manifest digest does not match the fetched content, or an Omnigent manifest declares identity fields that conflict with the pinned document
- **THEN** composition and activation MUST fail closed

### Requirement: Stack cardinality
An Omnigent install stack SHALL contain exactly one active tenant instance, exactly one active domain overlay, and one or more subject workloads.
Multi-domain hosting on one worker fleet is rejected for this contract
generation; a second domain is a second stack.

#### Scenario: A second domain overlay is declared
- **WHEN** an install manifest declares two active domain overlays
- **THEN** cardinality validation MUST reject the manifest

#### Scenario: A bootstrap install precedes subject onboarding
- **WHEN** an install is bootstrapping and no subject workload is active yet
- **THEN** the manifest is valid for bootstrap states but the install is not operational until at least one subject workload activates

### Requirement: Subject workload registry
Each subject workload SHALL be a registry entry in the Omnigent install manifest carrying its identity reference, activation state, and validator mode.
"What is installed and how live is it" is machine-readable from the
registry, never inferred from GitOps tree diffs.

#### Scenario: A workload's liveness is queried
- **WHEN** a consumer asks which subject workloads exist and their activation state
- **THEN** the registry answers without inspecting the GitOps tree

#### Scenario: An undeclared workload is present
- **WHEN** a deployable workload exists in the activation plane with no registry entry
- **THEN** verification MUST report the tree as out of conformance

### Requirement: Fail-closed compose and verify with evidence
Composition of core, domain overlay, and tenant configuration SHALL digest-verify every pinned input fail-closed and SHALL emit idempotent evidence records using the seeding vocabulary: resolve, fetch, digest-verify, validate, activate.
Validation applies `stricter_rule_wins` and rejects raw secrets. GitOps
remains the activation plane; dormant-foundation corresponds to
structural-only and the activation step corresponds to seed, so both
installs of a stack audit identically.

#### Scenario: A pinned overlay fails digest verification
- **WHEN** a fetched overlay's content digest does not match its pin
- **THEN** composition stops before validation and an evidence record captures the failure

#### Scenario: Evidence is emitted for a successful activation
- **WHEN** compose and verify complete and a workload activates
- **THEN** evidence records exist for each vocabulary step and re-running the step is idempotent

### Requirement: Pre-rendered effective worker profiles
Effective worker profiles SHALL be pre-rendered at compose time and committed with provenance annotations identifying the core revision, overlay pin, and tenant parameters that produced each value.
Launch-time composition is not a conforming alternative for governed work:
the enforceable slice is materialized, diffable, and auditable before any
worker runs.

#### Scenario: An effective profile is audited
- **WHEN** a reviewer inspects an effective worker profile value
- **THEN** its provenance annotation resolves to the exact core revision, overlay pin, or tenant parameter that set it

#### Scenario: A worker launches from an unrendered profile
- **WHEN** a worker launch is requested against overlay inputs that have no committed pre-rendered effective profile
- **THEN** the launch MUST be refused

### Requirement: Canonical vocabulary from birth
Machine identifiers in the Omnigent overlay and install-manifest contract family SHALL use the canonical `subject`, `tenant`, and `domain` spellings from their first published version.
Legacy `customer` and `client` spellings appear only inside pinned upstream
artifacts (the Hermes runtime manifest and v2 `contracts/hermes-runtime/`
schemas, frozen under the layer-vocabulary machine-identifier freeze) and
are interpreted via the published legacy-to-canonical mapping.

#### Scenario: A new field is added to this family
- **WHEN** a schema in this contract family declares a layer-referencing identifier
- **THEN** it uses `subject`/`tenant`/`domain` spellings

#### Scenario: A pinned upstream identifier is consumed
- **WHEN** the install manifest reads `customer_subject` or a role kind of `client` from the pinned Hermes runtime manifest
- **THEN** the value is interpreted through the layer-vocabulary mapping without modifying the pinned artifact

