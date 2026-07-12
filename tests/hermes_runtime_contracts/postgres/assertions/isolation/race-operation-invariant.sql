SELECT
  (SELECT count(*) FROM xfactory_runtime_v2.governed_projections
   WHERE operation_id = 'operation-race')::text || ':' ||
  (SELECT count(*) FROM xfactory_runtime_v2.operation_authorizations
   WHERE operation_id = 'operation-race')::text || ':' ||
  (SELECT count(*) FROM xfactory_runtime_v2.traceability_edges
   WHERE operation_id = 'operation-race')::text;
