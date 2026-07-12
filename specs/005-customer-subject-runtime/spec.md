# Feature Specification: Neutral Hermes Customer-Subject Runtime Contracts

**Feature Branch**: `005-customer-subject-runtime`

**Created**: 2026-07-12

Status: draft

**Input**: User description: "Resolve Gate G0 by encoding and realizing the universal Customer Hermes instance pattern at the openxFactory neutral level, validating multiple Customer instances in one installation, publishing a content-addressed bundle, and enabling Hermes Install to pin it before multi-subject work continues."

**Governed By**: `openspec/changes/add-hermes-customer-subject-runtime-contract/`

## User Scenarios & Testing

### User Story 1 - Instantiate Customer Hermes Per Subject (Priority: P1)

As a DomainxFactory author, I can declare one neutral Customer Hermes role template and instantiate it repeatedly for the domain's customer subjects without duplicating the static role declaration or introducing domain vocabulary into the neutral contract. codexFactory can call those instances Project Hermes, MedxFactory can call them Patient Hermes, and LedgerxFactory can call them Client Company Hermes while all three conform to one shared topology.

**Why this priority**: This is the missing G0 contract. Without a repeatable neutral Customer instance, one installation cannot represent multiple projects, patients, companies, campaigns, ledgers, or managed systems honestly.

**Independent Test**: Validate an operational installation with one Client layer, one Domain layer, and two Customer layers created from one Customer template; then validate project, patient, and client-company mappings against the same neutral contract.

**Acceptance Scenarios**:

1. **Given** a valid DomainxFactory with one Customer, one Client, and one Domain template, **When** an operational topology instantiates two distinct Customer subjects, **Then** both instances validate with unique durable identities and policy namespaces.
2. **Given** an existing static stack, **When** a second `role: customer` declaration is added instead of a runtime instance, **Then** static conformance fails as before.
3. **Given** codexFactory, MedxFactory, and LedgerxFactory subject mappings, **When** their examples are validated, **Then** each uses the same neutral customer-subject shape and keeps its domain alias outside required neutral vocabulary.
4. **Given** a Customer layer that is retired, **When** another subject attempts to reuse its layer identity, subject tuple, or policy namespace, **Then** lifecycle validation rejects the reuse and preserves the tombstone.
5. **Given** an idempotent Customer-subject provisioning request, **When** the same key and subject are retried, **Then** exactly one layer and lifecycle record result; reuse with a different subject fails.
6. **Given** an installing, suspended, failed, or retired topology, **When** its lifecycle is validated, **Then** singleton cardinality, no-new-job, governed recovery, and terminal-retirement rules are enforced for that state.
7. **Given** a static `extension` layer, **When** it is used to represent another Customer subject, **Then** conformance rejects the evasion.
8. **Given** immutable topology registrations and their lifecycle histories, **When** an actor directly mutates current state, changes/deletes an event, forks a predecessor, or attempts a transition out of retired, **Then** the operation fails and the derived projection remains reconciled to the append-only event chain.

---

### User Story 2 - Isolate Subjects and Govern Cross-Layer Work (Priority: P1)

As a customer-subject owner, I can trust that my jobs, artifacts, approvals, memory-adjacent evidence, and traces are isolated from every other Customer layer. A cross-layer operation occurs only under an exact, time-bounded, revocable authority chain that identifies the source and target resources and leaves immutable authorization evidence.

**Why this priority**: Repeatability without isolation would turn the neutral pattern into a data and authority leak, especially for patient and accounting-company instances.

**Independent Test**: Exercise two Customer identities against the same installation and prove that neither can enumerate, read, write, approve, trace, probe storage existence, or assume scope in the other layer; then prove one exact bound projection succeeds and every altered, reversed, expired, revoked, or transitive variant fails.

**Acceptance Scenarios**:

1. **Given** Customer A and Customer B in one stack, **When** A attempts any direct governed-record operation against B, **Then** the operation exposes no B row, body, digest-existence signal, or lifecycle effect.
2. **Given** a principal without an active scope grant, **When** it supplies a forged layer, stack, or installation context, **Then** trusted scope establishment fails closed.
3. **Given** an exact active source grant, target acceptance where required, and source-to-target binding, **When** the governed operation commits, **Then** the write and immutable operation-authorization evidence commit atomically using database-derived time.
4. **Given** binding revocation racing an operation, **When** both transactions execute, **Then** serialization produces either a committed pre-revocation operation with evidence or a rejected post-revocation operation, never an unaudited write.
5. **Given** a target approved at one digest, **When** the target or artifact body changes, **Then** the approval cannot authorize the changed bytes.
6. **Given** self-issued, cyclic, wrong-scope, expired, or revoked authority, **When** a governed action is attempted, **Then** the authority chain fails before work begins.
7. **Given** an approval cancellation, expiry, or revocation event, **When** its issuer lacks the exact active grant and scope at database-derived effective time, **Then** the supersession is rejected.
8. **Given** a trust-anchor rotation authorized by the current anchor policy, **When** new and historical authority are evaluated, **Then** new grants use the active root set while historical evidence retains the root chain valid at its original authorization time.

---

### User Story 3 - Upgrade Legacy Operational Evidence Safely (Priority: P2)

As an installation operator, I can initialize the new operational contract or migrate existing v1 state without inventing subject scope, losing rows, granting authority to unverifiable history, or accepting a partially drifted database.

**Why this priority**: The new contract must be deployable against both clean and existing installations. A convenient migration that guesses scope or authority would invalidate the isolation guarantees from User Story 2.

**Independent Test**: Apply the new operational contract twice to supported PostgreSQL 15 and 16 databases, migrate one-subject and two-subject seeded v1 datasets under approved mapping manifests, and exercise ambiguous/default mapping, concurrent writes, changed-map replay, crash/identical retry, drifted database objects, and quarantined legacy evidence.

**Acceptance Scenarios**:

1. **Given** an empty supported database, **When** the v2 operational contract is applied twice, **Then** both applications yield the same verified canonical state.
2. **Given** a v1 database with two legacy subject values and a complete detached mapping payload plus authority envelope, **When** migration locks the source and reproduces the approved logical boundary, **Then** every row ID from all twelve canonical v1 tables is preserved exactly once as correctly scoped non-authorizing compatibility history or permitted quarantine and is reconciled by reproducible counts and dataset digest.
3. **Given** missing, conflicting, or ambiguous scope evidence, **When** migration runs, **Then** the transaction aborts without partial authoritative state.
4. **Given** an artifact, approval, or trace record whose integrity or authority cannot be reconstructed, **When** migration runs, **Then** the record is preserved only in an inaccessible non-authoritative quarantine and cannot satisfy a gate or authoritative reference.
5. **Given** the same installation and migration ID with a changed mapping-payload digest, authority-envelope digest, or logical source boundary, **When** it is retried, **Then** replay fails closed; a new physical snapshot/WAL observation is acceptable only after rollback and only when the approved payload and logical boundary remain identical.
6. **Given** a same-named but incompatible pre-existing table, policy, function, trigger, role attribute/membership, owner, ACL, RLS enable/force flag, security-definer/search-path configuration, PUBLIC privilege, or quarantine grant, **When** readiness is evaluated, **Then** security/catalog drift is reported instead of being silently accepted.
7. **Given** a crash before migration commit, **When** the identical installation, migration ID, mapping payload, authority envelope, and logical boundary are retried under the session lock, **Then** zero partial authoritative state remains, the prior attempt becomes abandoned, and the retry converges exactly once even though its physical snapshot/WAL observation is new.
8. **Given** a proposed single default Customer mapping, **When** the frozen legacy dataset does not prove exactly one subject across all governed rows, **Then** migration rejects the default.

---

### User Story 4 - Publish and Consume an Exact Contract Bundle (Priority: P1)

As a Hermes Install maintainer, I can consume one published openxFactory bundle identified by an annotated release tag, exact commit, canonical inventory, and raw-file digests. I can verify publication online and verify already-present Git objects offline before declaring Gate G0 complete.

**Why this priority**: An implemented contract that is not reproducibly published and pinned does not unblock Hermes. Gate G0 closes only when the provider and consumer agree on the exact bytes.

**Independent Test**: Realize the next available additive bundle, independently reproduce every inventoried digest from the release commit, verify the published annotated tag, and run the Hermes checker against the exact pin plus deliberately altered tags, commits, paths, versions, and digests.

**Acceptance Scenarios**:

1. **Given** the final rebased release candidate, **When** all verification and independent review pass against that exact commit, **Then** that exact commit must land on published `origin/main` before the matching annotated tag may be published; any merge-created replacement commit reruns all gates.
2. **Given** the published tag and commit, **When** an independent verifier reads raw Git blobs, **Then** every required contract, validator, migration, fixture, manifest, changelog, and documentation digest matches the canonical release inventory.
3. **Given** a branch ref, tag-only pin, missing member, duplicate ID/path, path traversal, symlink escape, wrong schema version, or changed digest, **When** compatibility is checked, **Then** the check fails closed.
4. **Given** the exact commit objects are available but the network is unavailable, **When** offline verification runs, **Then** it reproduces every required digest without trusting mutable working-tree files.
5. **Given** the published neutral bundle, **When** Hermes Install completes its existing governed feature, **Then** its neutral core uses customer-subject identity/lifecycle vocabulary, its runtime evidence binds the compatibility-manifest digest, its exact landed source revision and artifact digests are recorded, and Gate G0/T009 remains closed until positive and negative pin checks pass.

### Edge Cases

- An installation is `installing` before singleton layers are ready, `configured` before any Customer is onboarded, suspended during an incident, or fully retired.
- A layer fails during provisioning or while active, recovers through a governed retry, or retires without losing its tombstone.
- A pseudonymous subject reference is syntactically valid but its issuer policy uses reversible or unkeyed deterministic derivation.
- An overlay manifest omits a file, includes a file outside its root, contains a symlink, or changes byte ordering or digest encoding.
- A scope grant is revoked while an already-pooled database connection still exists.
- An installation administrator or control-plane identity attempts direct Customer-table access.
- A binding's target is unchanged but its source artifact ID or digest changes.
- Multiple approval decisions conflict and the pinned decision policy has no deterministic resolution.
- Artifact content disappears or changes after admission or approval but before controlled execution.
- Migration loses its connection after writing some statements, commits before the runner receives acknowledgement, observes another physical snapshot after rollback, or competes with a v1 write before the durable successful-cutover freeze is installed.
- A release metadata change lands concurrently and consumes the next bundle version before this feature realizes or between review and promotion.
- A published release is found defective after tagging; the tag must remain immutable and a new release must supersede it.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST preserve exactly one static Customer, Client, and Domain role template per DomainxFactory, MUST continue rejecting duplicate canonical role declarations, and MUST reject using `role: extension` to represent another Customer instance.
- **FR-002**: The system MUST represent concrete runtime layers separately from static role templates.
- **FR-003**: Every Customer instance MUST carry a domain-owned subject kind, issuer, namespace, pseudonymous surrogate reference in `urn:xfactory:subject:<uuid>` form, and pinned issuer-policy attestation.
- **FR-004**: The subject-reference policy MUST permit only independently generated cryptographically random UUIDv4/UUIDv7 surrogates or approved keyed tokenization and MUST prohibit UUIDv1/v3/v5, direct identifiers, reversible encoding, raw or unkeyed hashes, and other deterministic unkeyed derivation from source identities.
- **FR-005**: Installation, stack, and layer identity registrations MUST be immutable; lifecycle state MUST derive from an immutable initial state plus one append-only predecessor-linked event chain. Any current-state projection MUST be non-authoritative, governed-operation-only, and reconciled to that chain. Direct registration/state mutation, event update/delete, predecessor forks, and every transition out of `retired` MUST fail. The runtime topology MUST enforce the closed topology transitions `installing -> configured`, `configured -> operational|retired`, `operational -> suspended|retired`, `suspended -> operational|retired`, with `retired` terminal; and the closed layer transitions `provisioning -> active|failed|retired`, `active -> suspended|failed|retired`, `suspended -> active|failed|retired`, `failed -> provisioning|retired`, with `retired` terminal. State behavior MUST include installing cardinality, configured/operational readiness, suspended no-new-job behavior, governed recovery from failure, and all-layer retirement.
- **FR-006**: An installing topology MUST allow at most one non-retired Client and Domain and no Customer; a configured topology MUST contain exactly one active Client and one active Domain; an operational topology MUST additionally contain at least one active Customer.
- **FR-007**: Layer IDs, Customer subject tuples, and policy namespaces MUST remain globally unique within a stack through append-only registration and durable retirement tombstones.
- **FR-008**: All single-file contracts/templates and directory overlays MUST be content-addressed at exact commits; overlay manifests MUST completely inventory their declared roots under closed exclusion rules.
- **FR-009**: Every governed record MUST identify its installation, stack, and owning layer, while installation administration MUST use an explicit non-Customer administrative scope.
- **FR-010**: Runtime persistence MUST enforce default-deny scope for all governed records through non-owner identities and MUST prevent direct cross-subject and cross-installation access.
- **FR-011**: Trusted scope establishment MUST map the authenticated database principal through an active `assume_scope` grant on every transaction and MUST reject forged, stale, revoked, retired, or leaked pooled scope.
- **FR-012**: Each installation MUST have an out-of-band-approved trust anchor, and every non-genesis authority grant MUST form an acyclic, scope-narrowing chain to an active trusted anchor.
- **FR-013**: Authority grants, revocations, trust-anchor events, bindings, and operation-authorization records MUST be immutable and append-only.
- **FR-014**: Cross-layer bindings MUST identify exact source and target layers, exact source and target resource coordinates, action, purpose, time bounds, and required source/target authority.
- **FR-015**: Content-bearing binding resources MUST include immutable digests; omission MAY occur only for a closed set of identity-level resources.
- **FR-016**: Binding/grant validation, database-derived time evaluation, serialization, governed write, trace edge, and operation-authorization evidence MUST share one atomic transaction.
- **FR-017**: Wildcard, self-bound, inherited, transitive, reversed, expired, revoked, source-swapped, cyclic, or wrong-scope authority MUST fail closed.
- **FR-018**: Artifact records MUST be wholly immutable, content-addressed, installation/layer namespaced, and reverified at admission, approval, and controlled execution.
- **FR-019**: Unauthorized artifact requests MUST be rejected before blob lookup with an identical response shape/status, and physical deduplication MUST expose no cross-layer semantic existence, deletion, lifecycle, or authorization oracle.
- **FR-020**: Approval requests MUST bind requester authority, exact target/action/scope, reviewer selector, and immutable decision-policy digest.
- **FR-021**: Each approval decision MUST bind its actual reviewer authority and repeat the exact request target/action/scope/policy; each append-only expiry, cancellation, or revocation event MUST bind its issuer principal, exact active grant/digest, scope, and database-derived effective time.
- **FR-022**: Conflicting decisions MUST remain non-authorizing unless the pinned decision policy defines a deterministic resolution.
- **FR-023**: Trace edges MUST bind digest-addressed source/target endpoints to the exact operation authorization, binding, and grants; trace evidence MUST NOT grant authority.
- **FR-024**: V2 job, run, and event records MUST share the same neutral installation/stack/layer scope and MUST NOT require domain-specific nouns.
- **FR-025**: Existing v1 contract paths, unchanged v1 envelope/run/event fixtures, and valid pinned consumers MUST remain supported through the additive compatibility bridge.
- **FR-026**: The v2 operational contract MUST detect drifted pre-existing objects and MUST verify idempotent reapplication through a preflight/apply/postflight boundary rather than relying on object names alone or repairing state before comparison. Its canonical introspection MUST cover tables, policies, functions, triggers, role attributes/memberships, schema/table/function ownership and ACLs, `relrowsecurity`/`relforcerowsecurity`, security-definer/search-path configuration, PUBLIC execute/create privileges, quarantine grants, and the successful-cutover v1 freeze surface.
- **FR-027**: Migration MUST require a typed detached mapping payload that fixes source database/schema identity, exact v1 catalog profile, expected per-table counts/dataset digest, subject mappings, administrative/principal mappings, target topology, policy, and exact profile `xfactory-v1-dataset-binary-v1` whose magic, `u8` tags, `u64be` lengths, typed encodings, ordering, canonical JSON, and SHA-256 coverage match the ratified governed-record requirement. A separate content-addressed authority envelope MUST bind that payload digest to an exact active `run_migration` principal/grant/policy/scope/anchor chain without creating a digest cycle. A single default Customer mapping is permitted only when the observed logical boundary proves exactly one subject across every governed row.
- **FR-028**: Migration MUST hold one session advisory lock on installation plus migration ID across crash-surviving attempt and authoritative transactions; MUST lock the fixed v1 tables before source reads; MUST derive a logical source boundary plus database-observed physical cutover envelope; MUST install a durable successful-cutover v1 governed-write freeze; MUST preserve every row and ID from all twelve canonical v1 tables in exactly one correctly scoped non-authorizing compatibility-history or permitted quarantine classification; and MUST reconcile immutable input/output evidence.
- **FR-029**: Missing, ambiguous, conflicting, concurrently changed, non-canonical, or replay-drifted migration input MUST abort atomically. Retry identity MUST bind installation, migration ID, mapping-payload digest, and logical boundary; after rollback, a new physical snapshot/WAL observation MUST NOT be treated as drift when the logical boundary is unchanged, while a changed payload, authority envelope, logical boundary, or reconciliation MUST fail closed.
- **FR-030**: Unverifiable legacy artifacts, approvals, and trace edges MUST be stored only in a separate non-authoritative quarantine unavailable to runtime roles or authoritative references.
- **FR-031**: Canonical validation MUST include an indexed positive/negative fixture matrix, including two Customer instances in one installation and project/patient/client-company examples using the same neutral contract.
- **FR-032**: The additive bundle MUST include a canonical release digest inventory covering every required semantic file and hashing raw Git blob bytes with an unambiguous format while excluding the inventory itself.
- **FR-033**: Release realization MUST recheck and allocate the next available version after final rebase and immediately before promotion, MUST review/test the exact unchanged candidate, MUST land that exact commit on published `origin/main`, and MUST rerun all gates if merge creates a different commit before publishing an annotated tag.
- **FR-034**: A consuming install MUST pin and verify the canonical repository, bundle tag, exact commit, manifest and inventory digests, and unique per-contract ID/path/version/digest entries.
- **FR-035**: Compatibility verification MUST support online remote-tag proof and offline exact-Git-object verification and MUST fail every movable, incomplete, duplicated, escaping, mismatched, or drifted pin.
- **FR-036**: The compatibility manifest's digest MUST be bound from runtime or realization evidence and MUST NOT be self-recorded.
- **FR-037**: A versioned regression inventory MUST name every supported DomainxFactory repository and exact pin in the compatibility denominator; all inventoried DomainxFactory validation, strict OpenSpec validation, Speckit consistency analysis, and independent architecture/contract/security/privacy/operations/release review MUST pass before publication.
- **FR-038**: openxFactory implementation and publication MUST remain owned by this feature; downstream Hermes neutralization/checker/pinning MUST remain owned by its existing OpenSpec/Speckit feature and accepted here only as external Gate evidence.
- **FR-039**: Customer-subject provisioning MUST be idempotent: identical key/subject retries return one layer and lifecycle record, conflicting key reuse fails, retirement rejects new jobs, and artifacts/approvals/traces/audit plus the identity tombstone remain preserved.
- **FR-040**: Approval supersession by an unauthorized, expired, revoked, or wrong-scope issuer MUST fail closed.
- **FR-041**: The operational contract and migration acceptance matrix MUST cover PostgreSQL major versions 15 and 16; expanding or removing a supported major requires governed compatibility evidence.
- **FR-042**: Manifest bundle version, changelog heading, annotated tag, exact main-line commit, and release inventory MUST agree; release metadata MUST reject host-absolute paths, and removal of legacy `local_source_path` MUST be preceded by a recorded supported-consumer audit.
- **FR-043**: Gate G0 closure evidence MUST require canonical consumer repository `opensoft/xFactory-Hermes-Install`, reject the distinct `FarHeap/Hermes-Install` product, and record the exact landed consumer commit, repository-relative compatibility-manifest/checker/runtime-binding/evidence paths and digests, and positive/negative command results.
- **FR-044**: Trust-anchor rotation or revocation MUST be authorized by the current anchor policy, new grants MUST validate through the active root set, and historical evidence MUST preserve and validate against the root chain active at its authorization time.
- **FR-045**: Static DomainxFactory isolation vocabulary MUST add the neutral `per_customer_subject` value while retaining validation support for existing domain aliases such as `per_project`, `per_patient`, `per_ledger`, and `per_campaign` during the compatibility bridge.

### Key Entities

- **Installation**: One deployed Hermes boundary with a durable immutable identity, event-derived lifecycle, trust anchor, and exactly one stack for this G0 profile.
- **Stack**: The single DomainxFactory assembly within a G0 installation, bound to exact template and contract pins; general multi-stack installations remain out of scope.
- **Role Template**: The single static Customer, Client, or Domain declaration a DomainxFactory supplies for reuse.
- **Layer Instance**: A concrete runtime realization of a role template with durable immutable identity, event-derived lifecycle, overlay pin, and policy namespace.
- **Topology Lifecycle Event**: An immutable predecessor-linked installation, stack, or layer transition whose chain is the authoritative source for current lifecycle state.
- **Customer Subject**: The domain-owned kind plus governed pseudonymous surrogate that selects one repeatable Customer layer.
- **Subject Reference Policy**: The issuer's pinned rules and attestation for non-linkable pseudonymous subject references.
- **Overlay Manifest**: A complete content-addressed inventory for one declared overlay root.
- **Trust Anchor**: The installation's out-of-band-approved genesis authority and policy digest.
- **Authority Grant**: An immutable, scoped, time-bounded link in an acyclic chain to the installation trust anchor.
- **Cross-Layer Binding**: An immutable authorization envelope for one exact source-to-target resource action.
- **Operation Authorization**: The immutable result of atomic grant/binding/time evaluation for one governed operation.
- **Artifact Record**: Immutable scoped metadata for finalized, content-addressed bytes.
- **Approval Request / Decision / Supersession**: Immutable records binding an exact target/action/policy to requester and reviewer authority.
- **Trace Edge**: Immutable digest-addressed evidence linking resources and the authority used for a governed operation.
- **Migration Payload / Authority Envelope / Logical Boundary / Cutover Ledger**: The detached approved expected-content mapping; its independently digest-bound active `run_migration` authority; the content-derived source boundary reproduced under lock; and immutable physical attempt, classification, reconciliation, and outcome evidence for a v1-to-v2 cutover.
- **Legacy Quarantine Record**: Preserved but structurally non-authoritative evidence that cannot enter runtime gates.
- **Release Digest Inventory**: The canonical raw-Git-blob digest set for one contract bundle.
- **Compatibility Manifest**: The install consumer's externally digest-bound declaration of the exact published bundle and files it accepts.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Installing, configured, operational-with-two-Customers, suspended, failed/recovered, and retired fixtures validate only in their allowed states; UUIDv4, UUIDv7, and approved keyed-token subject references pass; and 100% of indexed invalid cardinality, extension-role evasion, lifecycle, identity-reuse, UUIDv1/v3/v5/unsafe-reference-policy, and overlay-pin fixtures fail.
- **SC-002**: Project, patient, and client-company examples validate against one neutral contract with zero required domain-specific nouns.
- **SC-003**: 100% of DomainxFactory stacks named with exact pins in the versioned regression inventory continue to validate unchanged, duplicate static Customer roles continue to fail, and unchanged v1 envelope/run/event fixtures remain valid at their pinned paths.
- **SC-004**: Across the complete isolation matrix, Customer A obtains zero rows, bodies, metadata, existence signals, or write effects owned by Customer B without an exact governed projection.
- **SC-005**: 100% of invalid authority-chain, scope-forgery, binding, revocation-race, artifact-drift, approval, and trace cases fail closed; every successful cross-layer case has one atomic operation-authorization record.
- **SC-006**: Clean initialization and repeated initialization through the preflight/apply/postflight boundary produce an identical verified operational contract without repairing drift first, and 100% of drifted-object fixtures block readiness.
- **SC-007**: One-subject and two-subject migrations preserve 100% of source row IDs and counts across all twelve canonical v1 tables, classify every row exactly once as correctly scoped non-authorizing compatibility history or permitted quarantine, reproduce the source digest, and leave zero authorizing row for unmapped or unverifiable evidence.
- **SC-008**: 100% of ambiguous/default-map, concurrent-write, altered-payload/authority/logical-boundary, reconciliation, drifted-DDL, and quarantine-boundary negatives fail without partial authoritative state; a changed physical observation after rollback succeeds only when the logical boundary is identical.
- **SC-009**: An independent verifier confirms manifest/changelog/tag/version/inventory agreement and reproduces 100% of raw-blob digests from the exact reviewed commit reachable from published `origin/main`; host-absolute release paths and an unaudited legacy-path removal fail.
- **SC-010**: Online and offline compatibility checks pass for one exact landed Hermes Install commit whose manifest/checker/runtime-binding/evidence paths and digests are recorded, and reject 100% of deliberately altered tag, commit, manifest, path, version, and digest cases.
- **SC-011**: Strict OpenSpec validation reports zero failures, Speckit analysis reports zero critical/high findings, and the final independent expert panel reports zero unresolved P1/P2 findings on the exact release candidate.
- **SC-012**: Gate G0/T009 remains closed until remote release evidence and Hermes Install evidence independently reproduce every required digest; no dependent multi-subject implementation begins early.
- **SC-013**: 100% of identical provisioning retries converge to one layer/lifecycle record, conflicting idempotency-key reuse fails, and retirement rejects all new jobs while preserving every evidence class and tombstone.
- **SC-014**: A pre-commit migration crash leaves zero partial authoritative rows; an identical installation/migration/payload/authority/logical-boundary retry records abandonment and converges exactly once under the session lock; committed success is terminal; and changed payload, authority envelope, or logical boundary replay fails even though an identical post-rollback retry may record another physical snapshot/WAL observation.
- **SC-015**: 100% of trust-anchor rotations/revocations require current-policy authority; new grants validate only through the active root set while historical operation evidence validates against its original as-of anchor chain.
- **SC-016**: The complete clean-apply, RLS, locking, concurrency, drift, migration, and retry suite passes independently on PostgreSQL 15 and PostgreSQL 16.
- **SC-017**: The neutral `per_customer_subject` isolation value validates, and 100% of inventoried existing stacks using supported `per_project`, `per_patient`, `per_ledger`, `per_campaign`, or other retained aliases continue to validate unchanged.

## Assumptions

- The approved OpenSpec change is the authoritative governance handoff for this feature.
- openxFactory remains the canonical owner of shared neutral contract meaning; DomainxFactories own aliases and stricter overlays.
- One installation may be configured before any Customer subject exists, but operational readiness requires at least one active Customer.
- The G0 topology intentionally contains exactly one stack per installation; general multi-stack installations require a later governed change.
- Subject references are pseudonymous surrogates whose real-world resolution remains in an approved domain system outside the neutral topology.
- Existing v1 contract consumers and readable history remain supported during the additive bridge; a successfully cut-over installation freezes further v1 governed writes, and any dual-write continuation requires a later governed change. Making v2 the default belongs to a later governed major release.
- The next bundle version is selected only at realization because other active contract changes may publish first.
- Real PostgreSQL 15 and 16 databases and every DomainxFactory checkout named in the versioned regression inventory are available for verification.
- This feature publishes contracts, validators, fixtures, migrations, and evidence; it does not deploy a live Hermes service or worker.
- The existing Hermes Install OpenSpec/Speckit feature owns downstream interface neutralization, the compatibility checker, and the final pin.
