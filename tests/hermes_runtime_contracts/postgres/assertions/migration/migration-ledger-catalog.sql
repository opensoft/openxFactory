-- Migration ledger structural catalog: the staging/attempt/event/observation/
-- reconciliation tables, the eight scoped legacy_* compatibility-history
-- tables, their immutability triggers, forced row security, and the
-- migrator-facing governed API functions all exist exactly as pinned.
SELECT count(*) = 23
       AND bool_and(present)
FROM (
  SELECT expected.name,
         CASE expected.kind
           WHEN 'table' THEN to_regclass('xfactory_runtime_v2.' || expected.name)
             IS NOT NULL
           WHEN 'immutable_trigger' THEN EXISTS (
             SELECT 1
             FROM pg_trigger trg
             WHERE trg.tgrelid = to_regclass('xfactory_runtime_v2.'
               || replace(expected.name, '_immutable', ''))
               AND trg.tgname = expected.name
               AND NOT trg.tgisinternal
           )
           WHEN 'forced_rls' THEN EXISTS (
             SELECT 1
             FROM pg_class cls
             JOIN pg_namespace ns ON ns.oid = cls.relnamespace
             WHERE ns.nspname = 'xfactory_runtime_v2'
               AND cls.relname = expected.name
               AND cls.relrowsecurity
               AND cls.relforcerowsecurity
           ) AND EXISTS (
             SELECT 1
             FROM pg_policies pol
             WHERE pol.schemaname = 'xfactory_runtime_v2'
               AND pol.tablename = expected.name
               AND pol.policyname = expected.name || '_exact_scope'
           )
           WHEN 'api_function' THEN EXISTS (
             SELECT 1
             FROM pg_proc proc
             JOIN pg_namespace ns ON ns.oid = proc.pronamespace
             WHERE ns.nspname = 'xfactory_runtime_api_v2'
               AND proc.proname = expected.name
               AND proc.prosecdef
           )
         END AS present
  FROM (
    VALUES
      ('migration_staging', 'table'),
      ('migration_attempts', 'table'),
      ('migration_attempt_events', 'table'),
      ('migration_cutover_observations', 'table'),
      ('migration_reconciliations', 'table'),
      ('migration_staging_immutable', 'immutable_trigger'),
      ('migration_attempts_immutable', 'immutable_trigger'),
      ('migration_attempt_events_immutable', 'immutable_trigger'),
      ('migration_cutover_observations_immutable', 'immutable_trigger'),
      ('migration_reconciliations_immutable', 'immutable_trigger'),
      ('legacy_jobs', 'forced_rls'),
      ('legacy_job_runs', 'forced_rls'),
      ('legacy_job_events', 'forced_rls'),
      ('legacy_workers', 'forced_rls'),
      ('legacy_groups', 'forced_rls'),
      ('legacy_profiles', 'forced_rls'),
      ('legacy_group_memberships', 'forced_rls'),
      ('legacy_github_team_mappings', 'forced_rls'),
      ('stage_migration', 'api_function'),
      ('begin_migration_attempt', 'api_function'),
      ('execute_v1_cutover', 'api_function'),
      ('fail_migration_attempt', 'api_function'),
      ('migration_result', 'api_function')
  ) AS expected (name, kind)
) checks;
