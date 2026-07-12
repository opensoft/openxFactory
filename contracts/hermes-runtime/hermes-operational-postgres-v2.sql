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
  role_class text not null check (role_class in ('runtime', 'control', 'audit')),
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

reset role;
