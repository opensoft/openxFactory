SET lock_timeout = '15s';
SET statement_timeout = '30s';
BEGIN;
SELECT xfactory_runtime_api_v2.assume_scope(
  'install-01', '', '', 'grant-control-scope'
);
SELECT xfactory_runtime_api_v2.project_artifact(
  'operation-race', 'binding-a-b', 'artifact-a',
  'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
  'artifact-b-draft',
  'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
  'grant-a-project',
  'trace-operation-race'
);
COMMIT;
