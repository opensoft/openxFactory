\set ON_ERROR_STOP on

INSERT INTO xfactory_runtime_v2.installation_registrations (
  installation_id, registration_id, registration_digest, initial_state,
  genesis_anchor_id, created_at
) VALUES (
  'install-01', 'installation-registration-01',
  'sha256:1111111111111111111111111111111111111111111111111111111111111111',
  'installing', 'anchor-01', '2026-07-12T12:00:00Z'
);

INSERT INTO xfactory_runtime_v2.stack_registrations (
  installation_id, stack_id, registration_id, registration_digest,
  domain_id, initial_state, created_at
) VALUES (
  'install-01', 'stack-01', 'stack-registration-01',
  'sha256:2222222222222222222222222222222222222222222222222222222222222222',
  'example-domain', 'installing', '2026-07-12T12:00:00Z'
);

INSERT INTO xfactory_runtime_v2.layer_registrations (
  installation_id, stack_id, layer_id, registration_id,
  registration_digest, role, template_role, display_name, policy_namespace,
  initial_state, customer_subject_kind, customer_subject_issuer,
  customer_subject_namespace, customer_subject_ref, created_at
) VALUES
  (
    'install-01', 'stack-01', 'client-01', 'layer-registration-client',
    'sha256:3333333333333333333333333333333333333333333333333333333333333333',
    'client', 'client', 'Client Hermes', 'stack-01.client.singleton',
    'provisioning', NULL, NULL, NULL, NULL, '2026-07-12T12:00:00Z'
  ),
  (
    'install-01', 'stack-01', 'domain-01', 'layer-registration-domain',
    'sha256:4444444444444444444444444444444444444444444444444444444444444444',
    'domain', 'domain', 'Domain Hermes', 'stack-01.domain.singleton',
    'provisioning', NULL, NULL, NULL, NULL, '2026-07-12T12:00:00Z'
  ),
  (
    'install-01', 'stack-01', 'customer-a', 'layer-registration-a',
    'sha256:5555555555555555555555555555555555555555555555555555555555555555',
    'customer', 'customer', 'Customer A', 'stack-01.customer.a',
    'provisioning', 'software_project', 'example-domain', 'subjects',
    'urn:xfactory:subject:9f32f1de-82a7-4e38-a83d-9e5dd9189a11',
    '2026-07-12T12:00:00Z'
  ),
  (
    'install-01', 'stack-01', 'customer-b', 'layer-registration-b',
    'sha256:6666666666666666666666666666666666666666666666666666666666666666',
    'customer', 'customer', 'Customer B', 'stack-01.customer.b',
    'provisioning', 'software_project', 'example-domain', 'subjects',
    'urn:xfactory:subject:018f47a0-7b2c-7abc-8def-0123456789ab',
    '2026-07-12T12:00:00Z'
  );
