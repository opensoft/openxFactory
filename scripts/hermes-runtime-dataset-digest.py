#!/usr/bin/env python3
"""Deterministic ``xfactory-v1-dataset-binary-v1`` dataset digest CLI."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

# ``python scripts/hermes-runtime-dataset-digest.py`` otherwise places only the
# scripts directory on sys.path.  Add the repository root so this thin
# entrypoint reuses the importable validation package.
_ENTRYPOINT_REPO = Path(__file__).resolve().parents[1]
if str(_ENTRYPOINT_REPO) not in sys.path:
    sys.path.insert(0, str(_ENTRYPOINT_REPO))

from scripts.hermes_runtime_validation.migration import (  # noqa: E402
    DATASET_PROFILE,
    MigrationContractError,
    dataset_stream,
    load_dataset_description,
    table_frame_digest,
)
from scripts.hermes_runtime_validation.migration import (  # noqa: E402
    table_row_counts as dataset_table_row_counts,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--emit-stream", type=Path, dest="emit_stream")
    return parser


def _render(
    findings: list[dict[str, str]],
    *,
    as_json: bool,
    exit_code: int,
    selection: dict[str, Any],
    summary: dict[str, Any],
) -> None:
    findings.sort(
        key=lambda item: (
            item["case_id"],
            item["path"],
            item["code"],
            item["message"],
        )
    )
    if as_json:
        payload = {
            "exit_code": exit_code,
            "findings": findings,
            "mode": "dataset-digest",
            "selection": selection,
            "status": "pass" if exit_code == 0 else "error",
            "summary": summary,
        }
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        return
    if not findings:
        print(f"dataset_digest {summary['dataset_digest']}")
        for identity in sorted(summary["per_table_digests"]):
            print(
                f"table {identity} rows={summary['table_row_counts'][identity]} "
                f"digest={summary['per_table_digests'][identity]}"
            )
        print(
            f"Hermes v1 dataset digest: pass ({summary['table_count']} tables, "
            f"{summary['row_count_total']} rows, profile {DATASET_PROFILE})"
        )
        return
    for finding in findings:
        case = f" case={finding['case_id']}" if finding["case_id"] else ""
        path = f" path={finding['path']}" if finding["path"] else ""
        print(
            f"{finding['code']} {finding['severity']}{case}{path}: "
            f"{finding['message']}"
        )


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    selection = {"dataset": str(arguments.dataset)}
    if not arguments.dataset.is_file():
        print(
            f"hermes-runtime-dataset-digest: dataset file unavailable: "
            f"{arguments.dataset}",
            file=sys.stderr,
        )
        return 2
    try:
        dataset = load_dataset_description(arguments.dataset)
        stream = dataset_stream(dataset)
        per_table_digests = {
            f"{table['schema_name']}.{table['table_name']}": table_frame_digest(table)
            for table in dataset["tables"]
        }
        row_counts = dataset_table_row_counts(dataset)
    except MigrationContractError as exc:
        findings = [
            {
                "code": exc.code,
                "severity": "error",
                "case_id": "",
                "path": str(arguments.dataset),
                "message": exc.message,
            }
        ]
        _render(
            findings,
            as_json=arguments.as_json,
            exit_code=1,
            selection=selection,
            summary={},
        )
        return 1
    if arguments.emit_stream is not None:
        try:
            arguments.emit_stream.write_bytes(stream)
        except OSError as exc:
            print(
                f"hermes-runtime-dataset-digest: cannot write stream: {exc}",
                file=sys.stderr,
            )
            return 2
    summary = {
        "dataset_digest": "sha256:" + hashlib.sha256(stream).hexdigest(),
        "per_table_digests": per_table_digests,
        "profile": DATASET_PROFILE,
        "row_count_total": sum(row_counts.values()),
        "stream_byte_length": len(stream),
        "table_count": len(dataset["tables"]),
        "table_row_counts": row_counts,
    }
    _render(
        [],
        as_json=arguments.as_json,
        exit_code=0,
        selection=selection,
        summary=summary,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
