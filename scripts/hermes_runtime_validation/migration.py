"""Detached v1-to-v2 migration mapping, dataset-digest, and staging semantics.

This module realizes the ratified ``xfactory-v1-dataset-binary-v1`` framing
profile, the detached mapping-payload/authority-envelope digest identities,
and the canonical staging handoff document.  Everything is pure stdlib plus
the family's strict YAML loader: no network, clock, or database access, so
the same bytes mean the same thing in Python and in the PostgreSQL
conformance lane.

Two deliberately distinct canonical-JSON profiles exist (integration
decision D2):

- **Record digests and the staging document** (mapping payload, authority
  envelope, catalog record, logical boundary) use the shipped
  ``xfactory-canonical-json-v1`` family profile — byte-identical to Python
  ``json.dumps(value, ensure_ascii=False, sort_keys=True,
  separators=(",", ":"))`` and to SQL ``xfactory_runtime_v2.canonical_json``.
  That profile short-escapes ``\\b \\f \\n \\r \\t``; to keep the deviation
  from the ratified prose unreachable, every payload/envelope string is
  rejected when it contains a control character U+0000–U+001F (stable code
  ``HGR-MIGRATION-CONTROL-CHARACTER``), so both profiles agree byte-for-byte
  on every accepted record.
- **Dataset tag-``0x36`` JSON value frames** (and only those) use the
  dedicated ratified-exact serializer :func:`canonical_json_text`: escape
  only ``"``, ``\\``, and ALL controls U+0000–U+001F as lowercase
  ``\\u00xx`` — never short escapes.

Fail-closed rules:

- floating-point values are forbidden everywhere (YAML floats included);
- every value encoding must already be canonical (no silent normalization of
  integers, timestamps, or hex);
- unknown fields, duplicate identities, and ambiguous orderings raise
  :class:`MigrationContractError` with a stable finding code.
"""

from __future__ import annotations

import json
import hashlib
import re
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

from .loader import YamlLoadError, load_yaml_document

DATASET_PROFILE = "xfactory-v1-dataset-binary-v1"
CATALOG_PROFILE = "xfactory-v1-catalog-v1"
LOGICAL_BOUNDARY_PROFILE = "xfactory-v1-logical-boundary-v1"

DATASET_DESCRIPTION_KIND = "xfactory-v1-dataset-description"
GOLDEN_VECTORS_KIND = "xfactory-v1-dataset-golden-vectors"
MAPPING_PAYLOAD_KIND = "openxfactory-hermes-runtime-migration-mapping-payload"
AUTHORITY_ENVELOPE_KIND = "openxfactory-hermes-runtime-migration-authority-envelope"
STAGING_DOCUMENT_KIND = "openxfactory-hermes-runtime-migration-staging"

CANONICAL_V1_TABLES = (
    "hermes_approval_requests",
    "hermes_approvals",
    "hermes_github_team_mappings",
    "hermes_group_memberships",
    "hermes_groups",
    "hermes_job_artifacts",
    "hermes_job_events",
    "hermes_job_runs",
    "hermes_jobs",
    "hermes_profiles",
    "hermes_traceability_edges",
    "hermes_workers",
)

QUARANTINE_REASON_CODES = (
    "missing_content_digest",
    "missing_target_digest",
    "missing_reviewer_authority",
    "missing_binding_evidence",
    "unverifiable_ancestry",
)

_MAGIC = b"XFV1DS\x00\x01"

_TAG_TABLE = 0x10
_TAG_SCHEMA_NAME = 0x11
_TAG_TABLE_NAME = 0x12
_TAG_COLUMN_COUNT = 0x13
_TAG_COLUMN = 0x14
_TAG_COLUMN_NAME = 0x15
_TAG_COLUMN_TYPE = 0x16
_TAG_ROW_COUNT = 0x17
_TAG_ROW = 0x20
_TAG_ROW_COLUMN = 0x21
_TAG_NULL = 0x30
_TAG_TEXT = 0x31
_TAG_INTEGER = 0x32
_TAG_BOOLEAN = 0x33
_TAG_TIMESTAMP = 0x34
_TAG_BINARY = 0x35
_TAG_JSON = 0x36

_NORMALIZED_TYPES = ("text", "int4", "int8", "bool", "timestamptz", "jsonb", "bytea")
_CELL_KIND_BY_TYPE = {
    "text": "text",
    "int4": "integer",
    "int8": "integer",
    "bool": "boolean",
    "timestamptz": "timestamp",
    "jsonb": "json",
    "bytea": "binary",
}
_INTEGER_RANGES = {
    "int4": (-(2**31), 2**31 - 1),
    "int8": (-(2**63), 2**63 - 1),
}

_CANONICAL_ID = re.compile(r"^[a-z0-9](?:[a-z0-9._:-]{0,126}[a-z0-9])?$")
_SHA256_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_LOWERCASE_HEX = re.compile(r"^(?:[0-9a-f]{2})*$")
_CANONICAL_INTEGER = re.compile(r"^(?:0|-?[1-9][0-9]*)$")
_CANONICAL_TIMESTAMP = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z$"
)
_RFC3339_TIMESTAMP = re.compile(
    r"^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[01])"
    r"T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?"
    r"(Z|[+-]([01][0-9]|2[0-3]):[0-5][0-9])$"
)
_SUBJECT_REF = re.compile(
    r"^urn:xfactory:subject:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}"
    r"-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)


class MigrationContractError(ValueError):
    """Fail-closed migration contract violation with a stable finding code."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


def _error(code: str, message: str) -> MigrationContractError:
    return MigrationContractError(code, message)


# ---------------------------------------------------------------------------
# Canonical JSON (ratified migration profile rules)
# ---------------------------------------------------------------------------


def _canonical_string(value: str) -> str:
    rendered = ['"']
    for character in value:
        if character == '"':
            rendered.append('\\"')
        elif character == "\\":
            rendered.append("\\\\")
        elif ord(character) < 0x20:
            rendered.append(f"\\u{ord(character):04x}")
        else:
            rendered.append(character)
    rendered.append('"')
    return "".join(rendered)


def _canonical_decimal(value: Decimal) -> str:
    if not value.is_finite():
        raise _error(
            "HGR-MIGRATION-JSON-VALUE", "non-finite decimal numbers are forbidden"
        )
    sign, digits, exponent = value.as_tuple()
    digit_text = "".join(str(digit) for digit in digits)
    if digit_text.strip("0") == "":
        return "0"
    if exponent >= 0:
        rendered = (digit_text + "0" * exponent).lstrip("0")
    else:
        point = len(digit_text) + exponent
        if point <= 0:
            integral = "0"
            fraction = "0" * (-point) + digit_text
        else:
            integral = digit_text[:point].lstrip("0") or "0"
            fraction = digit_text[point:]
        fraction = fraction.rstrip("0")
        rendered = integral + (f".{fraction}" if fraction else "")
    return ("-" if sign else "") + rendered


def _canonical_json_fragment(value: Any, path: str) -> str:
    if value is None:
        return "null"
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        return str(value)
    if isinstance(value, Decimal):
        return _canonical_decimal(value)
    if type(value) is float:
        raise _error(
            "HGR-MIGRATION-JSON-VALUE",
            f"{path}: floating-point values are forbidden in canonical JSON",
        )
    if type(value) is str:
        return _canonical_string(value)
    if type(value) is list:
        rendered = ",".join(
            _canonical_json_fragment(item, f"{path}[{index}]")
            for index, item in enumerate(value)
        )
        return f"[{rendered}]"
    if type(value) is dict:
        for key in value:
            if type(key) is not str:
                raise _error(
                    "HGR-MIGRATION-JSON-VALUE",
                    f"{path}: canonical JSON object keys must be strings",
                )
        members = []
        for key in sorted(value, key=lambda item: item.encode("utf-8")):
            members.append(
                _canonical_string(key)
                + ":"
                + _canonical_json_fragment(value[key], f"{path}.{key}")
            )
        return "{" + ",".join(members) + "}"
    raise _error(
        "HGR-MIGRATION-JSON-VALUE",
        f"{path}: {type(value).__name__} is not a canonical JSON value",
    )


def canonical_json_text(value: Any) -> str:
    """Render tag-``0x36`` canonical JSON per the exact ratified rules.

    This is the dedicated dataset-stream serializer of decision D2: ALL
    control characters are escaped as lowercase ``\\u00xx`` (never ``\\n``
    style short escapes).  Record digests deliberately do NOT use it — see
    :func:`family_canonical_json_text`.
    """

    return _canonical_json_fragment(value, "$")


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return canonical_json_text(value).encode("utf-8")
    except UnicodeEncodeError as exc:
        raise _error(
            "HGR-MIGRATION-JSON-VALUE",
            f"canonical JSON is not encodable UTF-8: {exc}",
        ) from exc


def _validate_family_json(value: Any, path: str) -> None:
    if value is None or type(value) in (bool, int, str):
        return
    if type(value) is float:
        raise _error(
            "HGR-MIGRATION-JSON-VALUE",
            f"{path}: floating-point values are forbidden in canonical JSON",
        )
    if type(value) is list:
        for index, item in enumerate(value):
            _validate_family_json(item, f"{path}[{index}]")
        return
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise _error(
                    "HGR-MIGRATION-JSON-VALUE",
                    f"{path}: canonical JSON object keys must be strings",
                )
            _validate_family_json(item, f"{path}.{key}")
        return
    raise _error(
        "HGR-MIGRATION-JSON-VALUE",
        f"{path}: {type(value).__name__} is not a canonical JSON value",
    )


def family_canonical_json_text(value: Any) -> str:
    """Render the shipped ``xfactory-canonical-json-v1`` family profile.

    Byte-identical to SQL ``xfactory_runtime_v2.canonical_json`` and to the
    family's ``semantics.authority.canonical_record_digest`` encoding.  Used
    for every US3 record digest and the staging document (decision D2).
    """

    _validate_family_json(value, "$")
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def family_canonical_json_bytes(value: Any) -> bytes:
    try:
        return family_canonical_json_text(value).encode("utf-8")
    except UnicodeEncodeError as exc:
        raise _error(
            "HGR-MIGRATION-JSON-VALUE",
            f"canonical JSON is not encodable UTF-8: {exc}",
        ) from exc


def record_digest(record: Mapping[str, Any], *, omit_field: str | None) -> str:
    """Digest one closed record, omitting only its own named digest field.

    Uses the shipped family canonical-JSON profile so PostgreSQL's
    ``canonical_record_digest`` recomputes the identical digest.
    """

    if not isinstance(record, Mapping):
        raise _error("HGR-MIGRATION-JSON-VALUE", "record must be a mapping")
    payload = {
        key: value
        for key, value in record.items()
        if omit_field is None or key != omit_field
    }
    return "sha256:" + hashlib.sha256(family_canonical_json_bytes(payload)).hexdigest()


def mapping_payload_digest(payload: Mapping[str, Any]) -> str:
    return record_digest(payload, omit_field="mapping_payload_digest")


def authority_envelope_digest(envelope: Mapping[str, Any]) -> str:
    return record_digest(envelope, omit_field="authority_envelope_digest")


# ---------------------------------------------------------------------------
# Shared field validators
# ---------------------------------------------------------------------------


def _require_mapping(value: Any, code: str, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise _error(code, f"{label} must be a mapping")
    return value


def _require_closed(
    value: Mapping[str, Any], fields: tuple[str, ...], code: str, label: str
) -> None:
    missing = [field for field in fields if field not in value]
    if missing:
        raise _error(code, f"{label} is missing required fields {missing}")
    unknown = [field for field in value if field not in fields]
    if unknown:
        raise _error(code, f"{label} carries unknown fields {unknown}")


def _require_text(value: Any, code: str, label: str, *, maximum: int = 512) -> str:
    if type(value) is not str or not value or len(value) > maximum:
        raise _error(code, f"{label} must be a non-empty string of at most {maximum}")
    for character in value:
        if ord(character) < 0x20 or ord(character) == 0x7F:
            raise _error(code, f"{label} must not contain control characters")
    return value


def _require_canonical_id(value: Any, code: str, label: str) -> str:
    if type(value) is not str or not _CANONICAL_ID.fullmatch(value):
        raise _error(code, f"{label} must be a canonical identifier")
    return value


def _require_digest(value: Any, code: str, label: str) -> str:
    if type(value) is not str or not _SHA256_DIGEST.fullmatch(value):
        raise _error(code, f"{label} must match sha256:<64 lowercase hex>")
    return value


def _require_int(value: Any, code: str, label: str, *, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise _error(code, f"{label} must be an integer of at least {minimum}")
    return value


def _reject_floats(value: Any, code: str, path: str = "$") -> None:
    if type(value) is float:
        raise _error(code, f"{path}: floating-point values are forbidden")
    if type(value) is list:
        for index, item in enumerate(value):
            _reject_floats(item, code, f"{path}[{index}]")
    elif isinstance(value, Mapping):
        for key, item in value.items():
            _reject_floats(item, code, f"{path}.{key}")


def _reject_control_characters(value: Any, path: str = "$") -> None:
    """Reject U+0000–U+001F in every string of a payload/envelope (D2).

    The rejection makes the short-escape deviation of the shipped family
    canonical-JSON profile unreachable: on every accepted record the family
    profile and the ratified rules produce identical bytes.
    """

    if type(value) is str:
        for character in value:
            if ord(character) < 0x20:
                raise _error(
                    "HGR-MIGRATION-CONTROL-CHARACTER",
                    f"{path}: control character U+{ord(character):04X} is"
                    " forbidden in payload and envelope strings",
                )
    elif type(value) is list:
        for index, item in enumerate(value):
            _reject_control_characters(item, f"{path}[{index}]")
    elif isinstance(value, Mapping):
        for key, item in value.items():
            if type(key) is str:
                _reject_control_characters(key, f"{path}.{key}")
            _reject_control_characters(item, f"{path}.{key}")


_NEUTRAL_TOKEN = re.compile(r"^[a-z][a-z0-9._-]{0,127}$")


def _require_neutral_token(value: Any, code: str, label: str) -> str:
    if type(value) is not str or not _NEUTRAL_TOKEN.fullmatch(value):
        raise _error(code, f"{label} must be a neutral token")
    return value


# ---------------------------------------------------------------------------
# Dataset description validation
# ---------------------------------------------------------------------------


def _validate_column(column: Any, path: str) -> Mapping[str, Any]:
    record = _require_mapping(column, "HGR-MIGRATION-DATASET-COLUMN", path)
    _require_closed(
        record,
        ("name", "normalized_type", "nullable", "primary_key_position"),
        "HGR-MIGRATION-DATASET-COLUMN",
        path,
    )
    _require_text(record["name"], "HGR-MIGRATION-DATASET-COLUMN", f"{path}.name")
    if record["normalized_type"] not in _NORMALIZED_TYPES:
        raise _error(
            "HGR-MIGRATION-DATASET-COLUMN",
            f"{path}.normalized_type must be one of {list(_NORMALIZED_TYPES)}",
        )
    if type(record["nullable"]) is not bool:
        raise _error(
            "HGR-MIGRATION-DATASET-COLUMN", f"{path}.nullable must be a boolean"
        )
    _require_int(
        record["primary_key_position"],
        "HGR-MIGRATION-DATASET-COLUMN",
        f"{path}.primary_key_position",
    )
    return record


def _validate_table(table: Any, path: str) -> Mapping[str, Any]:
    record = _require_mapping(table, "HGR-MIGRATION-DATASET-TABLE", path)
    _require_closed(
        record,
        ("schema_name", "table_name", "columns", "rows"),
        "HGR-MIGRATION-DATASET-TABLE",
        path,
    )
    _require_text(
        record["schema_name"],
        "HGR-MIGRATION-DATASET-TABLE",
        f"{path}.schema_name",
        maximum=128,
    )
    _require_text(
        record["table_name"],
        "HGR-MIGRATION-DATASET-TABLE",
        f"{path}.table_name",
        maximum=128,
    )
    columns = record["columns"]
    if type(columns) is not list or not columns:
        raise _error(
            "HGR-MIGRATION-DATASET-TABLE", f"{path}.columns must be a non-empty list"
        )
    names: set[str] = set()
    key_positions: list[int] = []
    for index, column in enumerate(columns):
        validated = _validate_column(column, f"{path}.columns[{index}]")
        if validated["name"] in names:
            raise _error(
                "HGR-MIGRATION-DATASET-COLUMN",
                f"{path}.columns[{index}]: duplicate column name"
                f" {validated['name']!r}",
            )
        names.add(validated["name"])
        if validated["primary_key_position"] > 0:
            key_positions.append(validated["primary_key_position"])
    if sorted(key_positions) != list(range(1, len(key_positions) + 1)) or (
        not key_positions
    ):
        raise _error(
            "HGR-MIGRATION-DATASET-COLUMN",
            f"{path}: primary key positions must be exactly 1..K with K >= 1",
        )
    rows = record["rows"]
    if type(rows) is not list:
        raise _error("HGR-MIGRATION-DATASET-TABLE", f"{path}.rows must be a list")
    for row_index, row in enumerate(rows):
        row_path = f"{path}.rows[{row_index}]"
        if type(row) is not list or len(row) != len(columns):
            raise _error(
                "HGR-MIGRATION-DATASET-ROW",
                f"{row_path} must be a list with one cell per schema ordinal",
            )
        for cell_index, cell in enumerate(row):
            _validate_cell(cell, columns[cell_index], f"{row_path}[{cell_index}]")
    return record


def _validate_cell(cell: Any, column: Mapping[str, Any], path: str) -> None:
    record = _require_mapping(cell, "HGR-MIGRATION-DATASET-ROW", path)
    cell_type = record.get("type", "")
    if cell_type is None:
        _require_closed(record, ("type",), "HGR-MIGRATION-DATASET-ROW", path)
        if not column["nullable"]:
            raise _error(
                "HGR-MIGRATION-DATASET-VALUE",
                f"{path}: null cell in non-nullable column {column['name']!r}",
            )
        return
    _require_closed(record, ("type", "value"), "HGR-MIGRATION-DATASET-ROW", path)
    expected_kind = _CELL_KIND_BY_TYPE[column["normalized_type"]]
    if cell_type != expected_kind:
        raise _error(
            "HGR-MIGRATION-DATASET-VALUE",
            f"{path}: cell type {cell_type!r} does not match column"
            f" {column['name']!r} normalized type {column['normalized_type']!r}",
        )
    value = record["value"]
    if cell_type == "text":
        if type(value) is not str:
            raise _error(
                "HGR-MIGRATION-DATASET-VALUE", f"{path}: text value must be a string"
            )
    elif cell_type == "integer":
        if type(value) is not str or not _CANONICAL_INTEGER.fullmatch(value):
            raise _error(
                "HGR-MIGRATION-DATASET-VALUE",
                f"{path}: integer value must be a minimal base-10 string",
            )
        minimum, maximum = _INTEGER_RANGES[column["normalized_type"]]
        if not minimum <= int(value) <= maximum:
            raise _error(
                "HGR-MIGRATION-DATASET-VALUE",
                f"{path}: integer value out of {column['normalized_type']} range",
            )
    elif cell_type == "boolean":
        if type(value) is not bool:
            raise _error(
                "HGR-MIGRATION-DATASET-VALUE",
                f"{path}: boolean value must be true or false",
            )
    elif cell_type == "timestamp":
        if type(value) is not str or not _CANONICAL_TIMESTAMP.fullmatch(value):
            raise _error(
                "HGR-MIGRATION-DATASET-VALUE",
                f"{path}: timestamp must be UTC RFC 3339 with exactly six"
                " fractional digits and Z",
            )
        try:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError as exc:
            raise _error(
                "HGR-MIGRATION-DATASET-VALUE", f"{path}: invalid timestamp: {exc}"
            ) from exc
    elif cell_type == "binary":
        if type(value) is not str or not _LOWERCASE_HEX.fullmatch(value):
            raise _error(
                "HGR-MIGRATION-DATASET-VALUE",
                f"{path}: binary value must be even-length lowercase hex",
            )
    elif cell_type == "json":
        _reject_floats(value, "HGR-MIGRATION-DATASET-VALUE", path)
        canonical_json_bytes(value)
    else:  # pragma: no cover - closed by _CELL_KIND_BY_TYPE
        raise _error("HGR-MIGRATION-DATASET-VALUE", f"{path}: unknown cell type")


def _validate_dataset(dataset: Any) -> Mapping[str, Any]:
    record = _require_mapping(dataset, "HGR-MIGRATION-DATASET-SHAPE", "dataset")
    _require_closed(
        record,
        ("schema_version", "kind", "source_schema", "tables"),
        "HGR-MIGRATION-DATASET-SHAPE",
        "dataset",
    )
    if record["schema_version"] != 1 or type(record["schema_version"]) is not int:
        raise _error(
            "HGR-MIGRATION-DATASET-SHAPE", "dataset schema_version must be exactly 1"
        )
    if record["kind"] != DATASET_DESCRIPTION_KIND:
        raise _error(
            "HGR-MIGRATION-DATASET-SHAPE",
            f"dataset kind must be {DATASET_DESCRIPTION_KIND!r}",
        )
    source_schema = _require_text(
        record["source_schema"],
        "HGR-MIGRATION-DATASET-SHAPE",
        "dataset.source_schema",
        maximum=128,
    )
    tables = record["tables"]
    if type(tables) is not list:
        raise _error("HGR-MIGRATION-DATASET-SHAPE", "dataset.tables must be a list")
    seen: set[tuple[str, str]] = set()
    for index, table in enumerate(tables):
        validated = _validate_table(table, f"dataset.tables[{index}]")
        if validated["schema_name"] != source_schema:
            raise _error(
                "HGR-MIGRATION-DATASET-TABLE",
                f"dataset.tables[{index}].schema_name must equal"
                f" dataset.source_schema {source_schema!r}",
            )
        identity = (validated["schema_name"], validated["table_name"])
        if identity in seen:
            raise _error(
                "HGR-MIGRATION-DATASET-ORDER",
                f"duplicate table identity {identity!r}",
            )
        seen.add(identity)
    return record


# ---------------------------------------------------------------------------
# Binary framing (xfactory-v1-dataset-binary-v1)
# ---------------------------------------------------------------------------


def _frame(tag: int, payload: bytes) -> bytes:
    return bytes((tag,)) + len(payload).to_bytes(8, "big") + payload


def _value_frame(cell: Mapping[str, Any]) -> bytes:
    cell_type = cell.get("type")
    if cell_type is None:
        return _frame(_TAG_NULL, b"")
    value = cell["value"]
    if cell_type == "text":
        return _frame(_TAG_TEXT, value.encode("utf-8"))
    if cell_type == "integer":
        return _frame(_TAG_INTEGER, value.encode("ascii"))
    if cell_type == "boolean":
        return _frame(_TAG_BOOLEAN, b"\x01" if value else b"\x00")
    if cell_type == "timestamp":
        return _frame(_TAG_TIMESTAMP, value.encode("ascii"))
    if cell_type == "binary":
        return _frame(_TAG_BINARY, value.encode("ascii"))
    if cell_type == "json":
        return _frame(_TAG_JSON, canonical_json_bytes(value))
    raise _error(
        "HGR-MIGRATION-DATASET-VALUE", f"unknown value cell type {cell_type!r}"
    )


def _column_frame(ordinal: int, column: Mapping[str, Any]) -> bytes:
    payload = (
        ordinal.to_bytes(8, "big")
        + (b"\x01" if column["nullable"] else b"\x00")
        + int(column["primary_key_position"]).to_bytes(8, "big")
        + _frame(_TAG_COLUMN_NAME, column["name"].encode("utf-8"))
        + _frame(_TAG_COLUMN_TYPE, column["normalized_type"].encode("ascii"))
    )
    return _frame(_TAG_COLUMN, payload)


def _row_frame(row: list[Any], columns: list[Mapping[str, Any]]) -> tuple[bytes, bytes]:
    """Return (framed-primary-key sort key, complete row frame bytes)."""

    value_frames = [_value_frame(cell) for cell in row]
    payload = b"".join(
        _frame(_TAG_ROW_COLUMN, (index + 1).to_bytes(8, "big") + value_frames[index])
        for index in range(len(columns))
    )
    key_ordinals = sorted(
        (
            (column["primary_key_position"], index)
            for index, column in enumerate(columns)
            if column["primary_key_position"] > 0
        ),
    )
    sort_key = b"".join(value_frames[index] for _, index in key_ordinals)
    return sort_key, _frame(_TAG_ROW, payload)


def _table_frame_validated(table: Mapping[str, Any]) -> bytes:
    columns = list(table["columns"])
    payload = (
        _frame(_TAG_SCHEMA_NAME, table["schema_name"].encode("utf-8"))
        + _frame(_TAG_TABLE_NAME, table["table_name"].encode("utf-8"))
        + _frame(_TAG_COLUMN_COUNT, len(columns).to_bytes(8, "big"))
        + b"".join(
            _column_frame(index + 1, column) for index, column in enumerate(columns)
        )
        + _frame(_TAG_ROW_COUNT, len(table["rows"]).to_bytes(8, "big"))
    )
    framed_rows = [_row_frame(row, columns) for row in table["rows"]]
    seen_keys: set[bytes] = set()
    for sort_key, _ in framed_rows:
        if sort_key in seen_keys:
            raise _error(
                "HGR-MIGRATION-DATASET-ORDER",
                f"table {table['schema_name']}.{table['table_name']} contains"
                " duplicate framed primary-key bytes",
            )
        seen_keys.add(sort_key)
    payload += b"".join(frame for _, frame in sorted(framed_rows))
    return _frame(_TAG_TABLE, payload)


def table_frame(table: Mapping[str, Any]) -> bytes:
    """Return the complete ordered ``10`` frame for one table description."""

    validated = _validate_table(table, "table")
    return _table_frame_validated(validated)


def table_frame_digest(table: Mapping[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(table_frame(table)).hexdigest()


def _sorted_tables(dataset: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return sorted(
        dataset["tables"],
        key=lambda table: (
            table["schema_name"].encode("utf-8"),
            table["table_name"].encode("utf-8"),
        ),
    )


def dataset_stream(dataset: Mapping[str, Any]) -> bytes:
    """Return the complete ``xfactory-v1-dataset-binary-v1`` byte stream."""

    validated = _validate_dataset(dataset)
    return _MAGIC + b"".join(
        _table_frame_validated(table) for table in _sorted_tables(validated)
    )


def dataset_digest(dataset: Mapping[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(dataset_stream(dataset)).hexdigest()


def catalog_from_dataset(dataset: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Derive the §4.3 catalog entries in canonical table order."""

    validated = _validate_dataset(dataset)
    catalog: list[dict[str, Any]] = []
    for table in _sorted_tables(validated):
        catalog.append(
            {
                "schema_name": table["schema_name"],
                "table_name": table["table_name"],
                "columns": [
                    {
                        "ordinal": index + 1,
                        "name": column["name"],
                        "normalized_type": column["normalized_type"],
                        "nullable": column["nullable"],
                        "primary_key_position": column["primary_key_position"],
                    }
                    for index, column in enumerate(table["columns"])
                ],
            }
        )
    return catalog


def _validate_catalog(catalog: Any) -> list[Mapping[str, Any]]:
    if type(catalog) is not list or not catalog:
        raise _error(
            "HGR-MIGRATION-PAYLOAD-CATALOG", "catalog must be a non-empty list"
        )
    entries: list[Mapping[str, Any]] = []
    previous: tuple[bytes, bytes] | None = None
    for index, entry in enumerate(catalog):
        path = f"catalog[{index}]"
        record = _require_mapping(entry, "HGR-MIGRATION-PAYLOAD-CATALOG", path)
        _require_closed(
            record,
            ("schema_name", "table_name", "columns"),
            "HGR-MIGRATION-PAYLOAD-CATALOG",
            path,
        )
        _require_text(
            record["schema_name"],
            "HGR-MIGRATION-PAYLOAD-CATALOG",
            f"{path}.schema_name",
            maximum=128,
        )
        _require_text(
            record["table_name"],
            "HGR-MIGRATION-PAYLOAD-CATALOG",
            f"{path}.table_name",
            maximum=128,
        )
        columns = record["columns"]
        if type(columns) is not list or not columns:
            raise _error(
                "HGR-MIGRATION-PAYLOAD-CATALOG",
                f"{path}.columns must be a non-empty list",
            )
        names: set[str] = set()
        key_positions: list[int] = []
        for column_index, column in enumerate(columns):
            column_path = f"{path}.columns[{column_index}]"
            column_record = _require_mapping(
                column, "HGR-MIGRATION-PAYLOAD-CATALOG", column_path
            )
            _require_closed(
                column_record,
                (
                    "ordinal",
                    "name",
                    "normalized_type",
                    "nullable",
                    "primary_key_position",
                ),
                "HGR-MIGRATION-PAYLOAD-CATALOG",
                column_path,
            )
            ordinal = _require_int(
                column_record["ordinal"],
                "HGR-MIGRATION-PAYLOAD-CATALOG",
                f"{column_path}.ordinal",
                minimum=1,
            )
            if ordinal != column_index + 1:
                raise _error(
                    "HGR-MIGRATION-PAYLOAD-CATALOG",
                    f"{column_path}.ordinal must equal its 1-based position",
                )
            _require_text(
                column_record["name"],
                "HGR-MIGRATION-PAYLOAD-CATALOG",
                f"{column_path}.name",
            )
            if column_record["name"] in names:
                raise _error(
                    "HGR-MIGRATION-PAYLOAD-CATALOG",
                    f"{column_path}.name duplicates another column",
                )
            names.add(column_record["name"])
            if column_record["normalized_type"] not in _NORMALIZED_TYPES:
                raise _error(
                    "HGR-MIGRATION-PAYLOAD-CATALOG",
                    f"{column_path}.normalized_type must be one of"
                    f" {list(_NORMALIZED_TYPES)}",
                )
            if type(column_record["nullable"]) is not bool:
                raise _error(
                    "HGR-MIGRATION-PAYLOAD-CATALOG",
                    f"{column_path}.nullable must be a boolean",
                )
            position = _require_int(
                column_record["primary_key_position"],
                "HGR-MIGRATION-PAYLOAD-CATALOG",
                f"{column_path}.primary_key_position",
            )
            if position > 0:
                key_positions.append(position)
        if sorted(key_positions) != list(range(1, len(key_positions) + 1)) or (
            not key_positions
        ):
            raise _error(
                "HGR-MIGRATION-PAYLOAD-CATALOG",
                f"{path}: primary key positions must be exactly 1..K with K >= 1",
            )
        identity = (
            record["schema_name"].encode("utf-8"),
            record["table_name"].encode("utf-8"),
        )
        if previous is not None and identity <= previous:
            raise _error(
                "HGR-MIGRATION-PAYLOAD-CATALOG",
                "catalog entries must be strictly sorted by raw UTF-8"
                " (schema, table) bytes",
            )
        previous = identity
        entries.append(record)
    return entries


def catalog_digest(catalog: Any) -> str:
    """Digest the §4.3 ``xfactory-v1-catalog-v1`` catalog record."""

    entries = _validate_catalog(catalog)
    record = {
        "profile": CATALOG_PROFILE,
        "tables": [dict(entry) for entry in entries],
    }
    return record_digest(record, omit_field=None)


def table_row_counts(dataset: Mapping[str, Any]) -> dict[str, int]:
    validated = _validate_dataset(dataset)
    return {
        f"{table['schema_name']}.{table['table_name']}": len(table["rows"])
        for table in _sorted_tables(validated)
    }


def logical_boundary_id(
    *,
    source_identity: Mapping[str, Any],
    catalog: Any,
    table_row_counts: Mapping[str, Any],
    dataset_digest: str,
) -> str:
    identity = _require_mapping(
        source_identity, "HGR-MIGRATION-BOUNDARY-SHAPE", "source_identity"
    )
    _require_closed(
        identity,
        ("source_database", "source_schema"),
        "HGR-MIGRATION-BOUNDARY-SHAPE",
        "source_identity",
    )
    _require_text(
        identity["source_database"],
        "HGR-MIGRATION-BOUNDARY-SHAPE",
        "source_identity.source_database",
        maximum=128,
    )
    _require_text(
        identity["source_schema"],
        "HGR-MIGRATION-BOUNDARY-SHAPE",
        "source_identity.source_schema",
        maximum=128,
    )
    counts = _require_mapping(
        table_row_counts, "HGR-MIGRATION-BOUNDARY-SHAPE", "table_row_counts"
    )
    for key, value in counts.items():
        _require_int(
            value, "HGR-MIGRATION-BOUNDARY-SHAPE", f"table_row_counts[{key!r}]"
        )
    _require_digest(dataset_digest, "HGR-MIGRATION-BOUNDARY-SHAPE", "dataset_digest")
    boundary = {
        "profile": LOGICAL_BOUNDARY_PROFILE,
        "source_identity": dict(identity),
        "catalog_digest": catalog_digest(catalog),
        "table_row_counts": dict(counts),
        "dataset_digest": dataset_digest,
    }
    return record_digest(boundary, omit_field=None)


# ---------------------------------------------------------------------------
# Mapping payload and authority envelope validation
# ---------------------------------------------------------------------------

_PAYLOAD_FIELDS = (
    "schema_version",
    "kind",
    "migration_id",
    "installation_id",
    "source_identity",
    "source_catalog",
    "expected_table_row_counts",
    "expected_dataset_digest",
    "digest_profile",
    "subject_mappings",
    "admin_mappings",
    "single_default_mapping",
    "target_topology",
    "migration_policy",
    "mapping_payload_digest",
)

_ENVELOPE_FIELDS = (
    "schema_version",
    "kind",
    "migration_id",
    "installation_id",
    "mapping_payload_digest",
    "approver_principal_id",
    "run_migration_grant_id",
    "run_migration_grant_digest",
    "policy_ref",
    "policy_digest",
    "scope",
    "trust_anchor_id",
    "trust_anchor_digest",
    "approved_at",
    "authority_envelope_digest",
)


def _validate_subject_mappings(
    value: Any, layer_ids: set[str]
) -> list[Mapping[str, Any]]:
    if type(value) is not list:
        raise _error("HGR-MIGRATION-PAYLOAD-MAPPING", "subject_mappings must be a list")
    seen_projects: set[str] = set()
    subject_by_layer: dict[str, str] = {}
    entries: list[Mapping[str, Any]] = []
    for index, entry in enumerate(value):
        path = f"subject_mappings[{index}]"
        record = _require_mapping(entry, "HGR-MIGRATION-PAYLOAD-MAPPING", path)
        _require_closed(
            record,
            ("legacy_project", "layer_id", "customer_subject"),
            "HGR-MIGRATION-PAYLOAD-MAPPING",
            path,
        )
        project = _require_text(
            record["legacy_project"],
            "HGR-MIGRATION-PAYLOAD-MAPPING",
            f"{path}.legacy_project",
        )
        if project in seen_projects:
            raise _error(
                "HGR-MIGRATION-PAYLOAD-MAPPING",
                f"{path}: legacy project {project!r} maps to multiple layers",
            )
        seen_projects.add(project)
        layer_id = _require_canonical_id(
            record["layer_id"], "HGR-MIGRATION-PAYLOAD-MAPPING", f"{path}.layer_id"
        )
        if layer_id not in layer_ids:
            raise _error(
                "HGR-MIGRATION-PAYLOAD-MAPPING",
                f"{path}.layer_id {layer_id!r} is not a declared Customer layer",
            )
        subject = _require_mapping(
            record["customer_subject"],
            "HGR-MIGRATION-PAYLOAD-MAPPING",
            f"{path}.customer_subject",
        )
        _require_closed(
            subject,
            ("kind", "issuer", "namespace", "ref"),
            "HGR-MIGRATION-PAYLOAD-MAPPING",
            f"{path}.customer_subject",
        )
        for field in ("kind", "issuer", "namespace"):
            _require_neutral_token(
                subject[field],
                "HGR-MIGRATION-PAYLOAD-MAPPING",
                f"{path}.customer_subject.{field}",
            )
        if type(subject["ref"]) is not str or not _SUBJECT_REF.fullmatch(
            subject["ref"]
        ):
            raise _error(
                "HGR-MIGRATION-PAYLOAD-MAPPING",
                f"{path}.customer_subject.ref must match"
                " urn:xfactory:subject:<uuid>",
            )
        rendered_subject = canonical_json_text(dict(subject))
        if subject_by_layer.setdefault(layer_id, rendered_subject) != (
            rendered_subject
        ):
            raise _error(
                "HGR-MIGRATION-PAYLOAD-MAPPING",
                f"{path}: layer {layer_id!r} is bound to conflicting"
                " customer subjects",
            )
        entries.append(record)
    return entries


def _validate_admin_mappings(value: Any, layer_ids: set[str]) -> None:
    record = _require_mapping(value, "HGR-MIGRATION-PAYLOAD-MAPPING", "admin_mappings")
    _require_closed(
        record,
        ("workers", "groups", "profiles"),
        "HGR-MIGRATION-PAYLOAD-MAPPING",
        "admin_mappings",
    )
    for collection in ("workers", "groups", "profiles"):
        entries = record[collection]
        if type(entries) is not list:
            raise _error(
                "HGR-MIGRATION-PAYLOAD-MAPPING",
                f"admin_mappings.{collection} must be a list",
            )
        seen: set[str] = set()
        for index, entry in enumerate(entries):
            path = f"admin_mappings.{collection}[{index}]"
            mapping = _require_mapping(entry, "HGR-MIGRATION-PAYLOAD-MAPPING", path)
            scope_kind = mapping.get("scope_kind")
            if scope_kind == "layer":
                _require_closed(
                    mapping,
                    ("source_pk", "scope_kind", "layer_id"),
                    "HGR-MIGRATION-PAYLOAD-MAPPING",
                    path,
                )
                layer_id = _require_canonical_id(
                    mapping["layer_id"],
                    "HGR-MIGRATION-PAYLOAD-MAPPING",
                    f"{path}.layer_id",
                )
                if layer_id not in layer_ids:
                    raise _error(
                        "HGR-MIGRATION-PAYLOAD-MAPPING",
                        f"{path}.layer_id {layer_id!r} is not a declared layer",
                    )
            elif scope_kind == "installation_admin":
                _require_closed(
                    mapping,
                    ("source_pk", "scope_kind"),
                    "HGR-MIGRATION-PAYLOAD-MAPPING",
                    path,
                )
            else:
                raise _error(
                    "HGR-MIGRATION-PAYLOAD-MAPPING",
                    f"{path}.scope_kind must be 'layer' or 'installation_admin'",
                )
            source_pk = mapping["source_pk"]
            if type(source_pk) is not str:
                raise _error(
                    "HGR-MIGRATION-PAYLOAD-MAPPING",
                    f"{path}.source_pk must be a canonical JSON array string",
                )
            try:
                parsed = json.loads(source_pk)
            except ValueError as exc:
                raise _error(
                    "HGR-MIGRATION-PAYLOAD-MAPPING",
                    f"{path}.source_pk is not JSON: {exc}",
                ) from exc
            if (
                type(parsed) is not list
                or not parsed
                or any(type(item) is not str for item in parsed)
                or canonical_json_text(parsed) != source_pk
            ):
                raise _error(
                    "HGR-MIGRATION-PAYLOAD-MAPPING",
                    f"{path}.source_pk must be the canonical JSON array of the"
                    " primary-key text values",
                )
            if source_pk in seen:
                raise _error(
                    "HGR-MIGRATION-PAYLOAD-MAPPING",
                    f"{path}.source_pk duplicates another {collection} mapping",
                )
            seen.add(source_pk)


def _validate_single_default_mapping(value: Any, projects: set[str]) -> None:
    if value is None:
        return
    record = _require_mapping(
        value, "HGR-MIGRATION-PAYLOAD-MAPPING", "single_default_mapping"
    )
    if type(record.get("enabled")) is not bool:
        raise _error(
            "HGR-MIGRATION-PAYLOAD-MAPPING",
            "single_default_mapping.enabled must be a boolean",
        )
    if record["enabled"]:
        _require_closed(
            record,
            ("enabled", "legacy_project"),
            "HGR-MIGRATION-PAYLOAD-MAPPING",
            "single_default_mapping",
        )
        project = _require_text(
            record["legacy_project"],
            "HGR-MIGRATION-PAYLOAD-MAPPING",
            "single_default_mapping.legacy_project",
        )
        if project not in projects:
            raise _error(
                "HGR-MIGRATION-PAYLOAD-MAPPING",
                "single_default_mapping.legacy_project must be a mapped"
                " legacy project",
            )
    else:
        _require_closed(
            record,
            ("enabled",),
            "HGR-MIGRATION-PAYLOAD-MAPPING",
            "single_default_mapping",
        )


def _validate_target_topology(value: Any, installation_id: str) -> set[str]:
    record = _require_mapping(
        value, "HGR-MIGRATION-PAYLOAD-TOPOLOGY", "target_topology"
    )
    _require_closed(
        record,
        (
            "installation_id",
            "stack_id",
            "client_layer_id",
            "domain_layer_id",
            "customer_layer_ids",
        ),
        "HGR-MIGRATION-PAYLOAD-TOPOLOGY",
        "target_topology",
    )
    if record["installation_id"] != installation_id:
        raise _error(
            "HGR-MIGRATION-PAYLOAD-TOPOLOGY",
            "target_topology.installation_id must equal the payload" " installation_id",
        )
    for field in ("installation_id", "stack_id", "client_layer_id", "domain_layer_id"):
        _require_canonical_id(
            record[field],
            "HGR-MIGRATION-PAYLOAD-TOPOLOGY",
            f"target_topology.{field}",
        )
    customer_layer_ids = record["customer_layer_ids"]
    if type(customer_layer_ids) is not list or not customer_layer_ids:
        raise _error(
            "HGR-MIGRATION-PAYLOAD-TOPOLOGY",
            "target_topology.customer_layer_ids must be a non-empty list",
        )
    for index, layer_id in enumerate(customer_layer_ids):
        _require_canonical_id(
            layer_id,
            "HGR-MIGRATION-PAYLOAD-TOPOLOGY",
            f"target_topology.customer_layer_ids[{index}]",
        )
    all_layers = [
        record["client_layer_id"],
        record["domain_layer_id"],
        *customer_layer_ids,
    ]
    if len(set(all_layers)) != len(all_layers):
        raise _error(
            "HGR-MIGRATION-PAYLOAD-TOPOLOGY",
            "target_topology layer identifiers must be pairwise distinct",
        )
    return set(all_layers)


def validate_mapping_payload(payload: Any) -> None:
    """Validate the closed detached mapping payload; raise on any violation."""

    record = _require_mapping(payload, "HGR-MIGRATION-PAYLOAD-SHAPE", "payload")
    _reject_floats(record, "HGR-MIGRATION-PAYLOAD-SHAPE", "payload")
    _reject_control_characters(record, "payload")
    _require_closed(record, _PAYLOAD_FIELDS, "HGR-MIGRATION-PAYLOAD-SHAPE", "payload")
    if type(record["schema_version"]) is not int or record["schema_version"] != 1:
        raise _error(
            "HGR-MIGRATION-PAYLOAD-FIELD", "payload schema_version must be exactly 1"
        )
    if record["kind"] != MAPPING_PAYLOAD_KIND:
        raise _error(
            "HGR-MIGRATION-PAYLOAD-FIELD",
            f"payload kind must be {MAPPING_PAYLOAD_KIND!r}",
        )
    _require_canonical_id(
        record["migration_id"], "HGR-MIGRATION-PAYLOAD-FIELD", "payload.migration_id"
    )
    installation_id = _require_canonical_id(
        record["installation_id"],
        "HGR-MIGRATION-PAYLOAD-FIELD",
        "payload.installation_id",
    )
    identity = _require_mapping(
        record["source_identity"], "HGR-MIGRATION-PAYLOAD-FIELD", "source_identity"
    )
    _require_closed(
        identity,
        ("source_database", "source_schema"),
        "HGR-MIGRATION-PAYLOAD-FIELD",
        "payload.source_identity",
    )
    _require_text(
        identity["source_database"],
        "HGR-MIGRATION-PAYLOAD-FIELD",
        "payload.source_identity.source_database",
        maximum=128,
    )
    source_schema = _require_text(
        identity["source_schema"],
        "HGR-MIGRATION-PAYLOAD-FIELD",
        "payload.source_identity.source_schema",
        maximum=128,
    )
    catalog = _validate_catalog(record["source_catalog"])
    observed_tables = [entry["table_name"] for entry in catalog]
    if observed_tables != list(CANONICAL_V1_TABLES):
        raise _error(
            "HGR-MIGRATION-PAYLOAD-CATALOG",
            "source_catalog must contain exactly the twelve canonical v1"
            " tables in raw UTF-8 (schema, table) order",
        )
    for entry in catalog:
        if entry["schema_name"] != source_schema:
            raise _error(
                "HGR-MIGRATION-PAYLOAD-CATALOG",
                "source_catalog schema_name must equal"
                " source_identity.source_schema",
            )
    counts = _require_mapping(
        record["expected_table_row_counts"],
        "HGR-MIGRATION-PAYLOAD-COUNTS",
        "expected_table_row_counts",
    )
    expected_keys = {
        f"{entry['schema_name']}.{entry['table_name']}" for entry in catalog
    }
    if set(counts) != expected_keys:
        raise _error(
            "HGR-MIGRATION-PAYLOAD-COUNTS",
            "expected_table_row_counts keys must be exactly the twelve"
            " <schema>.<table> catalog identities",
        )
    for key, value in counts.items():
        _require_int(
            value,
            "HGR-MIGRATION-PAYLOAD-COUNTS",
            f"expected_table_row_counts[{key!r}]",
        )
    _require_digest(
        record["expected_dataset_digest"],
        "HGR-MIGRATION-PAYLOAD-FIELD",
        "payload.expected_dataset_digest",
    )
    if record["digest_profile"] != DATASET_PROFILE:
        raise _error(
            "HGR-MIGRATION-PAYLOAD-FIELD",
            f"payload.digest_profile must be {DATASET_PROFILE!r}",
        )
    declared_layers = _validate_target_topology(
        record["target_topology"], installation_id
    )
    customer_layers = declared_layers - {
        record["target_topology"]["client_layer_id"],
        record["target_topology"]["domain_layer_id"],
    }
    subject_entries = _validate_subject_mappings(
        record["subject_mappings"], customer_layers
    )
    _validate_admin_mappings(record["admin_mappings"], declared_layers)
    _validate_single_default_mapping(
        record["single_default_mapping"],
        {entry["legacy_project"] for entry in subject_entries},
    )
    policy = _require_mapping(
        record["migration_policy"], "HGR-MIGRATION-PAYLOAD-FIELD", "migration_policy"
    )
    _require_closed(
        policy,
        ("policy_ref", "policy_digest"),
        "HGR-MIGRATION-PAYLOAD-FIELD",
        "payload.migration_policy",
    )
    _require_text(
        policy["policy_ref"],
        "HGR-MIGRATION-PAYLOAD-FIELD",
        "payload.migration_policy.policy_ref",
    )
    _require_digest(
        policy["policy_digest"],
        "HGR-MIGRATION-PAYLOAD-FIELD",
        "payload.migration_policy.policy_digest",
    )
    declared = _require_digest(
        record["mapping_payload_digest"],
        "HGR-MIGRATION-PAYLOAD-DIGEST",
        "payload.mapping_payload_digest",
    )
    recomputed = mapping_payload_digest(record)
    if declared != recomputed:
        raise _error(
            "HGR-MIGRATION-PAYLOAD-DIGEST",
            "payload.mapping_payload_digest does not match the recomputed"
            f" detached payload digest {recomputed}",
        )


def validate_authority_envelope(envelope: Any, *, payload: Any) -> None:
    """Validate the detached authority envelope against its exact payload."""

    validate_mapping_payload(payload)
    record = _require_mapping(envelope, "HGR-MIGRATION-ENVELOPE-SHAPE", "envelope")
    _reject_floats(record, "HGR-MIGRATION-ENVELOPE-SHAPE", "envelope")
    _reject_control_characters(record, "envelope")
    _require_closed(
        record, _ENVELOPE_FIELDS, "HGR-MIGRATION-ENVELOPE-SHAPE", "envelope"
    )
    if type(record["schema_version"]) is not int or record["schema_version"] != 1:
        raise _error(
            "HGR-MIGRATION-ENVELOPE-FIELD",
            "envelope schema_version must be exactly 1",
        )
    if record["kind"] != AUTHORITY_ENVELOPE_KIND:
        raise _error(
            "HGR-MIGRATION-ENVELOPE-FIELD",
            f"envelope kind must be {AUTHORITY_ENVELOPE_KIND!r}",
        )
    for field in ("migration_id", "installation_id"):
        _require_canonical_id(
            record[field], "HGR-MIGRATION-ENVELOPE-FIELD", f"envelope.{field}"
        )
        if record[field] != payload[field]:
            raise _error(
                "HGR-MIGRATION-ENVELOPE-BINDING",
                f"envelope.{field} must equal the payload {field}",
            )
    declared_payload_digest = _require_digest(
        record["mapping_payload_digest"],
        "HGR-MIGRATION-ENVELOPE-BINDING",
        "envelope.mapping_payload_digest",
    )
    if declared_payload_digest != mapping_payload_digest(payload):
        raise _error(
            "HGR-MIGRATION-ENVELOPE-BINDING",
            "envelope.mapping_payload_digest does not bind the detached"
            " payload digest",
        )
    for field in ("approver_principal_id", "run_migration_grant_id", "trust_anchor_id"):
        _require_canonical_id(
            record[field], "HGR-MIGRATION-ENVELOPE-FIELD", f"envelope.{field}"
        )
    for field in ("run_migration_grant_digest", "policy_digest", "trust_anchor_digest"):
        _require_digest(
            record[field], "HGR-MIGRATION-ENVELOPE-FIELD", f"envelope.{field}"
        )
    _require_text(
        record["policy_ref"], "HGR-MIGRATION-ENVELOPE-FIELD", "envelope.policy_ref"
    )
    scope = _require_mapping(
        record["scope"], "HGR-MIGRATION-ENVELOPE-FIELD", "envelope.scope"
    )
    _require_closed(
        scope, ("installation_id",), "HGR-MIGRATION-ENVELOPE-FIELD", "envelope.scope"
    )
    if scope["installation_id"] != record["installation_id"]:
        raise _error(
            "HGR-MIGRATION-ENVELOPE-BINDING",
            "envelope.scope.installation_id must equal the envelope" " installation_id",
        )
    if type(record["approved_at"]) is not str or not _RFC3339_TIMESTAMP.fullmatch(
        record["approved_at"]
    ):
        raise _error(
            "HGR-MIGRATION-ENVELOPE-FIELD",
            "envelope.approved_at must be an RFC 3339 timestamp",
        )
    declared = _require_digest(
        record["authority_envelope_digest"],
        "HGR-MIGRATION-ENVELOPE-DIGEST",
        "envelope.authority_envelope_digest",
    )
    recomputed = authority_envelope_digest(record)
    if declared != recomputed:
        raise _error(
            "HGR-MIGRATION-ENVELOPE-DIGEST",
            "envelope.authority_envelope_digest does not match the recomputed"
            f" detached envelope digest {recomputed}",
        )


def build_staging_document(payload: Any, envelope: Any) -> str:
    """Validate both records and return the canonical staging JSON text.

    The staging document is rendered with the shipped family profile so the
    SQL staging path recomputes byte-identical digests (decision D2); the
    control-character rejection inside both validators keeps that profile
    byte-identical to the ratified rules for every accepted document.
    """

    validate_mapping_payload(payload)
    validate_authority_envelope(envelope, payload=payload)
    document = {
        "schema_version": 1,
        "kind": STAGING_DOCUMENT_KIND,
        "payload": payload,
        "authority_envelope": envelope,
    }
    return family_canonical_json_text(document)


# ---------------------------------------------------------------------------
# Strict file loaders
# ---------------------------------------------------------------------------


def _load_strict_yaml(path: Path | str) -> Any:
    try:
        document = load_yaml_document(path)
    except YamlLoadError as exc:
        raise _error("HGR-MIGRATION-YAML", str(exc)) from exc
    _reject_floats(document, "HGR-MIGRATION-FLOAT")
    return document


def load_dataset_description(path: Path | str) -> dict[str, Any]:
    """Load and fully validate one dataset-description YAML document."""

    document = _load_strict_yaml(path)
    validated = _validate_dataset(document)
    return dict(validated)


def load_golden_vectors(path: Path | str) -> list[dict[str, Any]]:
    """Load and validate the frozen golden-vector suite."""

    document = _load_strict_yaml(path)
    record = _require_mapping(document, "HGR-MIGRATION-VECTORS-SHAPE", "vectors file")
    _require_closed(
        record,
        ("schema_version", "kind", "vectors"),
        "HGR-MIGRATION-VECTORS-SHAPE",
        "vectors file",
    )
    if type(record["schema_version"]) is not int or record["schema_version"] != 1:
        raise _error(
            "HGR-MIGRATION-VECTORS-SHAPE",
            "vectors schema_version must be exactly 1",
        )
    if record["kind"] != GOLDEN_VECTORS_KIND:
        raise _error(
            "HGR-MIGRATION-VECTORS-SHAPE",
            f"vectors kind must be {GOLDEN_VECTORS_KIND!r}",
        )
    vectors = record["vectors"]
    if type(vectors) is not list or not vectors:
        raise _error("HGR-MIGRATION-VECTORS-SHAPE", "vectors must be a non-empty list")
    seen_ids: set[str] = set()
    validated: list[dict[str, Any]] = []
    required_fields = (
        "vector_id",
        "dataset",
        "expected_stream_sha256",
        "expected_table_frame_digests",
    )
    known_fields = required_fields + ("expected_stream_hex",)
    for index, vector in enumerate(vectors):
        path_label = f"vectors[{index}]"
        entry = _require_mapping(vector, "HGR-MIGRATION-VECTORS-SHAPE", path_label)
        missing = [name for name in required_fields if name not in entry]
        if missing:
            raise _error(
                "HGR-MIGRATION-VECTORS-SHAPE",
                f"{path_label} is missing required fields {missing}",
            )
        unknown = [name for name in entry if name not in known_fields]
        if unknown:
            raise _error(
                "HGR-MIGRATION-VECTORS-SHAPE",
                f"{path_label} carries unknown fields {unknown}",
            )
        vector_id = _require_text(
            entry["vector_id"],
            "HGR-MIGRATION-VECTORS-SHAPE",
            f"{path_label}.vector_id",
        )
        if vector_id in seen_ids:
            raise _error(
                "HGR-MIGRATION-VECTORS-SHAPE",
                f"{path_label}: duplicate vector_id {vector_id!r}",
            )
        seen_ids.add(vector_id)
        dataset = _validate_dataset(entry["dataset"])
        declared_sha = _require_digest(
            entry["expected_stream_sha256"],
            "HGR-MIGRATION-VECTORS-SHAPE",
            f"{path_label}.expected_stream_sha256",
        )
        if "expected_stream_hex" in entry:
            hex_text = entry["expected_stream_hex"]
            if type(hex_text) is not str or not _LOWERCASE_HEX.fullmatch(hex_text):
                raise _error(
                    "HGR-MIGRATION-VECTORS-SHAPE",
                    f"{path_label}.expected_stream_hex must be even-length"
                    " lowercase hex",
                )
            hex_sha = "sha256:" + hashlib.sha256(bytes.fromhex(hex_text)).hexdigest()
            if hex_sha != declared_sha:
                raise _error(
                    "HGR-MIGRATION-VECTORS-SHAPE",
                    f"{path_label}: expected_stream_hex hashes to {hex_sha},"
                    " not the declared expected_stream_sha256",
                )
        digests = _require_mapping(
            entry["expected_table_frame_digests"],
            "HGR-MIGRATION-VECTORS-SHAPE",
            f"{path_label}.expected_table_frame_digests",
        )
        expected_keys = {
            f"{table['schema_name']}.{table['table_name']}"
            for table in dataset["tables"]
        }
        if set(digests) != expected_keys:
            raise _error(
                "HGR-MIGRATION-VECTORS-SHAPE",
                f"{path_label}.expected_table_frame_digests keys must exactly"
                " cover the dataset tables",
            )
        for key, value in digests.items():
            _require_digest(
                value,
                "HGR-MIGRATION-VECTORS-SHAPE",
                f"{path_label}.expected_table_frame_digests[{key!r}]",
            )
        validated.append(dict(entry))
    return validated
