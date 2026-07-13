#!/usr/bin/env python3
"""Read-only PostgreSQL readiness and drift fingerprinting for the v2 contract.

This tool proves whether one target database matches a canonical Hermes
runtime profile without mutating or repairing anything.  The expected profile
is always derived live from the canonical DDL: the tool creates one scratch
database, applies the canonical contract file(s) inside a single transaction,
captures the catalog fingerprint, and rolls the transaction back so even
cluster-level statements (``create role`` guards, ``alter role`` hardening,
event triggers) leave no trace.  The target database is fingerprinted inside
a ``read only`` transaction.  Frozen object inventories are never used, so
the tool stays correct as the canonical surface grows.

Profiles:

- ``fresh-v2``       expected state after the v2 DDL only.
- ``v1-pre-cutover`` expected state after the v2 DDL plus the pinned v1 DDL.
- ``v1-cutover``     as above, then the canonical migration surface
  ``contracts/hermes-runtime/migrations/v1-to-v2.sql`` followed by
  ``select xfactory_runtime_v2.install_v1_freeze('profile-derivation')``,
  so a database legitimately cut over through the production migration
  path is the expected state, never drift.
  If the canonical DDL does not provide that installer its absence is
  reported as the readiness finding ``XFV2-FREEZE-INSTALLER-MISSING``
  (exit 1), never as a crash.

Fingerprint dimensions (each independently reported): schemas, tables,
columns, constraints, indexes, policies, functions, function security
(security definer plus ``proconfig`` search path), triggers, role attributes,
role memberships, ownership, ACLs, row-security enable/force flags, PUBLIC
privileges, trusted-schema writability, quarantine grants, durable v1 freeze
objects, and the quarantine dependency guard (event triggers).

Stable finding codes are ``XFV2-<DIMENSION>-<MISSING|EXTRA|ALTERED>`` plus the
operational code ``XFV2-FREEZE-INSTALLER-MISSING``.  Role membership findings
are policy-based rather than scratch-diffed because cluster membership state
is shared between the scratch and target fingerprints: any membership in a
schema-owning role and any membership edge between two canonical roles is
drift unless the canonical DDL itself created that edge.

Exit codes: 0 ready, 1 findings, 2 harness or usage error.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import re
import secrets
import shlex
import subprocess
import sys
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_V2_DDL = (
    REPOSITORY_ROOT / "contracts/hermes-runtime/hermes-operational-postgres-v2.sql"
)
CANONICAL_V1_DDL = REPOSITORY_ROOT / "contracts/schemas/hermes-operational-postgres.sql"
CANONICAL_MIGRATION_DDL = (
    REPOSITORY_ROOT / "contracts/hermes-runtime/migrations/v1-to-v2.sql"
)

PROFILE_FRESH_V2 = "fresh-v2"
PROFILE_V1_PRE_CUTOVER = "v1-pre-cutover"
PROFILE_V1_CUTOVER = "v1-cutover"
PROFILES = (PROFILE_FRESH_V2, PROFILE_V1_PRE_CUTOVER, PROFILE_V1_CUTOVER)

MAINTENANCE_DATABASE = "postgres"
DATABASE_PLACEHOLDER = "{database}"
QUARANTINE_SCHEMA = "xfactory_legacy_quarantine_v2"
FREEZE_DERIVATION_MIGRATION_ID = "profile-derivation"
SCRATCH_DATABASE_PREFIX = "xfv2_scratch_"

_SCHEMA_NAMESPACE_LIKE = "xfactory%"
_ROLE_NAMESPACE_LIKE = "xfactory\\_v2\\_%"
_CREATE_ROLE_PATTERN = re.compile(r"create role\s+([A-Za-z0-9_]+)", re.IGNORECASE)
_FREEZE_INSTALLER_MISSING_PATTERN = re.compile(
    r"function xfactory_runtime_v2\.install_v1_freeze\([^)]*\) does not exist",
    re.IGNORECASE,
)

_DIMENSION_LINE_PREFIX = "XFDIM:"
_SCOPE_LINE_PREFIX = "XFSCOPE:"

READINESS_REPORT_KIND = "openxfactory-hermes-runtime-postgres-readiness-report"


class ToolError(Exception):
    """Harness or usage failure (exit 2), never a readiness finding."""


class FreezeInstallerMissing(Exception):
    """The pinned v1-cutover freeze installer has not landed yet."""


@dataclass(frozen=True)
class Finding:
    code: str
    dimension: str
    kind: str
    object: str
    detail: dict[str, Any] | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "dimension": self.dimension,
            "kind": self.kind,
            "object": self.object,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class DimensionSpec:
    name: str
    code_stem: str
    key_fields: tuple[str, ...]
    parent: str | None = None
    parent_key_fields: tuple[str, ...] = ()
    altered_only: bool = False
    altered_code: str | None = None


DIMENSIONS: tuple[DimensionSpec, ...] = (
    DimensionSpec("schemas", "XFV2-SCHEMA", ("name",)),
    DimensionSpec("tables", "XFV2-TABLE", ("schema", "name")),
    DimensionSpec(
        "columns",
        "XFV2-COLUMN",
        ("schema", "table", "column"),
        parent="tables",
        parent_key_fields=("schema", "table"),
    ),
    DimensionSpec(
        "constraints",
        "XFV2-CONSTRAINT",
        ("schema", "table", "name"),
        parent="tables",
        parent_key_fields=("schema", "table"),
    ),
    DimensionSpec(
        "indexes",
        "XFV2-INDEX",
        ("schema", "table", "name"),
        parent="tables",
        parent_key_fields=("schema", "table"),
    ),
    DimensionSpec(
        "policies",
        "XFV2-POLICY",
        ("schema", "table", "name"),
        parent="tables",
        parent_key_fields=("schema", "table"),
    ),
    DimensionSpec("functions", "XFV2-FUNCTION", ("schema", "name", "arguments")),
    DimensionSpec(
        "function_security",
        "XFV2-FUNCTION-SECURITY",
        ("schema", "name", "arguments"),
        parent="functions",
        parent_key_fields=("schema", "name", "arguments"),
        altered_only=True,
    ),
    DimensionSpec(
        "triggers",
        "XFV2-TRIGGER",
        ("schema", "table", "name"),
        parent="tables",
        parent_key_fields=("schema", "table"),
    ),
    DimensionSpec(
        "role_attributes",
        "XFV2-ROLE",
        ("name",),
        altered_code="XFV2-ROLE-ATTRIBUTE-ALTERED",
    ),
    DimensionSpec(
        "ownership", "XFV2-OWNERSHIP", ("kind", "identity"), altered_only=True
    ),
    DimensionSpec("acls", "XFV2-ACL", ("kind", "identity"), altered_only=True),
    DimensionSpec(
        "row_security",
        "XFV2-ROW-SECURITY",
        ("schema", "table"),
        parent="tables",
        parent_key_fields=("schema", "table"),
    ),
    DimensionSpec(
        "public_privileges",
        "XFV2-PUBLIC-PRIVILEGE",
        ("kind", "identity"),
        altered_only=True,
    ),
    DimensionSpec(
        "trusted_schemas",
        "XFV2-TRUSTED-SCHEMA",
        ("schema", "role"),
        altered_only=True,
    ),
    DimensionSpec(
        "quarantine_grants",
        "XFV2-QUARANTINE-GRANT",
        ("kind", "identity", "grantee"),
    ),
    DimensionSpec("freeze", "XFV2-FREEZE", ("schema", "table", "name")),
    DimensionSpec("dependency_guard", "XFV2-DEPENDENCY-GUARD", ("name",)),
)

MEMBERSHIP_DIMENSION = "role_memberships"
MEMBERSHIP_CODE_STEM = "XFV2-ROLE-MEMBERSHIP"
FREEZE_INSTALLER_MISSING_CODE = "XFV2-FREEZE-INSTALLER-MISSING"


@dataclass(frozen=True)
class Scope:
    schemas: tuple[str, ...]
    v1_tables: tuple[tuple[str, str], ...]
    roles: tuple[str, ...]
    owner_roles: tuple[str, ...]


@dataclass
class ExpectedProfile:
    profile: str
    scope: Scope
    dimensions: dict[str, list[dict[str, Any]]]
    expected_memberships: list[dict[str, Any]] = field(default_factory=list)


def sql_literal(value: str) -> str:
    if "\x00" in value:
        raise ToolError("SQL literals must not contain NUL bytes")
    return "'" + value.replace("'", "''") + "'"


def _values_subquery(rows: list[tuple[str, ...]], columns: tuple[str, ...]) -> str:
    """Inline scope rows as a subquery with the given column names."""

    if not rows:
        null_columns = ", ".join(f"null::text as {name}" for name in columns)
        return f"select {null_columns} where false"
    rendered = ",\n      ".join(
        "(" + ", ".join(sql_literal(cell) for cell in row) + ")" for row in rows
    )
    column_list = ", ".join(columns)
    return (
        f"select {column_list} from (values\n      {rendered}\n"
        f"    ) as scope_values({column_list})"
    )


@dataclass(frozen=True)
class ScopeSQL:
    """SQL fragments yielding the fingerprint scope in either capture mode."""

    schemas: str
    v1_tables: str
    roles: str
    owner_roles: str


_TEMP_SCOPE_SQL = ScopeSQL(
    schemas="select nspname from xfv2_scope_schemas",
    v1_tables="select schema_name, table_name from xfv2_scope_v1_tables",
    roles="select rolname from xfv2_scope_roles",
    owner_roles="select rolname from xfv2_owner_roles",
)


def _inline_scope_sql(scope: Scope) -> ScopeSQL:
    return ScopeSQL(
        schemas=_values_subquery([(name,) for name in scope.schemas], ("nspname",)),
        v1_tables=_values_subquery(
            [tuple(pair) for pair in scope.v1_tables], ("schema_name", "table_name")
        ),
        roles=_values_subquery([(name,) for name in scope.roles], ("rolname",)),
        owner_roles=_values_subquery(
            [(name,) for name in scope.owner_roles], ("rolname",)
        ),
    )


def _tagged(tag: str, name: str, aggregate_sql: str) -> str:
    return (
        f"select {sql_literal(tag + name + ':')} || coalesce((\n"
        f"{aggregate_sql}\n"
        f"), '[]');"
    )


def _dimension_aggregates(scope_sql: ScopeSQL) -> list[tuple[str, str]]:
    """Return ``(dimension name, scalar jsonb-agg text SQL)`` pairs."""

    schemas = scope_sql.schemas
    v1_tables = scope_sql.v1_tables
    roles = scope_sql.roles
    owner_roles = scope_sql.owner_roles
    table_scope = (
        f"(n.nspname in ({schemas})\n"
        f"        or (n.nspname, c.relname) in ({v1_tables}))"
    )

    statements: list[tuple[str, str]] = []

    statements.append(
        (
            "schemas",
            f"""
  select jsonb_agg(jsonb_build_object('name', s.nspname) order by s.nspname)::text
  from (
    select n.nspname
    from pg_catalog.pg_namespace n
    where n.nspname in ({schemas})
       or (n.nspname like {sql_literal(_SCHEMA_NAMESPACE_LIKE)}
           and n.nspname not in ({schemas}))
  ) s
""",
        )
    )

    statements.append(
        (
            "tables",
            f"""
  select jsonb_agg(jsonb_build_object(
      'schema', t.nspname, 'name', t.relname,
      'kind', t.relkind, 'persistence', t.relpersistence
    ) order by t.nspname, t.relname)::text
  from (
    select n.nspname, c.relname, c.relkind::text as relkind,
           c.relpersistence::text as relpersistence
    from pg_catalog.pg_class c
    join pg_catalog.pg_namespace n on n.oid = c.relnamespace
    where c.relkind in ('r', 'p', 'v', 'm', 'f')
      and {table_scope}
  ) t
""",
        )
    )

    statements.append(
        (
            "columns",
            f"""
  select jsonb_agg(jsonb_build_object(
      'schema', t.nspname, 'table', t.relname, 'column', t.attname,
      'position', t.attnum, 'type', t.column_type, 'not_null', t.attnotnull,
      'default', t.default_expr, 'identity', t.attidentity,
      'generated', t.attgenerated
    ) order by t.nspname, t.relname, t.attnum)::text
  from (
    select n.nspname, c.relname, a.attname, a.attnum,
           pg_catalog.format_type(a.atttypid, a.atttypmod) as column_type,
           a.attnotnull,
           pg_catalog.pg_get_expr(ad.adbin, ad.adrelid) as default_expr,
           a.attidentity::text as attidentity,
           a.attgenerated::text as attgenerated
    from pg_catalog.pg_attribute a
    join pg_catalog.pg_class c on c.oid = a.attrelid
    join pg_catalog.pg_namespace n on n.oid = c.relnamespace
    left join pg_catalog.pg_attrdef ad
      on ad.adrelid = a.attrelid and ad.adnum = a.attnum
    where a.attnum > 0 and not a.attisdropped
      and c.relkind in ('r', 'p', 'v', 'm', 'f')
      and {table_scope}
  ) t
""",
        )
    )

    statements.append(
        (
            "constraints",
            f"""
  select jsonb_agg(jsonb_build_object(
      'schema', t.nspname, 'table', t.relname, 'name', t.conname,
      'definition', t.definition
    ) order by t.nspname, t.relname, t.conname)::text
  from (
    select n.nspname, c.relname, con.conname,
           pg_catalog.pg_get_constraintdef(con.oid) as definition
    from pg_catalog.pg_constraint con
    join pg_catalog.pg_class c on c.oid = con.conrelid
    join pg_catalog.pg_namespace n on n.oid = c.relnamespace
    where {table_scope}
  ) t
""",
        )
    )

    statements.append(
        (
            "indexes",
            f"""
  select jsonb_agg(jsonb_build_object(
      'schema', t.schemaname, 'table', t.tablename, 'name', t.indexname,
      'definition', t.indexdef
    ) order by t.schemaname, t.tablename, t.indexname)::text
  from (
    select i.schemaname, i.tablename, i.indexname, i.indexdef
    from pg_catalog.pg_indexes i
    where i.schemaname in ({schemas})
       or (i.schemaname, i.tablename) in ({v1_tables})
  ) t
""",
        )
    )

    statements.append(
        (
            "policies",
            f"""
  select jsonb_agg(jsonb_build_object(
      'schema', t.schemaname, 'table', t.tablename, 'name', t.policyname,
      'permissive', t.permissive, 'command', t.cmd, 'roles', t.role_list,
      'using', t.qual, 'with_check', t.with_check
    ) order by t.schemaname, t.tablename, t.policyname)::text
  from (
    select p.schemaname, p.tablename, p.policyname, p.permissive, p.cmd,
           (select pg_catalog.array_agg(role_name order by role_name)
            from pg_catalog.unnest(p.roles) role_name)::text as role_list,
           p.qual, p.with_check
    from pg_catalog.pg_policies p
    where p.schemaname in ({schemas})
  ) t
""",
        )
    )

    statements.append(
        (
            "functions",
            f"""
  select jsonb_agg(jsonb_build_object(
      'schema', t.nspname, 'name', t.proname, 'arguments', t.arguments,
      'returns', t.returns, 'language', t.language, 'kind', t.prokind,
      'volatility', t.provolatile, 'strict', t.proisstrict,
      'definition_sha256', t.definition_sha256
    ) order by t.nspname, t.proname, t.arguments)::text
  from (
    select n.nspname, p.proname,
           pg_catalog.pg_get_function_identity_arguments(p.oid) as arguments,
           pg_catalog.pg_get_function_result(p.oid) as returns,
           l.lanname::text as language, p.prokind::text as prokind,
           p.provolatile::text as provolatile, p.proisstrict,
           pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(
             pg_catalog.pg_get_functiondef(p.oid), 'UTF8')), 'hex')
             as definition_sha256
    from pg_catalog.pg_proc p
    join pg_catalog.pg_namespace n on n.oid = p.pronamespace
    join pg_catalog.pg_language l on l.oid = p.prolang
    where n.nspname in ({schemas}) and p.prokind in ('f', 'p')
  ) t
""",
        )
    )

    statements.append(
        (
            "function_security",
            f"""
  select jsonb_agg(jsonb_build_object(
      'schema', t.nspname, 'name', t.proname, 'arguments', t.arguments,
      'security_definer', t.prosecdef, 'config', t.config
    ) order by t.nspname, t.proname, t.arguments)::text
  from (
    select n.nspname, p.proname,
           pg_catalog.pg_get_function_identity_arguments(p.oid) as arguments,
           p.prosecdef,
           (select pg_catalog.array_agg(cfg order by cfg)
            from pg_catalog.unnest(
              coalesce(p.proconfig, array[]::text[])) cfg)::text as config
    from pg_catalog.pg_proc p
    join pg_catalog.pg_namespace n on n.oid = p.pronamespace
    where n.nspname in ({schemas}) and p.prokind in ('f', 'p')
  ) t
""",
        )
    )

    statements.append(
        (
            "triggers",
            f"""
  select jsonb_agg(jsonb_build_object(
      'schema', t.nspname, 'table', t.relname, 'name', t.tgname,
      'enabled', t.tgenabled, 'definition', t.definition
    ) order by t.nspname, t.relname, t.tgname)::text
  from (
    select n.nspname, c.relname, g.tgname, g.tgenabled::text as tgenabled,
           pg_catalog.pg_get_triggerdef(g.oid) as definition
    from pg_catalog.pg_trigger g
    join pg_catalog.pg_class c on c.oid = g.tgrelid
    join pg_catalog.pg_namespace n on n.oid = c.relnamespace
    where not g.tgisinternal and n.nspname in ({schemas})
  ) t
""",
        )
    )

    statements.append(
        (
            "role_attributes",
            f"""
  select jsonb_agg(jsonb_build_object(
      'name', t.rolname, 'superuser', t.rolsuper, 'inherit', t.rolinherit,
      'create_role', t.rolcreaterole, 'create_db', t.rolcreatedb,
      'can_login', t.rolcanlogin, 'replication', t.rolreplication,
      'bypass_rls', t.rolbypassrls
    ) order by t.rolname)::text
  from (
    select r.rolname, r.rolsuper, r.rolinherit, r.rolcreaterole,
           r.rolcreatedb, r.rolcanlogin, r.rolreplication, r.rolbypassrls
    from pg_catalog.pg_roles r
    where r.rolname in ({roles})
       or (r.rolname like {sql_literal(_ROLE_NAMESPACE_LIKE)} escape '\\'
           and r.rolname not in ({roles}))
  ) t
""",
        )
    )

    statements.append(
        (
            MEMBERSHIP_DIMENSION,
            f"""
  select jsonb_agg(jsonb_build_object(
      'member', t.member, 'granted', t.granted, 'admin', t.admin_option
    ) order by t.member, t.granted)::text
  from (
    select m.rolname as member, g.rolname as granted, am.admin_option
    from pg_catalog.pg_auth_members am
    join pg_catalog.pg_roles g on g.oid = am.roleid
    join pg_catalog.pg_roles m on m.oid = am.member
    where g.rolname in ({owner_roles})
       or (g.rolname in ({roles}) and m.rolname in ({roles}))
  ) t
""",
        )
    )

    statements.append(
        (
            "ownership",
            f"""
  select jsonb_agg(jsonb_build_object(
      'kind', t.kind, 'identity', t.identity, 'owner', t.owner
    ) order by t.kind, t.identity)::text
  from (
    select 'schema' as kind, n.nspname as identity,
           pg_catalog.pg_get_userbyid(n.nspowner) as owner
    from pg_catalog.pg_namespace n
    where n.nspname in ({schemas})
    union all
    select 'table', n.nspname || '.' || c.relname,
           pg_catalog.pg_get_userbyid(c.relowner)
    from pg_catalog.pg_class c
    join pg_catalog.pg_namespace n on n.oid = c.relnamespace
    where c.relkind in ('r', 'p', 'v', 'm', 'f')
      and {table_scope}
    union all
    select 'function',
           n.nspname || '.' || p.proname || '(' ||
             pg_catalog.pg_get_function_identity_arguments(p.oid) || ')',
           pg_catalog.pg_get_userbyid(p.proowner)
    from pg_catalog.pg_proc p
    join pg_catalog.pg_namespace n on n.oid = p.pronamespace
    where n.nspname in ({schemas}) and p.prokind in ('f', 'p')
  ) t
""",
        )
    )

    statements.append(
        (
            "acls",
            f"""
  select jsonb_agg(jsonb_build_object(
      'kind', t.kind, 'identity', t.identity, 'acl', t.acl
    ) order by t.kind, t.identity)::text
  from (
    select 'schema' as kind, n.nspname as identity,
           case when n.nspacl is null then '<default>'
                else (select pg_catalog.array_agg(a::text order by a::text)
                      from pg_catalog.unnest(n.nspacl) a)::text
           end as acl
    from pg_catalog.pg_namespace n
    where n.nspname in ({schemas})
    union all
    select 'table', n.nspname || '.' || c.relname,
           case when c.relacl is null then '<default>'
                else (select pg_catalog.array_agg(a::text order by a::text)
                      from pg_catalog.unnest(c.relacl) a)::text
           end
    from pg_catalog.pg_class c
    join pg_catalog.pg_namespace n on n.oid = c.relnamespace
    where c.relkind in ('r', 'p', 'v', 'm', 'f')
      and {table_scope}
    union all
    select 'function',
           n.nspname || '.' || p.proname || '(' ||
             pg_catalog.pg_get_function_identity_arguments(p.oid) || ')',
           case when p.proacl is null then '<default>'
                else (select pg_catalog.array_agg(a::text order by a::text)
                      from pg_catalog.unnest(p.proacl) a)::text
           end
    from pg_catalog.pg_proc p
    join pg_catalog.pg_namespace n on n.oid = p.pronamespace
    where n.nspname in ({schemas}) and p.prokind in ('f', 'p')
  ) t
""",
        )
    )

    statements.append(
        (
            "row_security",
            f"""
  select jsonb_agg(jsonb_build_object(
      'schema', t.nspname, 'table', t.relname,
      'row_security', t.relrowsecurity, 'force_row_security',
      t.relforcerowsecurity
    ) order by t.nspname, t.relname)::text
  from (
    select n.nspname, c.relname, c.relrowsecurity, c.relforcerowsecurity
    from pg_catalog.pg_class c
    join pg_catalog.pg_namespace n on n.oid = c.relnamespace
    where c.relkind in ('r', 'p')
      and {table_scope}
  ) t
""",
        )
    )

    statements.append(
        (
            "public_privileges",
            f"""
  select jsonb_agg(jsonb_build_object(
      'kind', t.kind, 'identity', t.identity,
      'public_privileges', t.public_privileges
    ) order by t.kind, t.identity)::text
  from (
    select 'schema' as kind, n.nspname as identity,
           coalesce((select pg_catalog.array_agg(
                e.privilege_type order by e.privilege_type)
             from pg_catalog.aclexplode(coalesce(
               n.nspacl, pg_catalog.acldefault('n', n.nspowner))) e
             where e.grantee = 0), array[]::text[])::text
             as public_privileges
    from pg_catalog.pg_namespace n
    where n.nspname in ({schemas})
    union all
    select 'table', n.nspname || '.' || c.relname,
           coalesce((select pg_catalog.array_agg(
                e.privilege_type order by e.privilege_type)
             from pg_catalog.aclexplode(coalesce(
               c.relacl, pg_catalog.acldefault('r', c.relowner))) e
             where e.grantee = 0), array[]::text[])::text
    from pg_catalog.pg_class c
    join pg_catalog.pg_namespace n on n.oid = c.relnamespace
    where c.relkind in ('r', 'p', 'v', 'm', 'f')
      and {table_scope}
    union all
    select 'function',
           n.nspname || '.' || p.proname || '(' ||
             pg_catalog.pg_get_function_identity_arguments(p.oid) || ')',
           coalesce((select pg_catalog.array_agg(
                e.privilege_type order by e.privilege_type)
             from pg_catalog.aclexplode(coalesce(
               p.proacl, pg_catalog.acldefault('f', p.proowner))) e
             where e.grantee = 0), array[]::text[])::text
    from pg_catalog.pg_proc p
    join pg_catalog.pg_namespace n on n.oid = p.pronamespace
    where n.nspname in ({schemas}) and p.prokind in ('f', 'p')
  ) t
""",
        )
    )

    statements.append(
        (
            "trusted_schemas",
            f"""
  select jsonb_agg(jsonb_build_object(
      'schema', t.schema_name, 'role', t.rolname, 'can_create', t.can_create
    ) order by t.schema_name, t.rolname)::text
  from (
    with function_config as (
      select pg_catalog.unnest(p.proconfig) as entry
      from pg_catalog.pg_proc p
      join pg_catalog.pg_namespace n on n.oid = p.pronamespace
      where n.nspname in ({schemas}) and p.proconfig is not null
    ),
    search_path_schemas as (
      select pg_catalog.btrim(token, ' "') as schema_name
      from function_config,
           lateral pg_catalog.regexp_split_to_table(
             pg_catalog.substring(entry, '^search_path=(.*)$'), ',') token
      where entry like 'search\\_path=%' escape '\\'
    ),
    trusted as (
      select distinct candidate.schema_name
      from (
        select schema_name from search_path_schemas
        union
        select nspname from pg_catalog.pg_namespace
        where nspname in ({schemas})
      ) candidate
      where exists (
        select 1 from pg_catalog.pg_namespace present
        where present.nspname = candidate.schema_name
      )
    )
    select trusted.schema_name, scoped_role.rolname,
           pg_catalog.has_schema_privilege(
             scoped_role.rolname, trusted.schema_name, 'create') as can_create
    from trusted
    cross join (
      select r.rolname from pg_catalog.pg_roles r
      where r.rolname in ({roles})
    ) scoped_role
  ) t
""",
        )
    )

    quarantine_literal = sql_literal(QUARANTINE_SCHEMA)
    statements.append(
        (
            "quarantine_grants",
            f"""
  select jsonb_agg(jsonb_build_object(
      'kind', t.kind, 'identity', t.identity, 'grantee', t.grantee,
      'privileges', t.privileges
    ) order by t.kind, t.identity, t.grantee)::text
  from (
    select entries.kind, entries.identity,
           case when entries.grantee = 0 then 'public'
                else pg_catalog.pg_get_userbyid(entries.grantee)
           end as grantee,
           (select pg_catalog.array_agg(p order by p)
            from pg_catalog.unnest(entries.privilege_list) p)::text
             as privileges
    from (
      select 'schema' as kind, n.nspname as identity, e.grantee,
             pg_catalog.array_agg(e.privilege_type) as privilege_list
      from pg_catalog.pg_namespace n,
           lateral pg_catalog.aclexplode(coalesce(
             n.nspacl, pg_catalog.acldefault('n', n.nspowner))) e
      where n.nspname = {quarantine_literal}
        and n.nspname in ({schemas})
      group by n.nspname, e.grantee
      union all
      select 'table', n.nspname || '.' || c.relname, e.grantee,
             pg_catalog.array_agg(e.privilege_type)
      from pg_catalog.pg_class c
      join pg_catalog.pg_namespace n on n.oid = c.relnamespace,
           lateral pg_catalog.aclexplode(coalesce(
             c.relacl, pg_catalog.acldefault('r', c.relowner))) e
      where c.relkind in ('r', 'p', 'v', 'm', 'f')
        and n.nspname = {quarantine_literal}
        and n.nspname in ({schemas})
      group by n.nspname, c.relname, e.grantee
      union all
      select 'function',
             n.nspname || '.' || p.proname || '(' ||
               pg_catalog.pg_get_function_identity_arguments(p.oid) || ')',
             e.grantee, pg_catalog.array_agg(e.privilege_type)
      from pg_catalog.pg_proc p
      join pg_catalog.pg_namespace n on n.oid = p.pronamespace,
           lateral pg_catalog.aclexplode(coalesce(
             p.proacl, pg_catalog.acldefault('f', p.proowner))) e
      where p.prokind in ('f', 'p')
        and n.nspname = {quarantine_literal}
        and n.nspname in ({schemas})
      group by n.nspname, p.proname, p.oid, e.grantee
    ) entries
  ) t
""",
        )
    )

    statements.append(
        (
            "freeze",
            f"""
  select jsonb_agg(jsonb_build_object(
      'schema', t.nspname, 'table', t.relname, 'name', t.tgname,
      'enabled', t.tgenabled, 'trigger_type', t.tgtype,
      'function', t.trigger_function
    ) order by t.nspname, t.relname, t.tgname)::text
  from (
    select n.nspname, c.relname, g.tgname, g.tgenabled::text as tgenabled,
           g.tgtype::int as tgtype,
           fn_schema.nspname || '.' || fp.proname as trigger_function
    from pg_catalog.pg_trigger g
    join pg_catalog.pg_class c on c.oid = g.tgrelid
    join pg_catalog.pg_namespace n on n.oid = c.relnamespace
    join pg_catalog.pg_proc fp on fp.oid = g.tgfoid
    join pg_catalog.pg_namespace fn_schema on fn_schema.oid = fp.pronamespace
    where not g.tgisinternal
      and (n.nspname, c.relname) in ({v1_tables})
  ) t
""",
        )
    )

    statements.append(
        (
            "dependency_guard",
            """
  select jsonb_agg(jsonb_build_object(
      'name', t.evtname, 'event', t.evtevent, 'enabled', t.evtenabled,
      'function', t.guard_function, 'tags', t.tags
    ) order by t.evtname)::text
  from (
    select e.evtname, e.evtevent, e.evtenabled::text as evtenabled,
           n.nspname || '.' || p.proname as guard_function,
           (select pg_catalog.array_agg(tag order by tag)
            from pg_catalog.unnest(
              coalesce(e.evttags, array[]::text[])) tag)::text as tags
    from pg_catalog.pg_event_trigger e
    join pg_catalog.pg_proc p on p.oid = e.evtfoid
    join pg_catalog.pg_namespace n on n.oid = p.pronamespace
  ) t
""",
        )
    )

    return statements


def _dimension_statements(scope_sql: ScopeSQL) -> list[tuple[str, str]]:
    """Return ``(dimension name, one-row tagged SQL statement)`` pairs."""

    return [
        (name, _tagged(_DIMENSION_LINE_PREFIX, name, aggregate.rstrip()))
        for name, aggregate in _dimension_aggregates(scope_sql)
    ]


def _scope_emission_statements() -> str:
    parts = [
        _tagged(
            _SCOPE_LINE_PREFIX,
            "schemas",
            """
  select jsonb_agg(nspname order by nspname)::text
  from xfv2_scope_schemas
""".rstrip(),
        ),
        _tagged(
            _SCOPE_LINE_PREFIX,
            "v1_tables",
            """
  select jsonb_agg(jsonb_build_object(
      'schema', schema_name, 'table', table_name
    ) order by schema_name, table_name)::text
  from xfv2_scope_v1_tables
""".rstrip(),
        ),
        _tagged(
            _SCOPE_LINE_PREFIX,
            "roles",
            """
  select jsonb_agg(rolname order by rolname)::text
  from xfv2_scope_roles
""".rstrip(),
        ),
        _tagged(
            _SCOPE_LINE_PREFIX,
            "owner_roles",
            """
  select jsonb_agg(rolname order by rolname)::text
  from xfv2_owner_roles
""".rstrip(),
        ),
        _tagged(
            _SCOPE_LINE_PREFIX,
            "expected_memberships",
            """
  select jsonb_agg(jsonb_build_object(
      'member', member_name, 'granted', role_name, 'admin', admin_option
    ) order by member_name, role_name)::text
  from xfv2_expected_memberships
""".rstrip(),
        ),
    ]
    return "\n".join(parts)


def declared_role_names(ddl_text: str) -> tuple[str, ...]:
    return tuple(
        sorted({match.lower() for match in _CREATE_ROLE_PATTERN.findall(ddl_text)})
    )


def build_scratch_script(
    profile: str,
    v2_ddl: str,
    v1_ddl: str | None,
    migration_ddl: str | None = None,
) -> str:
    """One transaction: snapshot, apply canonical DDL, fingerprint, roll back."""

    declared = declared_role_names(v2_ddl) + (
        declared_role_names(v1_ddl) if v1_ddl else ()
    )
    declared_values = _values_subquery(
        [(name,) for name in sorted(set(declared))], ("rolname",)
    )

    sections: list[str] = ["begin;"]
    sections.append("""
create temporary table xfv2_pre_schemas on commit drop as
  select n.nspname from pg_catalog.pg_namespace n;
create temporary table xfv2_pre_relations on commit drop as
  select n.nspname, c.relname
  from pg_catalog.pg_class c
  join pg_catalog.pg_namespace n on n.oid = c.relnamespace
  where c.relkind in ('r', 'p');
create temporary table xfv2_pre_roles on commit drop as
  select r.rolname from pg_catalog.pg_roles r;
create temporary table xfv2_pre_members on commit drop as
  select m.rolname as member_name, g.rolname as role_name, am.admin_option
  from pg_catalog.pg_auth_members am
  join pg_catalog.pg_roles g on g.oid = am.roleid
  join pg_catalog.pg_roles m on m.oid = am.member;
""".strip())
    sections.append(v2_ddl)
    # The canonical v2 DDL leaves session state behind (its `set role` is
    # reset, but `set search_path = pg_catalog, xfactory_runtime_v2` is not).
    # Normalize both so the pinned v1 DDL creates its unqualified
    # `public.hermes_*` tables exactly where a fresh-connection apply would.
    sections.append("reset role;\nreset search_path;")
    if profile in (PROFILE_V1_PRE_CUTOVER, PROFILE_V1_CUTOVER):
        if v1_ddl is None:
            raise ToolError("the pinned v1 DDL is required for v1 profiles")
        sections.append(v1_ddl)
    if profile == PROFILE_V1_CUTOVER:
        if migration_ddl is None:
            raise ToolError(
                "the canonical migration DDL is required for the v1-cutover profile"
            )
        # The ratified migration surface is published contract and the durable
        # freeze exists only through it, so its helper functions and grants
        # are canonical post-cutover state, not drift.  Normalize the session
        # state it leaves behind before the freeze call, exactly as after the
        # v2 DDL.
        sections.append(migration_ddl)
        sections.append("reset role;\nreset search_path;")
        sections.append(
            "select xfactory_runtime_v2.install_v1_freeze("
            f"{sql_literal(FREEZE_DERIVATION_MIGRATION_ID)});"
        )
    sections.append(f"""
create temporary table xfv2_scope_schemas on commit drop as
  select n.nspname from pg_catalog.pg_namespace n
  where n.nspname not in (select nspname from xfv2_pre_schemas)
    and n.nspname not like 'pg\\_%' escape '\\'
    and n.nspname <> 'information_schema';
create temporary table xfv2_scope_v1_tables on commit drop as
  select n.nspname as schema_name, c.relname as table_name
  from pg_catalog.pg_class c
  join pg_catalog.pg_namespace n on n.oid = c.relnamespace
  where c.relkind in ('r', 'p')
    and n.nspname not in (select nspname from xfv2_scope_schemas)
    and n.nspname not like 'pg\\_%' escape '\\'
    and n.nspname <> 'information_schema'
    and (n.nspname, c.relname) not in
      (select nspname, relname from xfv2_pre_relations);
create temporary table xfv2_scope_roles on commit drop as
  select r.rolname from pg_catalog.pg_roles r
  where r.rolname in ({declared_values})
  union
  select r.rolname from pg_catalog.pg_roles r
  where r.rolname not in (select rolname from xfv2_pre_roles)
  union
  select pg_catalog.pg_get_userbyid(n.nspowner)
  from pg_catalog.pg_namespace n
  where n.nspname in (select nspname from xfv2_scope_schemas);
create temporary table xfv2_owner_roles on commit drop as
  select distinct pg_catalog.pg_get_userbyid(n.nspowner) as rolname
  from pg_catalog.pg_namespace n
  where n.nspname in (select nspname from xfv2_scope_schemas);
create temporary table xfv2_expected_memberships on commit drop as
  select m.rolname as member_name, g.rolname as role_name, am.admin_option
  from pg_catalog.pg_auth_members am
  join pg_catalog.pg_roles g on g.oid = am.roleid
  join pg_catalog.pg_roles m on m.oid = am.member
  where (m.rolname, g.rolname) not in
    (select member_name, role_name from xfv2_pre_members);
""".strip())
    sections.append(_scope_emission_statements())
    sections.append(
        "\n".join(statement for _, statement in _dimension_statements(_TEMP_SCOPE_SQL))
    )
    sections.append("rollback;")
    return "\n".join(sections) + "\n"


def build_target_capture_script(scope: Scope) -> str:
    """Read-only fingerprint of the connected database for the given scope."""

    scope_sql = _inline_scope_sql(scope)
    body = "\n".join(statement for _, statement in _dimension_statements(scope_sql))
    return f"begin;\nset transaction read only;\n{body}\nrollback;\n"


def parse_tagged_lines(stdout: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Split psql output into scope payloads and dimension payloads."""

    scope_payloads: dict[str, Any] = {}
    dimension_payloads: dict[str, Any] = {}
    for line in stdout.splitlines():
        stripped = line.strip()
        for prefix, sink in (
            (_SCOPE_LINE_PREFIX, scope_payloads),
            (_DIMENSION_LINE_PREFIX, dimension_payloads),
        ):
            if stripped.startswith(prefix):
                name, _, payload = stripped[len(prefix) :].partition(":")
                try:
                    sink[name] = json.loads(payload)
                except json.JSONDecodeError as error:
                    raise ToolError(
                        f"unparseable fingerprint payload for {name}: {error}"
                    ) from error
    return scope_payloads, dimension_payloads


class PsqlRunner:
    """Run SQL through the injected psql command template, one call per script."""

    def __init__(self, template: str, environment: dict[str, str] | None = None):
        arguments = shlex.split(template)
        if not any(DATABASE_PLACEHOLDER in argument for argument in arguments):
            raise ToolError(
                "--psql-command must contain the literal placeholder {database}"
            )
        self._arguments = arguments
        self._environment = environment

    def argv(self, database: str) -> list[str]:
        return [
            argument.replace(DATABASE_PLACEHOLDER, database)
            for argument in self._arguments
        ]

    def run(
        self, database: str, sql: str, *, timeout: float = 300.0
    ) -> subprocess.CompletedProcess[str]:
        try:
            return subprocess.run(
                self.argv(database),
                input=sql,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=self._environment,
                check=False,
            )
        except FileNotFoundError as error:
            raise ToolError(f"psql command is unavailable: {error}") from error
        except subprocess.TimeoutExpired as error:
            raise ToolError(
                f"psql call against {database!r} timed out after {timeout}s"
            ) from error

    def run_checked(
        self, database: str, sql: str, *, timeout: float = 300.0, action: str
    ) -> subprocess.CompletedProcess[str]:
        result = self.run(database, sql, timeout=timeout)
        if result.returncode != 0:
            raise ToolError(
                f"{action} failed (exit {result.returncode}): "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )
        return result


def require_superuser(runner: PsqlRunner, database: str) -> None:
    result = runner.run_checked(
        database,
        "select 'XFSUPER:' || current_setting('is_superuser');\n",
        timeout=60,
        action=f"connection probe against {database!r}",
    )
    flags = [
        line.strip()[len("XFSUPER:") :]
        for line in result.stdout.splitlines()
        if line.strip().startswith("XFSUPER:")
    ]
    if flags != ["on"]:
        raise ToolError(
            "the canonical DDL boundary requires a superuser session "
            f"(is_superuser={flags or ['unknown']})"
        )


def _scratch_database_name() -> str:
    return f"{SCRATCH_DATABASE_PREFIX}{os.getpid()}_{secrets.token_hex(4)}"


def derive_expected_profile(runner: PsqlRunner, profile: str) -> ExpectedProfile:
    """Create a scratch database, derive the canonical profile, drop scratch.

    Every cluster-level statement in the canonical DDL runs inside a rolled
    back transaction, so profile derivation never repairs or mutates shared
    role or event-trigger state before the target comparison.
    """

    if profile not in PROFILES:
        raise ToolError(f"unknown profile {profile!r}")
    if not CANONICAL_V2_DDL.is_file():
        raise ToolError(f"canonical v2 DDL is unavailable: {CANONICAL_V2_DDL}")
    v2_ddl = CANONICAL_V2_DDL.read_text(encoding="utf-8")
    v1_ddl: str | None = None
    if profile in (PROFILE_V1_PRE_CUTOVER, PROFILE_V1_CUTOVER):
        if not CANONICAL_V1_DDL.is_file():
            raise ToolError(f"pinned v1 DDL is unavailable: {CANONICAL_V1_DDL}")
        v1_ddl = CANONICAL_V1_DDL.read_text(encoding="utf-8")
    migration_ddl: str | None = None
    if profile == PROFILE_V1_CUTOVER:
        if not CANONICAL_MIGRATION_DDL.is_file():
            raise ToolError(
                f"canonical migration DDL is unavailable: {CANONICAL_MIGRATION_DDL}"
            )
        migration_ddl = CANONICAL_MIGRATION_DDL.read_text(encoding="utf-8")

    script = build_scratch_script(profile, v2_ddl, v1_ddl, migration_ddl)
    scratch = _scratch_database_name()
    runner.run_checked(
        MAINTENANCE_DATABASE,
        f'create database "{scratch}";\n',
        timeout=120,
        action="scratch database creation",
    )
    try:
        result = runner.run(scratch, script, timeout=600)
        if result.returncode != 0:
            if (
                profile == PROFILE_V1_CUTOVER
                and _FREEZE_INSTALLER_MISSING_PATTERN.search(result.stderr or "")
            ):
                raise FreezeInstallerMissing(result.stderr.strip())
            raise ToolError(
                "canonical profile derivation failed "
                f"(exit {result.returncode}): {result.stderr.strip()}"
            )
        scope_payloads, dimension_payloads = parse_tagged_lines(result.stdout)
    finally:
        runner.run(
            MAINTENANCE_DATABASE,
            f'drop database if exists "{scratch}" with (force);\n',
            timeout=120,
        )

    required_scope = {
        "schemas",
        "v1_tables",
        "roles",
        "owner_roles",
        "expected_memberships",
    }
    missing_scope = sorted(required_scope - scope_payloads.keys())
    if missing_scope:
        raise ToolError(f"scratch derivation lost scope payloads: {missing_scope}")
    expected_dimension_names = {
        name for name, _ in _dimension_statements(_TEMP_SCOPE_SQL)
    }
    missing_dimensions = sorted(expected_dimension_names - dimension_payloads.keys())
    if missing_dimensions:
        raise ToolError(
            f"scratch derivation lost dimension payloads: {missing_dimensions}"
        )

    scope = Scope(
        schemas=tuple(scope_payloads["schemas"]),
        v1_tables=tuple(
            (entry["schema"], entry["table"]) for entry in scope_payloads["v1_tables"]
        ),
        roles=tuple(scope_payloads["roles"]),
        owner_roles=tuple(scope_payloads["owner_roles"]),
    )
    memberships = scope_payloads["expected_memberships"]
    dimensions = {
        name: dimension_payloads[name]
        for name in expected_dimension_names
        if name != MEMBERSHIP_DIMENSION
    }
    return ExpectedProfile(
        profile=profile,
        scope=scope,
        dimensions=dimensions,
        expected_memberships=memberships,
    )


def capture_target_fingerprint(
    runner: PsqlRunner, database: str, scope: Scope
) -> dict[str, list[dict[str, Any]]]:
    result = runner.run_checked(
        database,
        build_target_capture_script(scope),
        timeout=300,
        action=f"target fingerprint capture against {database!r}",
    )
    _, dimension_payloads = parse_tagged_lines(result.stdout)
    expected_names = {name for name, _ in _dimension_statements(_TEMP_SCOPE_SQL)}
    missing = sorted(expected_names - dimension_payloads.keys())
    if missing:
        raise ToolError(f"target capture lost dimension payloads: {missing}")
    return dimension_payloads


def _row_key(row: dict[str, Any], fields: tuple[str, ...]) -> tuple[Any, ...]:
    return tuple(row.get(field_name) for field_name in fields)


def _object_label(key: tuple[Any, ...]) -> str:
    return ":".join(str(part) for part in key)


def _code_for(spec: DimensionSpec, kind: str) -> str:
    if kind == "altered" and spec.altered_code is not None:
        return spec.altered_code
    return f"{spec.code_stem}-{kind.upper()}"


def _diff_dimension(
    spec: DimensionSpec,
    expected_rows: list[dict[str, Any]],
    observed_rows: list[dict[str, Any]],
    shared_parents: dict[str, set[tuple[Any, ...]]],
) -> list[Finding]:
    expected_by_key = {_row_key(row, spec.key_fields): row for row in expected_rows}
    observed_by_key = {_row_key(row, spec.key_fields): row for row in observed_rows}

    def parent_present(row: dict[str, Any]) -> bool:
        if spec.parent is None:
            return True
        parent_keys = shared_parents.get(spec.parent)
        if parent_keys is None:
            return True
        return _row_key(row, spec.parent_key_fields) in parent_keys

    findings: list[Finding] = []
    for key in sorted(
        expected_by_key.keys() | observed_by_key.keys(),
        key=lambda item: tuple(str(part) for part in item),
    ):
        expected_row = expected_by_key.get(key)
        observed_row = observed_by_key.get(key)
        if expected_row is None:
            if spec.altered_only or not parent_present(observed_row):
                continue
            findings.append(
                Finding(
                    code=_code_for(spec, "extra"),
                    dimension=spec.name,
                    kind="extra",
                    object=_object_label(key),
                    detail={"observed": observed_row},
                )
            )
        elif observed_row is None:
            if spec.altered_only or not parent_present(expected_row):
                continue
            findings.append(
                Finding(
                    code=_code_for(spec, "missing"),
                    dimension=spec.name,
                    kind="missing",
                    object=_object_label(key),
                    detail={"expected": expected_row},
                )
            )
        else:
            changed = {
                field_name: {
                    "expected": expected_row.get(field_name),
                    "observed": observed_row.get(field_name),
                }
                for field_name in sorted(expected_row.keys() | observed_row.keys())
                if expected_row.get(field_name) != observed_row.get(field_name)
            }
            if changed:
                findings.append(
                    Finding(
                        code=_code_for(spec, "altered"),
                        dimension=spec.name,
                        kind="altered",
                        object=_object_label(key),
                        detail=changed,
                    )
                )
    return findings


def _membership_findings(
    expected_memberships: list[dict[str, Any]],
    observed_memberships: list[dict[str, Any]],
) -> list[Finding]:
    def edge(row: dict[str, Any]) -> tuple[Any, Any, Any]:
        return (row.get("member"), row.get("granted"), row.get("admin"))

    expected_edges = {
        (
            row.get("member_name", row.get("member")),
            row.get("role_name", row.get("granted")),
            row.get("admin_option", row.get("admin")),
        )
        for row in expected_memberships
    }
    observed_edges = {edge(row) for row in observed_memberships}

    findings: list[Finding] = []
    for member, granted, admin in sorted(
        observed_edges - expected_edges, key=lambda item: tuple(str(p) for p in item)
    ):
        findings.append(
            Finding(
                code=f"{MEMBERSHIP_CODE_STEM}-EXTRA",
                dimension=MEMBERSHIP_DIMENSION,
                kind="extra",
                object=f"{member}:{granted}",
                detail={
                    "observed": {"member": member, "granted": granted, "admin": admin}
                },
            )
        )
    for member, granted, admin in sorted(
        expected_edges - observed_edges, key=lambda item: tuple(str(p) for p in item)
    ):
        findings.append(
            Finding(
                code=f"{MEMBERSHIP_CODE_STEM}-MISSING",
                dimension=MEMBERSHIP_DIMENSION,
                kind="missing",
                object=f"{member}:{granted}",
                detail={
                    "expected": {"member": member, "granted": granted, "admin": admin}
                },
            )
        )
    return findings


def diff_profiles(
    expected: ExpectedProfile, observed: dict[str, list[dict[str, Any]]]
) -> list[Finding]:
    shared_parents: dict[str, set[tuple[Any, ...]]] = {}
    for parent_name, parent_keys in (
        ("tables", ("schema", "name")),
        ("functions", ("schema", "name", "arguments")),
    ):
        expected_rows = expected.dimensions.get(parent_name, [])
        observed_rows = observed.get(parent_name, [])
        shared_parents[parent_name] = {
            _row_key(row, parent_keys) for row in expected_rows
        } & {_row_key(row, parent_keys) for row in observed_rows}

    findings: list[Finding] = []
    for spec in DIMENSIONS:
        findings.extend(
            _diff_dimension(
                spec,
                expected.dimensions.get(spec.name, []),
                observed.get(spec.name, []),
                shared_parents,
            )
        )
    findings.extend(
        _membership_findings(
            expected.expected_memberships, observed.get(MEMBERSHIP_DIMENSION, [])
        )
    )
    return sorted(findings, key=lambda f: (f.dimension, f.object, f.code))


def freeze_installer_missing_finding() -> Finding:
    return Finding(
        code=FREEZE_INSTALLER_MISSING_CODE,
        dimension="freeze",
        kind="missing",
        object="xfactory_runtime_v2.install_v1_freeze",
        detail={
            "expected": (
                "callable xfactory_runtime_v2.install_v1_freeze(text) so the "
                "v1-cutover profile can be derived from the canonical DDL"
            )
        },
    )


def _assert_json_safe(value: Any, path: str = "$") -> None:
    if isinstance(value, float):
        raise ToolError(f"floating-point value forbidden in report at {path}")
    if isinstance(value, dict):
        for key, item in value.items():
            _assert_json_safe(item, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _assert_json_safe(item, f"{path}[{index}]")


def build_readiness_report(
    profile: str, database: str, findings: list[Finding], error: str | None = None
) -> dict[str, Any]:
    if error is not None:
        status = "error"
    elif findings:
        status = "findings"
    else:
        status = "ready"
    report = {
        "schema_version": 1,
        "kind": READINESS_REPORT_KIND,
        "profile": profile,
        "database": database,
        "status": status,
        "finding_count": len(findings),
        "findings": [finding.to_json() for finding in findings],
        "error": error,
    }
    _assert_json_safe(report)
    return report


def emit_report(report: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, sort_keys=True, separators=(",", ":")))
        return
    print(f"profile: {report['profile']}")
    print(f"database: {report['database']}")
    print(f"status: {report['status']}")
    if report.get("error"):
        print(f"error: {report['error']}")
    for finding in report["findings"]:
        print(f"{finding['code']} {finding['dimension']} {finding['object']}")


def run_validation(
    template: str, database: str, profile: str
) -> tuple[dict[str, Any], int]:
    runner = PsqlRunner(template)
    require_superuser(runner, database)
    try:
        expected = derive_expected_profile(runner, profile)
    except FreezeInstallerMissing:
        report = build_readiness_report(
            profile, database, [freeze_installer_missing_finding()]
        )
        return report, 1
    observed = capture_target_fingerprint(runner, database, expected.scope)
    findings = diff_profiles(expected, observed)
    report = build_readiness_report(profile, database, findings)
    return report, 0 if not findings else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only readiness and drift fingerprinting for the Hermes "
            "runtime v2 PostgreSQL contract."
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
    parser.add_argument("--profile", required=True, choices=PROFILES)
    parser.add_argument("--json", action="store_true", dest="as_json")
    options = parser.parse_args(argv)

    try:
        report, exit_code = run_validation(
            options.psql_command, options.database, options.profile
        )
    except ToolError as error:
        report = build_readiness_report(
            options.profile, options.database, [], error=str(error)
        )
        emit_report(report, options.as_json)
        return 2
    emit_report(report, options.as_json)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
