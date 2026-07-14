"""RED real-PostgreSQL contracts for migration recovery and convergence.

T054: the installation+migration-ID session advisory lock spans the attempt,
authoritative, and recovery transactions; pre-lock and post-lock concurrent
v1 writes are aborted or excluded by the proven cutover locks and the durable
write freeze; crash, abandon, and retry converge exactly once; a committed
success survives loss of the client acknowledgement as the stored result;
and replays with a changed payload, authority envelope, or logical boundary
fail closed while a changed physical snapshot after rollback converges.
"""

from __future__ import annotations

import copy
import json
import subprocess
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from scripts.hermes_runtime_validation import migration

from .conftest import (
    BASE_DATABASE,
    COMPOSE_FILE,
    ISOLATION_FIXTURE_ROOT,
    MIGRATION_ASSERTION_ROOT,
    MIGRATION_FIXTURE_ROOT,
    MIGRATION_SQL,
    REPOSITORY_ROOT,
    PostgresCluster,
    PostgresDatabase,
    assert_sql_fails,
    assert_sql_succeeds,
)

pytestmark = pytest.mark.postgres

MIGRATION_RUNNER = REPOSITORY_ROOT / "scripts/run-hermes-v1-to-v2-migration.sh"
TWO_SUBJECT_DATASET = MIGRATION_FIXTURE_ROOT / "v1-two-subject-dataset.yaml"
TWO_SUBJECT_SEED = MIGRATION_FIXTURE_ROOT / "10-v1-two-subject-seed.sql"
MIGRATION_AUTHORITY_SEED = MIGRATION_FIXTURE_ROOT / "30-migration-authority.sql"

# The twelve table locks must be top-level utility statements, in bytewise
# (schema, table) order, issued BEFORE the serializable snapshot is
# established (before the SELECT that calls execute_v1_cutover); the function
# itself only verifies they are pre-held (D11).
V1_LOCK_STATEMENT = """LOCK TABLE public.hermes_approval_requests IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_approvals IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_github_team_mappings IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_group_memberships IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_groups IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_job_artifacts IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_job_events IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_job_runs IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_jobs IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_profiles IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_traceability_edges IN SHARE ROW EXCLUSIVE MODE;
LOCK TABLE public.hermes_workers IN SHARE ROW EXCLUSIVE MODE;"""

# Value-for-value cell mirror of the racing INSERT used by the lock-wait
# regression test, in hermes_jobs schema ordinal order, so the re-staged
# mapping payload can bind the post-race logical boundary.
RACER_JOB_CELLS = [
    {"type": "text", "value": "job-racer"},
    {"type": "integer", "value": "1"},
    {"type": "text", "value": "Hermes"},
    {"type": "text", "value": "build"},
    {"type": "text", "value": "project-alfa"},
    {"type": None},
    {"type": None},
    {"type": "text", "value": "opensoft"},
    {"type": "text", "value": "repo-alfa"},
    {"type": "text", "value": "main"},
    {"type": "text", "value": "orchestrators/build.yaml"},
    {"type": "text", "value": "policies/routing.yaml"},
    {"type": "text", "value": "auth-profile-01"},
    {"type": "text", "value": "subscription"},
    {"type": "text", "value": "queued"},
    {"type": "json", "value": {}},
    {"type": "timestamp", "value": "2026-07-01T00:00:03.000000Z"},
    {"type": "timestamp", "value": "2026-07-01T00:00:03.000000Z"},
]

POLICY_REF = "policies/delegated.yaml"
POLICY_DIGEST = "sha256:d" + "0" * 63
SUBJECT_ALFA = {
    "kind": "software_project",
    "issuer": "example-domain",
    "namespace": "subjects",
    "ref": "urn:xfactory:subject:9f32f1de-82a7-4e38-a83d-9e5dd9189a11",
}
SUBJECT_BETA = {
    "kind": "software_project",
    "issuer": "example-domain",
    "namespace": "subjects",
    "ref": "urn:xfactory:subject:018f47a0-7b2c-7abc-8def-0123456789ab",
}
HISTORY_TABLES = (
    "legacy_jobs",
    "legacy_job_runs",
    "legacy_job_events",
    "legacy_workers",
    "legacy_groups",
    "legacy_profiles",
    "legacy_group_memberships",
    "legacy_github_team_mappings",
)
FROZEN_FRAGMENTS = ("frozen", "freeze", "denied", "forbidden")


def _assertion(name: str) -> Path:
    return MIGRATION_ASSERTION_ROOT / name


def _lock_expression(migration_id: str) -> str:
    return (
        "hashtextextended('xfactory-v1-to-v2-migration:' || 'install-01' || "
        f"E'\\n' || '{migration_id}', 0)"
    )


def _seed_migration_base(database: PostgresDatabase) -> None:
    for fixture in ("10-two-customer-topology.sql", "20-authority.sql"):
        assert_sql_succeeds(database.file(ISOLATION_FIXTURE_ROOT / fixture))
    assert_sql_succeeds(database.file(MIGRATION_AUTHORITY_SEED))


def _apply_migration_sql(database: PostgresDatabase) -> None:
    assert MIGRATION_SQL.is_file(), (
        "migration SQL is unavailable; RED boundary: " f"{MIGRATION_SQL}"
    )
    assert_sql_succeeds(database.file(MIGRATION_SQL, timeout=60))


def _cell_text(cell: dict) -> str:
    assert cell.get("type") is not None, "primary-key cells must not be null"
    value = cell["value"]
    assert isinstance(value, str), "v1 primary keys frame as text encodings"
    return value


def _pk_arrays(dataset: dict, table_name: str) -> list[str]:
    table = next(
        table for table in dataset["tables"] if table["table_name"] == table_name
    )
    key_ordinals = sorted(
        (column["primary_key_position"], index)
        for index, column in enumerate(table["columns"])
        if column["primary_key_position"] > 0
    )
    return sorted(
        migration.canonical_json_text(
            [_cell_text(row[index]) for _, index in key_ordinals]
        )
        for row in table["rows"]
    )


def _build_payload(
    dataset: dict,
    *,
    source_database: str,
    migration_id: str,
    subject_mappings: list[dict] | None = None,
) -> dict:
    payload = {
        "schema_version": 1,
        "kind": migration.MAPPING_PAYLOAD_KIND,
        "migration_id": migration_id,
        "installation_id": "install-01",
        "source_identity": {
            "source_database": source_database,
            "source_schema": "public",
        },
        "source_catalog": migration.catalog_from_dataset(dataset),
        "expected_table_row_counts": migration.table_row_counts(dataset),
        "expected_dataset_digest": migration.dataset_digest(dataset),
        "digest_profile": migration.DATASET_PROFILE,
        "subject_mappings": subject_mappings
        or [
            {
                "legacy_project": "project-alfa",
                "layer_id": "customer-a",
                "customer_subject": SUBJECT_ALFA,
            },
            {
                "legacy_project": "project-beta",
                "layer_id": "customer-b",
                "customer_subject": SUBJECT_BETA,
            },
        ],
        "admin_mappings": {
            collection: [
                {"source_pk": pk, "scope_kind": "installation_admin"}
                for pk in _pk_arrays(dataset, table_name)
            ]
            for collection, table_name in (
                ("workers", "hermes_workers"),
                ("groups", "hermes_groups"),
                ("profiles", "hermes_profiles"),
            )
        },
        "single_default_mapping": None,
        "target_topology": {
            "installation_id": "install-01",
            "stack_id": "stack-01",
            "client_layer_id": "client-01",
            "domain_layer_id": "domain-01",
            "customer_layer_ids": ["customer-a", "customer-b"],
        },
        "migration_policy": {
            "policy_ref": POLICY_REF,
            "policy_digest": POLICY_DIGEST,
        },
    }
    payload["mapping_payload_digest"] = migration.mapping_payload_digest(payload)
    return payload


def _mint_run_migration_grant(
    database: PostgresDatabase,
    *,
    grant_id: str,
    migration_id: str,
    payload_digest: str,
) -> str:
    """Mint an exact-resource run_migration grant and return the digest the
    database actually stored (the compute trigger derives it server-side)."""

    minted = database.sql(f"""
        INSERT INTO xfactory_runtime_v2.authority_grants (
          installation_id, grant_id, record_digest, digest_profile, grant_kind,
          grantee_stack_id, grantee_layer_id, grantee_principal_id,
          grantee_principal_digest, trust_anchor_id, trust_anchor_digest,
          issuer_grant_id, issuer_grant_digest, scope_kind, scope_stack_id,
          scope_layer_id, action, resource_type, resource_id, resource_digest,
          policy_repository, policy_commit, policy_ref, policy_digest,
          starts_at, expires_at, issued_at
        )
        SELECT
          'install-01', '{grant_id}', 'sha256:{"9" * 64}',
          'xfactory-canonical-json-v1', 'delegated',
          principal.stack_id, principal.layer_id, principal.principal_id,
          principal.record_digest, NULL, NULL,
          'grant-root-issue', issuer_grant.record_digest,
          'installation', '', '', 'run_migration', 'migration_mapping',
          '{migration_id}', '{payload_digest}',
          'opensoft/exampleFactory', 'dddddddddddddddddddddddddddddddddddddddd',
          '{POLICY_REF}', '{POLICY_DIGEST}',
          '2020-01-01T00:00:00Z'::timestamptz,
          '2099-01-01T00:00:00Z'::timestamptz,
          '2020-01-01T00:00:00Z'::timestamptz
        FROM xfactory_runtime_v2.principals principal
        JOIN xfactory_runtime_v2.authority_grants issuer_grant
          ON issuer_grant.installation_id = 'install-01'
         AND issuer_grant.grant_id = 'grant-root-issue'
        WHERE principal.installation_id = 'install-01'
          AND principal.principal_id = 'principal-migrator';
        """)
    assert_sql_succeeds(minted)
    return database.scalar(
        "SELECT record_digest FROM xfactory_runtime_v2.authority_grants "
        f"WHERE installation_id = 'install-01' AND grant_id = '{grant_id}';"
    )


def _staged_document(
    database: PostgresDatabase,
    *,
    migration_id: str,
    dataset: dict,
    source_database: str,
    grant_suffix: str = "01",
    subject_mappings: list[dict] | None = None,
) -> str:
    payload = _build_payload(
        dataset,
        source_database=source_database,
        migration_id=migration_id,
        subject_mappings=subject_mappings,
    )
    grant_id = f"grant-run-migration-{migration_id}-{grant_suffix}"
    grant_digest = _mint_run_migration_grant(
        database,
        grant_id=grant_id,
        migration_id=migration_id,
        payload_digest=payload["mapping_payload_digest"],
    )
    anchor_digest = database.scalar(
        "SELECT record_digest FROM xfactory_runtime_v2.installation_trust_anchors "
        "WHERE installation_id = 'install-01' AND anchor_id = 'anchor-01';"
    )
    envelope = {
        "schema_version": 1,
        "kind": migration.AUTHORITY_ENVELOPE_KIND,
        "migration_id": migration_id,
        "installation_id": "install-01",
        "mapping_payload_digest": payload["mapping_payload_digest"],
        "approver_principal_id": "principal-migrator",
        "run_migration_grant_id": grant_id,
        "run_migration_grant_digest": grant_digest,
        "policy_ref": POLICY_REF,
        "policy_digest": POLICY_DIGEST,
        "scope": {"installation_id": "install-01"},
        "trust_anchor_id": "anchor-01",
        "trust_anchor_digest": anchor_digest,
        "approved_at": "2026-07-12T12:00:00Z",
    }
    envelope["authority_envelope_digest"] = migration.authority_envelope_digest(
        envelope
    )
    return migration.build_staging_document(payload, envelope)


def _psql_template(cluster: PostgresCluster) -> str:
    return (
        f"docker compose --file {COMPOSE_FILE} "
        f"--project-name {cluster.project_name} "
        "exec -T postgres psql -X -q -A -t -v ON_ERROR_STOP=1 "
        "-U hcs_migrator -d {database}"
    )


def _run_runner(
    database: PostgresDatabase, staging_path: Path, migration_id: str
) -> subprocess.CompletedProcess[str]:
    assert MIGRATION_RUNNER.is_file(), (
        "migration runner is unavailable; RED boundary: " f"{MIGRATION_RUNNER}"
    )
    cluster = database.cluster
    return cluster.run_subprocess(
        [
            "sh",
            str(MIGRATION_RUNNER),
            "--database",
            database.name,
            "--staging-file",
            str(staging_path),
            "--installation-id",
            "install-01",
            "--migration-id",
            migration_id,
        ],
        cwd=REPOSITORY_ROOT,
        env={
            **cluster.environment,
            "HERMES_MIGRATION_PSQL_COMMAND": _psql_template(cluster),
        },
        timeout=300,
    )


def _stage_and_begin(database: PostgresDatabase, staging_text: str, mid: str) -> None:
    """Stage and open the STARTED attempt in one locked committed transaction.

    The session (and therefore its advisory lock) ends with the script; the
    committed STARTED event survives for a later session to recover.
    """

    result = database.sql(
        f"""
        SELECT pg_advisory_lock({_lock_expression(mid)});
        BEGIN;
        SELECT xfactory_runtime_api_v2.stage_migration(
          $hcs_recovery${staging_text}$hcs_recovery$::jsonb);
        SELECT xfactory_runtime_api_v2.begin_migration_attempt(
          'install-01', '{mid}');
        COMMIT;
        """,
        user="hcs_migrator",
    )
    assert_sql_succeeds(result)


def _count(database: PostgresDatabase, statement: str) -> int:
    return int(database.scalar(statement))


def _event_count(database: PostgresDatabase, mid: str, event_type: str) -> int:
    return _count(
        database,
        "SELECT count(*) FROM xfactory_runtime_v2.migration_attempt_events "
        f"WHERE migration_id = '{mid}' AND event_type = '{event_type}';",
    )


def _classified_counts(database: PostgresDatabase, mid: str) -> tuple[int, int]:
    history = sum(
        _count(
            database,
            f"SELECT count(*) FROM xfactory_runtime_v2.{table} "
            f"WHERE migration_id = '{mid}';",
        )
        for table in HISTORY_TABLES
    )
    quarantined = _count(
        database,
        "SELECT count(*) FROM "
        "xfactory_legacy_quarantine_v2.legacy_quarantine_records "
        f"WHERE migration_id = '{mid}';",
    )
    return history, quarantined


def _assert_assertions_hold(database: PostgresDatabase, *names: str) -> None:
    for name in names:
        result = database.file(_assertion(name))
        assert_sql_succeeds(result)
        assert result.stdout.strip() == "t", name


def _write_staging(tmp_path: Path, staging_text: str, name: str) -> Path:
    staging_path = tmp_path / name
    staging_path.write_text(staging_text, encoding="utf-8")
    return staging_path


class TestSessionLock:
    def test_migration_ledger_catalog_holds(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        _seed_migration_base(postgres_v1_database)
        _apply_migration_sql(postgres_v1_database)
        _assert_assertions_hold(postgres_v1_database, "migration-ledger-catalog.sql")

    def test_attempt_and_recovery_apis_require_the_session_lock(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        _apply_migration_sql(database)
        assert_sql_succeeds(database.file(TWO_SUBJECT_SEED))
        dataset = migration.load_dataset_description(TWO_SUBJECT_DATASET)
        mid = "migration-lock-required-01"
        staging_text = _staged_document(
            database,
            migration_id=mid,
            dataset=dataset,
            source_database=database.name,
        )
        # Staging validates content and authority; it does not require the
        # session lock. Every attempt/recovery transition does.
        assert_sql_succeeds(
            database.sql(
                "SELECT xfactory_runtime_api_v2.stage_migration("
                f"$hcs_recovery${staging_text}$hcs_recovery$::jsonb);",
                user="hcs_migrator",
            )
        )
        unlocked_begin = database.sql(
            "SELECT xfactory_runtime_api_v2.begin_migration_attempt("
            f"'install-01', '{mid}');",
            user="hcs_migrator",
        )
        assert_sql_fails(unlocked_begin, "HGR-MIGRATION-LOCK-NOT-HELD", "lock")
        unlocked_fail = database.sql(
            "SELECT xfactory_runtime_api_v2.fail_migration_attempt("
            f"'install-01', '{mid}', '{mid}-attempt-1', 'probe');",
            user="hcs_migrator",
        )
        assert_sql_fails(unlocked_fail, "HGR-MIGRATION-LOCK-NOT-HELD", "lock")
        unlocked_cutover = database.sql(
            f"""
            BEGIN ISOLATION LEVEL SERIALIZABLE;
            SELECT xfactory_runtime_api_v2.execute_v1_cutover(
              'install-01', '{mid}', '{mid}-attempt-1');
            ROLLBACK;
            """,
            user="hcs_migrator",
        )
        assert_sql_fails(unlocked_cutover, "HGR-MIGRATION-LOCK-NOT-HELD", "lock")
        assert _event_count(database, mid, "started") == 0

    def test_session_lock_is_exclusive_per_installation_and_migration_id(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        same_key = (
            f"SELECT pg_try_advisory_lock({_lock_expression('migration-race-01')});\n"
            "SELECT pg_sleep(1.5);\n"
            "SELECT pg_advisory_unlock_all();"
        )
        outcomes = database.race(
            [("hermes_runtime", same_key), ("hermes_runtime", same_key)]
        )
        acquired = []
        for outcome in outcomes:
            assert outcome.returncode == 0, outcome.stderr
            acquired.append(outcome.stdout.strip().splitlines()[0].strip())
        assert sorted(acquired) == ["f", "t"], (
            "exactly one concurrent session may hold the installation+"
            f"migration-id lock: {acquired}"
        )

        different_key = (
            f"SELECT pg_try_advisory_lock({_lock_expression('migration-race-02')});\n"
            "SELECT pg_sleep(0.5);\n"
            "SELECT pg_advisory_unlock_all();"
        )
        other_key = (
            f"SELECT pg_try_advisory_lock({_lock_expression('migration-race-03')});\n"
            "SELECT pg_sleep(0.5);\n"
            "SELECT pg_advisory_unlock_all();"
        )
        outcomes = database.race(
            [("hermes_runtime", different_key), ("hermes_runtime", other_key)]
        )
        for outcome in outcomes:
            assert outcome.returncode == 0, outcome.stderr
            assert (
                outcome.stdout.strip().splitlines()[0].strip() == "t"
            ), "distinct migration ids must not contend for one lock"


class TestConcurrentRunners:
    """Two whole runner processes contend for one installation+migration id.

    Lock exclusivity and the lock-not-held guard are proven at the SQL level in
    ``TestSessionLock``; this is the end-to-end companion (F-4): two concurrent
    invocations of ``scripts/run-hermes-v1-to-v2-migration.sh`` against the SAME
    installation+migration id must resolve to exactly one ``succeeded`` (exit 0,
    a single SUCCEEDED ledger event, reconciliation intact) and one clean
    ``lock-unavailable`` (exit 1) that opens no attempt and leaves zero state.

    The race is sequenced deterministically rather than by sleeping. A blocker
    transaction pre-holds the first v1 table lock the winner takes (bytewise
    order -> ``public.hermes_approval_requests``). The winner acquires the
    session advisory lock, commits its STARTED attempt, then parks on that
    ``LOCK TABLE``; reaching that wait is the proof it already holds the advisory
    lock. The loser is launched only after the winner is confirmed parked, so
    its ``pg_try_advisory_lock`` provably fails; the blocker is released only
    after the loser has recorded its clean lock-unavailable outcome.
    """

    _BLOCKED_TABLE = "hermes_approval_requests"

    def _share_row_exclusive_locks(
        self, database: PostgresDatabase, *, granted: bool
    ) -> int:
        return _count(
            database,
            "SELECT count(*) FROM pg_locks lock_row "
            "JOIN pg_class rel ON rel.oid = lock_row.relation "
            "JOIN pg_namespace ns ON ns.oid = rel.relnamespace "
            "WHERE ns.nspname = 'public' "
            f"AND rel.relname = '{self._BLOCKED_TABLE}' "
            "AND lock_row.mode = 'ShareRowExclusiveLock' "
            f"AND lock_row.granted IS {'true' if granted else 'false'};",
        )

    def _poll_until(self, predicate: Callable[[], bool], *, message: str) -> None:
        for _ in range(120):
            if predicate():
                return
            time.sleep(0.25)
        raise AssertionError(message)

    def test_two_runners_resolve_to_one_success_and_one_lock_unavailable(
        self, postgres_v1_database: PostgresDatabase, tmp_path: Path
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        _apply_migration_sql(database)
        assert_sql_succeeds(database.file(TWO_SUBJECT_SEED))
        dataset = migration.load_dataset_description(TWO_SUBJECT_DATASET)
        mid = "migration-two-runner-01"
        staging_text = _staged_document(
            database,
            migration_id=mid,
            dataset=dataset,
            source_database=database.name,
        )
        staging_path = _write_staging(tmp_path, staging_text, "staging.json")

        # The blocker holds the first v1 table lock the winning runner takes.
        # It never mutates a row (a bare LOCK TABLE, then it waits), so on
        # release the approved logical boundary is still exact.
        app_name = f"f4-blocker-{mid}"
        blocker_sql = f"""
SET application_name = '{app_name}';
BEGIN;
LOCK TABLE public.{self._BLOCKED_TABLE} IN SHARE ROW EXCLUSIVE MODE;
SELECT pg_sleep(120);
COMMIT;
"""
        release_sql = (
            "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
            f"WHERE application_name = '{app_name}' AND pid <> pg_backend_pid();"
        )

        with ThreadPoolExecutor(max_workers=2) as executor:
            blocker_future = executor.submit(
                database.sql, blocker_sql, user="hcs_migrator", timeout=180
            )
            self._poll_until(
                lambda: self._share_row_exclusive_locks(database, granted=True) >= 1,
                message="blocker never acquired the SHARE ROW EXCLUSIVE table lock",
            )

            winner_future = executor.submit(_run_runner, database, staging_path, mid)
            # Parking on the pre-held table lock proves the winner already holds
            # the session advisory lock and committed exactly one STARTED attempt.
            self._poll_until(
                lambda: self._share_row_exclusive_locks(database, granted=False) >= 1,
                message="winning runner never parked on the pre-held v1 table lock",
            )
            assert (
                _event_count(database, mid, "started") == 1
            ), "the parked winner must have committed exactly one STARTED attempt"

            # The loser races the SAME installation+migration id while the winner
            # holds the advisory lock: its pg_try_advisory_lock fails at once.
            loser = _run_runner(database, staging_path, mid)
            assert loser.returncode == 1, f"{loser.stdout}\n{loser.stderr}"
            assert "outcome=lock-unavailable" in loser.stdout
            # The loser quit before staging: it opened no attempt and wrote no
            # v2 state; the winner's single STARTED attempt is untouched.
            assert _event_count(database, mid, "started") == 1
            assert _classified_counts(database, mid) == (0, 0)

            # Release the blocker; the winner takes the twelve locks and converges.
            terminated = database.scalar(release_sql)
            assert terminated == "t", terminated
            winner = winner_future.result(timeout=300)
            blocker_future.result(timeout=60)

        assert winner.returncode == 0, f"{winner.stdout}\n{winner.stderr}"
        assert "outcome=succeeded" in winner.stdout

        # Exactly one attempt reached a terminal SUCCEEDED, with no FAILED or
        # ABANDONED sibling, and reconciliation is complete and exactly-once.
        assert _event_count(database, mid, "started") == 1
        assert _event_count(database, mid, "succeeded") == 1
        assert _event_count(database, mid, "failed") == 0
        assert _event_count(database, mid, "abandoned") == 0
        counts = migration.table_row_counts(dataset)
        history, quarantined = _classified_counts(database, mid)
        assert history + quarantined == sum(counts.values())
        _assert_assertions_hold(
            database,
            "migration-event-chain-invariant.sql",
            "migration-reconciliation-invariant.sql",
            "migration-freeze-catalog.sql",
        )


class TestConcurrentV1Writes:
    def test_pre_lock_write_aborts_cleanly_and_unchanged_boundary_retry_converges(
        self, postgres_v1_database: PostgresDatabase, tmp_path: Path
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        _apply_migration_sql(database)
        assert_sql_succeeds(database.file(TWO_SUBJECT_SEED))
        dataset = migration.load_dataset_description(TWO_SUBJECT_DATASET)
        mid = "migration-prelock-01"
        staging_text = _staged_document(
            database,
            migration_id=mid,
            dataset=dataset,
            source_database=database.name,
        )
        staging_path = _write_staging(tmp_path, staging_text, "staging.json")

        # A governed v1 write lands after payload approval and before the
        # migration session takes its locks: the observed logical boundary
        # no longer matches the approved one.
        assert_sql_succeeds(
            database.sql(
                "INSERT INTO public.hermes_groups (id, purpose) "
                "VALUES ('group-racer', 'pre-lock write');"
            )
        )
        first = _run_runner(database, staging_path, mid)
        assert first.returncode == 1, f"{first.stdout}\n{first.stderr}"
        assert "outcome=attempt-failed" in first.stdout
        assert _event_count(database, mid, "failed") == 1
        assert _classified_counts(database, mid) == (
            0,
            0,
        ), "an aborted cutover must leave no partial v2 state"
        # No freeze was installed by the failed attempt: v1 stays writable.
        assert_sql_succeeds(
            database.sql("DELETE FROM public.hermes_groups WHERE id = 'group-racer';")
        )

        # Content is back on the approved logical boundary; the retry runs in
        # a new transaction (a different physical snapshot) and converges.
        second = _run_runner(database, staging_path, mid)
        assert second.returncode == 0, f"{second.stdout}\n{second.stderr}"
        assert "outcome=succeeded" in second.stdout
        assert _event_count(database, mid, "succeeded") == 1
        assert _event_count(database, mid, "failed") == 1
        counts = migration.table_row_counts(dataset)
        history, quarantined = _classified_counts(database, mid)
        assert history + quarantined == sum(counts.values())
        _assert_assertions_hold(
            database,
            "migration-event-chain-invariant.sql",
            "migration-reconciliation-invariant.sql",
            "migration-freeze-catalog.sql",
        )
        expected_boundary = migration.logical_boundary_id(
            source_identity={
                "source_database": database.name,
                "source_schema": "public",
            },
            catalog=migration.catalog_from_dataset(dataset),
            table_row_counts=counts,
            dataset_digest=migration.dataset_digest(dataset),
        )
        stored_boundary = database.scalar(
            "SELECT logical_boundary_id "
            "FROM xfactory_runtime_v2.migration_cutover_observations "
            "WHERE attempt_id = ("
            "  SELECT attempt_id FROM xfactory_runtime_v2.migration_attempt_events"
            f"  WHERE migration_id = '{mid}' AND event_type = 'succeeded');"
        )
        assert (
            stored_boundary == expected_boundary
        ), "the converged retry must bind the unchanged approved boundary"

    def test_post_lock_write_is_excluded_by_cutover_locks_and_durable_freeze(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        _apply_migration_sql(database)
        assert_sql_succeeds(database.file(TWO_SUBJECT_SEED))
        dataset = migration.load_dataset_description(TWO_SUBJECT_DATASET)
        mid = "migration-postlock-01"
        staging_text = _staged_document(
            database,
            migration_id=mid,
            dataset=dataset,
            source_database=database.name,
        )
        _stage_and_begin(database, staging_text, mid)

        cutover_session = f"""
SET lock_timeout = '30s';
SET statement_timeout = '40s';
SELECT pg_advisory_lock({_lock_expression(mid)});
BEGIN ISOLATION LEVEL SERIALIZABLE;
{V1_LOCK_STATEMENT}
SELECT xfactory_runtime_api_v2.execute_v1_cutover(
  'install-01', '{mid}', '{mid}-attempt-1');
SELECT pg_sleep(3);
COMMIT;
SELECT pg_advisory_unlock_all();
"""
        racing_write = """
SET lock_timeout = '30s';
SET statement_timeout = '40s';
SELECT pg_sleep(1.2);
INSERT INTO public.hermes_jobs (
  id, schema_version, issued_by, job_type, project, feature_id, epic_id,
  repository_org, repository_name, repository_default_branch,
  orchestrator_path, routing_policy_path, auth_profile_id, auth_mode,
  status, envelope, created_at, updated_at
) VALUES (
  'job-racer', 1, 'Hermes', 'build', 'project-alfa', NULL, NULL,
  'opensoft', 'repo-alfa', 'main', 'orchestrators/build.yaml',
  'policies/routing.yaml', 'auth-profile-01', 'subscription', 'queued',
  '{}', '2026-07-01T00:00:03.000000Z', '2026-07-01T00:00:03.000000Z'
);
"""
        cutover_result, write_result = database.race(
            [("hcs_migrator", cutover_session), ("hermes_runtime", racing_write)],
            timeout=60,
        )
        assert (
            cutover_result.returncode == 0
        ), f"{cutover_result.stdout}\n{cutover_result.stderr}"
        rendered = "\n".join(
            part for part in (cutover_result.stdout, cutover_result.stderr) if part
        )
        assert '"status": "succeeded"' in rendered
        assert_sql_fails(write_result, *FROZEN_FRAGMENTS)
        assert (
            database.scalar(
                "SELECT count(*) FROM public.hermes_jobs WHERE id = 'job-racer';"
            )
            == "0"
        ), "the blocked write must be excluded, not applied after cutover"
        assert (
            database.scalar(
                "SELECT count(*) FROM xfactory_runtime_v2.legacy_jobs "
                f"WHERE migration_id = '{mid}' "
                "AND source_pk = '[\"job-racer\"]';"
            )
            == "0"
        ), "no ledger entry may cite the excluded write"
        counts = migration.table_row_counts(dataset)
        history, quarantined = _classified_counts(database, mid)
        assert history + quarantined == sum(counts.values())
        _assert_assertions_hold(database, "migration-freeze-catalog.sql")

    def test_cutover_requires_preheld_v1_table_locks(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        """The cutover function never takes the twelve table locks itself: a
        lock acquired inside the function would follow the transaction
        snapshot and re-create the lock-wait stranding race. A session that
        holds the advisory lock and an open started attempt but skipped the
        top-level LOCK statements must fail closed BEFORE any governed
        source read, with the stable finding code."""
        database = postgres_v1_database
        _seed_migration_base(database)
        _apply_migration_sql(database)
        assert_sql_succeeds(database.file(TWO_SUBJECT_SEED))
        dataset = migration.load_dataset_description(TWO_SUBJECT_DATASET)
        mid = "migration-nopreheld-01"
        staging_text = _staged_document(
            database,
            migration_id=mid,
            dataset=dataset,
            source_database=database.name,
        )
        _stage_and_begin(database, staging_text, mid)

        unlocked_session = f"""
SELECT pg_advisory_lock({_lock_expression(mid)});
BEGIN ISOLATION LEVEL SERIALIZABLE;
SELECT xfactory_runtime_api_v2.execute_v1_cutover(
  'install-01', '{mid}', '{mid}-attempt-1');
COMMIT;
"""
        rejected = database.sql(unlocked_session, user="hcs_migrator")
        assert_sql_fails(rejected, "HGR-MIGRATION-V1-LOCKS-NOT-PREHELD")
        assert _event_count(database, mid, "succeeded") == 0
        assert _classified_counts(database, mid) == (
            0,
            0,
        ), "the lock-verify guard must fail closed without partial v2 state"
        # No freeze was installed by the rejected attempt: v1 stays writable.
        assert_sql_succeeds(
            database.sql(
                "INSERT INTO public.hermes_groups (id, purpose) "
                "VALUES ('group-nopreheld-probe', 'probe');"
            )
        )

    def test_write_committing_during_lock_wait_aborts_cutover(
        self, postgres_v1_database: PostgresDatabase, tmp_path: Path
    ) -> None:
        """A v1 write that starts before the cutover's table locks and commits
        while the cutover blocks on them must be observed by the boundary
        check, never stranded in a frozen table behind a SUCCEEDED ledger.
        The serializable snapshot is only taken after the top-level LOCK
        statements, so the committed racer row is visible and the observed
        boundary diverges from the approved payload. A re-staged mapping
        payload that binds the post-race boundary then converges and counts
        the racer row (F-P1 regression, D11)."""
        database = postgres_v1_database
        _seed_migration_base(database)
        _apply_migration_sql(database)
        assert_sql_succeeds(database.file(TWO_SUBJECT_SEED))
        dataset = migration.load_dataset_description(TWO_SUBJECT_DATASET)
        mid = "migration-lockwait-01"
        staging_text = _staged_document(
            database,
            migration_id=mid,
            dataset=dataset,
            source_database=database.name,
        )
        _stage_and_begin(database, staging_text, mid)

        # The writer holds an uncommitted insert when the cutover statement
        # begins, so the cutover blocks on LOCK TABLE; the writer then commits
        # while the cutover is still waiting for the lock.
        racing_write = """
SET lock_timeout = '30s';
SET statement_timeout = '40s';
BEGIN;
INSERT INTO public.hermes_jobs (
  id, schema_version, issued_by, job_type, project, feature_id, epic_id,
  repository_org, repository_name, repository_default_branch,
  orchestrator_path, routing_policy_path, auth_profile_id, auth_mode,
  status, envelope, created_at, updated_at
) VALUES (
  'job-racer', 1, 'Hermes', 'build', 'project-alfa', NULL, NULL,
  'opensoft', 'repo-alfa', 'main', 'orchestrators/build.yaml',
  'policies/routing.yaml', 'auth-profile-01', 'subscription', 'queued',
  '{}', '2026-07-01T00:00:03.000000Z', '2026-07-01T00:00:03.000000Z'
);
SELECT pg_sleep(3);
COMMIT;
"""
        cutover_session = f"""
SET lock_timeout = '30s';
SET statement_timeout = '40s';
SELECT pg_sleep(1.2);
SELECT pg_advisory_lock({_lock_expression(mid)});
BEGIN ISOLATION LEVEL SERIALIZABLE;
{V1_LOCK_STATEMENT}
SELECT xfactory_runtime_api_v2.execute_v1_cutover(
  'install-01', '{mid}', '{mid}-attempt-1');
COMMIT;
SELECT pg_advisory_unlock_all();
"""
        write_result, cutover_result = database.race(
            [("hermes_runtime", racing_write), ("hcs_migrator", cutover_session)],
            timeout=60,
        )
        assert_sql_succeeds(write_result)
        assert_sql_fails(cutover_result, "HGR-MIGRATION-BOUNDARY-MISMATCH")

        fail_session = f"""
SELECT pg_advisory_lock({_lock_expression(mid)});
SELECT xfactory_runtime_api_v2.fail_migration_attempt(
  'install-01', '{mid}', '{mid}-attempt-1', 'boundary drift during lock wait');
SELECT pg_advisory_unlock_all();
"""
        assert_sql_succeeds(database.sql(fail_session, user="hcs_migrator"))
        assert _event_count(database, mid, "succeeded") == 0, (
            "no SUCCEEDED ledger may be produced for the raced attempt: it "
            "would omit the committed racer row"
        )
        assert _event_count(database, mid, "failed") == 1
        assert _classified_counts(database, mid) == (
            0,
            0,
        ), "the aborted cutover must leave no partial v2 state"
        assert (
            database.scalar(
                "SELECT count(*) FROM public.hermes_jobs WHERE id = 'job-racer';"
            )
            == "1"
        ), "the racing write committed and must remain in the source table"

        # A retry with a RE-STAGED mapping payload binding the post-race
        # logical boundary (racer row included) converges and counts the row:
        # nothing is stranded outside the ledger. The failed migration id
        # stays bound to its old payload digest, so the re-staged document
        # runs under a fresh migration id.
        racer_dataset = copy.deepcopy(dataset)
        racer_table = next(
            table
            for table in racer_dataset["tables"]
            if table["table_name"] == "hermes_jobs"
        )
        racer_table["rows"].append(copy.deepcopy(RACER_JOB_CELLS))
        restaged_mid = "migration-lockwait-02"
        restaged_text = _staged_document(
            database,
            migration_id=restaged_mid,
            dataset=racer_dataset,
            source_database=database.name,
        )
        restaged_path = _write_staging(tmp_path, restaged_text, "restaged.json")
        retry = _run_runner(database, restaged_path, restaged_mid)
        assert retry.returncode == 0, f"{retry.stdout}\n{retry.stderr}"
        assert "outcome=succeeded" in retry.stdout
        assert _event_count(database, restaged_mid, "succeeded") == 1
        counts = migration.table_row_counts(racer_dataset)
        history, quarantined = _classified_counts(database, restaged_mid)
        assert history + quarantined == sum(counts.values())
        assert (
            database.scalar(
                "SELECT count(*) FROM xfactory_runtime_v2.legacy_jobs "
                f"WHERE migration_id = '{restaged_mid}' "
                "AND source_pk = '[\"job-racer\"]';"
            )
            == "1"
        ), "the successful ledger must count the racer row, never strand it"
        _assert_assertions_hold(database, "migration-freeze-catalog.sql")


class TestReplayRejection:
    def test_changed_payload_or_envelope_replay_after_success_fails_closed(
        self, postgres_v1_database: PostgresDatabase, tmp_path: Path
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        _apply_migration_sql(database)
        assert_sql_succeeds(database.file(TWO_SUBJECT_SEED))
        dataset = migration.load_dataset_description(TWO_SUBJECT_DATASET)
        mid = "migration-replay-01"
        staging_text = _staged_document(
            database,
            migration_id=mid,
            dataset=dataset,
            source_database=database.name,
        )
        staging_path = _write_staging(tmp_path, staging_text, "staging.json")
        first = _run_runner(database, staging_path, mid)
        assert first.returncode == 0, f"{first.stdout}\n{first.stderr}"

        changed_payload = _staged_document(
            database,
            migration_id=mid,
            dataset=dataset,
            source_database=database.name,
            grant_suffix="02",
            subject_mappings=[
                {
                    "legacy_project": "project-alfa",
                    "layer_id": "customer-b",
                    "customer_subject": SUBJECT_BETA,
                },
                {
                    "legacy_project": "project-beta",
                    "layer_id": "customer-a",
                    "customer_subject": SUBJECT_ALFA,
                },
            ],
        )
        changed_path = _write_staging(tmp_path, changed_payload, "changed.json")
        replay = _run_runner(database, changed_path, mid)
        assert replay.returncode == 1, f"{replay.stdout}\n{replay.stderr}"
        assert "outcome=staging-rejected" in replay.stdout

        # Same payload bytes, different authority envelope: equally rejected.
        envelope_only = _staged_document(
            database,
            migration_id=mid,
            dataset=dataset,
            source_database=database.name,
            grant_suffix="03",
        )
        envelope_path = _write_staging(tmp_path, envelope_only, "envelope.json")
        envelope_replay = _run_runner(database, envelope_path, mid)
        assert (
            envelope_replay.returncode == 1
        ), f"{envelope_replay.stdout}\n{envelope_replay.stderr}"
        assert "outcome=staging-rejected" in envelope_replay.stdout

        assert _event_count(database, mid, "succeeded") == 1
        counts = migration.table_row_counts(dataset)
        history, quarantined = _classified_counts(database, mid)
        assert history + quarantined == sum(
            counts.values()
        ), "rejected replays must not reapply or duplicate rows"

    def test_authority_revoked_between_staging_and_cutover_fails_the_attempt(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        _apply_migration_sql(database)
        assert_sql_succeeds(database.file(TWO_SUBJECT_SEED))
        dataset = migration.load_dataset_description(TWO_SUBJECT_DATASET)
        mid = "migration-revoked-01"
        staging_text = _staged_document(
            database,
            migration_id=mid,
            dataset=dataset,
            source_database=database.name,
        )
        _stage_and_begin(database, staging_text, mid)

        grant_id = f"grant-run-migration-{mid}-01"
        revoked = database.sql(f"""
            INSERT INTO xfactory_runtime_v2.authority_grant_revocations (
              installation_id, revocation_id, record_digest, grant_id,
              grant_digest, revoker_grant_id, reason, effective_at
            )
            SELECT 'install-01', 'revocation-{grant_id}',
                   'sha256:{"8" * 64}', grant_id, record_digest,
                   'grant-root-issue', 'revoked before cutover',
                   '2020-01-02T00:00:00Z'::timestamptz
            FROM xfactory_runtime_v2.authority_grants
            WHERE installation_id = 'install-01' AND grant_id = '{grant_id}';
            """)
        assert_sql_succeeds(revoked)

        recovery_session = f"""
SELECT pg_advisory_lock({_lock_expression(mid)});
BEGIN ISOLATION LEVEL SERIALIZABLE;
{V1_LOCK_STATEMENT}
SELECT xfactory_runtime_api_v2.execute_v1_cutover(
  'install-01', '{mid}', '{mid}-attempt-1');
COMMIT;
"""
        rejected = database.sql(recovery_session, user="hcs_migrator")
        assert_sql_fails(rejected, "authority", "revoked", "HGR-MIGRATION")

        fail_session = f"""
SELECT pg_advisory_lock({_lock_expression(mid)});
SELECT xfactory_runtime_api_v2.fail_migration_attempt(
  'install-01', '{mid}', '{mid}-attempt-1', 'authority revoked');
SELECT pg_advisory_unlock_all();
"""
        assert_sql_succeeds(database.sql(fail_session, user="hcs_migrator"))
        assert _event_count(database, mid, "failed") == 1
        assert _classified_counts(database, mid) == (0, 0)
        # The failed attempt must not have frozen the v1 surface.
        probe = database.sql(
            "INSERT INTO public.hermes_groups (id, purpose) "
            "VALUES ('group-post-revoke', 'probe');"
        )
        assert_sql_succeeds(probe)


class TestCrashRecovery:
    def _seed_private_base(self, database: PostgresDatabase) -> dict:
        _seed_migration_base(database)
        _apply_migration_sql(database)
        assert_sql_succeeds(database.file(TWO_SUBJECT_SEED))
        return migration.load_dataset_description(TWO_SUBJECT_DATASET)

    def _restart(self, cluster: PostgresCluster) -> None:
        up = cluster.compose("up", "--detach", "--wait", "postgres", timeout=90)
        assert up.returncode == 0, f"{up.stdout}\n{up.stderr}"
        for _ in range(50):
            readiness = cluster.psql(BASE_DATABASE, "SELECT 1;")
            if readiness.returncode == 0:
                return
            time.sleep(0.3)
        raise AssertionError("private cluster did not become ready after restart")

    def _wait_for_event(
        self, database: PostgresDatabase, mid: str, event_type: str
    ) -> None:
        for _ in range(60):
            result = database.sql(
                "SELECT count(*) FROM xfactory_runtime_v2.migration_attempt_events "
                f"WHERE migration_id = '{mid}' AND event_type = '{event_type}';"
            )
            if result.returncode == 0 and result.stdout.strip().endswith("1"):
                return
            time.sleep(0.5)
        raise AssertionError(f"never observed committed {event_type} event")

    def test_crash_mid_cutover_abandons_and_retry_converges_exactly_once(
        self, private_postgres_cluster: PostgresCluster, tmp_path: Path
    ) -> None:
        cluster = private_postgres_cluster
        database = PostgresDatabase(cluster, BASE_DATABASE)
        dataset = self._seed_private_base(database)
        mid = "migration-crash-01"
        staging_text = _staged_document(
            database,
            migration_id=mid,
            dataset=dataset,
            source_database=BASE_DATABASE,
        )
        staging_path = _write_staging(tmp_path, staging_text, "staging.json")

        interrupted_session = f"""
SELECT pg_advisory_lock({_lock_expression(mid)});
BEGIN;
SELECT xfactory_runtime_api_v2.stage_migration(
  $hcs_recovery${staging_text}$hcs_recovery$::jsonb);
SELECT xfactory_runtime_api_v2.begin_migration_attempt(
  'install-01', '{mid}');
COMMIT;
BEGIN ISOLATION LEVEL SERIALIZABLE;
{V1_LOCK_STATEMENT}
SELECT xfactory_runtime_api_v2.execute_v1_cutover(
  'install-01', '{mid}', '{mid}-attempt-1');
SELECT pg_sleep(30);
COMMIT;
"""
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                database.sql, interrupted_session, user="hcs_migrator", timeout=60
            )
            self._wait_for_event(database, mid, "started")
            time.sleep(1.5)  # bias the kill into the held-lock cutover window
            killed = cluster.compose("kill", "postgres")
            assert killed.returncode == 0, f"{killed.stdout}\n{killed.stderr}"
            interrupted = future.result(timeout=90)
        assert (
            interrupted.returncode != 0
        ), "the crashed migration session must not report success"

        self._restart(cluster)
        assert _event_count(database, mid, "started") == 1
        assert _event_count(database, mid, "succeeded") == 0
        assert _classified_counts(database, mid) == (
            0,
            0,
        ), "the interrupted authoritative transaction must leave no rows"

        retry = _run_runner(database, staging_path, mid)
        assert retry.returncode == 0, f"{retry.stdout}\n{retry.stderr}"
        assert "outcome=succeeded" in retry.stdout
        assert (
            _event_count(database, mid, "abandoned") == 1
        ), "recovery must append ABANDONED for the interrupted attempt"
        assert _event_count(database, mid, "succeeded") == 1
        counts = migration.table_row_counts(dataset)
        history, quarantined = _classified_counts(database, mid)
        assert history + quarantined == sum(counts.values())
        _assert_assertions_hold(
            database,
            "migration-event-chain-invariant.sql",
            "migration-reconciliation-invariant.sql",
            "migration-freeze-catalog.sql",
        )

    def test_committed_success_before_client_ack_converges_to_stored_result(
        self, private_postgres_cluster: PostgresCluster, tmp_path: Path
    ) -> None:
        cluster = private_postgres_cluster
        database = PostgresDatabase(cluster, BASE_DATABASE)
        dataset = self._seed_private_base(database)
        mid = "migration-ackloss-01"
        staging_text = _staged_document(
            database,
            migration_id=mid,
            dataset=dataset,
            source_database=BASE_DATABASE,
        )
        staging_path = _write_staging(tmp_path, staging_text, "staging.json")

        acked_late_session = f"""
SELECT pg_advisory_lock({_lock_expression(mid)});
BEGIN;
SELECT xfactory_runtime_api_v2.stage_migration(
  $hcs_recovery${staging_text}$hcs_recovery$::jsonb);
SELECT xfactory_runtime_api_v2.begin_migration_attempt(
  'install-01', '{mid}');
COMMIT;
BEGIN ISOLATION LEVEL SERIALIZABLE;
{V1_LOCK_STATEMENT}
SELECT xfactory_runtime_api_v2.execute_v1_cutover(
  'install-01', '{mid}', '{mid}-attempt-1');
COMMIT;
SELECT pg_sleep(30);
SELECT 'client-acknowledged';
"""
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                database.sql, acked_late_session, user="hcs_migrator", timeout=60
            )
            self._wait_for_event(database, mid, "succeeded")
            killed = cluster.compose("kill", "postgres")
            assert killed.returncode == 0, f"{killed.stdout}\n{killed.stderr}"
            lost_ack = future.result(timeout=90)
        assert lost_ack.returncode != 0, "the client acknowledgement must be lost"
        assert "client-acknowledged" not in lost_ack.stdout

        self._restart(cluster)
        assert (
            _event_count(database, mid, "succeeded") == 1
        ), "the committed success must survive the crash"
        counts = migration.table_row_counts(dataset)
        history, quarantined = _classified_counts(database, mid)
        assert history + quarantined == sum(counts.values())

        converged = _run_runner(database, staging_path, mid)
        assert converged.returncode == 0, f"{converged.stdout}\n{converged.stderr}"
        assert "outcome=converged-terminal-success" in converged.stdout
        result_line = next(
            line
            for line in converged.stdout.splitlines()
            if line.startswith("hermes-v1-to-v2: result=")
        )
        stored = json.loads(result_line.removeprefix("hermes-v1-to-v2: result="))
        assert stored["status"] == "succeeded"
        assert stored["terminal"] is True
        assert stored["reconciliation"]["compatibility_history_count"] == history
        assert stored["reconciliation"]["quarantine_count"] == quarantined
        assert (
            _event_count(database, mid, "succeeded") == 1
        ), "the stored-result observer must not append a second success"
        history_after, quarantined_after = _classified_counts(database, mid)
        assert (history_after, quarantined_after) == (
            history,
            quarantined,
        ), "the stored-result observer must not reapply rows"
        frozen_probe = database.sql(
            "INSERT INTO public.hermes_groups (id, purpose) "
            "VALUES ('group-after-crash', 'probe');"
        )
        assert_sql_fails(frozen_probe, *FROZEN_FRAGMENTS)
        _assert_assertions_hold(
            database,
            "migration-event-chain-invariant.sql",
            "migration-reconciliation-invariant.sql",
            "migration-freeze-catalog.sql",
        )
