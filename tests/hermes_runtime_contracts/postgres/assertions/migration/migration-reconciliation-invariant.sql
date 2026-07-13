-- Reconciliation invariant: every succeeded attempt carries exactly one
-- cutover observation and one reconciliation whose per_table document holds
-- all twelve canonical tables, whose totals equal the per-table sums, and
-- whose every source row reconciles into exactly one class.
SELECT coalesce(bool_and(reconciled), true)
FROM (
  SELECT
    (
      SELECT count(*) = 1
      FROM xfactory_runtime_v2.migration_cutover_observations observation
      WHERE observation.attempt_id = success.attempt_id
    )
    AND (
      SELECT count(*) = 1
      FROM xfactory_runtime_v2.migration_reconciliations reconciliation
      WHERE reconciliation.attempt_id = success.attempt_id
    )
    AND (
      SELECT
        (SELECT count(*) FROM jsonb_object_keys(reconciliation.per_table)) = 12
        AND reconciliation.compatibility_history_count = (
          SELECT sum((entry.value ->> 'compatibility_history')::bigint)
          FROM jsonb_each(reconciliation.per_table) entry
        )
        AND reconciliation.quarantine_count = (
          SELECT sum((entry.value ->> 'quarantine')::bigint)
          FROM jsonb_each(reconciliation.per_table) entry
        )
        AND NOT EXISTS (
          SELECT 1
          FROM jsonb_each(reconciliation.per_table) entry
          WHERE (entry.value ->> 'input_count')::bigint
            <> (entry.value ->> 'compatibility_history')::bigint
               + (entry.value ->> 'quarantine')::bigint
        )
      FROM xfactory_runtime_v2.migration_reconciliations reconciliation
      WHERE reconciliation.attempt_id = success.attempt_id
    ) AS reconciled
  FROM (
    SELECT DISTINCT attempt_id
    FROM xfactory_runtime_v2.migration_attempt_events
    WHERE event_type = 'succeeded'
  ) success
) checks;
