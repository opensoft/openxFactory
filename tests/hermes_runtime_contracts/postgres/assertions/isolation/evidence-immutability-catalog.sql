WITH expected(name) AS (
  VALUES
    ('artifact_records'),
    ('artifact_lifecycle_events'),
    ('approval_decision_policies'),
    ('approval_requests'),
    ('approval_decisions'),
    ('approval_supersession_events'),
    ('operation_authorizations'),
    ('traceability_edges')
), relations AS (
  SELECT
    expected.name,
    to_regclass(format('xfactory_runtime_v2.%I', expected.name)) AS relation
  FROM expected
)
SELECT count(*) = 8
AND bool_and(
  relation IS NOT NULL
  AND EXISTS (
    SELECT 1
    FROM pg_trigger
    WHERE tgrelid = relation
      AND NOT tgisinternal
  )
)
FROM relations;
