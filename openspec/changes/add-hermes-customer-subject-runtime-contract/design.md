Status: ratified
Ratified by: user approval of `add-hermes-customer-subject-runtime-contract` on 2026-07-12

## Context

`docs/xfactory-domain-factory-model.md` already establishes that each customer subject receives one Customer Hermes instance or logical team. The same neutral role maps to Project Hermes in codexFactory, Patient Hermes in MedxFactory, and Client Company or Ledger Hermes in LedgerxFactory. The current machine contracts do not realize that architecture: `xfactory-domain-stack.schema.yaml` and `validate-domain-factory.py` intentionally collapse the static declaration to one layer per canonical role, v1 job records still require the engineering noun `project`, and the v1 operational DDL has no installation/stack/layer scope.

Gate G0 therefore requires a new neutral runtime-instance contract rather than a codex-specific exception in Hermes Install. The change crosses topology, durable data, authorization, migration, validation, release identity, and a downstream compatibility pin. Existing v1 consumers and existing DomainxFactory `stack.yaml` files must remain valid while new Hermes runtimes opt into v2.

## Goals / Non-Goals

**Goals:**

- Make the documented one-Customer-Hermes-per-subject pattern canonical and machine-checkable for every DomainxFactory.
- Distinguish static role templates from concrete runtime layer instances without weakening the existing one-template-per-role rule.
- Define installation, stack, layer, and customer-subject identity plus lifecycle-aware cardinality.
- Enforce default-deny subject isolation and exact, auditable cross-layer authority.
- Make artifacts, approvals, and trace records content-addressed, immutable, scoped, and revocable where authority is involved.
- Supply parallel v2 message and Postgres contracts plus an atomic, idempotent v1-to-v2 migration.
- Prove the model with two active Customer instances in one installation and domain-neutral mapping fixtures.
- Publish a content-addressed contract bundle and require Hermes Install to verify its pin before dependent implementation.

**Non-Goals:**

- Implement or deploy a Hermes service, manager profile, worker pool, or DomainxFactory runtime.
- Define project, patient, client-company, clinical, accounting, or engineering policy in the neutral repository.
- Permit direct cross-layer database visibility; bindings authorize explicit governed operations, not broad row access.
- Remove or reject v1 schemas during the additive compatibility window.
- Reuse a customer-subject identity, layer identity, or policy namespace after retirement.
- Allocate a bundle minor version before release realization establishes the next available version.

## Decisions

### 1. Static role declarations remain templates; runtime instances are separate

`stack.yaml hermes.layers` continues to declare exactly one Customer, one Client, and one Domain role template. Duplicate canonical roles remain invalid. Its descriptions and validator messages will explicitly call these declarations templates, and `per_customer_subject` will be added as a neutral isolation vocabulary value without removing existing domain aliases.

A new `contracts/hermes-runtime/runtime-topology.schema.yaml` owns concrete instances. This avoids breaking every DomainxFactory, preserves unambiguous workflow ownership by canonical role, and lets subject onboarding occur without source-repository edits.

**Alternative considered:** repeat `role: customer` in `stack.yaml`. Rejected because the file is a reusable DomainxFactory declaration, its validator indexes by role, and runtime subjects are private lifecycle state rather than source configuration.

### 2. `customer_subject` is the canonical repeatable identity

Every Customer instance carries `customer_subject.kind`, `customer_subject.issuer`, `customer_subject.namespace`, `customer_subject.ref`, and a pinned reference-policy attestation. `kind` is domain-owned vocabulary. `ref` uses the constrained `urn:xfactory:subject:<uuid>` surrogate format and is resolved only by the owning domain system. The policy requires an independently generated cryptographically random UUIDv4/UUIDv7 surrogate or approved keyed tokenization; UUIDv3/v5, reversible encoding, raw/unkeyed hashes, and other deterministic derivation from a patient, account, or source identifier are forbidden. The issuer attests that the surrogate contains no direct identifier or secret. Deterministic sentinel/deny-pattern scans are defense in depth; the neutral validator does not claim that arbitrary PII can be recognized semantically.

Client and Domain instances must not carry `customer_subject`. Domain overlays may expose aliases such as project, patient, or client company, but canonical lifecycle operations remain provision/retire customer subject.

**Alternative considered:** canonical `project_ref`. Rejected because it makes the shared contract engineering-specific and cannot represent patients, companies, campaigns, ledgers, or managed systems honestly.

### 3. Topology identity and cardinality are lifecycle-aware

The topology records immutable Installation, Stack, and Layer registrations with durable IDs, initial state, exact DomainxFactory/template pins, and append-only lifecycle-event chains. Each layer registration records a globally durable `layer_id`, canonical role, display name, unique policy namespace, exact overlay pin, and immutable initial state. Current state is derived from one predecessor-linked chain; any current-state projection is non-authoritative, reconciled to the chain, and writable only by a governed transition in the same transaction as event append. Direct registration/state mutation, lifecycle event update/delete, a forked predecessor, and every transition out of retired fail closed.

- Topology states are `installing`, `configured`, `operational`, `suspended`, and `retired`; allowed transitions are installing to configured, configured to operational or retired, operational to suspended or retired, suspended to operational or retired, and no transition out of retired.
- Layer states are `provisioning`, `active`, `suspended`, `failed`, and `retired`; provisioning may become active, failed, or retired; active may suspend, fail, or retire; suspended may reactivate, fail, or retire; failed may re-enter provisioning through a governed recovery or retire; retired is terminal.
- `installing` allows at most one non-retired Client and Domain registration and zero Customer registrations.
- `configured` requires exactly one active Client and one active Domain and permits zero or more active Customer instances.
- `operational` requires exactly one active Client, exactly one active Domain, and at least one active Customer instance.
- `suspended` preserves all registrations but permits no new governed jobs; `retired` requires terminal retirement of every layer and permits no new work.
- A conformance fixture must contain at least two active Customer instances.
- Registrations and lifecycle events are never updated or hard-deleted. Layer IDs, customer-subject tuples, and policy namespaces are protected by the registration plus terminal-event tombstone and are unique for the lifetime of the stack, including retired instances.

Single-file pins use a canonical repository identifier, repository-relative regular-file path, exact 40-hex commit, schema identifier/version where applicable, and SHA-256 digest. Directory overlays are pinned through an `overlay-manifest.schema.yaml` document containing one repository-relative `overlay_root`, a bytewise-sorted inventory of every regular file recursively below that root, raw-file SHA-256 digests, and the closed exclusions `.gitkeep` and an optional colocated generated digest inventory. The runtime pin identifies and hashes that manifest. Branch-only, tag-only, unresolved, traversing, symlink-escaping, incomplete, or digest-drifted pins fail.

### 4. The v2 contract family is explicit and composable

New contracts live under `contracts/hermes-runtime/`:

- `shared-definitions.schema.yaml`
- `customer-subject-reference-profile.schema.yaml`
- `overlay-manifest.schema.yaml`
- `runtime-topology.schema.yaml`
- `installation-lifecycle-event.schema.yaml`
- `stack-lifecycle-event.schema.yaml`
- `layer-lifecycle-event.schema.yaml`
- `installation-trust-anchor.schema.yaml`
- `installation-trust-anchor-event.schema.yaml`
- `principal.schema.yaml`
- `principal-lifecycle-event.schema.yaml`
- `database-principal-binding.schema.yaml`
- `database-principal-binding-revocation.schema.yaml`
- `authority-grant.schema.yaml`
- `authority-grant-revocation.schema.yaml`
- `cross-layer-binding.schema.yaml`
- `cross-layer-binding-revocation.schema.yaml`
- `operation-authorization.schema.yaml`
- `artifact-record.schema.yaml`
- `artifact-lifecycle-event.schema.yaml`
- `approval-request.schema.yaml`
- `approval-decision-policy.schema.yaml`
- `approval-decision.schema.yaml`
- `approval-supersession-event.schema.yaml`
- `traceability-edge.schema.yaml`
- `hermes-job-envelope-v2.schema.yaml`
- `hermes-job-run-v2.schema.yaml`
- `hermes-job-event-v2.schema.yaml`
- `hermes-operational-postgres-v2.sql`
- `legacy-quarantine-record.schema.yaml`
- `consumer-handoff-receipt.schema.yaml`
- `migrations/v1-to-v2-mapping.schema.yaml`
- `migrations/v1-to-v2.sql`

Release identity is defined by `contracts/releases/release-digest-inventory.schema.yaml`; realized inventories live at `contracts/releases/<bundle-tag>.digests.yaml` and are checked by `scripts/validate-contract-release.py`.

Every governed v2 record uses the same closed scope tuple: `installation_id`, `stack_id`, and `layer_id`. Cross-layer records carry exact source and target scopes. Installation-wide administrative state uses an explicit installation scope; it is never assigned to a fabricated Customer layer.

### 5. Isolation is default-deny; bindings authorize bounded operations

Each Customer layer has a unique policy namespace and persistence scope. The v2 SQL contract separates a non-login migration/table-owner role, per-layer runtime principals, an installation control-plane principal, and an audit-export principal. Runtime principals have no `BYPASSRLS`, cannot assume owner/admin roles, and reach governed tables only under forced row-level security. A trusted security-definer scope setter maps the authenticated `session_user` through an active, unexpired `assume_scope` authority grant and sets transaction-local scope; it MUST NOT authorize from `current_user`, which resolves to the function owner inside a security-definer function, and callers cannot supply an ungranted scope. Every transaction rechecks grant and principal/layer lifecycle state. Grant revocation or principal/layer retirement invalidates new scope and already-pooled connections. Connection checkout and return clear scope, and missing, malformed, stale, cross-installation, or reused scope fails closed. Installation administration grants no direct subject-data visibility. The control plane has only execute permission on governed operations and no direct table access.

Each installation begins with one immutable, out-of-band-approved trust-anchor record whose key/principal and policy digest may issue only root-scoped grants. Every non-genesis authority grant cites an issuer grant authorized for `issue_grant`; validation walks to the active trusted anchor, rejects self-issuance and cycles, and enforces scope narrowing. Anchor rotation/revocation is an append-only event requiring the current anchor policy and does not rewrite historical evidence. Source-layer authority is required for disclosing a source resource.

For the G0 realization, there is exactly one genesis anchor and at most one
active root at any evaluation time. Each replacement anchor is another
immutable record; one linear `rotate` event activates it and deactivates its
predecessor, while a `revoke` event may leave no active root and therefore
fails all new authorization closed. A root grant cites the active anchor and
has no issuer grant; every delegated grant cites an `issue_grant` grant.
Historical evidence resolves the anchor active at its recorded authorization
time. Principal types are the closed set `human`, `agent`, `service`, and
`group`; their closed lifecycle is `provisioning -> active|retired`,
`active -> suspended|retired`, `suspended -> active|retired`, with terminal
retirement.

Authority grants are immutable records containing principal, issuer grant, source scope, allowed action, exact resource constraints, policy digest, effective time, and expiry; revocation is append-only. Cross-layer bindings cite the creator's active authority grant and contain exact source/target layers, exact `source_resource` and `target_resource` coordinates, one allowed action, purpose, start time, and expiry. Both resources require digests for content-bearing types; digest omission is permitted only for the closed identity types `layer_identity`, `principal_identity`, and `policy_namespace`. Target acceptance authority is also required when the pinned target policy demands it. Wildcards, inheritance, self-bindings, cycles, and transitive authority are invalid.

G0 uses the closed action vocabulary `assume_scope`, `issue_grant`,
`revoke_grant`, `rotate_trust_anchor`, `revoke_trust_anchor`,
`create_binding`, `revoke_binding`, `accept_cross_layer`,
`project_resource`, `create_artifact`, `decide_approval`,
`request_approval`, `supersede_approval`, `transition_lifecycle`, `run_migration`, and
`publish_contract`. Every authority record uses
`xfactory-canonical-json-v1`: SHA-256 over UTF-8 compact, sorted-key JSON of
the complete closed record with its own `record_digest` omitted; floating
point and non-JSON values are forbidden. G0 requires an exact target-acceptance
grant for every cross-layer binding. A content-bearing target must therefore
exist as an immutable draft with a known ID and digest before binding;
nondeterministic unknown-target creation is outside G0. Anchor/grant
revocation requires current-root `revoke_*` authority; binding revocation
requires exact source `revoke_binding` authority plus target acceptance.
Approval requests require exact `request_approval` authority for the target
ID/digest. Reviewer and supersession selectors are closed to exact principal
IDs, principal types, or group-principal IDs; free-text/self-asserted roles
cannot confer approval authority.

A binding does not relax SQL row visibility. It authorizes a controlled service operation that creates a content-addressed projection or governed record in the receiving layer with a trace edge back to the source. Binding/grant validation, database-derived time evaluation, required row locks, the governed write, and an immutable operation-authorization record occur in one transaction. A concurrent expiry or revocation wins unless the authorization transaction has already serialized and committed; no check-then-write window is allowed.

### 6. Governed evidence is immutable and digest-bound

Artifact records require owning scope, immutable artifact ID, SHA-256 digest, byte size, media type, producer, deterministic `<installation_id>/<layer_id>/sha256/<digest>` storage key, and optional job/run correlation. Physical deduplication, if any, remains behind scoped indirection; unauthorized cross-layer requests are rejected before blob lookup with the same response shape/status and expose no semantic existence, lifecycle, deletion, or authorization oracle. The entire record is immutable; lifecycle changes are append-only events. A record is not created until content is finalized, so every authoritative artifact has a non-null digest and size. Available metadata cannot point to missing or digest-mismatched content, and body digest/size are reverified at approval and controlled execution time.

Approval requests are append-only and immutable and carry the exact target type/ID/digest/scope, requested action and authority scope, requester principal/grant, reviewer selector, and decision-policy reference/digest. Each append-only decision repeats the target/action/scope/policy and carries its actual reviewer principal/grant. Expiry, cancellation, and revocation are separate supersession events whose issuers also prove active authority. The governed decision-policy schema defines required reviewer selectors and aggregation; conflicting terminal decisions leave the request contested and non-authorizing unless that exact policy defines a deterministic resolution. Target digest drift, request expiry, grant revocation, or authority-scope mismatch invalidates approval.

Trace endpoints repeat type, ID, digest, and layer scope. Cross-layer edges cite one active exact binding; same-layer edges must not claim unrelated binding authority. Trace edges are evidence, not authority grants, and are append-only.

### 7. v2 coexists with v1 and migration requires explicit scope evidence

The existing v1 contract definitions and source-row bytes remain unchanged and accepted with deprecation guidance. New consumers opt into the parallel v2 family. A successful migrated installation preserves readable v1 history but adds the governed durable write-freeze described below; continuing writable v1 state would require a later governed dual-write contract. The v2 Postgres contract uses a dedicated authoritative namespace. Reapplication verifies canonical object definitions and checksums rather than trusting `IF NOT EXISTS`; same-named drifted tables, policies, functions, triggers, role attributes/memberships, ownership/ACLs, row-security flags, security-definer/search-path configuration, PUBLIC privileges, trusted-schema writability, or quarantine grants fail readiness.

The executable migration uses four distinct content identities so approval does not depend on a digest cycle and crash recovery does not pretend that a physical database snapshot can be recreated:

1. A detached mapping payload fixes migration ID, source database/schema identity, the exact twelve-table v1 catalog profile, expected per-table counts and dataset digest, legacy subject-to-layer mappings, explicit group/profile/worker installation/layer or installation-admin mappings, target topology, single-default proof where applicable, and migration policy. Its `mapping_payload_digest` covers only that closed payload.
2. A detached authority envelope repeats the payload digest and binds it to the exact approver principal, active `run_migration` grant, policy digest, governed installation scope, and trust-anchor chain. The grant constrains resource type `migration_mapping`, the exact migration ID, and `mapping_payload_digest`; `authority_envelope_digest` covers the payload plus detached authority references without changing the payload digest.
3. After the fixed source locks, PostgreSQL recomputes source identity, catalog digest, per-table counts, and dataset digest. Those content facts form the logical source-boundary ID and must match the approved payload.
4. PostgreSQL creates an immutable physical cutover observation for each accepted attempt. Its cutover envelope binds both earlier digests, the logical boundary, actual transaction snapshot and WAL position, active authority at database-derived time, target contract identity, and reconciliation digest.

Each legacy `project` value maps to one exact Customer `layer_id` and governed customer-subject tuple. Related jobs, runs, and events inherit scope only through verified ancestry. Groups, profiles, and workers have explicit layer or installation-administration mappings; memberships and GitHub-team mappings inherit only verified mapped endpoints and never confer v2 authority. A single default Customer mapping is legal only when every governed ancestry path proves one customer subject. The migration reconciles all twelve canonical v1 tables and classifies each row exactly once. The base v2 SQL defines immutable `legacy_jobs`, `legacy_job_runs`, `legacy_job_events`, `legacy_workers`, `legacy_groups`, `legacy_profiles`, `legacy_group_memberships`, and `legacy_github_team_mappings` compatibility-history targets plus migration staging/attempt/event/reconciliation and quarantine storage/security structures. The source-specific migration SQL only validates and transforms the v1 data, reconciles it, and attaches the durable successful-cutover freeze. V1 artifact rows lack complete finalized-body and producer-authority evidence, approval rows lack immutable target and reviewer-authority evidence, and trace rows lack digest-bound endpoints and binding evidence, so they enter only the separate non-authoritative quarantine. Migration never upgrades legacy history into an executable v2 job or an authorizing approval.

The dataset digest uses ratified profile `xfactory-v1-dataset-binary-v1` rather than implementation-defined string concatenation. It begins `XFV1DS || 00 01`; every frame is `tag:u8 || length:u64be || payload`; table/schema/name/column/count/row tags are respectively `10`, `11`, `12`, `14`, `17`, and `20`, with column-count `13`, column-name/type `15`/`16`, and row-column `21`. Value tags are null/text/integer/boolean/timestamp/binary/JSON `30` through `36` with the exact encodings in the governed-record requirement. Table and row ordering, canonical JSON, and SHA-256 coverage are likewise identical to that requirement. Golden vectors freeze every byte and must agree in Python and PostgreSQL 15/16.

One dedicated psql-based runner holds a session advisory lock derived from installation plus migration ID across multiple transactions. It validates canonical staging and active authority, commits `STARTED`, then begins the authoritative transaction at `SERIALIZABLE`, locks the fixed v1 tables in bytewise order before reading governed rows, recomputes the logical boundary, migrates, quarantines, reconciles, installs a durable v1 governed-write freeze, appends `SUCCEEDED`, and commits. Ordinary failure rolls back before `FAILED` is appended while the session lock is still held. Process death releases the lock; the next runner appends `ABANDONED` before an identical retry. A committed success is terminal and subsequent identical observers return its stored result.

Retry identity is installation plus migration ID, mapping-payload digest, and logical boundary. A post-rollback attempt may have a new transaction snapshot or WAL observation only when its content-derived logical boundary is identical. Changed payload, authority envelope, catalog, counts, dataset digest, scope mapping, or reconciliation fails closed. The successful transaction makes the v1 governed-write freeze durable before releasing the cutover locks; v1 contract files and readable history remain unchanged, but post-cutover v1 mutation is not supported without a later governed dual-write change.

Fresh initialization and reapplication use a governed preflight/apply boundary rather than running mutating `IF NOT EXISTS` or role repair before drift evaluation. One apply session acquires an application advisory lock, compares every existing object and security authority with the canonical fresh-v2 profile, applies the complete DDL transactionally only when the preflight accepts empty or exact state, and confirms the postflight profile before success. Migration readiness additionally compares the v1-cutover profile, including source-table definitions and successful freeze triggers. Missing, extra, or altered objects never become silently repaired state.

Quarantine has immutable closed records, no runtime/control/audit direct access, and no outward authoritative FK, view, materialized-view, function, or gate dependency. A database DDL guard rejects creation of such a dependency. Evidence can leave quarantine only by creating an independent new governed record under current authority; the quarantine row itself is never promoted or referenced as authority.

**Alternative considered:** add nullable scope columns to v1 and infer one default Project. Rejected because it silently invents authority and loses isolation in multi-subject data.

### 8. Semantic validation supplements structural schemas

`scripts/validate-hermes-runtime-contracts.py` will validate Draft 2020-12-compatible structure plus cross-document semantics that schemas alone cannot express: closed lifecycle transitions, durable identity tombstones, reference profiles, overlay inventories, pin resolution, authority grants, binding direction/source/target/expiry/revocation, artifact-body integrity, approval target and policy agreement, trace authorization proof, manifest coverage, and negative isolation cases.

Fixtures under `contracts/hermes-runtime/fixtures/` cover:

- two Customer instances in one operational installation;
- codexFactory project, MedxFactory patient, and LedgerxFactory client-company mappings against the same neutral schema;
- invalid lifecycle/cardinality, tombstone reuse, reference-profile/attestation failure, overlay/pin drift, wildcard/transitive/reversed/source-swapped/revoked bindings, artifact drift, approval/authority drift, trace mismatch, and cross-subject access;
- clean v2 apply, idempotent verified reapply, drifted pre-existing DDL, forged/missing/reused database scope, owner/admin bypass attempts, revocation races, artifact replacement after approval, and pooled-connection leakage;
- one-subject and two-subject v1 migration, frozen-source reconciliation, crash/retry, altered-map replay, concurrent v1 writes, quarantine boundary enforcement, and atomic failure for missing or ambiguous mappings.

Automated tests live under `tests/hermes_runtime_contracts/` and exercise both schema/semantic validation and real ephemeral Postgres behavior.

### 9. Publication and downstream pinning are content-addressed gates

At realization, the next available additive bundle version is allocated. `contracts/releases/<bundle-tag>.digests.yaml` inventories every required Hermes runtime schema, SQL file, migration, validator, fixture, fixture index, modified static schema/validator, manifest, changelog, and contract README. Each entry uses a repository-relative regular-file path and lowercase `sha256:<64hex>` of raw Git blob bytes sorted bytewise by path. The digest inventory excludes itself; the exact commit is anchored by the annotated tag and downstream compatibility manifest to avoid circular content. Contract files, manifest, changelog, README, and inventory are committed atomically. `scripts/validate-contract-release.py` validates candidate working-tree bytes before commit and exact Git blob bytes after commit/tag.

The release is not published until the tag, manifest version, changelog heading, repository commit, inventory membership, and per-file digests agree. Removal of `source_compatibility_ref.local_source_path` occurs only after a repository-wide consumer audit proves it is unsupported metadata; canonical repository and source-commit fields remain, and the compatibility evidence is recorded so the release remains additive.

The Gate G0 consumer is canonical repository `opensoft/xFactory-Hermes-Install`; the distinct `FarHeap/Hermes-Install` single-layer product MUST be rejected by the handoff receipt. The xFactory installer must record the canonical openxFactory repository, bundle tag, exact commit, canonical manifest path/digest, unique contract IDs/paths/schema versions/digests, and release-inventory path/digest. Its compatibility-manifest digest is stored in the runtime manifest and realization evidence, never inside the compatibility manifest itself. The checker has an online G0 mode that proves the annotated tag exists on the canonical remote and dereferences to the commit, and an offline runtime mode that validates exact commit/tree/blob objects already present locally. Both modes fail closed for branch refs, tag-only pins, duplicate paths, missing bundle members, path traversal, symlinks, wrong consumer repository, or digest drift. Gate evidence also records the exact landed xFactory Hermes Install commit plus repository-relative compatibility-manifest, checker, runtime-binding, and evidence paths/digests and the positive/negative command results.

The planned Hermes runtime currently exposes `project_ref`, `/projects`, and `provision-project`. Before it claims compatibility, the existing Hermes OpenSpec change and Speckit specification, plan, research, data model, contracts, quickstart, and tasks must consistently use customer-subject identity and lifecycle names; Project aliases remain in codexFactory specialization. Strict OpenSpec validation and Speckit analysis must pass after the Feature Integrator reconciles shared artifacts and task state.

## Risks / Trade-offs

- **Release metadata races with other active contract changes** → Rebase immediately before realization and allocate the next bundle version only after merge order is known.
- **RLS tests pass as a privileged owner but not for runtime identities** → Enforce the role/grant/scope-setter model and test non-owner, forged-scope, admin, pooled-connection, cross-stack, and cross-installation negatives.
- **Opaque subject references still contain sensitive data** → Require pseudonymous domain-issued references, scan fixtures/evidence, and keep resolution in the owning domain system.
- **Migration invents missing scope or authority** → Require an explicit typed mapping and abort atomically on every unmapped or ambiguous row; quarantine unverifiable evidence.
- **Parallel v1/v2 contracts increase temporary maintenance** → Keep the bridge explicit, add deprecation guidance, and make v2 the default only at the governed major release.
- **Bindings become an accidental access-control bypass** → Keep SQL visibility closed, authorize only exact service operations, and require immutable binding evidence on every cross-layer trace.
- **Neutral Hermes Install drifts back to Project vocabulary** → Validate its manifest and lifecycle interface against the neutral bundle; keep domain aliases outside the canonical core.

## Migration Plan

1. Land and validate the OpenSpec decision and hand it one-to-one to a Speckit feature.
2. Add v2 schemas, semantic validator, fixture matrix, canonical Postgres DDL, and migration tests without changing v1 acceptance.
3. Run preliminary strict OpenSpec, DomainxFactory, schema, semantic, and real-Postgres verification before release integration.
4. Rebase on the current canonical branch, resolve manifest/changelog conflicts, allocate the next available additive bundle version, build the digest inventory, and commit the exact release candidate.
5. Rerun the complete contract, migration, isolation, security, release, and existing-regression suites plus independent review against that exact candidate commit; make no semantic edit after it passes.
6. Promote the exact reviewed commit to published `origin/main`. If the merge strategy creates any different commit, rerun every gate and review on that exact main-line commit. Recheck bundle-version availability immediately before promotion.
7. Create and push the annotated tag only for the unchanged reviewed commit reachable from `origin/main`, then independently verify the remote commit, tag, manifest, inventory, and digests.
8. Hand the published evidence to the existing Hermes OpenSpec/Speckit feature, whose Feature Integrator owns neutralization, compatibility-manifest/checker implementation, exact pinning, and positive/negative checks.
9. Mark Gate G0/T009 complete only after the published remote bundle and exact landed Hermes revision independently reproduce every required digest and the downstream consistency analysis passes.

Rollback preserves v1 contracts and tables. A failed v2 migration rolls back atomically. A bad unpublished candidate is replaced before tagging; a published bad tag is never moved and must be superseded by a new additive release with an explicit changelog correction.

## Open Questions

No blocking product question remains. The release minor number is deliberately unresolved until realization, and live Hermes deployment bindings remain Gate G1 rather than part of this contract gate.
