"""RED real-PostgreSQL contracts for transaction-local pooled scope."""

from __future__ import annotations

import pytest

from .conftest import PostgresDatabase, assert_sql_fails, assert_sql_succeeds

pytestmark = pytest.mark.postgres


def test_assumed_scope_is_transaction_local_and_absent_after_commit(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        SELECT current_setting('xfactory.layer_id', true);
        COMMIT;
        SELECT COALESCE(NULLIF(current_setting('xfactory.layer_id', true), ''), 'absent');
        """,
        user="hcs_customer_a",
    )
    assert_sql_succeeds(result)
    rows = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    assert rows[-2:] == ["customer-a", "absent"]


def test_clear_scope_removes_all_authoritative_context_before_pool_return(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        SELECT xfactory_runtime_api_v2.clear_scope();
        SELECT count(*) FROM xfactory_runtime_v2.artifact_records;
        ROLLBACK;
        """,
        user="hcs_customer_a",
    )
    assert_sql_succeeds(result)
    assert result.stdout.splitlines()[-1].strip() == "0"


def test_same_session_second_transaction_never_reuses_prior_customer_scope(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        SELECT count(*) FROM xfactory_runtime_v2.artifact_records;
        COMMIT;
        BEGIN;
        SELECT count(*) FROM xfactory_runtime_v2.artifact_records;
        ROLLBACK;
        """,
        user="hcs_customer_a",
    )
    assert_sql_succeeds(result)
    counts = [
        line.strip() for line in result.stdout.splitlines() if line.strip().isdigit()
    ]
    assert counts[-2:] == ["1", "0"]


def test_same_session_cannot_switch_to_another_principals_scope(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        COMMIT;
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-b', 'grant-b-scope'
        );
        COMMIT;
        """,
        user="hcs_customer_a",
    )
    assert_sql_fails(result, "session_user", "principal", "scope", "grant")


def test_revocation_invalidates_next_transaction_on_same_physical_session(
    postgres_database: PostgresDatabase,
) -> None:
    # psql's shell escape launches the revoker while this exact authenticated
    # psql process remains alive, modelling a checked-in pooled connection.
    result = postgres_database.sql(
        rf"""
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        SELECT count(*) FROM xfactory_runtime_v2.artifact_records;
        COMMIT;
        \! PGPASSWORD="$POSTGRES_PASSWORD" psql -X -v ON_ERROR_STOP=1 -h 127.0.0.1 -U hcs_control_plane -d {postgres_database.name} -c "BEGIN; SELECT xfactory_runtime_api_v2.assume_scope('install-01', '', '', 'grant-control-scope'); SELECT xfactory_runtime_api_v2.revoke_authority_grant('revoke-a-scope', 'grant-a-scope', 'grant-control-revoke-scope', 'pooled-scope-test'); COMMIT"
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        SELECT count(*) FROM xfactory_runtime_v2.artifact_records;
        COMMIT;
        """,
        user="hcs_customer_a",
    )
    assert_sql_fails(result, "revoked", "grant", "scope", "authority")
    assert postgres_database.scalar("""
        SELECT count(*)
        FROM xfactory_runtime_v2.authority_grant_revocations
        WHERE revocation_id = 'revoke-a-scope'
          AND grant_id = 'grant-a-scope';
        """) == "1"
