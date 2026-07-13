"""RED real-PostgreSQL contracts for the locked v2 apply boundary."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable

import pytest

from scripts.hermes_runtime_validation import migration

from .conftest import (
    CANONICAL_DDL_V1,
    COMPOSE_FILE,
    ISOLATION_FIXTURE_ROOT,
    MIGRATION_FIXTURE_ROOT,
    MIGRATION_SQL,
    REPOSITORY_ROOT,
    PostgresCluster,
    PostgresDatabase,
    assert_sql_fails,
    assert_sql_succeeds,
)

pytestmark = pytest.mark.postgres

APPLY_SCRIPT = REPOSITORY_ROOT / "scripts/apply-hermes-runtime-postgres-v2.py"
VALIDATE_SCRIPT = REPOSITORY_ROOT / "scripts/validate-hermes-runtime-postgres.py"
MIGRATION_RUNNER = REPOSITORY_ROOT / "scripts/run-hermes-v1-to-v2-migration.sh"
TWO_SUBJECT_DATASET = MIGRATION_FIXTURE_ROOT / "v1-two-subject-dataset.yaml"
TWO_SUBJECT_SEED = MIGRATION_FIXTURE_ROOT / "10-v1-two-subject-seed.sql"
MIGRATION_AUTHORITY_SEED = MIGRATION_FIXTURE_ROOT / "30-migration-authority.sql"

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

RunSubprocess = Callable[..., subprocess.CompletedProcess[str]]


def _psql_template(cluster: PostgresCluster) -> str:
    """SIC-shaped psql command template targeting the session cluster."""

    compose_file = str(COMPOSE_FILE)
    assert " " not in compose_file, compose_file
    assert " " not in cluster.project_name, cluster.project_name
    return (
        f"docker compose --file {compose_file} "
        f"--project-name {cluster.project_name} "
        "exec -T postgres psql -X -q -A -t -v ON_ERROR_STOP=1 "
        "-U hermes_runtime -d " + "{database}"
    )


def _run_tool(
    run_subprocess: RunSubprocess,
    cluster: PostgresCluster,
    script: Path,
    *arguments: str,
    timeout: float = 1200,
) -> subprocess.CompletedProcess[str]:
    assert script.is_file(), f"required tool is unavailable: {script}"
    return run_subprocess(
        [sys.executable, script, *arguments],
        cwd=REPOSITORY_ROOT,
        env=cluster.environment,
        timeout=timeout,
    )


def _report_from(result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert lines, f"tool produced no report: {result.stderr}"
    return json.loads(lines[-1])


def _apply(
    run_subprocess: RunSubprocess, database: PostgresDatabase
) -> tuple[dict[str, Any], subprocess.CompletedProcess[str]]:
    result = _run_tool(
        run_subprocess,
        database.cluster,
        APPLY_SCRIPT,
        "--psql-command",
        _psql_template(database.cluster),
        "--database",
        database.name,
        "--json",
    )
    return _report_from(result), result


def _validate(
    run_subprocess: RunSubprocess, database: PostgresDatabase, profile: str
) -> tuple[dict[str, Any], subprocess.CompletedProcess[str]]:
    result = _run_tool(
        run_subprocess,
        database.cluster,
        VALIDATE_SCRIPT,
        "--psql-command",
        _psql_template(database.cluster),
        "--database",
        database.name,
        "--profile",
        profile,
        "--json",
    )
    return _report_from(result), result


def _finding_codes(report: dict[str, Any]) -> set[str]:
    return {finding["code"] for finding in report["findings"]}


def test_apply_script_pins_the_apply_boundary_advisory_lock() -> None:
    source = APPLY_SCRIPT.read_text(encoding="utf-8")
    assert "pg_advisory_lock" in source
    assert "hashtextextended" in source
    assert "xfactory-v2-apply-boundary" in source


def test_clean_apply_to_empty_database_passes_the_locked_boundary(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    report, result = _apply(run_postgres_subprocess, postgres_empty_database)
    assert result.returncode == 0, f"{report}\n{result.stderr}"
    assert report["action"] == "applied"
    assert report["status"] == "ready"
    assert report["finding_count"] == 0
    # The empty preflight honestly differs from the fresh-v2 profile; only the
    # postflight proof may be clean.
    assert report["preflight_finding_count"] > 0

    readiness, verdict = _validate(
        run_postgres_subprocess, postgres_empty_database, "fresh-v2"
    )
    assert verdict.returncode == 0, f"{readiness}\n{verdict.stderr}"
    assert readiness["status"] == "ready"
    assert readiness["findings"] == []


def test_verified_reapply_over_exact_state_verifies_without_mutation(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    first, first_result = _apply(run_postgres_subprocess, postgres_empty_database)
    assert first_result.returncode == 0, f"{first}\n{first_result.stderr}"
    assert first["action"] == "applied"

    witness_sql = (
        "select count(*) from pg_catalog.pg_class c "
        "join pg_catalog.pg_namespace n on n.oid = c.relnamespace "
        "where n.nspname like 'xfactory%';"
    )
    witness_before = postgres_empty_database.scalar(witness_sql)

    second, second_result = _apply(run_postgres_subprocess, postgres_empty_database)
    assert second_result.returncode == 0, f"{second}\n{second_result.stderr}"
    assert second["action"] == "verified"
    assert second["status"] == "ready"
    assert second["preflight_finding_count"] == 0
    assert postgres_empty_database.scalar(witness_sql) == witness_before


def test_concurrent_applies_serialize_on_the_apply_boundary_lock(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    """Two racing applies resolve to exactly one apply plus one verify.

    The pinned session advisory lock makes the second session's preflight
    wait for the first session's committed apply, so the loser must observe
    the exact fresh-v2 state instead of double-applying or corrupting it.
    """

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(_apply, run_postgres_subprocess, postgres_empty_database)
            for _ in range(2)
        ]
        outcomes = [future.result(timeout=1300) for future in futures]

    for report, result in outcomes:
        assert result.returncode == 0, f"{report}\n{result.stderr}"
        assert report["status"] == "ready"
        assert report["finding_count"] == 0
    actions = sorted(report["action"] for report, _ in outcomes)
    assert actions == ["applied", "verified"], actions

    readiness, verdict = _validate(
        run_postgres_subprocess, postgres_empty_database, "fresh-v2"
    )
    assert verdict.returncode == 0, f"{readiness}\n{verdict.stderr}"
    assert readiness["status"] == "ready"


def test_refused_apply_leaves_zero_objects(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    tampered = postgres_empty_database.sql(
        "create table public.xfv2_tamper (id integer);"
    )
    assert_sql_succeeds(tampered)

    report, result = _apply(run_postgres_subprocess, postgres_empty_database)
    assert result.returncode == 1, f"{report}\n{result.stderr}"
    assert report["action"] == "refused"
    assert report["status"] == "refused"
    assert report["finding_count"] > 0

    # Preflight ran BEFORE any mutation: the refused target carries zero
    # canonical objects, roles side effects, or event triggers.
    assert (
        postgres_empty_database.scalar(
            "select count(*) from pg_catalog.pg_namespace "
            "where nspname like 'xfactory%';"
        )
        == "0"
    )
    assert (
        postgres_empty_database.scalar(
            "select count(*) from pg_catalog.pg_class c "
            "join pg_catalog.pg_namespace n on n.oid = c.relnamespace "
            "where n.nspname like 'xfactory%';"
        )
        == "0"
    )
    assert (
        postgres_empty_database.scalar(
            "select count(*) from pg_catalog.pg_event_trigger;"
        )
        == "0"
    )


def test_reapply_refuses_drifted_state_without_repairing_it(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    first, first_result = _apply(run_postgres_subprocess, postgres_empty_database)
    assert first_result.returncode == 0, f"{first}\n{first_result.stderr}"

    dropped = postgres_empty_database.sql(
        "drop table xfactory_runtime_v2.governed_projections cascade;"
    )
    assert_sql_succeeds(dropped)

    report, result = _apply(run_postgres_subprocess, postgres_empty_database)
    assert result.returncode == 1, f"{report}\n{result.stderr}"
    assert report["action"] == "refused"
    assert "XFV2-TABLE-MISSING" in _finding_codes(report)

    # The refused boundary never repaired the drift.
    assert (
        postgres_empty_database.scalar(
            "select coalesce(pg_catalog.to_regclass("
            "'xfactory_runtime_v2.governed_projections')::text, 'absent');"
        )
        == "absent"
    )


def test_reapply_refuses_drifted_role_attributes_at_the_boundary(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    """Cluster-level mutation: always reverted, even on assertion failure."""

    first, first_result = _apply(run_postgres_subprocess, postgres_empty_database)
    assert first_result.returncode == 0, f"{first}\n{first_result.stderr}"

    mutated = postgres_empty_database.sql("alter role xfactory_v2_control createdb;")
    assert_sql_succeeds(mutated)
    try:
        report, result = _apply(run_postgres_subprocess, postgres_empty_database)
        assert result.returncode == 1, f"{report}\n{result.stderr}"
        assert report["action"] == "refused"
        assert "XFV2-ROLE-ATTRIBUTE-ALTERED" in _finding_codes(report)
    finally:
        reverted = postgres_empty_database.sql(
            "alter role xfactory_v2_control nocreatedb;"
        )
        assert_sql_succeeds(reverted)


def test_reapply_downgrades_verified_state_on_rogue_owner_membership(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    """Cluster-level mutation: always reverted, even on assertion failure.

    Cluster membership state is shared with the scratch derivation, so the
    in-session exact comparison cannot see it; the boundary must still fail
    through the postflight membership policy without repairing the edge.
    """

    first, first_result = _apply(run_postgres_subprocess, postgres_empty_database)
    assert first_result.returncode == 0, f"{first}\n{first_result.stderr}"

    mutated = postgres_empty_database.sql("grant xfactory_v2_owner to hcs_unbound;")
    assert_sql_succeeds(mutated)
    try:
        report, result = _apply(run_postgres_subprocess, postgres_empty_database)
        assert result.returncode == 1, f"{report}\n{result.stderr}"
        assert report["action"] == "verified"
        assert report["status"] == "findings"
        assert "XFV2-ROLE-MEMBERSHIP-EXTRA" in _finding_codes(report)
    finally:
        reverted = postgres_empty_database.sql(
            "revoke xfactory_v2_owner from hcs_unbound;"
        )
        assert_sql_succeeds(reverted)


def test_v1_pre_cutover_profile_reports_ready_after_v2_and_v1_apply(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    report, result = _apply(run_postgres_subprocess, postgres_empty_database)
    assert result.returncode == 0, f"{report}\n{result.stderr}"

    applied_v1 = postgres_empty_database.file(CANONICAL_DDL_V1, timeout=60)
    assert_sql_succeeds(applied_v1)

    readiness, verdict = _validate(
        run_postgres_subprocess, postgres_empty_database, "v1-pre-cutover"
    )
    assert verdict.returncode == 0, f"{readiness}\n{verdict.stderr}"
    assert readiness["status"] == "ready"
    assert readiness["findings"] == []


def test_v1_cutover_readiness_fails_closed_before_the_durable_freeze(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    """A pre-cutover database is never v1-cutover ready, and never a crash.

    Before the migration surface lands this reports the honest
    ``XFV2-FREEZE-INSTALLER-MISSING`` finding; afterwards it reports the
    missing durable-freeze objects themselves.  Both are findings (exit 1),
    never a harness error (exit 2).
    """

    report, result = _apply(run_postgres_subprocess, postgres_empty_database)
    assert result.returncode == 0, f"{report}\n{result.stderr}"

    applied_v1 = postgres_empty_database.file(CANONICAL_DDL_V1, timeout=60)
    assert_sql_succeeds(applied_v1)

    readiness, verdict = _validate(
        run_postgres_subprocess, postgres_empty_database, "v1-cutover"
    )
    assert verdict.returncode == 1, f"{readiness}\n{verdict.stderr}"
    assert readiness["status"] == "findings"
    codes = _finding_codes(readiness)
    assert any(code.startswith("XFV2-FREEZE") for code in codes), codes


def test_v1_cutover_profile_reports_ready_after_freeze_installation(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    """Migration surface plus freeze installer is exactly the v1-cutover profile.

    The amended derivation recipe (integration decision D10) includes the
    canonical migration surface, so the honest v1-cutover baseline applies
    ``migrations/v1-to-v2.sql`` as the superuser before installing the freeze.
    """

    report, result = _apply(run_postgres_subprocess, postgres_empty_database)
    assert result.returncode == 0, f"{report}\n{result.stderr}"

    applied_v1 = postgres_empty_database.file(CANONICAL_DDL_V1, timeout=60)
    assert_sql_succeeds(applied_v1)

    applied_migration = postgres_empty_database.file(MIGRATION_SQL, timeout=60)
    assert_sql_succeeds(applied_migration)

    frozen = postgres_empty_database.sql(
        "select xfactory_runtime_v2.install_v1_freeze('profile-derivation');"
    )
    assert_sql_succeeds(frozen)

    readiness, verdict = _validate(
        run_postgres_subprocess, postgres_empty_database, "v1-cutover"
    )
    assert verdict.returncode == 0, f"{readiness}\n{verdict.stderr}"
    assert readiness["status"] == "ready"
    assert readiness["findings"] == []


_SEED_V1_JOB_SQL = (
    "insert into public.hermes_jobs ("
    "  id, schema_version, issued_by, job_type, project,"
    "  repository_org, repository_name, repository_default_branch,"
    "  orchestrator_path, routing_policy_path, auth_profile_id, auth_mode,"
    "  envelope"
    ") values ("
    "  'job-clean-apply-{suffix}', 1, 'Hermes', 'engineering', 'project-alfa',"
    "  'opensoft', 'demo', 'main',"
    "  'orchestrators/demo.yaml', 'routing/demo.yaml', 'auth-profile-01',"
    "  'subscription', '{{\"kind\": \"job\"}}'::jsonb"
    ");"
)


def test_v1_seeded_database_validates_pre_cutover_and_freeze_is_durable(
    postgres_v1_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    """Seeded v1 rows never disturb catalog readiness; the freeze is live."""

    seeded = postgres_v1_database.sql(_SEED_V1_JOB_SQL.format(suffix="01"))
    assert_sql_succeeds(seeded)

    readiness, verdict = _validate(
        run_postgres_subprocess, postgres_v1_database, "v1-pre-cutover"
    )
    assert verdict.returncode == 0, f"{readiness}\n{verdict.stderr}"
    assert readiness["status"] == "ready"
    assert readiness["findings"] == []

    # The v1-cutover baseline includes the canonical migration surface (D10):
    # apply it as the superuser after the v1 DDL and before the freeze.
    applied_migration = postgres_v1_database.file(MIGRATION_SQL, timeout=60)
    assert_sql_succeeds(applied_migration)

    frozen = postgres_v1_database.sql(
        "select xfactory_runtime_v2.install_v1_freeze('profile-derivation');"
    )
    assert_sql_succeeds(frozen)

    blocked = postgres_v1_database.sql(_SEED_V1_JOB_SQL.format(suffix="02"))
    assert_sql_fails(blocked, "HGR-MIGRATION-V1-FROZEN", "frozen")
    assert postgres_v1_database.scalar("select count(*) from public.hermes_jobs;") == (
        "1"
    )

    readiness, verdict = _validate(
        run_postgres_subprocess, postgres_v1_database, "v1-cutover"
    )
    assert verdict.returncode == 0, f"{readiness}\n{verdict.stderr}"
    assert readiness["status"] == "ready"
    assert readiness["findings"] == []


# --- D10 end-to-end guard: the production migration path IS v1-cutover ----
# Staging/runner mechanics mirror test_migration.py / test_migration_recovery.py
# (each migration module keeps its helpers self-contained by convention).


def _migration_cell_text(cell: dict) -> str:
    assert cell.get("type") is not None, "primary-key cells must not be null"
    value = cell["value"]
    assert isinstance(value, str), "v1 primary keys frame as text encodings"
    return value


def _migration_pk_arrays(dataset: dict, table_name: str) -> list[str]:
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
            [_migration_cell_text(row[index]) for _, index in key_ordinals]
        )
        for row in table["rows"]
    )


def _build_migration_payload(
    dataset: dict, *, source_database: str, migration_id: str
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
        "subject_mappings": [
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
                for pk in _migration_pk_arrays(dataset, table_name)
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
    """Mint an exact-resource run_migration grant; return the stored digest.

    The ``authority_grants_compute_digest`` trigger recomputes
    ``record_digest`` server-side, so the returned value is what
    ``migration_verify_authority`` actually checks against.
    """

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


def _staged_migration_document(
    database: PostgresDatabase, *, migration_id: str, dataset: dict
) -> str:
    payload = _build_migration_payload(
        dataset, source_database=database.name, migration_id=migration_id
    )
    grant_id = f"grant-run-migration-{migration_id}-01"
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


def _migrator_psql_template(cluster: PostgresCluster) -> str:
    return (
        f"docker compose --file {COMPOSE_FILE} "
        f"--project-name {cluster.project_name} "
        "exec -T postgres psql -X -q -A -t -v ON_ERROR_STOP=1 "
        "-U hcs_migrator -d {database}"
    )


def _run_migration_runner(
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
            "HERMES_MIGRATION_PSQL_COMMAND": _migrator_psql_template(cluster),
        },
        timeout=300,
    )


def test_runner_migrated_database_reports_v1_cutover_ready(
    postgres_v1_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
    tmp_path: Path,
) -> None:
    """A database migrated by the real production path is v1-cutover ready.

    End-to-end guard for integration decision D10: after the v2 DDL
    (template), the pinned v1 DDL (fixture), ``migrations/v1-to-v2.sql`` as
    the superuser, the seeded migration fixtures, a canonical staging
    document, and ``scripts/run-hermes-v1-to-v2-migration.sh`` driven as
    ``hcs_migrator`` to terminal success, the readiness validator MUST
    report the v1-cutover profile ``ready`` with zero findings — the
    ratified postflight clause is satisfiable by the ratified migration
    protocol itself.  This deliberately exercises the production runner
    instead of shortcutting via a direct ``install_v1_freeze`` call.
    """

    database = postgres_v1_database
    applied_migration = database.file(MIGRATION_SQL, timeout=60)
    assert_sql_succeeds(applied_migration)
    for fixture in ("10-two-customer-topology.sql", "20-authority.sql"):
        assert_sql_succeeds(database.file(ISOLATION_FIXTURE_ROOT / fixture))
    assert_sql_succeeds(database.file(MIGRATION_AUTHORITY_SEED))
    assert_sql_succeeds(database.file(TWO_SUBJECT_SEED))

    migration_id = "migration-cutover-readiness-01"
    dataset = migration.load_dataset_description(TWO_SUBJECT_DATASET)
    staging_path = tmp_path / "staging.json"
    staging_path.write_text(
        _staged_migration_document(
            database, migration_id=migration_id, dataset=dataset
        ),
        encoding="utf-8",
    )

    run = _run_migration_runner(database, staging_path, migration_id)
    assert run.returncode == 0, f"{run.stdout}\n{run.stderr}"
    assert "outcome=succeeded" in run.stdout

    readiness, verdict = _validate(run_postgres_subprocess, database, "v1-cutover")
    assert verdict.returncode == 0, f"{readiness}\n{verdict.stderr}"
    assert readiness["status"] == "ready"
    assert readiness["finding_count"] == 0
    assert readiness["findings"] == []
