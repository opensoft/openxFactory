# V1 Hermes Operational Schema — Authoritative DDL Location

## 1. Authoritative v1 DDL: found, in the worktree itself

**Primary (authoritative for the migration):**
`/workspace/projects/xFactory/openxFactory-worktrees/005-customer-subject-runtime/contracts/schemas/hermes-operational-postgres.sql`

- Registered in `contracts/manifest.yaml` (lines 81–91) as contract id `hermes-operational-postgres`, `type: sql_schema`, `schema_version: 1`, `source_path: Omnigent-Install/schemas/hermes-operational-postgres.sql`, `compatibility: copied_from_source_commit`, `adapter_owner: Omnigent-Install`. Landed in commit `057c032` ("Copy shared factory contracts (#14)").
- Also indexed in `contracts/README.md` line 38.
- This single file defines **exactly the twelve canonical tables** named in the specs, plus 6 indexes. Tables live in the default `public` schema (research.md Decision 5: "Preserve `public.hermes_*` v1 tables"). All PKs are `text`; no sequences, no extensions required.

**Upstream original:** `/workspace/projects/xFactory/installs/omnigent-install/schemas/hermes-operational-postgres.sql` — byte-identical **except** it contains a 13th table, `hermes_worker_readiness` (worker_id text PK, status check available/unavailable, current_jobs, metadata jsonb, registered_at, last_seen_at, updated_at). That table is **not** part of the twelve and not mentioned anywhere in the worktree — the openxFactory copy (without it) is the migration-authoritative surface. Worth flagging to the mapping-payload/catalog-profile design: a real v1 database created from the Omnigent original would contain this extra table.

## 2. Exact v1 table definitions (verbatim from the authoritative file)

```sql
create table if not exists hermes_jobs (
  id text primary key,
  schema_version integer not null,
  issued_by text not null check (issued_by = 'Hermes'),
  job_type text not null,
  project text not null,
  feature_id text,
  epic_id text,
  repository_org text not null,
  repository_name text not null,
  repository_default_branch text not null,
  orchestrator_path text not null,
  routing_policy_path text not null,
  auth_profile_id text not null,
  auth_mode text not null check (auth_mode in ('subscription', 'api', 'mixed')),
  status text not null default 'queued',
  envelope jsonb not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists hermes_job_runs (
  id text primary key,
  job_id text not null references hermes_jobs(id),
  project text not null,
  feature_id text,
  status text not null check (
    status in ('queued','running','waiting_for_approval','approved','blocked','failed','complete','cancelled')
  ),
  current_stage text not null,
  worker_id text not null,
  worker_pool text not null,
  host_class text not null,
  container_id text,
  auth_profile_id text not null,
  auth_mode text not null,
  provider_keys_used boolean not null default false,
  run_record jsonb not null,
  started_at timestamptz not null,
  completed_at timestamptz
);

create table if not exists hermes_job_events (
  id text primary key,
  job_id text not null references hermes_jobs(id),
  run_id text references hermes_job_runs(id),
  occurred_at timestamptz not null,
  event_type text not null,
  actor_type text not null,
  actor_id text not null,
  stage text,
  payload jsonb not null default '{}'::jsonb
);

create table if not exists hermes_job_artifacts (
  id text primary key,
  job_id text not null references hermes_jobs(id),
  run_id text references hermes_job_runs(id),
  artifact_type text not null,
  path text not null,
  sha256 text,
  produced_by text not null,
  approval_state text not null default 'pending',
  created_at timestamptz not null default now()
);

create table if not exists hermes_approval_requests (
  id text primary key,
  job_id text not null references hermes_jobs(id),
  run_id text references hermes_job_runs(id),
  requested_by text not null,
  approval_type text not null,
  status text not null default 'pending',
  artifact_id text references hermes_job_artifacts(id),
  created_at timestamptz not null default now(),
  resolved_at timestamptz
);

create table if not exists hermes_approvals (
  id text primary key,
  approval_request_id text not null references hermes_approval_requests(id),
  job_id text not null references hermes_jobs(id),
  actor_type text not null,
  actor_id text not null,
  decision text not null check (decision in ('approved', 'rejected', 'changes_requested')),
  authority_scope text,
  rationale text,
  created_at timestamptz not null default now()
);

create table if not exists hermes_traceability_edges (
  id text primary key,
  job_id text references hermes_jobs(id),
  from_type text not null,
  from_id text not null,
  to_type text not null,
  to_id text not null,
  relation text not null,
  created_at timestamptz not null default now()
);

create table if not exists hermes_workers (
  id text primary key,
  worker_pool text not null,
  host_class text not null,
  status text not null,
  auth_profile_id text not null,
  auth_mode text not null check (auth_mode in ('subscription', 'api', 'mixed')),
  max_concurrent_jobs integer not null default 1,
  current_jobs integer not null default 0,
  capabilities jsonb not null default '[]'::jsonb,
  metadata jsonb not null default '{}'::jsonb,
  registered_at timestamptz not null default now(),
  last_seen_at timestamptz not null default now()
);

create table if not exists hermes_groups (
  id text primary key,
  purpose text not null,
  agents jsonb not null default '[]'::jsonb,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists hermes_profiles (
  id text primary key,
  role text not null,
  home_group text not null references hermes_groups(id),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists hermes_group_memberships (
  profile_id text not null references hermes_profiles(id),
  group_id text not null references hermes_groups(id),
  membership_type text not null default 'member',
  created_at timestamptz not null default now(),
  primary key (profile_id, group_id)
);

create table if not exists hermes_github_team_mappings (
  group_id text primary key references hermes_groups(id),
  github_team text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

Indexes (lines 163–179 of the file): `hermes_job_events(job_id, occurred_at)`, `hermes_job_runs(job_id)`, `hermes_traceability_edges(from_type, from_id)`, `(to_type, to_id)`, `hermes_workers(worker_pool, status)`, `hermes_group_memberships(group_id)`.

Note the twelve-table names in research.md line 87 exactly match this file: `hermes_jobs, hermes_job_runs, hermes_job_events, hermes_job_artifacts, hermes_approval_requests, hermes_approvals, hermes_traceability_edges, hermes_workers, hermes_groups, hermes_profiles, hermes_group_memberships, hermes_github_team_mappings`. ("artifacts" = `hermes_job_artifacts`, "traces" = `hermes_traceability_edges`.)

## 3. What the specs say about the v1 source shape / seeds

- `specs/005-customer-subject-runtime/research.md` Decision 5 (lines 77–93): keep `public.hermes_*` v1 tables untouched; the exact twelve-table surface listed above; jobs/runs/events/workers/groups/profiles/memberships/github-team-mappings migrate to `legacy_*` scoped, immutable, non-authorizing compatibility-history tables owned by the base v2 SQL; artifacts, approval requests, approvals, and trace edges go **only** to quarantine (their v1 shapes cannot prove finalized bytes / immutable authority / digest-bound evidence — consistent with the DDL above: `sha256` nullable, no digests on approvals/traces).
- Decision 8 + `spec.md` FR-027: the detached mapping payload fixes "the exact twelve-table v1 catalog profile, expected per-table counts and dataset digest" under digest profile `xfactory-v1-dataset-binary-v1` (magic `XFV1DS || 00 01`, `tag:u8 || length:u64be || payload` frames, tags 10–17/20–21 structural, 30–36 for null/text/integer/boolean/timestamp/binary/JSON, framed-primary-key row ordering, schema-ordinal columns, SHA-256 over magic + table stream). Note the value tag set covers exactly the types used by this DDL (text, integer, boolean, timestamptz, jsonb, plus null).
- `fable-swarm-handoff-us3.md` lines 84–99: exactly-one classification per row across the twelve tables; do not alter the binary profile.
- `data-model.md` lines 301–315: mapping-payload and migration-attempt entities; success records "all twelve v1 per-table input counts/digests."

**Test seeds:** `tasks.md` T062 explicitly assigns the tests to create the v1 source data: "Add deterministic all-twelve-table v1 seeds, detached payload/authority envelopes, logical/physical boundary vectors, ... under `tests/hermes_runtime_contracts/postgres/fixtures/migration/` and `.../assertions/migration/`." No `contracts/hermes-runtime/migrations/` dir or migration fixtures exist yet (T059/T062 pending). So tests construct the v1 source database themselves — but they should construct it by applying the authoritative contract file `contracts/schemas/hermes-operational-postgres.sql` (not by inventing DDL), since that is the pinned `schema_version: 1` contract the mapping payload's "exact v1 catalog profile" must describe.

## 4. Direct answer to (3)

A v1 DDL **does** exist and is authoritative: `contracts/schemas/hermes-operational-postgres.sql` in this worktree (copied verbatim from `installs/omnigent-install/schemas/hermes-operational-postgres.sql`, minus `hermes_worker_readiness`). Migration code and test seeds should apply that file to build exact v1 source databases; tests only need to define seed **rows** (T062), not seed DDL.

## Open questions
- The Omnigent-Install original DDL contains a 13th table `hermes_worker_readiness` that the openxFactory v1 copy omits and no spec mentions — should the mapping payload's 'exact twelve-table v1 catalog profile' tolerate (ignore), reject, or quarantine extra non-canonical tables present in a real v1 source database?
- The twelve-table catalog profile in the mapping payload fixes table identity and counts/digest, but no spec states whether it also fixes column names/types (schema-ordinal columns in the digest profile imply column metadata is digest-covered via tags 12-15) — confirm the catalog profile encodes the exact column list from contracts/schemas/hermes-operational-postgres.sql.