-- Quarantine boundary catalog: the sealed schema exists with its single
-- immutable record table, no usage or table privileges reach the runtime,
-- control, audit, or migrator role classes, PUBLIC holds nothing, and the
-- quarantine dependency guard event trigger is installed and enabled.
SELECT count(*) = 12
       AND bool_and(holds)
FROM (
  VALUES
    ('schema-exists', EXISTS (
      SELECT 1 FROM pg_namespace
      WHERE nspname = 'xfactory_legacy_quarantine_v2'
    )),
    ('table-exists', to_regclass(
      'xfactory_legacy_quarantine_v2.legacy_quarantine_records') IS NOT NULL),
    ('immutable-trigger', EXISTS (
      SELECT 1
      FROM pg_trigger trg
      WHERE trg.tgrelid = to_regclass(
          'xfactory_legacy_quarantine_v2.legacy_quarantine_records')
        AND trg.tgname = 'legacy_quarantine_records_immutable'
        AND NOT trg.tgisinternal
    )),
    ('no-runtime-schema-usage', NOT has_schema_privilege(
      'xfactory_v2_runtime', 'xfactory_legacy_quarantine_v2', 'USAGE')),
    ('no-control-schema-usage', NOT has_schema_privilege(
      'xfactory_v2_control', 'xfactory_legacy_quarantine_v2', 'USAGE')),
    ('no-audit-schema-usage', NOT has_schema_privilege(
      'xfactory_v2_audit', 'xfactory_legacy_quarantine_v2', 'USAGE')),
    ('no-migrator-schema-usage', NOT has_schema_privilege(
      'xfactory_v2_migrator', 'xfactory_legacy_quarantine_v2', 'USAGE')),
    ('no-runtime-table-select', NOT has_table_privilege(
      'xfactory_v2_runtime',
      'xfactory_legacy_quarantine_v2.legacy_quarantine_records', 'SELECT')),
    ('no-migrator-table-select', NOT has_table_privilege(
      'xfactory_v2_migrator',
      'xfactory_legacy_quarantine_v2.legacy_quarantine_records', 'SELECT')),
    ('no-public-table-privileges', NOT EXISTS (
      SELECT 1
      FROM pg_class cls
      CROSS JOIN LATERAL aclexplode(
        coalesce(cls.relacl, '{}'::aclitem[])) acl_entry
      WHERE cls.oid = to_regclass(
          'xfactory_legacy_quarantine_v2.legacy_quarantine_records')
        AND acl_entry.grantee = 0
    )),
    ('dependency-guard-installed', EXISTS (
      SELECT 1
      FROM pg_event_trigger evt
      JOIN pg_proc proc ON proc.oid = evt.evtfoid
      JOIN pg_namespace ns ON ns.oid = proc.pronamespace
      WHERE evt.evtname = 'xfactory_quarantine_dependency_guard'
        AND evt.evtevent = 'ddl_command_end'
        AND evt.evtenabled <> 'D'
        AND ns.nspname = 'xfactory_runtime_v2'
        AND proc.proname = 'reject_quarantine_dependency'
    )),
    ('no-authoritative-dependency', NOT EXISTS (
      SELECT 1
      FROM pg_depend dep
      JOIN pg_class quarantined ON quarantined.oid = dep.refobjid
      JOIN pg_namespace quarantine_ns
        ON quarantine_ns.oid = quarantined.relnamespace
      LEFT JOIN pg_class dependent ON dependent.oid = dep.objid
        AND dep.classid = 'pg_class'::regclass
      LEFT JOIN pg_constraint dependent_constraint
        ON dependent_constraint.oid = dep.objid
        AND dep.classid = 'pg_constraint'::regclass
      WHERE dep.deptype IN ('n', 'a')
        AND dep.refclassid = 'pg_class'::regclass
        AND quarantine_ns.nspname = 'xfactory_legacy_quarantine_v2'
        AND coalesce(
          (SELECT ns.nspname FROM pg_namespace ns
           WHERE ns.oid = dependent.relnamespace),
          (SELECT ns.nspname FROM pg_namespace ns
           WHERE ns.oid = dependent_constraint.connamespace),
          'xfactory_legacy_quarantine_v2'
        ) <> 'xfactory_legacy_quarantine_v2'
    ))
) AS checks (probe, holds);
