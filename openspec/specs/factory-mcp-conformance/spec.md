# factory-mcp-conformance Specification

## Purpose
Describe and validate advisory domain MCP capabilities consistently while retaining domain ownership, lossless outcomes and explicit limits on conformance claims.

## Requirements

### Requirement: Closed versioned declaration

The profile SHALL accept only the declared version and advisory profile with a domain-owned, closed tool catalog. Each tool SHALL declare schema references, trusted binding rules, operational effects, outcome/error mappings, evidence disclosure, repetition and limits. Unknown fields, duplicate identifiers and undeclared tools SHALL be rejected.

#### Scenario: Complete declaration
- **WHEN** a complete synthetic declaration names unique tools and all required concerns
- **THEN** validation reports its structure valid without granting deployment or authority status

#### Scenario: Malformed catalog
- **WHEN** a declaration contains duplicate tool IDs, unknown fields, unknown versions or a missing required concern
- **THEN** validation fails with stable codes and locations

### Requirement: Offline pinned reference integrity

Schema references SHALL identify repository, immutable revision, relative path and SHA-256 digest. Verification SHALL use explicitly supplied snapshot roots without fetching network content or executing referenced code. It SHALL refuse missing roots, digest mismatches, invalid schemas, escaping paths and nonlocal schema references.

#### Scenario: Exact artifacts
- **WHEN** all schema references resolve to supplied contained artifacts with matching digests
- **THEN** reference integrity passes

#### Scenario: Untrusted reference
- **WHEN** a schema references a remote URL, absolute path, traversal path, symlink escape or mismatched digest
- **THEN** verification refuses without external network access

#### Scenario: Unavailable snapshot
- **WHEN** a pinned schema snapshot root cannot be supplied
- **THEN** reference verification reports unavailable and makes no conformance claim

### Requirement: Identity and scope mapping

Each declaration SHALL distinguish domain identity from installation, environment, canonical resource URI and deployment availability. Trusted mapping SHALL describe verified principal, permitted subject and operation, policy origin, neutral scope references and revocation posture. A caller reference SHALL NOT confer scope. Unresolved mappings SHALL remain explicit gaps.

#### Scenario: Undeployed contract
- **WHEN** a callable has no hosted installation
- **THEN** the declaration marks it not deployed and makes no operational URI claim

#### Scenario: Frozen mapping
- **WHEN** a host resolves bindings only at startup
- **THEN** the declaration identifies frozen revocation posture rather than claiming live revocation

#### Scenario: Caller-supplied authority
- **WHEN** a mapping treats caller policy or hostname alone as authorization
- **THEN** semantic validation rejects the mapping

### Requirement: Independent effects and advisory authority

The advisory profile SHALL require authority_effect none and separately declare external reads, execution, persistence and target-state mutation. It SHALL reject target-state mutation and approval grants. Declared execution SHALL be bounded and host-controlled, with evidence or explicit gaps. Persistence SHALL not be hidden merely because a result is advisory.

#### Scenario: Verification effects
- **WHEN** a tool executes trusted checks and stores replay state
- **THEN** it declares execution and persistence while retaining authority_effect none

#### Scenario: Mutating declaration
- **WHEN** a declaration grants approval or permits target-state mutation
- **THEN** the advisory profile rejects it

### Requirement: Lossless results and explicit failures

Each tool SHALL map all declared domain statuses and error codes to completed evaluations or execution failures. A negative policy finding SHALL remain a completed evaluation. The mapping SHALL NOT turn inability to evaluate into eligibility. Domain objects SHALL remain unchanged in structuredContent, with explicit isError semantics and no injected common wrapper.

#### Scenario: Negative evaluation
- **WHEN** the domain result is blocked by policy
- **THEN** the mapping preserves the blocked object and treats it as a completed evaluation

#### Scenario: Unavailable dependency
- **WHEN** the domain cannot evaluate because a dependency is unavailable
- **THEN** the mapping identifies an execution failure and never eligible

#### Scenario: Existing digested result
- **WHEN** a codex result carries its original domain fields and digests
- **THEN** mapping preserves the object verbatim

### Requirement: Evidence and disclosure boundaries

Declarations SHALL identify evaluated input, trusted context, observation/evaluation time where applicable, contract and artifact provenance association, and domain-specific disclosure rules. Raw credentials and provider payloads SHALL not be public evidence. Claims of audit resolution SHALL identify real evidence or remain gaps; a digest SHALL NOT imply confidentiality or authorization.

#### Scenario: Domain differences
- **WHEN** one domain suppresses raw paths and another exposes authorized record references
- **THEN** each records its own bounded disclosure mapping

#### Scenario: Unimplemented sink
- **WHEN** only an opaque event ID exists with no resolving sink evidence
- **THEN** the declaration records an audit gap and does not claim durable auditability

### Requirement: Per-tool repetition and deadlines

A declaration SHALL select reevaluate, lease_replay or fresh_observation and describe deadline semantics. Lease replay SHALL declare persistence, key/principal scope, conflict behavior and coordination. Fresh observation SHALL declare external reads, host-controlled age limits and final age checks, retaining original observation timestamps. Trace IDs SHALL NOT serve as grants or implicit idempotency keys.

#### Scenario: Consistent replay
- **WHEN** a lease-replay declaration names principal scope, storage and coordination
- **THEN** its declared repetition semantics are internally consistent

#### Scenario: Contradictory effects
- **WHEN** lease replay omits persistence or fresh observation omits external reads
- **THEN** semantic validation rejects the contradiction

#### Scenario: Cached observation
- **WHEN** a fresh-observation implementation can receive cached data
- **THEN** the mapping requires original timestamps and host age checks rather than relabeling it fresh

### Requirement: Honest validation and domain ownership

The validator SHALL report structure, reference integrity, semantic consistency and gaps separately with deterministic diagnostics. It SHALL distinguish valid-with-gaps from an invalid declaration and SHALL NOT certify behavioral or deployment conformance from declaration validity. Neutral executable fixtures SHALL be domain-independent. Existing codex observations SHALL be source-pinned and SHALL NOT amend or certify codex tools. Domain adoption SHALL require separately accepted version/pin evidence.

#### Scenario: Explicit gap
- **WHEN** a structurally valid consistent mapping declares an unresolved scope mapping
- **THEN** the report exposes valid-with-gaps without a verified-conformance claim

#### Scenario: Deterministic validation
- **WHEN** the same input and snapshots are validated repeatedly
- **THEN** diagnostic codes and ordering are stable

#### Scenario: Existing tools
- **WHEN** the neutral profile is introduced
- **THEN** codex schemas, outputs and client compatibility remain unchanged

#### Scenario: Unreleased profile
- **WHEN** an Ops mapping refers to the proposed neutral contract
- **THEN** it remains a proposed fit until accepted adoption evidence exists
