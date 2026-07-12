WITH expected(name) AS (
  VALUES
    ('installation_registrations'),
    ('stack_registrations'),
    ('layer_registrations'),
    ('installation_lifecycle_events'),
    ('stack_lifecycle_events'),
    ('layer_lifecycle_events'),
    ('lifecycle_projections')
), resolved AS (
  SELECT
    name,
    to_regclass(format('xfactory_runtime_v2.%I', name)) AS relation
  FROM expected
)
SELECT bool_and(
  relation IS NOT NULL
  AND EXISTS (
    SELECT 1
    FROM pg_trigger
    WHERE tgrelid = relation
      AND NOT tgisinternal
  )
)
FROM resolved;
