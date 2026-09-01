from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from scripts.hermes_runtime_validation.pytest_inventory import (
    EvidenceTestNodes,
    collect_evidence_test_nodes,
)

RELATIVE_TEST = Path("tests/hermes_runtime_contracts/test_evidence.py")


def write_test(root: Path, source: str) -> str:
    path = root / RELATIVE_TEST
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return RELATIVE_TEST.as_posix()


def collect(root: Path, node_id: str) -> EvidenceTestNodes:
    register: Mapping[str, object] = {
        "entries": [{"test_node_ids": [node_id]}]
    }
    return collect_evidence_test_nodes(root, register)
