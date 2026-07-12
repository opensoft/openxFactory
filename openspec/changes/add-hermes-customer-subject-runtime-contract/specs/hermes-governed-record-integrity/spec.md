Status: ratified
Ratified by: user approval of `add-hermes-customer-subject-runtime-contract` on 2026-07-12

## ADDED Requirements

### Requirement: Governed records carry explicit scope
Every v2 governed record SHALL carry a closed scope identifying its installation, stack, and owning layer. Cross-layer records SHALL carry exact source and target scopes. Installation-wide administration SHALL use an explicit installation scope and MUST NOT fabricate a Customer layer.

#### Scenario: Job evidence is recorded
- **WHEN** a job, run, event, artifact, approval, or trace record is created
- **THEN** its installation, stack, and owning layer MUST be present and referentially valid

#### Scenario: Governed record omits layer scope
- **WHEN** a layer-owned record omits or mismatches its layer scope
- **THEN** structural or persistence validation MUST fail

#### Scenario: Administrative record is installation-wide
- **WHEN** a worker pool or administrator group is not owned by one Customer layer
- **THEN** it MUST use an explicit installation administrative scope rather than an arbitrary Customer scope

### Requirement: Customer-subject persistence is default-deny
The canonical v2 persistence contract SHALL isolate all governed layer rows by installation, stack, and layer through relational scope, forced row-level controls, and distinct database roles. The migration/table owner SHALL be unavailable to runtime; runtime roles SHALL have no `BYPASSRLS` or role-escalation path; installation administration SHALL imply no subject-data visibility; and the cross-layer control plane SHALL have governed-function execution but no direct table access. A trusted transaction-local scope setter SHALL map the authenticated `session_user`, not the security-definer `current_user`, through an active, unexpired `assume_scope` authority grant, reject caller-selected ungranted scope, and clear scope on connection checkout/return. Every transaction SHALL recheck grant revocation and principal/layer lifecycle state; revocation or retirement SHALL invalidate new scope and already-pooled connections. Missing, malformed, stale, forged, cross-stack, cross-installation, and pooled-connection scope reuse SHALL fail closed.

#### Scenario: Subject A queries Subject B
- **WHEN** a runtime identity scoped to Customer A attempts to enumerate or read Customer B jobs, artifacts, approvals, or traces
- **THEN** no Customer B row MUST be visible

#### Scenario: Subject A attempts a write into Subject B
- **WHEN** a runtime identity scoped to Customer A attempts to create, mutate, or delete a Customer B record
- **THEN** persistence MUST reject the operation

#### Scenario: Test runs as database owner
- **WHEN** an isolation test uses an owner or bypass-RLS identity
- **THEN** it MUST NOT count as isolation acceptance evidence

#### Scenario: Runtime principal forges scope
- **WHEN** a layer runtime principal supplies another layer, stack, or installation to the trusted scope setter or directly changes the backing session context
- **THEN** persistence MUST reject the scope and expose no foreign row

#### Scenario: Installation administrator queries subject data
- **WHEN** an installation-administration principal attempts direct access to Customer-layer tables without an exact governed operation
- **THEN** persistence MUST reject the query

#### Scenario: Pooled connection is reused
- **WHEN** a connection returns to the pool after Customer A and is checked out for Customer B
- **THEN** Customer A scope MUST be absent before Customer B begins
- **AND** a missing reset MUST fail the isolation suite

#### Scenario: Principal scope grant is revoked
- **WHEN** an `assume_scope` grant is revoked or its principal/layer is retired before a new transaction on an existing pooled connection
- **THEN** the trusted setter MUST reject that scope and expose no governed row

### Requirement: Principal authority is explicit, immutable, and revocable
Each installation SHALL begin with exactly one immutable, out-of-band-approved trust-anchor record whose principal/key and policy digest may issue only root-scoped grants. Every non-genesis authority grant SHALL cite an issuer grant with `issue_grant` authority, narrow or preserve its issuer's scope, and form an acyclic chain to one active trusted anchor. Trust-anchor rotation or revocation SHALL be an append-only event authorized by the current anchor policy and MUST NOT rewrite historical evidence.

Every principal that assumes database scope, creates a binding, accepts a cross-layer resource, decides or supersedes an approval, or performs another governed action SHALL cite an immutable authority grant. A grant SHALL identify principal, issuer grant, installation/stack/layer scope, exact allowed action and resource constraints, pinned policy digest, effective time, and expiry. Grants SHALL be append-only; revocation SHALL be a separate append-only event. Wildcard, self-issued, cyclic, inherited, transitive, expired, or revoked authority MUST NOT authorize work.

#### Scenario: Principal acts under an exact active grant
- **WHEN** the principal, scope, action, resource, policy digest, and database-derived time match one active grant
- **THEN** the governed operation MAY proceed and MUST record the grant ID and digest

#### Scenario: Wrong-layer reviewer attempts approval
- **WHEN** a reviewer has authority in a different layer but no exact grant for the request authority scope
- **THEN** the decision MUST NOT authorize the target

#### Scenario: Grant is revoked during later use
- **WHEN** an earlier record cites a grant that is revoked before a new governed operation
- **THEN** the earlier audit record remains immutable
- **AND** the grant MUST NOT authorize the new operation

#### Scenario: Grant chain is self-issued or cyclic
- **WHEN** a grant cites itself, forms an issuer cycle, or cannot reach an active trusted installation anchor
- **THEN** authority validation MUST fail

#### Scenario: Root trust anchor rotates
- **WHEN** the current anchor policy authorizes a new root and append-only rotation event
- **THEN** new grants MUST validate only against the active root set
- **AND** historical records MUST retain the anchor chain valid at their authorization time

### Requirement: Cross-layer authority is exact, directional, and revocable
A cross-layer binding SHALL be immutable and cite its creator authority grant plus exact source and target layers, exact source resource type/ID/digest, exact target resource type/ID/digest, exactly one allowed action, purpose, start time, and expiry. Digests SHALL be mandatory for content-bearing resources and MAY be omitted only for the closed identity types `layer_identity`, `principal_identity`, and `policy_namespace`. A pinned target policy MAY require an exact target-acceptance grant. Wildcards, self-bindings, inheritance, and transitive authority SHALL be invalid. Revocation SHALL be an append-only event.

Binding/grant validation, database-derived time evaluation, required serialization locks, the governed write, and an immutable operation-authorization record SHALL commit in one transaction. A concurrent expiry or revocation SHALL prevent authorization unless that operation has already serialized and committed; a check-then-write window is forbidden.

#### Scenario: Exact active binding authorizes an operation
- **WHEN** an operation matches every source and target resource coordinate, digest, action, purpose, active grant, target acceptance, and time constraint of one binding
- **THEN** the controlled service operation MAY proceed and MUST record the binding and operation-authorization IDs and digests

#### Scenario: Binding direction is reversed
- **WHEN** an operation reverses the binding source and target
- **THEN** authorization MUST fail

#### Scenario: Transitive authority is attempted
- **WHEN** A is bound to B and B is bound to C but no exact A-to-C binding exists
- **THEN** A-to-C authorization MUST fail

#### Scenario: Binding is expired or revoked
- **WHEN** a matching binding has expired or has a valid revocation event
- **THEN** it MUST NOT authorize new work

#### Scenario: Source artifact is swapped under a binding
- **WHEN** an operation presents a different source resource ID or digest while retaining the same target and action
- **THEN** authorization MUST fail

#### Scenario: Revocation races a projection
- **WHEN** binding revocation and projection authorization execute concurrently
- **THEN** serialization MUST yield either a committed projection authorized before revocation or a rejected projection after revocation
- **AND** no projection may commit without an immutable operation-authorization record from the same transaction

### Requirement: Artifact records are content-addressed and immutable
Every artifact record SHALL identify its owning scope, artifact ID, SHA-256 content digest, byte size, media type, producer, deterministic `<installation_id>/<layer_id>/sha256/<digest>` storage key, creation time, and optional job/run correlation. Physical deduplication, if used, SHALL remain behind scoped indirection; unauthorized cross-layer requests SHALL be rejected before blob lookup with the same response shape/status and SHALL expose no semantic existence, lifecycle, deletion, or authorization oracle. The entire record SHALL be append-only and immutable; lifecycle changes SHALL be separate append-only events. Artifact metadata SHALL NOT become governed until content is finalized. Available content MUST exist and match its recorded digest and size at admission, approval, and controlled execution time.

#### Scenario: Available artifact is verified
- **WHEN** an artifact record is accepted as available
- **THEN** its body MUST exist at the governed storage key and match its non-null digest and byte size

#### Scenario: Artifact body or digest drifts
- **WHEN** an artifact body is missing or its bytes differ from the recorded digest or size
- **THEN** validation MUST fail and the artifact MUST NOT be approvable

#### Scenario: Artifact identity is rebound
- **WHEN** an actor attempts to update or delete any artifact-record field or resubmit an artifact ID with different metadata
- **THEN** persistence MUST reject the mutation

#### Scenario: Caller supplies a traversing path
- **WHEN** an artifact attempts to use an absolute, traversing, symlink-escaping, or non-content-addressed caller path as canonical storage identity
- **THEN** validation MUST fail

#### Scenario: Artifact body changes after approval
- **WHEN** an approved artifact body is missing or replaced before controlled execution
- **THEN** execution-time verification MUST fail and the prior approval MUST NOT authorize the bytes

#### Scenario: Another layer probes a shared digest
- **WHEN** Customer A supplies the digest of a Customer B artifact to storage lookup, lifecycle, or deletion operations
- **THEN** the result MUST reveal no existence or metadata oracle for Customer B and MUST NOT affect its body

### Requirement: Approval authority is immutable and target-digest-bound
Approval requests SHALL be append-only and immutable and carry the exact target type/ID/digest/scope, requested action and authority scope, requester principal/grant, reviewer selector, and decision-policy reference/digest. Each append-only decision SHALL repeat the exact target/action/scope/policy and carry its actual reviewer principal/grant. Expiry, cancellation, and revocation SHALL be separate append-only supersession events whose issuers also cite exact active grants. The canonical decision-policy contract SHALL define required reviewer selectors and aggregation; conflicting terminal decisions SHALL leave a request contested and non-authorizing unless that exact policy defines a deterministic resolution. A record with a mismatched or stale target digest, expired request, revoked grant, unauthorized issuer, or wrong reviewer scope MUST NOT authorize work.

#### Scenario: Matching decision approves an immutable target
- **WHEN** an authorized reviewer decides an unexpired request and the decision repeats the exact request target and authority scope
- **THEN** the decision MAY authorize only that target digest and action

#### Scenario: Target changes after approval
- **WHEN** the target content digest differs from the digest in the approval decision
- **THEN** the prior decision MUST NOT authorize the changed target

#### Scenario: Approval is revoked
- **WHEN** an authorized append-only revocation supersedes an approval decision
- **THEN** the decision remains in audit history but MUST NOT authorize subsequent work

#### Scenario: Approval record is mutated
- **WHEN** an actor attempts to update or delete an approval request, decision, or supersession event
- **THEN** persistence MUST reject the operation

#### Scenario: Conflicting terminal decisions exist
- **WHEN** unsuperseded decisions conflict and the pinned decision policy does not deterministically resolve that combination
- **THEN** the approval request MUST be contested and MUST NOT authorize work

#### Scenario: Unauthorized actor supersedes approval
- **WHEN** an actor without an exact active grant attempts to cancel, expire, or revoke a request or decision
- **THEN** the supersession event MUST be rejected

### Requirement: Traceability is scoped, digest-bound, and backed by authority
Every trace edge SHALL be append-only and identify source and target type, ID, digest, and layer scope plus relation and creator. A cross-layer edge SHALL cite the exact immutable operation-authorization record, binding, and grants that matched its endpoints and action in the same transaction. A same-layer edge MUST NOT use unrelated cross-layer authority. Trace evidence MUST NOT itself grant authority.

#### Scenario: Cross-layer projection is traced
- **WHEN** a governed resource is projected between layers under an active exact binding
- **THEN** the trace edge MUST record both digest-bound endpoints plus the operation-authorization ID/digest and cited binding/grant IDs/digests

#### Scenario: Cross-layer edge lacks binding proof
- **WHEN** source and target layers differ and no exact active binding is cited
- **THEN** trace validation and persistence MUST fail

#### Scenario: Endpoint digest mismatches
- **WHEN** a trace endpoint digest does not match the referenced immutable resource
- **THEN** validation MUST fail

### Requirement: v2 persistence coexists with v1 and migrates atomically
openxFactory SHALL publish a fresh-install v2 operational Postgres contract, a typed migration-mapping schema, and an executable idempotent v1-to-v2 migration without mutating v1 semantics in place. Reapplication SHALL compare canonical object definitions/checksums and fail on incompatible pre-existing tables, policies, functions, triggers, role attributes/memberships, schema/table/function ownership and ACLs, row-security enable/force flags, security-definer/search-path configuration, PUBLIC privileges, or quarantine grants.

Migration SHALL disable or equivalently lock v1 governed writes, execute against a recorded source database/schema identity and transaction snapshot or WAL position, consume a content-addressed and authority-approved scope mapping, preserve every legacy row and identifier, reconcile pre/post row counts and source digest, and append an immutable migration ledger. The mapping contract SHALL make the dataset digest independently reproducible by fixing UTF-8 table-name order, primary-key row order, schema-ordinal column order, length-prefixed value framing, an explicit null marker, UTC RFC 3339 microsecond timestamps, lowercase-hex binary, canonical JSON, table metadata frames, and SHA-256 over the framed tables. Missing, conflicting, or ambiguous scope, concurrent source drift, reconciliation mismatch, or replay with a changed mapping SHALL abort atomically. Unverifiable legacy artifacts, approvals, and trace edges SHALL be copied only to a separate quarantine schema that runtime roles cannot query and authoritative tables, views, foreign keys, and gates cannot reference.

#### Scenario: Clean v2 database is initialized twice
- **WHEN** the v2 DDL is applied to an empty supported Postgres database and applied again
- **THEN** both applications MUST succeed only after canonical introspection confirms the same resulting contract state

#### Scenario: Same-named database object or security authority has drifted
- **WHEN** a pre-existing table, policy, function, trigger, role attribute/membership, owner, ACL, row-security flag, function security/search path, PUBLIC privilege, or quarantine grant has the expected name but an incompatible definition or checksum
- **THEN** v2 readiness MUST fail rather than silently accepting `IF NOT EXISTS`

#### Scenario: Two-subject v1 database is migrated
- **WHEN** a seeded v1 database contains two legacy project values and a complete explicit mapping to two Customer layers
- **THEN** migration MUST preserve all row IDs and assign each related row to the correct layer

#### Scenario: Migration mapping is ambiguous
- **WHEN** a legacy value maps to multiple layers or a scoped legacy row has no provable mapping
- **THEN** the migration transaction MUST abort without partial v2 state

#### Scenario: Source changes during cutover
- **WHEN** a v1 governed write races migration or source row counts/digest no longer match the frozen snapshot
- **THEN** migration MUST abort or exclude the write through the proven cutover lock
- **AND** no successful ledger entry may omit the row

#### Scenario: Migration is retried with another map
- **WHEN** a completed or interrupted migration ID is replayed with a different mapping-manifest digest or source snapshot
- **THEN** the migration MUST fail closed

#### Scenario: Legacy approval lacks target digest
- **WHEN** a v1 approval cannot be tied to an immutable target digest
- **THEN** migration MUST preserve it only in the non-authoritative quarantine schema
- **AND** it MUST NOT satisfy a v2 approval gate

#### Scenario: Quarantined evidence is referenced
- **WHEN** a runtime principal, authoritative foreign key, approval gate, or trace tries to read, reference, or promote a quarantine record directly
- **THEN** persistence MUST reject the operation
- **AND** any later authoritative evidence MUST be created as a new governed record under current authority

### Requirement: Published bundle identity is reproducible
The v2 family SHALL be published only as part of an additive contract bundle whose manifest, changelog, annotated tag, exact repository commit, contract IDs/paths/schema versions, and canonical release digest inventory agree. The inventory SHALL live at `contracts/releases/<bundle-tag>.digests.yaml`, validate against `contracts/releases/release-digest-inventory.schema.yaml`, list repository-relative regular-file paths in bytewise order, and encode raw Git blob hashes as lowercase `sha256:<64hex>`. It SHALL include every required Hermes runtime schema, SQL file, migration, validator, fixture/index, modified static schema/validator, manifest, changelog, and contract README while excluding the inventory itself. The release verifier SHALL validate candidate bytes before commit and derive exact bytes from the pinned Git commit after commit/tag.

#### Scenario: Release candidate is realized
- **WHEN** the next available bundle version is allocated after final rebase
- **THEN** contract files, manifest, changelog, and digest inventory MUST be committed atomically
- **AND** the complete suites and independent review MUST pass against that exact candidate commit before tagging
- **AND** the exact reviewed commit MUST be reachable from published `origin/main`
- **AND** a merge-created replacement commit MUST rerun all gates and review before the matching annotated tag points to it

#### Scenario: Tag is missing or movable evidence is used
- **WHEN** the bundle tag is absent remotely or a consumer relies on a branch, tag, or working-tree file without the exact commit and digest
- **THEN** publication or consumption MUST fail closed

#### Scenario: Manifest contains a host-local path
- **WHEN** release metadata contains a host-absolute source or contract path
- **THEN** release validation MUST fail

#### Scenario: Digest inventory membership is incomplete
- **WHEN** a required semantic file is absent, duplicated, out of order, symlinked, or hashed after text canonicalization rather than from raw Git blob bytes
- **THEN** release validation MUST fail

#### Scenario: Legacy local source path is removed
- **WHEN** `source_compatibility_ref.local_source_path` is removed from the manifest in the additive bundle
- **THEN** a repository-wide consumer audit MUST prove no supported consumer requires it
- **AND** canonical source repository and commit provenance MUST remain
