-- Durable v1 write-freeze catalog: every one of the twelve canonical
-- public.hermes_* tables carries the hermes_v1_freeze_write trigger bound to
-- xfactory_runtime_v2.reject_frozen_v1_write. Meaningful after a successful
-- cutover (and after crash recovery, because the trigger is catalog-durable).
SELECT count(*) = 12
       AND bool_and(frozen)
FROM (
  SELECT expected.table_name,
         EXISTS (
           SELECT 1
           FROM pg_trigger trg
           JOIN pg_proc proc ON proc.oid = trg.tgfoid
           JOIN pg_namespace proc_ns ON proc_ns.oid = proc.pronamespace
           WHERE trg.tgrelid = to_regclass('public.' || expected.table_name)
             AND trg.tgname = 'hermes_v1_freeze_write'
             AND NOT trg.tgisinternal
             AND proc_ns.nspname = 'xfactory_runtime_v2'
             AND proc.proname = 'reject_frozen_v1_write'
         ) AS frozen
  FROM (
    VALUES
      ('hermes_approval_requests'),
      ('hermes_approvals'),
      ('hermes_github_team_mappings'),
      ('hermes_group_memberships'),
      ('hermes_groups'),
      ('hermes_job_artifacts'),
      ('hermes_job_events'),
      ('hermes_job_runs'),
      ('hermes_jobs'),
      ('hermes_profiles'),
      ('hermes_traceability_edges'),
      ('hermes_workers')
  ) AS expected (table_name)
) checks;
