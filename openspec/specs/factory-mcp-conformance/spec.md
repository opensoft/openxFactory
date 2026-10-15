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

Each tool SHALL map all declared domain statuses and error codes to completed evaluations or execution failures. Result-schema statuses SHALL map to completed evaluations, and error-inventory codes SHALL map to execution failures. A negative policy finding SHALL remain a completed evaluation. The mapping SHALL NOT turn inability to evaluate that the domain reports through its error inventory into eligibility. Domain objects SHALL remain unchanged in structuredContent, with explicit isError semantics and no injected common wrapper.

#### Scenario: Negative evaluation
- **WHEN** the domain result is blocked by policy
- **THEN** the mapping preserves the blocked object and treats it as a completed evaluation

#### Scenario: Unavailable dependency
- **WHEN** the domain reports through its error inventory that it cannot evaluate because a dependency is unavailable
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

### Requirement: Hosted declarations carry an authorization block

A declaration whose service is deployed SHALL carry an authorization block, and a declaration whose service is not deployed SHALL NOT carry one. The block SHALL name the token issuer, the accepted token-signing algorithms, the token audience with its binding, and the path of the server's protected-resource metadata. The service's canonical resource URI is the protected resource the block describes, and for a deployed service it SHALL carry no query component. The issuer SHALL be an absolute https issuer identifier with no query, fragment or userinfo, never a runtime or product name. The metadata path SHALL be the well-known location that RFC 9728 § 3.1 derives from the canonical resource URI. The block SHALL carry no key material, client secret or token, and SHALL cite evidence or an explicit gap for its claims. Like every other declaration field, the block is checked offline, and its validity SHALL NOT certify that a server enforces it.

#### Scenario: Hosted declaration without the block
- **WHEN** a declaration's service is deployed and the declaration carries no authorization block
- **THEN** validation refuses it with a stable code located at the service

#### Scenario: Stdio-only declaration
- **WHEN** a declaration's service is not deployed because its server is reached only over stdio
- **THEN** no authorization block is required, and a block that is present is refused

#### Scenario: Issuer named rather than identified
- **WHEN** the block's issuer is not an absolute https issuer identifier, for example a bare runtime name, or it carries a query, fragment or userinfo
- **THEN** validation refuses the issuer

#### Scenario: Metadata off the well-known path
- **WHEN** the block's metadata path differs from the RFC 9728 well-known location for the canonical resource URI
- **THEN** validation refuses the path

#### Scenario: Hosted resource URI with a query
- **WHEN** a deployed service's canonical resource URI carries a query component
- **THEN** validation refuses the resource URI

#### Scenario: Unsupported authorization claim
- **WHEN** the block cites neither evidence nor a gap for its authorization claims
- **THEN** validation refuses the block
- **AND** a block supported only by a gap is reported valid-with-gaps, not verified

### Requirement: RS256 token-signing baseline

Every hosted domain server SHALL accept access tokens signed with RS256. The block's algorithm list SHALL name RS256, MAY also name EdDSA, and SHALL name no other algorithm. The algorithm `none` and every HMAC algorithm SHALL be refused by name. Admitting a further algorithm SHALL be a governed change to this capability, never a domain's default.

#### Scenario: RS256 absent
- **WHEN** a hosted declaration's algorithm list omits RS256, for example by naming EdDSA alone
- **THEN** validation refuses the list

#### Scenario: Unsigned or symmetric algorithm
- **WHEN** the algorithm list names `none`, HS256, HS384 or HS512, in any letter case
- **THEN** validation refuses that entry by name

#### Scenario: EdDSA beside RS256
- **WHEN** the algorithm list names RS256 and EdDSA
- **THEN** the algorithm list is accepted

#### Scenario: An algorithm the profile does not admit
- **WHEN** the algorithm list names another algorithm beside RS256, for example ES256
- **THEN** validation refuses that entry as not admitted by this profile

### Requirement: Audience bound to the server's own resource

A hosted server SHALL accept only access tokens issued for it as their audience, as RFC 8707 § 2 describes. The block SHALL declare exactly one audience value that the server requires, bound either to the service's canonical resource URI or to an identifier the issuer assigns to this resource alone. A resource-URI binding SHALL name exactly the canonical resource URI. No audience SHALL contain a wildcard or equal the issuer identifier. Sharing an issuer SHALL NOT make tokens interchangeable between domain servers.

#### Scenario: Audience is the server's own resource
- **WHEN** the block binds its audience to the resource URI and names the service's canonical resource URI
- **THEN** the audience binding is accepted

#### Scenario: Audience names another resource
- **WHEN** the block binds its audience to the resource URI but names any value other than the service's canonical resource URI
- **THEN** validation refuses the audience as unbound

#### Scenario: Issuer-assigned audience
- **WHEN** the issuer places an identifier it assigned to this resource in the token's audience instead of the resource URI
- **THEN** the block may bind the audience to that identifier
- **AND** the block's cited evidence or gap carries that binding, and validation does not certify it

#### Scenario: Unbounded audience
- **WHEN** the declared audience contains a wildcard or equals the issuer identifier
- **THEN** validation refuses the audience

### Requirement: Per-domain error vocabularies

Each domain SHALL keep its own error codes and error envelope in its own published schemas. The profile SHALL NOT define or require a neutral error-code vocabulary, and conformance SHALL NOT require a domain to change a published schema. The lossless outcome mapping SHALL be the only layer the domains share: each code's class and isError semantics, with the domain object unchanged in structuredContent. A code name that two domains both use SHALL carry no shared meaning or retry semantics through the profile.

#### Scenario: Two domains share a code name
- **WHEN** two domains' error inventories each hold a code of the same name with different envelopes or retry semantics
- **THEN** each declaration maps its own code through its own error inventory, and the profile treats the two codes as unrelated

#### Scenario: A code no other domain uses
- **WHEN** a domain's error inventory holds a code that no other domain and no neutral list uses
- **THEN** the declaration is judged by its own mapping alone and is not refused for that code's name
