# hermes-governed-record-integrity Specification

## Purpose
Define the scope, isolation, authority, governed-evidence, migration,
quarantine, release, and PostgreSQL conformance requirements for durable Hermes
records.

## Requirements

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
The canonical v2 persistence contract SHALL isolate all governed layer rows by
installation, stack, and layer through relational scope, forced row-level controls,
and distinct database roles. The migration/table owner SHALL be unavailable to
runtime; runtime roles SHALL have no `BYPASSRLS` or role-escalation path;
installation administration SHALL imply no subject-data visibility; and the
cross-layer control plane SHALL have governed-function execution but no direct
table access. A trusted transaction-local scope setter SHALL map the authenticated
`session_user`, not the security-definer `current_user`, through an active,
unexpired `assume_scope` authority grant, reject caller-selected ungranted scope,
and clear scope on connection checkout/return. Every transaction SHALL recheck
grant revocation and principal/layer lifecycle state; revocation or retirement
SHALL invalidate new scope and already-pooled connections. Missing, malformed,
stale, forged, cross-stack, cross-installation, and pooled-connection scope reuse
SHALL fail closed.

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
openxFactory SHALL publish a fresh-install v2 operational Postgres contract, a typed migration-mapping schema, and an executable idempotent v1-to-v2 migration without rewriting v1 contract definitions or existing source-row bytes in place. A successful cutover MAY add the governed durable write-freeze required below while preserving readable v1 history; it MUST NOT silently continue writable v1 state without a governed dual-write contract. Initialization and reapplication SHALL use one locked preflight/apply/postflight boundary: preflight SHALL compare every existing canonical object and security authority before mutating DDL or role repair; apply SHALL execute transactionally only for empty or exact accepted state; and postflight SHALL prove the selected fresh-v2 or v1-cutover profile before success. It SHALL fail on incompatible pre-existing tables, policies, functions, triggers, role attributes/memberships, schema/table/function ownership and ACLs, row-security enable/force flags, security-definer/search-path configuration, PUBLIC privileges, quarantine grants, durable-freeze objects, or quarantine dependency guards.

Migration SHALL consume a detached, content-addressed mapping payload that fixes the source database/schema identity, exact v1 catalog profile, expected per-table row counts and dataset digest, subject and administrative/principal mappings, target topology, and migration policy. A separate authority envelope SHALL bind that payload digest to the exact approver principal, active `run_migration` grant, policy digest, scope, and trust-anchor chain without including the authority envelope in the payload digest. After acquiring one session advisory lock on installation plus migration ID, the runner SHALL persist append-only attempt evidence, begin the authoritative transaction at `SERIALIZABLE`, and acquire the fixed v1 table locks in bytewise order before reading governed source rows.

Under those locks, PostgreSQL SHALL recompute the source catalog, counts, and dataset digest and derive a logical source-boundary ID from those values plus source identity. It SHALL abort atomically when that observed content differs from the approved payload. For an accepted attempt, PostgreSQL SHALL create an immutable cutover envelope that binds the payload and authority-envelope digests, logical boundary, database-observed transaction snapshot and WAL position, active `run_migration` authority, database-derived time, and reconciliation digest. Every one of the twelve canonical v1 tables SHALL reconcile exactly once: each source row and identifier SHALL appear in exactly one scoped, immutable, non-authorizing compatibility-history record or, only for an unverifiable legacy artifact, approval, or trace row, in exactly one non-authoritative quarantine record. No migrated legacy history SHALL acquire v2 execution or approval authority merely by migration.

The dataset digest SHALL use profile `xfactory-v1-dataset-binary-v1`. Its byte stream begins with ASCII `XFV1DS` followed by bytes `00 01`. Every frame is `tag:u8 || payload_length:u64be || payload`. The stream then concatenates table frames tagged `10`. Each table payload contains schema-name frame `11`, table-name frame `12`, column-count frame `13` whose payload is `u64be`, one column frame `14` per schema ordinal whose payload is `ordinal:u64be || nullable:u8 || primary_key_position:u64be || name-frame-15 || normalized-type-frame-16`, row-count frame `17` whose payload is `u64be`, and row frames `20`. `nullable` is exactly `00` or `01`; primary-key position is zero for a non-key column and one-based otherwise; and normalized type is exactly one ASCII value from `text`, `int4`, `int8`, `bool`, `timestamptz`, `jsonb`, or `bytea`. A row payload concatenates one column frame `21` per schema ordinal; each column payload is `ordinal:u64be || value-frame`. Value frames are null `30` with an empty payload, text `31` as UTF-8, integer `32` as minimal base-10 UTF-8 with no plus sign or leading zero, boolean `33` as exactly byte `00` or `01`, timestamp `34` as UTC RFC 3339 UTF-8 with exactly six fractional digits and `Z`, binary `35` as lowercase-hex ASCII, and JSON `36` as the canonical UTF-8 form below.

Tables SHALL sort by raw UTF-8 `(schema, table)` bytes; rows SHALL sort lexicographically by the concatenation of their framed primary-key value frames, never database collation; columns SHALL remain in schema ordinal order; and no Unicode normalization SHALL occur. Canonical JSON SHALL preserve array order; sort object keys by raw UTF-8 bytes; escape only quotation mark, reverse solidus, and control code points `U+0000` through `U+001F` using lowercase `\u00xx`; emit `true`, `false`, and `null` literally; and render arbitrary-precision decimal numbers without exponent or plus sign, without insignificant leading or trailing zeros, and with negative zero normalized to `0`. SHA-256 SHALL cover the magic/version bytes plus every complete ordered table frame. Missing, conflicting, or ambiguous scope, concurrent source drift, reconciliation mismatch, non-canonical staging, or replay with a changed mapping payload, authority envelope, or logical boundary SHALL abort atomically.

Successful cutover SHALL install a durable v1 governed-write freeze in the same transaction before releasing the source locks while preserving the unchanged v1 contract and readable history. `STARTED` SHALL survive before the authoritative transaction; `SUCCEEDED` SHALL commit with its cutover envelope and reconciliation; `FAILED` or `ABANDONED` SHALL be appended only after rollback or crash recovery. Retry identity SHALL be installation plus migration ID, mapping-payload digest, and logical boundary. An identical retry MAY record a different physical snapshot/WAL observation after rollback only when the logical boundary is unchanged; it SHALL converge exactly once, and a retry after committed success SHALL return the stored result without reapplying rows. Quarantine SHALL remain unavailable to runtime roles, authoritative tables, views, foreign keys, and gates, and any later governed evidence SHALL be created anew through normal current authority.

#### Scenario: Clean v2 database is initialized twice
- **WHEN** the v2 DDL is applied to an empty supported Postgres database and applied again
- **THEN** both applications MUST pass locked preflight and transactional apply plus postflight with the same canonical resulting contract state and without repairing drift before comparison

#### Scenario: Same-named database object or security authority has drifted
- **WHEN** a pre-existing table, policy, function, trigger, role attribute/membership, owner, ACL, row-security flag, function security/search path, PUBLIC privilege, quarantine grant/dependency guard, or durable-freeze object has the expected name but an incompatible definition or checksum
- **THEN** v2 readiness MUST fail rather than silently accepting `IF NOT EXISTS`

#### Scenario: Two-subject v1 database is migrated
- **WHEN** a seeded v1 database contains two legacy project values and a complete explicit mapping to two Customer layers
- **THEN** migration MUST preserve every row ID, assign each related row to the correct layer or installation-administration scope, and classify every row from all twelve canonical v1 tables exactly once as non-authorizing compatibility history or permitted quarantine

#### Scenario: Migration mapping is ambiguous
- **WHEN** a legacy value maps to multiple layers or a scoped legacy row has no provable mapping
- **THEN** the migration transaction MUST abort without partial v2 state

#### Scenario: Source changes during cutover
- **WHEN** a v1 governed write races migration or the observed catalog, row counts, or dataset digest no longer match the approved logical boundary
- **THEN** migration MUST abort or exclude the write through the proven cutover locks and successful durable v1 write freeze
- **AND** no successful ledger entry may omit the row

#### Scenario: Migration is retried with another map
- **WHEN** a completed or interrupted migration ID is replayed with a different mapping-payload digest, authority-envelope digest, or logical source boundary
- **THEN** the migration MUST fail closed
- **AND** a new physical snapshot/WAL observation after rollback MAY converge only when the approved payload and logical boundary are unchanged

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
