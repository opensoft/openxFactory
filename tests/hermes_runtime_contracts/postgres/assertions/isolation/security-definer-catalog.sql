WITH expected(name) AS (
  VALUES
    ('assume_scope'),
    ('clear_scope'),
    ('transition_layer'),
    ('admit_artifact'),
    ('probe_artifact'),
    ('record_approval_decision'),
    ('supersede_approval'),
    ('approval_authorizes'),
    ('project_artifact'),
    ('revoke_authority_grant'),
    ('revoke_cross_layer_binding')
), functions AS (
  SELECT
    expected.name,
    proc.oid,
    proc.prosecdef,
    proc.proconfig,
    has_function_privilege('public', proc.oid, 'EXECUTE') AS public_execute
  FROM expected
  LEFT JOIN pg_proc AS proc ON proc.proname = expected.name
  LEFT JOIN pg_namespace AS ns
    ON ns.oid = proc.pronamespace
   AND ns.nspname = 'xfactory_runtime_api_v2'
)
SELECT count(*) = 11
AND bool_and(
  oid IS NOT NULL
  AND prosecdef
  AND NOT public_execute
  AND EXISTS (
    SELECT 1
    FROM unnest(COALESCE(proconfig, ARRAY[]::text[])) AS setting
    WHERE setting LIKE 'search_path=%'
  )
)
FROM functions;
