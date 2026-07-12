"""Self-describing fixture index validation and expectation evaluation."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Iterable, Mapping, Sequence

_CODE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")


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


def validate_index(index: Mapping[str, object], *, fixture_root: Path) -> list[dict]:
    """Return deterministic findings for a portable fixture index."""

    findings: list[dict] = []
    cases = index.get("cases", []) if isinstance(index, Mapping) else []
    if not isinstance(cases, list):
        return [_finding("HGR-FIXTURE-CASES-TYPE", "cases must be a list", path="cases")]

    case_ids: set[str] = set()
    paths: dict[str, str] = {}
    dependencies: dict[str, tuple[str, ...]] = {}

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

        expected = case.get("expected", {}) or {}
        if not isinstance(expected, Mapping):
            expected = {}
        outcome = expected.get("outcome")
        primary = expected.get("primary_finding_code")
        if outcome == "fail" and (not isinstance(primary, str) or not _CODE.fullmatch(primary)):
            findings.append(
                _finding(
                    "HGR-FIXTURE-PRIMARY-CODE-REQUIRED",
                    "negative cases require one stable primary finding code",
                    case_id=case_id,
                    path="expected.primary_finding_code",
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
    requested = tuple(selected_case_ids) if selected_case_ids is not None else tuple(cases)
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
    passed = not actual_codes if outcome == "pass" else not missing_primary and not unexpected
    return {
        "passed": passed,
        "expected_outcome": outcome,
        "primary_code": primary,
        "actual_codes": actual_codes,
        "missing_primary": missing_primary,
        "unexpected_codes": unexpected,
    }
