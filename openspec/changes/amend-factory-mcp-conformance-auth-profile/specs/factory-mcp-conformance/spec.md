## ADDED Requirements

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

## MODIFIED Requirements

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
