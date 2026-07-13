"""RED contract for US3 migration mapping, digest, and staging semantics."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from scripts.hermes_runtime_validation import migration
from scripts.hermes_runtime_validation.loader import load_yaml_document
from scripts.hermes_runtime_validation.semantics.authority import (
    canonical_record_digest,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_ROOT = REPOSITORY_ROOT / "contracts/hermes-runtime"
MAPPING_SCHEMA_PATH = CONTRACT_ROOT / "migrations/v1-to-v2-mapping.schema.yaml"
QUARANTINE_SCHEMA_PATH = CONTRACT_ROOT / "legacy-quarantine-record.schema.yaml"
GOLDEN_VECTORS_PATH = (
    REPOSITORY_ROOT
    / "tests/hermes_runtime_contracts/postgres/fixtures/digest-golden-vectors.yaml"
)
DATASET_DIGEST_CLI = REPOSITORY_ROOT / "scripts/hermes-runtime-dataset-digest.py"
CANONICAL_SCHEMA_BASE = "https://xforge.us/schemas/openxfactory/hermes-runtime/v2/"

# Hand-derived in the golden-vector file's header comment; repeated here so a
# fixture edit cannot silently drift away from the spec arithmetic.
SMALLEST_VECTOR_HEX = (
    "584656314453000110000000000000008b11000000000000000173120000000000000001"
    "74130000000000000008000000000000000114000000000000002800000000000000010000"
    "000000000000011500000000000000016116000000000000000474657874170000000000000008"
    "000000000000000120000000000000001b2100000000000000120000000000000001"
    "31000000000000000178"
)

REQUIRED_VECTOR_IDS = {
    "smallest-single-row",
    "every-value-tag",
    "composite-pk-framed-order",
    "table-order-raw-utf8",
    "empty-twelve-table",
}


def _vectors() -> list[dict]:
    return migration.load_golden_vectors(GOLDEN_VECTORS_PATH)


def _vector(vector_id: str) -> dict:
    return next(vector for vector in _vectors() if vector["vector_id"] == vector_id)


def _schemas() -> tuple[dict, dict, dict]:
    return (
        load_yaml_document(MAPPING_SCHEMA_PATH),
        load_yaml_document(QUARANTINE_SCHEMA_PATH),
        load_yaml_document(CONTRACT_ROOT / "shared-definitions.schema.yaml"),
    )


def _registry() -> Registry:
    return Registry().with_resources(
        (
            schema["$id"],
            Resource.from_contents(schema, default_specification=DRAFT202012),
        )
        for schema in _schemas()
    )


def _validator_for(schema: dict | str) -> Draft202012Validator:
    target = schema if isinstance(schema, dict) else {"$ref": schema}
    return Draft202012Validator(
        target, registry=_registry(), format_checker=FormatChecker()
    )


def build_payload(**overrides) -> dict:
    dataset = _vector("empty-twelve-table")["dataset"]
    payload = {
        "schema_version": 1,
        "kind": migration.MAPPING_PAYLOAD_KIND,
        "migration_id": "migration-01",
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
                "customer_subject": {
                    "kind": "software_project",
                    "issuer": "example-domain",
                    "namespace": "subjects",
                    "ref": (
                        "urn:xfactory:subject:" "9f32f1de-82a7-4e38-a83d-9e5dd9189a11"
                    ),
                },
            },
            {
                "legacy_project": "project-beta",
                "layer_id": "customer-b",
                "customer_subject": {
                    "kind": "software_project",
                    "issuer": "example-domain",
                    "namespace": "subjects",
                    "ref": (
                        "urn:xfactory:subject:" "018f47a0-7b2c-7abc-8def-0123456789ab"
                    ),
                },
            },
        ],
        "admin_mappings": {
            "workers": [
                {"source_pk": '["worker-01"]', "scope_kind": "installation_admin"},
                {
                    "source_pk": '["worker-02"]',
                    "scope_kind": "layer",
                    "layer_id": "customer-a",
                },
            ],
            "groups": [],
            "profiles": [],
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
            "policy_ref": "policies/delegated.yaml",
            "policy_digest": "sha256:" + "d0" * 32,
        },
    }
    payload.update(overrides)
    payload.pop("mapping_payload_digest", None)
    payload["mapping_payload_digest"] = migration.mapping_payload_digest(payload)
    return payload


def build_envelope(payload: dict, **overrides) -> dict:
    envelope = {
        "schema_version": 1,
        "kind": migration.AUTHORITY_ENVELOPE_KIND,
        "migration_id": payload["migration_id"],
        "installation_id": payload["installation_id"],
        "mapping_payload_digest": payload["mapping_payload_digest"],
        "approver_principal_id": "principal-migrator",
        "run_migration_grant_id": "grant-run-migration-01",
        "run_migration_grant_digest": "sha256:" + "e1" * 32,
        "policy_ref": "policies/delegated.yaml",
        "policy_digest": "sha256:" + "d0" * 32,
        "scope": {"installation_id": payload["installation_id"]},
        "trust_anchor_id": "anchor-01",
        "trust_anchor_digest": "sha256:" + "a0" * 32,
        "approved_at": "2026-07-12T12:00:00Z",
    }
    envelope.update(overrides)
    envelope.pop("authority_envelope_digest", None)
    envelope["authority_envelope_digest"] = migration.authority_envelope_digest(
        envelope
    )
    return envelope


def _error_code(callable_, *args, **kwargs) -> str:
    with pytest.raises(migration.MigrationContractError) as excinfo:
        callable_(*args, **kwargs)
    return excinfo.value.code


def build_quarantine_record(**overrides) -> dict:
    record = {
        "schema_version": 1,
        "kind": "openxfactory-hermes-runtime-legacy-quarantine-record",
        "migration_id": "migration-01",
        "source_schema": "public",
        "source_table": "hermes_job_artifacts",
        "source_pk": '["artifact-01"]',
        "source_row_digest": "sha256:" + "ab" * 32,
        "reason_code": "missing_content_digest",
        "source_row": {"id": "artifact-01", "sha256": None},
        "captured_at": "2026-07-12T12:00:00Z",
    }
    record.update(overrides)
    return record


class TestGoldenVectors:
    def test_vector_file_covers_the_required_cases(self) -> None:
        vectors = _vectors()
        assert {vector["vector_id"] for vector in vectors} >= REQUIRED_VECTOR_IDS

    @pytest.mark.parametrize("vector_id", sorted(REQUIRED_VECTOR_IDS))
    def test_stream_reproduces_every_vector_exactly(self, vector_id: str) -> None:
        vector = _vector(vector_id)
        dataset = vector["dataset"]
        stream = migration.dataset_stream(dataset)
        if "expected_stream_hex" in vector:
            assert stream.hex() == vector["expected_stream_hex"]
        assert migration.dataset_digest(dataset) == vector["expected_stream_sha256"]
        per_table = {
            f"{table['schema_name']}.{table['table_name']}": (
                migration.table_frame_digest(table)
            )
            for table in dataset["tables"]
        }
        assert per_table == vector["expected_table_frame_digests"]

    def test_hand_derived_smallest_vector_bytes_are_pinned(self) -> None:
        vector = _vector("smallest-single-row")
        assert vector["expected_stream_hex"] == SMALLEST_VECTOR_HEX
        stream = bytes.fromhex(SMALLEST_VECTOR_HEX)
        assert stream.startswith(b"XFV1DS\x00\x01")
        assert len(stream) == 156

    def test_control_character_json_value_uses_backslash_u000a(self) -> None:
        vector = _vector("every-value-tag")
        stream_hex = vector["expected_stream_hex"]
        # Bytes of "line" + backslash + "u000a" + "break" inside the tag-36
        # JSON payload: the LF is the six-character lowercase escape.
        assert "6c696e655c7530303061627265616b" in stream_hex
        # The two-character short escape 5c 6e ("\n") never appears inside
        # the JSON payload region for that value.
        assert "6c696e655c6e627265616b" not in stream_hex

    def test_loader_rejects_hex_and_sha_disagreement(self, tmp_path: Path) -> None:
        vector = _vector("smallest-single-row")
        forged = {
            "schema_version": 1,
            "kind": migration.GOLDEN_VECTORS_KIND,
            "vectors": [
                {
                    "vector_id": "forged",
                    "dataset": vector["dataset"],
                    "expected_stream_hex": vector["expected_stream_hex"],
                    "expected_stream_sha256": "sha256:" + "0" * 64,
                    "expected_table_frame_digests": (
                        vector["expected_table_frame_digests"]
                    ),
                }
            ],
        }
        target = tmp_path / "forged-vectors.yaml"
        target.write_text(json.dumps(forged), encoding="utf-8")
        assert (
            _error_code(migration.load_golden_vectors, target)
            == "HGR-MIGRATION-VECTORS-SHAPE"
        )


class TestCanonicalJsonProfiles:
    def test_dataset_serializer_escapes_all_controls_lowercase(self) -> None:
        assert migration.canonical_json_text({"k": "a\nb"}) == '{"k":"a\\u000ab"}'
        assert migration.canonical_json_text("\x00\x1f") == '"\\u0000\\u001f"'
        assert migration.canonical_json_text('q"\\') == '"q\\"\\\\"'

    def test_dataset_serializer_sorts_keys_by_raw_utf8_and_keeps_astral(self) -> None:
        rendered = migration.canonical_json_text({"€": 1, "z": 2, "a": [None, True]})
        assert rendered == '{"a":[null,true],"z":2,"€":1}'
        assert migration.canonical_json_text({"s": "🚀"}) == '{"s":"🚀"}'

    def test_floats_are_forbidden_in_both_profiles(self) -> None:
        assert (
            _error_code(migration.canonical_json_text, {"x": 1.5})
            == "HGR-MIGRATION-JSON-VALUE"
        )
        assert (
            _error_code(migration.family_canonical_json_text, {"x": 1.5})
            == "HGR-MIGRATION-JSON-VALUE"
        )

    def test_family_profile_matches_shipped_record_digest(self) -> None:
        record = {"kind": "sample", "values": ["é", 12, None, {"n": True}]}
        assert migration.record_digest(record, omit_field=None) == (
            canonical_record_digest(record)
        )

    def test_profiles_deliberately_split_on_control_characters(self) -> None:
        value = {"k": "a\nb"}
        assert migration.family_canonical_json_text(value) == '{"k":"a\\nb"}'
        assert migration.canonical_json_text(value) == '{"k":"a\\u000ab"}'

    def test_profiles_agree_byte_for_byte_on_control_free_values(self) -> None:
        value = {"z": ["é", "🚀", ""], "a": 0, "n": None, "€": {"y": False}}
        assert migration.canonical_json_text(value) == (
            migration.family_canonical_json_text(value)
        )


class TestMappingPayloadValidation:
    def test_valid_payload_passes(self) -> None:
        migration.validate_mapping_payload(build_payload())

    def test_control_characters_raise_the_stable_code(self) -> None:
        payload = build_payload()
        payload["migration_policy"]["policy_ref"] = "policies/\x01bad.yaml"
        payload["mapping_payload_digest"] = migration.mapping_payload_digest(payload)
        assert (
            _error_code(migration.validate_mapping_payload, payload)
            == "HGR-MIGRATION-CONTROL-CHARACTER"
        )

    def test_unknown_and_missing_fields_fail_closed(self) -> None:
        payload = build_payload()
        payload["surprise"] = True
        assert (
            _error_code(migration.validate_mapping_payload, payload)
            == "HGR-MIGRATION-PAYLOAD-SHAPE"
        )
        payload = build_payload()
        del payload["digest_profile"]
        assert (
            _error_code(migration.validate_mapping_payload, payload)
            == "HGR-MIGRATION-PAYLOAD-SHAPE"
        )

    def test_tampered_payload_fails_digest_binding(self) -> None:
        payload = build_payload()
        payload["installation_id"] = "install-02"
        payload["target_topology"]["installation_id"] = "install-02"
        assert (
            _error_code(migration.validate_mapping_payload, payload)
            == "HGR-MIGRATION-PAYLOAD-DIGEST"
        )

    def test_catalog_must_be_exactly_the_twelve_tables_in_order(self) -> None:
        payload = build_payload()
        payload["source_catalog"] = payload["source_catalog"][:11]
        payload["expected_table_row_counts"] = {
            f"{entry['schema_name']}.{entry['table_name']}": 0
            for entry in payload["source_catalog"]
        }
        payload["mapping_payload_digest"] = migration.mapping_payload_digest(payload)
        assert (
            _error_code(migration.validate_mapping_payload, payload)
            == "HGR-MIGRATION-PAYLOAD-CATALOG"
        )
        payload = build_payload()
        payload["source_catalog"] = list(reversed(payload["source_catalog"]))
        payload["mapping_payload_digest"] = migration.mapping_payload_digest(payload)
        assert (
            _error_code(migration.validate_mapping_payload, payload)
            == "HGR-MIGRATION-PAYLOAD-CATALOG"
        )

    def test_counts_must_cover_exactly_the_catalog_identities(self) -> None:
        payload = build_payload()
        del payload["expected_table_row_counts"]["public.hermes_jobs"]
        payload["mapping_payload_digest"] = migration.mapping_payload_digest(payload)
        assert (
            _error_code(migration.validate_mapping_payload, payload)
            == "HGR-MIGRATION-PAYLOAD-COUNTS"
        )

    def test_ambiguous_subject_mapping_fails(self) -> None:
        payload = build_payload()
        payload["subject_mappings"].append(
            dict(payload["subject_mappings"][0], layer_id="customer-b")
        )
        payload["mapping_payload_digest"] = migration.mapping_payload_digest(payload)
        assert (
            _error_code(migration.validate_mapping_payload, payload)
            == "HGR-MIGRATION-PAYLOAD-MAPPING"
        )

    def test_subject_mapping_layer_must_be_declared_customer_layer(self) -> None:
        payload = build_payload()
        payload["subject_mappings"][0]["layer_id"] = "client-01"
        payload["mapping_payload_digest"] = migration.mapping_payload_digest(payload)
        assert (
            _error_code(migration.validate_mapping_payload, payload)
            == "HGR-MIGRATION-PAYLOAD-MAPPING"
        )

    def test_admin_source_pk_must_be_canonical_json_array(self) -> None:
        payload = build_payload()
        payload["admin_mappings"]["workers"][0]["source_pk"] = '["a", "b"]'
        payload["mapping_payload_digest"] = migration.mapping_payload_digest(payload)
        assert (
            _error_code(migration.validate_mapping_payload, payload)
            == "HGR-MIGRATION-PAYLOAD-MAPPING"
        )

    def test_single_default_mapping_requires_a_mapped_project(self) -> None:
        payload = build_payload(
            single_default_mapping={"enabled": True, "legacy_project": "ghost"}
        )
        assert (
            _error_code(migration.validate_mapping_payload, payload)
            == "HGR-MIGRATION-PAYLOAD-MAPPING"
        )


class TestAuthorityEnvelopeValidation:
    def test_valid_envelope_passes(self) -> None:
        payload = build_payload()
        migration.validate_authority_envelope(build_envelope(payload), payload=payload)

    def test_envelope_must_bind_the_exact_payload_digest(self) -> None:
        payload = build_payload()
        envelope = build_envelope(payload, mapping_payload_digest="sha256:" + "9" * 64)
        assert (
            _error_code(
                migration.validate_authority_envelope, envelope, payload=payload
            )
            == "HGR-MIGRATION-ENVELOPE-BINDING"
        )

    def test_envelope_identity_must_match_payload(self) -> None:
        payload = build_payload()
        envelope = build_envelope(payload, migration_id="migration-99")
        assert (
            _error_code(
                migration.validate_authority_envelope, envelope, payload=payload
            )
            == "HGR-MIGRATION-ENVELOPE-BINDING"
        )

    def test_tampered_envelope_fails_self_digest(self) -> None:
        payload = build_payload()
        envelope = build_envelope(payload)
        envelope["approved_at"] = "2026-07-12T13:00:00Z"
        assert (
            _error_code(
                migration.validate_authority_envelope, envelope, payload=payload
            )
            == "HGR-MIGRATION-ENVELOPE-DIGEST"
        )

    def test_envelope_control_characters_raise_the_stable_code(self) -> None:
        payload = build_payload()
        envelope = build_envelope(payload, policy_ref="p\tq")
        assert (
            _error_code(
                migration.validate_authority_envelope, envelope, payload=payload
            )
            == "HGR-MIGRATION-CONTROL-CHARACTER"
        )


class TestStagingDocument:
    def test_staging_document_is_family_canonical_json(self) -> None:
        payload = build_payload()
        envelope = build_envelope(payload)
        document_text = migration.build_staging_document(payload, envelope)
        document = json.loads(document_text)
        assert document_text == json.dumps(
            document,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        assert document["kind"] == migration.STAGING_DOCUMENT_KIND
        assert document["payload"] == payload
        assert document["authority_envelope"] == envelope


class TestBoundaryAndCatalogIdentities:
    def test_logical_boundary_is_content_derived(self) -> None:
        dataset = _vector("empty-twelve-table")["dataset"]
        catalog = migration.catalog_from_dataset(dataset)
        counts = migration.table_row_counts(dataset)
        digest = migration.dataset_digest(dataset)
        identity = {"source_database": "db-a", "source_schema": "public"}
        first = migration.logical_boundary_id(
            source_identity=identity,
            catalog=catalog,
            table_row_counts=counts,
            dataset_digest=digest,
        )
        second = migration.logical_boundary_id(
            source_identity=dict(identity),
            catalog=[dict(entry) for entry in catalog],
            table_row_counts=dict(counts),
            dataset_digest=digest,
        )
        assert first == second
        expected = migration.record_digest(
            {
                "profile": migration.LOGICAL_BOUNDARY_PROFILE,
                "source_identity": identity,
                "catalog_digest": migration.catalog_digest(catalog),
                "table_row_counts": counts,
                "dataset_digest": digest,
            },
            omit_field=None,
        )
        assert first == expected
        drifted = migration.logical_boundary_id(
            source_identity=identity,
            catalog=catalog,
            table_row_counts=counts,
            dataset_digest="sha256:" + "1" * 64,
        )
        assert drifted != first

    def test_catalog_digest_covers_the_profile_record(self) -> None:
        catalog = migration.catalog_from_dataset(
            _vector("empty-twelve-table")["dataset"]
        )
        assert migration.catalog_digest(catalog) == migration.record_digest(
            {"profile": migration.CATALOG_PROFILE, "tables": catalog},
            omit_field=None,
        )


class TestDatasetValidation:
    def test_null_in_non_nullable_column_fails(self) -> None:
        dataset = json.loads(json.dumps(_vector("smallest-single-row")["dataset"]))
        dataset["tables"][0]["rows"][0][0] = {"type": None}
        assert (
            _error_code(migration.dataset_stream, dataset)
            == "HGR-MIGRATION-DATASET-VALUE"
        )

    @pytest.mark.parametrize("value", ["007", "+7", "-0", "1.0", ""])
    def test_non_minimal_integers_fail(self, value: str) -> None:
        dataset = {
            "schema_version": 1,
            "kind": migration.DATASET_DESCRIPTION_KIND,
            "source_schema": "public",
            "tables": [
                {
                    "schema_name": "public",
                    "table_name": "t",
                    "columns": [
                        {
                            "name": "n",
                            "normalized_type": "int8",
                            "nullable": False,
                            "primary_key_position": 1,
                        }
                    ],
                    "rows": [[{"type": "integer", "value": value}]],
                }
            ],
        }
        assert (
            _error_code(migration.dataset_stream, dataset)
            == "HGR-MIGRATION-DATASET-VALUE"
        )

    def test_timestamp_requires_exactly_six_fractional_digits_utc(self) -> None:
        for bad in (
            "2026-07-01T00:00:00Z",
            "2026-07-01T00:00:00.000Z",
            "2026-07-01T00:00:00.0000000Z",
            "2026-07-01T00:00:00.000000+00:00",
            "2026-13-01T00:00:00.000000Z",
        ):
            dataset = {
                "schema_version": 1,
                "kind": migration.DATASET_DESCRIPTION_KIND,
                "source_schema": "public",
                "tables": [
                    {
                        "schema_name": "public",
                        "table_name": "t",
                        "columns": [
                            {
                                "name": "ts",
                                "normalized_type": "timestamptz",
                                "nullable": False,
                                "primary_key_position": 1,
                            }
                        ],
                        "rows": [[{"type": "timestamp", "value": bad}]],
                    }
                ],
            }
            assert (
                _error_code(migration.dataset_stream, dataset)
                == "HGR-MIGRATION-DATASET-VALUE"
            )

    def test_binary_requires_even_lowercase_hex(self) -> None:
        for bad in ("0F", "abc", "0xff"):
            dataset = {
                "schema_version": 1,
                "kind": migration.DATASET_DESCRIPTION_KIND,
                "source_schema": "public",
                "tables": [
                    {
                        "schema_name": "public",
                        "table_name": "t",
                        "columns": [
                            {
                                "name": "b",
                                "normalized_type": "bytea",
                                "nullable": False,
                                "primary_key_position": 1,
                            }
                        ],
                        "rows": [[{"type": "binary", "value": bad}]],
                    }
                ],
            }
            assert (
                _error_code(migration.dataset_stream, dataset)
                == "HGR-MIGRATION-DATASET-VALUE"
            )

    def test_duplicate_framed_primary_keys_fail(self) -> None:
        dataset = json.loads(json.dumps(_vector("smallest-single-row")["dataset"]))
        dataset["tables"][0]["rows"].append([{"type": "text", "value": "x"}])
        assert (
            _error_code(migration.dataset_stream, dataset)
            == "HGR-MIGRATION-DATASET-ORDER"
        )

    def test_cell_type_must_match_column_normalized_type(self) -> None:
        dataset = json.loads(json.dumps(_vector("smallest-single-row")["dataset"]))
        dataset["tables"][0]["rows"][0][0] = {"type": "integer", "value": "1"}
        assert (
            _error_code(migration.dataset_stream, dataset)
            == "HGR-MIGRATION-DATASET-VALUE"
        )


class TestSchemaContracts:
    def test_schema_files_carry_the_family_annotations(self) -> None:
        for path, contract_id in (
            (MAPPING_SCHEMA_PATH, "v1-to-v2-mapping"),
            (QUARANTINE_SCHEMA_PATH, "legacy-quarantine-record"),
        ):
            schema = load_yaml_document(path)
            assert schema["schema_version"] == 1
            assert schema["kind"] == "openxfactory-hermes-runtime-contract-schema"
            assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
            relative = path.relative_to(CONTRACT_ROOT).as_posix()
            assert schema["$id"] == CANONICAL_SCHEMA_BASE + relative
            assert schema["contract_id"] == contract_id
            assert schema["contract_schema_version"] == 2
            Draft202012Validator.check_schema(schema)

    def test_mapping_schema_is_self_contained(self) -> None:
        text = MAPPING_SCHEMA_PATH.read_text(encoding="utf-8")
        assert "shared-definitions.schema.yaml" not in text

    def test_schema_closes_valid_payload_envelope_and_staging(self) -> None:
        mapping_schema, _, _ = _schemas()
        payload = build_payload()
        envelope = build_envelope(payload)
        staging = json.loads(migration.build_staging_document(payload, envelope))
        assert not list(_validator_for(mapping_schema).iter_errors(payload))
        assert not list(
            _validator_for(
                mapping_schema["$id"] + "#/$defs/authority_envelope"
            ).iter_errors(envelope)
        )
        assert not list(
            _validator_for(
                mapping_schema["$id"] + "#/$defs/staging_document"
            ).iter_errors(staging)
        )

    def test_schema_rejects_reordered_catalog_and_unknown_fields(self) -> None:
        mapping_schema, _, _ = _schemas()
        validator = _validator_for(mapping_schema)
        payload = build_payload()
        reordered = dict(
            payload, source_catalog=list(reversed(payload["source_catalog"]))
        )
        assert list(validator.iter_errors(reordered))
        unknown = dict(payload, surprise=True)
        assert list(validator.iter_errors(unknown))
        wrong_profile = dict(payload, digest_profile="xfactory-v2-dataset-binary-v1")
        assert list(validator.iter_errors(wrong_profile))

    def test_quarantine_schema_closes_the_record(self) -> None:
        _, quarantine_schema, _ = _schemas()
        validator = _validator_for(quarantine_schema)
        assert not list(validator.iter_errors(build_quarantine_record()))
        assert list(
            validator.iter_errors(build_quarantine_record(source_table="hermes_jobs"))
        )
        assert list(
            validator.iter_errors(build_quarantine_record(reason_code="because"))
        )
        assert list(validator.iter_errors(build_quarantine_record(promoted=True)))
        missing = build_quarantine_record()
        del missing["source_row_digest"]
        assert list(validator.iter_errors(missing))


class TestDatasetDigestCli:
    def _run(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(DATASET_DIGEST_CLI), *arguments],
            capture_output=True,
            text=True,
            check=False,
            cwd=REPOSITORY_ROOT,
        )

    def test_cli_matches_the_library_digest(self, tmp_path: Path) -> None:
        vector = _vector("smallest-single-row")
        dataset_path = tmp_path / "dataset.yaml"
        dataset_path.write_text(json.dumps(vector["dataset"]), encoding="utf-8")
        result = self._run("--dataset", str(dataset_path), "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert payload["status"] == "pass"
        assert payload["summary"]["dataset_digest"] == (
            vector["expected_stream_sha256"]
        )
        assert payload["summary"]["per_table_digests"] == (
            vector["expected_table_frame_digests"]
        )

    def test_cli_emits_the_exact_stream_bytes(self, tmp_path: Path) -> None:
        vector = _vector("smallest-single-row")
        dataset_path = tmp_path / "dataset.yaml"
        dataset_path.write_text(json.dumps(vector["dataset"]), encoding="utf-8")
        stream_path = tmp_path / "stream.bin"
        result = self._run(
            "--dataset", str(dataset_path), "--emit-stream", str(stream_path)
        )
        assert result.returncode == 0, result.stderr
        assert stream_path.read_bytes().hex() == vector["expected_stream_hex"]

    def test_cli_reports_findings_with_exit_one(self, tmp_path: Path) -> None:
        dataset_path = tmp_path / "dataset.yaml"
        dataset_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "kind": "wrong",
                    "source_schema": "s",
                    "tables": [],
                }
            ),
            encoding="utf-8",
        )
        result = self._run("--dataset", str(dataset_path))
        assert result.returncode == 1
        assert "HGR-MIGRATION-DATASET-SHAPE" in result.stdout

    def test_cli_missing_dataset_is_a_harness_error(self, tmp_path: Path) -> None:
        result = self._run("--dataset", str(tmp_path / "absent.yaml"))
        assert result.returncode == 2
