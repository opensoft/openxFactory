-- Hermes operational state for Omnigent integration.
-- This database stores job status, events, approvals, artifacts, and traceability
-- indexes. It must never store credential material, OAuth tokens, or API keys.

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
    status in (
      'queued',
      'running',
      'waiting_for_approval',
      'approved',
      'blocked',
      'failed',
      'complete',
      'cancelled'
    )
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

create index if not exists hermes_job_events_job_time_idx
  on hermes_job_events(job_id, occurred_at);

create index if not exists hermes_job_runs_job_idx
  on hermes_job_runs(job_id);

create index if not exists hermes_traceability_from_idx
  on hermes_traceability_edges(from_type, from_id);

create index if not exists hermes_traceability_to_idx
  on hermes_traceability_edges(to_type, to_id);

create index if not exists hermes_workers_pool_status_idx
  on hermes_workers(worker_pool, status);

create index if not exists hermes_group_memberships_group_idx
  on hermes_group_memberships(group_id);
