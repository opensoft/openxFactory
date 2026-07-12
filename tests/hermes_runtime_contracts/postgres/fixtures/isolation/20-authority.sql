\set ON_ERROR_STOP on

INSERT INTO xfactory_runtime_v2.principals (
  installation_id, stack_id, layer_id, principal_id, record_digest,
  digest_profile, principal_type, scope_kind, initial_state, created_at
) VALUES
  ('install-01', 'stack-01', 'customer-a', 'principal-a', 'sha256:a100000000000000000000000000000000000000000000000000000000000001', 'xfactory-canonical-json-v1', 'agent', 'layer', 'provisioning', '2026-07-12T12:00:00Z'),
  ('install-01', 'stack-01', 'customer-b', 'principal-b', 'sha256:a200000000000000000000000000000000000000000000000000000000000002', 'xfactory-canonical-json-v1', 'agent', 'layer', 'provisioning', '2026-07-12T12:00:00Z'),
  ('install-01', '', '', 'principal-admin', 'sha256:a300000000000000000000000000000000000000000000000000000000000003', 'xfactory-canonical-json-v1', 'human', 'installation_admin', 'provisioning', '2026-07-12T12:00:00Z'),
  ('install-01', '', '', 'principal-control', 'sha256:a400000000000000000000000000000000000000000000000000000000000004', 'xfactory-canonical-json-v1', 'service', 'installation_admin', 'provisioning', '2026-07-12T12:00:00Z'),
  ('install-01', 'stack-01', 'customer-b', 'reviewer-a', 'sha256:a500000000000000000000000000000000000000000000000000000000000005', 'xfactory-canonical-json-v1', 'human', 'layer', 'provisioning', '2026-07-12T12:00:00Z'),
  ('install-01', 'stack-01', 'customer-b', 'reviewer-b', 'sha256:a600000000000000000000000000000000000000000000000000000000000006', 'xfactory-canonical-json-v1', 'human', 'layer', 'provisioning', '2026-07-12T12:00:00Z');

INSERT INTO xfactory_runtime_v2.installation_trust_anchors (
  installation_id, anchor_id, record_digest, digest_profile, anchor_kind,
  principal_stack_id, principal_layer_id, principal_id, principal_digest,
  key_provider, key_id, key_algorithm, policy_repository, policy_commit,
  policy_ref,
  policy_digest, authorized_evidence_digest, effective_at, created_at
) VALUES (
  'install-01', 'anchor-01',
  'sha256:c300000000000000000000000000000000000000000000000000000000000003',
  'xfactory-canonical-json-v1', 'genesis', '', '', 'principal-control',
  'sha256:a400000000000000000000000000000000000000000000000000000000000004',
  'example-kms', 'anchor-01', 'ed25519', 'opensoft/exampleFactory',
  'dddddddddddddddddddddddddddddddddddddddd', 'policies/authority.yaml',
  'sha256:c100000000000000000000000000000000000000000000000000000000000001',
  'sha256:c200000000000000000000000000000000000000000000000000000000000002',
  '2020-01-01T00:00:00Z', '2020-01-01T00:00:00Z'
);

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
  'install-01', 'grant-root-issue',
  'sha256:d100000000000000000000000000000000000000000000000000000000000001',
  'xfactory-canonical-json-v1', 'root', '', '', 'principal-control',
  principal.record_digest, 'anchor-01', anchor_record.record_digest,
  NULL, NULL, 'installation', '', '', 'issue_grant',
  'policy_namespace', 'install-01', NULL, 'opensoft/exampleFactory',
  'dddddddddddddddddddddddddddddddddddddddd', 'policies/authority.yaml',
  'sha256:c100000000000000000000000000000000000000000000000000000000000001',
  '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z',
  '2020-01-01T00:00:00Z'
FROM xfactory_runtime_v2.principals principal
CROSS JOIN xfactory_runtime_v2.installation_trust_anchors anchor_record
WHERE principal.installation_id = 'install-01'
  AND principal.stack_id = ''
  AND principal.layer_id = ''
  AND principal.principal_id = 'principal-control'
  AND anchor_record.installation_id = 'install-01'
  AND anchor_record.anchor_id = 'anchor-01';

WITH seed (
  installation_id, grant_id, record_digest, digest_profile, grant_kind,
  grantee_stack_id, grantee_layer_id, grantee_principal_id,
  trust_anchor_id, trust_anchor_digest, issuer_grant_id, issuer_grant_digest,
  scope_kind, scope_stack_id, scope_layer_id, action, resource_type,
  resource_id, resource_digest, policy_ref, policy_digest, starts_at, expires_at
) AS (VALUES
  ('install-01', 'grant-control-scope', 'sha256:d200000000000000000000000000000000000000000000000000000000000002', 'xfactory-canonical-json-v1', 'delegated', '', '', 'principal-control', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'installation', '', '', 'assume_scope', 'policy_namespace', 'install-01', NULL, 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-a-scope', 'sha256:d300000000000000000000000000000000000000000000000000000000000003', 'xfactory-canonical-json-v1', 'delegated', 'stack-01', 'customer-a', 'principal-a', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-a', 'assume_scope', 'layer_identity', 'customer-a', NULL, 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-b-scope', 'sha256:d400000000000000000000000000000000000000000000000000000000000004', 'xfactory-canonical-json-v1', 'delegated', 'stack-01', 'customer-b', 'principal-b', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-b', 'assume_scope', 'layer_identity', 'customer-b', NULL, 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-review-a-scope', 'sha256:d500000000000000000000000000000000000000000000000000000000000005', 'xfactory-canonical-json-v1', 'delegated', 'stack-01', 'customer-b', 'reviewer-a', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-b', 'assume_scope', 'layer_identity', 'customer-b', NULL, 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-review-b-scope', 'sha256:d600000000000000000000000000000000000000000000000000000000000006', 'xfactory-canonical-json-v1', 'delegated', 'stack-01', 'customer-b', 'reviewer-b', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-b', 'assume_scope', 'layer_identity', 'customer-b', NULL, 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-a-artifact', 'sha256:d700000000000000000000000000000000000000000000000000000000000007', 'xfactory-canonical-json-v1', 'delegated', 'stack-01', 'customer-a', 'principal-a', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-a', 'create_artifact', 'artifact', 'artifact-a', 'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314', 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-a-artifact-new', 'sha256:d800000000000000000000000000000000000000000000000000000000000008', 'xfactory-canonical-json-v1', 'delegated', 'stack-01', 'customer-a', 'principal-a', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-a', 'create_artifact', 'artifact', 'artifact-a-new', 'sha256:480aa7aef6e198db395d4a678bd677aff5130f6fdb84a9e38075c355dc7ad0b6', 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-a-project', 'sha256:d900000000000000000000000000000000000000000000000000000000000009', 'xfactory-canonical-json-v1', 'delegated', '', '', 'principal-control', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-a', 'project_resource', 'artifact', 'artifact-a', 'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314', 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-a-create-binding', 'sha256:e500000000000000000000000000000000000000000000000000000000000005', 'xfactory-canonical-json-v1', 'delegated', '', '', 'principal-control', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-a', 'create_binding', 'artifact', 'artifact-a', 'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314', 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-b-accept', 'sha256:da0000000000000000000000000000000000000000000000000000000000000a', 'xfactory-canonical-json-v1', 'delegated', 'stack-01', 'customer-b', 'principal-b', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-b', 'accept_cross_layer', 'artifact', 'artifact-b-draft', 'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314', 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-b-request', 'sha256:e300000000000000000000000000000000000000000000000000000000000003', 'xfactory-canonical-json-v1', 'delegated', 'stack-01', 'customer-b', 'principal-b', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-b', 'request_approval', 'artifact', 'artifact-b-draft', 'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314', 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-b-artifact-draft', 'sha256:e400000000000000000000000000000000000000000000000000000000000004', 'xfactory-canonical-json-v1', 'delegated', 'stack-01', 'customer-b', 'principal-b', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-b', 'create_artifact', 'artifact', 'artifact-b-draft', 'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314', 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-review-a-decide', 'sha256:dd0000000000000000000000000000000000000000000000000000000000000d', 'xfactory-canonical-json-v1', 'delegated', 'stack-01', 'customer-b', 'reviewer-a', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-b', 'decide_approval', 'approval_request', 'approval-b', 'sha256:ed0000000000000000000000000000000000000000000000000000000000000d', 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-review-b-decide', 'sha256:de0000000000000000000000000000000000000000000000000000000000000e', 'xfactory-canonical-json-v1', 'delegated', 'stack-01', 'customer-b', 'reviewer-b', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-b', 'decide_approval', 'approval_request', 'approval-b', 'sha256:ed0000000000000000000000000000000000000000000000000000000000000d', 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-b-supersede', 'sha256:df0000000000000000000000000000000000000000000000000000000000000f', 'xfactory-canonical-json-v1', 'delegated', 'stack-01', 'customer-b', 'principal-b', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-b', 'supersede_approval', 'approval_request', 'approval-b', 'sha256:ed0000000000000000000000000000000000000000000000000000000000000d', 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z'),
  ('install-01', 'grant-transition-a', 'sha256:e000000000000000000000000000000000000000000000000000000000000010', 'xfactory-canonical-json-v1', 'delegated', '', '', 'principal-control', NULL, NULL, 'grant-root-issue', 'sha256:d100000000000000000000000000000000000000000000000000000000000001', 'layer', 'stack-01', 'customer-a', 'transition_lifecycle', 'layer_identity', 'customer-a', NULL, 'policy://example/delegated-v1', 'sha256:d000000000000000000000000000000000000000000000000000000000000000', '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z')
)
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
  seed.installation_id, seed.grant_id, seed.record_digest, seed.digest_profile,
  seed.grant_kind, seed.grantee_stack_id, seed.grantee_layer_id,
  seed.grantee_principal_id, principal.record_digest, NULL, NULL,
  seed.issuer_grant_id, issuer_grant.record_digest,
  seed.scope_kind, seed.scope_stack_id, seed.scope_layer_id, seed.action,
  seed.resource_type, seed.resource_id, seed.resource_digest,
  'opensoft/exampleFactory', 'dddddddddddddddddddddddddddddddddddddddd',
  'policies/delegated.yaml', seed.policy_digest,
  seed.starts_at::timestamptz, seed.expires_at::timestamptz,
  seed.starts_at::timestamptz
FROM seed
JOIN xfactory_runtime_v2.principals principal
  ON principal.installation_id = seed.installation_id
 AND principal.stack_id = seed.grantee_stack_id
 AND principal.layer_id = seed.grantee_layer_id
 AND principal.principal_id = seed.grantee_principal_id
JOIN xfactory_runtime_v2.authority_grants issuer_grant
  ON issuer_grant.installation_id = seed.installation_id
 AND issuer_grant.grant_id = seed.issuer_grant_id;

WITH revoke_seed (grant_id, resource_id) AS (VALUES
  ('grant-control-revoke', 'grant-a-project'),
  ('grant-control-revoke-scope', 'grant-a-scope')
)
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
  'install-01', revoke_seed.grant_id,
  'sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
  'xfactory-canonical-json-v1', 'delegated', '', '', 'principal-control',
  principal.record_digest, NULL, NULL, 'grant-root-issue',
  issuer_grant.record_digest, 'installation', '', '', 'revoke_grant',
  'authority_grant', target_grant.grant_id, target_grant.record_digest,
  'opensoft/exampleFactory', 'dddddddddddddddddddddddddddddddddddddddd',
  'policies/delegated.yaml',
  'sha256:d000000000000000000000000000000000000000000000000000000000000000',
  '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z',
  '2020-01-01T00:00:00Z'
FROM revoke_seed
JOIN xfactory_runtime_v2.authority_grants target_grant
  ON target_grant.installation_id = 'install-01'
 AND target_grant.grant_id = revoke_seed.resource_id
JOIN xfactory_runtime_v2.authority_grants issuer_grant
  ON issuer_grant.installation_id = 'install-01'
 AND issuer_grant.grant_id = 'grant-root-issue'
JOIN xfactory_runtime_v2.principals principal
  ON principal.installation_id = 'install-01'
 AND principal.stack_id = ''
 AND principal.layer_id = ''
 AND principal.principal_id = 'principal-control';

INSERT INTO xfactory_runtime_v2.database_principal_bindings (
  installation_id, stack_id, layer_id, binding_id, record_digest,
  digest_profile, session_user_name, principal_id, principal_digest,
  role_class, creator_grant_id, creator_grant_digest, bound_at
) VALUES
  ('install-01', 'stack-01', 'customer-a', 'dbbind-a', 'sha256:b100000000000000000000000000000000000000000000000000000000000001', 'xfactory-canonical-json-v1', 'hcs_customer_a', 'principal-a', 'sha256:a100000000000000000000000000000000000000000000000000000000000001', 'runtime', 'grant-a-scope', (SELECT record_digest FROM xfactory_runtime_v2.authority_grants WHERE grant_id = 'grant-a-scope'), '2026-07-12T12:00:00Z'),
  ('install-01', 'stack-01', 'customer-b', 'dbbind-b', 'sha256:b200000000000000000000000000000000000000000000000000000000000002', 'xfactory-canonical-json-v1', 'hcs_customer_b', 'principal-b', 'sha256:a200000000000000000000000000000000000000000000000000000000000002', 'runtime', 'grant-b-scope', (SELECT record_digest FROM xfactory_runtime_v2.authority_grants WHERE grant_id = 'grant-b-scope'), '2026-07-12T12:00:00Z'),
  ('install-01', '', '', 'dbbind-control', 'sha256:b400000000000000000000000000000000000000000000000000000000000004', 'xfactory-canonical-json-v1', 'hcs_control_plane', 'principal-control', 'sha256:a400000000000000000000000000000000000000000000000000000000000004', 'control', 'grant-control-scope', (SELECT record_digest FROM xfactory_runtime_v2.authority_grants WHERE grant_id = 'grant-control-scope'), '2026-07-12T12:00:00Z'),
  ('install-01', 'stack-01', 'customer-b', 'dbbind-review-a', 'sha256:b500000000000000000000000000000000000000000000000000000000000005', 'xfactory-canonical-json-v1', 'hcs_reviewer_a', 'reviewer-a', 'sha256:a500000000000000000000000000000000000000000000000000000000000005', 'runtime', 'grant-review-a-scope', (SELECT record_digest FROM xfactory_runtime_v2.authority_grants WHERE grant_id = 'grant-review-a-scope'), '2026-07-12T12:00:00Z'),
  ('install-01', 'stack-01', 'customer-b', 'dbbind-review-b', 'sha256:b600000000000000000000000000000000000000000000000000000000000006', 'xfactory-canonical-json-v1', 'hcs_reviewer_b', 'reviewer-b', 'sha256:a600000000000000000000000000000000000000000000000000000000000006', 'runtime', 'grant-review-b-scope', (SELECT record_digest FROM xfactory_runtime_v2.authority_grants WHERE grant_id = 'grant-review-b-scope'), '2026-07-12T12:00:00Z');

INSERT INTO xfactory_runtime_v2.installation_lifecycle_events (
  installation_id, event_id, event_digest, predecessor_id,
  predecessor_digest, from_state, to_state, authority_grant_id, reason,
  occurred_at
) VALUES
  ('install-01', 'installation-configured', 'sha256:f100000000000000000000000000000000000000000000000000000000000001', 'installation-registration-01', 'sha256:1111111111111111111111111111111111111111111111111111111111111111', 'installing', 'configured', 'grant-root-issue', 'seed-configured', '2026-07-12T12:05:00Z'),
  ('install-01', 'installation-operational', 'sha256:f200000000000000000000000000000000000000000000000000000000000002', 'installation-configured', 'sha256:f100000000000000000000000000000000000000000000000000000000000001', 'configured', 'operational', 'grant-root-issue', 'seed-operational', '2026-07-12T12:06:00Z');

INSERT INTO xfactory_runtime_v2.stack_lifecycle_events (
  installation_id, stack_id, event_id, event_digest, predecessor_id,
  predecessor_digest, from_state, to_state, authority_grant_id, reason,
  occurred_at
) VALUES
  ('install-01', 'stack-01', 'stack-configured', 'sha256:f300000000000000000000000000000000000000000000000000000000000003', 'stack-registration-01', 'sha256:2222222222222222222222222222222222222222222222222222222222222222', 'installing', 'configured', 'grant-root-issue', 'seed-configured', '2026-07-12T12:05:00Z'),
  ('install-01', 'stack-01', 'stack-operational', 'sha256:f400000000000000000000000000000000000000000000000000000000000004', 'stack-configured', 'sha256:f300000000000000000000000000000000000000000000000000000000000003', 'configured', 'operational', 'grant-root-issue', 'seed-operational', '2026-07-12T12:06:00Z');

INSERT INTO xfactory_runtime_v2.layer_lifecycle_events (
  installation_id, stack_id, layer_id, event_id, event_digest,
  predecessor_kind, predecessor_id, predecessor_digest, from_state, to_state,
  authority_grant_id, authority_grant_digest, reason, occurred_at
) VALUES
  ('install-01', 'stack-01', 'client-01', 'activate-client', 'sha256:f500000000000000000000000000000000000000000000000000000000000005', 'registration', 'layer-registration-client', 'sha256:3333333333333333333333333333333333333333333333333333333333333333', 'provisioning', 'active', 'grant-root-issue', (SELECT record_digest FROM xfactory_runtime_v2.authority_grants WHERE installation_id = 'install-01' AND grant_id = 'grant-root-issue'), 'seed-active', '2026-07-12T12:05:00Z'),
  ('install-01', 'stack-01', 'domain-01', 'activate-domain', 'sha256:f600000000000000000000000000000000000000000000000000000000000006', 'registration', 'layer-registration-domain', 'sha256:4444444444444444444444444444444444444444444444444444444444444444', 'provisioning', 'active', 'grant-root-issue', (SELECT record_digest FROM xfactory_runtime_v2.authority_grants WHERE installation_id = 'install-01' AND grant_id = 'grant-root-issue'), 'seed-active', '2026-07-12T12:05:00Z'),
  ('install-01', 'stack-01', 'customer-a', 'activate-a', 'sha256:f700000000000000000000000000000000000000000000000000000000000007', 'registration', 'layer-registration-a', 'sha256:5555555555555555555555555555555555555555555555555555555555555555', 'provisioning', 'active', 'grant-root-issue', (SELECT record_digest FROM xfactory_runtime_v2.authority_grants WHERE installation_id = 'install-01' AND grant_id = 'grant-root-issue'), 'seed-active', '2026-07-12T12:05:00Z'),
  ('install-01', 'stack-01', 'customer-b', 'activate-b', 'sha256:f800000000000000000000000000000000000000000000000000000000000008', 'registration', 'layer-registration-b', 'sha256:6666666666666666666666666666666666666666666666666666666666666666', 'provisioning', 'active', 'grant-root-issue', (SELECT record_digest FROM xfactory_runtime_v2.authority_grants WHERE installation_id = 'install-01' AND grant_id = 'grant-root-issue'), 'seed-active', '2026-07-12T12:05:00Z');

INSERT INTO xfactory_runtime_v2.principal_lifecycle_events (
  installation_id, stack_id, layer_id, principal_id, event_id, event_digest,
  predecessor_id, predecessor_digest, from_state, to_state,
  authority_grant_id, reason, occurred_at
) SELECT
  installation_id, stack_id, layer_id, principal_id,
  'activate-' || principal_id,
  'sha256:' || repeat(substr(md5(principal_id), 1, 1), 64),
  principal_id, record_digest, 'provisioning', 'active', 'grant-root-issue',
  'seed-active', '2026-07-12T12:05:00Z'
FROM xfactory_runtime_v2.principals;

INSERT INTO xfactory_runtime_v2.cross_layer_bindings (
  installation_id, binding_id, record_digest, digest_profile,
  source_stack_id, source_layer_id, source_resource_type, source_resource_id,
  source_resource_digest, target_stack_id, target_layer_id,
  target_resource_type, target_resource_id, target_resource_digest, action,
  purpose, creator_principal_stack_id, creator_principal_layer_id,
  creator_principal_id, creator_principal_digest,
  creator_grant_id, creator_grant_digest,
  target_acceptance_grant_id, target_acceptance_grant_digest,
  target_acceptance_principal_stack_id, target_acceptance_principal_layer_id,
  target_acceptance_principal_id, target_acceptance_principal_digest,
  starts_at, expires_at, created_at
) VALUES (
  'install-01', 'binding-a-b',
  'sha256:e100000000000000000000000000000000000000000000000000000000000001',
  'xfactory-canonical-json-v1', 'stack-01', 'customer-a', 'artifact',
  'artifact-a',
  'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
  'stack-01', 'customer-b', 'artifact', 'artifact-b-draft',
  'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
  'project_resource', 'approved-test-projection', '', '', 'principal-control',
  'sha256:a400000000000000000000000000000000000000000000000000000000000004',
  'grant-a-create-binding',
  (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
   WHERE grant_id = 'grant-a-create-binding'),
  'grant-b-accept',
  (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
   WHERE grant_id = 'grant-b-accept'),
  'stack-01', 'customer-b', 'principal-b',
  'sha256:a200000000000000000000000000000000000000000000000000000000000002',
  '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z',
  '2026-07-12T12:09:00Z'
);

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
  'install-01', 'grant-a-revoke-binding',
  'sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
  'xfactory-canonical-json-v1', 'delegated', '', '', 'principal-control',
  principal.record_digest, NULL, NULL, 'grant-root-issue',
  issuer_grant.record_digest, 'layer', 'stack-01', 'customer-a',
  'revoke_binding', 'cross_layer_binding', binding.binding_id,
  binding.record_digest, 'opensoft/exampleFactory',
  'dddddddddddddddddddddddddddddddddddddddd', 'policies/delegated.yaml',
  'sha256:d000000000000000000000000000000000000000000000000000000000000000',
  '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z',
  '2020-01-01T00:00:00Z'
FROM xfactory_runtime_v2.cross_layer_bindings binding
JOIN xfactory_runtime_v2.authority_grants issuer_grant
  ON issuer_grant.installation_id = binding.installation_id
 AND issuer_grant.grant_id = 'grant-root-issue'
JOIN xfactory_runtime_v2.principals principal
  ON principal.installation_id = binding.installation_id
 AND principal.stack_id = ''
 AND principal.layer_id = ''
 AND principal.principal_id = 'principal-control'
WHERE binding.installation_id = 'install-01'
  AND binding.binding_id = 'binding-a-b';

INSERT INTO xfactory_runtime_v2.lifecycle_projections (
  entity_kind, installation_id, stack_id, layer_id, entity_id, derived_state,
  latest_event_id, latest_event_digest, terminal_at
) VALUES
  ('installation', 'install-01', '', '', 'install-01', 'operational', 'installation-operational', 'sha256:f200000000000000000000000000000000000000000000000000000000000002', NULL),
  ('stack', 'install-01', 'stack-01', '', 'stack-01', 'operational', 'stack-operational', 'sha256:f400000000000000000000000000000000000000000000000000000000000004', NULL),
  ('layer', 'install-01', 'stack-01', 'client-01', 'client-01', 'active', 'activate-client', 'sha256:f500000000000000000000000000000000000000000000000000000000000005', NULL),
  ('layer', 'install-01', 'stack-01', 'domain-01', 'domain-01', 'active', 'activate-domain', 'sha256:f600000000000000000000000000000000000000000000000000000000000006', NULL),
  ('layer', 'install-01', 'stack-01', 'customer-a', 'customer-a', 'active', 'activate-a', 'sha256:f700000000000000000000000000000000000000000000000000000000000007', NULL),
  ('layer', 'install-01', 'stack-01', 'customer-b', 'customer-b', 'active', 'activate-b', 'sha256:f800000000000000000000000000000000000000000000000000000000000008', NULL);

INSERT INTO xfactory_runtime_v2.lifecycle_projections (
  entity_kind, installation_id, stack_id, layer_id, entity_id, derived_state,
  latest_event_id, latest_event_digest, terminal_at
) SELECT
  'principal', installation_id, stack_id, layer_id, principal_id, 'active',
  'activate-' || principal_id,
  'sha256:' || repeat(substr(md5(principal_id), 1, 1), 64), NULL
FROM xfactory_runtime_v2.principals;
