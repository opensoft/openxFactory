# Phase 0 Research: Neutral Hermes Customer-Subject Runtime Contracts

Status: draft

**Date**: 2026-07-12

**Feature**: `005-customer-subject-runtime`

**Governed By**: `openspec/changes/add-hermes-customer-subject-runtime-contract/`

## Decision 1: Publish a composable contract family

**Decision**: Place the v2 family under `contracts/hermes-runtime/`. Give each independently consumed topology, installation/stack/layer lifecycle event, authority, binding, artifact, approval, trace, job, migration, and quarantine record its own closed Draft 2020-12 schema. Share only primitive definitions through `$defs`. Add `contract-index.yaml`, `acceptance-map.yaml`, and `evidence-register.yaml` to define required membership and requirement/scenario/evidence parity. Keep release inventory contracts under `contracts/releases/`.

**Rationale**: This follows the repository's avatar-client family pattern, permits consumers to pin only the records they use, improves error locality, and keeps the additive v2 family visibly separate from copied v1 schemas.

**Alternatives considered**:

- One monolithic `oneOf` schema: rejected because it weakens independent versioning and produces poor validation errors.
- Add every v2 file to `contracts/schemas/`: rejected because it obscures family identity and mixes parallel v1/v2 surfaces.
- Embed all fixtures in one YAML file: rejected because graph, SQL, race, and migration cases become unreviewable.

## Decision 2: Use strict Draft 2020-12 with offline-only references

**Decision**: Every `*.schema.yaml` carries YAML annotation keywords `schema_version` and `kind` plus `$schema`, `$id`, `contract_id`, and `contract_schema_version`. The canonical absolute ID base is `https://xforge.us/schemas/openxfactory/hermes-runtime/v2/`; each `$id` is that base plus its family-relative path and cross-file `$ref` values are relative within the base. Relative refs resolve only through an offline `referencing.Registry` built from the exact family catalog. The catalog rejects IDs outside the base, duplicate IDs, alternate URI aliases for one file, and any unregistered resolution. `Draft202012Validator.check_schema`, `Draft202012Validator`, and an explicit `FormatChecker` are mandatory. Governed records use `additionalProperties: false` or `unevaluatedProperties: false`; extension points are explicit and cannot carry authority.

The loader rejects duplicate keys, YAML merge keys and unknown tags, non-string mapping keys, anchors/aliases, timestamp coercion, NaN/Infinity, and every non-JSON value. No network or `file:` fallback is permitted for `$ref` resolution.

**Rationale**: Plain `yaml.safe_load` plus informal `schema_version/name/type` checks cannot prove reference closure or consistent JSON semantics. The chosen path extends the proven offline registry pattern in `scripts/validate-avatar-client.py`.

**Alternatives considered**:

- Deprecated `RefResolver`: rejected because current `jsonschema` uses `referencing`.
- Online schema retrieval: rejected as mutable and unsafe.
- Custom JSON Schema graph/time keywords: rejected because fixtures must remain portable to any conformant implementation.

## Decision 3: Separate the CLI from reusable semantic modules

**Decision**: Keep `scripts/validate-hermes-runtime-contracts.py` as a thin executable and place reusable private modules under `scripts/hermes_runtime_validation/`. Separate catalog/loading/schema/fixture/content/acceptance services from pure semantic modules for topology, references, overlays, authority, isolation, artifacts, approvals, traceability, jobs, and migration. `scripts/validate-contract-release.py` reuses catalog/content loading but remains a separate release gate.

Pipeline order:

1. Load the exact contract index and enforce unique required membership.
2. Enforce strict YAML-to-JSON compatibility.
3. Check every schema and close every offline `$ref`.
4. Execute structural fixtures.
5. Execute pure semantic rules with fixture-supplied evaluation time.
6. Prove acceptance-map/OpenSpec/evidence parity.
7. Verify overlay/Git-object/digest evidence through an injected content resolver.
8. In candidate mode, require complete release metadata and inventory without
   pretending that a remote main-line commit or tag already exists.
9. In realization mode, require the exact remote commit, annotated tag, and
   tag-object evidence in addition to the unchanged candidate surface.

Exit codes are `0` pass, `1` findings, and `2` dependency/harness error. Findings have stable codes, deterministic path/code ordering, and human plus JSON output. CLI modes include `--strict`, `--case`, `--phase`, `--json`, `--require-candidate`, and `--require-realization`.

**Rationale**: The family has graph, time, Git, and database semantics that exceed one maintainable validator file. Pure modules remain testable without turning reference tooling into a runtime service.

**Alternatives considered**:

- One large script: rejected for reviewability and test isolation.
- A runtime package under `src/`: rejected because the constitution permits reference validators, not a deployed service.

## Decision 4: Make fixtures self-describing and reason-specific

**Decision**: `contracts/hermes-runtime/fixtures/index.yaml` is the portable suite. Each case declares a stable case ID, phase, class, requirement/scenario IDs, ordered inputs, fixed evaluation time where relevant, expected outcome, required primary finding code, allowed secondary codes, and evidence ID. PostgreSQL cases additionally identify supported majors, seeds/scripts, row/digest expectations, and authoritative deltas.

Every fixture path is unique, repository-relative, regular, below the fixture root, non-symlinked, indexed, and included in the release inventory. An invalid case must fail for its declared stable finding code, not merely produce any error. Acceptance and evidence parity fail for missing, duplicate, dangling, or skipped required scenarios.

**Rationale**: A malformed negative fixture must not accidentally pass because it failed for an unrelated reason. The index also lets non-Python consumers execute the suite.

**Alternatives considered**:

- Tests with unindexed inline data: rejected because they cannot form portable release evidence.
- Outcome-only negative fixtures: rejected because wrong-reason failures conceal regressions.

## Decision 5: Keep v1 untouched and separate authoritative, API, and quarantine namespaces

**Decision**: Preserve `public.hermes_*` v1 tables. The v2 SQL defines:

- `xfactory_runtime_v2`: authoritative tables, types, security state, tombstones, grants, bindings, jobs, evidence, and migration ledger.
- `xfactory_runtime_api_v2`: governed `SECURITY DEFINER` entrypoints only.
- `xfactory_legacy_quarantine_v2`: unverifiable migration evidence, inaccessible to runtime/control and forbidden as an authoritative FK/view source.

Layer-owned identities and FKs use composite `(installation_id, stack_id, layer_id, id)` keys. Tenant rows do not receive globally unique `id` constraints that could become cross-layer existence oracles through referential checks.

Migration reconciles the exact twelve-table v1 surface: `hermes_jobs`, `hermes_job_runs`, `hermes_job_events`, `hermes_job_artifacts`, `hermes_approval_requests`, `hermes_approvals`, `hermes_traceability_edges`, `hermes_workers`, `hermes_groups`, `hermes_profiles`, `hermes_group_memberships`, and `hermes_github_team_mappings`. The base v2 SQL owns `legacy_jobs`, `legacy_job_runs`, `legacy_job_events`, `legacy_workers`, `legacy_groups`, `legacy_profiles`, `legacy_group_memberships`, and `legacy_github_team_mappings` as scoped, immutable, explicitly non-authorizing compatibility-history tables, plus migration staging/attempt/event/reconciliation tables and the closed quarantine-record table/security boundary. Job ancestry selects Customer scope; workers, groups, and profiles use explicit layer or installation-administration mappings; memberships and GitHub-team mappings inherit only verified mapped endpoints. Artifacts, approval requests, approvals, and trace edges enter only the separate quarantine because their v1 shapes cannot prove the finalized bytes, immutable target/reviewer authority, or digest-bound binding evidence required for governed v2 authority. Each source row appears in exactly one of those two classifications, and migration does not populate executable v2 jobs or authorizing v2 approval records from legacy history. The source-specific migration SQL owns only catalog assertions, transforms, reconciliation, and v1 freeze attachment over those base structures.

**Rationale**: Parallel namespaces make the additive bridge honest and rollback-safe. Structural quarantine ensures incomplete legacy evidence cannot accidentally satisfy v2 gates.

**Alternatives considered**:

- Nullable scope columns on v1: rejected because they encourage guessed authority and complex rollback.
- Global tenant-row IDs: rejected because uniqueness/FK errors can disclose cross-layer existence.

## Decision 6: Bind database scope to authenticated principals and active grants

**Decision**: Define NOLOGIN role classes for owner, migrator, runtime, control, and audit. Runtime/control/audit are NOSUPERUSER, NOCREATEDB, NOCREATEROLE, NOREPLICATION, and NOBYPASSRLS; they cannot assume owner/migrator, create schemas, truncate, reference quarantine, or access tables outside their class.

Installation, stack, and layer identities are immutable registrations with immutable initial states. Separate predecessor-linked lifecycle-event tables are authoritative. A governed transition locks the entity/latest event, validates one closed transition and active authority, appends the event, and updates a non-authoritative projection atomically. Direct registration/event/projection writes, event forks, projection drift, and every transition out of `retired` fail; readiness reconstructs projections from the chain.

Every governed layer table has `ENABLE ROW LEVEL SECURITY`, `FORCE ROW LEVEL SECURITY`, explicit `USING`, and explicit `WITH CHECK`. `xfactory_runtime_api_v2.assume_scope(...)` is owned by the NOLOGIN owner, fixes `search_path`, revokes PUBLIC execute, binds the invoker through `session_user`, checks an active `assume_scope` grant plus principal/layer lifecycle, and sets transaction-local scope/grant data. RLS calls a trusted helper that revalidates the tuple and grant; custom GUC bytes are never trusted alone. One non-escalatable login represents one governed principal. Tests cover direct forged settings, `SET ROLE`, missing/revoked scope, retired identities, cross-stack/install access, owner/admin attempts, and same-session pool reuse.

**Rationale**: `current_user` becomes the function owner inside `SECURITY DEFINER`; `session_user` preserves the authenticated login. Custom settings alone are caller-controlled and cannot be authority.

**References**:

- PostgreSQL row security: `https://www.postgresql.org/docs/15/ddl-rowsecurity.html`
- Safe security-definer functions: `https://www.postgresql.org/docs/16/sql-createfunction.html`
- Session/current user semantics: `https://www.postgresql.org/docs/16/functions-info.html`
- Transaction-local settings: `https://www.postgresql.org/docs/16/functions-admin.html`

**Alternatives considered**:

- Application-supplied scope or GUC-only RLS: rejected as forgeable.
- Database/schema per subject: rejected because it does not realize one shared neutral installation and makes lifecycle/migration unbounded.

## Decision 7: Serialize cross-layer authorization and revocation in one transaction

**Decision**: Grants, bindings, decisions, traces, and authorization evidence are insert-only with privilege denial plus defensive update/delete rejection triggers. Trust-anchor and grant validation is as-of-time, acyclic, and scope-narrowing.

The portable and SQL contracts share a closed G0 authority-action vocabulary
and the `xfactory-canonical-json-v1` record-digest profile. One immutable
genesis anchor begins the linear rotation history; rotation replaces the one
active root, while revocation may leave none. Root grants cite that active
anchor, delegated grants cite an `issue_grant` chain, and historical evidence
uses the root active at its recorded time. Every G0 cross-layer binding also
requires exact target acceptance and, for content-bearing targets, a
pre-existing immutable target draft with a known digest.
Approval admission similarly requires an exact `request_approval` grant, and
reviewer/supersession selection uses governed principal identity/type/group
rather than self-asserted role text.

One governed cross-layer API takes advisory transaction locks in canonical anchor/grant/binding/resource order, locks authority rows, evaluates grants/revocations/expiry with `transaction_timestamp()`, verifies exact source/target IDs and digests plus target acceptance, and inserts the projection/artifact, operation authorization, and trace edge together. Revocation uses the same lock keys/order. Either the operation commits first with immutable evidence or revocation wins.

**Rationale**: This removes the authorization check/write race while allowing unrelated Customer subjects to proceed concurrently.

**Alternatives considered**:

- `SERIALIZABLE` alone: rejected because it does not define the authority serialization point or retry order.
- Broad table locks: rejected because they destroy subject concurrency.

## Decision 8: Freeze migration input and make its digest independently reproducible

**Decision**: Validate the YAML mapping outside SQL, normalize it to canonical JSON, and split its content identities before staging. A detached mapping payload fixes migration ID, source database/schema identity, the exact twelve-table v1 catalog profile, expected per-table counts and dataset digest, subject/admin/principal mappings, target topology, single-default proof where applicable, and migration policy. `mapping_payload_digest` covers only that closed payload. A detached authority envelope binds the payload digest to the exact approver principal, active `run_migration` grant, policy digest, installation scope, and trust-anchor chain; the grant constrains resource type `migration_mapping`, migration ID, and payload digest. `authority_envelope_digest` covers the canonical staging envelope without participating in the payload digest, so approval is content-addressed without a digest cycle. SQL accepts only that validated canonical staging form and independently recomputes both digests and current authority.

One psql-based migration runner acquires a session advisory lock derived only from installation plus migration ID and retains it across the attempt and authoritative transactions. It records `STARTED` before the main transaction. Cutover then starts `SERIALIZABLE`, locks the fixed v1 table list in bytewise order before the first governed source read with `SHARE ROW EXCLUSIVE`, recomputes the catalog, counts, and dataset digest, and derives a logical source-boundary ID from those values plus source identity. Any difference from the approved payload aborts. PostgreSQL records the actual transaction snapshot and WAL position only in a physical cutover observation bound to both earlier digests, the logical boundary, active authority at database-derived time, target contract identity, and reconciliation digest.

Digest profile `xfactory-v1-dataset-binary-v1` is exact binary framing rather than delimited text. Bytes begin `XFV1DS || 00 01`; every frame is `tag:u8 || length:u64be || payload`. Table/schema/name/column-count/column/name/type/row-count/row/row-column tags are `10`/`11`/`12`/`13`/`14`/`15`/`16`/`17`/`20`/`21`; null/text/integer/boolean/timestamp/binary/JSON tags are `30` through `36`. The profile uses UTF-8 without Unicode normalization, raw UTF-8 schema/table ordering, framed-primary-key byte ordering independent of collation, schema-ordinal columns, exact typed encodings, UTC RFC 3339 timestamps with six fractional digits and `Z`, lowercase-hex binary, and arbitrary-precision canonical JSON with raw-UTF-8 key order, minimal control/string escapes, exponent-free insignificant-zero-free decimals, and negative zero normalized to `0`. Table frames contain schema, table, ordered column metadata, row count, and ordered row frames; SHA-256 covers the magic plus complete table stream. Golden vectors freeze every byte and must agree in Python and PostgreSQL 15/16.

The authoritative transaction migrates non-authorizing compatibility history, quarantines unverifiable evidence, reconciles every row/ID from all twelve v1 tables exactly once, installs a durable v1 governed-write freeze, appends `SUCCEEDED`, and commits. Contract files and readable v1 history remain supported; writes to a successfully cut-over v1 dataset stay frozen unless a later governed dual-write change replaces that boundary. Ordinary failure rolls back before the runner appends `FAILED` while retaining its session lock. Process death releases the lock; the next runner appends `ABANDONED` before retry. A committed success is terminal and an identical observer returns its recorded result without reapplying rows.

Retry identity is `(installation_id, migration_id, mapping_payload_digest, logical_boundary_id)`. After rollback, another physical snapshot or WAL observation may converge only when the approved payload, authority envelope, and logical content boundary are unchanged. Changed mapping, authority, source catalog, counts, dataset digest, scope classification, or reconciliation fails closed.

**Rationale**: A physical MVCC snapshot cannot be approved before the cutover transaction exists or recreated after a crash. The approved payload therefore binds expected source content, the database proves that content under lock, and each attempt records its physical observation. A failure record cannot survive inside the transaction it describes if that transaction rolls back, so the session-locked runner and separate attempt/event ledger preserve crash evidence without weakening atomic authoritative state.

**References**:

- PostgreSQL explicit locking: `https://www.postgresql.org/docs/16/sql-lock.html`
- Transaction snapshot rules: `https://www.postgresql.org/docs/16/sql-set-transaction.html`

**Alternatives considered**:

- Infer one default layer: rejected for multi-subject data and allowed only with proof of exactly one subject.
- Dual-write v1/v2 for this migration: rejected as unnecessary complexity for the first governed cutover; a frozen maintenance window is explicit.

## Decision 9: Prove PostgreSQL behavior through official 15/16 images and in-container psql

**Decision**: Pin Python test dependencies through `requirements/hermes-runtime-contracts.in` and a generated hash-locked file. Use stdlib subprocess plus the mounted Docker CLI; do not add psycopg, pgTAP, or Testcontainers. Parameterized Compose runs official PostgreSQL 15 and 16 images without host ports or persistent volumes and executes `psql -X -v ON_ERROR_STOP=1` in same-image client containers. A dedicated psql migration runner retains its session advisory lock across its separate attempt, authoritative, and failure/recovery transactions. The release evidence records resolved image digests.

SQL and pytest cases cover clean apply/reapply, full security-catalog drift, immutable topology lifecycle/event projection, actual non-owner logins, RLS/scope pooling, binding/revocation races, frozen migration/write races, crash/identical retry, quarantine, and digest parity. Security drift includes role attributes/memberships, ownership/ACLs, row-security enable/force flags, security-definer/search-path configuration, PUBLIC privileges, trusted-schema writability, and quarantine grants. Docker absence is a release failure, not a skip.

Canonical application is a separate preflight/apply/postflight boundary, not a raw invocation of mutating `IF NOT EXISTS` or role repair. One psql session takes an application advisory lock, compares existing objects and authorities with the fresh-v2 catalog profile, executes the DDL as one transaction only for empty or exact state, and proves the postflight profile before success. Migration readiness uses a second v1-cutover profile containing the exact legacy catalog and durable freeze surface. This prevents drift from being silently repaired before it is reported.

**Rationale**: The required PostgreSQL semantics cannot be proven in SQLite or mocks. In-container psql avoids another client/driver dependency and matches both official server majors.

**Alternatives considered**:

- psycopg/Testcontainers: rejected as redundant dependency surface for a contract suite.
- Nested Omnigent v1 smoke: rejected because it tests a copied adapter schema and only one major.

## Decision 10: Make release inventory closed, non-circular, and Git-object-derived

**Decision**: `contracts/releases/release-digest-inventory.schema.yaml` defines realized `contracts/releases/<bundle-tag>.digests.yaml`. Entries are unique and bytewise-path-sorted with artifact ID, normalized path, type, Git mode, optional schema ID/version, and lowercase `sha256:<64hex>` of raw Git blob bytes. Membership is derived from canonical registrations and includes the entire Hermes family, indexed fixtures, validators, hash-locked `requirements/hermes-runtime-contracts.in` and `.lock`, the PostgreSQL 15/16 image lock, modified static schema/validator, inventory schema, manifest, changelog, contract README, and every modified normative contract/versioning doc. The realized inventory excludes only itself.

`scripts/validate-contract-release.py` supports candidate build, exact-commit verification through `git ls-tree`/`git cat-file`, a pre-tag `verify-promotion` check, and remote annotated-tag verification. `verify-promotion` proves tag absence, next-version validity, candidate reachability from remote main, and unchanged release-surface blob IDs after the reviewed candidate. It rejects missing/extra/duplicate/out-of-order/symlink/submodule/traversing/host-path members. Commit and inventory digest remain outside the inventory to avoid circularity; the tag and downstream compatibility manifest anchor them.

**Rationale**: Per-file raw blobs make membership and exact bytes independently reproducible in a clean clone.

**Alternatives considered**:

- Directory/tree digest only: rejected because it hides semantic membership.
- Inventory containing its own digest or commit: rejected as circular.
- Working-tree-only verification: rejected as mutable.

## Decision 11: Promote only an exact reviewed main-line commit

**Decision**: Serialize release integration, fetch origin/tags, rebase, immediately recheck bundle/tag availability, allocate the version, update all release surfaces, build the inventory, and commit candidate C. Run every gate and independent review on C. Promote without squash/rebase rewriting when possible. Verify C is reachable from published `origin/main` and no release surface drifted, then tag C. If promotion creates commit M, M becomes the candidate and every gate/review reruns before tagging. Never move a published tag.

Current planning baseline is `contract-v1.6` with no aggregate `contract-v*` tag; no next minor is reserved. The local forbidden `local_source_path` is removed only after the supported-consumer audit.

**Rationale**: Tag-before-merge is unrealized, while tagging a merge-created SHA without rerunning would publish an unreviewed revision.

**Alternatives considered**:

- Tag feature commit before promotion: rejected by release-realization governance.
- Squash/rebase merge after exact-candidate review: rejected because it changes the reviewed identity.

## Decision 12: Version the regression denominator and downstream closure evidence

**Decision**: Add the schema-validated realized Domain regression inventory at `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`, indexed by `contracts/hermes-runtime/fixtures/index.yaml`, containing canonical repository, published commit, stack path/digest, domain ID, and expected contract pin/result. The initial denominator is:

| Repository | Published commit | `stack.yaml` raw-blob digest |
|---|---|---|
| `opensoft/AdxFactory` | `d0e42622d1da51a3aa6475e2df076df4e55e7918` | `sha256:b5ab723eac7395523a7988468076048e4d0426e03b556231dfb4c282bb8b3fc9` |
| `opensoft/LedgerxFactory` | `1b2ca4c1e66b5e90c9e983a7d0aad11c1ab5ae1c` | `sha256:85d67c54a07f3d4e31943257cf43cb19e0fc400f39a0c719591ed30eeb140ab9` |
| `opensoft/MedxFactory` | `280fdbb5aee8cd83f5c75defd652c1a60039cd0e` | `sha256:02e4b34528217870e982462dde4ff8624c29a7b9e61f3ab405f4710307ff6622` |
| `opensoft/OpsxFactory` | `beed3481fb7f500695bcc4394bb686fab125ad71` | `sha256:3de89a6c7e8b9f112deb7074b8798dc17311425f819968f2f7e1c7e86c7e8fa0` |
| `opensoft/codexFactory` | `7bfa492f700de29cdeab31dc899420745546d982` | `sha256:06f88e192bfd17d42ea6519072e472b9f6d028d88ab0985065640e37c9719722` |

Every entry pins openxFactory commit `3d51c3ed5854d112bcc049e1ef7f70863b993fa3`, schema version 1, and `stack.yaml`. LegalxFactory is explicitly excluded because it has no canonical `stack.yaml`. Tests obtain exact Git blobs, never dirty local directories, and generate a duplicate-Customer negative for each positive.

The validator accepts repeatable `--domain-repo <canonical-repo>=<checkout>` mappings or `--domain-repo-root <mirror-cache>`. Root resolution uses only `<root>/<owner>/<repo>` or `<root>/<owner>/<repo>.git` and rejects ambiguity. It verifies only `commit:path` Git objects. CI prepares temporary filtered/bare mirrors and fetches the exact commits through the existing Git transport; missing objects or unavailable authenticated access exit 2 and fail release.

Hermes Install remains owned by `001-three-layer-hermes-runtime` in canonical repository `opensoft/xFactory-Hermes-Install`. Its packet lives at `evidence/gates/g0/<bundle-tag>.yaml` and validates against `config/schemas/g0-closure-evidence.schema.yaml`. It records the exact openxFactory tag/commit/tag object/manifest/inventory/contracts and the exact landed Hermes commit plus compatibility-manifest/checker/runtime-binding/evidence paths/digests and positive/negative results. The receipt schema fixes `consumer_repository` to `opensoft/xFactory-Hermes-Install`; the indexed negative fixture `fixtures/pins/consumer-receipt-wrong-repository.yaml` supplies `FarHeap/Hermes-Install` and MUST fail with stable code `HGR-HANDOFF-CONSUMER-REPOSITORY`. openxFactory validates and records `openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/hermes-install-g0-handoff.yaml` against the canonical `contracts/hermes-runtime/consumer-handoff-receipt.schema.yaml` only after Hermes lands. Validation requires `--consumer-repo opensoft/xFactory-Hermes-Install=<checkout-or-mirror>` (or the deterministic consumer-root equivalent), reads the packet and every recorded downstream artifact as exact `commit:path` objects, and exits 2 if the landed commit/object or authenticated fetch is unavailable. Receipt validation is required before OpenSpec task 5 closure.

**Rationale**: “All current domains” and transient checker output are not reproducible evidence. Exact repo revisions make the regression denominator and Gate closure auditable.

**Alternatives considered**:

- Scan whatever local DomainxFactory directories exist: rejected as dirty-state dependent.
- Let this feature edit Hermes Install: rejected by one-OpenSpec/one-Speckit ownership.

## Resolved Unknowns

All material specification unknowns are resolved. Bundle minor version, final PostgreSQL image digests, exact release commit, and exact downstream Hermes commit are intentionally realization-time values governed by the contracts above rather than planning ambiguities.
