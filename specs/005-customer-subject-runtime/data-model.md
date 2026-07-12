# Data Model: Neutral Hermes Customer-Subject Runtime Contracts

Status: draft

**Date**: 2026-07-12

**Feature**: `005-customer-subject-runtime`

## Modeling Rules

- Static DomainxFactory Hermes layers are role templates; runtime layers are durable instances.
- This G0 profile has one installation, exactly one stack, one Client singleton, one Domain singleton, and zero-to-many Customer instances.
- Every layer-owned authoritative identity uses full scope `(installation_id, stack_id, layer_id, id)`.
- Customer-layer local IDs are not globally unique across layers; constraints and FKs retain the full scope to avoid existence oracles.
- Immutable records are inserted once. Lifecycle, revocation, cancellation, and correction are new append-only events.
- Content-bearing references use lowercase `sha256:<64hex>` digests and immutable scoped resource coordinates.
- Real-world subject identity is never present. Resolution of `urn:xfactory:subject:<uuid>` stays with the domain issuer.
- Quarantine records have no authoritative FK/view path and cannot be promoted in place.

## Topology And Identity

### Installation

Represents one deployed Hermes authority boundary.

| Field | Required | Rules |
|---|---:|---|
| `installation_id` | yes | Durable neutral ID; never reused |
| `initial_lifecycle_state` | yes | Immutable constant `installing`; current state is event-derived |
| `genesis_anchor_id` | yes | Immutable out-of-band-approved genesis anchor; active as-of roots derive from anchor events |
| `created_at` | yes | Immutable RFC 3339 timestamp |

Relationship: exactly one Stack for this G0 profile. General multi-stack installation support is explicitly out of scope.

Active trust is a derived projection evaluated from the immutable genesis anchor and append-only TrustAnchorEvents at the operation's authorization time; Installation is never mutated to point at a rotating active root. Installation lifecycle is likewise derived from its immutable initial state and lifecycle-event chain; retirement time is the terminal event time, not a mutable Installation field.

### Stack

Represents the one DomainxFactory assembly installed inside an Installation.

| Field | Required | Rules |
|---|---:|---|
| `installation_id` | yes | Parent Installation |
| `stack_id` | yes | Durable within installation; never reused |
| `domain_id` | yes | Domain-owned neutral identifier |
| `domain_stack_pin` | yes | Exact Git file/overlay pin |
| `contract_bundle_pin` | yes | Exact openxFactory bundle identity |
| `initial_lifecycle_state` | yes | Immutable constant `installing`; current state is event-derived |

### RoleTemplate

The static `stack.yaml` declaration for one canonical role.

| Field | Required | Rules |
|---|---:|---|
| `role` | yes | Exactly one each of `customer`, `client`, `domain` |
| `display_name` | yes | Domain alias; non-authoritative |
| `overlay` | yes | Repository-relative overlay root/manifest |
| `authority_scope` | extension only | An extension cannot represent a Customer subject |

### LayerRegistration

Immutable identity registration for one concrete role instance. Its terminal
tombstone is the registration plus terminal lifecycle event; neither is deleted.

| Field | Required | Rules |
|---|---:|---|
| `installation_id`, `stack_id`, `layer_id` | yes | Durable composite identity |
| `role` | yes | `customer`, `client`, or `domain` |
| `template_role` | yes | References one static RoleTemplate |
| `display_name` | yes | Domain alias/display only |
| `policy_namespace` | yes | Unique for stack lifetime, including retired layers |
| `overlay_manifest_pin` | yes | Exact manifest commit/path/digest |
| `initial_lifecycle_state` | yes | Immutable constant `provisioning`; current state is event-derived |
| `customer_subject` | Customer only | CustomerSubjectRef; forbidden on Client/Domain |
| `created_at` | yes | Immutable |

Uniqueness: `layer_id`, `policy_namespace`, and Customer subject tuple are lifetime-unique. Rows cannot be hard-deleted.

### CustomerSubjectRef

Pseudonymous domain subject bound to one Customer LayerRegistration.

| Field | Required | Rules |
|---|---:|---|
| `kind` | yes | Domain-owned string, not neutral enum |
| `issuer` | yes | Stable non-sensitive issuer ID |
| `namespace` | yes | Non-sensitive issuer namespace |
| `ref` | yes | `urn:xfactory:subject:<uuid>` |
| `reference_policy_pin` | yes | Exact policy path/commit/digest |
| `issuer_attestation_digest` | yes | Attests approved random/keyed construction |

Approved construction: independently generated UUIDv4/UUIDv7 or approved keyed tokenization. UUIDv1/v3/v5, direct identifiers, reversible encodings, and unkeyed derivations are invalid.

### OverlayManifest

Content-addressed directory overlay inventory.

| Field | Required | Rules |
|---|---:|---|
| `repository` | yes | Canonical repository identifier |
| `commit` | yes | Exact 40-hex commit |
| `overlay_root` | yes | Normalized repository-relative directory |
| `files[]` | yes | Every regular file recursively under root, bytewise path order |
| `files[].path` | yes | Unique, normalized, within root |
| `files[].digest` | yes | Raw-file SHA-256 |
| `exclusions[]` | yes | Closed supported exclusions only |

No symlink, submodule, traversal, missing, or extra regular file is accepted.

### InstallationLifecycleEvent / StackLifecycleEvent / LayerLifecycleEvent

These three closed record shapes are the authoritative lifecycle source for
their corresponding immutable identity registrations.

| Field | Required | Rules |
|---|---:|---|
| `event_id`, `event_digest` | yes | Durable ID and digest over the immutable event |
| entity scope | yes | Exact installation, stack, and layer coordinates applicable to the event kind |
| `predecessor_ref` | yes | Exact registration ID/digest for the first event, otherwise prior event ID/digest |
| `from_state`, `to_state` | yes | One allowed edge in the entity's closed state graph |
| `authority_grant_id`, `authority_grant_digest` | yes | Exact active authority for the transition |
| `occurred_at` | yes | Database-derived transition time |
| `reason` | yes | Non-empty governed reason code/text |

For one entity, the registration/event graph has exactly one successor per
predecessor and no forks or cycles. A governed transition locks the entity and
latest event, validates authority and the requested edge, appends the event,
and updates any cache projection in one transaction. The first event must name
the immutable registration as predecessor and start at its initial state.
Update/delete privileges and defensive triggers reject changes to registrations
or events.

### LifecycleProjection

The database may maintain installation/stack/layer current-state projection
rows containing the entity scope, latest event ID/digest, derived state, and
derived terminal time. These rows are non-authoritative, unavailable for direct
runtime mutation, and writable only by the governed transition function in the
same transaction as event append. Readiness recomputes every projection from
the registration/event chain and fails on drift; direct projection mutation is
rejected and cannot authorize work.

## Topology State Machines

Every state shown below is derived from the immutable registration and its
linear lifecycle-event chain; it is not updated on the identity record.

### Installation/Stack Topology

```text
installing ──▶ configured ──▶ operational ──▶ suspended
    │              │              │              │
    │              └──────────────┴──────────────┤
    └────────────────────────────────────────────▶ retired

suspended ──▶ operational
retired: terminal
```

- `installing`: at most one non-retired Client and Domain; no Customer registration.
- `configured`: exactly one active Client and Domain; zero or more active Customers.
- `operational`: configured cardinality plus at least one active Customer.
- `suspended`: registrations preserved; no new governed jobs.
- `retired`: every layer retired; no new work.

### Layer

```text
provisioning ──▶ active ──▶ suspended
      │            │           │
      ├──▶ failed ◀─┴───────────┤
      │      │                  │
      │      └──▶ provisioning  │
      └─────────────────────────┴──▶ retired

suspended ──▶ active
retired: terminal
```

Failed recovery requires a new governed lifecycle event. Retirement preserves all evidence and tombstones.

## Principal And Authority

### InstallationTrustAnchor

Out-of-band-approved genesis authority.

| Field | Required | Rules |
|---|---:|---|
| `anchor_id` | yes | Durable installation-scoped ID |
| `installation_id` | yes | Exact installation |
| `principal_ref` / `key_ref` | yes | Reference only, no secret/key bytes |
| `policy_ref`, `policy_digest` | yes | Exact root policy |
| `effective_at` | yes | Database-derived/as-of evaluation time |
| `authorized_evidence_digest` | yes | External approval evidence |

### TrustAnchorEvent

Append-only `rotated` or `revoked` event authorized under the then-current anchor policy. Historical operation evidence retains the anchor chain valid at its `authorized_at` time.

### Principal

Neutral actor identity used by authority and database mappings.

Fields: scoped `principal_id`, `principal_type`, lifecycle, owning scope, and optional external reference. No credential material.

### DatabasePrincipalBinding

Maps one authenticated PostgreSQL `session_user` to one Principal. A runtime login is non-escalatable and has only the granted role class. Binding lifecycle is append-only/revocable.

### AuthorityGrant

Immutable scope/action/resource authority link.

| Field | Required | Rules |
|---|---:|---|
| `grant_id` | yes | Installation-scoped durable ID |
| `principal_ref` | yes | Grantee |
| `issuer_grant_ref` | non-genesis | Must authorize `issue_grant` |
| `scope` | yes | Installation/stack/layer or explicit admin scope |
| `action` | yes | One closed action |
| `resource_constraint` | yes | Exact type/ID and digest where content-bearing |
| `policy_ref`, `policy_digest` | yes | Immutable governing policy |
| `starts_at`, `expires_at` | yes | Database-derived evaluation |

Validation walks an acyclic, scope-narrowing chain to an active as-of trust anchor. Revocation is a separate AuthorityGrantRevocation.

### CrossLayerBinding

Immutable one-action authorization from exact source to target.

Fields: binding ID, source/target layer scopes, exact source resource, exact target resource, action, purpose, creator grant, optional target-acceptance grant, starts/expires. Content resources require digests. Identity-level digest omission is limited to the closed allowed types.

### OperationAuthorization

Immutable output of the atomic authorization transaction.

Fields: operation ID, exact source/target resources, binding ID/digest, all grant IDs/digests, trust-anchor/as-of references, action/purpose, database-derived `authorized_at`, target result ID/digest, and transaction correlation. It is inserted atomically with the governed target and trace.

## Governed Evidence

### ArtifactRecord

Entirely immutable metadata for finalized bytes.

Fields: owning scope, artifact ID, content digest, byte size, media type, producer principal/grant, scoped storage key `<installation>/<layer>/sha256/<hex>`, created time, optional job/run. Lifecycle is represented only by ArtifactLifecycleEvent.

### ApprovalDecisionPolicy

Immutable policy defining reviewer selectors, required counts/roles, aggregation, conflict handling, expiry rules, and supersession authorities. It is pinned by reference and digest.

### ApprovalRequest

Immutable target/action request containing exact target type/ID/digest/scope, requester principal/grant, reviewer selector, decision-policy pin, authority scope, created/expiry time.

### ApprovalDecision

Immutable reviewer decision repeating exact request target/action/scope/policy plus actual reviewer principal/grant, decision, rationale reference, and database-derived time.

### ApprovalSupersessionEvent

Append-only expiry/cancellation/revocation containing target request/decision, issuer principal/grant/digest, scope, reason, and database-derived effective time.

### TraceabilityEdge

Immutable digest-addressed relation between source and target resource endpoints. Cross-layer edges cite OperationAuthorization, CrossLayerBinding, and grants; same-layer edges cannot claim unrelated cross-layer authority. Trace is evidence, never a grant.

## Job Lifecycle V2

### HermesJobEnvelopeV2

Neutral job request with exact layer scope, job identity/type, issuer, workflow references, worker/routing requirements, approval requirements, outputs, trace root, and stop conditions. No Project/repository/feature noun is required by the neutral core.

### HermesJobRunV2

Run state bound to the exact job scope and identity. Contains worker/auth references, stage/status, immutable event/artifact/approval/trace references, and summary references.

### HermesJobEventV2

Append-only event bound to exact job/run scope, monotonic sequence, actor principal, event type, database-derived occurrence time, and schema-validated payload reference.

## Migration

### MigrationMapping

Typed, content-addressed, authority-approved cutover input.

Fields include migration ID, source DB/schema identity, fixed v1 table definitions, snapshot/WAL identity, row-count/dataset-digest evidence, legacy subject-to-layer mappings, explicit group/profile/worker admin mappings, single-default proof where applicable, target topology pin, mapping digest, approver grant/policy digest, and deterministic digest-profile version.

### MigrationAttempt / MigrationAttemptEvent

Append-only attempt identity and lifecycle events. The latest-event graph is `started -> succeeded|failed|abandoned`, `failed|abandoned -> started` for identical retry, and `succeeded` terminal. A transaction advisory lock derived from `(migration_id, source_snapshot, mapping_digest)` is acquired before state evaluation, so concurrent identical retries yield one executor and one convergent observer. Unique tuple identity makes exact retry converge; changed snapshot/map fails. Success records input/output counts/digests and target contract identity.

### LegacyQuarantineRecord

Non-authoritative preserved source evidence.

Fields: migration ID, source schema/table, canonical source PK, source-row digest, closed reason code, raw-row JSON, captured time. Quarantine has no runtime/control USAGE, no outward authoritative FK/view, and no in-place promotion.

## Contract And Release Evidence

### ContractIndex

Closed catalog of every required family contract with ID, path, type, schema version, intended consumers, and semantic/release membership.

### FixtureCase

Indexed case with phase/class, requirements/scenarios, ordered inputs, fixed evaluation time, expected outcome and stable finding code, and evidence ID.

### AcceptanceMap / EvidenceRegister

Stable mappings from OpenSpec capability requirements/scenarios to feature FRs, fixtures/tests, and recorded results. Parity is exact: missing, duplicate, dangling, or skipped required evidence fails.

### DomainRegressionEntry

Versioned supported-consumer denominator: canonical repository, exact published commit, stack path/raw-blob digest, domain ID, expected openxFactory pin/schema, and expected result. Explicit exclusions carry reason/evidence.

### ReleaseDigestInventory

Closed realized bundle membership. Fields: bundle tag, canonical repository, digest algorithm/source/order, and unique bytewise-sorted entries containing artifact ID/path/type/Git mode/schema identity/version/digest. The inventory excludes itself and contains no commit to avoid circularity.

### HermesG0HandoffReceipt

openxFactory-side external receipt stored at `openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/hermes-install-g0-handoff.yaml` and validated against `contracts/hermes-runtime/consumer-handoff-receipt.schema.yaml` only after Hermes Install lands. Its `consumer_repository` is the schema constant `opensoft/xFactory-Hermes-Install`; `FarHeap/Hermes-Install` is a different single-layer product and is rejected. It pins the exact Hermes repository commit and its `evidence/gates/g0/<bundle-tag>.yaml` packet path/digest; that downstream packet validates against `config/schemas/g0-closure-evidence.schema.yaml` and owns manifest/checker/runtime/evidence paths/digests and positive/negative results.
