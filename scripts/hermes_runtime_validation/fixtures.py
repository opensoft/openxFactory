"""Self-describing fixture index validation and expectation evaluation."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Iterable, Mapping, Sequence

from .loader import YamlLoadError, load_yaml_document
from .pytest_inventory import collect_static_pytest_nodes

_CODE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")
_POSTGRES_IMAGE = re.compile(r"^postgres@sha256:[0-9a-f]{64}$")
_POSTGRES_EVIDENCE_KIND = "HermesRuntimePostgresEvidence"
_POSTGRES_IMAGE_LOCK = Path("tests/hermes_runtime_contracts/postgres/images.lock.yaml")
_POSTGRES_MATRIX_PROFILE = "xfactory-postgres-matrix-v1"
_POSTGRES_NODE_PROFILE = "xfactory-pytest-nodeids-v1"
_POSTGRES_SOURCE_PROFILE = "xfactory-postgres-source-inputs-v1"
_POSTGRES_SUITE_ID = "hermes-runtime-postgres"


def _finding(code: str, message: str, *, case_id: str = "", path: str = "") -> dict:
    return {
        "code": code,
        "severity": "error",
        "case_id": case_id,
        "path": path,
        "message": message,
    }


def _canonical_time(value: object) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset().total_seconds() == 0


def _normalized_fixture_path(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    candidate = PurePosixPath(value)
    if candidate.is_absolute() or ".." in candidate.parts or "." in candidate.parts:
        return None
    normalized = candidate.as_posix()
    return normalized if normalized == value else None


def _case_map(index: Mapping[str, object]) -> dict[str, Mapping[str, object]]:
    result: dict[str, Mapping[str, object]] = {}
    for case in index.get("cases", []) or []:
        if isinstance(case, Mapping) and isinstance(case.get("case_id"), str):
            result.setdefault(str(case["case_id"]), case)
    return result


def _canonical_digest(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def database_matrix_identity(case: Mapping[str, object]) -> dict[str, str]:
    """Return the content identity for one indexed PostgreSQL matrix."""

    database = case.get("database")
    if not isinstance(database, Mapping):
        raise ValueError("database metadata is required")
    governed_database = {
        str(key): value for key, value in database.items() if key != "result_refs"
    }
    payload = {
        "case_id": case.get("case_id"),
        "requirement_ids": case.get("requirement_ids"),
        "scenario_ids": case.get("scenario_ids"),
        "database": governed_database,
    }
    return {
        "profile": _POSTGRES_MATRIX_PROFILE,
        "case_id": str(case.get("case_id", "")),
        "digest": _canonical_digest(payload),
    }


def repository_source_identity(
    repository_root: Path, case: Mapping[str, object]
) -> dict[str, object]:
    """Bind evidence to canonical content of the indexed PostgreSQL inputs.

    The identity deliberately does not depend on Git state.  It therefore
    survives committing the result record and validates identically in a clean
    clone, while any change to an indexed test, seed, assertion, or authoritative
    matrix metadata invalidates the prior evidence.
    """

    database = case.get("database")
    if not isinstance(database, Mapping):
        raise ValueError("database metadata is required")
    members: list[dict[str, str]] = []
    seen: set[str] = set()
    for field in (
        "source_paths",
        "test_modules",
        "seed_scripts",
        "assertion_scripts",
    ):
        paths = database.get(field)
        if not isinstance(paths, list) or not paths:
            raise ValueError(f"database.{field} must index at least one source input")
        for raw_path in paths:
            normalized = _normalized_fixture_path(raw_path)
            if normalized is None:
                raise ValueError(f"database.{field} contains an invalid source path")
            if normalized in seen:
                raise ValueError(
                    f"database source input is indexed twice: {normalized}"
                )
            seen.add(normalized)
            candidate = repository_root / normalized
            if not candidate.is_file() or candidate.is_symlink():
                raise ValueError(f"database source input is unavailable: {normalized}")
            members.append(
                {
                    "path": normalized,
                    "digest": "sha256:"
                    + hashlib.sha256(candidate.read_bytes()).hexdigest(),
                }
            )
    members.sort(key=lambda member: member["path"].encode("utf-8"))
    payload = {
        "profile": _POSTGRES_SOURCE_PROFILE,
        "matrix": database_matrix_identity(case),
        "members": members,
    }
    return {
        "identity_kind": "canonical_content",
        "profile": _POSTGRES_SOURCE_PROFILE,
        "member_count": len(members),
        "digest": _canonical_digest(payload),
    }


def collect_database_test_count(
    repository_root: Path,
    database: Mapping[str, object],
    major: int,
) -> int:
    """Collect the exact indexed PostgreSQL suite count without running it."""

    return len(collect_database_test_nodes(repository_root, database, major))


def collect_database_test_nodes(
    repository_root: Path,
    database: Mapping[str, object],
    major: int,
) -> tuple[str, ...]:
    """Return the exact statically proved node IDs selected for one major."""

    modules = database.get("test_modules")
    if not isinstance(modules, list) or not modules:
        raise ValueError("indexed PostgreSQL test modules are required")
    prefix = str(major)
    expected = tuple(
        node_id
        for node_id in collect_static_pytest_nodes(
            repository_root, tuple(str(module) for module in modules)
        )
        if (
            (parameter := node_id.rpartition("[")[2].removesuffix("]")) == prefix
            or parameter.startswith(prefix + "-")
            or not any(
                parameter == candidate or parameter.startswith(candidate + "-")
                for candidate in ("15", "16")
            )
        )
    )
    if not expected:
        raise ValueError("indexed PostgreSQL node inventory is empty")
    return expected


def database_test_suite(
    repository_root: Path,
    database: Mapping[str, object],
    major: int,
) -> dict[str, object]:
    """Return the canonical exact-node suite identity for one major."""

    node_ids = collect_database_test_nodes(repository_root, database, major)
    payload = {
        "profile": _POSTGRES_NODE_PROFILE,
        "major": major,
        "node_ids": list(node_ids),
    }
    return {
        "id": _POSTGRES_SUITE_ID,
        "test_count": len(node_ids),
        "node_profile": _POSTGRES_NODE_PROFILE,
        "node_digest": _canonical_digest(payload),
    }


def _database_result_findings(
    result: object,
    *,
    case_id: str,
    path: str,
    major: int,
    expected_outcome: str,
    expected_image: str,
    expected_source: Mapping[str, object],
    expected_matrix: Mapping[str, str],
    expected_suite: Mapping[str, object],
) -> list[dict]:
    findings: list[dict] = []
    if not isinstance(result, Mapping):
        return [
            _finding(
                "HGR-FIXTURE-DATABASE-RESULT-SHAPE",
                "database result must be a closed JSON object",
                case_id=case_id,
                path=path,
            )
        ]
    expected_fields = {
        "schema_version",
        "kind",
        "major",
        "outcome",
        "image",
        "source_identity",
        "suite",
        "matrix",
    }
    if set(result) != expected_fields:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-RESULT-SHAPE",
                f"result fields must be exactly {sorted(expected_fields)}",
                case_id=case_id,
                path=path,
            )
        )
    if (
        result.get("schema_version") != 1
        or result.get("kind") != _POSTGRES_EVIDENCE_KIND
    ):
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-RESULT-IDENTITY",
                "result requires schema_version 1 and canonical evidence kind",
                case_id=case_id,
                path=path,
            )
        )
    if result.get("major") != major:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-RESULT-MAJOR",
                f"result must bind PostgreSQL major {major}",
                case_id=case_id,
                path=path,
            )
        )
    if result.get("outcome") != expected_outcome or expected_outcome != "pass":
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-RESULT-OUTCOME",
                "indexed database acceptance requires an exact pass outcome",
                case_id=case_id,
                path=path,
            )
        )
    if result.get("image") != expected_image:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-RESULT-IMAGE",
                "result image must exactly match the selected major's image lock",
                case_id=case_id,
                path=path,
            )
        )
    if result.get("source_identity") != expected_source:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-RESULT-SOURCE",
                "result source identity is stale or does not match the indexed PostgreSQL inputs",
                case_id=case_id,
                path=path,
            )
        )
    if result.get("suite") != expected_suite:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-RESULT-SUITE",
                "result suite identity and executed test count must exactly match collection",
                case_id=case_id,
                path=path,
            )
        )
    if result.get("matrix") != expected_matrix:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-RESULT-MATRIX",
                "result matrix identity does not match indexed authoritative metadata",
                case_id=case_id,
                path=path,
            )
        )
    return findings


def _database_case_findings(
    case: Mapping[str, object],
    *,
    case_id: str,
    repository_root: Path,
) -> list[dict]:
    findings: list[dict] = []
    database = case.get("database")
    if not isinstance(database, Mapping):
        return [
            _finding(
                "HGR-FIXTURE-DATABASE-METADATA-REQUIRED",
                "database cases require database metadata",
                case_id=case_id,
                path="database",
            )
        ]

    expected_fields = {
        "engine",
        "supported_majors",
        "source_paths",
        "test_modules",
        "seed_scripts",
        "assertion_scripts",
        "row_expectations",
        "digest_expectations",
        "authoritative_deltas",
        "result_refs",
    }
    missing = expected_fields - database.keys()
    unknown = database.keys() - expected_fields
    if missing:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-METADATA-MISSING",
                f"database metadata is missing {sorted(missing)}",
                case_id=case_id,
                path="database",
            )
        )
    if unknown:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-METADATA-UNKNOWN",
                f"database metadata has unknown fields {sorted(unknown)}",
                case_id=case_id,
                path="database",
            )
        )
    if database.get("engine") != "postgresql":
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-ENGINE",
                "database engine must be postgresql",
                case_id=case_id,
                path="database.engine",
            )
        )

    majors = database.get("supported_majors")
    if (
        not isinstance(majors, list)
        or not majors
        or any(type(major) is not int or major not in {15, 16} for major in majors)
        or len(majors) != len(set(majors))
        or majors != sorted(majors)
    ):
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-MAJORS",
                "supported majors must be a unique sorted subset of [15, 16]",
                case_id=case_id,
                path="database.supported_majors",
            )
        )
        majors = []

    path_fields = {
        "source_paths": None,
        "test_modules": ".py",
        "seed_scripts": ".sql",
        "assertion_scripts": ".sql",
    }
    indexed_source_paths: dict[str, str] = {}
    for field, suffix in path_fields.items():
        values = database.get(field)
        if not isinstance(values, list) or not values:
            findings.append(
                _finding(
                    "HGR-FIXTURE-DATABASE-PATHS-REQUIRED",
                    f"{field} must be a non-empty list",
                    case_id=case_id,
                    path=f"database.{field}",
                )
            )
            continue
        for position, value in enumerate(values):
            normalized = _normalized_fixture_path(value)
            path = f"database.{field}[{position}]"
            if normalized is None or (
                suffix is not None and not normalized.endswith(suffix)
            ):
                findings.append(
                    _finding(
                        "HGR-FIXTURE-DATABASE-PATH-INVALID",
                        "normalized repository-relative regular-file path required"
                        + (f" with suffix {suffix}" if suffix else ""),
                        case_id=case_id,
                        path=path,
                    )
                )
                continue
            prior_field = indexed_source_paths.get(normalized)
            if prior_field is not None:
                findings.append(
                    _finding(
                        "HGR-FIXTURE-DATABASE-PATH-DUPLICATE",
                        f"database source path is already indexed by {prior_field}: {normalized}",
                        case_id=case_id,
                        path=path,
                    )
                )
                continue
            indexed_source_paths[normalized] = field
            candidate = repository_root / normalized
            if not candidate.is_file() or candidate.is_symlink():
                findings.append(
                    _finding(
                        "HGR-FIXTURE-DATABASE-PATH-UNAVAILABLE",
                        f"database input is not an indexed regular file: {normalized}",
                        case_id=case_id,
                        path=path,
                    )
                )

    for field in ("row_expectations", "digest_expectations"):
        value = database.get(field)
        if not isinstance(value, Mapping) or not value:
            findings.append(
                _finding(
                    "HGR-FIXTURE-DATABASE-EXPECTATION-REQUIRED",
                    f"{field} must be a non-empty mapping",
                    case_id=case_id,
                    path=f"database.{field}",
                )
            )
    deltas = database.get("authoritative_deltas")
    if (
        not isinstance(deltas, list)
        or not deltas
        or any(not isinstance(delta, str) or not delta for delta in deltas)
    ):
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-DELTAS-REQUIRED",
                "authoritative_deltas must be a non-empty string list",
                case_id=case_id,
                path="database.authoritative_deltas",
            )
        )

    locked_images: dict[int, str] = {}
    lock_path = repository_root / _POSTGRES_IMAGE_LOCK
    try:
        lock = load_yaml_document(lock_path)
    except YamlLoadError as error:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-IMAGE-LOCK",
                str(error),
                case_id=case_id,
                path=_POSTGRES_IMAGE_LOCK.as_posix(),
            )
        )
        lock = None
    if isinstance(lock, Mapping):
        images = lock.get("images")
        if (
            lock.get("schema_version") != 1
            or lock.get("kind") != "HermesRuntimePostgresImageLock"
            or not isinstance(images, Mapping)
        ):
            findings.append(
                _finding(
                    "HGR-FIXTURE-DATABASE-IMAGE-LOCK",
                    "canonical PostgreSQL image lock shape is required",
                    case_id=case_id,
                    path=_POSTGRES_IMAGE_LOCK.as_posix(),
                )
            )
        else:
            for locked_major in majors:
                entry = images.get(str(locked_major))
                image = (
                    entry.get("resolved_image") if isinstance(entry, Mapping) else None
                )
                if not isinstance(image, str) or not _POSTGRES_IMAGE.fullmatch(image):
                    findings.append(
                        _finding(
                            "HGR-FIXTURE-DATABASE-IMAGE-LOCK",
                            f"major {locked_major} lacks one canonical digest pin",
                            case_id=case_id,
                            path=_POSTGRES_IMAGE_LOCK.as_posix(),
                        )
                    )
                else:
                    locked_images[locked_major] = image
    elif lock is not None:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-IMAGE-LOCK",
                "canonical PostgreSQL image lock must be an object",
                case_id=case_id,
                path=_POSTGRES_IMAGE_LOCK.as_posix(),
            )
        )

    try:
        expected_source = repository_source_identity(repository_root, case)
    except ValueError as error:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-RESULT-SOURCE",
                str(error),
                case_id=case_id,
                path="database.result_refs",
            )
        )
        expected_source = None
    try:
        expected_matrix = database_matrix_identity(case)
    except (TypeError, ValueError) as error:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-RESULT-MATRIX",
                str(error),
                case_id=case_id,
                path="database",
            )
        )
        expected_matrix = None

    refs = database.get("result_refs")
    seen_ref_majors: set[int] = set()
    collected_suites: dict[int, Mapping[str, object]] = {}
    if not isinstance(refs, list) or not refs:
        findings.append(
            _finding(
                "HGR-FIXTURE-DATABASE-RESULTS-REQUIRED",
                "one result reference per supported major is required",
                case_id=case_id,
                path="database.result_refs",
            )
        )
    else:
        for position, ref in enumerate(refs):
            path = f"database.result_refs[{position}]"
            if not isinstance(ref, Mapping) or set(ref) != {
                "major",
                "path",
                "expected_outcome",
            }:
                findings.append(
                    _finding(
                        "HGR-FIXTURE-DATABASE-RESULT-INVALID",
                        "result reference requires only major, path, and expected_outcome",
                        case_id=case_id,
                        path=path,
                    )
                )
                continue
            major = ref.get("major")
            normalized = _normalized_fixture_path(ref.get("path"))
            if (
                type(major) is not int
                or major in seen_ref_majors
                or major not in majors
                or normalized is None
                or not normalized.endswith(".json")
                or ref.get("expected_outcome") != "pass"
            ):
                findings.append(
                    _finding(
                        "HGR-FIXTURE-DATABASE-RESULT-INVALID",
                        "result must uniquely bind a supported major to a passing JSON record",
                        case_id=case_id,
                        path=path,
                    )
                )
                continue
            seen_ref_majors.add(major)
            candidate = repository_root / normalized
            if not candidate.is_file() or candidate.is_symlink():
                findings.append(
                    _finding(
                        "HGR-FIXTURE-DATABASE-RESULT-UNAVAILABLE",
                        f"database result is unavailable: {normalized}",
                        case_id=case_id,
                        path=path,
                    )
                )
                continue
            try:
                result_document = load_yaml_document(candidate)
            except YamlLoadError as error:
                findings.append(
                    _finding(
                        "HGR-FIXTURE-DATABASE-RESULT-DOCUMENT",
                        str(error),
                        case_id=case_id,
                        path=path,
                    )
                )
                continue
            if major not in collected_suites:
                try:
                    collected_suites[major] = database_test_suite(
                        repository_root, database, major
                    )
                except ValueError as error:
                    findings.append(
                        _finding(
                            "HGR-FIXTURE-DATABASE-SUITE-COLLECTION",
                            str(error),
                            case_id=case_id,
                            path=path,
                        )
                    )
                    continue
            expected_image = locked_images.get(major)
            if (
                expected_image is None
                or expected_source is None
                or expected_matrix is None
            ):
                continue
            findings.extend(
                _database_result_findings(
                    result_document,
                    case_id=case_id,
                    path=path,
                    major=major,
                    expected_outcome=str(ref.get("expected_outcome", "")),
                    expected_image=expected_image,
                    expected_source=expected_source,
                    expected_matrix=expected_matrix,
                    expected_suite=collected_suites[major],
                )
            )
        if seen_ref_majors != set(majors):
            findings.append(
                _finding(
                    "HGR-FIXTURE-DATABASE-RESULT-COVERAGE",
                    "result references must cover every supported major exactly once",
                    case_id=case_id,
                    path="database.result_refs",
                )
            )
    return findings


def validate_index(
    index: Mapping[str, object],
    *,
    fixture_root: Path,
    repository_root: Path | None = None,
) -> list[dict]:
    """Return deterministic findings for a portable fixture index."""

    findings: list[dict] = []
    cases = index.get("cases", []) if isinstance(index, Mapping) else []
    if not isinstance(cases, list):
        return [
            _finding("HGR-FIXTURE-CASES-TYPE", "cases must be a list", path="cases")
        ]

    repo_root = (
        repository_root.resolve()
        if repository_root is not None
        else fixture_root.resolve().parents[2]
    )
    case_ids: set[str] = set()
    paths: dict[str, str] = {}
    dependencies: dict[str, tuple[str, ...]] = {}
    indexed_documents: list[tuple[str, str, Path, Mapping[str, object]]] = []

    for position, case in enumerate(cases):
        if not isinstance(case, Mapping):
            findings.append(
                _finding(
                    "HGR-FIXTURE-CASE-TYPE",
                    "fixture case must be an object",
                    path=f"cases[{position}]",
                )
            )
            continue
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            findings.append(
                _finding(
                    "HGR-FIXTURE-CASE-ID-REQUIRED",
                    "case_id must be a non-empty string",
                    path=f"cases[{position}].case_id",
                )
            )
            continue
        if case_id in case_ids:
            findings.append(
                _finding(
                    "HGR-FIXTURE-CASE-ID-DUPLICATE",
                    f"duplicate case_id {case_id}",
                    case_id=case_id,
                    path="case_id",
                )
            )
        case_ids.add(case_id)

        raw_dependencies = case.get("depends_on", []) or []
        if isinstance(raw_dependencies, list) and all(
            isinstance(item, str) for item in raw_dependencies
        ):
            dependencies[case_id] = tuple(raw_dependencies)
        else:
            findings.append(
                _finding(
                    "HGR-FIXTURE-DEPENDENCY-TYPE",
                    "depends_on must contain case IDs",
                    case_id=case_id,
                    path="depends_on",
                )
            )
            dependencies[case_id] = ()

        inputs = case.get("inputs", []) or []
        if not isinstance(inputs, list):
            inputs = []
            findings.append(
                _finding(
                    "HGR-FIXTURE-INPUTS-TYPE",
                    "inputs must be a list",
                    case_id=case_id,
                    path="inputs",
                )
            )
        for raw_path in inputs:
            fixture_path = _normalized_fixture_path(raw_path)
            if fixture_path is None:
                findings.append(
                    _finding(
                        "HGR-FIXTURE-PATH-INVALID",
                        f"invalid fixture path {raw_path!r}",
                        case_id=case_id,
                        path="inputs",
                    )
                )
                continue
            if fixture_path in paths:
                findings.append(
                    _finding(
                        "HGR-FIXTURE-PATH-DUPLICATE",
                        f"{fixture_path} is also owned by {paths[fixture_path]}",
                        case_id=case_id,
                        path=fixture_path,
                    )
                )
            else:
                paths[fixture_path] = case_id
            resolved = fixture_root / fixture_path
            if not resolved.is_file() or resolved.is_symlink():
                findings.append(
                    _finding(
                        "HGR-FIXTURE-PATH-UNAVAILABLE",
                        f"fixture is not an indexed regular file: {fixture_path}",
                        case_id=case_id,
                        path=fixture_path,
                    )
                )
            elif resolved.suffix in {".yaml", ".yml"}:
                try:
                    fixture_document = load_yaml_document(resolved)
                except YamlLoadError as error:
                    findings.append(
                        _finding(
                            "HGR-FIXTURE-DOCUMENT-INVALID",
                            str(error),
                            case_id=case_id,
                            path=fixture_path,
                        )
                    )
                else:
                    if isinstance(fixture_document, Mapping):
                        indexed_documents.append(
                            (case_id, fixture_path, resolved, fixture_document)
                        )

        if case.get("phase") == "semantic":
            evaluation_time = case.get("evaluation_time")
            if evaluation_time is None:
                findings.append(
                    _finding(
                        "HGR-FIXTURE-EVALUATION-TIME-REQUIRED",
                        "semantic cases require a fixed UTC evaluation_time",
                        case_id=case_id,
                        path="evaluation_time",
                    )
                )
            elif not _canonical_time(evaluation_time):
                findings.append(
                    _finding(
                        "HGR-FIXTURE-EVALUATION-TIME-INVALID",
                        "evaluation_time must be an RFC 3339 UTC timestamp",
                        case_id=case_id,
                        path="evaluation_time",
                    )
                )
        elif case.get("phase") == "database":
            findings.extend(
                _database_case_findings(
                    case,
                    case_id=case_id,
                    repository_root=repo_root,
                )
            )

        expected = case.get("expected", {}) or {}
        if not isinstance(expected, Mapping):
            expected = {}
        outcome = expected.get("outcome")
        primary = expected.get("primary_finding_code")
        if outcome == "fail" and (
            not isinstance(primary, str) or not _CODE.fullmatch(primary)
        ):
            findings.append(
                _finding(
                    "HGR-FIXTURE-PRIMARY-CODE-REQUIRED",
                    "negative cases require one stable primary finding code",
                    case_id=case_id,
                    path="expected.primary_finding_code",
                )
            )

    for case_id, fixture_path, _, fixture_document in indexed_documents:
        case = next(
            item
            for item in cases
            if isinstance(item, Mapping) and item.get("case_id") == case_id
        )
        for field in (
            "case_id",
            "phase",
            "class",
            "requirement_ids",
            "scenario_ids",
            "evaluation_time",
        ):
            if field in fixture_document and fixture_document[field] != case.get(field):
                findings.append(
                    _finding(
                        "HGR-FIXTURE-SELF-DESCRIPTION-MISMATCH",
                        f"fixture {field} does not match its index entry",
                        case_id=case_id,
                        path=f"{fixture_path}.{field}",
                    )
                )
    known_ids = set(dependencies)
    dependency_missing = False
    for case_id, required in dependencies.items():
        for dependency in required:
            if dependency not in known_ids:
                dependency_missing = True
                findings.append(
                    _finding(
                        "HGR-FIXTURE-DEPENDENCY-MISSING",
                        f"unknown dependency {dependency}",
                        case_id=case_id,
                        path="depends_on",
                    )
                )

    if not dependency_missing:
        try:
            dependency_order(index)
        except ValueError as error:
            findings.append(
                _finding("HGR-FIXTURE-DEPENDENCY-CYCLE", str(error), path="depends_on")
            )

    return sorted(
        findings,
        key=lambda item: (
            str(item["case_id"]),
            str(item["path"]),
            str(item["code"]),
            str(item["message"]),
        ),
    )


def dependency_order(
    index: Mapping[str, object],
    *,
    selected_case_ids: Sequence[str] | None = None,
) -> tuple[str, ...]:
    """Return dependencies before dependents using deterministic bytewise IDs."""

    cases = _case_map(index)
    requested = (
        tuple(selected_case_ids) if selected_case_ids is not None else tuple(cases)
    )
    ordered: list[str] = []
    permanent: set[str] = set()
    visiting: set[str] = set()

    def visit(case_id: str) -> None:
        if case_id in permanent:
            return
        if case_id in visiting:
            raise ValueError(f"fixture dependency cycle includes {case_id}")
        if case_id not in cases:
            raise ValueError(f"unknown fixture dependency {case_id}")
        visiting.add(case_id)
        dependencies = cases[case_id].get("depends_on", []) or []
        for dependency in sorted(str(item) for item in dependencies):
            visit(dependency)
        visiting.remove(case_id)
        permanent.add(case_id)
        ordered.append(case_id)

    for case_id in sorted(requested):
        visit(case_id)
    return tuple(ordered)


def evaluate_expected_findings(
    case: Mapping[str, object],
    findings: Iterable[Mapping[str, object]],
) -> dict[str, object]:
    """Evaluate a case without allowing an unrelated failure to satisfy it."""

    actual_codes = tuple(sorted(str(item["code"]) for item in findings))
    expected = case.get("expected", {}) or {}
    if not isinstance(expected, Mapping):
        expected = {}
    outcome = expected.get("outcome")
    primary = expected.get("primary_finding_code")
    allowed_secondary = tuple(
        str(code) for code in (expected.get("allowed_secondary_codes", []) or [])
    )
    missing_primary = outcome == "fail" and primary not in actual_codes
    allowed = {str(primary), *allowed_secondary} if primary is not None else set()
    unexpected = tuple(code for code in actual_codes if code not in allowed)
    passed = (
        not actual_codes
        if outcome == "pass"
        else not missing_primary and not unexpected
    )
    return {
        "passed": passed,
        "expected_outcome": outcome,
        "primary_code": primary,
        "actual_codes": actual_codes,
        "missing_primary": missing_primary,
        "unexpected_codes": unexpected,
    }
