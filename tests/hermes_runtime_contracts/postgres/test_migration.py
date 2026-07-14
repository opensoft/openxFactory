"""RED real-PostgreSQL contracts for the v1-to-v2 migration boundary.

Golden-vector framing and detached mapping/envelope schema-digest contracts
are green from Lane A's library alone; every test that stages, observes, or
executes a migration is deliberately RED until the production SQL surface
(`contracts/hermes-runtime/migrations/v1-to-v2.sql`, the migration functions
in the v2 DDL, `scripts/run-hermes-v1-to-v2-migration.sh`, and the
`fixtures/migration/` seeds) lands.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from decimal import Decimal
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from scripts.hermes_runtime_validation import migration
from scripts.hermes_runtime_validation.loader import load_yaml_document

from .conftest import (
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

GOLDEN_VECTORS_PATH = Path(__file__).resolve().parent / (
    "fixtures/digest-golden-vectors.yaml"
)
MAPPING_SCHEMA_PATH = (
    REPOSITORY_ROOT / "contracts/hermes-runtime/migrations/v1-to-v2-mapping.schema.yaml"
)
QUARANTINE_SCHEMA_PATH = (
    REPOSITORY_ROOT / "contracts/hermes-runtime/legacy-quarantine-record.schema.yaml"
)
SHARED_DEFINITIONS_PATH = (
    REPOSITORY_ROOT / "contracts/hermes-runtime/shared-definitions.schema.yaml"
)
MIGRATION_RUNNER = REPOSITORY_ROOT / "scripts/run-hermes-v1-to-v2-migration.sh"
TWO_SUBJECT_DATASET = MIGRATION_FIXTURE_ROOT / "v1-two-subject-dataset.yaml"
ONE_SUBJECT_DATASET = MIGRATION_FIXTURE_ROOT / "v1-one-subject-dataset.yaml"
TWO_SUBJECT_SEED = MIGRATION_FIXTURE_ROOT / "10-v1-two-subject-seed.sql"
ONE_SUBJECT_SEED = MIGRATION_FIXTURE_ROOT / "11-v1-one-subject-seed.sql"
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

HISTORY_TABLES = {
    "hermes_jobs": "legacy_jobs",
    "hermes_job_runs": "legacy_job_runs",
    "hermes_job_events": "legacy_job_events",
    "hermes_workers": "legacy_workers",
    "hermes_groups": "legacy_groups",
    "hermes_profiles": "legacy_profiles",
    "hermes_group_memberships": "legacy_group_memberships",
    "hermes_github_team_mappings": "legacy_github_team_mappings",
}
QUARANTINE_REASONS = {
    "hermes_job_artifacts": "missing_content_digest",
    "hermes_approval_requests": "missing_target_digest",
    "hermes_approvals": "missing_reviewer_authority",
    "hermes_traceability_edges": "missing_binding_evidence",
}

AUTHORITY_REJECTION_FRAGMENTS = (
    "authority",
    "grant",
    "revoked",
    "expired",
    "inactive",
    "denied",
    "forbidden",
    "HGR-MIGRATION",
)


def _vectors() -> list[dict]:
    return migration.load_golden_vectors(GOLDEN_VECTORS_PATH)


def _vector(vector_id: str) -> dict:
    return next(vector for vector in _vectors() if vector["vector_id"] == vector_id)


def _seed_migration_base(database: PostgresDatabase) -> None:
    """Apply the source-specific migration SQL plus the seeded base.

    ``migrations/v1-to-v2.sql`` is the superuser-applied, independently
    re-runnable deployment step carrying the pinned-catalog assertions, the
    owner grants over the v1 surface, and the transform functions; the
    ``postgres_v1_database`` fixture deliberately ships without it.  The
    isolation topology/authority seeds and Lane C's migration authority seed
    follow (the fixture ships unseeded)."""

    assert_sql_succeeds(database.file(MIGRATION_SQL, timeout=60))
    for fixture in ("10-two-customer-topology.sql", "20-authority.sql"):
        assert_sql_succeeds(database.file(ISOLATION_FIXTURE_ROOT / fixture))
    assert_sql_succeeds(database.file(MIGRATION_AUTHORITY_SEED))


def _grant_digest(grant_id: str) -> str:
    return "sha256:" + hashlib.sha256(grant_id.encode("utf-8")).hexdigest()


def _mint_run_migration_grant(
    database: PostgresDatabase,
    *,
    grant_id: str,
    migration_id: str,
    payload_digest: str,
    expires_at: str = "2099-01-01T00:00:00Z",
) -> str:
    """Issue an exact-resource ``run_migration`` grant to principal-migrator.

    The ratified grant constrains resource type ``migration_mapping``, the
    exact migration ID, and the exact mapping-payload digest, so each staged
    payload needs its own grant; tests mint it under the seeded root pattern.
    Returns the grant record digest as RECOMPUTED BY THE DATABASE: the
    ``authority_grants_compute_digest`` trigger derives ``record_digest``
    from the canonical grant content, so a locally fabricated digest would
    never satisfy ``migration_verify_authority``.
    """

    placeholder_digest = _grant_digest(grant_id)
    result = database.sql(f"""
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
          'install-01', '{grant_id}', '{placeholder_digest}',
          'xfactory-canonical-json-v1', 'delegated',
          principal.stack_id, principal.layer_id, principal.principal_id,
          principal.record_digest, NULL, NULL,
          'grant-root-issue', issuer_grant.record_digest,
          'installation', '', '', 'run_migration', 'migration_mapping',
          '{migration_id}', '{payload_digest}',
          'opensoft/exampleFactory', 'dddddddddddddddddddddddddddddddddddddddd',
          '{POLICY_REF}', '{POLICY_DIGEST}',
          '2020-01-01T00:00:00Z'::timestamptz, '{expires_at}'::timestamptz,
          '2020-01-01T00:00:00Z'::timestamptz
        FROM xfactory_runtime_v2.principals principal
        JOIN xfactory_runtime_v2.authority_grants issuer_grant
          ON issuer_grant.installation_id = 'install-01'
         AND issuer_grant.grant_id = 'grant-root-issue'
        WHERE principal.installation_id = 'install-01'
          AND principal.principal_id = 'principal-migrator';
        SELECT record_digest FROM xfactory_runtime_v2.authority_grants
         WHERE installation_id = 'install-01' AND grant_id = '{grant_id}';
        """)
    assert_sql_succeeds(result)
    minted = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    assert minted and minted[-1].startswith("sha256:"), (
        "run_migration grant was not minted; is principal-migrator seeded by "
        "fixtures/migration/30-migration-authority.sql?"
    )
    return minted[-1]


def _revoke_grant(database: PostgresDatabase, grant_id: str) -> None:
    revocation_id = f"revocation-{grant_id}"
    result = database.sql(f"""
        INSERT INTO xfactory_runtime_v2.authority_grant_revocations (
          installation_id, revocation_id, record_digest, grant_id,
          grant_digest, revoker_grant_id, reason, effective_at
        )
        SELECT 'install-01', '{revocation_id}',
               '{_grant_digest(revocation_id)}', grant_id, record_digest,
               'grant-root-issue', 'migration contract test revocation',
               '2020-01-02T00:00:00Z'::timestamptz
        FROM xfactory_runtime_v2.authority_grants
        WHERE installation_id = 'install-01' AND grant_id = '{grant_id}';
        """)
    assert_sql_succeeds(result)


def _cell_text(cell: dict) -> str:
    assert cell.get("type") is not None, "primary-key cells must not be null"
    value = cell["value"]
    assert isinstance(value, str), "v1 primary keys frame as text encodings"
    return value


def _table(dataset: dict, table_name: str) -> dict:
    return next(
        table for table in dataset["tables"] if table["table_name"] == table_name
    )


def _pk_arrays(dataset: dict, table_name: str) -> set[str]:
    table = _table(dataset, table_name)
    key_ordinals = sorted(
        (column["primary_key_position"], index)
        for index, column in enumerate(table["columns"])
        if column["primary_key_position"] > 0
    )
    return {
        migration.canonical_json_text(
            [_cell_text(row[index]) for _, index in key_ordinals]
        )
        for row in table["rows"]
    }


# Dollar-quote tag for expected-content JSON shipped into psql (F-2).
_EXPECTED_JSON_TAG = "hcs_expected"


def _expected_source_row(row: list[dict], columns: list[dict]) -> dict:
    """Mirror the ledger's ``source_row`` jsonb for one seeded dataset row.

    ``migration_live_row_json_expression`` preserves text/timestamp/binary
    values as JSON strings, jsonb columns verbatim, integers as JSON numbers,
    booleans as JSON booleans, and NULL as JSON null."""

    members: dict = {}
    for cell, column in zip(row, columns, strict=True):
        if cell.get("type") is None:
            members[column["name"]] = None
        elif cell["type"] == "integer":
            members[column["name"]] = int(cell["value"])
        else:
            members[column["name"]] = cell["value"]
    return members


def _expected_preservation(dataset: dict, table_name: str) -> list[dict]:
    """Expected (source_pk, source_row_digest, source_row) per seeded row.

    The digest is recomputed INDEPENDENTLY from the YAML mirror through the
    Python §7 row framing (golden-vector-proven byte-equal to the SQL side),
    so a transform that corrupted preserved bytes or stored a digest over
    different bytes cannot pass."""

    table = _table(dataset, table_name)
    columns = table["columns"]
    key_ordinals = sorted(
        (column["primary_key_position"], index)
        for index, column in enumerate(columns)
        if column["primary_key_position"] > 0
    )
    entries = []
    for row in table["rows"]:
        _, row_frame = migration._row_frame(row, columns)
        entries.append(
            {
                "source_pk": migration.canonical_json_text(
                    [_cell_text(row[index]) for _, index in key_ordinals]
                ),
                "source_row_digest": "sha256:" + hashlib.sha256(row_frame).hexdigest(),
                "source_row": _expected_source_row(row, columns),
            }
        )
    return entries


def _assert_preserved_rows(
    database: PostgresDatabase,
    *,
    migration_id: str,
    relation: str,
    extra_join_sql: str,
    entries: list[dict],
    label: str,
) -> None:
    """Assert stored source_row content and source_row_digest round-trip.

    One aggregate query per table: every expected row must join on its
    source_pk with an equal digest and semantically equal source_row jsonb,
    and the join must cover exactly the expected row count."""

    expected_json = json.dumps(entries, ensure_ascii=True, sort_keys=True)
    assert _EXPECTED_JSON_TAG not in expected_json, "reserved quoting tag"
    verdict = database.scalar(
        "SELECT coalesce(bool_and("
        "stored.source_row_digest = expected.entry->>'source_row_digest' "
        "AND stored.source_row = expected.entry->'source_row'), false) "
        f"AND count(*) = {len(entries)} "
        "FROM jsonb_array_elements("
        f"${_EXPECTED_JSON_TAG}${expected_json}${_EXPECTED_JSON_TAG}$::jsonb"
        ") AS expected(entry) "
        f"JOIN {relation} stored "
        f"ON stored.migration_id = '{migration_id}' "
        f"{extra_join_sql}"
        "AND stored.source_pk = expected.entry->>'source_pk';"
    )
    assert verdict == "t", (
        f"{label} must preserve every source row's content and digest "
        "exactly as seeded"
    )


def _admin_mappings_from_dataset(dataset: dict) -> dict:
    """Map every worker/group/profile row to installation administration."""

    return {
        collection: [
            {"source_pk": pk, "scope_kind": "installation_admin"}
            for pk in sorted(_pk_arrays(dataset, table_name))
        ]
        for collection, table_name in (
            ("workers", "hermes_workers"),
            ("groups", "hermes_groups"),
            ("profiles", "hermes_profiles"),
        )
    }


def _build_payload(
    dataset: dict,
    *,
    database: PostgresDatabase,
    migration_id: str,
    subject_mappings: list[dict],
    single_default_mapping: dict | None = None,
) -> dict:
    payload = {
        "schema_version": 1,
        "kind": migration.MAPPING_PAYLOAD_KIND,
        "migration_id": migration_id,
        "installation_id": "install-01",
        "source_identity": {
            "source_database": database.name,
            "source_schema": "public",
        },
        "source_catalog": migration.catalog_from_dataset(dataset),
        "expected_table_row_counts": migration.table_row_counts(dataset),
        "expected_dataset_digest": migration.dataset_digest(dataset),
        "digest_profile": migration.DATASET_PROFILE,
        "subject_mappings": subject_mappings,
        "admin_mappings": _admin_mappings_from_dataset(dataset),
        "single_default_mapping": single_default_mapping,
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


def _build_envelope(
    database: PostgresDatabase,
    payload: dict,
    *,
    grant_id: str,
    grant_digest: str,
    **overrides,
) -> dict:
    anchor_digest = database.scalar(
        "SELECT record_digest FROM xfactory_runtime_v2.installation_trust_anchors "
        "WHERE installation_id = 'install-01' AND anchor_id = 'anchor-01';"
    )
    envelope = {
        "schema_version": 1,
        "kind": migration.AUTHORITY_ENVELOPE_KIND,
        "migration_id": payload["migration_id"],
        "installation_id": payload["installation_id"],
        "mapping_payload_digest": payload["mapping_payload_digest"],
        "approver_principal_id": "principal-migrator",
        "run_migration_grant_id": grant_id,
        "run_migration_grant_digest": grant_digest,
        "policy_ref": POLICY_REF,
        "policy_digest": POLICY_DIGEST,
        "scope": {"installation_id": payload["installation_id"]},
        "trust_anchor_id": "anchor-01",
        "trust_anchor_digest": anchor_digest,
        "approved_at": "2026-07-12T12:00:00Z",
    }
    envelope.update(overrides)
    envelope.pop("authority_envelope_digest", None)
    envelope["authority_envelope_digest"] = migration.authority_envelope_digest(
        envelope
    )
    return envelope


def _stage(
    database: PostgresDatabase, staging_text: str
) -> subprocess.CompletedProcess[str]:
    return database.sql(
        "SELECT xfactory_runtime_api_v2.stage_migration("
        f"$hcsstaging${staging_text}$hcsstaging$::jsonb);",
        user="hcs_migrator",
    )


def _staged_payload(
    database: PostgresDatabase,
    *,
    migration_id: str,
    dataset: dict,
    subject_mappings: list[dict],
    single_default_mapping: dict | None = None,
    grant_suffix: str = "01",
) -> tuple[dict, dict, str]:
    payload = _build_payload(
        dataset,
        database=database,
        migration_id=migration_id,
        subject_mappings=subject_mappings,
        single_default_mapping=single_default_mapping,
    )
    grant_id = f"grant-run-migration-{migration_id}-{grant_suffix}"
    grant_digest = _mint_run_migration_grant(
        database,
        grant_id=grant_id,
        migration_id=migration_id,
        payload_digest=payload["mapping_payload_digest"],
    )
    envelope = _build_envelope(
        database, payload, grant_id=grant_id, grant_digest=grant_digest
    )
    staging_text = migration.build_staging_document(payload, envelope)
    return payload, envelope, staging_text


def _psql_template(cluster: PostgresCluster) -> str:
    return (
        f"docker compose --file {COMPOSE_FILE} "
        f"--project-name {cluster.project_name} "
        "exec -T postgres psql -X -q -A -t -v ON_ERROR_STOP=1 "
        "-U hcs_migrator -d {database}"
    )


def _run_migration_runner(
    database: PostgresDatabase,
    staging_path: Path,
    *,
    migration_id: str,
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


def _count(database: PostgresDatabase, statement: str) -> int:
    return int(database.scalar(statement))


def _write_staging(tmp_path: Path, staging_text: str) -> Path:
    staging_path = tmp_path / "staging.json"
    staging_path.write_text(staging_text, encoding="utf-8")
    return staging_path


class TestGoldenVectorFraming:
    """Byte-exact framing contracts; green from the Python library alone."""

    def test_every_golden_vector_reproduces_exactly(self) -> None:
        vectors = _vectors()
        assert len(vectors) >= 5
        for vector in vectors:
            dataset = vector["dataset"]
            stream = migration.dataset_stream(dataset)
            if "expected_stream_hex" in vector:
                assert stream.hex() == vector["expected_stream_hex"], vector[
                    "vector_id"
                ]
            assert migration.dataset_digest(dataset) == (
                vector["expected_stream_sha256"]
            ), vector["vector_id"]
            per_table = {
                f"{table['schema_name']}.{table['table_name']}": (
                    migration.table_frame_digest(table)
                )
                for table in dataset["tables"]
            }
            assert per_table == vector["expected_table_frame_digests"], vector[
                "vector_id"
            ]


class TestDetachedSchemaAndDigests:
    """Detached mapping-payload/authority-envelope schema and digest tests."""

    def _validators(self) -> tuple[Draft202012Validator, Draft202012Validator]:
        mapping_schema = load_yaml_document(MAPPING_SCHEMA_PATH)
        quarantine_schema = load_yaml_document(QUARANTINE_SCHEMA_PATH)
        shared = load_yaml_document(SHARED_DEFINITIONS_PATH)
        registry = Registry().with_resources(
            (
                schema["$id"],
                Resource.from_contents(schema, default_specification=DRAFT202012),
            )
            for schema in (mapping_schema, quarantine_schema, shared)
        )
        payload_validator = Draft202012Validator(
            mapping_schema, registry=registry, format_checker=FormatChecker()
        )
        staging_validator = Draft202012Validator(
            {"$ref": mapping_schema["$id"] + "#/$defs/staging_document"},
            registry=registry,
            format_checker=FormatChecker(),
        )
        return payload_validator, staging_validator

    def _sample_payload_and_envelope(self) -> tuple[dict, dict]:
        dataset = _vector("empty-twelve-table")["dataset"]
        payload = {
            "schema_version": 1,
            "kind": migration.MAPPING_PAYLOAD_KIND,
            "migration_id": "migration-schema-check",
            "installation_id": "install-01",
            "source_identity": {
                "source_database": "hcs_v1_source",
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
                }
            ],
            "admin_mappings": {"workers": [], "groups": [], "profiles": []},
            "single_default_mapping": {
                "enabled": True,
                "legacy_project": ("project-alfa"),
            },
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
        envelope = {
            "schema_version": 1,
            "kind": migration.AUTHORITY_ENVELOPE_KIND,
            "migration_id": payload["migration_id"],
            "installation_id": "install-01",
            "mapping_payload_digest": payload["mapping_payload_digest"],
            "approver_principal_id": "principal-migrator",
            "run_migration_grant_id": "grant-run-migration-01",
            "run_migration_grant_digest": "sha256:" + "e1" * 32,
            "policy_ref": POLICY_REF,
            "policy_digest": POLICY_DIGEST,
            "scope": {"installation_id": "install-01"},
            "trust_anchor_id": "anchor-01",
            "trust_anchor_digest": "sha256:" + "a0" * 32,
            "approved_at": "2026-07-12T12:00:00Z",
        }
        envelope["authority_envelope_digest"] = migration.authority_envelope_digest(
            envelope
        )
        return payload, envelope

    def test_detached_payload_and_envelope_validate_and_digest_bind(self) -> None:
        payload, envelope = self._sample_payload_and_envelope()
        migration.validate_mapping_payload(payload)
        migration.validate_authority_envelope(envelope, payload=payload)
        payload_validator, staging_validator = self._validators()
        assert not list(payload_validator.iter_errors(payload))
        staging = json.loads(migration.build_staging_document(payload, envelope))
        assert not list(staging_validator.iter_errors(staging))

    def test_tampered_payload_or_envelope_fails_digest_validation(self) -> None:
        payload, envelope = self._sample_payload_and_envelope()
        tampered_payload = dict(payload, migration_id="migration-tampered")
        with pytest.raises(migration.MigrationContractError) as payload_error:
            migration.validate_mapping_payload(tampered_payload)
        assert payload_error.value.code == "HGR-MIGRATION-PAYLOAD-DIGEST"
        tampered_envelope = dict(envelope, approved_at="2026-07-12T13:00:00Z")
        with pytest.raises(migration.MigrationContractError) as envelope_error:
            migration.validate_authority_envelope(tampered_envelope, payload=payload)
        assert envelope_error.value.code == "HGR-MIGRATION-ENVELOPE-DIGEST"


class TestDigestParityAcrossEngines:
    """Python, SQL-from-JSON, and live-observation digest parity per major."""

    def test_sql_stream_from_matches_python_for_every_golden_vector(
        self, postgres_database: PostgresDatabase
    ) -> None:
        for vector in _vectors():
            dataset = vector["dataset"]
            expected_hex = migration.dataset_stream(dataset).hex()
            rendered = json.dumps(dataset, ensure_ascii=False)
            result = postgres_database.sql(
                "BEGIN;\n"
                "SELECT encode(xfactory_runtime_v2.migration_dataset_stream_from("
                f"$hcsdataset${rendered}$hcsdataset$::jsonb), 'hex');\n"
                "ROLLBACK;"
            )
            assert_sql_succeeds(result)
            assert result.stdout.strip().splitlines()[-1].strip() == expected_hex, (
                f"major {postgres_database.major} SQL stream diverges from the "
                f"Python framing for vector {vector['vector_id']}"
            )

    def test_live_observation_matches_python_digest_of_the_yaml_mirror(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        _seed_migration_base(postgres_v1_database)
        assert_sql_succeeds(postgres_v1_database.file(TWO_SUBJECT_SEED))
        dataset = migration.load_dataset_description(TWO_SUBJECT_DATASET)
        expected = {
            "dataset_digest": migration.dataset_digest(dataset),
            "catalog_digest": migration.catalog_digest(
                migration.catalog_from_dataset(dataset)
            ),
            "table_row_counts": migration.table_row_counts(dataset),
        }
        result = postgres_v1_database.sql(
            "BEGIN;\n"
            "SELECT xfactory_runtime_v2.migration_observe_source('public');\n"
            "ROLLBACK;"
        )
        assert_sql_succeeds(result)
        observation = json.loads(result.stdout.strip().splitlines()[-1].strip())
        assert observation["dataset_digest"] == expected["dataset_digest"]
        assert observation["catalog_digest"] == expected["catalog_digest"]
        assert observation["table_row_counts"] == expected["table_row_counts"]


class TestCanonicalStagingHandoff:
    def test_stage_migration_recomputes_and_matches_python_digests(
        self, postgres_v1_database: PostgresDatabase, tmp_path: Path
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        dataset = _vector("empty-twelve-table")["dataset"]
        payload, envelope, staging_text = _staged_payload(
            database,
            migration_id="migration-stage-01",
            dataset=dataset,
            subject_mappings=[
                {
                    "legacy_project": "project-alfa",
                    "layer_id": "customer-a",
                    "customer_subject": SUBJECT_ALFA,
                }
            ],
        )
        assert_sql_succeeds(_stage(database, staging_text))
        stored = database.scalar(
            "SELECT mapping_payload_digest || '|' || authority_envelope_digest "
            "FROM xfactory_runtime_v2.migration_staging "
            "WHERE installation_id = 'install-01' "
            "AND migration_id = 'migration-stage-01';"
        )
        assert stored == (
            payload["mapping_payload_digest"]
            + "|"
            + envelope["authority_envelope_digest"]
        ), "database-recomputed staging digests must equal the detached digests"

    def test_identical_restage_is_idempotent_and_conflicting_restage_fails(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        dataset = _vector("empty-twelve-table")["dataset"]
        _, _, staging_text = _staged_payload(
            database,
            migration_id="migration-stage-02",
            dataset=dataset,
            subject_mappings=[
                {
                    "legacy_project": "project-alfa",
                    "layer_id": "customer-a",
                    "customer_subject": SUBJECT_ALFA,
                }
            ],
        )
        assert_sql_succeeds(_stage(database, staging_text))
        assert_sql_succeeds(_stage(database, staging_text))
        assert (
            _count(
                database,
                "SELECT count(*) FROM xfactory_runtime_v2.migration_staging "
                "WHERE migration_id = 'migration-stage-02';",
            )
            == 1
        )
        _, _, conflicting = _staged_payload(
            database,
            migration_id="migration-stage-02",
            dataset=dataset,
            subject_mappings=[
                {
                    "legacy_project": "project-alfa",
                    "layer_id": "customer-b",
                    "customer_subject": SUBJECT_BETA,
                }
            ],
            grant_suffix="02",
        )
        assert_sql_fails(
            _stage(database, conflicting),
            "conflict",
            "mismatch",
            "already staged",
            "different",
        )

    def test_non_canonical_staging_with_broken_digest_binding_fails(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        dataset = _vector("empty-twelve-table")["dataset"]
        payload, envelope, _ = _staged_payload(
            database,
            migration_id="migration-stage-03",
            dataset=dataset,
            subject_mappings=[
                {
                    "legacy_project": "project-alfa",
                    "layer_id": "customer-a",
                    "customer_subject": SUBJECT_ALFA,
                }
            ],
        )
        tampered = dict(
            payload,
            installation_id="install-01",
            migration_policy=dict(
                payload["migration_policy"], policy_ref="policies/other.yaml"
            ),
        )
        document = {
            "schema_version": 1,
            "kind": migration.STAGING_DOCUMENT_KIND,
            "payload": tampered,
            "authority_envelope": envelope,
        }
        assert_sql_fails(
            _stage(database, migration.family_canonical_json_text(document)),
            "digest",
            "mismatch",
            "canonical",
        )

    def test_control_characters_are_rejected_at_the_sql_staging_boundary(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        dataset = _vector("empty-twelve-table")["dataset"]
        payload, _, _ = _staged_payload(
            database,
            migration_id="migration-stage-04",
            dataset=dataset,
            subject_mappings=[
                {
                    "legacy_project": "project-alfa",
                    "layer_id": "customer-a",
                    "customer_subject": SUBJECT_ALFA,
                }
            ],
        )
        # Assemble a self-consistent staging document that smuggles a control
        # character, bypassing the Python validators on purpose: PostgreSQL
        # must reject it independently with the stable code.
        smuggled = {
            key: value
            for key, value in payload.items()
            if key != "mapping_payload_digest"
        }
        smuggled["migration_policy"] = dict(
            smuggled["migration_policy"], policy_ref="policies/\nbad.yaml"
        )
        smuggled["mapping_payload_digest"] = migration.mapping_payload_digest(smuggled)
        # The grant binds the smuggled payload exactly, so the control
        # character is the only remaining reason to reject.
        grant_digest = _mint_run_migration_grant(
            database,
            grant_id="grant-run-migration-control-04",
            migration_id=smuggled["migration_id"],
            payload_digest=smuggled["mapping_payload_digest"],
        )
        envelope = {
            "schema_version": 1,
            "kind": migration.AUTHORITY_ENVELOPE_KIND,
            "migration_id": smuggled["migration_id"],
            "installation_id": "install-01",
            "mapping_payload_digest": smuggled["mapping_payload_digest"],
            "approver_principal_id": "principal-migrator",
            "run_migration_grant_id": "grant-run-migration-control-04",
            "run_migration_grant_digest": grant_digest,
            "policy_ref": POLICY_REF,
            "policy_digest": POLICY_DIGEST,
            "scope": {"installation_id": "install-01"},
            "trust_anchor_id": "anchor-01",
            "trust_anchor_digest": "sha256:" + "a0" * 32,
            "approved_at": "2026-07-12T12:00:00Z",
        }
        envelope["authority_envelope_digest"] = migration.authority_envelope_digest(
            envelope
        )
        document = {
            "schema_version": 1,
            "kind": migration.STAGING_DOCUMENT_KIND,
            "payload": smuggled,
            "authority_envelope": envelope,
        }
        assert_sql_fails(
            _stage(database, migration.family_canonical_json_text(document)),
            "control",
            "HGR-MIGRATION-CONTROL-CHARACTER",
        )


class TestStagingAuthorityRejections:
    def _payload_and_grant(
        self, database: PostgresDatabase, migration_id: str
    ) -> tuple[dict, str, str]:
        dataset = _vector("empty-twelve-table")["dataset"]
        payload = _build_payload(
            dataset,
            database=database,
            migration_id=migration_id,
            subject_mappings=[
                {
                    "legacy_project": "project-alfa",
                    "layer_id": "customer-a",
                    "customer_subject": SUBJECT_ALFA,
                }
            ],
        )
        grant_id = f"grant-run-migration-{migration_id}"
        grant_digest = _mint_run_migration_grant(
            database,
            grant_id=grant_id,
            migration_id=migration_id,
            payload_digest=payload["mapping_payload_digest"],
        )
        return payload, grant_id, grant_digest

    def test_forged_grant_digest_is_rejected(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        payload, grant_id, _ = self._payload_and_grant(database, "migration-auth-01")
        forged = _build_envelope(
            database,
            payload,
            grant_id=grant_id,
            grant_digest="sha256:" + "9" * 64,
        )
        document = {
            "schema_version": 1,
            "kind": migration.STAGING_DOCUMENT_KIND,
            "payload": payload,
            "authority_envelope": forged,
        }
        assert_sql_fails(
            _stage(database, migration.family_canonical_json_text(document)),
            *AUTHORITY_REJECTION_FRAGMENTS,
            "digest",
            "mismatch",
        )

    def test_nonexistent_grant_is_rejected(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        payload, _, _ = self._payload_and_grant(database, "migration-auth-02")
        envelope = _build_envelope(
            database,
            payload,
            grant_id="grant-ghost",
            grant_digest=_grant_digest("grant-ghost"),
        )
        staging_text = migration.build_staging_document(payload, envelope)
        assert_sql_fails(_stage(database, staging_text), *AUTHORITY_REJECTION_FRAGMENTS)

    def test_revoked_grant_is_rejected(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        payload, grant_id, grant_digest = self._payload_and_grant(
            database, "migration-auth-03"
        )
        _revoke_grant(database, grant_id)
        envelope = _build_envelope(
            database, payload, grant_id=grant_id, grant_digest=grant_digest
        )
        staging_text = migration.build_staging_document(payload, envelope)
        assert_sql_fails(_stage(database, staging_text), *AUTHORITY_REJECTION_FRAGMENTS)

    def test_wrong_scope_or_action_grant_is_rejected(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        dataset = _vector("empty-twelve-table")["dataset"]
        payload = _build_payload(
            dataset,
            database=database,
            migration_id="migration-auth-04",
            subject_mappings=[
                {
                    "legacy_project": "project-alfa",
                    "layer_id": "customer-a",
                    "customer_subject": SUBJECT_ALFA,
                }
            ],
        )
        # grant-a-artifact is active but constrains create_artifact on an
        # artifact resource — never run_migration on migration_mapping.
        wrong_grant_digest = database.scalar(
            "SELECT record_digest FROM xfactory_runtime_v2.authority_grants "
            "WHERE installation_id = 'install-01' "
            "AND grant_id = 'grant-a-artifact';"
        )
        envelope = _build_envelope(
            database,
            payload,
            grant_id="grant-a-artifact",
            grant_digest=wrong_grant_digest,
        )
        staging_text = migration.build_staging_document(payload, envelope)
        assert_sql_fails(_stage(database, staging_text), *AUTHORITY_REJECTION_FRAGMENTS)

    def test_inactive_trust_chain_is_rejected(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        dataset = _vector("empty-twelve-table")["dataset"]
        payload = _build_payload(
            dataset,
            database=database,
            migration_id="migration-auth-05",
            subject_mappings=[
                {
                    "legacy_project": "project-alfa",
                    "layer_id": "customer-a",
                    "customer_subject": SUBJECT_ALFA,
                }
            ],
        )
        grant_id = "grant-run-migration-expired-05"
        grant_digest = _mint_run_migration_grant(
            database,
            grant_id=grant_id,
            migration_id="migration-auth-05",
            payload_digest=payload["mapping_payload_digest"],
            expires_at="2021-01-01T00:00:00Z",
        )
        envelope = _build_envelope(
            database, payload, grant_id=grant_id, grant_digest=grant_digest
        )
        staging_text = migration.build_staging_document(payload, envelope)
        assert_sql_fails(_stage(database, staging_text), *AUTHORITY_REJECTION_FRAGMENTS)


class TestLogicalVersusPhysicalBoundary:
    def test_logical_boundary_is_content_derived_across_transactions(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        dataset = _vector("empty-twelve-table")["dataset"]
        source_identity = {
            "source_database": database.name,
            "source_schema": "public",
        }
        expected_boundary = migration.logical_boundary_id(
            source_identity=source_identity,
            catalog=migration.catalog_from_dataset(dataset),
            table_row_counts=migration.table_row_counts(dataset),
            dataset_digest=migration.dataset_digest(dataset),
        )
        identity_json = migration.family_canonical_json_text(source_identity)
        boundary_sql = (
            "BEGIN;\n"
            "SELECT xfactory_runtime_v2.migration_logical_boundary("
            f"$hcsident${identity_json}$hcsident$::jsonb, "
            "xfactory_runtime_v2.migration_observe_source('public'));\n"
            "ROLLBACK;"
        )
        first = database.sql(boundary_sql)
        assert_sql_succeeds(first)
        second = database.sql(boundary_sql)
        assert_sql_succeeds(second)
        first_boundary = first.stdout.strip().splitlines()[-1].strip()
        second_boundary = second.stdout.strip().splitlines()[-1].strip()
        assert first_boundary == second_boundary, (
            "two physically distinct observations of unchanged content must "
            "derive the same logical boundary"
        )
        assert (
            first_boundary == expected_boundary
        ), "SQL logical boundary must equal the Python derivation"


class TestExecutedMigrations:
    def _prepare(
        self,
        database: PostgresDatabase,
        tmp_path: Path,
        *,
        seed: Path,
        dataset_path: Path,
        migration_id: str,
        subject_mappings: list[dict],
        single_default_mapping: dict | None = None,
    ) -> tuple[dict, dict, Path]:
        _seed_migration_base(database)
        assert_sql_succeeds(database.file(seed))
        dataset = migration.load_dataset_description(dataset_path)
        payload, envelope, staging_text = _staged_payload(
            database,
            migration_id=migration_id,
            dataset=dataset,
            subject_mappings=subject_mappings,
            single_default_mapping=single_default_mapping,
        )
        return dataset, payload, _write_staging(tmp_path, staging_text)

    def test_two_subject_migration_classifies_every_row_exactly_once(
        self, postgres_v1_database: PostgresDatabase, tmp_path: Path
    ) -> None:
        database = postgres_v1_database
        migration_id = "migration-two-subject-01"
        dataset, payload, staging_path = self._prepare(
            database,
            tmp_path,
            seed=TWO_SUBJECT_SEED,
            dataset_path=TWO_SUBJECT_DATASET,
            migration_id=migration_id,
            subject_mappings=[
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
        )
        run = _run_migration_runner(database, staging_path, migration_id=migration_id)
        assert run.returncode == 0, f"{run.stdout}\n{run.stderr}"

        counts = migration.table_row_counts(dataset)
        total_source = sum(counts.values())
        classified = 0
        for source_table, legacy_table in HISTORY_TABLES.items():
            legacy_count = _count(
                database,
                f"SELECT count(*) FROM xfactory_runtime_v2.{legacy_table} "
                f"WHERE migration_id = '{migration_id}';",
            )
            assert (
                legacy_count == counts[f"public.{source_table}"]
            ), f"{legacy_table} must carry exactly the {source_table} rows"
            classified += legacy_count
        for source_table, reason_code in QUARANTINE_REASONS.items():
            quarantine_count = _count(
                database,
                "SELECT count(*) FROM "
                "xfactory_legacy_quarantine_v2.legacy_quarantine_records "
                f"WHERE migration_id = '{migration_id}' "
                f"AND source_table = '{source_table}';",
            )
            assert (
                quarantine_count == counts[f"public.{source_table}"]
            ), f"every {source_table} row must be quarantined exactly once"
            classified += quarantine_count
            reason_ok = database.scalar(
                "SELECT coalesce(bool_and(reason_code = "
                f"'{reason_code}'), true) FROM "
                "xfactory_legacy_quarantine_v2.legacy_quarantine_records "
                f"WHERE migration_id = '{migration_id}' "
                f"AND source_table = '{source_table}';"
            )
            assert reason_ok == "t"
        assert (
            classified == total_source
        ), "all twelve canonical tables must reconcile exactly once"

        for source_table, legacy_table in HISTORY_TABLES.items():
            expected_pks = _pk_arrays(dataset, source_table)
            stored = database.sql(
                f"SELECT source_pk FROM xfactory_runtime_v2.{legacy_table} "
                f"WHERE migration_id = '{migration_id}';"
            )
            assert_sql_succeeds(stored)
            stored_pks = {
                line.strip() for line in stored.stdout.splitlines() if line.strip()
            }
            assert (
                stored_pks == expected_pks
            ), f"{legacy_table} must preserve every source row identifier"

        # Quarantine rows must preserve every source identifier too, not merely
        # match a count (F-2): a transform that dropped or rewrote source_pk
        # would otherwise pass on counts alone.
        for source_table in QUARANTINE_REASONS:
            expected_pks = _pk_arrays(dataset, source_table)
            stored = database.sql(
                "SELECT source_pk FROM "
                "xfactory_legacy_quarantine_v2.legacy_quarantine_records "
                f"WHERE migration_id = '{migration_id}' "
                f"AND source_table = '{source_table}';"
            )
            assert_sql_succeeds(stored)
            stored_pks = {
                line.strip() for line in stored.stdout.splitlines() if line.strip()
            }
            assert (
                stored_pks == expected_pks
            ), f"quarantined {source_table} must preserve every source identifier"

        # Preserved record CONTENT must round-trip, not just counts and
        # identifiers (F-2): every row of all twelve tables is compared
        # cell-for-cell against the seeded YAML mirror, and every stored
        # source_row_digest against a digest recomputed independently in
        # Python. The seeded dataset deliberately carries the trickiest
        # value forms — non-ASCII text (agent-β, group-übersicht, נכשל),
        # JSON string escapes ("she said \"hi\"", a\b, embedded newlines),
        # booleans, composite primary keys (hermes_group_memberships), and
        # microsecond timestamps — per the T053 preservation promise.
        for source_table, legacy_table in HISTORY_TABLES.items():
            _assert_preserved_rows(
                database,
                migration_id=migration_id,
                relation=f"xfactory_runtime_v2.{legacy_table}",
                extra_join_sql="",
                entries=_expected_preservation(dataset, source_table),
                label=legacy_table,
            )
        for source_table in QUARANTINE_REASONS:
            _assert_preserved_rows(
                database,
                migration_id=migration_id,
                relation=("xfactory_legacy_quarantine_v2.legacy_quarantine_records"),
                extra_join_sql=(f"AND stored.source_table = '{source_table}' "),
                entries=_expected_preservation(dataset, source_table),
                label=f"quarantined {source_table}",
            )

        scope_ok = database.scalar(
            "SELECT coalesce(bool_and(scope_kind = 'layer' AND layer_id = CASE "
            "source_row->>'project' WHEN 'project-alfa' THEN 'customer-a' "
            "WHEN 'project-beta' THEN 'customer-b' END), false) "
            f"FROM xfactory_runtime_v2.legacy_jobs "
            f"WHERE migration_id = '{migration_id}';"
        )
        assert scope_ok == "t", "jobs must map to the exact subject layer"
        admin_ok = database.scalar(
            "SELECT coalesce(bool_and(scope_kind = 'installation_admin' "
            "AND layer_id IS NULL), false) "
            f"FROM xfactory_runtime_v2.legacy_workers "
            f"WHERE migration_id = '{migration_id}';"
        )
        assert admin_ok == "t", "workers map to installation administration"

        admin_rows_visible_to_customer = database.sql(
            "BEGIN;\n"
            "SELECT xfactory_runtime_api_v2.assume_scope("
            "'install-01', 'stack-01', 'customer-a', 'grant-a-scope');\n"
            "SELECT count(*) FROM xfactory_runtime_v2.legacy_workers;\n"
            "ROLLBACK;",
            user="hcs_customer_a",
        )
        assert_sql_succeeds(admin_rows_visible_to_customer)
        assert (
            admin_rows_visible_to_customer.stdout.strip().splitlines()[-1].strip()
            == "0"
        ), "installation_admin history must be invisible to customer scopes"

        # Behavioral RLS on the layer-scoped legacy_* history (F-3): each
        # customer scope must see EXACTLY its own subject's rows — not zero
        # (a deny-all policy) and not another layer's (a leak). This exercises
        # the <table>_exact_scope predicate, which the catalog assertion only
        # confirms exists.
        alfa_jobs = _count(
            database,
            "SELECT count(*) FROM xfactory_runtime_v2.legacy_jobs "
            "WHERE source_row->>'project' = 'project-alfa';",
        )
        beta_jobs = _count(
            database,
            "SELECT count(*) FROM xfactory_runtime_v2.legacy_jobs "
            "WHERE source_row->>'project' = 'project-beta';",
        )
        assert alfa_jobs > 0 and beta_jobs > 0, "both subjects must seed jobs"
        for scope_user, grant, own, foreign in (
            ("hcs_customer_a", "grant-a-scope", alfa_jobs, beta_jobs),
            ("hcs_customer_b", "grant-b-scope", beta_jobs, alfa_jobs),
        ):
            layer = "customer-a" if scope_user == "hcs_customer_a" else "customer-b"
            scoped = database.sql(
                "BEGIN;\n"
                "SELECT xfactory_runtime_api_v2.assume_scope("
                f"'install-01', 'stack-01', '{layer}', '{grant}');\n"
                "SELECT count(*) FROM xfactory_runtime_v2.legacy_jobs;\n"
                "ROLLBACK;",
                user=scope_user,
            )
            assert_sql_succeeds(scoped)
            visible = int(scoped.stdout.strip().splitlines()[-1].strip())
            assert visible == own, (
                f"{scope_user} must see exactly its {own} own legacy job rows, "
                f"saw {visible} (deny-all or cross-layer leak)"
            )

        rerun = _run_migration_runner(database, staging_path, migration_id=migration_id)
        assert rerun.returncode == 0, (
            "terminal success must converge as a stored-result observer: "
            f"{rerun.stdout}\n{rerun.stderr}"
        )
        assert (
            _count(
                database,
                "SELECT count(*) FROM xfactory_runtime_v2.migration_attempt_events "
                f"WHERE migration_id = '{migration_id}' "
                "AND event_type = 'succeeded';",
            )
            == 1
        ), "a retry after committed success must not append a second success"
        assert (
            _count(
                database,
                f"SELECT count(*) FROM xfactory_runtime_v2.legacy_jobs "
                f"WHERE migration_id = '{migration_id}';",
            )
            == counts["public.hermes_jobs"]
        ), "a stored-result observer must not reapply rows"

        frozen_write = database.sql(
            "INSERT INTO public.hermes_jobs (id, schema_version, issued_by, "
            "job_type, project, repository_org, repository_name, "
            "repository_default_branch, orchestrator_path, "
            "routing_policy_path, auth_profile_id, auth_mode, envelope) "
            "VALUES ('job-after-freeze', 1, 'Hermes', 'build', 'project-alfa', "
            "'org', 'repo', 'main', 'orch', 'route', 'auth', 'api', '{}');"
        )
        assert_sql_fails(frozen_write, "freeze", "frozen", "denied", "forbidden")

    def test_one_subject_default_map_migration_succeeds(
        self, postgres_v1_database: PostgresDatabase, tmp_path: Path
    ) -> None:
        database = postgres_v1_database
        migration_id = "migration-one-subject-01"
        dataset, _, staging_path = self._prepare(
            database,
            tmp_path,
            seed=ONE_SUBJECT_SEED,
            dataset_path=ONE_SUBJECT_DATASET,
            migration_id=migration_id,
            subject_mappings=[
                {
                    "legacy_project": "project-alfa",
                    "layer_id": "customer-a",
                    "customer_subject": SUBJECT_ALFA,
                }
            ],
            single_default_mapping={
                "enabled": True,
                "legacy_project": "project-alfa",
            },
        )
        run = _run_migration_runner(database, staging_path, migration_id=migration_id)
        assert run.returncode == 0, f"{run.stdout}\n{run.stderr}"
        counts = migration.table_row_counts(dataset)
        assert (
            _count(
                database,
                "SELECT count(*) FROM xfactory_runtime_v2.legacy_jobs "
                f"WHERE migration_id = '{migration_id}';",
            )
            == counts["public.hermes_jobs"]
        )
        single_layer = database.scalar(
            "SELECT coalesce(bool_and(layer_id = 'customer-a'), false) "
            "FROM xfactory_runtime_v2.legacy_jobs "
            f"WHERE migration_id = '{migration_id}';"
        )
        assert (
            single_layer == "t"
        ), "the proven single default map must scope every job to customer-a"

    def test_default_map_with_two_observed_projects_aborts_without_partial_state(
        self, postgres_v1_database: PostgresDatabase, tmp_path: Path
    ) -> None:
        database = postgres_v1_database
        migration_id = "migration-default-abort-01"
        _, _, staging_path = self._prepare(
            database,
            tmp_path,
            seed=TWO_SUBJECT_SEED,
            dataset_path=TWO_SUBJECT_DATASET,
            migration_id=migration_id,
            subject_mappings=[
                {
                    "legacy_project": "project-alfa",
                    "layer_id": "customer-a",
                    "customer_subject": SUBJECT_ALFA,
                }
            ],
            single_default_mapping={
                "enabled": True,
                "legacy_project": "project-alfa",
            },
        )
        run = _run_migration_runner(database, staging_path, migration_id=migration_id)
        assert run.returncode == 1, (
            "two observed distinct projects must make the single default map "
            f"illegal: {run.stdout}\n{run.stderr}"
        )
        for legacy_table in HISTORY_TABLES.values():
            assert (
                _count(
                    database,
                    f"SELECT count(*) FROM xfactory_runtime_v2.{legacy_table} "
                    f"WHERE migration_id = '{migration_id}';",
                )
                == 0
            ), f"aborted migration left partial state in {legacy_table}"
        assert (
            _count(
                database,
                "SELECT count(*) FROM "
                "xfactory_legacy_quarantine_v2.legacy_quarantine_records "
                f"WHERE migration_id = '{migration_id}';",
            )
            == 0
        ), "aborted migration left partial quarantine state"
        unfrozen_write = database.sql(
            "INSERT INTO public.hermes_groups (id, purpose) "
            "VALUES ('group-after-abort', 'probe');"
        )
        assert_sql_succeeds(unfrozen_write)


# ---------------------------------------------------------------------------
# F-7 / F-8 / F-9 fail-closed hardening of the SQL digest surface (P3 backlog).
# ---------------------------------------------------------------------------

# Ratified canonical-JSON DECIMAL number edge cases (spec.md:188 -- arbitrary-
# precision decimals rendered without exponent or plus sign, without
# insignificant leading or trailing zeros, negative zero normalised to 0).  The
# YAML fixture corpus cannot express these (migration.py rejects every float on
# load), so the SQL number branch is exercised here directly against the
# dedicated Python serializer.
_DECIMAL_NUMBER_LITERALS = (
    "1E2",
    "1e-3",
    "1.23E5",
    "1.500",
    "100.100",
    "1.0",
    "0.00",
    "-0",
    "-0.0",
    "-0E0",
    "-1.50",
    "9.99",
    "100",
    "12345678901234567890.00",
    "123456789012345678901234567890.123456789",
)

# Timestamps that satisfy the frame's shape regex but sit outside / inside the
# RFC-3339-expressible AD calendar domain that migration.py's datetime.strptime
# draws.  SQL and Python must accept and reject the identical sets.
_TIMESTAMP_ACCEPTED = (
    "2026-07-12T12:00:00.000000Z",
    "0001-01-01T00:00:00.000000Z",
    "9999-12-31T23:59:59.999999Z",
    "2024-02-29T00:00:00.000000Z",  # 2024 is a leap year
)
_TIMESTAMP_REJECTED = (
    "0000-01-01T00:00:00.000000Z",  # year zero does not exist
    "2026-13-01T00:00:00.000000Z",  # month 13
    "2026-02-30T00:00:00.000000Z",  # 30 February
    "2026-02-29T00:00:00.000000Z",  # 2026 is not a leap year
    "2026-07-12T24:00:00.000000Z",  # 24:00 rolls to the next day
    "2026-07-12T12:60:00.000000Z",  # minute 60
    "2016-12-31T23:59:60.000000Z",  # leap second rolls forward
    "2026-07-12T12:00:61.000000Z",  # second 61
)


def _single_table_dataset(columns: list[dict], rows: list[list[dict]]) -> dict:
    """Build a one-table dataset description shared by both digest engines."""

    return {
        "schema_version": 1,
        "kind": "xfactory-v1-dataset-description",
        "source_schema": "public",
        "tables": [
            {
                "schema_name": "public",
                "table_name": "t",
                "columns": columns,
                "rows": rows,
            }
        ],
    }


def _stream_from_hex_sql(dataset: dict) -> str:
    rendered = json.dumps(dataset, ensure_ascii=False)
    return (
        "SELECT encode(xfactory_runtime_v2.migration_dataset_stream_from("
        f"$hcsds${rendered}$hcsds$::jsonb), 'hex');"
    )


def _stream_from_sql(dataset: dict) -> str:
    rendered = json.dumps(dataset, ensure_ascii=False)
    return (
        "SELECT xfactory_runtime_v2.migration_dataset_stream_from("
        f"$hcsds${rendered}$hcsds$::jsonb);"
    )


_ID_TEXT_PK = {
    "name": "id",
    "normalized_type": "text",
    "nullable": False,
    "primary_key_position": 1,
}


class TestCanonicalJsonNumberParity:
    """F-7: the ratified DECIMAL number rules, exercised over live jsonb.

    The number branch (e.g. a ``hermes_jobs.envelope`` carrying a decimal) is
    unreachable from the YAML corpus because ``migration.py`` rejects every
    float on load, so its byte-parity with the dedicated Python serializer is
    proven here against real ``jsonb`` inputs.
    """

    def test_sql_canonical_json_value_matches_python_for_decimal_edge_cases(
        self, postgres_database: PostgresDatabase
    ) -> None:
        for literal in _DECIMAL_NUMBER_LITERALS:
            expected = migration.canonical_json_text(
                json.loads(literal, parse_float=Decimal)
            )
            rendered = postgres_database.scalar(
                "SELECT xfactory_runtime_v2.migration_canonical_json_value("
                f"'{literal}'::jsonb);"
            )
            assert rendered == expected, (
                f"major {postgres_database.major}: SQL canonical JSON for "
                f"{literal!r} was {rendered!r}; Python emitted {expected!r}"
            )

    def test_value_frame_json_tag_matches_python_for_decimal_edge_cases(
        self, postgres_database: PostgresDatabase
    ) -> None:
        for literal in _DECIMAL_NUMBER_LITERALS:
            expected = migration._value_frame(
                {"type": "json", "value": json.loads(literal, parse_float=Decimal)}
            ).hex()
            cell_json = '{"type": "json", "value": ' + literal + "}"
            rendered = postgres_database.scalar(
                "SELECT encode(xfactory_runtime_v2.migration_value_frame("
                f"$hcsds${cell_json}$hcsds$::jsonb), 'hex');"
            )
            assert rendered == expected, (
                f"major {postgres_database.major}: SQL 0x36 frame for {literal!r} "
                f"was {rendered!r}; Python emitted {expected!r}"
            )

    def test_jsonb_envelope_decimals_frame_identically_through_dataset_stream(
        self, postgres_database: PostgresDatabase
    ) -> None:
        envelope_json = (
            '{"weight":1.500,"delta":1e-3,"zero":-0,"neg_zero":-0.0,"count":100,'
            '"big":123456789012345678901234567890.123456789,'
            '"nested":{"ratio":0.00,"label":"é"},"series":[1.0,-0E0,9.99]}'
        )
        dataset_json = (
            '{"schema_version":1,"kind":"xfactory-v1-dataset-description",'
            '"source_schema":"public","tables":[{"schema_name":"public",'
            '"table_name":"envelopes","columns":['
            '{"name":"id","normalized_type":"text","nullable":false,'
            '"primary_key_position":1},'
            '{"name":"envelope","normalized_type":"jsonb","nullable":false,'
            '"primary_key_position":0}],"rows":[[{"type":"text","value":"e1"},'
            '{"type":"json","value":' + envelope_json + "}]]}]}"
        )
        expected = migration.dataset_stream(
            json.loads(dataset_json, parse_float=Decimal)
        ).hex()
        rendered = postgres_database.scalar(
            "SELECT encode(xfactory_runtime_v2.migration_dataset_stream_from("
            f"$hcsds${dataset_json}$hcsds$::jsonb), 'hex');"
        )
        assert rendered == expected, (
            f"major {postgres_database.major}: live jsonb envelope decimals "
            "diverge from the Python dataset framing"
        )

    def test_non_finite_and_float_numbers_are_rejected_by_both_engines(
        self, postgres_database: PostgresDatabase
    ) -> None:
        # The dedicated serializer fails closed on Python floats and non-finite
        # values -- the reason decimals are unreachable via the YAML corpus.
        for value in (1.5, 0.1, float("nan"), float("inf")):
            with pytest.raises(migration.MigrationContractError) as serializer_error:
                migration.canonical_json_text(value)
            assert serializer_error.value.code == "HGR-MIGRATION-JSON-VALUE"
        # A json dataset cell carrying a float is rejected during validation.
        floating_cell = _single_table_dataset(
            [
                _ID_TEXT_PK,
                {
                    "name": "envelope",
                    "normalized_type": "jsonb",
                    "nullable": False,
                    "primary_key_position": 0,
                },
            ],
            [[{"type": "text", "value": "e1"}, {"type": "json", "value": {"x": 1.5}}]],
        )
        with pytest.raises(migration.MigrationContractError) as cell_error:
            migration.dataset_stream(floating_cell)
        assert cell_error.value.code == "HGR-MIGRATION-DATASET-VALUE"
        # Non-finite numbers are not representable as jsonb: the SQL surface
        # rejects them at the type boundary, matching the Python fail-closed.
        for token in ("NaN", "Infinity", "-Infinity"):
            result = postgres_database.sql(f"SELECT '{token}'::jsonb;")
            assert_sql_fails(result, "invalid input", "json")


class TestTimestampCalendarDomain:
    """F-8: the frozen-source digest fails closed outside the AD RFC-3339
    calendar domain and rejects exactly the timestamps migration.py rejects."""

    _COLUMNS = [
        _ID_TEXT_PK,
        {
            "name": "ts",
            "normalized_type": "timestamptz",
            "nullable": False,
            "primary_key_position": 0,
        },
    ]

    def test_value_frame_and_python_agree_on_the_calendar_domain(
        self, postgres_database: PostgresDatabase
    ) -> None:
        for value in _TIMESTAMP_ACCEPTED:
            dataset = _single_table_dataset(
                self._COLUMNS,
                [
                    [
                        {"type": "text", "value": "r1"},
                        {"type": "timestamp", "value": value},
                    ]
                ],
            )
            expected = migration.dataset_stream(dataset).hex()
            rendered = postgres_database.scalar(_stream_from_hex_sql(dataset))
            assert rendered == expected, f"accepted timestamp diverged: {value}"
        for value in _TIMESTAMP_REJECTED:
            dataset = _single_table_dataset(
                self._COLUMNS,
                [
                    [
                        {"type": "text", "value": "r1"},
                        {"type": "timestamp", "value": value},
                    ]
                ],
            )
            with pytest.raises(migration.MigrationContractError) as python_error:
                migration.dataset_stream(dataset)
            assert python_error.value.code == "HGR-MIGRATION-DATASET-VALUE", value
            result = postgres_database.sql(_stream_from_sql(dataset))
            assert_sql_fails(result, "hgr-migration-dataset-value")

    def test_live_observation_fails_closed_on_bc_era_timestamp(
        self, postgres_v1_database: PostgresDatabase
    ) -> None:
        database = postgres_v1_database
        _seed_migration_base(database)
        assert_sql_succeeds(database.file(TWO_SUBJECT_SEED))
        # Positive control: valid AD source data observes cleanly.
        assert_sql_succeeds(
            database.sql(
                "BEGIN;\n"
                "SELECT xfactory_runtime_v2.migration_observe_source('public');\n"
                "ROLLBACK;"
            )
        )
        # A BC-era instant renders to the same four-digit-year string as its AD
        # alias (44 BC and AD 44 both frame as 0044-...), so the frozen-source
        # digest would be non-injective.  The observe path must fail closed.
        assert_sql_succeeds(
            database.sql(
                "UPDATE public.hermes_jobs "
                "SET created_at = timestamptz '0044-03-15 12:00:00 BC';"
            )
        )
        result = database.sql(
            "BEGIN;\n"
            "SELECT xfactory_runtime_v2.migration_observe_source('public');\n"
            "ROLLBACK;"
        )
        assert_sql_fails(result, "hgr-migration-dataset-value")


class TestDatasetStreamFailClosed:
    """F-9: migration_dataset_stream_from fails closed on profile-invalid
    datasets and duplicate framed primary keys, matching migration.py."""

    def test_stream_from_fails_closed_on_duplicate_framed_primary_keys(
        self, postgres_database: PostgresDatabase
    ) -> None:
        columns = [
            _ID_TEXT_PK,
            {
                "name": "payload",
                "normalized_type": "text",
                "nullable": False,
                "primary_key_position": 0,
            },
        ]
        duplicate = _single_table_dataset(
            columns,
            [
                [{"type": "text", "value": "dup"}, {"type": "text", "value": "a"}],
                [{"type": "text", "value": "dup"}, {"type": "text", "value": "b"}],
            ],
        )
        with pytest.raises(migration.MigrationContractError) as python_error:
            migration.dataset_stream(duplicate)
        assert python_error.value.code == "HGR-MIGRATION-DATASET-ORDER"
        result = postgres_database.sql(_stream_from_sql(duplicate))
        assert_sql_fails(result, "hgr-migration-dataset-order")
        # Distinct primary keys still frame, byte-identically across engines.
        unique = _single_table_dataset(
            columns,
            [
                [{"type": "text", "value": "k1"}, {"type": "text", "value": "a"}],
                [{"type": "text", "value": "k2"}, {"type": "text", "value": "b"}],
            ],
        )
        assert postgres_database.scalar(_stream_from_hex_sql(unique)) == (
            migration.dataset_stream(unique).hex()
        )

    def test_stream_from_fails_closed_on_duplicate_composite_primary_keys(
        self, postgres_database: PostgresDatabase
    ) -> None:
        columns = [
            {
                "name": "a",
                "normalized_type": "text",
                "nullable": False,
                "primary_key_position": 1,
            },
            {
                "name": "b",
                "normalized_type": "int4",
                "nullable": False,
                "primary_key_position": 2,
            },
        ]
        duplicate = _single_table_dataset(
            columns,
            [
                [{"type": "text", "value": "x"}, {"type": "integer", "value": "1"}],
                [{"type": "text", "value": "x"}, {"type": "integer", "value": "1"}],
            ],
        )
        with pytest.raises(migration.MigrationContractError) as python_error:
            migration.dataset_stream(duplicate)
        assert python_error.value.code == "HGR-MIGRATION-DATASET-ORDER"
        result = postgres_database.sql(_stream_from_sql(duplicate))
        assert_sql_fails(result, "hgr-migration-dataset-order")

    def test_stream_from_fails_closed_on_duplicate_column_names(
        self, postgres_database: PostgresDatabase
    ) -> None:
        dataset = _single_table_dataset(
            [
                _ID_TEXT_PK,
                {
                    "name": "id",
                    "normalized_type": "int4",
                    "nullable": True,
                    "primary_key_position": 0,
                },
            ],
            [],
        )
        with pytest.raises(migration.MigrationContractError) as python_error:
            migration.dataset_stream(dataset)
        assert python_error.value.code == "HGR-MIGRATION-DATASET-COLUMN"
        result = postgres_database.sql(_stream_from_sql(dataset))
        assert_sql_fails(result, "hgr-migration-dataset-column")
