# US3 Shared Interface Contract (SIC)

Coordinator-pinned interfaces for the Gate G0 US3 swarm (T052–T065).
Worktree: `/workspace/projects/xFactory/openxFactory-worktrees/005-customer-subject-runtime`
(all repo paths below are relative to it). This document is NOT repository
content — never commit it or copy prose from it into committed files.

Every name, byte, and signature pinned here is FROZEN. If you believe a pin is
wrong, implement it as pinned anyway and report the concern in your
`escalations` output — do not unilaterally diverge, other lanes depend on it.
Semantics are governed by the ratified documents (read them; they win over
this file for behavior, this file wins for names/formats).

## 0. Mandatory reading (in this order)

1. `specs/005-customer-subject-runtime/fable-swarm-handoff-us3.md` — mission + stop conditions
2. `openspec/changes/archive/2026-08-27-add-hermes-customer-subject-runtime-contract/specs/hermes-governed-record-integrity/spec.md` — requirement "v2 persistence coexists with v1 and migrates atomically" (THE binding requirement; byte-exact digest profile text lives here)
3. `openspec/changes/archive/2026-08-27-add-hermes-customer-subject-runtime-contract/design.md` — Decisions 7 (migration protocol) and context
4. `specs/005-customer-subject-runtime/research.md` — Decisions 5, 6, 8, 9
5. `specs/005-customer-subject-runtime/data-model.md` — "Migration" section
6. `specs/005-customer-subject-runtime/tasks.md` — your lane's task text (T052–T065)
7. Your lane's briefs (scratchpad, sibling to this file):
   - `brief-sql-surface.md` — v2.sql conventions (Lane C mandatory; A/B skim)
   - `brief-test-harness.md` — harness mechanics (all lanes)
   - `brief-validation-tooling.md` — validator/schema dialect (Lane A mandatory)
   - `brief-v1-inventory.md` — exact v1 DDL (all lanes)
   - `brief-catalogs-gates.md` — catalog shapes (Lane D only)

## 1. Stop conditions (from the handoff — absolute)

- Do NOT start US4, allocate a bundle version, tag/publish, or edit
  `opensoft/xFactory-Hermes-Install`.
- Do NOT mark OpenSpec acceptance or Gate G0 complete.
- Do NOT regenerate `tests/hermes_runtime_contracts/postgres/evidence/*.json`
  (Lane D/integration does that after source freeze; the runner deletes them
  when it runs — that is fine, just never hand-author them).
- Do NOT commit. The coordinator owns the single US3 checkpoint commit.
- Do NOT write host-absolute paths into any repository file.

## 2. File ownership (collisions are forbidden)

Already edited by the coordinator (consume, do not edit):
- `tests/hermes_runtime_contracts/postgres/conftest.py` — new frozen fixtures:
  - `postgres_empty_database` — empty per-test DB, NO DDL applied (Lane B)
  - `postgres_v1_database` — v2-template clone + pinned v1 DDL applied, unseeded (Lanes A/C)
  - `private_postgres_cluster` — function-scoped disposable cluster (v2+v1 DDL
    and cluster roles applied to `hermes_runtime_contracts`), safe to
    `cluster.compose("kill", "postgres")` and restart (Lane C crash tests)
  - constants `CANONICAL_DDL_V1` (= `contracts/schemas/hermes-operational-postgres.sql`),
    `MIGRATION_SQL` (= `contracts/hermes-runtime/migrations/v1-to-v2.sql`),
    `MIGRATION_FIXTURE_ROOT`, `MIGRATION_ASSERTION_ROOT`
- `tests/hermes_runtime_contracts/postgres/fixtures/isolation/00-cluster-roles.sql`
  — added login role `hcs_migrator`, member of `xfactory_v2_migrator`.

Lane A owns exclusively:
- `tests/hermes_runtime_contracts/postgres/test_migration.py`
- `contracts/hermes-runtime/migrations/v1-to-v2-mapping.schema.yaml`
- `contracts/hermes-runtime/legacy-quarantine-record.schema.yaml`
- `scripts/hermes_runtime_validation/migration.py`
- `scripts/hermes-runtime-dataset-digest.py`
- `tests/hermes_runtime_contracts/postgres/fixtures/digest-golden-vectors.yaml`

Lane B owns exclusively:
- `tests/hermes_runtime_contracts/postgres/test_clean_apply.py`
- `tests/hermes_runtime_contracts/postgres/test_ddl_drift.py`
- `scripts/apply-hermes-runtime-postgres-v2.py`
- `scripts/validate-hermes-runtime-postgres.py`

Lane C owns exclusively:
- `contracts/hermes-runtime/hermes-operational-postgres-v2.sql` (append-only
  evolution; never weaken existing US1/US2 objects)
- `contracts/hermes-runtime/migrations/v1-to-v2.sql` (new)
- `scripts/run-hermes-v1-to-v2-migration.sh` (new)
- `tests/hermes_runtime_contracts/postgres/test_migration_recovery.py`
- `tests/hermes_runtime_contracts/postgres/test_quarantine.py`
- `tests/hermes_runtime_contracts/postgres/fixtures/migration/` (all files)
- `tests/hermes_runtime_contracts/postgres/assertions/migration/` (all files)
- Lane C MAY additionally repair existing US2 expectations that legitimately
  change because the SQL surface grew (`test_contract_alignment.py`,
  `assertions/isolation/*-catalog.sql`) — smallest possible diffs, and report
  each such repair in your output.

Lane D (runs later, not now): `contracts/hermes-runtime/contract-index.yaml`,
`contracts/hermes-runtime/fixtures/index.yaml`,
`contracts/hermes-runtime/acceptance-map.yaml`,
`contracts/hermes-runtime/evidence-register.yaml`,
`contracts/hermes-runtime/README.md`, `specs/005-customer-subject-runtime/tasks.md`
checkboxes. NO other lane touches these — your unregistered files will fail
the strict validator until Lane D runs; that is expected and correct.

Nobody touches: `scripts/run-hermes-runtime-postgres-tests.sh`,
`tests/hermes_runtime_contracts/postgres/compose.yaml`, `images.lock.yaml`,
`contracts/schemas/hermes-operational-postgres.sql` (pinned v1 contract),
anything under `openspec/`, `specs/` (docs), or `contracts/releases/`.

## 3. Namespaces, roles, placement

- Migration ledger/staging tables + all helper functions: schema
  `xfactory_runtime_v2` (owner `xfactory_v2_owner`, created in the existing
  `set role xfactory_v2_owner` section — append new DDL BEFORE the final
  `reset role;`).
- Governed entrypoints: schema `xfactory_runtime_api_v2`, SECURITY DEFINER,
  `set search_path = pg_catalog, xfactory_runtime_v2` per existing convention.
- The 8 compatibility-history tables live in `xfactory_runtime_v2` (they are
  scoped, RLS-forced governed records — research Decision 5), NOT in the
  quarantine schema.
- Quarantine: single table `xfactory_legacy_quarantine_v2.legacy_quarantine_records`.
  The schema already exists sealed (no usage grants). Grant usage/insert paths
  to owner only; migrator reaches it only through owner-owned SECURITY DEFINER
  functions. Runtime/control/audit get NOTHING.
- `xfactory_v2_migrator` finally gets privileges: usage on
  `xfactory_runtime_api_v2` + execute on exactly the migration API functions
  in §5 (never direct table grants, never quarantine access).
- Test login for migrator class: `hcs_migrator` (already provisioned).

## 4. Digest profiles — byte-exact pins

### 4.1 Frame tags are HEXADECIMAL byte values

The ratified text writes byte literals in hex (`bytes 00 01`, `nullable is
exactly 00 or 01`). All tags are therefore hex bytes, nibble-grouped:
structure `0x10–0x17`, rows `0x20–0x21`, values `0x30–0x36`.

- Stream: ASCII `XFV1DS` + `0x00 0x01`, then table frames.
- Frame: `tag:u8 || payload_length:u64be || payload`.
- Table frame tag `0x10`; payload = schema-name frame `0x11` (UTF-8),
  table-name frame `0x12` (UTF-8), column-count frame `0x13` (payload u64be),
  one column frame `0x14` per schema ordinal, row-count frame `0x17`
  (payload u64be), then row frames `0x20`.
- Column frame `0x14` payload = `ordinal:u64be || nullable:u8 (0x00|0x01) ||
  primary_key_position:u64be (0 = non-key, else 1-based) || name frame 0x15
  (UTF-8) || normalized-type frame 0x16 (ASCII, one of: text int4 int8 bool
  timestamptz jsonb bytea)`.
- Row frame `0x20` payload = one column frame `0x21` per schema ordinal;
  `0x21` payload = `ordinal:u64be || value frame`.
- Value frames: null `0x30` (empty payload); text `0x31` (UTF-8); integer
  `0x32` (minimal base-10 UTF-8, no `+`, no leading zeros, `-` allowed, zero
  is `0`); boolean `0x33` (single byte `0x00`/`0x01`); timestamp `0x34` (UTC
  RFC 3339 UTF-8, exactly six fractional digits, `Z`, e.g.
  `2026-07-12T12:00:00.000000Z`); binary `0x35` (lowercase-hex ASCII of the
  bytes, no prefix); json `0x36` (canonical JSON UTF-8, §4.2).
- Ordering: tables sorted by raw UTF-8 `(schema, table)` bytes; rows sorted
  bytewise by the concatenation of their FRAMED primary-key value frames in
  primary-key-position order; columns in schema ordinal order (1-based). No
  Unicode normalization anywhere.
- SHA-256 covers magic+version bytes plus every complete ordered table frame.
- v1 type normalization: `integer→int4`, `bigint→int8`, `boolean→bool`,
  `text→text`, `timestamptz→timestamptz`, `jsonb→jsonb`, `bytea→bytea`.
  Anything else in an observed source column ⇒ fail closed.

### 4.2 Canonical JSON (`xfactory-canonical-json-v1`)

UTF-8 compact (no whitespace) JSON: object keys sorted by raw UTF-8 bytes;
array order preserved; escape ONLY `"`, `\`, and U+0000–U+001F as lowercase
`\u00xx`; `true`/`false`/`null` literal; numbers are arbitrary-precision
decimals without exponent, `+`, or insignificant zeros; `-0` → `0`; floats
and non-JSON values forbidden. Record digests: `sha256:<64hex>` over the
canonical JSON of the complete closed record with its own digest field
omitted. The existing SQL implementation is
`xfactory_runtime_v2.canonical_json(jsonb)` /
`canonical_record_digest(...)` — Lane A's Python MUST byte-match it (read it
before implementing; if it contradicts the ratified rules, match the ratified
rules and escalate).

### 4.3 Derived identities

- `catalog_digest` = record digest of
  `{"profile":"xfactory-v1-catalog-v1","tables":[<catalog entries, table
  order as §4.1>]}` where each entry is
  `{"schema_name","table_name","columns":[{"ordinal","name","normalized_type","nullable","primary_key_position"}...]}`.
- `logical_boundary_id` = `sha256:` + SHA-256 of canonical JSON of
  `{"profile":"xfactory-v1-logical-boundary-v1","source_identity":{"source_database":...,"source_schema":...},"catalog_digest":...,"table_row_counts":{"<schema>.<table>":<int>...},"dataset_digest":...}`.
- Per-table digest = `sha256:` over that table's complete `0x10` frame bytes.
- Per-row digest (used in legacy_*/quarantine rows) = `sha256:` over that
  row's complete `0x20` frame bytes.

## 5. SQL surface pins (Lane C implements; A/B consume)

Tables in `xfactory_runtime_v2` (all immutable via the existing
`reject_immutable_mutation` trigger pattern; text IDs; no sequences):

- `migration_staging(installation_id, migration_id, payload jsonb,
  authority_envelope jsonb, mapping_payload_digest, authority_envelope_digest,
  staged_at)` PK `(installation_id, migration_id)` — digests are DB-recomputed,
  never trusted from the caller.
- `migration_attempts(attempt_id, installation_id, migration_id,
  mapping_payload_digest, created_at)`
- `migration_attempt_events(event_id, attempt_id, installation_id,
  migration_id, event_type CHECK IN ('started','succeeded','failed','abandoned'),
  predecessor_event_id, reason, occurred_at)` — linear chain per attempt
  series, database-derived time.
- `migration_cutover_observations(observation_id, attempt_id,
  mapping_payload_digest, authority_envelope_digest, logical_boundary_id,
  transaction_snapshot, wal_position, authorized_at, run_migration_grant_id,
  run_migration_grant_digest, target_contract_identity jsonb,
  reconciliation_digest)`
- `migration_reconciliations(reconciliation_id, attempt_id, per_table jsonb,
  compatibility_history_count, quarantine_count, freeze jsonb,
  reconciliation_digest)` — `per_table` has all twelve entries with input
  count, table-frame digest, and classification counts.
- 8 compatibility-history tables, uniform shape:
  `legacy_jobs, legacy_job_runs, legacy_job_events, legacy_workers,
  legacy_groups, legacy_profiles, legacy_group_memberships,
  legacy_github_team_mappings` each
  `(migration_id, source_schema, source_table, source_pk, source_row_digest,
  source_row jsonb, scope_kind CHECK IN ('layer','installation_admin'),
  installation_id, stack_id, layer_id /*null for installation_admin*/,
  captured_at)` PK `(migration_id, source_schema, source_table, source_pk)`;
  RLS enabled+forced with policy `<table>_exact_scope` (existing pattern);
  `scope_kind='installation_admin'` rows must NOT be visible to customer-layer
  scopes; select granted to `xfactory_v2_runtime, xfactory_v2_audit`.
  `source_pk` = canonical JSON array of the PK column values in
  primary-key-position order, encoded as their §4.1 text forms.
  `source_row` = JSON object column-name → value (§4.1 text encodings; null
  stays JSON null; jsonb embedded as-is).
- Quarantine: `xfactory_legacy_quarantine_v2.legacy_quarantine_records(
  migration_id, source_schema, source_table, source_pk, source_row_digest,
  reason_code CHECK IN ('missing_content_digest','missing_target_digest',
  'missing_reviewer_authority','missing_binding_evidence',
  'unverifiable_ancestry'), source_row jsonb, captured_at)` same PK pattern.

Functions (owner-owned; grant execute on the api ones to
`xfactory_v2_migrator` only):

- `xfactory_runtime_v2.migration_observe_source(source_schema text) returns jsonb`
  → `{"catalog":[...], "catalog_digest":..., "table_row_counts":{...},
  "per_table_digests":{...}, "dataset_digest":...}` over exactly the twelve
  canonical tables (missing/drifted table or unsupported column type ⇒ raise).
- `xfactory_runtime_v2.migration_dataset_stream(source_schema text) returns bytea`
- `xfactory_runtime_v2.migration_dataset_stream_from(dataset jsonb) returns bytea`
  (input = dataset-description JSON, §7 shape — used for golden-vector parity)
- `xfactory_runtime_v2.migration_dataset_digest(source_schema text) returns text`
- `xfactory_runtime_v2.migration_logical_boundary(source_identity jsonb,
  observation jsonb) returns text`
- `xfactory_runtime_v2.install_v1_freeze(requested_migration_id text) returns jsonb`
  — installs, on each of the twelve v1 tables: trigger `hermes_v1_freeze_write`
  (BEFORE INSERT OR UPDATE OR DELETE OR TRUNCATE where applicable) calling
  `xfactory_runtime_v2.reject_frozen_v1_write()`, plus write REVOKEs; returns
  the freeze identity JSON recorded in the reconciliation.
- `xfactory_runtime_api_v2.stage_migration(staging jsonb) returns jsonb` —
  input is the §6 staging document; independently recomputes both digests,
  verifies the envelope binds the payload digest and an ACTIVE `run_migration`
  grant chain (reuse `active_authority_chain`, resource constraints: type
  `migration_mapping`, exact migration_id, exact payload digest); inserts
  staging; idempotent for byte-identical re-stage; conflicting re-stage fails.
- `xfactory_runtime_api_v2.begin_migration_attempt(requested_installation_id
  text, requested_migration_id text) returns jsonb` — own committed txn under
  the session lock: terminal-success ⇒ return stored result
  `{"status":"succeeded","terminal":true,...}` without new attempt; open
  prior attempt ⇒ append `abandoned` first; else create attempt + `started`.
- `xfactory_runtime_api_v2.execute_v1_cutover(requested_installation_id text,
  requested_migration_id text, requested_attempt_id text) returns jsonb` —
  body of the authoritative SERIALIZABLE transaction (caller opens it). D11
  amendment (F-P1): the CALLER acquires the twelve
  `LOCK TABLE public.hermes_* IN SHARE ROW EXCLUSIVE MODE` locks as top-level
  utility statements, in bytewise `(schema,table)` order, immediately after
  `BEGIN ISOLATION LEVEL SERIALIZABLE;` and BEFORE the
  `select execute_v1_cutover(...)` — a top-level LOCK does not take the
  transaction snapshot, so the snapshot is pinned only after all locks are
  held. The function VERIFIES (never acquires) the locks and raises
  `HGR-MIGRATION-V1-LOCKS-NOT-PREHELD` if the session does not already hold
  `ShareRowExclusiveLock` or stronger on each of the twelve; then: observe; recompute
  logical boundary and abort on any payload mismatch; migrate the 8 → legacy_*
  with ancestry/mapping rules; quarantine the 4; reconcile exactly-once for
  every source row; `install_v1_freeze`; insert cutover observation
  (`pg_current_snapshot()::text`, `pg_current_wal_lsn()::text`,
  `transaction_timestamp()`); append `succeeded`; return reconciliation
  summary.
- `xfactory_runtime_api_v2.fail_migration_attempt(requested_installation_id
  text, requested_migration_id text, requested_attempt_id text, reason text)
  returns void` — appended AFTER rollback, session lock still held.
- `xfactory_runtime_api_v2.migration_result(requested_installation_id text,
  requested_migration_id text) returns jsonb` — read-only status/result.

Advisory lock keys (pinned exactly):
- Migration session lock:
  `pg_advisory_lock(hashtextextended('xfactory-v1-to-v2-migration:' || installation_id || E'\n' || migration_id, 0))`
- Apply-boundary session lock (Lane B):
  `pg_advisory_lock(hashtextextended('xfactory-v2-apply-boundary', 0))`

Quarantine DDL guard: event trigger `xfactory_quarantine_dependency_guard`
ON `ddl_command_end`, function
`xfactory_runtime_v2.reject_quarantine_dependency()` — rejects any new
non-quarantine object depending on quarantine objects. Event triggers need
superuser: create it OUTSIDE the `set role xfactory_v2_owner` section (after
`reset role;` at file end).

Classification (fixed): compatibility history ⇐ `hermes_jobs`,
`hermes_job_runs`, `hermes_job_events`, `hermes_workers`, `hermes_groups`,
`hermes_profiles`, `hermes_group_memberships`, `hermes_github_team_mappings`.
Quarantine ⇐ `hermes_job_artifacts`, `hermes_approval_requests`,
`hermes_approvals`, `hermes_traceability_edges` (reason codes:
artifacts→`missing_content_digest`, approval_requests→`missing_target_digest`,
approvals→`missing_reviewer_authority`,
traceability_edges→`missing_binding_evidence`).

Scope resolution: jobs via `subject_mappings` on `hermes_jobs.project`;
runs/events inherit ONLY through verified job ancestry (row's own `project`
field, where present, must agree with the ancestor job's, else abort);
workers/groups/profiles via explicit per-source-PK `admin_mappings`
(layer or installation_admin); memberships/github mappings inherit only when
every endpoint maps and all endpoints agree on one scope; any unmapped or
ambiguous governed row ⇒ whole-transaction abort. `single_default_mapping`
is legal only when the observed distinct `project` values across jobs and
runs are exactly the one mapped value.

`migrations/v1-to-v2.sql`: source-specific validation/transform/reconcile/
freeze-attachment logic ONLY (catalog assertions, the mapping/ancestry
transforms, reconciliation, freeze attachment); base structures stay in the
main v2 file. Mirror the file frame: lowercase SQL, header comment,
`set role xfactory_v2_owner; set search_path = pg_catalog,
xfactory_runtime_v2;` ... `reset role;`.

## 6. Staging document (Python builds it, SQL independently verifies)

Canonical JSON (one line, §4.2):

```json
{"schema_version":1,"kind":"openxfactory-hermes-runtime-migration-staging",
 "payload":{...mapping payload...},
 "authority_envelope":{...envelope...}}
```

Mapping payload closed field set (kind
`openxfactory-hermes-runtime-migration-mapping-payload`, `schema_version: 1`):
`migration_id, installation_id, source_identity{source_database,source_schema},
source_catalog (twelve entries, §4.3 shape, §4.1 order),
expected_table_row_counts{"<schema>.<table>":int},
expected_dataset_digest, digest_profile:"xfactory-v1-dataset-binary-v1",
subject_mappings:[{legacy_project, layer_id,
customer_subject{kind,issuer,namespace,ref}}],
admin_mappings:{workers:[{source_pk, scope_kind, layer_id?}], groups:[...],
profiles:[...]}, single_default_mapping:{enabled:bool, legacy_project?} | null,
target_topology:{installation_id, stack_id, client_layer_id, domain_layer_id,
customer_layer_ids:[...]}, migration_policy:{policy_ref, policy_digest},
mapping_payload_digest` (self-digest omitted from own digest computation).

Authority envelope closed field set (kind
`openxfactory-hermes-runtime-migration-authority-envelope`, `schema_version: 1`):
`migration_id, installation_id, mapping_payload_digest,
approver_principal_id, run_migration_grant_id, run_migration_grant_digest,
policy_ref, policy_digest, scope{installation_id}, trust_anchor_id,
trust_anchor_digest, approved_at, authority_envelope_digest` (self-digest
omitted from own digest computation; payload digest included so no cycle).

## 7. Dataset description + golden vectors (YAML)

Dataset description (input to the digest CLI, `migration_dataset_stream_from`,
and the seed mirrors):

```yaml
schema_version: 1
kind: xfactory-v1-dataset-description
source_schema: public
tables:
  - schema_name: public
    table_name: hermes_jobs
    columns:            # ordinal = 1-based list position
      - {name: id, normalized_type: text, nullable: false, primary_key_position: 1}
      - {name: schema_version, normalized_type: int4, nullable: false, primary_key_position: 0}
    rows:               # any order; digest sorts by framed PK
      - - {type: text, value: "job-1"}
        - {type: integer, value: "1"}     # string to keep arbitrary precision
```

Cell forms: `{type: null}`, `{type: text, value: str}`,
`{type: integer, value: str}`, `{type: boolean, value: true|false}`,
`{type: timestamp, value: "....Z" (six fractional digits)}`,
`{type: binary, value: "<lowercase hex>"}`, `{type: json, value: <any JSON>}`.

Golden vectors file `tests/hermes_runtime_contracts/postgres/fixtures/digest-golden-vectors.yaml`:

```yaml
schema_version: 1
kind: xfactory-v1-dataset-golden-vectors
vectors:
  - vector_id: <stable-id>
    dataset: {<inline dataset description>}
    expected_stream_hex: "<full lowercase hex of the entire stream>"   # small vectors
    expected_stream_sha256: "sha256:<hex>"
    expected_table_frame_digests: {"public.hermes_jobs": "sha256:<hex>", ...}
```

The smallest vector must be hand-derived byte-by-byte (documented in a YAML
comment) — never generated by the implementation it validates. Include at
minimum: empty twelve-table dataset; single-row single-table; composite-PK
row-ordering case; every value tag incl. unicode (non-ASCII, astral), empty
string, negative/zero integers, `-0` JSON normalization, nested JSON with
key-sort + escapes; a null in a nullable column.

## 8. Python library `scripts/hermes_runtime_validation/migration.py` (Lane A)

Exact public API (other lanes' tests import these):

```python
DATASET_PROFILE = "xfactory-v1-dataset-binary-v1"
CATALOG_PROFILE = "xfactory-v1-catalog-v1"
LOGICAL_BOUNDARY_PROFILE = "xfactory-v1-logical-boundary-v1"

class MigrationContractError(ValueError):  # .code: stable finding code, .message
def canonical_json_text(value) -> str
def canonical_json_bytes(value) -> bytes
def record_digest(record, *, omit_field) -> str          # "sha256:<hex>"
def mapping_payload_digest(payload) -> str               # omit mapping_payload_digest
def authority_envelope_digest(envelope) -> str           # omit authority_envelope_digest
def dataset_stream(dataset) -> bytes
def dataset_digest(dataset) -> str
def table_frame(table) -> bytes
def table_frame_digest(table) -> str
def catalog_from_dataset(dataset) -> list[dict]
def catalog_digest(catalog) -> str
def table_row_counts(dataset) -> dict[str, int]
def logical_boundary_id(*, source_identity, catalog, table_row_counts, dataset_digest) -> str
def validate_mapping_payload(payload) -> None            # raises MigrationContractError
def validate_authority_envelope(envelope, *, payload) -> None
def build_staging_document(payload, envelope) -> str     # validates, returns canonical JSON text
def load_dataset_description(path) -> dict
def load_golden_vectors(path) -> list[dict]
```

Pure stdlib + PyYAML. No floats anywhere (YAML floats ⇒ error). Loader
strictness per the family conventions (see `brief-validation-tooling.md`).

CLI `scripts/hermes-runtime-dataset-digest.py`:
`--dataset <yaml> [--json] [--emit-stream <path>]` prints dataset digest,
per-table digests, row counts; exit 0 ok / 1 findings / 2 harness error.

## 9. Operational scripts (Lane B, Lane C)

Connection indirection (tests inject the compose path): a psql command
TEMPLATE string, shlex-split, containing the literal placeholder `{database}`;
the tool substitutes the target database per connection and pipes SQL on
stdin. In-container psql over the local socket needs no password (official
image trusts local). Example tests will pass:
`docker compose --file <abs compose> --project-name <proj> exec -T postgres
psql -X -q -A -t -v ON_ERROR_STOP=1 -U hermes_runtime -d {database}`.

- `scripts/validate-hermes-runtime-postgres.py --psql-command "<template>"
  --database <name> --profile {fresh-v2,v1-pre-cutover,v1-cutover} [--json]`
  — READ-ONLY fingerprint/readiness: derives the expected profile
  deterministically by creating a scratch database (via the template against
  the `postgres` maintenance DB), applying the canonical DDL(s)
  (fresh-v2: v2 only; v1-pre-cutover: v2+v1; v1-cutover: v2+v1 then
  `contracts/hermes-runtime/migrations/v1-to-v2.sql` then
  `select xfactory_runtime_v2.install_v1_freeze('profile-derivation')`
  — amended by D10; the original pin omitted the migrations file and made
  every legitimately cut-over database report 3x XFV2-FUNCTION-EXTRA +
  12x XFV2-ACL-ALTERED),
  fingerprinting scratch and target, diffing, then dropping scratch.
  Fingerprint dimensions (each independently reported): tables/columns/
  constraints/indexes, policies, functions (incl. security-definer +
  proconfig/search_path), triggers, role attributes + memberships, schema/
  table/function ownership + ACLs, relrowsecurity/relforcerowsecurity, PUBLIC
  privileges, trusted-schema writability, quarantine grants, durable-freeze
  objects, event-trigger dependency guard. Exit 0 ready / 1 findings / 2 error.
- `scripts/apply-hermes-runtime-postgres-v2.py --psql-command "<template>"
  --database <name> [--json]` — the locked boundary: one session takes the
  apply advisory lock (§5), preflights (empty or exact fresh-v2 state ONLY —
  never mutate or repair before comparison), applies the complete v2 DDL in
  one transaction when accepted, postflights fresh-v2, reports. Exit codes
  as above.
- `scripts/run-hermes-v1-to-v2-migration.sh` (POSIX sh, ShellCheck-clean):
  env `HERMES_MIGRATION_PSQL_COMMAND` (same `{database}` template semantics,
  connecting as a MIGRATOR-class login, e.g. `-U hcs_migrator` in tests —
  note in-container socket auth trusts any user), args
  `--database <name> --staging-file <canonical-json path>
  --installation-id <id> --migration-id <id>`. ONE long-lived psql session
  (session advisory lock lives on its connection) drives: acquire lock →
  txn: stage + begin_migration_attempt (STARTED survives) → SERIALIZABLE txn:
  execute_v1_cutover + commit → on error: rollback, txn: fail_migration_attempt
  → release lock. Terminal-success observer path exits 0 with the stored
  result. Exit 0 success/converged, 1 failed (FAILED/ABANDONED recorded),
  2 harness error. psql scripting hint: run the controlled section with
  ON_ERROR_STOP off and branch on `\if :ERROR` / `:SQLSTATE`; never leave the
  session between lock acquisition and terminal event.

## 10. Migration fixtures (Lane C authors; A and C consume)

Under `tests/hermes_runtime_contracts/postgres/fixtures/migration/`:
- `10-v1-two-subject-seed.sql` — deterministic rows in ALL twelve tables,
  two legacy projects `project-alfa`, `project-beta`; every table ≥2 rows;
  include: nulls in nullable columns, non-ASCII text, jsonb values needing
  key-sorting/escapes, fixed timestamps (`2026-07-01T00:00:00.000000Z`
  style), composite-PK rows in `hermes_group_memberships`.
- `11-v1-one-subject-seed.sql` — single project `project-alfa` (default-map
  positive case).
- `30-migration-authority.sql` — migration principal `principal-migrator`,
  DB binding for `hcs_migrator`, and an ACTIVE `run_migration` grant chain
  (resource type `migration_mapping`) issued under the existing seeded
  anchor/root pattern — copy the conventions of
  `fixtures/isolation/20-authority.sql` (grant IDs deterministic, e.g.
  `grant-run-migration-01`).
- YAML mirrors `v1-two-subject-dataset.yaml`, `v1-one-subject-dataset.yaml` —
  EXACTLY the same logical content as the SQL seeds, §7 shape. Digest parity
  between mirror (Python/SQL-from-jsonb) and live tables (SQL observe) is a
  required test.
- Every seed starts `\set ON_ERROR_STOP on`.
- Assertions under `assertions/migration/` follow the existing catalog/probe
  conventions (`WITH expected(...) VALUES ... bool_and(...)` single-boolean,
  or invariant strings like `"1:1:1"`).

Base topology/authority for migration tests: apply
`fixtures/isolation/10-two-customer-topology.sql` + `20-authority.sql` first
(the `postgres_v1_database` fixture does NOT seed them), then `30-migration-authority.sql`.
Target layer IDs available from the isolation topology: installation
`install-01`, stack `stack-01`, customer layers `customer-a`, `customer-b`
(check the seed file for exact IDs and reuse them in payload
`target_topology` and `subject_mappings`).

## 11. Test conventions (all lanes)

- `pytestmark = pytest.mark.postgres` in every new module under `postgres/`.
- NEVER `pytest.skip` in `postgres/` (the runner rejects skips).
- Import from `.conftest`; module docstring
  `"""RED real-PostgreSQL contracts for <topic>."""`.
- One psql call = one connection = one script; re-`assume_scope` per script;
  probes wrapped `BEGIN; ... ROLLBACK;`.
- `assert_sql_fails(result, *fragments)` with several plausible wordings.
- Deterministic literals for expected digests ONLY in golden vectors; live-DB
  expectations computed via `hermes_runtime_validation.migration` at test
  time (sys.path: tests already get `PYTHONPATH=$repo_root`; import as
  `from scripts.hermes_runtime_validation import migration` — check how
  existing tests import the package in `test_runner_contract.py` and match).
- Self-verify before returning: `black --check` on new Python,
  `python3 -m compileall -q` them, `shellcheck` + `sh -n` on new shell,
  `.venv/bin/pytest <your pure-python tests> -q` where applicable, and for
  live-DB work run at least your own modules against ONE major:
  `HERMES_RUNTIME_POSTGRES_MAJOR=16 .venv/bin/pytest
  tests/hermes_runtime_contracts/postgres/<your files> -m postgres -q -p
  no:cacheprovider` from the worktree root. Docker + both pinned images are
  available. RED tests that fail because ANOTHER lane's artifact does not
  exist yet are expected — report them as such, do not weaken them.

## 12. Output contract (every lane returns structured JSON)

`files_written` (paths + one-line purpose), `tests_run` (commands + outcomes),
`red_expected` (tests intentionally failing pending other lanes),
`repairs_to_existing` (Lane C only), `escalations` (pin disagreements,
spec ambiguities you resolved locally — state the resolution), `notes`.
