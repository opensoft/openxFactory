"""RED real-PostgreSQL contracts for authorization/revocation races."""

from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from .conftest import (
    ISOLATION_ASSERTION_ROOT,
    PostgresDatabase,
    assert_sql_succeeds,
)

pytestmark = pytest.mark.postgres


def _sql(name: str) -> str:
    path = ISOLATION_ASSERTION_ROOT / name
    assert path.is_file(), path
    return path.read_text(encoding="utf-8")


def _assert_operation_race_outcome(
    database: PostgresDatabase,
    operation: subprocess.CompletedProcess[str],
) -> None:
    invariant = database.file(ISOLATION_ASSERTION_ROOT / "race-operation-invariant.sql")
    assert_sql_succeeds(invariant)
    counts = invariant.stdout.strip()
    if operation.returncode == 0:
        assert counts == "1:1:1"
    else:
        rendered = (operation.stdout + operation.stderr).lower()
        assert "deadlock" not in rendered
        assert "lock timeout" not in rendered
        assert any(
            fragment in rendered
            for fragment in ("revoked", "authority", "binding", "grant")
        ), rendered
        assert counts == "0:0:0"


def test_operation_vs_binding_revocation_has_only_two_atomic_outcomes(
    postgres_database: PostgresDatabase,
) -> None:
    operation, revocation = postgres_database.race(
        [
            ("hcs_control_plane", _sql("project-race.sql")),
            ("hcs_control_plane", _sql("revoke-binding-race.sql")),
        ]
    )
    assert_sql_succeeds(revocation)
    assert postgres_database.scalar("""
        SELECT count(*)
        FROM xfactory_runtime_v2.cross_layer_binding_revocations
        WHERE revocation_id = 'revoke-binding-race'
          AND binding_id = 'binding-a-b';
        """) == "1"
    _assert_operation_race_outcome(postgres_database, operation)


def test_operation_vs_grant_revocation_has_only_two_atomic_outcomes(
    postgres_database: PostgresDatabase,
) -> None:
    operation, revocation = postgres_database.race(
        [
            ("hcs_control_plane", _sql("project-race.sql")),
            ("hcs_control_plane", _sql("revoke-grant-race.sql")),
        ]
    )
    assert_sql_succeeds(revocation)
    assert postgres_database.scalar("""
        SELECT count(*)
        FROM xfactory_runtime_v2.authority_grant_revocations
        WHERE revocation_id = 'revoke-grant-race'
          AND grant_id = 'grant-a-project';
        """) == "1"
    _assert_operation_race_outcome(postgres_database, operation)


def test_grant_and_binding_revocations_share_canonical_deadlock_free_lock_order(
    postgres_database: PostgresDatabase,
) -> None:
    grant_revocation, binding_revocation = postgres_database.race(
        [
            ("hcs_control_plane", _sql("revoke-grant-race.sql")),
            ("hcs_control_plane", _sql("revoke-binding-race.sql")),
        ]
    )
    assert_sql_succeeds(grant_revocation)
    assert_sql_succeeds(binding_revocation)
    rendered = (
        grant_revocation.stdout
        + grant_revocation.stderr
        + binding_revocation.stdout
        + binding_revocation.stderr
    ).lower()
    assert "deadlock" not in rendered
    assert "lock timeout" not in rendered
    assert postgres_database.scalar("""
        SELECT
          (SELECT count(*)
           FROM xfactory_runtime_v2.authority_grant_revocations
           WHERE revocation_id = 'revoke-grant-race')::text || ':' ||
          (SELECT count(*)
           FROM xfactory_runtime_v2.cross_layer_binding_revocations
           WHERE revocation_id = 'revoke-binding-race')::text;
        """) == "1:1"
