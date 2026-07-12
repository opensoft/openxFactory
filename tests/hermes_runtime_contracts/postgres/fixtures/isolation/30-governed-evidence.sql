\set ON_ERROR_STOP on

INSERT INTO xfactory_runtime_v2.artifact_bodies (
  installation_id, stack_id, layer_id, artifact_id, content_digest,
  byte_size, content, created_at
) VALUES
  ('install-01', 'stack-01', 'customer-a', 'artifact-a', 'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314', 15, convert_to('customer-a-body', 'UTF8'), '2026-07-12T12:10:00Z'),
  ('install-01', 'stack-01', 'customer-b', 'artifact-b-draft', 'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314', 15, convert_to('customer-a-body', 'UTF8'), '2026-07-12T12:10:00Z');

INSERT INTO xfactory_runtime_v2.artifact_records (
  installation_id, stack_id, layer_id, artifact_id, record_digest,
  digest_profile, content_digest, byte_size, media_type, storage_key,
  producer_principal_id, producer_grant_id, producer_grant_digest, created_at
) VALUES
  ('install-01', 'stack-01', 'customer-a', 'artifact-a', 'sha256:ea0000000000000000000000000000000000000000000000000000000000000a', 'xfactory-canonical-json-v1', 'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314', 15, 'text/plain', 'install-01/customer-a/sha256/b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314', 'principal-a', 'grant-a-artifact', (SELECT record_digest FROM xfactory_runtime_v2.authority_grants WHERE grant_id = 'grant-a-artifact'), '2026-07-12T12:10:00Z'),
  ('install-01', 'stack-01', 'customer-b', 'artifact-b-draft', 'sha256:eb0000000000000000000000000000000000000000000000000000000000000b', 'xfactory-canonical-json-v1', 'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314', 15, 'text/plain', 'install-01/customer-b/sha256/b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314', 'principal-b', 'grant-b-artifact-draft', (SELECT record_digest FROM xfactory_runtime_v2.authority_grants WHERE grant_id = 'grant-b-artifact-draft'), '2026-07-12T12:10:00Z');

INSERT INTO xfactory_runtime_v2.artifact_lifecycle_events (
  installation_id, stack_id, layer_id, artifact_id, event_id, event_digest,
  artifact_record_digest, predecessor_kind, predecessor_id,
  predecessor_digest, event_type, actor_principal_id,
  actor_principal_digest, actor_grant_id, actor_grant_digest,
  reason, occurred_at
) VALUES (
  'install-01', 'stack-01', 'customer-a', 'artifact-a',
  'artifact-a:available',
  'sha256:1111111111111111111111111111111111111111111111111111111111111111',
  'sha256:ea0000000000000000000000000000000000000000000000000000000000000a',
  'artifact_record', 'artifact-a',
  'sha256:ea0000000000000000000000000000000000000000000000000000000000000a',
  'available', 'principal-a',
  'sha256:a100000000000000000000000000000000000000000000000000000000000001',
  'grant-a-artifact',
  (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
   WHERE grant_id = 'grant-a-artifact'),
  'seed-available',
  '2026-07-12T12:10:00Z'
);

INSERT INTO xfactory_runtime_v2.approval_decision_policies (
  installation_id, stack_id, layer_id, policy_id, policy_digest,
  authority_scope_kind, authority_stack_id, authority_layer_id,
  reviewer_selectors, aggregation, minimum_approvals,
  conflict_resolution, supersession_authorities, created_at
) VALUES (
  'install-01', 'stack-01', 'customer-b', 'two-reviewer-policy',
  'sha256:ec0000000000000000000000000000000000000000000000000000000000000c',
  'layer', 'stack-01', 'customer-b',
  '[{"selector_id":"reviewer-a","principal_ids":["reviewer-a"],"minimum_count":1,"distinct_principals":true},{"selector_id":"reviewer-b","principal_ids":["reviewer-b"],"minimum_count":1,"distinct_principals":true}]'::jsonb,
  'minimum_approvals', 2, 'contested',
  '[{"event_type":"expired","principal_ids":["principal-b"]},{"event_type":"cancelled","principal_ids":["principal-b"]},{"event_type":"revoked","principal_ids":["principal-b"]}]'::jsonb,
  '2026-07-12T12:10:00Z'
);

INSERT INTO xfactory_runtime_v2.approval_requests (
  installation_id, stack_id, layer_id, request_id, record_digest,
  digest_profile, target_type, target_id, target_digest, target_stack_id,
  target_layer_id, requested_action, authority_scope_kind,
  authority_stack_id, authority_layer_id, requester_stack_id,
  requester_layer_id, requester_principal_id, requester_principal_digest,
  requester_grant_id, requester_grant_digest,
  reviewer_selector_ids,
  decision_policy_id, decision_policy_digest, created_at, expires_at
) VALUES (
  'install-01', 'stack-01', 'customer-b', 'approval-b',
  'sha256:ed0000000000000000000000000000000000000000000000000000000000000d',
  'xfactory-canonical-json-v1', 'artifact', 'artifact-b-draft',
  'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
  'stack-01', 'customer-b', 'project_resource', 'layer',
  'stack-01', 'customer-b', 'stack-01', 'customer-b', 'principal-b',
  'sha256:a200000000000000000000000000000000000000000000000000000000000002',
  'grant-b-request',
  (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
   WHERE grant_id = 'grant-b-request'),
  ARRAY['reviewer-a', 'reviewer-b'],
  'two-reviewer-policy',
  'sha256:ec0000000000000000000000000000000000000000000000000000000000000c',
  '2026-07-12T12:10:00Z', '2099-01-01T00:00:00Z'
);

INSERT INTO xfactory_runtime_v2.traceability_edges (
  installation_id, stack_id, layer_id, edge_id, edge_digest,
  source_stack_id, source_layer_id, source_type, source_id, source_digest,
  target_stack_id, target_layer_id, target_type, target_id, target_digest,
  relation, creator_stack_id, creator_layer_id, creator_principal_id,
  creator_principal_digest, creator_grant_id, creator_grant_digest,
  operation_id, operation_digest, binding_id, binding_digest, grant_refs,
  created_at
) VALUES (
  'install-01', 'stack-01', 'customer-a', 'trace-a-local',
  'sha256:ee0000000000000000000000000000000000000000000000000000000000000e',
  'stack-01', 'customer-a', 'artifact', 'artifact-a',
  'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
  'stack-01', 'customer-a', 'artifact', 'artifact-a',
  'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
  'derived_from', 'stack-01', 'customer-a', 'principal-a',
  'sha256:a100000000000000000000000000000000000000000000000000000000000001',
  'grant-a-project',
  (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
   WHERE grant_id = 'grant-a-project'),
  NULL, NULL, NULL, NULL, NULL,
  '2026-07-12T12:10:00Z'
);
