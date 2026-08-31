from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

_collected: list[str] = []
_started: list[str] = []
_reports: list[dict[str, str | bool]] = []


def pytest_configure(config: pytest.Config) -> None:
    del config
    _collected.clear()
    _started.clear()
    _reports.clear()
    if not os.environ.get("HERMES_RUNTIME_PYTEST_REPORT"):
        raise pytest.UsageError("HERMES_RUNTIME_PYTEST_REPORT is required")


def pytest_collection_finish(session: pytest.Session) -> None:
    _collected.extend(item.nodeid for item in session.items)


def pytest_runtest_logstart(nodeid: str, location: tuple[str, int | None, str]) -> None:
    del location
    _started.append(nodeid)


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    _reports.append(
        {
            "node_id": report.nodeid,
            "phase": report.when,
            "outcome": report.outcome,
            "wasxfail": hasattr(report, "wasxfail"),
        }
    )


def pytest_sessionfinish(session: pytest.Session, exitstatus: int | pytest.ExitCode) -> None:
    del session, exitstatus
    path = Path(os.environ["HERMES_RUNTIME_PYTEST_REPORT"])
    payload = {
        "collected_node_ids": sorted(_collected),
        "started_node_ids": sorted(_started),
        "reports": sorted(
            _reports,
            key=lambda report: (str(report["node_id"]), str(report["phase"])),
        ),
    }
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)
