-- openxFactory Hermes customer-subject operational contract v2.
--
-- This file is additive: it does not alter the v1 public.hermes_* surface.
-- It is applied by a PostgreSQL superuser or controlled migrator and creates
-- NOLOGIN role classes, owner-only authoritative state, governed API
-- entrypoints, forced row-level isolation, and append-only evidence.

do $roles$
begin
  if not exists (select 1 from pg_roles where rolname = 'xfactory_v2_owner') then
    create role xfactory_v2_owner nologin;
  end if;
  if not exists (select 1 from pg_roles where rolname = 'xfactory_v2_migrator') then
    create role xfactory_v2_migrator nologin;
  end if;
  if not exists (select 1 from pg_roles where rolname = 'xfactory_v2_runtime') then
    create role xfactory_v2_runtime nologin;
  end if;
  if not exists (select 1 from pg_roles where rolname = 'xfactory_v2_control') then
    create role xfactory_v2_control nologin;
  end if;
  if not exists (select 1 from pg_roles where rolname = 'xfactory_v2_audit') then
    create role xfactory_v2_audit nologin;
  end if;
end
$roles$;

alter role xfactory_v2_owner
  nologin nosuperuser nocreatedb nocreaterole noinherit noreplication nobypassrls;
alter role xfactory_v2_migrator
  nologin nosuperuser nocreatedb nocreaterole noinherit noreplication nobypassrls;
alter role xfactory_v2_runtime
  nologin nosuperuser nocreatedb nocreaterole inherit noreplication nobypassrls;
alter role xfactory_v2_control
  nologin nosuperuser nocreatedb nocreaterole inherit noreplication nobypassrls;
alter role xfactory_v2_audit
  nologin nosuperuser nocreatedb nocreaterole inherit noreplication nobypassrls;

create schema if not exists xfactory_runtime_v2 authorization xfactory_v2_owner;
create schema if not exists xfactory_runtime_api_v2 authorization xfactory_v2_owner;
create schema if not exists xfactory_legacy_quarantine_v2 authorization xfactory_v2_owner;
alter schema xfactory_runtime_v2 owner to xfactory_v2_owner;
alter schema xfactory_runtime_api_v2 owner to xfactory_v2_owner;
alter schema xfactory_legacy_quarantine_v2 owner to xfactory_v2_owner;

revoke all on schema xfactory_runtime_v2 from public;
revoke all on schema xfactory_runtime_api_v2 from public;
revoke all on schema xfactory_legacy_quarantine_v2 from public;
grant usage on schema xfactory_runtime_v2 to xfactory_v2_runtime, xfactory_v2_audit;
grant usage on schema xfactory_runtime_api_v2 to
  xfactory_v2_runtime, xfactory_v2_control, xfactory_v2_audit;

set role xfactory_v2_owner;
set search_path = pg_catalog, xfactory_runtime_v2;

create table if not exists xfactory_runtime_v2.installation_registrations (
  installation_id text primary key,
  registration_id text not null unique,
  registration_digest text not null check (registration_digest ~ '^sha256:[0-9a-f]{64}$'),
  initial_state text not null check (initial_state = 'installing'),
  genesis_anchor_id text not null,
  created_at timestamptz not null
);

create table if not exists xfactory_runtime_v2.stack_registrations (
  installation_id text not null
    references xfactory_runtime_v2.installation_registrations(installation_id),
  stack_id text not null,
  registration_id text not null,
  registration_digest text not null check (registration_digest ~ '^sha256:[0-9a-f]{64}$'),
  domain_id text not null,
  initial_state text not null check (initial_state = 'installing'),
  created_at timestamptz not null,
  primary key (installation_id, stack_id),
  unique (installation_id, registration_id)
);

create table if not exists xfactory_runtime_v2.layer_registrations (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  registration_id text not null,
  registration_digest text not null check (registration_digest ~ '^sha256:[0-9a-f]{64}$'),
  role text not null check (role in ('customer', 'client', 'domain')),
  template_role text not null check (template_role = role),
  display_name text not null,
  policy_namespace text not null,
  initial_state text not null check (initial_state = 'provisioning'),
  customer_subject_kind text,
  customer_subject_issuer text,
  customer_subject_namespace text,
  customer_subject_ref text,
  created_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id),
  unique (installation_id, stack_id, registration_id),
  unique (installation_id, stack_id, policy_namespace),
  foreign key (installation_id, stack_id)
    references xfactory_runtime_v2.stack_registrations(installation_id, stack_id),
  check (
    (
      role = 'customer'
      and customer_subject_kind is not null
      and customer_subject_issuer is not null
      and customer_subject_namespace is not null
      and customer_subject_ref ~ '^urn:xfactory:subject:[0-9a-f-]{36}$'
    )
    or (
      role <> 'customer'
      and customer_subject_kind is null
      and customer_subject_issuer is null
      and customer_subject_namespace is null
      and customer_subject_ref is null
    )
  )
);

create unique index if not exists layer_customer_subject_lifetime_uq
  on xfactory_runtime_v2.layer_registrations (
    installation_id,
    stack_id,
    customer_subject_kind,
    customer_subject_issuer,
    customer_subject_namespace,
    customer_subject_ref
  )
  where role = 'customer';

create table if not exists xfactory_runtime_v2.installation_lifecycle_events (
  installation_id text not null,
  event_id text not null,
  event_digest text not null check (event_digest ~ '^sha256:[0-9a-f]{64}$'),
  predecessor_id text not null,
  predecessor_digest text not null check (predecessor_digest ~ '^sha256:[0-9a-f]{64}$'),
  from_state text not null,
  to_state text not null,
  authority_grant_id text not null,
  reason text not null,
  occurred_at timestamptz not null,
  primary key (installation_id, event_id),
  foreign key (installation_id)
    references xfactory_runtime_v2.installation_registrations(installation_id)
);

create table if not exists xfactory_runtime_v2.stack_lifecycle_events (
  installation_id text not null,
  stack_id text not null,
  event_id text not null,
  event_digest text not null check (event_digest ~ '^sha256:[0-9a-f]{64}$'),
  predecessor_id text not null,
  predecessor_digest text not null check (predecessor_digest ~ '^sha256:[0-9a-f]{64}$'),
  from_state text not null,
  to_state text not null,
  authority_grant_id text not null,
  reason text not null,
  occurred_at timestamptz not null,
  primary key (installation_id, stack_id, event_id),
  foreign key (installation_id, stack_id)
    references xfactory_runtime_v2.stack_registrations(installation_id, stack_id)
);

create table if not exists xfactory_runtime_v2.layer_lifecycle_events (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  event_id text not null,
  event_digest text not null check (event_digest ~ '^sha256:[0-9a-f]{64}$'),
  predecessor_kind text not null check (predecessor_kind in ('registration', 'event')),
  predecessor_id text not null,
  predecessor_digest text not null check (predecessor_digest ~ '^sha256:[0-9a-f]{64}$'),
  from_state text not null,
  to_state text not null,
  authority_grant_id text not null,
  authority_grant_digest text not null
    check (authority_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  reason text not null,
  occurred_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, event_id),
  foreign key (installation_id, stack_id, layer_id)
    references xfactory_runtime_v2.layer_registrations(installation_id, stack_id, layer_id)
);

create unique index if not exists installation_lifecycle_predecessor_uq
  on xfactory_runtime_v2.installation_lifecycle_events
    (installation_id, predecessor_id, predecessor_digest);
create unique index if not exists stack_lifecycle_predecessor_uq
  on xfactory_runtime_v2.stack_lifecycle_events
    (installation_id, stack_id, predecessor_id, predecessor_digest);
create unique index if not exists layer_lifecycle_predecessor_uq
  on xfactory_runtime_v2.layer_lifecycle_events
    (installation_id, stack_id, layer_id, predecessor_kind,
     predecessor_id, predecessor_digest);

create table if not exists xfactory_runtime_v2.lifecycle_projections (
  entity_kind text not null check (entity_kind in ('installation', 'stack', 'layer', 'principal')),
  installation_id text not null,
  stack_id text not null default '',
  layer_id text not null default '',
  entity_id text not null,
  derived_state text not null,
  latest_event_id text,
  latest_event_digest text check (
    latest_event_digest is null or latest_event_digest ~ '^sha256:[0-9a-f]{64}$'
  ),
  terminal_at timestamptz,
  primary key (entity_kind, installation_id, stack_id, layer_id, entity_id)
);

create table if not exists xfactory_runtime_v2.principals (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  principal_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  digest_profile text not null check (digest_profile = 'xfactory-canonical-json-v1'),
  principal_type text not null check (principal_type in ('human', 'agent', 'service', 'group')),
  scope_kind text not null check (scope_kind in ('layer', 'installation_admin')),
  initial_state text not null check (initial_state = 'provisioning'),
  external_ref text,
  created_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, principal_id),
  check (
    (scope_kind = 'layer' and stack_id <> '' and layer_id <> '')
    or (scope_kind = 'installation_admin' and stack_id = '' and layer_id = '')
  )
);

create table if not exists xfactory_runtime_v2.principal_lifecycle_events (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  principal_id text not null,
  event_id text not null,
  event_digest text not null check (event_digest ~ '^sha256:[0-9a-f]{64}$'),
  predecessor_id text not null,
  predecessor_digest text not null check (predecessor_digest ~ '^sha256:[0-9a-f]{64}$'),
  from_state text not null,
  to_state text not null,
  authority_grant_id text not null,
  reason text not null,
  occurred_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, principal_id, event_id),
  foreign key (installation_id, stack_id, layer_id, principal_id)
    references xfactory_runtime_v2.principals
      (installation_id, stack_id, layer_id, principal_id)
);

create unique index if not exists principal_lifecycle_predecessor_uq
  on xfactory_runtime_v2.principal_lifecycle_events
    (installation_id, stack_id, layer_id, principal_id, predecessor_id, predecessor_digest);

create table if not exists xfactory_runtime_v2.database_principal_bindings (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  binding_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  digest_profile text not null check (digest_profile = 'xfactory-canonical-json-v1'),
  session_user_name text not null unique,
  principal_id text not null,
  principal_digest text not null check (principal_digest ~ '^sha256:[0-9a-f]{64}$'),
  role_class text not null
    check (role_class in ('runtime', 'control', 'audit', 'migrator')),
  creator_grant_id text not null,
  creator_grant_digest text not null
    check (creator_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  bound_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, binding_id),
  foreign key (installation_id, stack_id, layer_id, principal_id)
    references xfactory_runtime_v2.principals
      (installation_id, stack_id, layer_id, principal_id)
);

create table if not exists xfactory_runtime_v2.database_principal_binding_revocations (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  revocation_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  binding_id text not null,
  issuer_grant_id text not null,
  reason text not null,
  effective_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, revocation_id),
  foreign key (installation_id, stack_id, layer_id, binding_id)
    references xfactory_runtime_v2.database_principal_bindings
      (installation_id, stack_id, layer_id, binding_id)
);

create table if not exists xfactory_runtime_v2.installation_trust_anchors (
  installation_id text not null,
  anchor_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  digest_profile text not null check (digest_profile = 'xfactory-canonical-json-v1'),
  anchor_kind text not null check (anchor_kind in ('genesis', 'rotated')),
  principal_stack_id text not null,
  principal_layer_id text not null,
  principal_id text not null,
  principal_digest text not null check (principal_digest ~ '^sha256:[0-9a-f]{64}$'),
  key_provider text not null,
  key_id text not null,
  key_algorithm text not null,
  policy_repository text not null,
  policy_commit text not null check (policy_commit ~ '^[0-9a-f]{40}$'),
  policy_ref text not null,
  policy_digest text not null check (policy_digest ~ '^sha256:[0-9a-f]{64}$'),
  authorized_evidence_digest text not null
    check (authorized_evidence_digest ~ '^sha256:[0-9a-f]{64}$'),
  effective_at timestamptz not null,
  created_at timestamptz not null,
  primary key (installation_id, anchor_id),
  foreign key (installation_id)
    references xfactory_runtime_v2.installation_registrations(installation_id),
  foreign key (installation_id, principal_stack_id, principal_layer_id, principal_id)
    references xfactory_runtime_v2.principals
      (installation_id, stack_id, layer_id, principal_id)
);

create unique index if not exists installation_one_genesis_anchor_uq
  on xfactory_runtime_v2.installation_trust_anchors (installation_id)
  where anchor_kind = 'genesis';

create table if not exists xfactory_runtime_v2.installation_trust_anchor_events (
  installation_id text not null,
  event_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  digest_profile text not null check (digest_profile = 'xfactory-canonical-json-v1'),
  event_type text not null check (event_type in ('rotate', 'revoke')),
  predecessor_kind text not null check (predecessor_kind in ('registration', 'event')),
  predecessor_id text not null,
  predecessor_digest text not null check (predecessor_digest ~ '^sha256:[0-9a-f]{64}$'),
  from_anchor_id text not null,
  from_anchor_digest text not null check (from_anchor_digest ~ '^sha256:[0-9a-f]{64}$'),
  to_anchor_id text,
  to_anchor_digest text check (
    to_anchor_digest is null or to_anchor_digest ~ '^sha256:[0-9a-f]{64}$'
  ),
  authority_principal_stack_id text not null,
  authority_principal_layer_id text not null,
  authority_principal_id text not null,
  authority_principal_digest text not null
    check (authority_principal_digest ~ '^sha256:[0-9a-f]{64}$'),
  authority_grant_id text not null,
  authority_grant_digest text not null
    check (authority_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  reason text not null,
  effective_at timestamptz not null,
  occurred_at timestamptz not null,
  primary key (installation_id, event_id),
  foreign key (installation_id, from_anchor_id)
    references xfactory_runtime_v2.installation_trust_anchors(installation_id, anchor_id),
  check (
    (event_type = 'rotate' and to_anchor_id is not null and to_anchor_digest is not null)
    or (event_type = 'revoke' and to_anchor_id is null and to_anchor_digest is null)
  )
);

create unique index if not exists trust_anchor_event_predecessor_uq
  on xfactory_runtime_v2.installation_trust_anchor_events
    (installation_id, predecessor_kind, predecessor_id, predecessor_digest);

create table if not exists xfactory_runtime_v2.authority_grants (
  installation_id text not null,
  grant_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  digest_profile text not null check (digest_profile = 'xfactory-canonical-json-v1'),
  grant_kind text not null check (grant_kind in ('root', 'delegated')),
  grantee_stack_id text not null,
  grantee_layer_id text not null,
  grantee_principal_id text not null,
  grantee_principal_digest text not null
    check (grantee_principal_digest ~ '^sha256:[0-9a-f]{64}$'),
  trust_anchor_id text,
  trust_anchor_digest text check (
    trust_anchor_digest is null or trust_anchor_digest ~ '^sha256:[0-9a-f]{64}$'
  ),
  issuer_grant_id text,
  issuer_grant_digest text check (
    issuer_grant_digest is null or issuer_grant_digest ~ '^sha256:[0-9a-f]{64}$'
  ),
  scope_kind text not null check (scope_kind in ('installation', 'stack', 'layer')),
  scope_stack_id text not null,
  scope_layer_id text not null,
  action text not null check (action in (
    'assume_scope', 'issue_grant', 'revoke_grant',
    'rotate_trust_anchor', 'revoke_trust_anchor',
    'create_binding', 'revoke_binding', 'accept_cross_layer',
    'project_resource', 'create_artifact', 'request_approval', 'decide_approval',
    'supersede_approval', 'transition_lifecycle', 'run_migration',
    'publish_contract'
  )),
  resource_type text not null,
  resource_id text not null,
  resource_digest text check (
    resource_digest is null or resource_digest ~ '^sha256:[0-9a-f]{64}$'
  ),
  policy_repository text not null,
  policy_commit text not null check (policy_commit ~ '^[0-9a-f]{40}$'),
  policy_ref text not null,
  policy_digest text not null check (policy_digest ~ '^sha256:[0-9a-f]{64}$'),
  starts_at timestamptz not null,
  expires_at timestamptz not null,
  issued_at timestamptz not null,
  primary key (installation_id, grant_id),
  check (expires_at > starts_at),
  check (issued_at >= starts_at and issued_at < expires_at),
  check (
    (scope_kind = 'installation' and scope_stack_id = '' and scope_layer_id = '')
    or (scope_kind = 'stack' and scope_stack_id <> '' and scope_layer_id = '')
    or (scope_kind = 'layer' and scope_stack_id <> '' and scope_layer_id <> '')
  ),
  constraint authority_grants_root_scope_ck check (
    (
      grant_kind = 'root'
      and trust_anchor_id is not null
      and trust_anchor_digest is not null
      and issuer_grant_id is null
      and issuer_grant_digest is null
      and scope_kind = 'installation'
      and scope_stack_id = ''
      and scope_layer_id = ''
    )
    or (
      grant_kind = 'delegated'
      and trust_anchor_id is null
      and trust_anchor_digest is null
      and issuer_grant_id is not null
      and issuer_grant_digest is not null
    )
  )
);

create table if not exists xfactory_runtime_v2.authority_grant_revocations (
  installation_id text not null,
  revocation_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  grant_id text not null,
  grant_digest text not null check (grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  revoker_grant_id text not null,
  reason text not null,
  effective_at timestamptz not null,
  primary key (installation_id, revocation_id),
  foreign key (installation_id, grant_id)
    references xfactory_runtime_v2.authority_grants(installation_id, grant_id)
);

create unique index if not exists authority_grant_one_revocation_uq
  on xfactory_runtime_v2.authority_grant_revocations (installation_id, grant_id);

create table if not exists xfactory_runtime_v2.cross_layer_bindings (
  installation_id text not null,
  binding_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  digest_profile text not null check (digest_profile = 'xfactory-canonical-json-v1'),
  source_stack_id text not null,
  source_layer_id text not null,
  source_resource_type text not null,
  source_resource_id text not null,
  source_resource_digest text,
  target_stack_id text not null,
  target_layer_id text not null,
  target_resource_type text not null,
  target_resource_id text not null,
  target_resource_digest text,
  action text not null check (action = 'project_resource'),
  purpose text not null,
  creator_principal_stack_id text not null,
  creator_principal_layer_id text not null,
  creator_principal_id text not null,
  creator_principal_digest text not null
    check (creator_principal_digest ~ '^sha256:[0-9a-f]{64}$'),
  creator_grant_id text not null,
  creator_grant_digest text not null check (creator_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  target_acceptance_grant_id text not null,
  target_acceptance_grant_digest text not null
    check (target_acceptance_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  target_acceptance_principal_stack_id text not null,
  target_acceptance_principal_layer_id text not null,
  target_acceptance_principal_id text not null,
  target_acceptance_principal_digest text not null
    check (target_acceptance_principal_digest ~ '^sha256:[0-9a-f]{64}$'),
  starts_at timestamptz not null,
  expires_at timestamptz not null,
  created_at timestamptz not null,
  primary key (installation_id, binding_id),
  check (source_stack_id <> target_stack_id or source_layer_id <> target_layer_id),
  check (expires_at > starts_at),
  check (
    (source_resource_type in ('layer_identity', 'principal_identity', 'policy_namespace')
      and source_resource_digest is null)
    or source_resource_digest ~ '^sha256:[0-9a-f]{64}$'
  ),
  check (
    (target_resource_type in ('layer_identity', 'principal_identity', 'policy_namespace')
      and target_resource_digest is null)
    or target_resource_digest ~ '^sha256:[0-9a-f]{64}$'
  )
);

create table if not exists xfactory_runtime_v2.cross_layer_binding_revocations (
  installation_id text not null,
  revocation_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  binding_id text not null,
  binding_digest text not null check (binding_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_revoker_grant_id text not null,
  target_acceptance_grant_id text not null,
  reason text not null,
  effective_at timestamptz not null,
  primary key (installation_id, revocation_id),
  foreign key (installation_id, binding_id)
    references xfactory_runtime_v2.cross_layer_bindings(installation_id, binding_id)
);

create unique index if not exists cross_layer_binding_one_revocation_uq
  on xfactory_runtime_v2.cross_layer_binding_revocations (installation_id, binding_id);

create table if not exists xfactory_runtime_v2.artifact_bodies (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  artifact_id text not null,
  content_digest text not null check (content_digest ~ '^sha256:[0-9a-f]{64}$'),
  byte_size bigint not null check (byte_size >= 0),
  content bytea not null,
  created_at timestamptz not null default transaction_timestamp(),
  primary key (installation_id, stack_id, layer_id, artifact_id)
);

create table if not exists xfactory_runtime_v2.artifact_records (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  artifact_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  digest_profile text not null check (digest_profile = 'xfactory-canonical-json-v1'),
  content_digest text not null check (content_digest ~ '^sha256:[0-9a-f]{64}$'),
  byte_size bigint not null check (byte_size >= 0),
  media_type text not null,
  storage_key text not null,
  producer_principal_id text not null,
  producer_grant_id text not null,
  producer_grant_digest text not null
    check (producer_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  job_id text,
  run_id text,
  created_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, artifact_id),
  foreign key (installation_id, stack_id, layer_id, artifact_id)
    references xfactory_runtime_v2.artifact_bodies
      (installation_id, stack_id, layer_id, artifact_id),
  check (
    storage_key =
      installation_id || '/' || layer_id || '/sha256/' ||
      substring(content_digest from 8)
  )
);

create table if not exists xfactory_runtime_v2.artifact_lifecycle_events (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  artifact_id text not null,
  event_id text not null,
  event_digest text not null check (event_digest ~ '^sha256:[0-9a-f]{64}$'),
  artifact_record_digest text not null
    check (artifact_record_digest ~ '^sha256:[0-9a-f]{64}$'),
  predecessor_kind text not null check (predecessor_kind in ('artifact_record', 'event')),
  predecessor_id text not null,
  predecessor_digest text not null check (predecessor_digest ~ '^sha256:[0-9a-f]{64}$'),
  event_type text not null check (event_type in ('available', 'retired', 'tombstoned')),
  actor_principal_id text not null,
  actor_principal_digest text not null check (actor_principal_digest ~ '^sha256:[0-9a-f]{64}$'),
  actor_grant_id text not null,
  actor_grant_digest text not null check (actor_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  reason text not null,
  occurred_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, artifact_id, event_id),
  foreign key (installation_id, stack_id, layer_id, artifact_id)
    references xfactory_runtime_v2.artifact_records
      (installation_id, stack_id, layer_id, artifact_id)
);

create unique index if not exists artifact_event_predecessor_uq
  on xfactory_runtime_v2.artifact_lifecycle_events
    (installation_id, stack_id, layer_id, artifact_id,
     predecessor_kind, predecessor_id, predecessor_digest);

create table if not exists xfactory_runtime_v2.approval_decision_policies (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  policy_id text not null,
  policy_digest text not null check (policy_digest ~ '^sha256:[0-9a-f]{64}$'),
  authority_scope_kind text not null check (
    authority_scope_kind in ('installation', 'installation_admin', 'stack', 'layer')
  ),
  authority_stack_id text not null,
  authority_layer_id text not null,
  reviewer_selectors jsonb not null check (jsonb_typeof(reviewer_selectors) = 'array'),
  aggregation text not null
    check (aggregation in ('all_required_selectors', 'minimum_approvals')),
  minimum_approvals integer check (minimum_approvals > 0),
  conflict_resolution text not null
    check (conflict_resolution in ('contested', 'reject_overrides')),
  supersession_authorities jsonb not null
    check (jsonb_typeof(supersession_authorities) = 'array'),
  created_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, policy_id),
  check (
    (aggregation = 'minimum_approvals' and minimum_approvals is not null)
    or (aggregation = 'all_required_selectors' and minimum_approvals is null)
  )
);

create table if not exists xfactory_runtime_v2.approval_requests (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  request_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  digest_profile text not null check (digest_profile = 'xfactory-canonical-json-v1'),
  target_type text not null,
  target_id text not null,
  target_digest text not null check (target_digest ~ '^sha256:[0-9a-f]{64}$'),
  target_stack_id text not null,
  target_layer_id text not null,
  requested_action text not null,
  authority_scope_kind text not null check (
    authority_scope_kind in ('installation', 'stack', 'layer')
  ),
  authority_stack_id text not null,
  authority_layer_id text not null,
  requester_stack_id text not null,
  requester_layer_id text not null,
  requester_principal_id text not null,
  requester_principal_digest text not null
    check (requester_principal_digest ~ '^sha256:[0-9a-f]{64}$'),
  requester_grant_id text not null,
  requester_grant_digest text not null
    check (requester_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  reviewer_selector_ids text[] not null,
  decision_policy_id text not null,
  decision_policy_digest text not null check (
    decision_policy_digest ~ '^sha256:[0-9a-f]{64}$'
  ),
  created_at timestamptz not null,
  expires_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, request_id),
  foreign key (installation_id, stack_id, layer_id, decision_policy_id)
    references xfactory_runtime_v2.approval_decision_policies
      (installation_id, stack_id, layer_id, policy_id),
  check (expires_at > created_at),
  check (
    (authority_scope_kind = 'installation'
      and authority_stack_id = '' and authority_layer_id = '')
    or (authority_scope_kind = 'stack'
      and authority_stack_id <> '' and authority_layer_id = '')
    or (authority_scope_kind = 'layer'
      and authority_stack_id <> '' and authority_layer_id <> '')
  )
);

create table if not exists xfactory_runtime_v2.approval_decisions (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  decision_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  digest_profile text not null check (digest_profile = 'xfactory-canonical-json-v1'),
  request_id text not null,
  request_digest text not null check (request_digest ~ '^sha256:[0-9a-f]{64}$'),
  target_type text not null,
  target_id text not null,
  target_digest text not null check (target_digest ~ '^sha256:[0-9a-f]{64}$'),
  target_stack_id text not null,
  target_layer_id text not null,
  requested_action text not null,
  authority_scope_kind text not null check (
    authority_scope_kind in ('installation', 'installation_admin', 'stack', 'layer')
  ),
  authority_stack_id text not null,
  authority_layer_id text not null,
  decision_policy_id text not null,
  decision_policy_digest text not null check (
    decision_policy_digest ~ '^sha256:[0-9a-f]{64}$'
  ),
  reviewer_selector_id text not null,
  reviewer_stack_id text not null,
  reviewer_layer_id text not null,
  reviewer_principal_id text not null,
  reviewer_principal_digest text not null
    check (reviewer_principal_digest ~ '^sha256:[0-9a-f]{64}$'),
  reviewer_grant_id text not null,
  reviewer_grant_digest text not null
    check (reviewer_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  decision text not null check (
    decision in ('approve', 'reject')
  ),
  rationale_ref text,
  decided_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, decision_id),
  foreign key (installation_id, stack_id, layer_id, request_id)
    references xfactory_runtime_v2.approval_requests
      (installation_id, stack_id, layer_id, request_id),
  check (
    (authority_scope_kind in ('installation', 'installation_admin')
      and authority_stack_id = '' and authority_layer_id = '')
    or (authority_scope_kind = 'stack'
      and authority_stack_id <> '' and authority_layer_id = '')
    or (authority_scope_kind = 'layer'
      and authority_stack_id <> '' and authority_layer_id <> '')
  )
);

create table if not exists xfactory_runtime_v2.approval_supersession_events (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  event_id text not null,
  event_digest text not null check (event_digest ~ '^sha256:[0-9a-f]{64}$'),
  event_type text not null check (event_type in ('expired', 'cancelled', 'revoked')),
  target_kind text not null check (target_kind in ('request', 'decision')),
  target_id text not null,
  target_digest text not null check (target_digest ~ '^sha256:[0-9a-f]{64}$'),
  authority_scope_kind text not null check (
    authority_scope_kind in ('installation', 'installation_admin', 'stack', 'layer')
  ),
  authority_stack_id text not null,
  authority_layer_id text not null,
  issuer_stack_id text not null,
  issuer_layer_id text not null,
  issuer_principal_id text not null,
  issuer_principal_digest text not null
    check (issuer_principal_digest ~ '^sha256:[0-9a-f]{64}$'),
  issuer_grant_id text not null,
  issuer_grant_digest text not null
    check (issuer_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  reason text not null,
  effective_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, event_id),
  check (
    (authority_scope_kind in ('installation', 'installation_admin')
      and authority_stack_id = '' and authority_layer_id = '')
    or (authority_scope_kind = 'stack'
      and authority_stack_id <> '' and authority_layer_id = '')
    or (authority_scope_kind = 'layer'
      and authority_stack_id <> '' and authority_layer_id <> '')
  )
);

create table if not exists xfactory_runtime_v2.governed_projections (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  projection_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_stack_id text not null,
  source_layer_id text not null,
  source_resource_type text not null,
  source_resource_id text not null,
  source_resource_digest text not null
    check (source_resource_digest ~ '^sha256:[0-9a-f]{64}$'),
  target_resource_type text not null,
  target_resource_id text not null,
  target_resource_digest text not null
    check (target_resource_digest ~ '^sha256:[0-9a-f]{64}$'),
  binding_id text not null,
  operation_id text not null,
  created_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, projection_id)
);

create table if not exists xfactory_runtime_v2.operation_authorizations (
  installation_id text not null,
  operation_id text not null,
  record_digest text not null check (record_digest ~ '^sha256:[0-9a-f]{64}$'),
  digest_profile text not null check (digest_profile = 'xfactory-canonical-json-v1'),
  binding_id text not null,
  binding_digest text not null check (binding_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_stack_id text not null,
  source_layer_id text not null,
  source_resource_type text not null,
  source_resource_id text not null,
  source_resource_digest text not null
    check (source_resource_digest ~ '^sha256:[0-9a-f]{64}$'),
  target_stack_id text not null,
  target_layer_id text not null,
  target_resource_type text not null,
  target_resource_id text not null,
  target_resource_digest text not null
    check (target_resource_digest ~ '^sha256:[0-9a-f]{64}$'),
  action text not null check (action = 'project_resource'),
  purpose text not null,
  actor_stack_id text not null,
  actor_layer_id text not null,
  actor_principal_id text not null,
  actor_principal_digest text not null
    check (actor_principal_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_grant_id text not null,
  source_grant_digest text not null check (source_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  target_acceptance_grant_id text not null,
  target_acceptance_grant_digest text not null
    check (target_acceptance_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  trust_anchor_id text not null,
  trust_anchor_digest text not null check (trust_anchor_digest ~ '^sha256:[0-9a-f]{64}$'),
  transaction_id text not null,
  target_result_type text not null,
  target_result_id text not null,
  target_result_digest text,
  authorized_at timestamptz not null,
  primary key (installation_id, operation_id),
  foreign key (installation_id, binding_id)
    references xfactory_runtime_v2.cross_layer_bindings(installation_id, binding_id)
);

create table if not exists xfactory_runtime_v2.traceability_edges (
  installation_id text not null,
  stack_id text not null,
  layer_id text not null,
  edge_id text not null,
  edge_digest text not null check (edge_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_stack_id text not null,
  source_layer_id text not null,
  source_type text not null,
  source_id text not null,
  source_digest text not null check (source_digest ~ '^sha256:[0-9a-f]{64}$'),
  target_stack_id text not null,
  target_layer_id text not null,
  target_type text not null,
  target_id text not null,
  target_digest text not null check (target_digest ~ '^sha256:[0-9a-f]{64}$'),
  relation text not null,
  creator_stack_id text not null,
  creator_layer_id text not null,
  creator_principal_id text not null,
  creator_principal_digest text not null
    check (creator_principal_digest ~ '^sha256:[0-9a-f]{64}$'),
  creator_grant_id text not null,
  creator_grant_digest text not null
    check (creator_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  operation_id text,
  operation_digest text check (
    operation_digest is null or operation_digest ~ '^sha256:[0-9a-f]{64}$'
  ),
  binding_id text,
  binding_digest text check (
    binding_digest is null or binding_digest ~ '^sha256:[0-9a-f]{64}$'
  ),
  grant_refs jsonb,
  created_at timestamptz not null,
  primary key (installation_id, stack_id, layer_id, edge_id),
  check (
    (
      source_stack_id = target_stack_id
      and source_layer_id = target_layer_id
      and operation_id is null
      and binding_id is null
      and grant_refs is null
    )
    or (
      (source_stack_id <> target_stack_id or source_layer_id <> target_layer_id)
      and operation_id is not null
      and operation_digest is not null
      and binding_id is not null
      and binding_digest is not null
      and jsonb_typeof(grant_refs) = 'array'
      and jsonb_array_length(grant_refs) > 0
    )
  )
);

create or replace function xfactory_runtime_v2.reject_immutable_mutation()
returns trigger
language plpgsql
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
begin
  raise exception using
    errcode = '55000',
    message = 'HGR-IMMUTABLE-RECORD: update and delete are forbidden';
end
$function$;

create or replace function xfactory_runtime_v2.reject_ungoverned_projection_mutation()
returns trigger
language plpgsql
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
begin
  if current_setting('xfactory.governed_projection_write', true) is distinct from 'on' then
    raise exception using
      errcode = '55000',
      message = 'HGR-LIFECYCLE-PROJECTION-GOVERNED-ONLY';
  end if;
  return case when tg_op = 'DELETE' then old else new end;
end
$function$;

create or replace function xfactory_runtime_v2.reconcile_lifecycle_projection()
returns trigger
language plpgsql
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  event_state text;
begin
  if new.latest_event_id is null or new.latest_event_digest is null then
    raise exception using
      errcode = '55000',
      message = 'HGR-LIFECYCLE-PROJECTION-UNRECONCILED: projection requires a lifecycle event';
  end if;

  case new.entity_kind
    when 'installation' then
      if new.stack_id <> '' or new.layer_id <> ''
         or new.entity_id <> new.installation_id then
        raise exception using
          errcode = '55000',
          message = 'HGR-LIFECYCLE-PROJECTION-UNRECONCILED: installation projection scope does not reconcile';
      end if;
      select lifecycle.to_state
      into event_state
      from xfactory_runtime_v2.installation_lifecycle_events lifecycle
      where lifecycle.installation_id = new.installation_id
        and lifecycle.event_id = new.latest_event_id
        and lifecycle.event_digest = new.latest_event_digest;
    when 'stack' then
      if new.layer_id <> '' or new.entity_id <> new.stack_id then
        raise exception using
          errcode = '55000',
          message = 'HGR-LIFECYCLE-PROJECTION-UNRECONCILED: stack projection scope does not reconcile';
      end if;
      select lifecycle.to_state
      into event_state
      from xfactory_runtime_v2.stack_lifecycle_events lifecycle
      where lifecycle.installation_id = new.installation_id
        and lifecycle.stack_id = new.stack_id
        and lifecycle.event_id = new.latest_event_id
        and lifecycle.event_digest = new.latest_event_digest;
    when 'layer' then
      if new.entity_id <> new.layer_id then
        raise exception using
          errcode = '55000',
          message = 'HGR-LIFECYCLE-PROJECTION-UNRECONCILED: layer projection scope does not reconcile';
      end if;
      select lifecycle.to_state
      into event_state
      from xfactory_runtime_v2.layer_lifecycle_events lifecycle
      where lifecycle.installation_id = new.installation_id
        and lifecycle.stack_id = new.stack_id
        and lifecycle.layer_id = new.layer_id
        and lifecycle.event_id = new.latest_event_id
        and lifecycle.event_digest = new.latest_event_digest;
    when 'principal' then
      select lifecycle.to_state
      into event_state
      from xfactory_runtime_v2.principal_lifecycle_events lifecycle
      where lifecycle.installation_id = new.installation_id
        and lifecycle.stack_id = new.stack_id
        and lifecycle.layer_id = new.layer_id
        and lifecycle.principal_id = new.entity_id
        and lifecycle.event_id = new.latest_event_id
        and lifecycle.event_digest = new.latest_event_digest;
    else
      event_state := null;
  end case;

  if event_state is null or event_state <> new.derived_state then
    raise exception using
      errcode = '55000',
      message = 'HGR-LIFECYCLE-PROJECTION-UNRECONCILED: projection does not reconcile with lifecycle event';
  end if;
  return new;
end
$function$;

do $immutable_triggers$
declare
  relation_name text;
  trigger_name text;
begin
  foreach relation_name in array array[
    'installation_registrations',
    'stack_registrations',
    'layer_registrations',
    'installation_lifecycle_events',
    'stack_lifecycle_events',
    'layer_lifecycle_events',
    'principals',
    'principal_lifecycle_events',
    'database_principal_bindings',
    'database_principal_binding_revocations',
    'installation_trust_anchors',
    'installation_trust_anchor_events',
    'authority_grants',
    'authority_grant_revocations',
    'cross_layer_bindings',
    'cross_layer_binding_revocations',
    'artifact_records',
    'artifact_lifecycle_events',
    'approval_decision_policies',
    'approval_requests',
    'approval_decisions',
    'approval_supersession_events',
    'governed_projections',
    'operation_authorizations',
    'traceability_edges'
  ]
  loop
    trigger_name := relation_name || '_immutable';
    if not exists (
      select 1
      from pg_trigger
      where tgrelid = format('xfactory_runtime_v2.%I', relation_name)::regclass
        and tgname = trigger_name
        and not tgisinternal
    ) then
      execute format(
        'create trigger %I before update or delete on xfactory_runtime_v2.%I '
        'for each row execute function xfactory_runtime_v2.reject_immutable_mutation()',
        trigger_name,
        relation_name
      );
    end if;
  end loop;
end
$immutable_triggers$;

drop trigger if exists lifecycle_projections_governed_only
  on xfactory_runtime_v2.lifecycle_projections;
create trigger lifecycle_projections_governed_only
before update or delete on xfactory_runtime_v2.lifecycle_projections
for each row execute function
  xfactory_runtime_v2.reject_ungoverned_projection_mutation();

drop trigger if exists lifecycle_projections_reconciled
  on xfactory_runtime_v2.lifecycle_projections;
create trigger lifecycle_projections_reconciled
before insert or update on xfactory_runtime_v2.lifecycle_projections
for each row execute function
  xfactory_runtime_v2.reconcile_lifecycle_projection();

create or replace function xfactory_runtime_v2.scope_contains(
  parent_kind text,
  parent_stack text,
  parent_layer text,
  child_kind text,
  child_stack text,
  child_layer text
)
returns boolean
language sql
immutable
strict
set search_path = pg_catalog
as $function$
  select case parent_kind
    when 'installation' then true
    when 'stack' then
      child_kind in ('stack', 'layer') and child_stack = parent_stack
    when 'layer' then
      child_kind = 'layer'
      and child_stack = parent_stack
      and child_layer = parent_layer
    else false
  end
$function$;

create or replace function xfactory_runtime_v2.principal_is_active_at(
  requested_installation_id text,
  requested_stack_id text,
  requested_layer_id text,
  requested_principal_id text,
  evaluation_time timestamptz
)
returns boolean
language sql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select coalesce(
    (
      select lifecycle.to_state
      from xfactory_runtime_v2.principal_lifecycle_events lifecycle
      where lifecycle.installation_id = principal.installation_id
        and lifecycle.stack_id = principal.stack_id
        and lifecycle.layer_id = principal.layer_id
        and lifecycle.principal_id = principal.principal_id
        and lifecycle.occurred_at <= evaluation_time
      order by lifecycle.occurred_at desc, lifecycle.event_id collate "C" desc
      limit 1
    ),
    principal.initial_state
  ) = 'active'
  from xfactory_runtime_v2.principals principal
  where principal.installation_id = requested_installation_id
    and principal.stack_id = requested_stack_id
    and principal.layer_id = requested_layer_id
    and principal.principal_id = requested_principal_id
$function$;

create or replace function xfactory_runtime_v2.anchor_is_active(
  requested_installation_id text,
  requested_anchor_id text,
  evaluation_time timestamptz
)
returns boolean
language plpgsql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  genesis_anchor xfactory_runtime_v2.installation_trust_anchors%rowtype;
  successor_anchor xfactory_runtime_v2.installation_trust_anchors%rowtype;
  authority_grant xfactory_runtime_v2.authority_grants%rowtype;
  authority_principal xfactory_runtime_v2.principals%rowtype;
  anchor_event record;
  active_anchor_id text;
  active_anchor_digest text;
  active_policy_repository text;
  active_policy_commit text;
  active_policy_ref text;
  active_policy_digest text;
  previous_kind text;
  previous_id text;
  previous_digest text;
  expected_action text;
  expected_event_digest text;
  event_payload jsonb;
begin
  if (
    select count(*)
    from xfactory_runtime_v2.installation_trust_anchors anchor_record
    where anchor_record.installation_id = requested_installation_id
      and anchor_record.anchor_kind = 'genesis'
  ) <> 1 then
    return false;
  end if;

  select anchor_record.*
  into strict genesis_anchor
  from xfactory_runtime_v2.installation_trust_anchors anchor_record
  where anchor_record.installation_id = requested_installation_id
    and anchor_record.anchor_kind = 'genesis';
  if genesis_anchor.effective_at > evaluation_time then
    return false;
  end if;

  active_anchor_id := genesis_anchor.anchor_id;
  active_anchor_digest := genesis_anchor.record_digest;
  active_policy_repository := genesis_anchor.policy_repository;
  active_policy_commit := genesis_anchor.policy_commit;
  active_policy_ref := genesis_anchor.policy_ref;
  active_policy_digest := genesis_anchor.policy_digest;
  previous_kind := 'registration';
  previous_id := genesis_anchor.anchor_id;
  previous_digest := genesis_anchor.record_digest;

  for anchor_event in
    select event_record.*
    from xfactory_runtime_v2.installation_trust_anchor_events event_record
    where event_record.installation_id = requested_installation_id
      and event_record.effective_at <= evaluation_time
    order by event_record.effective_at, event_record.event_id collate "C"
  loop
    if active_anchor_id is null
       or anchor_event.predecessor_kind <> previous_kind
       or anchor_event.predecessor_id <> previous_id
       or anchor_event.predecessor_digest <> previous_digest
       or anchor_event.from_anchor_id <> active_anchor_id
       or anchor_event.from_anchor_digest <> active_anchor_digest then
      return false;
    end if;

    select principal.*
    into authority_principal
    from xfactory_runtime_v2.principals principal
    where principal.installation_id = requested_installation_id
      and principal.stack_id = anchor_event.authority_principal_stack_id
      and principal.layer_id = anchor_event.authority_principal_layer_id
      and principal.principal_id = anchor_event.authority_principal_id
      and principal.record_digest = anchor_event.authority_principal_digest;
    if not found or not xfactory_runtime_v2.principal_is_active_at(
      requested_installation_id,
      anchor_event.authority_principal_stack_id,
      anchor_event.authority_principal_layer_id,
      anchor_event.authority_principal_id,
      anchor_event.effective_at
    ) then
      return false;
    end if;

    select grant_record.*
    into authority_grant
    from xfactory_runtime_v2.authority_grants grant_record
    where grant_record.installation_id = requested_installation_id
      and grant_record.grant_id = anchor_event.authority_grant_id
      and grant_record.record_digest = anchor_event.authority_grant_digest;
    expected_action := case anchor_event.event_type
      when 'rotate' then 'rotate_trust_anchor'
      when 'revoke' then 'revoke_trust_anchor'
    end;
    if not found
       or authority_grant.grant_kind <> 'root'
       or authority_grant.action <> expected_action
       or authority_grant.grantee_stack_id <>
         anchor_event.authority_principal_stack_id
       or authority_grant.grantee_layer_id <>
         anchor_event.authority_principal_layer_id
       or authority_grant.grantee_principal_id <>
         anchor_event.authority_principal_id
       or authority_grant.grantee_principal_digest <>
         anchor_event.authority_principal_digest
       or authority_grant.trust_anchor_id <> active_anchor_id
       or authority_grant.trust_anchor_digest <> active_anchor_digest
       or authority_grant.scope_kind <> 'installation'
       or authority_grant.scope_stack_id <> ''
       or authority_grant.scope_layer_id <> ''
       or authority_grant.resource_type <> 'trust_anchor'
       or authority_grant.resource_id <> active_anchor_id
       or authority_grant.resource_digest <> active_anchor_digest
       or authority_grant.policy_repository <> active_policy_repository
       or authority_grant.policy_commit <> active_policy_commit
       or authority_grant.policy_ref <> active_policy_ref
       or authority_grant.policy_digest <> active_policy_digest
       or authority_grant.starts_at > anchor_event.effective_at
       or authority_grant.expires_at <= anchor_event.effective_at
       or authority_grant.issued_at > anchor_event.effective_at
       or exists (
         select 1
         from xfactory_runtime_v2.authority_grant_revocations revocation
         where revocation.installation_id = authority_grant.installation_id
           and revocation.grant_id = authority_grant.grant_id
           and revocation.grant_digest = authority_grant.record_digest
           and revocation.effective_at <= anchor_event.effective_at
       ) then
      return false;
    end if;

    event_payload := jsonb_build_object(
      'schema_version', 1,
      'kind', 'openxfactory-installation-trust-anchor-event',
      'event_id', anchor_event.event_id,
      'record_digest_profile', anchor_event.digest_profile,
      'installation_id', anchor_event.installation_id,
      'predecessor_ref', jsonb_build_object(
        'kind', anchor_event.predecessor_kind,
        'id', anchor_event.predecessor_id,
        'record_digest', anchor_event.predecessor_digest
      ),
      'event_type', anchor_event.event_type,
      'predecessor_anchor_ref', jsonb_build_object(
        'installation_id', anchor_event.installation_id,
        'anchor_id', anchor_event.from_anchor_id,
        'record_digest', anchor_event.from_anchor_digest
      ),
      'authorizing_principal_ref', jsonb_build_object(
        'scope', case authority_principal.scope_kind
          when 'layer' then jsonb_build_object(
            'scope_kind', 'layer',
            'installation_id', authority_principal.installation_id,
            'stack_id', authority_principal.stack_id,
            'layer_id', authority_principal.layer_id
          )
          else jsonb_build_object(
            'scope_kind', 'installation_admin',
            'installation_id', authority_principal.installation_id
          )
        end,
        'principal_id', authority_principal.principal_id,
        'record_digest', authority_principal.record_digest
      ),
      'authorizing_grant_ref', jsonb_build_object(
        'installation_id', authority_grant.installation_id,
        'grant_id', authority_grant.grant_id,
        'record_digest', authority_grant.record_digest
      ),
      'effective_at', to_char(
        anchor_event.effective_at at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
      ),
      'occurred_at', to_char(
        anchor_event.occurred_at at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
      ),
      'reason', anchor_event.reason
    );

    if anchor_event.event_type = 'rotate' then
      select anchor_record.*
      into successor_anchor
      from xfactory_runtime_v2.installation_trust_anchors anchor_record
      where anchor_record.installation_id = requested_installation_id
        and anchor_record.anchor_id = anchor_event.to_anchor_id
        and anchor_record.record_digest = anchor_event.to_anchor_digest
        and anchor_record.anchor_kind = 'rotated';
      if not found
         or successor_anchor.effective_at > anchor_event.effective_at then
        return false;
      end if;
      event_payload := event_payload || jsonb_build_object(
        'successor_anchor_ref', jsonb_build_object(
          'installation_id', anchor_event.installation_id,
          'anchor_id', anchor_event.to_anchor_id,
          'record_digest', anchor_event.to_anchor_digest
        )
      );
    elsif anchor_event.to_anchor_id is not null
       or anchor_event.to_anchor_digest is not null then
      return false;
    end if;

    expected_event_digest :=
      xfactory_runtime_v2.canonical_record_digest(event_payload);
    if expected_event_digest <> anchor_event.record_digest then
      return false;
    end if;

    if anchor_event.event_type = 'rotate' then
      active_anchor_id := successor_anchor.anchor_id;
      active_anchor_digest := successor_anchor.record_digest;
      active_policy_repository := successor_anchor.policy_repository;
      active_policy_commit := successor_anchor.policy_commit;
      active_policy_ref := successor_anchor.policy_ref;
      active_policy_digest := successor_anchor.policy_digest;
    else
      active_anchor_id := null;
      active_anchor_digest := null;
      active_policy_repository := null;
      active_policy_commit := null;
      active_policy_ref := null;
      active_policy_digest := null;
    end if;
    previous_kind := 'event';
    previous_id := anchor_event.event_id;
    previous_digest := anchor_event.record_digest;
  end loop;

  return active_anchor_id = requested_anchor_id
    and exists (
      select 1
      from xfactory_runtime_v2.installation_trust_anchors requested_anchor
      where requested_anchor.installation_id = requested_installation_id
        and requested_anchor.anchor_id = requested_anchor_id
        and requested_anchor.record_digest = active_anchor_digest
        and requested_anchor.effective_at <= evaluation_time
    );
end
$function$;

create or replace function xfactory_runtime_v2.active_authority_chain(
  requested_installation_id text,
  requested_grant_id text,
  requested_action text,
  requested_scope_kind text,
  requested_stack_id text,
  requested_layer_id text,
  requested_principal_id text default null,
  evaluation_time timestamptz default transaction_timestamp()
)
returns table (
  root_anchor_id text,
  root_anchor_digest text,
  leaf_grant_digest text,
  leaf_principal_id text
)
language sql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  with recursive chain as (
    select
      g.*,
      array[g.grant_id]::text[] as path,
      true as link_valid,
      0 as depth
    from xfactory_runtime_v2.authority_grants g
    where g.installation_id = requested_installation_id
      and g.grant_id = requested_grant_id

    union all

    select
      parent.*,
      child.path || parent.grant_id,
      child.link_valid
        and child.grant_kind = 'delegated'
        and child.issuer_grant_digest = parent.record_digest
        and parent.action = 'issue_grant'
        and xfactory_runtime_v2.scope_contains(
          parent.scope_kind,
          parent.scope_stack_id,
          parent.scope_layer_id,
          child.scope_kind,
          child.scope_stack_id,
          child.scope_layer_id
        )
        and child.starts_at >= parent.starts_at
        and child.expires_at <= parent.expires_at,
      child.depth + 1
    from chain child
    join xfactory_runtime_v2.authority_grants parent
      on parent.installation_id = child.installation_id
     and parent.grant_id = child.issuer_grant_id
    where child.grant_kind = 'delegated'
      and child.depth < 63
      and not parent.grant_id = any(child.path)
  ),
  evaluated as (
    select
      c.*,
      not exists (
        select 1
        from xfactory_runtime_v2.authority_grant_revocations r
        where r.installation_id = c.installation_id
          and r.grant_id = c.grant_id
          and r.grant_digest = c.record_digest
          and r.effective_at <= evaluation_time
      ) as unrevoked,
      exists (
        select 1
        from xfactory_runtime_v2.principals p
        where p.installation_id = c.installation_id
          and p.stack_id = c.grantee_stack_id
          and p.layer_id = c.grantee_layer_id
          and p.principal_id = c.grantee_principal_id
          and p.record_digest = c.grantee_principal_digest
          and xfactory_runtime_v2.principal_is_active_at(
            p.installation_id, p.stack_id, p.layer_id, p.principal_id,
            evaluation_time
          )
      ) as principal_active
    from chain c
  ),
  leaf as (
    select *
    from evaluated
    where grant_id = requested_grant_id
      and action = requested_action
      and xfactory_runtime_v2.scope_contains(
        scope_kind,
        scope_stack_id,
        scope_layer_id,
        requested_scope_kind,
        requested_stack_id,
        requested_layer_id
      )
      and (
        requested_principal_id is null
        or grantee_principal_id = requested_principal_id
      )
  ),
  root as (
    select *
    from evaluated
    where grant_kind = 'root'
      and trust_anchor_id is not null
      and scope_kind = 'installation'
      and scope_stack_id = ''
      and scope_layer_id = ''
      and exists (
        select 1
        from xfactory_runtime_v2.installation_trust_anchors anchor_record
        where anchor_record.installation_id = evaluated.installation_id
          and anchor_record.anchor_id = evaluated.trust_anchor_id
          and anchor_record.record_digest = evaluated.trust_anchor_digest
      )
      and xfactory_runtime_v2.anchor_is_active(
        installation_id,
        trust_anchor_id,
        evaluation_time
      )
  )
  select
    root.trust_anchor_id,
    root.trust_anchor_digest,
    leaf.record_digest,
    leaf.grantee_principal_id
  from leaf
  join root on true
  where leaf.starts_at <= evaluation_time
    and leaf.expires_at > evaluation_time
    and leaf.unrevoked
    and leaf.principal_active
    and root.starts_at <= evaluation_time
    and root.expires_at > evaluation_time
    and root.unrevoked
    and root.principal_active
    and not exists (
      select 1
      from evaluated invalid
      where not invalid.link_valid
        or invalid.starts_at > evaluation_time
        or invalid.expires_at <= evaluation_time
        or not invalid.unrevoked
        or not invalid.principal_active
    )
    and (select count(*) from root) = 1
$function$;

create or replace function xfactory_runtime_v2.enforce_cross_layer_binding_creation()
returns trigger
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  creator_principal xfactory_runtime_v2.principals%rowtype;
  acceptance_principal xfactory_runtime_v2.principals%rowtype;
begin
  new.created_at := transaction_timestamp();
  if new.created_at < new.starts_at
     or new.created_at >= new.expires_at then
    raise exception using
      errcode = '42501',
      message = 'HGR-BINDING-CREATION-TIME';
  end if;

  if not exists (
    select 1
    from xfactory_runtime_v2.principals principal
    where principal.installation_id = new.installation_id
      and principal.stack_id = new.creator_principal_stack_id
      and principal.layer_id = new.creator_principal_layer_id
      and principal.principal_id = new.creator_principal_id
      and principal.record_digest = new.creator_principal_digest
      and xfactory_runtime_v2.principal_is_active_at(
        principal.installation_id, principal.stack_id, principal.layer_id,
        principal.principal_id, new.created_at
      )
  ) or not exists (
    select 1
    from xfactory_runtime_v2.active_authority_chain(
      new.installation_id,
      new.creator_grant_id,
      'create_binding',
      'layer',
      new.source_stack_id,
      new.source_layer_id,
      new.creator_principal_id,
      new.created_at
    )
  ) or not exists (
    select 1
    from xfactory_runtime_v2.authority_grants creator_grant
    where creator_grant.installation_id = new.installation_id
      and creator_grant.grant_id = new.creator_grant_id
      and creator_grant.record_digest = new.creator_grant_digest
      and creator_grant.grantee_stack_id = new.creator_principal_stack_id
      and creator_grant.grantee_layer_id = new.creator_principal_layer_id
      and creator_grant.grantee_principal_id = new.creator_principal_id
      and creator_grant.grantee_principal_digest = new.creator_principal_digest
      and creator_grant.action = 'create_binding'
      and creator_grant.scope_kind = 'layer'
      and creator_grant.scope_stack_id = new.source_stack_id
      and creator_grant.scope_layer_id = new.source_layer_id
      and creator_grant.resource_type = new.source_resource_type
      and creator_grant.resource_id = new.source_resource_id
      and creator_grant.resource_digest is not distinct from
        new.source_resource_digest
      and creator_grant.policy_ref <> ''
      and creator_grant.policy_digest ~ '^sha256:[0-9a-f]{64}$'
  ) then
    raise exception using
      errcode = '42501',
      message = 'HGR-BINDING-CREATION-AUTHORITY';
  end if;

  if not exists (
    select 1
    from xfactory_runtime_v2.principals principal
    where principal.installation_id = new.installation_id
      and principal.stack_id = new.target_acceptance_principal_stack_id
      and principal.layer_id = new.target_acceptance_principal_layer_id
      and principal.principal_id = new.target_acceptance_principal_id
      and principal.record_digest = new.target_acceptance_principal_digest
      and xfactory_runtime_v2.principal_is_active_at(
        principal.installation_id, principal.stack_id, principal.layer_id,
        principal.principal_id, new.created_at
      )
  ) or not exists (
    select 1
    from xfactory_runtime_v2.active_authority_chain(
      new.installation_id,
      new.target_acceptance_grant_id,
      'accept_cross_layer',
      'layer',
      new.target_stack_id,
      new.target_layer_id,
      new.target_acceptance_principal_id,
      new.created_at
    )
  ) or not exists (
    select 1
    from xfactory_runtime_v2.authority_grants acceptance_grant
    where acceptance_grant.installation_id = new.installation_id
      and acceptance_grant.grant_id = new.target_acceptance_grant_id
      and acceptance_grant.record_digest = new.target_acceptance_grant_digest
      and acceptance_grant.grantee_stack_id =
        new.target_acceptance_principal_stack_id
      and acceptance_grant.grantee_layer_id =
        new.target_acceptance_principal_layer_id
      and acceptance_grant.grantee_principal_id =
        new.target_acceptance_principal_id
      and acceptance_grant.grantee_principal_digest =
        new.target_acceptance_principal_digest
      and acceptance_grant.action = 'accept_cross_layer'
      and acceptance_grant.scope_kind = 'layer'
      and acceptance_grant.scope_stack_id = new.target_stack_id
      and acceptance_grant.scope_layer_id = new.target_layer_id
      and acceptance_grant.resource_type = new.target_resource_type
      and acceptance_grant.resource_id = new.target_resource_id
      and acceptance_grant.resource_digest is not distinct from
        new.target_resource_digest
      and acceptance_grant.policy_ref <> ''
      and acceptance_grant.policy_digest ~ '^sha256:[0-9a-f]{64}$'
  ) then
    raise exception using
      errcode = '42501',
      message = 'HGR-BINDING-TARGET-ACCEPTANCE';
  end if;

  select principal.*
  into strict creator_principal
  from xfactory_runtime_v2.principals principal
  where principal.installation_id = new.installation_id
    and principal.stack_id = new.creator_principal_stack_id
    and principal.layer_id = new.creator_principal_layer_id
    and principal.principal_id = new.creator_principal_id
    and principal.record_digest = new.creator_principal_digest;
  select principal.*
  into strict acceptance_principal
  from xfactory_runtime_v2.principals principal
  where principal.installation_id = new.installation_id
    and principal.stack_id = new.target_acceptance_principal_stack_id
    and principal.layer_id = new.target_acceptance_principal_layer_id
    and principal.principal_id = new.target_acceptance_principal_id
    and principal.record_digest = new.target_acceptance_principal_digest;

  new.record_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'schema_version', 1,
      'kind', 'openxfactory-cross-layer-binding',
      'binding_id', new.binding_id,
      'record_digest_profile', new.digest_profile,
      'source_scope', xfactory_runtime_v2.governed_scope_json(
        'layer', new.installation_id,
        new.source_stack_id, new.source_layer_id
      ),
      'target_scope', xfactory_runtime_v2.governed_scope_json(
        'layer', new.installation_id,
        new.target_stack_id, new.target_layer_id
      ),
      'source_resource', xfactory_runtime_v2.resource_reference_json(
        new.installation_id, 'layer',
        new.source_stack_id, new.source_layer_id,
        new.source_resource_type, new.source_resource_id,
        new.source_resource_digest
      ),
      'target_resource', xfactory_runtime_v2.resource_reference_json(
        new.installation_id, 'layer',
        new.target_stack_id, new.target_layer_id,
        new.target_resource_type, new.target_resource_id,
        new.target_resource_digest
      ),
      'action', new.action,
      'purpose', new.purpose,
      'creator_principal_ref', jsonb_build_object(
        'scope', xfactory_runtime_v2.governed_scope_json(
          creator_principal.scope_kind, creator_principal.installation_id,
          creator_principal.stack_id, creator_principal.layer_id
        ),
        'principal_id', creator_principal.principal_id,
        'record_digest', creator_principal.record_digest
      ),
      'creator_grant_ref', jsonb_build_object(
        'installation_id', new.installation_id,
        'grant_id', new.creator_grant_id,
        'record_digest', new.creator_grant_digest
      ),
      'target_acceptance_principal_ref', jsonb_build_object(
        'scope', xfactory_runtime_v2.governed_scope_json(
          acceptance_principal.scope_kind,
          acceptance_principal.installation_id,
          acceptance_principal.stack_id,
          acceptance_principal.layer_id
        ),
        'principal_id', acceptance_principal.principal_id,
        'record_digest', acceptance_principal.record_digest
      ),
      'target_acceptance_grant_ref', jsonb_build_object(
        'installation_id', new.installation_id,
        'grant_id', new.target_acceptance_grant_id,
        'record_digest', new.target_acceptance_grant_digest
      ),
      'starts_at', to_char(
        new.starts_at at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
      ),
      'expires_at', to_char(
        new.expires_at at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
      ),
      'created_at', to_char(
        new.created_at at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
      )
    )
  );

  return new;
end
$function$;

drop trigger if exists cross_layer_bindings_creation_authorized
  on xfactory_runtime_v2.cross_layer_bindings;
create trigger cross_layer_bindings_creation_authorized
before insert on xfactory_runtime_v2.cross_layer_bindings
for each row execute function
  xfactory_runtime_v2.enforce_cross_layer_binding_creation();

create or replace function xfactory_runtime_v2.principal_is_active(
  requested_installation_id text,
  requested_stack_id text,
  requested_layer_id text,
  requested_principal_id text
)
returns boolean
language sql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select exists (
    select 1
    from xfactory_runtime_v2.principals p
    join xfactory_runtime_v2.lifecycle_projections projection
      on projection.entity_kind = 'principal'
     and projection.installation_id = p.installation_id
     and projection.stack_id = p.stack_id
     and projection.layer_id = p.layer_id
     and projection.entity_id = p.principal_id
     and projection.derived_state = 'active'
    where p.installation_id = requested_installation_id
      and p.stack_id = requested_stack_id
      and p.layer_id = requested_layer_id
      and p.principal_id = requested_principal_id
  )
$function$;

create or replace function xfactory_runtime_v2.layer_is_active(
  requested_installation_id text,
  requested_stack_id text,
  requested_layer_id text
)
returns boolean
language sql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select exists (
    select 1
    from xfactory_runtime_v2.layer_registrations layer
    join xfactory_runtime_v2.lifecycle_projections projection
      on projection.entity_kind = 'layer'
     and projection.installation_id = layer.installation_id
     and projection.stack_id = layer.stack_id
     and projection.layer_id = layer.layer_id
     and projection.entity_id = layer.layer_id
     and projection.derived_state = 'active'
    where layer.installation_id = requested_installation_id
      and layer.stack_id = requested_stack_id
      and layer.layer_id = requested_layer_id
  )
$function$;

create or replace function xfactory_runtime_api_v2.current_scope_matches(
  requested_installation_id text,
  requested_stack_id text,
  requested_layer_id text
)
returns boolean
language sql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select
    current_setting('xfactory.installation_id', true) = requested_installation_id
    and current_setting('xfactory.stack_id', true) = requested_stack_id
    and current_setting('xfactory.layer_id', true) = requested_layer_id
    and exists (
      select 1
      from xfactory_runtime_v2.database_principal_bindings binding
      where binding.session_user_name = session_user::text
        and binding.installation_id = requested_installation_id
        and binding.stack_id = requested_stack_id
        and binding.layer_id = requested_layer_id
        and binding.principal_id =
          current_setting('xfactory.principal_id', true)
        and binding.creator_grant_id =
          current_setting('xfactory.grant_id', true)
        and exists (
          select 1
          from xfactory_runtime_v2.principals bound_principal
          where bound_principal.installation_id = binding.installation_id
            and bound_principal.stack_id = binding.stack_id
            and bound_principal.layer_id = binding.layer_id
            and bound_principal.principal_id = binding.principal_id
            and bound_principal.record_digest = binding.principal_digest
        )
        and exists (
          select 1
          from xfactory_runtime_v2.authority_grants creator_grant
          where creator_grant.installation_id = binding.installation_id
            and creator_grant.grant_id = binding.creator_grant_id
            and creator_grant.record_digest = binding.creator_grant_digest
            and creator_grant.action = 'assume_scope'
            and creator_grant.grantee_principal_id = binding.principal_id
            and creator_grant.grantee_principal_digest = binding.principal_digest
            and creator_grant.scope_stack_id = binding.stack_id
            and creator_grant.scope_layer_id = binding.layer_id
        )
        and not exists (
          select 1
          from xfactory_runtime_v2.database_principal_binding_revocations revoked
          where revoked.installation_id = binding.installation_id
            and revoked.stack_id = binding.stack_id
            and revoked.layer_id = binding.layer_id
            and revoked.binding_id = binding.binding_id
            and revoked.effective_at <= transaction_timestamp()
        )
        and xfactory_runtime_v2.principal_is_active(
          binding.installation_id,
          binding.stack_id,
          binding.layer_id,
          binding.principal_id
        )
        and (
          (
            binding.stack_id <> ''
            and binding.layer_id <> ''
            and xfactory_runtime_v2.layer_is_active(
              binding.installation_id,
              binding.stack_id,
              binding.layer_id
            )
            and exists (
              select 1
              from xfactory_runtime_v2.active_authority_chain(
                binding.installation_id,
                current_setting('xfactory.grant_id', true),
                'assume_scope',
                'layer',
                binding.stack_id,
                binding.layer_id,
                binding.principal_id,
                transaction_timestamp()
              )
            )
            and exists (
              select 1
              from xfactory_runtime_v2.authority_grants scope_grant
              where scope_grant.installation_id = binding.installation_id
                and scope_grant.grant_id =
                  current_setting('xfactory.grant_id', true)
                and scope_grant.resource_type = 'layer_identity'
                and scope_grant.resource_id = binding.layer_id
                and scope_grant.resource_digest is null
            )
          )
          or (
            binding.stack_id = ''
            and binding.layer_id = ''
            and binding.role_class in ('control', 'audit')
            and exists (
              select 1
              from xfactory_runtime_v2.active_authority_chain(
                binding.installation_id,
                current_setting('xfactory.grant_id', true),
                'assume_scope',
                'installation',
                '',
                '',
                binding.principal_id,
                transaction_timestamp()
              )
            )
            and exists (
              select 1
              from xfactory_runtime_v2.authority_grants scope_grant
              where scope_grant.installation_id = binding.installation_id
                and scope_grant.grant_id =
                  current_setting('xfactory.grant_id', true)
                and scope_grant.resource_type = 'policy_namespace'
                and scope_grant.resource_id = binding.installation_id
                and scope_grant.resource_digest is null
            )
          )
        )
    )
$function$;

create or replace function xfactory_runtime_api_v2.assume_scope(
  requested_installation_id text,
  requested_stack_id text,
  requested_layer_id text,
  requested_grant_id text
)
returns void
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  binding_record xfactory_runtime_v2.database_principal_bindings%rowtype;
  required_role name;
  requested_scope_kind text;
begin
  select binding.*
  into strict binding_record
  from xfactory_runtime_v2.database_principal_bindings binding
  where binding.session_user_name = session_user::text
    and binding.installation_id = requested_installation_id
    and binding.stack_id = requested_stack_id
    and binding.layer_id = requested_layer_id
    and not exists (
      select 1
      from xfactory_runtime_v2.database_principal_binding_revocations revoked
      where revoked.installation_id = binding.installation_id
        and revoked.stack_id = binding.stack_id
        and revoked.layer_id = binding.layer_id
        and revoked.binding_id = binding.binding_id
        and revoked.effective_at <= transaction_timestamp()
    );

  required_role := case binding_record.role_class
    when 'runtime' then 'xfactory_v2_runtime'::name
    when 'control' then 'xfactory_v2_control'::name
    when 'audit' then 'xfactory_v2_audit'::name
  end;
  if required_role is null
     or not pg_has_role(session_user, required_role, 'member') then
    raise exception using
      errcode = '42501',
      message = 'HGR-SCOPE-DATABASE-ROLE-MISMATCH';
  end if;
  if not xfactory_runtime_v2.principal_is_active(
    requested_installation_id,
    requested_stack_id,
    requested_layer_id,
    binding_record.principal_id
  ) then
    raise exception using
      errcode = '42501',
      message = 'HGR-SCOPE-PRINCIPAL-INACTIVE';
  end if;
  if requested_stack_id = '' and requested_layer_id = '' then
    if binding_record.role_class not in ('control', 'audit') or not exists (
      select 1
      from xfactory_runtime_v2.principals principal
      where principal.installation_id = requested_installation_id
        and principal.stack_id = ''
        and principal.layer_id = ''
        and principal.principal_id = binding_record.principal_id
        and principal.scope_kind = 'installation_admin'
    ) then
      raise exception using
        errcode = '42501',
        message = 'HGR-SCOPE-ADMIN-BINDING-MISMATCH';
    end if;
    requested_scope_kind := 'installation';
  else
    if requested_stack_id = '' or requested_layer_id = ''
       or not xfactory_runtime_v2.layer_is_active(
         requested_installation_id,
         requested_stack_id,
         requested_layer_id
       ) then
      raise exception using
        errcode = '42501',
        message = 'HGR-SCOPE-LAYER-INACTIVE';
    end if;
    requested_scope_kind := 'layer';
  end if;
  if not exists (
    select 1
    from xfactory_runtime_v2.active_authority_chain(
      requested_installation_id,
      requested_grant_id,
      'assume_scope',
      requested_scope_kind,
      requested_stack_id,
      requested_layer_id,
      binding_record.principal_id,
      transaction_timestamp()
    )
  ) or requested_grant_id <> binding_record.creator_grant_id
    or not exists (
    select 1
    from xfactory_runtime_v2.authority_grants grant_record
    where grant_record.installation_id = requested_installation_id
      and grant_record.grant_id = requested_grant_id
      and grant_record.record_digest = binding_record.creator_grant_digest
      and grant_record.grantee_principal_digest = binding_record.principal_digest
      and (
        (
          requested_scope_kind = 'layer'
          and grant_record.resource_type = 'layer_identity'
          and grant_record.resource_id = requested_layer_id
          and grant_record.resource_digest is null
        )
        or (
          requested_scope_kind = 'installation'
          and grant_record.resource_type = 'policy_namespace'
          and grant_record.resource_id = requested_installation_id
          and grant_record.resource_digest is null
        )
      )
  ) then
    raise exception using
      errcode = '42501',
      message = 'HGR-SCOPE-GRANT-INACTIVE';
  end if;

  perform set_config('xfactory.installation_id', requested_installation_id, true);
  perform set_config('xfactory.stack_id', requested_stack_id, true);
  perform set_config('xfactory.layer_id', requested_layer_id, true);
  perform set_config('xfactory.principal_id', binding_record.principal_id, true);
  perform set_config('xfactory.grant_id', requested_grant_id, true);
end
$function$;

create or replace function xfactory_runtime_api_v2.clear_scope()
returns void
language plpgsql
security definer
set search_path = pg_catalog
as $function$
begin
  perform set_config('xfactory.installation_id', '', true);
  perform set_config('xfactory.stack_id', '', true);
  perform set_config('xfactory.layer_id', '', true);
  perform set_config('xfactory.principal_id', '', true);
  perform set_config('xfactory.grant_id', '', true);
end
$function$;

create or replace function xfactory_runtime_api_v2.transition_layer(
  requested_event_id text,
  requested_installation_id text,
  requested_stack_id text,
  requested_layer_id text,
  requested_to_state text,
  requested_authority_grant_id text,
  requested_reason text
)
returns void
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  registration_record xfactory_runtime_v2.layer_registrations%rowtype;
  projection_record xfactory_runtime_v2.lifecycle_projections%rowtype;
  current_state text;
  predecessor_kind text;
  predecessor_id text;
  predecessor_digest text;
  transition_allowed boolean;
  actor_principal text;
  event_time timestamptz := transaction_timestamp();
  event_record_digest text;
  authority_grant xfactory_runtime_v2.authority_grants%rowtype;
begin
  if not (
    (
      current_setting('xfactory.stack_id', true) = ''
      and current_setting('xfactory.layer_id', true) = ''
      and xfactory_runtime_api_v2.current_scope_matches(
        requested_installation_id, '', ''
      )
    )
    or xfactory_runtime_api_v2.current_scope_matches(
      requested_installation_id,
      requested_stack_id,
      requested_layer_id
    )
  ) then
    raise exception using errcode = '42501', message = 'HGR-SCOPE-NOT-ASSUMED';
  end if;
  actor_principal := current_setting('xfactory.principal_id', true);
  if not exists (
    select 1
    from xfactory_runtime_v2.active_authority_chain(
      requested_installation_id,
      requested_authority_grant_id,
      'transition_lifecycle',
      'layer',
      requested_stack_id,
      requested_layer_id,
      actor_principal,
      event_time
    )
  ) or not exists (
    select 1
    from xfactory_runtime_v2.authority_grants transition_grant
    where transition_grant.installation_id = requested_installation_id
      and transition_grant.grant_id = requested_authority_grant_id
      and transition_grant.resource_type = 'layer_identity'
      and transition_grant.resource_id = requested_layer_id
      and transition_grant.resource_digest is null
  ) then
    raise exception using
      errcode = '42501',
      message = 'HGR-LIFECYCLE-AUTHORITY-INACTIVE';
  end if;

  select grant_record.*
  into strict authority_grant
  from xfactory_runtime_v2.authority_grants grant_record
  where grant_record.installation_id = requested_installation_id
    and grant_record.grant_id = requested_authority_grant_id;

  select *
  into strict registration_record
  from xfactory_runtime_v2.layer_registrations
  where installation_id = requested_installation_id
    and stack_id = requested_stack_id
    and layer_id = requested_layer_id
  for update;

  select *
  into projection_record
  from xfactory_runtime_v2.lifecycle_projections
  where entity_kind = 'layer'
    and installation_id = requested_installation_id
    and stack_id = requested_stack_id
    and layer_id = requested_layer_id
    and entity_id = requested_layer_id
  for update;

  if found then
    current_state := projection_record.derived_state;
    predecessor_kind := 'event';
    predecessor_id := projection_record.latest_event_id;
    predecessor_digest := projection_record.latest_event_digest;
  else
    current_state := registration_record.initial_state;
    predecessor_kind := 'registration';
    predecessor_id := registration_record.registration_id;
    predecessor_digest := registration_record.registration_digest;
  end if;

  transition_allowed := case current_state
    when 'provisioning' then requested_to_state in ('active', 'failed', 'retired')
    when 'active' then requested_to_state in ('suspended', 'failed', 'retired')
    when 'suspended' then requested_to_state in ('active', 'failed', 'retired')
    when 'failed' then requested_to_state in ('provisioning', 'retired')
    when 'retired' then false
    else false
  end;
  if not transition_allowed then
    raise exception using
      errcode = '23514',
      message = 'HCS-LIFECYCLE-TRANSITION';
  end if;

  event_record_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'schema_version', 1,
      'kind', 'openxfactory-layer-lifecycle-event',
      'event_id', requested_event_id,
      'installation_id', requested_installation_id,
      'stack_id', requested_stack_id,
      'layer_id', requested_layer_id,
      'predecessor_ref', jsonb_build_object(
        'kind', predecessor_kind,
        'id', predecessor_id,
        'digest', predecessor_digest
      ),
      'from_state', current_state,
      'to_state', requested_to_state,
      'authority_grant_id', authority_grant.grant_id,
      'authority_grant_digest', authority_grant.record_digest,
      'occurred_at', to_char(
        event_time at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
      ),
      'reason', requested_reason
    )
  );

  insert into xfactory_runtime_v2.layer_lifecycle_events (
    installation_id, stack_id, layer_id, event_id, event_digest,
    predecessor_kind, predecessor_id, predecessor_digest,
    from_state, to_state, authority_grant_id, authority_grant_digest,
    reason, occurred_at
  ) values (
    requested_installation_id, requested_stack_id, requested_layer_id,
    requested_event_id, event_record_digest, predecessor_kind,
    predecessor_id, predecessor_digest, current_state, requested_to_state,
    requested_authority_grant_id, authority_grant.record_digest,
    requested_reason, event_time
  );

  perform set_config('xfactory.governed_projection_write', 'on', true);
  insert into xfactory_runtime_v2.lifecycle_projections (
    entity_kind, installation_id, stack_id, layer_id, entity_id, derived_state,
    latest_event_id, latest_event_digest, terminal_at
  ) values (
    'layer', requested_installation_id, requested_stack_id,
    requested_layer_id, requested_layer_id, requested_to_state,
    requested_event_id, event_record_digest,
    case when requested_to_state = 'retired' then event_time end
  )
  on conflict (entity_kind, installation_id, stack_id, layer_id, entity_id)
  do update set
    derived_state = excluded.derived_state,
    latest_event_id = excluded.latest_event_id,
    latest_event_digest = excluded.latest_event_digest,
    terminal_at = excluded.terminal_at;
  perform set_config('xfactory.governed_projection_write', '', true);
end
$function$;

create or replace function xfactory_runtime_api_v2.admit_artifact(
  requested_artifact_id text,
  requested_content bytea,
  requested_media_type text,
  requested_producer_grant_id text
)
returns void
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  scope_installation text := current_setting('xfactory.installation_id', true);
  scope_stack text := current_setting('xfactory.stack_id', true);
  scope_layer text := current_setting('xfactory.layer_id', true);
  actor_principal text := current_setting('xfactory.principal_id', true);
  content_digest text;
  content_size bigint;
  admission_time timestamptz := transaction_timestamp();
  storage_key_value text;
  artifact_record_digest text;
  lifecycle_event_digest text;
  producer_grant xfactory_runtime_v2.authority_grants%rowtype;
  producer_principal_digest text;
begin
  if not xfactory_runtime_api_v2.current_scope_matches(
    scope_installation, scope_stack, scope_layer
  ) then
    raise exception using errcode = '42501', message = 'HGR-SCOPE-NOT-ASSUMED';
  end if;
  if requested_artifact_id is null or requested_artifact_id = ''
     or requested_media_type is null or requested_media_type = '' then
    raise exception using errcode = '22023', message = 'HGR-ARTIFACT-INPUT-INVALID';
  end if;
  content_digest := 'sha256:' || encode(sha256(requested_content), 'hex');
  content_size := octet_length(requested_content);
  if not exists (
    select 1
    from xfactory_runtime_v2.active_authority_chain(
      scope_installation,
      requested_producer_grant_id,
      'create_artifact',
      'layer',
      scope_stack,
      scope_layer,
      actor_principal,
      admission_time
    )
  ) or not exists (
    select 1
    from xfactory_runtime_v2.authority_grants grant_record
    where grant_record.installation_id = scope_installation
      and grant_record.grant_id = requested_producer_grant_id
      and grant_record.resource_type = 'artifact'
      and grant_record.resource_id = requested_artifact_id
      and grant_record.resource_digest = content_digest
  ) then
    raise exception using errcode = '42501', message = 'HGR-ARTIFACT-AUTHORITY';
  end if;

  select grant_record.*
  into strict producer_grant
  from xfactory_runtime_v2.authority_grants grant_record
  where grant_record.installation_id = scope_installation
    and grant_record.grant_id = requested_producer_grant_id;
  select principal.record_digest
  into strict producer_principal_digest
  from xfactory_runtime_v2.principals principal
  where principal.installation_id = scope_installation
    and principal.stack_id = scope_stack
    and principal.layer_id = scope_layer
    and principal.principal_id = actor_principal;

  storage_key_value := scope_installation || '/' || scope_layer || '/sha256/' ||
    substring(content_digest from 8);
  artifact_record_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'schema_version', 1,
      'kind', 'openxfactory-hermes-runtime-artifact-record',
      'installation_id', scope_installation,
      'stack_id', scope_stack,
      'layer_id', scope_layer,
      'artifact_id', requested_artifact_id,
      'content_digest', content_digest,
      'byte_size', content_size,
      'media_type', requested_media_type,
      'producer_principal_ref', jsonb_build_object(
        'scope', jsonb_build_object(
          'scope_kind', 'layer',
          'installation_id', scope_installation,
          'stack_id', scope_stack,
          'layer_id', scope_layer
        ),
        'principal_id', actor_principal,
        'record_digest', producer_principal_digest
      ),
      'producer_grant_ref', jsonb_build_object(
        'installation_id', scope_installation,
        'grant_id', requested_producer_grant_id,
        'record_digest', producer_grant.record_digest
      ),
      'storage_key', storage_key_value,
      'created_at', to_char(admission_time at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"')
    )
  );
  lifecycle_event_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'schema_version', 1,
      'kind', 'openxfactory-hermes-runtime-artifact-lifecycle-event',
      'event_id', requested_artifact_id || ':available',
      'installation_id', scope_installation,
      'stack_id', scope_stack,
      'layer_id', scope_layer,
      'artifact_id', requested_artifact_id,
      'artifact_record_digest', artifact_record_digest,
      'predecessor_ref', jsonb_build_object(
        'kind', 'artifact_record',
        'id', requested_artifact_id,
        'digest', artifact_record_digest
      ),
      'event_type', 'available',
      'actor_principal_ref', jsonb_build_object(
        'scope', jsonb_build_object(
          'scope_kind', 'layer',
          'installation_id', scope_installation,
          'stack_id', scope_stack,
          'layer_id', scope_layer
        ),
        'principal_id', actor_principal,
        'record_digest', producer_principal_digest
      ),
      'actor_grant_ref', jsonb_build_object(
        'installation_id', scope_installation,
        'grant_id', requested_producer_grant_id,
        'record_digest', producer_grant.record_digest
      ),
      'occurred_at', to_char(admission_time at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'),
      'reason', 'admitted'
    )
  );

  insert into xfactory_runtime_v2.artifact_bodies (
    installation_id, stack_id, layer_id, artifact_id, content_digest,
    byte_size, content, created_at
  ) values (
    scope_installation, scope_stack, scope_layer, requested_artifact_id,
    content_digest, content_size, requested_content, admission_time
  );
  insert into xfactory_runtime_v2.artifact_records (
    installation_id, stack_id, layer_id, artifact_id, record_digest,
    digest_profile, content_digest, byte_size, media_type, storage_key,
    producer_principal_id, producer_grant_id, producer_grant_digest, created_at
  ) values (
    scope_installation, scope_stack, scope_layer, requested_artifact_id,
    artifact_record_digest, 'xfactory-canonical-json-v1', content_digest,
    content_size, requested_media_type,
    storage_key_value,
    actor_principal, requested_producer_grant_id,
    (
      select record_digest
      from xfactory_runtime_v2.authority_grants
      where installation_id = scope_installation
        and grant_id = requested_producer_grant_id
    ),
    admission_time
  );
  insert into xfactory_runtime_v2.artifact_lifecycle_events (
    installation_id, stack_id, layer_id, artifact_id, event_id,
    event_digest, artifact_record_digest, predecessor_kind, predecessor_id,
    predecessor_digest, event_type, actor_principal_id,
    actor_principal_digest, actor_grant_id, actor_grant_digest,
    reason, occurred_at
  ) values (
    scope_installation, scope_stack, scope_layer, requested_artifact_id,
    requested_artifact_id || ':available', lifecycle_event_digest,
    artifact_record_digest, 'artifact_record', requested_artifact_id,
    artifact_record_digest, 'available', actor_principal,
    producer_principal_digest, requested_producer_grant_id,
    producer_grant.record_digest, 'admitted', admission_time
  );
end
$function$;

create or replace function xfactory_runtime_api_v2.probe_artifact(
  requested_artifact_id text
)
returns jsonb
language plpgsql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  scope_installation text := current_setting('xfactory.installation_id', true);
  scope_stack text := current_setting('xfactory.stack_id', true);
  scope_layer text := current_setting('xfactory.layer_id', true);
  artifact_record xfactory_runtime_v2.artifact_records%rowtype;
begin
  if not xfactory_runtime_api_v2.current_scope_matches(
    scope_installation, scope_stack, scope_layer
  ) then
    return jsonb_build_object('outcome', 'not_found');
  end if;
  select record.*
  into artifact_record
  from xfactory_runtime_v2.artifact_records record
  where record.installation_id = scope_installation
    and record.stack_id = scope_stack
    and record.layer_id = scope_layer
    and record.artifact_id = requested_artifact_id;
  if not found then
    return jsonb_build_object('outcome', 'not_found');
  end if;
  return jsonb_build_object(
    'outcome', 'available',
    'artifact_id', artifact_record.artifact_id,
    'content_digest', artifact_record.content_digest,
    'byte_size', artifact_record.byte_size,
    'media_type', artifact_record.media_type
  );
end
$function$;

create unique index if not exists approval_one_decision_per_reviewer_uq
  on xfactory_runtime_v2.approval_decisions (
    installation_id, stack_id, layer_id, request_id, reviewer_principal_id
  );

create or replace function xfactory_runtime_v2.artifact_body_matches(
  requested_installation_id text,
  requested_stack_id text,
  requested_layer_id text,
  requested_artifact_id text,
  requested_digest text
)
returns boolean
language sql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select exists (
    select 1
    from xfactory_runtime_v2.artifact_records record
    join xfactory_runtime_v2.artifact_bodies body
      using (installation_id, stack_id, layer_id, artifact_id)
    where record.installation_id = requested_installation_id
      and record.stack_id = requested_stack_id
      and record.layer_id = requested_layer_id
      and record.artifact_id = requested_artifact_id
      and record.content_digest = requested_digest
      and body.content_digest = record.content_digest
      and body.byte_size = record.byte_size
      and body.content_digest = 'sha256:' || encode(sha256(body.content), 'hex')
      and body.byte_size = octet_length(body.content)
  )
$function$;

create or replace function xfactory_runtime_v2.governed_scope_json(
  requested_scope_kind text,
  requested_installation_id text,
  requested_stack_id text,
  requested_layer_id text
)
returns jsonb
language sql
immutable
strict
set search_path = pg_catalog
as $function$
  select case requested_scope_kind
    when 'installation' then jsonb_build_object(
      'scope_kind', 'installation',
      'installation_id', requested_installation_id
    )
    when 'installation_admin' then jsonb_build_object(
      'scope_kind', 'installation_admin',
      'installation_id', requested_installation_id
    )
    when 'stack' then jsonb_build_object(
      'scope_kind', 'stack',
      'installation_id', requested_installation_id,
      'stack_id', requested_stack_id
    )
    when 'layer' then jsonb_build_object(
      'scope_kind', 'layer',
      'installation_id', requested_installation_id,
      'stack_id', requested_stack_id,
      'layer_id', requested_layer_id
    )
  end
$function$;

create or replace function xfactory_runtime_v2.principal_selector_matches(
  reviewer_selector jsonb,
  requested_principal_id text,
  requested_principal_type text
)
returns boolean
language sql
immutable
strict
set search_path = pg_catalog
as $function$
  select
    (
      reviewer_selector ? 'principal_ids'
      and reviewer_selector->'principal_ids'
        @> jsonb_build_array(requested_principal_id)
    )
    or (
      reviewer_selector ? 'principal_types'
      and reviewer_selector->'principal_types'
        @> jsonb_build_array(requested_principal_type)
    )
    or (
      reviewer_selector ? 'group_principal_ids'
      and requested_principal_type = 'group'
      and reviewer_selector->'group_principal_ids'
        @> jsonb_build_array(requested_principal_id)
    )
$function$;

create or replace function xfactory_runtime_api_v2.record_approval_decision(
  requested_decision_id text,
  requested_request_id text,
  requested_decision text,
  requested_reviewer_grant_id text
)
returns void
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  scope_installation text := current_setting('xfactory.installation_id', true);
  scope_stack text := current_setting('xfactory.stack_id', true);
  scope_layer text := current_setting('xfactory.layer_id', true);
  actor_principal text := current_setting('xfactory.principal_id', true);
  decision_time timestamptz := transaction_timestamp();
  request_record xfactory_runtime_v2.approval_requests%rowtype;
  policy_record xfactory_runtime_v2.approval_decision_policies%rowtype;
  reviewer_grant xfactory_runtime_v2.authority_grants%rowtype;
  reviewer_principal xfactory_runtime_v2.principals%rowtype;
  policy_selector_ids text[];
  requested_selector_ids text[];
  matching_selector_id text;
  matching_selector_count integer;
  decision_record_digest text;
begin
  if not xfactory_runtime_api_v2.current_scope_matches(
    scope_installation, scope_stack, scope_layer
  ) then
    raise exception using errcode = '42501', message = 'HGR-SCOPE-NOT-ASSUMED';
  end if;
  if requested_decision not in ('approve', 'reject') then
    raise exception using errcode = '22023', message = 'HGR-APPROVAL-DECISION-INVALID';
  end if;

  select request.*
  into request_record
  from xfactory_runtime_v2.approval_requests request
  where request.installation_id = scope_installation
    and request.stack_id = scope_stack
    and request.layer_id = scope_layer
    and request.request_id = requested_request_id
  for share;
  if not found then
    raise exception using
      errcode = '42501',
      message = 'HGR-APPROVAL-REVIEWER-AUTHORITY';
  end if;

  if request_record.expires_at <= decision_time
     or exists (
       select 1
       from xfactory_runtime_v2.approval_supersession_events supersession
       where supersession.installation_id = request_record.installation_id
         and supersession.stack_id = request_record.stack_id
         and supersession.layer_id = request_record.layer_id
         and supersession.target_kind = 'request'
         and supersession.target_id = request_record.request_id
         and supersession.target_digest = request_record.record_digest
         and supersession.effective_at <= decision_time
     ) then
    raise exception using errcode = '42501', message = 'HGR-APPROVAL-REQUEST-INACTIVE';
  end if;

  select policy.*
  into strict policy_record
  from xfactory_runtime_v2.approval_decision_policies policy
  where policy.installation_id = request_record.installation_id
    and policy.stack_id = request_record.stack_id
    and policy.layer_id = request_record.layer_id
    and policy.policy_id = request_record.decision_policy_id
    and policy.policy_digest = request_record.decision_policy_digest;

  if policy_record.authority_scope_kind <> request_record.authority_scope_kind
     or policy_record.authority_stack_id <> request_record.authority_stack_id
     or policy_record.authority_layer_id <> request_record.authority_layer_id then
    raise exception using errcode = '42501', message = 'HGR-APPROVAL-POLICY-MISMATCH';
  end if;

  select array_agg(selector->>'selector_id' order by selector->>'selector_id')
  into policy_selector_ids
  from jsonb_array_elements(policy_record.reviewer_selectors) selector;
  select array_agg(selector_id order by selector_id)
  into requested_selector_ids
  from unnest(request_record.reviewer_selector_ids) selector_id;
  if policy_selector_ids is distinct from requested_selector_ids
     or cardinality(policy_selector_ids) <> (
       select count(distinct selector->>'selector_id')
       from jsonb_array_elements(policy_record.reviewer_selectors) selector
     ) then
    raise exception using errcode = '42501', message = 'HGR-APPROVAL-REVIEWER-SELECTOR';
  end if;

  select grant_record.*
  into reviewer_grant
  from xfactory_runtime_v2.authority_grants grant_record
  where grant_record.installation_id = scope_installation
    and grant_record.grant_id = requested_reviewer_grant_id
  for share;
  if not found
     or reviewer_grant.grantee_principal_id <> actor_principal
     or reviewer_grant.resource_type <> 'approval_request'
     or reviewer_grant.resource_id <> requested_request_id
     or reviewer_grant.resource_digest <> request_record.record_digest then
    raise exception using errcode = '42501', message = 'HGR-APPROVAL-REVIEWER-AUTHORITY';
  end if;

  select principal.*
  into reviewer_principal
  from xfactory_runtime_v2.principals principal
  where principal.installation_id = reviewer_grant.installation_id
    and principal.stack_id = reviewer_grant.grantee_stack_id
    and principal.layer_id = reviewer_grant.grantee_layer_id
    and principal.principal_id = reviewer_grant.grantee_principal_id
    and principal.record_digest = reviewer_grant.grantee_principal_digest;
  if not found then
    raise exception using errcode = '42501', message = 'HGR-APPROVAL-REVIEWER-AUTHORITY';
  end if;

  if not exists (
    select 1
    from xfactory_runtime_v2.active_authority_chain(
      scope_installation,
      requested_reviewer_grant_id,
      'decide_approval',
      case when request_record.authority_scope_kind = 'installation_admin'
        then 'installation' else request_record.authority_scope_kind end,
      request_record.authority_stack_id,
      request_record.authority_layer_id,
      actor_principal,
      decision_time
    )
  ) then
    raise exception using errcode = '42501', message = 'HGR-APPROVAL-REVIEWER-AUTHORITY';
  end if;

  select count(*), min(selector->>'selector_id')
  into matching_selector_count, matching_selector_id
  from jsonb_array_elements(policy_record.reviewer_selectors) selector
  where selector->>'selector_id' = any(request_record.reviewer_selector_ids)
    and xfactory_runtime_v2.principal_selector_matches(
      selector, reviewer_principal.principal_id,
      reviewer_principal.principal_type
    );
  if matching_selector_count <> 1 then
    raise exception using errcode = '42501', message = 'HGR-APPROVAL-REVIEWER-SELECTOR';
  end if;

  decision_record_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'schema_version', 1,
      'kind', 'openxfactory-hermes-runtime-approval-decision',
      'decision_id', requested_decision_id,
      'request_id', request_record.request_id,
      'request_digest', request_record.record_digest,
      'owning_scope', xfactory_runtime_v2.governed_scope_json(
        'layer', request_record.installation_id,
        request_record.stack_id, request_record.layer_id
      ),
      'target', jsonb_build_object(
        'installation_id', request_record.installation_id,
        'stack_id', request_record.target_stack_id,
        'layer_id', request_record.target_layer_id,
        'resource_type', request_record.target_type,
        'resource_id', request_record.target_id,
        'digest', request_record.target_digest
      ),
      'requested_action', request_record.requested_action,
      'authority_scope', xfactory_runtime_v2.governed_scope_json(
        request_record.authority_scope_kind, request_record.installation_id,
        request_record.authority_stack_id, request_record.authority_layer_id
      ),
      'decision_policy_id', request_record.decision_policy_id,
      'decision_policy_digest', request_record.decision_policy_digest,
      'reviewer_selector_id', matching_selector_id,
      'actual_reviewer_principal_ref', jsonb_build_object(
        'scope', xfactory_runtime_v2.governed_scope_json(
          reviewer_principal.scope_kind, reviewer_principal.installation_id,
          reviewer_principal.stack_id, reviewer_principal.layer_id
        ),
        'principal_id', reviewer_principal.principal_id,
        'record_digest', reviewer_principal.record_digest
      ),
      'reviewer_grant_ref', jsonb_build_object(
        'installation_id', reviewer_grant.installation_id,
        'grant_id', reviewer_grant.grant_id,
        'record_digest', reviewer_grant.record_digest
      ),
      'decision', requested_decision,
      'decided_at', to_char(
        decision_time at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
      )
    )
  );

  insert into xfactory_runtime_v2.approval_decisions (
    installation_id, stack_id, layer_id, decision_id, record_digest,
    digest_profile, request_id, request_digest,
    target_type, target_id, target_digest,
    target_stack_id, target_layer_id, requested_action,
    authority_scope_kind, authority_stack_id, authority_layer_id,
    decision_policy_id, decision_policy_digest, reviewer_selector_id,
    reviewer_stack_id, reviewer_layer_id, reviewer_principal_id,
    reviewer_principal_digest, reviewer_grant_id, reviewer_grant_digest,
    decision, decided_at
  ) values (
    request_record.installation_id, request_record.stack_id,
    request_record.layer_id, requested_decision_id, decision_record_digest,
    'xfactory-canonical-json-v1', request_record.request_id,
    request_record.record_digest,
    request_record.target_type, request_record.target_id,
    request_record.target_digest, request_record.target_stack_id,
    request_record.target_layer_id, request_record.requested_action,
    request_record.authority_scope_kind, request_record.authority_stack_id,
    request_record.authority_layer_id, request_record.decision_policy_id,
    request_record.decision_policy_digest, matching_selector_id,
    reviewer_principal.stack_id, reviewer_principal.layer_id,
    reviewer_principal.principal_id, reviewer_principal.record_digest,
    reviewer_grant.grant_id, reviewer_grant.record_digest,
    requested_decision, decision_time
  );
end
$function$;

create or replace function xfactory_runtime_api_v2.supersede_approval(
  requested_event_id text,
  requested_request_id text,
  requested_decision_id text,
  requested_event_type text,
  requested_issuer_grant_id text,
  requested_reason text
)
returns void
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  scope_installation text := current_setting('xfactory.installation_id', true);
  scope_stack text := current_setting('xfactory.stack_id', true);
  scope_layer text := current_setting('xfactory.layer_id', true);
  actor_principal text := current_setting('xfactory.principal_id', true);
  effective_time timestamptz := transaction_timestamp();
  request_record xfactory_runtime_v2.approval_requests%rowtype;
  decision_record xfactory_runtime_v2.approval_decisions%rowtype;
  policy_record xfactory_runtime_v2.approval_decision_policies%rowtype;
  issuer_grant xfactory_runtime_v2.authority_grants%rowtype;
  issuer_principal xfactory_runtime_v2.principals%rowtype;
  target_kind_value text;
  target_id_value text;
  target_digest_value text;
  target_resource_type text;
  event_record_digest text;
begin
  if not xfactory_runtime_api_v2.current_scope_matches(
    scope_installation, scope_stack, scope_layer
  ) then
    raise exception using errcode = '42501', message = 'HGR-SCOPE-NOT-ASSUMED';
  end if;
  if requested_event_type not in ('expired', 'cancelled', 'revoked')
     or requested_reason is null or btrim(requested_reason) = '' then
    raise exception using errcode = '22023', message = 'HGR-APPROVAL-SUPERSESSION-INVALID';
  end if;
  select request.*
  into request_record
  from xfactory_runtime_v2.approval_requests request
  where request.installation_id = scope_installation
    and request.stack_id = scope_stack
    and request.layer_id = scope_layer
    and request.request_id = requested_request_id
  for share;
  if not found then
    raise exception using
      errcode = '42501',
      message = 'HGR-APPROVAL-SCOPE-AUTHORITY';
  end if;

  select policy.*
  into strict policy_record
  from xfactory_runtime_v2.approval_decision_policies policy
  where policy.installation_id = request_record.installation_id
    and policy.stack_id = request_record.stack_id
    and policy.layer_id = request_record.layer_id
    and policy.policy_id = request_record.decision_policy_id
    and policy.policy_digest = request_record.decision_policy_digest;
  if policy_record.authority_scope_kind <> request_record.authority_scope_kind
     or policy_record.authority_stack_id <> request_record.authority_stack_id
     or policy_record.authority_layer_id <> request_record.authority_layer_id then
    raise exception using errcode = '42501', message = 'HGR-APPROVAL-POLICY-MISMATCH';
  end if;

  if requested_decision_id is null then
    target_kind_value := 'request';
    target_id_value := request_record.request_id;
    target_digest_value := request_record.record_digest;
    target_resource_type := 'approval_request';
  else
    select decision.*
    into decision_record
    from xfactory_runtime_v2.approval_decisions decision
    where decision.installation_id = request_record.installation_id
      and decision.stack_id = request_record.stack_id
      and decision.layer_id = request_record.layer_id
      and decision.request_id = request_record.request_id
      and decision.decision_id = requested_decision_id;
    if not found then
      raise exception using errcode = '22023', message = 'HGR-APPROVAL-DECISION-NOT-FOUND';
    end if;
    target_kind_value := 'decision';
    target_id_value := decision_record.decision_id;
    target_digest_value := decision_record.record_digest;
    target_resource_type := 'approval_decision';
  end if;

  select grant_record.*
  into issuer_grant
  from xfactory_runtime_v2.authority_grants grant_record
  where grant_record.installation_id = scope_installation
    and grant_record.grant_id = requested_issuer_grant_id
  for share;
  if not found
     or issuer_grant.grantee_principal_id <> actor_principal
     or issuer_grant.resource_type <> target_resource_type
     or issuer_grant.resource_id <> target_id_value
     or issuer_grant.resource_digest <> target_digest_value then
    raise exception using errcode = '42501', message = 'HGR-APPROVAL-SUPERSESSION-AUTHORITY';
  end if;

  select principal.*
  into issuer_principal
  from xfactory_runtime_v2.principals principal
  where principal.installation_id = issuer_grant.installation_id
    and principal.stack_id = issuer_grant.grantee_stack_id
    and principal.layer_id = issuer_grant.grantee_layer_id
    and principal.principal_id = issuer_grant.grantee_principal_id
    and principal.record_digest = issuer_grant.grantee_principal_digest;
  if not found or not exists (
    select 1
    from jsonb_array_elements(policy_record.supersession_authorities) authority
    where authority->>'event_type' = requested_event_type
      and xfactory_runtime_v2.principal_selector_matches(
        authority, issuer_principal.principal_id,
        issuer_principal.principal_type
      )
  ) then
    raise exception using errcode = '42501', message = 'HGR-APPROVAL-SUPERSESSION-AUTHORITY';
  end if;

  if not exists (
    select 1
    from xfactory_runtime_v2.active_authority_chain(
      scope_installation,
      requested_issuer_grant_id,
      'supersede_approval',
      case when policy_record.authority_scope_kind = 'installation_admin'
        then 'installation' else policy_record.authority_scope_kind end,
      policy_record.authority_stack_id,
      policy_record.authority_layer_id,
      actor_principal,
      effective_time
    )
  ) then
    raise exception using errcode = '42501', message = 'HGR-APPROVAL-SUPERSESSION-AUTHORITY';
  end if;

  event_record_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'schema_version', 1,
      'kind', 'openxfactory-hermes-runtime-approval-supersession-event',
      'event_id', requested_event_id,
      'event_type', requested_event_type,
      'target_kind', target_kind_value,
      'target_id', target_id_value,
      'target_digest', target_digest_value,
      'owning_scope', xfactory_runtime_v2.governed_scope_json(
        'layer', request_record.installation_id,
        request_record.stack_id, request_record.layer_id
      ),
      'authority_scope', xfactory_runtime_v2.governed_scope_json(
        policy_record.authority_scope_kind, request_record.installation_id,
        policy_record.authority_stack_id, policy_record.authority_layer_id
      ),
      'issuer_principal_ref', jsonb_build_object(
        'scope', xfactory_runtime_v2.governed_scope_json(
          issuer_principal.scope_kind, issuer_principal.installation_id,
          issuer_principal.stack_id, issuer_principal.layer_id
        ),
        'principal_id', issuer_principal.principal_id,
        'record_digest', issuer_principal.record_digest
      ),
      'issuer_grant_ref', jsonb_build_object(
        'installation_id', issuer_grant.installation_id,
        'grant_id', issuer_grant.grant_id,
        'record_digest', issuer_grant.record_digest
      ),
      'effective_at', to_char(
        effective_time at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
      ),
      'reason', requested_reason
    )
  );

  insert into xfactory_runtime_v2.approval_supersession_events (
    installation_id, stack_id, layer_id, event_id, event_digest,
    event_type, target_kind, target_id, target_digest,
    authority_scope_kind, authority_stack_id, authority_layer_id,
    issuer_stack_id, issuer_layer_id, issuer_principal_id,
    issuer_principal_digest, issuer_grant_id, issuer_grant_digest,
    reason, effective_at
  ) values (
    scope_installation, scope_stack, scope_layer, requested_event_id,
    event_record_digest, requested_event_type, target_kind_value,
    target_id_value, target_digest_value,
    policy_record.authority_scope_kind, policy_record.authority_stack_id,
    policy_record.authority_layer_id, issuer_principal.stack_id,
    issuer_principal.layer_id, issuer_principal.principal_id,
    issuer_principal.record_digest, issuer_grant.grant_id,
    issuer_grant.record_digest, requested_reason, effective_time
  );
end
$function$;

create or replace function xfactory_runtime_api_v2.approval_authorizes(
  requested_request_id text
)
returns boolean
language plpgsql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  scope_installation text := current_setting('xfactory.installation_id', true);
  scope_stack text := current_setting('xfactory.stack_id', true);
  scope_layer text := current_setting('xfactory.layer_id', true);
  evaluation_time timestamptz := transaction_timestamp();
  request_record xfactory_runtime_v2.approval_requests%rowtype;
  policy_record xfactory_runtime_v2.approval_decision_policies%rowtype;
  approvals integer;
  rejections integer;
  policy_selector_ids text[];
  request_selector_ids text[];
  selectors_satisfied boolean;
begin
  if not xfactory_runtime_api_v2.current_scope_matches(
    scope_installation, scope_stack, scope_layer
  ) then
    return false;
  end if;
  select request.*
  into request_record
  from xfactory_runtime_v2.approval_requests request
  where request.installation_id = scope_installation
    and request.stack_id = scope_stack
    and request.layer_id = scope_layer
    and request.request_id = requested_request_id;
  if not found or request_record.expires_at <= evaluation_time then
    return false;
  end if;
  if not exists (
    select 1
    from xfactory_runtime_v2.active_authority_chain(
      request_record.installation_id,
      request_record.requester_grant_id,
      'request_approval',
      case when request_record.authority_scope_kind = 'installation_admin'
        then 'installation' else request_record.authority_scope_kind end,
      request_record.authority_stack_id,
      request_record.authority_layer_id,
      request_record.requester_principal_id,
      evaluation_time
    )
  ) or not exists (
    select 1
    from xfactory_runtime_v2.authority_grants requester_grant
    where requester_grant.installation_id = request_record.installation_id
      and requester_grant.grant_id = request_record.requester_grant_id
      and requester_grant.record_digest = request_record.requester_grant_digest
      and requester_grant.grantee_stack_id = request_record.requester_stack_id
      and requester_grant.grantee_layer_id = request_record.requester_layer_id
      and requester_grant.grantee_principal_id = request_record.requester_principal_id
      and requester_grant.grantee_principal_digest =
        request_record.requester_principal_digest
      and requester_grant.resource_type = request_record.target_type
      and requester_grant.resource_id = request_record.target_id
      and requester_grant.resource_digest = request_record.target_digest
  ) then
    return false;
  end if;
  select policy.*
  into policy_record
  from xfactory_runtime_v2.approval_decision_policies policy
  where policy.installation_id = request_record.installation_id
    and policy.stack_id = request_record.stack_id
    and policy.layer_id = request_record.layer_id
    and policy.policy_id = request_record.decision_policy_id
    and policy.policy_digest = request_record.decision_policy_digest;
  if not found
     or policy_record.authority_scope_kind <> request_record.authority_scope_kind
     or policy_record.authority_stack_id <> request_record.authority_stack_id
     or policy_record.authority_layer_id <> request_record.authority_layer_id then
    return false;
  end if;

  select array_agg(selector->>'selector_id' order by selector->>'selector_id')
  into policy_selector_ids
  from jsonb_array_elements(policy_record.reviewer_selectors) selector;
  select array_agg(selector_id order by selector_id)
  into request_selector_ids
  from unnest(request_record.reviewer_selector_ids) selector_id;
  if policy_selector_ids is distinct from request_selector_ids
     or cardinality(policy_selector_ids) <> (
       select count(distinct selector->>'selector_id')
       from jsonb_array_elements(policy_record.reviewer_selectors) selector
     )
     or exists (
       select 1
       from jsonb_array_elements(policy_record.reviewer_selectors) selector
       where not (selector ? 'selector_id')
          or not (selector ? 'minimum_count')
          or coalesce((selector->>'minimum_count')::integer, 0) < 1
          or selector->>'distinct_principals' <> 'true'
          or not (
            selector ? 'principal_ids'
            or selector ? 'principal_types'
            or selector ? 'group_principal_ids'
          )
     )
     or (
       select count(*) <> count(distinct authority->>'event_type')
       from jsonb_array_elements(policy_record.supersession_authorities) authority
     ) then
    return false;
  end if;
  if exists (
    select 1
    from xfactory_runtime_v2.approval_supersession_events supersession
    where supersession.installation_id = request_record.installation_id
      and supersession.stack_id = request_record.stack_id
      and supersession.layer_id = request_record.layer_id
      and supersession.target_kind = 'request'
      and supersession.target_id = request_record.request_id
      and supersession.target_digest = request_record.record_digest
      and supersession.effective_at <= evaluation_time
  ) then
    return false;
  end if;
  if request_record.target_type = 'artifact'
     and not xfactory_runtime_v2.artifact_body_matches(
       request_record.installation_id,
       request_record.target_stack_id,
       request_record.target_layer_id,
       request_record.target_id,
       request_record.target_digest
     ) then
    return false;
  end if;

  with valid_decisions as (
    select decision_record.*
    from xfactory_runtime_v2.approval_decisions decision_record
    join xfactory_runtime_v2.principals reviewer_principal
      on reviewer_principal.installation_id = decision_record.installation_id
     and reviewer_principal.stack_id = decision_record.reviewer_stack_id
     and reviewer_principal.layer_id = decision_record.reviewer_layer_id
     and reviewer_principal.principal_id = decision_record.reviewer_principal_id
     and reviewer_principal.record_digest =
       decision_record.reviewer_principal_digest
    join xfactory_runtime_v2.authority_grants reviewer_grant
      on reviewer_grant.installation_id = decision_record.installation_id
     and reviewer_grant.grant_id = decision_record.reviewer_grant_id
     and reviewer_grant.record_digest = decision_record.reviewer_grant_digest
     and reviewer_grant.grantee_stack_id = decision_record.reviewer_stack_id
     and reviewer_grant.grantee_layer_id = decision_record.reviewer_layer_id
     and reviewer_grant.grantee_principal_id =
       decision_record.reviewer_principal_id
     and reviewer_grant.grantee_principal_digest =
       decision_record.reviewer_principal_digest
     and reviewer_grant.resource_type = 'approval_request'
     and reviewer_grant.resource_id = decision_record.request_id
     and reviewer_grant.resource_digest = request_record.record_digest
    where decision_record.installation_id = request_record.installation_id
      and decision_record.stack_id = request_record.stack_id
      and decision_record.layer_id = request_record.layer_id
      and decision_record.request_id = request_record.request_id
      and decision_record.request_digest = request_record.record_digest
      and decision_record.target_type = request_record.target_type
      and decision_record.target_id = request_record.target_id
      and decision_record.target_digest = request_record.target_digest
      and decision_record.target_stack_id = request_record.target_stack_id
      and decision_record.target_layer_id = request_record.target_layer_id
      and decision_record.requested_action = request_record.requested_action
      and decision_record.authority_scope_kind = request_record.authority_scope_kind
      and decision_record.authority_stack_id = request_record.authority_stack_id
      and decision_record.authority_layer_id = request_record.authority_layer_id
      and decision_record.decision_policy_id = request_record.decision_policy_id
      and decision_record.decision_policy_digest =
        request_record.decision_policy_digest
      and decision_record.reviewer_selector_id =
        any(request_record.reviewer_selector_ids)
      and exists (
        select 1
        from jsonb_array_elements(policy_record.reviewer_selectors) selector
        where selector->>'selector_id' = decision_record.reviewer_selector_id
          and xfactory_runtime_v2.principal_selector_matches(
            selector, reviewer_principal.principal_id,
            reviewer_principal.principal_type
          )
      )
      and exists (
        select 1
        from xfactory_runtime_v2.active_authority_chain(
          decision_record.installation_id,
          decision_record.reviewer_grant_id,
          'decide_approval',
          case when decision_record.authority_scope_kind = 'installation_admin'
            then 'installation' else decision_record.authority_scope_kind end,
          decision_record.authority_stack_id,
          decision_record.authority_layer_id,
          decision_record.reviewer_principal_id,
          evaluation_time
        )
      )
      and not exists (
        select 1
        from xfactory_runtime_v2.approval_supersession_events supersession
        where supersession.installation_id = decision_record.installation_id
          and supersession.stack_id = decision_record.stack_id
          and supersession.layer_id = decision_record.layer_id
          and supersession.target_kind = 'decision'
          and supersession.target_id = decision_record.decision_id
          and supersession.target_digest = decision_record.record_digest
          and supersession.effective_at <= evaluation_time
      )
  ),
  totals as (
    select
      count(distinct reviewer_principal_id)
        filter (where decision = 'approve')::integer as approval_count,
      count(distinct reviewer_principal_id)
        filter (where decision = 'reject')::integer as rejection_count
    from valid_decisions
  ),
  selector_requirements as (
    select
      selector->>'selector_id' as selector_id,
      (selector->>'minimum_count')::integer as minimum_count
    from jsonb_array_elements(policy_record.reviewer_selectors) selector
    where selector->>'selector_id' = any(request_record.reviewer_selector_ids)
  ),
  selector_results as (
    select
      requirement.selector_id,
      requirement.minimum_count,
      count(distinct decision_record.reviewer_principal_id)
        filter (where decision_record.decision = 'approve')::integer
        as approval_count
    from selector_requirements requirement
    left join valid_decisions decision_record
      on decision_record.reviewer_selector_id = requirement.selector_id
    group by requirement.selector_id, requirement.minimum_count
  )
  select
    totals.approval_count,
    totals.rejection_count,
    bool_and(selector_results.approval_count >= selector_results.minimum_count)
  into approvals, rejections, selectors_satisfied
  from totals
  cross join selector_results
  group by totals.approval_count, totals.rejection_count;

  if rejections > 0
     and policy_record.conflict_resolution in ('contested', 'reject_overrides') then
    return false;
  end if;
  if policy_record.aggregation = 'minimum_approvals' then
    return approvals >= policy_record.minimum_approvals and rejections = 0;
  end if;
  if policy_record.aggregation = 'all_required_selectors' then
    return coalesce(selectors_satisfied, false) and rejections = 0;
  end if;
  return false;
end
$function$;

create or replace function xfactory_runtime_v2.canonical_json(
  value jsonb
)
returns text
language plpgsql
immutable
strict
set search_path = pg_catalog
as $function$
declare
  rendered text;
  numeric_text text;
begin
  case jsonb_typeof(value)
    when 'object' then
      select coalesce(
        '{' || string_agg(
          to_jsonb(member.key)::text || ':' ||
            xfactory_runtime_v2.canonical_json(member.value),
          ',' order by member.key collate "C"
        ) || '}',
        '{}'
      )
      into rendered
      from jsonb_each(value) member;
      return rendered;
    when 'array' then
      select coalesce(
        '[' || string_agg(
          xfactory_runtime_v2.canonical_json(member.value),
          ',' order by member.ordinality
        ) || ']',
        '[]'
      )
      into rendered
      from jsonb_array_elements(value) with ordinality member(value, ordinality);
      return rendered;
    when 'number' then
      numeric_text := value::text;
      if numeric_text ~ '[.eE]' then
        raise exception using
          errcode = '22023',
          message = 'HGR-RECORD-DIGEST-NONINTEGER: floating-point values are forbidden';
      end if;
      return numeric_text;
    else
      return value::text;
  end case;
end
$function$;

create or replace function xfactory_runtime_v2.canonical_record_digest(
  record_without_digest jsonb
)
returns text
language sql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select 'sha256:' || encode(
    sha256(convert_to(
      xfactory_runtime_v2.canonical_json(record_without_digest),
      'UTF8'
    )),
    'hex'
  )
$function$;

create or replace function xfactory_runtime_v2.resource_reference_json(
  requested_installation_id text,
  requested_scope_kind text,
  requested_stack_id text,
  requested_layer_id text,
  requested_resource_type text,
  requested_resource_id text,
  requested_resource_digest text
)
returns jsonb
language plpgsql
immutable
set search_path = pg_catalog
as $function$
declare
  reference_payload jsonb := jsonb_build_object(
    'installation_id', requested_installation_id,
    'resource_type', requested_resource_type,
    'resource_id', requested_resource_id
  );
begin
  if requested_scope_kind in ('stack', 'layer') then
    reference_payload := reference_payload || jsonb_build_object(
      'stack_id', requested_stack_id
    );
  end if;
  if requested_scope_kind = 'layer' then
    reference_payload := reference_payload || jsonb_build_object(
      'layer_id', requested_layer_id
    );
  end if;
  if requested_resource_digest is not null then
    reference_payload := reference_payload || jsonb_build_object(
      'digest', requested_resource_digest
    );
  end if;
  return reference_payload;
end
$function$;

create or replace function xfactory_runtime_v2.compute_trust_anchor_record_digest()
returns trigger
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  anchor_principal xfactory_runtime_v2.principals%rowtype;
begin
  select principal.*
  into anchor_principal
  from xfactory_runtime_v2.principals principal
  where principal.installation_id = new.installation_id
    and principal.stack_id = new.principal_stack_id
    and principal.layer_id = new.principal_layer_id
    and principal.principal_id = new.principal_id
    and principal.record_digest = new.principal_digest;
  if not found then
    raise exception using
      errcode = '42501',
      message = 'HGR-ANCHOR-PRINCIPAL-REFERENCE';
  end if;

  new.record_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'schema_version', 1,
      'kind', 'openxfactory-installation-trust-anchor',
      'anchor_id', new.anchor_id,
      'record_digest_profile', new.digest_profile,
      'installation_id', new.installation_id,
      'anchor_kind', new.anchor_kind,
      'principal_ref', jsonb_build_object(
        'scope', xfactory_runtime_v2.governed_scope_json(
          anchor_principal.scope_kind, anchor_principal.installation_id,
          anchor_principal.stack_id, anchor_principal.layer_id
        ),
        'principal_id', anchor_principal.principal_id,
        'record_digest', anchor_principal.record_digest
      ),
      'key_ref', jsonb_build_object(
        'provider', new.key_provider,
        'key_id', new.key_id,
        'algorithm', new.key_algorithm
      ),
      'policy_pin', jsonb_build_object(
        'repository', new.policy_repository,
        'commit', new.policy_commit,
        'path', new.policy_ref,
        'digest', new.policy_digest
      ),
      'effective_at', to_char(
        new.effective_at at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
      ),
      'authorized_evidence_digest', new.authorized_evidence_digest,
      'created_at', to_char(
        new.created_at at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
      )
    )
  );
  return new;
end
$function$;

create or replace function xfactory_runtime_v2.compute_authority_grant_record_digest()
returns trigger
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  grantee_principal xfactory_runtime_v2.principals%rowtype;
  grant_payload jsonb;
begin
  select principal.*
  into grantee_principal
  from xfactory_runtime_v2.principals principal
  where principal.installation_id = new.installation_id
    and principal.stack_id = new.grantee_stack_id
    and principal.layer_id = new.grantee_layer_id
    and principal.principal_id = new.grantee_principal_id
    and principal.record_digest = new.grantee_principal_digest;
  if not found then
    raise exception using
      errcode = '42501',
      message = 'HGR-GRANT-PRINCIPAL-REFERENCE';
  end if;

  grant_payload := jsonb_build_object(
    'schema_version', 1,
    'kind', 'openxfactory-authority-grant',
    'grant_id', new.grant_id,
    'record_digest_profile', new.digest_profile,
    'installation_id', new.installation_id,
    'grant_kind', new.grant_kind,
    'principal_ref', jsonb_build_object(
      'scope', xfactory_runtime_v2.governed_scope_json(
        grantee_principal.scope_kind, grantee_principal.installation_id,
        grantee_principal.stack_id, grantee_principal.layer_id
      ),
      'principal_id', grantee_principal.principal_id,
      'record_digest', grantee_principal.record_digest
    ),
    'scope', xfactory_runtime_v2.governed_scope_json(
      new.scope_kind, new.installation_id,
      new.scope_stack_id, new.scope_layer_id
    ),
    'action', new.action,
    'resource_constraint', xfactory_runtime_v2.resource_reference_json(
      new.installation_id, new.scope_kind,
      new.scope_stack_id, new.scope_layer_id,
      new.resource_type, new.resource_id, new.resource_digest
    ),
    'policy_pin', jsonb_build_object(
      'repository', new.policy_repository,
      'commit', new.policy_commit,
      'path', new.policy_ref,
      'digest', new.policy_digest
    ),
    'starts_at', to_char(
      new.starts_at at time zone 'UTC',
      'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
    ),
    'expires_at', to_char(
      new.expires_at at time zone 'UTC',
      'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
    ),
    'issued_at', to_char(
      new.issued_at at time zone 'UTC',
      'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
    )
  );

  if new.grant_kind = 'root' then
    if not exists (
      select 1
      from xfactory_runtime_v2.installation_trust_anchors anchor_record
      where anchor_record.installation_id = new.installation_id
        and anchor_record.anchor_id = new.trust_anchor_id
        and anchor_record.record_digest = new.trust_anchor_digest
    ) then
      raise exception using
        errcode = '42501',
        message = 'HGR-GRANT-ANCHOR-REFERENCE';
    end if;
    grant_payload := grant_payload || jsonb_build_object(
      'root_anchor_ref', jsonb_build_object(
        'installation_id', new.installation_id,
        'anchor_id', new.trust_anchor_id,
        'record_digest', new.trust_anchor_digest
      )
    );
  else
    if not exists (
      select 1
      from xfactory_runtime_v2.authority_grants issuer_grant
      where issuer_grant.installation_id = new.installation_id
        and issuer_grant.grant_id = new.issuer_grant_id
        and issuer_grant.record_digest = new.issuer_grant_digest
    ) then
      raise exception using
        errcode = '42501',
        message = 'HGR-GRANT-ISSUER-REFERENCE';
    end if;
    grant_payload := grant_payload || jsonb_build_object(
      'issuer_grant_ref', jsonb_build_object(
        'installation_id', new.installation_id,
        'grant_id', new.issuer_grant_id,
        'record_digest', new.issuer_grant_digest
      )
    );
  end if;

  new.record_digest :=
    xfactory_runtime_v2.canonical_record_digest(grant_payload);
  return new;
end
$function$;

drop trigger if exists installation_trust_anchors_compute_digest
  on xfactory_runtime_v2.installation_trust_anchors;
create trigger installation_trust_anchors_compute_digest
before insert on xfactory_runtime_v2.installation_trust_anchors
for each row execute function
  xfactory_runtime_v2.compute_trust_anchor_record_digest();

drop trigger if exists authority_grants_compute_digest
  on xfactory_runtime_v2.authority_grants;
create trigger authority_grants_compute_digest
before insert on xfactory_runtime_v2.authority_grants
for each row execute function
  xfactory_runtime_v2.compute_authority_grant_record_digest();

create or replace function xfactory_runtime_api_v2.revoke_authority_grant(
  requested_revocation_id text,
  requested_grant_id text,
  requested_revoker_grant_id text,
  requested_reason text
)
returns void
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  scope_installation text := current_setting('xfactory.installation_id', true);
  scope_stack text := current_setting('xfactory.stack_id', true);
  scope_layer text := current_setting('xfactory.layer_id', true);
  actor_principal text := current_setting('xfactory.principal_id', true);
  revoked_grant xfactory_runtime_v2.authority_grants%rowtype;
  effective_time timestamptz := transaction_timestamp();
  revocation_digest text;
begin
  if not xfactory_runtime_api_v2.current_scope_matches(
    scope_installation, scope_stack, scope_layer
  ) then
    raise exception using errcode = '42501', message = 'HGR-SCOPE-NOT-ASSUMED';
  end if;
  perform pg_advisory_xact_lock(
    hashtextextended('anchor:' || scope_installation, 0)
  );
  perform pg_advisory_xact_lock(
    hashtextextended('grant:' || least(requested_grant_id, requested_revoker_grant_id), 0)
  );
  perform pg_advisory_xact_lock(
    hashtextextended('grant:' || greatest(requested_grant_id, requested_revoker_grant_id), 0)
  );

  select grant_record.*
  into strict revoked_grant
  from xfactory_runtime_v2.authority_grants grant_record
  where grant_record.installation_id = scope_installation
    and grant_record.grant_id = requested_grant_id
  for update;

  if not exists (
    select 1
    from xfactory_runtime_v2.active_authority_chain(
      scope_installation,
      requested_revoker_grant_id,
      'revoke_grant',
      'installation',
      '',
      '',
      actor_principal,
      effective_time
    )
  ) or not exists (
    select 1
    from xfactory_runtime_v2.authority_grants revoker
    where revoker.installation_id = scope_installation
      and revoker.grant_id = requested_revoker_grant_id
      and revoker.resource_type = 'authority_grant'
      and revoker.resource_id = revoked_grant.grant_id
      and revoker.resource_digest = revoked_grant.record_digest
  ) then
    raise exception using errcode = '42501', message = 'HGR-GRANT-REVOCATION-AUTHORITY';
  end if;
  revocation_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'installation_id', scope_installation,
      'revocation_id', requested_revocation_id,
      'grant_id', revoked_grant.grant_id,
      'grant_digest', revoked_grant.record_digest,
      'revoker_grant_id', requested_revoker_grant_id,
      'reason', requested_reason,
      'effective_at', to_char(effective_time at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"')
    )
  );
  insert into xfactory_runtime_v2.authority_grant_revocations (
    installation_id, revocation_id, record_digest, grant_id, grant_digest,
    revoker_grant_id, reason, effective_at
  ) values (
    scope_installation, requested_revocation_id, revocation_digest,
    revoked_grant.grant_id, revoked_grant.record_digest,
    requested_revoker_grant_id, requested_reason, effective_time
  );
end
$function$;

create or replace function xfactory_runtime_api_v2.revoke_cross_layer_binding(
  requested_revocation_id text,
  requested_binding_id text,
  requested_source_revoker_grant_id text,
  requested_target_acceptance_grant_id text,
  requested_reason text
)
returns void
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  scope_installation text := current_setting('xfactory.installation_id', true);
  scope_stack text := current_setting('xfactory.stack_id', true);
  scope_layer text := current_setting('xfactory.layer_id', true);
  actor_principal text := current_setting('xfactory.principal_id', true);
  binding_record xfactory_runtime_v2.cross_layer_bindings%rowtype;
  effective_time timestamptz := transaction_timestamp();
  revocation_digest text;
begin
  if not xfactory_runtime_api_v2.current_scope_matches(
    scope_installation, scope_stack, scope_layer
  ) then
    raise exception using errcode = '42501', message = 'HGR-SCOPE-NOT-ASSUMED';
  end if;
  perform pg_advisory_xact_lock(
    hashtextextended('anchor:' || scope_installation, 0)
  );
  perform pg_advisory_xact_lock(
    hashtextextended(
      'grant:' || least(
        requested_source_revoker_grant_id,
        requested_target_acceptance_grant_id
      ),
      0
    )
  );
  perform pg_advisory_xact_lock(
    hashtextextended(
      'grant:' || greatest(
        requested_source_revoker_grant_id,
        requested_target_acceptance_grant_id
      ),
      0
    )
  );
  perform pg_advisory_xact_lock(
    hashtextextended('binding:' || requested_binding_id, 0)
  );

  select binding.*
  into strict binding_record
  from xfactory_runtime_v2.cross_layer_bindings binding
  where binding.installation_id = scope_installation
    and binding.binding_id = requested_binding_id
  for update;

  if not (scope_stack = '' and scope_layer = '')
     and (
       binding_record.source_stack_id <> scope_stack
       or binding_record.source_layer_id <> scope_layer
     ) then
    raise exception using errcode = '42501', message = 'HGR-BINDING-DIRECTION';
  end if;
  if not exists (
    select 1
    from xfactory_runtime_v2.active_authority_chain(
      scope_installation,
      requested_source_revoker_grant_id,
      'revoke_binding',
      'layer',
      binding_record.source_stack_id,
      binding_record.source_layer_id,
      actor_principal,
      effective_time
    )
  ) or not exists (
    select 1
    from xfactory_runtime_v2.authority_grants revoker
    where revoker.installation_id = scope_installation
      and revoker.grant_id = requested_source_revoker_grant_id
      and revoker.resource_type = 'cross_layer_binding'
      and revoker.resource_id = binding_record.binding_id
      and revoker.resource_digest = binding_record.record_digest
  ) then
    raise exception using errcode = '42501', message = 'HGR-BINDING-REVOCATION-AUTHORITY';
  end if;
  if not exists (
    select 1
    from xfactory_runtime_v2.active_authority_chain(
      scope_installation,
      requested_target_acceptance_grant_id,
      'accept_cross_layer',
      'layer',
      binding_record.target_stack_id,
      binding_record.target_layer_id,
      null,
      effective_time
    )
  ) or requested_target_acceptance_grant_id <>
    binding_record.target_acceptance_grant_id then
    raise exception using errcode = '42501', message = 'HGR-BINDING-TARGET-ACCEPTANCE';
  end if;

  revocation_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'installation_id', scope_installation,
      'revocation_id', requested_revocation_id,
      'binding_id', binding_record.binding_id,
      'binding_digest', binding_record.record_digest,
      'source_revoker_grant_id', requested_source_revoker_grant_id,
      'target_acceptance_grant_id', requested_target_acceptance_grant_id,
      'reason', requested_reason,
      'effective_at', to_char(effective_time at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"')
    )
  );
  insert into xfactory_runtime_v2.cross_layer_binding_revocations (
    installation_id, revocation_id, record_digest, binding_id,
    binding_digest, source_revoker_grant_id, target_acceptance_grant_id,
    reason, effective_at
  ) values (
    scope_installation, requested_revocation_id, revocation_digest,
    binding_record.binding_id, binding_record.record_digest,
    requested_source_revoker_grant_id, requested_target_acceptance_grant_id,
    requested_reason, effective_time
  );
end
$function$;

create or replace function xfactory_runtime_api_v2.project_artifact(
  requested_operation_id text,
  requested_binding_id text,
  requested_source_artifact_id text,
  requested_source_digest text,
  requested_target_artifact_id text,
  requested_target_digest text,
  requested_source_grant_id text,
  requested_trace_id text
)
returns void
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  scope_installation text := current_setting('xfactory.installation_id', true);
  scope_stack text := current_setting('xfactory.stack_id', true);
  scope_layer text := current_setting('xfactory.layer_id', true);
  actor_principal text := current_setting('xfactory.principal_id', true);
  binding_record xfactory_runtime_v2.cross_layer_bindings%rowtype;
  source_record xfactory_runtime_v2.artifact_records%rowtype;
  source_body xfactory_runtime_v2.artifact_bodies%rowtype;
  target_record xfactory_runtime_v2.artifact_records%rowtype;
  target_body xfactory_runtime_v2.artifact_bodies%rowtype;
  creator_chain record;
  source_chain record;
  accepted_chain record;
  authorization_time timestamptz := transaction_timestamp();
  target_record_digest text;
  operation_digest text;
  projection_digest text;
  trace_digest text;
  transaction_correlation text;
  actor_principal_digest text;
  source_grant_digest text;
  target_acceptance_principal_digest text;
  target_lifecycle_digest text;
begin
  if not xfactory_runtime_api_v2.current_scope_matches(
    scope_installation, scope_stack, scope_layer
  ) then
    raise exception using errcode = '42501', message = 'HGR-SCOPE-NOT-ASSUMED';
  end if;
  if requested_source_digest !~ '^sha256:[0-9a-f]{64}$'
     or requested_target_digest !~ '^sha256:[0-9a-f]{64}$' then
    raise exception using errcode = '22023', message = 'HGR-OPERATION-DIGEST-INVALID';
  end if;

  select binding.*
  into strict binding_record
  from xfactory_runtime_v2.cross_layer_bindings binding
  where binding.installation_id = scope_installation
    and binding.binding_id = requested_binding_id;

  perform pg_advisory_xact_lock(
    hashtextextended('anchor:' || scope_installation, 0)
  );
  perform pg_advisory_xact_lock(hashtextextended('grant:' || locks.grant_id, 0))
  from (
    select distinct grant_id
    from unnest(array[
      binding_record.creator_grant_id,
      requested_source_grant_id,
      binding_record.target_acceptance_grant_id
    ]) grant_id
    order by grant_id
  ) locks;
  perform pg_advisory_xact_lock(
    hashtextextended('binding:' || requested_binding_id, 0)
  );
  perform pg_advisory_xact_lock(
    hashtextextended(
      least(
        'resource:' || scope_installation || ':' ||
          binding_record.source_stack_id || ':' ||
          binding_record.source_layer_id || ':' || requested_source_artifact_id,
        'resource:' || scope_installation || ':' ||
          binding_record.target_stack_id || ':' ||
          binding_record.target_layer_id || ':' || requested_target_artifact_id
      ),
      0
    )
  );
  perform pg_advisory_xact_lock(
    hashtextextended(
      greatest(
        'resource:' || scope_installation || ':' ||
          binding_record.source_stack_id || ':' ||
          binding_record.source_layer_id || ':' || requested_source_artifact_id,
        'resource:' || scope_installation || ':' ||
          binding_record.target_stack_id || ':' ||
          binding_record.target_layer_id || ':' || requested_target_artifact_id
      ),
      0
    )
  );

  select binding.*
  into strict binding_record
  from xfactory_runtime_v2.cross_layer_bindings binding
  where binding.installation_id = scope_installation
    and binding.binding_id = requested_binding_id
  for update;

  if (
       not (scope_stack = '' and scope_layer = '')
       and (
         binding_record.source_stack_id <> scope_stack
         or binding_record.source_layer_id <> scope_layer
       )
     )
     or binding_record.source_resource_type <> 'artifact'
     or binding_record.target_resource_type <> 'artifact'
     or binding_record.source_resource_id <> requested_source_artifact_id
     or binding_record.source_resource_digest <> requested_source_digest
     or binding_record.target_resource_id <> requested_target_artifact_id
     or binding_record.target_resource_digest <> requested_target_digest
     or binding_record.action <> 'project_resource' then
    raise exception using errcode = '42501', message = 'HGR-BINDING-RESOURCE-MISMATCH';
  end if;
  if binding_record.starts_at > authorization_time
     or binding_record.expires_at <= authorization_time
     or exists (
       select 1
       from xfactory_runtime_v2.cross_layer_binding_revocations revoked
       where revoked.installation_id = binding_record.installation_id
         and revoked.binding_id = binding_record.binding_id
         and revoked.binding_digest = binding_record.record_digest
         and revoked.effective_at <= authorization_time
     ) then
    raise exception using errcode = '42501', message = 'HGR-BINDING-INACTIVE';
  end if;

  select *
  into creator_chain
  from xfactory_runtime_v2.active_authority_chain(
    scope_installation,
    binding_record.creator_grant_id,
    'create_binding',
    'layer',
    binding_record.source_stack_id,
    binding_record.source_layer_id,
    binding_record.creator_principal_id,
    authorization_time
  );
  if not found or not exists (
    select 1
    from xfactory_runtime_v2.authority_grants creator
    where creator.installation_id = scope_installation
      and creator.grant_id = binding_record.creator_grant_id
      and creator.record_digest = binding_record.creator_grant_digest
      and creator.grantee_principal_id = binding_record.creator_principal_id
      and creator.grantee_principal_digest = binding_record.creator_principal_digest
      and creator.resource_type = 'artifact'
      and creator.resource_id = requested_source_artifact_id
      and creator.resource_digest = requested_source_digest
  ) then
    raise exception using errcode = '42501', message = 'HGR-BINDING-SOURCE-AUTHORITY';
  end if;

  select *
  into source_chain
  from xfactory_runtime_v2.active_authority_chain(
    scope_installation,
    requested_source_grant_id,
    'project_resource',
    'layer',
    binding_record.source_stack_id,
    binding_record.source_layer_id,
    actor_principal,
    authorization_time
  );
  if not found or not exists (
    select 1
    from xfactory_runtime_v2.authority_grants source_grant
    where source_grant.installation_id = scope_installation
      and source_grant.grant_id = requested_source_grant_id
      and source_grant.resource_type = 'artifact'
      and source_grant.resource_id = requested_source_artifact_id
      and source_grant.resource_digest = requested_source_digest
  ) then
    raise exception using errcode = '42501', message = 'HGR-OPERATION-SOURCE-AUTHORITY';
  end if;

  select *
  into accepted_chain
  from xfactory_runtime_v2.active_authority_chain(
    scope_installation,
    binding_record.target_acceptance_grant_id,
    'accept_cross_layer',
    'layer',
    binding_record.target_stack_id,
    binding_record.target_layer_id,
    null,
    authorization_time
  );
  if not found or not exists (
    select 1
    from xfactory_runtime_v2.authority_grants acceptance
    where acceptance.installation_id = scope_installation
      and acceptance.grant_id = binding_record.target_acceptance_grant_id
      and acceptance.record_digest =
        binding_record.target_acceptance_grant_digest
      and acceptance.resource_type = 'artifact'
      and acceptance.resource_id = requested_target_artifact_id
      and acceptance.resource_digest = requested_target_digest
  ) then
    raise exception using errcode = '42501', message = 'HGR-BINDING-TARGET-ACCEPTANCE';
  end if;

  select principal.record_digest
  into strict actor_principal_digest
  from xfactory_runtime_v2.principals principal
  where principal.installation_id = scope_installation
    and principal.stack_id = ''
    and principal.layer_id = ''
    and principal.principal_id = actor_principal;
  select record_digest
  into strict source_grant_digest
  from xfactory_runtime_v2.authority_grants
  where installation_id = scope_installation
    and grant_id = requested_source_grant_id;
  select record_digest
  into strict target_acceptance_principal_digest
  from xfactory_runtime_v2.principals
  where installation_id = scope_installation
    and stack_id = binding_record.target_acceptance_principal_stack_id
    and layer_id = binding_record.target_acceptance_principal_layer_id
    and principal_id = binding_record.target_acceptance_principal_id;

  select record.*
  into strict source_record
  from xfactory_runtime_v2.artifact_records record
  where record.installation_id = scope_installation
    and record.stack_id = binding_record.source_stack_id
    and record.layer_id = binding_record.source_layer_id
    and record.artifact_id = requested_source_artifact_id
  for share;
  select body.*
  into strict source_body
  from xfactory_runtime_v2.artifact_bodies body
  where body.installation_id = scope_installation
    and body.stack_id = binding_record.source_stack_id
    and body.layer_id = binding_record.source_layer_id
    and body.artifact_id = requested_source_artifact_id
  for share;
  if source_record.content_digest <> requested_source_digest
     or source_body.content_digest <> requested_source_digest
     or source_body.content_digest <>
       'sha256:' || encode(sha256(source_body.content), 'hex')
     or source_body.byte_size <> octet_length(source_body.content)
     or requested_target_digest <> requested_source_digest then
    raise exception using errcode = '55000', message = 'HGR-ARTIFACT-BODY-DRIFT';
  end if;

  select record.*
  into strict target_record
  from xfactory_runtime_v2.artifact_records record
  where record.installation_id = scope_installation
    and record.stack_id = binding_record.target_stack_id
    and record.layer_id = binding_record.target_layer_id
    and record.artifact_id = requested_target_artifact_id
  for share;
  select body.*
  into strict target_body
  from xfactory_runtime_v2.artifact_bodies body
  where body.installation_id = scope_installation
    and body.stack_id = binding_record.target_stack_id
    and body.layer_id = binding_record.target_layer_id
    and body.artifact_id = requested_target_artifact_id
  for share;
  if target_record.content_digest <> requested_target_digest
     or target_body.content_digest <> requested_target_digest
     or target_body.content_digest <>
       'sha256:' || encode(sha256(target_body.content), 'hex')
     or target_body.byte_size <> octet_length(target_body.content)
     or target_body.content <> source_body.content
     or exists (
       select 1
       from xfactory_runtime_v2.artifact_lifecycle_events lifecycle
       where lifecycle.installation_id = target_record.installation_id
         and lifecycle.stack_id = target_record.stack_id
         and lifecycle.layer_id = target_record.layer_id
         and lifecycle.artifact_id = target_record.artifact_id
         and lifecycle.event_type = 'available'
     ) then
    raise exception using errcode = '55000', message = 'HGR-TARGET-DRAFT-MISMATCH';
  end if;

  transaction_correlation := 'tx-' || txid_current()::text || '-' || requested_operation_id;
  target_record_digest := target_record.record_digest;
  operation_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'schema_version', 1,
      'kind', 'openxfactory-operation-authorization',
      'operation_id', requested_operation_id,
      'record_digest_profile', 'xfactory-canonical-json-v1',
      'source_scope', jsonb_build_object(
        'scope_kind', 'layer', 'installation_id', scope_installation,
        'stack_id', binding_record.source_stack_id,
        'layer_id', binding_record.source_layer_id
      ),
      'target_scope', jsonb_build_object(
        'scope_kind', 'layer', 'installation_id', scope_installation,
        'stack_id', binding_record.target_stack_id,
        'layer_id', binding_record.target_layer_id
      ),
      'source_resource', jsonb_build_object(
        'installation_id', scope_installation,
        'stack_id', binding_record.source_stack_id,
        'layer_id', binding_record.source_layer_id,
        'resource_type', 'artifact', 'resource_id', requested_source_artifact_id,
        'digest', requested_source_digest
      ),
      'target_resource', jsonb_build_object(
        'installation_id', scope_installation,
        'stack_id', binding_record.target_stack_id,
        'layer_id', binding_record.target_layer_id,
        'resource_type', 'artifact', 'resource_id', requested_target_artifact_id,
        'digest', requested_target_digest
      ),
      'action', 'project_resource',
      'purpose', binding_record.purpose,
      'actor_principal_ref', jsonb_build_object(
        'scope', jsonb_build_object(
          'scope_kind', 'installation_admin',
          'installation_id', scope_installation
        ),
        'principal_id', actor_principal,
        'record_digest', actor_principal_digest
      ),
      'source_grant_ref', jsonb_build_object(
        'installation_id', scope_installation,
        'grant_id', requested_source_grant_id,
        'record_digest', source_grant_digest
      ),
      'target_acceptance_grant_ref', jsonb_build_object(
        'installation_id', scope_installation,
        'grant_id', binding_record.target_acceptance_grant_id,
        'record_digest', binding_record.target_acceptance_grant_digest
      ),
      'binding_ref', jsonb_build_object(
        'installation_id', scope_installation,
        'binding_id', binding_record.binding_id,
        'record_digest', binding_record.record_digest
      ),
      'anchor_ref', jsonb_build_object(
        'installation_id', scope_installation,
        'anchor_id', source_chain.root_anchor_id,
        'record_digest', source_chain.root_anchor_digest
      ),
      'authorized_at', to_char(authorization_time at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'),
      'target_result', jsonb_build_object(
        'installation_id', scope_installation,
        'stack_id', binding_record.target_stack_id,
        'layer_id', binding_record.target_layer_id,
        'resource_type', 'artifact', 'resource_id', requested_target_artifact_id,
        'digest', requested_target_digest
      ),
      'transaction_id', transaction_correlation
    )
  );
  projection_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'installation_id', scope_installation,
      'projection_id', requested_operation_id,
      'binding_id', binding_record.binding_id,
      'target_id', requested_target_artifact_id,
      'target_digest', requested_target_digest
    )
  );
  trace_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'schema_version', 1,
      'kind', 'openxfactory-hermes-runtime-traceability-edge',
      'edge_id', requested_trace_id,
      'owning_scope', jsonb_build_object(
        'scope_kind', 'layer', 'installation_id', scope_installation,
        'stack_id', binding_record.target_stack_id,
        'layer_id', binding_record.target_layer_id
      ),
      'relation', 'project_resource',
      'source', jsonb_build_object(
        'installation_id', scope_installation,
        'stack_id', binding_record.source_stack_id,
        'layer_id', binding_record.source_layer_id,
        'resource_type', 'artifact', 'resource_id', requested_source_artifact_id,
        'digest', requested_source_digest
      ),
      'target', jsonb_build_object(
        'installation_id', scope_installation,
        'stack_id', binding_record.target_stack_id,
        'layer_id', binding_record.target_layer_id,
        'resource_type', 'artifact', 'resource_id', requested_target_artifact_id,
        'digest', requested_target_digest
      ),
      'creator_principal_ref', jsonb_build_object(
        'scope', jsonb_build_object(
          'scope_kind', 'installation_admin', 'installation_id', scope_installation
        ),
        'principal_id', actor_principal,
        'record_digest', actor_principal_digest
      ),
      'creator_grant_ref', jsonb_build_object(
        'installation_id', scope_installation,
        'grant_id', requested_source_grant_id,
        'record_digest', source_grant_digest
      ),
      'cross_layer_authority', jsonb_build_object(
        'operation_authorization_ref', jsonb_build_object(
          'installation_id', scope_installation,
          'operation_id', requested_operation_id,
          'record_digest', operation_digest
        ),
        'binding_ref', jsonb_build_object(
          'installation_id', scope_installation,
          'binding_id', binding_record.binding_id,
          'record_digest', binding_record.record_digest
        ),
        'grant_refs', jsonb_build_array(
          jsonb_build_object(
            'installation_id', scope_installation,
            'grant_id', requested_source_grant_id,
            'record_digest', source_grant_digest
          ),
          jsonb_build_object(
            'installation_id', scope_installation,
            'grant_id', binding_record.target_acceptance_grant_id,
            'record_digest', binding_record.target_acceptance_grant_digest
          )
        )
      ),
      'created_at', to_char(authorization_time at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"')
    )
  );
  target_lifecycle_digest := xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'schema_version', 1,
      'kind', 'openxfactory-hermes-runtime-artifact-lifecycle-event',
      'event_id', requested_operation_id || ':available',
      'installation_id', scope_installation,
      'stack_id', binding_record.target_stack_id,
      'layer_id', binding_record.target_layer_id,
      'artifact_id', requested_target_artifact_id,
      'artifact_record_digest', target_record_digest,
      'predecessor_ref', jsonb_build_object(
        'kind', 'artifact_record', 'id', requested_target_artifact_id,
        'digest', target_record_digest
      ),
      'event_type', 'available',
      'actor_principal_ref', jsonb_build_object(
        'scope', jsonb_build_object(
          'scope_kind', 'installation_admin', 'installation_id', scope_installation
        ),
        'principal_id', actor_principal,
        'record_digest', actor_principal_digest
      ),
      'actor_grant_ref', jsonb_build_object(
        'installation_id', scope_installation,
        'grant_id', requested_source_grant_id,
        'record_digest', source_grant_digest
      ),
      'occurred_at', to_char(authorization_time at time zone 'UTC',
        'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'),
      'reason', 'cross-layer projection'
    )
  );

  insert into xfactory_runtime_v2.artifact_lifecycle_events (
    installation_id, stack_id, layer_id, artifact_id, event_id,
    event_digest, artifact_record_digest, predecessor_kind, predecessor_id,
    predecessor_digest, event_type, actor_principal_id,
    actor_principal_digest, actor_grant_id, actor_grant_digest,
    reason, occurred_at
  ) values (
    scope_installation, binding_record.target_stack_id,
    binding_record.target_layer_id, requested_target_artifact_id,
    requested_operation_id || ':available', target_lifecycle_digest,
    target_record_digest, 'artifact_record', requested_target_artifact_id,
    target_record_digest, 'available', actor_principal,
    actor_principal_digest, requested_source_grant_id, source_grant_digest,
    'cross-layer projection', authorization_time
  );
  insert into xfactory_runtime_v2.governed_projections (
    installation_id, stack_id, layer_id, projection_id, record_digest,
    source_stack_id, source_layer_id, source_resource_type,
    source_resource_id, source_resource_digest, target_resource_type,
    target_resource_id, target_resource_digest, binding_id, operation_id,
    created_at
  ) values (
    scope_installation, binding_record.target_stack_id,
    binding_record.target_layer_id, requested_operation_id, projection_digest,
    binding_record.source_stack_id, binding_record.source_layer_id, 'artifact',
    requested_source_artifact_id, requested_source_digest, 'artifact',
    requested_target_artifact_id, requested_target_digest,
    binding_record.binding_id, requested_operation_id, authorization_time
  );
  insert into xfactory_runtime_v2.operation_authorizations (
    installation_id, operation_id, record_digest, digest_profile,
    binding_id, binding_digest, source_stack_id, source_layer_id,
    source_resource_type, source_resource_id, source_resource_digest,
    target_stack_id, target_layer_id, target_resource_type,
    target_resource_id, target_resource_digest, action, purpose,
    actor_stack_id, actor_layer_id, actor_principal_id,
    actor_principal_digest, source_grant_id, source_grant_digest,
    target_acceptance_grant_id, target_acceptance_grant_digest,
    trust_anchor_id, trust_anchor_digest, transaction_id,
    target_result_type, target_result_id, target_result_digest, authorized_at
  ) values (
    scope_installation, requested_operation_id, operation_digest,
    'xfactory-canonical-json-v1', binding_record.binding_id,
    binding_record.record_digest, binding_record.source_stack_id,
    binding_record.source_layer_id, 'artifact',
    requested_source_artifact_id, requested_source_digest,
    binding_record.target_stack_id, binding_record.target_layer_id, 'artifact',
    requested_target_artifact_id, requested_target_digest, 'project_resource',
    binding_record.purpose, '', '', actor_principal, actor_principal_digest,
    requested_source_grant_id, source_grant_digest,
    binding_record.target_acceptance_grant_id,
    binding_record.target_acceptance_grant_digest,
    source_chain.root_anchor_id, source_chain.root_anchor_digest,
    transaction_correlation, 'artifact', requested_target_artifact_id,
    requested_target_digest, authorization_time
  );
  insert into xfactory_runtime_v2.traceability_edges (
    installation_id, stack_id, layer_id, edge_id, edge_digest,
    source_stack_id, source_layer_id, source_type, source_id, source_digest,
    target_stack_id, target_layer_id, target_type, target_id, target_digest,
    relation, creator_stack_id, creator_layer_id, creator_principal_id,
    creator_principal_digest, creator_grant_id, creator_grant_digest,
    operation_id, operation_digest, binding_id, binding_digest, grant_refs,
    created_at
  ) values (
    scope_installation, binding_record.target_stack_id,
    binding_record.target_layer_id, requested_trace_id, trace_digest,
    binding_record.source_stack_id, binding_record.source_layer_id, 'artifact',
    requested_source_artifact_id, requested_source_digest,
    binding_record.target_stack_id, binding_record.target_layer_id, 'artifact',
    requested_target_artifact_id, requested_target_digest, 'project_resource',
    '', '', actor_principal, actor_principal_digest,
    requested_source_grant_id, source_grant_digest,
    requested_operation_id, operation_digest, binding_record.binding_id,
    binding_record.record_digest,
    jsonb_build_array(
      jsonb_build_object(
        'installation_id', scope_installation,
        'grant_id', requested_source_grant_id,
        'record_digest', source_grant_digest
      ),
      jsonb_build_object(
        'installation_id', scope_installation,
        'grant_id', binding_record.target_acceptance_grant_id,
        'record_digest', binding_record.target_acceptance_grant_digest
      )
    ),
    authorization_time
  );
end
$function$;

do $row_security$
declare
  relation_name text;
  policy_name text;
begin
  foreach relation_name in array array[
    'layer_registrations',
    'layer_lifecycle_events',
    'principals',
    'principal_lifecycle_events',
    'database_principal_bindings',
    'database_principal_binding_revocations',
    'artifact_bodies',
    'artifact_records',
    'artifact_lifecycle_events',
    'approval_decision_policies',
    'approval_requests',
    'approval_decisions',
    'approval_supersession_events',
    'governed_projections',
    'traceability_edges'
  ]
  loop
    execute format(
      'alter table xfactory_runtime_v2.%I enable row level security',
      relation_name
    );
    execute format(
      'alter table xfactory_runtime_v2.%I force row level security',
      relation_name
    );
    policy_name := relation_name || '_exact_scope';
    execute format(
      'drop policy if exists %I on xfactory_runtime_v2.%I',
      policy_name,
      relation_name
    );
    execute format(
      'create policy %I on xfactory_runtime_v2.%I '
      'using (current_user = %L or '
      'xfactory_runtime_api_v2.current_scope_matches('
      'installation_id, stack_id, layer_id)) '
      'with check (current_user = %L or '
      'xfactory_runtime_api_v2.current_scope_matches('
      'installation_id, stack_id, layer_id))',
      policy_name,
      relation_name,
      'xfactory_v2_owner',
      'xfactory_v2_owner'
    );
  end loop;

  alter table xfactory_runtime_v2.operation_authorizations
    enable row level security;
  alter table xfactory_runtime_v2.operation_authorizations
    force row level security;
  drop policy if exists operation_authorizations_exact_scope
    on xfactory_runtime_v2.operation_authorizations;
  create policy operation_authorizations_exact_scope
    on xfactory_runtime_v2.operation_authorizations
    using (
      current_user = 'xfactory_v2_owner'
      or xfactory_runtime_api_v2.current_scope_matches(
        installation_id, target_stack_id, target_layer_id
      )
    )
    with check (
      current_user = 'xfactory_v2_owner'
      or xfactory_runtime_api_v2.current_scope_matches(
        installation_id, target_stack_id, target_layer_id
      )
    );
end
$row_security$;

revoke all on all tables in schema xfactory_runtime_v2 from public;
revoke all on all sequences in schema xfactory_runtime_v2 from public;
revoke all on all functions in schema xfactory_runtime_v2 from public;
revoke all on all functions in schema xfactory_runtime_api_v2 from public;

grant select on
  xfactory_runtime_v2.layer_registrations,
  xfactory_runtime_v2.layer_lifecycle_events,
  xfactory_runtime_v2.principals,
  xfactory_runtime_v2.principal_lifecycle_events,
  xfactory_runtime_v2.database_principal_bindings,
  xfactory_runtime_v2.database_principal_binding_revocations,
  xfactory_runtime_v2.artifact_records,
  xfactory_runtime_v2.artifact_lifecycle_events,
  xfactory_runtime_v2.approval_decision_policies,
  xfactory_runtime_v2.approval_requests,
  xfactory_runtime_v2.approval_decisions,
  xfactory_runtime_v2.approval_supersession_events,
  xfactory_runtime_v2.governed_projections,
  xfactory_runtime_v2.operation_authorizations,
  xfactory_runtime_v2.traceability_edges
to xfactory_v2_runtime, xfactory_v2_audit;

grant execute on function
  xfactory_runtime_api_v2.current_scope_matches(text, text, text),
  xfactory_runtime_api_v2.assume_scope(text, text, text, text),
  xfactory_runtime_api_v2.clear_scope(),
  xfactory_runtime_api_v2.transition_layer(
    text, text, text, text, text, text, text
  ),
  xfactory_runtime_api_v2.admit_artifact(text, bytea, text, text),
  xfactory_runtime_api_v2.probe_artifact(text),
  xfactory_runtime_api_v2.record_approval_decision(
    text, text, text, text
  ),
  xfactory_runtime_api_v2.supersede_approval(
    text, text, text, text, text, text
  ),
  xfactory_runtime_api_v2.approval_authorizes(text)
to xfactory_v2_runtime;

grant execute on function
  xfactory_runtime_api_v2.current_scope_matches(text, text, text),
  xfactory_runtime_api_v2.assume_scope(text, text, text, text),
  xfactory_runtime_api_v2.clear_scope(),
  xfactory_runtime_api_v2.transition_layer(
    text, text, text, text, text, text, text
  ),
  xfactory_runtime_api_v2.project_artifact(
    text, text, text, text, text, text, text, text
  ),
  xfactory_runtime_api_v2.revoke_authority_grant(
    text, text, text, text
  ),
  xfactory_runtime_api_v2.revoke_cross_layer_binding(
    text, text, text, text, text
  ),
  xfactory_runtime_api_v2.probe_artifact(text)
to xfactory_v2_control;

grant execute on function
  xfactory_runtime_api_v2.current_scope_matches(text, text, text),
  xfactory_runtime_api_v2.assume_scope(text, text, text, text),
  xfactory_runtime_api_v2.clear_scope(),
  xfactory_runtime_api_v2.probe_artifact(text),
  xfactory_runtime_api_v2.approval_authorizes(text)
to xfactory_v2_audit;

-- v1-to-v2 migration surface (US3): append-only evolution of this contract.
-- Adds the migration staging/attempt/event/observation/reconciliation ledger,
-- the eight scoped legacy_* compatibility-history tables, the sealed legacy
-- quarantine record table, the exact xfactory-v1-dataset-binary-v1 framing
-- and canonical-JSON derivation functions, the durable v1 write freeze, and
-- the governed migrator-only API entrypoints.

create table if not exists xfactory_runtime_v2.migration_staging (
  installation_id text not null,
  migration_id text not null,
  payload jsonb not null,
  authority_envelope jsonb not null,
  mapping_payload_digest text not null
    check (mapping_payload_digest ~ '^sha256:[0-9a-f]{64}$'),
  authority_envelope_digest text not null
    check (authority_envelope_digest ~ '^sha256:[0-9a-f]{64}$'),
  staged_at timestamptz not null,
  primary key (installation_id, migration_id),
  foreign key (installation_id)
    references xfactory_runtime_v2.installation_registrations(installation_id)
);

create table if not exists xfactory_runtime_v2.migration_attempts (
  attempt_id text not null,
  installation_id text not null,
  migration_id text not null,
  mapping_payload_digest text not null
    check (mapping_payload_digest ~ '^sha256:[0-9a-f]{64}$'),
  created_at timestamptz not null,
  primary key (installation_id, migration_id, attempt_id),
  foreign key (installation_id, migration_id)
    references xfactory_runtime_v2.migration_staging
      (installation_id, migration_id)
);

create unique index if not exists migration_attempt_identity_uq
  on xfactory_runtime_v2.migration_attempts (attempt_id);

create table if not exists xfactory_runtime_v2.migration_attempt_events (
  event_id text not null,
  attempt_id text not null,
  installation_id text not null,
  migration_id text not null,
  event_type text not null
    check (event_type in ('started', 'succeeded', 'failed', 'abandoned')),
  predecessor_event_id text,
  reason text,
  occurred_at timestamptz not null,
  primary key (installation_id, migration_id, event_id),
  foreign key (attempt_id)
    references xfactory_runtime_v2.migration_attempts(attempt_id)
);

create unique index if not exists migration_event_predecessor_uq
  on xfactory_runtime_v2.migration_attempt_events
    (installation_id, migration_id, predecessor_event_id);

create unique index if not exists migration_event_one_root_uq
  on xfactory_runtime_v2.migration_attempt_events
    (installation_id, migration_id)
  where predecessor_event_id is null;

create table if not exists xfactory_runtime_v2.migration_cutover_observations (
  observation_id text not null,
  attempt_id text not null,
  mapping_payload_digest text not null
    check (mapping_payload_digest ~ '^sha256:[0-9a-f]{64}$'),
  authority_envelope_digest text not null
    check (authority_envelope_digest ~ '^sha256:[0-9a-f]{64}$'),
  logical_boundary_id text not null
    check (logical_boundary_id ~ '^sha256:[0-9a-f]{64}$'),
  transaction_snapshot text not null,
  wal_position text not null,
  authorized_at timestamptz not null,
  run_migration_grant_id text not null,
  run_migration_grant_digest text not null
    check (run_migration_grant_digest ~ '^sha256:[0-9a-f]{64}$'),
  target_contract_identity jsonb not null,
  reconciliation_digest text not null
    check (reconciliation_digest ~ '^sha256:[0-9a-f]{64}$'),
  primary key (observation_id),
  foreign key (attempt_id)
    references xfactory_runtime_v2.migration_attempts(attempt_id)
);

create unique index if not exists migration_observation_one_per_attempt_uq
  on xfactory_runtime_v2.migration_cutover_observations (attempt_id);

create table if not exists xfactory_runtime_v2.migration_reconciliations (
  reconciliation_id text not null,
  attempt_id text not null,
  per_table jsonb not null,
  compatibility_history_count bigint not null
    check (compatibility_history_count >= 0),
  quarantine_count bigint not null check (quarantine_count >= 0),
  "freeze" jsonb not null,
  reconciliation_digest text not null
    check (reconciliation_digest ~ '^sha256:[0-9a-f]{64}$'),
  primary key (reconciliation_id),
  foreign key (attempt_id)
    references xfactory_runtime_v2.migration_attempts(attempt_id)
);

create unique index if not exists migration_reconciliation_one_per_attempt_uq
  on xfactory_runtime_v2.migration_reconciliations (attempt_id);

create table if not exists xfactory_runtime_v2.legacy_jobs (
  migration_id text not null,
  source_schema text not null,
  source_table text not null,
  source_pk text not null,
  source_row_digest text not null
    check (source_row_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_row jsonb not null,
  scope_kind text not null check (scope_kind in ('layer', 'installation_admin')),
  installation_id text not null,
  stack_id text,
  layer_id text,
  captured_at timestamptz not null,
  primary key (migration_id, source_schema, source_table, source_pk),
  check (
    (scope_kind = 'layer' and stack_id is not null and layer_id is not null)
    or (scope_kind = 'installation_admin'
        and stack_id is null and layer_id is null)
  ),
  foreign key (installation_id, stack_id, layer_id)
    references xfactory_runtime_v2.layer_registrations
      (installation_id, stack_id, layer_id)
);

create table if not exists xfactory_runtime_v2.legacy_job_runs (
  migration_id text not null,
  source_schema text not null,
  source_table text not null,
  source_pk text not null,
  source_row_digest text not null
    check (source_row_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_row jsonb not null,
  scope_kind text not null check (scope_kind in ('layer', 'installation_admin')),
  installation_id text not null,
  stack_id text,
  layer_id text,
  captured_at timestamptz not null,
  primary key (migration_id, source_schema, source_table, source_pk),
  check (
    (scope_kind = 'layer' and stack_id is not null and layer_id is not null)
    or (scope_kind = 'installation_admin'
        and stack_id is null and layer_id is null)
  ),
  foreign key (installation_id, stack_id, layer_id)
    references xfactory_runtime_v2.layer_registrations
      (installation_id, stack_id, layer_id)
);

create table if not exists xfactory_runtime_v2.legacy_job_events (
  migration_id text not null,
  source_schema text not null,
  source_table text not null,
  source_pk text not null,
  source_row_digest text not null
    check (source_row_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_row jsonb not null,
  scope_kind text not null check (scope_kind in ('layer', 'installation_admin')),
  installation_id text not null,
  stack_id text,
  layer_id text,
  captured_at timestamptz not null,
  primary key (migration_id, source_schema, source_table, source_pk),
  check (
    (scope_kind = 'layer' and stack_id is not null and layer_id is not null)
    or (scope_kind = 'installation_admin'
        and stack_id is null and layer_id is null)
  ),
  foreign key (installation_id, stack_id, layer_id)
    references xfactory_runtime_v2.layer_registrations
      (installation_id, stack_id, layer_id)
);

create table if not exists xfactory_runtime_v2.legacy_workers (
  migration_id text not null,
  source_schema text not null,
  source_table text not null,
  source_pk text not null,
  source_row_digest text not null
    check (source_row_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_row jsonb not null,
  scope_kind text not null check (scope_kind in ('layer', 'installation_admin')),
  installation_id text not null,
  stack_id text,
  layer_id text,
  captured_at timestamptz not null,
  primary key (migration_id, source_schema, source_table, source_pk),
  check (
    (scope_kind = 'layer' and stack_id is not null and layer_id is not null)
    or (scope_kind = 'installation_admin'
        and stack_id is null and layer_id is null)
  ),
  foreign key (installation_id, stack_id, layer_id)
    references xfactory_runtime_v2.layer_registrations
      (installation_id, stack_id, layer_id)
);

create table if not exists xfactory_runtime_v2.legacy_groups (
  migration_id text not null,
  source_schema text not null,
  source_table text not null,
  source_pk text not null,
  source_row_digest text not null
    check (source_row_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_row jsonb not null,
  scope_kind text not null check (scope_kind in ('layer', 'installation_admin')),
  installation_id text not null,
  stack_id text,
  layer_id text,
  captured_at timestamptz not null,
  primary key (migration_id, source_schema, source_table, source_pk),
  check (
    (scope_kind = 'layer' and stack_id is not null and layer_id is not null)
    or (scope_kind = 'installation_admin'
        and stack_id is null and layer_id is null)
  ),
  foreign key (installation_id, stack_id, layer_id)
    references xfactory_runtime_v2.layer_registrations
      (installation_id, stack_id, layer_id)
);

create table if not exists xfactory_runtime_v2.legacy_profiles (
  migration_id text not null,
  source_schema text not null,
  source_table text not null,
  source_pk text not null,
  source_row_digest text not null
    check (source_row_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_row jsonb not null,
  scope_kind text not null check (scope_kind in ('layer', 'installation_admin')),
  installation_id text not null,
  stack_id text,
  layer_id text,
  captured_at timestamptz not null,
  primary key (migration_id, source_schema, source_table, source_pk),
  check (
    (scope_kind = 'layer' and stack_id is not null and layer_id is not null)
    or (scope_kind = 'installation_admin'
        and stack_id is null and layer_id is null)
  ),
  foreign key (installation_id, stack_id, layer_id)
    references xfactory_runtime_v2.layer_registrations
      (installation_id, stack_id, layer_id)
);

create table if not exists xfactory_runtime_v2.legacy_group_memberships (
  migration_id text not null,
  source_schema text not null,
  source_table text not null,
  source_pk text not null,
  source_row_digest text not null
    check (source_row_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_row jsonb not null,
  scope_kind text not null check (scope_kind in ('layer', 'installation_admin')),
  installation_id text not null,
  stack_id text,
  layer_id text,
  captured_at timestamptz not null,
  primary key (migration_id, source_schema, source_table, source_pk),
  check (
    (scope_kind = 'layer' and stack_id is not null and layer_id is not null)
    or (scope_kind = 'installation_admin'
        and stack_id is null and layer_id is null)
  ),
  foreign key (installation_id, stack_id, layer_id)
    references xfactory_runtime_v2.layer_registrations
      (installation_id, stack_id, layer_id)
);

create table if not exists xfactory_runtime_v2.legacy_github_team_mappings (
  migration_id text not null,
  source_schema text not null,
  source_table text not null,
  source_pk text not null,
  source_row_digest text not null
    check (source_row_digest ~ '^sha256:[0-9a-f]{64}$'),
  source_row jsonb not null,
  scope_kind text not null check (scope_kind in ('layer', 'installation_admin')),
  installation_id text not null,
  stack_id text,
  layer_id text,
  captured_at timestamptz not null,
  primary key (migration_id, source_schema, source_table, source_pk),
  check (
    (scope_kind = 'layer' and stack_id is not null and layer_id is not null)
    or (scope_kind = 'installation_admin'
        and stack_id is null and layer_id is null)
  ),
  foreign key (installation_id, stack_id, layer_id)
    references xfactory_runtime_v2.layer_registrations
      (installation_id, stack_id, layer_id)
);

create table if not exists xfactory_legacy_quarantine_v2.legacy_quarantine_records (
  migration_id text not null,
  source_schema text not null,
  source_table text not null,
  source_pk text not null,
  source_row_digest text not null
    check (source_row_digest ~ '^sha256:[0-9a-f]{64}$'),
  reason_code text not null check (reason_code in (
    'missing_content_digest', 'missing_target_digest',
    'missing_reviewer_authority', 'missing_binding_evidence',
    'unverifiable_ancestry'
  )),
  source_row jsonb not null,
  captured_at timestamptz not null,
  primary key (migration_id, source_schema, source_table, source_pk)
);

create or replace function xfactory_runtime_v2.migration_u64be(
  value bigint
)
returns bytea
language plpgsql
immutable
strict
set search_path = pg_catalog
as $function$
begin
  if value < 0 then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-FRAME: u64be values must be non-negative';
  end if;
  return decode(lpad(to_hex(value), 16, '0'), 'hex');
end
$function$;

create or replace function xfactory_runtime_v2.migration_frame(
  tag integer,
  payload bytea
)
returns bytea
language sql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select decode(lpad(to_hex(tag), 2, '0'), 'hex')
    || xfactory_runtime_v2.migration_u64be(length(payload)::bigint)
    || payload
$function$;

create or replace function xfactory_runtime_v2.migration_canonical_json_string(
  value text
)
returns text
language sql
immutable
strict
set search_path = pg_catalog
as $function$
  select '"' || coalesce(string_agg(
    case
      when part.character = '"' then '\"'
      when part.character = '\' then '\\'
      when ascii(part.character) < 32
        then '\u00' || lpad(to_hex(ascii(part.character)), 2, '0')
      else part.character
    end,
    '' order by idx.char_index
  ), '') || '"'
  from generate_series(1, length(value)) as idx(char_index),
    lateral (select substr(value, idx.char_index, 1) as character) part
$function$;

create or replace function xfactory_runtime_v2.migration_canonical_json_value(
  value jsonb
)
returns text
language plpgsql
immutable
strict
set search_path = pg_catalog
as $function$
declare
  rendered text;
  numeric_text text;
begin
  case jsonb_typeof(value)
    when 'object' then
      select coalesce(
        '{' || string_agg(
          xfactory_runtime_v2.migration_canonical_json_string(member.key)
            || ':'
            || xfactory_runtime_v2.migration_canonical_json_value(member.value),
          ',' order by convert_to(member.key, 'UTF8')
        ) || '}',
        '{}'
      )
      into rendered
      from jsonb_each(value) member;
      return rendered;
    when 'array' then
      select coalesce(
        '[' || string_agg(
          xfactory_runtime_v2.migration_canonical_json_value(member.value),
          ',' order by member.ordinality
        ) || ']',
        '[]'
      )
      into rendered
      from jsonb_array_elements(value) with ordinality member(value, ordinality);
      return rendered;
    when 'string' then
      return xfactory_runtime_v2.migration_canonical_json_string(value #>> '{}');
    when 'number' then
      numeric_text := value::text;
      if numeric_text ~ '[eE]' then
        raise exception using
          errcode = '22023',
          message = 'HGR-MIGRATION-JSON-VALUE: exponent number forms are forbidden';
      end if;
      if position('.' in numeric_text) > 0 then
        numeric_text := regexp_replace(numeric_text, '0+$', '');
        numeric_text := regexp_replace(numeric_text, '\.$', '');
      end if;
      if numeric_text in ('-0', '') then
        numeric_text := '0';
      end if;
      return numeric_text;
    else
      return value::text;
  end case;
end
$function$;

create or replace function xfactory_runtime_v2.migration_reject_control_characters(
  value jsonb
)
returns void
language plpgsql
immutable
strict
set search_path = pg_catalog
as $function$
declare
  member record;
begin
  case jsonb_typeof(value)
    when 'string' then
      if (value #>> '{}') ~ '[\x01-\x1f]' then
        raise exception using
          errcode = '22023',
          message = 'HGR-MIGRATION-CONTROL-CHARACTER: control characters are '
            'forbidden in payload and envelope strings';
      end if;
    when 'object' then
      for member in select entry.key, entry.value from jsonb_each(value) entry
      loop
        if member.key ~ '[\x01-\x1f]' then
          raise exception using
            errcode = '22023',
            message = 'HGR-MIGRATION-CONTROL-CHARACTER: control characters are '
              'forbidden in payload and envelope field names';
        end if;
        perform xfactory_runtime_v2.migration_reject_control_characters(
          member.value
        );
      end loop;
    when 'array' then
      for member in
        select entry.value from jsonb_array_elements(value) entry
      loop
        perform xfactory_runtime_v2.migration_reject_control_characters(
          member.value
        );
      end loop;
    else
      null;
  end case;
end
$function$;

create or replace function xfactory_runtime_v2.migration_value_frame(
  cell jsonb
)
returns bytea
language plpgsql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  cell_kind text;
  cell_value jsonb;
  value_text text;
begin
  if jsonb_typeof(cell) <> 'object' or not cell ? 'type' then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-DATASET-VALUE: cells must carry a type field';
  end if;
  if jsonb_typeof(cell->'type') = 'null' then
    return xfactory_runtime_v2.migration_frame(x'30'::int, ''::bytea);
  end if;
  cell_kind := cell #>> '{type}';
  if cell_kind = 'null' then
    return xfactory_runtime_v2.migration_frame(x'30'::int, ''::bytea);
  end if;
  if not cell ? 'value' then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-DATASET-VALUE: non-null cells must carry a value';
  end if;
  cell_value := cell->'value';
  case cell_kind
    when 'text' then
      if jsonb_typeof(cell_value) <> 'string' then
        raise exception using
          errcode = '22023',
          message = 'HGR-MIGRATION-DATASET-VALUE: text cells must be strings';
      end if;
      return xfactory_runtime_v2.migration_frame(
        x'31'::int, convert_to(cell_value #>> '{}', 'UTF8')
      );
    when 'integer' then
      value_text := cell_value #>> '{}';
      if jsonb_typeof(cell_value) <> 'string'
         or value_text !~ '^(0|-?[1-9][0-9]*)$' then
        raise exception using
          errcode = '22023',
          message = 'HGR-MIGRATION-DATASET-VALUE: integer cells must be '
            'minimal base-10 strings';
      end if;
      return xfactory_runtime_v2.migration_frame(
        x'32'::int, convert_to(value_text, 'UTF8')
      );
    when 'boolean' then
      if jsonb_typeof(cell_value) <> 'boolean' then
        raise exception using
          errcode = '22023',
          message = 'HGR-MIGRATION-DATASET-VALUE: boolean cells must be '
            'true or false';
      end if;
      return xfactory_runtime_v2.migration_frame(
        x'33'::int,
        case when cell_value = 'true'::jsonb
          then decode('01', 'hex') else decode('00', 'hex') end
      );
    when 'timestamp' then
      value_text := cell_value #>> '{}';
      if jsonb_typeof(cell_value) <> 'string'
         or value_text !~
           '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z$'
      then
        raise exception using
          errcode = '22023',
          message = 'HGR-MIGRATION-DATASET-VALUE: timestamp cells must be UTC '
            'RFC 3339 with exactly six fractional digits and Z';
      end if;
      return xfactory_runtime_v2.migration_frame(
        x'34'::int, convert_to(value_text, 'UTF8')
      );
    when 'binary' then
      value_text := cell_value #>> '{}';
      if jsonb_typeof(cell_value) <> 'string'
         or value_text !~ '^([0-9a-f]{2})*$' then
        raise exception using
          errcode = '22023',
          message = 'HGR-MIGRATION-DATASET-VALUE: binary cells must be '
            'even-length lowercase hex';
      end if;
      return xfactory_runtime_v2.migration_frame(
        x'35'::int, convert_to(value_text, 'UTF8')
      );
    when 'json' then
      return xfactory_runtime_v2.migration_frame(
        x'36'::int,
        convert_to(
          xfactory_runtime_v2.migration_canonical_json_value(cell_value),
          'UTF8'
        )
      );
    else
      raise exception using
        errcode = '22023',
        message = 'HGR-MIGRATION-DATASET-VALUE: unknown cell type';
  end case;
end
$function$;

create or replace function xfactory_runtime_v2.migration_row_frame(
  cells jsonb
)
returns bytea
language sql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select xfactory_runtime_v2.migration_frame(
    x'20'::int,
    coalesce(
      (
        select string_agg(
          xfactory_runtime_v2.migration_frame(
            x'21'::int,
            xfactory_runtime_v2.migration_u64be(cell.ordinality)
              || xfactory_runtime_v2.migration_value_frame(cell.value)
          ),
          ''::bytea order by cell.ordinality
        )
        from jsonb_array_elements(cells) with ordinality
          cell(value, ordinality)
      ),
      ''::bytea
    )
  )
$function$;

create or replace function xfactory_runtime_v2.migration_row_digest(
  cells jsonb
)
returns text
language sql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select 'sha256:' || encode(
    sha256(xfactory_runtime_v2.migration_row_frame(cells)), 'hex'
  )
$function$;

create or replace function xfactory_runtime_v2.migration_key_frames(
  cells jsonb
)
returns bytea
language sql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select coalesce(
    (
      select string_agg(
        xfactory_runtime_v2.migration_value_frame(cell.value),
        ''::bytea order by cell.ordinality
      )
      from jsonb_array_elements(cells) with ordinality cell(value, ordinality)
    ),
    ''::bytea
  )
$function$;

create or replace function xfactory_runtime_v2.migration_canonical_v1_tables()
returns text[]
language sql
immutable
set search_path = pg_catalog
as $function$
  select array[
    'hermes_approval_requests',
    'hermes_approvals',
    'hermes_github_team_mappings',
    'hermes_group_memberships',
    'hermes_groups',
    'hermes_job_artifacts',
    'hermes_job_events',
    'hermes_job_runs',
    'hermes_jobs',
    'hermes_profiles',
    'hermes_traceability_edges',
    'hermes_workers'
  ]
$function$;

create or replace function xfactory_runtime_v2.migration_source_catalog(
  source_schema text
)
returns jsonb
language plpgsql
stable
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  table_name text;
  relation_oid oid;
  relation_kind "char";
  columns_json jsonb;
  catalog_json jsonb := '[]'::jsonb;
begin
  foreach table_name in array
    xfactory_runtime_v2.migration_canonical_v1_tables()
  loop
    select cls.oid, cls.relkind
    into relation_oid, relation_kind
    from pg_class cls
    join pg_namespace ns on ns.oid = cls.relnamespace
    where ns.nspname = source_schema
      and cls.relname = table_name;
    if relation_oid is null or relation_kind <> 'r' then
      raise exception using
        errcode = '55000',
        message = format(
          'HGR-MIGRATION-CATALOG: canonical v1 table %I.%I is missing',
          source_schema, table_name
        );
    end if;
    if not exists (
      select 1 from pg_index idx
      where idx.indrelid = relation_oid and idx.indisprimary
    ) then
      raise exception using
        errcode = '55000',
        message = format(
          'HGR-MIGRATION-CATALOG: canonical v1 table %I.%I has no primary key',
          source_schema, table_name
        );
    end if;
    select jsonb_agg(
      jsonb_build_object(
        'ordinal', column_row.ordinal,
        'name', column_row.column_name,
        'normalized_type', column_row.normalized_type,
        'nullable', column_row.nullable,
        'primary_key_position', column_row.primary_key_position
      )
      order by column_row.ordinal
    )
    into columns_json
    from (
      select
        row_number() over (order by attr.attnum) as ordinal,
        attr.attname::text as column_name,
        case typ.typname
          when 'int4' then 'int4'
          when 'int8' then 'int8'
          when 'bool' then 'bool'
          when 'text' then 'text'
          when 'timestamptz' then 'timestamptz'
          when 'jsonb' then 'jsonb'
          when 'bytea' then 'bytea'
        end as normalized_type,
        not attr.attnotnull as nullable,
        coalesce(
          (
            select key_column.position
            from pg_index idx,
              unnest(idx.indkey::int2[]) with ordinality
                as key_column(key_attnum, position)
            where idx.indrelid = relation_oid
              and idx.indisprimary
              and key_column.key_attnum = attr.attnum
          ),
          0
        ) as primary_key_position
      from pg_attribute attr
      join pg_type typ on typ.oid = attr.atttypid
      where attr.attrelid = relation_oid
        and attr.attnum > 0
        and not attr.attisdropped
    ) column_row;
    if columns_json is null
       or exists (
         select 1
         from jsonb_array_elements(columns_json) entry
         where entry.value->>'normalized_type' is null
       ) then
      raise exception using
        errcode = '55000',
        message = format(
          'HGR-MIGRATION-CATALOG: %I.%I carries an unsupported column type',
          source_schema, table_name
        );
    end if;
    catalog_json := catalog_json || jsonb_build_array(
      jsonb_build_object(
        'schema_name', source_schema,
        'table_name', table_name,
        'columns', columns_json
      )
    );
  end loop;
  return catalog_json;
end
$function$;

create or replace function xfactory_runtime_v2.migration_catalog_digest(
  catalog jsonb
)
returns text
language sql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'profile', 'xfactory-v1-catalog-v1',
      'tables', catalog
    )
  )
$function$;

create or replace function xfactory_runtime_v2.migration_live_cells_expression(
  table_entry jsonb
)
returns text
language plpgsql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  column_entry jsonb;
  cell_expressions text[] := array[]::text[];
  column_reference text;
  cell_expression text;
begin
  for column_entry in
    select entry.value
    from jsonb_array_elements(table_entry->'columns') entry
    order by (entry.value->>'ordinal')::int
  loop
    column_reference := format('t.%I', column_entry->>'name');
    case column_entry->>'normalized_type'
      when 'text' then
        cell_expression := format(
          $cell$case when %1$s is null then jsonb_build_object('type', null)
            else jsonb_build_object('type', 'text', 'value', %1$s) end$cell$,
          column_reference
        );
      when 'int4' then
        cell_expression := format(
          $cell$case when %1$s is null then jsonb_build_object('type', null)
            else jsonb_build_object('type', 'integer', 'value', %1$s::text)
            end$cell$,
          column_reference
        );
      when 'int8' then
        cell_expression := format(
          $cell$case when %1$s is null then jsonb_build_object('type', null)
            else jsonb_build_object('type', 'integer', 'value', %1$s::text)
            end$cell$,
          column_reference
        );
      when 'bool' then
        cell_expression := format(
          $cell$case when %1$s is null then jsonb_build_object('type', null)
            else jsonb_build_object('type', 'boolean', 'value', %1$s) end$cell$,
          column_reference
        );
      when 'timestamptz' then
        cell_expression := format(
          $cell$case when %1$s is null then jsonb_build_object('type', null)
            else jsonb_build_object('type', 'timestamp', 'value',
              to_char(%1$s at time zone 'UTC',
                'YYYY-MM-DD"T"HH24:MI:SS.US"Z"')) end$cell$,
          column_reference
        );
      when 'jsonb' then
        cell_expression := format(
          $cell$case when %1$s is null then jsonb_build_object('type', null)
            else jsonb_build_object('type', 'json', 'value', %1$s) end$cell$,
          column_reference
        );
      when 'bytea' then
        cell_expression := format(
          $cell$case when %1$s is null then jsonb_build_object('type', null)
            else jsonb_build_object('type', 'binary', 'value',
              encode(%1$s, 'hex')) end$cell$,
          column_reference
        );
      else
        raise exception using
          errcode = '55000',
          message = 'HGR-MIGRATION-CATALOG: unsupported normalized type';
    end case;
    cell_expressions := cell_expressions || cell_expression;
  end loop;
  return format('jsonb_build_array(%s)', array_to_string(cell_expressions, ', '));
end
$function$;

create or replace function xfactory_runtime_v2.migration_pk_cells_expression(
  table_entry jsonb
)
returns text
language plpgsql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  column_entry jsonb;
  cell_expressions text[] := array[]::text[];
begin
  for column_entry in
    select entry.value
    from jsonb_array_elements(table_entry->'columns') entry
    where (entry.value->>'primary_key_position')::int > 0
    order by (entry.value->>'primary_key_position')::int
  loop
    case column_entry->>'normalized_type'
      when 'text' then
        cell_expressions := cell_expressions || format(
          $cell$jsonb_build_object('type', 'text', 'value', t.%I)$cell$,
          column_entry->>'name'
        );
      when 'int4' then
        cell_expressions := cell_expressions || format(
          $cell$jsonb_build_object('type', 'integer', 'value', t.%I::text)$cell$,
          column_entry->>'name'
        );
      when 'int8' then
        cell_expressions := cell_expressions || format(
          $cell$jsonb_build_object('type', 'integer', 'value', t.%I::text)$cell$,
          column_entry->>'name'
        );
      else
        raise exception using
          errcode = '55000',
          message = 'HGR-MIGRATION-CATALOG: unsupported primary-key column type';
    end case;
  end loop;
  if cardinality(cell_expressions) = 0 then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-CATALOG: primary-key columns are required';
  end if;
  return format('jsonb_build_array(%s)', array_to_string(cell_expressions, ', '));
end
$function$;

create or replace function xfactory_runtime_v2.migration_live_row_json_expression(
  table_entry jsonb
)
returns text
language plpgsql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  column_entry jsonb;
  member_expressions text[] := array[]::text[];
  column_reference text;
  value_expression text;
begin
  for column_entry in
    select entry.value
    from jsonb_array_elements(table_entry->'columns') entry
    order by (entry.value->>'ordinal')::int
  loop
    column_reference := format('t.%I', column_entry->>'name');
    case column_entry->>'normalized_type'
      when 'timestamptz' then
        value_expression := format(
          $value$case when %1$s is null then 'null'::jsonb
            else to_jsonb(to_char(%1$s at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"')) end$value$,
          column_reference
        );
      when 'bytea' then
        value_expression := format(
          $value$case when %1$s is null then 'null'::jsonb
            else to_jsonb(encode(%1$s, 'hex')) end$value$,
          column_reference
        );
      when 'jsonb' then
        value_expression := format(
          $value$coalesce(%1$s, 'null'::jsonb)$value$,
          column_reference
        );
      else
        value_expression := format(
          $value$case when %1$s is null then 'null'::jsonb
            else to_jsonb(%1$s) end$value$,
          column_reference
        );
    end case;
    member_expressions := member_expressions || format(
      '%L, %s', column_entry->>'name', value_expression
    );
  end loop;
  return format(
    'jsonb_build_object(%s)', array_to_string(member_expressions, ', ')
  );
end
$function$;

create or replace function xfactory_runtime_v2.migration_pk_values_expression(
  table_entry jsonb
)
returns text
language plpgsql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  column_entry jsonb;
  value_expressions text[] := array[]::text[];
begin
  for column_entry in
    select entry.value
    from jsonb_array_elements(table_entry->'columns') entry
    where (entry.value->>'primary_key_position')::int > 0
    order by (entry.value->>'primary_key_position')::int
  loop
    value_expressions := value_expressions || format(
      't.%I::text', column_entry->>'name'
    );
  end loop;
  if cardinality(value_expressions) = 0 then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-CATALOG: primary-key columns are required';
  end if;
  return format('array[%s]', array_to_string(value_expressions, ', '));
end
$function$;

create or replace function xfactory_runtime_v2.migration_source_rows(
  source_schema text,
  table_entry jsonb
)
returns table (
  source_pk text,
  source_row_digest text,
  source_row jsonb,
  pk_values text[]
)
language plpgsql
stable
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
begin
  return query execute format(
    $query$
    select
      xfactory_runtime_v2.migration_canonical_json_value(
        to_jsonb(%s)
      ) as source_pk,
      xfactory_runtime_v2.migration_row_digest(%s) as source_row_digest,
      %s as source_row,
      %s as pk_values
    from %I.%I t
    $query$,
    xfactory_runtime_v2.migration_pk_values_expression(table_entry),
    xfactory_runtime_v2.migration_live_cells_expression(table_entry),
    xfactory_runtime_v2.migration_live_row_json_expression(table_entry),
    xfactory_runtime_v2.migration_pk_values_expression(table_entry),
    source_schema,
    table_entry->>'table_name'
  );
end
$function$;

create or replace function xfactory_runtime_v2.migration_table_frame(
  in source_schema text,
  in table_entry jsonb,
  out table_frame bytea,
  out row_count bigint
)
language plpgsql
stable
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  column_frames bytea;
  column_count bigint;
  row_frames bytea;
begin
  select
    coalesce(
      string_agg(
        xfactory_runtime_v2.migration_frame(
          x'14'::int,
          xfactory_runtime_v2.migration_u64be(
            (entry.value->>'ordinal')::bigint
          )
          || case when (entry.value->>'nullable')::boolean
               then decode('01', 'hex') else decode('00', 'hex') end
          || xfactory_runtime_v2.migration_u64be(
               (entry.value->>'primary_key_position')::bigint
             )
          || xfactory_runtime_v2.migration_frame(
               x'15'::int, convert_to(entry.value->>'name', 'UTF8')
             )
          || xfactory_runtime_v2.migration_frame(
               x'16'::int, convert_to(entry.value->>'normalized_type', 'UTF8')
             )
        ),
        ''::bytea order by (entry.value->>'ordinal')::int
      ),
      ''::bytea
    ),
    count(*)::bigint
  into column_frames, column_count
  from jsonb_array_elements(table_entry->'columns') entry;

  execute format(
    $query$
    select
      coalesce(
        string_agg(framed.row_frame, ''::bytea order by framed.sort_key),
        ''::bytea
      ),
      count(*)::bigint
    from (
      select
        xfactory_runtime_v2.migration_row_frame(%s) as row_frame,
        xfactory_runtime_v2.migration_key_frames(%s) as sort_key
      from %I.%I t
    ) framed
    $query$,
    xfactory_runtime_v2.migration_live_cells_expression(table_entry),
    xfactory_runtime_v2.migration_pk_cells_expression(table_entry),
    source_schema,
    table_entry->>'table_name'
  )
  into row_frames, row_count;

  table_frame := xfactory_runtime_v2.migration_frame(
    x'10'::int,
    xfactory_runtime_v2.migration_frame(
      x'11'::int, convert_to(table_entry->>'schema_name', 'UTF8')
    )
    || xfactory_runtime_v2.migration_frame(
         x'12'::int, convert_to(table_entry->>'table_name', 'UTF8')
       )
    || xfactory_runtime_v2.migration_frame(
         x'13'::int, xfactory_runtime_v2.migration_u64be(column_count)
       )
    || column_frames
    || xfactory_runtime_v2.migration_frame(
         x'17'::int, xfactory_runtime_v2.migration_u64be(row_count)
       )
    || row_frames
  );
end
$function$;

create or replace function xfactory_runtime_v2.migration_dataset_stream(
  source_schema text
)
returns bytea
language plpgsql
stable
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  catalog_json jsonb;
  table_entry jsonb;
  stream bytea := '\x584656314453'::bytea || decode('0001', 'hex');
  framed record;
begin
  catalog_json := xfactory_runtime_v2.migration_source_catalog(source_schema);
  for table_entry in
    select entry.value
    from jsonb_array_elements(catalog_json) entry
    order by convert_to(entry.value->>'schema_name', 'UTF8'),
      convert_to(entry.value->>'table_name', 'UTF8')
  loop
    select frame.table_frame
    into framed
    from xfactory_runtime_v2.migration_table_frame(
      source_schema, table_entry
    ) frame;
    stream := stream || framed.table_frame;
  end loop;
  return stream;
end
$function$;

create or replace function xfactory_runtime_v2.migration_dataset_digest(
  source_schema text
)
returns text
language sql
stable
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select 'sha256:' || encode(
    sha256(xfactory_runtime_v2.migration_dataset_stream(source_schema)), 'hex'
  )
$function$;

create or replace function xfactory_runtime_v2.migration_observe_source(
  source_schema text
)
returns jsonb
language plpgsql
stable
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  catalog_json jsonb;
  table_entry jsonb;
  stream bytea := '\x584656314453'::bytea || decode('0001', 'hex');
  framed record;
  table_row_counts jsonb := '{}'::jsonb;
  per_table_digests jsonb := '{}'::jsonb;
  table_key text;
begin
  catalog_json := xfactory_runtime_v2.migration_source_catalog(source_schema);
  for table_entry in
    select entry.value
    from jsonb_array_elements(catalog_json) entry
    order by convert_to(entry.value->>'schema_name', 'UTF8'),
      convert_to(entry.value->>'table_name', 'UTF8')
  loop
    select frame.table_frame, frame.row_count
    into framed
    from xfactory_runtime_v2.migration_table_frame(
      source_schema, table_entry
    ) frame;
    table_key := (table_entry->>'schema_name') || '.'
      || (table_entry->>'table_name');
    table_row_counts := table_row_counts
      || jsonb_build_object(table_key, framed.row_count);
    per_table_digests := per_table_digests || jsonb_build_object(
      table_key,
      'sha256:' || encode(sha256(framed.table_frame), 'hex')
    );
    stream := stream || framed.table_frame;
  end loop;
  return jsonb_build_object(
    'catalog', catalog_json,
    'catalog_digest', xfactory_runtime_v2.migration_catalog_digest(catalog_json),
    'table_row_counts', table_row_counts,
    'per_table_digests', per_table_digests,
    'dataset_digest', 'sha256:' || encode(sha256(stream), 'hex')
  );
end
$function$;

create or replace function xfactory_runtime_v2.migration_dataset_stream_from(
  dataset jsonb
)
returns bytea
language plpgsql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  table_entry jsonb;
  column_entry jsonb;
  stream bytea := '\x584656314453'::bytea || decode('0001', 'hex');
  column_frames bytea;
  column_count bigint;
  row_frames bytea;
  row_count bigint;
  seen_tables text[] := array[]::text[];
  table_key text;
begin
  if jsonb_typeof(dataset) <> 'object'
     or dataset->>'kind' is distinct from 'xfactory-v1-dataset-description'
     or dataset->'schema_version' is distinct from '1'::jsonb
     or jsonb_typeof(dataset->'tables') <> 'array' then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-DATASET-SHAPE: dataset descriptions must carry '
        'schema_version 1, the dataset-description kind, and a tables list';
  end if;
  for table_entry in
    select entry.value
    from jsonb_array_elements(dataset->'tables') entry
    order by convert_to(entry.value->>'schema_name', 'UTF8'),
      convert_to(entry.value->>'table_name', 'UTF8')
  loop
    if table_entry->>'schema_name' is null
       or table_entry->>'table_name' is null
       or jsonb_typeof(table_entry->'columns') <> 'array'
       or jsonb_typeof(table_entry->'rows') <> 'array' then
      raise exception using
        errcode = '22023',
        message = 'HGR-MIGRATION-DATASET-SHAPE: table entries must carry '
          'schema_name, table_name, columns, and rows';
    end if;
    table_key := (table_entry->>'schema_name') || '.'
      || (table_entry->>'table_name');
    if table_key = any(seen_tables) then
      raise exception using
        errcode = '22023',
        message = 'HGR-MIGRATION-DATASET-SHAPE: duplicate dataset table entry';
    end if;
    seen_tables := seen_tables || table_key;

    if exists (
      select 1
      from jsonb_array_elements(table_entry->'columns') entry
      where jsonb_typeof(entry.value) <> 'object'
        or entry.value->>'name' is null
        or entry.value->>'normalized_type' is null
        or entry.value->>'normalized_type' not in
          ('text', 'int4', 'int8', 'bool', 'timestamptz', 'jsonb', 'bytea')
        or jsonb_typeof(entry.value->'nullable') <> 'boolean'
        or jsonb_typeof(entry.value->'primary_key_position') <> 'number'
    ) then
      raise exception using
        errcode = '22023',
        message = 'HGR-MIGRATION-DATASET-COLUMN: dataset columns must carry '
          'name, normalized_type, nullable, and primary_key_position';
    end if;

    select
      coalesce(
        string_agg(
          xfactory_runtime_v2.migration_frame(
            x'14'::int,
            xfactory_runtime_v2.migration_u64be(entry.ordinality)
            || case when (entry.value->>'nullable')::boolean
                 then decode('01', 'hex') else decode('00', 'hex') end
            || xfactory_runtime_v2.migration_u64be(
                 (entry.value->>'primary_key_position')::bigint
               )
            || xfactory_runtime_v2.migration_frame(
                 x'15'::int, convert_to(entry.value->>'name', 'UTF8')
               )
            || xfactory_runtime_v2.migration_frame(
                 x'16'::int,
                 convert_to(entry.value->>'normalized_type', 'UTF8')
               )
          ),
          ''::bytea order by entry.ordinality
        ),
        ''::bytea
      ),
      count(*)::bigint
    into column_frames, column_count
    from jsonb_array_elements(table_entry->'columns') with ordinality
      entry(value, ordinality);

    select
      coalesce(
        string_agg(framed.row_frame, ''::bytea order by framed.sort_key),
        ''::bytea
      ),
      count(*)::bigint
    into row_frames, row_count
    from (
      select
        xfactory_runtime_v2.migration_row_frame(
          xfactory_runtime_v2.migration_dataset_row_cells(
            table_entry->'columns', row_entry.value
          )
        ) as row_frame,
        xfactory_runtime_v2.migration_key_frames(
          xfactory_runtime_v2.migration_dataset_key_cells(
            table_entry->'columns', row_entry.value
          )
        ) as sort_key
      from jsonb_array_elements(table_entry->'rows') row_entry
    ) framed;

    stream := stream || xfactory_runtime_v2.migration_frame(
      x'10'::int,
      xfactory_runtime_v2.migration_frame(
        x'11'::int, convert_to(table_entry->>'schema_name', 'UTF8')
      )
      || xfactory_runtime_v2.migration_frame(
           x'12'::int, convert_to(table_entry->>'table_name', 'UTF8')
         )
      || xfactory_runtime_v2.migration_frame(
           x'13'::int, xfactory_runtime_v2.migration_u64be(column_count)
         )
      || column_frames
      || xfactory_runtime_v2.migration_frame(
           x'17'::int, xfactory_runtime_v2.migration_u64be(row_count)
         )
      || row_frames
    );
  end loop;
  return stream;
end
$function$;

create or replace function xfactory_runtime_v2.migration_dataset_row_cells(
  columns jsonb,
  row_cells jsonb
)
returns jsonb
language plpgsql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  column_count int;
  cell_count int;
  position int;
  column_entry jsonb;
  cell jsonb;
  expected_kind text;
  cell_kind text;
begin
  if jsonb_typeof(row_cells) <> 'array' then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-DATASET-ROW: rows must be cell arrays';
  end if;
  column_count := jsonb_array_length(columns);
  cell_count := jsonb_array_length(row_cells);
  if cell_count <> column_count then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-DATASET-ROW: rows must carry exactly one cell '
        'per schema-ordinal column';
  end if;
  for position in 1..column_count loop
    column_entry := columns->(position - 1);
    cell := row_cells->(position - 1);
    if jsonb_typeof(cell->'type') = 'null' or cell #>> '{type}' = 'null' then
      if not (column_entry->>'nullable')::boolean then
        raise exception using
          errcode = '22023',
          message = 'HGR-MIGRATION-DATASET-VALUE: null cell in a non-nullable '
            'column';
      end if;
      continue;
    end if;
    expected_kind := case column_entry->>'normalized_type'
      when 'text' then 'text'
      when 'int4' then 'integer'
      when 'int8' then 'integer'
      when 'bool' then 'boolean'
      when 'timestamptz' then 'timestamp'
      when 'jsonb' then 'json'
      when 'bytea' then 'binary'
    end;
    cell_kind := cell #>> '{type}';
    if cell_kind is distinct from expected_kind then
      raise exception using
        errcode = '22023',
        message = 'HGR-MIGRATION-DATASET-VALUE: cell type does not match the '
          'column normalized type';
    end if;
    if cell_kind = 'integer' then
      if column_entry->>'normalized_type' = 'int4'
         and ((cell #>> '{value}')::numeric > 2147483647
           or (cell #>> '{value}')::numeric < -2147483648) then
        raise exception using
          errcode = '22023',
          message = 'HGR-MIGRATION-DATASET-VALUE: integer value out of range';
      end if;
      if (cell #>> '{value}')::numeric > 9223372036854775807
         or (cell #>> '{value}')::numeric < -9223372036854775808 then
        raise exception using
          errcode = '22023',
          message = 'HGR-MIGRATION-DATASET-VALUE: integer value out of range';
      end if;
    end if;
  end loop;
  return row_cells;
end
$function$;

create or replace function xfactory_runtime_v2.migration_dataset_key_cells(
  columns jsonb,
  row_cells jsonb
)
returns jsonb
language plpgsql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  key_cells jsonb;
begin
  select coalesce(
    jsonb_agg(
      row_cells->((column_entry.ordinality - 1)::int)
      order by (column_entry.value->>'primary_key_position')::int
    ),
    '[]'::jsonb
  )
  into key_cells
  from jsonb_array_elements(columns) with ordinality
    column_entry(value, ordinality)
  where (column_entry.value->>'primary_key_position')::int > 0;
  if key_cells = '[]'::jsonb then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-DATASET-ROW: primary-key cells are required';
  end if;
  if exists (
    select 1
    from jsonb_array_elements(key_cells) cell
    where jsonb_typeof(cell.value->'type') = 'null'
      or cell.value #>> '{type}' = 'null'
  ) then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-DATASET-ROW: primary-key cells must not be null';
  end if;
  return key_cells;
end
$function$;

create or replace function xfactory_runtime_v2.migration_logical_boundary(
  source_identity jsonb,
  observation jsonb
)
returns text
language plpgsql
immutable
strict
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
begin
  if jsonb_typeof(source_identity) <> 'object'
     or source_identity->>'source_database' is null
     or source_identity->>'source_schema' is null
     or (select count(*) from jsonb_object_keys(source_identity)) <> 2 then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-BOUNDARY-SHAPE: source identity must carry '
        'exactly source_database and source_schema';
  end if;
  if observation->>'catalog_digest' is null
     or jsonb_typeof(observation->'table_row_counts') <> 'object'
     or observation->>'dataset_digest' is null then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-BOUNDARY-SHAPE: observations must carry '
        'catalog_digest, table_row_counts, and dataset_digest';
  end if;
  return xfactory_runtime_v2.canonical_record_digest(
    jsonb_build_object(
      'profile', 'xfactory-v1-logical-boundary-v1',
      'source_identity', source_identity,
      'catalog_digest', observation->>'catalog_digest',
      'table_row_counts', observation->'table_row_counts',
      'dataset_digest', observation->>'dataset_digest'
    )
  );
end
$function$;

create or replace function xfactory_runtime_v2.migration_session_lock_key(
  requested_installation_id text,
  requested_migration_id text
)
returns bigint
language sql
immutable
strict
set search_path = pg_catalog
as $function$
  select hashtextextended(
    'xfactory-v1-to-v2-migration:' || requested_installation_id || E'\n'
      || requested_migration_id,
    0
  )
$function$;

create or replace function xfactory_runtime_v2.migration_assert_session_lock(
  requested_installation_id text,
  requested_migration_id text
)
returns void
language plpgsql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  lock_key bigint := xfactory_runtime_v2.migration_session_lock_key(
    requested_installation_id, requested_migration_id
  );
begin
  if not exists (
    select 1
    from pg_locks held
    where held.locktype = 'advisory'
      and held.pid = pg_backend_pid()
      and held.granted
      and held.classid::bigint = ((lock_key >> 32) & 4294967295)
      and held.objid::bigint = (lock_key & 4294967295)
      and held.objsubid = 1
  ) then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-LOCK-NOT-HELD: the migration session advisory '
        'lock on installation plus migration id must be held';
  end if;
end
$function$;

create or replace function xfactory_runtime_v2.migration_latest_event(
  requested_installation_id text,
  requested_migration_id text
)
returns xfactory_runtime_v2.migration_attempt_events
language sql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select tip.*
  from xfactory_runtime_v2.migration_attempt_events tip
  where tip.installation_id = requested_installation_id
    and tip.migration_id = requested_migration_id
    and not exists (
      select 1
      from xfactory_runtime_v2.migration_attempt_events successor
      where successor.installation_id = tip.installation_id
        and successor.migration_id = tip.migration_id
        and successor.predecessor_event_id = tip.event_id
    )
$function$;

create or replace function xfactory_runtime_v2.migration_verify_authority(
  requested_installation_id text,
  requested_migration_id text,
  authority_envelope jsonb,
  payload_digest text
)
returns void
language plpgsql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  grant_record xfactory_runtime_v2.authority_grants%rowtype;
  chain_record record;
begin
  select grant_row.*
  into grant_record
  from xfactory_runtime_v2.authority_grants grant_row
  where grant_row.installation_id = requested_installation_id
    and grant_row.grant_id = authority_envelope->>'run_migration_grant_id';
  if not found
     or grant_record.record_digest is distinct from
       authority_envelope->>'run_migration_grant_digest'
     or grant_record.action <> 'run_migration'
     or grant_record.resource_type <> 'migration_mapping'
     or grant_record.resource_id <> requested_migration_id
     or grant_record.resource_digest is distinct from payload_digest then
    raise exception using
      errcode = '42501',
      message = 'HGR-MIGRATION-AUTHORITY: the authority envelope must cite an '
        'exact run_migration grant over resource type migration_mapping, this '
        'migration id, and this mapping payload digest';
  end if;
  select chain.*
  into chain_record
  from xfactory_runtime_v2.active_authority_chain(
    requested_installation_id,
    authority_envelope->>'run_migration_grant_id',
    'run_migration',
    'installation',
    '',
    '',
    authority_envelope->>'approver_principal_id',
    transaction_timestamp()
  ) chain;
  if not found then
    raise exception using
      errcode = '42501',
      message = 'HGR-MIGRATION-AUTHORITY: no active run_migration authority '
        'chain reaches an active trust anchor for the approver principal';
  end if;
  if chain_record.root_anchor_id is distinct from
       authority_envelope->>'trust_anchor_id'
     or chain_record.root_anchor_digest is distinct from
       authority_envelope->>'trust_anchor_digest' then
    raise exception using
      errcode = '42501',
      message = 'HGR-MIGRATION-AUTHORITY: the authority envelope trust anchor '
        'does not match the active trust-anchor chain';
  end if;
end
$function$;

create or replace function xfactory_runtime_v2.reject_frozen_v1_write()
returns trigger
language plpgsql
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
begin
  raise exception using
    errcode = '55000',
    message = format(
      'HGR-MIGRATION-V1-FROZEN: %I.%I is frozen by migration %s; governed '
      'writes require a later governed dual-write contract',
      tg_table_schema, tg_table_name, coalesce(tg_argv[0], 'unknown')
    );
end
$function$;

create or replace function xfactory_runtime_v2.install_v1_freeze(
  requested_migration_id text
)
returns jsonb
language plpgsql
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  table_name text;
  relation_oid oid;
  frozen_tables jsonb := '[]'::jsonb;
  freeze_record jsonb;
  message_level text := current_setting('client_min_messages');
  freeze_time text := to_char(
    transaction_timestamp() at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
  );
begin
  foreach table_name in array
    xfactory_runtime_v2.migration_canonical_v1_tables()
  loop
    relation_oid := to_regclass(format('%I.%I', 'public', table_name));
    if relation_oid is null then
      raise exception using
        errcode = '55000',
        message = format(
          'HGR-MIGRATION-V1-FROZEN: canonical v1 table public.%I is missing',
          table_name
        );
    end if;
    if not exists (
      select 1
      from pg_trigger existing
      where existing.tgrelid = relation_oid
        and existing.tgname = 'hermes_v1_freeze_write'
        and not existing.tgisinternal
    ) then
      execute format(
        'create trigger hermes_v1_freeze_write '
        'before insert or update or delete or truncate on public.%I '
        'for each statement execute function '
        'xfactory_runtime_v2.reject_frozen_v1_write(%L)',
        table_name,
        requested_migration_id
      );
    end if;
    -- the durable enforcement is the trigger; the accompanying write revoke
    -- is best-effort acl hygiene and stays silent when there is nothing the
    -- executing role can revoke (postgres warns per irrevocable privilege).
    perform set_config('client_min_messages', 'error', true);
    execute format(
      'revoke insert, update, delete, truncate on public.%I from public',
      table_name
    );
    perform set_config('client_min_messages', message_level, true);
    frozen_tables := frozen_tables || to_jsonb(table_name);
  end loop;
  freeze_record := jsonb_build_object(
    'schema_version', 1,
    'kind', 'openxfactory-hermes-runtime-v1-write-freeze',
    'migration_id', requested_migration_id,
    'source_schema', 'public',
    'trigger_name', 'hermes_v1_freeze_write',
    'frozen_tables', frozen_tables,
    'frozen_at', freeze_time
  );
  return freeze_record || jsonb_build_object(
    'freeze_digest',
    xfactory_runtime_v2.canonical_record_digest(freeze_record)
  );
end
$function$;

create or replace function xfactory_runtime_v2.migration_result_document(
  requested_installation_id text,
  requested_migration_id text
)
returns jsonb
language plpgsql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  staging_record xfactory_runtime_v2.migration_staging%rowtype;
  tip xfactory_runtime_v2.migration_attempt_events;
  result_document jsonb;
begin
  select staging.*
  into staging_record
  from xfactory_runtime_v2.migration_staging staging
  where staging.installation_id = requested_installation_id
    and staging.migration_id = requested_migration_id;
  tip := xfactory_runtime_v2.migration_latest_event(
    requested_installation_id, requested_migration_id
  );
  result_document := jsonb_build_object(
    'schema_version', 1,
    'kind', 'openxfactory-hermes-runtime-migration-result',
    'installation_id', requested_installation_id,
    'migration_id', requested_migration_id,
    'staged', staging_record.installation_id is not null,
    'status', coalesce(tip.event_type, 'unstarted'),
    'terminal', coalesce(tip.event_type, '') = 'succeeded',
    'attempt_id', tip.attempt_id,
    'mapping_payload_digest', staging_record.mapping_payload_digest,
    'authority_envelope_digest', staging_record.authority_envelope_digest
  );
  if coalesce(tip.event_type, '') = 'succeeded' then
    result_document := result_document || (
      select jsonb_build_object(
        'logical_boundary_id', observation.logical_boundary_id,
        'observation', jsonb_build_object(
          'observation_id', observation.observation_id,
          'transaction_snapshot', observation.transaction_snapshot,
          'wal_position', observation.wal_position,
          'authorized_at', to_char(
            observation.authorized_at at time zone 'UTC',
            'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
          ),
          'run_migration_grant_id', observation.run_migration_grant_id,
          'run_migration_grant_digest', observation.run_migration_grant_digest,
          'target_contract_identity', observation.target_contract_identity
        ),
        'reconciliation', jsonb_build_object(
          'reconciliation_id', reconciliation.reconciliation_id,
          'per_table', reconciliation.per_table,
          'compatibility_history_count',
            reconciliation.compatibility_history_count,
          'quarantine_count', reconciliation.quarantine_count,
          'freeze', reconciliation."freeze",
          'reconciliation_digest', reconciliation.reconciliation_digest
        )
      )
      from xfactory_runtime_v2.migration_cutover_observations observation
      join xfactory_runtime_v2.migration_reconciliations reconciliation
        on reconciliation.attempt_id = observation.attempt_id
      where observation.attempt_id = tip.attempt_id
    );
  end if;
  return result_document;
end
$function$;

create or replace function xfactory_runtime_api_v2.stage_migration(
  staging jsonb
)
returns jsonb
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  payload jsonb;
  authority_envelope jsonb;
  requested_installation_id text;
  requested_migration_id text;
  payload_digest text;
  envelope_digest text;
  existing_record xfactory_runtime_v2.migration_staging%rowtype;
  staging_time timestamptz := transaction_timestamp();
begin
  if jsonb_typeof(staging) <> 'object'
     or staging->'schema_version' is distinct from '1'::jsonb
     or staging->>'kind' is distinct from
       'openxfactory-hermes-runtime-migration-staging'
     or jsonb_typeof(staging->'payload') <> 'object'
     or jsonb_typeof(staging->'authority_envelope') <> 'object'
     or (select count(*) from jsonb_object_keys(staging)) <> 4 then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-STAGING-SHAPE: staging documents must carry '
        'exactly schema_version 1, the staging kind, payload, and '
        'authority_envelope';
  end if;
  payload := staging->'payload';
  authority_envelope := staging->'authority_envelope';
  perform xfactory_runtime_v2.migration_reject_control_characters(payload);
  perform xfactory_runtime_v2.migration_reject_control_characters(
    authority_envelope
  );

  if not (payload ?& array[
       'schema_version', 'kind', 'migration_id', 'installation_id',
       'source_identity', 'source_catalog', 'expected_table_row_counts',
       'expected_dataset_digest', 'digest_profile', 'subject_mappings',
       'admin_mappings', 'single_default_mapping', 'target_topology',
       'migration_policy', 'mapping_payload_digest'
     ])
     or (select count(*) from jsonb_object_keys(payload)) <> 15
     or payload->'schema_version' is distinct from '1'::jsonb
     or payload->>'kind' is distinct from
       'openxfactory-hermes-runtime-migration-mapping-payload'
     or payload->>'digest_profile' is distinct from
       'xfactory-v1-dataset-binary-v1'
     or coalesce(payload->>'migration_id', '') = ''
     or coalesce(payload->>'installation_id', '') = ''
     or jsonb_typeof(payload->'source_identity') <> 'object'
     or payload #>> '{source_identity,source_database}' is null
     or payload #>> '{source_identity,source_schema}' is null then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-STAGING-SHAPE: the mapping payload must be the '
        'closed schema_version 1 detached payload with the pinned digest '
        'profile';
  end if;
  if not (authority_envelope ?& array[
       'schema_version', 'kind', 'migration_id', 'installation_id',
       'mapping_payload_digest', 'approver_principal_id',
       'run_migration_grant_id', 'run_migration_grant_digest', 'policy_ref',
       'policy_digest', 'scope', 'trust_anchor_id', 'trust_anchor_digest',
       'approved_at', 'authority_envelope_digest'
     ])
     or (select count(*) from jsonb_object_keys(authority_envelope)) <> 15
     or authority_envelope->'schema_version' is distinct from '1'::jsonb
     or authority_envelope->>'kind' is distinct from
       'openxfactory-hermes-runtime-migration-authority-envelope'
     or jsonb_typeof(authority_envelope->'scope') <> 'object'
     or (
       select count(*) from jsonb_object_keys(authority_envelope->'scope')
     ) <> 1 then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-STAGING-SHAPE: the authority envelope must be '
        'the closed schema_version 1 detached envelope';
  end if;

  requested_installation_id := payload->>'installation_id';
  requested_migration_id := payload->>'migration_id';
  if authority_envelope->>'installation_id' is distinct from
       requested_installation_id
     or authority_envelope->>'migration_id' is distinct from
       requested_migration_id
     or authority_envelope #>> '{scope,installation_id}' is distinct from
       requested_installation_id then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-STAGING-SHAPE: the authority envelope must bind '
        'the exact payload installation and migration identity';
  end if;

  payload_digest := xfactory_runtime_v2.canonical_record_digest(
    payload - 'mapping_payload_digest'
  );
  if payload->>'mapping_payload_digest' is distinct from payload_digest then
    raise exception using
      errcode = '22023',
      message = format(
        'HGR-MIGRATION-STAGING-DIGEST: the declared mapping payload digest '
        'does not match the database-recomputed digest %s',
        payload_digest
      );
  end if;
  if authority_envelope->>'mapping_payload_digest' is distinct from
       payload_digest then
    raise exception using
      errcode = '22023',
      message = 'HGR-MIGRATION-STAGING-DIGEST: the authority envelope does not '
        'bind the database-recomputed mapping payload digest';
  end if;
  envelope_digest := xfactory_runtime_v2.canonical_record_digest(
    authority_envelope - 'authority_envelope_digest'
  );
  if authority_envelope->>'authority_envelope_digest' is distinct from
       envelope_digest then
    raise exception using
      errcode = '22023',
      message = format(
        'HGR-MIGRATION-STAGING-DIGEST: the declared authority envelope digest '
        'does not match the database-recomputed digest %s',
        envelope_digest
      );
  end if;

  perform xfactory_runtime_v2.migration_verify_authority(
    requested_installation_id,
    requested_migration_id,
    authority_envelope,
    payload_digest
  );

  select existing.*
  into existing_record
  from xfactory_runtime_v2.migration_staging existing
  where existing.installation_id = requested_installation_id
    and existing.migration_id = requested_migration_id
  for share;
  if found then
    if existing_record.mapping_payload_digest = payload_digest
       and existing_record.authority_envelope_digest = envelope_digest then
      return jsonb_build_object(
        'installation_id', requested_installation_id,
        'migration_id', requested_migration_id,
        'mapping_payload_digest', payload_digest,
        'authority_envelope_digest', envelope_digest,
        'restaged', true
      );
    end if;
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-STAGING-CONFLICT: a different mapping payload '
        'or authority envelope is already staged for this migration id';
  end if;

  insert into xfactory_runtime_v2.migration_staging (
    installation_id, migration_id, payload, authority_envelope,
    mapping_payload_digest, authority_envelope_digest, staged_at
  ) values (
    requested_installation_id, requested_migration_id, payload,
    authority_envelope, payload_digest, envelope_digest, staging_time
  );
  return jsonb_build_object(
    'installation_id', requested_installation_id,
    'migration_id', requested_migration_id,
    'mapping_payload_digest', payload_digest,
    'authority_envelope_digest', envelope_digest,
    'restaged', false
  );
end
$function$;

create or replace function xfactory_runtime_api_v2.begin_migration_attempt(
  requested_installation_id text,
  requested_migration_id text
)
returns jsonb
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  staging_record xfactory_runtime_v2.migration_staging%rowtype;
  tip xfactory_runtime_v2.migration_attempt_events;
  attempt_number bigint;
  new_attempt_id text;
  predecessor_id text;
  event_time timestamptz := transaction_timestamp();
begin
  perform xfactory_runtime_v2.migration_assert_session_lock(
    requested_installation_id, requested_migration_id
  );
  select staging.*
  into staging_record
  from xfactory_runtime_v2.migration_staging staging
  where staging.installation_id = requested_installation_id
    and staging.migration_id = requested_migration_id
  for share;
  if not found then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-NOT-STAGED: a validated canonical staging '
        'document is required before an attempt may begin';
  end if;

  tip := xfactory_runtime_v2.migration_latest_event(
    requested_installation_id, requested_migration_id
  );
  if tip.event_type = 'succeeded' then
    return xfactory_runtime_v2.migration_result_document(
      requested_installation_id, requested_migration_id
    );
  end if;
  predecessor_id := tip.event_id;
  if tip.event_type = 'started' then
    insert into xfactory_runtime_v2.migration_attempt_events (
      event_id, attempt_id, installation_id, migration_id, event_type,
      predecessor_event_id, reason, occurred_at
    ) values (
      tip.attempt_id || ':abandoned', tip.attempt_id,
      requested_installation_id, requested_migration_id, 'abandoned',
      tip.event_id,
      'prior attempt abandoned after interruption or crash recovery',
      event_time
    );
    predecessor_id := tip.attempt_id || ':abandoned';
  end if;

  select count(*) + 1
  into attempt_number
  from xfactory_runtime_v2.migration_attempts attempts
  where attempts.installation_id = requested_installation_id
    and attempts.migration_id = requested_migration_id;
  new_attempt_id := requested_migration_id || '-attempt-'
    || attempt_number::text;
  insert into xfactory_runtime_v2.migration_attempts (
    attempt_id, installation_id, migration_id, mapping_payload_digest,
    created_at
  ) values (
    new_attempt_id, requested_installation_id, requested_migration_id,
    staging_record.mapping_payload_digest, event_time
  );
  insert into xfactory_runtime_v2.migration_attempt_events (
    event_id, attempt_id, installation_id, migration_id, event_type,
    predecessor_event_id, reason, occurred_at
  ) values (
    new_attempt_id || ':started', new_attempt_id, requested_installation_id,
    requested_migration_id, 'started', predecessor_id, null, event_time
  );
  return jsonb_build_object(
    'status', 'started',
    'terminal', false,
    'installation_id', requested_installation_id,
    'migration_id', requested_migration_id,
    'attempt_id', new_attempt_id,
    'mapping_payload_digest', staging_record.mapping_payload_digest
  );
end
$function$;

create or replace function xfactory_runtime_api_v2.execute_v1_cutover(
  requested_installation_id text,
  requested_migration_id text,
  requested_attempt_id text
)
returns jsonb
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  staging_record xfactory_runtime_v2.migration_staging%rowtype;
  attempt_record xfactory_runtime_v2.migration_attempts%rowtype;
  tip xfactory_runtime_v2.migration_attempt_events;
  payload jsonb;
  source_schema text;
  missing_locks text[];
  observation jsonb;
  observed_boundary text;
  approved_boundary text;
  reconciliation jsonb;
  freeze_record jsonb;
  reconciliation_payload jsonb;
  reconciliation_digest text;
  compatibility_count bigint;
  quarantine_count bigint;
  cutover_time timestamptz := transaction_timestamp();
begin
  perform xfactory_runtime_v2.migration_assert_session_lock(
    requested_installation_id, requested_migration_id
  );
  if current_setting('transaction_isolation') <> 'serializable' then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-NOT-SERIALIZABLE: the authoritative cutover '
        'transaction must run at serializable isolation';
  end if;

  select staging.*
  into staging_record
  from xfactory_runtime_v2.migration_staging staging
  where staging.installation_id = requested_installation_id
    and staging.migration_id = requested_migration_id
  for share;
  if not found then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-NOT-STAGED: no validated staging document '
        'exists for this migration id';
  end if;
  select attempts.*
  into attempt_record
  from xfactory_runtime_v2.migration_attempts attempts
  where attempts.installation_id = requested_installation_id
    and attempts.migration_id = requested_migration_id
    and attempts.attempt_id = requested_attempt_id;
  if not found
     or attempt_record.mapping_payload_digest is distinct from
       staging_record.mapping_payload_digest then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-ATTEMPT-STATE: the cutover attempt must exist '
        'and bind the staged mapping payload digest';
  end if;
  tip := xfactory_runtime_v2.migration_latest_event(
    requested_installation_id, requested_migration_id
  );
  if tip.event_type is distinct from 'started'
     or tip.attempt_id is distinct from requested_attempt_id then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-ATTEMPT-STATE: cutover requires this attempt '
        'to hold the open started event';
  end if;

  payload := staging_record.payload;
  perform xfactory_runtime_v2.migration_verify_authority(
    requested_installation_id,
    requested_migration_id,
    staging_record.authority_envelope,
    staging_record.mapping_payload_digest
  );

  source_schema := payload #>> '{source_identity,source_schema}';
  if payload #>> '{source_identity,source_database}' is distinct from
       current_database() then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-SOURCE-IDENTITY: the approved source_database '
        'does not match the connected database';
  end if;
  if source_schema is distinct from 'public' then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-SOURCE-IDENTITY: the pinned v1 contract lives '
        'in schema public';
  end if;

  -- the twelve v1 table locks must already be held by this session, taken as
  -- top-level lock statements before the serializable snapshot was
  -- established. a lock acquired here would follow the snapshot (taken at the
  -- first statement of this transaction), so a v1 write committing while the
  -- lock waited would be committed in the table yet invisible to the observed
  -- boundary and stranded by the freeze.
  select array_agg(required.table_name order by required.table_name)
  into missing_locks
  from unnest(xfactory_runtime_v2.migration_canonical_v1_tables())
    as required(table_name)
  where not exists (
    select 1
    from pg_locks held
    where held.locktype = 'relation'
      and held.pid = pg_backend_pid()
      and held.granted
      and held.relation = to_regclass(
        format('%I.%I', source_schema, required.table_name)
      )
      and held.mode in (
        'ShareRowExclusiveLock', 'ExclusiveLock', 'AccessExclusiveLock'
      )
  );
  if missing_locks is not null then
    raise exception using
      errcode = '55000',
      message = format(
        'HGR-MIGRATION-V1-LOCKS-NOT-PREHELD: the cutover session must hold '
        'share row exclusive locks on every canonical v1 table before the '
        'serializable snapshot is taken; missing: %s',
        array_to_string(missing_locks, ', ')
      );
  end if;

  observation := xfactory_runtime_v2.migration_observe_source(source_schema);
  observed_boundary := xfactory_runtime_v2.migration_logical_boundary(
    payload->'source_identity', observation
  );
  approved_boundary := xfactory_runtime_v2.migration_logical_boundary(
    payload->'source_identity',
    jsonb_build_object(
      'catalog_digest',
      xfactory_runtime_v2.migration_catalog_digest(payload->'source_catalog'),
      'table_row_counts', payload->'expected_table_row_counts',
      'dataset_digest', payload->>'expected_dataset_digest'
    )
  );
  if observed_boundary is distinct from approved_boundary then
    raise exception using
      errcode = '55000',
      message = format(
        'HGR-MIGRATION-BOUNDARY-MISMATCH: observed logical source boundary %s '
        'does not equal the approved boundary %s',
        observed_boundary, approved_boundary
      );
  end if;

  reconciliation := xfactory_runtime_v2.migration_run_source_transforms(
    requested_installation_id, requested_migration_id, payload, observation
  );
  compatibility_count := (reconciliation->>'compatibility_history_count')::bigint;
  quarantine_count := (reconciliation->>'quarantine_count')::bigint;

  freeze_record := xfactory_runtime_v2.migration_attach_v1_freeze(
    requested_migration_id
  );

  reconciliation_payload := jsonb_build_object(
    'schema_version', 1,
    'kind', 'openxfactory-hermes-runtime-migration-reconciliation',
    'installation_id', requested_installation_id,
    'migration_id', requested_migration_id,
    'attempt_id', requested_attempt_id,
    'logical_boundary_id', observed_boundary,
    'per_table', reconciliation->'per_table',
    'compatibility_history_count', compatibility_count,
    'quarantine_count', quarantine_count,
    'freeze', freeze_record
  );
  reconciliation_digest := xfactory_runtime_v2.canonical_record_digest(
    reconciliation_payload
  );
  insert into xfactory_runtime_v2.migration_reconciliations (
    reconciliation_id, attempt_id, per_table, compatibility_history_count,
    quarantine_count, "freeze", reconciliation_digest
  ) values (
    requested_attempt_id || ':reconciliation', requested_attempt_id,
    reconciliation->'per_table', compatibility_count, quarantine_count,
    freeze_record, reconciliation_digest
  );
  insert into xfactory_runtime_v2.migration_cutover_observations (
    observation_id, attempt_id, mapping_payload_digest,
    authority_envelope_digest, logical_boundary_id, transaction_snapshot,
    wal_position, authorized_at, run_migration_grant_id,
    run_migration_grant_digest, target_contract_identity,
    reconciliation_digest
  ) values (
    requested_attempt_id || ':observation', requested_attempt_id,
    staging_record.mapping_payload_digest,
    staging_record.authority_envelope_digest, observed_boundary,
    pg_current_snapshot()::text, pg_current_wal_lsn()::text, cutover_time,
    staging_record.authority_envelope->>'run_migration_grant_id',
    staging_record.authority_envelope->>'run_migration_grant_digest',
    jsonb_build_object(
      'contract', 'hermes-operational-postgres-v2',
      'schema_version', 1,
      'target_topology', payload->'target_topology'
    ),
    reconciliation_digest
  );
  insert into xfactory_runtime_v2.migration_attempt_events (
    event_id, attempt_id, installation_id, migration_id, event_type,
    predecessor_event_id, reason, occurred_at
  ) values (
    requested_attempt_id || ':succeeded', requested_attempt_id,
    requested_installation_id, requested_migration_id, 'succeeded',
    tip.event_id, null, cutover_time
  );
  return jsonb_build_object(
    'status', 'succeeded',
    'terminal', true,
    'installation_id', requested_installation_id,
    'migration_id', requested_migration_id,
    'attempt_id', requested_attempt_id,
    'logical_boundary_id', observed_boundary,
    'per_table', reconciliation->'per_table',
    'compatibility_history_count', compatibility_count,
    'quarantine_count', quarantine_count,
    'freeze', freeze_record,
    'reconciliation_digest', reconciliation_digest
  );
end
$function$;

create or replace function xfactory_runtime_api_v2.fail_migration_attempt(
  requested_installation_id text,
  requested_migration_id text,
  requested_attempt_id text,
  reason text
)
returns void
language plpgsql
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
declare
  tip xfactory_runtime_v2.migration_attempt_events;
begin
  perform xfactory_runtime_v2.migration_assert_session_lock(
    requested_installation_id, requested_migration_id
  );
  tip := xfactory_runtime_v2.migration_latest_event(
    requested_installation_id, requested_migration_id
  );
  if tip.event_type is distinct from 'started'
     or tip.attempt_id is distinct from requested_attempt_id then
    raise exception using
      errcode = '55000',
      message = 'HGR-MIGRATION-ATTEMPT-STATE: only the open started attempt '
        'may append its failure event';
  end if;
  insert into xfactory_runtime_v2.migration_attempt_events (
    event_id, attempt_id, installation_id, migration_id, event_type,
    predecessor_event_id, reason, occurred_at
  ) values (
    requested_attempt_id || ':failed', requested_attempt_id,
    requested_installation_id, requested_migration_id, 'failed', tip.event_id,
    coalesce(nullif(reason, ''), 'migration attempt failed'),
    transaction_timestamp()
  );
end
$function$;

create or replace function xfactory_runtime_api_v2.migration_result(
  requested_installation_id text,
  requested_migration_id text
)
returns jsonb
language sql
stable
security definer
set search_path = pg_catalog, xfactory_runtime_v2
as $function$
  select xfactory_runtime_v2.migration_result_document(
    requested_installation_id, requested_migration_id
  )
$function$;

do $migration_immutable_triggers$
declare
  relation_name text;
  trigger_name text;
begin
  foreach relation_name in array array[
    'migration_staging',
    'migration_attempts',
    'migration_attempt_events',
    'migration_cutover_observations',
    'migration_reconciliations',
    'legacy_jobs',
    'legacy_job_runs',
    'legacy_job_events',
    'legacy_workers',
    'legacy_groups',
    'legacy_profiles',
    'legacy_group_memberships',
    'legacy_github_team_mappings'
  ]
  loop
    trigger_name := relation_name || '_immutable';
    if not exists (
      select 1
      from pg_trigger
      where tgrelid = format('xfactory_runtime_v2.%I', relation_name)::regclass
        and tgname = trigger_name
        and not tgisinternal
    ) then
      execute format(
        'create trigger %I before update or delete on xfactory_runtime_v2.%I '
        'for each row execute function xfactory_runtime_v2.reject_immutable_mutation()',
        trigger_name,
        relation_name
      );
    end if;
  end loop;
  if not exists (
    select 1
    from pg_trigger
    where tgrelid =
        'xfactory_legacy_quarantine_v2.legacy_quarantine_records'::regclass
      and tgname = 'legacy_quarantine_records_immutable'
      and not tgisinternal
  ) then
    create trigger legacy_quarantine_records_immutable
    before update or delete
      on xfactory_legacy_quarantine_v2.legacy_quarantine_records
    for each row execute function
      xfactory_runtime_v2.reject_immutable_mutation();
  end if;
end
$migration_immutable_triggers$;

do $migration_row_security$
declare
  relation_name text;
  policy_name text;
begin
  foreach relation_name in array array[
    'legacy_jobs',
    'legacy_job_runs',
    'legacy_job_events',
    'legacy_workers',
    'legacy_groups',
    'legacy_profiles',
    'legacy_group_memberships',
    'legacy_github_team_mappings'
  ]
  loop
    execute format(
      'alter table xfactory_runtime_v2.%I enable row level security',
      relation_name
    );
    execute format(
      'alter table xfactory_runtime_v2.%I force row level security',
      relation_name
    );
    policy_name := relation_name || '_exact_scope';
    execute format(
      'drop policy if exists %I on xfactory_runtime_v2.%I',
      policy_name,
      relation_name
    );
    execute format(
      'create policy %I on xfactory_runtime_v2.%I '
      'using (current_user = %L or '
      'xfactory_runtime_api_v2.current_scope_matches('
      'installation_id, stack_id, layer_id)) '
      'with check (current_user = %L or '
      'xfactory_runtime_api_v2.current_scope_matches('
      'installation_id, stack_id, layer_id))',
      policy_name,
      relation_name,
      'xfactory_v2_owner',
      'xfactory_v2_owner'
    );
  end loop;
end
$migration_row_security$;

create or replace function xfactory_runtime_v2.reject_quarantine_dependency()
returns event_trigger
language plpgsql
set search_path = pg_catalog
as $function$
declare
  quarantine_namespace oid;
  offending record;
begin
  select ns.oid into quarantine_namespace
  from pg_namespace ns
  where ns.nspname = 'xfactory_legacy_quarantine_v2';
  if quarantine_namespace is null then
    return;
  end if;
  select
    dep.classid,
    dep.objid,
    dep.objsubid
  into offending
  from pg_depend dep
  where dep.deptype in ('n', 'a')
    and (
      (
        dep.refclassid = 'pg_class'::regclass
        and dep.refobjid in (
          select cls.oid from pg_class cls
          where cls.relnamespace = quarantine_namespace
        )
      )
      or (
        dep.refclassid = 'pg_type'::regclass
        and dep.refobjid in (
          select typ.oid from pg_type typ
          where typ.typnamespace = quarantine_namespace
        )
      )
    )
    and coalesce(
      case dep.classid
        when 'pg_class'::regclass then (
          select cls.relnamespace from pg_class cls where cls.oid = dep.objid
        )
        when 'pg_constraint'::regclass then (
          select coalesce(rel.relnamespace, con.connamespace)
          from pg_constraint con
          left join pg_class rel on rel.oid = con.conrelid
          where con.oid = dep.objid
        )
        when 'pg_proc'::regclass then (
          select proc.pronamespace from pg_proc proc
          where proc.oid = dep.objid
        )
        when 'pg_rewrite'::regclass then (
          select rel.relnamespace
          from pg_rewrite rewrite
          join pg_class rel on rel.oid = rewrite.ev_class
          where rewrite.oid = dep.objid
        )
        when 'pg_trigger'::regclass then (
          select rel.relnamespace
          from pg_trigger trig
          join pg_class rel on rel.oid = trig.tgrelid
          where trig.oid = dep.objid
        )
        when 'pg_attrdef'::regclass then (
          select rel.relnamespace
          from pg_attrdef attrdef
          join pg_class rel on rel.oid = attrdef.adrelid
          where attrdef.oid = dep.objid
        )
        else null
      end,
      0
    ) <> quarantine_namespace
  limit 1;
  if found then
    raise exception using
      errcode = '55000',
      message = format(
        'HGR-QUARANTINE-DEPENDENCY: %s may not depend on the sealed legacy '
        'quarantine schema; later governed evidence must be created anew '
        'under current authority',
        pg_describe_object(offending.classid, offending.objid,
          offending.objsubid)
      );
  end if;
end
$function$;

revoke all on all tables in schema xfactory_runtime_v2 from public;
revoke all on all functions in schema xfactory_runtime_v2 from public;
revoke all on all functions in schema xfactory_runtime_api_v2 from public;
revoke all on all tables in schema xfactory_legacy_quarantine_v2 from public;

grant select on
  xfactory_runtime_v2.legacy_jobs,
  xfactory_runtime_v2.legacy_job_runs,
  xfactory_runtime_v2.legacy_job_events,
  xfactory_runtime_v2.legacy_workers,
  xfactory_runtime_v2.legacy_groups,
  xfactory_runtime_v2.legacy_profiles,
  xfactory_runtime_v2.legacy_group_memberships,
  xfactory_runtime_v2.legacy_github_team_mappings
to xfactory_v2_runtime, xfactory_v2_audit;

grant usage on schema xfactory_runtime_api_v2 to xfactory_v2_migrator;

grant execute on function
  xfactory_runtime_api_v2.stage_migration(jsonb),
  xfactory_runtime_api_v2.begin_migration_attempt(text, text),
  xfactory_runtime_api_v2.execute_v1_cutover(text, text, text),
  xfactory_runtime_api_v2.fail_migration_attempt(text, text, text, text),
  xfactory_runtime_api_v2.migration_result(text, text)
to xfactory_v2_migrator;

reset role;

-- the quarantine dependency guard is an event trigger and therefore requires
-- superuser context: it is created outside the owner section, after reset.
do $quarantine_guard$
begin
  if not exists (
    select 1
    from pg_event_trigger
    where evtname = 'xfactory_quarantine_dependency_guard'
  ) then
    create event trigger xfactory_quarantine_dependency_guard
      on ddl_command_end
      execute function xfactory_runtime_v2.reject_quarantine_dependency();
  end if;
end
$quarantine_guard$;
