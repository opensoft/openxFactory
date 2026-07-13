#!/usr/bin/env python3
"""Locked preflight/apply/postflight boundary for the Hermes runtime v2 DDL.

One psql session (one connection) takes the pinned apply-boundary advisory
lock ``pg_advisory_lock(hashtextextended('xfactory-v2-apply-boundary', 0))``
and then, while holding it:

1. preflights the target database READ-ONLY and compares it against the
   live-derived fresh-v2 profile BEFORE any mutation or role repair;
2. accepts only an EMPTY database (transactional apply of the complete
   canonical v2 DDL: one ``begin; ... commit;``) or an EXACT fresh-v2
   database (verified reapply: nothing is executed, because the canonical
   DDL's ``create role`` DO-blocks and any event triggers live outside the
   database and must never be repaired or replayed over matching state);
3. refuses anything else without executing a single statement against the
   target;
4. postflights the resulting state and reports the proof.

The expected profile is derived from the canonical DDL by the sibling
read-only validator (scratch database, rolled-back transaction), never from
frozen object inventories.  A refused apply therefore leaves zero objects,
and a failed transactional apply rolls back to zero objects.

Requires a bootstrap-superuser session.  Exit codes: 0 applied or verified
and ready, 1 refused or drift findings, 2 harness or usage error.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType
from typing import Any

_VALIDATOR_MODULE_NAME = "hermes_runtime_postgres_validation"
_VALIDATOR_PATH = (
    Path(__file__).resolve().parent / "validate-hermes-runtime-postgres.py"
)

APPLY_LOCK_NAME = "xfactory-v2-apply-boundary"
APPLY_REPORT_KIND = "openxfactory-hermes-runtime-postgres-apply-report"
APPLY_REFUSED_CODE = "XFV2-APPLY-REFUSED"

ACTION_APPLIED = "applied"
ACTION_VERIFIED = "verified"
ACTION_REFUSED = "refused"

_PHASE_PREFIX = "XFPHASE:"
_ACTION_PREFIX = "XFACTION:"
_PREFLIGHT_PHASE = "preflight"
_POSTFLIGHT_PHASE = "postflight"


def _load_validation_module() -> ModuleType:
    if _VALIDATOR_MODULE_NAME in sys.modules:
        return sys.modules[_VALIDATOR_MODULE_NAME]
    spec = importlib.util.spec_from_file_location(
        _VALIDATOR_MODULE_NAME, _VALIDATOR_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"validator module unavailable: {_VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[_VALIDATOR_MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


validation = _load_validation_module()


def _empty_database_condition() -> str:
    """SQL boolean: the target database carries no user-visible objects."""

    return """(
  not exists (
    select 1 from pg_catalog.pg_namespace n
    where n.nspname <> 'public'
      and n.nspname <> 'information_schema'
      and n.nspname not like 'pg\\_%' escape '\\'
  )
  and not exists (
    select 1 from pg_catalog.pg_class c
    join pg_catalog.pg_namespace n on n.oid = c.relnamespace
    where n.nspname = 'public'
  )
  and not exists (
    select 1 from pg_catalog.pg_proc p
    join pg_catalog.pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public'
  )
  and not exists (select 1 from pg_catalog.pg_event_trigger)
)"""


def _exact_profile_condition(expected: Any, scope_sql: Any) -> str:
    """SQL boolean: every fingerprint dimension equals the expected payload.

    Role memberships are deliberately excluded here: cluster membership state
    is shared between the scratch derivation and this session, so payload
    equality would hold even for rogue edges.  The Python postflight applies
    the membership policy instead and downgrades a ``verified`` action to
    findings when an edge violates it.
    """

    conditions: list[str] = []
    for name, aggregate in validation._dimension_aggregates(scope_sql):
        if name == validation.MEMBERSHIP_DIMENSION:
            continue
        expected_payload = expected.dimensions.get(name, [])
        literal = validation.sql_literal(
            json.dumps(expected_payload, ensure_ascii=False, separators=(",", ":"))
        )
        conditions.append(
            f"coalesce((\n{aggregate.rstrip()}\n), '[]')::jsonb = {literal}::jsonb"
        )
    return "(\n" + "\n  and ".join(conditions) + "\n)"


def _capture_section(scope_sql: Any) -> str:
    statements = "\n".join(
        statement for _, statement in validation._dimension_statements(scope_sql)
    )
    return f"begin;\nset transaction read only;\n{statements}\nrollback;"


def build_apply_session_script(expected: Any, v2_ddl: str) -> str:
    """One connection: lock, decide, preflight, conditionally apply, postflight."""

    scope_sql = validation._inline_scope_sql(expected.scope)
    empty_condition = _empty_database_condition()
    exact_condition = _exact_profile_condition(expected, scope_sql)
    capture = _capture_section(scope_sql)
    lock_literal = validation.sql_literal(APPLY_LOCK_NAME)
    sections = [
        "select pg_advisory_lock(" f"pg_catalog.hashtextextended({lock_literal}, 0));",
        # Both decisions read pre-mutation state under the session lock.
        f"select case when {empty_condition}\n"
        "  then 'true' else 'false' end as xfv2_empty \\gset",
        f"select case when {exact_condition}\n"
        "  then 'true' else 'false' end as xfv2_exact \\gset",
        f"select {validation.sql_literal(_PHASE_PREFIX + _PREFLIGHT_PHASE)};",
        capture,
        "\\if :xfv2_empty",
        f"select {validation.sql_literal(_ACTION_PREFIX + ACTION_APPLIED)};",
        "begin;",
        v2_ddl,
        "commit;",
        "\\elif :xfv2_exact",
        f"select {validation.sql_literal(_ACTION_PREFIX + ACTION_VERIFIED)};",
        "\\else",
        f"select {validation.sql_literal(_ACTION_PREFIX + ACTION_REFUSED)};",
        "\\endif",
        # The canonical DDL leaves `set search_path` behind, which changes
        # how pg_get_*def deparse schema qualifications.  Normalize session
        # state so the postflight capture byte-matches the scratch profile.
        "reset role;",
        "reset search_path;",
        f"select {validation.sql_literal(_PHASE_PREFIX + _POSTFLIGHT_PHASE)};",
        capture,
    ]
    return "\n".join(sections) + "\n"


def parse_session_output(stdout: str) -> tuple[str, dict[str, dict[str, Any]]]:
    """Split session output into the action taken and per-phase payloads."""

    actions: list[str] = []
    phase_lines: dict[str, list[str]] = {_PREFLIGHT_PHASE: [], _POSTFLIGHT_PHASE: []}
    current_phase: str | None = None
    for line in stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith(_PHASE_PREFIX):
            phase = stripped[len(_PHASE_PREFIX) :]
            if phase not in phase_lines:
                raise validation.ToolError(f"unknown session phase {phase!r}")
            current_phase = phase
            continue
        if stripped.startswith(_ACTION_PREFIX):
            actions.append(stripped[len(_ACTION_PREFIX) :])
            continue
        if current_phase is not None:
            phase_lines[current_phase].append(line)
    if len(actions) != 1 or actions[0] not in (
        ACTION_APPLIED,
        ACTION_VERIFIED,
        ACTION_REFUSED,
    ):
        raise validation.ToolError(
            f"apply session reported no unambiguous action (saw {actions!r})"
        )

    expected_names = {
        name for name, _ in validation._dimension_statements(validation._TEMP_SCOPE_SQL)
    }
    phases: dict[str, dict[str, Any]] = {}
    for phase, lines in phase_lines.items():
        _, dimension_payloads = validation.parse_tagged_lines("\n".join(lines))
        missing = sorted(expected_names - dimension_payloads.keys())
        if missing:
            raise validation.ToolError(
                f"apply session {phase} capture lost dimension payloads: {missing}"
            )
        phases[phase] = dimension_payloads
    return actions[0], phases


def refused_finding(database: str) -> Any:
    return validation.Finding(
        code=APPLY_REFUSED_CODE,
        dimension="apply_boundary",
        kind="refused",
        object=database,
        detail={
            "expected": (
                "an empty database or an exact fresh-v2 database; the locked "
                "boundary never mutates or repairs any other state"
            )
        },
    )


def build_apply_report(
    database: str,
    action: str | None,
    findings: list[Any],
    preflight_findings: list[Any] | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    if error is not None:
        status = "error"
    elif action == ACTION_REFUSED:
        status = "refused"
    elif findings:
        status = "findings"
    else:
        status = "ready"
    report = {
        "schema_version": 1,
        "kind": APPLY_REPORT_KIND,
        "database": database,
        "profile": validation.PROFILE_FRESH_V2,
        "action": action,
        "status": status,
        "finding_count": len(findings),
        "findings": [finding.to_json() for finding in findings],
        "preflight_finding_count": (
            len(preflight_findings) if preflight_findings is not None else None
        ),
        "error": error,
    }
    validation._assert_json_safe(report)
    return report


def run_apply(template: str, database: str) -> tuple[dict[str, Any], int]:
    runner = validation.PsqlRunner(template)
    validation.require_superuser(runner, database)
    if not validation.CANONICAL_V2_DDL.is_file():
        raise validation.ToolError(
            f"canonical v2 DDL is unavailable: {validation.CANONICAL_V2_DDL}"
        )
    v2_ddl = validation.CANONICAL_V2_DDL.read_text(encoding="utf-8")
    expected = validation.derive_expected_profile(runner, validation.PROFILE_FRESH_V2)
    script = build_apply_session_script(expected, v2_ddl)
    result = runner.run(database, script, timeout=900)
    if result.returncode != 0:
        raise validation.ToolError(
            "apply session failed before reaching a terminal state "
            f"(exit {result.returncode}): "
            f"{result.stderr.strip() or result.stdout.strip()}"
        )
    action, phases = parse_session_output(result.stdout)
    preflight_findings = validation.diff_profiles(expected, phases[_PREFLIGHT_PHASE])
    postflight_findings = validation.diff_profiles(expected, phases[_POSTFLIGHT_PHASE])
    if action == ACTION_REFUSED:
        findings = preflight_findings or [refused_finding(database)]
        report = build_apply_report(
            database, action, findings, preflight_findings=preflight_findings
        )
        return report, 1
    report = build_apply_report(
        database,
        action,
        postflight_findings,
        preflight_findings=preflight_findings,
    )
    return report, 0 if not postflight_findings else 1


def emit_report(report: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, sort_keys=True, separators=(",", ":")))
        return
    print(f"database: {report['database']}")
    print(f"action: {report['action']}")
    print(f"status: {report['status']}")
    if report.get("error"):
        print(f"error: {report['error']}")
    for finding in report["findings"]:
        print(f"{finding['code']} {finding['dimension']} {finding['object']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Locked preflight/apply/postflight boundary for the canonical "
            "Hermes runtime v2 PostgreSQL DDL."
        )
    )
    parser.add_argument(
        "--psql-command",
        required=True,
        help=(
            "psql command template; must contain the literal placeholder "
            "{database} and pipe SQL over stdin"
        ),
    )
    parser.add_argument("--database", required=True, help="target database name")
    parser.add_argument("--json", action="store_true", dest="as_json")
    options = parser.parse_args(argv)

    try:
        report, exit_code = run_apply(options.psql_command, options.database)
    except validation.ToolError as error:
        report = build_apply_report(options.database, None, [], error=str(error))
        emit_report(report, options.as_json)
        return 2
    emit_report(report, options.as_json)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
