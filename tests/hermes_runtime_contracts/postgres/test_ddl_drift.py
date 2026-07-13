"""RED real-PostgreSQL contracts for per-dimension DDL drift readiness."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable

import pytest

from .conftest import (
    CANONICAL_DDL,
    CANONICAL_DDL_V1,
    COMPOSE_FILE,
    MIGRATION_SQL,
    REPOSITORY_ROOT,
    PostgresCluster,
    PostgresDatabase,
    assert_sql_succeeds,
)

pytestmark = pytest.mark.postgres

VALIDATE_SCRIPT = REPOSITORY_ROOT / "scripts/validate-hermes-runtime-postgres.py"

RunSubprocess = Callable[..., subprocess.CompletedProcess[str]]


def _psql_template(cluster: PostgresCluster) -> str:
    compose_file = str(COMPOSE_FILE)
    assert " " not in compose_file, compose_file
    assert " " not in cluster.project_name, cluster.project_name
    return (
        f"docker compose --file {compose_file} "
        f"--project-name {cluster.project_name} "
        "exec -T postgres psql -X -q -A -t -v ON_ERROR_STOP=1 "
        "-U hermes_runtime -d " + "{database}"
    )


def _validate(
    run_subprocess: RunSubprocess,
    database: PostgresDatabase,
    profile: str,
    script: Path = VALIDATE_SCRIPT,
) -> tuple[dict[str, Any], subprocess.CompletedProcess[str]]:
    assert script.is_file(), script
    result = run_subprocess(
        [
            sys.executable,
            script,
            "--psql-command",
            _psql_template(database.cluster),
            "--database",
            database.name,
            "--profile",
            profile,
            "--json",
        ],
        cwd=REPOSITORY_ROOT,
        env=database.cluster.environment,
        timeout=900,
    )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert lines, f"validator produced no report: {result.stderr}"
    return json.loads(lines[-1]), result


def _apply_fresh_v2(database: PostgresDatabase) -> None:
    applied = database.file(CANONICAL_DDL, timeout=90)
    assert_sql_succeeds(applied)


def _apply_v1(database: PostgresDatabase) -> None:
    applied = database.file(CANONICAL_DDL_V1, timeout=60)
    assert_sql_succeeds(applied)


def _finding_codes(report: dict[str, Any]) -> set[str]:
    return {finding["code"] for finding in report["findings"]}


def _assert_reports_code(
    run_subprocess: RunSubprocess,
    database: PostgresDatabase,
    profile: str,
    expected_code: str,
    script: Path = VALIDATE_SCRIPT,
) -> None:
    report, result = _validate(run_subprocess, database, profile, script)
    assert result.returncode == 1, f"{report}\n{result.stderr}"
    assert report["status"] == "findings"
    codes = _finding_codes(report)
    assert expected_code in codes, (expected_code, sorted(codes))


def test_freshly_applied_database_reports_fresh_v2_ready(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    _apply_fresh_v2(postgres_empty_database)
    report, result = _validate(
        run_postgres_subprocess, postgres_empty_database, "fresh-v2"
    )
    assert result.returncode == 0, f"{report}\n{result.stderr}"
    assert report["status"] == "ready"
    assert report["findings"] == []


DRIFT_CASES: tuple[tuple[str, str, str], ...] = (
    (
        "table-missing",
        "drop table xfactory_runtime_v2.governed_projections cascade;",
        "XFV2-TABLE-MISSING",
    ),
    (
        "table-extra",
        "create table xfactory_runtime_v2.xfv2_drift_extra (id text primary key);",
        "XFV2-TABLE-EXTRA",
    ),
    (
        "column-missing",
        "alter table xfactory_runtime_v2.governed_projections "
        "drop column binding_id;",
        "XFV2-COLUMN-MISSING",
    ),
    (
        "column-extra",
        "alter table xfactory_runtime_v2.governed_projections "
        "add column xfv2_drift_extra text;",
        "XFV2-COLUMN-EXTRA",
    ),
    (
        "column-altered",
        "alter table xfactory_runtime_v2.governed_projections "
        "alter column operation_id set default 'xfv2-drift';",
        "XFV2-COLUMN-ALTERED",
    ),
    (
        "constraint-missing",
        "alter table xfactory_runtime_v2.governed_projections "
        "drop constraint governed_projections_pkey;",
        "XFV2-CONSTRAINT-MISSING",
    ),
    (
        "constraint-extra",
        "alter table xfactory_runtime_v2.governed_projections "
        "add constraint xfv2_drift_extra_check check (operation_id is not null);",
        "XFV2-CONSTRAINT-EXTRA",
    ),
    (
        "constraint-altered",
        "alter table xfactory_runtime_v2.governed_projections "
        "drop constraint governed_projections_pkey;\n"
        "alter table xfactory_runtime_v2.governed_projections "
        "add constraint governed_projections_pkey primary key "
        "(installation_id, stack_id, layer_id, projection_id, record_digest);",
        "XFV2-CONSTRAINT-ALTERED",
    ),
    (
        "index-missing",
        "drop index xfactory_runtime_v2.layer_customer_subject_lifetime_uq;",
        "XFV2-INDEX-MISSING",
    ),
    (
        "index-extra",
        "create index xfv2_drift_idx "
        "on xfactory_runtime_v2.governed_projections (operation_id);",
        "XFV2-INDEX-EXTRA",
    ),
    (
        "index-altered",
        "drop index xfactory_runtime_v2.layer_customer_subject_lifetime_uq;\n"
        "create index layer_customer_subject_lifetime_uq "
        "on xfactory_runtime_v2.layer_registrations (installation_id);",
        "XFV2-INDEX-ALTERED",
    ),
    (
        "policy-missing",
        "drop policy governed_projections_exact_scope "
        "on xfactory_runtime_v2.governed_projections;",
        "XFV2-POLICY-MISSING",
    ),
    (
        "policy-extra",
        "create policy xfv2_drift_policy "
        "on xfactory_runtime_v2.governed_projections for select using (true);",
        "XFV2-POLICY-EXTRA",
    ),
    (
        "policy-altered",
        "alter policy operation_authorizations_exact_scope "
        "on xfactory_runtime_v2.operation_authorizations to xfactory_v2_runtime;",
        "XFV2-POLICY-ALTERED",
    ),
    (
        "function-missing",
        "drop function xfactory_runtime_api_v2.probe_artifact(text);",
        "XFV2-FUNCTION-MISSING",
    ),
    (
        "function-extra",
        "create function xfactory_runtime_v2.xfv2_drift_function() "
        "returns integer language sql as $$select 1$$;",
        "XFV2-FUNCTION-EXTRA",
    ),
    (
        "security-definer-altered",
        "alter function xfactory_runtime_api_v2.probe_artifact(text) "
        "security invoker;",
        "XFV2-FUNCTION-SECURITY-ALTERED",
    ),
    (
        "search-path-altered",
        "alter function xfactory_runtime_api_v2.clear_scope() "
        "set search_path = xfactory_runtime_v2, public;",
        "XFV2-FUNCTION-SECURITY-ALTERED",
    ),
    (
        "trigger-altered",
        "alter table xfactory_runtime_v2.lifecycle_projections "
        "disable trigger lifecycle_projections_governed_only;",
        "XFV2-TRIGGER-ALTERED",
    ),
    (
        "trigger-missing",
        "drop trigger lifecycle_projections_reconciled "
        "on xfactory_runtime_v2.lifecycle_projections;",
        "XFV2-TRIGGER-MISSING",
    ),
    (
        "trigger-extra",
        "create function public.xfv2_drift_row_touch() returns trigger "
        "language plpgsql as $$begin return new; end$$;\n"
        "create trigger xfv2_drift_trigger before insert "
        "on xfactory_runtime_v2.governed_projections "
        "for each row execute function public.xfv2_drift_row_touch();",
        "XFV2-TRIGGER-EXTRA",
    ),
    (
        "ownership-altered",
        "alter table xfactory_runtime_v2.governed_projections "
        "owner to xfactory_v2_control;",
        "XFV2-OWNERSHIP-ALTERED",
    ),
    (
        "acl-altered",
        "grant insert on xfactory_runtime_v2.traceability_edges "
        "to xfactory_v2_audit;",
        "XFV2-ACL-ALTERED",
    ),
    (
        "acl-revoked",
        "revoke all on xfactory_runtime_v2.traceability_edges from "
        "xfactory_v2_owner, xfactory_v2_runtime, xfactory_v2_audit;",
        "XFV2-ACL-ALTERED",
    ),
    (
        "row-security-altered",
        "alter table xfactory_runtime_v2.traceability_edges "
        "no force row level security;",
        "XFV2-ROW-SECURITY-ALTERED",
    ),
    (
        "public-privilege-altered",
        "grant select on xfactory_runtime_v2.governed_projections to public;",
        "XFV2-PUBLIC-PRIVILEGE-ALTERED",
    ),
    (
        "trusted-schema-altered",
        "grant create on schema xfactory_runtime_v2 to xfactory_v2_runtime;",
        "XFV2-TRUSTED-SCHEMA-ALTERED",
    ),
    (
        "quarantine-grant-extra",
        "grant usage on schema xfactory_legacy_quarantine_v2 "
        "to xfactory_v2_runtime;",
        "XFV2-QUARANTINE-GRANT-EXTRA",
    ),
    (
        "schema-extra",
        "create schema xfactory_drift_evil;",
        "XFV2-SCHEMA-EXTRA",
    ),
    (
        "schema-missing",
        "drop schema xfactory_legacy_quarantine_v2 cascade;",
        "XFV2-SCHEMA-MISSING",
    ),
    (
        "dependency-guard-extra",
        "create function public.xfv2_drift_event_probe() "
        "returns event_trigger language plpgsql as $$begin end$$;\n"
        "create event trigger xfv2_drift_guard on ddl_command_end "
        "execute function public.xfv2_drift_event_probe();",
        "XFV2-DEPENDENCY-GUARD-EXTRA",
    ),
)


@pytest.mark.parametrize(
    ("mutation_sql", "expected_code"),
    [(mutation, code) for _, mutation, code in DRIFT_CASES],
    ids=[case_id for case_id, _, _ in DRIFT_CASES],
)
def test_each_drift_dimension_reports_its_stable_finding_code(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
    mutation_sql: str,
    expected_code: str,
) -> None:
    _apply_fresh_v2(postgres_empty_database)
    mutated = postgres_empty_database.sql(mutation_sql)
    assert_sql_succeeds(mutated)
    _assert_reports_code(
        run_postgres_subprocess, postgres_empty_database, "fresh-v2", expected_code
    )


def test_role_attribute_drift_reports_stable_finding_code(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    """Cluster-level mutation: always reverted, even on assertion failure."""

    _apply_fresh_v2(postgres_empty_database)
    mutated = postgres_empty_database.sql("alter role xfactory_v2_audit createdb;")
    assert_sql_succeeds(mutated)
    try:
        _assert_reports_code(
            run_postgres_subprocess,
            postgres_empty_database,
            "fresh-v2",
            "XFV2-ROLE-ATTRIBUTE-ALTERED",
        )
    finally:
        reverted = postgres_empty_database.sql(
            "alter role xfactory_v2_audit nocreatedb;"
        )
        assert_sql_succeeds(reverted)


def test_role_membership_drift_reports_stable_finding_code(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    """Cluster-level mutation: always reverted, even on assertion failure."""

    _apply_fresh_v2(postgres_empty_database)
    mutated = postgres_empty_database.sql("grant xfactory_v2_owner to hcs_unbound;")
    assert_sql_succeeds(mutated)
    try:
        _assert_reports_code(
            run_postgres_subprocess,
            postgres_empty_database,
            "fresh-v2",
            "XFV2-ROLE-MEMBERSHIP-EXTRA",
        )
    finally:
        reverted = postgres_empty_database.sql(
            "revoke xfactory_v2_owner from hcs_unbound;"
        )
        assert_sql_succeeds(reverted)


_MEMBERSHIP_PROBE_DDL_TAIL = (
    "\n-- Membership-missing probe: the member role and its canonical edge\n"
    "-- exist only inside the validator's rolled-back scratch derivation.\n"
    "reset role;\n"
    "create role xfv2_f5_missing_member nologin;\n"
    "grant xfactory_v2_owner to xfv2_f5_missing_member;\n"
)


def _augmented_membership_validator(tmp_path: Path) -> Path:
    """Current validator bytes whose canonical v2 DDL gains one membership.

    Expected membership edges are policy-based: only edges the canonical DDL
    itself creates during the rolled-back scratch derivation are expected, and
    the current canonical DDL grants none, so the missing direction cannot be
    produced by mutating a target.  Re-rooting a byte-for-byte copy of the
    validator over the current canonical DDL plus one appended role-and-grant
    tail derives an expected edge no pristine target holds, without ever
    mutating the repository, the target database, or shared cluster state.
    """

    script_copy = tmp_path / VALIDATE_SCRIPT.relative_to(REPOSITORY_ROOT)
    script_copy.parent.mkdir(parents=True, exist_ok=True)
    script_copy.write_bytes(VALIDATE_SCRIPT.read_bytes())
    ddl_copy = tmp_path / CANONICAL_DDL.relative_to(REPOSITORY_ROOT)
    ddl_copy.parent.mkdir(parents=True, exist_ok=True)
    ddl_copy.write_text(
        CANONICAL_DDL.read_text(encoding="utf-8") + _MEMBERSHIP_PROBE_DDL_TAIL,
        encoding="utf-8",
    )
    return script_copy


def test_role_membership_missing_reports_stable_finding_code(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
    tmp_path: Path,
) -> None:
    """A canonical membership edge absent from the target is reported.

    The probe grant lives only inside the augmented scratch derivation (and
    is rolled back with it), so no cluster-level revert is needed and the
    pristine target legitimately lacks the expected edge.
    """

    _apply_fresh_v2(postgres_empty_database)
    script = _augmented_membership_validator(tmp_path)
    _assert_reports_code(
        run_postgres_subprocess,
        postgres_empty_database,
        "fresh-v2",
        "XFV2-ROLE-MEMBERSHIP-MISSING",
        script=script,
    )


def test_rogue_trigger_on_v1_surface_reports_freeze_extra(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    _apply_fresh_v2(postgres_empty_database)
    _apply_v1(postgres_empty_database)
    mutated = postgres_empty_database.sql(
        "create function public.xfv2_drift_touch() returns trigger "
        "language plpgsql as $$begin return new; end$$;\n"
        "create trigger xfv2_drift_freeze before insert on public.hermes_jobs "
        "for each row execute function public.xfv2_drift_touch();"
    )
    assert_sql_succeeds(mutated)
    _assert_reports_code(
        run_postgres_subprocess,
        postgres_empty_database,
        "v1-pre-cutover",
        "XFV2-FREEZE-EXTRA",
    )


def test_missing_freeze_trigger_after_cutover_reports_freeze_missing(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    """Thawing one frozen v1 table is durable-freeze drift, independently."""

    _apply_fresh_v2(postgres_empty_database)
    _apply_v1(postgres_empty_database)
    # The v1-cutover baseline includes the canonical migration surface (D10):
    # apply it as the superuser after the v1 DDL and before the freeze.
    applied_migration = postgres_empty_database.file(MIGRATION_SQL, timeout=60)
    assert_sql_succeeds(applied_migration)
    frozen = postgres_empty_database.sql(
        "select xfactory_runtime_v2.install_v1_freeze('profile-derivation');"
    )
    assert_sql_succeeds(frozen)
    thawed = postgres_empty_database.sql(
        "drop trigger hermes_v1_freeze_write on public.hermes_jobs;"
    )
    assert_sql_succeeds(thawed)
    _assert_reports_code(
        run_postgres_subprocess,
        postgres_empty_database,
        "v1-cutover",
        "XFV2-FREEZE-MISSING",
    )


def test_missing_dependency_guard_reports_guard_missing(
    postgres_empty_database: PostgresDatabase,
    run_postgres_subprocess: RunSubprocess,
) -> None:
    """Dropping the quarantine dependency guard is independently reported."""

    _apply_fresh_v2(postgres_empty_database)
    dropped = postgres_empty_database.sql(
        "drop event trigger xfactory_quarantine_dependency_guard;"
    )
    assert_sql_succeeds(dropped)
    _assert_reports_code(
        run_postgres_subprocess,
        postgres_empty_database,
        "fresh-v2",
        "XFV2-DEPENDENCY-GUARD-MISSING",
    )
