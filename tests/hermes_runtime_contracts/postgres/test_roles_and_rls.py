"""RED real-PostgreSQL contracts for roles, trusted scope, and forced RLS."""

from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from .conftest import (
    ISOLATION_ASSERTION_ROOT,
    PostgresDatabase,
    assert_sql_fails,
    assert_sql_succeeds,
)

pytestmark = pytest.mark.postgres


def _assertion(name: str) -> Path:
    return ISOLATION_ASSERTION_ROOT / name


def _assert_zero_rows_or_denied(result: subprocess.CompletedProcess[str]) -> None:
    if result.returncode == 0:
        rows = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        assert rows[-1] == "0", rows
    else:
        assert_sql_fails(result, "permission", "scope", "denied", "authority")


def test_runtime_control_and_audit_roles_are_non_owner_non_bypass_identities(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.file(_assertion("role-catalog.sql"))
    assert_sql_succeeds(result)
    assert result.stdout.strip() == "t"


def test_all_layer_evidence_tables_enable_and_force_rls(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.file(_assertion("rls-catalog.sql"))
    assert_sql_succeeds(result)
    assert result.stdout.strip() == "t"


def test_governed_api_is_security_definer_fixed_path_and_not_public(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.file(_assertion("security-definer-catalog.sql"))
    assert_sql_succeeds(result)
    assert result.stdout.strip() == "t"


def test_assume_scope_binds_authenticated_session_user_to_exact_principal(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        SELECT session_user || ':' || current_user || ':' ||
               string_agg(DISTINCT layer_id, ',' ORDER BY layer_id)
        FROM xfactory_runtime_v2.artifact_records;
        ROLLBACK;
        """,
        user="hcs_customer_a",
    )
    assert_sql_succeeds(result)
    assert result.stdout.splitlines()[-1].strip() == (
        "hcs_customer_a:hcs_customer_a:customer-a"
    )


def test_customer_a_cannot_enumerate_or_read_customer_b(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        SELECT count(*)
        FROM xfactory_runtime_v2.artifact_records
        WHERE installation_id = 'install-01'
          AND stack_id = 'stack-01'
          AND layer_id = 'customer-b';
        ROLLBACK;
        """,
        user="hcs_customer_a",
    )
    assert_sql_succeeds(result)
    assert result.stdout.splitlines()[-1].strip() == "0"


@pytest.mark.parametrize("operation", ["insert", "update", "delete"])
def test_customer_a_cannot_write_or_delete_customer_b(
    postgres_database: PostgresDatabase,
    operation: str,
) -> None:
    statements = {
        "insert": """
          INSERT INTO xfactory_runtime_v2.artifact_records (
            installation_id, stack_id, layer_id, artifact_id, record_digest,
            digest_profile, content_digest, byte_size, media_type,
            storage_key, producer_principal_id, producer_grant_id,
            producer_grant_digest, created_at
          ) VALUES (
            'install-01', 'stack-01', 'customer-b', 'forged-by-a',
            'sha256:abababababababababababababababababababababababababababababababab',
            'xfactory-canonical-json-v1',
            'sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            1, 'text/plain',
            'install-01/customer-b/sha256/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'principal-a', 'grant-a-artifact',
            'sha256:d700000000000000000000000000000000000000000000000000000000000007',
            transaction_timestamp()
          );
        """,
        "update": """
          UPDATE xfactory_runtime_v2.artifact_records
          SET media_type = 'application/octet-stream'
          WHERE installation_id = 'install-01'
            AND stack_id = 'stack-01'
            AND layer_id = 'customer-b';
        """,
        "delete": """
          DELETE FROM xfactory_runtime_v2.artifact_records
          WHERE installation_id = 'install-01'
            AND stack_id = 'stack-01'
            AND layer_id = 'customer-b';
        """,
    }
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        """ + statements[operation] + "\nCOMMIT;",
        user="hcs_customer_a",
    )
    if operation == "insert":
        assert_sql_fails(result, "row-level", "policy", "scope", "permission")
    else:
        # RLS may hide the row and yield a harmless zero-row command. Either
        # outcome is valid only when B remains unchanged.
        if result.returncode != 0:
            assert_sql_fails(result, "immutable", "row-level", "scope", "permission")
    assert postgres_database.scalar("""
        SELECT count(*)
        FROM xfactory_runtime_v2.artifact_records
        WHERE installation_id = 'install-01'
          AND stack_id = 'stack-01'
          AND layer_id = 'customer-b'
          AND artifact_id = 'artifact-b-draft';
        """) == "1"


def test_forged_custom_gucs_do_not_establish_scope(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT set_config('xfactory.installation_id', 'install-01', true);
        SELECT set_config('xfactory.stack_id', 'stack-01', true);
        SELECT set_config('xfactory.layer_id', 'customer-b', true);
        SELECT set_config('xfactory.grant_id', 'grant-b-scope', true);
        SELECT count(*) FROM xfactory_runtime_v2.artifact_records;
        ROLLBACK;
        """,
        user="hcs_unbound",
    )
    _assert_zero_rows_or_denied(result)


@pytest.mark.parametrize("user", ["hcs_install_admin", "hcs_control_plane"])
def test_install_admin_and_control_plane_have_no_direct_subject_visibility(
    postgres_database: PostgresDatabase,
    user: str,
) -> None:
    result = postgres_database.sql(
        "SELECT count(*) FROM xfactory_runtime_v2.artifact_records;",
        user=user,
    )
    _assert_zero_rows_or_denied(result)


def test_runtime_login_cannot_assume_owner_or_migrator(
    postgres_database: PostgresDatabase,
) -> None:
    for role in ("xfactory_v2_owner", "xfactory_v2_migrator"):
        result = postgres_database.sql(f"SET ROLE {role};", user="hcs_customer_a")
        assert_sql_fails(result, "permission", "role", "denied")


@pytest.mark.parametrize(
    ("installation_id", "stack_id", "layer_id", "grant_id"),
    [
        ("install-02", "stack-01", "customer-a", "grant-a-scope"),
        ("install-01", "stack-02", "customer-a", "grant-a-scope"),
        ("install-01", "stack-01", "customer-b", "grant-a-scope"),
        ("install-01", "stack-01", "customer-b", "grant-b-scope"),
    ],
)
def test_assume_scope_rejects_cross_install_stack_layer_or_foreign_grant(
    postgres_database: PostgresDatabase,
    installation_id: str,
    stack_id: str,
    layer_id: str,
    grant_id: str,
) -> None:
    result = postgres_database.sql(
        f"""
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          '{installation_id}', '{stack_id}', '{layer_id}', '{grant_id}'
        );
        ROLLBACK;
        """,
        user="hcs_customer_a",
    )
    assert_sql_fails(result, "session_user", "principal", "scope", "grant", "authority")
