\set ON_ERROR_STOP on

-- Migration authority seed: the installation-administration migration
-- principal, its activation evidence, the hcs_migrator database binding, and
-- a deterministic ACTIVE run_migration grant chain issued under the seeded
-- anchor/root pattern of fixtures/isolation/20-authority.sql. Apply after
-- 10-two-customer-topology.sql and 20-authority.sql.

INSERT INTO xfactory_runtime_v2.principals (
  installation_id, stack_id, layer_id, principal_id, record_digest,
  digest_profile, principal_type, scope_kind, initial_state, created_at
) VALUES (
  'install-01', '', '', 'principal-migrator',
  'sha256:a700000000000000000000000000000000000000000000000000000000000007',
  'xfactory-canonical-json-v1', 'service', 'installation_admin',
  'provisioning', '2026-07-12T12:00:00Z'
);

INSERT INTO xfactory_runtime_v2.principal_lifecycle_events (
  installation_id, stack_id, layer_id, principal_id, event_id, event_digest,
  predecessor_id, predecessor_digest, from_state, to_state,
  authority_grant_id, reason, occurred_at
) VALUES (
  'install-01', '', '', 'principal-migrator', 'activate-principal-migrator',
  'sha256:' || repeat(substr(md5('principal-migrator'), 1, 1), 64),
  'principal-migrator',
  'sha256:a700000000000000000000000000000000000000000000000000000000000007',
  'provisioning', 'active', 'grant-root-issue', 'seed-active',
  '2026-07-12T12:05:00Z'
);

INSERT INTO xfactory_runtime_v2.lifecycle_projections (
  entity_kind, installation_id, stack_id, layer_id, entity_id, derived_state,
  latest_event_id, latest_event_digest, terminal_at
) VALUES (
  'principal', 'install-01', '', '', 'principal-migrator', 'active',
  'activate-principal-migrator',
  'sha256:' || repeat(substr(md5('principal-migrator'), 1, 1), 64), NULL
);

INSERT INTO xfactory_runtime_v2.database_principal_bindings (
  installation_id, stack_id, layer_id, binding_id, record_digest,
  digest_profile, session_user_name, principal_id, principal_digest,
  role_class, creator_grant_id, creator_grant_digest, bound_at
) VALUES (
  'install-01', '', '', 'dbbind-migrator',
  'sha256:b700000000000000000000000000000000000000000000000000000000000007',
  'xfactory-canonical-json-v1', 'hcs_migrator', 'principal-migrator',
  'sha256:a700000000000000000000000000000000000000000000000000000000000007',
  'migrator', 'grant-root-issue',
  (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
   WHERE installation_id = 'install-01' AND grant_id = 'grant-root-issue'),
  '2026-07-12T12:00:00Z'
);

-- Deterministic ACTIVE run_migration grant chain under grant-root-issue.
-- The resource digest is a fixed placeholder: it proves the active chain
-- shape yet can never authorize a real payload, whose grant must bind the
-- exact database-recomputed mapping-payload digest (tests mint those).
INSERT INTO xfactory_runtime_v2.authority_grants (
  installation_id, grant_id, record_digest, digest_profile, grant_kind,
  grantee_stack_id, grantee_layer_id, grantee_principal_id,
  grantee_principal_digest, trust_anchor_id, trust_anchor_digest,
  issuer_grant_id, issuer_grant_digest, scope_kind, scope_stack_id,
  scope_layer_id, action, resource_type, resource_id, resource_digest,
  policy_repository, policy_commit, policy_ref, policy_digest,
  starts_at, expires_at, issued_at
)
SELECT
  'install-01', 'grant-run-migration-01',
  'sha256:d700000000000000000000000000000000000000000000000000000000000017',
  'xfactory-canonical-json-v1', 'delegated', '', '', 'principal-migrator',
  principal.record_digest, NULL, NULL,
  'grant-root-issue', issuer_grant.record_digest,
  'installation', '', '', 'run_migration', 'migration_mapping',
  'migration-01',
  'sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
  'opensoft/exampleFactory', 'dddddddddddddddddddddddddddddddddddddddd',
  'policies/delegated.yaml',
  'sha256:d000000000000000000000000000000000000000000000000000000000000000',
  '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z', '2020-01-01T00:00:00Z'
FROM xfactory_runtime_v2.principals principal
JOIN xfactory_runtime_v2.authority_grants issuer_grant
  ON issuer_grant.installation_id = 'install-01'
 AND issuer_grant.grant_id = 'grant-root-issue'
WHERE principal.installation_id = 'install-01'
  AND principal.stack_id = ''
  AND principal.layer_id = ''
  AND principal.principal_id = 'principal-migrator';
