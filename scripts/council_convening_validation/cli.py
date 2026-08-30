from __future__ import annotations

import argparse
import json

from .models import ContractViolation, HarnessError, Report
from .runner import execute, report_for_finding


class Arguments(argparse.Namespace):
    strict: bool = False
    case_id: str | None = None
    json: bool = False


def _emit(report: Report, json_output: bool) -> None:
    payload = report.to_json()
    if json_output:
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        return
    if not payload["findings"]:
        version = payload["contract_version"]
        case_count = len(payload["cases"])
        print(f"council-convening contract v{version}: {case_count} case(s), 0 finding(s)")
        return
    for finding in payload["findings"]:
        location = finding["path"] or finding["case_id"] or "harness"
        print(f"{finding['severity'].upper()} [{finding['code']}] {location}: {finding['message']}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the indexed council-convening conformance corpus.",
    )
    _ = parser.add_argument("--strict", action="store_true", help="Treat warnings as mismatches.")
    _ = parser.add_argument("--case", dest="case_id", help="Validate one exact case identifier.")
    _ = parser.add_argument("--json", action="store_true", help="Emit deterministic JSON.")
    arguments = parser.parse_args(namespace=Arguments())
    try:
        execution = execute(arguments.case_id, arguments.strict)
    except ContractViolation as error:
        _emit(report_for_finding(error.finding, "fail"), arguments.json)
        return 1
    except HarnessError as error:
        _emit(report_for_finding(error.finding, "error"), arguments.json)
        return 2
    _emit(execution.report, arguments.json)
    return execution.exit_code
