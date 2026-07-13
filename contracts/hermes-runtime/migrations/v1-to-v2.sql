-- openxFactory hermes v1-to-v2 migration: source-specific logic only.
--
-- This file owns the pinned v1 catalog assertions, the mapping and ancestry
-- transforms into the base legacy_* compatibility-history tables, the fixed
-- quarantine classification, exactly-once reconciliation, and durable v1
-- write-freeze attachment. Base structures, framing, staging, attempt, and
-- observation machinery live in hermes-operational-postgres-v2.sql, which
-- must be applied first. It is applied by a PostgreSQL superuser or
-- controlled migrator and is independently re-runnable.

do $catalog_assertions$
declare
  expected_catalog jsonb := $catalog$
    [
      {
        "schema_name": "public",
        "table_name": "hermes_approval_requests",
        "columns": [
          {"name": "id", "normalized_type": "text", "nullable": false, "ordinal": 1, "primary_key_position": 1},
          {"name": "job_id", "normalized_type": "text", "nullable": false, "ordinal": 2, "primary_key_position": 0},
          {"name": "run_id", "normalized_type": "text", "nullable": true, "ordinal": 3, "primary_key_position": 0},
          {"name": "requested_by", "normalized_type": "text", "nullable": false, "ordinal": 4, "primary_key_position": 0},
          {"name": "approval_type", "normalized_type": "text", "nullable": false, "ordinal": 5, "primary_key_position": 0},
          {"name": "status", "normalized_type": "text", "nullable": false, "ordinal": 6, "primary_key_position": 0},
          {"name": "artifact_id", "normalized_type": "text", "nullable": true, "ordinal": 7, "primary_key_position": 0},
          {"name": "created_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 8, "primary_key_position": 0},
          {"name": "resolved_at", "normalized_type": "timestamptz", "nullable": true, "ordinal": 9, "primary_key_position": 0}
        ]
      },
      {
        "schema_name": "public",
        "table_name": "hermes_approvals",
        "columns": [
          {"name": "id", "normalized_type": "text", "nullable": false, "ordinal": 1, "primary_key_position": 1},
          {"name": "approval_request_id", "normalized_type": "text", "nullable": false, "ordinal": 2, "primary_key_position": 0},
          {"name": "job_id", "normalized_type": "text", "nullable": false, "ordinal": 3, "primary_key_position": 0},
          {"name": "actor_type", "normalized_type": "text", "nullable": false, "ordinal": 4, "primary_key_position": 0},
          {"name": "actor_id", "normalized_type": "text", "nullable": false, "ordinal": 5, "primary_key_position": 0},
          {"name": "decision", "normalized_type": "text", "nullable": false, "ordinal": 6, "primary_key_position": 0},
          {"name": "authority_scope", "normalized_type": "text", "nullable": true, "ordinal": 7, "primary_key_position": 0},
          {"name": "rationale", "normalized_type": "text", "nullable": true, "ordinal": 8, "primary_key_position": 0},
          {"name": "created_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 9, "primary_key_position": 0}
        ]
      },
      {
        "schema_name": "public",
        "table_name": "hermes_github_team_mappings",
        "columns": [
          {"name": "group_id", "normalized_type": "text", "nullable": false, "ordinal": 1, "primary_key_position": 1},
          {"name": "github_team", "normalized_type": "text", "nullable": false, "ordinal": 2, "primary_key_position": 0},
          {"name": "created_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 3, "primary_key_position": 0},
          {"name": "updated_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 4, "primary_key_position": 0}
        ]
      },
      {
        "schema_name": "public",
        "table_name": "hermes_group_memberships",
        "columns": [
          {"name": "profile_id", "normalized_type": "text", "nullable": false, "ordinal": 1, "primary_key_position": 1},
          {"name": "group_id", "normalized_type": "text", "nullable": false, "ordinal": 2, "primary_key_position": 2},
          {"name": "membership_type", "normalized_type": "text", "nullable": false, "ordinal": 3, "primary_key_position": 0},
          {"name": "created_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 4, "primary_key_position": 0}
        ]
      },
      {
        "schema_name": "public",
        "table_name": "hermes_groups",
        "columns": [
          {"name": "id", "normalized_type": "text", "nullable": false, "ordinal": 1, "primary_key_position": 1},
          {"name": "purpose", "normalized_type": "text", "nullable": false, "ordinal": 2, "primary_key_position": 0},
          {"name": "agents", "normalized_type": "jsonb", "nullable": false, "ordinal": 3, "primary_key_position": 0},
          {"name": "metadata", "normalized_type": "jsonb", "nullable": false, "ordinal": 4, "primary_key_position": 0},
          {"name": "created_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 5, "primary_key_position": 0},
          {"name": "updated_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 6, "primary_key_position": 0}
        ]
      },
      {
        "schema_name": "public",
        "table_name": "hermes_job_artifacts",
        "columns": [
          {"name": "id", "normalized_type": "text", "nullable": false, "ordinal": 1, "primary_key_position": 1},
          {"name": "job_id", "normalized_type": "text", "nullable": false, "ordinal": 2, "primary_key_position": 0},
          {"name": "run_id", "normalized_type": "text", "nullable": true, "ordinal": 3, "primary_key_position": 0},
          {"name": "artifact_type", "normalized_type": "text", "nullable": false, "ordinal": 4, "primary_key_position": 0},
          {"name": "path", "normalized_type": "text", "nullable": false, "ordinal": 5, "primary_key_position": 0},
          {"name": "sha256", "normalized_type": "text", "nullable": true, "ordinal": 6, "primary_key_position": 0},
          {"name": "produced_by", "normalized_type": "text", "nullable": false, "ordinal": 7, "primary_key_position": 0},
          {"name": "approval_state", "normalized_type": "text", "nullable": false, "ordinal": 8, "primary_key_position": 0},
          {"name": "created_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 9, "primary_key_position": 0}
        ]
      },
      {
        "schema_name": "public",
        "table_name": "hermes_job_events",
        "columns": [
          {"name": "id", "normalized_type": "text", "nullable": false, "ordinal": 1, "primary_key_position": 1},
          {"name": "job_id", "normalized_type": "text", "nullable": false, "ordinal": 2, "primary_key_position": 0},
          {"name": "run_id", "normalized_type": "text", "nullable": true, "ordinal": 3, "primary_key_position": 0},
          {"name": "occurred_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 4, "primary_key_position": 0},
          {"name": "event_type", "normalized_type": "text", "nullable": false, "ordinal": 5, "primary_key_position": 0},
          {"name": "actor_type", "normalized_type": "text", "nullable": false, "ordinal": 6, "primary_key_position": 0},
          {"name": "actor_id", "normalized_type": "text", "nullable": false, "ordinal": 7, "primary_key_position": 0},
          {"name": "stage", "normalized_type": "text", "nullable": true, "ordinal": 8, "primary_key_position": 0},
          {"name": "payload", "normalized_type": "jsonb", "nullable": false, "ordinal": 9, "primary_key_position": 0}
        ]
      },
      {
        "schema_name": "public",
        "table_name": "hermes_job_runs",
        "columns": [
          {"name": "id", "normalized_type": "text", "nullable": false, "ordinal": 1, "primary_key_position": 1},
          {"name": "job_id", "normalized_type": "text", "nullable": false, "ordinal": 2, "primary_key_position": 0},
          {"name": "project", "normalized_type": "text", "nullable": false, "ordinal": 3, "primary_key_position": 0},
          {"name": "feature_id", "normalized_type": "text", "nullable": true, "ordinal": 4, "primary_key_position": 0},
          {"name": "status", "normalized_type": "text", "nullable": false, "ordinal": 5, "primary_key_position": 0},
          {"name": "current_stage", "normalized_type": "text", "nullable": false, "ordinal": 6, "primary_key_position": 0},
          {"name": "worker_id", "normalized_type": "text", "nullable": false, "ordinal": 7, "primary_key_position": 0},
          {"name": "worker_pool", "normalized_type": "text", "nullable": false, "ordinal": 8, "primary_key_position": 0},
          {"name": "host_class", "normalized_type": "text", "nullable": false, "ordinal": 9, "primary_key_position": 0},
          {"name": "container_id", "normalized_type": "text", "nullable": true, "ordinal": 10, "primary_key_position": 0},
          {"name": "auth_profile_id", "normalized_type": "text", "nullable": false, "ordinal": 11, "primary_key_position": 0},
          {"name": "auth_mode", "normalized_type": "text", "nullable": false, "ordinal": 12, "primary_key_position": 0},
          {"name": "provider_keys_used", "normalized_type": "bool", "nullable": false, "ordinal": 13, "primary_key_position": 0},
          {"name": "run_record", "normalized_type": "jsonb", "nullable": false, "ordinal": 14, "primary_key_position": 0},
          {"name": "started_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 15, "primary_key_position": 0},
          {"name": "completed_at", "normalized_type": "timestamptz", "nullable": true, "ordinal": 16, "primary_key_position": 0}
        ]
      },
      {
        "schema_name": "public",
        "table_name": "hermes_jobs",
        "columns": [
          {"name": "id", "normalized_type": "text", "nullable": false, "ordinal": 1, "primary_key_position": 1},
          {"name": "schema_version", "normalized_type": "int4", "nullable": false, "ordinal": 2, "primary_key_position": 0},
          {"name": "issued_by", "normalized_type": "text", "nullable": false, "ordinal": 3, "primary_key_position": 0},
          {"name": "job_type", "normalized_type": "text", "nullable": false, "ordinal": 4, "primary_key_position": 0},
          {"name": "project", "normalized_type": "text", "nullable": false, "ordinal": 5, "primary_key_position": 0},
          {"name": "feature_id", "normalized_type": "text", "nullable": true, "ordinal": 6, "primary_key_position": 0},
          {"name": "epic_id", "normalized_type": "text", "nullable": true, "ordinal": 7, "primary_key_position": 0},
          {"name": "repository_org", "normalized_type": "text", "nullable": false, "ordinal": 8, "primary_key_position": 0},
          {"name": "repository_name", "normalized_type": "text", "nullable": false, "ordinal": 9, "primary_key_position": 0},
          {"name": "repository_default_branch", "normalized_type": "text", "nullable": false, "ordinal": 10, "primary_key_position": 0},
          {"name": "orchestrator_path", "normalized_type": "text", "nullable": false, "ordinal": 11, "primary_key_position": 0},
          {"name": "routing_policy_path", "normalized_type": "text", "nullable": false, "ordinal": 12, "primary_key_position": 0},
          {"name": "auth_profile_id", "normalized_type": "text", "nullable": false, "ordinal": 13, "primary_key_position": 0},
          {"name": "auth_mode", "normalized_type": "text", "nullable": false, "ordinal": 14, "primary_key_position": 0},
          {"name": "status", "normalized_type": "text", "nullable": false, "ordinal": 15, "primary_key_position": 0},
          {"name": "envelope", "normalized_type": "jsonb", "nullable": false, "ordinal": 16, "primary_key_position": 0},
          {"name": "created_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 17, "primary_key_position": 0},
          {"name": "updated_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 18, "primary_key_position": 0}
        ]
      },
      {
        "schema_name": "public",
        "table_name": "hermes_profiles",
        "columns": [
          {"name": "id", "normalized_type": "text", "nullable": false, "ordinal": 1, "primary_key_position": 1},
          {"name": "role", "normalized_type": "text", "nullable": false, "ordinal": 2, "primary_key_position": 0},
          {"name": "home_group", "normalized_type": "text", "nullable": false, "ordinal": 3, "primary_key_position": 0},
          {"name": "metadata", "normalized_type": "jsonb", "nullable": false, "ordinal": 4, "primary_key_position": 0},
          {"name": "created_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 5, "primary_key_position": 0},
          {"name": "updated_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 6, "primary_key_position": 0}
        ]
      },
      {
        "schema_name": "public",
        "table_name": "hermes_traceability_edges",
        "columns": [
          {"name": "id", "normalized_type": "text", "nullable": false, "ordinal": 1, "primary_key_position": 1},
          {"name": "job_id", "normalized_type": "text", "nullable": true, "ordinal": 2, "primary_key_position": 0},
          {"name": "from_type", "normalized_type": "text", "nullable": false, "ordinal": 3, "primary_key_position": 0},
          {"name": "from_id", "normalized_type": "text", "nullable": false, "ordinal": 4, "primary_key_position": 0},
          {"name": "to_type", "normalized_type": "text", "nullable": false, "ordinal": 5, "primary_key_position": 0},
          {"name": "to_id", "normalized_type": "text", "nullable": false, "ordinal": 6, "primary_key_position": 0},
          {"name": "relation", "normalized_type": "text", "nullable": false, "ordinal": 7, "primary_key_position": 0},
          {"name": "created_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 8, "primary_key_position": 0}
        ]
      },
      {
        "schema_name": "public",
        "table_name": "hermes_workers",
        "columns": [
          {"name": "id", "normalized_type": "text", "nullable": false, "ordinal": 1, "primary_key_position": 1},
          {"name": "worker_pool", "normalized_type": "text", "nullable": false, "ordinal": 2, "primary_key_position": 0},
          {"name": "host_class", "normalized_type": "text", "nullable": false, "ordinal": 3, "primary_key_position": 0},
          {"name": "status", "normalized_type": "text", "nullable": false, "ordinal": 4, "primary_key_position": 0},
          {"name": "auth_profile_id", "normalized_type": "text", "nullable": false, "ordinal": 5, "primary_key_position": 0},
          {"name": "auth_mode", "normalized_type": "text", "nullable": false, "ordinal": 6, "primary_key_position": 0},
          {"name": "max_concurrent_jobs", "normalized_type": "int4", "nullable": false, "ordinal": 7, "primary_key_position": 0},
          {"name": "current_jobs", "normalized_type": "int4", "nullable": false, "ordinal": 8, "primary_key_position": 0},
          {"name": "capabilities", "normalized_type": "jsonb", "nullable": false, "ordinal": 9, "primary_key_position": 0},
          {"name": "metadata", "normalized_type": "jsonb", "nullable": false, "ordinal": 10, "primary_key_position": 0},
          {"name": "registered_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 11, "primary_key_position": 0},
          {"name": "last_seen_at", "normalized_type": "timestamptz", "nullable": false, "ordinal": 12, "primary_key_position": 0}
        ]
      }
    ]
  $catalog$::jsonb;
  observed_catalog jsonb;
begin
  observed_catalog := xfactory_runtime_v2.migration_source_catalog('public');
  if observed_catalog is distinct from expected_catalog then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-CATALOG: the connected database does not carry '
        'the exact pinned twelve-table v1 catalog from '
        'contracts/schemas/hermes-operational-postgres.sql';
  end if;
end
$catalog_assertions$;

-- freeze attachment and cutover observation run as the contract owner, which
-- does not own the v1 surface: grant it exactly the read, lock, and trigger
-- authority the governed cutover requires. write statements remain rejected
-- by the durable freeze trigger after cutover.
grant select, update, trigger on
  public.hermes_approval_requests,
  public.hermes_approvals,
  public.hermes_github_team_mappings,
  public.hermes_group_memberships,
  public.hermes_groups,
  public.hermes_job_artifacts,
  public.hermes_job_events,
  public.hermes_job_runs,
  public.hermes_jobs,
  public.hermes_profiles,
  public.hermes_traceability_edges,
  public.hermes_workers
to xfactory_v2_owner;

-- the migration session itself (a migrator-class login) must take the twelve
-- share row exclusive table locks as top-level statements before its
-- serializable snapshot is established: a lock acquired inside the cutover
-- function follows the snapshot and could omit a v1 write that committed
-- while the lock waited. postgresql requires update privilege for a
-- non-owner to lock at that strength (select is insufficient on both
-- supported majors), so this grant widening over the v1 surface is ratified
-- by us3 integration decision d11. write statements remain rejected by the
-- durable freeze trigger after cutover, and the migration protocol itself
-- never issues update.
grant update on
  public.hermes_approval_requests,
  public.hermes_approvals,
  public.hermes_github_team_mappings,
  public.hermes_group_memberships,
  public.hermes_groups,
  public.hermes_job_artifacts,
  public.hermes_job_events,
  public.hermes_job_runs,
  public.hermes_jobs,
  public.hermes_profiles,
  public.hermes_traceability_edges,
  public.hermes_workers
to xfactory_v2_migrator;

set role xfactory_v2_owner;
set search_path = pg_catalog, xfactory_runtime_v2;

create or replace function xfactory_runtime_v2.migration_catalog_entry(
  catalog jsonb,
  requested_table text
)
returns jsonb
language sql
immutable
strict
set search_path = pg_catalog
as $function$
  select entry.value
  from jsonb_array_elements(catalog) entry
  where entry.value->>'table_name' = requested_table
$function$;

create or replace function xfactory_runtime_v2.migration_attach_v1_freeze(
  requested_migration_id text
)
returns jsonb
language plpgsql
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
begin
  return xfactory_runtime_v2.install_v1_freeze(requested_migration_id);
end
$function$;

create or replace function xfactory_runtime_v2.migration_run_source_transforms(
  requested_installation_id text,
  requested_migration_id text,
  payload jsonb,
  observation jsonb
)
returns jsonb
language plpgsql
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  legacy_schema text := payload #>> '{source_identity,source_schema}';
  target_stack_id text := payload #>> '{target_topology,stack_id}';
  subject_mappings jsonb := payload->'subject_mappings';
  admin_mappings jsonb := payload->'admin_mappings';
  catalog_json jsonb := observation->'catalog';
  capture_time timestamptz := transaction_timestamp();
  admin_collection text;
  quarantine_table text;
  quarantine_reason text;
  history_table text;
  table_entry jsonb;
  table_key text;
  input_count bigint;
  history_count bigint;
  row_quarantine_count bigint;
  total_history bigint := 0;
  total_quarantine bigint := 0;
  per_table jsonb := '{}'::jsonb;
begin
  if legacy_schema is distinct from 'public'
     or jsonb_typeof(subject_mappings) <> 'array'
     or jsonb_typeof(admin_mappings) <> 'object'
     or jsonb_typeof(catalog_json) <> 'array' then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-STAGING-SHAPE: the transforms require the '
        'public v1 schema, subject and admin mappings, and an observed '
        'catalog';
  end if;

  -- a legacy project may map to at most one customer layer, exactly once.
  if exists (
    select 1
    from jsonb_array_elements(subject_mappings) entry
    group by entry.value->>'legacy_project'
    having count(*) > 1
  ) then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-AMBIGUOUS-SCOPE: a legacy project value maps '
        'to more than one customer layer';
  end if;

  -- admin mappings must name each source primary key at most once and use
  -- the closed scope vocabulary.
  foreach admin_collection in array array['workers', 'groups', 'profiles']
  loop
    if exists (
      select 1
      from jsonb_array_elements(admin_mappings->admin_collection) entry
      group by entry.value->>'source_pk'
      having count(*) > 1
    ) then
      raise exception using
        errcode = '55000',
        message = format(
          'HGR-MIGRATION-AMBIGUOUS-SCOPE: admin_mappings.%s maps a source '
          'primary key more than once',
          admin_collection
        );
    end if;
    if exists (
      select 1
      from jsonb_array_elements(admin_mappings->admin_collection) entry
      where entry.value->>'scope_kind' not in ('layer', 'installation_admin')
        or (
          entry.value->>'scope_kind' = 'layer'
          and coalesce(entry.value->>'layer_id', '') = ''
        )
    ) then
      raise exception using
        errcode = '55000',
        message = format(
          'HGR-MIGRATION-AMBIGUOUS-SCOPE: admin_mappings.%s carries an '
          'unusable scope',
          admin_collection
        );
    end if;
  end loop;

  -- every subject mapping must target a declared customer layer and every
  -- mapped layer must be a registered layer of the target stack.
  if exists (
    select 1
    from jsonb_array_elements(subject_mappings) entry
    where not (
      payload->'target_topology'->'customer_layer_ids'
        ? (entry.value->>'layer_id')
    )
  ) then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-TARGET-LAYER: subject mappings must target '
        'declared customer layers';
  end if;
  if exists (
    select mapped.layer_id
    from (
      select entry.value->>'layer_id' as layer_id
      from jsonb_array_elements(subject_mappings) entry
      union all
      select entry.value->>'layer_id'
      from jsonb_array_elements(admin_mappings->'workers') entry
      where entry.value->>'scope_kind' = 'layer'
      union all
      select entry.value->>'layer_id'
      from jsonb_array_elements(admin_mappings->'groups') entry
      where entry.value->>'scope_kind' = 'layer'
      union all
      select entry.value->>'layer_id'
      from jsonb_array_elements(admin_mappings->'profiles') entry
      where entry.value->>'scope_kind' = 'layer'
    ) mapped
    where not exists (
      select 1
      from xfactory_runtime_v2.layer_registrations registration
      where registration.installation_id = requested_installation_id
        and registration.stack_id = target_stack_id
        and registration.layer_id = mapped.layer_id
    )
  ) then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-TARGET-LAYER: every mapped layer must be a '
        'registered layer of the target stack';
  end if;

  -- single-default proof: legal only when the observed distinct project
  -- values across jobs and runs are exactly the one mapped value.
  if jsonb_typeof(payload->'single_default_mapping') = 'object'
     and (payload #>> '{single_default_mapping,enabled}')::boolean then
    if not exists (select 1 from public.hermes_jobs)
       or exists (
         select 1
         from (
           select jobs.project from public.hermes_jobs jobs
           union
           select runs.project from public.hermes_job_runs runs
         ) observed
         where observed.project is distinct from
           (payload #>> '{single_default_mapping,legacy_project}')
       ) then
      raise exception using
        errcode = '55000',
        message = 'HGR-MIGRATION-DEFAULT-MAPPING: single_default_mapping '
          'requires exactly one observed legacy project equal to the mapped '
          'value';
    end if;
  end if;

  -- jobs classify through subject mappings on their own project value; any
  -- unmapped governed row aborts the whole transaction.
  if exists (
    select 1
    from public.hermes_jobs jobs
    where not exists (
      select 1
      from jsonb_array_elements(subject_mappings) entry
      where entry.value->>'legacy_project' = jobs.project
    )
  ) then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-UNMAPPED-ROW: a hermes_jobs row carries a '
        'legacy project with no subject mapping';
  end if;

  -- runs and events inherit scope only through verified job ancestry.
  if exists (
    select 1
    from public.hermes_job_runs runs
    join public.hermes_jobs jobs on jobs.id = runs.job_id
    where runs.project is distinct from jobs.project
  ) then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-ANCESTRY-CONFLICT: a hermes_job_runs row '
        'disagrees with its ancestor job project';
  end if;
  if exists (
    select 1
    from public.hermes_job_events events
    join public.hermes_job_runs runs on runs.id = events.run_id
    where events.run_id is not null
      and runs.job_id is distinct from events.job_id
  ) then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-ANCESTRY-CONFLICT: a hermes_job_events row '
        'cites a run that belongs to a different job';
  end if;

  -- workers, groups, and profiles require explicit per-source-pk mappings.
  if exists (
    select 1
    from xfactory_runtime_v2.migration_source_rows(
      legacy_schema,
      xfactory_runtime_v2.migration_catalog_entry(catalog_json, 'hermes_workers')
    ) rows
    where not exists (
      select 1
      from jsonb_array_elements(admin_mappings->'workers') entry
      where entry.value->>'source_pk' = rows.source_pk
    )
  ) then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-UNMAPPED-ROW: a hermes_workers row has no '
        'explicit admin mapping';
  end if;
  if exists (
    select 1
    from xfactory_runtime_v2.migration_source_rows(
      legacy_schema,
      xfactory_runtime_v2.migration_catalog_entry(catalog_json, 'hermes_groups')
    ) rows
    where not exists (
      select 1
      from jsonb_array_elements(admin_mappings->'groups') entry
      where entry.value->>'source_pk' = rows.source_pk
    )
  ) then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-UNMAPPED-ROW: a hermes_groups row has no '
        'explicit admin mapping';
  end if;
  if exists (
    select 1
    from xfactory_runtime_v2.migration_source_rows(
      legacy_schema,
      xfactory_runtime_v2.migration_catalog_entry(catalog_json, 'hermes_profiles')
    ) rows
    where not exists (
      select 1
      from jsonb_array_elements(admin_mappings->'profiles') entry
      where entry.value->>'source_pk' = rows.source_pk
    )
  ) then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-UNMAPPED-ROW: a hermes_profiles row has no '
        'explicit admin mapping';
  end if;

  -- memberships and github team mappings inherit only when every endpoint
  -- maps and all endpoints agree on one scope.
  if exists (
    select 1
    from public.hermes_group_memberships memberships
    left join lateral (
      select entry.value->>'scope_kind' as scope_kind,
        entry.value->>'layer_id' as layer_id
      from jsonb_array_elements(admin_mappings->'profiles') entry
      where entry.value->>'source_pk' =
        xfactory_runtime_v2.migration_canonical_json_value(
          to_jsonb(array[memberships.profile_id])
        )
    ) profile_scope on true
    left join lateral (
      select entry.value->>'scope_kind' as scope_kind,
        entry.value->>'layer_id' as layer_id
      from jsonb_array_elements(admin_mappings->'groups') entry
      where entry.value->>'source_pk' =
        xfactory_runtime_v2.migration_canonical_json_value(
          to_jsonb(array[memberships.group_id])
        )
    ) group_scope on true
    where profile_scope.scope_kind is null
      or group_scope.scope_kind is null
      or profile_scope.scope_kind is distinct from group_scope.scope_kind
      or profile_scope.layer_id is distinct from group_scope.layer_id
  ) then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-ENDPOINT-SCOPE: a hermes_group_memberships row '
        'has an unmapped endpoint or endpoints that disagree on one scope';
  end if;
  if exists (
    select 1
    from public.hermes_github_team_mappings team_mappings
    where not exists (
      select 1
      from jsonb_array_elements(admin_mappings->'groups') entry
      where entry.value->>'source_pk' =
        xfactory_runtime_v2.migration_canonical_json_value(
          to_jsonb(array[team_mappings.group_id])
        )
    )
  ) then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-ENDPOINT-SCOPE: a hermes_github_team_mappings '
        'row cites a group with no explicit admin mapping';
  end if;

  -- compatibility-history migration: jobs.
  insert into xfactory_runtime_v2.legacy_jobs (
    migration_id, source_schema, source_table, source_pk, source_row_digest,
    source_row, scope_kind, installation_id, stack_id, layer_id, captured_at
  )
  select
    requested_migration_id, legacy_schema, 'hermes_jobs', rows.source_pk,
    rows.source_row_digest, rows.source_row, 'layer',
    requested_installation_id, target_stack_id, mapping.layer_id, capture_time
  from xfactory_runtime_v2.migration_source_rows(
    legacy_schema,
    xfactory_runtime_v2.migration_catalog_entry(catalog_json, 'hermes_jobs')
  ) rows
  join lateral (
    select entry.value->>'layer_id' as layer_id
    from jsonb_array_elements(subject_mappings) entry
    where entry.value->>'legacy_project' = rows.source_row->>'project'
  ) mapping on true;

  -- compatibility-history migration: runs inherit their job scope.
  insert into xfactory_runtime_v2.legacy_job_runs (
    migration_id, source_schema, source_table, source_pk, source_row_digest,
    source_row, scope_kind, installation_id, stack_id, layer_id, captured_at
  )
  select
    requested_migration_id, legacy_schema, 'hermes_job_runs', rows.source_pk,
    rows.source_row_digest, rows.source_row, 'layer',
    requested_installation_id, target_stack_id, mapping.layer_id, capture_time
  from xfactory_runtime_v2.migration_source_rows(
    legacy_schema,
    xfactory_runtime_v2.migration_catalog_entry(catalog_json, 'hermes_job_runs')
  ) rows
  join public.hermes_jobs ancestor
    on ancestor.id = rows.source_row->>'job_id'
  join lateral (
    select entry.value->>'layer_id' as layer_id
    from jsonb_array_elements(subject_mappings) entry
    where entry.value->>'legacy_project' = ancestor.project
  ) mapping on true;

  -- compatibility-history migration: events inherit their job scope.
  insert into xfactory_runtime_v2.legacy_job_events (
    migration_id, source_schema, source_table, source_pk, source_row_digest,
    source_row, scope_kind, installation_id, stack_id, layer_id, captured_at
  )
  select
    requested_migration_id, legacy_schema, 'hermes_job_events', rows.source_pk,
    rows.source_row_digest, rows.source_row, 'layer',
    requested_installation_id, target_stack_id, mapping.layer_id, capture_time
  from xfactory_runtime_v2.migration_source_rows(
    legacy_schema,
    xfactory_runtime_v2.migration_catalog_entry(catalog_json, 'hermes_job_events')
  ) rows
  join public.hermes_jobs ancestor
    on ancestor.id = rows.source_row->>'job_id'
  join lateral (
    select entry.value->>'layer_id' as layer_id
    from jsonb_array_elements(subject_mappings) entry
    where entry.value->>'legacy_project' = ancestor.project
  ) mapping on true;

  -- compatibility-history migration: workers, groups, and profiles use their
  -- explicit layer or installation-administration mappings.
  insert into xfactory_runtime_v2.legacy_workers (
    migration_id, source_schema, source_table, source_pk, source_row_digest,
    source_row, scope_kind, installation_id, stack_id, layer_id, captured_at
  )
  select
    requested_migration_id, legacy_schema, 'hermes_workers', rows.source_pk,
    rows.source_row_digest, rows.source_row, mapping.scope_kind,
    requested_installation_id,
    case when mapping.scope_kind = 'layer' then target_stack_id end,
    case when mapping.scope_kind = 'layer' then mapping.layer_id end,
    capture_time
  from xfactory_runtime_v2.migration_source_rows(
    legacy_schema,
    xfactory_runtime_v2.migration_catalog_entry(catalog_json, 'hermes_workers')
  ) rows
  join lateral (
    select entry.value->>'scope_kind' as scope_kind,
      entry.value->>'layer_id' as layer_id
    from jsonb_array_elements(admin_mappings->'workers') entry
    where entry.value->>'source_pk' = rows.source_pk
  ) mapping on true;

  insert into xfactory_runtime_v2.legacy_groups (
    migration_id, source_schema, source_table, source_pk, source_row_digest,
    source_row, scope_kind, installation_id, stack_id, layer_id, captured_at
  )
  select
    requested_migration_id, legacy_schema, 'hermes_groups', rows.source_pk,
    rows.source_row_digest, rows.source_row, mapping.scope_kind,
    requested_installation_id,
    case when mapping.scope_kind = 'layer' then target_stack_id end,
    case when mapping.scope_kind = 'layer' then mapping.layer_id end,
    capture_time
  from xfactory_runtime_v2.migration_source_rows(
    legacy_schema,
    xfactory_runtime_v2.migration_catalog_entry(catalog_json, 'hermes_groups')
  ) rows
  join lateral (
    select entry.value->>'scope_kind' as scope_kind,
      entry.value->>'layer_id' as layer_id
    from jsonb_array_elements(admin_mappings->'groups') entry
    where entry.value->>'source_pk' = rows.source_pk
  ) mapping on true;

  insert into xfactory_runtime_v2.legacy_profiles (
    migration_id, source_schema, source_table, source_pk, source_row_digest,
    source_row, scope_kind, installation_id, stack_id, layer_id, captured_at
  )
  select
    requested_migration_id, legacy_schema, 'hermes_profiles', rows.source_pk,
    rows.source_row_digest, rows.source_row, mapping.scope_kind,
    requested_installation_id,
    case when mapping.scope_kind = 'layer' then target_stack_id end,
    case when mapping.scope_kind = 'layer' then mapping.layer_id end,
    capture_time
  from xfactory_runtime_v2.migration_source_rows(
    legacy_schema,
    xfactory_runtime_v2.migration_catalog_entry(catalog_json, 'hermes_profiles')
  ) rows
  join lateral (
    select entry.value->>'scope_kind' as scope_kind,
      entry.value->>'layer_id' as layer_id
    from jsonb_array_elements(admin_mappings->'profiles') entry
    where entry.value->>'source_pk' = rows.source_pk
  ) mapping on true;

  -- compatibility-history migration: memberships carry the one scope their
  -- verified endpoints agree on.
  insert into xfactory_runtime_v2.legacy_group_memberships (
    migration_id, source_schema, source_table, source_pk, source_row_digest,
    source_row, scope_kind, installation_id, stack_id, layer_id, captured_at
  )
  select
    requested_migration_id, legacy_schema, 'hermes_group_memberships',
    rows.source_pk, rows.source_row_digest, rows.source_row,
    profile_scope.scope_kind, requested_installation_id,
    case when profile_scope.scope_kind = 'layer' then target_stack_id end,
    case when profile_scope.scope_kind = 'layer' then profile_scope.layer_id end,
    capture_time
  from xfactory_runtime_v2.migration_source_rows(
    legacy_schema,
    xfactory_runtime_v2.migration_catalog_entry(
      catalog_json, 'hermes_group_memberships'
    )
  ) rows
  join lateral (
    select entry.value->>'scope_kind' as scope_kind,
      entry.value->>'layer_id' as layer_id
    from jsonb_array_elements(admin_mappings->'profiles') entry
    where entry.value->>'source_pk' =
      xfactory_runtime_v2.migration_canonical_json_value(
        to_jsonb(array[rows.pk_values[1]])
      )
  ) profile_scope on true
  join lateral (
    select entry.value->>'scope_kind' as scope_kind,
      entry.value->>'layer_id' as layer_id
    from jsonb_array_elements(admin_mappings->'groups') entry
    where entry.value->>'source_pk' =
      xfactory_runtime_v2.migration_canonical_json_value(
        to_jsonb(array[rows.pk_values[2]])
      )
  ) group_scope on true
  where profile_scope.scope_kind = group_scope.scope_kind
    and profile_scope.layer_id is not distinct from group_scope.layer_id;

  -- compatibility-history migration: github team mappings inherit their
  -- group endpoint scope.
  insert into xfactory_runtime_v2.legacy_github_team_mappings (
    migration_id, source_schema, source_table, source_pk, source_row_digest,
    source_row, scope_kind, installation_id, stack_id, layer_id, captured_at
  )
  select
    requested_migration_id, legacy_schema, 'hermes_github_team_mappings',
    rows.source_pk, rows.source_row_digest, rows.source_row,
    group_scope.scope_kind, requested_installation_id,
    case when group_scope.scope_kind = 'layer' then target_stack_id end,
    case when group_scope.scope_kind = 'layer' then group_scope.layer_id end,
    capture_time
  from xfactory_runtime_v2.migration_source_rows(
    legacy_schema,
    xfactory_runtime_v2.migration_catalog_entry(
      catalog_json, 'hermes_github_team_mappings'
    )
  ) rows
  join lateral (
    select entry.value->>'scope_kind' as scope_kind,
      entry.value->>'layer_id' as layer_id
    from jsonb_array_elements(admin_mappings->'groups') entry
    where entry.value->>'source_pk' =
      xfactory_runtime_v2.migration_canonical_json_value(
        to_jsonb(array[rows.pk_values[1]])
      )
  ) group_scope on true;

  -- fixed quarantine classification: unverifiable artifact, approval-request,
  -- approval, and trace rows enter only the sealed quarantine table.
  for quarantine_table, quarantine_reason in
    select classification.source_table, classification.reason_code
    from (
      values
        ('hermes_job_artifacts', 'missing_content_digest'),
        ('hermes_approval_requests', 'missing_target_digest'),
        ('hermes_approvals', 'missing_reviewer_authority'),
        ('hermes_traceability_edges', 'missing_binding_evidence')
    ) classification(source_table, reason_code)
  loop
    insert into xfactory_legacy_quarantine_v2.legacy_quarantine_records (
      migration_id, source_schema, source_table, source_pk, source_row_digest,
      reason_code, source_row, captured_at
    )
    select
      requested_migration_id, legacy_schema, quarantine_table, rows.source_pk,
      rows.source_row_digest, quarantine_reason, rows.source_row, capture_time
    from xfactory_runtime_v2.migration_source_rows(
      legacy_schema,
      xfactory_runtime_v2.migration_catalog_entry(
        catalog_json, quarantine_table
      )
    ) rows;
  end loop;

  -- exactly-once reconciliation over all twelve canonical tables.
  for table_entry in
    select entry.value
    from jsonb_array_elements(catalog_json) entry
    order by convert_to(entry.value->>'schema_name', 'UTF8'),
      convert_to(entry.value->>'table_name', 'UTF8')
  loop
    table_key := (table_entry->>'schema_name') || '.'
      || (table_entry->>'table_name');
    input_count := (observation->'table_row_counts'->>table_key)::bigint;
    history_table := case table_entry->>'table_name'
      when 'hermes_jobs' then 'legacy_jobs'
      when 'hermes_job_runs' then 'legacy_job_runs'
      when 'hermes_job_events' then 'legacy_job_events'
      when 'hermes_workers' then 'legacy_workers'
      when 'hermes_groups' then 'legacy_groups'
      when 'hermes_profiles' then 'legacy_profiles'
      when 'hermes_group_memberships' then 'legacy_group_memberships'
      when 'hermes_github_team_mappings' then 'legacy_github_team_mappings'
      else null
    end;
    if history_table is not null then
      execute format(
        'select count(*) from xfactory_runtime_v2.%I where migration_id = $1 '
        'and source_schema = $2 and source_table = $3',
        history_table
      )
      into history_count
      using requested_migration_id, legacy_schema,
        table_entry->>'table_name';
    else
      history_count := 0;
    end if;
    select count(*)
    into row_quarantine_count
    from xfactory_legacy_quarantine_v2.legacy_quarantine_records quarantined
    where quarantined.migration_id = requested_migration_id
      and quarantined.source_schema = legacy_schema
      and quarantined.source_table = table_entry->>'table_name';
    if history_count + row_quarantine_count <> input_count
       or (history_table is not null and row_quarantine_count <> 0)
       or (history_table is null and history_count <> 0) then
      raise exception using
        errcode = '55000',
        message = format(
          'HGR-MIGRATION-RECONCILIATION: %s reconciles %s compatibility '
          'history and %s quarantine rows against %s source rows',
          table_key, history_count, row_quarantine_count, input_count
        );
    end if;
    per_table := per_table || jsonb_build_object(
      table_key,
      jsonb_build_object(
        'input_count', input_count,
        'table_frame_digest', observation->'per_table_digests'->>table_key,
        'compatibility_history', history_count,
        'quarantine', row_quarantine_count
      )
    );
    total_history := total_history + history_count;
    total_quarantine := total_quarantine + row_quarantine_count;
  end loop;

  return jsonb_build_object(
    'per_table', per_table,
    'compatibility_history_count', total_history,
    'quarantine_count', total_quarantine
  );
end
$function$;

reset role;
