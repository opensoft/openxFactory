"""RED real-PostgreSQL contracts for the legacy quarantine boundary.

T055: quarantined legacy evidence is preserved only as immutable closed
records inside the sealed ``xfactory_legacy_quarantine_v2`` schema. No
runtime, control, audit, or migrator principal reads it directly; no
authoritative foreign key, view, materialized view, or function may depend
on it; nothing promotes a quarantine row in place; and the only exit is a
new governed record created under current authority.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from .conftest import (
    MIGRATION_ASSERTION_ROOT,
    PostgresDatabase,
    assert_sql_fails,
    assert_sql_succeeds,
)

pytestmark = pytest.mark.postgres

QUARANTINE_TABLE = "xfactory_legacy_quarantine_v2.legacy_quarantine_records"

DEPENDENCY_REJECTION_FRAGMENTS = (
    "HGR-QUARANTINE-DEPENDENCY",
    "quarantine",
    "permission denied",
)
IMMUTABLE_FRAGMENTS = ("immutable", "append-only", "denied", "forbidden")
ACCESS_DENIED_FRAGMENTS = ("permission denied", "denied", "not permitted")


def _assertion(name: str) -> Path:
    return MIGRATION_ASSERTION_ROOT / name


def _seed_quarantine_rows(database: PostgresDatabase) -> None:
    """Seed two closed quarantine records directly as the bootstrap owner.

    Executed-migration provenance for quarantine content is covered by
    ``test_migration.py``; the boundary contracts below only need immutable
    rows to exist.
    """

    result = database.sql(f"""
        INSERT INTO {QUARANTINE_TABLE} (
          migration_id, source_schema, source_table, source_pk,
          source_row_digest, reason_code, source_row, captured_at
        ) VALUES
          ('migration-quarantine-01', 'public', 'hermes_approvals',
           '["approval-01"]',
           'sha256:1111111111111111111111111111111111111111111111111111111111111111',
           'missing_reviewer_authority',
           '{{"id": "approval-01", "decision": "approved"}}',
           '2026-07-01T00:00:00.000000Z'),
          ('migration-quarantine-01', 'public', 'hermes_job_artifacts',
           '["artifact-01"]',
           'sha256:2222222222222222222222222222222222222222222222222222222222222222',
           'missing_content_digest',
           '{{"id": "artifact-01", "sha256": null}}',
           '2026-07-01T00:00:00.000000Z');
        """)
    assert_sql_succeeds(result)


def test_quarantine_boundary_catalog_holds(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.file(_assertion("quarantine-boundary-catalog.sql"))
    assert_sql_succeeds(result)
    assert result.stdout.strip() == "t"


@pytest.mark.parametrize(
    "login",
    ["hcs_customer_a", "hcs_control_plane", "hcs_audit", "hcs_migrator", "hcs_unbound"],
)
def test_no_role_class_reads_quarantine_directly(
    postgres_database: PostgresDatabase, login: str
) -> None:
    _seed_quarantine_rows(postgres_database)
    result = postgres_database.sql(
        f"SELECT count(*) FROM {QUARANTINE_TABLE};", user=login
    )
    assert_sql_fails(result, *ACCESS_DENIED_FRAGMENTS)


def test_runtime_scope_cannot_reach_quarantine_even_after_assume_scope(
    postgres_database: PostgresDatabase,
) -> None:
    _seed_quarantine_rows(postgres_database)
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        SELECT count(*)
        FROM xfactory_legacy_quarantine_v2.legacy_quarantine_records;
        ROLLBACK;
        """,
        user="hcs_customer_a",
    )
    assert_sql_fails(result, *ACCESS_DENIED_FRAGMENTS)


@pytest.mark.parametrize(
    "statement",
    [
        (
            f"INSERT INTO {QUARANTINE_TABLE} (migration_id, source_schema,"
            " source_table, source_pk, source_row_digest, reason_code,"
            " source_row, captured_at) VALUES ('migration-probe', 'public',"
            " 'hermes_approvals', '[\"probe\"]',"
            " 'sha256:3333333333333333333333333333333333333333333333333333333333333333',"
            " 'missing_reviewer_authority', '{}',"
            " '2026-07-01T00:00:00.000000Z');"
        ),
        f"UPDATE {QUARANTINE_TABLE} SET reason_code = 'unverifiable_ancestry';",
        f"DELETE FROM {QUARANTINE_TABLE};",
    ],
    ids=["insert", "update", "delete"],
)
def test_runtime_login_cannot_write_quarantine(
    postgres_database: PostgresDatabase, statement: str
) -> None:
    _seed_quarantine_rows(postgres_database)
    result = postgres_database.sql(statement, user="hcs_customer_a")
    assert_sql_fails(result, *ACCESS_DENIED_FRAGMENTS)


@pytest.mark.parametrize(
    "statement",
    [
        (
            f"UPDATE {QUARANTINE_TABLE} SET source_row ="
            " jsonb_set(source_row, '{approval_state}', '\"approved\"')"
            " WHERE source_table = 'hermes_job_artifacts';"
        ),
        (
            f"UPDATE {QUARANTINE_TABLE} SET reason_code ="
            " 'unverifiable_ancestry' WHERE source_table = 'hermes_approvals';"
        ),
        f"DELETE FROM {QUARANTINE_TABLE} WHERE source_table = 'hermes_approvals';",
    ],
    ids=["promote-in-place", "reclassify", "delete"],
)
def test_quarantine_rows_are_immutable_even_to_bootstrap(
    postgres_database: PostgresDatabase, statement: str
) -> None:
    _seed_quarantine_rows(postgres_database)
    result = postgres_database.sql(statement)
    assert_sql_fails(result, *IMMUTABLE_FRAGMENTS)
    count = postgres_database.scalar(f"SELECT count(*) FROM {QUARANTINE_TABLE};")
    assert count == "2", "rejected mutations must leave the closed records intact"


@pytest.mark.parametrize(
    "ddl",
    [
        (
            "CREATE VIEW public.quarantine_probe_view AS"
            f" SELECT source_pk FROM {QUARANTINE_TABLE};"
        ),
        (
            "CREATE MATERIALIZED VIEW public.quarantine_probe_matview AS"
            f" SELECT source_pk FROM {QUARANTINE_TABLE};"
        ),
        (
            "CREATE TABLE public.quarantine_probe_fk ("
            "  migration_id text NOT NULL, source_schema text NOT NULL,"
            "  source_table text NOT NULL, source_pk text NOT NULL,"
            "  FOREIGN KEY (migration_id, source_schema, source_table,"
            "    source_pk) REFERENCES"
            f"  {QUARANTINE_TABLE}"
            "    (migration_id, source_schema, source_table, source_pk));"
        ),
        (
            "CREATE FUNCTION public.quarantine_probe_fn() RETURNS bigint"
            " LANGUAGE sql BEGIN ATOMIC"
            f" SELECT count(*) FROM {QUARANTINE_TABLE}; END;"
        ),
    ],
    ids=["view", "materialized-view", "foreign-key", "sql-function"],
)
def test_no_object_may_take_a_dependency_on_quarantine(
    postgres_database: PostgresDatabase, ddl: str
) -> None:
    _seed_quarantine_rows(postgres_database)
    result = postgres_database.sql(ddl)
    assert_sql_fails(result, *DEPENDENCY_REJECTION_FRAGMENTS)
    # The rejected DDL must leave no dependent object behind.
    leftovers = postgres_database.scalar(
        "SELECT (SELECT count(*) FROM pg_class"
        " WHERE relname LIKE 'quarantine_probe%')"
        " + (SELECT count(*) FROM pg_proc"
        " WHERE proname LIKE 'quarantine_probe%');"
    )
    assert leftovers == "0"


def test_dependency_guard_does_not_reject_unrelated_ddl(
    postgres_database: PostgresDatabase,
) -> None:
    _seed_quarantine_rows(postgres_database)
    result = postgres_database.sql("""
        CREATE VIEW public.legacy_history_probe_view AS
          SELECT source_pk FROM xfactory_runtime_v2.legacy_jobs;
        DROP VIEW public.legacy_history_probe_view;
        """)
    assert_sql_succeeds(result)


def test_quarantine_exit_is_a_new_governed_record_under_current_authority(
    postgres_database: PostgresDatabase,
) -> None:
    """No in-place promotion exists; the sanctioned exit re-creates content
    as a fresh governed artifact through the current authority chain, and the
    quarantine record stays byte-identical."""

    _seed_quarantine_rows(postgres_database)
    before = postgres_database.scalar(
        f"SELECT source_row_digest FROM {QUARANTINE_TABLE}"
        " WHERE source_table = 'hermes_job_artifacts';"
    )
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
    digest = postgres_database.scalar(
        "SELECT content_digest FROM xfactory_runtime_v2.artifact_records"
        " WHERE artifact_id = 'artifact-a-new';"
    )
    assert digest == (
        "sha256:480aa7aef6e198db395d4a678bd677aff5130f6fdb84a9e38075c355dc7ad0b6"
    ), "the exit path must mint a digest-bound governed record"
    after = postgres_database.scalar(
        f"SELECT source_row_digest FROM {QUARANTINE_TABLE}"
        " WHERE source_table = 'hermes_job_artifacts';"
    )
    assert after == before, "the quarantine record must remain a closed record"
