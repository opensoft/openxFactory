\set ON_ERROR_STOP on

-- Deterministic two-subject v1 seed: every canonical table carries rows,
-- legacy projects project-alfa and project-beta both appear across jobs
-- and runs, and the values exercise nulls, non-ASCII text, canonical
-- JSON key sorting/escapes (including a real newline), booleans, int4
-- values, composite primary keys, and fixed microsecond timestamps.
-- Value-for-value mirror: v1-two-subject-dataset.yaml.

INSERT INTO public.hermes_groups (
  id, purpose, agents, metadata, created_at, updated_at
) VALUES
  ('group-ops', 'operations', '[]', '{"note": "line1\nline2"}', '2026-07-01T00:00:00.000000Z', '2026-07-01T00:00:01.000000Z'),
  ('group-core', 'orchestration', '["agent-a", "agent-b"]', '{"labels": {"a": "alpha", "β": "beta"}, "tier": 1}', '2026-07-01T00:00:00.000000Z', '2026-07-01T00:00:00.000000Z'),
  ('group-übersicht', 'beobachtung', '["agent-ü"]', '{}', '2026-07-01T00:00:01.000000Z', '2026-07-01T08:30:00.123456Z');

INSERT INTO public.hermes_profiles (
  id, role, home_group, metadata, created_at, updated_at
) VALUES
  ('profile-bob', 'reviewer', 'group-ops', '{}', '2026-07-01T00:00:01.000000Z', '2026-07-01T00:00:01.000000Z'),
  ('profile-anna', 'engineer', 'group-core', '{"quote": "she said \"hi\""}', '2026-07-01T00:00:00.000000Z', '2026-07-01T00:00:00.000000Z'),
  ('profile-cära', 'operator', 'group-übersicht', '{"backslash": "a\\b"}', '2026-07-01T00:00:01.000000Z', '2026-07-01T08:30:00.123456Z');

INSERT INTO public.hermes_group_memberships (
  profile_id, group_id, membership_type, created_at
) VALUES
  ('profile-bob', 'group-ops', 'owner', '2026-07-01T00:00:02.000000Z'),
  ('profile-anna', 'group-core', 'member', '2026-07-01T00:00:00.000000Z'),
  ('profile-bob', 'group-core', 'member', '2026-07-01T00:00:01.000000Z'),
  ('profile-cära', 'group-übersicht', 'member', '2026-07-01T00:00:02.000000Z'),
  ('profile-anna', 'group-ops', 'observer', '2026-07-01T00:00:01.000000Z');

INSERT INTO public.hermes_github_team_mappings (
  group_id, github_team, created_at, updated_at
) VALUES
  ('group-ops', 'opensoft/team-ops', '2026-07-01T00:00:00.000000Z', '2026-07-01T00:00:02.000000Z'),
  ('group-core', 'opensoft/team-core', '2026-07-01T00:00:00.000000Z', '2026-07-01T00:00:00.000000Z');

INSERT INTO public.hermes_workers (
  id, worker_pool, host_class, status, auth_profile_id, auth_mode,
  max_concurrent_jobs, current_jobs, capabilities, metadata, registered_at, last_seen_at
) VALUES
  ('worker-02', 'pool-beta', 'gpu', 'busy', 'auth-profile-02', 'api', 1, 1, '[]', '{"gpu": true, "memory_gb": 16}', '2026-07-01T00:00:01.000000Z', '2026-07-01T08:30:00.123456Z'),
  ('worker-01', 'pool-alpha', 'standard', 'idle', 'auth-profile-01', 'subscription', 3, 0, '["build", "test"]', '{}', '2026-07-01T00:00:00.000000Z', '2026-07-01T00:00:01.000000Z');

INSERT INTO public.hermes_jobs (
  id, schema_version, issued_by, job_type, project, feature_id,
  epic_id, repository_org, repository_name, repository_default_branch, orchestrator_path, routing_policy_path,
  auth_profile_id, auth_mode, status, envelope, created_at, updated_at
) VALUES
  ('job-beta-01', 2, 'Hermes', 'deploy', 'project-beta', 'feat-b-1', NULL, 'opensoft', 'repo-β', 'release', 'orchestrators/deploy.yaml', 'policies/routing.yaml', 'auth-profile-02', 'mixed', 'failed', '{"note": "line1\nline2", "when": {"retries": 0}}', '2026-07-01T00:00:02.000000Z', '2026-07-01T08:30:00.123456Z'),
  ('job-alfa-01', 1, 'Hermes', 'build', 'project-alfa', 'feat-α-1', NULL, 'opensoft', 'repo-alfa', 'main', 'orchestrators/build.yaml', 'policies/routing.yaml', 'auth-profile-01', 'subscription', 'complete', '{"labels": {"tier": "gold", "α": "one"}, "steps": ["plan", "build"]}', '2026-07-01T00:00:00.000000Z', '2026-07-01T00:00:01.000000Z'),
  ('job-alfa-02', 1, 'Hermes', 'test', 'project-alfa', NULL, 'epic-9', 'opensoft', 'repo-alfa', 'main', 'orchestrators/test.yaml', 'policies/routing.yaml', 'auth-profile-01', 'api', 'queued', '{}', '2026-07-01T00:00:01.000000Z', '2026-07-01T00:00:01.000000Z');

INSERT INTO public.hermes_job_runs (
  id, job_id, project, feature_id, status, current_stage,
  worker_id, worker_pool, host_class, container_id, auth_profile_id, auth_mode,
  provider_keys_used, run_record, started_at, completed_at
) VALUES
  ('run-beta-01-a', 'job-beta-01', 'project-beta', 'feat-b-1', 'failed', 'deploy', 'worker-02', 'pool-beta', 'gpu', 'container-β', 'auth-profile-02', 'mixed', true, '{"exit": 1, "stderr": "boom"}', '2026-07-01T00:00:02.000000Z', '2026-07-01T08:30:00.123456Z'),
  ('run-alfa-01-a', 'job-alfa-01', 'project-alfa', 'feat-α-1', 'complete', 'done', 'worker-01', 'pool-alpha', 'standard', 'container-01', 'auth-profile-01', 'subscription', false, '{"exit": 0}', '2026-07-01T00:00:00.000000Z', '2026-07-01T00:00:01.000000Z'),
  ('run-alfa-02-a', 'job-alfa-02', 'project-alfa', NULL, 'queued', 'pending', 'worker-01', 'pool-alpha', 'standard', NULL, 'auth-profile-01', 'api', false, '{}', '2026-07-01T00:00:01.000000Z', NULL);

INSERT INTO public.hermes_job_events (
  id, job_id, run_id, occurred_at, event_type, actor_type,
  actor_id, stage, payload
) VALUES
  ('event-02', 'job-alfa-01', NULL, '2026-07-01T00:00:01.000000Z', 'job_completed', 'system', 'hermes', NULL, '{}'),
  ('event-01', 'job-alfa-01', 'run-alfa-01-a', '2026-07-01T00:00:00.000000Z', 'stage_completed', 'agent', 'agent-a', 'build', '{"ok": true}'),
  ('event-03', 'job-beta-01', 'run-beta-01-a', '2026-07-01T08:30:00.123456Z', 'stage_failed', 'agent', 'agent-β', 'deploy', '{"error": "נכשל"}');

INSERT INTO public.hermes_job_artifacts (
  id, job_id, run_id, artifact_type, path, sha256,
  produced_by, approval_state, created_at
) VALUES
  ('artifact-02', 'job-beta-01', NULL, 'log', 'artifacts/deploy.log', NULL, 'agent-β', 'pending', '2026-07-01T08:30:00.123456Z'),
  ('artifact-01', 'job-alfa-01', 'run-alfa-01-a', 'report', 'artifacts/report.md', '1f2e3d4c5b6a79880123456789abcdef0123456789abcdef0123456789abcdef', 'agent-a', 'approved', '2026-07-01T00:00:01.000000Z');

INSERT INTO public.hermes_approval_requests (
  id, job_id, run_id, requested_by, approval_type, status,
  artifact_id, created_at, resolved_at
) VALUES
  ('request-02', 'job-beta-01', NULL, 'agent-β', 'stage_gate', 'pending', NULL, '2026-07-01T08:30:00.123456Z', NULL),
  ('request-01', 'job-alfa-01', 'run-alfa-01-a', 'agent-a', 'artifact_release', 'approved', 'artifact-01', '2026-07-01T00:00:01.000000Z', '2026-07-01T00:00:02.000000Z');

INSERT INTO public.hermes_approvals (
  id, approval_request_id, job_id, actor_type, actor_id, decision,
  authority_scope, rationale, created_at
) VALUES
  ('approval-02', 'request-01', 'job-alfa-01', 'human', 'reviewer-two', 'changes_requested', NULL, NULL, '2026-07-01T00:00:02.000000Z'),
  ('approval-01', 'request-01', 'job-alfa-01', 'human', 'reviewer-lead', 'approved', 'project-lead', 'looks good', '2026-07-01T00:00:02.000000Z');

INSERT INTO public.hermes_traceability_edges (
  id, job_id, from_type, from_id, to_type, to_id,
  relation, created_at
) VALUES
  ('edge-02', NULL, 'spec', 'spec-α', 'job', 'job-beta-01', 'implements', '2026-07-01T08:30:00.123456Z'),
  ('edge-01', 'job-alfa-01', 'job', 'job-alfa-01', 'artifact', 'artifact-01', 'produced', '2026-07-01T00:00:01.000000Z');
