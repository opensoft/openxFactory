WITH expected(name) AS (
  VALUES
    ('artifact_bodies'),
    ('artifact_records'),
    ('artifact_lifecycle_events'),
    ('approval_decision_policies'),
    ('approval_requests'),
    ('approval_decisions'),
    ('approval_supersession_events'),
    ('governed_projections'),
    ('operation_authorizations'),
    ('traceability_edges')
), relations AS (
  SELECT expected.name, cls.oid, cls.relrowsecurity, cls.relforcerowsecurity
  FROM expected
  LEFT JOIN pg_class AS cls ON cls.relname = expected.name
  LEFT JOIN pg_namespace AS ns
    ON ns.oid = cls.relnamespace
   AND ns.nspname = 'xfactory_runtime_v2'
)
SELECT count(*) = 10
AND bool_and(oid IS NOT NULL AND relrowsecurity AND relforcerowsecurity)
FROM relations;
