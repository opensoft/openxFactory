"""PostgreSQL alignment checks for the portable Hermes authority contracts.

These tests intentionally exercise the database contract independently from
the portable fixture suite.  A PostgreSQL realization must not accept a weaker
authority or evidence model than the published YAML schemas and semantics.
"""

from __future__ import annotations

import json

import pytest

from scripts.hermes_runtime_validation.semantics.authority import (
    canonical_record_digest,
)

from .conftest import PostgresDatabase, assert_sql_fails, assert_sql_succeeds

pytestmark = pytest.mark.postgres


def _digest(character: str) -> str:
    return f"sha256:{character * 64}"


def _rows(result: object) -> list[str]:
    stdout = getattr(result, "stdout", "")
    return [line.strip() for line in stdout.splitlines() if line.strip()]


def _columns(database: PostgresDatabase, table: str) -> set[str]:
    value = database.scalar(f"""
        SELECT string_agg(column_name, ',' ORDER BY ordinal_position)
        FROM information_schema.columns
        WHERE table_schema = 'xfactory_runtime_v2'
          AND table_name = '{table}';
        """)
    return set(value.split(","))


def _function_definitions(database: PostgresDatabase) -> str:
    result = database.sql("""
        SELECT pg_get_functiondef(proc.oid)
        FROM pg_proc AS proc
        JOIN pg_namespace AS namespace ON namespace.oid = proc.pronamespace
        WHERE namespace.nspname IN ('xfactory_runtime_v2', 'xfactory_runtime_api_v2')
        ORDER BY namespace.nspname, proc.proname, proc.oid;
        """)
    assert_sql_succeeds(result)
    return result.stdout.lower()


def _constraint_definitions(database: PostgresDatabase, table: str) -> str:
    return database.scalar(f"""
        SELECT coalesce(string_agg(pg_get_constraintdef(constraint_row.oid), ' '), '')
        FROM pg_constraint AS constraint_row
        WHERE constraint_row.conrelid =
          'xfactory_runtime_v2.{table}'::regclass;
        """).lower()


def _assert_rejected_or_false(result: object) -> None:
    if getattr(result, "returncode", 1) != 0:
        return
    rows = _rows(result)
    assert rows and rows[-1] in {"f", "0"}, rows


def test_approval_storage_can_represent_canonical_selector_policy(
    postgres_database: PostgresDatabase,
) -> None:
    assert {
        "reviewer_selectors",
        "minimum_approvals",
        "supersession_authorities",
    } <= _columns(postgres_database, "approval_decision_policies")
    assert "reviewer_selector_ids" in _columns(postgres_database, "approval_requests")
    assert "reviewer_selector_id" in _columns(postgres_database, "approval_decisions")

    definitions = _function_definitions(postgres_database)
    for required_semantic in (
        "all_required_selectors",
        "minimum_count",
        "principal_types",
        "group_principal_ids",
        "reviewer_selector_id",
    ):
        assert required_semantic in definitions


def test_sql_uses_the_canonical_closed_event_and_decision_vocabularies(
    postgres_database: PostgresDatabase,
) -> None:
    decisions = _constraint_definitions(postgres_database, "approval_decisions")
    assert "'approve'" in decisions and "'reject'" in decisions
    assert "'approved'" not in decisions
    assert "'rejected'" not in decisions
    assert "'changes_requested'" not in decisions

    artifact_events = _constraint_definitions(
        postgres_database, "artifact_lifecycle_events"
    )
    assert {
        "event_digest",
        "artifact_record_digest",
        "predecessor_kind",
        "predecessor_id",
        "predecessor_digest",
        "actor_principal_id",
        "actor_principal_digest",
        "actor_grant_id",
        "actor_grant_digest",
    } <= _columns(postgres_database, "artifact_lifecycle_events")
    for event_type in ("available", "retired", "tombstoned"):
        assert f"'{event_type}'" in artifact_events
    assert "'withdrawn'" not in artifact_events
    assert "'retained'" not in artifact_events

    anchor_events = _constraint_definitions(
        postgres_database, "installation_trust_anchor_events"
    )
    assert "'rotate'" in anchor_events and "'revoke'" in anchor_events
    assert "'rotated'" not in anchor_events
    assert "'revoked'" not in anchor_events


def test_root_grant_must_match_the_exact_anchor_digest(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(f"""
        BEGIN;
        INSERT INTO xfactory_runtime_v2.authority_grants (
          installation_id, grant_id, record_digest, digest_profile, grant_kind,
          grantee_stack_id, grantee_layer_id, grantee_principal_id,
          grantee_principal_digest,
          trust_anchor_id, trust_anchor_digest, issuer_grant_id,
          issuer_grant_digest, scope_kind, scope_stack_id, scope_layer_id,
          action, resource_type, resource_id, resource_digest,
          policy_repository, policy_commit, policy_ref, policy_digest,
          starts_at, expires_at, issued_at
        ) VALUES (
          'install-01', 'grant-forged-anchor-digest', '{_digest("1")}',
          'xfactory-canonical-json-v1', 'root', '', '', 'principal-control',
          'sha256:a400000000000000000000000000000000000000000000000000000000000004',
          'anchor-01', '{_digest("f")}', NULL, NULL, 'installation', '', '',
          'issue_grant', 'policy_namespace', 'install-01', NULL,
          'opensoft/exampleFactory',
          'dddddddddddddddddddddddddddddddddddddddd',
          'policies/authority.yaml', '{_digest("c")}',
          '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z',
          '2020-01-01T00:00:00Z'
        );
        SELECT EXISTS (
          SELECT 1 FROM xfactory_runtime_v2.active_authority_chain(
            'install-01', 'grant-forged-anchor-digest', 'issue_grant',
            'installation', '', '', 'principal-control',
            '2026-07-12T13:00:00Z'
          )
        )::text;
        ROLLBACK;
        """)
    assert_sql_fails(result, "hgr-grant-anchor-reference")


def test_root_grant_cannot_bypass_the_installation_scope_boundary(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(f"""
        BEGIN;
        INSERT INTO xfactory_runtime_v2.authority_grants (
          installation_id, grant_id, record_digest, digest_profile, grant_kind,
          grantee_stack_id, grantee_layer_id, grantee_principal_id,
          grantee_principal_digest,
          trust_anchor_id, trust_anchor_digest, issuer_grant_id,
          issuer_grant_digest, scope_kind, scope_stack_id, scope_layer_id,
          action, resource_type, resource_id, resource_digest,
          policy_repository, policy_commit, policy_ref, policy_digest,
          starts_at, expires_at, issued_at
        ) VALUES (
          'install-01', 'grant-root-layer-scope', '{_digest("2")}',
          'xfactory-canonical-json-v1', 'root', 'stack-01', 'customer-a',
          'principal-a',
          'sha256:a100000000000000000000000000000000000000000000000000000000000001',
          'anchor-01',
          (SELECT record_digest
           FROM xfactory_runtime_v2.installation_trust_anchors
           WHERE installation_id = 'install-01' AND anchor_id = 'anchor-01'),
          NULL, NULL, 'layer', 'stack-01', 'customer-a',
          'assume_scope', 'layer_identity', 'customer-a', NULL,
          'opensoft/exampleFactory',
          'dddddddddddddddddddddddddddddddddddddddd',
          'policies/authority.yaml', '{_digest("c")}',
          '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z',
          '2020-01-01T00:00:00Z'
        );
        SELECT EXISTS (
          SELECT 1 FROM xfactory_runtime_v2.active_authority_chain(
            'install-01', 'grant-root-layer-scope', 'assume_scope',
            'layer', 'stack-01', 'customer-a', 'principal-a',
            '2026-07-12T13:00:00Z'
          )
        )::text;
        ROLLBACK;
        """)
    assert_sql_fails(result, "authority_grants_root_scope_ck")


def test_malformed_anchor_rotation_cannot_activate_a_new_root(
    postgres_database: PostgresDatabase,
) -> None:
    assert {
        "from_anchor_digest",
        "to_anchor_digest",
        "authority_grant_digest",
    } <= _columns(postgres_database, "installation_trust_anchor_events")

    valid_result = postgres_database.sql(f"""
        BEGIN;
        INSERT INTO xfactory_runtime_v2.installation_trust_anchors (
          installation_id, anchor_id, record_digest, digest_profile,
          anchor_kind, principal_stack_id, principal_layer_id, principal_id,
          principal_digest, key_provider, key_id, key_algorithm,
          policy_repository, policy_commit, policy_ref, policy_digest,
          authorized_evidence_digest, effective_at, created_at
        ) VALUES (
          'install-01', 'anchor-approved', '{_digest("b")}',
          'xfactory-canonical-json-v1', 'rotated', '', '',
          'principal-control',
          'sha256:a400000000000000000000000000000000000000000000000000000000000004',
          'example-kms', 'anchor-approved', 'ed25519',
          'opensoft/exampleFactory',
          'dddddddddddddddddddddddddddddddddddddddd',
          'policies/authority.yaml',
          'sha256:c100000000000000000000000000000000000000000000000000000000000001',
          '{_digest("5")}', '2026-07-12T12:06:00Z',
          '2026-07-12T12:06:00Z'
        );
        INSERT INTO xfactory_runtime_v2.authority_grants (
          installation_id, grant_id, record_digest, digest_profile, grant_kind,
          grantee_stack_id, grantee_layer_id, grantee_principal_id,
          grantee_principal_digest, trust_anchor_id, trust_anchor_digest,
          issuer_grant_id, issuer_grant_digest, scope_kind, scope_stack_id,
          scope_layer_id, action, resource_type, resource_id, resource_digest,
          policy_repository, policy_commit, policy_ref, policy_digest,
          starts_at, expires_at, issued_at
        ) VALUES (
          'install-01', 'grant-root-rotate-approved', '{_digest("d")}',
          'xfactory-canonical-json-v1', 'root', '', '', 'principal-control',
          'sha256:a400000000000000000000000000000000000000000000000000000000000004',
          'anchor-01',
          (SELECT record_digest
           FROM xfactory_runtime_v2.installation_trust_anchors
           WHERE installation_id = 'install-01' AND anchor_id = 'anchor-01'),
          NULL, NULL, 'installation', '', '', 'rotate_trust_anchor',
          'trust_anchor', 'anchor-01',
          (SELECT record_digest
           FROM xfactory_runtime_v2.installation_trust_anchors
           WHERE installation_id = 'install-01' AND anchor_id = 'anchor-01'),
          'opensoft/exampleFactory',
          'dddddddddddddddddddddddddddddddddddddddd',
          'policies/authority.yaml',
          'sha256:c100000000000000000000000000000000000000000000000000000000000001',
          '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z',
          '2020-01-01T00:00:00Z'
        );
        INSERT INTO xfactory_runtime_v2.installation_trust_anchor_events (
          installation_id, event_id, record_digest, digest_profile, event_type,
          predecessor_kind, predecessor_id, predecessor_digest,
          from_anchor_id, from_anchor_digest, to_anchor_id, to_anchor_digest,
          authority_principal_stack_id, authority_principal_layer_id,
          authority_principal_id, authority_principal_digest,
          authority_grant_id, authority_grant_digest, reason,
          effective_at, occurred_at
        ) VALUES (
          'install-01', 'rotate-approved',
          xfactory_runtime_v2.canonical_record_digest(
            jsonb_build_object(
              'schema_version', 1,
              'kind', 'openxfactory-installation-trust-anchor-event',
              'event_id', 'rotate-approved',
              'record_digest_profile', 'xfactory-canonical-json-v1',
              'installation_id', 'install-01',
              'predecessor_ref', jsonb_build_object(
                'kind', 'registration', 'id', 'anchor-01',
                'record_digest', (SELECT record_digest
                 FROM xfactory_runtime_v2.installation_trust_anchors
                 WHERE installation_id = 'install-01'
                   AND anchor_id = 'anchor-01')
              ),
              'event_type', 'rotate',
              'predecessor_anchor_ref', jsonb_build_object(
                'installation_id', 'install-01', 'anchor_id', 'anchor-01',
                'record_digest', (SELECT record_digest
                 FROM xfactory_runtime_v2.installation_trust_anchors
                 WHERE installation_id = 'install-01'
                   AND anchor_id = 'anchor-01')
              ),
              'successor_anchor_ref', jsonb_build_object(
                'installation_id', 'install-01',
                'anchor_id', 'anchor-approved',
                'record_digest', (SELECT record_digest
                 FROM xfactory_runtime_v2.installation_trust_anchors
                 WHERE installation_id = 'install-01'
                   AND anchor_id = 'anchor-approved')
              ),
              'authorizing_principal_ref', jsonb_build_object(
                'scope', jsonb_build_object(
                  'scope_kind', 'installation_admin',
                  'installation_id', 'install-01'
                ),
                'principal_id', 'principal-control',
                'record_digest',
                'sha256:a400000000000000000000000000000000000000000000000000000000000004'
              ),
              'authorizing_grant_ref', jsonb_build_object(
                'installation_id', 'install-01',
                'grant_id', 'grant-root-rotate-approved',
                'record_digest', (SELECT record_digest
                 FROM xfactory_runtime_v2.authority_grants
                 WHERE installation_id = 'install-01'
                   AND grant_id = 'grant-root-rotate-approved')
              ),
              'effective_at', '2026-07-12T12:07:00.000000Z',
              'occurred_at', '2026-07-12T12:07:00.000000Z',
              'reason', 'approved-current-root-rotation'
            )
          ),
          'xfactory-canonical-json-v1', 'rotate', 'registration', 'anchor-01',
          (SELECT record_digest
           FROM xfactory_runtime_v2.installation_trust_anchors
           WHERE installation_id = 'install-01' AND anchor_id = 'anchor-01'),
          'anchor-01',
          (SELECT record_digest
           FROM xfactory_runtime_v2.installation_trust_anchors
           WHERE installation_id = 'install-01' AND anchor_id = 'anchor-01'),
          'anchor-approved',
          (SELECT record_digest
           FROM xfactory_runtime_v2.installation_trust_anchors
           WHERE installation_id = 'install-01'
             AND anchor_id = 'anchor-approved'),
          '', '', 'principal-control',
          'sha256:a400000000000000000000000000000000000000000000000000000000000004',
          'grant-root-rotate-approved',
          (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
           WHERE installation_id = 'install-01'
             AND grant_id = 'grant-root-rotate-approved'),
          'approved-current-root-rotation', '2026-07-12T12:07:00Z',
          '2026-07-12T12:07:00Z'
        );
        SELECT xfactory_runtime_v2.anchor_is_active(
          'install-01', 'anchor-approved', '2026-07-12T13:00:00Z'
        )::text;
        ROLLBACK;
        """)
    assert_sql_succeeds(valid_result)
    assert _rows(valid_result)[-1] == "true"

    result = postgres_database.sql(f"""
        BEGIN;
        INSERT INTO xfactory_runtime_v2.installation_trust_anchors (
          installation_id, anchor_id, record_digest, digest_profile,
          anchor_kind, principal_stack_id, principal_layer_id, principal_id,
          principal_digest, key_provider, key_id, key_algorithm,
          policy_repository, policy_commit, policy_ref, policy_digest,
          authorized_evidence_digest, effective_at, created_at
        ) VALUES (
          'install-01', 'anchor-unapproved', '{_digest("3")}',
          'xfactory-canonical-json-v1', 'rotated', '', '',
          'principal-control',
          'sha256:a400000000000000000000000000000000000000000000000000000000000004',
          'example-kms', 'anchor-unapproved', 'ed25519',
          'opensoft/exampleFactory',
          'dddddddddddddddddddddddddddddddddddddddd',
          'policies/authority.yaml',
          'sha256:c100000000000000000000000000000000000000000000000000000000000001',
          '{_digest("5")}', '2026-07-12T12:06:00Z',
          '2026-07-12T12:06:00Z'
        );
        INSERT INTO xfactory_runtime_v2.installation_trust_anchor_events (
          installation_id, event_id, record_digest, digest_profile, event_type,
          predecessor_kind, predecessor_id, predecessor_digest,
          from_anchor_id, from_anchor_digest, to_anchor_id, to_anchor_digest,
          authority_principal_stack_id, authority_principal_layer_id,
          authority_principal_id, authority_principal_digest,
          authority_grant_id, authority_grant_digest, reason,
          effective_at, occurred_at
        ) VALUES (
          'install-01', 'rotate-unapproved',
          xfactory_runtime_v2.canonical_record_digest(
            jsonb_build_object(
              'schema_version', 1,
              'kind', 'openxfactory-installation-trust-anchor-event',
              'event_id', 'rotate-unapproved',
              'record_digest_profile', 'xfactory-canonical-json-v1',
              'installation_id', 'install-01',
              'predecessor_ref', jsonb_build_object(
                'kind', 'event', 'id', 'event-never-existed',
                'record_digest', '{_digest("7")}'
              ),
              'event_type', 'rotate',
              'predecessor_anchor_ref', jsonb_build_object(
                'installation_id', 'install-01', 'anchor_id', 'anchor-01',
                'record_digest', (SELECT record_digest
                 FROM xfactory_runtime_v2.installation_trust_anchors
                 WHERE installation_id = 'install-01'
                   AND anchor_id = 'anchor-01')
              ),
              'successor_anchor_ref', jsonb_build_object(
                'installation_id', 'install-01',
                'anchor_id', 'anchor-unapproved',
                'record_digest', (SELECT record_digest
                 FROM xfactory_runtime_v2.installation_trust_anchors
                 WHERE installation_id = 'install-01'
                   AND anchor_id = 'anchor-unapproved')
              ),
              'authorizing_principal_ref', jsonb_build_object(
                'scope', jsonb_build_object(
                  'scope_kind', 'installation_admin',
                  'installation_id', 'install-01'
                ),
                'principal_id', 'principal-control',
                'record_digest',
                'sha256:a400000000000000000000000000000000000000000000000000000000000004'
              ),
              'authorizing_grant_ref', jsonb_build_object(
                'installation_id', 'install-01',
                'grant_id', 'grant-a-project',
                'record_digest', (SELECT record_digest
                 FROM xfactory_runtime_v2.authority_grants
                 WHERE installation_id = 'install-01'
                   AND grant_id = 'grant-a-project')
              ),
              'effective_at', '2026-07-12T12:07:00.000000Z',
              'occurred_at', '2026-07-12T12:07:00.000000Z',
              'reason', 'not-authorized-by-current-anchor'
            )
          ),
          'xfactory-canonical-json-v1', 'rotate', 'event',
          'event-never-existed', '{_digest("7")}', 'anchor-01',
          (SELECT record_digest
           FROM xfactory_runtime_v2.installation_trust_anchors
           WHERE installation_id = 'install-01' AND anchor_id = 'anchor-01'),
          'anchor-unapproved',
          (SELECT record_digest
           FROM xfactory_runtime_v2.installation_trust_anchors
           WHERE installation_id = 'install-01'
             AND anchor_id = 'anchor-unapproved'),
          '', '',
          'principal-control',
          'sha256:a400000000000000000000000000000000000000000000000000000000000004',
          'grant-a-project',
          (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
           WHERE installation_id = 'install-01' AND grant_id = 'grant-a-project'),
          'not-authorized-by-current-anchor', '2026-07-12T12:07:00Z',
          '2026-07-12T12:07:00Z'
        );
        SELECT xfactory_runtime_v2.anchor_is_active(
          'install-01', 'anchor-unapproved', '2026-07-12T13:00:00Z'
        )::text;
        ROLLBACK;
        """)
    assert_sql_succeeds(result)
    assert _rows(result)[-1] == "false"


def test_binding_creation_and_operation_authority_are_distinct(
    postgres_database: PostgresDatabase,
) -> None:
    assert {"creator_principal_id", "creator_principal_digest"} <= _columns(
        postgres_database, "cross_layer_bindings"
    )
    assert {"source_grant_id", "source_grant_digest"} <= _columns(
        postgres_database, "operation_authorizations"
    )
    assert postgres_database.scalar("""
        SELECT bool_and(creator.action = 'create_binding')
        FROM xfactory_runtime_v2.cross_layer_bindings AS binding
        JOIN xfactory_runtime_v2.authority_grants AS creator
          ON creator.installation_id = binding.installation_id
         AND creator.grant_id = binding.creator_grant_id
         AND creator.record_digest = binding.creator_grant_digest;
        """) == "t"

    arguments = postgres_database.scalar("""
        SELECT pg_get_function_arguments(proc.oid)
        FROM pg_proc AS proc
        JOIN pg_namespace AS namespace ON namespace.oid = proc.pronamespace
        WHERE namespace.nspname = 'xfactory_runtime_api_v2'
          AND proc.proname = 'project_artifact';
        """)
    assert "requested_source_grant_id" in arguments

    invalid_creator = postgres_database.sql("""
        BEGIN;
        INSERT INTO xfactory_runtime_v2.cross_layer_bindings (
          installation_id, binding_id, record_digest, digest_profile,
          source_stack_id, source_layer_id, source_resource_type,
          source_resource_id, source_resource_digest, target_stack_id,
          target_layer_id, target_resource_type, target_resource_id,
          target_resource_digest, action, purpose,
          creator_principal_stack_id, creator_principal_layer_id,
          creator_principal_id, creator_principal_digest,
          creator_grant_id, creator_grant_digest,
          target_acceptance_grant_id, target_acceptance_grant_digest,
          target_acceptance_principal_stack_id,
          target_acceptance_principal_layer_id,
          target_acceptance_principal_id,
          target_acceptance_principal_digest, starts_at, expires_at, created_at
        ) VALUES (
          'install-01', 'binding-invalid-creator',
          'sha256:1111111111111111111111111111111111111111111111111111111111111111',
          'xfactory-canonical-json-v1', 'stack-01', 'customer-a', 'artifact',
          'artifact-a',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'stack-01', 'customer-b', 'artifact', 'artifact-b-draft',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'project_resource', 'invalid-creator-test', '', '',
          'principal-control',
          'sha256:a400000000000000000000000000000000000000000000000000000000000004',
          'grant-a-project',
          (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
           WHERE installation_id = 'install-01' AND grant_id = 'grant-a-project'),
          'grant-b-accept',
          (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
           WHERE installation_id = 'install-01' AND grant_id = 'grant-b-accept'),
          'stack-01', 'customer-b', 'principal-b',
          'sha256:a200000000000000000000000000000000000000000000000000000000000002',
          '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z',
          '2026-07-12T12:09:00Z'
        );
        ROLLBACK;
        """)
    assert_sql_fails(invalid_creator, "hgr-binding-creation-authority")

    invalid_acceptance = postgres_database.sql("""
        BEGIN;
        INSERT INTO xfactory_runtime_v2.cross_layer_bindings (
          installation_id, binding_id, record_digest, digest_profile,
          source_stack_id, source_layer_id, source_resource_type,
          source_resource_id, source_resource_digest, target_stack_id,
          target_layer_id, target_resource_type, target_resource_id,
          target_resource_digest, action, purpose,
          creator_principal_stack_id, creator_principal_layer_id,
          creator_principal_id, creator_principal_digest,
          creator_grant_id, creator_grant_digest,
          target_acceptance_grant_id, target_acceptance_grant_digest,
          target_acceptance_principal_stack_id,
          target_acceptance_principal_layer_id,
          target_acceptance_principal_id,
          target_acceptance_principal_digest, starts_at, expires_at, created_at
        ) VALUES (
          'install-01', 'binding-invalid-acceptance',
          'sha256:2222222222222222222222222222222222222222222222222222222222222222',
          'xfactory-canonical-json-v1', 'stack-01', 'customer-a', 'artifact',
          'artifact-a',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'stack-01', 'customer-b', 'artifact', 'artifact-b-draft',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'project_resource', 'invalid-acceptance-test', '', '',
          'principal-control',
          'sha256:a400000000000000000000000000000000000000000000000000000000000004',
          'grant-a-create-binding',
          (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
           WHERE installation_id = 'install-01'
             AND grant_id = 'grant-a-create-binding'),
          'grant-b-artifact-draft',
          (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
           WHERE installation_id = 'install-01'
             AND grant_id = 'grant-b-artifact-draft'),
          'stack-01', 'customer-b', 'principal-b',
          'sha256:a200000000000000000000000000000000000000000000000000000000000002',
          '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z',
          '2026-07-12T12:09:00Z'
        );
        ROLLBACK;
        """)
    assert_sql_fails(invalid_acceptance, "hgr-binding-target-acceptance")

    database_timestamp = postgres_database.sql("""
        BEGIN;
        INSERT INTO xfactory_runtime_v2.cross_layer_bindings (
          installation_id, binding_id, record_digest, digest_profile,
          source_stack_id, source_layer_id, source_resource_type,
          source_resource_id, source_resource_digest, target_stack_id,
          target_layer_id, target_resource_type, target_resource_id,
          target_resource_digest, action, purpose,
          creator_principal_stack_id, creator_principal_layer_id,
          creator_principal_id, creator_principal_digest,
          creator_grant_id, creator_grant_digest,
          target_acceptance_grant_id, target_acceptance_grant_digest,
          target_acceptance_principal_stack_id,
          target_acceptance_principal_layer_id,
          target_acceptance_principal_id,
          target_acceptance_principal_digest, starts_at, expires_at, created_at
        ) VALUES (
          'install-01', 'binding-database-created-at',
          'sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
          'xfactory-canonical-json-v1', 'stack-01', 'customer-a', 'artifact',
          'artifact-a',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'stack-01', 'customer-b', 'artifact', 'artifact-b-draft',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'project_resource', 'database-created-at-test', '', '',
          'principal-control',
          'sha256:a400000000000000000000000000000000000000000000000000000000000004',
          'grant-a-create-binding',
          (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
           WHERE installation_id = 'install-01'
             AND grant_id = 'grant-a-create-binding'),
          'grant-b-accept',
          (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
           WHERE installation_id = 'install-01' AND grant_id = 'grant-b-accept'),
          'stack-01', 'customer-b', 'principal-b',
          'sha256:a200000000000000000000000000000000000000000000000000000000000002',
          '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z',
          '2020-01-02T00:00:00Z'
        );
        SELECT
          (created_at = transaction_timestamp())::text || ':' ||
          (record_digest <>
            'sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
          )::text
        FROM xfactory_runtime_v2.cross_layer_bindings
        WHERE installation_id = 'install-01'
          AND binding_id = 'binding-database-created-at';
        ROLLBACK;
        """)
    assert_sql_succeeds(database_timestamp)
    assert _rows(database_timestamp)[-1] == "true:true"

    backdated_expired_authority = postgres_database.sql("""
        BEGIN;
        INSERT INTO xfactory_runtime_v2.authority_grants (
          installation_id, grant_id, record_digest, digest_profile, grant_kind,
          grantee_stack_id, grantee_layer_id, grantee_principal_id,
          grantee_principal_digest, trust_anchor_id, trust_anchor_digest,
          issuer_grant_id, issuer_grant_digest, scope_kind, scope_stack_id,
          scope_layer_id, action, resource_type, resource_id, resource_digest,
          policy_repository, policy_commit, policy_ref, policy_digest,
          starts_at, expires_at, issued_at
        ) VALUES (
          'install-01', 'grant-a-create-binding-expired',
          'sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
          'xfactory-canonical-json-v1', 'delegated', '', '',
          'principal-control',
          'sha256:a400000000000000000000000000000000000000000000000000000000000004',
          NULL, NULL, 'grant-root-issue',
          (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
           WHERE installation_id = 'install-01' AND grant_id = 'grant-root-issue'),
          'layer', 'stack-01', 'customer-a', 'create_binding', 'artifact',
          'artifact-a',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'opensoft/exampleFactory',
          'dddddddddddddddddddddddddddddddddddddddd',
          'policies/delegated.yaml',
          'sha256:c200000000000000000000000000000000000000000000000000000000000002',
          '2020-01-01T00:00:00Z', '2021-01-01T00:00:00Z',
          '2020-01-01T00:00:00Z'
        );
        INSERT INTO xfactory_runtime_v2.cross_layer_bindings (
          installation_id, binding_id, record_digest, digest_profile,
          source_stack_id, source_layer_id, source_resource_type,
          source_resource_id, source_resource_digest, target_stack_id,
          target_layer_id, target_resource_type, target_resource_id,
          target_resource_digest, action, purpose,
          creator_principal_stack_id, creator_principal_layer_id,
          creator_principal_id, creator_principal_digest,
          creator_grant_id, creator_grant_digest,
          target_acceptance_grant_id, target_acceptance_grant_digest,
          target_acceptance_principal_stack_id,
          target_acceptance_principal_layer_id,
          target_acceptance_principal_id,
          target_acceptance_principal_digest, starts_at, expires_at, created_at
        ) VALUES (
          'install-01', 'binding-backdated-expired-grant',
          'sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
          'xfactory-canonical-json-v1', 'stack-01', 'customer-a', 'artifact',
          'artifact-a',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'stack-01', 'customer-b', 'artifact', 'artifact-b-draft',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'project_resource', 'backdated-expired-grant-test', '', '',
          'principal-control',
          'sha256:a400000000000000000000000000000000000000000000000000000000000004',
          'grant-a-create-binding-expired',
          (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
           WHERE installation_id = 'install-01'
             AND grant_id = 'grant-a-create-binding-expired'),
          'grant-b-accept',
          (SELECT record_digest FROM xfactory_runtime_v2.authority_grants
           WHERE installation_id = 'install-01' AND grant_id = 'grant-b-accept'),
          'stack-01', 'customer-b', 'principal-b',
          'sha256:a200000000000000000000000000000000000000000000000000000000000002',
          '2020-01-01T00:00:00Z', '2099-01-01T00:00:00Z',
          '2020-06-01T00:00:00Z'
        );
        ROLLBACK;
        """)
    assert_sql_fails(backdated_expired_authority, "hgr-binding-creation-authority")


def test_authority_rechecks_noncaller_principal_lifecycle(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(f"""
        BEGIN;
        INSERT INTO xfactory_runtime_v2.principal_lifecycle_events (
          installation_id, stack_id, layer_id, principal_id, event_id,
          event_digest, predecessor_id, predecessor_digest, from_state,
          to_state, authority_grant_id, reason, occurred_at
        )
        SELECT
          projection.installation_id, projection.stack_id, projection.layer_id,
          projection.entity_id, 'suspend-' || projection.entity_id,
          CASE projection.entity_id
            WHEN 'reviewer-a' THEN '{_digest("7")}'
            ELSE '{_digest("8")}'
          END,
          projection.latest_event_id, projection.latest_event_digest,
          projection.derived_state, 'suspended', 'grant-root-issue',
          'test governed suspension', transaction_timestamp()
        FROM xfactory_runtime_v2.lifecycle_projections projection
        WHERE projection.entity_kind = 'principal'
          AND projection.installation_id = 'install-01'
          AND projection.stack_id = 'stack-01'
          AND projection.layer_id = 'customer-b'
          AND projection.entity_id IN ('reviewer-a', 'principal-b');
        SELECT set_config('xfactory.governed_projection_write', 'on', true);
        UPDATE xfactory_runtime_v2.lifecycle_projections
        SET derived_state = 'suspended',
            latest_event_id = 'suspend-' || entity_id,
            latest_event_digest = CASE entity_id
              WHEN 'reviewer-a' THEN '{_digest("7")}'
              ELSE '{_digest("8")}'
            END
        WHERE entity_kind = 'principal'
          AND installation_id = 'install-01'
          AND stack_id = 'stack-01'
          AND layer_id = 'customer-b'
          AND entity_id IN ('reviewer-a', 'principal-b');
        SELECT
          EXISTS (
            SELECT 1 FROM xfactory_runtime_v2.active_authority_chain(
              'install-01', 'grant-review-a-decide', 'decide_approval',
              'layer', 'stack-01', 'customer-b', 'reviewer-a',
              transaction_timestamp()
            )
          )::text || ':' ||
          EXISTS (
            SELECT 1 FROM xfactory_runtime_v2.active_authority_chain(
              'install-01', 'grant-b-accept', 'accept_cross_layer',
              'layer', 'stack-01', 'customer-b', NULL,
              transaction_timestamp()
            )
          )::text;
        ROLLBACK;
        """)
    assert_sql_succeeds(result)
    assert _rows(result)[-1] == "false:false"


def test_supersession_storage_and_gate_bind_the_exact_policy_target(
    postgres_database: PostgresDatabase,
) -> None:
    assert {
        "target_kind",
        "target_id",
        "target_digest",
        "authority_scope_kind",
    } <= _columns(postgres_database, "approval_supersession_events")

    definitions = _function_definitions(postgres_database)
    for required_semantic in (
        "supersession_authorities",
        "approval_request",
        "approval_decision",
        "target_digest",
    ):
        assert required_semantic in definitions


def test_trace_storage_retains_creator_and_complete_cross_layer_grant_refs(
    postgres_database: PostgresDatabase,
) -> None:
    columns = _columns(postgres_database, "traceability_edges")
    assert {"creator_grant_id", "creator_grant_digest"} <= columns

    tables = set(postgres_database.scalar("""
            SELECT string_agg(table_name, ',' ORDER BY table_name)
            FROM information_schema.tables
            WHERE table_schema = 'xfactory_runtime_v2';
            """).split(","))
    inline_grants = {
        "source_grant_id",
        "source_grant_digest",
        "target_acceptance_grant_id",
        "target_acceptance_grant_digest",
    } <= columns
    assert (
        inline_grants or "grant_refs" in columns or "traceability_edge_grants" in tables
    )


def test_sql_and_python_share_one_canonical_record_digest(
    postgres_database: PostgresDatabase,
) -> None:
    record = {
        "schema_version": 1,
        "kind": "openxfactory-operation-authorization",
        "operation_id": "operation-digest-vector",
        "action": "project_resource",
        "purpose": "contract-alignment",
        "nested": {"z": 3, "a": [True, None, "utf8-é"]},
    }
    expected = canonical_record_digest(record)
    encoded = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
    actual = postgres_database.scalar(
        "SELECT xfactory_runtime_v2.canonical_record_digest("
        f"$record${encoded}$record$::jsonb);"
    )
    assert actual == expected

    admitted = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        SELECT xfactory_runtime_api_v2.admit_artifact(
          'artifact-a-new', convert_to('new-artifact-body', 'UTF8'),
          'text/plain', 'grant-a-artifact-new'
        );
        COMMIT;
        """,
        user="hcs_customer_a",
    )
    assert_sql_succeeds(admitted)

    persisted_artifact = json.loads(postgres_database.scalar("""
        SELECT jsonb_build_object(
          'stored_digest', artifact.record_digest,
          'record', jsonb_build_object(
            'schema_version', 1,
            'kind', 'openxfactory-hermes-runtime-artifact-record',
            'installation_id', artifact.installation_id,
            'stack_id', artifact.stack_id,
            'layer_id', artifact.layer_id,
            'artifact_id', artifact.artifact_id,
            'content_digest', artifact.content_digest,
            'byte_size', artifact.byte_size,
            'media_type', artifact.media_type,
            'producer_principal_ref', jsonb_build_object(
              'scope', jsonb_build_object(
                'scope_kind', 'layer',
                'installation_id', artifact.installation_id,
                'stack_id', artifact.stack_id,
                'layer_id', artifact.layer_id
              ),
              'principal_id', artifact.producer_principal_id,
              'record_digest', principal.record_digest
            ),
            'producer_grant_ref', jsonb_build_object(
              'installation_id', artifact.installation_id,
              'grant_id', artifact.producer_grant_id,
              'record_digest', artifact.producer_grant_digest
            ),
            'storage_key', artifact.storage_key,
            'created_at', to_char(
              artifact.created_at at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
            )
          )
        )::text
        FROM xfactory_runtime_v2.artifact_records artifact
        JOIN xfactory_runtime_v2.principals principal
          ON principal.installation_id = artifact.installation_id
         AND principal.stack_id = artifact.stack_id
         AND principal.layer_id = artifact.layer_id
         AND principal.principal_id = artifact.producer_principal_id
        WHERE artifact.artifact_id = 'artifact-a-new';
        """))
    assert persisted_artifact["stored_digest"] == canonical_record_digest(
        persisted_artifact["record"]
    )

    persisted_lifecycle = json.loads(postgres_database.scalar("""
        SELECT jsonb_build_object(
          'stored_digest', lifecycle.event_digest,
          'record', jsonb_build_object(
            'schema_version', 1,
            'kind', 'openxfactory-hermes-runtime-artifact-lifecycle-event',
            'event_id', lifecycle.event_id,
            'installation_id', lifecycle.installation_id,
            'stack_id', lifecycle.stack_id,
            'layer_id', lifecycle.layer_id,
            'artifact_id', lifecycle.artifact_id,
            'artifact_record_digest', lifecycle.artifact_record_digest,
            'predecessor_ref', jsonb_build_object(
              'kind', lifecycle.predecessor_kind,
              'id', lifecycle.predecessor_id,
              'digest', lifecycle.predecessor_digest
            ),
            'event_type', lifecycle.event_type,
            'actor_principal_ref', jsonb_build_object(
              'scope', jsonb_build_object(
                'scope_kind', 'layer',
                'installation_id', lifecycle.installation_id,
                'stack_id', lifecycle.stack_id,
                'layer_id', lifecycle.layer_id
              ),
              'principal_id', lifecycle.actor_principal_id,
              'record_digest', lifecycle.actor_principal_digest
            ),
            'actor_grant_ref', jsonb_build_object(
              'installation_id', lifecycle.installation_id,
              'grant_id', lifecycle.actor_grant_id,
              'record_digest', lifecycle.actor_grant_digest
            ),
            'occurred_at', to_char(
              lifecycle.occurred_at at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
            ),
            'reason', lifecycle.reason
          )
        )::text
        FROM xfactory_runtime_v2.artifact_lifecycle_events lifecycle
        WHERE lifecycle.artifact_id = 'artifact-a-new';
        """))
    assert persisted_lifecycle["stored_digest"] == canonical_record_digest(
        persisted_lifecycle["record"]
    )

    projected = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', '', '', 'grant-control-scope'
        );
        SELECT xfactory_runtime_api_v2.project_artifact(
          'operation-digest-roundtrip', 'binding-a-b', 'artifact-a',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'artifact-b-draft',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'grant-a-project', 'trace-digest-roundtrip'
        );
        COMMIT;
        """,
        user="hcs_control_plane",
    )
    assert_sql_succeeds(projected)

    persisted_operation = json.loads(postgres_database.scalar("""
        SELECT jsonb_build_object(
          'stored_digest', operation.record_digest,
          'record', jsonb_build_object(
            'schema_version', 1,
            'kind', 'openxfactory-operation-authorization',
            'operation_id', operation.operation_id,
            'record_digest_profile', operation.digest_profile,
            'source_scope', jsonb_build_object(
              'scope_kind', 'layer',
              'installation_id', operation.installation_id,
              'stack_id', operation.source_stack_id,
              'layer_id', operation.source_layer_id
            ),
            'target_scope', jsonb_build_object(
              'scope_kind', 'layer',
              'installation_id', operation.installation_id,
              'stack_id', operation.target_stack_id,
              'layer_id', operation.target_layer_id
            ),
            'source_resource', jsonb_build_object(
              'installation_id', operation.installation_id,
              'stack_id', operation.source_stack_id,
              'layer_id', operation.source_layer_id,
              'resource_type', operation.source_resource_type,
              'resource_id', operation.source_resource_id,
              'digest', operation.source_resource_digest
            ),
            'target_resource', jsonb_build_object(
              'installation_id', operation.installation_id,
              'stack_id', operation.target_stack_id,
              'layer_id', operation.target_layer_id,
              'resource_type', operation.target_resource_type,
              'resource_id', operation.target_resource_id,
              'digest', operation.target_resource_digest
            ),
            'action', operation.action,
            'purpose', operation.purpose,
            'actor_principal_ref', jsonb_build_object(
              'scope', jsonb_build_object(
                'scope_kind', 'installation_admin',
                'installation_id', operation.installation_id
              ),
              'principal_id', operation.actor_principal_id,
              'record_digest', operation.actor_principal_digest
            ),
            'source_grant_ref', jsonb_build_object(
              'installation_id', operation.installation_id,
              'grant_id', operation.source_grant_id,
              'record_digest', operation.source_grant_digest
            ),
            'target_acceptance_grant_ref', jsonb_build_object(
              'installation_id', operation.installation_id,
              'grant_id', operation.target_acceptance_grant_id,
              'record_digest', operation.target_acceptance_grant_digest
            ),
            'binding_ref', jsonb_build_object(
              'installation_id', operation.installation_id,
              'binding_id', operation.binding_id,
              'record_digest', operation.binding_digest
            ),
            'anchor_ref', jsonb_build_object(
              'installation_id', operation.installation_id,
              'anchor_id', operation.trust_anchor_id,
              'record_digest', operation.trust_anchor_digest
            ),
            'authorized_at', to_char(
              operation.authorized_at at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
            ),
            'target_result', jsonb_build_object(
              'installation_id', operation.installation_id,
              'stack_id', operation.target_stack_id,
              'layer_id', operation.target_layer_id,
              'resource_type', operation.target_result_type,
              'resource_id', operation.target_result_id,
              'digest', operation.target_result_digest
            ),
            'transaction_id', operation.transaction_id
          )
        )::text
        FROM xfactory_runtime_v2.operation_authorizations operation
        WHERE operation.operation_id = 'operation-digest-roundtrip';
        """))
    assert persisted_operation["stored_digest"] == canonical_record_digest(
        persisted_operation["record"]
    )

    persisted_trace = json.loads(postgres_database.scalar("""
        SELECT jsonb_build_object(
          'stored_digest', edge.edge_digest,
          'record', jsonb_build_object(
            'schema_version', 1,
            'kind', 'openxfactory-hermes-runtime-traceability-edge',
            'edge_id', edge.edge_id,
            'owning_scope', jsonb_build_object(
              'scope_kind', 'layer',
              'installation_id', edge.installation_id,
              'stack_id', edge.stack_id,
              'layer_id', edge.layer_id
            ),
            'relation', edge.relation,
            'source', jsonb_build_object(
              'installation_id', edge.installation_id,
              'stack_id', edge.source_stack_id,
              'layer_id', edge.source_layer_id,
              'resource_type', edge.source_type,
              'resource_id', edge.source_id,
              'digest', edge.source_digest
            ),
            'target', jsonb_build_object(
              'installation_id', edge.installation_id,
              'stack_id', edge.target_stack_id,
              'layer_id', edge.target_layer_id,
              'resource_type', edge.target_type,
              'resource_id', edge.target_id,
              'digest', edge.target_digest
            ),
            'creator_principal_ref', jsonb_build_object(
              'scope', jsonb_build_object(
                'scope_kind', 'installation_admin',
                'installation_id', edge.installation_id
              ),
              'principal_id', edge.creator_principal_id,
              'record_digest', edge.creator_principal_digest
            ),
            'creator_grant_ref', jsonb_build_object(
              'installation_id', edge.installation_id,
              'grant_id', edge.creator_grant_id,
              'record_digest', edge.creator_grant_digest
            ),
            'cross_layer_authority', jsonb_build_object(
              'operation_authorization_ref', jsonb_build_object(
                'installation_id', edge.installation_id,
                'operation_id', edge.operation_id,
                'record_digest', edge.operation_digest
              ),
              'binding_ref', jsonb_build_object(
                'installation_id', edge.installation_id,
                'binding_id', edge.binding_id,
                'record_digest', edge.binding_digest
              ),
              'grant_refs', edge.grant_refs
            ),
            'created_at', to_char(
              edge.created_at at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
            )
          )
        )::text
        FROM xfactory_runtime_v2.traceability_edges edge
        WHERE edge.edge_id = 'trace-digest-roundtrip';
        """))
    assert persisted_trace["stored_digest"] == canonical_record_digest(
        persisted_trace["record"]
    )


def test_static_authority_records_are_database_computed_canonical_content(
    postgres_database: PostgresDatabase,
) -> None:
    persisted_anchor = json.loads(postgres_database.scalar("""
        SELECT jsonb_build_object(
          'stored_digest', anchor_record.record_digest,
          'record', jsonb_build_object(
            'schema_version', 1,
            'kind', 'openxfactory-installation-trust-anchor',
            'anchor_id', anchor_record.anchor_id,
            'record_digest_profile', anchor_record.digest_profile,
            'installation_id', anchor_record.installation_id,
            'anchor_kind', anchor_record.anchor_kind,
            'principal_ref', jsonb_build_object(
              'scope', jsonb_build_object(
                'scope_kind', 'installation_admin',
                'installation_id', anchor_record.installation_id
              ),
              'principal_id', anchor_record.principal_id,
              'record_digest', anchor_record.principal_digest
            ),
            'key_ref', jsonb_build_object(
              'provider', anchor_record.key_provider,
              'key_id', anchor_record.key_id,
              'algorithm', anchor_record.key_algorithm
            ),
            'policy_pin', jsonb_build_object(
              'repository', anchor_record.policy_repository,
              'commit', anchor_record.policy_commit,
              'path', anchor_record.policy_ref,
              'digest', anchor_record.policy_digest
            ),
            'effective_at', to_char(
              anchor_record.effective_at at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
            ),
            'authorized_evidence_digest',
              anchor_record.authorized_evidence_digest,
            'created_at', to_char(
              anchor_record.created_at at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
            )
          )
        )::text
        FROM xfactory_runtime_v2.installation_trust_anchors anchor_record
        WHERE anchor_record.installation_id = 'install-01'
          AND anchor_record.anchor_id = 'anchor-01';
        """))
    assert persisted_anchor["stored_digest"] != (
        "sha256:c300000000000000000000000000000000000000000000000000000000000003"
    )
    assert persisted_anchor["stored_digest"] == canonical_record_digest(
        persisted_anchor["record"]
    )

    persisted_grant = json.loads(postgres_database.scalar("""
        SELECT jsonb_build_object(
          'stored_digest', grant_record.record_digest,
          'record', jsonb_build_object(
            'schema_version', 1,
            'kind', 'openxfactory-authority-grant',
            'grant_id', grant_record.grant_id,
            'record_digest_profile', grant_record.digest_profile,
            'installation_id', grant_record.installation_id,
            'grant_kind', grant_record.grant_kind,
            'principal_ref', jsonb_build_object(
              'scope', jsonb_build_object(
                'scope_kind', 'installation_admin',
                'installation_id', grant_record.installation_id
              ),
              'principal_id', grant_record.grantee_principal_id,
              'record_digest', grant_record.grantee_principal_digest
            ),
            'scope', jsonb_build_object(
              'scope_kind', 'layer',
              'installation_id', grant_record.installation_id,
              'stack_id', grant_record.scope_stack_id,
              'layer_id', grant_record.scope_layer_id
            ),
            'action', grant_record.action,
            'resource_constraint', jsonb_build_object(
              'installation_id', grant_record.installation_id,
              'stack_id', grant_record.scope_stack_id,
              'layer_id', grant_record.scope_layer_id,
              'resource_type', grant_record.resource_type,
              'resource_id', grant_record.resource_id,
              'digest', grant_record.resource_digest
            ),
            'policy_pin', jsonb_build_object(
              'repository', grant_record.policy_repository,
              'commit', grant_record.policy_commit,
              'path', grant_record.policy_ref,
              'digest', grant_record.policy_digest
            ),
            'issuer_grant_ref', jsonb_build_object(
              'installation_id', grant_record.installation_id,
              'grant_id', grant_record.issuer_grant_id,
              'record_digest', grant_record.issuer_grant_digest
            ),
            'starts_at', to_char(
              grant_record.starts_at at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
            ),
            'expires_at', to_char(
              grant_record.expires_at at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
            ),
            'issued_at', to_char(
              grant_record.issued_at at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
            )
          )
        )::text
        FROM xfactory_runtime_v2.authority_grants grant_record
        WHERE grant_record.installation_id = 'install-01'
          AND grant_record.grant_id = 'grant-a-create-binding';
        """))
    assert persisted_grant["stored_digest"] != (
        "sha256:e500000000000000000000000000000000000000000000000000000000000005"
    )
    assert persisted_grant["stored_digest"] == canonical_record_digest(
        persisted_grant["record"]
    )

    persisted_binding = json.loads(postgres_database.scalar("""
        SELECT jsonb_build_object(
          'stored_digest', binding.record_digest,
          'record', jsonb_build_object(
            'schema_version', 1,
            'kind', 'openxfactory-cross-layer-binding',
            'binding_id', binding.binding_id,
            'record_digest_profile', binding.digest_profile,
            'source_scope', jsonb_build_object(
              'scope_kind', 'layer',
              'installation_id', binding.installation_id,
              'stack_id', binding.source_stack_id,
              'layer_id', binding.source_layer_id
            ),
            'target_scope', jsonb_build_object(
              'scope_kind', 'layer',
              'installation_id', binding.installation_id,
              'stack_id', binding.target_stack_id,
              'layer_id', binding.target_layer_id
            ),
            'source_resource', jsonb_build_object(
              'installation_id', binding.installation_id,
              'stack_id', binding.source_stack_id,
              'layer_id', binding.source_layer_id,
              'resource_type', binding.source_resource_type,
              'resource_id', binding.source_resource_id,
              'digest', binding.source_resource_digest
            ),
            'target_resource', jsonb_build_object(
              'installation_id', binding.installation_id,
              'stack_id', binding.target_stack_id,
              'layer_id', binding.target_layer_id,
              'resource_type', binding.target_resource_type,
              'resource_id', binding.target_resource_id,
              'digest', binding.target_resource_digest
            ),
            'action', binding.action,
            'purpose', binding.purpose,
            'creator_principal_ref', jsonb_build_object(
              'scope', jsonb_build_object(
                'scope_kind', 'installation_admin',
                'installation_id', binding.installation_id
              ),
              'principal_id', binding.creator_principal_id,
              'record_digest', binding.creator_principal_digest
            ),
            'creator_grant_ref', jsonb_build_object(
              'installation_id', binding.installation_id,
              'grant_id', binding.creator_grant_id,
              'record_digest', binding.creator_grant_digest
            ),
            'target_acceptance_principal_ref', jsonb_build_object(
              'scope', jsonb_build_object(
                'scope_kind', 'layer',
                'installation_id', binding.installation_id,
                'stack_id', binding.target_acceptance_principal_stack_id,
                'layer_id', binding.target_acceptance_principal_layer_id
              ),
              'principal_id', binding.target_acceptance_principal_id,
              'record_digest', binding.target_acceptance_principal_digest
            ),
            'target_acceptance_grant_ref', jsonb_build_object(
              'installation_id', binding.installation_id,
              'grant_id', binding.target_acceptance_grant_id,
              'record_digest', binding.target_acceptance_grant_digest
            ),
            'starts_at', to_char(
              binding.starts_at at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
            ),
            'expires_at', to_char(
              binding.expires_at at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
            ),
            'created_at', to_char(
              binding.created_at at time zone 'UTC',
              'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
            )
          )
        )::text
        FROM xfactory_runtime_v2.cross_layer_bindings binding
        WHERE binding.installation_id = 'install-01'
          AND binding.binding_id = 'binding-a-b';
        """))
    assert persisted_binding["stored_digest"] != (
        "sha256:e100000000000000000000000000000000000000000000000000000000000001"
    )
    assert persisted_binding["stored_digest"] == canonical_record_digest(
        persisted_binding["record"]
    )


def test_governed_apis_do_not_trust_caller_supplied_record_digests(
    postgres_database: PostgresDatabase,
) -> None:
    definitions = _function_definitions(postgres_database)
    for function_name in ("record_approval_decision", "supersede_approval"):
        marker = f"function xfactory_runtime_api_v2.{function_name}"
        start = definitions.index(marker)
        next_function = definitions.find("create or replace function", start + 1)
        definition = definitions[start : next_function if next_function >= 0 else None]
        if "requested_record_digest" in definition:
            assert "canonical_record_digest" in definition


def test_database_binding_creator_is_an_exact_assume_scope_grant(
    postgres_database: PostgresDatabase,
) -> None:
    assert {
        "record_digest",
        "digest_profile",
        "principal_digest",
        "creator_grant_digest",
        "bound_at",
    } <= _columns(postgres_database, "database_principal_bindings")
    assert postgres_database.scalar("""
        SELECT bool_and(
          creator.action = 'assume_scope'
          AND creator.grantee_principal_id = binding.principal_id
          AND creator.scope_stack_id = binding.stack_id
          AND creator.scope_layer_id = binding.layer_id
        )
        FROM xfactory_runtime_v2.database_principal_bindings AS binding
        JOIN xfactory_runtime_v2.authority_grants AS creator
          ON creator.installation_id = binding.installation_id
         AND creator.grant_id = binding.creator_grant_id;
        """) == "t"


def test_invalid_database_binding_cannot_borrow_an_unrelated_scope_grant(
    postgres_database: PostgresDatabase,
) -> None:
    inserted = postgres_database.sql(f"""
        INSERT INTO xfactory_runtime_v2.database_principal_bindings (
          installation_id, stack_id, layer_id, binding_id, record_digest,
          digest_profile, session_user_name, principal_id, principal_digest,
          role_class, creator_grant_id, creator_grant_digest, bound_at
        ) VALUES (
          'install-01', 'stack-01', 'customer-a', 'dbbind-untrusted',
          '{_digest("9")}', 'xfactory-canonical-json-v1', 'hcs_unbound',
          'principal-a',
          'sha256:a100000000000000000000000000000000000000000000000000000000000001',
          'runtime', 'grant-root-issue',
          'sha256:d100000000000000000000000000000000000000000000000000000000000001',
          '2026-07-12T12:11:00Z'
        );
        """)
    assert_sql_succeeds(inserted)

    assumed = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        COMMIT;
        """,
        user="hcs_unbound",
    )
    assert_sql_fails(assumed, "hgr-scope-grant-inactive")


def test_projection_insert_requires_a_reconciled_lifecycle_event(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(f"""
        BEGIN;
        INSERT INTO xfactory_runtime_v2.principals (
          installation_id, stack_id, layer_id, principal_id, record_digest,
          digest_profile, principal_type, scope_kind, initial_state, created_at
        ) VALUES (
          'install-01', 'stack-01', 'customer-a', 'principal-unreconciled',
          '{_digest("a")}', 'xfactory-canonical-json-v1', 'agent', 'layer',
          'provisioning', '2026-07-12T12:12:00Z'
        );
        INSERT INTO xfactory_runtime_v2.lifecycle_projections (
          entity_kind, installation_id, stack_id, layer_id, entity_id,
          derived_state, latest_event_id, latest_event_digest
        ) VALUES (
          'principal', 'install-01', 'stack-01', 'customer-a',
          'principal-unreconciled', 'active', 'event-never-existed',
          '{_digest("b")}'
        );
        ROLLBACK;
        """)
    assert_sql_fails(result, "projection", "lifecycle", "event", "reconcile")
