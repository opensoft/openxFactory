"""RED real-PostgreSQL contracts for immutable topology lifecycle state."""

from __future__ import annotations

from pathlib import Path

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


def test_topology_tables_have_defensive_immutability_guards(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.file(_assertion("topology-catalog.sql"))
    assert_sql_succeeds(result)
    assert result.stdout.strip() == "t"


@pytest.mark.parametrize(
    "statement",
    [
        """
        UPDATE xfactory_runtime_v2.layer_registrations
        SET policy_namespace = 'stack-01.customer.rewritten'
        WHERE installation_id = 'install-01'
          AND stack_id = 'stack-01'
          AND layer_id = 'customer-a';
        """,
        """
        DELETE FROM xfactory_runtime_v2.layer_registrations
        WHERE installation_id = 'install-01'
          AND stack_id = 'stack-01'
          AND layer_id = 'customer-a';
        """,
        """
        UPDATE xfactory_runtime_v2.layer_lifecycle_events
        SET reason = 'rewritten-history'
        WHERE event_id = 'activate-a';
        """,
        """
        DELETE FROM xfactory_runtime_v2.layer_lifecycle_events
        WHERE event_id = 'activate-a';
        """,
    ],
    ids=[
        "registration-update",
        "registration-delete",
        "event-update",
        "event-delete",
    ],
)
def test_registration_and_event_history_rejects_direct_mutation_even_by_bootstrap(
    postgres_database: PostgresDatabase,
    statement: str,
) -> None:
    result = postgres_database.sql(statement)
    assert_sql_fails(result, "immutable", "append-only", "denied", "forbidden")


def test_lifecycle_projection_rejects_direct_mutation(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql("""
        UPDATE xfactory_runtime_v2.lifecycle_projections
        SET derived_state = 'retired'
        WHERE entity_kind = 'layer'
          AND installation_id = 'install-01'
          AND stack_id = 'stack-01'
          AND layer_id = 'customer-a';
        """)
    assert_sql_fails(result, "projection", "governed", "immutable", "denied")
    assert postgres_database.scalar("""
        SELECT derived_state
        FROM xfactory_runtime_v2.lifecycle_projections
        WHERE entity_kind = 'layer'
          AND installation_id = 'install-01'
          AND stack_id = 'stack-01'
          AND layer_id = 'customer-a';
        """) == "active"


def test_governed_transition_appends_event_and_projection_atomically(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', '', '', 'grant-control-scope'
        );
        SELECT xfactory_runtime_api_v2.transition_layer(
          'suspend-a', 'install-01', 'stack-01', 'customer-a', 'suspended',
          'grant-transition-a', 'incident-suspension'
        );
        COMMIT;
        """,
        user="hcs_control_plane",
    )
    assert_sql_succeeds(result)
    assert postgres_database.scalar("""
        SELECT
          (SELECT count(*) FROM xfactory_runtime_v2.layer_lifecycle_events
           WHERE event_id = 'suspend-a')::text
          || ':' ||
          (SELECT derived_state FROM xfactory_runtime_v2.lifecycle_projections
           WHERE entity_kind = 'layer'
             AND installation_id = 'install-01'
             AND stack_id = 'stack-01'
             AND layer_id = 'customer-a');
        """) == "1:suspended"


def test_stale_successor_and_transition_out_of_retired_fail_closed(
    postgres_database: PostgresDatabase,
) -> None:
    retired = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', '', '', 'grant-control-scope'
        );
        SELECT xfactory_runtime_api_v2.transition_layer(
          'retire-a', 'install-01', 'stack-01', 'customer-a', 'retired',
          'grant-transition-a', 'governed-retirement'
        );
        COMMIT;
        """,
        user="hcs_control_plane",
    )
    assert_sql_succeeds(retired)

    reversed_retirement = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', '', '', 'grant-control-scope'
        );
        SELECT xfactory_runtime_api_v2.transition_layer(
          'reactivate-a', 'install-01', 'stack-01', 'customer-a', 'active',
          'grant-transition-a', 'forbidden-reversal'
        );
        COMMIT;
        """,
        user="hcs_control_plane",
    )
    assert_sql_fails(
        reversed_retirement, "retired", "terminal", "transition", "lifecycle"
    )
    assert postgres_database.scalar("""
        SELECT derived_state
        FROM xfactory_runtime_v2.lifecycle_projections
        WHERE entity_kind = 'layer'
          AND installation_id = 'install-01'
          AND stack_id = 'stack-01'
          AND layer_id = 'customer-a';
        """) == "retired"
