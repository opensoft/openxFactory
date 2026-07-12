SET lock_timeout = '15s';
SET statement_timeout = '30s';
BEGIN;
SELECT xfactory_runtime_api_v2.assume_scope(
  'install-01', '', '', 'grant-control-scope'
);
SELECT xfactory_runtime_api_v2.revoke_authority_grant(
  'revoke-grant-race', 'grant-a-project', 'grant-control-revoke',
  'race-revocation'
);
COMMIT;
