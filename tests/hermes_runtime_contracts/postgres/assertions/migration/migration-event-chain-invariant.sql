-- Attempt-event chain invariant over every (installation_id, migration_id):
-- exactly one root event, no event with more than one successor, at most one
-- terminal succeeded event, and every event type inside the closed set.
SELECT coalesce(bool_and(chain_holds), true)
FROM (
  SELECT
    (
      SELECT count(*) = 1
      FROM xfactory_runtime_v2.migration_attempt_events roots
      WHERE roots.installation_id = series.installation_id
        AND roots.migration_id = series.migration_id
        AND roots.predecessor_event_id IS NULL
    )
    AND NOT EXISTS (
      SELECT 1
      FROM xfactory_runtime_v2.migration_attempt_events tip
      WHERE tip.installation_id = series.installation_id
        AND tip.migration_id = series.migration_id
      GROUP BY tip.predecessor_event_id
      HAVING tip.predecessor_event_id IS NOT NULL AND count(*) > 1
    )
    AND (
      SELECT count(*) <= 1
      FROM xfactory_runtime_v2.migration_attempt_events terminal
      WHERE terminal.installation_id = series.installation_id
        AND terminal.migration_id = series.migration_id
        AND terminal.event_type = 'succeeded'
    )
    AND NOT EXISTS (
      SELECT 1
      FROM xfactory_runtime_v2.migration_attempt_events successor
      WHERE successor.installation_id = series.installation_id
        AND successor.migration_id = series.migration_id
        AND successor.predecessor_event_id IN (
          SELECT done.event_id
          FROM xfactory_runtime_v2.migration_attempt_events done
          WHERE done.installation_id = series.installation_id
            AND done.migration_id = series.migration_id
            AND done.event_type = 'succeeded'
        )
    ) AS chain_holds
  FROM (
    SELECT DISTINCT installation_id, migration_id
    FROM xfactory_runtime_v2.migration_attempt_events
  ) series
) checks;
