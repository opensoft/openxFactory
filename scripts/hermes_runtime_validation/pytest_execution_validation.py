from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from collections.abc import Mapping
from pathlib import Path

type JsonValue = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]


class ExecutionReportError(ValueError):
    pass


def validate_execution_report(
    expected_path: Path,
    report_path: Path,
    junit_path: Path,
) -> int:
    expected = _string_list(_load_json(expected_path), "expected node IDs")
    if not expected or expected != sorted(expected) or len(expected) != len(set(expected)):
        raise ExecutionReportError("expected node IDs must be nonempty, unique, and sorted")
    report = _mapping(_load_json(report_path), "execution report")
    if set(report) != {"collected_node_ids", "started_node_ids", "reports"}:
        raise ExecutionReportError("execution report fields are not canonical")
    collected = _string_list(report["collected_node_ids"], "collected node IDs")
    started = _string_list(report["started_node_ids"], "started node IDs")
    if collected != expected or started != expected:
        raise ExecutionReportError("executed pytest node IDs differ from static inventory")
    if len(collected) != len(set(collected)) or len(started) != len(set(started)):
        raise ExecutionReportError("execution report contains duplicate node IDs")
    _validate_phase_reports(report["reports"], expected)
    _validate_junit(junit_path, len(expected))
    return len(expected)


def _load_json(path: Path) -> JsonValue:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ExecutionReportError(f"invalid JSON evidence: {path}") from error


def _mapping(value: JsonValue, label: str) -> Mapping[str, JsonValue]:
    if not isinstance(value, Mapping) or not all(
        isinstance(key, str) for key in value
    ):
        raise ExecutionReportError(f"{label} must be an object")
    return value


def _string_list(value: JsonValue, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ExecutionReportError(f"{label} must be a string array")
    return value


def _validate_phase_reports(value: JsonValue, expected: list[str]) -> None:
    if not isinstance(value, list):
        raise ExecutionReportError("execution reports must be an array")
    actual: dict[tuple[str, str], tuple[str, bool]] = {}
    for item in value:
        report = _mapping(item, "phase report")
        if set(report) != {"node_id", "phase", "outcome", "wasxfail"}:
            raise ExecutionReportError("phase report fields are not canonical")
        node_id = report["node_id"]
        phase = report["phase"]
        outcome = report["outcome"]
        wasxfail = report["wasxfail"]
        if (
            not isinstance(node_id, str)
            or not isinstance(phase, str)
            or not isinstance(outcome, str)
            or not isinstance(wasxfail, bool)
        ):
            raise ExecutionReportError("phase report values have invalid types")
        key = (node_id, phase)
        if key in actual:
            raise ExecutionReportError("execution report contains duplicate phases")
        actual[key] = (outcome, wasxfail)
    required = {
        (node_id, phase)
        for node_id in expected
        for phase in ("setup", "call", "teardown")
    }
    if set(actual) != required or any(
        outcome != "passed" or wasxfail for outcome, wasxfail in actual.values()
    ):
        raise ExecutionReportError(
            "every expected node must pass every phase without xfail"
        )


def _validate_junit(path: Path, expected_count: int) -> None:
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as error:
        raise ExecutionReportError("pytest JUnit evidence is invalid") from error
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    totals = {
        field: int(
            root.attrib.get(
                field,
                sum(int(item.attrib.get(field, 0)) for item in suites),
            )
        )
        for field in ("tests", "failures", "errors", "skipped")
    }
    if totals != {
        "tests": expected_count,
        "failures": 0,
        "errors": 0,
        "skipped": 0,
    }:
        raise ExecutionReportError(
            "pytest JUnit totals differ from exact node evidence"
        )


def main(arguments: list[str]) -> int:
    if len(arguments) != 3:
        return 2
    try:
        count = validate_execution_report(*(Path(argument) for argument in arguments))
    except ExecutionReportError as error:
        print(str(error), file=sys.stderr)
        return 1
    print(count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
