# Brief: `hermes-operational-postgres-v2.sql` conventions (for the v1→v2 migration surface)

File: `/workspace/projects/xFactory/openxFactory-worktrees/005-customer-subject-runtime/contracts/hermes-runtime/hermes-operational-postgres-v2.sql` (4471 lines). New file to create: `migrations/v1-to-v2.sql` alongside it.

## 1. Overall file organization

There are **no section-banner comments** anywhere — the only comment is the 6-line file header (lines 1–6), lowercase prose stating the file "is additive: it does not alter the v1 `public.hermes_*` surface" and "is applied by a PostgreSQL superuser or controlled migrator". Everything else is bare lowercase SQL, 2-space indent, ~80-col wrapping, snake_case throughout. Order of the file:

1. `do $roles$ ... $roles$;` — conditional `create role ... nologin` for 5 roles (guarded by `if not exists (select 1 from pg_roles where rolname = ...)`).
2. `alter role ...` hardening lines (nologin nosuperuser nocreatedb nocreaterole [no]inherit noreplication nobypassrls).
3. `create schema if not exists <schema> authorization xfactory_v2_owner;` × 3, then redundant `alter schema ... owner to xfactory_v2_owner;` × 3.
4. `revoke all on schema ... from public;` × 3, then `grant usage on schema ...` to the consumer roles.
5. **Line 53–54:** `set role xfactory_v2_owner;` and `set search_path = pg_catalog, xfactory_runtime_v2;` — *everything after this runs as the owner*.
6. Tables + their indexes (interleaved, index right after the table it belongs to), lines 56–869.
7. Generic trigger functions (`reject_immutable_mutation`, `reject_ungoverned_projection_mutation`, `reconcile_lifecycle_projection`) then a `do $immutable_triggers$` loop that attaches `<table>_immutable` triggers to a literal array of 25 table names.
8. Helper/authority functions (`scope_contains`, `principal_is_active_at`, `anchor_is_active`, `active_authority_chain`), enforcement trigger fn + trigger for cross_layer_bindings, more helpers (`principal_is_active`, `layer_is_active`).
9. API functions in `xfactory_runtime_api_v2` (`current_scope_matches`, `assume_scope`, `clear_scope`, `transition_layer`, `admit_artifact`, `probe_artifact`), one stray index (`approval_one_decision_per_reviewer_uq`, line 2455), more helpers (`artifact_body_matches`, `governed_scope_json`, `principal_selector_matches`), more API fns (`record_approval_decision`, `supersede_approval`, `approval_authorizes`).
10. Canonicalization functions (`canonical_json`, `canonical_record_digest`, `resource_reference_json`) — mid/late file, lines 3243–3350.
11. Digest-computing trigger functions + their `drop trigger if exists` / `create trigger` pairs (trust anchors, authority grants).
12. Remaining API fns (`revoke_authority_grant`, `revoke_cross_layer_binding`, `project_artifact`).
13. `do $row_security$` block (lines 4328–4401): loops a literal array of layer-scoped tables, enable + **force** row level security, creates `<table>_exact_scope` policies; plus a bespoke policy for `operation_authorizations`.
14. Final privilege section (4403–4469): `revoke all on all tables/sequences/functions in schema ... from public;`, `grant select on <explicit table list> to xfactory_v2_runtime, xfactory_v2_audit;`, three `grant execute on function <explicit signature list>` blocks (runtime / control / audit).
15. **Last line (4471): `reset role;`**

Idempotency style: `create table if not exists`, `create [unique] index if not exists`, `create or replace function`, `drop trigger if exists` + `create trigger`, `drop policy if exists` + `create policy`, DO-block guards for roles. Dollar-quote tags are semantic: `$roles$`, `$immutable_triggers$`, `$row_security$`, and every function body uses `$function$`.

## 2. Schemas

| Schema | Contents |
|---|---|
| `xfactory_runtime_v2` | All 26 tables (authoritative state + evidence), all internal/helper/trigger functions. Owner: `xfactory_v2_owner`. `usage` granted to `xfactory_v2_runtime, xfactory_v2_audit` (NOT control — control reaches data only via API functions). |
| `xfactory_runtime_api_v2` | Governed API entrypoint functions only, no tables. `usage` granted to runtime, control, audit. |
| `xfactory_legacy_quarantine_v2` | **Created empty** (lines 41, 44, 48). Owned by owner, `revoke all ... from public`, and **no usage grant to anyone** — a pre-built sealed quarantine boundary awaiting content. |

Tables in `xfactory_runtime_v2` (all `text` ids, no serials/sequences anywhere): `installation_registrations`, `stack_registrations`, `layer_registrations`, `installation_lifecycle_events`, `stack_lifecycle_events`, `layer_lifecycle_events`, `lifecycle_projections`, `principals`, `principal_lifecycle_events`, `database_principal_bindings`, `database_principal_binding_revocations`, `installation_trust_anchors`, `installation_trust_anchor_events`, `authority_grants`, `authority_grant_revocations`, `cross_layer_bindings`, `cross_layer_binding_revocations`, `artifact_bodies`, `artifact_records`, `artifact_lifecycle_events`, `approval_decision_policies`, `approval_requests`, `approval_decisions`, `approval_supersession_events`, `governed_projections`, `operation_authorizations`, `traceability_edges`.

**Placement for the new work:** migration staging/attempt/event/reconciliation tables belong in `xfactory_runtime_v2` (they are governed authoritative state/evidence; add them to the `_immutable` trigger array and grant/RLS lists as appropriate); any callable migration API belongs in `xfactory_runtime_api_v2`; `legacy_*` compatibility-history tables belong in `xfactory_legacy_quarantine_v2` — that schema exists precisely as the quarantine boundary and currently grants usage to nobody (a migrator-only usage grant would be the minimal opening). Note `authority_grants.action` already enumerates **`'run_migration'`** and `'publish_contract'` (line 382–389) — the migration surface should be authorized by grants with `action = 'run_migration'`.

## 3. Role model

Five NOLOGIN role classes, created conditionally then hardened:

- `xfactory_v2_owner` — `noinherit`; owns all three schemas and (via `set role`) every object; RLS policies whitelist it by name.
- `xfactory_v2_migrator` — `noinherit`; **created and hardened but currently granted nothing** — clearly reserved for exactly this migration surface.
- `xfactory_v2_runtime`, `xfactory_v2_control`, `xfactory_v2_audit` — `inherit`; consumer classes. Real login users are made members; `assume_scope` verifies membership via `pg_has_role(session_user, required_role, 'member')` mapping `database_principal_bindings.role_class in ('runtime','control','audit')` to these roles.

GRANT/REVOKE conventions: default-deny. Per-schema `revoke all ... from public` immediately after creation; at end of file blanket `revoke all on all tables/sequences/functions in schema xfactory_runtime_v2 from public` plus functions in the api schema; then **explicit enumerated grants only**: `grant select on <15 layer-scoped tables> to xfactory_v2_runtime, xfactory_v2_audit` (installation-scoped tables like `authority_grants`, `installation_trust_anchors`, `cross_layer_bindings`, `lifecycle_projections`, `artifact_bodies` get **no** direct select — reachable only through SECURITY DEFINER functions), and `grant execute on function` lists with **full parameter signatures**, one block per role class. No `grant all`, ever. No table INSERT/UPDATE/DELETE grants at all — writes happen only inside SECURITY DEFINER API functions or by owner.

RLS: applied in the `do $row_security$` block via `alter table ... enable row level security` + `alter table ... force row level security` (force so even the owner is subject except where the policy exempts it). One policy per table, named **`<table_name>_exact_scope`**, `drop policy if exists` first, both `using` and `with check` identical:
```
current_user = 'xfactory_v2_owner'
or xfactory_runtime_api_v2.current_scope_matches(installation_id, stack_id, layer_id)
```
(`operation_authorizations` variant checks `installation_id, target_stack_id, target_layer_id`.)

search_path / SECURITY DEFINER conventions: **every function** carries a `set search_path` clause. Pure helpers: `language sql immutable strict set search_path = pg_catalog`. Data-reading predicates: `language sql|plpgsql stable security definer set search_path = pg_catalog, xfactory_runtime_v2`. Mutating API fns: `language plpgsql security definer set search_path = pg_catalog, xfactory_runtime_v2`. Trigger fns that only raise: no security definer, `set search_path = pg_catalog, xfactory_runtime_v2`. `pg_catalog` always first; the "trusted schema" set is only ever `pg_catalog` + `xfactory_runtime_v2`. All qualified names are written schema-qualified in bodies despite the search_path.

Session context: transaction-local GUCs `xfactory.installation_id|stack_id|layer_id|principal_id|grant_id` set via `set_config(..., true)` in `assume_scope`/`clear_scope`; guarded write-enable flag `xfactory.governed_projection_write = 'on'` toggled around governed projection upserts. Error convention: `raise exception using errcode = '42501'|'55000'|'22023'|'23514', message = 'HGR-<TOPIC>-<DETAIL>[: prose]'` (one `HCS-LIFECYCLE-TRANSITION`). A durable v1 write freeze / quarantine rejection should mint new `HGR-` codes in this style.

## 4. In-database record digests (US2)

Three functions, all in `xfactory_runtime_v2`:

```sql
create or replace function xfactory_runtime_v2.canonical_json(value jsonb)
returns text language plpgsql immutable strict set search_path = pg_catalog
```
Recursive canonicalization: objects rendered `'{' || string_agg(to_jsonb(member.key)::text || ':' || canonical_json(member.value), ',' order by member.key collate "C") || '}'` (empty → `'{}'`); arrays in ordinality order; **numbers must be integers** — any `[.eE]` raises `22023 HGR-RECORD-DIGEST-NONINTEGER: floating-point values are forbidden`; other scalars via `value::text`.

```sql
create or replace function xfactory_runtime_v2.canonical_record_digest(record_without_digest jsonb)
returns text language sql immutable strict set search_path = pg_catalog, xfactory_runtime_v2
-- body: select 'sha256:' || encode(sha256(convert_to(xfactory_runtime_v2.canonical_json(record_without_digest), 'UTF8')), 'hex')
```

```sql
create or replace function xfactory_runtime_v2.resource_reference_json(
  requested_installation_id text, requested_scope_kind text, requested_stack_id text,
  requested_layer_id text, requested_resource_type text, requested_resource_id text,
  requested_resource_digest text) returns jsonb language plpgsql immutable
```
plus `governed_scope_json(requested_scope_kind, requested_installation_id, requested_stack_id, requested_layer_id) returns jsonb language sql immutable strict` which emits `{scope_kind, installation_id[, stack_id[, layer_id]]}`.

Digest-bound record pattern: every payload is a `jsonb_build_object` **starting** with `'schema_version', 1, 'kind', 'openxfactory-...'`, then the record's own id, then (for digest-profiled records) `'record_digest_profile', new.digest_profile`; refs are nested objects `{installation_id, <id-field>, record_digest}` (principal refs additionally carry a `scope` built by `governed_scope_json`); timestamps serialized as `to_char(ts at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"')`. Existing kinds: `openxfactory-installation-trust-anchor`, `openxfactory-installation-trust-anchor-event`, `openxfactory-authority-grant`, `openxfactory-cross-layer-binding`, `openxfactory-layer-lifecycle-event`, `openxfactory-operation-authorization`, `openxfactory-hermes-runtime-artifact-record`, `openxfactory-hermes-runtime-artifact-lifecycle-event`, `openxfactory-hermes-runtime-approval-decision`, `openxfactory-hermes-runtime-approval-supersession-event`, `openxfactory-hermes-runtime-traceability-edge`. New migration records should follow: `openxfactory-<name>` kind, digest via `canonical_record_digest`.

Two enforcement modes: (a) **BEFORE INSERT triggers compute/overwrite `new.record_digest` server-side** — `compute_trust_anchor_record_digest()` (trigger `installation_trust_anchors_compute_digest`), `compute_authority_grant_record_digest()` (trigger `authority_grants_compute_digest`), and `enforce_cross_layer_binding_creation()` (trigger `cross_layer_bindings_creation_authorized`, which also authorizes and stamps time); (b) API functions compute the digest into a local `..._digest text` variable and insert it. Verification replays: `anchor_is_active` recomputes each event's digest with `canonical_record_digest(event_payload)` and returns false on mismatch. Column pattern: `record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$')` and `digest_profile text not null check (digest_profile = 'xfactory-canonical-json-v1')` on every digest-bound table; every foreign digest column carries the same regex check.

## 5. Database-derived time / backdating defenses

- All effective times come from **`transaction_timestamp()`**, captured once into a declared local (`event_time`, `admission_time`, `decision_time`, `effective_time`, `authorization_time`) or as a parameter default (`active_authority_chain(... evaluation_time timestamptz default transaction_timestamp())`).
- Client-supplied creation times are overwritten: `enforce_cross_layer_binding_creation` does `new.created_at := transaction_timestamp();` then rejects if `new.created_at < new.starts_at or new.created_at >= new.expires_at` (`42501 HGR-BINDING-CREATION-TIME`).
- Table checks: `authority_grants` — `check (expires_at > starts_at)`, `check (issued_at >= starts_at and issued_at < expires_at)`; validity evaluated as `starts_at <= evaluation_time and expires_at > evaluation_time`; anchor replay rejects grants with `starts_at > effective_at`, `expires_at <= effective_at`, or `issued_at > effective_at`.
- Revocations use `effective_at <= transaction_timestamp()` comparisons; child grants must nest in parent windows (`child.starts_at >= parent.starts_at and child.expires_at <= parent.expires_at`).
- Only column default in the file: `artifact_bodies.created_at timestamptz not null default transaction_timestamp()`. Transaction correlation string: `'tx-' || txid_current()::text || '-' || requested_operation_id`.
A migration attempt/event surface should stamp its own times from `transaction_timestamp()` inside SECURITY DEFINER functions or BEFORE INSERT triggers, never trust caller timestamps.

## 6. Naming conventions

- Tables: plural snake_case nouns; evidence tables end `_events`, `_revocations`, `_registrations`, `_records`, `_bodies`; so plausible new names read like `migration_stagings`/`migration_attempts`/`migration_attempt_events`/`migration_reconciliations`, `legacy_*` in the quarantine schema.
- Columns: `*_id text`, `*_digest text` (always regex-checked), `occurred_at`/`effective_at`/`created_at`/`*_at timestamptz not null`; parameters prefixed `requested_`; locals suffixed `_record`, `_time`, `_digest`, `_value`.
- Indexes: all unique, named `<subject>_<qualifier>_uq` (e.g. `installation_one_genesis_anchor_uq`, `layer_lifecycle_predecessor_uq`, `approval_one_decision_per_reviewer_uq`); partial where needed (`where anchor_kind = 'genesis'`). No non-unique indexes exist.
- Constraints: almost all checks are inline/unnamed; the single named one is `constraint authority_grants_root_scope_ck` — so named checks use `<table>_<meaning>_ck`. FKs/PKs unnamed, written as table-level `primary key (...)` / `foreign key (...) references ...`.
- Triggers: `<table>_immutable`, `<table>_compute_digest` style (`installation_trust_anchors_compute_digest`), behavior-named (`cross_layer_bindings_creation_authorized`, `lifecycle_projections_governed_only`, `lifecycle_projections_reconciled`).
- Functions: internal = predicate/verb phrases (`scope_contains`, `principal_is_active_at`, `anchor_is_active`, `active_authority_chain`, `artifact_body_matches`, `reject_*`, `compute_*`, `enforce_*`, `reconcile_*`, `canonical_*`, `*_json`); API = imperative verbs (`assume_scope`, `clear_scope`, `transition_layer`, `admit_artifact`, `probe_artifact`, `record_approval_decision`, `supersede_approval`, `approval_authorizes`, `revoke_authority_grant`, `revoke_cross_layer_binding`, `project_artifact`, `current_scope_matches`).
- Policies: `<table>_exact_scope`. Error messages: `HGR-UPPER-KEBAB` codes. Deterministic ordering always uses `collate "C"`.

## 7. Installation / instance model

- `installation_registrations.installation_id text primary key` — **opaque text, no format constraint**; carries `registration_id` (unique), `registration_digest sha256`, `initial_state = 'installing'`, `genesis_anchor_id`, `created_at`. Exactly one genesis trust anchor per installation (partial unique index `installation_one_genesis_anchor_uq ... where anchor_kind = 'genesis'`).
- Hierarchy keys compose left-to-right: `(installation_id)` → `(installation_id, stack_id)` → `(installation_id, stack_id, layer_id)` → entity id. Installation-scoped rows use **empty-string `stack_id`/`layer_id`** (not NULL), e.g. `principals` check: `scope_kind = 'installation_admin' and stack_id = '' and layer_id = ''`.
- The **customer** is a layer: `layer_registrations.role in ('customer','client','domain')`; customer layers must carry `customer_subject_kind/issuer/namespace` and `customer_subject_ref ~ '^urn:xfactory:subject:[0-9a-f-]{36}$'` (UUID URN), unique per stack via partial index `layer_customer_subject_lifetime_uq ... where role = 'customer'`.
- An installation-scoped advisory lock already exists and is what a migration lock should mirror: `pg_advisory_xact_lock(hashtextextended('anchor:' || scope_installation, 0))` — i.e. key on a `'<namespace>:' || installation_id` string hashed with `hashtextextended(text, 0)`.

## 8. Existing locking patterns

- **Advisory locks: only `pg_advisory_xact_lock(hashtextextended('<ns>:<key>', 0))`** (transaction-scoped, 64-bit, seed 0). Namespaces in use: `'anchor:' || installation_id` (serializes all authority mutations per installation — taken first in every mutator), `'grant:' || grant_id`, `'binding:' || binding_id`, `'resource:' || installation || ':' || stack || ':' || layer || ':' || artifact_id`. Deadlock avoidance by ordered acquisition: pairs taken via `least(...)` then `greatest(...)`; sets via a sorted `select distinct ... order by` loop (see `project_artifact`, lines 3820–3861). Used in `revoke_authority_grant`, `revoke_cross_layer_binding`, `project_artifact`. There are **no session-scoped advisory locks yet** — the requested "session advisory locks" (`pg_advisory_lock` / `pg_try_advisory_lock`) are new, but should reuse the `hashtextextended('<namespace>:' || installation_id, 0)` keying (e.g. `'migration:' || installation_id`).
- Row locks: `select ... into strict ... for update` on the row being mutated; `for share` on rows merely validated (approval requests, artifact records/bodies, grants during decision recording).

## 9. How the file ends / where appended DDL goes

Ending sequence: `project_artifact` function → `do $row_security$` RLS block (4328–4401) → blanket public revokes (4403–4406) → `grant select` table list (4408–4424) → three `grant execute` blocks with full signatures for runtime (4426–4442), control (4444–4461), audit (4463–4469) → **`reset role;` (4471, final statement)**. There is no validation/assertion epilogue.

Appended DDL therefore **must be inserted before `reset role;`** so it executes as `xfactory_v2_owner` (which owns the new objects and makes SECURITY DEFINER functions run as owner). Follow the file's integration pattern: either (a) add new table names into the existing `$immutable_triggers$` array and `$row_security$` array and the grant lists in place, or (b) append self-contained blocks (tables + indexes + functions + a new DO block for triggers/RLS + explicit revoke/grant statements) after line 4469 and before `reset role;`. Given the file otherwise groups by concern, the least-surprising approach for a bolt-on surface is (b): a contiguous appended migration section that repeats the header-comment style (a short lowercase `--` prose block), creates the quarantine/legacy tables schema-qualified as `xfactory_legacy_quarantine_v2.legacy_*`, migration tables as `xfactory_runtime_v2.migration_*`, API entrypoints as `xfactory_runtime_api_v2.*`, attaches `<table>_immutable` triggers via the same loop pattern, and finishes with its own `revoke all ... from public` + enumerated grants (this is the natural place to finally grant `xfactory_v2_migrator` usage/execute — today that role has zero privileges). `migrations/v1-to-v2.sql` should mirror the frame exactly: header comment, conditional role guards if it needs any, `set role xfactory_v2_owner; set search_path = pg_catalog, xfactory_runtime_v2;` ... `reset role;`, and freeze the v1 surface by revoking writes / attaching reject triggers on `public.hermes_*` tables (the v1 surface is only ever referred to as `public.hermes_*`; this file touches nothing in `public`).

## Extra load-bearing signatures (for reuse)

```sql
xfactory_runtime_v2.active_authority_chain(
  requested_installation_id text, requested_grant_id text, requested_action text,
  requested_scope_kind text, requested_stack_id text, requested_layer_id text,
  requested_principal_id text default null,
  evaluation_time timestamptz default transaction_timestamp()
) returns table (root_anchor_id text, root_anchor_digest text,
                 leaf_grant_digest text, leaf_principal_id text)
-- language sql stable security definer; recursive CTE, depth < 63, cycle-guarded,
-- requires exactly one active root grant anchored to an active trust anchor.

xfactory_runtime_api_v2.current_scope_matches(
  requested_installation_id text, requested_stack_id text, requested_layer_id text
) returns boolean  -- the RLS predicate; checks GUCs + binding + grant + liveness.

xfactory_runtime_api_v2.assume_scope(
  requested_installation_id text, requested_stack_id text,
  requested_layer_id text, requested_grant_id text) returns void
```
`authority_grants.action` values (add nothing without a contract change; `'run_migration'` already exists): `assume_scope, issue_grant, revoke_grant, rotate_trust_anchor, revoke_trust_anchor, create_binding, revoke_binding, accept_cross_layer, project_resource, create_artifact, request_approval, decide_approval, supersede_approval, transition_lifecycle, run_migration, publish_contract`.

## Open questions
- Should legacy_* compatibility-history tables live in xfactory_legacy_quarantine_v2 (the empty sealed schema clearly built for this) or in xfactory_runtime_v2 with a legacy_ prefix? The brief recommends the quarantine schema, but no existing object demonstrates the pattern.
- xfactory_v2_migrator currently has zero grants and no schema usage - confirm the migration surface is where it finally gets privileges (usage on quarantine schema + execute on migration API), and whether migration API functions should be granted to migrator only or also to control.
- The v1 surface (public.hermes_*) is never touched by this file - the durable v1 write freeze presumably belongs in migrations/v1-to-v2.sql (revokes + reject triggers on public.hermes_*), but the v1 file itself was not read; engineers should read hermes-operational-postgres v1 to enumerate the exact hermes_* tables and their write roles before freezing.
- Session advisory locks (pg_advisory_lock) have no precedent in the file - only pg_advisory_xact_lock; confirm the intended unlock/ownership discipline (who releases on failure) since the file has no session-scoped state today.
- Whether new record kinds for migration evidence should use the 'openxfactory-hermes-runtime-*' prefix (used by runtime-minted evidence) or the shorter 'openxfactory-*' prefix (used by registration-time records) - both exist; pick per whether records are API-minted or migrator-supplied.