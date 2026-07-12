# Planning Contract: Canonical Schema Inventory

Status: draft

This inventory defines the intended canonical family boundary. Implementation may refine file internals but must not silently omit or merge authorities that have distinct immutability, lifecycle, or pinning requirements.

## Family Metadata

| Path | Purpose |
|---|---|
| `contracts/hermes-runtime/README.md` | Ownership, consumers, versioning, lifecycle, and validation guide |
| `contracts/hermes-runtime/contract-index.yaml` | Closed required-file/contract-ID catalog |
| `contracts/hermes-runtime/acceptance-map.yaml` | OpenSpec requirement/scenario to evidence map |
| `contracts/hermes-runtime/evidence-register.yaml` | Stable fixture/test evidence bindings |
| `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` | Realized supported DomainxFactory commit/path/digest denominator; indexed by `fixtures/index.yaml` |
| `contracts/hermes-runtime/shared-definitions.schema.yaml` | IDs, digests, scopes, Git pins, principal/resource references |

## Topology And Identity

| Path | Contract identity |
|---|---|
| `customer-subject-reference-profile.schema.yaml` | Approved pseudonymous reference construction and attestation |
| `overlay-manifest.schema.yaml` | Complete recursively inventoried overlay root |
| `runtime-topology.schema.yaml` | Installation/stack/layer instances, lifecycle, cardinality, tombstones |
| `installation-lifecycle-event.schema.yaml` | Append-only predecessor-linked Installation state transition |
| `stack-lifecycle-event.schema.yaml` | Append-only predecessor-linked Stack state transition |
| `layer-lifecycle-event.schema.yaml` | Append-only predecessor-linked Layer state transition and retirement tombstone |
| `domain-regression-inventory.schema.yaml` | Versioned supported DomainxFactory denominator |

## Authority And Cross-Layer Operations

| Path | Contract identity |
|---|---|
| `installation-trust-anchor.schema.yaml` | Out-of-band genesis authority |
| `installation-trust-anchor-event.schema.yaml` | As-of rotation/revocation |
| `principal.schema.yaml` | Neutral principal identity and lifecycle |
| `principal-lifecycle-event.schema.yaml` | Append-only principal suspension/retirement |
| `database-principal-binding.schema.yaml` | Authenticated database login to Principal binding |
| `database-principal-binding-revocation.schema.yaml` | Append-only login-binding revocation |
| `authority-grant.schema.yaml` | Immutable scope/action/resource grant chain |
| `authority-grant-revocation.schema.yaml` | Append-only grant revocation |
| `cross-layer-binding.schema.yaml` | Exact source/target one-action binding |
| `cross-layer-binding-revocation.schema.yaml` | Append-only binding revocation |
| `operation-authorization.schema.yaml` | Atomic authorization result and authority proof |

## Governed Evidence

| Path | Contract identity |
|---|---|
| `artifact-record.schema.yaml` | Immutable scoped content record |
| `artifact-lifecycle-event.schema.yaml` | Append-only artifact state transition |
| `approval-request.schema.yaml` | Immutable requester/target/policy request |
| `approval-decision-policy.schema.yaml` | Reviewer selection/aggregation/conflict policy |
| `approval-decision.schema.yaml` | Immutable actual reviewer decision |
| `approval-supersession-event.schema.yaml` | Authorized expiry/cancel/revoke event |
| `traceability-edge.schema.yaml` | Digest-bound source/target evidence and operation proof |

## Job And Persistence

| Path | Contract identity |
|---|---|
| `hermes-job-envelope-v2.schema.yaml` | Neutral scoped job request |
| `hermes-job-run-v2.schema.yaml` | Neutral scoped run state |
| `hermes-job-event-v2.schema.yaml` | Neutral scoped append-only event |
| `legacy-quarantine-record.schema.yaml` | Structurally non-authoritative legacy evidence |
| `hermes-operational-postgres-v2.sql` | Fresh-install authoritative/API/quarantine namespaces |
| `migrations/v1-to-v2-mapping.schema.yaml` | Frozen-source typed mapping and digest profile |
| `migrations/v1-to-v2.sql` | Atomic, idempotent cutover |

## Release

| Path | Contract identity |
|---|---|
| `contracts/releases/release-digest-inventory.schema.yaml` | Closed raw-Git-blob inventory shape |
| `contracts/releases/<bundle-tag>.digests.yaml` | Realization-time inventory; excludes itself |
| `contracts/hermes-runtime/consumer-handoff-receipt.schema.yaml` | Content-addressed downstream Gate G0 acceptance receipt |

## Common Schema Rules

- Draft 2020-12 with canonical ID base `https://xforge.us/schemas/openxfactory/hermes-runtime/v2/`; each schema `$id` is the base plus its family-relative path, and every cross-file `$ref` is relative within that base.
- The offline catalog rejects IDs outside the canonical base, duplicate IDs, alternate URI aliases for one path, and any unregistered resolution.
- Every YAML schema also carries top-level annotation keywords `schema_version` and `kind` in addition to `$schema`, `$id`, `contract_id`, and `contract_schema_version`; the catalog requires them.
- `contract_id` and integer `contract_schema_version` on every canonical schema.
- Closed authority, lifecycle, scope, resource, and evidence shapes.
- Explicit namespaced extension objects only where additive data is safe; extensions never grant authority.
- Lowercase `sha256:<64hex>` for content-addressed references.
- Repository-relative normalized paths; no absolute path, traversal, symlink, submodule, or mutable branch pin.
- Structural schemas do not pretend to enforce temporal, graph, Git-object, or transactional semantics; the canonical validator and PostgreSQL contract do.
- Hash-locked validator inputs `requirements/hermes-runtime-contracts.in` and `requirements/hermes-runtime-contracts.lock` are semantic release members alongside validator code.
- `tests/hermes_runtime_contracts/postgres/images.lock.yaml` is a semantic release member so PostgreSQL 15/16 conformance evidence is tied to immutable image digests rather than mutable major tags.
