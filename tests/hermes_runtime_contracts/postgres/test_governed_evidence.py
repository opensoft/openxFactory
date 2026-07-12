"""RED real-PostgreSQL contracts for artifacts, approvals, and traces."""

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


def _record_decision(
    database: PostgresDatabase,
    *,
    user: str,
    scope_grant: str,
    decision_id: str,
    decision: str,
    reviewer_grant: str,
) -> None:
    result = database.sql(
        f"""
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01',
          'customer-b',
          '{scope_grant}'
        );
        SELECT xfactory_runtime_api_v2.record_approval_decision(
          '{decision_id}', 'approval-b', '{decision}', '{reviewer_grant}'
        );
        COMMIT;
        """,
        user=user,
    )
    assert_sql_succeeds(result)


def _approval_authorizes(database: PostgresDatabase) -> str:
    result = database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-b', 'grant-b-scope'
        );
        SELECT xfactory_runtime_api_v2.approval_authorizes('approval-b');
        ROLLBACK;
        """,
        user="hcs_customer_b",
    )
    assert_sql_succeeds(result)
    return result.stdout.splitlines()[-1].strip()


def test_evidence_tables_have_defensive_append_only_guards(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.file(_assertion("evidence-immutability-catalog.sql"))
    assert_sql_succeeds(result)
    assert result.stdout.strip() == "t"


@pytest.mark.parametrize(
    "statement",
    [
        """
        UPDATE xfactory_runtime_v2.artifact_records
        SET media_type = 'application/octet-stream'
        WHERE artifact_id = 'artifact-a';
        """,
        """
        DELETE FROM xfactory_runtime_v2.approval_requests
        WHERE request_id = 'approval-b';
        """,
        """
        UPDATE xfactory_runtime_v2.approval_decision_policies
        SET minimum_approvals = 1
        WHERE policy_id = 'two-reviewer-policy';
        """,
        """
        DELETE FROM xfactory_runtime_v2.traceability_edges
        WHERE edge_id = 'trace-a-local';
        """,
    ],
    ids=["artifact", "approval-request", "decision-policy", "trace-edge"],
)
def test_artifact_approval_and_trace_records_are_immutable_even_to_bootstrap(
    postgres_database: PostgresDatabase,
    statement: str,
) -> None:
    result = postgres_database.sql(statement)
    assert_sql_fails(result, "immutable", "append-only", "denied", "forbidden")


def test_artifact_admission_derives_digest_size_and_scoped_storage_key(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        SELECT xfactory_runtime_api_v2.admit_artifact(
          'artifact-a-new', convert_to('new-artifact-body', 'UTF8'),
          'text/plain', 'grant-a-artifact-new'
        );
        SELECT content_digest || ':' || byte_size::text || ':' || storage_key
        FROM xfactory_runtime_v2.artifact_records
        WHERE artifact_id = 'artifact-a-new';
        COMMIT;
        """,
        user="hcs_customer_a",
    )
    assert_sql_succeeds(result)
    assert result.stdout.splitlines()[-1].strip() == (
        "sha256:480aa7aef6e198db395d4a678bd677aff5130f6fdb84a9e38075c355dc7ad0b6"
        ":17:install-01/customer-a/sha256/"
        "480aa7aef6e198db395d4a678bd677aff5130f6fdb84a9e38075c355dc7ad0b6"
    )


def test_cross_layer_artifact_probe_is_indistinguishable_from_missing(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        SELECT xfactory_runtime_api_v2.probe_artifact('artifact-b-draft')
             = xfactory_runtime_api_v2.probe_artifact('artifact-never-existed');
        ROLLBACK;
        """,
        user="hcs_customer_a",
    )
    assert_sql_succeeds(result)
    assert result.stdout.splitlines()[-1].strip() == "t"


def test_matching_two_reviewer_decisions_authorize_exact_target_digest(
    postgres_database: PostgresDatabase,
) -> None:
    _record_decision(
        postgres_database,
        user="hcs_reviewer_a",
        scope_grant="grant-review-a-scope",
        decision_id="decision-a-approve",
        decision="approve",
        reviewer_grant="grant-review-a-decide",
    )
    _record_decision(
        postgres_database,
        user="hcs_reviewer_b",
        scope_grant="grant-review-b-scope",
        decision_id="decision-b-approve",
        decision="approve",
        reviewer_grant="grant-review-b-decide",
    )
    assert _approval_authorizes(postgres_database) == "t"


def test_conflicting_terminal_decisions_remain_contested_and_nonauthorizing(
    postgres_database: PostgresDatabase,
) -> None:
    _record_decision(
        postgres_database,
        user="hcs_reviewer_a",
        scope_grant="grant-review-a-scope",
        decision_id="decision-a-approve",
        decision="approve",
        reviewer_grant="grant-review-a-decide",
    )
    _record_decision(
        postgres_database,
        user="hcs_reviewer_b",
        scope_grant="grant-review-b-scope",
        decision_id="decision-b-reject",
        decision="reject",
        reviewer_grant="grant-review-b-decide",
    )
    assert _approval_authorizes(postgres_database) == "f"


def test_artifact_body_is_reverified_after_approval_before_authorization(
    postgres_database: PostgresDatabase,
) -> None:
    _record_decision(
        postgres_database,
        user="hcs_reviewer_a",
        scope_grant="grant-review-a-scope",
        decision_id="decision-a-approve",
        decision="approve",
        reviewer_grant="grant-review-a-decide",
    )
    _record_decision(
        postgres_database,
        user="hcs_reviewer_b",
        scope_grant="grant-review-b-scope",
        decision_id="decision-b-approve",
        decision="approve",
        reviewer_grant="grant-review-b-decide",
    )
    drift = postgres_database.sql("""
        UPDATE xfactory_runtime_v2.artifact_bodies
        SET content = convert_to('customer-b-approved-body', 'UTF8'),
            content_digest = 'sha256:b745ff6cb7f92deb92d6c39ee9275edd8bba00155251573fd82fef99249cda32',
            byte_size = 24
        WHERE installation_id = 'install-01'
          AND stack_id = 'stack-01'
          AND layer_id = 'customer-b'
          AND artifact_id = 'artifact-b-draft';
        """)
    assert_sql_succeeds(drift)
    assert _approval_authorizes(postgres_database) == "f"


def test_approval_supersession_requires_exact_active_issuer_authority(
    postgres_database: PostgresDatabase,
) -> None:
    unauthorized = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-a', 'grant-a-scope'
        );
        SELECT xfactory_runtime_api_v2.supersede_approval(
          'supersede-unauthorized', 'approval-b', NULL, 'cancelled',
          'grant-a-project', 'wrong-layer-cancel'
        );
        COMMIT;
        """,
        user="hcs_customer_a",
    )
    assert_sql_fails(unauthorized, "authority", "grant", "scope", "issuer")

    authorized = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', 'stack-01', 'customer-b', 'grant-b-scope'
        );
        SELECT xfactory_runtime_api_v2.supersede_approval(
          'supersede-authorized', 'approval-b', NULL, 'cancelled',
          'grant-b-supersede', 'owner-cancel'
        );
        COMMIT;
        """,
        user="hcs_customer_b",
    )
    assert_sql_succeeds(authorized)
    assert postgres_database.scalar("""
        SELECT count(*)
        FROM xfactory_runtime_v2.approval_supersession_events
        WHERE event_id = 'supersede-authorized';
        """) == "1"
    assert _approval_authorizes(postgres_database) == "f"


def test_approval_decision_is_append_only_after_governed_insert(
    postgres_database: PostgresDatabase,
) -> None:
    _record_decision(
        postgres_database,
        user="hcs_reviewer_a",
        scope_grant="grant-review-a-scope",
        decision_id="decision-a-approve",
        decision="approve",
        reviewer_grant="grant-review-a-decide",
    )
    rewritten = postgres_database.sql("""
        UPDATE xfactory_runtime_v2.approval_decisions
        SET decision = 'reject'
        WHERE decision_id = 'decision-a-approve';
        """)
    assert_sql_fails(rewritten, "immutable", "append-only", "denied")


def test_cross_layer_operation_commits_target_authorization_and_trace_atomically(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', '', '', 'grant-control-scope'
        );
        SELECT xfactory_runtime_api_v2.project_artifact(
          'operation-success', 'binding-a-b', 'artifact-a',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'artifact-b-draft',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'grant-a-project',
          'trace-operation-success'
        );
        COMMIT;
        """,
        user="hcs_control_plane",
    )
    assert_sql_succeeds(result)
    assert postgres_database.scalar("""
        SELECT
          (SELECT count(*) FROM xfactory_runtime_v2.governed_projections
           WHERE operation_id = 'operation-success')::text || ':' ||
          (SELECT count(*) FROM xfactory_runtime_v2.operation_authorizations
           WHERE operation_id = 'operation-success')::text || ':' ||
          (SELECT count(*) FROM xfactory_runtime_v2.traceability_edges
           WHERE operation_id = 'operation-success')::text;
        """) == "1:1:1"


def test_failed_cross_layer_operation_rolls_back_every_authoritative_effect(
    postgres_database: PostgresDatabase,
) -> None:
    result = postgres_database.sql(
        """
        BEGIN;
        SELECT xfactory_runtime_api_v2.assume_scope(
          'install-01', '', '', 'grant-control-scope'
        );
        SELECT xfactory_runtime_api_v2.project_artifact(
          'operation-wrong-digest', 'binding-a-b', 'artifact-a',
          'sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
          'artifact-b-draft',
          'sha256:b6122b8c80d8845d1222fc3f280cea1587ec2af413417df2c082abc821343314',
          'grant-a-project',
          'trace-operation-wrong-digest'
        );
        COMMIT;
        """,
        user="hcs_control_plane",
    )
    assert_sql_fails(result, "digest", "resource", "binding", "authority")
    assert postgres_database.scalar("""
        SELECT
          (SELECT count(*) FROM xfactory_runtime_v2.governed_projections
           WHERE operation_id = 'operation-wrong-digest')::text || ':' ||
          (SELECT count(*) FROM xfactory_runtime_v2.operation_authorizations
           WHERE operation_id = 'operation-wrong-digest')::text || ':' ||
          (SELECT count(*) FROM xfactory_runtime_v2.traceability_edges
           WHERE operation_id = 'operation-wrong-digest')::text;
        """) == "0:0:0"
